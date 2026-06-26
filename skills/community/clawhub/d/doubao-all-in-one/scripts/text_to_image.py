# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "volcengine-python-sdk[ark]",
# ]
# ///

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from volcenginesdkarkruntime.types.images import OptimizePromptOptions, SequentialImageGenerationOptions

from common import create_client, default_output_path, generate_image_with_fallback, get_trace_id, log_params, save_image_results, setup_logging

setup_logging()


DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_PROMPT = (
    "充满活力的特写编辑肖像，模特眼神锐利，头戴雕塑感帽子，"
    "色彩拼接丰富，眼部焦点锐利，景深较浅，具备 Vogue 杂志封面的美学风格，"
    "采用中画幅拍摄，工作室灯光效果强烈。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="豆包文生图")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="提示词")
    parser.add_argument("--name", default="", help="文件名描述，不超过 10 个中文字")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型 ID")
    parser.add_argument("--size", default="2K", help="输出尺寸，如 2K、3K、4K 或 2048x2048，默认 2K")
    parser.add_argument(
        "--output", type=Path, help="输出文件路径，默认写入 outputs/doubao/images/text_to_image/",
    )
    parser.add_argument("--watermark", action="store_true", default=False, help="添加水印（默认关闭）")
    parser.add_argument(
        "--response-format", choices=["b64_json", "url"], default="b64_json",
        help="返回格式，默认 b64_json",
    )
    parser.add_argument("--output-format", choices=["png", "jpeg"], default=None, help="输出文件格式（仅 5.0 lite）")
    parser.add_argument(
        "--guidance-scale", type=float, default=None,
        help="文本权重，范围 [1, 10]（仅 3.0 系列支持）",
    )
    parser.add_argument(
        "--sequential-image-generation", choices=["auto", "disabled"], default="disabled",
        help="组图模式：auto（自动判断）/ disabled（关闭）",
    )
    parser.add_argument(
        "--max-images", type=int, default=15, help="组图最大数量，范围 [1, 15]",
    )
    parser.add_argument(
        "--optimize-prompt", choices=["standard", "fast"], default=None,
        help="提示词优化模式：standard / fast（仅 5.0 lite/4.5/4.0）",
    )
    parser.add_argument(
        "--web-search", action="store_true", default=False,
        help="启用联网搜索（仅 5.0 lite）",
    )
    return parser.parse_args()


def main() -> None:
    pipeline_start = time.monotonic()
    args = parse_args()
    trace_id = get_trace_id()
    log_params("文生图开始", model=args.model, size=args.size, prompt=args.prompt, name=args.name)
    client = create_client()
    output_path = args.output or default_output_path("images", "text_to_image", name=args.name)

    # Build kwargs
    kwargs: dict = {
        "prompt": args.prompt,
        "size": args.size,
        "response_format": args.response_format,
        "watermark": args.watermark,
        "sequential_image_generation": args.sequential_image_generation,
    }
    if args.sequential_image_generation == "auto" and args.max_images is not None:
        kwargs["sequential_image_generation_options"] = SequentialImageGenerationOptions(max_images=args.max_images)
    if args.optimize_prompt is not None:
        kwargs["optimize_prompt_options"] = OptimizePromptOptions(mode=args.optimize_prompt)
    if args.web_search:
        kwargs["tools"] = [{"type": "web_search"}]
    if args.guidance_scale is not None:
        kwargs["guidance_scale"] = args.guidance_scale
    if args.output_format is not None:
        kwargs["output_format"] = args.output_format

    api_start = time.monotonic()
    response, used_model = generate_image_with_fallback(client, model=args.model, **kwargs)
    api_elapsed = time.monotonic() - api_start
    log_params("模型 API 调用完成", model=used_model, elapsed=round(api_elapsed, 3))

    # Save all images (group image support)
    results = save_image_results(response.data, output_path)
    log_params("图片保存完成", count=len(results), path=str(output_path.name))

    first_result = {
        "type": "image",
        "scene": "text_to_image",
        "provider": "doubao",
        "trace_id": trace_id,
        "used_model": used_model,
    }
    # Attach first image's local_path for backward compatibility
    if results:
        first_result["local_path"] = results[0].get("local_path", "")
        if len(results) > 1:
            first_result["images"] = results

    total_elapsed = time.monotonic() - pipeline_start
    log_params("文生图完成", total_elapsed=round(total_elapsed, 3))
    output = {
        **first_result,
        "image_count": len(results),
        "generated_images": len([r for r in results if "local_path" in r]),
        "timing": {
            "total_elapsed": round(total_elapsed, 3),
            "api_elapsed": round(api_elapsed, 3),
        },
        "usage": {
            "generated_images": getattr(response, "usage", None) and getattr(response.usage, "generated_images", 0) or len(results),
            "output_tokens": getattr(response, "usage", None) and getattr(response.usage, "output_tokens", 0) or 0,
            "total_tokens": getattr(response, "usage", None) and getattr(response.usage, "total_tokens", 0) or 0,
        } if hasattr(response, "usage") else {},
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
