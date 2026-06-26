#!/usr/bin/env python3
"""
Doubao Image Gen v2.3.0 — ByteDance AI Image Gen Skill
====================================================
核心功能:
  1. 文生图 (Text-to-Image) — 根据文本描述生成图片
  2. 图生图 (Image-to-Image) — 基于参考图进行编辑/风格转换（支持本地路径/URL/base64）
  3. 智能模型调度 — 4.5 → 5.0Lite → 4.0 自动降级
  4. 每日限制 — 每模型每日最高 18 次，全部超限自动拒绝
  5. 历史追踪 — 7 天 JSON 记录，含完整提示词/分辨率/比例
  6. 控制台自动同步 — 每次调用前查询平台用量，谁多按谁的
  7. 灵活尺寸 — 2K/4K + 比例 + 精准分辨率 (最大 16,777,216 像素)

API 参考: https://www.volcengine.com/docs/82379/1541523
"""

import os
import sys
import json
import time
import datetime
import re
import io
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# ============================================================
# Windows 编码修复: 强制 stdout 使用 UTF-8，兼容 emoji 输出
# ============================================================
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ============================================================
# 依赖检测: requests 是唯一必需的外部依赖
# ============================================================
try:
    import requests
except ImportError:
    print("ERROR: 需要安装 requests 库。请运行: pip install requests")
    raise SystemExit(1)

# PIL 可选，用于图生图时读取上传图片分辨率
try:
    from PIL import Image as PILImage
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Volcengine SDK 可选，用于控制台用量查询
try:
    import volcenginesdkcore
    HAS_VOLC_SDK = True
except ImportError:
    HAS_VOLC_SDK = False

# ============================================================
# 自动加载 .env 文件（尽早，在模块配置前）
# ============================================================
try:
    from pathlib import Path as _Path
    _env_file = _Path(__file__).resolve().parent / ".env"
    if _env_file.exists():
        with open(_env_file, "r", encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _key, _, _val = _line.partition("=")
                    _key, _val = _key.strip(), _val.strip().strip('"').strip("'")
                    if _key not in os.environ:
                        os.environ[_key] = _val
except Exception:
    pass

# ============================================================
# 控制台用量同步器 — 自动查询平台用量，"谁多按谁的"
# ============================================================

class ConsoleSyncer:
    """
    ListEndpoints 获取当前接入点ID → GetInferenceUsage 查询用量。
    每模型只查一个当前接入点，不缓存历史端点。
    规则: local = max(local, platform)
    """

    _EP_MATCH = {
        "doubao-seedream-4.5": "Doubao-Seedream-4.5",
        "doubao-seedream-5.0-lite": "Doubao-Seedream-5.0-Lite",
        "doubao-seedream-4.0": "Doubao-Seedream-4.0",
    }

    def __init__(self):
        self._ak = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
        self._sk = os.environ.get("VOLCENGINE_SECRET_KEY", "")
        self._region = os.environ.get("VOLCENGINE_REGION", "cn-beijing")
        self._enabled = bool(self._ak and self._sk and HAS_VOLC_SDK)
        # .env 中配置的 MODEL_ID 也是端点 ID，直接用于查询
        self._ep_overrides = {
            "Doubao-Seedream-4.5": os.environ.get("DOUBAO_MODEL_45_ID", ""),
            "Doubao-Seedream-5.0-Lite": os.environ.get("DOUBAO_MODEL_50L_ID", ""),
            "Doubao-Seedream-4.0": os.environ.get("DOUBAO_MODEL_40_ID", ""),
        }

    @property
    def enabled(self):
        return self._enabled

    def _api(self):
        cfg = volcenginesdkcore.Configuration()
        cfg.ak = self._ak; cfg.sk = self._sk; cfg.region = self._region
        return volcenginesdkcore.UniversalApi(volcenginesdkcore.ApiClient(configuration=cfg))

    def _current_endpoint_ids(self):
        """获取接入点ID映射。优先用 .env 配置，其次 ListEndpoints 自动检测。"""
        result = {}
        # 1) .env 中指定了端点 ID 的，直接使用
        for name, eid in self._ep_overrides.items():
            if eid:
                result[name] = eid.strip().lower()
        if len(result) == 3:
            return result
        # 2) 自动检测
        try:
            api = self._api()
            info = volcenginesdkcore.UniversalInfo(
                method="POST", service="ark", version="2024-01-01",
                action="ListEndpoints", content_type="application/json")
            for it in api.do_call(info, {}).get("Items", []):
                nm = it.get("Name", "").strip().lower()
                eid = it.get("Id", "")
                if not eid:
                    continue
                for key, display_name in self._EP_MATCH.items():
                    if nm.startswith(key.replace(".", "-")):
                        if display_name not in result:
                            result[display_name] = eid.lower()
                        break
            return result
        except Exception:
            return result

    def query_today_image_counts(self):
        """查询今日三个模型用量(仅当前接入点)。"""
        if not self._enabled:
            return {}
        ep = self._current_endpoint_ids()
        if not ep:
            return {}
        try:
            today = datetime.date.today().strftime("%Y-%m-%d")
            api = self._api()
            info = volcenginesdkcore.UniversalInfo(
                method="POST", service="ark", version="2024-01-01",
                action="GetInferenceUsage", content_type="application/json")
            r = api.do_call(info, {
                "QueryInterval": "Day", "StartTime": today, "EndTime": today,
                "Filters": [{"Key": "ModelEndpoint", "Values": list(ep.values())}]})
            fs = [f["Name"] for f in r.get("Fields", [])]
            rows = r.get("Data", [])
            if "ModelEndpoint" not in fs or "ImageCount" not in fs:
                return {}
            ei, ii = fs.index("ModelEndpoint"), fs.index("ImageCount")
            id2name = {v: k for k, v in ep.items()}
            c = {}
            for row in rows:
                m = id2name.get(str(row[ei])) if ei < len(row) else None
                if m:
                    c[m] = c.get(m, 0) + int(row[ii] or 0)
            return c
        except Exception:
            return {}

    def sync_to_local(self, history_manager):
        pc = self.query_today_image_counts()
        if not pc or sum(pc.values()) == 0:
            return {m["name"]: "no_platform_data" for m in MODELS}
        rv, today = {}, HistoryManager._today()
        lc = history_manager.data.setdefault("daily_counts", {}).setdefault(today, {})
        for m in MODELS:
            n = m["name"]
            p = pc.get(n, 0)
            l = lc.get(n, 0)
            if p > l:
                lc[n] = p; rv[n] = "synced"
            else:
                rv[n] = "kept_local"
        history_manager._save()
        return rv


# ============================================================
# 全局配置 — 环境变量可覆盖，无硬编码密钥
# ============================================================

MODELS: List[Dict] = [
    {"name": "Doubao-Seedream-4.5",     "model_id": os.environ.get("DOUBAO_MODEL_45_ID", ""),  "priority": 1, "daily_limit": 18, "min_pixels": 3686400, "max_size": "4K"},
    {"name": "Doubao-Seedream-5.0-Lite", "model_id": os.environ.get("DOUBAO_MODEL_50L_ID", ""), "priority": 2, "daily_limit": 18, "min_pixels": 0,       "max_size": "3K"},
    {"name": "Doubao-Seedream-4.0",     "model_id": os.environ.get("DOUBAO_MODEL_40_ID", ""),  "priority": 3, "daily_limit": 18, "min_pixels": 0,       "max_size": "4K"},
]

# 验证接入点已配置
_MODEL_ENV_MAP = {"Doubao-Seedream-4.5": "DOUBAO_MODEL_45_ID", "Doubao-Seedream-5.0-Lite": "DOUBAO_MODEL_50L_ID", "Doubao-Seedream-4.0": "DOUBAO_MODEL_40_ID"}
for m in MODELS:
    if not m["model_id"]:
        raise RuntimeError(
            f"未设置 {_MODEL_ENV_MAP[m['name']]}，请在火山方舟控制台获取接入点 Model ID 后设置环境变量。"
            f" 打开 https://console.volcengine.com/ark → 在线推理 → 复制 Model ID"
        )

API_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
DEFAULT_SIZE = "3K"
# 默认加水印，.env 设 DEFAULT_WATERMARK=false 永久关闭
DEFAULT_WATERMARK = os.environ.get("DEFAULT_WATERMARK", "true").lower() != "false"
# API 原生支持的自适应预设（可直接传给 API，模型自定宽高比）
API_ADAPTIVE_PRESETS = {"2K", "4K"}

PRESET_SIZES: Dict[str, Tuple[int, int, str, int]] = {
    "2K": (2048, 2048, "1:1", 4_194_304),
    "3K": (3072, 3072, "1:1", 9_437_184),
    "4K": (4096, 4096, "1:1", 16_777_216),
}
RECOMMENDED_RATIOS: Dict[str, Tuple[int, int]] = {
    "1:1": (2048, 2048), "4:3": (2304, 1728), "3:4": (1728, 2304),
    "16:9": (2560, 1440), "9:16": (1440, 2560), "3:2": (2496, 1664),
    "2:3": (1664, 2496), "21:9": (3024, 1296),
}
MAX_PIXELS = 16_777_216
HISTORY_RETENTION_DAYS = 7
API_TIMEOUT = 120

BASE_DIR: Path = Path(__file__).resolve().parent
HISTORY_FILE: Path = Path(os.environ.get("DOUBAO_HISTORY_FILE", str(BASE_DIR / "image_gen_history.json")))
IMAGE_DIR: Path = Path(os.environ.get("DOUBAO_IMAGE_DIR", str(BASE_DIR / "Image")))
TEMP_DIR: Path = Path(os.environ.get("DOUBAO_TEMP_DIR", str(BASE_DIR / "Temp")))


class _JSONEncoder(json.JSONEncoder):
    """自定义 JSON 编码器，确保中文正常显示、浮点数合理精度"""
    def default(self, obj):
        return super().default(obj)


class HistoryManager:
    """
    历史记录管理器

    职责:
    - 加载/保存 image_gen_history.json
    - 记录每次调用（完整提示词、模型、时间、分辨率、比例、像素数）
    - 每日模型调用计数
    - 自动清理 7 天前数据
    - 控制台数据同步（仅当控制台 > 本地时同步）

    文件结构:
    {
        "history": [{ record }, ...],
        "daily_counts": { "YYYY-MM-DD": { "ModelName": count }, ... }
    }
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.data = self._load()
        self._auto_clean()

    # ---- 数据加载/保存 ----

    def _load(self) -> Dict:
        """从文件加载历史数据；文件不存在或损坏则返回空结构。"""
        if not self.file_path.exists():
            return {"history": [], "daily_counts": {}}
        try:
            with open(self.file_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                # 兼容旧格式
                if "history" not in data:
                    data["history"] = []
                if "daily_counts" not in data:
                    data["daily_counts"] = {}
                return data
        except (json.JSONDecodeError, IOError):
            return {"history": [], "daily_counts": {}}

    def _save(self) -> None:
        """将当前数据写入 JSON 文件。"""
        self._ensure_dir()
        tmp_path = self.file_path.with_suffix(".json.tmp")
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(self.data, fh, ensure_ascii=False, indent=2, cls=_JSONEncoder)
        tmp_path.replace(self.file_path)

    def _ensure_dir(self) -> None:
        """确保历史文件所在目录存在。"""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    # ---- 自动清理 ----

    def _auto_clean(self) -> None:
        """删除 7 天前的历史记录和每日计数。"""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=HISTORY_RETENTION_DAYS)
        cutoff_ts = cutoff.timestamp()
        cutoff_str = cutoff.strftime("%Y-%m-%d")

        # 清理历史记录
        self.data["history"] = [
            r for r in self.data["history"]
            if r.get("timestamp", 0) >= cutoff_ts
        ]

        # 清理每日计数
        self.data["daily_counts"] = {
            d: c for d, c in self.data["daily_counts"].items()
            if d >= cutoff_str
        }

    # ---- 日期工具 ----

    @staticmethod
    def _today() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d")

    # ---- 计数查询 ----

    def get_daily_count(self, model_name: str) -> int:
        """获取指定模型今天的调用次数。"""
        today = self._today()
        return self.data.setdefault("daily_counts", {}).setdefault(today, {}).get(model_name, 0)

    def get_all_counts(self) -> Dict[str, int]:
        """获取今天所有模型的调用次数。"""
        today = self._today()
        counts = self.data.setdefault("daily_counts", {}).setdefault(today, {})
        return {m["name"]: counts.get(m["name"], 0) for m in MODELS}

    def get_total_history_count(self) -> int:
        """获取历史记录总数。"""
        return len(self.data.get("history", []))

    # ---- 计数修改 ----

    def increment_count(self, model_name: str) -> int:
        """
        增加模型调用计数并返回当前值。

        副作用: 自动清理过期记录后保存。
        """
        self._auto_clean()
        today = self._today()
        counts = self.data.setdefault("daily_counts", {}).setdefault(today, {})
        counts[model_name] = counts.get(model_name, 0) + 1
        self._save()
        return counts[model_name]

    # ---- 记录追加 ----

    def add_record(self, record: Dict) -> None:
        """
        追加一条调用记录到历史，自动清理后保存。

        record 必须包含:
        - timestamp (float)
        - datetime (str)
        - mode (str): "text-to-image" 或 "image-to-image"
        - model (str)
        - endpoint (str)
        - prompt (str): 用户原始提示词
        - full_prompt (str): 投喂给模型的完整提示词
        - style (str|None)
        - reference_image (str|None): 图生图的参考图 URL
        - size_requested (str)
        - size_type (str)
        - resolution (str)
        - ratio (str)
        - pixels (int)
        - image_url (str)
        """
        self._auto_clean()
        self.data.setdefault("history", []).append(record)
        self._save()

    # ---- 控制台同步 ----

    def sync_from_console(self, console_counts: Dict[str, int]) -> Dict[str, str]:
        """
        从控制台数据同步本地计数。

        规则: 控制台数据 > 本地数据 → 同步到本地
              控制台数据 ≤ 本地数据 → 不操作（保留本地）

        参数:
            console_counts: {"Doubao-Seedream-4.5": 12, "Doubao-Seedream-5.0-Lite": 3, ...}

        返回: {"ModelName": "synced" | "skipped" | "not_found"}
        """
        today = self._today()
        local_counts = self.data.setdefault("daily_counts", {}).setdefault(today, {})
        result = {}

        for model_name, console_count in console_counts.items():
            local_count = local_counts.get(model_name, 0)
            if console_count > local_count:
                local_counts[model_name] = console_count
                result[model_name] = "synced"
            elif console_count <= local_count:
                result[model_name] = "skipped"

        # 处理控制台没有但本地有的模型
        for model_name in local_counts:
            if model_name not in console_counts:
                result[model_name] = "local_only"

        self._save()
        return result

    # ---- 状态查询 ----

    def get_status(self) -> Dict:
        """获取所有模型的今日状态。"""
        return {
            "date": self._today(),
            "total_history": self.get_total_history_count(),
            "models": [
                {
                    "name": m["name"],
                    "count": self.get_daily_count(m["name"]),
                    "limit": m["daily_limit"],
                    "remaining": m["daily_limit"] - self.get_daily_count(m["name"]),
                    "available": self.get_daily_count(m["name"]) < m["daily_limit"],
                    "priority": m["priority"],
                }
                for m in MODELS
            ]
        }


# ============================================================
# 豆包图片生成器 — 文生图 + 图生图
# ============================================================

class DoubaoImageGenerator:
    """
    豆包 Seedream 图片生成器

    用法:
        gen = DoubaoImageGenerator()  # 从环境变量读取 API Key

        # 文生图
        result = gen.generate_text_to_image("可爱的猫咪", size="2K")

        # 图生图
        result = gen.generate_image_to_image(
            "把背景换成森林",
            image_url="https://example.com/photo.jpg"
        )

        # 查看状态
        status = gen.get_status()

        # 控制台同步
        gen.sync_console_counts({"Doubao-Seedream-4.5": 12})
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化生成器。

        参数:
            api_key: 火山方舟 API Key。
                     不传则从环境变量 ARK_API_KEY 或 VOLCENGINE_API_KEY 读取。
        """
        self.api_key = (
            api_key
            or os.environ.get("ARK_API_KEY", "")
            or os.environ.get("VOLCENGINE_API_KEY", "")
        )
        self.history = HistoryManager(HISTORY_FILE)
        self._console = ConsoleSyncer()  # 控制台同步器

    def _auto_console_sync(self) -> None:
        """
        每次生图前从控制台同步用量，并静默清理 Temp 过期文件。

        规则: 平台 > 本地 → 同步; 本地 > 平台 → 保留本地。
        """
        if not self._console.enabled:
            return
        self._console.sync_to_local(self.history)
        self._cleanup_temp()

    def _cleanup_temp(self):
        """静默清理 Temp 目录中访问时间超过 7 天的文件。"""
        try:
            if not TEMP_DIR.exists():
                return
            cutoff = time.time() - 7 * 86400
            for f in TEMP_DIR.iterdir():
                if f.is_file() and f.stat().st_atime < cutoff:
                    f.unlink()
        except Exception:
            pass

    # ---- 模型选择 ----

    def _select_available_model(self, force_model: Optional[str] = None) -> Optional[Dict]:
        """
        按优先级选择可用模型。

        参数:
            force_model: 强制使用指定模型。支持简称: 4.5 / 5l / 5.0l / 4.0 / 40

        返回: 模型配置字典 或 None
        """
        if force_model:
            for model in MODELS:
                if force_model == model["name"]:
                    if self.history.get_daily_count(model["name"]) < model["daily_limit"]:
                        return model
                    return None
            return None

        for model in MODELS:
            if self.history.get_daily_count(model["name"]) < model["daily_limit"]:
                return model
        return None

    # ---- 尺寸解析 ----

    @staticmethod
    def _gcd(a: int, b: int) -> int:
        """计算最大公约数（欧几里得算法）。"""
        while b:
            a, b = b, a % b
        return a

    @classmethod
    def _parse_size(cls, size: str) -> Tuple[str, int, int, str, str]:
        """
        解析尺寸参数，返回 API 就绪的 size 字符串和参考分辨率。

        支持的格式:
          - 预设:   "2K" / "4K" → 直接传给 API，参考分辨率用于记录
          - 比例:   "16:9" → 计算 "WxH" 传给 API
          - 精准:   "1920x1080" → 直接传给 API

        返回: (api_size_str, ref_width, ref_height, ratio_str, size_type)
              api_size_str: 传给 API 的 size 字段值
              ref_width/ref_height: 参考分辨率（用于历史记录）
              ratio_str: 比例字符串
              size_type ∈ {"preset", "aspect", "custom", "fallback"}
        """
        raw = size.strip()

        # 1) 预设尺寸 — 直接传给 API（无额外比例时）
        upper = raw.upper()
        if upper in PRESET_SIZES:
            w, h, r, _ = PRESET_SIZES[upper]
            return (upper, w, h, r, "preset")

        # 2) 比例格式  W:H → 查找推荐值
        m = re.match(r"^(\d{1,4}):(\d{1,4})$", raw)
        if m:
            ratio_key = f"{int(m.group(1))}:{int(m.group(2))}"
            # 优先用推荐值
            if ratio_key in RECOMMENDED_RATIOS:
                w, h = RECOMMENDED_RATIOS[ratio_key]
                return (f"{w}x{h}", w, h, ratio_key, "aspect")
            # 未在推荐列表中，按 2K 基准计算
            rw, rh = int(m.group(1)), int(m.group(2))
            base = 2048
            w = base
            h = int(base * rh / rw)
            pixels = w * h
            if pixels > MAX_PIXELS:
                scale = (MAX_PIXELS / pixels) ** 0.5
                w = int(w * scale)
                h = int(h * scale)
            return (f"{w}x{h}", w, h, f"{rw}:{rh}", "aspect")

        # 3) 精准分辨率  WxH
        m = re.match(r"^(\d{1,4})x(\d{1,4})$", raw, re.IGNORECASE)
        if m:
            w, h = int(m.group(1)), int(m.group(2))
            if w > 0 and h > 0:
                pixels = w * h
                if pixels > MAX_PIXELS:
                    scale = (MAX_PIXELS / pixels) ** 0.5
                    w = int(w * scale)
                    h = int(h * scale)
                g = cls._gcd(w, h)
                return (f"{w}x{h}", w, h, f"{w // g}:{h // g}", "custom")

        # 4) 无法识别 → 回退默认 2K
        w, h, r, _ = PRESET_SIZES[DEFAULT_SIZE]
        return (DEFAULT_SIZE, w, h, r, "fallback")

    @classmethod
    def _compute_size_with_ratio(
        cls, preset: str, ratio_str: str
    ) -> Tuple[str, int, int, str]:
        """
        根据预设尺寸(2K/3K/4K) + 比例计算最佳分辨率。

        原理: 使用预设的像素目标值，按比例分配宽高。
        如 4K + 16:9 → 像素目标 16,777,216 → 6240×2656

        返回: (api_size_str, width, height, simplified_ratio)
        """
        preset_key = preset.strip().upper()
        if preset_key not in PRESET_SIZES:
            preset_key = DEFAULT_SIZE

        _, _, _, target_pixels = PRESET_SIZES[preset_key]

        # 解析比例
        m = re.match(r"^(\d{1,4}):(\d{1,4})$", ratio_str.strip())
        if not m:
            # 无效比例，回退预设默认
            w, h, r, _ = PRESET_SIZES[preset_key]
            return (preset_key, w, h, r)

        rw, rh = int(m.group(1)), int(m.group(2))
        # w = sqrt(target_pixels × rw / rh)
        # h = w × rh / rw
        w_float = (target_pixels * rw / rh) ** 0.5
        h_float = w_float * rh / rw
        w = int(round(w_float))
        h = int(round(h_float))

        # 确保像素不超上限且不低于最低要求
        pixels = w * h
        if pixels > MAX_PIXELS:
            scale = (MAX_PIXELS / pixels) ** 0.5
            w = int(w * scale)
            h = int(h * scale)

        # 简化比例
        g = cls._gcd(w, h)
        simple_ratio = f"{w // g}:{h // g}"

        return (f"{w}x{h}", w, h, simple_ratio)

    @staticmethod
    def _get_image_resolution(image_path_or_url: str) -> Optional[Tuple[int, int]]:
        """
        获取图片分辨率。支持本地路径和远程 URL。

        PIL 不可用时返回 None（调用方应使用默认值）。
        """
        if not HAS_PIL:
            return None
        try:
            data = io.BytesIO()
            total = 0
            if image_path_or_url.startswith(("http://", "https://")):
                resp = requests.get(image_path_or_url, timeout=15, stream=True)
                resp.raise_for_status()
                for chunk in resp.iter_content(8192):
                    data.write(chunk)
                    total += len(chunk)
                    if total > 10 * 1024 * 1024:
                        break
                data.seek(0)
            else:
                # 本地文件
                with open(image_path_or_url, "rb") as f:
                    data.write(f.read(10 * 1024 * 1024))
                data.seek(0)
            img = PILImage.open(data)
            return img.size  # (width, height)
        except Exception:
            return None

    @staticmethod
    def _encode_image(image_path_or_url: str) -> str:
        """
        将图片输入规范化为 API 可接受的格式。

        本地文件 → 先复制到 TEMP_DIR → base64 data URI；公网 URL → 原样返回。
        """
        if image_path_or_url.startswith(("http://", "https://")):
            return image_path_or_url
        if image_path_or_url.startswith("data:"):
            return image_path_or_url  # 已经是 base64

        src = Path(image_path_or_url)
        if not src.is_file():
            raise FileNotFoundError(f"图片文件不存在: {image_path_or_url}")

        # 复制到 TEMP_DIR（统一管理，规避路径权限和特殊字符问题）
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        suffix = src.suffix.lower()
        safe_name = f"ref_{abs(hash(str(src))):x}{suffix}"
        tmp_path = TEMP_DIR / safe_name
        import shutil
        shutil.copy2(src, tmp_path)

        raw = tmp_path.read_bytes()
        if len(raw) > 15 * 1024 * 1024:
            raise ValueError(f"图片文件过大 ({len(raw) / 1024 / 1024:.1f} MB)，最大 15 MB")

        fmt = suffix.lstrip(".")
        if fmt == "jpg":
            fmt = "jpeg"
        elif fmt not in ("png", "jpeg", "webp", "bmp", "tiff", "gif"):
            fmt = "png"

        import base64
        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:image/{fmt};base64,{b64}"

    @staticmethod
    def _encode_images(image_list: List[str]) -> List[str]:
        """批量规范化图片输入。"""
        return [DoubaoImageGenerator._encode_image(img) for img in image_list]

    # ---- API 调用 ----

    def _build_payload(
        self,
        model_id: str,
        prompt: str,
        size_str: str,
        *,
        image_urls: Optional[List[str]] = None,
        sequential: bool = False,
        max_images: int = 4,
        response_format: str = "url",
        watermark: bool = DEFAULT_WATERMARK,
    ) -> Tuple[Dict, Dict]:
        """
        构建 API 请求 payload 和 headers。

        size_str: "2K"/"4K" (预设) 或 "1920x1080" (精准像素)
        sequential: True 启用组图模式
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload: Dict = {
            "model": model_id,
            "prompt": prompt,
            "size": size_str,
            "response_format": response_format,
            "watermark": watermark,
        }

        # 图生图/多图融合模式：传递参考图
        if image_urls:
            payload["image"] = image_urls

        # 组图模式
        if sequential or (image_urls and max_images > 1):
            payload["sequential_image_generation"] = "auto"
            payload["sequential_image_generation_options"] = {"max_images": max_images}
        elif image_urls:
            payload["sequential_image_generation"] = "disabled"
        # 纯文生图不传 sequential 字段

        return payload, headers

    def _call_api(self, payload: Dict, headers: Dict) -> str:
        """
        调用火山引擎图片生成 API。

        返回: 图片 URL（或 base64 字符串，取决于 response_format）。

        异常:
            requests.RequestException — 网络/HTTP 错误
            (KeyError, IndexError)       — 响应格式异常
        """
        resp = requests.post(API_BASE_URL, headers=headers, json=payload, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        # 提取图片
        if "data" in data and len(data["data"]) > 0:
            item = data["data"][0]
            return item.get("url", "") or item.get("b64_json", "")
        return ""

    def _call_api_sequence(self, payload: Dict, headers: Dict) -> List[str]:
        """
        调用组图生成 API，返回多张图片 URL 列表。
        """
        resp = requests.post(API_BASE_URL, headers=headers, json=payload, timeout=API_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        urls = []
        if "data" in data:
            for item in data["data"]:
                url = item.get("url", "") or item.get("b64_json", "")
                if url:
                    urls.append(url)
        return urls

    # ---- 图片保存 ----

    @staticmethod
    def _make_filename(prompt: str, resolution: str, model_name: str = "") -> str:
        """根据内容+分辨率+模型+时间生成文件名，如 洪崖洞2K-5.0L-223208.png"""
        clean = re.sub(r'[\\/:*?"<>|]', '', prompt).strip()
        clean = re.sub(r'\s+', '', clean)
        if len(clean) > 16:
            clean = clean[:16]
        res_short = resolution.replace('×', 'x').replace(' ', '')
        model_short = model_name.replace("Doubao-Seedream-", "").replace("-Lite", "L")
        ts = datetime.datetime.now().strftime("%H%M%S")
        return f"{clean}{res_short}-{model_short}-{ts}.png"

    def _save_image(self, image_url: str, prompt: str, resolution: str, model_name: str = "", index: int = 0) -> Optional[str]:
        """下载图片到 Image/ 目录，返回本地路径。"""
        if not image_url or not image_url.startswith("http"):
            return None
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        base = self._make_filename(prompt, resolution, model_name)
        if index > 0:
            base = f"{Path(base).stem}_{index}.png"
        filepath = IMAGE_DIR / base
        last_error = None
        # 尝试直连和代理
        for use_proxy in (False, True):
            try:
                proxies = None
                if use_proxy:
                    for key in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
                        p = os.environ.get(key, "")
                        if p:
                            proxies = {"https": p, "http": p}
                            break
                r = requests.get(image_url, timeout=60, proxies=proxies)
                r.raise_for_status()
                filepath.write_bytes(r.content)
                return str(filepath)
            except Exception as e:
                last_error = e
                continue
        print(f"   ⚠️ 图片下载失败: {type(last_error).__name__}: {last_error}", file=sys.stderr)
        return None

    # ---- 记录构建 ----

    @staticmethod
    def _build_record(
        mode: str,
        model: Dict,
        prompt: str,
        full_prompt: str,
        style: Optional[str],
        reference_image: Optional[str],
        size_requested: str,
        size_type: str,
        width: int,
        height: int,
        ratio: str,
        image_url: str,
    ) -> Dict:
        """构建一条历史记录。"""
        ts = time.time()
        url_short = image_url if len(image_url) <= 200 else image_url[:197] + "..."
        return {
            "timestamp": ts,
            "datetime": datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode,
            "model": model["name"],
            "model_id": model["model_id"],
            "prompt": prompt,
            "full_prompt": full_prompt,
            "style": style,
            "reference_image": reference_image,
            "size_requested": size_requested,
            "size_type": size_type,
            "resolution": f"{width}x{height}" if width > 0 else "adaptive",
            "ratio": ratio,
            "pixels": width * height if width > 0 else 0,
            "image_url": image_url,
            "image_url_short": url_short,
        }

    @staticmethod
    def _build_success_result(
        mode: str,
        model: Dict,
        image_url: str,
        width: int,
        height: int,
        size_requested: str,
        ratio: str,
        count_today: int,
        local_path: Optional[str] = None,
    ) -> Dict:
        """构建成功结果字典。"""
        result = {
            "success": True,
            "mode": mode,
            "model": model["name"],
            "image_url": image_url,
            "resolution": f"{width}x{height}" if width > 0 else "adaptive",
            "size_requested": size_requested,
            "ratio": ratio,
            "pixels": width * height if width > 0 else 0,
            "count_today": count_today,
            "limit": model["daily_limit"],
        }
        if local_path:
            result["local_path"] = local_path
        return result

    @staticmethod
    def _build_sequence_result(
        mode: str,
        model: Dict,
        image_urls: List[str],
        local_paths: List[str],
        width: int,
        height: int,
        size_requested: str,
        ratio: str,
        count_today: int,
    ) -> Dict:
        """构建组图成功结果字典。"""
        return {
            "success": True,
            "mode": mode,
            "model": model["name"],
            "image_urls": image_urls,
            "local_paths": local_paths,
            "generated_count": len(image_urls),
            "resolution": f"{width}x{height}" if width > 0 else "adaptive",
            "size_requested": size_requested,
            "ratio": ratio,
            "pixels": width * height if width > 0 else 0,
            "count_today": count_today,
            "limit": model["daily_limit"],
        }

    # ---- 文生图 ----

    def generate_text_to_image(
        self,
        prompt: str,
        size: str = DEFAULT_SIZE,
        style: Optional[str] = None,
        response_format: str = "url",
        watermark: bool = DEFAULT_WATERMARK,
        *,
        ratio: Optional[str] = None,
        force_model: Optional[str] = None,
    ) -> Dict:
        """
        文生图：根据文本描述生成图片。

        参数:
            prompt:   图片描述（越详细越好）
            size:     尺寸 — "2K"/"4K"/"16:9"/"1920x1080" 等
            ratio:    比例（可选）。仅当 size 为预设 "2K"/"4K" 时生效。
                      如 size="4K", ratio="16:9" → 6240×2656
            style:    风格标签（可选）
            response_format: "url"（默认）或 "b64_json"
            watermark: 是否添加水印
            force_model: 强制使用指定模型名（如"Doubao-Seedream-4.0"）

        返回: 结果字典 {success, image_url, resolution, ...}
        """
        # 0) 每次生图前同步控制台用量
        self._auto_console_sync()

        # 1) 选择模型
        model = self._select_available_model(force_model)
        if not model:
            return self._all_models_exhausted_error(force_model)

        # 2) 解析尺寸
        # - API 自适应预设（2K/4K）不传比例 → 直传 API，模型自定宽高
        # - 非 API 预设（3K）或其他带比例 → 自行计算
        upper = size.strip().upper()
        if upper in API_ADAPTIVE_PRESETS and ratio is None:
            api_size = upper
            ref_w, ref_h = 0, 0
            display_ratio, size_type = "adaptive", "preset_adaptive"
        elif upper in PRESET_SIZES and ratio is None:
            # 非 API 预设无比例 → 按默认 16:9 计算
            api_size, ref_w, ref_h, display_ratio = self._compute_size_with_ratio(size, "16:9")
            size_type = "preset_with_ratio"
        elif ratio and upper in PRESET_SIZES:
            api_size, ref_w, ref_h, display_ratio = self._compute_size_with_ratio(size, ratio)
            size_type = "preset_with_ratio"
        else:
            api_size, ref_w, ref_h, display_ratio, size_type = self._parse_size(size)

        # 3) 检查模型最小像素要求（自适应模式跳过，API 自行决定）
        if size_type != "preset_adaptive":
            model_min = model.get("min_pixels", 0)
            if model_min > 0 and ref_w * ref_h < model_min:
                # 自动升级到模型最低要求
                scale = (model_min / (ref_w * ref_h)) ** 0.5
                ref_w = int(ref_w * scale)
                ref_h = int(ref_h * scale)
                api_size = f"{ref_w}x{ref_h}"
                size_type = "aspect"

        # 4) 构建提示词
        full_prompt = f"{style}, {prompt}" if style else prompt

        try:
            # 5) 调用 API
            payload, headers = self._build_payload(
                model["model_id"], full_prompt, api_size,
                response_format=response_format, watermark=watermark,
            )
            image_url = self._call_api(payload, headers)

            # 6) 记录
            self.history.increment_count(model["name"])
            record = self._build_record(
                mode="text-to-image",
                model=model,
                prompt=prompt,
                full_prompt=full_prompt,
                style=style,
                reference_image=None,
                size_requested=size,
                size_type=size_type,
                width=ref_w,
                height=ref_h,
                ratio=display_ratio,
                image_url=image_url,
            )
            self.history.add_record(record)

            # 7) 下载到本地 Image/
            local_path = self._save_image(image_url, prompt, size, model["name"])

            # 8) 返回结果
            return self._build_success_result(
                mode="text-to-image",
                model=model,
                image_url=image_url,
                width=ref_w,
                height=ref_h,
                size_requested=size,
                ratio=display_ratio,
                count_today=self.history.get_daily_count(model["name"]),
                local_path=local_path,
            )

        except requests.HTTPError as exc:
            return self._api_error_result(exc, model)
        except Exception as exc:
            return {"success": False, "error": f"生成失败: {type(exc).__name__}: {exc}"}

    # ---- 组图生成（Sequential） ----

    def generate_sequence(
        self,
        prompt: str,
        max_images: int = 4,
        *,
        image_urls: Optional[List[str]] = None,
        size: str = DEFAULT_SIZE,
        ratio: Optional[str] = None,
        style: Optional[str] = None,
        force_model: Optional[str] = None,
        watermark: bool = DEFAULT_WATERMARK,
    ) -> Dict:
        """
        组图生成：一次生成多张连续图片。

        支持 4 种模式:
          1. 文生组图: 仅 prompt + max_images
          2. 图生组图(单参考): image_urls=[url1] + max_images
          3. 多图融合单张: image_urls=[url1,url2] + max_images=1
          4. 多图融合组图: image_urls=[url1,url2] + max_images>1

        参数:
            prompt:     图片描述。多图融合时可用"图1""图2"指代参考图
            max_images: 最多生成张数 (1-15，默认 4)
            image_urls: 参考图列表（可选，最多 10 张）。
                       每项支持: 公网 URL / 本地路径 / base64 data URI
            size:       输出尺寸
            ratio:      比例（仅预设 size 时生效）
            style:      风格标签

        返回: {success, image_urls: [...], model, count_today, ...}
        """
        # 0) 自动同步控制台用量
        self._auto_console_sync()

        # 0.5) 规范化输入：本地路径自动转 base64
        if image_urls:
            image_urls = self._encode_images(image_urls)

        model = self._select_available_model(force_model)
        if not model:
            return self._all_models_exhausted_error(force_model)

        # 解析尺寸
        upper = size.strip().upper()
        if upper in API_ADAPTIVE_PRESETS and ratio is None:
            api_size = upper
            ref_w, ref_h = 0, 0
            display_ratio, size_type = "adaptive", "preset_adaptive"
        elif upper in PRESET_SIZES and ratio is None:
            api_size, ref_w, ref_h, display_ratio = self._compute_size_with_ratio(size, "16:9")
            size_type = "preset_with_ratio"
        elif ratio and upper in PRESET_SIZES:
            api_size, ref_w, ref_h, display_ratio = self._compute_size_with_ratio(size, ratio)
            size_type = "preset_with_ratio"
        else:
            api_size, ref_w, ref_h, display_ratio, size_type = self._parse_size(size)

        # 限制 max_images
        max_images = max(1, min(max_images, 15))
        total_refs = len(image_urls) if image_urls else 0
        if total_refs + max_images > 15:
            max_images = 15 - total_refs
            if max_images <= 0:
                return {"success": False, "error": "参考图+输出图总量不能超过 15 张"}

        # 自动补张数声明：API 需要 prompt 明确写"生成N张"，否则只出1张
        if max_images > 1:
            has_count = bool(re.search(r'(生成|generate|create|make)\s*\d+\s*(张|images|pictures|photos)', prompt, re.IGNORECASE))
            if not has_count:
                prompt = f"生成{max_images}张图 {prompt}"

        full_prompt = f"{style}, {prompt}" if style else prompt

        # 确定 mode 标签
        if image_urls and len(image_urls) >= 2:
            mode_tag = "multi-ref-sequence" if max_images > 1 else "multi-ref-fusion"
        elif image_urls:
            mode_tag = "image-to-image-sequence"
        else:
            mode_tag = "text-to-image-sequence"

        try:
            payload, headers = self._build_payload(
                model["model_id"], full_prompt, api_size,
                image_urls=image_urls,
                sequential=True,
                max_images=max_images,
                watermark=watermark,
            )
            image_urls_out = self._call_api_sequence(payload, headers)

            # 记录（每张生成图计为 1 次调用）
            local_paths = []
            for i, iurl in enumerate(image_urls_out):
                self.history.increment_count(model["name"])
                rec = self._build_record(
                    mode=f"{mode_tag}#{i + 1}",
                    model=model,
                    prompt=prompt,
                    full_prompt=full_prompt,
                    style=style,
                    reference_image=image_urls[0] if image_urls and len(image_urls) == 1 else None,
                    size_requested=size,
                    size_type=size_type,
                    width=ref_w,
                    height=ref_h,
                    ratio=display_ratio,
                    image_url=iurl,
                )
                self.history.add_record(rec)
                # 下载到本地
                lp = self._save_image(iurl, prompt, size, model["name"], index=i + 1)
                if lp: local_paths.append(lp)

            return self._build_sequence_result(
                mode=mode_tag,
                model=model,
                local_paths=local_paths,
                image_urls=image_urls_out,
                width=ref_w,
                height=ref_h,
                size_requested=size,
                ratio=display_ratio,
                count_today=self.history.get_daily_count(model["name"]),
            )

        except requests.HTTPError as exc:
            return self._api_error_result(exc, model)
        except Exception as exc:
            return {"success": False, "error": f"组图生成失败: {type(exc).__name__}: {exc}"}

    # ---- 图生图 ----

    def generate_image_to_image(
        self,
        prompt: str,
        image_url: str,
        size: Optional[str] = None,
        style: Optional[str] = None,
        response_format: str = "url",
        watermark: bool = DEFAULT_WATERMARK,
        *,
        force_model: Optional[str] = None,
    ) -> Dict:
        """
        图生图：基于参考图进行编辑/风格转换。

        参数:
            prompt:    编辑指令（如"把背景换成森林"）
            image_url: 参考图。支持:
                       - 公网 URL (http/https)
                       - 本地文件路径 (C:/.../photo.jpg) — 自动 base64 编码
                       - 已有的 base64 data URI
            size:      输出尺寸（可选）。
                       不传 → 自动检测参考图分辨率；
                       传了 → 按指定尺寸。
            style:     风格标签（可选）
            response_format: "url" 或 "b64_json"
            watermark: 是否添加水印

        返回: 结果字典
        """
        # 0) 规范化输入：本地路径自动转 base64
        image_url = self._encode_image(image_url)

        # 1) 自动同步控制台用量
        self._auto_console_sync()

        # 2) 选择模型
        model = self._select_available_model()
        if not model:
            return self._all_models_exhausted_error(force_model)

        # 3) 解析尺寸 — 优先自定义，其次参考图分辨率，最后默认 2K
        if size:
            api_size, ref_w, ref_h, ratio, size_type = self._parse_size(size)
        else:
            detected = self._get_image_resolution(image_url)
            if detected:
                w, h = detected
                pixels = w * h
                if pixels > MAX_PIXELS:
                    scale = (MAX_PIXELS / pixels) ** 0.5
                    w = int(w * scale)
                    h = int(h * scale)
                g = self._gcd(w, h)
                size_type = "auto"
                ref_w, ref_h = w, h
                ratio = f"{w // g}:{h // g}"
                api_size = f"{w}x{h}"
                size = api_size
            else:
                # 无法获取分辨率，回退默认
                api_size, ref_w, ref_h, ratio, size_type = self._parse_size(DEFAULT_SIZE)
                size = DEFAULT_SIZE

        # 3) 检查模型最小像素要求（自适应模式跳过，API 自行决定）
        if size_type != "preset_adaptive":
            model_min = model.get("min_pixels", 0)
            if model_min > 0 and ref_w * ref_h < model_min:
                scale = (model_min / (ref_w * ref_h)) ** 0.5
                ref_w = int(ref_w * scale)
                ref_h = int(ref_h * scale)
                api_size = f"{ref_w}x{ref_h}"
                if size_type == "auto":
                    size = api_size

        # 4) 构建提示词
        full_prompt = f"{style}, {prompt}" if style else prompt

        try:
            # 5) 调用 API（传入参考图 URL）
            payload, headers = self._build_payload(
                model["model_id"], full_prompt, api_size,
                image_urls=[image_url],
                response_format=response_format, watermark=watermark,
            )
            result_url = self._call_api(payload, headers)

            # 6) 记录
            self.history.increment_count(model["name"])
            record = self._build_record(
                mode="image-to-image",
                model=model,
                prompt=prompt,
                full_prompt=full_prompt,
                style=style,
                reference_image=image_url,
                size_requested=size or "auto",
                size_type=size_type,
                width=ref_w,
                height=ref_h,
                ratio=ratio,
                image_url=result_url,
            )
            self.history.add_record(record)

            # 7) 下载到本地
            local_path = self._save_image(result_url, prompt, size or "auto", model["name"])

            # 8) 返回结果
            return self._build_success_result(
                mode="image-to-image",
                model=model,
                image_url=result_url,
                width=ref_w,
                height=ref_h,
                size_requested=size or "auto",
                ratio=ratio,
                count_today=self.history.get_daily_count(model["name"]),
                local_path=local_path,
            )

        except requests.HTTPError as exc:
            return self._api_error_result(exc, model)
        except Exception as exc:
            return {"success": False, "error": f"图生图失败: {type(exc).__name__}: {exc}"}

    # ---- 错误结果构建 ----

    def _all_models_exhausted_error(self, force_model: str = None) -> Dict:
        """构建超限错误结果。如果指定了模型则提示该模型超限。"""
        if force_model:
            return {
                "success": False,
                "error": f"指定模型 {force_model} 今日调用已达 18 次上限，已自动拒绝。请换模型或明天再试。",
            }
        status = self.get_status()
        return {
            "success": False,
            "error": "所有模型今日调用次数已达上限（每模型 18 次/天），请明天再试！",
            "status": {
                m["name"]: {"count": m["count"], "remaining": m["remaining"]}
                for m in status["models"]
            },
        }

    @staticmethod
    def _api_error_result(http_error: requests.HTTPError, model: Dict) -> Dict:
        """构建 API HTTP 错误结果。"""
        status_code = http_error.response.status_code if http_error.response is not None else 0
        detail = ""
        try:
            detail = http_error.response.json()
        except Exception:
            detail = http_error.response.text if http_error.response is not None else ""
        return {
            "success": False,
            "error": f"API 请求失败 (HTTP {status_code})",
            "model": model["name"],
            "status_code": status_code,
            "detail": str(detail)[:500],
        }

    # ---- 状态查询 ----

    def get_status(self) -> Dict:
        """获取当前状态（所有模型今日计数、历史总数）。"""
        return self.history.get_status()

    # ---- 控制台同步 ----

    def sync_console_counts(self, console_counts: Dict[str, int]) -> Dict:
        """
        从控制台同步计数。

        参数:
            console_counts: {"Doubao-Seedream-4.5": 12, ...}

        返回:
            {model_name: "synced"|"skipped"|"local_only"}
        """
        return self.history.sync_from_console(console_counts)

    # ---- 兼容别名（保持向后兼容） ----

    def generate(self, prompt: str, size: str = DEFAULT_SIZE, style: Optional[str] = None) -> Dict:
        """【兼容】文生图别名，等同于 generate_text_to_image()。"""
        return self.generate_text_to_image(prompt=prompt, size=size, style=style)

    def get_history(self) -> List[Dict]:
        """获取完整调用历史列表。"""
        return self.history.data.get("history", [])

    def get_total_history_count(self) -> int:
        """获取历史记录总数。"""
        return self.history.get_total_history_count()

    def get_daily_counts(self) -> Dict[str, Dict]:
        """获取所有日期的每日计数。"""
        return self.history.data.get("daily_counts", {})


# ============================================================
# 纯 SDK — 触发词检测在 SKILL.md 中，由 AI 处理
# Python 只接收解析好的参数并执行
# ============================================================


def extract_image_url(text: str) -> Optional[str]:
    """
    从文本中提取图片 URL。

    返回: 第一个匹配的 URL 或 None。
    """
    # 匹配 http/https URL（常见图片格式）
    url_pattern = r'(https?://\S+\.(?:png|jpg|jpeg|webp|gif|bmp)(?:\?\S*)?)'
    matches = re.findall(url_pattern, text, re.IGNORECASE)
    if matches:
        return matches[0]
    # 匹配任意 http/https URL
    url_pattern_any = r'(https?://\S+)'
    matches_any = re.findall(url_pattern_any, text)
    if matches_any:
        return matches_any[0]
    return None


# ============================================================
# 主入口 — 命令行交互 / 测试
# ============================================================

def _parse_flags(args: List[str]) -> Tuple[List[str], Dict[str, str]]:
    """
    从命令行参数中提取 --flag value 对。

    返回: (剩余位置参数列表, {flag: value})
    支持: --size, --ratio, --model
    """
    flags: Dict[str, str] = {}
    remaining: List[str] = []
    i = 0
    while i < len(args):
        if args[i] in ("--size", "-s") and i + 1 < len(args):
            flags["size"] = args[i + 1]
            i += 2
        elif args[i] in ("--ratio", "-r") and i + 1 < len(args):
            flags["ratio"] = args[i + 1]
            i += 2
        elif args[i] == "--no-watermark":
            flags["no_watermark"] = True
            i += 1
        elif args[i] in ("--model", "-m") and i + 1 < len(args):
            flags["model"] = args[i + 1]
            i += 2
        else:
            remaining.append(args[i])
            i += 1
    return remaining, flags


def main():
    """命令行入口，用于手动测试和对模型展示用法。"""
    import sys

    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h", "help"):
        _print_usage()
        return

    subcmd = sys.argv[1].lower()

    if subcmd == "status":
        _cmd_status()
    elif subcmd in ("gen", "generate"):
        remaining, flags = _parse_flags(sys.argv[2:])
        _cmd_gen(remaining, flags)
    elif subcmd in ("img2img", "edit"):
        remaining, flags = _parse_flags(sys.argv[2:])
        _cmd_img2img(remaining, flags)
    elif subcmd in ("seq", "sequence", "fusion"):
        # 用 _parse_flags 解析通用标志，再手动解析 --num --refs
        remaining, flags = _parse_flags(sys.argv[2:])
        pos = []
        i = 0
        # 重新扫描位置参数，跳过已解析的标志
        raw_args = sys.argv[2:]
        while i < len(raw_args):
            a = raw_args[i]
            if a in ("--size", "-s", "--ratio", "-r", "--model", "-m") and i + 1 < len(raw_args):
                i += 2; continue
            elif a == "--no-watermark":
                i += 1; continue
            elif a == "--num" and i + 1 < len(raw_args):
                flags["num"] = raw_args[i + 1]; i += 2
            elif a == "--refs":
                i += 1
                while i < len(raw_args) and not raw_args[i].startswith("--"):
                    pos.append(raw_args[i]); i += 1
            elif not a.startswith("--"):
                pos.append(a); i += 1
            else:
                i += 1
        _cmd_seq(pos, flags)
    elif subcmd == "sync":
        _cmd_sync(sys.argv[2:])
    elif subcmd == "history":
        _cmd_history()
    elif subcmd == "test":
        _cmd_test()
    else:
        # 兼容旧用法: python doubao_image_gen.py "prompt" [size] [--ratio R]
        remaining, flags = _parse_flags(sys.argv[1:])
        prompt = remaining[0] if remaining else sys.argv[1]
        size = flags.get("size") or (remaining[1] if len(remaining) > 1 else None) or DEFAULT_SIZE
        _cmd_gen([prompt, size], flags)


def _print_usage():
    """打印详细使用说明。"""
    print(r"""
╔══════════════════════════════════════════════════════════════════════╗
║              ByteDance AI Image Gen v2.3.0                         ║
║              火山方舟 Seedream 图片生成/编辑                         ║
╚══════════════════════════════════════════════════════════════════════╝

【命令】
  python doubao_image_gen.py status                    查看状态/用量
  python doubao_image_gen.py sync                      控制台用量同步
  python doubao_image_gen.py history                   7天调用历史
  python doubao_image_gen.py gen <参数...>             文生单图
  python doubao_image_gen.py img2img <参数...>         图生单图
  python doubao_image_gen.py seq <参数...>             组图/融合

【全局参数】
  --size, -s       画质/分辨率       2K | 3K(默认) | 4K | WxH      gen/img2img/seq
  --ratio, -r      宽高比           16:9|9:16|1:1|4:3|21:9|2:1…    gen
  --model, -m      强制指定模型      Doubao-Seedream-4.5            gen/img2img/seq
                                     Doubao-Seedream-5.0-Lite
                                     Doubao-Seedream-4.0
  --no-watermark   关闭水印          开关                          gen/img2img/seq
  --num            生成张数          1-15                         seq
  --refs           参考图路径        文件路径…                      seq

【画质说明】
  2K/4K  → API 自适应宽高（不传 ratio 时服务端自定）
  3K     → 默认 4096x2304，传 ratio 时按比例计算
  WxH    → 精准分辨率，最大 16,777,216 px
  优先级: --size > 位置参数 > 默认 3K

【模型调度】
  默认自动降级: 4.5 → 5.0-Lite → 4.0
  每模型日限 18 次，指定模型超限不切换
  如简称 → 需传 --model 的完整名称: 4.5→Doubao-Seedream-4.5  5l→Doubao-Seedream-5.0-Lite  4.0→Doubao-Seedream-4.0

【水印控制】
  .env 设 DEFAULT_WATERMARK=false 永久关闭
  单次可用 --no-watermark

【调用示例】
  python doubao_image_gen.py gen "一只猫"                                         文生单图 默认3K
  python doubao_image_gen.py gen "一只猫" 4K --ratio 16:9                         文生 4K+16:9
  python doubao_image_gen.py gen "一只猫" 4K --ratio 21:9 --model "Doubao-Seedream-4.0"  文生 全参数
  python doubao_image_gen.py img2img "换成雪景" photo.jpg                         图生单图 自适应
  python doubao_image_gen.py img2img "改成油画" photo.jpg --size 4K               图生 4K输出
  python doubao_image_gen.py img2img "换背景" photo.jpg --model "Doubao-Seedream-4.0"  图生 全参数
  python doubao_image_gen.py seq "四季风景" --num 4                               文生组图 x4
  python doubao_image_gen.py seq "科幻场景" --num 2 --size 4K --model "Doubao-Seedream-4.0"  文生组图 全参数
  python doubao_image_gen.py seq "不同色调" --refs a.jpg --num 2                  图生组图 单参考→x2
  python doubao_image_gen.py seq "融合为超现实" --refs a.jpg b.jpg --num 1        多图融合 双图→1张
  python doubao_image_gen.py seq "无缝融合" --refs a.jpg b.jpg --num 1 --size 4K --ratio 21:9  多图融合 全参数
""")

def _cmd_status():
    """查看当前状态。"""
    gen = DoubaoImageGenerator()
    status = gen.get_status()
    print(f"\n📊 今日状态 ({status['date']})")
    print(f"   历史记录总数: {status['total_history']}")
    print(f"   {'─' * 48}")
    for m in status["models"]:
        icon = "🟢" if m["available"] else "🔴"
        bar = _progress_bar(m["count"], m["limit"])
        print(f"   {icon} [P{m['priority']}] {m['name']}")
        print(f"      {bar} {m['count']}/{m['limit']} (剩余: {m['remaining']})")


def _cmd_gen(args: List[str], flags: Dict[str, str] = None):
    """文生图命令。支持 --size/-s 和 --ratio/-r 命名参数。"""
    if not args:
        print("❌ 请提供提示词")
        return
    if flags is None:
        flags = {}

    prompt = args[0]
    # 尺寸优先级: --size 标志 > 位置参数 args[1] > 默认值
    size = flags.get("size") or (args[1] if len(args) > 1 else None) or DEFAULT_SIZE
    # 比例: 仅 --ratio 标志
    ratio = flags.get("ratio")

    gen = DoubaoImageGenerator()
    _print_status_header(gen)

    # 预选模型用于显示
    selected = gen._select_available_model(flags.get("model"))
    if not selected:
        _print_result(gen._all_models_exhausted_error(flags.get("model")))
        return

    print(f"\n🎨 文生图")
    print(f"   模型:   {selected['name']}")
    print(f"   提示词: {prompt}")
    print(f"   尺寸:   {size}" + (f" ({ratio})" if ratio else ""))
    print(f"   正在生成...")

    result = gen.generate_text_to_image(prompt, size, ratio=ratio, force_model=selected["name"], watermark=not flags.get("no_watermark"))
    _print_result(result)


def _cmd_img2img(args: List[str], flags: Dict[str, str] = None):
    """图生图命令（支持本地路径和公网URL）。支持 --size/-s 命名参数。"""
    if len(args) < 2:
        print("❌ 用法: python doubao_image_gen.py img2img <提示词> <图片URL或本地路径> [尺寸] [--size SIZE]")
        return
    if flags is None:
        flags = {}

    prompt = args[0]
    image_url = args[1]
    # 尺寸优先级: --size 标志 > 位置参数 args[2]
    size = flags.get("size") or (args[2] if len(args) > 2 else None)

    gen = DoubaoImageGenerator()
    _print_status_header(gen)

    # 预选模型用于显示
    selected = gen._select_available_model(flags.get("model"))
    if not selected:
        _print_result(gen._all_models_exhausted_error(flags.get("model")))
        return

    print(f"\n🖼️  图生图")
    print(f"   模型:     {selected['name']}")
    print(f"   提示词:   {prompt}")
    display_src = image_url[:80] + ("..." if len(image_url) > 80 else "")
    print(f"   参考图:   {display_src}")
    print(f"   尺寸:     {size or '自动检测'}")
    print(f"   正在生成...")

    result = gen.generate_image_to_image(prompt, image_url, size=size, force_model=selected["name"], watermark=not flags.get("no_watermark"))
    _print_result(result)


def _cmd_seq(args: List[str], flags: Dict[str, str] = None):
    """组图命令：文生组图或多图融合。支持 --size/-s --num/-n --refs。"""
    if not args:
        print("❌ 用法: python doubao_image_gen.py seq <提示词> [--size SIZE] [--num N] [--refs img1 img2...]")
        print("   示例: python doubao_image_gen.py seq \"四季风景\" --num 4")
        print("   示例: python doubao_image_gen.py seq \"不同色调\" --refs a.jpg --num 2")
        print("   示例: python doubao_image_gen.py seq \"融合\" --refs a.jpg b.jpg --num 1  (多图融合)")
        return
    if flags is None:
        flags = {}

    prompt = args[0]
    size = flags.get("size") or DEFAULT_SIZE
    max_images = int(flags.get("num", "4"))
    refs = [a for a in args[1:] if not a.startswith("-")] if len(args) > 1 else []

    gen = DoubaoImageGenerator()
    _print_status_header(gen)

    # 预选模型用于显示
    selected = gen._select_available_model(flags.get("model"))
    if not selected:
        _print_result(gen._all_models_exhausted_error(flags.get("model")))
        return

    mode = "融合" if len(refs) >= 2 and max_images == 1 else ("图生组图" if refs else "文生组图")
    print(f"\n🔄 {mode}")
    print(f"   模型:   {selected['name']}")
    print(f"   提示词: {prompt}")
    print(f"   张数:   {max_images}")
    if refs:
        print(f"   参考图: {len(refs)} 张")
    print(f"   尺寸:   {size}")
    print(f"   正在生成...")

    result = gen.generate_sequence(prompt, max_images=max_images, image_urls=refs if refs else None, size=size, ratio=flags.get("ratio"), force_model=selected["name"], watermark=not flags.get("no_watermark"))
    _print_result(result)


def _cmd_sync(args: List[str]):
    """控制台用量查询并同步。不带参数自动查，带参数手动设。"""
    gen = DoubaoImageGenerator()

    if not args:
        # 自动模式：从控制台查询并同步
        print(f"\n🔄 控制台用量查询中...")
        if not gen._console.enabled:
            print("❌ IAM 密钥未配置，请在 .env 中设置 VOLCENGINE_ACCESS_KEY 和 VOLCENGINE_SECRET_KEY")
            return

        before = {m["name"]: m["count"] for m in gen.get_status()["models"]}
        console_counts = gen._console.query_today_image_counts()

        if not console_counts or sum(console_counts.values()) == 0:
            print("⚠️  控制台返回无数据")
            return

        print(f"\n   对比 (本地 → 控制台)")
        updated = False
        for name, console_count in console_counts.items():
            local_count = before.get(name, 0)
            arrow = "↑" if console_count > local_count else "→" if console_count == local_count else "↓"
            print(f"   {name}: {local_count} {arrow} {console_count}")

        gen._console.sync_to_local(gen.history)
        print(f"\n   同步后:")
        for m in gen.get_status()["models"]:
            print(f"   {m['name']}: {m['count']}/{m['limit']}")
        return

    # 手动模式：手动指定控制台用量
    console_counts = {}
    for arg in args:
        parts = arg.split("=", 1)
        if len(parts) == 2:
            console_counts[parts[0].strip()] = int(parts[1].strip())

    print(f"\n🔄 手动同步")
    before = {m["name"]: m["count"] for m in gen.get_status()["models"]}
    result = gen._console.sync_to_local(gen.history)

    for model_name, action in result.items():
        icon = "✅" if "synced" in str(action) else "📌"
        print(f"   {icon} {model_name}: {action}")

    print(f"\n   同步后:")
    for m in gen.get_status()["models"]:
        print(f"   {m['name']}: {m['count']}/{m['limit']}")


def _cmd_history():
    """查看历史记录。"""
    gen = DoubaoImageGenerator()
    records = gen.get_history()
    print(f"\n📋 历史记录 (共 {len(records)} 条, 保留 {HISTORY_RETENTION_DAYS} 天)")
    print(f"   {'─' * 60}")
    for r in records[-20:]:  # 最近 20 条
        mode_icon = "🎨" if r.get("mode") == "text-to-image" else "🖼️"
        print(f"   {mode_icon} {r.get('datetime', '?')} | {r.get('model', '?')}")
        print(f"      Prompt: {r.get('prompt', '?')[:60]}...")
        print(f"      Size: {r.get('resolution', '?')} | Ratio: {r.get('ratio', '?')}")
        if r.get("reference_image"):
            print(f"      Ref: {r['reference_image'][:60]}...")


def _cmd_test():
    """运行自检（不调用 API）。"""
    print("\n🧪 运行自检...\n")

    gen = DoubaoImageGenerator()
    ok = 0
    total = 0

    # 测试 1: 状态查询
    total += 1
    try:
        status = gen.get_status()
        print(f"   ✅ 状态查询: {len(status['models'])} 个模型")
        ok += 1
    except Exception as e:
        print(f"   ❌ 状态查询: {e}")

    # 测试 2: 尺寸解析
    total += 1
    try:
        cases = [
            ("2K",    ("2K", 2048, 2048, "1:1", "preset")),
            ("4K",    ("4K", 4096, 4096, "1:1", "preset")),
            ("16:9",  ("2560x1440", 2560, 1440, "16:9", "aspect")),
            ("1:1",   ("2048x2048", 2048, 2048, "1:1", "aspect")),
            ("1024x1024", ("1024x1024", 1024, 1024, "1:1", "custom")),
            ("invalid", ("2K", 2048, 2048, "1:1", "fallback")),
        ]
        all_ok = True
        for inp, expected in cases:
            result = DoubaoImageGenerator._parse_size(inp)
            # Compare key fields
            if result[0] != expected[0] or result[1] != expected[1] or result[2] != expected[2]:
                all_ok = False
                print(f"      ⚠️  {inp} → {result[0]} {result[1]}x{result[2]} (期望 {expected[0]} {expected[1]}x{expected[2]})")
        if all_ok:
            print(f"   ✅ 尺寸解析: {len(cases)} 个测试通过")
            ok += 1
        else:
            print(f"   ⚠️ 尺寸解析: 部分不匹配")
    except Exception as e:
        print(f"   ❌ 尺寸解析: {e}")

    # 测试 3: 跳过（触发词检测已移至 SKILL.md）

    # 测试 4: URL 提取
    total += 1
    try:
        cases = [
            ("图生图 换背景 https://example.com/photo.jpg", "https://example.com/photo.jpg"),
            ("img2img edit https://cdn.test.com/img.png?w=100", "https://cdn.test.com/img.png?w=100"),
            ("文生图 一只猫", None),
            ("generate a cat", None),
        ]
        all_ok = True
        for inp, exp in cases:
            got = extract_image_url(inp)
            if got != exp:
                all_ok = False
                print(f"      ⚠️  '{inp}' → {got} (期望 {exp})")
        if all_ok:
            print(f"   ✅ URL 提取: {len(cases)} 个测试通过")
            ok += 1
        else:
            print(f"   ⚠️ URL 提取: 部分不匹配")
    except Exception as e:
        print(f"   ❌ URL 提取: {e}")

    # 测试 5: 历史记录
    total += 1
    try:
        count = gen.get_total_history_count()
        print(f"   ✅ 历史记录: {count} 条")
        ok += 1
    except Exception as e:
        print(f"   ❌ 历史记录: {e}")

    print(f"\n   {'─' * 40}")
    print(f"   结果: {ok}/{total} 通过")
    print(f"   API Key 已配置: {'是' if gen.api_key else '否'}")


def _print_status_header(gen: DoubaoImageGenerator):
    """打印当前模型状态（先生成前同步控制台）。"""
    gen._auto_console_sync()
    status = gen.get_status()
    print(f"\n📊 {status['date']}")
    for m in status["models"]:
        icon = "🟢" if m["available"] else "🔴"
        print(f"   {icon} {m['name']}: {m['count']}/{m['limit']}")


def _print_result(result: Dict):
    """打印生成结果。"""
    if result["success"]:
        print(f"\n✅ 生成成功!")
        print(f"   模式:     {result.get('mode', 'text-to-image')}")
        print(f"   模型:     {result['model']}")
        print(f"   今日:     {result['count_today']}/{result['limit']}")
        print(f"   分辨率:   {result.get('resolution', 'adaptive')}")
        print(f"   比例:     {result.get('ratio', '-')}")
        pixels = result.get('pixels', 0)
        if pixels:
            print(f"   像素:     {pixels:,}")
        # 单图/组图兼容
        if 'image_urls' in result:
            print(f"   图片:     {len(result['image_urls'])} 张")
            for lp in result.get("local_paths", []):
                print(f"   文件:     {lp}")
        elif 'image_url' in result:
            lp = result.get('local_path', '')
            if lp:
                print(f"   文件:     {lp}")
            else:
                print(f"   ⚠️ 下载失败，仅远程URL: {result['image_url']}")
    else:
        print(f"\n❌ 生成失败: {result.get('error', '未知错误')}")
        if "status" in result:
            for name, s in result["status"].items():
                print(f"   {name}: {s['count']}/{18}")


def _progress_bar(count: int, limit: int, width: int = 20) -> str:
    """生成进度条字符串。"""
    filled = int(width * count / limit)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}]"


# ============================================================
# 模块入口
# ============================================================

if __name__ == "__main__":
    main()
