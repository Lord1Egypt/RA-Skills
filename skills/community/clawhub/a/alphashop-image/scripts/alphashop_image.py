#!/usr/bin/env python3
"""
AlphaShop Image API — unified CLI for all 11 image processing endpoints.

Usage:
  python alphashop_image.py <command> [options]

Commands (sync):
  translate          图片翻译
  translate-pro      图片翻译PRO（支持auto语种识别）
  enlarge            图片高清放大
  extract-object     图片主题抠图
  detect-elements    图片元素识别
  remove-elements    图片元素智能消除
  crop               图像裁剪

Commands (async — submit + query):
  virtual-try-on     创建虚拟试衣任务
  query-try-on       查询虚拟试衣结果
  change-model       创建模特换肤任务
  query-change-model 查询模特换肤结果

Auth: env ALPHASHOP_ACCESS_KEY / ALPHASHOP_SECRET_KEY (JWT HS256).
"""
import sys
import os
import json
import time
import argparse
import requests
import jwt

BASE_URL = "https://api.alphashop.cn"


# ── Auth ─────────────────────────────────────────────────────────────────────

def get_token():
    ak = os.environ.get("ALPHASHOP_ACCESS_KEY", "").strip()
    sk = os.environ.get("ALPHASHOP_SECRET_KEY", "").strip()
    if not ak or not sk:
        print("Error: Set ALPHASHOP_ACCESS_KEY and ALPHASHOP_SECRET_KEY env vars.", file=sys.stderr)
        sys.exit(1)
    now = int(time.time())
    token = jwt.encode({"iss": ak, "exp": now + 1800, "nbf": now - 5}, sk, algorithm="HS256", headers={"alg": "HS256"})
    return token if isinstance(token, str) else token.decode("utf-8")


def call_api(path: str, body: dict) -> dict:
    """POST to AlphaShop API, return parsed JSON response."""
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {get_token()}"}
    try:
        r = requests.post(url, json=body, headers=headers, timeout=120)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        try:
            print(f"Response: {r.text}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except Exception as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_translate(args):
    body = {"imageUrl": args.image_url, "sourceLanguage": args.source_lang, "targetLanguage": args.target_lang}
    if args.include_product_area:
        body["includingProductArea"] = True
    if args.use_editor:
        body["useImageEditor"] = True
    if args.translate_brand:
        body["translatingBrandInTheProduct"] = True
    print(json.dumps(call_api("/ai.image.translateImage/1.0", body), ensure_ascii=False, indent=2))


def cmd_translate_pro(args):
    body = {"imageUrl": args.image_url, "sourceLanguage": args.source_lang, "targetLanguage": args.target_lang}
    if args.include_product_area:
        body["includingProductArea"] = True
    if args.use_editor:
        body["useImageEditor"] = True
    if args.translate_brand:
        body["translatingBrandInTheProduct"] = True
    print(json.dumps(call_api("/ai.image.translateImagePro/1.0", body), ensure_ascii=False, indent=2))


def cmd_enlarge(args):
    body = {"imageUrl": args.image_url}
    if args.factor:
        body["upscaleFactor"] = args.factor
    print(json.dumps(call_api("/ai.image.imageEnlargement/1.0", body), ensure_ascii=False, indent=2))


def cmd_extract_object(args):
    body = {"imageUrl": args.image_url, "transparentFlag": args.transparent}
    if args.target_width:
        body["targetWidth"] = args.target_width
    if args.target_height:
        body["targetHeight"] = args.target_height
    if args.bg_color:
        body["bgColor"] = args.bg_color
    print(json.dumps(call_api("/ai.image.imageObjectExtraction/1.0", body), ensure_ascii=False, indent=2))


def cmd_detect_elements(args):
    body = {"imageUrl": args.image_url}
    if args.object_elements:
        body["objectDetectElements"] = args.object_elements
    if args.non_object_elements:
        body["nonObjectDetectElements"] = args.non_object_elements
    if args.return_character:
        body["returnCharacter"] = 1
    if args.return_border_pixel:
        body["returnBorderPixel"] = 1
    if args.return_product_prop:
        body["returnProductProp"] = 1
    if args.return_product_num:
        body["returnProductNum"] = 1
    if args.return_character_prop:
        body["returnCharacterProp"] = 1
    print(json.dumps(call_api("/ai.image.imageElementDetect/1.0", body), ensure_ascii=False, indent=2))


def cmd_remove_elements(args):
    body = {"imageUrl": args.image_url}
    flag_map = {
        "obj_watermark": "objRemoveWatermark",
        "obj_character": "objRemoveCharacter",
        "obj_logo": "objRemoveLogo",
        "obj_npx": "objRemoveNpx",
        "obj_qrcode": "objRemoveQrcode",
        "noobj_watermark": "noobjRemoveWatermark",
        "noobj_character": "noobjRemoveCharacter",
        "noobj_logo": "noobjRemoveLogo",
        "noobj_npx": "noobjRemoveNpx",
        "noobj_qrcode": "noobjRemoveQrcode",
    }
    for attr, key in flag_map.items():
        val = getattr(args, attr, None)
        if val:
            body[key] = val
    print(json.dumps(call_api("/ai.image.imageElementRemove/1.0", body), ensure_ascii=False, indent=2))


def cmd_crop(args):
    body = {"imageUrl": args.image_url}
    if args.target_width:
        body["targetWidth"] = args.target_width
    if args.target_height:
        body["targetHeight"] = args.target_height
    print(json.dumps(call_api("/ai.image.imageCut/1.0", body), ensure_ascii=False, indent=2))


def cmd_virtual_try_on(args):
    clothes_list = []
    for item in args.clothes:
        parts = item.split(",", 1)
        if len(parts) != 2:
            print(f"Error: --clothes format is 'URL,TYPE' (type: tops/bottoms/dresses). Got: {item}", file=sys.stderr)
            sys.exit(1)
        clothes_list.append({"imageUrl": parts[0].strip(), "type": parts[1].strip()})
    body = {"clothesInfoList": clothes_list, "generateCount": args.count}
    if args.model_images:
        body["modelImageList"] = args.model_images
    else:
        body["modelImageList"] = []
    print(json.dumps(call_api("/ai.image.submitVirtualModelTask/1.0", body), ensure_ascii=False, indent=2))


def cmd_query_try_on(args):
    print(json.dumps(call_api("/ai.image.queryImageGenerateVirtualModelTask/1.0", {"taskId": args.task_id}), ensure_ascii=False, indent=2))


def cmd_change_model(args):
    body = {
        "imageUrl": args.image_url,
        "model": args.model_type,
        "bgStyle": args.bg_style,
        "age": args.age,
        "gender": args.gender,
        "imageNum": args.num,
    }
    if args.keep_bg is not None:
        body["maskKeepBg"] = args.keep_bg
    print(json.dumps(call_api("/ai.image.submitImageChangeModelTask/1.0", body), ensure_ascii=False, indent=2))


def cmd_query_change_model(args):
    print(json.dumps(call_api("/ai.image.queryImageChangeModelTask/1.0", {"taskId": args.task_id}), ensure_ascii=False, indent=2))


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AlphaShop Image API CLI")
    sub = parser.add_subparsers(dest="command")
    sub.required = True

    # -- translate --
    p = sub.add_parser("translate", help="图片翻译")
    p.add_argument("--image-url", required=True, help="原图URL")
    p.add_argument("--source-lang", required=True, help="源语种 ISO code")
    p.add_argument("--target-lang", required=True, help="目标语种 ISO code")
    p.add_argument("--include-product-area", action="store_true", help="翻译商品主体上文字")
    p.add_argument("--use-editor", action="store_true", help="使用图翻编辑器协议")
    p.add_argument("--translate-brand", action="store_true", help="翻译品牌上文字")
    p.set_defaults(func=cmd_translate)

    # -- translate-pro --
    p = sub.add_parser("translate-pro", help="图片翻译PRO（支持auto源语种）")
    p.add_argument("--image-url", required=True, help="原图URL")
    p.add_argument("--source-lang", required=True, help="源语种（支持auto自动识别9种语言）")
    p.add_argument("--target-lang", required=True, help="目标语种 ISO code")
    p.add_argument("--include-product-area", action="store_true", help="翻译商品主体上文字")
    p.add_argument("--use-editor", action="store_true", help="使用图翻编辑器协议")
    p.add_argument("--translate-brand", action="store_true", help="翻译品牌上文字")
    p.set_defaults(func=cmd_translate_pro)

    # -- enlarge --
    p = sub.add_parser("enlarge", help="图片高清放大")
    p.add_argument("--image-url", required=True, help="图片URL（100×100~3000×3000）")
    p.add_argument("--factor", type=int, choices=[2, 3, 4], help="放大倍数（默认2）")
    p.set_defaults(func=cmd_enlarge)

    # -- extract-object --
    p = sub.add_parser("extract-object", help="图片主题抠图")
    p.add_argument("--image-url", required=True, help="图片URL")
    p.add_argument("--transparent", type=lambda x: x.lower() == "true", required=True, help="透明底 true/false")
    p.add_argument("--target-width", type=int, help="目标宽度")
    p.add_argument("--target-height", type=int, help="目标高度")
    p.add_argument("--bg-color", help="背景BGR色彩值，如 '255,255,255'")
    p.set_defaults(func=cmd_extract_object)

    # -- detect-elements --
    p = sub.add_parser("detect-elements", help="图片元素识别")
    p.add_argument("--image-url", required=True, help="图片URL")
    p.add_argument("--object-elements", type=int, nargs="+", help="主体检测元素 1=水印 2=Logo 3=文字 4=含字色块")
    p.add_argument("--non-object-elements", type=int, nargs="+", help="非主体检测元素（同上）")
    p.add_argument("--return-character", action="store_true", help="返回OCR文字")
    p.add_argument("--return-border-pixel", action="store_true", help="返回主体边缘距离")
    p.add_argument("--return-product-prop", action="store_true", help="返回主体面积占比")
    p.add_argument("--return-product-num", action="store_true", help="返回主体数量")
    p.add_argument("--return-character-prop", action="store_true", help="返回文字占比")
    p.set_defaults(func=cmd_detect_elements)

    # -- remove-elements --
    p = sub.add_parser("remove-elements", help="图片元素智能消除")
    p.add_argument("--image-url", required=True, help="图片URL（JPG/JPEG/PNG/BMP，256×256~3000×3000，≤10MB）")
    p.add_argument("--obj-watermark", type=int, help="主体消除水印")
    p.add_argument("--obj-character", type=int, help="主体消除文字")
    p.add_argument("--obj-logo", type=int, help="主体消除logo")
    p.add_argument("--obj-npx", type=int, help="主体消除牛皮癣")
    p.add_argument("--obj-qrcode", type=int, help="主体消除二维码")
    p.add_argument("--noobj-watermark", type=int, help="非主体消除水印")
    p.add_argument("--noobj-character", type=int, help="非主体消除文字")
    p.add_argument("--noobj-logo", type=int, help="非主体消除Logo")
    p.add_argument("--noobj-npx", type=int, help="非主体消除牛皮癣")
    p.add_argument("--noobj-qrcode", type=int, help="非主体消除二维码")
    p.set_defaults(func=cmd_remove_elements)

    # -- crop --
    p = sub.add_parser("crop", help="图像裁剪")
    p.add_argument("--image-url", required=True, help="图片URL")
    p.add_argument("--target-width", type=int, help="目标宽度")
    p.add_argument("--target-height", type=int, help="目标高度")
    p.set_defaults(func=cmd_crop)

    # -- virtual-try-on --
    p = sub.add_parser("virtual-try-on", help="创建虚拟试衣任务")
    p.add_argument("--model-images", nargs="*", help="模特图URL列表（最多8张，不传则生成随机模特）")
    p.add_argument("--clothes", nargs="+", required=True, help="服饰，格式: 'URL,TYPE'（TYPE: tops/bottoms/dresses）")
    p.add_argument("--count", type=int, required=True, help="生成图片数量")
    p.set_defaults(func=cmd_virtual_try_on)

    # -- query-try-on --
    p = sub.add_parser("query-try-on", help="查询虚拟试衣任务结果")
    p.add_argument("--task-id", required=True, help="任务ID")
    p.set_defaults(func=cmd_query_try_on)

    # -- change-model --
    p = sub.add_parser("change-model", help="创建模特换肤任务")
    p.add_argument("--image-url", required=True, help="图片URL")
    p.add_argument("--model-type", required=True, choices=["YELLOW", "BLACK", "WHITE", "BROWN"], help="模特类型")
    p.add_argument("--bg-style", required=True, choices=["NATURE", "URBAN", "INDOOR"], help="背景风格")
    p.add_argument("--age", required=True, choices=["YOUTH", "MIDDLE_AGE", "OLD_AGE"], help="年龄段")
    p.add_argument("--gender", required=True, choices=["MALE", "FEMALE"], help="性别")
    p.add_argument("--num", type=int, required=True, help="生成图片张数")
    p.add_argument("--keep-bg", type=lambda x: x.lower() == "true", default=None, help="保留背景 true/false（默认true）")
    p.set_defaults(func=cmd_change_model)

    # -- query-change-model --
    p = sub.add_parser("query-change-model", help="查询模特换肤任务结果")
    p.add_argument("--task-id", required=True, help="任务ID")
    p.set_defaults(func=cmd_query_change_model)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
