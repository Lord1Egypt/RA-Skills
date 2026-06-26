"""Qwen 编辑图脚本。

两种调用方式：
1. 标记编辑：--prompt + --markers-file（从 JSON 文件读取原图/标记图）
2. 自由编辑：--prompt + --raw-image（可多次传入，直接用用户 prompt）

生成的图片默认推送到画布。

用法：
    # 标记编辑
    py qwen_edit_image.py --prompt "把<<标记点1>>修改为蓝色" --markers-file "<画布图片文件URL>"

    # 自由编辑（单图）
    py qwen_edit_image.py --prompt "变成卡通风格" --raw-image "<图片URL>"

    # 自由编辑（多图）
    py qwen_edit_image.py --prompt "把图一的人物放到图二的背景上" --raw-image "img1.png" --raw-image "img2.png"

SECURITY MANIFEST:
- Environment variables accessed: QWEN_EDIT_IMAGE_API_KEY, QWEN_EDIT_IMAGE_MODEL, QWEN_BASE_URL, CANVAS_SERVER
- External endpoints called: https://dashscope.aliyuncs.com/api/v1 (Qwen API), http://localhost:*/api/canvas/sync/* (local canvas)
- Local files read: markers-file JSON (if provided as local path), raw-image files (if provided as local paths)
- Local files written: none
"""
import argparse
import json
import os
import urllib.request

QWEN_BASE_URL = os.environ.get("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/api/v1")
QWEN_EDIT_IMAGE_API_KEY = os.environ.get("QWEN_EDIT_IMAGE_API_KEY", "")
QWEN_EDIT_IMAGE_MODEL = os.environ.get("QWEN_EDIT_IMAGE_MODEL", "qwen-image-edit-max-2026-01-16")
CANVAS_SERVER = os.environ.get("CANVAS_SERVER", "http://localhost:39301")


def build_marker_prompt(user_instruction: str) -> str:
    """标记编辑模式的专业提示词。"""
    return f"""Using the provided images (original image and dashed marked image):

The marked image has a colored dashed border, with colors limited to red, yellow, blue, or green, indicating the area within the dashed line that needs editing. {user_instruction}

The lower right corner of the colored border contains a colored circle with a number; the number corresponds to different modification logic.

Important: Do not include or retain any colored (red, yellow, blue, or green) dashed borders in the final output image. Colored dashed borders are for reference only and must be completely removed.

Important Notes:
- Understand the purpose of the dashed border and edit the area and objects it contains, paying attention to details.
- Remove all auxiliary dashed markers and numbers from the modified image, ensuring no trace remains.
- Keep everything outside the marked areas exactly the same.
- Preserve the original style, lighting, and composition.
- Ensure all changes blend naturally with the surrounding environment."""


def load_file(path: str) -> dict:
    """加载 JSON 文件（支持 URL 或本地路径）。"""
    if path.startswith(("http://", "https://")):
        with urllib.request.urlopen(path, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def download_as_base64(image_ref: str) -> str:
    """下载图片并转为 base64 data URL。"""
    from image_to_base64 import image_to_base64
    return image_to_base64(image_ref)


def call_qwen(prompt: str, image_refs: list[str]) -> str:
    """调用 Qwen 编辑图 API，返回结果图 URL。"""
    if not QWEN_EDIT_IMAGE_API_KEY:
        raise RuntimeError("请设置环境变量 QWEN_EDIT_IMAGE_API_KEY")

    from dashscope import MultiModalConversation
    import dashscope

    dashscope.base_http_api_url = QWEN_BASE_URL

    content = [{"image": download_as_base64(ref)} for ref in image_refs]
    content.append({"text": prompt})

    response = MultiModalConversation.call(
        api_key=QWEN_EDIT_IMAGE_API_KEY,
        model=QWEN_EDIT_IMAGE_MODEL,
        messages=[{"role": "user", "content": content}],
        stream=False,
        n=1,
        watermark=False,
    )

    status_code = getattr(response, "status_code", None) or response.get("status_code")
    if status_code != 200:
        code = getattr(response, "code", None) or response.get("code", "")
        message = getattr(response, "message", None) or response.get("message", "")
        raise RuntimeError(f"Qwen 编辑图调用失败: {code} - {message}")

    output = getattr(response, "output", None) or response.get("output", {})
    choices = getattr(output, "choices", None) or output.get("choices", [])
    if not choices:
        raise RuntimeError("Qwen 编辑图返回为空")

    msg = choices[0].get("message", {})
    for item in msg.get("content", []):
        if "image" in item:
            return item["image"]

    raise RuntimeError("Qwen 编辑图返回中没有图片 URL")


def _push_to_canvas(image_url: str) -> dict:
    """推送图片到画布，返回结果。"""
    try:
        from push_to_canvas import push_to_canvas
        element_id, local_url = push_to_canvas(image_url)
        return {"pushed": True, "element_id": element_id, "local_url": local_url}
    except Exception as e:
        return {"pushed": False, "push_error": str(e)}


def run_marker_edit(prompt: str, markers_file: str) -> list[dict]:
    """标记编辑模式：从 JSON 文件读取图片信息。"""
    data = load_file(markers_file)
    canvas_markers = data.get("canvas_markers", [])
    if not canvas_markers:
        raise RuntimeError("标记文件中没有 canvas_markers 数据")

    results = []
    for item in canvas_markers:
        raw_image = item.get("raw_image")
        marked_image = item.get("marked_image")
        if not raw_image or not marked_image:
            continue

        final_prompt = build_marker_prompt(prompt)
        image_url = call_qwen(final_prompt, [raw_image, marked_image])

        result = {"id": item.get("id"), "markers": item.get("markers", []), "status": "ok", "url": image_url}
        result.update(_push_to_canvas(image_url))
        results.append(result)

    return results


def run_free_edit(prompt: str, raw_images: list[str]) -> list[dict]:
    """自由编辑模式：直接用用户 prompt + 原图。"""
    image_url = call_qwen(prompt, raw_images)
    result = {"status": "ok", "url": image_url}
    result.update(_push_to_canvas(image_url))
    return [result]


def main():
    parser = argparse.ArgumentParser(description="Qwen 编辑图")
    parser.add_argument("--prompt", required=True, help="编辑指令")
    parser.add_argument("--markers-file", default=None, help="画布图片文件 URL 或本地路径（标记编辑模式）")
    parser.add_argument("--raw-image", action="append", dest="raw_images", default=None, help="原图 URL 或本地路径，可多次传入（自由编辑模式）")
    args = parser.parse_args()

    if args.markers_file and args.raw_images:
        raise RuntimeError("--markers-file 和 --raw-image 不能同时使用")
    if not args.markers_file and not args.raw_images:
        raise RuntimeError("必须指定 --markers-file 或 --raw-image")

    if args.markers_file:
        results = run_marker_edit(args.prompt, args.markers_file)
    else:
        results = run_free_edit(args.prompt, args.raw_images)

    output = results[0] if len(results) == 1 else results
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
