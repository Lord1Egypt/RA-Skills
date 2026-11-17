#!/usr/bin/env python3
"""
感知节点（PerceptionNode） - 被动能力执行器 / Tool Use 统一入口层

【行为红线 · 必读】
本模块是框架次循环"感知接口（Tool Use）"的落地，严格遵循 tool_use_spec.md
的职责边界红线：
  - 被动能力执行器：只按调用方给定参数执行能力、返回结构化契约；
    不拥有任何决策权 / 推理权 / 判断权（那些属于映射层与外环）。
  - 无自主推理：调用与否、结果如何处置，由上层决定；本层仅按预置规则
    （如确定性错误码集合、retryable 标志）机械响应。
  - 最小化自我表述：只输出结构化契约数据与 operational telemetry
    （trace_id / backend / duration 等）；不输出任何主体性 / 叙事性 / 拔高性
    措辞（禁止"我认为/我治理/我进化/核心 IP"等）。

功能（均为"执行态"能力，非决策）：
- 工具调用入口（web_search, get_weather, calculator, search_documents, toolnode）
- Trace ID 全链路追踪
- 缓存策略（执行态复用）
- 重试机制（仅确定性规则驱动）
- 性能监控
- 分页支持
- SSE 流式响应（模拟）
- 可观测性（调试模式、日志 —— 进程内执行态，不进入契约）
- 版本控制
- Token 预估
- 错误台账（内部状态，用于重试判定与可观测；错误事件上报上层，入库决策在上层）

基于：tool_use_spec.md 接口规范（2026版）
"""
__version__ = "1.0.0"


import sys
import os
import json
import argparse
import subprocess
import time
import hashlib
import uuid
import datetime
import logging
import ast
import math
from typing import Dict, List, Optional, Any, AsyncGenerator, Callable
from dataclasses import dataclass, field
from functools import lru_cache
from collections import OrderedDict
from interfaces import TraceContext, ValidationResult, create_trace_context

# 导入 toolnode 的参数 Schema（单一事实来源，供参数校验复用）
# toolnode.py 缺失时（保命场景：Rust 二进制 + Python 原型都没了）回退到 busybox_fallback.SCHEMAS，
# 保证保命模式下参数校验仍生效（Step 4）。
try:
    from toolnode import SCHEMAS as TOOLNODE_SCHEMAS
except Exception:
    try:
        from busybox_fallback import SCHEMAS as TOOLNODE_SCHEMAS
    except Exception:
        TOOLNODE_SCHEMAS = {}

# BusyBox 保命层（Step 4）：能力层缺失/崩溃时的最后兜底。纯 stdlib，内嵌进程。
try:
    import busybox_fallback
except Exception:
    busybox_fallback = None

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('perception_node')

# 确保当前目录在 sys.path 中（供同目录其他模块导入）
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 集中加载 C 扩展（c_ext_loader 按显式文件路径加载，规避命名空间包遮蔽）
try:
    from c_ext_loader import load_c_extension, PERCEPTION_NODE_SYMBOLS
    _cpn_mod, C_EXT_AVAILABLE, _cpn_detail = load_c_extension(
        "core_perception_node", required_symbols=PERCEPTION_NODE_SYMBOLS,
        runtime_probe=("generate_trace_id", (), {}))
    if C_EXT_AVAILABLE:
        core_perception_node = _cpn_mod
        c_generate_trace_id = core_perception_node.generate_trace_id
        logger.info(_cpn_detail)
    else:
        logger.warning(f"{_cpn_detail}, using pure Python implementation")
        core_perception_node = None
        c_generate_trace_id = None
except Exception as e:
    logger.warning(f"C extension not available: {e}, using pure Python implementation")
    C_EXT_AVAILABLE = False
    core_perception_node = None
    c_generate_trace_id = None

# 尝试导入错误智慧库模块
try:
    from error_wisdom_prevention import PreventionEngine, quick_pre_check
    from error_wisdom_manager import ErrorWisdomManager
    ERROR_WISDOM_AVAILABLE = True
    logger.info("Error Wisdom modules loaded successfully")
except ImportError as e:
    logger.warning(f"Error Wisdom modules not available: {e}")
    ERROR_WISDOM_AVAILABLE = False

# ==================== 工具定义 ====================

@dataclass
class ToolConfig:
    """工具配置"""
    name: str
    description: str
    version: str = "1.0.0"
    cacheable: bool = False
    cache_ttl: int = 600
    cache_key_params: List[str] = field(default_factory=list)
    streaming: bool = False
    estimated_tokens: Dict[str, Any] = field(default_factory=dict)
    deprecated: bool = False
    sunset_date: Optional[str] = None
    replacement: Optional[str] = None
    stub: bool = False  # 是否为桩（未真正实现，禁止进入主路径）


# 工具注册表
TOOL_REGISTRY: Dict[str, ToolConfig] = {
    "web_search": ToolConfig(
        name="web_search",
        description="搜索网络信息",
        version="1.0.0",
        cacheable=True,
        cache_ttl=300,
        cache_key_params=["query"],
        estimated_tokens={"input": 50, "output": {"typical": 200, "max": 1000}},
        stub=True
    ),
    "get_weather": ToolConfig(
        name="get_weather",
        description="获取指定城市的实时天气信息",
        version="1.0.0",
        cacheable=True,
        cache_ttl=600,
        cache_key_params=["location", "unit"],
        estimated_tokens={"input": 50, "output": {"typical": 100, "max": 200}},
        stub=True
    ),
    "calculator": ToolConfig(
        name="calculator",
        description="执行数学计算（四则/幂/取模 + 科学函数 sqrt/sin/cos/log/exp/pow/atan2 及常量 pi/e/tau）",
        version="1.1.0",
        cacheable=True,
        cache_ttl=3600,
        cache_key_params=["expression"],
        estimated_tokens={"input": 100, "output": {"typical": 50, "max": 100}}
    ),
    "search_documents": ToolConfig(
        name="search_documents",
        description="搜索文档数据库（支持分页）",
        version="2.1.0",
        cacheable=True,
        cache_ttl=300,
        estimated_tokens={"input": 100, "output": {"min": 200, "max": 5000, "typical": 1000}},
        stub=True
    ),
    "toolnode": ToolConfig(
        name="toolnode",
        description="统一工具节点（fs/sys/proc/exec），由 PerceptionNode 经 subprocess 路由到 toolnode.py（真实能力层）",
        version="1.0.0",
        cacheable=False,
        estimated_tokens={"input": 100, "output": {"typical": 500, "max": 4000}}
    )
}


# ==================== 辅助函数 ====================

# ==================== 安全计算（calculator 白名单求值，v2） ====================
# 与 C 扩展 tool_calculator（纯 C 白名单求值器）行为对齐：
# - 仅允许 数字字面量 / 四则 / 幂 / 取模 / 地板除 / 一元正负 / 括号
# - 函数与常量严格白名单（math 常用科学函数），任意未登记名字一律拒绝
# - 无自由 eval：AST 白名单校验 + 清空 __builtins__ 的受限命名空间
#   免疫 __import__ / ().__class__ / open / lambda 等沙箱逃逸
_CALC_AST_ALLOWED = frozenset({
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant, ast.Name, ast.Call,
    ast.Load,  # Name/Call 的上下文标记，无害
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
    ast.UAdd, ast.USub,
})

# 单/双参函数白名单（与 C 扩展 CALC_UNARY/CALC_BINARY 对齐；min/max 限定双参）
_CALC_FUNCS = frozenset({
    "fabs", "sqrt", "cbrt", "sin", "cos", "tan",
    "asin", "acos", "atan", "sinh", "cosh", "tanh",
    "asinh", "acosh", "atanh", "exp", "expm1",
    "log", "log2", "log10", "log1p",
    "floor", "ceil", "trunc",
    "degrees", "radians", "erf", "erfc", "gamma", "lgamma",
    "pow", "atan2", "hypot", "fmod", "copysign", "remainder",
})
# 非 math 模块的内置函数（C 侧为 fabs/nearbyint/fmin/fmax 对应实现；min/max 限定双参）
_CALC_FUNCS_BUILTIN = {"abs", "round", "min", "max"}
_CALC_CONSTS = frozenset({"pi", "e", "tau", "inf", "nan"})


def _safe_calc(expression: str) -> Any:
    """白名单安全求值（AST 校验 + math 受限命名空间）。

    - 数字字面量仅限 int/float（拒绝字符串/复数/布尔等非常规数值）
    - 函数调用必须是白名单内的裸名字（拒绝属性访问、下标）
    - 执行时 __builtins__ 清空，只暴露白名单函数与常量
    """
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("invalid expression")
    called = {n.func.id for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    for node in ast.walk(tree):
        if type(node) not in _CALC_AST_ALLOWED:
            raise ValueError(f"disallowed node: {type(node).__name__}")
        if isinstance(node, ast.Constant):
            v = node.value
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                raise ValueError("only numeric literals allowed")
        if isinstance(node, ast.Name):
            if node.id in _CALC_FUNCS | _CALC_FUNCS_BUILTIN and node.id not in called:
                raise ValueError(f"function must be called: {node.id}")  # 裸函数名拒绝（对齐 C 扩展）
            if node.id not in _CALC_FUNCS | _CALC_FUNCS_BUILTIN | _CALC_CONSTS:
                raise ValueError(f"unknown name: {node.id}")
        if isinstance(node, ast.Call) and not isinstance(node.func, ast.Name):
            raise ValueError("function call must be a plain name")
    ns = {name: getattr(math, name) for name in _CALC_FUNCS}
    ns.update({"abs": abs, "round": round})  # 内置 abs / round（round 为 half-even，与 C nearbyint 一致）
    ns.update({name: getattr(math, name) for name in ("pi", "e", "tau")})
    ns.update({"inf": float("inf"), "nan": float("nan")})
    # min/max 限定双参（与 C 扩展 fmin/fmax 对齐）
    ns.update({"min": lambda a, b: a if a < b else b,
               "max": lambda a, b: a if a > b else b})
    return eval(compile(tree, "<safe_calc>", "eval"), {"__builtins__": {}}, ns)


def generate_trace_id() -> str:
    """生成 Trace ID"""
    if C_EXT_AVAILABLE:
        try:
            return c_generate_trace_id()
        except Exception as e:
            logger.warning(f"Failed to generate trace ID with C extension: {e}")

    date_str = datetime.datetime.utcnow().strftime("%Y%m%d")
    uuid_str = uuid.uuid4().hex[:12]
    return f"trace_{date_str}_{uuid_str}"


def get_timestamp_iso8601() -> str:
    """获取 ISO 8601 格式的时间戳"""
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def get_cache_key(tool_name: str, params: dict, key_params: List[str]) -> str:
    """生成缓存键"""
    filtered_params = {k: v for k, v in params.items() if k in key_params}
    params_str = json.dumps(filtered_params, sort_keys=True)
    return hashlib.md5(f"{tool_name}:{params_str}".encode()).hexdigest()


# ==================== 缓存实现 ====================

class ToolCache:
    """工具结果缓存（LRU）"""

    def __init__(self, max_size: int = 1000):
        self.cache: OrderedDict[str, tuple] = OrderedDict()
        self.max_size = max_size

    def get(self, tool_name: str, params: dict, config: ToolConfig) -> Optional[dict]:
        """获取缓存结果"""
        if not config.cacheable:
            return None

        cache_key = get_cache_key(tool_name, params, config.cache_key_params)

        if cache_key in self.cache:
            result, cached_time = self.cache[cache_key]

            # 检查是否过期
            if time.time() - cached_time < config.cache_ttl:
                # 更新访问顺序
                self.cache.move_to_end(cache_key)

                # 添加缓存元数据（保留原始 trace_id）
                original_trace_id = result.get('metadata', {}).get('trace_id')
                cached_result = result.copy()
                if 'metadata' not in cached_result:
                    cached_result['metadata'] = {}
                cached_result['metadata'].update({
                    'cache': {
                        'hit': True,
                        'cached_at': datetime.datetime.fromtimestamp(cached_time).isoformat(),
                        'ttl_remaining': config.cache_ttl - (time.time() - cached_time)
                    },
                    'trace_id': original_trace_id  # 保留原始 trace_id
                })

                logger.info(f"Cache hit for {tool_name}: {cache_key}")
                return cached_result
            else:
                # 缓存过期
                del self.cache[cache_key]

        return None

    def set(self, tool_name: str, params: dict, result: dict, config: ToolConfig) -> None:
        """设置缓存结果"""
        if not config.cacheable:
            return

        cache_key = get_cache_key(tool_name, params, config.cache_key_params)

        # 检查缓存大小
        if len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)

        self.cache[cache_key] = (result, time.time())
        logger.info(f"Cached result for {tool_name}: {cache_key}")

    def clear(self) -> None:
        """清空缓存"""
        self.cache.clear()
        logger.info("Cache cleared")


# ==================== 可观测性管理器 ====================

class ObservabilityManager:
    """可观测性管理器"""

    def __init__(self):
        self.metrics = {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "retry_count": 0
        }

    def log_call(self, tool_name: str, trace_id: str, params: dict) -> None:
        """记录工具调用"""
        self.metrics["total_calls"] += 1
        logger.info(f"Tool called: {tool_name}", extra={
            "trace_id": trace_id,
            "tool_name": tool_name,
            "params": params
        })

    def log_success(self, tool_name: str, trace_id: str, execution_time_ms: float) -> None:
        """记录成功调用"""
        self.metrics["successful_calls"] += 1
        logger.info(f"Tool completed: {tool_name}", extra={
            "trace_id": trace_id,
            "tool_name": tool_name,
            "execution_time_ms": execution_time_ms
        })

    def log_error(self, tool_name: str, trace_id: str, error: Exception, retryable: bool) -> None:
        """记录错误"""
        self.metrics["failed_calls"] += 1
        logger.error(f"Tool failed: {tool_name}", extra={
            "trace_id": trace_id,
            "tool_name": tool_name,
            "error": str(error),
            "retryable": retryable
        }, exc_info=True)

    def log_failure(self, tool_name: str, trace_id: str, error_code: str, message: str) -> None:
        """记录错误契约结果（success=False 的业务失败，非抛异常路径）。

        与 log_error 共同支撑真实成功率指标——此前错误契约只入智慧库不计 failed_calls，
        致 failed_calls 恒为异常数、成功率指标失真（Step 5 Q7 发现并修正）。
        """
        self.metrics["failed_calls"] += 1
        # 注意：LogRecord 保留属性（message/name/levelname 等）不可放入 extra，否则抛 KeyError
        logger.info(f"Tool failed (contract): {tool_name} ({error_code})", extra={
            "trace_id": trace_id,
            "tool_name": tool_name,
            "error_code": error_code,
            "error_message": message,
        })

    def log_cache_hit(self, tool_name: str) -> None:
        """记录缓存命中"""
        self.metrics["cache_hits"] += 1

    def log_cache_miss(self, tool_name: str) -> None:
        """记录缓存未命中"""
        self.metrics["cache_misses"] += 1

    def log_retry(self, tool_name: str) -> None:
        """记录重试"""
        self.metrics["retry_count"] += 1
        logger.warning(f"Tool retry: {tool_name}")

    def get_metrics(self) -> dict:
        """获取指标"""
        return self.metrics.copy()


# ==================== 感知节点主类 ====================

class PerceptionNode:
    """感知节点（PerceptionNode） - 被动能力执行器 / Tool Use 统一入口层。

    严格遵循 tool_use_spec.md 职责边界红线：无自主推理、最小化自我表述。
    错误事件经 error_wisdom 接口**单向上报**给框架记录层；入库/复盘/预防等
    决策性动作由上层完成，本层不因此获得任何决策权（详见模块 docstring）。
    """

    def __init__(self, memory_dir: str = "./agi_memory"):
        self.c_ext_available = C_EXT_AVAILABLE
        self.cache = ToolCache()
        self.observability = ObservabilityManager()
        self.memory_dir = memory_dir
        
        # 初始化错误事件上报（单向依赖：本层只把错误事件上报给框架记录层，
        # 入库/复盘/预防等决策在上层完成；本层不因此改动自身行为，也不反向约束上层）
        self.prevention_engine = None
        self.error_wisdom_manager = None

        if ERROR_WISDOM_AVAILABLE:
            try:
                self.prevention_engine = PreventionEngine(memory_dir)
                self.error_wisdom_manager = ErrorWisdomManager(memory_dir)
                logger.info("Error event reporting enabled (upstream)")
            except Exception as e:
                logger.warning(f"Failed to initialize Error Wisdom: {e}")

    def call_tool(
        self,
        tool_name: str,
        params: dict,
        **options
    ) -> dict:
        """
        调用工具（统一入口）

        参数：
            tool_name: 工具名称
            params: 工具参数
            options: 可选参数
                - enable_cache: 是否启用缓存（默认 True）
                - enable_retry: 是否启用重试（默认 True）
                - debug: 调试模式（默认 False）
                - max_retries: 最大重试次数（默认 3）

        返回：
            工具执行结果
        """
        # 获取工具配置
        tool_config = TOOL_REGISTRY.get(tool_name)

        # 尽早生成 trace_id，保证所有分支（含提前返回）可追踪（Q3）
        trace_id = generate_trace_id()

        if not tool_config:
            return {
                "success": False,
                "status": "error",
                "error": {
                    "code": "TOOL_NOT_FOUND",
                    "message": f"Tool '{tool_name}' not found"
                },
                "metadata": {
                    "tool_name": tool_name,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id
                }
            }

        # 检查工具是否已废弃
        if tool_config.deprecated:
            return {
                "success": False,
                "status": "error",
                "error": {
                    "code": "TOOL_DEPRECATED",
                    "message": f"Tool '{tool_name}' is deprecated",
                    "replacement": tool_config.replacement,
                    "sunset_date": tool_config.sunset_date
                },
                "metadata": {
                    "tool_name": tool_name,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id
                }
            }

        # 检查工具是否仅为桩（未真正实现，禁止进入主路径）— Q1 质量门禁
        if tool_config.stub and not options.get('allow_stub', False):
            return {
                "success": False,
                "status": "error",
                "error": {
                    "code": "STUB_NOT_IMPLEMENTED",
                    "message": f"Tool '{tool_name}' is a stub and not implemented",
                    "replacement": "toolnode"
                },
                "metadata": {
                    "tool_name": tool_name,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id
                }
            }

        # 参数 Schema 校验（Q2：真实接线工具强制校验）
        if tool_name == "toolnode":
            verr = self._validate_toolnode_params(params)
            if verr:
                return {
                    "success": False,
                    "status": "error",
                    "error": {
                        "code": "INVALID_PARAMS",
                        "message": verr,
                        "retryable": False
                    },
                    "metadata": {
                        "tool_name": tool_name,
                        "timestamp": get_timestamp_iso8601(),
                        "trace_id": trace_id
                    }
                }

        # 记录调用
        self.observability.log_call(tool_name, trace_id, params)
        
        # ========== 新增：前置预防检查 ==========
        pre_check_result = self._pre_check(tool_name, params)
        
        # 如果前置检查发现严重错误，直接返回
        if not pre_check_result.get("pass", True):
            return {
                "success": False,
                "status": "error",
                "error": {
                    "code": "PREVENTION_CHECK_FAILED",
                    "message": "; ".join(pre_check_result.get("warnings", [])),
                    "suggestions": pre_check_result.get("suggestions", []),
                    "prevention_triggered": True
                },
                "metadata": {
                    "tool_name": tool_name,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id
                }
            }
        
        # 应用自动修正
        if pre_check_result.get("auto_fixes"):
            params = params.copy()
            params.update(pre_check_result["auto_fixes"])
            logger.info(f"Auto-fixes applied: {pre_check_result['auto_fixes']}")
        # ========== 预防检查结束 ==========

        start_time = time.time()

        try:
            # 检查缓存
            if options.get('enable_cache', True) and tool_config.cacheable:
                cached_result = self.cache.get(tool_name, params, tool_config)
                if cached_result:
                    self.observability.log_cache_hit(tool_name)
                    return cached_result
                else:
                    self.observability.log_cache_miss(tool_name)

            # 执行工具
            enable_retry = options.get('enable_retry', True)
            max_retries = options.get('max_retries', 3)

            if enable_retry:
                result = self._execute_with_retry(
                    tool_name,
                    params,
                    tool_config,
                    trace_id,
                    max_retries
                )
            else:
                result = self._execute_tool(tool_name, params, tool_config, trace_id)

            execution_time = (time.time() - start_time) * 1000

            if result.get('success'):
                self.observability.log_success(tool_name, trace_id, execution_time)

                # 添加性能数据
                if 'metadata' not in result:
                    result['metadata'] = {}
                result['metadata']['performance'] = {
                    'total_ms': execution_time
                }

                # 缓存结果
                if options.get('enable_cache', True) and tool_config.cacheable:
                    # 保存原始的 trace_id
                    original_trace_id = result.get('metadata', {}).get('trace_id')
                    self.cache.set(tool_name, params, result, tool_config)
                    # 确保返回结果包含 trace_id
                    if 'metadata' not in result:
                        result['metadata'] = {}
                    result['metadata']['trace_id'] = original_trace_id or trace_id

                # 调试信息
                if options.get('debug', False):
                    result['debug_info'] = {
                        'cache_hit': False,
                        'retry_count': result.get('retry_count', 0),
                        'execution_time_ms': execution_time,
                        'tool_config': {
                            'version': tool_config.version,
                            'cacheable': tool_config.cacheable,
                            'estimated_tokens': tool_config.estimated_tokens
                        }
                    }
            else:
                execution_time = (time.time() - start_time) * 1000
                if 'metadata' not in result:
                    result['metadata'] = {}
                result['metadata']['performance'] = {
                    'total_ms': execution_time
                }
                # Q7：错误契约（success=False 的业务失败）计入可观测性 failed_calls，
                # 支撑真实成功率指标（此前仅异常计 failed_calls，成功率失真）。
                self.observability.log_failure(
                    tool_name, trace_id,
                    (result.get("error") or {}).get("code", "UNKNOWN"),
                    (result.get("error") or {}).get("message", ""),
                )
                # Q6：真实工具失败（非客户端错误）自动入错误智慧库，闭环复盘
                if tool_name == "toolnode":
                    ecode = (result.get("error") or {}).get("code", "")
                    _client_errors = ("INVALID_PARAMS", "PATH_NOT_FOUND", "PERMISSION_DENIED",
                                      "UNKNOWN_GROUP", "UNKNOWN_OP", "BAD_PARAMS_JSON",
                                      "STUB_NOT_IMPLEMENTED")
                    if ecode and ecode not in _client_errors:
                        self._record_error_to_wisdom(
                            tool_name, params,
                            RuntimeError(f"{ecode}: {(result.get('error') or {}).get('message', '')}"),
                            trace_id
                        )

            return result

        except Exception as error:
            execution_time = (time.time() - start_time) * 1000
            
            # ========== 新增：记录错误到错误智慧库 ==========
            self._record_error_to_wisdom(tool_name, params, error, trace_id)
            # ========== 错误记录结束 ==========

            error_result = {
                "success": False,
                "status": "error",
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(error)
                },
                "metadata": {
                    "tool_name": tool_name,
                    "execution_time_ms": execution_time,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id,
                    "performance": {"total_ms": execution_time}
                }
            }

            self.observability.log_error(tool_name, trace_id, error, False)

            return error_result

    def _execute_tool(self, tool_name: str, params: dict, config: ToolConfig, trace_id: str) -> dict:
        """执行工具（基础版本）"""
        # C 扩展仅实现 calculator；其余（含 toolnode 真实能力层）走 Python 路径
        if self.c_ext_available and tool_name == "calculator":
            try:
                # 调用 C 扩展
                result = core_perception_node.call_tool(tool_name, params)
                # 确保包含 trace_id
                if 'metadata' in result and 'trace_id' not in result['metadata']:
                    result['metadata']['trace_id'] = trace_id
                return result
            except Exception as e:
                logger.warning(f"C extension failed for {tool_name}: {e}, falling back to Python")

        # Python 实现的后备方案（toolnode 经 subprocess 路由到统一工具节点）
        return self._execute_tool_python(tool_name, params, config, trace_id)

    def _execute_tool_python(self, tool_name: str, params: dict, config: ToolConfig, trace_id: str) -> dict:
        """纯 Python 实现的后备方案"""
        start_time = time.time()

        try:
            # toolnode：经 subprocess 路由到统一工具节点（真实能力层）
            if tool_name == "toolnode":
                return self._execute_toolnode(params, config, trace_id)

            if tool_name == "web_search":
                data = {
                    "query": params.get("query", ""),
                    "results": [],
                    "count": 0
                }
            elif tool_name == "get_weather":
                data = {
                    "location": params.get("location", ""),
                    "temperature": 25,
                    "condition": "sunny",
                    "unit": params.get("unit", "celsius")
                }
            elif tool_name == "calculator":
                expression = params.get("expression", "0")
                try:
                    # v2：白名单安全求值（AST 校验 + math 受限命名空间），替代裸 eval
                    result = _safe_calc(expression)
                    data = {
                        "expression": expression,
                        "result": result
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "status": "error",
                        "error": {
                            "code": "CALC_ERROR",
                            "message": str(e),
                            "retryable": False
                        },
                        "metadata": {
                            "tool_name": tool_name,
                            "timestamp": get_timestamp_iso8601(),
                            "trace_id": trace_id
                        }
                    }
            elif tool_name == "search_documents":
                # 处理分页
                limit = params.get("limit", 10)
                if limit < 1 or limit > 100:
                    return {
                        "success": False,
                        "status": "error",
                        "error": {
                            "code": "INVALID_PARAMS",
                            "message": "limit must be between 1 and 100",
                            "retryable": False
                        },
                        "metadata": {
                            "tool_name": tool_name,
                            "timestamp": get_timestamp_iso8601(),
                            "trace_id": trace_id
                        }
                    }

                cursor = params.get("cursor", "")
                data = {
                    "query": params.get("query", ""),
                    "items": [],
                    "pagination": {
                        "has_more": False,
                        "next_cursor": cursor,
                        "total_count": 0
                    }
                }
            else:
                return {
                    "success": False,
                    "status": "error",
                    "error": {
                        "code": "TOOL_NOT_FOUND",
                        "message": f"Tool '{tool_name}' not found",
                        "retryable": False
                    },
                    "metadata": {
                        "tool_name": tool_name,
                        "timestamp": get_timestamp_iso8601(),
                        "trace_id": trace_id
                    }
                }

            execution_time = (time.time() - start_time) * 1000

            return {
                "success": True,
                "status": "success",
                "data": data,
                "metadata": {
                    "tool_name": tool_name,
                    "execution_time_ms": execution_time,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id
                }
            }

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "success": False,
                "status": "error",
                "error": {
                    "code": "EXECUTION_ERROR",
                    "message": str(e),
                    "retryable": False
                },
                "metadata": {
                    "tool_name": tool_name,
                    "execution_time_ms": execution_time,
                    "timestamp": get_timestamp_iso8601(),
                    "trace_id": trace_id
                }
            }

    def _validate_toolnode_params(self, params: dict) -> Optional[str]:
        """校验 toolnode 参数（group/op + 各操作 required）。返回错误信息或 None。"""
        group = params.get("group")
        op = params.get("op")
        if not group or not op:
            return "toolnode requires 'group' and 'op'"
        schema = TOOLNODE_SCHEMAS.get(group, {}).get(op)
        if not schema:
            return f"unknown toolnode operation: {group}.{op}"
        missing = [r for r in schema.get("required", []) if r not in params]
        if missing:
            return f"toolnode {group}.{op} missing required params: {', '.join(missing)}"
        return None

    def _toolnode_binary_path(self):
        """解析 toolnode 能力层入口：优先 Rust 静态二进制（toolnode / toolnode.exe），
        不存在则回退 Python 原型 toolnode.py。返回 (path, is_rust)。

        Step 3 后主路径是 Rust 二进制（零依赖、跨平台双二进制），Python 原型保留为
        可回退的安全网——任一缺失都不致治理层失效。
        """
        ext = ".exe" if os.name == "nt" else ""
        bin_path = os.path.join(current_dir, "toolnode" + ext)
        if os.path.exists(bin_path):
            return bin_path, True
        py_path = os.path.join(current_dir, "toolnode.py")
        if os.path.exists(py_path):
            return py_path, False
        return None, False

    def _execute_toolnode(self, params: dict, config: ToolConfig, trace_id: str) -> dict:
        """经 subprocess 调用 toolnode（Rust 二进制优先，回退 Python 原型），透传 trace_id，
        解析并归一化统一契约（Q3/Q4）。

        能力层三级兜底（Step 4）：Rust 二进制(主) → Python 原型(回退) → BusyBox(保命)。
        - bin_path 为 None（Rust + Python 原型都缺）→ 直接走 BusyBox
        - subprocess spawn 失败 / 超时（OSError/TimeoutExpired）→ 能力层崩溃，走 BusyBox
        - stdout 非合法契约（非 JSON / 无 status）→ 能力层崩溃，走 BusyBox
        - 合法错误契约（exit 1 + 合法 JSON，如 COMMAND_TIMEOUT）→ **不**触发兜底，那是业务结果

        toolnode/busybox 均输出 status-based 契约；此处统一经 _normalize_toolnode_contract
        归一化为 PerceptionNode 内部 success-based 契约。
        """
        group = params["group"]
        op = params["op"]
        bin_path, is_rust = self._toolnode_binary_path()

        # —— 能力层全缺：直接保命层 ——
        if bin_path is None:
            logger.warning("[toolnode] no capability binary found, falling back to BusyBox (trace=%s)", trace_id)
            return self._busybox_fallback(group, op, params, trace_id)

        if is_rust:
            cmd = [
                bin_path, group, op,
                "--params", json.dumps(params, ensure_ascii=False),
                "--trace-id", trace_id, "--timeout", "120",
            ]
        else:
            cmd = [
                sys.executable, bin_path, group, op,
                "--params", json.dumps(params, ensure_ascii=False),
                "--trace-id", trace_id, "--timeout", "120",
            ]
        logger.info("[toolnode] using %s backend for %s.%s (trace=%s)",
                    "rust" if is_rust else "python", group, op, trace_id)

        # —— 子进程调用：spawn 失败/超时视为能力层崩溃，转保命层 ——
        try:
            proc = subprocess.run(cmd, capture_output=True, timeout=120)
        except (subprocess.TimeoutExpired, OSError) as e:
            logger.warning("[toolnode] capability layer crashed (%s: %s), falling back to BusyBox (trace=%s)",
                           type(e).__name__, e, trace_id)
            return self._busybox_fallback(group, op, params, trace_id)

        stdout = proc.stdout.decode("utf-8", errors="replace") if isinstance(proc.stdout, bytes) else (proc.stdout or "")
        stderr = proc.stderr.decode("utf-8", errors="replace") if isinstance(proc.stderr, bytes) else (proc.stderr or "")

        # toolnode 约定：成功 exit 0、失败 exit 1，但失败时仍把错误契约写进 stdout。
        # 因此先按契约解析 stdout：合法契约（含合法错误契约）直接归一化返回；
        # 仅当 stdout 非合法契约时，才视为能力层崩溃 → 转保命层（而非降级 EXECUTION_ERROR）。
        result = None
        try:
            parsed = json.loads(stdout)
            if isinstance(parsed, dict) and "status" in parsed:
                result = parsed
        except (json.JSONDecodeError, ValueError):
            pass
        if result is None:
            logger.warning("[toolnode] non-contract output from capability layer (rc=%s), falling back to BusyBox (trace=%s)",
                           proc.returncode, trace_id)
            return self._busybox_fallback(group, op, params, trace_id)

        return self._normalize_toolnode_contract(result, trace_id)

    def _busybox_fallback(self, group: str, op: str, params: dict, trace_id: str) -> dict:
        """BusyBox 保命层入口（Step 4）。纯 stdlib，内嵌于治理层进程——只要 PerceptionNode
        活即活，即使 Rust 二进制与 toolnode.py 全缺也能维持核心 fs/proc.list/sys.all/exec.run。

        返回与 toolnode 一致的统一契约，metadata.backend="busybox" 标记可观测。
        兜底层自身异常绝不裸抛（再无下一级），一律包成契约。
        """
        if busybox_fallback is None:
            # 极端情况：busybox_fallback.py 也丢了。返回明确错误，不静默。
            contract = {
                "status": "error", "data": None,
                "error": {"code": "BUSYBOX_UNAVAILABLE",
                          "message": "capability layer down and busybox_fallback module missing",
                          "retryable": False},
                "metadata": {"trace_id": trace_id, "backend": "none"},
                "trace_id": trace_id, "timestamp": get_timestamp_iso8601(),
            }
            return contract
        logger.info("[toolnode] using busybox backend for %s.%s (trace=%s)", group, op, trace_id)
        result = busybox_fallback.execute(group, op, params, trace_id)
        return self._normalize_toolnode_contract(result, trace_id)

    def _normalize_toolnode_contract(self, result: dict, trace_id: str) -> dict:
        """边界归一化：toolnode/busybox 的 status-based → PerceptionNode 内部 success-based。

        这是能力层→治理层的唯一契约边界。此前正是 'success' 键缺失被 _execute_with_retry
        误判失败，导致所有 toolnode 调用返回 EXECUTION_ERROR。
        """
        success = result.get("status") == "success"
        result["success"] = success
        if not success:
            err = result.get("error")
            if not isinstance(err, dict):
                result["error"] = {"code": "EXECUTION_ERROR", "message": str(err), "retryable": False}
        if result.get("status") is None:
            result["status"] = "success" if success else "error"

        # 防静默失败：确保链路 trace_id 与能力层回报一致（不一致则强制对齐，绝不静默丢弃）
        if result.get("trace_id") != trace_id:
            result["trace_id"] = trace_id
        if isinstance(result.get("metadata"), dict):
            result["metadata"]["trace_id"] = trace_id
        else:
            result["metadata"] = {"trace_id": trace_id}
        return result

    def _execute_with_retry(
        self,
        tool_name: str,
        params: dict,
        config: ToolConfig,
        trace_id: str,
        max_retries: int = 3
    ) -> dict:
        """执行工具（带重试）"""
        retry_count = 0
        last_error = None

        while retry_count < max_retries:
            try:
                result = self._execute_tool(tool_name, params, config, trace_id)

                # 检查是否需要重试
                if not result.get('success'):
                    error_code = result.get('error', {}).get('code')

                    # 参数/权限/确定性业务错误不重试
                    _no_retry = [
                        'INVALID_PARAMS', 'PERMISSION_DENIED', 'TOOL_NOT_FOUND',
                        'TOOL_DEPRECATED', 'EXECUTION_ERROR', 'CALC_ERROR',
                        'PATH_NOT_FOUND', 'DANGEROUS_COMMAND_BLOCKED', 'COMMAND_TIMEOUT',
                        'COMMAND_FAILED', 'BAD_PARAMS_JSON', 'UNKNOWN_GROUP', 'UNKNOWN_OP',
                        # BusyBox 保命层错误均为确定性（不支持/不可用/内部异常），不应重试（Step 4）
                        'BUSYBOX_UNSUPPORTED', 'BUSYBOX_UNAVAILABLE', 'BUSYBOX_INTERNAL_ERROR',
                    ]
                    if error_code in _no_retry:
                        return result

                    # 其他错误继续重试
                    last_error = result
                    retry_count += 1
                    self.observability.log_retry(tool_name)
                    time.sleep(2 ** retry_count)  # 指数退避
                    continue

                # 添加重试计数
                if retry_count > 0:
                    result['retry_count'] = retry_count

                return result

            except Exception as e:
                last_error = {
                    "success": False,
                    "status": "error",
                    "error": {
                        "code": "EXECUTION_ERROR",
                        "message": str(e),
                        "retryable": True
                    },
                    "metadata": {
                        "tool_name": tool_name,
                        "timestamp": get_timestamp_iso8601(),
                        "trace_id": trace_id
                    }
                }
                retry_count += 1
                self.observability.log_retry(tool_name)
                time.sleep(2 ** retry_count)  # 指数退避

        # 重试次数用尽
        return last_error

    def call_tool_with_streaming(
        self,
        tool_name: str,
        params: dict,
        **options
    ) -> AsyncGenerator:
        """
        调用工具并流式返回进度（模拟）

        参数：
            tool_name: 工具名称
            params: 工具参数
            options: 可选参数

        返回：
            异步生成器，产生 SSE 事件
        """
        import asyncio

        async def _stream():
            trace_id = generate_trace_id()

            # 推送开始事件
            yield {
                "event": "tool_progress",
                "id": f"evt_{trace_id}_start",
                "data": {
                    "progress": 0,
                    "message": f"开始执行工具: {tool_name}",
                    "metadata": {
                        "tool_name": tool_name,
                        "timestamp": get_timestamp_iso8601(),
                        "trace_id": trace_id
                    }
                }
            }

            # 模拟进度
            for i in range(0, 101, 20):
                await asyncio.sleep(0.1)
                yield {
                    "event": "tool_progress",
                    "id": f"evt_{trace_id}_progress_{i}",
                    "data": {
                        "progress": i,
                        "message": f"处理中... {i}%",
                        "metadata": {
                            "tool_name": tool_name,
                            "timestamp": get_timestamp_iso8601(),
                            "trace_id": trace_id
                        }
                    }
                }

            # 执行工具
            try:
                result = self.call_tool(tool_name, params, **options)

                # 推送成功结果
                yield {
                    "event": "tool_result",
                    "id": f"evt_{trace_id}_result",
                    "data": result
                }

            except Exception as error:
                # 推送错误事件
                yield {
                    "event": "tool_error",
                    "id": f"evt_{trace_id}_error",
                    "data": {
                        "success": False,
                        "status": "error",
                        "error": {
                            "code": "EXECUTION_ERROR",
                            "message": str(error)
                        },
                        "metadata": {
                            "tool_name": tool_name,
                            "timestamp": get_timestamp_iso8601(),
                            "trace_id": trace_id
                        }
                    }
                }

        return _stream()

    def get_metrics(self) -> dict:
        """获取可观测性指标"""
        return self.observability.get_metrics()

    def clear_cache(self) -> None:
        """清空缓存"""
        self.cache.clear()
    
    # ==================== 错误智慧库集成方法 ====================
    
    def _pre_check(self, tool_name: str, params: dict) -> dict:
        """
        前置预防检查
        
        Args:
            tool_name: 工具名称
            params: 调用参数
        
        Returns:
            检查结果 {
                "pass": bool,
                "warnings": [],
                "auto_fixes": {},
                "suggestions": []
            }
        """
        if not self.prevention_engine:
            return {"pass": True}
        
        try:
            # 获取工具schema（如果有）
            tool_schema = self._get_tool_schema(tool_name)
            
            # 执行预防检查
            result = self.prevention_engine.quick_check(tool_name, params, tool_schema)
            
            # 预防引擎对未知工具可能返回 None → 视为放行（防静默失败：勿因 None 崩溃）
            if not isinstance(result, dict):
                return {"pass": True}
            return result
        except Exception as e:
            logger.warning(f"Pre-check failed: {e}")
            return {"pass": True}
    
    def _get_tool_schema(self, tool_name: str) -> Optional[dict]:
        """
        获取工具schema
        
        Args:
            tool_name: 工具名称
        
        Returns:
            工具schema（简化版）
        """
        # 简化实现：返回基本schema
        schemas = {
            "get_weather": {
                "name": "get_weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市名称"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "温度单位"
                        }
                    },
                    "required": ["location"]
                }
            },
            "calculator": {
                "name": "calculator",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "数学表达式"
                        }
                    },
                    "required": ["expression"]
                }
            },
            "web_search": {
                "name": "web_search",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        }
                    },
                    "required": ["query"]
                }
            },
            "search_documents": {
                "name": "search_documents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "limit": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "description": "返回数量"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
        
        return schemas.get(tool_name)
    
    def _record_error_to_wisdom(
        self,
        tool_name: str,
        params: dict,
        error: Exception,
        trace_id: str
    ):
        """
        上报错误事件给框架记录层（单向）。

        注意：本层是被动能力执行器，不做"复盘/进化/决策"。此处仅把错误事件
        上报给上层 error_wisdom 接口；是否入库、如何预防，由记录层决策。
        这是红线允许的"单向依赖"，本层不因上报结果改变自身行为、也不反向
        约束上层 schema。
        """
        if not self.error_wisdom_manager:
            return
        
        try:
            # 分析错误类型（机械分类，非语义判断）
            error_type = "工具性错误"
            error_subtype = self._classify_tool_error(error)
            
            # 上报错误事件（决策在上层）
            self.error_wisdom_manager.record_error(
                error_type=error_type,
                error_subtype=error_subtype,
                error_code="EXECUTION_ERROR",
                error_description=f"工具 {tool_name} 执行失败: {str(error)}",
                root_cause=f"参数: {params}, 异常: {type(error).__name__}",
                solution="检查参数和工具状态",
                prevention_strategy="前置参数验证",
                trace_id=trace_id,
                severity="moderate",
                trigger_scenario=f"工具调用: {tool_name}"
            )
            
            logger.info(f"Error recorded to wisdom: {trace_id}")
        except Exception as e:
            logger.warning(f"Failed to record error to wisdom: {e}")
    
    def _classify_tool_error(self, error: Exception) -> str:
        """
        分类工具错误
        
        Args:
            error: 异常对象
        
        Returns:
            错误子类型
        """
        error_name = type(error).__name__
        
        # 网络错误
        if any(keyword in error_name.lower() for keyword in ['timeout', 'connection', 'network']):
            return "调用失败类"
        
        # 参数错误
        if any(keyword in error_name.lower() for keyword in ['value', 'type', 'parameter', 'argument']):
            return "参数构造类"
        
        # 默认
        return "调用失败类"


# ==================== 命令行接口 ====================

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="AGI Perception Node - Enhanced Tool Use Interface (2026)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # call 命令
    call_parser = subparsers.add_parser("call", help="Call a tool")
    call_parser.add_argument("--tool", required=True, help="Tool name")
    call_parser.add_argument("--params", required=True, help="JSON string of parameters")
    call_parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    call_parser.add_argument("--no-cache", action="store_true", help="Disable cache")
    call_parser.add_argument("--no-retry", action="store_true", help="Disable retry")

    # test 命令
    test_parser = subparsers.add_parser("test", help="Test the perception node")
    test_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # metrics 命令
    metrics_parser = subparsers.add_parser("metrics", help="Show metrics")

    args = parser.parse_args()

    if args.command == "call":
        node = PerceptionNode()
        params = json.loads(args.params)

        options = {
            "debug": args.debug,
            "enable_cache": not args.no_cache,
            "enable_retry": not args.no_retry
        }

        result = node.call_tool(args.tool, params, **options)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "test":
        node = PerceptionNode()
        print("Testing Perception Node...")
        print(f"C Extension Available: {node.c_ext_available}")

        # 测试各种工具
        tests = [
            ("web_search", {"query": "AGI"}),
            ("get_weather", {"location": "Beijing", "unit": "celsius"}),
            ("calculator", {"expression": "2 + 3 * 4"}),
            ("search_documents", {"query": "AGI", "limit": 10}),
            ("toolnode", {"group": "sys", "op": "all"}),
            ("toolnode", {"group": "fs", "op": "write", "path": os.path.join(current_dir, "_toolnode_selftest.txt"), "content": "selftest"}),
        ]

        options = {"debug": args.debug}

        for tool_name, params in tests:
            print(f"\n{'='*60}")
            print(f"Testing {tool_name}:")
            print(f"{'='*60}")
            result = node.call_tool(tool_name, params, **options)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        # 显示指标
        print(f"\n{'='*60}")
        print("Metrics:")
        print(f"{'='*60}")
        print(json.dumps(node.get_metrics(), indent=2, ensure_ascii=False))

    elif args.command == "metrics":
        node = PerceptionNode()
        print(json.dumps(node.get_metrics(), indent=2, ensure_ascii=False))

    else:
        # 如果没有提供命令，显示帮助
        parser.print_help()


if __name__ == "__main__":
    main()
