"""Agnes AI 视频生成 API（纯生成层）。项目级编排在 project-generate/video_utils.py。"""

import json, os, sys, time
from datetime import datetime
from typing import Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# 显式确保本目录的 config 模块被正确加载，
# 避免 project-generate 的 modules/config.py（作为 namespace package `modules.config`）
# 在 `from config import ...` 时被冲突解析。
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from config import _log, get_agnes_api_base
from image_api import load_api_key, upload_to_url

API_BASE_VIDEO = get_agnes_api_base()
DEFAULT_VIDEO_MODEL = "agnes-video-v2.0"
# 提交重试封顶：避免 400 Invalid image 等 4xx 客户端错误触发永久自旋，
# 也防止 429/5xx 把整轮轮询拖垮。超过封顶返回 None，交由上层换首帧 / 下一轮重试。
MAX_API_RETRY = 6
VALID_FRAMES = [8 * n + 1 for n in range(1, 56) if 8 * n + 1 <= 441]
DURATION_PRESETS = {"3s": 81, "5s": 121, "10s": 241, "18s": 441}
DURATION_TO_FRAMES = {3: 81, 5: 121, 10: 241, 18: 441}
ASPECT_MAP = {"16:9": (1280, 720), "9:16": (720, 1280), "1:1": (1024, 1024)}
_MULTI_IMAGE_KW = ["对比", "变化前", "变化后", "转变", "转化", "from", "to",
    "transformation", "时间流逝", "昼夜", "season", "before", "after", "之前", "之后", "过去", "现在"]
_KEYFRAMES_KW = ["多人", "多人互动", "多角色", "multiple characters", "关键帧", "keyframe",
    "插值", "interpolate", "场景切换", "转场", "transition between", "群体", "群像", "crowd",
    "complex scene", "两个角色", "two characters", "交互", "interaction", "激烈", "intense", "complex motion"]

_last_submit_result: dict[str, Any] | None = None


def get_last_submit_result() -> dict[str, Any] | None:
    return _last_submit_result


def _select_mode(description: str, num_images: int = 1) -> str:
    if num_images < 2:
        return "standard"
    desc_lower = description.lower()
    for kw in _MULTI_IMAGE_KW:
        if kw in desc_lower:
            return "multi-image"
    for kw in _KEYFRAMES_KW:
        if kw in desc_lower:
            return "keyframes"
    return "standard"


def submit_video(
    prompt: str = "", ref_img: str = "", mode: str = "standard",
    ref_paths: list[str] | None = None, ref_urls: list[str] | None = None,
    duration: int | float | None = None, aspect: str = "9:16",
    project: str | None = None, shot_id: int | None = None,
    seed: int | None = None, negative_prompt: str | None = None,
    *,
    num_frames: int | None = None, frame_rate: int = 24,
    width: int | None = None, height: int | None = None,
) -> str | None:
    global _last_submit_result
    _last_submit_result = None

    # ── 尺寸 / 帧数 ──
    if width is None or height is None:
        if aspect in ASPECT_MAP:
            width, height = ASPECT_MAP[aspect]
        elif "x" in aspect:
            parts = aspect.split("x")
            width, height = int(parts[0]), int(parts[1])
        else:
            width, height = 720, 1280

    if num_frames is None:
        if duration is not None:
            num_frames = DURATION_TO_FRAMES.get(int(duration), duration * 24 + 1)
        else:
            num_frames = 121

    # ── 模式检测 ──
    if mode is None or mode == "auto":
        n_imgs = 0
        if ref_urls:
            n_imgs = len(ref_urls)
        elif ref_paths:
            n_imgs = len(ref_paths)
        elif ref_img and os.path.isfile(ref_img):
            n_imgs = 1
        mode = _select_mode(prompt, num_images=n_imgs)

    # ── 参考图上传 ──
    label = f"shot_{shot_id}" if shot_id else ""
    log_mode = f" [{mode}]" if mode != "standard" else ""
    _log(f"  [Agnes] {label}提交{log_mode}...")
    api_key = load_api_key()

    payload: dict[str, Any] = {
        "model": DEFAULT_VIDEO_MODEL, "prompt": prompt,
        "num_frames": num_frames, "frame_rate": frame_rate,
        "width": width, "height": height,
    }

    _uploaded_urls: list[str] = []
    if mode == "standard":
        # 单参考图
        if ref_urls:
            payload["image"] = ref_urls[0]
            _uploaded_urls = [ref_urls[0]]
        elif ref_paths:
            payload["image"] = upload_to_url(ref_paths[0], project=project)
            _uploaded_urls = [payload["image"]]
        elif ref_img and os.path.isfile(ref_img):
            payload["image"] = upload_to_url(ref_img, project=project)
            _uploaded_urls = [payload["image"]]
    elif mode in ("keyframes", "multi-image"):
        # 多参考图
        _uploaded_urls = _collect_urls(ref_urls, ref_paths, ref_img, project)
        if len(_uploaded_urls) < 2:
            _log(f"  ❌ {mode} 需要至少 2 张参考图", level=0)
            return None
        extra = payload.setdefault("extra_body", {})
        extra["image"] = _uploaded_urls
        if mode == "keyframes":
            extra["mode"] = "keyframes"
        _log(f"    [参考图] {len(_uploaded_urls)} 张")

    if seed is not None:
        payload["seed"] = seed
        _log(f"    [种子] {seed}")
    if negative_prompt:
        payload["negative_prompt"] = negative_prompt
        _log(f"    [负向提示] {negative_prompt[:60]}...")

    # ── 提交 ──
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        f"{API_BASE_VIDEO}/videos", data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )
    # 有限重试：封顶 MAX_API_RETRY 次，避免 400 Invalid image 等 4xx 客户端错误触发
    # while True 永久自旋；也防止 429/5xx 把整轮轮询拖垮。超过封顶返回 None，
    # 交由上层换首帧 / 下一轮轮询重试。
    api_attempt = 0
    while api_attempt < MAX_API_RETRY:
        api_attempt += 1
        try:
            with urlopen(req, timeout=600) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                task_id = result.get("task_id") or result.get("id")
                if not task_id:
                    _log(f"  ❌ API 返回无 task_id", level=0)
                    # 无 task_id 也重试（可能是响应格式异常）
                    wait = min(30 * (2 ** (api_attempt - 1)), 300)
                    _log(f"  ⚠️ 无 task_id，{wait}秒后重试 (第{api_attempt}次)...")
                    time.sleep(wait)
                    continue
                _log(f"  ✅ task_id={task_id} (status: {result.get('status', 'unknown')})")
                _last_submit_result = {"task_id": task_id, "image_urls": _uploaded_urls}
                return task_id
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            # 4xx 客户端错误（非 429 限流）属永久失败，不可重试：400 Invalid image / 403 等立即放弃
            if 400 <= e.code < 500 and e.code != 429:
                _log(f"  ❌ HTTP {e.code}（客户端错误，不可重试）: {body[:300]}", level=0)
                return None
            wait = min(30 * (2 ** (api_attempt - 1)), 300)
            _log(f"  ⚠️ HTTP {e.code}，{wait}秒后重试 (第{api_attempt}次)...")
            time.sleep(wait)
            continue
        except Exception as e:
            wait = min(30 * (2 ** (api_attempt - 1)), 300)
            _log(f"  ⚠️ 提交异常 ({e})，{wait}秒后重试 (第{api_attempt}次)...")
            time.sleep(wait)
            continue
    _log(f"  ❌ 提交重试 {MAX_API_RETRY} 次仍失败，放弃", level=0)
    return None


def _collect_urls(
    ref_urls: list[str] | None,
    ref_paths: list[str] | None,
    ref_img: str | None,
    project: str | None,
) -> list[str]:
    """收集并上传多张参考图，返回 URL 列表。"""
    result: list[str] = []
    if ref_urls:
        for u in ref_urls:
            if u.startswith("http://") or u.startswith("https://"):
                result.append(u)
            elif os.path.isfile(u):
                result.append(upload_to_url(u, project=project))
            else:
                _log(f"    ⚠️ 无效参考图: {u[:60]}")
    elif ref_paths:
        for p in ref_paths:
            if os.path.isfile(p):
                result.append(upload_to_url(p, project=project))
    elif ref_img and os.path.isfile(ref_img):
        result.append(upload_to_url(ref_img, project=project))
    return result


def quick_query(task_id: str) -> dict[str, Any]:
    try:
        api_key = load_api_key()
    except SystemExit:
        return {"status": "error", "progress": 0, "video_url": None, "raw": {"error": "API Key 未配置"}}
    req = Request(
        f"{API_BASE_VIDEO}/videos/{task_id}",
        headers={"Authorization": f"Bearer {api_key}"}, method="GET",
    )
    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"status": "error", "progress": 0, "video_url": None, "raw": {"error": f"HTTP {e.code}: {body}"}}
    except URLError as e:
        return {"status": "error", "progress": 0, "video_url": None, "raw": {"error": str(e.reason)}}
    status = data.get("status", "unknown")
    progress = data.get("progress", 0)
    video_url = None
    if status == "completed":
        # url 可能在顶层字段或 metadata.url（API 版本差异）
        video_url = data.get("url") or data.get("metadata", {}).get("url")
    return {"status": status, "progress": progress, "video_url": video_url, "raw": data}


def poll_task(api_key: str, task_id: str, poll_interval: int = 15, timeout: int = 600) -> str:
    start = time.time()
    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            raise SystemExit(f"[ERROR] 超时 ({timeout}s)：任务 {task_id} 未完成")
        req = Request(
            f"{API_BASE_VIDEO}/videos/{task_id}",
            headers={"Authorization": f"Bearer {api_key}"}, method="GET",
        )
        try:
            with urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
            result = json.loads(body)
        except HTTPError as e:
            body_err = e.read().decode("utf-8", errors="replace")
            _log(f"[ERROR] 查询失败 HTTP {e.code}: {body_err[:200]}")
            time.sleep(poll_interval)
            continue
        except (URLError, json.JSONDecodeError, OSError) as e:
            _log(f"[WARN] 查询异常 ({type(e).__name__}: {e})，{poll_interval}s 后重试...")
            time.sleep(poll_interval)
            continue
        status = result.get("status", "unknown")
        progress = result.get("progress", 0)
        _log(f"  [状态] {status} | 进度: {progress}% | 耗时: {int(elapsed)}s")
        if status == "completed":
            video_url = result.get("url") or result.get("metadata", {}).get("url")
            if not video_url:
                raise SystemExit(f"[ERROR] 完成但无视频 URL: {json.dumps(result, ensure_ascii=False)}")
            _log(f"  [OK] 视频生成完成！")
            return video_url
        elif status == "failed":
            raise SystemExit(f"[ERROR] 视频生成失败: {result.get('error', '未知错误')}")
        time.sleep(poll_interval)


def download_video(url: str, output_path: str) -> str:
    _log(f"  [下载] 从 {url[:60]}...")
    data = None
    dl_attempt = 0
    while True:
        dl_attempt += 1
        try:
            req = Request(url, method="GET")
            with urlopen(req, timeout=300) as resp:
                data = resp.read()
            break
        except (URLError, ConnectionError, OSError) as e:
            wait = min(2 ** min(dl_attempt, 8), 300)
            _log(f"  ⚠️  视频下载失败 (第{dl_attempt}次): {e}，{wait}秒后重试...")
            time.sleep(wait)
            continue
    with open(output_path, "wb") as f:
        f.write(data)
    _log(f"  [OK] 保存: {output_path}")
    return output_path


def get_closest_valid_frames(target: int) -> int:
    return min(VALID_FRAMES, key=lambda x: abs(x - target))


def parse_size(size_str: str) -> tuple[int, int]:
    if size_str in ASPECT_MAP:
        return ASPECT_MAP[size_str]
    if "x" in size_str:
        parts = size_str.split("x")
        return int(parts[0]), int(parts[1])
    return 1152, 768
