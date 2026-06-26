#!/usr/bin/env python3
"""Direct inquiry CLI entrypoint."""

COMMAND_NAME = "inquiry"
COMMAND_DESC = "发起 inquiry 实例或按 instanceId 查询结果"

import json
import os
import re
import sys
import argparse
import uuid
from typing import Any, List

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _output import print_error
from _errors import ParamError
from capabilities.inquiry.service import get_inquiry_result, start_direct_inquiry

DEFAULT_OUTPUT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '.skill_outputs'))


def _extract_final_result(instance_data: Any) -> Any:
    """Return the result payload for final machine output."""
    if not isinstance(instance_data, dict):
        return []
    data = instance_data.get("data")
    if isinstance(data, dict) and "result" in data:
        return data.get("result")
    return []


def _extract_field_desc(instance_data: Any) -> Any:
    """Return fieldDesc from instance data when provided by the API."""
    if not isinstance(instance_data, dict):
        return {}
    data = instance_data.get("data")
    if isinstance(data, dict) and "fieldDesc" in data:
        return data.get("fieldDesc")
    if "fieldDesc" in instance_data:
        return instance_data.get("fieldDesc")
    return {}


def _build_final_output(result: Any) -> dict:
    """Build the final machine output with instanceId, fieldDesc, and result."""
    if not isinstance(result, dict):
        return {"instanceId": "", "fieldDesc": {}, "result": []}
    instance_data = result.get("instance_data", {})
    return {
        "instanceId": result.get("instance_id", ""),
        "fieldDesc": _extract_field_desc(instance_data),
        "result": _extract_final_result(instance_data),
    }


def _build_start_output(result: Any) -> dict:
    """Build the start output with only instanceId."""
    if not isinstance(result, dict):
        return {"instanceId": ""}
    return {"instanceId": result.get("instance_id", "")}


def _write_uuid_output_file(output_dir: str, payload: Any) -> str:
    """Write final JSON output to a per-run UUID file."""
    output_root = os.path.abspath(output_dir)
    os.makedirs(output_root, exist_ok=True)
    output_path = os.path.join(output_root, "inquiry-data-{}.json".format(uuid.uuid4().hex))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
        f.write("\n")
    return output_path


def _print_json(payload: Any, compact: bool = False) -> None:
    """Print JSON payload."""
    if compact:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


def _emit_query_output(payload: Any, output_dir: str) -> None:
    """Write query output to a UUID file and print only its path."""
    output_file = _write_uuid_output_file(output_dir, payload)
    _print_json({"outputFile": output_file})


def _split_plain_questions(raw: str) -> List[str]:
    """Split plain text questions by newlines or semicolons."""
    return [part.strip() for part in re.split(r"[\n;；]+", raw or "") if part.strip()]


def _parse_questions(raw: str) -> List[Any]:
    """Parse questions from JSON or plain text."""
    raw = (raw or "").strip()
    if not raw:
        return []

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return _split_plain_questions(raw)

    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, str):
        return _split_plain_questions(parsed)
    if isinstance(parsed, dict):
        return [parsed]

    raise ParamError("questions 必须是 JSON 数组、JSON 对象、字符串或分号/换行分隔文本")


def main():
    parser = argparse.ArgumentParser(description="发起 inquiry 实例或按 instanceId 查询结果")
    parser.add_argument("--requirement", "-r", default="",
                        help="发起 inquiry 时必填，需包含找品需求和询盘问题")
    parser.add_argument("--instance-id", default="",
                        help="查询已有 inquiry 实例数据时传入")
    parser.add_argument("--questions", "-q", default="",
                        help="可选。询盘问题，支持 JSON 数组/对象/字符串，或分号/换行分隔文本")
    parser.add_argument("--purchase-size", "-c", type=int, default=1,
                        help="采购数量，默认 1")
    parser.add_argument("--inquiry-item-size", type=int, default=30,
                        help="询盘商品数，默认 30")
    parser.add_argument("--recall-item-size", type=int, default=30,
                        help="找品商品数，默认 30")
    parser.add_argument("--image", default="",
                        help="本地图片路径，多个用逗号分隔；HTTP(S) URL 会按远程图片处理（可选）")
    parser.add_argument("--image-url", default="",
                        help="图片 URL，多个用逗号分隔；会先下载并上传到纵横平台（可选）")
    parser.add_argument("--output-dir", default="",
                        help="查询实例数据时使用。脚本在该目录下自动生成 UUID 文件名并写入最终 JSON；默认使用仓库 .skill_outputs")
    parser.add_argument("--output-mode", choices=("file", "stdout"), default="file",
                        help="查询实例数据输出模式：file 只输出结果文件路径；stdout 直接输出结果 JSON")
    args = parser.parse_args()

    try:
        if args.instance_id:
            result = get_inquiry_result(
                instance_id=args.instance_id,
            )
            output = _build_final_output(result)
            if args.output_mode == "stdout":
                _print_json(output, compact=True)
            else:
                _emit_query_output(output, args.output_dir or DEFAULT_OUTPUT_DIR)
        else:
            if args.output_dir:
                raise ParamError("--output-dir 只能和 --instance-id 一起使用")
            if args.output_mode != "file":
                raise ParamError("--output-mode 只能和 --instance-id 一起使用")
            if not args.requirement.strip():
                raise ParamError("requirement 不能为空")
            question_list = _parse_questions(args.questions)
            local_images = [p.strip() for p in args.image.split(",") if p.strip()] if args.image else None
            image_urls = [u.strip() for u in args.image_url.split(",") if u.strip()] if args.image_url else None
            result = start_direct_inquiry(
                requirement=args.requirement,
                question_list=question_list,
                purchase_size=args.purchase_size,
                inquiry_item_size=args.inquiry_item_size,
                recall_item_size=args.recall_item_size,
                local_images=local_images,
                image_urls=image_urls,
            )
            _print_json(_build_start_output(result))
    except KeyboardInterrupt:
        print(json.dumps({
            "success": False,
            "message": "用户中断操作",
        }, ensure_ascii=False, indent=2))
    except Exception as e:
        print_error(e, {})


if __name__ == "__main__":
    main()
