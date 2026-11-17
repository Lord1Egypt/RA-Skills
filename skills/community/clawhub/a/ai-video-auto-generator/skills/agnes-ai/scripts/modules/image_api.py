"""Agnes AI 文生图/图生图 API 调用。"""
import base64, json, mimetypes, os, sys, time
from datetime import datetime
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_BASE = "https://apihub.agnes-ai.com/v1"
DEFAULT_MODEL = "agnes-image-2.1-flash"

# 最后一次 API 调用的原始错误（供上层分类+策略用）
_last_api_error: dict[str, Any] | None = None


def get_last_api_error() -> dict[str, Any] | None:
    """返回最近一次 generate_image 的 API 原始错误（如有），用于错误分类。"""
    return _last_api_error
VERSION = "2.1.0"

import sys
_mod_dir = os.path.dirname(os.path.abspath(__file__))
if _mod_dir not in sys.path:
    sys.path.insert(0, _mod_dir)
from config import _log, LOG_LEVEL


def _url_still_valid(url: str, timeout: int = 5) -> bool:
    """轻量 HEAD 请求验证 provider URL 是否仍可访问。过期则降级到图床上传。"""
    try:
        req = Request(url, method="HEAD")
        with urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def load_api_key(key_path: str | None = None) -> str:
    if key_path and os.path.isfile(key_path):
        with open(key_path, encoding="utf-8") as f:
            return f.read().strip()
    env_key = os.environ.get("AGNES_API_KEY")
    if env_key:
        return env_key
    default_path = os.path.expanduser("~/.agnes-api-key")
    if os.path.isfile(default_path):
        with open(default_path, encoding="utf-8") as f:
            return f.read().strip()
    try:
        from .config import get_agnes_key
        toml_key = get_agnes_key()
        if toml_key:
            return toml_key
    except ImportError:
        pass
    raise SystemExit(
        "错误：未找到 API Key。请执行以下任一操作：\n"
        "  1. 设置环境变量 AGNES_API_KEY\n"
        "  2. 将 Key 写入 ~/.agnes-api-key\n"
        "  3. 使用 --api-key 参数指定 Key 文件路径\n"
        "获取 Key：https://platform.agnes-ai.com"
    )


def _load_github_config() -> tuple[str, str]:
    """从统一配置读取 GitHub 仓库信息（通过 modules.config → _shared_tools Layer 2 优先级链）。"""
    try:
        from modules.config import get_github_repo, get_github_branch
        return get_github_repo(), get_github_branch()
    except ImportError:
        pass
    return "JinXuchen2020/video-images", "master"


def upload_to_url(local_path: str, project: str | None = None) -> str:
    GITHUB_REPO, GITHUB_BRANCH = _load_github_config()

    if project:
        proj_name = os.path.basename(os.path.abspath(project))
    else:
        _log("  ⚠️ upload_to_url: project=None，使用'default'（检查调用方是否漏传 project）")
        proj_name = "default"

    token = None
    pat_path = os.path.expanduser("~/.github-pat")
    if os.path.isfile(pat_path):
        with open(pat_path) as f:
            token = f.read().strip()
    if not token:
        token = os.environ.get("GITHUB_PAT")

    if token:
        # 优先使用 provider 返回的原始 URL（旁注文件），跳过 GitHub 上传
        url_sidecar = local_path + ".origin_url.txt"
        if os.path.isfile(url_sidecar):
            with open(url_sidecar, encoding="utf-8") as f:
                provider_url = f.read().strip()
            if provider_url and _url_still_valid(provider_url):
                _log(f"  -> 使用 provider URL: {provider_url[:60]}...")
                return provider_url
            else:
                # URL 已过期或不可达，降级到 GitHub 上传
                try:
                    os.remove(url_sidecar)
                    _log(f"  -> provider URL 已过期或不可达，删除 .origin_url.txt 旁注，降级到图床上传")
                except OSError:
                    pass

        remote_name = os.path.basename(local_path)
        encoded_remote_name = quote(remote_name, safe="")
        encoded_proj = quote(proj_name, safe="")
        api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{encoded_proj}/{encoded_remote_name}"
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{encoded_proj}/{encoded_remote_name}"

        upload_attempt = 0
        MAX_UPLOAD_RETRY = 4
        while upload_attempt < MAX_UPLOAD_RETRY:
            upload_attempt += 1
            try:
                sha = None
                get_req = Request(api_url, headers={
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github.v3+json",
                }, method="GET")
                try:
                    with urlopen(get_req, timeout=10) as resp:
                        existing = json.loads(resp.read().decode())
                        sha = existing.get("sha")
                        if sha:
                            _log(f"  -> GitHub 已存在: {raw_url}")
                            return raw_url
                except HTTPError:
                    pass

                # 文件不存在，读取原始文件上传（不压缩、不缩放）
                with open(local_path, "rb") as f:
                    content_b64 = base64.b64encode(f.read()).decode()
                _log(f"  -> 上传原图 ({os.path.getsize(local_path)//1024}KB)")

                payload = {
                    "message": f"upload {remote_name}",
                    "content": content_b64,
                    "branch": GITHUB_BRANCH,
                }

                put_req = Request(
                    api_url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"token {token}",
                        "Content-Type": "application/json",
                        "Accept": "application/vnd.github.v3+json",
                    },
                    method="PUT",
                )
                with urlopen(put_req, timeout=30) as resp:
                    result = json.loads(resp.read().decode())
                    if result.get("content", {}).get("name"):
                        _log(f"  -> GitHub URL: {raw_url}")
                        return raw_url
            except HTTPError as e:
                # 401/403 属凭据失效，重试无意义，直接抛出给上层
                if e.code in (401, 403):
                    msg = f"GitHub PAT 无效或已过期 (HTTP {e.code})，请检查 ~/.github-pat"
                    _log(f"  ❌ {msg}", level=0)
                    raise ValueError(msg)
                wait = min(10 * upload_attempt, 60)
                _log(f"  -> GitHub 上传失败 (HTTP {e.code})，{wait}秒后重试 (第{upload_attempt}次)...")
                time.sleep(wait)
                continue
            except Exception as e:
                err_name = type(e).__name__
                wait = min(10 * upload_attempt, 60)
                _log(f"  -> GitHub 上传失败 ({err_name})，{wait}秒后重试 (第{upload_attempt}次)...")
                time.sleep(wait)
                continue
        else:
            # while 正常耗尽（重试上限，多为 5xx/网络问题）
            msg = f"GitHub 上传重试 {MAX_UPLOAD_RETRY} 次失败，放弃"
            _log(f"  ❌ {msg}", level=0)
            raise RuntimeError(msg)

    # token 为空 → 无 GitHub PAT 配置，用 base64 data URI 内联图片
    # 注意：data URI 仅对 Agnes 图片生成有效，视频参考图不支持。若需视频，必须配置有效 PAT。
    try:
        from PIL import Image
        import io
        img = Image.open(local_path).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        compressed = buf.getvalue()
        b64 = base64.b64encode(compressed).decode()
        mime = "image/jpeg"
        original_kb = os.path.getsize(local_path) // 1024
        b64_size = len(b64) // 1024
        _log(f"  -> 压缩 base64 ({original_kb}KB → {b64_size}KB)")
    except Exception:
        with open(local_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        mime = mimetypes.guess_type(local_path)[0] or "image/png"
        b64_size = len(b64) // 1024
        if b64_size > 1000:
            _log(f"  ⚠️ base64 较大 ({b64_size} KB)")
        _log(f"  -> 使用 data URI ({b64_size} KB base64)")
    return f"data:{mime};base64,{b64}"

def generate_image(
    api_key: str,
    prompt: str,
    model: str = DEFAULT_MODEL,
    size: str = "1024x1024",
    n: int = 1,
    quality: str = "standard",
    output_dir: str = ".",
    ref_image: str | None = None,
    ref_images: list[str] | None = None,
    output_name: str | None = None,
    project: str | None = None,
    negative_prompt: str | None = None,
    seed: int | None = None,
) -> list[str]:
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": n,
        "quality": quality,
    }

    images_to_upload: list[str] = []
    if ref_images:
        images_to_upload = ref_images
        mode_label = f"图生图({len(ref_images)}张参考图)"
    elif ref_image:
        images_to_upload = [ref_image]
        mode_label = "图生图(单图)"
    else:
        mode_label = "文生图"

    payload["extra_body"] = {"response_format": "url"}
    if images_to_upload:
        payload["extra_body"]["image"] = [upload_to_url(p, project) for p in images_to_upload]

    if negative_prompt:
        payload["extra_body"]["negative_prompt"] = negative_prompt
    if seed is not None:
        payload["extra_body"]["seed"] = seed

    req = Request(
        f"{API_BASE}/images/generations",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    _log(f"  -> {mode_label}（模型: {model} | 尺寸: {size}）")

    if LOG_LEVEL >= 2:
        debug_payload = {k: v for k, v in payload.items() if k != "api_key"}
        _log(f"  [DEBUG] 请求体: {json.dumps(debug_payload, ensure_ascii=False)[:500]}", level=2)

    api_attempt = 0
    result = None
    MAX_API_RETRY = 6  # 防止持续 429/5xx 或 400 审核拒绝时无限重试卡死
    while api_attempt < MAX_API_RETRY:
        api_attempt += 1
        try:
            with urlopen(req, timeout=300) as resp:
                result = json.loads(resp.read().decode())
                _log(f"  [DEBUG] API 响应: {json.dumps(result, ensure_ascii=False)[:300]}", level=2)
                break
        except HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            # 4xx 客户端错误（非 429 限流）不可重试：400 审核拒绝 / 403 等立即放弃
            if 400 <= e.code < 500 and e.code != 429:
                _log(f"  ❌ HTTP {e.code}（客户端错误，不可重试）: {body[:300]}", level=0)
                global _last_api_error
                _last_api_error = {"error": {"code": str(e.code), "message": body[:500]}}
                return None
            wait = min(2 ** min(api_attempt, 8), 300)
            if api_attempt == 1:
                _log(f"  ⚠️ HTTP {e.code}: {body[:300]}")
            _log(f"  ⚠️ HTTP {e.code}，{wait}秒后重试 (第{api_attempt}次)...")
            time.sleep(wait)
            continue
        except URLError as e:
            wait = min(2 ** min(api_attempt, 8), 300)
            _log(f"  ⚠️ 网络错误 ({e.reason})，{wait}秒后重试 (第{api_attempt}次)...")
            time.sleep(wait)
            continue
    if result is None:
        _log(f"  ❌ 图像生成重试 {MAX_API_RETRY} 次仍失败，放弃", level=0)
        return None

    images = result.get("data", [])
    if not images:
        raise SystemExit("API 返回为空，没有图片数据。")

    os.makedirs(output_dir, exist_ok=True)
    saved_files = []

    for i, img_data in enumerate(images):
        url = img_data.get("url")
        if not url:
            _log(f"  [WARN] 第 {i+1} 张图无 URL，跳过")
            continue

        if output_name:
            if len(images) > 1:
                base, ext = os.path.splitext(output_name)
                filename = f"{base}_{i+1}{ext}"
            else:
                filename = output_name
        else:
            timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
            safe_prompt = "".join(c if c.isalnum() or c in " _-" else "_" for c in prompt[:30])
            filename = f"{safe_prompt}_{timestamp}_{i+1}.png"
        filepath = os.path.join(output_dir, filename)

        _log(f"  下载第 {i+1}/{len(images)} 张...")
        img_req = Request(url, headers={"User-Agent": "WorkBuddy-Agnes-Skill"})
        with urlopen(img_req, timeout=180) as img_resp:
            img_data_bytes = img_resp.read()

        with open(filepath, "wb") as f:
            f.write(img_data_bytes)

        # 保存 provider 返回的 URL 为旁注文件，供后续 upload_to_url 优先使用
        #（避免重新上传到 GitHub 等外部图床）
        url_sidecar = filepath + ".origin_url.txt"
        with open(url_sidecar, "w", encoding="utf-8") as f:
            f.write(url)

        saved_files.append(filepath)
        _log(f"  [OK] 保存: {filepath}")

    return saved_files
