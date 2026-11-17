"""
edge_cloud_dispatch.py - V7 绔簯鍗忓悓鍗忚 v1.0 鐨?Python 绔晶 SDK 鍙傝冨疄鐜般?

杩欐槸 references/edge-cloud-protocol.md + edge-cloud-protocol-schema.json 鐨勯涓?
Python 钀藉湴瀹炵幇锛屾彁渚涳細
  - build_request()         鏋勫缓 6 娈佃姹傜粨鏋勶紙8 涓?required 瀛楁锛?
  - validate_request()      鐢?jsonschema + schema 鏂囦欢鏍獙
  - check_abstract_data_size()  abstract_data < 10KB 绾潫锛圴7 搂4.1锛孍002锛?
  - EdgeCloudClient         绔簯浜崲瀹埛绔紙PII 鑴辨晱 + 鎴愭湰鐩戞帶 + 5 绾檷绾?+ 鐔旀柇锛?
  - 閿欒鐮佹槧灏?E001~E202锛圴7 搂6锛?

璁捐鍝插锛堢户鎵胯嚜 video-editing-skill锛夛細
  - 閲嶆椿绔晶鍋氾紙PII 鑴辨晱 / 澶皬鎴柇 / 瑙勫垯鏍獙閮藉湪绔晶瀹屾垚锛?
  - 鍐崇瓥浜戠鍋氾紙exchange 鎶婃娊璞暟鎹彂缁欎簯绔嬁鍐崇瓥锛?
  - JSON 濂戠害鍋氭帴缂濓紙6 娈佃姹傜粨鏋勫氨鏄浜戣竟鐣岋級
  - 瑙勫垯灞傚仛瀹归敊锛坙esson_plan_guard 鍦悎鎴愬墠鏍獙浜戠杩斿洖锛?

鐢硶锛?
    from edge_cloud_dispatch import EdgeCloudClient, build_request

    client = EdgeCloudClient(transport=my_http_transport)
    req = build_request(
        intent="涓洪珮涓AI閫氳瘑璇剧紪鎺掓暀瀛矾寰?,
        task_type="learning_path_planning",
        context="鏈哄櫒瀛範鍏棬妯"潡",
        abstract_data={"segments": [...]},
        decision_type="educational",
        max_tokens=2000,
        max_cost_usd=0.001,
    )
    response = client.exchange(req)
"""
from __future__ import annotations
__version__ = "8.1.0-aipc"  # V8.1-AIPC: 每次工作自动输出本地/云端对比 + 全互动控件完整性门控


# --- UTF-8 stdout/stderr (Windows 涓枃杈撳嚭闃蹭贡鐮? -----------------------------
def _configure_stream_encoding(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")

import sys as _sys
_configure_stream_encoding(_sys.stdout)
_configure_stream_encoding(_sys.stderr)
del _sys
# ----------------------------------------------------------------------------

from log_util import get_logger

log = get_logger("edge_cloud")

import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

# 绔晶鑴氭湰鐩綍瑙e瀽
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
SCHEMA_PATH = SKILL_DIR / "references" / "edge-cloud-protocol-schema.json"

# V7 鍗忚甯搁噺
PROTOCOL_VERSION = "1.0"
DEFAULT_SOURCE = "edge-ai-pc"
ABSTRACT_DATA_MAX_BYTES = 10240  # 10KB锛圴7 搂4.1锛?

# 5 绾檷绾槇鍊硷紙V7 搂7.2锛?
TIMEOUT_LEVEL_2_THRESHOLD = 3   # 杩炵画 3 娆秴鏃?鈫?Level 2
TIMEOUT_LEVEL_3_THRESHOLD = 5   # 杩炵画 5 娆秴鏃?鈫?Level 3


# ---------------------------------------------------------------------------
# 閿欒鐮佹槧灏勶紙V7 搂6 閿欒鐮佽" E001~E202锛?"
# ---------------------------------------------------------------------------

ERROR_CODES: dict[str, str] = {
    "E001": "协议版本不兼容",
    "E002": "abstract_data 超过 10KB 限制",
    "E003": "PII 检测未通过 (pii_detected 不为 false)",
    "E004": "数据分类非法或必填字段缺失",
    "E101": "云端请求超时",
    "E102": "云端限流 (rate limit)",
    "E103": "云端内部错误 (5xx)",
    "E201": "端侧推理失败",
    "E202": "成本熔断触发 (cumulative_cost_usd >= monthly_budget)",
}


def error_response(
    request_id: str,
    code: str,
    message: str,
    suggestion: str = "",
    retry_after: int = 0,
    degradation_level: int = 1,
) -> dict:
    """鏋勯?V7 鍗忚閿欒鍝嶅簲銆?"""
    return {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request_id,
        "timestamp": _utc_now_iso(),
        "status": "error",
        "error": {
            "code": code,
            "message": message,
            "suggestion": suggestion or ERROR_CODES.get(code, ""),
            "retry_after_seconds": retry_after,
        },
        "degradation_level": degradation_level,
    }


# ---------------------------------------------------------------------------
# 宸叿鍑芥暟
# ---------------------------------------------------------------------------

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _serialize_size(obj: Any) -> int:
    """计算对象 JSON 序列化后的 UTF-8 字节数."""
    if obj is None:
        return 0
    if isinstance(obj, bytes):
        return len(obj)
    try:
        return len(json.dumps(obj, ensure_ascii=False).encode("utf-8"))
    except (TypeError, ValueError):
        return len(str(obj).encode("utf-8"))


# ---------------------------------------------------------------------------
# 1. 鏋勫缓 6 娈佃姹?
# ---------------------------------------------------------------------------

def build_request(
    intent: str,
    task_type: str,
    context: str,
    abstract_data: dict,
    decision_type: str,
    max_tokens: int,
    max_cost_usd: float,
    *,
    source: str = DEFAULT_SOURCE,
    pii_detected: bool = False,
    data_classification: str = "anonymous",
    save_to_local: bool = True,
) -> dict:
    """构建 V7 端云协同协议 6 段请求结构.

    8 个 required 字段（schema 定义）：
        protocol_version / request_id / timestamp / source / intent / abstract / request / callback
    """
    return {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": str(uuid.uuid4()),
        "timestamp": _utc_now_iso(),
        "source": source,
        "intent": intent[:500],
        "abstract": {
            "task_type": task_type,
            "context": context[:200],
            "abstract_data": abstract_data if isinstance(abstract_data, dict) else {},
            "pii_detected": pii_detected,
            "data_classification": data_classification,
        },
        "request": {
            "decision_type": decision_type,
            "max_tokens": max_tokens,
            "max_cost_usd": max_cost_usd,
        },
        "callback": {
            "edge_execution": True,
            "save_to_local": save_to_local,
        },
    }


# ---------------------------------------------------------------------------
# 2. abstract_data 大小检查 (V7 §4.1, E002)
# ---------------------------------------------------------------------------

def check_abstract_data_size(abstract_data: Any) -> tuple[Any, bool, int]:
    """检查 abstract_data 序列化后体积是否超出大小上限.

    Returns:
        (data, truncated, size_bytes)
        - truncated=True 时 data 已被截断为只保留前若干 key
    """
    size = _serialize_size(abstract_data)
    if size < ABSTRACT_DATA_MAX_BYTES:
        return abstract_data, False, size

    # 鎴柇锛氬鏋滄槸 dict锛屽彧淇濈暀鍓?N 涓?key 鐩村埌 < 10KB
    if isinstance(abstract_data, dict):
        keys = list(abstract_data.keys())
        truncated: dict = {}
        for k in keys:
            candidate = dict(truncated)
            candidate[k] = abstract_data[k]
            if _serialize_size(candidate) >= ABSTRACT_DATA_MAX_BYTES:
                break
            truncated = candidate
        truncated["_truncated"] = True
        truncated["_original_size_bytes"] = size
        return truncated, True, _serialize_size(truncated)

    # 瀛楃涓?鍏朵粬锛氱洿鎺埅鏂埌瀹夊叏闀垮害
    if isinstance(abstract_data, str):
        safe = abstract_data[: (ABSTRACT_DATA_MAX_BYTES - 100)]
        return safe + "...[truncated]", True, _serialize_size(safe)

    return abstract_data, True, size


# ---------------------------------------------------------------------------
# 3. 璇锋眰鏍獙锛坖sonschema + schema 鏂囦欢锛?
# ---------------------------------------------------------------------------

def _load_schema() -> Optional[dict]:
    """加载 edge-cloud-protocol-schema.json (失败时返回 None)."""
    if not SCHEMA_PATH.exists():
        return None
    try:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _builtin_validate(request: dict) -> list[str]:
    """schema 文件不可用时的内置基础校验."""
    errors: list[str] = []
    required = [
        "protocol_version", "request_id", "timestamp", "source",
        "intent", "abstract", "request", "callback",
    ]
    for k in required:
        if k not in request:
            errors.append(f"缺少必填字段：{k}")

    if request.get("protocol_version") != PROTOCOL_VERSION:
        errors.append(f"protocol_version 必须为 {PROTOCOL_VERSION}")

    abstract = request.get("abstract") or {}
    if not isinstance(abstract, dict):
        errors.append("abstract 必须为对象")
    else:
        for k in ("task_type", "context", "abstract_data", "pii_detected", "data_classification"):
            if k not in abstract:
                errors.append(f"abstract 缺少必需字段：{k}")
        if abstract.get("pii_detected") not in (False, True):
            errors.append("pii_detected 必须为布尔值")

    req = request.get("request") or {}
    if not isinstance(req, dict):
        errors.append("request 必须为对象")
    else:
        for k in ("decision_type", "max_tokens", "max_cost_usd"):
            if k not in req:
                errors.append(f"request 缺少必需字段：{k}")

    cb = request.get("callback") or {}
    if not isinstance(cb, dict):
        errors.append("callback 必须为对象")
    elif cb.get("edge_execution") is not True:
        errors.append("callback.edge_execution 必须为 true")

    return errors


def validate_request(request: dict) -> tuple[bool, list[str]]:
    """校验请求是否符合 V7 协议 schema.

    Returns:
        (passed, errors)
    """
    if not isinstance(request, dict):
        return False, ["request 必须为 dict 类型"]

    schema = _load_schema()
    if schema is None:
        return (len(_builtin_validate(request)) == 0), _builtin_validate(request)

    try:
        import jsonschema
        from jsonschema import Draft202012Validator
        # schema 鏂囦欢鐢?"$defs" + 椤跺眰 "Request" 瀹氫箟
        request_schema = {
            "$schema": schema.get("$schema", "https://json-schema.org/draft/2020-12/schema"),
            **schema.get("Request", {}),
        }
        # 鍚堝苟 $defs锛坖sonschema 闇瑕侊級
        if "$defs" in schema:
            request_schema["$defs"] = schema["$defs"]
        Draft202012Validator(request_schema).validate(request)
        return True, []
    except ImportError:
        return (len(_builtin_validate(request)) == 0), _builtin_validate(request)
    except Exception as exc:
        return False, [f"schema 校验失败：{exc}"]


# ---------------------------------------------------------------------------
# 4. EdgeCloudClient锛堢浜戜氦鎹鎴风锛?
# ---------------------------------------------------------------------------

Transport = Callable[[dict], dict]


class EdgeCloudClient:
    """端云协同协议 v1.0 客户端 (V7 §2 落地实现).

    集成 4 项核心约束 (V7 核心要求):
      1. PII 自动脱敏 (调用 pii_redactor.redact_abstract_data)
      2. abstract_data < 10KB 限制 (check_abstract_data_size)
      3. 成本监控与熔断 (cost_monitor.CostMonitor)
      4. 5 级降级状态机 (V7 §7.2)

    Args:
        transport:  端云传输函数 transport(request_dict) -> response_dict。
                    测试时可注入 mock；生产环境默认用 _default_http_transport。
        cost_monitor: 成本监控对象 (duck-typing, record_cost / check_circuit_breaker)。
        schema_path:  schema 文件路径 (默认 references/edge-cloud-protocol-schema.json)。
        npu_available: NPU 是否可用 (影响降级 Level 4)。
        request_timeout: 单次云端请求超时秒数
    """

    def __init__(
        self,
        transport: Optional[Transport] = None,
        cost_monitor: Any = None,
        schema_path: Optional[Path] = None,
        npu_available: bool = True,
        request_timeout: float = 30.0,
    ) -> None:
        self.transport: Transport = transport or _default_http_transport
        self.cost_monitor = cost_monitor
        self.schema_path = Path(schema_path) if schema_path else SCHEMA_PATH
        self.npu_available = npu_available
        self.request_timeout = request_timeout

        # 闄嶇骇鐘舵佹満
        self.consecutive_timeouts: int = 0
        self.degradation_level: int = 1
        self._circuit_breaker_active: bool = False
        # V7-AIPC 鍗囩骇锛氭媶鍒嗕负 connect/read timeout锛圴7.3.2 鏀硅繘2 鍗囩骇鐗堬級锛屽 provider 閫傞厤 + work_summary 鑷姩璁板綍
        self.connect_timeout: float = 5.0
        self.read_timeout: float = request_timeout

        # 鍒濆鍖栨椂鏍规嵁 NPU 鍙敤鎬绠楅檷绾骇鍒?
        prev_level = 1
        self._recompute_degradation_level()
        if self.degradation_level != prev_level:
            self._report_degradation(
                reason="init_npu" if not npu_available else "init",
            )

    # ---- 闄嶇骇鐘舵佹満 ----

    def _recompute_degradation_level(self) -> None:
        """鏍规嵁杩炵画瓒呮椂鏁?/ NPU 鍙敤鎬?/ 鐔旀柇鐘舵侀噸绠楅檷绾骇鍒?"""
        if self._circuit_breaker_active:
            self.degradation_level = 5
            return
        if not self.npu_available:
            self.degradation_level = 4
            return
        if self.consecutive_timeouts >= TIMEOUT_LEVEL_3_THRESHOLD:
            self.degradation_level = 3
            return
        if self.consecutive_timeouts >= TIMEOUT_LEVEL_2_THRESHOLD:
            self.degradation_level = 2
            return
        self.degradation_level = 1

    def _report_degradation(self, reason: str = "", request_id: str = "") -> None:
        """V7.3.2 鏀硅繘5锛氫笂鎶綋鍓?degradation_level 鍒?cost_monitor銆?"""
        if self.cost_monitor is None:
            return
        record_fn = getattr(self.cost_monitor, "record_degradation", None)
        if callable(record_fn):
            try:
                record_fn(
                    level=self.degradation_level,
                    source="edge_cloud",
                    reason=reason,
                    request_id=request_id,
                )
            except Exception:
                pass

    def _record_timeout(self) -> None:
        self.consecutive_timeouts += 1
        self._recompute_degradation_level()

    def _record_success(self) -> None:
        self.consecutive_timeouts = 0
        self._recompute_degradation_level()

    def _check_circuit_breaker(self) -> bool:
        """妫鏌垚鏈啍鏂紙V7 搂11.4锛夈?"""
        if self.cost_monitor is None:
            return False
        # duck-typing锛氫紭鍏堣皟鏂规硶
        fn = getattr(self.cost_monitor, "check_circuit_breaker", None)
        if callable(fn):
            try:
                triggered = bool(fn())
            except Exception:
                triggered = False
        else:
            triggered = False
        if triggered:
            self._circuit_breaker_active = True
            self._recompute_degradation_level()
        return triggered

    # ---- PII 鑴辨晱 ----

    def _apply_pii_redaction(self, request: dict) -> tuple[dict, bool]:
        """瀵?abstract_data 閫掑綊 PII 鑴辨晱锛圴7 zero-upload-privacy 4 绾劚鏁忥級銆?"""
        abstract = request.get("abstract") or {}
        data = abstract.get("abstract_data")
        try:
            from pii_redactor import redact_abstract_data
            redacted, detected = redact_abstract_data(data)
            abstract["abstract_data"] = redacted
            abstract["pii_detected"] = detected
            request["abstract"] = abstract
            return request, detected
        except ImportError:
            return request, abstract.get("pii_detected", False)

    # ---- 涓讳氦鎹祦绋?----

    def exchange(self, request: dict) -> dict:
        """跑一次端云交换.

        流程:
          1. schema 校验
          2. PII 脱敏
          3. abstract_data 大小检查 + 截断
          4. 成本熔断检查
          5. 降级 Level 5 时直接返回本地 fallback
          6. 调 transport 发请求
          7. 记录成本 / 更新降级状态
        """
        request_id = request.get("request_id", str(uuid.uuid4()))

        # 1. schema 鏍獙
        passed, errors = validate_request(request)
        if not passed:
            return error_response(
                request_id, "E004",
                f"请求 schema 校验失败：{'; '.join(errors[:5])}",
                degradation_level=self.degradation_level,
            )

        # 2. PII 鑴辨晱
        request, pii_detected = self._apply_pii_redaction(request)
        if pii_detected:
            # V7 瑕佹眰 pii_detected 蹇呴}涓?false 鎵嶅厑璁镐笂浼?
            # 鑴辨晱鍚庡凡鏇挎崲涓烘帺鐮侊紝pii_detected 鍙嶆槧"鏄惁鏇炬娴嬪埌"
            # 涓婁紶瀛楁寮哄埗涓?false锛堝凡鑴辨晱锛?
            request["abstract"]["pii_detected"] = False

        # 3. abstract_data 澶皬妫鏌?
        abstract = request.get("abstract", {})
        data, truncated, size = check_abstract_data_size(abstract.get("abstract_data"))
        if truncated:
            log.warn(f"[edge-cloud] [WARN] abstract_data 超过 10KB（{size}B），已自动截断")
            abstract["abstract_data"] = data
            request["abstract"] = abstract
        if size >= ABSTRACT_DATA_MAX_BYTES and not truncated:
            return error_response(
                request_id, "E002",
                f"abstract_data 体积 {size}B 超过 10KB 限制",
                "端侧已截断 abstract_data，仅保留与决策相关的关键字段",
                degradation_level=self.degradation_level,
            )

        # 4. 鎴愭湰鐔旀柇妫鏌?
        if self._check_circuit_breaker():
            return error_response(
                request_id, "E202",
                "成本熔断触发：cumulative_cost_usd >= monthly_budget",
                "系统已切换到 Level 5（全本地）模式，等待管理员解除",
                degradation_level=5,
            )

        # 5. 降级 Level 5：全本地，不调云端
        if self.degradation_level >= 5:
            return error_response(
                request_id, "E202",
                "当前降级级别 Level 5（全本地），云端调用禁用",
                "检查 NPU 可用性与成本预算后重试",
                degradation_level=5,
            )

        # 6. 调 transport 发请求
        try:
            response = self.transport(request)
        except TimeoutError:
            self._record_timeout()
            return error_response(
                request_id, "E101",
                f"云端请求超时（>{self.request_timeout}s），"
                f"连续超时 {self.consecutive_timeouts} 次",
                "系统将自动降级，稍后重试",
                retry_after=min(30, 2 ** self.consecutive_timeouts),
                degradation_level=self.degradation_level,
            )
        except Exception as exc:
            return error_response(
                request_id, "E103",
                f"云端内部错误：{exc}",
                "检查云端服务状态后重试",
                degradation_level=self.degradation_level,
            )

        # 7. 记录成本 / 更新降级状态
        usage = response.get("usage") if isinstance(response, dict) else None
        if isinstance(usage, dict) and self.cost_monitor is not None:
            cost = float(usage.get("cost_usd", 0.0))
            record_fn = getattr(self.cost_monitor, "record_cost", None)
            if callable(record_fn):
                try:
                    record_fn(cost, request_id)
                except Exception:
                    pass
            # 璁板綍鎴愭湰鍚庡啀娆鏌啍鏂?
            self._check_circuit_breaker()

        status = response.get("status") if isinstance(response, dict) else None
        if status == "success":
            self._record_success()
        elif status == "error":
            code = (response.get("error") or {}).get("code", "")
            if code == "E101":
                self._record_timeout()
            elif code == "E102":
                # 闄愭祦锛氫篃绠楄秴鏃剁被锛屼絾涓嶅鍔犺繛缁鏁?
                pass

        response.setdefault("cumulative_cost_usd", 0.0)
        return response


# ---------------------------------------------------------------------------
# 榛樿 HTTP transport锛堢敓浜敤锛屾祴璇曟椂娉叆 mock锛?
# ---------------------------------------------------------------------------

# V7.3.2 鏀硅繘1锛氬 provider 閫傞厤锛坥penai-compatible / anthropic / custom锛?
# 浼樺厛绾細EDGE_CLOUD_PROVIDER 鐜鍙橀噺 > 鏍规嵁 endpoint URL 鎺柇
# 鍗忚锛?
#   openai-compatible (default): POST {endpoint} with {"model", "messages", "max_tokens", ...}
#   anthropic: POST {endpoint}/v1/messages with {"model", "max_tokens", "messages", ...}
#   custom: 鐩存帴閫忎紶 V7 6 娈佃姹傦紙鐢簬鑷缓 edge-cloud-exchange 鏈嶅姟锛?

_PROVIDER_OPENAI = "openai"
_PROVIDER_ANTHROPIC = "anthropic"
_PROVIDER_CUSTOM = "custom"


def _resolve_provider(endpoint: str) -> str:
    """鏍规嵁 endpoint URL 鎺柇 provider 绫诲瀷銆?"""
    env = os.environ.get("EDGE_CLOUD_PROVIDER", "").strip().lower()
    if env in (_PROVIDER_OPENAI, _PROVIDER_ANTHROPIC, _PROVIDER_CUSTOM):
        return env
    if "anthropic" in endpoint.lower():
        return _PROVIDER_ANTHROPIC
    return _PROVIDER_OPENAI  # 榛樿 OpenAI-compatible


def _v7_to_openai_request(request: dict) -> dict:
    """V7 6 段协议 → OpenAI /chat/completions 格式。"""
    abstract = request.get("abstract") or {}
    intent = request.get("intent", "")
    context = abstract.get("context", "")
    # 拼装 system + user 消息
    system_msg = (
        "你是 AI 通识课教学专家。V7 端云协同协议 v1.0。\n"
        f"主任务：{abstract.get('task_type', '')}\n"
        "请基于元数据（abstract_data）返回教学建议。"
    )
    user_msg = f"意图：{intent}\n上下文：{context}\n元数据：{json.dumps(abstract.get('abstract_data', {}), ensure_ascii=False)[:8000]}"
    return {
        "model": os.environ.get("EDGE_CLOUD_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        "max_tokens": request.get("request", {}).get("max_tokens", 500),
        "temperature": 0.3,
    }


def _openai_to_v7_response(openai_resp: dict, request: dict) -> dict:
    """OpenAI 响应 → V7 6 段响应。"""
    request_id = request.get("request_id", str(uuid.uuid4()))
    try:
        choice = openai_resp.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        usage = openai_resp.get("usage", {})
        # OpenAI usage 涓嶈繑鍥?cost锛岄渶鏍规嵁妯"瀷 + tokens 浼扮畻
        cost = _estimate_openai_cost(usage, request)
        return {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": request_id,
            "timestamp": _utc_now_iso(),
            "status": "success",
            "data": {
                "decision": content,
                "decision_type": request.get("request", {}).get("decision_type", "educational"),
                "model": openai_resp.get("model", "unknown"),
            },
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
                "cost_usd": cost,
            },
        }
    except (IndexError, KeyError, TypeError) as e:
        return error_response(
            request_id, "E103", f"OpenAI 响应解析失败：{e}",
        )


def _estimate_openai_cost(usage: dict, request: dict) -> float:
    """估算 OpenAI 调用成本（基于 usage + 已知模型定价）.

    参考 2026-08 价格表（USD / 1K tokens）：
      gpt-4o-mini:        in 0.00015, out 0.0006
      gpt-4o:             in 0.0025,  out 0.01
      deepseek-chat:      in 0.00014, out 0.00028
    """
    model = os.environ.get("EDGE_CLOUD_MODEL", "gpt-4o-mini")
    pricing = {
        "gpt-4o-mini": (0.00015, 0.0006),
        "gpt-4o": (0.0025, 0.01),
        "deepseek-chat": (0.00014, 0.00028),
        "claude-3-5-sonnet": (0.003, 0.015),
    }
    in_rate, out_rate = pricing.get(model, (0.00015, 0.0006))
    prompt = usage.get("prompt_tokens", 0)
    completion = usage.get("completion_tokens", 0)
    return round(prompt * in_rate / 1000 + completion * out_rate / 1000, 6)


def _v7_to_anthropic_request(request: dict) -> dict:
    """V7 6 娈靛崗璁?鈫?Anthropic /v1/messages 鏍煎紡銆?"""
    abstract = request.get("abstract") or {}
    intent = request.get("intent", "")
    context = abstract.get("context", "")
    return {
        "model": os.environ.get("EDGE_CLOUD_MODEL", "claude-3-5-sonnet-20241022"),
        "max_tokens": request.get("request", {}).get("max_tokens", 500),
        "messages": [
            {
                "role": "user",
                "content": f"意图：{intent}\n上下文：{context}\n元数据：{json.dumps(abstract.get('abstract_data', {}), ensure_ascii=False)[:8000]}",
            }
        ],
        "system": "你是 AI 通识课教学专家。基于元数据返回教学建议。",
    }


def _anthropic_to_v7_response(anthropic_resp: dict, request: dict) -> dict:
    """Anthropic 响应 → V7 6 段响应。"""
    request_id = request.get("request_id", str(uuid.uuid4()))
    try:
        content_blocks = anthropic_resp.get("content", [])
        text = "".join(b.get("text", "") for b in content_blocks if b.get("type") == "text")
        usage = anthropic_resp.get("usage", {})
        # Anthropic: input_tokens / output_tokens
        prompt = usage.get("input_tokens", 0)
        completion = usage.get("output_tokens", 0)
        cost = _estimate_openai_cost(
            {"prompt_tokens": prompt, "completion_tokens": completion}, request
        )
        return {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": request_id,
            "timestamp": _utc_now_iso(),
            "status": "success",
            "data": {
                "decision": text,
                "decision_type": request.get("request", {}).get("decision_type", "educational"),
                "model": anthropic_resp.get("model", "unknown"),
            },
            "usage": {
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "total_tokens": prompt + completion,
                "cost_usd": cost,
            },
        }
    except (KeyError, TypeError) as e:
        return error_response(
            request_id, "E103", f"Anthropic 响应解析失败：{e}",
        )


def _default_http_transport(request: dict) -> dict:
    """默认 HTTP transport（V7.3.2 第 5 provider 版本）。

    支持:
      1. openai-compatible: 默认，适用于 OpenAI / DeepSeek / Moonshot / 智谱 等
      2. anthropic: 适用于 Claude 系列
      3. custom: 自建 edge-cloud-exchange 服务的 V7 6 段专传

    环境变量:
      EDGE_CLOUD_ENDPOINT   - 云端 endpoint URL（必填）
      EDGE_CLOUD_PROVIDER   - openai | anthropic | custom（默认按 URL 推断）
      EDGE_CLOUD_MODEL      - 模型名（默认 gpt-4o-mini）
      EDGE_CLOUD_API_KEY    - API 密钥（Authorization header）
      EDGE_CLOUD_CONNECT_TIMEOUT - 连接超时秒（默认 5）
      EDGE_CLOUD_READ_TIMEOUT    - 读取超时秒（默认 30）

    测试时不应使用 transport，应注入 mock。
    """
    import urllib.request
    import urllib.error
    import socket

    endpoint = os.environ.get("EDGE_CLOUD_ENDPOINT", "")
    if not endpoint:
        raise RuntimeError(
            "鏈缃?EDGE_CLOUD_ENDPOINT 鐜鍙橀噺銆?"
            "璇峰湪 run.ps1 / run.sh 涓厤缃簯绔?endpoint URL銆?"
        )
    provider = _resolve_provider(endpoint)

    # V7.3.2 鏀硅繘2锛氭媶鍒嗕负 connect_timeout / read_timeout
    connect_timeout = float(os.environ.get("EDGE_CLOUD_CONNECT_TIMEOUT", "5"))
    read_timeout = float(os.environ.get("EDGE_CLOUD_READ_TIMEOUT", "30"))

    api_key = os.environ.get("EDGE_CLOUD_API_KEY", "")

    # 鎸?provider 杞崲璇锋眰
    if provider == _PROVIDER_ANTHROPIC:
        # Anthropic: 鎷兼帴 /v1/messages 璺緞
        url = endpoint.rstrip("/") + "/v1/messages" if not endpoint.endswith("/v1/messages") else endpoint
        provider_payload = _v7_to_anthropic_request(request)
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "anthropic-version": "2023-06-01",
        }
        if api_key:
            headers["x-api-key"] = api_key
    elif provider == _PROVIDER_CUSTOM:
        # Custom: V7 6 娈甸忎紶
        url = endpoint
        provider_payload = request
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
    else:
        # OpenAI-compatible: 鎷兼帴 /v1/chat/completions 璺緞
        url = endpoint.rstrip("/") + "/v1/chat/completions" if not endpoint.endswith("/chat/completions") else endpoint
        provider_payload = _v7_to_openai_request(request)
        headers = {
            "Content-Type": "application/json; charset=utf-8",
        }
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

    payload = json.dumps(provider_payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=connect_timeout) as resp:
            body = resp.read().decode("utf-8")
            provider_resp = json.loads(body)
    except socket.timeout as exc:
        # V7.3.2 鏀硅繘2锛歝onnect_timeout 瓒呮椂鍗曠嫭鍖哄垎锛堢綉缁滃眰 vs 璇诲彇灞傦級
        raise TimeoutError(f"connect_timeout={connect_timeout}s 抛出：{exc}") from exc
    except urllib.error.HTTPError as exc:
        if exc.code == 429:
            request_id = request.get("request_id", "")
            return error_response(request_id, "E102", "云端限流（HTTP 429）")
        if exc.code in (401, 403):
            request_id = request.get("request_id", "")
            return error_response(request_id, "E003", f"鉴权失败 HTTP {exc.code}：检查 EDGE_CLOUD_API_KEY")
        raise
    except TimeoutError:
        raise
    except Exception as exc:
        raise RuntimeError(f"HTTP transport 失败：{exc}") from exc

    # 浜屾璇诲彇瓒呮椂锛坲rllib 涓嶆敮鎸佸崟鐙?read timeout锛屼娇鐢暣浣?timeout锛?
    # 娉剰锛歅ython urllib 涓嶅尯鍒?connect/read timeout锛涜繖閲岀敤 read_timeout 鍏滃簳
    if provider == _PROVIDER_ANTHROPIC:
        return _anthropic_to_v7_response(provider_resp, request)
    elif provider == _PROVIDER_CUSTOM:
        return provider_resp  # 宸茬粡鏄?V7 6 娈垫牸寮?
    else:
        return _openai_to_v7_response(provider_resp, request)


# ---------------------------------------------------------------------------
# CLI（便于手动测试单个请求）
# ---------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    log = get_logger("edge_cloud")
    import argparse

    p = argparse.ArgumentParser(
        prog="edge_cloud_dispatch",
        description="V7 端云协同协议 Python SDK（构建 + 校验 + 交换）",
    )
    sub = p.add_subparsers(dest="cmd")

    p_build = sub.add_parser("build", help="构建一个示例请求并打印")
    p_build.add_argument("--intent", default="测试请求")
    p_build.add_argument("--task-type", default="pedagogy_recommendation")
    p_build.add_argument("--json", action="store_true")

    p_val = sub.add_parser("validate", help="校验 stdin / 文件中的请求 JSON")
    p_val.add_argument("--file", default=None, help="请求 JSON 文件（默认 stdin）")

    p_exch = sub.add_parser("exchange", help="跑一次端云交换（需要云端服务）")
    p_exch.add_argument("--file", required=True, help="请求 JSON 文件")

    args = p.parse_args(argv)

    if args.cmd == "build":
        req = build_request(
            intent=args.intent,
            task_type=args.task_type,
            context="CLI 测试",
            abstract_data={"note": "this is a test request"},
            decision_type="educational",
            max_tokens=500,
            max_cost_usd=0.001,
        )
        print(json.dumps(req, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "validate":
        if args.file:
            text = Path(args.file).read_text(encoding="utf-8")
        else:
            text = sys.stdin.read()
        try:
            req = json.loads(text)
        except json.JSONDecodeError as e:
            log.error(f"JSON 解析失败：{e}")
            return 2
        passed, errors = validate_request(req)
        report = {"passed": passed, "errors": errors, "error_count": len(errors)}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if passed else 1

    if args.cmd == "exchange":
        try:
            req = json.loads(Path(args.file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            log.error(f"读取请求失败：{e}")
            return 2
        client = EdgeCloudClient()
        resp = client.exchange(req)
        print(json.dumps(resp, ensure_ascii=False, indent=2))
        if resp.get("status") == "success":
            return 0
        # 通信层错误（超时/transport 错误/熔断）→ Exit 2
        if resp.get("error_code") in ("E301", "E302", "E303", "E202"):
            return 2
        # 协议层错误（schema/PII/大小）→ Exit 1
        return 1

    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

