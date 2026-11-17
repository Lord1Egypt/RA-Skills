#!/usr/bin/env python3
"""用 Seedance 2.5 逐节拍生成或保真修复电商销售视频。"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    raise SystemExit("缺少 requests，请运行 pip3 install requests")


API_ROOT = "https://ai-hive.iclip.cn/api/openapi/v1"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
I2V_MODEL = "public_model_seedance_2_5_i2v"
R2V_MODEL = "public_model_seedance_2_5_r2v"
EDIT_MODEL = "public_model_seedance_2_5_video_edit"
BEATS = ("hook", "problem", "demo", "proof", "objection", "result", "offer", "cta")
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}
VIDEO_TYPES = {
    ".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm",
}


def load_key(explicit=None):
    if explicit:
        return explicit
    if os.environ.get("AI_HIVE_API_KEY"):
        return os.environ["AI_HIVE_API_KEY"]
    try:
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        value = data.get("api_key")
        if value:
            try:
                if CONFIG.stat().st_mode & 0o077:
                    CONFIG.chmod(0o600)
            except OSError:
                pass
            return value
    except (OSError, ValueError):
        pass
    raise SystemExit(
        "缺少 AI Hive API Key。使用 --api-key、AI_HIVE_API_KEY，"
        "或运行 sales_video.py auth --api-key sk-api-*"
    )


class HiveVideo:
    def __init__(self, key, verbose=False):
        self.verbose = verbose
        self.headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        }

    def request(self, method, path, **kwargs):
        url = API_ROOT + "/" + path.lstrip("/")
        if self.verbose:
            print("[api]", method, url, file=sys.stderr)
        try:
            response = requests.request(
                method, url, headers=self.headers, timeout=30, **kwargs
            )
        except requests.RequestException as exc:
            raise SystemExit("AI Hive 请求失败：" + str(exc))
        if not response.ok:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise SystemExit(
                "AI Hive 返回错误 {}：{}".format(response.status_code, detail)
            )
        if response.status_code == 204:
            return None
        return response.json()

    def pricing(self, model_id, routing):
        models = self.request("GET", "models", params={"modelType": "VIDEO"})
        model = next(
            (row for row in models if row.get("publicModelId") == model_id), None
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + model_id)
        snapshot = next(
            (row for row in model.get("pricingSnapshot", [])
             if row.get("routingMode") == routing),
            None,
        )
        if snapshot is None:
            raise SystemExit("固定模型不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST", "media/upload-token",
            json={
                "filename": path.name,
                "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def generate(self, model_id, routing, snapshot, prompt, images, videos,
                 params, first_frame=None):
        body = {
            "publicModelId": model_id,
            "routingMode": routing,
            "prompt": prompt,
            "imageMediaIds": images,
            "videoMediaIds": videos,
            "audioMediaIds": [],
            "params": params,
            "pricingSnapshot": snapshot,
        }
        if first_frame:
            body["firstFrameMediaId"] = first_frame
        return self.request("POST", "generation/video", json=body)

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_identifier(value, flag):
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", value):
        raise SystemExit(flag + " 只能包含字母、数字、点、下划线和连字符")


def validate_product_sources(files, roles):
    if not files or len(files) > 8:
        raise SystemExit("必须提供 1 到 8 张批准的商品事实图")
    if len(files) != len(roles):
        raise SystemExit("每张 --product-source 必须对应一条 --product-role")


def validate_beat(args):
    validate_identifier(args.video_id, "--video-id")
    validate_product_sources(args.product_source, args.product_role)
    if args.total < 2 or args.total > 20:
        raise SystemExit("--total 必须在 2 到 20 之间")
    if args.position < 1 or args.position > args.total:
        raise SystemExit("--position 必须在 1 与 --total 之间")
    if args.beat == "hook" and args.position != 1:
        raise SystemExit("hook 必须是第 1 段")
    if args.beat == "cta" and args.position != args.total:
        raise SystemExit("cta 必须是最后一段")
    if args.beat in ("demo", "proof", "result") and not (
        args.claim and args.claim_source
    ):
        raise SystemExit("demo/proof/result 必须同时提供 --claim 与 --claim-source")
    if args.beat == "offer" and not (args.offer and args.offer_source):
        raise SystemExit("offer 必须同时提供 --offer 与 --offer-source")
    if len(args.continuity_lock) < 4:
        raise SystemExit("每个节拍至少提供 4 条 --continuity-lock")


def beat_prompt(args):
    roles = "；".join(
        "批准商品图{}={}".format(index, role)
        for index, role in enumerate(args.product_role, 1)
    )
    fields = [
        ("视频项目", args.video_id),
        ("节拍", "{}，第{}/{}段".format(args.beat, args.position, args.total)),
        ("发布平台", args.platform), ("目标受众", args.audience),
        ("本段销售任务", args.sales_job), ("唯一信息", args.single_message),
        ("商品事实素材", roles), ("主张", args.claim),
        ("主张批准来源", args.claim_source), ("活动内容", args.offer),
        ("活动批准来源", args.offer_source),
        ("跨段连续性锁定", "；".join(args.continuity_lock)),
        ("本段唯一动作", args.action), ("相机", args.camera),
        ("下一段交接", args.handoff_next), ("字幕与界面安全区", args.caption_safe),
        ("必须拒绝", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；一次只生成这个销售节拍，不自动补齐整条视频；"
        "商品、人物、包装、Logo、配件和活动事实只能来自批准素材；"
        "不要在画面内生成价格、参数、认证、评价、销量、功效或平台按钮；"
        "未提供的证据不得用视觉特效暗示；结尾必须形成可剪辑的稳定交接帧"
    )


def validate_repair(args):
    validate_identifier(args.video_id, "--video-id")
    validate_product_sources(args.product_source, args.product_role)
    if len(args.defect) < 1:
        raise SystemExit("repair 至少提供 1 条 --defect")
    if len(args.preserve) < 4:
        raise SystemExit("repair 至少提供 4 条 --preserve")


def repair_prompt(args):
    roles = "；".join(
        "批准商品图{}={}".format(index, role)
        for index, role in enumerate(args.product_role, 1)
    )
    fields = [
        ("视频项目", args.video_id), ("发布平台", args.platform),
        ("唯一修复目标", args.repair_goal),
        ("待修缺陷", "；".join(args.defect)),
        ("必须保持", "；".join(args.preserve)),
        ("商品事实素材", roles), ("事实批准来源", args.truth_source),
        ("必须拒绝", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；源视频是时间、动作、人物和镜头连续性的第一依据，商品事实图用于纠正局部漂移；"
        "仅修列出的缺陷，其他像素关系尽量不变；"
        "不得换SKU、换人、重构动作、延长视频、添加文案、补造卖点或借修复之名重新创作"
    )


def typed_file(filename, expected):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("素材不存在：" + str(path))
    allowed = IMAGE_TYPES if expected == "image" else VIDEO_TYPES
    content_type = allowed.get(path.suffix.lower())
    if content_type is None:
        raise SystemExit("{}素材格式不支持：{}".format(expected, path))
    return path, content_type


def upload(api, filename, expected):
    path, content_type = typed_file(filename, expected)
    ticket = api.upload_ticket(path, content_type)
    media_id = ticket["mediaId"]
    transfer = ticket["upload"]
    url = transfer["url"]
    if urlparse(url).scheme != "https":
        raise SystemExit("素材上传地址必须使用 HTTPS")
    try:
        with path.open("rb") as handle:
            response = requests.request(
                transfer.get("method", "PUT"), url,
                headers=transfer.get("headers", {}), data=handle, timeout=300,
            )
    except requests.RequestException as exc:
        raise SystemExit("素材上传失败：" + str(exc))
    if not response.ok:
        raise SystemExit(
            "素材上传失败 {}：{}".format(response.status_code, response.text)
        )
    api.complete_upload(media_id)
    print("[source]", path.name, "->", media_id)
    return media_id


def parse_params(values):
    result = {}
    for item in values or []:
        if "=" not in item:
            raise SystemExit("--param 必须使用 key=value：" + item)
        key, value = item.split("=", 1)
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
        result[key] = value
    return result


def preview(model_id, prompt, images, videos, params, first_frame=None):
    print(json.dumps({
        "publicModelId": model_id,
        "prompt": prompt,
        "productSources": images,
        "videoSources": videos,
        "firstFrame": first_frame,
        "params": params,
    }, ensure_ascii=False, indent=2))


def submit_beat(args):
    validate_beat(args)
    prompt = beat_prompt(args)
    params = parse_params(args.param)
    model_id = R2V_MODEL if args.motion_reference else I2V_MODEL
    if args.preview:
        preview(
            model_id, prompt, args.product_source,
            [args.motion_reference] if args.motion_reference else [], params,
            None if args.motion_reference else args.product_source[0],
        )
        return
    api = HiveVideo(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(model_id, args.routing)
    image_ids = [upload(api, item, "image") for item in args.product_source]
    if args.motion_reference:
        video_ids = [upload(api, args.motion_reference, "video")]
        first_frame = None
        request_images = image_ids
    else:
        video_ids = []
        first_frame = image_ids[0]
        request_images = image_ids[1:]
    response = api.generate(
        model_id, args.routing, snapshot, prompt, request_images, video_ids,
        params, first_frame=first_frame,
    )
    handle_response(
        api, response, args, "{:02d}-{}".format(args.position, args.beat)
    )


def submit_repair(args):
    validate_repair(args)
    prompt = repair_prompt(args)
    params = parse_params(args.param)
    if args.preview:
        preview(
            EDIT_MODEL, prompt, args.product_source, [args.source_video], params
        )
        return
    api = HiveVideo(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(EDIT_MODEL, args.routing)
    image_ids = [upload(api, item, "image") for item in args.product_source]
    source_id = upload(api, args.source_video, "video")
    response = api.generate(
        EDIT_MODEL, args.routing, snapshot, prompt, image_ids, [source_id], params
    )
    handle_response(api, response, args, "repair")


def handle_response(api, response, args, label):
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[sales-video]", args.video_id, label, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(
            api, task_id, Path(args.output_dir), args.video_id, label
        )


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "video"


def safe_download(url, destination):
    if urlparse(url).scheme != "https":
        raise SystemExit("结果下载地址必须使用 HTTPS")
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300) as response:
            response.raise_for_status()
            with destination.open("wb") as handle:
                for chunk in response.iter_content(8192):
                    if chunk:
                        handle.write(chunk)
    except requests.RequestException as exc:
        raise SystemExit("结果下载失败：" + str(exc))
    print("[saved]", destination)


def wait_and_download(api, task_id, output_dir, video_id, label):
    deadline = time.time() + 1200
    task = None
    while time.time() < deadline:
        task = api.task(task_id)
        items = task.get("items", [])
        statuses = [item.get("status", "UNKNOWN") for item in items]
        print("[task]", task_id, ",".join(statuses) or "PENDING")
        if items and all(value in ("COMPLETED", "FAILED") for value in statuses):
            break
        time.sleep(3)
    else:
        raise SystemExit("任务轮询超时；可用 status 命令继续查询原 taskId")
    prefix = "{}-{}".format(safe_name(video_id), safe_name(label))
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"], output_dir / "{}-{}.mp4".format(prefix, index)
            )


def status(args):
    api = HiveVideo(load_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def auth(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG.chmod(0o600)
    print("已安全写入", CONFIG)


def common_generation_flags(parser):
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--param", action="append")
    parser.add_argument(
        "--routing", choices=("COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"),
        default="COST_FIRST",
    )
    parser.add_argument("--output-dir", default=str(OUTPUT))
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def product_flags(parser):
    parser.add_argument("--product-source", nargs="+", required=True)
    parser.add_argument("--product-role", nargs="+", required=True)


def build_cli():
    root = argparse.ArgumentParser(
        description="Seedance 2.5 电商销售视频节拍生成与保真修复"
    )
    commands = root.add_subparsers(dest="command", required=True)

    beat = commands.add_parser("beat", help="生成一个可验收的销售节拍")
    beat.add_argument("--video-id", required=True)
    beat.add_argument("--beat", choices=BEATS, required=True)
    beat.add_argument("--position", type=int, required=True)
    beat.add_argument("--total", type=int, required=True)
    beat.add_argument("--platform", required=True)
    beat.add_argument("--audience", required=True)
    beat.add_argument("--sales-job", required=True)
    beat.add_argument("--single-message", required=True)
    product_flags(beat)
    beat.add_argument("--claim")
    beat.add_argument("--claim-source")
    beat.add_argument("--offer")
    beat.add_argument("--offer-source")
    beat.add_argument("--continuity-lock", action="append", required=True)
    beat.add_argument("--action", required=True)
    beat.add_argument("--camera", required=True)
    beat.add_argument("--handoff-next", required=True)
    beat.add_argument("--caption-safe", required=True)
    beat.add_argument("--reject")
    beat.add_argument("--motion-reference")
    common_generation_flags(beat)
    beat.set_defaults(handler=submit_beat)

    repair = commands.add_parser("repair", help="保留事实，仅修复指定视频缺陷")
    repair.add_argument("--video-id", required=True)
    repair.add_argument("--source-video", required=True)
    repair.add_argument("--platform", required=True)
    repair.add_argument("--repair-goal", required=True)
    repair.add_argument("--defect", action="append", required=True)
    repair.add_argument("--preserve", action="append", required=True)
    product_flags(repair)
    repair.add_argument("--truth-source", required=True)
    repair.add_argument("--reject")
    common_generation_flags(repair)
    repair.set_defaults(handler=submit_repair)

    task = commands.add_parser("status", help="查询原生成任务")
    task.add_argument("--task-id", required=True)
    task.add_argument("--api-key")
    task.add_argument("--verbose", action="store_true")
    task.set_defaults(handler=status)

    save = commands.add_parser("auth", help="保存 AI Hive API Key")
    save.add_argument("--api-key", required=True)
    save.set_defaults(handler=auth)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
