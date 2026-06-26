#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError
from typing import Dict, List, Optional, Tuple

WAVESPEED_UPLOAD = "https://api.wavespeed.ai/api/v3/media/upload/binary"
WAVESPEED_APIS = {
    "nano": "https://api.wavespeed.ai/api/v3/google/nano-banana-2/edit",
    "openai": "https://api.wavespeed.ai/api/v3/openai/gpt-image-1.5/edit",
    "fast": "https://api.wavespeed.ai/api/v3/google/nano-banana-2/edit-fast",
}
WAVESPEED_PREFERRED_ORDER = ["nano", "openai", "fast"]

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
ARK_BASE_URL = os.environ.get("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
NANO_BASE_URL = os.environ.get("NANO_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
NANO_MODEL = os.environ.get("NANO_MODEL", "gemini-3.1-flash-image-preview")
ARK_MODEL = os.environ.get("ARK_MODEL", "doubao-seedream-5-0-260128")

BODY_LOCK = (
    "这是一个没有下肢结构且有两只大鳌的龙虾状生物 记住他的生物特征 当我们给他穿上其他装备的时候 严格保持图一的形体结构 透视比例不变 保持图一的画风不变。"
    "只给这个角色增加不同装备，不要改变基础身体。"
    "严格保护角色资产，不要重设计角色本体，不要替换生物种类，不要改成其他物种或人形角色。"
    "保持同样的头身比例、同样的大鳌比例、同样的尾巴位置、同样的屏幕脸比例、同样的悬浮感。"
    "不要增加下肢，不要增加双腿、脚、膝盖、鞋子、裤腿或任何新的步行肢体结构，不要把角色改成站立式双足角色。"
    "如果灵感来源里出现有腿的角色，也只提取服装、配件、帽子、道具、配色和气质，不继承腿部或人体骨架。"
    "保持图一这种可爱、柔和、皮克斯感的3D卡通渲染风格。"
)

TEMPLATES = {
    "hiphop-streetwear": "嘻哈街头风：鸭舌帽、金链子、宽松街头服饰、潮流潮玩感。",
    "hero-tech-armor": "英雄科技装甲风：高科技装甲语言、能量核心、流线型护甲、英雄感但仍然可爱。",
    "platform-adventurer": "卡通平台冒险家风：经典冒险帽子、鲜明主色、冒险装束、轻松活泼。",
    "monster-trainer": "怪物训练师风：训练师帽子、功能性夹克或背心、冒险伙伴主角感。",
    "royal-regalia": "皇家礼装风：高辨识头饰、华丽礼服、精致装饰、收藏级角色感。",
    "candy-cyber": "糖果赛博风：柔和霓虹配色、赛博头饰、科技感服装、可爱未来感。",
    "cosmic-companion": "宇宙伙伴风：星环或宇宙头饰、温柔神秘的太空服饰、星尘与轨道元素、可爱又值得信任。",
    "animal-hood": "动物头套风：可爱包裹式头套、清晰头部轮廓、吉祥物感、萌系治愈感。",
    "mascot-crown": "吉祥物王冠风：小巧但高辨识度的头顶装饰、简洁但有身份感的头部设计。",
    "magical-mage": "魔法使风：长袍、法术配饰、优雅奇幻、安静神秘。",
}

BACKEND_CHOICES = ["wavespeed", "openai-direct", "nano-direct", "ark-direct"]
ALL_MODE_CHOICES = ["nano", "openai", "fast", "auto"]


def default_mother_image() -> Path:
    skill_dir = Path(__file__).resolve().parent.parent
    asset_path = skill_dir / "assets" / "default-mother-image.png"
    if asset_path.exists():
        return asset_path

    asset_path.parent.mkdir(parents=True, exist_ok=True)
    fallback_url = "https://www.8uddy.land/images/clawy.png"
    asset_path.write_bytes(http_get_bytes(fallback_url))
    return asset_path


def guess_mime(path: Path) -> str:
    return mimetypes.guess_type(str(path))[0] or "image/png"


def load_image_bytes(path: Path) -> bytes:
    return path.read_bytes()


def load_image_b64(path: Path) -> str:
    return base64.b64encode(load_image_bytes(path)).decode()


def build_prompt(template: str, inspiration: str, vibe: str, colors: str, extra: str) -> str:
    parts = [BODY_LOCK, "背景保持简洁干净的NFT头像风格。"]
    if template:
        parts.append(f"模板方向：{TEMPLATES[template]}")
    if inspiration:
        parts.append(f"灵感来源：{inspiration}。请参考这些灵感中的装备语言、气质、头饰、服装结构或配色，但不要破坏角色本体。")
    if vibe:
        parts.append(f"整体气质：{vibe}。")
    if colors:
        parts.append(f"配色偏好：{colors}。")
    if extra:
        parts.append(extra)
    return "".join(parts)


def detect_image_capability() -> Dict[str, List[str]]:
    capabilities: Dict[str, List[str]] = {}
    if os.environ.get("WAVESPEED_API_KEY"):
        capabilities["wavespeed"] = WAVESPEED_PREFERRED_ORDER.copy()
    if os.environ.get("OPENAI_API_KEY"):
        capabilities["openai-direct"] = ["openai"]
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("NANO_API_KEY"):
        capabilities["nano-direct"] = ["nano"]
    if os.environ.get("ARK_API_KEY"):
        capabilities["ark-direct"] = ["openai"]
    return capabilities


def choose_backend(requested_backend: Optional[str], available: Dict[str, List[str]]) -> Tuple[str, Optional[str]]:
    if not available:
        raise RuntimeError(
            "No usable image-edit capability found. Configure WaveSpeed, OpenAI direct, Nano direct, or Ark direct image-edit access."
        )
    preferred = ["wavespeed", "openai-direct", "nano-direct", "ark-direct"]
    if requested_backend:
        if requested_backend in available:
            return requested_backend, None
        fallback = next((b for b in preferred if b in available), next(iter(available)))
        return fallback, f"Requested backend '{requested_backend}' is not available. Falling back to '{fallback}'."
    chosen = next((b for b in preferred if b in available), next(iter(available)))
    return chosen, None


def choose_mode(backend: str, requested_mode: Optional[str], available: Dict[str, List[str]]) -> Tuple[str, Optional[str]]:
    modes = available[backend]
    if requested_mode and requested_mode != "auto":
        if requested_mode in modes:
            return requested_mode, None
        fallback = modes[0]
        return fallback, f"Requested mode '{requested_mode}' is not available for backend '{backend}'. Falling back to '{fallback}'."
    return modes[0], None


def http_json(method: str, url: str, headers: dict, payload: dict, timeout: int = 180) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={**headers, "Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def http_get_bytes(url: str, headers: Optional[dict] = None, timeout: int = 180) -> bytes:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def wavespeed_upload_image(path: Path, api_key: str) -> str:
    out = subprocess.check_output([
        "curl", "-sS", "-X", "POST", WAVESPEED_UPLOAD,
        "-H", f"Authorization: Bearer {api_key}",
        "-F", f"file=@{path}",
    ], text=True)
    data = json.loads(out)["data"]
    return data.get("download_url") or data.get("url")


def wavespeed_build_payload(mode: str, ref_url: str, prompt: str) -> dict:
    if mode == "openai":
        return {
            "images": [ref_url],
            "prompt": prompt,
            "size": "1024*1024",
            "quality": "high",
            "input_fidelity": "high",
            "output_format": "png",
            "enable_sync_mode": False,
            "enable_base64_output": False,
        }
    if mode == "fast":
        return {
            "images": [ref_url],
            "prompt": prompt,
            "resolution": "2k",
            "output_format": "png",
            "enable_web_search": False,
            "enable_sync_mode": False,
            "enable_base64_output": False,
        }
    return {
        "images": [ref_url],
        "prompt": prompt,
        "resolution": "1k",
        "output_format": "png",
        "enable_web_search": False,
        "enable_sync_mode": False,
        "enable_base64_output": False,
    }


def wavespeed_generate(mother_path: Path, prompt: str, mode: str) -> bytes:
    api_key = os.environ["WAVESPEED_API_KEY"]
    ref_url = wavespeed_upload_image(mother_path, api_key)
    payload = wavespeed_build_payload(mode, ref_url, prompt)
    created = http_json(
        "POST",
        WAVESPEED_APIS[mode],
        {"Authorization": f"Bearer {api_key}"},
        payload,
        timeout=120,
    )
    result_url = created["data"]["urls"]["get"]
    img_url = None
    for _ in range(120):
        req = urllib.request.Request(result_url, headers={"Authorization": f"Bearer {api_key}"})
        with urllib.request.urlopen(req, timeout=120) as r:
            body = json.loads(r.read().decode())
        data = body.get("data", body)
        outputs = data.get("outputs") or []
        if outputs:
            out = outputs[0]
            img_url = out if isinstance(out, str) else out.get("url") or out.get("image")
            break
        if data.get("status") in ("failed", "canceled"):
            raise RuntimeError(json.dumps(body, ensure_ascii=False))
        time.sleep(3)
    if not img_url:
        raise RuntimeError("timed out waiting for WaveSpeed generation")
    return http_get_bytes(img_url)


def openai_direct_generate(mother_path: Path, prompt: str) -> bytes:
    api_key = os.environ["OPENAI_API_KEY"]
    url = OPENAI_BASE_URL.rstrip("/") + "/images/edits"
    out = subprocess.check_output([
        "curl", "-sS", "-X", "POST", url,
        "-H", f"Authorization: Bearer {api_key}",
        "-F", "model=gpt-image-1",
        "-F", f"prompt={prompt}",
        "-F", f"image=@{mother_path}",
        "-F", "size=1024x1024",
        "-F", "quality=high",
        "-F", "response_format=b64_json",
    ], text=True)
    body = json.loads(out)
    if body.get("error"):
        raise RuntimeError(json.dumps(body["error"], ensure_ascii=False))
    item = (body.get("data") or [{}])[0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        return http_get_bytes(item["url"])
    raise RuntimeError(f"Unexpected OpenAI image response: {body}")


def nano_direct_generate(mother_path: Path, prompt: str) -> bytes:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("NANO_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY or NANO_API_KEY")
    url = NANO_BASE_URL.rstrip("/") + f"/models/{NANO_MODEL}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {
                    "inline_data": {
                        "mime_type": guess_mime(mother_path),
                        "data": load_image_b64(mother_path),
                    }
                },
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
        },
    }
    body = http_json("POST", url, {}, payload, timeout=240)
    for candidate in body.get("candidates", []):
        parts = (((candidate or {}).get("content") or {}).get("parts") or [])
        for part in parts:
            inline = part.get("inline_data") or part.get("inlineData")
            if inline and inline.get("data"):
                return base64.b64decode(inline["data"])
    raise RuntimeError(f"Unexpected Nano direct response: {body}")


def _ark_extract_image_bytes(body: dict) -> bytes:
    if body.get("error"):
        raise RuntimeError(json.dumps(body["error"], ensure_ascii=False))
    item = (body.get("data") or [{}])[0]
    if item.get("b64_json"):
        return base64.b64decode(item["b64_json"])
    if item.get("url"):
        return http_get_bytes(item["url"])
    if item.get("image"):
        return http_get_bytes(item["image"])
    raise RuntimeError(f"Unexpected Ark response: {body}")


def ark_direct_generate(mother_path: Path, prompt: str) -> bytes:
    api_key = os.environ["ARK_API_KEY"]
    url = ARK_BASE_URL.rstrip("/") + "/images/generations"
    data_uri = f"data:{guess_mime(mother_path)};base64,{load_image_b64(mother_path)}"

    payloads = [
        {
            "model": ARK_MODEL,
            "prompt": prompt,
            "image": [data_uri],
            "response_format": "url",
            "size": "2K",
            "watermark": False,
            "stream": False,
        },
        {
            "model": ARK_MODEL,
            "prompt": prompt,
            "reference_images": [data_uri],
            "response_format": "url",
            "size": "2K",
            "watermark": False,
            "stream": False,
        },
    ]

    errors = []
    for payload in payloads:
        try:
            body = http_json("POST", url, {"Authorization": f"Bearer {api_key}"}, payload, timeout=240)
            return _ark_extract_image_bytes(body)
        except Exception as e:
            errors.append(f"fields={','.join(payload.keys())}: {e}")
    raise RuntimeError(" | ".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mother_image", nargs="?", help="Optional path to a custom mother image. If omitted, use the bundled default Halfire Labs mother image.")
    parser.add_argument("--template", default="", choices=[""] + sorted(TEMPLATES), help="Optional stable template direction.")
    parser.add_argument("--inspiration", default="", help="Free-form inspiration source(s), e.g. 'Frieren, Chopper, black corgi hood'.")
    parser.add_argument("--vibe", default="", help="Desired vibe/personality, e.g. 'cute but elegant'.")
    parser.add_argument("--colors", default="", help="Preferred color direction, e.g. 'pastel blue and silver'.")
    parser.add_argument("--backend", default="", choices=[""] + BACKEND_CHOICES, help="Optional backend: wavespeed|openai-direct|nano-direct|ark-direct")
    parser.add_argument("--mode", default="auto", choices=ALL_MODE_CHOICES, help="Optional mode. WaveSpeed supports nano|openai|fast. Direct backends ignore unsupported modes.")
    parser.add_argument("--extra", default="")
    parser.add_argument("--out", default="./out/clawy-avatar.png")
    args = parser.parse_args()

    available = detect_image_capability()
    try:
        selected_backend, backend_note = choose_backend(args.backend or None, available)
        selected_mode, mode_note = choose_mode(selected_backend, args.mode or None, available)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    mother_path = Path(args.mother_image) if args.mother_image else default_mother_image()
    if not mother_path.exists():
        print(f"Mother image not found: {mother_path}", file=sys.stderr)
        return 2

    prompt = build_prompt(args.template, args.inspiration, args.vibe, args.colors, args.extra)

    if backend_note:
        print(backend_note, file=sys.stderr)
    if mode_note:
        print(mode_note, file=sys.stderr)
    print(f"Using backend: {selected_backend}", file=sys.stderr)
    print(f"Using mode: {selected_mode}", file=sys.stderr)

    try:
        if selected_backend == "wavespeed":
            image_bytes = wavespeed_generate(mother_path, prompt, selected_mode)
        elif selected_backend == "openai-direct":
            image_bytes = openai_direct_generate(mother_path, prompt)
        elif selected_backend == "nano-direct":
            image_bytes = nano_direct_generate(mother_path, prompt)
        elif selected_backend == "ark-direct":
            image_bytes = ark_direct_generate(mother_path, prompt)
        else:
            raise RuntimeError(f"Unsupported backend: {selected_backend}")
    except (HTTPError, URLError, subprocess.CalledProcessError, RuntimeError) as e:
        print(f"Generation failed via {selected_backend}: {e}", file=sys.stderr)
        return 2

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(image_bytes)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
