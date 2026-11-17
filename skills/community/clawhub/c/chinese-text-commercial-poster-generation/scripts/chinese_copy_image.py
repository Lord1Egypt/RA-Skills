#!/usr/bin/env python3
"""用 GPT Image 2 执行结构化商业文案合同、返修与离线字符审计。"""

import argparse
import difflib
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
MODEL_ID = "public_model_gpt_image_2"
CONFIG = Path.home() / ".ai-hive" / "config.json"
OUTPUT = Path.home() / "Downloads" / "AiHive"
PLATFORMS = (
    "taobao", "tmall", "jd", "pinduoduo", "douyin", "xiaohongshu",
    "wechat", "amazon", "tiktok-shop", "instagram", "shopify", "other",
)
ASSETS = (
    "ecommerce-card", "product-feature", "campaign-kv", "social-cover",
    "event-poster", "localized-ad", "menu-board", "package-front",
)
PRODUCT_ASSETS = {"ecommerce-card", "product-feature", "package-front"}
ZONES = {
    "headline", "subhead", "kicker", "badge", "date", "time", "location",
    "price", "cta", "disclaimer", "label",
}
IMAGE_TYPES = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
}


def load_key(explicit=None):
    if explicit:
        return explicit
    environment = os.environ.get("AI_HIVE_API_KEY")
    if environment:
        return environment
    try:
        saved = json.loads(CONFIG.read_text(encoding="utf-8"))
        value = saved.get("api_key")
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
        "或运行 chinese_copy_image.py auth --api-key sk-api-*"
    )


class CopyImageAPI:
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

    def price(self, routing):
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
            raise SystemExit("GPT Image 2 不支持所选路由：" + routing)
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


def parse_zone_items(values, flag):
    result = []
    seen = set()
    for item in values or []:
        if "=" not in item:
            raise SystemExit("{} 必须使用 zone=逐字内容：{}".format(flag, item))
        zone, text = item.split("=", 1)
        zone = zone.strip().lower()
        if zone not in ZONES and not re.fullmatch(r"custom-[a-z0-9-]+", zone):
            raise SystemExit("未知文字区域：" + zone)
        if not text:
            raise SystemExit("{} 的文字不能为空".format(zone))
        if zone in seen:
            raise SystemExit("同一命令中区域不能重复：" + zone)
        seen.add(zone)
        result.append((zone, text))
    return result


def validate_contract(args, repairing=False):
    copies = parse_zone_items(args.copy, "--copy")
    if not copies:
        raise SystemExit("至少提供一条 --copy zone=逐字内容")
    if len(copies) > 12 or sum(len(text) for _, text in copies) > 500:
        raise SystemExit("文案合同最多 12 段且总计不超过 500 个字符")
    if not args.copy_source.strip():
        raise SystemExit("--copy-source 不能为空")
    if args.source_image and len(args.source_image) > 6:
        raise SystemExit("最多提供 6 张 --source-image")
    if len(args.source_role or []) != len(args.source_image or []):
        raise SystemExit("每张 --source-image 必须对应一条 --source-role")
    if args.asset in PRODUCT_ASSETS and (
        not args.product_record or not args.source_image
    ):
        raise SystemExit(
            "商品类素材必须提供 --product-record 和至少一张 --source-image"
        )
    if args.batch < 1 or args.batch > 2:
        raise SystemExit("--batch 必须为 1 或 2")
    if repairing and not args.observed_error:
        raise SystemExit("repair 至少提供一条 --observed-error")
    return copies


def copy_contract_text(copies):
    return "；".join(
        "{} 区域必须逐字呈现『{}』".format(zone, text)
        for zone, text in copies
    )


def reference_text(roles, offset=1):
    return "；".join(
        "参考图{}={}".format(index, role)
        for index, role in enumerate(roles or [], offset)
    )


def build_prompt(args, copies, repairing=False):
    forbidden = "；".join("不得出现『{}』".format(x) for x in args.forbid_copy)
    source_roles = reference_text(args.source_role, 2 if repairing else 1)
    fields = [
        ("项目", args.project), ("渠道", args.platform), ("资产类型", args.asset),
        ("文案批准来源", args.copy_source),
        ("文案合同", copy_contract_text(copies)),
        ("参考图职责", source_roles), ("商品事实记录", args.product_record),
        ("视觉简报", args.visual_brief), ("版式计划", args.layout_plan),
        ("品牌规则", args.brand_rules), ("禁用文案", forbidden),
        ("禁用元素", args.forbid_element),
    ]
    if repairing:
        fields.insert(4, (
            "待修复底稿",
            "参考图1是待修复图片；保持未报错文字、主体、背景、色彩、版式与位置",
        ))
        fields.insert(5, ("已观察错误", "；".join(args.observed_error)))
    ending = (
        "；只修复已观察错误，不重写未报错区域；修复后再次严格执行完整文案合同"
        if repairing
        else "；按指定层级和区域排版，不增删、改写、翻译、重复或补充任何字符"
    )
    return "；".join(label + "：" + value for label, value in fields if value) + (
        ending
        + "；禁止装饰性伪文字；字符、数字、空格、大小写、标点与顺序都属于不可变数据；"
        + "结果必须由人工逐字校对，价格、法律、规格、二维码和包装强制信息不能仅靠模型定稿"
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


def submit(args, repairing=False):
    copies = validate_contract(args, repairing)
    api = CopyImageAPI(load_key(args.api_key), args.verbose)
    snapshot = api.price(args.routing)
    files = ([args.draft] if repairing else []) + list(args.source_image or [])
    media_ids = [upload(api, filename) for filename in files]
    response = api.generate(
        args.routing, snapshot, build_prompt(args, copies, repairing),
        media_ids, args.batch, parse_params(args.param),
    )
    task_id = response.get("taskId")
    if not task_id:
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return
    print("[copy-image]", args.project, args.asset, "taskId =", task_id)
    print("[proof-required] 生成文字必须逐字符人工核对")
    if not args.no_download:
        wait_and_download(api, task_id, Path(args.output_dir), args.project)


def compose(args):
    submit(args, False)


def repair(args):
    submit(args, True)


def preview(args):
    copies = validate_contract(args, bool(getattr(args, "draft", None)))
    print(build_prompt(args, copies, bool(getattr(args, "draft", None))))


def audit(args):
    expected = dict(parse_zone_items(args.expected, "--expected"))
    observed = dict(parse_zone_items(args.observed, "--observed"))
    zones = list(expected)
    extra = [zone for zone in observed if zone not in expected]
    results = []
    passed = True
    for zone in zones:
        want = expected[zone]
        got = observed.get(zone)
        exact = got == want
        passed = passed and exact
        results.append({
            "zone": zone, "exact": exact, "expected": want, "observed": got,
            "diff": "" if exact else " ".join(
                difflib.ndiff(want, got or "")
            ),
        })
    for zone in extra:
        passed = False
        results.append({
            "zone": zone, "exact": False, "expected": None,
            "observed": observed[zone], "diff": "unexpected zone",
        })
    print(json.dumps({"passed": passed, "results": results}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if passed else 2)


def safe_name(value):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-") or "copy-image"


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


def wait_and_download(api, task_id, output_dir, project):
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
                output_dir / "{}_{}.png".format(safe_name(project), index),
            )


def show_status(args):
    api = CopyImageAPI(load_key(args.api_key), args.verbose)
    print(json.dumps(api.task(args.task_id), ensure_ascii=False, indent=2))


def save_key(args):
    if not args.api_key.startswith("sk-api-") or len(args.api_key) < 20:
        raise SystemExit("API Key 格式错误，应为完整的 sk-api-*")
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(
        json.dumps({"api_key": args.api_key}, indent=2), encoding="utf-8"
    )
    CONFIG.chmod(0o600)
    print("已安全写入", CONFIG)


def contract_flags(parser):
    parser.add_argument("--project", required=True)
    parser.add_argument("--platform", choices=PLATFORMS, required=True)
    parser.add_argument("--asset", choices=ASSETS, required=True)
    parser.add_argument("--copy-source", required=True)
    parser.add_argument("--copy", action="append", default=[])
    parser.add_argument("--source-image", nargs="*", default=[])
    parser.add_argument("--source-role", nargs="*", default=[])
    parser.add_argument("--product-record")
    parser.add_argument("--visual-brief", required=True)
    parser.add_argument("--layout-plan", required=True)
    parser.add_argument("--brand-rules")
    parser.add_argument("--forbid-copy", action="append", default=[])
    parser.add_argument("--forbid-element")
    parser.add_argument("--batch", type=int, default=1)


def generation_flags(parser):
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
        description="GPT Image 2 精准中文商业文字图片工具"
    )
    commands = root.add_subparsers(dest="command", required=True)

    make = commands.add_parser("compose", help="按文案合同生成商业图片")
    contract_flags(make)
    generation_flags(make)
    make.set_defaults(handler=compose)

    fix = commands.add_parser("repair", help="按错误清单局部返修文字")
    contract_flags(fix)
    fix.add_argument("--draft", required=True)
    fix.add_argument("--observed-error", action="append", default=[])
    generation_flags(fix)
    fix.set_defaults(handler=repair)

    check = commands.add_parser("audit", help="离线逐字符比较预期与观察文本")
    check.add_argument("--expected", action="append", required=True)
    check.add_argument("--observed", action="append", required=True)
    check.set_defaults(handler=audit)

    status = commands.add_parser("status", help="查询生成任务")
    status.add_argument("--task-id", required=True)
    status.add_argument("--api-key")
    status.add_argument("--verbose", action="store_true")
    status.set_defaults(handler=show_status)

    auth = commands.add_parser("auth", help="保存 AI Hive API Key")
    auth.add_argument("--api-key", required=True)
    auth.set_defaults(handler=save_key)
    return root


def main():
    args = build_cli().parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()
