#!/usr/bin/env python3
"""为剪映/CapCut 时间线槽位生成 AI Hive Seedance 2.5 素材。"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("缺少 requests，请运行 pip3 install requests")


SERVICE = "https://ai-hive.iclip.cn/api/openapi/v1"
SECRET_FILE = Path.home() / ".ai-hive" / "config.json"
EXPORTS = Path.home() / "Downloads" / "AiHive"
CAPABILITIES = {
    "broll": "public_model_seedance_2_5_t2v",
    "opener": "public_model_seedance_2_5_i2v",
    "match": "public_model_seedance_2_5_r2v",
    "clean": "public_model_seedance_2_5_video_edit",
    "tail": "public_model_seedance_2_5_video_extend",
}
CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
}


def get_secret(argument=None):
    if argument:
        return argument
    environment = os.environ.get("AI_HIVE_API_KEY")
    if environment:
        return environment
    try:
        stored = json.loads(SECRET_FILE.read_text(encoding="utf-8"))
        value = stored.get("api_key")
        if value:
            try:
                if SECRET_FILE.stat().st_mode & 0o077:
                    SECRET_FILE.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 capcut_insert.py login --api-key sk-api-*"
    )


class InsertService:
    def __init__(self, secret, verbose=False):
        self.verbose = verbose
        self.headers = {
            "Authorization": "Bearer " + secret,
            "Content-Type": "application/json",
        }

    def call(self, method, resource, **kwargs):
        address = SERVICE + "/" + resource.lstrip("/")
        if self.verbose:
            print("[service]", method, address, file=sys.stderr)
        try:
            response = requests.request(
                method,
                address,
                headers=self.headers,
                timeout=30,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise SystemExit("AI Hive 请求失败：" + str(exc))
        if not response.ok:
            try:
                message = response.json()
            except ValueError:
                message = response.text
            raise SystemExit(
                "AI Hive 返回错误 {}：{}".format(response.status_code, message)
            )
        if response.status_code == 204:
            return None
        return response.json()

    def resolve(self, kind, routing):
        fixed_id = CAPABILITIES[kind]
        models = self.call("GET", "models", params={"modelType": "VIDEO"})
        model = next(
            (entry for entry in models if entry.get("publicModelId") == fixed_id),
            None,
        )
        if model is None:
            raise SystemExit("AI Hive 当前没有固定能力：" + fixed_id)
        snapshot = next(
            (
                entry
                for entry in model.get("pricingSnapshot", [])
                if entry.get("routingMode") == routing
            ),
            None,
        )
        if snapshot is None:
            raise SystemExit("固定能力不支持路由：" + routing)
        return fixed_id, snapshot

    def upload_plan(self, path, content_type):
        return self.call(
            "POST",
            "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete(self, media_id):
        self.call("POST", "media/{}/complete".format(media_id))

    def insert(self, model_id, routing, snapshot, prompt, params,
               image_ids, video_ids, first_frame=None):
        payload = {
            "publicModelId": model_id,
            "routingMode": routing,
            "prompt": prompt,
            "imageMediaIds": image_ids,
            "videoMediaIds": video_ids,
            "audioMediaIds": [],
            "params": params,
            "pricingSnapshot": snapshot,
        }
        if first_frame:
            payload["firstFrameMediaId"] = first_frame
        return self.call("POST", "generation/video", json=payload)

    def review(self, task_id):
        return self.call("GET", "generation/tasks/" + task_id)


def file_spec(filename, expected=None):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    content_type = CONTENT_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("仅允许常见图片或视频：" + str(path))
    if expected and not content_type.startswith(expected + "/"):
        raise SystemExit("该槽位需要{}文件：{}".format(expected, path))
    return path, content_type


def ingest(service, filename, expected=None):
    path, content_type = file_spec(filename, expected)
    ticket = service.upload_plan(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    upload_url = transfer["url"]
    if urlparse(upload_url).scheme != "https":
        raise SystemExit("素材上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as stream:
            response = requests.request(
                transfer.get("method", "PUT"),
                upload_url,
                headers=transfer.get("headers", {}),
                data=stream,
                timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    service.complete(media_id)
    print("[ingest]", path.name, "->", media_id)
    return media_id


def option_map(values):
    result = {}
    for text in values or []:
        if "=" not in text:
            raise SystemExit("--param 必须使用 key=value：" + text)
        name, value = text.split("=", 1)
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        result[name] = value
    return result


def slot_prompt(args):
    sections = [
        ("时间线槽位", args.slot),
        ("所需时长", str(args.seconds) + "秒"),
        ("前一镜末帧", args.before),
        ("后一镜首帧", args.after),
        ("本镜任务", args.task),
        ("匹配运动", args.motion),
        ("匹配色调", args.tone),
        ("字幕安全区", args.safe_zone),
        ("保护项", args.protect),
        ("补充要求", args.prompt),
    ]
    return "；".join(label + "：" + value for label, value in sections if value)


def verify_slot(args):
    if args.seconds <= 0 or args.seconds > 60:
        raise SystemExit("--seconds 必须在 0 到 60 之间")
    if not args.slot or not args.task:
        raise SystemExit("必须填写 --slot 和 --task")
    if args.kind == "broll":
        if any((args.first_frame, args.reference_image,
                args.reference_video, args.source_video)):
            raise SystemExit("broll 文生补镜不接受媒体输入")
    elif args.kind == "opener":
        if not args.first_frame:
            raise SystemExit("opener 必须提供一张 --first-frame")
        if any((args.reference_image, args.reference_video, args.source_video)):
            raise SystemExit("opener 只接受首帧")
    elif args.kind == "match":
        if not any((args.reference_image, args.reference_video)):
            raise SystemExit("match 至少需要一项相邻镜头参考")
        if args.first_frame or args.source_video:
            raise SystemExit("match 不接受首帧或编辑源视频")
    else:
        if not args.source_video:
            raise SystemExit(args.kind + " 必须提供一个 --source-video")
        if any((args.first_frame, args.reference_image, args.reference_video)):
            raise SystemExit(args.kind + " 只接受一个源视频")


def create_insert(args):
    verify_slot(args)
    service = InsertService(get_secret(args.api_key), args.verbose)
    model_id, snapshot = service.resolve(args.kind, args.routing)
    first_frame_id = None
    image_ids = []
    video_ids = []
    if args.first_frame:
        first_frame_id = ingest(service, args.first_frame, "image")
    for filename in args.reference_image or []:
        image_ids.append(ingest(service, filename, "image"))
    for filename in args.reference_video or []:
        video_ids.append(ingest(service, filename, "video"))
    if args.source_video:
        video_ids.append(ingest(service, args.source_video, "video"))
    params = option_map(args.param)
    if args.kind != "clean":
        params.setdefault("duration", args.seconds)
    if args.kind == "tail":
        params["extendDirection"] = "forward"
    response = service.insert(
        model_id,
        args.routing,
        snapshot,
        slot_prompt(args),
        params,
        image_ids,
        video_ids,
        first_frame_id,
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[insert]", args.slot, args.kind, "taskId =", task_id)
    print("[handoff] 结果是待回填素材，不包含字幕、音乐、贴纸或工程文件")
    if not args.no_download:
        wait_for_insert(service, task_id, Path(args.output_dir))


def download_clip(url, target):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with target.open("wb") as stream:
                for chunk in response.iter_content(8192):
                    if chunk:
                        stream.write(chunk)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", target)


def wait_for_insert(service, task_id, output_dir, timeout=1200):
    deadline = time.time() + timeout
    task = None
    while time.time() < deadline:
        task = service.review(task_id)
        items = task.get("items", [])
        statuses = [item.get("status", "UNKNOWN") for item in items]
        print("[review]", task_id, ",".join(statuses) or "PENDING")
        if items and all(value in ("COMPLETED", "FAILED") for value in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可用 review 命令继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            download_clip(
                item["resultUrl"],
                output_dir / "{}_{}.mp4".format(task_id, index),
            )


def review(args):
    service = InsertService(get_secret(args.api_key), args.verbose)
    print(json.dumps(service.review(args.task_id), ensure_ascii=False, indent=2))


def ingest_one(args):
    service = InsertService(get_secret(args.api_key), args.verbose)
    print(ingest(service, args.file))


def login(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    SECRET_FILE.parent.mkdir(parents=True, exist_ok=True)
    SECRET_FILE.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    SECRET_FILE.chmod(0o600)
    print("已安全写入", SECRET_FILE)


def connection_flags(parser):
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def build_cli():
    root = argparse.ArgumentParser(
        description="剪映/CapCut 时间线插槽的生成素材工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    insert = commands.add_parser("insert", help="生成一个时间线槽位素材")
    insert.add_argument("--kind", choices=CAPABILITIES, required=True)
    insert.add_argument("--slot", required=True, help="时间线位置或镜头编号")
    insert.add_argument("--seconds", required=True, type=float)
    insert.add_argument("--before", help="前一镜末帧状态")
    insert.add_argument("--after", help="后一镜首帧状态")
    insert.add_argument("--task", required=True, help="该插槽只解决的一项任务")
    insert.add_argument("--motion", help="需要匹配的运动方向和速度")
    insert.add_argument("--tone", help="需要匹配的色温和亮度")
    insert.add_argument("--safe-zone", help="字幕或平台按钮安全区")
    insert.add_argument("--protect", help="不得改变或生成的内容")
    insert.add_argument("--prompt", help="其他镜头说明")
    insert.add_argument("--first-frame")
    insert.add_argument("--reference-image", nargs="*")
    insert.add_argument("--reference-video", nargs="*")
    insert.add_argument("--source-video")
    insert.add_argument("--param", nargs="*")
    insert.add_argument(
        "--routing",
        choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    insert.add_argument("--output-dir", default=str(EXPORTS))
    insert.add_argument("--no-download", action="store_true")
    connection_flags(insert)
    insert.set_defaults(handler=create_insert)

    status = commands.add_parser("review", help="查询生成任务")
    status.add_argument("--task-id", required=True)
    connection_flags(status)
    status.set_defaults(handler=review)

    media = commands.add_parser("ingest", help="单独上传图片或视频")
    media.add_argument("--file", required=True)
    connection_flags(media)
    media.set_defaults(handler=ingest_one)

    auth = commands.add_parser("login", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=login)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
