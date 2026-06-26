#!/usr/bin/env python3
"""
感知节点 - Tool Use 接口（完整版 + 错误智慧库集成）

功能：
- 工具调用（web_search, get_weather, calculator, search_documents）
- Trace ID 全链路追踪
- 缓存策略
- 重试机制
- 性能监控
- 分页支持
- SSE 流式响应（模拟）
- 可观测性（调试模式、日志）
- 版本控制
- Token 预估
- 错误智慧库集成（前置预防检查 + 错误记录）

基于：tool_use_spec.md 接口规范（2026版）
"""

import sys
import os
import json
import argparse
import time
import hashlib
import uuid
import datetime
import logging
from typing import Dict, List, Optional, Any, AsyncGenerator, Callable
from dataclasses import dataclass, field
from functools import lru_cache
from collections import OrderedDict

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('perception_node')

# 确保当前目录在 sys.path 中
current_dir = os.path.dirname(os.path.abspath(__file__))
personality_core_dir = os.path.join(current_dir, 'personality_core')
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if personality_core_dir not in sys.path:
    sys.path.insert(0, personality_core_dir)

# 尝试导入 C 扩展
try:
    import core_perception_node
    from core_perception_node import generate_trace_id as c_generate_trace_id
    C_EXT_AVAILABLE = True
    logger.info("C extension loaded successfully")
except ImportError as e:
    logger.warning(f"C extension not available: {e}, using pure Python implementation")
    C_EXT_AVAILABLE = False

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


# 工具注册表
TOOL_REGISTRY: Dict[str, ToolConfig] = {
    "web_search": ToolConfig(
        name="web_search",
        description="搜索网络信息",
        version="1.0.0",
        cacheable=True,
        cache_ttl=300,
        cache_key_params=["query"],
        estimated_tokens={"input": 50, "output": {"typical": 200, "max": 1000}}
    ),
    "get_weather": ToolConfig(
        name="get_weather",
        description="获取指定城市的实时天气信息",
        version="1.0.0",
        cacheable=True,
        cache_ttl=600,
        cache_key_params=["location", "unit"],
        estimated_tokens={"input": 50, "output": {"typical": 100, "max": 200}}
    ),
    "calculator": ToolConfig(
        name="calculator",
        description="执行数学计算",
        version="1.0.0",
        cacheable=True,
        cache_ttl=3600,
        estimated_tokens={"input": 100, "output": {"typical": 50, "max": 100}}
    ),
    "search_documents": ToolConfig(
        name="search_documents",
        description="搜索文档数据库（支持分页）",
        version="2.1.0",
        cacheable=True,
        cache_ttl=300,
        estimated_tokens={"input": 100, "output": {"min": 200, "max": 5000, "typical": 1000}}
    )
}


# ==================== 辅助函数 ====================

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
    """感知节点 - Tool Use 接口（完整版 + 错误智慧库集成）"""

    def __init__(self, memory_dir: str = "./agi_memory"):
        self.c_ext_available = C_EXT_AVAILABLE
        self.cache = ToolCache()
        self.observability = ObservabilityManager()
        self.memory_dir = memory_dir
        
        # 初始化错误智慧库模块
        self.prevention_engine = None
        self.error_wisdom_manager = None
        
        if ERROR_WISDOM_AVAILABLE:
            try:
                self.prevention_engine = PreventionEngine(memory_dir)
                self.error_wisdom_manager = ErrorWisdomManager(memory_dir)
                logger.info("Error Wisdom integration enabled")
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
                    "trace_id": generate_trace_id()
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
                    "trace_id": generate_trace_id()
                }
            }

        # 生成 trace_id
        trace_id = generate_trace_id()

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
        if self.c_ext_available:
            try:
                # 调用 C 扩展
                result = core_perception_node.call_tool(tool_name, params)
                # 确保包含 trace_id
                if 'metadata' in result and 'trace_id' not in result['metadata']:
                    result['metadata']['trace_id'] = trace_id
                return result
            except Exception as e:
                logger.warning(f"C extension failed for {tool_name}: {e}, falling back to Python")

        # Python 实现的后备方案
        return self._execute_tool_python(tool_name, params, config, trace_id)

    def _execute_tool_python(self, tool_name: str, params: dict, config: ToolConfig, trace_id: str) -> dict:
        """纯 Python 实现的后备方案"""
        start_time = time.time()

        try:
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
                    result = eval(expression)
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

                    # 参数错误和权限错误不重试
                    if error_code in ['INVALID_PARAMS', 'PERMISSION_DENIED', 'TOOL_NOT_FOUND', 'TOOL_DEPRECATED']:
                        return result

                    # 执行错误和计算错误不重试
                    if error_code in ['EXECUTION_ERROR', 'CALC_ERROR']:
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
        记录错误到错误智慧库
        
        Args:
            tool_name: 工具名称
            params: 调用参数
            error: 异常对象
            trace_id: 追踪ID
        """
        if not self.error_wisdom_manager:
            return
        
        try:
            # 分析错误类型
            error_type = "工具性错误"
            error_subtype = self._classify_tool_error(error)
            
            # 记录错误
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
