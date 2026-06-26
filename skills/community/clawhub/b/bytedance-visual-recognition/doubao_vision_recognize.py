#!/usr/bin/env python3
"""
Doubao Vision Recognize v3.0.0
================================
图片/视频 → 文字/代码
  img-to-text    图片→文字  2.0Pro→2.0Code→2.0Lite→1.6V→1.8
  video-to-text  视频→文字  2.0Pro→2.0Code→2.0Lite→1.8→1.6V
  img-to-code    图片→代码  2.0Code→2.0Pro→Code→2.0Lite→1.8
  video-to-code  视频→代码  2.0Code→2.0Pro→2.0Lite

核心: 全自动降级 | thinking=enabled | Token追踪+30min控制台同步 | 日限180W/模型
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

try:
    _ef = Path(__file__).resolve().parent / ".env"
    if _ef.exists():
        with open(_ef, "r", encoding="utf-8") as _f:
            for _l in _f:
                _l = _l.strip()
                if _l and not _l.startswith("#") and "=" in _l:
                    _k, _, _v = _l.partition("=")
                    _k, _v = _k.strip(), _v.strip().strip('"').strip("'")
                    if _k not in os.environ:
                        os.environ[_k] = _v
except Exception:
    pass

API_URL = "https://ark.cn-beijing.volces.com/api/v3/responses"
ARK_API_KEY = os.environ.get("ARK_API_KEY", "")
IAM_AK = os.environ.get("VOLCENGINE_ACCESS_KEY", "")
IAM_SK = os.environ.get("VOLCENGINE_SECRET_KEY", "")
SYNC_INTERVAL = 30 * 60
RETENTION_DAYS = 7
TIMEOUT = 300
MAX_IMG = 15 * 1024 * 1024
MAX_VID = 50 * 1024 * 1024
MAX_PAYLOAD = 64 * 1024 * 1024
DAILY_LIMIT = 1_800_000
THINKING = "enabled"

BASE_DIR = Path(__file__).resolve().parent
HISTORY_FILE = Path(os.environ.get("VISION_HISTORY_FILE", str(BASE_DIR / "vision_history.json")))
TEMP_DIR = Path(os.environ.get("VISION_TEMP_DIR", str(BASE_DIR / "Temp")))
LAST_RESP_FILE = BASE_DIR / ".last_response"
ssl_ctx = ssl.create_default_context()

_MODELS = {
    "20PRO":  {"name": "Doubao-Seed-2.0-Pro",  "id": os.environ.get("DOUBAO_VISION_20P_ID", ""),  "env": "DOUBAO_VISION_20P_ID"},
    "20CODE": {"name": "Doubao-Seed-2.0-Code",  "id": os.environ.get("DOUBAO_VISION_20C_ID", ""),  "env": "DOUBAO_VISION_20C_ID"},
    "20LITE": {"name": "Doubao-Seed-2.0-Lite",  "id": os.environ.get("DOUBAO_VISION_20L_ID", ""),  "env": "DOUBAO_VISION_20L_ID"},
    "16V":    {"name": "Doubao-Seed-1.6-Vision", "id": os.environ.get("DOUBAO_VISION_16V_ID", ""),  "env": "DOUBAO_VISION_16V_ID"},
    "18":     {"name": "Doubao-Seed-1.8",        "id": os.environ.get("DOUBAO_VISION_18_ID", ""),   "env": "DOUBAO_VISION_18_ID"},
    "10CODE": {"name": "Doubao-Seed-Code",       "id": os.environ.get("DOUBAO_VISION_10C_ID", ""),  "env": "DOUBAO_VISION_10C_ID"},
}
for _m in _MODELS.values():
    if not _m["id"]:
        raise RuntimeError(f"未设置 {_m['env']}，请在 .env 中配置。")

_MODES = {
    "img-to-text":   {"label": "图片→文字", "chain": ["20PRO", "20CODE", "20LITE", "16V", "18"]},
    "video-to-text": {"label": "视频→文字", "chain": ["20PRO", "20CODE", "20LITE", "18", "16V"]},
    "img-to-code":   {"label": "图片→代码", "chain": ["20CODE", "20PRO", "10CODE", "20LITE", "18"]},
    "video-to-code": {"label": "视频→代码", "chain": ["20CODE", "20PRO", "20LITE"]},
}

_MODE_MAP = {
    ("image", "text"): "img-to-text",
    ("video", "text"): "video-to-text",
    ("image", "code"): "img-to-code",
    ("video", "code"): "video-to-code",
}

_MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tiff",
              ".mp4", ".mov", ".webm", ".avi", ".mkv", ".flv", ".wmv"}

SP_VISION = """你是一个专业的视觉识别和分析助手。请仔细观察用户提供的图片/视频内容，按以下规则完成分析：

【通用规则】(优先级从高到低)
1. 完整性规则: 需对内容进行完整分析，覆盖图形、文字、表格、场景等所有视觉元素维度，不能遗漏关键内容。
2. 匹配性规则: 分析结果需完全匹配用户指令的具体需求，用户未提及的冗余内容无需反馈。
3. 格式化规则: 若提取文字或表格，整理后须用 Markdown 格式输出；表格须转成标准 Markdown 表格格式；公式须转成标准 LaTeX 格式。
4. 默认规则: 用户若无特殊指令需求，分析结果以"场景描述"为核心，按用户日常阅读习惯整理成简洁的自然语言文本。

【后置检查】
1. 确认结果中没有用户未提及的冗余内容。
2. 确认所有需 Markdown 格式的内容格式正确。
3. 确认内容描述与实际显示一致，未出现主观臆断。"""

SP_VIDEO = """你是一个专业的视频内容分析助手。请仔细观察用户提供的视频内容，按以下规则完成分析：

【通用规则】(优先级从高到低)
1. 完整性规则: 需对视频内容进行完整分析，先梳理视频的完整叙事逻辑或操作流程，再按"核心内容-关键细节-总结归纳"的优先级整理结果。
2. 匹配性规则: 分析结果需完全匹配用户指令的具体需求。
3. 时间戳规则: 若视频中存在明确的时间节点或操作步骤，需为这些节点补充精确到秒的时间戳标记。
4. 默认规则: 用户若无特殊指令，分析结果以不超过300字的通俗易懂的自然语言文本输出。

【后置检查】
1. 确认结果中没有用户未提及的冗余内容。
2. 确认所有需时间戳标记的地方都已补充精确时间。
3. 确认分析结果格式布局符合日常阅读习惯。"""

SP_IMG_CODE = """你是一个专业的 UI 设计稿转代码助手。请仔细观察用户提供的图片，按以下规则生成代码：

【通用规则】(优先级从高到低)
1. 完整性规则: 需完整复刻图片中的 UI 布局、细节样式、交互元素视觉效果，不能遗漏任何关键视觉元素。
2. 匹配性规则: 生成的代码技术栈，需完全匹配用户指令中指定的技术栈。
3. 格式化规则: 代码需遵循统一规范，使用语义化 HTML 标签，CSS 类名采用 BEM 风格，代码结构清晰，关键部分需要添加注释说明。
4. 响应式规则: 代码需同时适配桌面端和移动端，在不同设备尺寸下保持视觉效果一致。
5. 默认规则: 用户若无特殊指令需求，技术栈默认使用 HTML+TailwindCSS，无需额外补充无用的 JS 代码。

【后置检查】
1. 确认代码的技术栈完全匹配用户指令的要求。
2. 确认代码中没有用户指令未提及的冗余内容。
3. 确认代码中所有需要图片的地方都使用了合理的占位图。
4. 确认代码的格式布局符合行业标准，没有语法错误。
5. 确认代码的复刻效果与原图的视觉效果高度匹配。"""

SP_VIDEO_CODE = """你是一个专业的视频转代码助手。请仔细观察用户提供的视频内容（可能是UI演示、网页录屏、应用操作录屏等），按以下规则生成代码：

【通用规则】(优先级从高到低)
1. 完整性规则: 需完整复刻视频中展示的 UI 布局、页面结构、交互流程和视觉样式，不能遗漏任何关键界面元素。
2. 匹配性规则: 生成的代码技术栈需完全匹配用户指令中指定的技术栈。
3. 格式化规则: 代码需遵循统一规范，使用语义化 HTML 标签，CSS 类名采用 BEM 风格，代码结构清晰，关键部分添加注释说明。
4. 响应式规则: 代码需同时适配桌面端和移动端，在不同设备尺寸下保持视觉效果一致。
5. 默认规则: 用户若无特殊指令需求，技术栈默认使用 HTML+TailwindCSS，无需额外补充无用的 JS 代码。

【后置检查】
1. 确认代码的技术栈完全匹配用户指令的要求。
2. 确认代码中没有用户指令未提及的冗余内容。
3. 确认代码中所有需要图片的地方都使用了合理的占位图。
4. 确认代码的格式布局符合行业标准，没有语法错误。
5. 确认代码的复刻效果与视频中展示的视觉效果高度匹配。"""

_SP_MAP = {
    "img-to-text": SP_VISION,
    "video-to-text": SP_VIDEO,
    "img-to-code": SP_IMG_CODE,
    "video-to-code": SP_VIDEO_CODE,
}


class ConsoleSyncer:
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
            ids = [m["id"] for m in _MODELS.values()]
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
        names = [m["name"] for m in _MODELS.values()]
        return {
            "date": today,
            "total_history": len(self.data.get("history", [])),
            "models": [{"name": n, "tokens": self.get_daily(n), "limit": DAILY_LIMIT} for n in names],
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
    def __init__(self):
        self.api_key = ARK_API_KEY
        self.history = HistoryManager(HISTORY_FILE)
        self._console = ConsoleSyncer()

    def _auto_sync(self):
        if self._console.enabled:
            self._console.sync_to_local(self.history)
        self._cleanup_temp()

    def _cleanup_temp(self):
        try:
            if not TEMP_DIR.exists():
                return
            cutoff = time.time() - 3 * 86400
            for f in TEMP_DIR.iterdir():
                if f.is_file() and f.stat().st_atime < cutoff:
                    f.unlink()
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
        for mk in _MODES[mode_key]["chain"]:
            spec = _MODELS[mk]
            if self.history.get_daily(spec["name"]) < DAILY_LIMIT:
                return {"key": mk, "name": spec["name"], "id": spec["id"]}
        return None

    def _encode_media(self, file_path: str, input_type: str) -> Tuple[str, str, str]:
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
        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        tmp = TEMP_DIR / f"v_{abs(hash(str(src))):x}{ext}"
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

    def _build_blocks(self, media: str, data_uri: str, prompt: str) -> List[Dict]:
        blocks = []
        if media == "image":
            blocks.append({"type": "input_image", "image_url": data_uri})
        else:
            blocks.append({"type": "input_video", "video_url": data_uri, "fps": 1.0})
        blocks.append({"type": "input_text", "text": prompt})
        return blocks

    def _resolve_prompt(self, mode_key: str, user_prompt: str) -> str:
        sp = _SP_MAP.get(mode_key, SP_VISION)
        if not user_prompt or not user_prompt.strip():
            if mode_key.endswith("-to-text"):
                return sp + "\n请详细描述该内容。"
            return sp + "\n请根据内容生成对应的前端代码（HTML+TailwindCSS）。"
        return sp + f"\n\n用户指令: {user_prompt}"

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
        self._auto_sync()
        mode = _MODE_MAP.get((input_type, output_type))
        if not mode:
            return {"success": False, "error": "无效参数组合，需 --image/--video + --text/--code"}
        if not file_path or not Path(file_path).is_file():
            return {"success": False, "error": "请提供图片/视频文件路径。"}
        try:
            data_uri, tmp_path, media = self._encode_media(file_path, input_type)
        except (FileNotFoundError, ValueError) as e:
            return {"success": False, "error": str(e)}
        md = _MODES[mode]
        model = self._select_model(mode)
        if not model:
            return {"success": False, "error": f"模式 {md['label']} 所有模型今日已超限，请明天再试。"}
        full_prompt = self._resolve_prompt(mode, prompt)
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        blocks = self._build_blocks(media, data_uri, full_prompt)
        payload = {"model": model["id"], "input": [{"role": "user", "content": blocks}],
                   "thinking": {"type": THINKING}}
        print(f"\n🔍 {md['label']}")
        print(f"   模型: {model['name']}")
        print(f"   文件: {Path(file_path).name} ({media})")
        if prompt:
            print(f"   指令: {prompt[:80]}...")
        try:
            st, body = self._post(API_URL, headers, json.dumps(payload).encode("utf-8"))
            if st != 200:
                try:
                    detail = json.loads(body)
                except Exception:
                    detail = body[:500]
                return {"success": False, "error": f"API 请求失败 (HTTP {st})",
                        "model": model["name"], "detail": str(detail)[:500]}
            result = json.loads(body)
        except Exception as e:
            return {"success": False, "error": f"API 调用失败: {type(e).__name__}: {e}"}
        tokens = self._extract_tokens(result)
        text = self._extract_text(result)
        new_total = self.history.add_tokens(model["name"], tokens["total_tokens"])
        resp_id = result.get("id", "")
        ts = time.time()
        self.history.add_record({
            "timestamp": ts, "datetime": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode, "model": model["name"], "model_id": model["id"],
            "file": file_path, "prompt": prompt or "(auto)",
            "input_tokens": tokens["input_tokens"], "output_tokens": tokens["output_tokens"],
            "total_tokens": tokens["total_tokens"], "reasoning_tokens": tokens["reasoning_tokens"],
            "cached_tokens": tokens["cached_tokens"], "response": text[:500],
        })
        if resp_id:
            self._save_last_resp(resp_id, model["id"], input_type, file_path)
        return {
            "success": True, "mode": mode, "model": model["name"],
            "file": file_path, "prompt": prompt or "(auto)", "tokens": tokens,
            "total_today": new_total, "limit": DAILY_LIMIT,
            "remaining": DAILY_LIMIT - new_total, "response": text, "resp_id": resp_id,
        }

    def _save_last_resp(self, resp_id: str, model_id: str, input_type: str, file_path: str):
        try:
            data = {"resp_id": resp_id, "model_id": model_id,
                    "input_type": input_type, "file": file_path,
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
        self._auto_sync()
        last = self._load_last_resp()
        if not last or not last.get("resp_id"):
            return {"success": False, "error": "没有可追问的记录，请先使用 rec 命令识别文件"}
        input_type = last.get("input_type", "image")
        mode = _MODE_MAP.get((input_type, output_type))
        if not mode:
            return {"success": False, "error": "无效输出类型，需 --text 或 --code"}
        md = _MODES[mode]
        orig_model_id = last.get("model_id", "")
        orig_model_name = ""
        for spec in _MODELS.values():
            if spec["id"] == orig_model_id:
                orig_model_name = spec["name"]
                break
        if not orig_model_name:
            orig_model_name = orig_model_id
        if self.history.get_daily(orig_model_name) >= DAILY_LIMIT:
            return {"success": False, "error": f"原始模型 {orig_model_name} 今日已超限，追问需同一模型，请明天再试或用 rec 重新开始"}
        sp = _SP_MAP.get(mode, SP_VISION)
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": orig_model_id,
            "previous_response_id": last["resp_id"],
            "instructions": sp,
            "input": [{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
            "thinking": {"type": THINKING},
        }
        fn = Path(last.get("file", "")).name
        print(f"\n💬 追问 [{md['label']}]")
        print(f"   模型: {orig_model_name}")
        print(f"   上次: {fn} ({input_type})")
        print(f"   指令: {prompt[:80]}...")
        try:
            st, body = self._post(API_URL, headers, json.dumps(payload).encode("utf-8"))
            if st != 200:
                try:
                    detail = json.loads(body)
                except Exception:
                    detail = body[:500]
                return {"success": False, "error": f"API 请求失败 (HTTP {st})",
                        "model": orig_model_name, "detail": str(detail)[:500]}
            result = json.loads(body)
        except Exception as e:
            return {"success": False, "error": f"API 调用失败: {type(e).__name__}: {e}"}
        tokens = self._extract_tokens(result)
        text = self._extract_text(result)
        new_total = self.history.add_tokens(orig_model_name, tokens["total_tokens"])
        new_resp_id = result.get("id", "")
        ts = time.time()
        self.history.add_record({
            "timestamp": ts, "datetime": datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
            "mode": mode, "model": orig_model_name, "model_id": orig_model_id,
            "file": last.get("file", ""), "prompt": prompt,
            "input_tokens": tokens["input_tokens"], "output_tokens": tokens["output_tokens"],
            "total_tokens": tokens["total_tokens"], "reasoning_tokens": tokens["reasoning_tokens"],
            "cached_tokens": tokens["cached_tokens"], "response": text[:500],
            "follow_up": True, "prev_resp_id": last["resp_id"],
        })
        if new_resp_id:
            self._save_last_resp(new_resp_id, orig_model_id, input_type, last.get("file", ""))
        return {
            "success": True, "mode": mode, "model": orig_model_name,
            "file": last.get("file", ""), "prompt": prompt, "tokens": tokens,
            "total_today": new_total, "limit": DAILY_LIMIT,
            "remaining": DAILY_LIMIT - new_total, "response": text, "resp_id": new_resp_id,
        }

    def get_status(self):
        return self.history.get_status()

    def get_history(self):
        return self.history.get_history()

    def sync_console(self):
        if not self._console.enabled:
            return {"error": "IAM 密钥未配置"}
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


def _print_usage():
    print(r"""
╔════════════════════════════════════════════════════════════╗
║       ByteDance Visual Recognition v3.0.0                 ║
║       火山方舟 豆包多模态视觉识别 + 代码生成                  ║
╚════════════════════════════════════════════════════════════╝

【命令】
  rec <文件/目录> [参数]    识别或批量处理
  ask [参数]                追问上次识别结果(无需重新上传文件)
  status                    查看状态/用量
  sync                      手动控制台同步
  history                   7天调用历史

【参数 - rec】
  --image          输入为图片
  --video          输入为视频
  --text           输出为文字
  --code           输出为代码
  --prompt, -p     一级提示词(可选)
  --batch          批量处理目录下所有媒体文件

【参数 - ask】
  --text           输出为文字
  --code           输出为代码
  --prompt, -p     追问内容

【模型选择】
  每模型每天 180W tokens超过自动降级，不支持指定模型
  img-to-text    图片→文字  2.0Pro→2.0Code→2.0Lite→1.6V→1.8
  video-to-text  视频→文字  2.0Pro→2.0Code→2.0Lite→1.8→1.6V
  img-to-code    图片→代码  2.0Code→2.0Pro→Code→2.0Lite→1.8
  video-to-code  视频→代码  2.0Code→2.0Pro→2.0Lite

【示例】
  rec photo.jpg --image --text
  rec photo.jpg --image --code
  rec video.mp4 --video --text
  rec photo.png --video --text
  rec photo.jpg --image --text --prompt "提取所有文字"
  rec ./images/ --batch --image --text

  # 追问(基于上次rec的结果，无需重新上传) 例：
  ask --text --prompt "图片的详细内容是？"
  ask --code --prompt "将图片转代码"
  ask --code --prompt "用React实现"
""")


def _print_status_header(vr: DoubaoVisionRecognizer):
    vr._auto_sync()
    st = vr.get_status()
    print(f"\n📊 {st['date']}")
    for m in st["models"]:
        icon = "🟢" if m["tokens"] < m["limit"] else "🔴"
        print(f"   {icon} {m['name']:<22s} {_fmt_wan(m['tokens'])}/{_fmt_wan(m['limit'])}")


def _print_result(result: Dict):
    if result["success"]:
        label = _MODES.get(result.get("mode", ""), {}).get("label", result.get("mode", ""))
        print(f"\n✅ 成功! [{label}]")
        print(f"   模型:    {result['model']}")
        t = result["tokens"]
        print(f"   Token:   输入 {t['input_tokens']} | 输出 {t['output_tokens']} | 推理 {t['reasoning_tokens']}")
        print(f"   本次:    {t['total_tokens']}")
        print(f"   今日:    {_fmt_wan(result['total_today'])} / {_fmt_wan(result['limit'])}")
        print(f"   剩余:    {_fmt_wan(result['remaining'])}")
        print(f"\n{'─' * 56}")
        print(f"📝 结果:\n{result['response']}")
    else:
        print(f"\n❌ 失败: {result.get('error', '未知错误')}")
        if "detail" in result:
            print(f"   详情: {result['detail']}")


def _cmd_status():
    vr = DoubaoVisionRecognizer()
    st = vr.get_status()
    print(f"\n📊 今日状态 ({st['date']})")
    print(f"   识别记录总数: {st['total_history']}")
    print(f"   {'─' * 56}")
    for m in st["models"]:
        icon = "🟢" if m["tokens"] < m["limit"] else "🔴"
        print(f"   {icon} {m['name']:<22s} {_fmt_wan(m['tokens'])}/{_fmt_wan(m['limit'])} (剩余: {_fmt_wan(m['limit'] - m['tokens'])})")
    tu = sum(m["tokens"] for m in st["models"])
    tl = sum(m["limit"] for m in st["models"])
    print(f"   {'─' * 56}")
    print(f"   总计: {_fmt_wan(tu)} / {_fmt_wan(tl)} tokens")
    print(f"\n📋 模式:")
    for mk, md in _MODES.items():
        chain = " -> ".join(_MODELS[k]["name"] for k in md["chain"])
        print(f"   {mk:14s} {md['label']:8s} {chain}")


def _cmd_sync():
    vr = DoubaoVisionRecognizer()
    if not vr._console.enabled:
        print("❌ IAM 密钥未配置")
        return
    print("\n🔄 控制台用量同步中...")
    before = {m["name"]: m["tokens"] for m in vr.get_status()["models"]}
    result = vr.sync_console()
    if not result:
        print("⚠️ 控制台返回无数据，保持本地计数")
        return
    print("\n   对比 (本地 -> 控制台):")
    after = vr.get_status()
    for m in after["models"]:
        action = result.get(m["name"], "?")
        icon = "🔄" if action == "synced" else "📌"
        print(f"   {icon} {m['name']:<22s} {_fmt_wan(before.get(m['name'], 0))} -> {_fmt_wan(m['tokens'])} ({action})")


def _cmd_history():
    vr = DoubaoVisionRecognizer()
    records = vr.get_history()
    print(f"\n📋 历史记录 (共 {len(records)} 条, 保留 {RETENTION_DAYS} 天)")
    print(f"   {'─' * 64}")
    for r in records[-20:]:
        print(f"   🔍 {r.get('datetime', '?')} | {r.get('mode', '?')} | {r.get('model', '?')}")
        fn = Path(r.get('file', '')).name if r.get('file') else '(无文件)'
        print(f"      文件: {fn}")
        print(f"      Token: 入{r.get('input_tokens', 0)} 出{r.get('output_tokens', 0)} 推理{r.get('reasoning_tokens', 0)}")


def _cmd_batch(args: List[str], flags: Dict[str, str]):
    if not args:
        print("❌ 请提供目录路径")
        return
    dp = Path(args[0])
    if not dp.is_dir():
        print(f"❌ 目录不存在: {dp}")
        return
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    bd = TEMP_DIR / f"batch_{dp.name}_{abs(hash(str(dp))):x}"
    if bd.exists():
        shutil.rmtree(bd)
    shutil.copytree(dp, bd)
    print(f"📁 已复制到 Temp: {bd}")
    files = sorted(f for f in bd.iterdir() if f.is_file() and f.suffix.lower() in _MEDIA_EXT)
    if not files:
        print(f"❌ 目录中没有支持的媒体文件: {dp}")
        return
    input_type = flags.get("input_type", "")
    output_type = flags.get("output_type", "")
    prompt = flags.get("prompt", "")
    vr = DoubaoVisionRecognizer()
    _print_status_header(vr)
    mode_label = f"{input_type}->{output_type}" if input_type else output_type
    print(f"\n📁 批量处理: {len(files)} 个文件 (模式: {mode_label})")
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
            print(f"   ❌ {result.get('error', '未知错误')}")
            if "超限" in result.get("error", ""):
                print("   ⚠️ 全部模型超限，停止批量处理")
                break
    print(f"\n{'─' * 56}")
    print(f"📊 批量完成: 成功 {ok}, 失败 {fail}")
    print(f"   Token 消耗: {total}")


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
            print("❌ 请提供文件或目录路径")
            print("   用法: rec <路径> --image|--video --text|--code [--prompt \"...\"] [--batch]")
            return
        it = flags.get("input_type", "")
        ot = flags.get("output_type", "")
        if not it:
            print("❌ 必须指定输入类型: --image 或 --video")
            return
        if not ot:
            print("❌ 必须指定输出类型: --text 或 --code")
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
            print("❌ 必须指定输出类型: --text 或 --code")
            return
        if not prompt:
            print("❌ 追问必须提供 --prompt 内容")
            print("   用法: ask --text|--code --prompt \"追问内容\"")
            return
        vr = DoubaoVisionRecognizer()
        _print_status_header(vr)
        _print_result(vr.follow_up(output_type=ot, prompt=prompt))
    else:
        print(f"❌ 未知命令: {arg1}")
        print("   可用命令: rec, ask, status, sync, history")
        print("   使用 --help 查看帮助")


if __name__ == "__main__":
    main()
