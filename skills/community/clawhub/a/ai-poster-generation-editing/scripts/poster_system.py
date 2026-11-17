#!/usr/bin/env python3
"""用 Nano Banana Pro 创建、局部修改和适配商业海报系统。"""

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
MODEL_ID = "public_model_nano_banana_pro"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
POSTER_TYPES = (
    "product-launch", "event", "promotion", "exhibition", "recruitment",
    "livestream", "seasonal", "store-opening",
)
DIRECTIONS = (
    "product-hero", "editorial", "minimal-grid", "collage", "cinematic",
    "typographic-space", "event-system",
)
CHANNELS = (
    "taobao", "tmall", "jd", "douyin", "xiaohongshu", "wechat",
    "instagram-post", "instagram-story", "tiktok", "print", "other",
)
DATA_ZONES = {
    "logo", "title", "subtitle", "subhead", "date", "time", "location",
    "price", "offer", "cta", "legal", "qr", "sponsor", "role",
    "requirements",
}
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
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
        "或运行 poster_system.py auth --api-key sk-api-*"
    )


class PosterAPI:
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

    def pricing(self, routing):
        models = self.request("GET", "models", params={"modelType": "IMAGE"})
        model = next(
            (row for row in models if row.get("publicModelId") == MODEL_ID), None
        )
        if model is None:
            raise SystemExit("当前模型列表没有固定能力：" + MODEL_ID)
        snapshot = next(
            (row for row in model.get("pricingSnapshot", [])
             if row.get("routingMode") == routing),
            None,
        )
        if snapshot is None:
            raise SystemExit("Nano Banana Pro 不支持所选路由：" + routing)
        return snapshot

    def upload_ticket(self, path, content_type):
        return self.request(
            "POST", "media/upload-token",
            json={
                "filename": path.name, "contentType": content_type,
                "sizeBytes": path.stat().st_size,
            },
        )

    def complete_upload(self, media_id):
        self.request("POST", "media/{}/complete".format(media_id))

    def generate(self, routing, snapshot, prompt, media_ids, batch, params):
        return self.request(
            "POST", "generation/image",
            json={
                "publicModelId": MODEL_ID, "routingMode": routing,
                "prompt": prompt, "batchSize": batch,
                "imageMediaIds": media_ids, "params": params,
                "pricingSnapshot": snapshot,
            },
        )

    def task(self, task_id):
        return self.request("GET", "generation/tasks/" + task_id)


def validate_sources(images, roles):
    if len(images or []) > 8:
        raise SystemExit("最多提供 8 张素材")
    if len(images or []) != len(roles or []):
        raise SystemExit("每张素材必须对应一条职责说明")


def validate_create(args):
    validate_sources(args.art_source, args.art_role)
    unknown = [zone for zone in args.production_zone if zone not in DATA_ZONES]
    if unknown:
        raise SystemExit("未知 --production-zone：" + ", ".join(unknown))
    if len(set(args.production_zone)) < 3:
        raise SystemExit("create 至少提供 3 个不同的 --production-zone")
    if args.lock_product and (not args.subject_truth or not args.art_source):
        raise SystemExit(
            "--lock-product 必须提供 --subject-truth 和商品 --art-source"
        )
    if args.text_mode == "draft" and not args.draft_copy:
        raise SystemExit("--text-mode draft 必须提供至少一条 --draft-copy zone=text")
    if args.text_mode == "blank" and args.draft_copy:
        raise SystemExit("--text-mode blank 不接受 --draft-copy")
    if args.batch < 1 or args.batch > 2:
        raise SystemExit("--batch 必须为 1 或 2")


def parse_draft_copy(values):
    result = []
    for item in values or []:
        if "=" not in item:
            raise SystemExit("--draft-copy 必须使用 zone=text：" + item)
        zone, text = item.split("=", 1)
        if zone not in DATA_ZONES or not text:
            raise SystemExit("--draft-copy 区域或文字无效：" + item)
        result.append("{} 区候选文字『{}』".format(zone, text))
    return "；".join(result)


def create_prompt(args):
    roles = "；".join(
        "参考图{}={}".format(i, role)
        for i, role in enumerate(args.art_role, 1)
    )
    text_rule = (
        "不生成任何实际字符，只为这些数据区留出可排版空间：{}".format(
            ", ".join(args.production_zone)
        )
        if args.text_mode == "blank"
        else "低风险排版草稿：{}；所有字符交付前逐字复核".format(
            parse_draft_copy(args.draft_copy)
        )
    )
    fields = [
        ("海报编号", args.poster_id), ("海报类型", args.poster_type),
        ("美术方向", args.direction), ("渠道", args.channel),
        ("观看者", args.viewer), ("视觉命题", args.art_thesis),
        ("焦点计划", args.focal_plan), ("阅读顺序", args.reading_order),
        ("设计系统", args.design_system), ("美术素材职责", roles),
        ("主体事实", args.subject_truth), ("文字策略", text_rule),
        ("拒绝项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；建立清晰的主视觉、第一信息层、第二信息层与制作安全区；"
        "风格素材不得改变商品、展品、门店、人物、Logo或活动事实；"
        "不得虚构价格、优惠条件、日期、地点、招聘条件、认证、赞助商、二维码或品牌关系；"
        "终稿按当前渠道与印刷规则人工检查"
    )


def validate_revise(args):
    validate_sources(args.art_source, args.art_role)
    if not args.edit_instruction:
        raise SystemExit("revise 至少提供一条 --edit-instruction")
    if len(args.frozen_layer) < 3:
        raise SystemExit("revise 至少提供 3 条 --frozen-layer")
    if args.batch != 1:
        raise SystemExit("revise 的 --batch 必须为 1")


def revise_prompt(args):
    roles = "；".join(
        "补充参考图{}={}".format(i, role)
        for i, role in enumerate(args.art_role, 2)
    )
    fields = [
        ("海报编号", args.poster_id),
        ("原稿", "参考图1是待修改海报"), ("修改原因", args.reason),
        ("只允许修改", "；".join(args.edit_instruction)),
        ("冻结图层", "；".join(args.frozen_layer)), ("补充素材职责", roles),
        ("文字策略", args.text_policy), ("拒绝项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；只处理列出的修改项，未列出的主视觉、结构、配色、版式、文字区和事实不得改变；"
        "补充参考图只承担指定职责；任何生成文字都必须逐字复核"
    )


def validate_adapt(args):
    if len(args.invariant) < 3:
        raise SystemExit("adapt 至少提供 3 条 --invariant")
    if args.batch < 1 or args.batch > 2:
        raise SystemExit("--batch 必须为 1 或 2")


def adapt_prompt(args):
    fields = [
        ("海报编号", args.poster_id),
        ("原稿", "参考图1是已批准海报"),
        ("原渠道", args.source_channel), ("目标渠道", args.target_channel),
        ("目标画布", args.target_canvas),
        ("跨版式不变量", "；".join(args.invariant)),
        ("重排计划", args.reflow_plan), ("覆盖层安全区", args.overlay_safe),
        ("文字策略", args.text_policy), ("拒绝项", args.reject),
    ]
    return "；".join(label + "：" + value for label, value in fields if value) + (
        "；这是版式适配，不是拉伸、简单裁切或重新发明创意；"
        "保持批准海报的事实、品牌语言、主视觉身份和信息优先级；"
        "目标渠道的文字、UI、安全区和裁切规则须人工复核"
    )


def source_file(filename):
    path = Path(filename)
    if not path.is_file():
        raise SystemExit("图片不存在：" + str(path))
    content_type = IMAGE_TYPES.get(path.suffix.lower())
    if not content_type:
        raise SystemExit("素材必须是 PNG、JPEG、WebP 或 GIF：" + str(path))
    return path, content_type


def upload(api, filename):
    path, content_type = source_file(filename)
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
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
        result[key] = value
    return result


def submit(args, prompt, filenames):
    api = PosterAPI(load_key(args.api_key), args.verbose)
    snapshot = api.pricing(args.routing)
    media_ids = [upload(api, item) for item in filenames]
    response = api.generate(
        args.routing, snapshot, prompt, media_ids,
        args.batch, parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[poster]", args.poster_id, args.command, "taskId =", task_id)
    if not args.no_download:
        wait_and_download(api, task_id, Path(args.output_dir), args.poster_id)


def create(args):
    validate_create(args)
    submit(args, create_prompt(args), args.art_source)


def revise(args):
    validate_revise(args)
    submit(args, revise_prompt(args), [args.poster] + args.art_source)


def adapt(args):
    validate_adapt(args)
    submit(args, adapt_prompt(args), [args.poster])


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "poster"


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


def wait_and_download(api, task_id, output_dir, poster_id):
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
        raise SystemExit("任务轮询超时；可用 status 命令继续查询")
    for index, item in enumerate(task.get("items", []), 1):
        if item.get("status") == "FAILED":
            print("[failed]", item.get("errorMessage"), file=sys.stderr)
        if item.get("status") == "COMPLETED" and item.get("resultUrl"):
            safe_download(
                item["resultUrl"],
                output_dir / "{}_{}.png".format(safe_name(poster_id), index),
            )


def status(args):
    api = PosterAPI(load_key(args.api_key), args.verbose)
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


def generation_flags(parser, batch_default=1):
    parser.add_argument("--batch", type=int, default=batch_default)
    parser.add_argument("--param", nargs="*")
    parser.add_argument(
        "--routing", choices=["COST_FIRST", "SPEED_FIRST", "SUCCESS_FIRST"],
        default="COST_FIRST",
    )
    parser.add_argument("--output-dir", default=str(OUTPUT))
    parser.add_argument("--no-download", action="store_true")
    parser.add_argument("--api-key")
    parser.add_argument("--verbose", action="store_true")


def build_cli():
    root = argparse.ArgumentParser(
        description="Nano Banana Pro 商业海报创建、修改与适配工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    make = commands.add_parser("create", help="创建新海报")
    make.add_argument("--poster-id", required=True)
    make.add_argument("--poster-type", choices=POSTER_TYPES, required=True)
    make.add_argument("--direction", choices=DIRECTIONS, required=True)
    make.add_argument("--channel", choices=CHANNELS, required=True)
    make.add_argument("--lock-product", action="store_true")
    make.add_argument("--art-source", nargs="*", default=[])
    make.add_argument("--art-role", nargs="*", default=[])
    make.add_argument("--subject-truth")
    make.add_argument("--viewer", required=True)
    make.add_argument("--art-thesis", required=True)
    make.add_argument("--focal-plan", required=True)
    make.add_argument("--reading-order", required=True)
    make.add_argument("--design-system", required=True)
    make.add_argument("--production-zone", action="append", required=True)
    make.add_argument("--text-mode", choices=["blank", "draft"], default="blank")
    make.add_argument("--draft-copy", action="append", default=[])
    make.add_argument("--reject")
    generation_flags(make)
    make.set_defaults(handler=create)

    edit = commands.add_parser("revise", help="锁定大部分内容后局部修改")
    edit.add_argument("--poster-id", required=True)
    edit.add_argument("--poster", required=True)
    edit.add_argument("--reason", required=True)
    edit.add_argument("--art-source", nargs="*", default=[])
    edit.add_argument("--art-role", nargs="*", default=[])
    edit.add_argument("--edit-instruction", action="append", required=True)
    edit.add_argument("--frozen-layer", action="append", required=True)
    edit.add_argument(
        "--text-policy", choices=["preserve", "remove-to-blank"],
        default="preserve",
    )
    edit.add_argument("--reject")
    generation_flags(edit)
    edit.set_defaults(handler=revise)

    resize = commands.add_parser("adapt", help="适配已批准海报到新渠道")
    resize.add_argument("--poster-id", required=True)
    resize.add_argument("--poster", required=True)
    resize.add_argument("--source-channel", choices=CHANNELS, required=True)
    resize.add_argument("--target-channel", choices=CHANNELS, required=True)
    resize.add_argument("--target-canvas", required=True)
    resize.add_argument("--invariant", action="append", required=True)
    resize.add_argument("--reflow-plan", required=True)
    resize.add_argument("--overlay-safe", required=True)
    resize.add_argument(
        "--text-policy", choices=["preserve", "placeholders", "remove-to-blank"],
        default="placeholders",
    )
    resize.add_argument("--reject")
    generation_flags(resize)
    resize.set_defaults(handler=adapt)

    task = commands.add_parser("status", help="查询生成任务")
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
