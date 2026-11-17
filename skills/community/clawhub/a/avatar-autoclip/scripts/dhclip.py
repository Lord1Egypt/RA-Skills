#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""avatar-autoclip —— 数字人 + 智能剪辑 一站式命令行客户端（零依赖，仅标准库）。

上游开放 API 的路径形式固定为：

    /api/v1/apps/<应用代号>/<接口代号>

实测要点（写进代码，避免踩）：
  * 官方文档里的 `endpoint_path`（如 `/v1/clip/template`）**不可信**，
    真实可通的永远是上面的 `/api/v1/apps/...` 形式。
  * 同一个接口在不同网关下的**响应信封不一样**：
      直连租户域名： {"code":1,"msg":"success","data":{...}}
      api.a7w.cn 中转：{"code":1,"msg":"success","data":{"result":{"code":"Succeed","data":{...}}}}
      个别接口（如音色列表）不经二次包装，data 直接就是业务体。
    所以统一走 `_unwrap()`，不要在任何地方自己 `["data"]` 取一层。

退出码约定：
  0 成功 / 2 用法错误 / 3 上游接口错误 / 4 本地预检不通过 /
  5 超出预算 / 6 等待超时 / 7 缺少必要授权声明
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

__version__ = "1.0.1"

DEFAULT_BASE = "https://api.a7w.cn/api/v1"

# ═══════════════════════════════════════════════════════════════════════════
# ★★★ 算力接口死锁（2026-10-09 站主指定）：本技能【只允许】访问 api.a7w.cn。
#
#   为什么要锁死：
#     技能用的是【用户自己的 API Key】，而这个 Key 只在 api.a7w.cn 上有意义。
#     一旦把根地址指到别处（--base / 环境变量 / 改常量），请求必然一路失败 ——
#     但旧行为只会抛一个含糊的网络/HTTP 错误，用户会以为是"技能坏了"，
#     然后反复重试。站主反馈的现象正是「更改后就一直错误」。
#
#   锁法（三层，任何一层都拦得住）：
#     ① 不再从环境变量读根地址 —— 少一个可改的入口；
#     ② Client 构造时就校验 host 必须是 api.a7w.cn —— 不是就【就地拒绝】，
#        连请求都不发出去，并明确告诉用户"是接口地址的问题，不是你的 Key"；
#     ③ 校验对 --base 同样生效 —— 传别的一律报错。
#
#   ⚠️ 如实说明：技能以源码分发，**改源码本身无法从技术上禁止**。
#      上面锁的是"正常配置路径"与"误改后的表现"。要更强，只能发编译产物
#      （PyInstaller 打包 / 走中继下发），那是另一个层面的工作。
# ═══════════════════════════════════════════════════════════════════════════
LOCKED_HOST = "api.a7w.cn"
LOCKED_BASE = "https://api.a7w.cn/api/v1"


def assert_base_locked(base: str) -> str:
    """根地址只能是 api.a7w.cn。返回规范化后的根地址；不是就抛 CliError。"""
    raw = (base or "").strip()
    if not raw:
        return LOCKED_BASE
    parsed = urllib.parse.urlparse(raw if "://" in raw else "https://" + raw)
    host = (parsed.hostname or "").lower()
    if host != LOCKED_HOST:
        raise CliError(
            "算力接口已锁定，不能改：本技能只允许访问 %s。\n"
            "  你给的是：%s\n"
            "\n"
            "  为什么锁：技能用的是你自己的 API Key，而 Key 只在 %s 上有效。\n"
            "  指到别的地址必然一路报错 —— 所以这里直接拒绝，不让你白折腾。\n"
            "  也就是说：出现错误时，先怀疑 Key / 余额 / 参数，【不要】去改接口地址。\n"
            "\n"
            "  想接别的服务，请另找一个对应的技能。" % (LOCKED_HOST, raw, LOCKED_HOST),
            code=EXIT_USAGE)
    return LOCKED_BASE

UA = "avatar-autoclip/%s (+python-stdlib)" % __version__

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_API = 3
EXIT_VALIDATION = 4
EXIT_BUDGET = 5
EXIT_TIMEOUT = 6
EXIT_AUTHZ = 7

# ---------------------------------------------------------------------------
# 应用与接口代号（来自 GET /api/v1/apps/<app> 的 code 字段，不要手改）
# ---------------------------------------------------------------------------
APP_LIPSYNC = "pic_lipsync"          # 图片数字人：图片 + 音频/文案 -> 口播视频
APP_CLIP = "smart_clip"              # 智能剪辑：模板 + 素材 -> 成片
APP_TTS = "voice_tts"                # 语音：文案 -> 音频（数字人的前置）
APP_IMAGE = "nano_banana"            # 参考生图：1 张参考图 -> N 张同风格人物图

API_LIPSYNC_SUBMIT = "submit"
API_LIPSYNC_QUERY = "query"
API_CLIP_TEMPLATE = "template"
API_CLIP_TEMPLATE_DETAIL = "template_detail"
API_CLIP_REALMAN = "realman_broadcast"
API_CLIP_MIXCUT = "broadcast_mixcut"
API_CLIP_NEWS = "news_mixcut"
API_TTS = "tts"
API_TTS_VOICES = "list_voices"
API_TTS_STT = "stt"
API_IMAGE_SUBMIT = "submit"
API_IMAGE_QUERY = "query"

# nano_banana 的两种任务类型
IMAGE_ACTION_GENERATE = "generate"   # 文生图
IMAGE_ACTION_EDIT = "edit"           # 基于参考图编辑 —— 即「参考生图」

# scene -> 提交接口。模板只能提交到对应的那个接口，跨用会被上游拒绝。
SCENE_TO_API = {
    "realMan": API_CLIP_REALMAN,
    "oralMixCutting": API_CLIP_MIXCUT,
    "newsMixCutting": API_CLIP_NEWS,
}
SCENE_LABEL = {
    "realMan": "真人口播（配合图片数字人的成片）",
    "oralMixCutting": "素材混剪（音频驱动 + 素材）",
    "newsMixCutting": "新闻体视频（标题 + 素材）",
}

# 平台硬限制（素材与媒体要求一节），本地先拦一道，别拿点数去试错
LIMITS = {
    "single_side_px": 2000,          # 单边分辨率上限
    "portrait_max_sec": 300.0,       # 真人口播 videoUrl < 5 分钟
    "portrait_max_bytes": 500 * 1024 * 1024,
    "material_video_max_sec": 60.0,  # 单条视频素材 <= 60s
    "material_image_sec": 2.0,       # 一张图按 2 秒计
    "material_total_sec": 300.0,     # 素材总时长 <= 5 分钟
    "audio_max_sec": 300.0,
    "subtitle_max_ms": 310000,
    "news_duration_sec": (5, 300),
    "news_title_len": (3, 1800),
    "bgm_max_bytes": 120 * 1024 * 1024,
    "cover_max_bytes": 10 * 1024 * 1024,
}


class CliError(Exception):
    """带退出码的业务异常。"""

    def __init__(self, message: str, code: int = EXIT_API, payload: Any = None):
        super().__init__(message)
        self.code = code
        self.payload = payload


class ApiError(CliError):
    def __init__(self, message: str, http_status: int = 0, payload: Any = None):
        super().__init__(message, code=EXIT_API, payload=payload)
        self.http_status = http_status


class ValidationError(CliError):
    def __init__(self, message: str, issues: Optional[List[str]] = None):
        super().__init__(message, code=EXIT_VALIDATION)
        self.issues = issues or []


# ---------------------------------------------------------------------------
# 响应信封拆解
# ---------------------------------------------------------------------------
_OK_CODES = {1, "1", "succeed", "success", "ok", "200", 200}
_FAIL_HINTS = ("失败", "错误", "无效", "不足", "拒绝", "不支持", "超时", "频繁")


def _looks_like_envelope(obj: Any) -> bool:
    return isinstance(obj, dict) and "code" in obj and (
        "data" in obj or "msg" in obj or "message" in obj
    )


def _code_ok(code: Any) -> bool:
    if isinstance(code, str):
        return code.strip().lower() in _OK_CODES
    return code in _OK_CODES


def _code_text(payload: Dict[str, Any]) -> str:
    for key in ("msg", "message", "error", "errmsg", "detail"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
        if isinstance(val, dict):
            inner = val.get("message") or val.get("msg")
            if isinstance(inner, str) and inner.strip():
                return inner.strip()
    return ""


def unwrap(payload: Any, _depth: int = 0) -> Any:
    """把一层层包装剥掉，返回真正的业务体。

    兼容四种实测形态：
      1. {"code":1,"msg":"...","data":{...}}                       直连租户域名
      2. {"code":1,...,"data":{"result":{"code":"Succeed",...}}}   api.a7w.cn 中转的二次包装
      3. 裸业务体（没有 code/msg），例如 {"total":38,"items":[...]}  音色列表这类
      4. {"error":{"code":...}}                                    网关的错误形态

    关键坑（实测踩过）：任务查询完成后 data 里**也有一个 result 字段**
    （如 {"status":"completed","result":{"video_url":...}}），
    它跟形态 2 的包装字段同名。所以只有 data 里**除了 result/sid 没有别的字段**时，
    才把 result 当成包装层；否则必须把整个 data 原样返回，
    否则会把 status 丢掉，轮询就永远等不到终态。
    """
    if _depth > 6 or not isinstance(payload, dict):
        return payload

    # 形态 4：错误对象
    if "error" in payload and "code" not in payload:
        err = payload["error"]
        if isinstance(err, (dict, str)) and _code_text({"error": err}):
            msg = _code_text({"error": err})
            if isinstance(err, dict) or any(h in msg for h in _FAIL_HINTS):
                raise ApiError(msg, payload=err)

    # 形态 3：裸业务体
    if not _looks_like_envelope(payload):
        return payload

    code = payload.get("code")
    if not _code_ok(code):
        msg = _code_text(payload) or ("接口返回失败 code=%r" % (code,))
        raise ApiError(msg, payload=payload.get("data"))

    if "data" not in payload:
        return payload

    data = payload["data"]

    # 形态 2：中转层把上游响应体整个塞进 data.result
    if isinstance(data, dict) and "result" in data:
        inner = data["result"]
        other_keys = set(data) - {"result", "sid"}
        sid = data.get("sid")

        # 情况 A：result 自己就是个带 code 的信封 → 一定是中转包装层。
        # ⚠️ 判据必须放在 other_keys 之前 —— 实测中转层会在 data 里
        # **同时**给 result 和 usage，如
        #   {"data":{"result":{"code":"Succeed","data":{...}}, "usage":{"points_cost":0}}}
        # 用"只看 other_keys 是否为空"会把这种当成任务结果而不剥，模板列表就永远是空的。
        if _looks_like_envelope(inner):
            return unwrap(inner, _depth + 1)

        # 情况 B：result 是数组
        if isinstance(inner, list):
            if other_keys:
                return data
            return {"results": inner, "sid": sid}

        # 情况 C：result 是普通对象。
        # 任务结果体就是这种：{"status":"completed","result":{"video_url":...}, "usage":...}
        # 此时 data 里还有 status/task_id 等字段，必须原样返回，不能只留 result。
        if isinstance(inner, dict):
            if other_keys:
                return data
            merged = dict(inner)
            if sid is not None and "sid" not in merged:
                merged["sid"] = sid
            return merged

        # 情况 D：result 是标量（如 "任务完成"）→ 整个 data 才有意义
        return data

    # 再剥一层同名信封
    if _looks_like_envelope(data):
        return unwrap(data, _depth + 1)

    return data


# ---------------------------------------------------------------------------
# 深层取值
# ---------------------------------------------------------------------------
VIDEO_KEYS = ("video_url", "video_uri", "videoUrl", "output_url", "result_url",
              "video", "url")
COVER_KEYS = ("cover_url", "cover_uri", "coverUrl", "first_frame_url")
AUDIO_KEYS = ("audio_url", "audio_uri", "audioUrl", "preview_audio_url", "output_url")
# 图片结果：nano_banana 实测放在 result.image_url / result.data[].image_url /
# result.results[].image_url，三层都出现过，所以多字段兜。
IMAGE_KEYS = ("image_url", "image_uri", "imageUrl", "output_url", "result_url", "url")


def find_deep(obj: Any, keys: Sequence[str], _depth: int = 0) -> Optional[str]:
    """在任意深的嵌套结构里找第一个非空字符串值（按 keys 的优先级）。"""
    if _depth > 12:
        return None
    if isinstance(obj, dict):
        for k in keys:
            val = obj.get(k)
            if isinstance(val, str) and val.strip():
                return val.strip()
        for val in obj.values():
            found = find_deep(val, keys, _depth + 1)
            if found:
                return found
        return None
    if isinstance(obj, list):
        for item in obj:
            found = find_deep(item, keys, _depth + 1)
            if found:
                return found
    return None


def find_number(obj: Any, keys: Sequence[str], _depth: int = 0) -> Optional[float]:
    """找数值字段（如 duration）。find_deep 只认字符串，数值字段要用这个。"""
    if _depth > 12:
        return None
    if isinstance(obj, dict):
        for k in keys:
            val = obj.get(k)
            if isinstance(val, bool):
                continue
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, str):
                try:
                    return float(val.strip())
                except ValueError:
                    pass
        for val in obj.values():
            found = find_number(val, keys, _depth + 1)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_number(item, keys, _depth + 1)
            if found is not None:
                return found
    return None


def find_points_cost(obj: Any) -> Optional[float]:
    """取真实扣费点数。平台的字段价不等于结算价，只有 points_cost 可信。"""
    if isinstance(obj, dict):
        usage = obj.get("usage")
        if isinstance(usage, dict):
            for k in ("points_cost", "points", "cost"):
                val = usage.get(k)
                if isinstance(val, (int, float)):
                    return float(val)
        for k in ("points_cost", "total_points"):
            val = obj.get(k)
            if isinstance(val, (int, float)):
                return float(val)
        for val in obj.values():
            found = find_points_cost(val)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_points_cost(item)
            if found is not None:
                return found
    return None


_STATUS_VALUES = ("pending", "queued", "processing", "running", "completed",
                  "succeeded", "success", "failed", "error", "cancelled",
                  "canceled", "timeout")


def resolve_task_status(obj: Any) -> Optional[str]:
    """在响应里找任务状态。**必须深层搜**。

    实测两种查询路由的状态字段位置不一样：
      * 通用 `GET /tasks/{id}`  → `data.status`
      * 应用级 `POST /apps/pic_lipsync/query` → `data.result.data.status`
    只在顶层找 key 的话，第二种永远拿不到状态，
    表现为"任务明明完成了，轮询却一直转到超时"。
    """
    if isinstance(obj, dict):
        for k in ("status", "task_status", "state"):
            val = obj.get(k)
            if isinstance(val, str) and val.strip().lower() in _STATUS_VALUES:
                return val.strip().lower()
        for val in obj.values():
            found = resolve_task_status(val)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = resolve_task_status(item)
            if found:
                return found
    return None


TERMINAL_OK = {"completed", "succeeded", "success"}
TERMINAL_BAD = {"failed", "error", "cancelled", "canceled", "timeout"}

# 实测到的**瞬时**故障：弹性 GPU 机器在提交后丢失。
# 这类失败任务不扣费（actual_points=0），重试基本是免费的，所以值得自动重试。
TRANSIENT_CODES = {
    "elastic_machine_lost_after_submit",
    "machine_lost",
    "server_error",
    "internal_error",
    "queue_limit_exceeded",
    "upstream_timeout",
}
TRANSIENT_HINTS = ("请稍后重试", "稍后重试", "机器", "繁忙", "try again", "temporarily")


def is_transient_error(payload: Any) -> bool:
    """判断这个失败是不是「重试一下就好」的那一类。"""
    def walk(node: Any, depth: int = 0) -> bool:
        if depth > 10:
            return False
        if isinstance(node, dict):
            code = node.get("code")
            if isinstance(code, str) and code.strip().lower() in TRANSIENT_CODES:
                return True
            for key in ("message", "msg", "error_msg"):
                val = node.get(key)
                if isinstance(val, str) and any(h in val for h in TRANSIENT_HINTS):
                    return True
            return any(walk(v, depth + 1) for v in node.values())
        if isinstance(node, list):
            return any(walk(i, depth + 1) for i in node)
        return False

    return walk(payload)


# ---------------------------------------------------------------------------
# 本地预检
# ---------------------------------------------------------------------------
_IMG_EXT = (".jpg", ".jpeg", ".png", ".webp")
_VID_EXT = (".mp4", ".mov")
_AUD_EXT = (".mp3", ".wav", ".m4a")
_BGM_EXT = (".mp3", ".wav", ".m4a")


def _ext_of(url: str) -> str:
    path = urllib.parse.urlparse(url).path
    m = re.search(r"(\.[A-Za-z0-9]+)$", path)
    return m.group(1).lower() if m else ""


def validate_url_list_uniq(urls: Iterable[str]) -> List[str]:
    """上游规则：驱动媒体 / 素材 / 背景音乐 / AI 封面 的地址不能重名，重名会渲染异常。"""
    seen: Dict[str, int] = {}
    for u in urls:
        if not u:
            continue
        seen[u] = seen.get(u, 0) + 1
    dups = [u for u, n in seen.items() if n > 1]
    return dups


def validate_subtitle(subs: Any) -> List[str]:
    issues: List[str] = []
    if subs is None:
        return issues
    if not isinstance(subs, list):
        return ["subtitle 必须是数组"]
    for i, item in enumerate(subs):
        if not isinstance(item, dict):
            issues.append("subtitle[%d] 不是对象" % i)
            continue
        for key in ("startMs", "endMs", "text"):
            if key not in item:
                issues.append("subtitle[%d] 缺 %s" % (i, key))
        s, e = item.get("startMs"), item.get("endMs")
        if isinstance(s, (int, float)) and isinstance(e, (int, float)):
            if e <= s:
                issues.append("subtitle[%d] endMs(%s) 必须大于 startMs(%s)" % (i, e, s))
            if e > LIMITS["subtitle_max_ms"]:
                issues.append("subtitle[%d] endMs=%s 超过上限 %s ms"
                              % (i, e, LIMITS["subtitle_max_ms"]))
    return issues


def validate_metadata(md: Any) -> List[str]:
    """元水印只支持一组数据，且 value 必须是字符串。"""
    if md is None:
        return []
    if not isinstance(md, dict):
        return ["processRules.metadata 必须是对象"]
    issues = []
    if len(md) != 1:
        issues.append("processRules.metadata 只支持写入一组数据，当前 %d 组" % len(md))
    for k, v in md.items():
        if not isinstance(v, str):
            issues.append("processRules.metadata.%s 的值必须是字符串（当前 %s）"
                          % (k, type(v).__name__))
    return issues


def validate_struct_layers(layers: Any) -> List[str]:
    if layers is None:
        return []
    if not isinstance(layers, list):
        return ["structLayers 必须是数组"]
    issues = []
    marks = {"headerLayer", "subtitleLayer", "ipLayer", "backgroundLayer", "figureLayer"}
    for i, item in enumerate(layers):
        if not isinstance(item, dict):
            issues.append("structLayers[%d] 不是对象" % i)
            continue
        mark = item.get("markCode")
        if mark not in marks:
            issues.append("structLayers[%d].markCode=%r 不在 %s" % (i, mark, sorted(marks)))
            continue
        if mark in ("backgroundLayer", "figureLayer") and "show" in item:
            issues.append("structLayers[%d] %s 不支持设置 show" % (i, mark))
        if mark == "headerLayer" and item.get("showMode") == "customize":
            st = item.get("showTime")
            if not isinstance(st, (int, float)) or st <= 0:
                issues.append("structLayers[%d] headerLayer+showMode=customize 时 showTime 必填且 > 0" % i)
    return issues


def _probe_local_media(path: str) -> Optional[Dict[str, Any]]:
    """本地文件才探测；URL 交给平台探。ffprobe 不在则返回 None（不假装知道）。"""
    if not os.path.isfile(path):
        return None
    import shutil
    import subprocess
    ffprobe = shutil.which("ffprobe")
    info: Dict[str, Any] = {"bytes": os.path.getsize(path)}
    if not ffprobe:
        return info
    try:
        out = subprocess.run(
            [ffprobe, "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", path],
            capture_output=True, text=True, timeout=60,
        )
        meta = json.loads(out.stdout or "{}")
        fmt = meta.get("format") or {}
        if fmt.get("duration"):
            info["duration"] = float(fmt["duration"])
        for st in meta.get("streams") or []:
            if st.get("codec_type") == "video":
                info["width"] = int(st.get("width") or 0)
                info["height"] = int(st.get("height") or 0)
                break
    except Exception:
        pass
    return info


def validate_single_side(path_or_url: str, info: Optional[Dict[str, Any]]) -> List[str]:
    if not info:
        return []
    w, h = info.get("width"), info.get("height")
    if w and h and max(w, h) >= LIMITS["single_side_px"]:
        return ["%s 单边 %dx%d，平台要求单边 < %dpx"
                % (os.path.basename(path_or_url), w, h, LIMITS["single_side_px"])]
    return []


def validate_materials(materials: Any) -> List[str]:
    if not isinstance(materials, list) or not materials:
        return ["materials 必须是非空数组"]
    issues: List[str] = []
    total = 0.0
    for i, item in enumerate(materials):
        if not isinstance(item, dict):
            issues.append("materials[%d] 不是对象" % i)
            continue
        mtype = item.get("type")
        url = item.get("fileUrl")
        if mtype not in ("image", "video"):
            issues.append("materials[%d].type=%r 必须是 image 或 video" % (i, mtype))
        if not isinstance(url, str) or not url.strip():
            issues.append("materials[%d].fileUrl 不能为空" % i)
            continue
        ext = _ext_of(url)
        if mtype == "image":
            if ext and ext not in _IMG_EXT:
                issues.append("materials[%d] 图片后缀 %s 不支持（jpg/png/webp）" % (i, ext))
            total += LIMITS["material_image_sec"]
        elif mtype == "video":
            if ext and ext not in _VID_EXT:
                issues.append("materials[%d] 视频后缀 %s 不支持（mp4/mov）" % (i, ext))
            local = url if os.path.isfile(url) else None
            info = _probe_local_media(local) if local else None
            if info and info.get("duration"):
                if info["duration"] > LIMITS["material_video_max_sec"]:
                    issues.append("materials[%d] 时长 %.1fs 超过单条素材上限 %.0fs"
                                  % (i, info["duration"], LIMITS["material_video_max_sec"]))
                total += info["duration"]
            else:
                # 探不到时长就不假装知道，按 0 计并在 dry-run 里提示
                pass
    if total > LIMITS["material_total_sec"]:
        issues.append("素材总量按 %.0fs 计，超过上限 %.0fs（图片按 2s/张计）"
                      % (total, LIMITS["material_total_sec"]))
    return issues


def build_ai_label_metadata(producer: str = "", produce_id: str = "") -> Dict[str, str]:
    """AI 显式/隐式标识。value 必须是字符串（上游硬性要求）。"""
    payload = {
        "Label": "1",
        "ContentProducer": producer or "未填写内容制作方",
        "ProduceID": produce_id or ("AC-" + uuid.uuid4().hex[:16].upper()),
    }
    return {"AIGC": json.dumps(payload, ensure_ascii=False, separators=(",", ":"))}


# ---------------------------------------------------------------------------
# HTTP 客户端
# ---------------------------------------------------------------------------
class Client:
    def __init__(self, base: str = DEFAULT_BASE, key: str = "", timeout: float = 120.0,
                 verbose: bool = False, budget: Optional[float] = None,
                 dry_run: bool = False):
        # ★ 算力接口死锁：非 api.a7w.cn 一律就地拒绝（详见文件头 LOCKED_BASE 注释）
        self.base = assert_base_locked(base)
        self.key = key
        self.timeout = timeout
        self.verbose = verbose
        self.budget = budget
        self.dry_run = dry_run
        self.spent = 0.0
        self.ledger: List[Dict[str, Any]] = []

    # -- 底层 ---------------------------------------------------------------
    def _url(self, path: str, params: Optional[Dict[str, Any]] = None) -> str:
        # 约定：path 永远写成 "/apps/<app>/<api>" 这种相对 api/v1 的片段
        url = self.base + ("/" + path.lstrip("/") if path else "")
        clean = {k: v for k, v in (params or {}).items() if v is not None and v != ""}
        if clean:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(clean)
        return url

    def request(self, method: str, path: str, params: Optional[Dict[str, Any]] = None,
                body: Optional[Dict[str, Any]] = None, raw: bool = False,
                files: Optional[Dict[str, str]] = None, timeout: Optional[float] = None) -> Any:
        if self.dry_run and method.upper() != "GET":
            preview = {"dry_run": True, "method": method.upper(),
                       "url": self._url(path, params), "body": body}
            return preview

        url = self._url(path, params)
        headers = {
            "Authorization": "Bearer %s" % self.key,
            "Accept": "application/json",
            "User-Agent": UA,
        }
        data: Optional[bytes] = None

        if files:
            boundary = "----dhclip" + uuid.uuid4().hex
            parts: List[bytes] = []
            for field, filepath in files.items():
                fname = os.path.basename(filepath)
                with open(filepath, "rb") as fh:
                    blob = fh.read()
                parts.append(("--%s\r\n" % boundary).encode())
                parts.append(
                    ('Content-Disposition: form-data; name="%s"; filename="%s"\r\n'
                     % (field, fname)).encode("utf-8"))
                parts.append(b"Content-Type: application/octet-stream\r\n\r\n")
                parts.append(blob)
                parts.append(b"\r\n")
            parts.append(("--%s--\r\n" % boundary).encode())
            data = b"".join(parts)
            headers["Content-Type"] = "multipart/form-data; boundary=%s" % boundary
        elif body is not None:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"

        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        if self.verbose:
            sys.stderr.write("[dhclip] %s %s\n" % (method.upper(), url))
            if body is not None:
                sys.stderr.write("[dhclip] body=%s\n"
                                 % json.dumps(body, ensure_ascii=False)[:2000])
        # 网关 502/503/504 与连不上是常态（实测中转层会间歇性返回 nginx 502）。
        # 只对这几种重试；500 与 4xx 不重试，避免把真正的业务失败也放大成多次调用。
        retry_status = {502, 503, 504}
        attempts = 3 if method.upper() == "GET" else 2
        text = ""
        http_status = 0
        last_err = ""
        for attempt in range(1, attempts + 1):
            try:
                with urllib.request.urlopen(req, timeout=timeout or self.timeout) as resp:
                    text = resp.read().decode("utf-8", "replace")
                    http_status = resp.status
                break
            except urllib.error.HTTPError as exc:
                text = exc.read().decode("utf-8", "replace")
                http_status = exc.code
                if exc.code in retry_status and attempt < attempts:
                    last_err = "HTTP %s" % exc.code
                    if self.verbose:
                        sys.stderr.write("[dhclip] %s，%d/%d 重试\n"
                                         % (last_err, attempt, attempts))
                    time.sleep(1.5 * attempt)
                    continue
                break
            except urllib.error.URLError as exc:
                last_err = str(exc.reason)
                if attempt < attempts:
                    if self.verbose:
                        sys.stderr.write("[dhclip] 连接失败（%s），%d/%d 重试\n"
                                         % (last_err, attempt, attempts))
                    time.sleep(1.5 * attempt)
                    continue
                raise ApiError("网络不可达：%s（%s）" % (last_err, url))
            except (TimeoutError, OSError) as exc:
                last_err = str(exc)
                if attempt < attempts:
                    time.sleep(1.5 * attempt)
                    continue
                raise ApiError("请求超时或被中断：%s（%s）" % (last_err, url))

        if raw:
            return text

        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            snippet = re.sub(r"\s+", " ", text)[:300]
            if http_status >= 500:
                raise ApiError(
                    "网关 %s（不是业务错误，稍后重试即可；%s）"
                    % (http_status, snippet[:120]), http_status=http_status)
            if http_status >= 400:
                raise ApiError("HTTP %s（响应不是 JSON）：%s" % (http_status, snippet),
                               http_status=http_status)
            raise ApiError("响应不是 JSON（HTTP %s）：%s" % (http_status, snippet),
                           http_status=http_status)

        if http_status >= 400:
            # 有的网关 HTTP 非 200 但 body 里带完整错误码
            err = ""
            if isinstance(parsed, dict):
                err = _code_text(parsed)
                code = parsed.get("code")
                if isinstance(code, str) and code and not err:
                    err = code
            raise ApiError("HTTP %s：%s" % (http_status, err or "请求失败"),
                           http_status=http_status, payload=parsed)

        data = unwrap(parsed)
        cost = find_points_cost(parsed)
        if cost is None:
            cost = find_points_cost(data)
        self._record(path, method, cost)
        return data

    def _record(self, path: str, method: str, cost: Optional[float]) -> None:
        if cost is None:
            return
        self.spent += cost
        self.ledger.append({"path": path, "method": method.upper(), "points": cost})
        if self.budget is not None and self.spent > self.budget:
            raise CliError("已超出预算上限 %.4f 点（累计 %.4f 点），就地中止"
                           % (self.budget, self.spent), code=EXIT_BUDGET)

    def get(self, path: str, **kw) -> Any:
        return self.request("GET", path, **kw)

    def post(self, path: str, **kw) -> Any:
        return self.request("POST", path, **kw)

    # -- 业务接口 -----------------------------------------------------------
    def balance(self) -> Any:
        return self.get("user/balance")

    def usage(self, start_date: str = "", end_date: str = "") -> Any:
        return self.get("user/usage", params={"start_date": start_date, "end_date": end_date})

    def pricing(self, app_code: str, api_code: str) -> Any:
        return self.get("pricing", params={"type": "app_api", "app_code": app_code,
                                           "api_code": api_code})

    def app_catalog(self, app_code: str) -> Any:
        return self.get("apps/%s" % app_code)

    def upload(self, filepath: str) -> Any:
        if not os.path.isfile(filepath):
            raise CliError("文件不存在：%s" % filepath, code=EXIT_USAGE)
        return self.post("upload", files={"file": filepath})

    # 通用异步任务查询（模型任务与应用任务共用）
    def task(self, task_id: str) -> Any:
        quoted = urllib.parse.quote(str(task_id), safe="")
        return self.get("tasks/%s" % quoted)

    # --- 数字人 ---
    def lipsync_submit(self, image_url: str, audio_url: str, mode: str = "audio",
                       content: str = "", prompt: str = "", quality: str = "standard",
                       model: str = "super-lipsync-pro", **extra) -> Any:
        body: Dict[str, Any] = {
            "model": model, "mode": mode, "image_url": image_url,
            "audio_url": audio_url, "quality": quality,
        }
        if content:
            body["content"] = content
        if prompt:
            body["prompt"] = prompt
        body.update(extra)
        return self.post("apps/%s/%s" % (APP_LIPSYNC, API_LIPSYNC_SUBMIT), body=body)

    def lipsync_query(self, task_id: str) -> Any:
        return self.post("apps/%s/%s" % (APP_LIPSYNC, API_LIPSYNC_QUERY),
                         body={"task_id": task_id})

    # --- 智能剪辑 ---
    def clip_templates(self, scene: str, page_size: int = 10, sid: str = "",
                       search_key: str = "", search_value: str = "", sort_by: str = "desc") -> Any:
        params = {"scene": scene, "pageSize": page_size, "sortBy": sort_by,
                  "sid": sid, "searchKey": search_key, "searchValue": search_value}
        return self.get("apps/%s/%s" % (APP_CLIP, API_CLIP_TEMPLATE), params=params)

    def clip_template_detail(self, template_id: str) -> Any:
        return self.get("apps/%s/%s" % (APP_CLIP, API_CLIP_TEMPLATE_DETAIL),
                        params={"id": template_id})

    def _clip_submit(self, api_code: str, body: Dict[str, Any]) -> Any:
        return self.post("apps/%s/%s" % (APP_CLIP, api_code), body=body)

    def clip_realman(self, style_id: str, video_url: str, **kw) -> Any:
        body = {"styleId": style_id, "videoUrl": video_url}
        body.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return self._clip_submit(API_CLIP_REALMAN, body)

    def clip_mixcut(self, style_id: str, materials: List[Dict[str, Any]], **kw) -> Any:
        body: Dict[str, Any] = {"styleId": style_id, "materials": materials}
        body.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return self._clip_submit(API_CLIP_MIXCUT, body)

    def clip_news(self, style_id: str, title: str, materials: List[Dict[str, Any]], **kw) -> Any:
        body: Dict[str, Any] = {"styleId": style_id, "title": title, "materials": materials}
        body.update({k: v for k, v in kw.items() if v not in (None, "", [], {})})
        return self._clip_submit(API_CLIP_NEWS, body)

    # --- 语音 ---
    def tts(self, text: str, voice: str = "", fmt: str = "mp3", model: str = "",
            speed: Optional[float] = None) -> Any:
        """同步 TTS。

        ⚠️ 实测在 api.a7w.cn 上**这条同步路由是坏的**：任何参数都返回
        `{"code":0,"msg":"任务处理失败，请稍后重试"}`。要出音频请走 tts_async()。
        保留本方法是为了在修好之后可以直接切回来，以及给自建域名用。
        """
        body: Dict[str, Any] = {"text": text, "format": fmt}
        if model:
            body["model"] = model
        if voice:
            body["reference_id"] = voice
        if speed is not None:
            body["prosody"] = {"speed": speed}
        return self.post("apps/%s/%s" % (APP_TTS, API_TTS), body=body)

    def tts_async(self, text: str, voice: str = "", fmt: str = "mp3",
                  engine: str = "tts_async", model: str = "",
                  speed: Optional[float] = None, callback_url: str = "") -> Any:
        """异步 TTS（实测可用）。返回 task_id，用 wait_task() 取 audio_url。

        `engine`：`tts_async`（HTTP 上游，适合长文本 ≤10000 字符）
                  或 `tts_live`（WebSocket 流式上游，长文本）。
        两者都实测可用；`tts_async` 更便宜（实测 0.7 点 vs 0.84 点）。
        """
        body: Dict[str, Any] = {"text": text, "format": fmt}
        if model:
            body["model"] = model
        if voice:
            body["reference_id"] = voice
        if speed is not None:
            body["prosody"] = {"speed": speed}
        if callback_url:
            body["callback_url"] = callback_url
        return self.post("apps/%s/%s" % (APP_TTS, engine), body=body)

    def voices(self, title: str = "", page_size: int = 20, page_number: int = 1) -> Any:
        return self.get("apps/%s/%s" % (APP_TTS, API_TTS_VOICES),
                        params={"title": title, "page_size": page_size,
                                "page_number": page_number})

    def clone_voice(self, title: str, audio_url: str,
                    texts: Optional[List[str]] = None, visibility: str = "private",
                    description: str = "", enhance: bool = True) -> Any:
        """克隆音色：给一段参考音频，换来一个专属 reference_id。

        这是「声音和人物特别像」的唯一正路 —— 平台自带音色只是通用音色，
        不会像某个人；要么直接给本人的音频，要么用本人的音频克隆一个音色。
        """
        body: Dict[str, Any] = {"title": title, "audio_url": audio_url,
                                "visibility": visibility}
        if texts:
            body["texts"] = list(texts)
        if description:
            body["description"] = description
        if enhance:
            body["enhance_audio_quality"] = True
        return self.post("apps/%s/clone_voice" % APP_TTS, body=body)

    def stt(self, audio_url: str, language: str = "", timestamps: bool = True) -> Any:
        body: Dict[str, Any] = {"audio_url": audio_url,
                                "ignore_timestamps": not timestamps}
        if language:
            body["language"] = language
        return self.post("apps/%s/%s" % (APP_TTS, API_TTS_STT), body=body)

    # --- 参考生图（nano_banana）---
    def image_submit(self, prompt: str, action: str = IMAGE_ACTION_GENERATE,
                     image_urls: Optional[List[str]] = None, resolution: str = "1K",
                     aspect_ratio: str = "", model: str = "",
                     callback_url: str = "") -> Any:
        """提交图片任务。

        `action="edit"` + `image_urls=[参考图]` 就是「参考生图」：
        在保持参考图人物身份/风格的前提下改场景、服装、姿态。
        """
        body: Dict[str, Any] = {"prompt": prompt, "action": action,
                                "resolution": resolution}
        if image_urls:
            body["image_urls"] = list(image_urls)
        if aspect_ratio:
            body["aspect_ratio"] = aspect_ratio
        if model:
            body["model"] = model
        if callback_url:
            body["callback_url"] = callback_url
        return self.post("apps/%s/%s" % (APP_IMAGE, API_IMAGE_SUBMIT), body=body)

    def image_query(self, task_id: str) -> Any:
        return self.get("apps/%s/%s" % (APP_IMAGE, API_IMAGE_QUERY),
                        params={"task_id": task_id})

    def image_generate(self, prompt: str, ref_url: str = "", **kw) -> Any:
        """便捷封装：给了参考图就走 edit（参考生图），否则走 generate（文生图）。"""
        if ref_url:
            kw.setdefault("action", IMAGE_ACTION_EDIT)
            kw.setdefault("image_urls", [ref_url])
        else:
            kw.setdefault("action", IMAGE_ACTION_GENERATE)
        return self.image_submit(prompt, **kw)

    # -- 轮询 ---------------------------------------------------------------
    def wait_task(self, task_id: str, interval: float = 10.0, max_wait: float = 3600.0,
                  on_tick=None, use_app_query: str = "",
                  require_keys: Sequence[str] = (),
                  settle_wait: float = 240.0) -> Dict[str, Any]:
        """轮询到终态。返回 {"status":..., "data":..., "task_id":..., "elapsed":...}。

        `use_app_query`：只有该应用**确实有 query 接口**时才传
        （目前只有 pic_lipsync）。smart_clip 没有 app 级 query，
        通用路由失败就只能重试，不能乱退到别的应用的 query 上去。

        `require_keys`：要求终态响应里必须能找到这些字段（一般是视频地址）。
        **实测必须要有这个** —— 任务刚翻成 completed 时，结果体里的
        `video_url` / `videoUrl` 可能还是**空字符串**，几秒后才被填上。
        没有这个兜底就会"任务完成了却报没有视频"。
        """
        deadline = time.time() + max_wait
        started = time.time()
        attempt = 0
        last: Any = None
        sleep_for = interval
        settle_deadline = 0.0
        while True:
            attempt += 1
            try:
                if use_app_query == APP_LIPSYNC:
                    last = self.lipsync_query(task_id)
                else:
                    last = self.task(task_id)
            except ApiError as exc:
                # 不自动改道到别的应用的 query —— 那会查到不属于本任务的东西
                if time.time() > deadline:
                    raise
                sys.stderr.write("[dhclip] 查询失败（%s），稍后重试\n" % exc)
                time.sleep(sleep_for)
                sleep_for = min(sleep_for * 1.3, 30.0)
                continue

            status = resolve_task_status(last) or ""
            elapsed = time.time() - started
            if on_tick:
                on_tick(attempt, status, elapsed, last)
            if status in TERMINAL_OK:
                if not require_keys:
                    return {"status": status, "data": last, "task_id": task_id,
                            "elapsed": elapsed}
                payload_url = find_deep(last, require_keys)
                if payload_url:
                    return {"status": status, "data": last, "task_id": task_id,
                            "elapsed": elapsed, "result_url": payload_url}
                # 已完成但结果还没落全 —— 继续等一小会儿
                if settle_deadline == 0.0:
                    settle_deadline = time.time() + settle_wait
                    sys.stderr.write(
                        "   任务已 completed，但结果地址还是空的，继续等结果落全…\n")
                if time.time() > settle_deadline:
                    raise CliError(
                        "任务 %s 已 completed，但等了 %.0fs 仍未拿到结果地址"
                        "（期望字段：%s）。用 `task %s` 再查一次，"
                        "上游偶发延迟落结果。" % (task_id, settle_wait,
                                                  "/".join(require_keys), task_id),
                        code=EXIT_API, payload=last)
                time.sleep(min(5.0, sleep_for))
                continue
            if status in TERMINAL_BAD:
                msg = _code_text(last) if isinstance(last, dict) else ""
                detail = find_deep(last, ("message", "error_msg", "reason")) or msg
                raise CliError("任务 %s 终态失败：%s" % (task_id, detail or status),
                               code=EXIT_API, payload=last)
            if time.time() > deadline:
                raise CliError("等待任务 %s 超过 %.0fs 仍未结束（最后状态 %r）"
                               % (task_id, max_wait, status), code=EXIT_TIMEOUT, payload=last)
            time.sleep(sleep_for)
            sleep_for = min(sleep_for * 1.3, 30.0)


# ---------------------------------------------------------------------------
# 入参解析辅助
# ---------------------------------------------------------------------------
def parse_materials(items: Optional[Sequence[str]]) -> List[Dict[str, Any]]:
    """--material image=URL / video=URL[:soundSwitch]"""
    out: List[Dict[str, Any]] = []
    for raw in items or []:
        if "=" not in raw:
            raise CliError("--material 格式应为 type=URL，收到 %r" % raw, code=EXIT_USAGE)
        mtype, url = raw.split("=", 1)
        mtype = mtype.strip().lower()
        if mtype not in ("image", "video"):
            raise CliError("--material 类型只能是 image / video，收到 %r" % mtype,
                           code=EXIT_USAGE)
        item: Dict[str, Any] = {"type": mtype, "fileUrl": url.strip()}
        out.append(item)
    return out


def parse_kv_list(items: Optional[Sequence[str]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for raw in items or []:
        if "=" not in raw:
            raise CliError("--set 格式应为 key=value，收到 %r" % raw, code=EXIT_USAGE)
        k, v = raw.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def parse_json_arg(value: Optional[str], flag: str) -> Any:
    if not value:
        return None
    if os.path.isfile(value):
        with open(value, "r", encoding="utf-8") as fh:
            return json.load(fh)
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise CliError("%s 既不是文件也不是合法 JSON：%s" % (flag, exc), code=EXIT_USAGE)


def read_text_arg(inline: str, text_file: str) -> str:
    """取口播文案：优先读文件。

    **强烈建议用 --text-file**：中文文案走命令行很容易被 shell 的引号、
    代码页（Windows PowerShell 默认 GBK）搞坏 ——
    实测直接把中文当参数传，会被 argparse 报成 "unrecognized arguments"。
    放文件里按 UTF-8 读就完全没这个问题。
    """
    if text_file:
        if not os.path.isfile(text_file):
            raise CliError("--text-file 指向的文件不存在：%s" % text_file, code=EXIT_USAGE)
        with open(text_file, "r", encoding="utf-8-sig") as fh:
            body = fh.read().strip()
        if not body:
            raise CliError("--text-file 是空文件：%s" % text_file, code=EXIT_USAGE)
        return body
    return inline or ""


def out(obj: Any, as_json: bool = False) -> None:
    if as_json:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(_pretty(obj) + "\n")


def _pretty(obj: Any) -> str:
    if isinstance(obj, (dict, list)):
        return json.dumps(obj, ensure_ascii=False, indent=2)
    return str(obj)


# ---------------------------------------------------------------------------
# 配置与凭据
# ---------------------------------------------------------------------------
def load_key(explicit: str = "") -> str:
    if explicit:
        return explicit.strip()
    for env in ("AVATAR_AUTOCLIP_KEY", "A7W_API_KEY", "A7W_KEY", "LIKEADMIN_API_KEY"):
        val = os.environ.get(env)
        if val and val.strip():
            return val.strip()
    for path in (
        os.path.join(os.path.expanduser("~"), ".a7w", "config.json"),
        os.path.join(os.path.expanduser("~"), ".likeadmin", "config.json"),
    ):
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            for k in ("key", "api_key", "apiKey", "token"):
                if isinstance(data.get(k), str) and data[k].strip():
                    return data[k].strip()
        except Exception:
            continue
    raise CliError(
        "没有找到 API Key。用 --key、或设 AVATAR_AUTOCLIP_KEY 环境变量。\n"
        "  注册领 Key：https://api.a7w.cn/", code=EXIT_USAGE)


def require_authorization(args) -> None:
    """人像/声音属于人格权，不是版权。没有显式声明就不做人像合成。"""
    if getattr(args, "authorized", False):
        return
    if os.environ.get("AVATAR_AUTOCLIP_AUTHORIZED", "").strip() in ("1", "true", "yes"):
        return
    raise CliError(
        "拒绝执行：涉及真实人像/声音的合成，必须显式声明已获得授权。\n"
        "  确认你拥有该人像与该声音的使用权后，加 --authorized 重跑。\n"
        "  可以用 AVATAR_AUTOCLIP_AUTHORIZED=1 环境变量常驻声明。",
        code=EXIT_AUTHZ)


# ---------------------------------------------------------------------------
# 子命令
# ---------------------------------------------------------------------------
def _tick_factory(quiet: bool):
    def _tick(attempt, status, elapsed, payload):
        if quiet:
            return
        sys.stderr.write("  [%6.0fs] #%d %s\n" % (elapsed, attempt, status or "unknown"))
    return _tick


def cmd_balance(client: Client, args) -> int:
    data = client.balance()
    out(data, args.json)
    return EXIT_OK


def cmd_pricing(client: Client, args) -> int:
    pairs = [(APP_LIPSYNC, API_LIPSYNC_SUBMIT), (APP_CLIP, API_CLIP_REALMAN),
             (APP_CLIP, API_CLIP_MIXCUT), (APP_CLIP, API_CLIP_NEWS),
             (APP_CLIP, API_CLIP_TEMPLATE), (APP_TTS, API_TTS)]
    result = {}
    for app, api in pairs:
        try:
            result["%s/%s" % (app, api)] = client.pricing(app, api)
        except CliError as exc:
            result["%s/%s" % (app, api)] = {"error": str(exc)}
    out(result, args.json)
    return EXIT_OK


def cmd_voices(client: Client, args) -> int:
    data = client.voices(title=args.title, page_size=args.limit)
    out(data, args.json)
    return EXIT_OK


def cmd_tts(client: Client, args) -> int:
    """文案 → 音频。默认走异步路由（同步那条在上游是坏的）。"""
    text = read_text_arg(args.text, args.text_file)
    if not text:
        raise ValidationError("缺少文案：用 --text 或 --text-file（推荐后者）")
    engine = getattr(args, "engine", "tts_async")
    if args.dry_run:
        out({"dry_run": True, "engine": engine, "text_len": len(text),
             "text": text[:60], "voice": args.voice or "<平台默认音色>"}, True)
        return EXIT_OK
    voice = _resolve_voice(client, args.voice)
    url = tts_to_audio(client, text, voice=voice, engine=engine, args=args)
    if args.json:
        out({"audio_url": url, "engine": engine, "voice": voice,
             "text_len": len(text)}, True)
    else:
        out({"audio_url": url})
    return EXIT_OK


def cmd_upload(client: Client, args) -> int:
    data = client.upload(args.file)
    out(data, args.json)
    return EXIT_OK


def cmd_task(client: Client, args) -> int:
    if getattr(args, "wait", False):
        return _finish_wait(client, args.task_id, args)
    data = client.task(args.task_id)
    if args.json:
        out(data, True)
        return EXIT_OK
    out({
        "status": resolve_task_status(data),
        "video_url": find_deep(data, VIDEO_KEYS),
        "cover_url": find_deep(data, COVER_KEYS),
        "raw": data,
    })
    return EXIT_OK


def cmd_templates(client: Client, args) -> int:
    """列模板。--table 打成一列带序号的清单，方便直接挑。"""
    if args.all:
        results: List[Any] = []
        sid = ""
        for _ in range(50):
            data = client.clip_templates(args.scene, page_size=args.page_size, sid=sid)
            items = (data or {}).get("results") if isinstance(data, dict) else data
            if not isinstance(items, list) or not items:
                break
            results.extend(items)
            sid = (data or {}).get("sid") if isinstance(data, dict) else None
            if not sid:
                break
        return _render_templates(results, args)

    data = client.clip_templates(args.scene, page_size=args.page_size,
                                 search_key=args.search_key, search_value=args.search_value,
                                 sort_by=args.sort_by)
    items = (data or {}).get("results") if isinstance(data, dict) else data
    return _render_templates(items if isinstance(items, list) else [], args,
                             sid=(data or {}).get("sid") if isinstance(data, dict) else None)


def _render_templates(items: List[Any], args, sid: Optional[str] = None) -> int:
    if args.json:
        payload: Dict[str, Any] = {"results": items}
        if sid:
            payload["sid"] = sid
        out(payload, True)
        return EXIT_OK
    if not items:
        out("（该场景下没有取到模板）")
        return EXIT_OK
    out("场景 %s 共 %d 条模板：" % (args.scene, len(items)))
    out("")
    out("  #   模板名称            比例    模板 ID")
    out("  --  ------------------  ------  ------------------------")
    for i, item in enumerate(items):
        out("  %-2d  %-18s  %-6s  %s"
            % (i, str(item.get("name") or "")[:18],
               str(item.get("ratio") or "-"), item.get("id")))
    out("")
    out("用 --template <ID> 指定，或直接 --template-index <#> 按序号挑。")
    if sid:
        out("（还有下一页，加 --all 翻完）")
    return EXIT_OK


def cmd_template(client: Client, args) -> int:
    data = client.clip_template_detail(args.id)
    if args.json:
        out(data, True)
        return EXIT_OK
    edit = ((data or {}).get("videoStructInfo") or {}).get("editInfo") or {}
    canvas = edit.get("canvas") or {}
    layers = {k: (v if v else "（模板无此图层）")
              for k, v in ((name, edit.get(name)) for name in
                           ("headerLayer", "subtitleLayer", "ipLayer",
                            "figureLayer", "backgroundLayer"))}
    out({
        "id": (data or {}).get("id"),
        "name": (data or {}).get("name"),
        "scene": (data or {}).get("scene"),
        "canvas": canvas,
        "layers": {k: ("有" if v != "（模板无此图层）" else v) for k, v in layers.items()},
        "raw": data,
    })
    return EXIT_OK


def _clip_common_body(args, client: Client) -> Dict[str, Any]:
    """拼装三个剪辑接口共有的可选字段。

    各子命令暴露的开关并不完全一致（news 没有 --preprocess，realman 没有
    --video-duration），所以这里一律用 getattr 取，不要直接 args.xxx，
    否则会 AttributeError。
    """
    body: Dict[str, Any] = {}
    g = lambda name, default=None: getattr(args, name, default)  # noqa: E731

    if g("title"):
        body["title"] = g("title")
    if g("language"):
        body["language"] = g("language")
    if g("introduce_name") or g("introduce_desc"):
        body["introduceCard"] = {"name": g("introduce_name", "") or "",
                                 "description": g("introduce_desc", "") or ""}
    pack: Dict[str, Any] = {}
    for flag, key in (("pack_header", "headerSwitch"), ("pack_material", "materialSwitch"),
                      ("pack_subtitle", "subtitleSwitch"), ("pack_keyword", "keywordSwitch")):
        val = g(flag)
        if val is not None:
            pack[key] = bool(val)
    bgm_url, bgm_volume, bgm_off = g("bgm_url", ""), g("bgm_volume"), g("bgm_off", False)
    if bgm_url or bgm_volume is not None or bgm_off:
        bgm: Dict[str, Any] = {}
        if bgm_off:
            bgm["audioSwitch"] = False
        elif bgm_url:
            bgm["audioSwitch"] = True
            bgm["audioUrl"] = bgm_url
        if bgm_volume is not None:
            if not 0 <= bgm_volume <= 1:
                raise ValidationError("--bgm-volume 必须在 0~1（保留一位小数）")
            bgm["volume"] = bgm_volume
        pack["backgroundMusic"] = bgm
    if pack:
        body["packRules"] = pack

    process: Dict[str, Any] = {}
    if g("ai_label"):
        process["watermarkShow"] = True
        process["metadata"] = build_ai_label_metadata(g("producer", ""), g("produce_id", ""))
    elif g("metadata"):
        process["metadata"] = g("metadata")
        issues = validate_metadata(g("metadata"))
        if issues:
            raise ValidationError("metadata 预检不通过", issues)
    if g("preprocess"):
        process["resourcePreprocessMethod"] = g("preprocess")
    if g("match_way"):
        process["materialMatchWay"] = g("match_way")
    if g("video_duration") is not None:
        lo, hi = LIMITS["news_duration_sec"]
        if not lo <= g("video_duration") <= hi:
            raise ValidationError("--video-duration 必须在 %d~%d 秒" % (lo, hi))
        process["videoDuration"] = g("video_duration")
    if g("composition"):
        process["materialComposition"] = g("composition")
    if g("cover_result_url") or g("cover_image_url"):
        cover: Dict[str, Any] = {"coverSwitch": True}
        if g("cover_template_id"):
            cover["templateId"] = g("cover_template_id")
        if g("cover_image_url"):
            cover["imageUrl"] = g("cover_image_url")
        if g("cover_result_url"):
            cover["resultImageUrl"] = g("cover_result_url")
        process["firstFrameCover"] = cover
    if process:
        body["processRules"] = process

    if g("subtitle"):
        body["subtitle"] = g("subtitle")
    if g("struct_layers"):
        body["structLayers"] = g("struct_layers")
    if g("callback_url"):
        body["callbackUrl"] = g("callback_url")
    if g("material_sound") is not None:
        body["materialSoundSwitch"] = bool(g("material_sound"))
    body.update(parse_kv_list(g("set", [])))
    return body


def _guarded_submit(client: Client, kind: str, body: Dict[str, Any], issues: List[str],
                    args) -> int:
    if issues:
        raise ValidationError("%s 预检不通过（%d 项）" % (kind, len(issues)), issues)
    if args.dry_run:
        out({"dry_run": True, "kind": kind, "body": body}, True)
        return EXIT_OK
    if not args.json:
        sys.stderr.write("提交 %s …\n" % kind)
    if kind == "realman_broadcast":
        data = client.clip_realman(body["styleId"], body["videoUrl"],
                                   **{k: v for k, v in body.items()
                                      if k not in ("styleId", "videoUrl")})
    elif kind == "broadcast_mixcut":
        data = client.clip_mixcut(body["styleId"], body["materials"],
                                  **{k: v for k, v in body.items()
                                     if k not in ("styleId", "materials")})
    elif kind == "news_mixcut":
        data = client.clip_news(body["styleId"], body["title"], body["materials"],
                                **{k: v for k, v in body.items()
                                   if k not in ("styleId", "title", "materials")})
    else:
        raise CliError("未知提交类型 %s" % kind, code=EXIT_USAGE)

    task_id = _extract_task_id(data)
    if not task_id:
        out({"submitted": True, "task_id": None, "raw": data}, args.json)
        return EXIT_OK
    if args.json and not args.wait:
        out({"task_id": task_id, "raw": data}, True)
        return EXIT_OK
    sys.stderr.write("已提交 task_id=%s\n" % task_id)
    if not args.wait:
        out({"task_id": task_id, "status": resolve_task_status(data), "raw": data}, args.json)
        return EXIT_OK

    try:
        return _finish_wait(client, task_id, args)
    except CliError as exc:
        # 实测：上游对 subtitle[] 的条数很敏感 —— 塞十几条以上会以
        # "任务处理失败，请稍后重试" 终态失败，而去掉 subtitle 同样参数就成功。
        # 与其让用户自己猜，不如自动退一次：去掉字幕重跑，把平台的自动字幕用上。
        # args.json 不影响是否重试：重试的提示一律走 stderr，JSON 只在最后输出一次
        if exc.code != EXIT_API or not body.get("subtitle"):
            raise
        n = len(body["subtitle"])
        sys.stderr.write(
            "   [警告] 带 %d 条 subtitle 的任务失败了：%s\n"
            "          这通常是上游对字幕条数的限制。自动去掉 subtitle 重试一次"
            "（改用平台自动字幕）…\n" % (n, exc))
        body.pop("subtitle", None)
        if kind == "realman_broadcast":
            data = client.clip_realman(body["styleId"], body["videoUrl"],
                                       **{k: v for k, v in body.items()
                                          if k not in ("styleId", "videoUrl")})
        elif kind == "broadcast_mixcut":
            data = client.clip_mixcut(body["styleId"], body["materials"],
                                      **{k: v for k, v in body.items()
                                         if k not in ("styleId", "materials")})
        else:
            data = client.clip_news(body["styleId"], body["title"], body["materials"],
                                    **{k: v for k, v in body.items()
                                       if k not in ("styleId", "title", "materials")})
        retry_id = _extract_task_id(data)
        if not retry_id:
            raise
        sys.stderr.write("          重试 task_id=%s\n" % retry_id)
        return _finish_wait(client, retry_id, args)


def _extract_task_id(data: Any) -> Optional[str]:
    if isinstance(data, dict):
        for k in ("task_id", "taskId", "id"):
            val = data.get(k)
            if isinstance(val, str) and val.strip():
                return val.strip()
        tid = find_deep(data, ("task_id", "taskId"))
        if tid:
            return tid
    return None


def _finish_wait(client: Client, task_id: str, args) -> int:
    try:
        result = client.wait_task(task_id, interval=args.poll_interval,
                                  max_wait=args.max_wait,
                                  on_tick=_tick_factory(args.json),
                                  use_app_query=args.app_query or "",
                                  require_keys=VIDEO_KEYS)
    except CliError as exc:
        if exc.code == EXIT_TIMEOUT:
            sys.stderr.write("%s\n" % exc)
            sys.stderr.write("任务仍在跑，可用 `task %s` 继续查。\n" % task_id)
        raise
    payload = result["data"]
    video = find_deep(payload, VIDEO_KEYS)
    out({
        "task_id": task_id,
        "status": result["status"],
        "elapsed_sec": round(result["elapsed"], 1),
        "video_url": video,
        "cover_url": find_deep(payload, COVER_KEYS),
        "duration": find_number(payload, ("duration",)),
        "points_cost": find_points_cost(payload),
        "raw": payload,
    }, args.json)
    return EXIT_OK


def collect_image_urls(payload: Any) -> List[str]:
    """把图片结果里的所有图片地址按出现顺序收全（去重）。

    nano_banana 的结果结构实测有三层都放图：
      result.image_url / result.data[].image_url / result.results[].image_url
    所以不能只取一个字段，要把三层都收上来再去重。
    """
    found: List[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for k in ("image_url", "image_uri", "imageUrl"):
                val = node.get(k)
                if isinstance(val, str) and val.strip().startswith("http"):
                    if val.strip() not in found:
                        found.append(val.strip())
            for val in node.values():
                walk(val)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(payload)
    return found


# 参考生图的默认分镜：同一个人、不同场景与服装。
# 目的是给数字人准备一批「同一身份、可直接拿去做口播」的竖版人物图。
DEFAULT_SHOTS = [
    "在明亮的居家厨房里对着镜头说话的半身近景，穿白色短袖T恤，自然微笑，双手有轻微手势",
    "在客厅沙发前对着镜头讲解的半身近景，穿浅灰色针织衫，放松自然",
    "在书房办公桌前对着镜头讲解的半身近景，穿深色衬衫，专注神情",
    "在明亮的纯色背景工作室里正面半身口播，职业休闲装扮，干净背景",
    "在户外街景自然光下对着镜头微笑的半身近景，穿休闲外套",
    "在咖啡厅里对着镜头聊天的半身近景，穿米色毛衣，暖色调光线",
]

# 身份一致性前缀：参考生图最关键的一句，不能省
IDENTITY_PREFIX = ("保持参考图里同一个人的面部特征、五官比例、发型与整体气质完全一致，"
                   "只改变场景、服装与姿态；")


def build_shot_prompt(shot: str, identity_prefix: str = IDENTITY_PREFIX) -> str:
    return "%s%s。真实照片质感，竖版构图，光线自然。" % (identity_prefix, shot)


def cmd_portraits(client: Client, args) -> int:
    """参考生图：1 张参考图 → N 张同风格人物图。"""
    shots = list(args.shot) if args.shot else DEFAULT_SHOTS
    n = args.n
    if n <= 0:
        raise CliError("--n 必须大于 0", code=EXIT_USAGE)
    if not args.ref and not args.allow_no_ref:
        raise CliError(
            "缺少 --ref（参考图 URL）。参考生图靠它保住人物身份一致性。\n"
            "  确实想纯文生图（不保身份）就加 --allow-no-ref。", code=EXIT_USAGE)
    if args.ref:
        require_authorization(args)

    # 分镜不够就循环复用
    plan = [shots[i % len(shots)] for i in range(n)]

    if args.dry_run:
        out({"dry_run": True, "action": IMAGE_ACTION_EDIT if args.ref else IMAGE_ACTION_GENERATE,
             "ref": args.ref or None, "resolution": args.resolution,
             "aspect_ratio": args.aspect_ratio,
             "shots": [build_shot_prompt(s, args.identity_prefix) for s in plan]}, True)
        return EXIT_OK

    results: List[Dict[str, Any]] = []
    for idx, shot in enumerate(plan):
        prompt = build_shot_prompt(shot, args.identity_prefix)
        sys.stderr.write("[%d/%d] 生图：%s\n" % (idx + 1, n, shot[:40]))
        try:
            data = client.image_generate(prompt, ref_url=args.ref,
                                         resolution=args.resolution,
                                         aspect_ratio=args.aspect_ratio,
                                         model=args.model or "")
            task_id = _extract_task_id(data)
            if not task_id:
                results.append({"index": idx, "shot": shot, "error": "no task_id",
                                "raw": data})
                continue
            res = client.wait_task(task_id, interval=args.poll_interval,
                                   max_wait=args.max_wait,
                                   require_keys=("image_url", "image_uri", "imageUrl"))
            urls = collect_image_urls(res["data"])
            results.append({"index": idx, "shot": shot, "task_id": task_id,
                            "status": res["status"], "image_url": urls[0] if urls else None,
                            "image_urls": urls,
                            "points_cost": find_points_cost(res["data"])})
            sys.stderr.write("        -> %s\n" % (urls[0] if urls else "（没拿到图片地址）"))
        except CliError as exc:
            sys.stderr.write("        失败：%s\n" % exc)
            results.append({"index": idx, "shot": shot, "error": str(exc)})

    ok = [r for r in results if r.get("image_url")]
    manifest = {"ref": args.ref or None, "resolution": args.resolution,
                "aspect_ratio": args.aspect_ratio,
                "count": len(ok), "images": results}
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, ensure_ascii=False, indent=2)
        sys.stderr.write("已写出清单：%s\n" % args.out)

    if args.json:
        out(manifest, True)
    else:
        out("参考生图完成：%d/%d 张可用" % (len(ok), n))
        out("")
        out("  #   图片地址")
        out("  --  ------------------------------------------------------------")
        for r in ok:
            out("  %-2d  %s" % (r["index"], r["image_url"]))
        out("")
        out("挑一张做数字人：把地址传给 make 的 --image，"
            "或用 make --ref … --portrait-index <#>。")
    return EXIT_OK if ok else EXIT_API


def _find_asr_segments(payload: Any, _depth: int = 0) -> List[Dict[str, Any]]:
    """在 ASR 返回里找字级分段数组。

    实测 `voice_tts/stt`（ignore_timestamps=false）返回：
      data.result.segments = [{"start":0,"end":0.16,"text":"大"}, …]
      data.result.text     = "大家好，欢迎来到今天的分享。"   ← 带标点的完整文本
    单位是**秒**，且是**单字符**粒度。
    """
    if _depth > 8:
        return []
    if isinstance(payload, dict):
        for key in ("segments", "words", "items"):
            val = payload.get(key)
            if isinstance(val, list) and val and isinstance(val[0], dict):
                if any(k in val[0] for k in ("start", "startMs", "start_time")):
                    return val
        for val in payload.values():
            found = _find_asr_segments(val, _depth + 1)
            if found:
                return found
    elif isinstance(payload, list):
        if payload and isinstance(payload[0], dict) and \
                any(k in payload[0] for k in ("start", "startMs", "start_time")):
            return payload
    return []


_PUNCT = set("，。！？、；：,.!?;:…—－-～~“”‘’\"'()（）《》〈〉【】[]〔〕 \t\n\r")


def _seg_time_ms(item: Dict[str, Any], which: str) -> Optional[float]:
    for key in ("%sMs" % which, "%ss" % which, "%s_%s" % (which, "ms" if which == "start" else "ms"),
                which, "%s_time" % which):
        if key in item:
            try:
                val = float(item[key])
            except (TypeError, ValueError):
                continue
            # 带 Ms 后缀或键名就是 startMs 的按毫秒，否则按秒
            if key.endswith("Ms") or key.endswith("_ms"):
                return val
            return val * 1000.0 if val < 1000 else val
    return None


def _align_punctuation(items: List[Dict[str, Any]], full_text: str) -> List[Dict[str, Any]]:
    """把完整文本里的标点补回字级分段。

    上游字级分段**不含标点**，但完整 `text` 里有（"大家好，欢迎…"）。
    按字符顺序对齐，把标点挂到它前面那个字上。

    ⚠️ 对齐**失败就不猜** —— 只有当完整文本去掉标点后与分段字符完全一致时才动手，
    否则原样返回（前端照着对齐后标点在句中的位置硬塞会错位）。
    """
    if not full_text or not items:
        return items
    texts = [str(it.get("text") or "") for it in items]
    stripped = "".join(ch for ch in full_text if ch not in _PUNCT)
    if stripped != "".join(texts):
        return items

    out: List[str] = []
    for it in items:
        out.append("")
    i = 0
    for ch in full_text:
        if ch in _PUNCT:
            k = len([x for x in out[:i] if x]) - 1
            if k >= 0:
                out[k] += ch
            continue
        if i < len(out):
            out[i] = ch
            i += 1
        else:
            out[-1] += ch
    for n, it in enumerate(items):
        it["text"] = out[n] or texts[n]
    return items


def subtitles_from_asr(payload: Any, align_text: bool = True,
                       min_ms: int = 40) -> List[Dict[str, int]]:
    """把 ASR 结果转成 `subtitle[]`（上游要的 startMs/endMs/text）。

    上游对 `subtitle[]` 有三个硬约束，这里一一兜住：
      1. `text` 是**单字符级别** —— 正好匹配 ASR 的字级分段
      2. `endMs` 必须 **> startMs** —— 实测有 `{"start":0.8,"end":0.8}` 这种零时长段
      3. `endMs` 上限 **310000**
    """
    segments = _find_asr_segments(payload)
    if not segments:
        return []

    items: List[Dict[str, Any]] = []
    for seg in segments:
        st = _seg_time_ms(seg, "start")
        en = _seg_time_ms(seg, "end")
        if st is None:
            continue
        if en is None or en <= st:
            en = st + min_ms
        text = seg.get("text")
        if text is None:
            text = seg.get("word") or seg.get("value") or ""
        items.append({"startMs": int(round(st)), "endMs": int(round(en)),
                      "text": str(text)})

    if not items:
        return []

    # 零时长/反序修正
    for idx, item in enumerate(items):
        if item["endMs"] <= item["startMs"]:
            nxt = items[idx + 1]["startMs"] if idx + 1 < len(items) else None
            cand = nxt if (nxt is not None and nxt > item["startMs"]) else item["startMs"] + min_ms * 3
            item["endMs"] = max(item["startMs"] + min_ms, cand)

    # 单调不重叠
    for idx in range(1, len(items)):
        if items[idx]["startMs"] < items[idx - 1]["endMs"]:
            items[idx]["startMs"] = items[idx - 1]["endMs"]
        if items[idx]["endMs"] <= items[idx]["startMs"]:
            items[idx]["endMs"] = items[idx]["startMs"] + min_ms

    # 上限
    cap = LIMITS["subtitle_max_ms"]
    for item in items:
        if item["endMs"] > cap:
            item["endMs"] = cap
        if item["startMs"] >= cap:
            item["startMs"] = cap - min_ms
            item["endMs"] = cap

    if align_text:
        full = ""
        if isinstance(payload, dict):
            full = str(payload.get("text") or "")
            if not full:
                inner = payload.get("result")
                if isinstance(inner, dict):
                    full = str(inner.get("text") or "")
        items = _align_punctuation(items, full)

    return items


def merge_subtitles(subs: List[Dict[str, Any]], max_chars: int = 18,
                    max_ms: int = 4000, hard_end_ms: Optional[int] = None
                    ) -> List[Dict[str, Any]]:
    """把字级字幕合并成句级字幕。

    上游文档说 `subtitle[].text` 只支持单字符，但**实测把 76 条单字符字幕整段传进去
    会被拒绝**（`{"code":0,"msg":"任务处理失败，请稍后重试"}`），
    去掉 subtitle[] 后同样参数就成功。所以按句合并成长度合理的条目更稳。

    合并规则：遇到标点（，。！？等）就断句；再按 max_chars / max_ms 兜住长句。
    另外把结尾 clamp 到 hard_end_ms（视频时长）以内 —— 字幕超出片子长度
    也是上游可能拒的一种情况。
    """
    if not subs:
        return []
    merged: List[Dict[str, Any]] = []
    cur: Optional[Dict[str, Any]] = None
    break_chars = set("，。！？；：、,.!?;:")

    for item in subs:
        text = str(item.get("text") or "")
        if cur is None:
            cur = {"startMs": item["startMs"], "endMs": item["endMs"], "text": text}
        else:
            too_long = len(cur["text"]) + len(text) > max_chars
            too_long_time = item["endMs"] - cur["startMs"] > max_ms
            if too_long or too_long_time:
                merged.append(cur)
                cur = {"startMs": item["startMs"], "endMs": item["endMs"], "text": text}
            else:
                cur["text"] += text
                cur["endMs"] = item["endMs"]
        if cur["text"] and cur["text"][-1] in break_chars:
            merged.append(cur)
            cur = None
    if cur is not None:
        merged.append(cur)

    if hard_end_ms:
        for item in merged:
            if item["startMs"] >= hard_end_ms:
                item["startMs"] = max(0, hard_end_ms - 200)
            if item["endMs"] > hard_end_ms:
                item["endMs"] = hard_end_ms
            if item["endMs"] <= item["startMs"]:
                item["endMs"] = min(hard_end_ms, item["startMs"] + 200)
    return merged


def cmd_clone(client: Client, args) -> int:
    """克隆音色 → 拿到专属 reference_id，再用它做 TTS，声音才像本人。"""
    data = client.clone_voice(args.title, args.audio, texts=args.text,
                              visibility=args.visibility,
                              description=args.description, enhance=args.enhance)
    voice_id = find_deep(data, ("reference_id", "id", "model_id", "voice_id"))
    if not voice_id:
        raise CliError("克隆返回里没找到音色 ID：%s" % _pretty(data))
    if args.json:
        out({"voice_id": voice_id, "title": args.title, "raw": data}, True)
    else:
        out("音色已创建：%s" % voice_id)
        out("")
        out("用法：把 %s 作为 --voice 传给 tts 或 make：" % voice_id)
        out("  python -X utf8 scripts/dhclip.py tts --text \"文案\" --voice %s" % voice_id)
    return EXIT_OK


def cmd_asr(client: Client, args) -> int:
    """语音转文字 → 可直接喂给剪辑接口的 subtitle[]（字级时间轴）。"""
    data = client.stt(args.audio, language=args.language, timestamps=True)
    subs = subtitles_from_asr(data)
    if not subs:
        raise CliError(
            "ASR 没有返回字级分段，拿不到 subtitle[]。原始返回：%s" % _pretty(data))
    payload: Dict[str, Any] = {"count": len(subs), "subtitle": subs}
    if getattr(args, "merge", False):
        payload["subtitle"] = merge_subtitles(subs, max_chars=getattr(args, "max_chars", 18))
        payload["merged_count"] = len(payload["subtitle"])
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(payload["subtitle"], fh, ensure_ascii=False, indent=2)
        sys.stderr.write("已写出 subtitle：%s（%d 条%s）\n"
                         % (args.out, len(payload["subtitle"]),
                            "，已按句合并" if getattr(args, "merge", False) else "，字级"))
    if args.json:
        out(payload, True)
    else:
        out("识别到 %d 个字级分段：" % len(subs))
        for item in subs[:20]:
            out("  %7d → %7d  %s" % (item["startMs"], item["endMs"], item["text"]))
        if len(subs) > 20:
            out("  …（共 %d 条）" % len(subs))
        if getattr(args, "merge", False):
            out("")
            out("按句合并后 %d 条：" % len(payload["subtitle"]))
            for item in payload["subtitle"]:
                out("  %7d → %7d  %s" % (item["startMs"], item["endMs"], item["text"]))
    return EXIT_OK


# ffmpeg 的候选位置：PATH 找不到时兜底搜这些。
# 存在的意义：本机 ffmpeg 常常放在**带中文的目录**下，用户手动配 PATH 很容易踩编码坑；
# 这里自动找到就能省掉那一步。也可以用 DHC_FFMPEG 环境变量显式指定。
FFMPEG_HINTS = (
    os.path.join(os.path.expanduser("~"), "Downloads", "_sjj-extract", "sujianjian"),
    os.path.join(os.path.expanduser("~"), "ffmpeg", "bin"),
    os.path.join(os.path.expanduser("~"), "scoop", "shims"),
    r"C:\ffmpeg\bin",
    r"C:\tools\ffmpeg\bin",
)


def _have_ffmpeg() -> Optional[str]:
    """找一个可用的 ffmpeg：环境变量 → PATH → 常见目录。"""
    import shutil
    explicit = os.environ.get("DHC_FFMPEG", "").strip()
    if explicit and os.path.isfile(explicit):
        return explicit
    found = shutil.which("ffmpeg")
    if found:
        return found
    for base in FFMPEG_HINTS:
        for name in ("ffmpeg.exe", "ffmpeg"):
            cand = os.path.join(base, name)
            if os.path.isfile(cand):
                return cand
    return None


def fit_image_local(client: Client, url: str, size: str, workdir: str = "",
                    quiet: bool = False) -> str:
    """把图片按目标尺寸缩放裁剪后重新上传，返回新的公网 URL。

    为什么要这一步（实测）：
      * 数字人的输入图有**单边 < 2000px** 的限制，2K 生图出来是 1536×2752（单边 2752）会被拒；
      * 而 `quality=max` 时数字人**按输入图的分辨率输出** —— 输入 768 宽就只能出 768 宽，
        最后被 1080×1920 的模板放大 1.4 倍，画面就发虚。

    所以最优链路是：2K 生图 → 本地缩放到 1080×1920 → 上传 → 数字人 max → 成片不放大。

    依赖 ffmpeg；没有 ffmpeg 时原样返回并说明原因（不假装成功）。
    """
    m = re.match(r"^\s*(\d+)\s*[xX*]\s*(\d+)\s*$", str(size))
    if not m:
        raise CliError("--fit 格式应为 宽x高，例如 1080x1920", code=EXIT_USAGE)
    width, height = int(m.group(1)), int(m.group(2))

    ffmpeg = _have_ffmpeg()
    if not ffmpeg:
        sys.stderr.write("    [警告] 没找到 ffmpeg，跳过 --fit 缩放（画面可能被模板放大）\n")
        return url

    import subprocess
    import tempfile
    # 默认落在**当前目录**而不是系统临时目录：
    # 实测在受限环境下 ffmpeg 写系统 Temp 会 `Could not open file ... I/O error`，
    # 而写当前工作目录正常。文件名带随机串，用完即删。
    workdir = workdir or os.getcwd()
    try:
        os.makedirs(workdir, exist_ok=True)
    except OSError:
        workdir = tempfile.gettempdir()
    src = os.path.join(workdir, "fit_src_%s" % uuid.uuid4().hex[:8])
    dst = os.path.join(workdir, "fit_%dx%d_%s.jpg" % (width, height, uuid.uuid4().hex[:8]))

    try:
        with urllib.request.urlopen(url, timeout=180) as resp:
            blob = resp.read()
        suffix = _ext_of(url) or ".jpg"
        src += suffix
        with open(src, "wb") as fh:
            fh.write(blob)
        # 先按短边撑满，再居中裁剪 —— 保证目标比例且不变形
        vf = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d"
              % (width, height, width, height))
        proc = subprocess.run([ffmpeg, "-v", "error", "-y", "-i", src,
                               "-vf", vf, "-q:v", "2", dst],
                              capture_output=True, text=True, timeout=180)
        if proc.returncode != 0 or not os.path.isfile(dst):
            sys.stderr.write("    [警告] ffmpeg 缩放失败（%s），用原图继续\n"
                             % (proc.stderr or "").strip()[:120])
            return url
        up = client.upload(dst)
        new_url = find_deep(up, ("url", "file_url", "path"))
        if not new_url:
            sys.stderr.write("    [警告] 缩放后上传没拿到 URL，用原图继续\n")
            return url
        if not quiet:
            sys.stderr.write("    已本地缩放并上传：%dx%d -> %s\n"
                             % (width, height, new_url))
        return new_url
    except Exception as exc:  # 网络/磁盘/ffmpeg 任一环节失败都不该打断出片
        sys.stderr.write("    [警告] --fit 处理失败（%s），用原图继续\n" % exc)
        return url
    finally:
        for path in (src, dst):
            try:
                if os.path.isfile(path):
                    os.unlink(path)
            except OSError:
                pass


def cmd_fit(client: Client, args) -> int:
    """把一张图缩放到目标尺寸并上传，返回可直接用于数字人的 URL。"""
    url = fit_image_local(client, args.image, args.size, workdir=args.workdir,
                          quiet=args.json)
    if args.json:
        out({"image_url": url, "size": args.size}, True)
    else:
        out(url)
    return EXIT_OK



def submit_dh_and_wait(client: Client, args, image_url: str, audio_url: str,
                       mode: str = "audio", content: str = "",
                       prompt: str = "", quality: str = "standard",
                       model: str = "super-lipsync-pro",
                       retries: int = 2, on_task=None,
                       on_retry=None) -> str:
    """提交数字人并等到出片，返回视频 URL。瞬时故障自动重试。

    实测 `elastic_machine_lost_after_submit`（弹性机器丢失）会随机出现，
    失败任务不扣费，所以直接重提一次是最省事的正确做法。

    `on_task(task_id, attempt)` / `on_retry(exc, attempt, wait_s)` 是给上层
    （比如网页工作流）汇报进度用的回调 —— **务必把 task_id 暴露出来**，
    否则任务号只写在 stderr 里，前端看不到、断了就没法续查。
    """
    last_exc: Optional[CliError] = None
    for attempt in range(1, retries + 2):
        sub = client.lipsync_submit(image_url, audio_url, mode=mode, content=content,
                                    prompt=prompt, quality=quality, model=model)
        task_id = _extract_task_id(sub)
        if not task_id:
            raise CliError("数字人提交后没有拿到 task_id：%s" % _pretty(sub))
        sys.stderr.write("   task_id=%s（第 %d 次尝试）\n" % (task_id, attempt))
        if on_task:
            on_task(task_id, attempt)
        try:
            res = client.wait_task(task_id, interval=args.poll_interval,
                                   max_wait=args.max_wait,
                                   on_tick=_tick_factory(args.json),
                                   require_keys=VIDEO_KEYS)
        except CliError as exc:
            last_exc = exc
            if attempt <= retries and is_transient_error(exc.payload):
                wait_s = 15 * attempt
                sys.stderr.write("   [重试] 上游瞬时故障（%s），%d 秒后重新提交…\n"
                                 % (exc, wait_s))
                if on_retry:
                    on_retry(exc, attempt, wait_s)
                time.sleep(wait_s)
                continue
            raise
        video = res.get("result_url") or find_deep(res["data"], VIDEO_KEYS)
        if not video:
            raise CliError("数字人任务完成但没有输出地址：%s" % _pretty(res["data"]))
        return video
    raise last_exc or CliError("数字人重试后仍失败")


def cmd_lipsync(client: Client, args) -> int:
    """图片数字人：提交单个口播任务。"""
    require_authorization(args)
    mode = args.mode
    if mode == "text" and not args.content:
        raise ValidationError("mode=text 必须提供 --content")
    if not args.audio:
        raise ValidationError("缺少 --audio（audio 模式为驱动音频；text 模式为参考音色）")
    if not args.image:
        raise ValidationError("缺少 --image（人物图片 URL）")
    body = {"model": args.model, "mode": mode, "image_url": args.image,
            "audio_url": args.audio, "quality": args.quality}
    if args.content:
        body["content"] = args.content
    if args.prompt:
        body["prompt"] = args.prompt
    if args.dry_run:
        out({"dry_run": True, "body": body}, True)
        return EXIT_OK
    sys.stderr.write("已提交数字人任务…\n")
    if args.json and not args.wait:
        sub = client.lipsync_submit(args.image, args.audio, mode=mode, content=args.content,
                                    prompt=args.prompt, quality=args.quality, model=args.model)
        out({"task_id": _extract_task_id(sub), "raw": sub}, True)
        return EXIT_OK
    if not args.wait:
        sub = client.lipsync_submit(args.image, args.audio, mode=mode, content=args.content,
                                    prompt=args.prompt, quality=args.quality, model=args.model)
        out({"task_id": _extract_task_id(sub), "status": resolve_task_status(sub),
             "raw": sub}, args.json)
        return EXIT_OK
    video = submit_dh_and_wait(client, args, args.image, args.audio, mode=mode,
                               content=args.content, prompt=args.prompt,
                               quality=args.quality, model=args.model)
    out({"status": "completed", "video_url": video}, args.json)
    return EXIT_OK


def cmd_realman(client: Client, args) -> int:
    if not args.template:
        raise ValidationError("缺少 --template（真人口播模板 ID，realMan 场景）")
    if not args.video:
        raise ValidationError("缺少 --video（真人口播视频 URL）")
    body = {"styleId": args.template, "videoUrl": args.video}
    body.update(_clip_common_body(args, client))
    issues: List[str] = []
    ext = _ext_of(args.video)
    if ext and ext not in _VID_EXT:
        issues.append("--video 后缀 %s 不支持（mp4/mov）" % ext)
    if args.materials:
        issues.extend(validate_materials(args.materials))
        body["materials"] = args.materials
    issues.extend(validate_subtitle(body.get("subtitle")))
    issues.extend(validate_struct_layers(body.get("structLayers")))
    urls = [args.video] + [m.get("fileUrl", "") for m in (args.materials or [])]
    bgm = (body.get("packRules") or {}).get("backgroundMusic") or {}
    urls.append(bgm.get("audioUrl", ""))
    cover = (body.get("processRules") or {}).get("firstFrameCover") or {}
    urls.append(cover.get("resultImageUrl", ""))
    dups = validate_url_list_uniq(urls)
    if dups:
        issues.append("以下地址被复用（upstream 会渲染异常）：%s" % "; ".join(dups))
    return _guarded_submit(client, "realman_broadcast", body, issues, args)


def cmd_mixcut(client: Client, args) -> int:
    if not args.template:
        raise ValidationError("缺少 --template（素材混剪模板 ID，oralMixCutting 场景）")
    if not args.materials:
        raise ValidationError("缺少 --material（素材混剪至少一条素材）")
    if args.content or args.speaker_id:
        raise ValidationError(
            "上游不支持该分支：broadcast_mixcut 目前只支持 audioUrl / 素材链路，"
            "传 content 或 speakerId 会被拒绝（unsupported_speaker_branch）。"
            "需要文案驱动请改用图片数字人 pic_lipsync 的 text 模式。")
    body = {"styleId": args.template, "materials": args.materials}
    if args.audio:
        body["audioUrl"] = args.audio
    body.update(_clip_common_body(args, client))
    issues = validate_materials(args.materials)
    issues.extend(validate_subtitle(body.get("subtitle")))
    issues.extend(validate_struct_layers(body.get("structLayers")))
    bgm = (body.get("packRules") or {}).get("backgroundMusic") or {}
    urls = [body.get("audioUrl", "")] + [m.get("fileUrl", "") for m in args.materials]
    urls += [bgm.get("audioUrl", ""),
             ((body.get("processRules") or {}).get("firstFrameCover") or {}).get("resultImageUrl", "")]
    dups = validate_url_list_uniq(urls)
    if dups:
        issues.append("以下地址被复用（upstream 会渲染异常）：%s" % "; ".join(dups))
    return _guarded_submit(client, "broadcast_mixcut", body, issues, args)


def cmd_news(client: Client, args) -> int:
    if not args.template:
        raise ValidationError("缺少 --template（新闻体模板 ID，newsMixCutting 场景）")
    if not args.title:
        raise ValidationError("缺少 --title（新闻体视频 title 必填，3~1800 字符）")
    lo, hi = LIMITS["news_title_len"]
    if not lo <= len(args.title) <= hi:
        raise ValidationError("--title 长度 %d 不在 %d~%d" % (len(args.title), lo, hi))
    if not args.materials:
        raise ValidationError("缺少 --material（新闻体视频至少一条素材）")
    body = {"styleId": args.template, "title": args.title, "materials": args.materials}
    body.update(_clip_common_body(args, client))
    issues = validate_materials(args.materials)
    issues.extend(validate_subtitle(body.get("subtitle")))
    issues.extend(validate_struct_layers(body.get("structLayers")))
    bgm = (body.get("packRules") or {}).get("backgroundMusic") or {}
    urls = [m.get("fileUrl", "") for m in args.materials] + [bgm.get("audioUrl", ""),
            ((body.get("processRules") or {}).get("firstFrameCover") or {}).get("resultImageUrl", "")]
    dups = validate_url_list_uniq(urls)
    if dups:
        issues.append("以下地址被复用（upstream 会渲染异常）：%s" % "; ".join(dups))
    return _guarded_submit(client, "news_mixcut", body, issues, args)


def cmd_make(client: Client, args) -> int:
    """一站式：参考图 → 人物图 → 数字人 → 自动剪辑成片（含可选自动封面）。"""
    require_authorization(args)
    args.text = read_text_arg(args.text, getattr(args, "text_file", ""))
    if not args.image and not args.ref:
        raise ValidationError("缺少 --image（形象图片 URL）或 --ref（参考图，先做参考生图）")
    if not args.dh_video and not args.audio and not args.text:
        raise ValidationError("至少给一个：--audio（驱动音频）、--text（口播文案，内部串 TTS）"
                              "或 --dh-video（现成口播视频，跳过数字人）")

    # ---------- 步骤 0（可选）：参考生图 ----------
    portrait_url = args.image
    if args.ref:
        if args.dry_run:
            out({"dry_run": True, "step": "portraits",
                 "ref": args.ref, "count": args.portrait_count,
                 "pick_index": args.portrait_index,
                 "aspect_ratio": args.portrait_aspect}, True)
            return EXIT_OK
        sys.stderr.write("⓪ 参考生图中（1 张参考图 → %d 张同风格人物图）…\n"
                         % args.portrait_count)
        shots = list(args.shots) if args.shots else DEFAULT_SHOTS
        made: List[Dict[str, Any]] = []
        for idx in range(args.portrait_count):
            shot = shots[idx % len(shots)]
            prompt = build_shot_prompt(shot)
            try:
                sub = client.image_generate(prompt, ref_url=args.ref,
                                            resolution=args.portrait_resolution,
                                            aspect_ratio=args.portrait_aspect,
                                            model=getattr(args, "portrait_model", "") or "")
                tid = _extract_task_id(sub)
                if not tid:
                    sys.stderr.write("    第 %d 张：没拿到 task_id，跳过\n" % idx)
                    continue
                res = client.wait_task(tid, interval=args.poll_interval,
                                       max_wait=args.max_wait,
                                       on_tick=_tick_factory(True),
                                       require_keys=("image_url", "image_uri", "imageUrl"))
                urls = collect_image_urls(res["data"])
                if urls:
                    made.append({"index": idx, "task_id": tid, "shot": shot,
                                 "image_url": urls[0]})
                    sys.stderr.write("    第 %d 张：%s\n" % (idx, urls[0]))
            except CliError as exc:
                sys.stderr.write("    第 %d 张失败：%s\n" % (idx, exc))
        if not made:
            raise CliError("参考生图一张都没成功，无法继续。可先用 portraits 子命令单独排查。")
        if args.portrait_out:
            with open(args.portrait_out, "w", encoding="utf-8") as fh:
                json.dump({"ref": args.ref, "images": made}, fh,
                          ensure_ascii=False, indent=2)
            sys.stderr.write("    清单已写出：%s\n" % args.portrait_out)
        pick = args.portrait_index
        if pick < 0 or pick >= len(made):
            sys.stderr.write("    --portrait-index %d 超范围（成功 %d 张），改用第 0 张\n"
                             % (pick, len(made)))
            pick = 0
        portrait_url = made[pick]["image_url"]
        sys.stderr.write("    选中第 %d 张做数字人：%s\n" % (pick, portrait_url))
        args.image = portrait_url

    # ---------- 步骤 0.5（可选）：本地缩放到数字人最合适的尺寸 ----------
    # 关键：数字人 quality=max 时**按输入图分辨率输出**，而输入图单边必须 <2000px。
    # 所以把 2K 图缩到 1080x1920 再上传，成片才是原生 1080x1920、不被模板放大。
    if getattr(args, "fit", "") and portrait_url:
        if args.dry_run:
            out({"dry_run": True, "step": "fit", "image_url": portrait_url,
                 "size": args.fit}, True)
            return EXIT_OK
        sys.stderr.write("⓪' 本地缩放到 %s 后重新上传…\n" % args.fit)
        portrait_url = fit_image_local(client, portrait_url, args.fit)
        args.image = portrait_url

    # ---------- 步骤 1：配音 ----------
    audio_url = args.audio
    dh_video_url = args.dh_video  # 允许跳过数字人，直接拿现成的口播视频去剪辑

    if dh_video_url:
        sys.stderr.write("跳过数字人：直接使用 --dh-video 的成片\n")
    else:
        if not audio_url:
            audio_url = _tts_frontend(client, args)

        # ---------- 步骤 2（可选）：ASR → 卡拉OK字幕 ----------
        if args.karaoke:
            if args.dry_run:
                out({"dry_run": True, "step": "asr", "audio_url": audio_url,
                     "note": "会调 voice_tts/stt（40 点）并把字级时间轴回填 subtitle[]"}, True)
                return EXIT_OK
            sys.stderr.write("② 语音识别中（取时间轴做字幕）…\n")
            try:
                stt_data = client.stt(audio_url, language=args.language, timestamps=True)
                subs = subtitles_from_asr(stt_data)
                if subs:
                    # 实测：把上百条单字符字幕整段传进去会被上游拒。
                    # 所以默认按句合并，并按音频时长 clamp 结尾。
                    audio_ms = find_number(stt_data, ("duration",))
                    hard_end = int(audio_ms * 1000) if audio_ms else None
                    merged = merge_subtitles(
                        subs, max_chars=getattr(args, "subtitle_max_chars", 18),
                        hard_end_ms=hard_end)
                    args.subtitle = merged
                    sys.stderr.write("    字幕 %d 条（字级 %d → 按句合并 %d，%s）\n"
                                     % (len(merged), len(subs), len(merged),
                                        "已按音频时长收尾" if hard_end else "未收尾"))
                else:
                    sys.stderr.write("    [警告] ASR 没返回字级分段，交给平台自动加字幕\n")
            except CliError as exc:
                sys.stderr.write("    [警告] ASR 失败（%s），交给平台自动加字幕\n" % exc)

        if args.dry_run:
            out({"dry_run": True, "step": "pic_lipsync", "image_url": args.image,
                 "audio_url": audio_url, "mode": args.mode,
                 "content": args.content, "quality": args.quality}, True)
            return EXIT_OK
        sys.stderr.write("③ 数字人合成中（图片 + 音频 → 口播视频）…\n")
        if not args.wait:
            sub = client.lipsync_submit(args.image, audio_url, mode=args.mode,
                                        content=args.content, prompt=args.prompt,
                                        quality=args.quality, model=args.model)
            out({"stage": "lipsync", "task_id": _extract_task_id(sub),
                 "audio_url": audio_url, "image_url": args.image}, args.json)
            return EXIT_OK
        dh_video_url = submit_dh_and_wait(
            client, args, args.image, audio_url, mode=args.mode,
            content=args.content, prompt=args.prompt, quality=args.quality,
            model=args.model)
        sys.stderr.write("   数字人成片：%s\n" % dh_video_url)

    # ---------- 自动封面 ----------
    if args.cover_final:
        args.cover_result_url = args.cover_final          # 直接当首帧
    elif args.cover_image:
        args.cover_image_url = args.cover_image           # 平台按这张底图生成 AI 封面
    elif args.auto_cover:
        # 用数字人形象图当底图，让平台生成 AI 首帧封面
        args.cover_image_url = portrait_url
    if args.cover_image_url or args.cover_result_url:
        sys.stderr.write("   封面：%s\n"
                         % ("用指定图当首帧" if args.cover_result_url
                            else "按底图生成 AI 封面"))

    # ---------- 选模板 ----------
    template_id = args.template
    if not template_id:
        if args.dry_run:
            template_id = "<自动挑选 realMan 模板>"
        else:
            template_id = _pick_template(client, args)
            if not template_id:
                raise CliError("没有取到可用模板。请显式传 --template，"
                               "或用 `templates --scene realMan` 先看一眼。")
            sys.stderr.write("④ 使用模板 %s\n" % template_id)

    if args.dry_run:
        out({"dry_run": True, "step": "realman_broadcast", "styleId": template_id,
             "videoUrl": dh_video_url, "materials": args.materials or [],
             "firstFrameCover": (args.cover_result_url or args.cover_image_url or None),
             "subtitle_count": len(args.subtitle or [])}, True)
        return EXIT_OK

    sys.stderr.write("④ 自动剪辑中（口播视频 + 模板 + 素材 → 成片）…\n")
    args.template = template_id
    args.video = dh_video_url
    return cmd_realman(client, args)


def _resolve_voice(client: Client, explicit: str, quiet: bool = False) -> str:
    """没指定音色就取平台音色列表的第一条。默认音色也能用（不传 reference_id）。"""
    if explicit:
        return explicit
    data = client.voices(page_size=1)
    items = (data or {}).get("items") if isinstance(data, dict) else None
    if items:
        vid = items[0].get("id") or items[0].get("model_id") or ""
        if vid and not quiet:
            sys.stderr.write("使用音色：%s（%s）\n"
                             % (vid, items[0].get("title") or "未命名"))
        return vid
    return ""


def tts_to_audio(client: Client, text: str, voice: str = "", engine: str = "tts_async",
                 args=None) -> str:
    """文案 → 音频 URL。默认走**异步** TTS（同步那条在 api.a7w.cn 上是坏的）。

    返回公网可访问的 mp3 地址，可直接喂给 pic_lipsync。
    """
    if engine == "tts":
        data = client.tts(text, voice=voice, fmt="mp3")
        url = find_deep(data, AUDIO_KEYS)
        if not url:
            raise CliError(
                "同步 TTS 没有返回音频地址：%s\n"
                "  同步路由实测在上游是坏的（一律返回「任务处理失败」），"
                "请改用默认的异步路由（去掉 --tts-engine tts），"
                "或用 --audio 直接给音频 URL 绕开 TTS。" % _pretty(data))
        return url

    data = client.tts_async(text, voice=voice, fmt="mp3", engine=engine)
    task_id = _extract_task_id(data)
    if not task_id:
        raise CliError("TTS 提交后没有拿到 task_id：%s" % _pretty(data))
    sys.stderr.write("   TTS task_id=%s（冻结 %s 点）\n"
                     % (task_id, (data or {}).get("frozen_points", "?")))
    interval = getattr(args, "poll_interval", 5.0) if args else 5.0
    max_wait = getattr(args, "max_wait", 600.0) if args else 600.0
    # TTS 很快（实测 3~6 秒），但也吃"completed 后结果地址还是空串"那个竞态，
    # 所以同样传 require_keys 兜底。
    res = client.wait_task(task_id, interval=min(interval, 5.0), max_wait=max_wait,
                           on_tick=_tick_factory(True),
                           require_keys=AUDIO_KEYS, settle_wait=60.0)
    url = res.get("result_url") or find_deep(res["data"], AUDIO_KEYS)
    if not url:
        raise CliError("TTS 完成但没有音频地址：%s" % _pretty(res["data"]))
    return url


def _tts_frontend(client: Client, args) -> str:
    """make 里的「文案 → 音频」步骤。"""
    if args.dry_run:
        return "<TTS audio_url>"
    voice = _resolve_voice(client, args.voice)
    engine = getattr(args, "tts_engine", "tts_async")
    url = tts_to_audio(client, args.text, voice=voice, engine=engine, args=args)
    sys.stderr.write("① 配音完成：%s\n" % url)
    return url


def _pick_template(client: Client, args) -> Optional[str]:
    if args.dry_run:
        return None
    data = client.clip_templates("realMan", page_size=args.template_scan)
    items = (data or {}).get("results") if isinstance(data, dict) else data
    if not isinstance(items, list) or not items:
        return None
    if args.template_name:
        for item in items:
            name = str(item.get("name") or "")
            if args.template_name in name:
                sys.stderr.write("按名称命中模板：%s（%s）\n" % (name, item.get("id")))
                return item.get("id")
        sys.stderr.write("没有名称含 %r 的模板，改用 %s\n"
                         % (args.template_name, _index_label(args.template_index)))
    idx = int(getattr(args, "template_index", 0) or 0)
    if idx < 0 or idx >= len(items):
        raise CliError("--template-index %d 超出范围（本页共 %d 条模板）"
                       % (idx, len(items)), code=EXIT_USAGE)
    picked = items[idx]
    sys.stderr.write("按序号选中模板 #%d：%s（%s）\n"
                     % (idx, picked.get("name"), picked.get("id")))
    return picked.get("id")


def _index_label(idx: Any) -> str:
    return "第 %s 条" % (int(idx or 0),)


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="dhclip.py",
        description="数字人 + 智能剪辑 一站式 CLI（图片数字人 pic_lipsync + 智能剪辑 smart_clip）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例：\n"
            "  # 一条命令：文案 → 数字人口播 → 套模板自动剪辑\n"
            "  python -X utf8 scripts/dhclip.py make \\\n"
            "      --image https://cdn/face.jpg --text \"大家好，今天聊三件事。\" \\\n"
            "      --material image=https://cdn/a.jpg --material video=https://cdn/b.mp4 \\\n"
            "      --title \"今天聊三件事\" --authorized --wait\n\n"
            "  # 只做数字人\n"
            "  python -X utf8 scripts/dhclip.py lipsync --image URL --audio URL \\\n"
            "      --authorized --wait\n\n"
            "  # 只看模板，不花钱\n"
            "  python -X utf8 scripts/dhclip.py templates --scene realMan\n"
        ),
    )
    p.add_argument("--version", action="version", version="avatar-autoclip %s" % __version__)

    # 全局开关定义两遍：顶层一份给"写在子命令前"的用法，parent 一份给"写在子命令后"的用法。
    # parent 里一律 default=SUPPRESS —— 子命令没写时不会覆盖顶层已解析的值，
    # 否则 `--json make ...` 会被子命令的 default=False 冲掉。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--key", default=argparse.SUPPRESS,
                        help="API Key（默认读 AVATAR_AUTOCLIP_KEY / A7W_API_KEY / ~/.a7w/config.json）")
    common.add_argument("--base", default=argparse.SUPPRESS,
                        help="★ 已锁定，只能 %s（传别的会直接报错）" % LOCKED_HOST)
    common.add_argument("--timeout", type=float, default=argparse.SUPPRESS,
                        help="单次请求超时秒数")
    common.add_argument("--budget", type=float, default=argparse.SUPPRESS,
                        help="预算上限（点）。超了就地中止，退出码 5；用 --budget 必须给单价")
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="以 JSON 输出（便于程序消费）")
    common.add_argument("--dry-run", action="store_true", default=argparse.SUPPRESS,
                        help="只打印将要提交的请求体，不发写请求")
    common.add_argument("-v", "--verbose", action="store_true", default=argparse.SUPPRESS,
                        help="打印请求日志到 stderr")

    p.add_argument("--key", default="", help=argparse.SUPPRESS)
    # ★ 不再从 AVATAR_AUTOCLIP_BASE 环境变量读根地址（少一个可改的入口）；
    #   给了 --base 也只是送去校验，非 api.a7w.cn 会被 assert_base_locked 拒掉。
    p.add_argument("--base", default=LOCKED_BASE, help=argparse.SUPPRESS)
    p.add_argument("--timeout", type=float, default=120.0, help=argparse.SUPPRESS)
    p.add_argument("--budget", type=float, default=None, help=argparse.SUPPRESS)
    p.add_argument("--json", action="store_true", default=False, help=argparse.SUPPRESS)
    p.add_argument("--dry-run", action="store_true", default=False, help=argparse.SUPPRESS)
    p.add_argument("-v", "--verbose", action="store_true", default=False, help=argparse.SUPPRESS)

    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("balance", parents=[common], help="查余额/点数")

    sp = sub.add_parser("pricing", parents=[common], help="查各接口当前有效价格")

    sp = sub.add_parser("voices", parents=[common], help="列出可用音色")
    sp.add_argument("--title", default="", help="按名称搜索")
    sp.add_argument("--limit", type=int, default=20)

    sp = sub.add_parser("tts", parents=[common],
                        help="文案 → 音频（默认异步路由；同步那条在上游是坏的）")
    sp.add_argument("--text", required=False, default="")
    sp.add_argument("--text-file", default="", help="从 UTF-8 文本文件读文案（推荐，避免中文编码问题）")
    sp.add_argument("--voice", default="", help="音色 ID（reference_id）；不传用平台默认音色")
    sp.add_argument("--format", default="mp3", choices=["mp3", "wav", "pcm", "opus"])
    sp.add_argument("--speed", type=float, default=None, help="语速，如 1.2")
    sp.add_argument("--engine", default="tts_async", choices=["tts_async", "tts_live", "tts"],
                    help="tts_async（默认，便宜）/ tts_live（流式上游）/ tts（同步，实测坏）")
    sp.add_argument("--poll-interval", type=float, default=5.0)
    sp.add_argument("--max-wait", type=float, default=600.0)

    sp = sub.add_parser("upload", parents=[common], help="上传本地文件换取临时 URL（24h 有效）")
    sp.add_argument("file")

    sp = sub.add_parser("task", parents=[common], help="按 task_id 查状态与结果")
    sp.add_argument("task_id")
    # 这里手写而不是复用 add_wait()：add_wait 定义在后面，此处还不可用
    sp.add_argument("--wait", action="store_true", help="轮询到终态")
    sp.add_argument("--poll-interval", type=float, default=10.0)
    sp.add_argument("--max-wait", type=float, default=3600.0)
    sp.add_argument("--app-query", default="", choices=["", APP_LIPSYNC],
                    help="强制走应用级 query（通用 /tasks 路由不可用时）")

    sp = sub.add_parser("templates", parents=[common], help="智能剪辑模板列表（免费）")
    sp.add_argument("--scene", required=True, choices=sorted(SCENE_TO_API))
    sp.add_argument("--page-size", type=int, default=10)
    sp.add_argument("--all", action="store_true", help="按 sid 游标翻完所有页")
    sp.add_argument("--table", action="store_true", help="打成带序号的清单（默认就是）")
    sp.add_argument("--search-key", default="", choices=["", "name", "id"])
    sp.add_argument("--search-value", default="")
    sp.add_argument("--sort-by", default="desc", choices=["desc", "asc"])

    sp = sub.add_parser("template", parents=[common], help="模板详情（画布、图层）")
    sp.add_argument("--id", required=True)

    sp = sub.add_parser("portraits", parents=[common],
                        help="参考生图：1 张参考图 → N 张同风格人物图（保住人物身份）")
    sp.add_argument("--ref", default="", help="参考图 URL；保住人物身份一致性的关键")
    sp.add_argument("--allow-no-ref", action="store_true",
                    help="允许不给参考图，退化成纯文生图（不保身份）")
    sp.add_argument("--n", type=int, default=4, help="生成几张，默认 4")
    sp.add_argument("--shot", action="append", default=[],
                    help="自定义分镜描述，可重复；不给就用内置的 6 个分镜循环")
    sp.add_argument("--identity-prefix", default=IDENTITY_PREFIX,
                    help="身份一致性前缀（默认已内置，一般不用改）")
    sp.add_argument("--aspect-ratio", default="9:16", help="默认 9:16 竖版")
    sp.add_argument("--resolution", default="1K", choices=["1K", "2K", "4K"])
    sp.add_argument("--model", default="", help="模型规格；不传用平台默认")
    sp.add_argument("--out", default="", help="把结果清单写成 JSON 文件")
    sp.add_argument("--poll-interval", type=float, default=10.0)
    sp.add_argument("--max-wait", type=float, default=900.0)
    sp.add_argument("--authorized", action="store_true",
                    help="声明已获得该人像的使用授权（给了 --ref 就必需）")

    sp = sub.add_parser("fit", parents=[common],
                        help="把一张图缩放到目标尺寸并上传（数字人前处理，避免被模板放大）")
    sp.add_argument("--image", required=True, help="源图 URL")
    sp.add_argument("--size", default="1080x1920", help="目标尺寸 WxH，默认 1080x1920")
    sp.add_argument("--workdir", default="", help="临时目录，默认系统临时目录")

    sp = sub.add_parser("clone", parents=[common],
                        help="克隆音色：给一段参考音频，得到一个专属音色 ID（声音像不像的关键）")
    sp.add_argument("--title", required=True, help="音色名称")
    sp.add_argument("--audio", required=True, help="参考音频 URL（mp3/wav/ogg/flac）")
    sp.add_argument("--text", action="append", default=[],
                    help="与音频对应的文本，可重复；不传则由平台自动 ASR")
    sp.add_argument("--visibility", default="private",
                    choices=["private", "unlist", "public"])
    sp.add_argument("--description", default="")
    sp.add_argument("--no-enhance", dest="enhance", action="store_false", default=True,
                    help="关掉音频质量增强（默认开）")

    sp = sub.add_parser("asr", parents=[common],
                        help="语音转文字并输出可直接用的 subtitle[]（字级时间轴）")
    sp.add_argument("--audio", required=True, help="音频 URL")
    sp.add_argument("--language", default="", help="识别语言，不传自动检测")
    sp.add_argument("--merge", action="store_true",
                    help="按句合并（强烈建议）：上游对长条数 subtitle[] 会拒，合并后更稳")
    sp.add_argument("--max-chars", type=int, default=18, help="合并时单条最大字数，默认 18")
    sp.add_argument("--out", default="", help="把 subtitle[] 写成 JSON 文件")

    def add_wait(sp):
        sp.add_argument("--wait", action="store_true", help="轮询到终态")
        sp.add_argument("--poll-interval", type=float, default=10.0)
        sp.add_argument("--max-wait", type=float, default=3600.0)
        sp.add_argument("--app-query", default="", choices=["", APP_LIPSYNC],
                        help="强制走应用级 query（通用 /tasks 路由不可用时）")
        return sp

    def add_clip_common(sp):
        # 注意：--title 由各子命令自己声明（news 用的是必填语义），这里不重复加，
        # 否则 argparse 报 "conflicting option string"。
        sp.add_argument("--language", default="")
        sp.add_argument("--introduce-name", default="")
        sp.add_argument("--introduce-desc", default="")
        sp.add_argument("--bgm-url", default="")
        sp.add_argument("--bgm-volume", type=float, default=None)
        sp.add_argument("--bgm-off", action="store_true")
        sp.add_argument("--pack-header", dest="pack_header", action="store_true", default=None)
        sp.add_argument("--pack-material", dest="pack_material", action="store_true", default=None)
        sp.add_argument("--pack-subtitle", dest="pack_subtitle", action="store_true", default=None)
        sp.add_argument("--pack-keyword", dest="pack_keyword", action="store_true", default=None)
        sp.add_argument("--subtitle", type=lambda v: parse_json_arg(v, "--subtitle"),
                        default=None, help="字幕数组（JSON 或文件路径），用于回填 ASR 结果")
        sp.add_argument("--struct-layers", type=lambda v: parse_json_arg(v, "--struct-layers"),
                        default=None, help="图层覆盖（JSON 或文件路径）")
        sp.add_argument("--metadata", type=lambda v: parse_json_arg(v, "--metadata"),
                        default=None, help="元水印（仅一组，value 必须是字符串）")
        sp.add_argument("--ai-label", dest="ai_label", action="store_true", default=None,
                        help="加 AI 生成标识（watermarkShow + AIGC 元水印）")
        sp.add_argument("--no-ai-label", dest="ai_label", action="store_false",
                        help="关掉 AI 标识（默认开）")
        sp.add_argument("--producer", default="", help="AIGC 标识里的内容制作方")
        sp.add_argument("--produce-id", default="", help="AIGC 标识里的内容编号")
        sp.add_argument("--callback-url", default="")
        sp.add_argument("--set", action="append", default=[],
                        help="透传任意顶层字段 key=value，可重复")
        return sp

    sp = sub.add_parser("lipsync", parents=[common], help="图片数字人：提交任务")
    sp.add_argument("--image", required=True, help="人物图片 URL")
    sp.add_argument("--audio", default="", help="audio 模式的驱动音频；text 模式的参考音色")
    sp.add_argument("--mode", default="audio", choices=["audio", "text"])
    sp.add_argument("--content", default="", help="text 模式的朗读文案")
    sp.add_argument("--prompt", default="", help="动作/表情/风格提示词")
    sp.add_argument("--quality", default="standard", choices=["fast", "standard", "max"])
    sp.add_argument("--model", default="super-lipsync-pro")
    sp.add_argument("--authorized", action="store_true", help="声明已获得该人像/声音的使用授权")
    add_wait(sp)

    sp = sub.add_parser("realman", parents=[common], help="智能剪辑 · 真人口播混剪")
    sp.add_argument("--template", default="", help="模板 ID（realMan 场景）")
    sp.add_argument("--title", default="", help="标题；不想显示标题就不要传")
    sp.add_argument("--video", default="", help="真人口播视频 URL（mp4/mov）")
    sp.add_argument("--material", action="append", default=[], help="素材 type=URL，可重复")
    sp.add_argument("--material-sound", dest="material_sound", action="store_true", default=None)
    sp.add_argument("--preprocess", default="", choices=["", "roughCut", "sliceMerge"])
    sp.add_argument("--match-way", default="", choices=["", "fuzzyMatch", "preciseMatch"])
    sp.add_argument("--cover-image-url", default="")
    sp.add_argument("--cover-result-url", default="")
    sp.add_argument("--cover-template-id", default="")
    add_clip_common(sp)
    add_wait(sp)

    sp = sub.add_parser("mixcut", parents=[common], help="智能剪辑 · 素材混剪")
    sp.add_argument("--template", default="")
    sp.add_argument("--title", default="")
    sp.add_argument("--audio", default="", help="音频 URL（与素材链路二选一）")
    sp.add_argument("--content", default="", help="该分支上游不支持，传了会被本地拦下")
    sp.add_argument("--speaker-id", default="", help="该分支上游不支持")
    sp.add_argument("--material", action="append", default=[], required=False)
    sp.add_argument("--preprocess", default="", choices=["", "roughCut", "sliceMerge"])
    sp.add_argument("--cover-image-url", default="")
    sp.add_argument("--cover-result-url", default="")
    sp.add_argument("--cover-template-id", default="")
    add_clip_common(sp)
    add_wait(sp)

    sp = sub.add_parser("news", parents=[common], help="智能剪辑 · 新闻体视频")
    sp.add_argument("--template", default="")
    sp.add_argument("--title", default="")
    sp.add_argument("--material", action="append", default=[])
    sp.add_argument("--video-duration", type=int, default=None, help="5~300 秒")
    sp.add_argument("--composition", default="", choices=["", "random", "order"])
    sp.add_argument("--cover-image-url", default="")
    sp.add_argument("--cover-result-url", default="")
    sp.add_argument("--cover-template-id", default="")
    add_clip_common(sp)
    add_wait(sp)

    sp = sub.add_parser("make", parents=[common],
                        help="一站式：图片+文字 → 数字人 → 自动剪辑成片（可带参考生图与自动封面）")
    sp.add_argument("--image", default="", help="数字人形象图片 URL")
    sp.add_argument("--ref", default="",
                    help="参考图 URL：先做参考生图，再拿生成图做数字人（与 --image 二选一）")
    sp.add_argument("--portrait-count", type=int, default=4,
                    help="参考生图张数（配合 --ref），默认 4")
    sp.add_argument("--portrait-index", type=int, default=0,
                    help="用第几张生成图做数字人，默认 0")
    sp.add_argument("--portrait-aspect", default="9:16", help="参考生图比例，默认 9:16 竖版")
    sp.add_argument("--portrait-resolution", default="1K", choices=["1K", "2K", "4K"],
                    help="2K/4K 必须配 --portrait-model（普通模型只到 1K）")
    sp.add_argument("--portrait-model", default="",
                    help="生图模型；要 2K/4K 高清档用 nano-banana-pro")
    sp.add_argument("--portrait-out", default="", help="参考生图清单写成 JSON 文件")
    sp.add_argument("--fit", default="",
                    help="本地把形象图缩放到 WxH 再上传（如 1080x1920）。"
                         "数字人 max 档按输入分辨率输出，缩放后成片才不被放大发虚；需 ffmpeg")
    sp.add_argument("--shots", action="append", default=[],
                    help="参考生图的自定义分镜描述，可重复")
    sp.add_argument("--auto-cover", action="store_true", default=None,
                    help="让平台用数字人形象图生成 AI 首帧封面（自动出封面）")
    sp.add_argument("--no-auto-cover", dest="auto_cover", action="store_false")
    sp.add_argument("--cover-image", default="", help="AI 封面的底图 URL（比 --auto-cover 更可控）")
    sp.add_argument("--cover-final", default="", help="直接把这张图当首帧封面（优先级最高）")
    sp.add_argument("--karaoke", action="store_true",
                    help="对配音音频跑 ASR，把时间轴回填 subtitle[]（按句合并，更稳）")
    sp.add_argument("--subtitle-max-chars", type=int, default=18,
                    help="--karaoke 合并时单条最大字数，默认 18")
    sp.add_argument("--text", default="", help="口播文案（内部串 TTS 生成音频，只需图片+文字）")
    sp.add_argument("--text-file", default="",
                    help="从 UTF-8 文本文件读文案（**中文强烈建议用这个**，避免命令行引号/编码问题）")
    sp.add_argument("--audio", default="", help="驱动音频 URL（给了就不用 TTS）")
    sp.add_argument("--voice", default="", help="TTS 音色 ID，不给则取音色列表第一条")
    sp.add_argument("--tts-engine", default="tts_async",
                    choices=["tts_async", "tts_live", "tts"],
                    help="TTS 路由：tts_async（默认）/ tts_live / tts（同步，实测坏）")
    sp.add_argument("--mode", default="audio", choices=["audio", "text"],
                    help="pic_lipsync 的模式；audio=音频驱动，text=文案驱动（仍需 --audio 作参考音色）")
    sp.add_argument("--content", default="", help="mode=text 时朗读的文案")
    sp.add_argument("--prompt", default="", help="数字人动作/表情提示词")
    sp.add_argument("--quality", default="standard", choices=["fast", "standard", "max"])
    sp.add_argument("--model", default="super-lipsync-pro")
    sp.add_argument("--dh-video", default="", help="跳过数字人，直接用现成口播视频去剪辑")
    sp.add_argument("--template", default="", help="剪辑模板 ID，不给则自动挑第一条 realMan 模板")
    sp.add_argument("--template-name", default="", help="按名称关键字挑模板")
    sp.add_argument("--template-index", type=int, default=0,
                    help="按序号挑模板（先用 templates --table 看序号），默认 0 即第一条")
    sp.add_argument("--template-scan", type=int, default=20, help="自动挑模板时扫多少条")
    sp.add_argument("--material", action="append", default=[], help="素材 type=URL，可重复")
    sp.add_argument("--title", default="")
    sp.add_argument("--language", default="")
    sp.add_argument("--introduce-name", default="")
    sp.add_argument("--introduce-desc", default="")
    sp.add_argument("--bgm-url", default="")
    sp.add_argument("--bgm-volume", type=float, default=None)
    sp.add_argument("--bgm-off", action="store_true")
    sp.add_argument("--pack-header", dest="pack_header", action="store_true", default=None)
    sp.add_argument("--pack-material", dest="pack_material", action="store_true", default=None)
    sp.add_argument("--pack-subtitle", dest="pack_subtitle", action="store_true", default=None)
    sp.add_argument("--pack-keyword", dest="pack_keyword", action="store_true", default=None)
    sp.add_argument("--subtitle", type=lambda v: parse_json_arg(v, "--subtitle"), default=None)
    sp.add_argument("--struct-layers", type=lambda v: parse_json_arg(v, "--struct-layers"), default=None)
    sp.add_argument("--metadata", type=lambda v: parse_json_arg(v, "--metadata"), default=None)
    sp.add_argument("--ai-label", dest="ai_label", action="store_true", default=None)
    sp.add_argument("--no-ai-label", dest="ai_label", action="store_false")
    sp.add_argument("--producer", default="")
    sp.add_argument("--produce-id", default="")
    sp.add_argument("--callback-url", default="")
    sp.add_argument("--preprocess", default="", choices=["", "roughCut", "sliceMerge"])
    sp.add_argument("--match-way", default="", choices=["", "fuzzyMatch", "preciseMatch"])
    sp.add_argument("--cover-image-url", default="")
    sp.add_argument("--cover-result-url", default="")
    sp.add_argument("--cover-template-id", default="")
    sp.add_argument("--set", action="append", default=[])
    sp.add_argument("--authorized", action="store_true",
                    help="声明已获得该人像/声音的使用授权")
    add_wait(sp)
    return p


CLIP_COMMANDS = {"realman", "mixcut", "news", "make"}


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    # --json 在顶层与子命令都有，子命令优先
    args.json = bool(getattr(args, "json", False)) or ("--json" in (argv or sys.argv))
    for attr, default in (("ai_label", True), ("authorized", False)):
        if not hasattr(args, attr):
            setattr(args, attr, default)
    if getattr(args, "cmd", "") in CLIP_COMMANDS and args.ai_label is None:
        args.ai_label = True
    for attr in ("material", "set"):
        if not hasattr(args, attr):
            setattr(args, attr, [])
    if not hasattr(args, "materials"):
        args.materials = None

    try:
        if args.cmd in ("realman", "mixcut", "news", "make"):
            args.materials = parse_materials(args.material)
        key = load_key(args.key)
        client = Client(base=args.base, key=key, timeout=args.timeout,
                        verbose=args.verbose, budget=args.budget,
                        dry_run=args.dry_run)
        handlers = {
            "balance": cmd_balance, "pricing": cmd_pricing, "voices": cmd_voices,
            "tts": cmd_tts, "upload": cmd_upload, "task": cmd_task,
            "templates": cmd_templates, "template": cmd_template,
            "portraits": cmd_portraits, "asr": cmd_asr,
            "fit": cmd_fit, "clone": cmd_clone,
            "lipsync": cmd_lipsync, "realman": cmd_realman, "mixcut": cmd_mixcut,
            "news": cmd_news, "make": cmd_make,
        }
        rc = handlers[args.cmd](client, args)
        if client.ledger and not args.json:
            total = sum(item["points"] for item in client.ledger)
            if total:
                sys.stderr.write("本次调用累计点数：%.4f\n" % total)
        return rc
    except ValidationError as exc:
        sys.stderr.write("预检不通过：%s\n" % exc)
        for issue in exc.issues:
            sys.stderr.write("  - %s\n" % issue)
        sys.stderr.write("（没有任何请求发出，不产生费用）\n")
        return exc.code
    except CliError as exc:
        sys.stderr.write("%s\n" % exc)
        return exc.code
    except KeyboardInterrupt:
        sys.stderr.write("已中断\n")
        return 130


if __name__ == "__main__":
    sys.exit(main())
