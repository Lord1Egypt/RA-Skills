"""命令行入口：argparse 与子命令分发。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from .client import EqxiuAigcClient
from .config_store import check_auth_status, load_config, login_interactive, token_from_config
from .constants import (
    CONFIG_PATH,
    DEFAULT_BASE_URL,
    DEFAULT_COS_BUCKET,
    DEFAULT_COS_PREFIX,
    DEFAULT_MATERIAL_SOURCE,
    DEFAULT_PRODUCT_CODE_SUB,
    EQXIU_COS_TOKEN_API_BASE,
    EQXIU_MATERIAL_API_BASE,
)
from .errors import EqxiuAigcApiError
from .upload_material import CosClientError, CosServiceError, upload_local_material


def load_json_arg(s: str) -> Any:
    return json.loads(s)


def main() -> int:
    parser = argparse.ArgumentParser(description="易企秀 AIGC HTTP API 客户端")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API 根地址（默认来自环境变量 EQXIU_AIGC_API_BASE 或 {DEFAULT_BASE_URL!r}）",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="请求超时秒数",
    )
    parser.add_argument(
        "--access-token",
        default=None,
        help=f"X-Openclaw-Token（默认从 {CONFIG_PATH} 读取）",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("login", help="交互式登录，保存 X-Openclaw-Token")

    p_create = sub.add_parser(
        "create",
        help="POST /aigc/draw/ai/create/stream 流式一键生成 H5（推荐）",
    )
    p_create.add_argument(
        "--prompt",
        required=True,
        help="用户需求描述，对应接口 userPrompt",
    )
    p_create.add_argument(
        "--product-code-sub",
        default=DEFAULT_PRODUCT_CODE_SUB,
        help=f"产品子码 productCodeSub（默认 {DEFAULT_PRODUCT_CODE_SUB!r}）",
    )

    p_auth = sub.add_parser("auth", help="认证相关命令")
    auth_sub = p_auth.add_subparsers(dest="auth_cmd", required=True)
    auth_sub.add_parser("status", help="验证 token 是否有效")

    p_et = sub.add_parser(
        "editable-text",
        help="GET /iaigc/h5_scene/get_editable_text 获取作品可编辑文本",
    )
    p_et.add_argument("--scene-id", type=int, required=True, help="作品 id（create 返回的 data.id）")

    p_ut = sub.add_parser(
        "update-text",
        help="POST /iaigc/h5_scene/update_editable_text 更新可编辑文本并发布",
    )
    p_ut.add_argument("--scene-id", type=int, required=True)
    p_ut.add_argument("--page-id", type=int, required=True)
    p_ut.add_argument("--element-id", type=int, required=True)
    p_ut.add_argument("--content", required=True, help="更新后的文案")
    p_ut.add_argument("--css-json", default=None, help='可选，元素 css JSON，如 \'{"fontSize":"32"}\'')
    p_ut.add_argument("--preview-url", default=None, help="可选，修正后原样回传到输出 JSON")

    p_bi = sub.add_parser("body-images", help="GET /iaigc/h5_scene/get_body_images 查询正文配图")
    p_bi.add_argument("--scene-id", type=int, required=True)
    p_bi.add_argument("--page-id", type=int, default=None)

    p_rb = sub.add_parser("replace-body-image", help="POST /iaigc/h5_scene/replace_body_image 换正文配图")
    p_rb.add_argument("--scene-id", type=int, required=True)
    p_rb.add_argument("--page-id", type=int, required=True)
    p_rb.add_argument("--element-id", required=True, help="正文配图元素 id")
    p_rb.add_argument("--src", required=True, help="新图 src 或素材 path")
    p_rb.add_argument("--source-id", default=None, help="可选，写入 properties.sourceId")

    p_up = sub.add_parser(
        "upload",
        help="COS 上传后登记易企秀素材库",
    )
    p_up.add_argument("--file", type=str, required=True, help="本地文件路径")
    p_up.add_argument("--bucket", type=str, default=DEFAULT_COS_BUCKET, help=f"业务 bucket（默认 {DEFAULT_COS_BUCKET}）")
    p_up.add_argument(
        "--prefix",
        type=str,
        default=DEFAULT_COS_PREFIX,
        help=f"与 token-upload 一致的 prefix（默认 {DEFAULT_COS_PREFIX!r}）",
    )
    p_up.add_argument("--name", type=str, default=None, help="COS 对象名；默认使用本地文件 basename")
    p_up.add_argument("--tmb-path", type=str, default=None, help="saveFile 的 tmbPath；默认与 COS key 相同")
    p_up.add_argument(
        "--source",
        type=str,
        default=DEFAULT_MATERIAL_SOURCE,
        help=f"saveFile 的 source（默认 {DEFAULT_MATERIAL_SOURCE!r}，可用环境变量 EQXIU_MATERIAL_SOURCE）",
    )
    p_up.add_argument("--tag-id", type=int, default=-1, help="saveFile 的 tagId（默认 -1）")
    p_up.add_argument("--file-type", type=int, default=1, help="saveFile 的 fileType（默认 1 图片）")
    p_up.add_argument(
        "--cos-api-base",
        type=str,
        default=EQXIU_COS_TOKEN_API_BASE,
        help=f"COS 凭证接口根（默认 {EQXIU_COS_TOKEN_API_BASE}）",
    )
    p_up.add_argument(
        "--material-api-base",
        type=str,
        default=EQXIU_MATERIAL_API_BASE,
        help=f"素材 saveFile 接口根（默认 {EQXIU_MATERIAL_API_BASE}）",
    )

    p_ml = sub.add_parser(
        "material-list",
        help="GET material-api …/m/material/user/upload/list2 查询当前用户上传素材",
    )
    p_ml.add_argument("--file-type", type=int, default=1, help="文件类型，1 一般为图片（默认 1）")
    p_ml.add_argument("--page-no", type=int, default=1, dest="page_no")
    p_ml.add_argument("--page-size", type=int, default=30, dest="page_size")
    p_ml.add_argument("--tag-id", type=int, default=-1, dest="tag_id")
    p_ml.add_argument(
        "--material-api-base",
        type=str,
        default=EQXIU_MATERIAL_API_BASE,
        help=f"素材接口根（默认 {EQXIU_MATERIAL_API_BASE}）",
    )

    args = parser.parse_args()
    cfg = load_config()
    token = (args.access_token or "").strip() or token_from_config(cfg)

    if args.cmd == "login":
        return login_interactive()

    try:
        if args.cmd == "auth":
            if args.auth_cmd != "status":
                print("未知 auth 子命令", file=sys.stderr)
                return 2
            if not token:
                print("缺少 X-Openclaw-Token：请先执行 login 或传 --access-token", file=sys.stderr)
                return 1
            out = check_auth_status(token, args.timeout)
        else:
            client = EqxiuAigcClient(base_url=args.base_url, timeout=args.timeout, access_token=token or None)
            if args.cmd == "create":
                if not token:
                    print(
                        "缺少 X-Openclaw-Token：请先执行 login 或传 --access-token",
                        file=sys.stderr,
                    )
                    return 1
                progress: list[str] = []

                def _on_progress(msg: str, _payload: Dict[str, Any]) -> None:
                    progress.append(msg)
                    print(msg, file=sys.stdout)

                data = client.create_h5_stream(
                    args.prompt,
                    product_code_sub=args.product_code_sub,
                    on_progress=_on_progress,
                )
                out = {
                    "success": True,
                    "progress": progress,
                    "data": data,
                    "previewUrl": data.get("previewUrl"),
                    "editUrl": data.get("editUrl"),
                }
            elif args.cmd == "update-text":
                css_obj: Optional[Dict[str, Any]] = None
                if args.css_json:
                    css_raw = load_json_arg(args.css_json)
                    if not isinstance(css_raw, dict):
                        print("css-json 必须是 JSON 对象", file=sys.stderr)
                        return 2
                    css_obj = css_raw
                update_result = client.update_editable_text(
                    scene_id=args.scene_id,
                    page_id=args.page_id,
                    element_id=args.element_id,
                    content=args.content.strip(),
                    css=css_obj,
                )
                out = {
                    "scene_id": args.scene_id,
                    "data": update_result,
                    "previewUrl": (args.preview_url or "").strip() or None,
                }
            elif args.cmd == "material-list":
                out = client.list_user_material_uploads(
                    file_type=args.file_type,
                    page_no=args.page_no,
                    page_size=args.page_size,
                    tag_id=args.tag_id,
                    material_api_base=args.material_api_base,
                )
            elif args.cmd == "editable-text":
                out = client.get_editable_text(args.scene_id)
            elif args.cmd == "body-images":
                out = client.get_body_images(args.scene_id, page_id=args.page_id)
            elif args.cmd == "replace-body-image":
                sid: Any = None
                if args.source_id is not None and str(args.source_id).strip() != "":
                    try:
                        sid = int(args.source_id)
                    except ValueError:
                        sid = args.source_id
                out = client.replace_body_image(
                    args.scene_id,
                    args.page_id,
                    args.element_id,
                    args.src,
                    source_id=sid,
                )
            elif args.cmd == "upload":
                if not token:
                    print(
                        json.dumps(
                            {
                                "success": False,
                                "code": 401,
                                "msg": "缺少 X-Openclaw-Token：请先执行 login 或传 --access-token。",
                            },
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                path = Path(args.file).expanduser()
                try:
                    out = upload_local_material(
                        token,
                        path,
                        bucket=args.bucket,
                        prefix=args.prefix,
                        object_name=args.name,
                        tmb_path=args.tmb_path,
                        source=args.source,
                        tag_id=args.tag_id,
                        file_type=args.file_type,
                        cos_api_base=args.cos_api_base,
                        material_api_base=args.material_api_base,
                    )
                except FileNotFoundError as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 400, "msg": str(e)},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except ValueError as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 400, "msg": str(e)},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except ImportError as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 500, "msg": str(e)},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except RuntimeError as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 400, "msg": str(e)},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except requests.RequestException as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 502, "msg": f"上传相关 HTTP 失败: {e}"},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except CosServiceError as e:
                    detail = e.get_digest_msg() if hasattr(e, "get_digest_msg") else str(e)
                    print(
                        json.dumps(
                            {"success": False, "code": 502, "msg": "COS 上传失败", "detail": detail},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except CosClientError as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 502, "msg": f"COS 客户端错误: {e}"},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
                except Exception as e:
                    print(
                        json.dumps(
                            {"success": False, "code": 500, "msg": str(e)},
                            ensure_ascii=False,
                            indent=2,
                        )
                    )
                    return 1
            else:
                print(f"未知子命令: {args.cmd}", file=sys.stderr)
                return 2
    except EqxiuAigcApiError as e:
        print(json.dumps({"error": str(e), "raw": e.raw}, ensure_ascii=False, indent=2))
        return 1
    except requests.RequestException as e:
        print(json.dumps({"error": f"HTTP 错误: {e}"}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0
