#!/usr/bin/env python3
"""
Doubao Vision Recognize v5.0.1
================================
Image/Video → Text/Code
  img-to-text     Doubao*6→GLM-4.6V→GLM-4.1V
  video-to-text   Doubao*6→GLM-4.6V→GLM-4.1V
  img-to-code     Doubao*5→GLM-4.6V→GLM-4.1V
  video-to-code   Doubao*5 (GLM unsupported)

Backends: Doubao Responses API + Zhipu Chat Completions API
Auto-syncs Volcengine IAM console token usage on each recognition.
"""

import base64
import hashlib
import hmac
import json
import os
import shutil
import ssl
import sys
import time

import unicodedata
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Default config (auto-generated config.json on first run)
_CONFIG_DEFAULTS = {
    "provider_mode":            0,
    "temp_retention_days":      7,
    "ark_api_key":              "",
    "doubao_seed_21p_id":     "",
    "doubao_seed_21t_id":     "",
    "doubao_seed_20p_id":     "",
    "doubao_seed_20c_id":     "",
    "doubao_seed_20l_id":     "",
    "doubao_seed_20m_id":     "",
    "volcengine_access_key":    "",
    "volcengine_secret_key":    "",
    "zhipu_api_key":            "",
    "privacy_notice_shown":     False,
}

_CONFIG_DESCRIPTIONS = {
    "provider_mode":            "0=all 1=Zhipu only 2=Doubao only",
    "temp_retention_days":      "Temp cache retention days (1-3650)",
    "ark_api_key":              "Volcengine Ark API Key",
    "doubao_seed_21p_id":     "Doubao-Seed-2.1-Pro endpoint ID",
    "doubao_seed_21t_id":     "Doubao-Seed-2.1-Turbo endpoint ID",
    "doubao_seed_20p_id":     "Doubao-Seed-2.0-Pro endpoint ID",
    "doubao_seed_20c_id":     "Doubao-Seed-2.0-Code endpoint ID",
    "doubao_seed_20l_id":     "Doubao-Seed-2.0-Lite endpoint ID",
    "doubao_seed_20m_id":     "Doubao-Seed-2.0-Mini endpoint ID",
    "volcengine_access_key":    "Volcengine IAM Access Key (optional)",
    "volcengine_secret_key":    "Volcengine IAM Secret Key (optional)",
    "zhipu_api_key":            "Zhipu API Key (free models)",
    "privacy_notice_shown":     "Privacy notice acknowledged (auto-set on first run)",
}

_PATH = Path(__file__).resolve().parent
_CONFIG_PATH = _PATH / "config.json"

# First run: auto-generate config.json with plaintext storage warning
if not _CONFIG_PATH.exists():
    meta = {"_comment": "⚠️ API keys stored in plaintext! Do not use on shared/backed-up/synced machines. Fill in values below, leave blank to disable."}
    config = dict(meta, **_CONFIG_DEFAULTS)
    with open(_CONFIG_PATH, "w", encoding="utf-8", newline="\n") as _f:
        json.dump(config, _f, ensure_ascii=False, indent=2)
        _f.write("\n")

# Load config
_cfg = {}
if _CONFIG_PATH.exists():
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as _f:
            _cfg = json.load(_f)
    except Exception:
        pass

API_URL = "https://ark.cn-beijing.volces.com/api/v3/responses"
ARK_API_KEY = _cfg.get("ark_api_key", "")
IAM_AK = _cfg.get("volcengine_access_key", "")
IAM_SK = _cfg.get("volcengine_secret_key", "")
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_API_KEY = _cfg.get("zhipu_api_key", "")
_PROVIDER_MODE = _cfg.get("provider_mode", 0)
_TEMP_RETENTION = max(1, min(3650, _cfg.get("temp_retention_days", 7)))
SYNC_INTERVAL = 30 * 60


def _show_privacy_notice():
    """Show privacy notice on first run and record acknowledgement"""
    if not _cfg.get("privacy_notice_shown", False):
        print("\n".join([
            "",
            "╔═══════════════════ Privacy & Data Notice ═══════════════════╗",
            "║ • Selected images/videos and prompts are base64-encoded     ║",
            "║   and sent to Volcengine (Doubao) or Zhipu (GLM) cloud APIs ║",
            "║ • API keys are stored in plaintext config.json              ║",
            "║ • Media cached in Temp/ (default 7-day retention)            ║",
            "║ • History in vision_history.json, context in .last_response  ║",
            "║ • Continuing past this notice acknowledges above practices  ║",
            "╚══════════════════════════════════════════════════════════════╝",

            "",
        ]))
        _cfg["privacy_notice_shown"] = True
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as _f:
                data = json.load(_f)
            data["privacy_notice_shown"] = True
            with open(_CONFIG_PATH, "w", encoding="utf-8", newline="\n") as _f:
                json.dump(data, _f, ensure_ascii=False, indent=2)
                _f.write("\n")
        except Exception:
            pass
SYNC_INTERVAL = 30 * 60
RETENTION_DAYS = 7
TIMEOUT = 300
MAX_IMG = 15 * 1024 * 1024
MAX_VID = 50 * 1024 * 1024
MAX_PAYLOAD = 64 * 1024 * 1024
DAILY_LIMIT = 1_800_000

# 按模式控制思考深度: text 模式轻思考(low)节省Token，code 模式均衡(medium)保证质量
_REASONING_EFFORT = {
    "img-to-text": "low",
    "video-to-text": "low",
    "img-to-code": "medium",
    "video-to-code": "medium",
}

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = Path(os.environ.get("VISION_HISTORY_FILE", str(BASE_DIR / "vision_history.json")))
TEMP_DIR = Path(os.environ.get("VISION_TEMP_DIR", str(BASE_DIR / "Temp")))
def _today_dir() -> Path:
    """返回今天的缓存子目录（Temp/YYYYMMDD）"""
    d = TEMP_DIR / datetime.now().strftime("%Y%m%d")
    d.mkdir(parents=True, exist_ok=True)
    return d
LAST_RESP_FILE = BASE_DIR / ".last_response"
ssl_ctx = ssl.create_default_context()

_MODELS = {
    "21PRO":  {"name": "Doubao-Seed-2.1-Pro",   "id": _cfg.get("doubao_seed_21p_id", ""),  "env": "doubao_seed_21p_id", "provider": "doubao"},
    "21TURBO":{"name": "Doubao-Seed-2.1-Turbo", "id": _cfg.get("doubao_seed_21t_id", ""),  "env": "doubao_seed_21t_id", "provider": "doubao"},
    "20PRO":  {"name": "Doubao-Seed-2.0-Pro",   "id": _cfg.get("doubao_seed_20p_id", ""),  "env": "doubao_seed_20p_id", "provider": "doubao"},
    "20CODE": {"name": "Doubao-Seed-2.0-Code",  "id": _cfg.get("doubao_seed_20c_id", ""),  "env": "doubao_seed_20c_id", "provider": "doubao"},
    "20LITE": {"name": "Doubao-Seed-2.0-Lite",  "id": _cfg.get("doubao_seed_20l_id", ""),  "env": "doubao_seed_20l_id", "provider": "doubao"},
    "20MINI": {"name": "Doubao-Seed-2.0-Mini",  "id": _cfg.get("doubao_seed_20m_id", ""),  "env": "doubao_seed_20m_id", "provider": "doubao"},
    "GLM46V": {"name": "GLM-4.6V-Flash",        "id": "glm-4.6v-flash" if ZHIPU_API_KEY else "",  "env": "ZHIPU_API_KEY",       "provider": "zhipu", "retries": 10},
    "GLM41V": {"name": "GLM-4.1V-Thinking-Flash","id": "glm-4.1v-thinking-flash" if ZHIPU_API_KEY else "", "env": "ZHIPU_API_KEY", "provider": "zhipu", "retries": 5},
}

def _validate_models():
    """延迟校验：任意配置一个模型 ID 即可运行。_select_model 会跳过空 ID。"""
    if not any(m["id"] for m in _MODELS.values()):
        raise RuntimeError("No models configured. Fill in at least one API Key or endpoint ID in config.json.")

_MAX_NAME_W = max(len(m["name"]) for m in _MODELS.values())


def _pad_name(name: str) -> str:
    return name + ' ' * (_MAX_NAME_W - len(name))


_MODES = {
    "img-to-text":   {"label": "Image→Text", "chain": ["21PRO", "21TURBO", "20PRO", "20CODE", "20LITE", "20MINI", "GLM46V", "GLM41V"]},
    "video-to-text": {"label": "Video→Text", "chain": ["21PRO", "21TURBO", "20PRO", "20CODE", "20LITE", "20MINI", "GLM46V", "GLM41V"]},
    "img-to-code":   {"label": "Image→Code", "chain": ["21PRO", "21TURBO", "20CODE", "20PRO", "20LITE", "GLM46V", "GLM41V"]},
    "video-to-code": {"label": "Video→Code", "chain": ["21PRO", "21TURBO", "20CODE", "20PRO", "20LITE"]},
}

_MODE_MAP = {
    ("image", "text"): "img-to-text",
    ("video", "text"): "video-to-text",
    ("image", "code"): "img-to-code",
    ("video", "code"): "video-to-code",
}

_MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff",
              ".mp4", ".mov", ".webm", ".avi", ".mkv", ".flv", ".wmv"}

SP_VISION = """You are a professional visual recognition and analysis assistant. Carefully observe the provided image/video content and follow these rules:

[General Rules] (priority from high to low)
1. Completeness: Analyze all visual elements including graphics, text, tables, and scenes without omitting key content.
2. Relevance: Results must exactly match the user's specific requirements. Exclude redundant content not requested.
3. Formatting: Use Markdown for extracted text/tables. Tables must be standard Markdown format. Formulas must be standard LaTeX.
4. Default: If no specific instructions, output a concise natural-language scene description.

[Post-Check]
1. Confirm no extraneous content not requested by user.
2. Verify all Markdown-formatted content is correctly formatted.
3. Ensure descriptions match the actual content without speculation."""

SP_VIDEO = """You are a professional video content analysis assistant. Carefully observe the provided video and follow these rules:

[General Rules] (priority from high to low)
1. Completeness: First map the full narrative logic or workflow, then organize results as "core content → key details → summary".
2. Relevance: Results must exactly match the user's specific requirements.
3. Timestamps: Mark all distinct time points or steps with precise second-level timestamps.
4. Default: If no specific instructions, output within 300 words in plain natural language.

[Post-Check]
1. Confirm no extraneous content not requested by user.
2. Verify all timestamps are present and precise.
3. Ensure output format matches everyday reading habits."""

SP_IMG_CODE = """You are a professional UI design-to-code assistant. Carefully observe the provided image and follow these rules:

[General Rules] (priority from high to low)
1. Completeness: Fully replicate the UI layout, detail styles, and interactive element visuals without omissions.
2. Relevance: Generated code tech stack must exactly match user-specified stack.
3. Formatting: Use semantic HTML tags, BEM-style CSS classes, clear structure, and key-point comments.
4. Responsive: Code must adapt to both desktop and mobile, maintaining visual consistency.
5. Default: If no stack specified, use HTML+TailwindCSS. Do not add unnecessary JS.

[Post-Check]
1. Confirm tech stack matches user requirements exactly.
2. Confirm no extraneous code not requested by user.
3. Confirm all images use reasonable placeholders.
4. Confirm formatting meets industry standards and has no syntax errors.
5. Confirm visual output closely matches the original image."""

SP_VIDEO_CODE = """You are a professional video-to-code assistant. Carefully observe the provided video (UI demo, screen recording, app walkthrough, etc.) and follow these rules:

[General Rules] (priority from high to low)
1. Completeness: Fully replicate UI layouts, page structures, interaction flows, and visual styles without omissions.
2. Relevance: Generated code tech stack must exactly match user-specified stack.
3. Formatting: Use semantic HTML tags, BEM-style CSS classes, clear structure, and key-point comments.
4. Responsive: Code must adapt to both desktop and mobile, maintaining visual consistency.
5. Default: If no stack specified, use HTML+TailwindCSS. Do not add unnecessary JS.

[Post-Check]
1. Confirm tech stack matches user requirements exactly.
2. Confirm no extraneous code not requested by user.
3. Confirm all images use reasonable placeholders.
4. Confirm formatting meets industry standards and has no syntax errors.
5. Confirm visual output closely matches the video content."""

_SP_MAP = {
    "img-to-text": SP_VISION,
    "video-to-text": SP_VIDEO,
    "img-to-code": SP_IMG_CODE,
    "video-to-code": SP_VIDEO_CODE,
}


class ConsoleSyncer:
    """Volcengine console usage sync via IAM HMAC-SHA256 signed GetInferenceUsage API"""
    def __init__(self):
        self._ak = IAM_AK
        self._sk = IAM_SK
        self._enabled = bool(self._ak and self._sk)
        self._last_sync = 0

    @property
    def enabled(self):
        return self._enabled

    def _sign(self, key: bytes, msg: str) -> bytes:
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def _build_auth(self, action: str, payload_str: str):
        svc, region, host = "ark", "cn-beijing", "open.volcengineapi.com"
        now = datetime.now(timezone.utc)
        ds = now.strftime("%Y%m%d")
        xd = now.strftime("%Y%m%dT%H%M%SZ")
        q = f"Action={action}&Version=2024-01-01"
        csha = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        ch = f"content-type:application/json; charset=UTF-8\nhost:{host}\nx-content-sha256:{csha}\nx-date:{xd}\n"
        sh = "content-type;host;x-content-sha256;x-date"
        cr = f"POST\n/\n{q}\n{ch}\n{sh}\n{csha}"
        cs = f"{ds}/{region}/{svc}/request"
        sts = f"HMAC-SHA256\n{xd}\n{cs}\n{hashlib.sha256(cr.encode('utf-8')).hexdigest()}"
        kd = self._sign(self._sk.encode("utf-8"), ds)
        kr = self._sign(kd, region)
        ks = self._sign(kr, svc)
        ksg = self._sign(ks, "request")
        sig = hmac.new(ksg, sts.encode("utf-8"), hashlib.sha256).hexdigest()
        auth = f"HMAC-SHA256 Credential={self._ak}/{cs}, SignedHeaders={sh}, Signature={sig}"
        return {"Authorization": auth, "Content-Type": "application/json; charset=UTF-8",
                "Host": host, "X-Date": xd, "X-Content-Sha256": csha}, q

    def _post(self, url, headers, data, timeout=30):
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as r:
                return r.status, json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            b = e.read().decode("utf-8", errors="replace")
            return e.code, json.loads(b) if b else {}

    def query_today(self):
        if not self._enabled:
            return {}
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            ids = [m["id"] for m in _MODELS.values() if m.get("provider", "doubao") == "doubao"]
            payload = {"QueryInterval": "Hour", "StartTime": yesterday, "EndTime": today,
                       "Filters": [{"Key": "ModelEndpoint", "Values": ids}]}
            ps = json.dumps(payload)
            hdrs, q = self._build_auth("GetInferenceUsage", ps)
            st, res = self._post(f"https://open.volcengineapi.com/?{q}", hdrs, ps.encode("utf-8"))
            if st != 200 or "Result" not in res:
                return {}
            fields = [f["Name"] for f in res["Result"].get("Fields", [])]
            data = res["Result"].get("Data", [])
            if "ModelEndpoint" not in fields or "TotalTokens" not in fields:
                return {}
            ei, ti = fields.index("ModelEndpoint"), fields.index("TotalTokens")
            nmap = {m["id"]: m["name"] for m in _MODELS.values()}
            counts: Dict[str, int] = {}
            for row in data:
                name = nmap.get(str(row[ei]) if ei < len(row) else "")
                if name:
                    counts[name] = counts.get(name, 0) + int(row[ti] or 0)
            return counts
        except Exception:
            return {}

    def sync_to_local(self, hm: "HistoryManager"):
        if not self._enabled or (time.time() - self._last_sync) < SYNC_INTERVAL:
            return {}
        self._last_sync = time.time()
        pc = self.query_today()
        if not pc or sum(pc.values()) == 0:
            return {}
        return hm.sync_from_console(pc)


class HistoryManager:
    """本地调用历史与 Token 用量管理器 — JSON 文件持久化，7天自动清理"""
    def __init__(self, path: Path):
        self.path = path
        self.data = self._load()
        self._clean()

    def _load(self) -> Dict:
        if not self.path.exists():
            return {"history": [], "daily_tokens": {}}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                d = json.load(f)
                d.setdefault("history", [])
                d.setdefault("daily_tokens", {})
                return d
        except (json.JSONDecodeError, IOError):
            return {"history": [], "daily_tokens": {}}

    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        tmp.replace(self.path)

    def _clean(self):
        cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
        cts, cds = cutoff.timestamp(), cutoff.strftime("%Y-%m-%d")
        self.data["history"] = [r for r in self.data["history"] if r.get("timestamp", 0) >= cts]
        self.data["daily_tokens"] = {d: c for d, c in self.data["daily_tokens"].items() if d >= cds}

    @staticmethod
    def _today():
        return datetime.now().strftime("%Y-%m-%d")

    def get_daily(self, name: str) -> int:
        return self.data.setdefault("daily_tokens", {}).setdefault(self._today(), {}).get(name, 0)

    def add_tokens(self, name: str, tokens: int) -> int:
        self._clean()
        c = self.data.setdefault("daily_tokens", {}).setdefault(self._today(), {})
        c[name] = c.get(name, 0) + tokens
        self._save()
        return c[name]

    def add_record(self, rec: Dict):
        self._clean()
        self.data.setdefault("history", []).append(rec)
        self._save()

    def get_status(self) -> Dict:
        today = self._today()
        models = []
        for m in _MODELS.values():
            configured = bool(m["id"]) and m["id"].strip() != "*"
            unlimited = m.get("provider") == "zhipu"
            models.append({
                "name": m["name"],
                "tokens": self.get_daily(m["name"]) if configured else 0,
                "limit": DAILY_LIMIT if not unlimited else -1,
                "configured": configured,
                "unlimited": unlimited,
            })
        return {
            "date": today,
            "total_history": len(self.data.get("history", [])),
            "models": models,
        }

    def sync_from_console(self, console: Dict[str, int]) -> Dict[str, str]:
        lc = self.data.setdefault("daily_tokens", {}).setdefault(self._today(), {})
        result = {}
        for name, cv in console.items():
            lv = lc.get(name, 0)
            if cv > lv:
                lc[name] = cv
                result[name] = "synced"
            else:
                result[name] = "kept_local"
        self._save()
        return result

    def get_history(self) -> List[Dict]:
        return self.data.get("history", [])


class DoubaoVisionRecognizer:
    """Core recognition engine — model selection, media encoding, API calls, result extraction"""
    def __init__(self):
        _validate_models()
        _show_privacy_notice()
        self.api_key = ARK_API_KEY
        self.history = HistoryManager(HISTORY_FILE)
        self._console = ConsoleSyncer()
        self._auto_sync()

    def _auto_sync(self):
        """Auto-sync IAM console usage on each recognition if IAM keys are configured"""
        if self._console.enabled:
            self._console.sync_to_local(self.history)
        self._cleanup_temp()

    def _cleanup_temp(self):
        """清理 Temp 下超过 TEMP_RETENTION_DAYS 天的日期子目录"""
        try:
            if not TEMP_DIR.exists():
                return
            cutoff = (datetime.now() - timedelta(days=_TEMP_RETENTION)).strftime("%Y%m%d")
            for d in TEMP_DIR.iterdir():
                if d.is_dir() and len(d.name) == 8 and d.name.isdigit() and d.name < cutoff:
                    shutil.rmtree(d, ignore_errors=True)
        except Exception:
            pass

    def _post(self, url, headers, data, timeout=TIMEOUT):
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8", errors="replace")

    def _select_model(self, mode_key: str) -> Optional[Dict]:
        """Select first non-over-limit model from fallback chain (filtered by PROVIDER_MODE)"""
        for mk in _MODES[mode_key]["chain"]:
            spec = _MODELS[mk]
            if not spec["id"]:
                continue
            # Provider filter: 1=Zhipu only, 2=Doubao only
            if _PROVIDER_MODE == 1 and spec["provider"] == "doubao":
                continue
            if _PROVIDER_MODE == 2 and spec["provider"] == "zhipu":
                continue
            if self.history.get_daily(spec["name"]) < DAILY_LIMIT:
                return {"key": mk, "name": spec["name"], "id": spec["id"], "provider": spec["provider"],
                        "retries": spec.get("retries", 0)}
        return None

    def _encode_media(self, file_path: str, input_type: str) -> Tuple[str, str, str]:
        """读取文件→Base64编码→生成data URI"""
        src = Path(file_path)
        if not src.is_file():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        ext = src.suffix.lower()
        raw = src.read_bytes()
        if input_type == "image":
            max_b, media = MAX_IMG, "image"
        elif input_type == "video":
            max_b, media = MAX_VID, "video"
        else:
            raise ValueError("必须指定输入类型: --image 或 --video")
        if len(raw) > max_b:
            raise ValueError(f"文件过大 ({len(raw)/1024/1024:.1f} MB)，最大 {max_b/1024/1024:.0f} MB")
        td = _today_dir()
        tmp = td / f"v_{hashlib.md5(str(src).encode()).hexdigest()[:12]}{ext}"
        shutil.copy2(src, tmp)
        fmt = ext.lstrip(".")
        if fmt == "jpg":
            fmt = "jpeg"
        elif fmt not in ("png", "jpeg", "webp", "bmp", "gif", "tiff", "mp4", "mov", "webm"):
            fmt = "png" if media == "image" else "mp4"
        b64 = base64.b64encode(raw).decode("ascii")
        payload_est = len(b64) + 2048
        if payload_est > MAX_PAYLOAD:
            raise ValueError(f"请求体过大 ({payload_est/1024/1024:.1f} MB)，API 上限 64 MB，请压缩文件后重试")
        return f"data:{media}/{fmt};base64,{b64}", str(tmp), media

    def _build_blocks(self, media: str, data_uri: str, prompt: str, output_type: str) -> List[Dict]:
        """构建多模态 API 的 content blocks — text模式用low细节省Token，code模式用high保证精度"""
        blocks = []
        if media == "image":
            detail = "low" if output_type == "text" else "high"
            blocks.append({"type": "input_image", "image_url": data_uri, "detail": detail})
        else:
            blocks.append({"type": "input_video", "video_url": data_uri, "fps": 1.0})
        blocks.append({"type": "input_text", "text": prompt})
        return blocks

    # ── GLM / Zhipu API Backend ────────────────────────────────────────

    def _build_zhipu_blocks(self, media: str, data_uri: str, prompt: str, sp: str) -> List[Dict]:
        """构建智谱 Chat Completions API 的 content blocks"""
        blocks = []
        if media == "image":
            blocks.append({"type": "image_url", "image_url": {"url": data_uri}})
        else:
            blocks.append({"type": "video_url", "video_url": {"url": data_uri}})
        blocks.append({"type": "text", "text": sp + "\n" + prompt})
        return blocks

    def _zhipu_call(self, model_info: Dict, messages: List[Dict],
                     retries: int = 5, interval: float = 1.0) -> Tuple[Optional[Dict], str]:
        """调用智谱 API，自动重试处理 429/502/503"""
        headers = {"Authorization": f"Bearer {ZHIPU_API_KEY}",
                   "Content-Type": "application/json"}
        payload = {"model": model_info["id"], "messages": messages,
                   "thinking": {"type": "enabled"}, "stream": False}
        last_error = ""
        for attempt in range(retries + 1):
            if attempt > 0:
                print(f"   ⚠️ Retry {attempt}/{retries} (1s)...")
                time.sleep(interval)
            try:
                st, body = self._post(ZHIPU_API_URL, headers, json.dumps(payload).encode("utf-8"))
                if st == 200:
                    return json.loads(body), ""
                elif st in (429, 502, 503):
                    last_error = f"HTTP {st}"
                    continue
                else:
                    return None, f"Zhipu API request failed (HTTP {st}): {body[:300]}"
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                continue
        return None, f"Zhipu API failed after {retries} retries: {last_error}"

    @staticmethod
    def _extract_zhipu_text(res: Dict) -> str:
        """从智谱 API 响应中提取文本"""
        for c in res.get("choices", []):
            msg = c.get("message", {})
            if msg.get("role") == "assistant":
                return msg.get("content", "")
        return ""

    @staticmethod
    def _extract_zhipu_tokens(res: Dict) -> Dict:
        """从智谱 API 响应中提取 Token 用量"""
        u = res.get("usage", {})
        return {
            "input_tokens": u.get("prompt_tokens", 0),
            "output_tokens": u.get("completion_tokens", 0),
            "total_tokens": u.get("total_tokens", 0),
            "reasoning_tokens": u.get("completion_tokens_details", {}).get("reasoning_tokens", 0),
            "cached_tokens": u.get("prompt_tokens_details", {}).get("cached_tokens", 0),
        }

    # ── 通用方法 ────────────────────────────────────────────────────

    def _resolve_prompt(self, mode_key: str, user_prompt: str) -> str:
        """Assemble final prompt: system preset + user instruction"""
        sp = _SP_MAP.get(mode_key, SP_VISION)
        if not user_prompt or not user_prompt.strip():
            if mode_key.endswith("-to-text"):
                return sp + "\nDescribe the content in detail."
            return sp + "\nGenerate frontend code based on the content (HTML+TailwindCSS)."
        return sp + f"\n\nUser instruction: {user_prompt}"

    def _extract_tokens(self, res: Dict) -> Dict:
        u = res.get("usage", {})
        return {
            "input_tokens": u.get("input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0),
            "total_tokens": u.get("total_tokens", 0),
            "reasoning_tokens": u.get("output_tokens_details", {}).get("reasoning_tokens", 0),
            "cached_tokens": u.get("input_tokens_details", {}).get("cached_tokens", 0),
        }

    def _extract_text(self, res: Dict) -> str:
        for o in res.get("output", []):
            if o.get("type") == "message":
                for c in o.get("content", []):
                    if c.get("type") == "output_text":
                        return c.get("text", "")
        return ""

    def process(self, file_path: str, input_type: str, output_type: str, prompt: str = "") -> Dict:
        """Main processing: encode → iterate fallback chain → call API (Doubao/GLM) → record on success"""
        self._cleanup_temp()
        mode = _MODE_MAP.get((input_type, output_type))
        if not mode:
            return {"success": False, "error": "Invalid input/output type. Use --image/--video + --text/--code"}
        if not file_path or not Path(file_path).is_file():
            return {"success": False, "error": "Please provide an image or video file path."}
        try:
            data_uri, tmp_path, media = self._encode_media(file_path, input_type)
        except (FileNotFoundError, ValueError) as e:
            return {"success": False, "error": str(e)}
        md = _MODES[mode]
        full_prompt = self._resolve_prompt(mode, prompt)
        sp = _SP_MAP.get(mode, SP_VISION)

        print(f"\n🔍 {md['label']}")
        print(f"   File: {Path(file_path).name} ({media})")
        if prompt:
            print(f"   Prompt: {prompt[:80]}...")

        last_error = ""
        for mk in _MODES[mode]["chain"]:
            spec = _MODELS[mk]
            if not spec["id"] or spec["id"].strip() == "*":
                continue
            if _PROVIDER_MODE == 1 and spec["provider"] == "doubao":
                continue
            if _PROVIDER_MODE == 2 and spec["provider"] == "zhipu":
                continue
            if self.history.get_daily(spec["name"]) >= DAILY_LIMIT:
                continue
            model = {"key": mk, "name": spec["name"], "id": spec["id"],
                     "provider": spec["provider"], "retries": spec.get("retries", 0)}
            provider = model["provider"]
            print(f"   → {model['name']} ({provider})")

            if provider == "zhipu":
                blocks = self._build_zhipu_blocks(media, data_uri, full_prompt, sp)
                messages = [{"role": "user", "content": blocks}]
                result, error = self._zhipu_call(model, messages, retries=model["retries"])
                if result is None:
                    print(f"   ✗ {model['name']}: {error[:80]}")
                    last_error = error
                    continue
                tokens = self._extract_zhipu_tokens(result)
                text = self._extract_zhipu_text(result)
                resp_id = result.get("id", "")
                self._save_glm_context(resp_id, model["id"], input_type, file_path,
                                        messages, text, mode)
            else:
                thinking_cfg = {"type": "enabled", "reasoning_effort": _REASONING_EFFORT[mode]}
                doubao_blocks = self._build_blocks(media, data_uri, full_prompt, output_type)
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {"model": model["id"], "input": [{"role": "user", "content": doubao_blocks}],
                           "thinking": thinking_cfg, "caching": {"type": "enabled"}}
                try:
                    st, body = self._post(API_URL, headers, json.dumps(payload).encode("utf-8"))
                except Exception as e:
                    print(f"   ✗ {model['name']}: {e}")
                    last_error = f"{type(e).__name__}: {e}"
                    continue
                if st != 200:
                    last_error = f"HTTP {st}"
                    print(f"   ✗ {model['name']}: HTTP {st}")
                    continue
                result = json.loads(body)
                tokens = self._extract_tokens(result)
                text = self._extract_text(result)
                resp_id = result.get("id", "")
                self._save_last_resp(resp_id, model["id"], input_type, file_path, provider)

            new_total = self.history.add_tokens(model["name"], tokens["total_tokens"])
            ts = time.time()
            self.history.add_record({
                "timestamp": ts, "datetime": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
                "mode": mode, "model": model["name"], "model_id": model["id"],
                "provider": provider,
                "file": file_path, "prompt": prompt or "(auto)",
                "input_tokens": tokens["input_tokens"], "output_tokens": tokens["output_tokens"],
                "total_tokens": tokens["total_tokens"], "reasoning_tokens": tokens["reasoning_tokens"],
                "cached_tokens": tokens["cached_tokens"], "response": text[:500],
            })
            limit = -1 if provider == "zhipu" else DAILY_LIMIT
            remaining = -1 if provider == "zhipu" else DAILY_LIMIT - new_total
            return {
                "success": True, "mode": mode, "model": model["name"],
                "file": file_path, "prompt": prompt or "(auto)", "tokens": tokens,
                "total_today": new_total, "limit": limit,
                "remaining": remaining, "response": text, "resp_id": resp_id,
            }

        return {"success": False,
                "error": f"All models failed for {md['label']}: {last_error or 'no available models'}"}

    def _save_last_resp(self, resp_id: str, model_id: str, input_type: str, file_path: str,
                         provider: str = "doubao"):
        """Save last response context for follow-up"""
        try:
            data = {"resp_id": resp_id, "model_id": model_id,
                    "input_type": input_type, "file": file_path,
                    "provider": provider, "ts": time.time()}
            tmp = LAST_RESP_FILE.with_suffix(".json.tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            tmp.replace(LAST_RESP_FILE)
        except Exception:
            pass

    def _save_glm_context(self, resp_id: str, model_id: str, input_type: str,
                           file_path: str, messages: List[Dict], assistant_text: str,
                           mode: str):
        """Save GLM multi-turn chat context (message history + last reply) for follow-up"""
        try:
            data = {"resp_id": resp_id, "model_id": model_id,
                    "input_type": input_type, "file": file_path,
                    "provider": "zhipu", "mode": mode,
                    "messages": messages,
                    "last_text": assistant_text,
                    "ts": time.time()}
            tmp = LAST_RESP_FILE.with_suffix(".json.tmp")
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            tmp.replace(LAST_RESP_FILE)
        except Exception:
            pass

    def _load_last_resp(self) -> Optional[Dict]:
        try:
            if LAST_RESP_FILE.exists():
                with open(LAST_RESP_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass
        return None

    def follow_up(self, output_type: str, prompt: str) -> Dict:
        """Follow-up: Doubao uses previous_response_id, GLM uses message history"""
        last = self._load_last_resp()
        if not last or not last.get("resp_id"):
            return {"success": False, "error": "No previous record to follow up on. Use rec command first."}
        input_type = last.get("input_type", "image")
        mode = _MODE_MAP.get((input_type, output_type))
        if not mode:
            return {"success": False, "error": "Invalid output type. Use --text or --code"}
        md = _MODES[mode]
        provider = last.get("provider", "doubao")
        orig_model_id = last.get("model_id", "")
        orig_model_name = ""
        retries = 0
        for spec in _MODELS.values():
            if spec["id"] == orig_model_id:
                orig_model_name = spec["name"]
                retries = spec.get("retries", 0)
                break
        if not orig_model_name:
            orig_model_name = orig_model_id
        sp = _SP_MAP.get(mode, SP_VISION)

        fn = Path(last.get("file", "")).name
        print(f"\n💬 Follow-up [{md['label']}]")
        print(f"   Model: {orig_model_name} ({provider})")
        print(f"   Prev: {fn} ({input_type})")
        print(f"   Prompt: {prompt[:80]}...")

        if provider == "zhipu":
            # GLM: 用消息历史维持多轮对话
            history_msgs = list(last.get("messages", []))
            history_msgs.append({"role": "assistant", "content": last.get("last_text", "")})
            history_msgs.append({"role": "user", "content": sp + "\n" + prompt})
            result, error = self._zhipu_call({"id": orig_model_id, "name": orig_model_name},
                                             history_msgs, retries=retries)
            if result is None:
                return {"success": False, "error": error, "model": orig_model_name}
            tokens = self._extract_zhipu_tokens(result)
            text = self._extract_zhipu_text(result)
            new_resp_id = result.get("id", "")
            api_err = ""
            self._save_glm_context(new_resp_id, orig_model_id, input_type,
                                    last.get("file", ""), history_msgs, text, mode)
        else:
            # Doubao: previous_response_id + 缓存
            if self.history.get_daily(orig_model_name) >= DAILY_LIMIT:
                return {"success": False, "error": f"Original model {orig_model_name} over daily limit. Try tomorrow or use rec to restart."}
            thinking_cfg = {"type": "enabled", "reasoning_effort": _REASONING_EFFORT[mode]}
            headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
            payload = {
                "model": orig_model_id,
                "previous_response_id": last["resp_id"],
                "input": [
                    {"role": "system", "content": [{"type": "input_text", "text": sp}]},
                    {"role": "user", "content": [{"type": "input_text", "text": prompt}]},
                ],
                "thinking": thinking_cfg,
                "caching": {"type": "enabled"},
            }
            try:
                st, body = self._post(API_URL, headers, json.dumps(payload).encode("utf-8"))
            except Exception as e:
                return {"success": False, "error": f"API call failed: {type(e).__name__}: {e}",
                        "model": orig_model_name}
            if st != 200:
                try:
                    detail = json.loads(body)
                except Exception:
                    detail = body[:500]
                return {"success": False, "error": f"API request failed (HTTP {st})",
                        "model": orig_model_name, "detail": str(detail)[:500]}
            result = json.loads(body)
            tokens = self._extract_tokens(result)
            text = self._extract_text(result)
            new_resp_id = result.get("id", "")
            api_err = ""
            self._save_last_resp(new_resp_id, orig_model_id, input_type,
                                  last.get("file", ""), provider)

        new_total = self.history.add_tokens(orig_model_name, tokens["total_tokens"])
        ts = time.time()
        self.history.add_record({
            "timestamp": ts, "datetime": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode, "model": orig_model_name, "model_id": orig_model_id,
            "provider": provider,
            "file": last.get("file", ""), "prompt": prompt,
            "input_tokens": tokens["input_tokens"], "output_tokens": tokens["output_tokens"],
            "total_tokens": tokens["total_tokens"], "reasoning_tokens": tokens["reasoning_tokens"],
            "cached_tokens": tokens["cached_tokens"], "response": text[:500],
            "follow_up": True, "prev_resp_id": last["resp_id"],
        })
        limit = -1 if provider == "zhipu" else DAILY_LIMIT
        remaining = -1 if provider == "zhipu" else DAILY_LIMIT - new_total
        return {
            "success": True, "mode": mode, "model": orig_model_name,
            "file": last.get("file", ""), "prompt": prompt, "tokens": tokens,
            "total_today": new_total, "limit": limit,
            "remaining": remaining, "response": text, "resp_id": new_resp_id,
        }

    def get_status(self):
        return self.history.get_status()

    def get_history(self):
        return self.history.get_history()

    def sync_console(self):
        if not self._console.enabled:
            return {"error": "IAM credentials not configured"}
        self._console._last_sync = 0
        return self._console.sync_to_local(self.history)


def _fmt_wan(val: int) -> str:
    w = val / 10_000
    return f"{w:.0f}W" if w == int(w) else f"{w:.2f}W"


def _parse_flags(args: List[str]) -> Tuple[List[str], Dict[str, str]]:
    flags: Dict[str, str] = {}
    rest: List[str] = []
    i = 0
    while i < len(args):
        if args[i] in ("--prompt", "-p") and i + 1 < len(args):
            flags["prompt"] = args[i + 1]; i += 2
        elif args[i] == "--video":
            flags["input_type"] = "video"; i += 1
        elif args[i] == "--image":
            flags["input_type"] = "image"; i += 1
        elif args[i] == "--text":
            flags["output_type"] = "text"; i += 1
        elif args[i] == "--code":
            flags["output_type"] = "code"; i += 1
        elif args[i] == "--batch":
            flags["batch"] = "true"; i += 1
        else:
            rest.append(args[i]); i += 1
    return rest, flags


def _display_width(text: str) -> int:
    """计算字符串在终端中的显示宽度（CJK + emoji 计 2 列）"""
    w = 0
    for ch in text:
        w += 2 if unicodedata.east_asian_width(ch) in ('W', 'F') else 1
    return w


def _center_text(text: str, width: int) -> str:
    """居中字符串，按显示宽度对齐"""
    dw = _display_width(text)
    left = (width - dw) // 2
    right = width - dw - left
    return ' ' * left + text + ' ' * right


def _print_usage():
    W = 60  # box inner width
    hr = '═' * W
    title1 = _center_text('ByteDance Visual Recognition v5.0.1', W)
    title2 = _center_text('Doubao-Seed + GLM Multimodal Vision & Code Generation', W)
    print(f"""
╔{hr}╗
║{title1}║
║{title2}║
╚{hr}╝

Commands
  rec <file/dir> [options]    Recognize or batch process
  ask [options]               Follow up on last recognition
  status                      View status/usage
  sync                        Console usage sync (auto-runs on rec/ask)
  history                     7-day call history

Options - rec
  --image          Input type: image
  --video          Input type: video
  --text           Output type: text
  --code           Output type: code
  --prompt, -p     Extra instruction (optional)
  --batch          Batch process all media files in directory

Options - ask
  --text           Output type: text
  --code           Output type: code
  --prompt, -p     Follow-up content

Model Selection
  180W tokens per model per day, auto-fallback on limit.
  img-to-text    Image→Text   Doubao*6 → GLM-4.6V-Flash → GLM-4.1V-Thinking
  video-to-text  Video→Text   Doubao*6 → GLM-4.6V-Flash → GLM-4.1V-Thinking
  img-to-code    Image→Code   Doubao*5 → GLM-4.6V-Flash → GLM-4.1V-Thinking
  video-to-code  Video→Code   Doubao*5 (GLM not supported for video→code)

  Falls back to free GLM models when all Doubao models are unavailable.

Examples
  rec photo.jpg --image --text
  rec photo.jpg --image --code
  rec video.mp4 --video --text
  rec video.mp4 --video --code
  rec photo.jpg --image --text --prompt "Extract all text"
  rec ./images/ --batch --image --text

  # Follow-up (Doubao: no re-upload; GLM: reuses history with media data)
  ask --text --prompt "What details does this image contain?"
  ask --code --prompt "Convert to React components"
""")


def _print_status_header(vr: DoubaoVisionRecognizer):
    st = vr.get_status()
    print(f"\n📊 {st['date']}")
    total_w = 56
    for m in st["models"]:
        if not m["configured"]:
            amount = "-W/-W"
        elif m["unlimited"]:
            amount = _fmt_wan(m["tokens"])
        else:
            amount = f"{_fmt_wan(m['tokens'])}/{_fmt_wan(m['limit'])}"
        icon = "🔴" if (not m["configured"]) else ("🔴" if m["tokens"] >= (10_000_000 if m["unlimited"] else m["limit"]) else "🟢")
        prefix = f"   {icon} {m['name']}"
        print(f"{prefix}{' ' * (total_w - _display_width(prefix) - len(amount))}{amount}")


def _print_result(result: Dict):
    if result["success"]:
        label = _MODES.get(result.get("mode", ""), {}).get("label", result.get("mode", ""))
        print(f"\n✅ Success! [{label}]")
        print(f"   Model:    {result['model']}")
        t = result["tokens"]
        print(f"   Tokens:   input {t['input_tokens']} | output {t['output_tokens']} | reasoning {t['reasoning_tokens']}")
        print(f"   Session:  {t['total_tokens']}")
        if result.get("limit", DAILY_LIMIT) < 0:
            print(f"   Today:    {_fmt_wan(result['total_today'])}")
        else:
            print(f"   Today:    {_fmt_wan(result['total_today'])} / {_fmt_wan(result['limit'])}")
            print(f"   Remaining:{_fmt_wan(result['remaining'])}")
        print(f"\n{'─' * 56}")
        print(f"📝 Result:\n{result['response']}")
    else:
        print(f"\n❌ Failed: {result.get('error', 'unknown error')}")
        if "detail" in result:
            print(f"   Detail: {result['detail']}")


def _cmd_status():
    vr = DoubaoVisionRecognizer()
    st = vr.get_status()
    print(f"\n📊 Today ({st['date']})")
    print(f"   Total records: {st['total_history']}")
    print(f"   {'─' * 56}")
    total_w = 56
    for m in st["models"]:
        if not m["configured"]:
            amount = "-W/-W"
        elif m["unlimited"]:
            amount = _fmt_wan(m["tokens"])
        else:
            amount = f"{_fmt_wan(m['tokens'])}/{_fmt_wan(m['limit'])}"
        icon = "🔴" if (not m["configured"]) else ("🔴" if m["tokens"] >= (10_000_000 if m["unlimited"] else m["limit"]) else "🟢")
        extra = "" if not (m["configured"] and not m["unlimited"]) else f" (remaining: {_fmt_wan(m['limit'] - m['tokens'])})"
        prefix = f"   {icon} {m['name']}"
        print(f"{prefix}{' ' * (total_w - _display_width(prefix) - len(amount) - len(extra))}{amount}{extra}")
    tu = sum(m["tokens"] for m in st["models"] if m["configured"])
    tl = sum(m["limit"] for m in st["models"] if m["configured"] and not m["unlimited"])
    print(f"   {'─' * 56}")
    print(f"   Configured total: {_fmt_wan(tu)} / {'∞W' if any(m['unlimited'] for m in st['models'] if m['configured']) else _fmt_wan(tl) + ' tokens'}")
    print(f"\n📋 Modes:")
    for mk, md in _MODES.items():
        chain = " -> ".join(_MODELS[k]["name"] for k in md["chain"])
        print(f"   {mk:14s} {md['label']:10s} {chain}")


def _cmd_sync():
    vr = DoubaoVisionRecognizer()
    if not vr._console.enabled:
        print("❌ IAM credentials not configured")
        return
    print("\n🔄 Syncing console usage...")
    before = {m["name"]: m["tokens"] for m in vr.get_status()["models"]}
    result = vr.sync_console()
    if not result:
        print("⚠️ Console returned no data, keeping local counts")
        return
    print("\n   Compare (local -> console):")
    after = vr.get_status()
    for m in after["models"]:
        action = result.get(m["name"], "?")
        icon = "🔄" if action == "synced" else "📌"
        print(f"   {icon} {m['name']:<24s} {_fmt_wan(before.get(m['name'], 0))} -> {_fmt_wan(m['tokens'])} ({action})")


def _cmd_history():
    vr = DoubaoVisionRecognizer()
    records = vr.get_history()
    print(f"\n📋 History ({len(records)} records, {RETENTION_DAYS}-day retention)")
    print(f"   {'─' * 64}")
    for r in records[-20:]:
        print(f"   🔍 {r.get('datetime', '?')} | {r.get('mode', '?')} | {r.get('model', '?')}")
        fn = Path(r.get('file', '')).name if r.get('file') else '(no file)'
        print(f"      File: {fn}")
        print(f"      Tokens: in{r.get('input_tokens', 0)} out{r.get('output_tokens', 0)} reasoning{r.get('reasoning_tokens', 0)}")


def _cmd_batch(args: List[str], flags: Dict[str, str]):
    if not args:
        print("❌ Please provide a directory path")
        return
    dp = Path(args[0])
    if not dp.is_dir():
        print(f"❌ Directory not found: {dp}")
        return
    td = _today_dir()
    bd = td / f"batch_{dp.name}_{hashlib.md5(str(dp).encode()).hexdigest()[:12]}"
    if bd.exists():
        shutil.rmtree(bd)
    bd.mkdir(parents=True, exist_ok=True)
    files = sorted(f for f in dp.iterdir() if f.is_file() and f.suffix.lower() in _MEDIA_EXT)
    if not files:
        print(f"❌ No supported media files found in: {dp}")
        return
    for f in files:
        shutil.copy2(f, bd / f.name)
    print(f"📁 Copied {len(files)} media files to Temp: {bd}")
    input_type = flags.get("input_type", "")
    output_type = flags.get("output_type", "")
    prompt = flags.get("prompt", "")
    vr = DoubaoVisionRecognizer()
    _print_status_header(vr)
    mode_label = f"{input_type}->{output_type}" if input_type else output_type
    print(f"\n📁 Batch processing: {len(files)} files (mode: {mode_label})")
    ok, fail, total = 0, 0, 0
    for i, f in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}] {f.name}")
        result = vr.process(str(f), input_type=input_type, output_type=output_type, prompt=prompt)
        if result["success"]:
            ok += 1
            total += result["tokens"]["total_tokens"]
            print(f"   ✅ {result['model']} | tokens: {result['tokens']['total_tokens']}")
            rp = result.get("response", "")[:120]
            if rp:
                print(f"   💬 {rp}...")
        else:
            fail += 1
            print(f"   ❌ {result.get('error', 'unknown error')}")
            if "limit" in result.get("error", "").lower():
                print("   ⚠️ All models over limit, stopping batch")
                break
    print(f"\n{'─' * 56}")
    print(f"📊 Batch complete: {ok} succeeded, {fail} failed")
    print(f"   Tokens consumed: {total}")


def main():
    if len(sys.argv) < 2:
        _print_usage()
        return
    arg1 = sys.argv[1]
    if arg1 in ("--help", "-h"):
        _print_usage()
        return
    sub = arg1.lower()
    if sub == "status":
        _cmd_status()
    elif sub == "sync":
        _cmd_sync()
    elif sub == "history":
        _cmd_history()
    elif sub == "rec":
        rest, flags = _parse_flags(sys.argv[2:])
        if not rest:
            print("❌ Please provide a file or directory path")
            print("   Usage: rec <path> --image|--video --text|--code [--prompt \"...\"] [--batch]")
            return
        it = flags.get("input_type", "")
        ot = flags.get("output_type", "")
        if not it:
            print("❌ Must specify input type: --image or --video")
            return
        if not ot:
            print("❌ Must specify output type: --text or --code")
            return
        target = rest[0]
        if flags.get("batch") == "true":
            _cmd_batch([target], flags)
            return
        vr = DoubaoVisionRecognizer()
        _print_status_header(vr)
        _print_result(vr.process(target, input_type=it, output_type=ot, prompt=flags.get("prompt", "")))
    elif sub == "ask":
        rest, flags = _parse_flags(sys.argv[2:])
        ot = flags.get("output_type", "")
        prompt = flags.get("prompt", "")
        if not ot:
            print("❌ Must specify output type: --text or --code")
            return
        if not prompt:
            print("❌ Follow-up requires --prompt content")
            print("   Usage: ask --text|--code --prompt \"follow-up content\"")
            return
        vr = DoubaoVisionRecognizer()
        _print_status_header(vr)
        _print_result(vr.follow_up(output_type=ot, prompt=prompt))
    else:
        print(f"❌ Unknown command: {arg1}")
        print("   Available commands: rec, ask, status, sync, history")
        print("   Use --help for help")


if __name__ == "__main__":
    main()
