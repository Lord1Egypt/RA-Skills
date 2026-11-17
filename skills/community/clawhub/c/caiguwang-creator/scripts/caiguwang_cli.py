#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""才谷网投票技能入口：python caiguwang_cli.py <命令> [参数]"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from caiguwang import client, config


def out(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _sanitize_auth(result):
    """安全兜底：剥离 uid/username/nickname 等内部标识（对话内容可能被截图分享，不应外泄）"""
    data = result.get("data")
    if isinstance(data, dict):
        for k in ("uid", "username", "nickname"):
            data.pop(k, None)
        if "valid" not in data and result.get("code") == 200:
            data["valid"] = True
            if data.get("account") is None:
                data["account"] = "用户"
    return result


def cmd_auth(args):
    if args.action == "login":
        token = (args.token or "").strip()
        if not token:
            token = input("请粘贴访问令牌（后台「养虾Skill」页获取）: ").strip()
        if not token:
            print(json.dumps({"success": False, "code": 400, "msg": "令牌不能为空"}, ensure_ascii=False))
            return
        path = config.save_token(token)
        result = client.auth_status()
        if result.get("code") == 200:
            # 不透传接口响应体（旧版接口可能含 uid/username），只报绑定结果
            out({"success": True, "code": 200, "msg": "登录成功，令牌已保存到 %s" % path})
        else:
            out(result)
    else:
        token = config.load_token()
        if not token:
            out({"success": False, "code": 1002, "msg": "未配置令牌，请先执行 login --token <令牌>"})
            return
        out(_sanitize_auth(client.auth_status()))


def cmd_search(args):
    out(client.search_templates(keyword=args.kw or "", page=args.page, size=args.size))


def _build_body(args):
    body = {}
    if args.describe:
        body["describe"] = args.describe
    if args.title:
        body["title"] = args.title
    if args.intro:
        body["intro"] = args.intro
    if args.notice:
        body["notice"] = args.notice
    if args.start:
        body["start_time"] = args.start
    if args.end:
        body["end_time"] = args.end
    if args.multi:
        body["multi"] = 1
    if args.per_user_count is not None:
        body["per_user_count"] = args.per_user_count
    if args.per_user_scope:
        body["per_user_scope"] = args.per_user_scope
    if args.select_min is not None:
        body["select_min"] = args.select_min
    if args.select_max is not None:
        body["select_max"] = args.select_max
    if args.groups:
        body["groups"] = [g.strip() for g in args.groups.split(",") if g.strip()]
    if args.apply:
        body["apply"] = 1
    if args.template:
        body["template_id"] = args.template
    if args.sponsor:
        body["sponsor_name"] = args.sponsor
    if args.sponsor_tel:
        body["sponsor_tel"] = args.sponsor_tel
    if args.cover:
        body["cover"] = args.cover
    raw_items = ""
    if args.items_file:
        raw_items = Path(args.items_file).read_text(encoding="utf-8")
    elif args.items:
        raw_items = args.items
    if raw_items:
        try:
            parsed = json.loads(raw_items)
        except ValueError:
            return None, "选手列表不是合法 JSON"
        if not isinstance(parsed, list):
            return None, "选手列表需为数组，如 [{\"name\":\"选手一\",\"image\":\"https://...\"}]"
        body["items"] = parsed
    return body, None


def cmd_create(args):
    if not args.describe and not args.title:
        out({"success": False, "code": 400, "msg": "请提供 --describe（AI 一句话生成）或 --title（手动创建）"})
        return
    body, err = _build_body(args)
    if err:
        out({"success": False, "code": 400, "msg": err})
        return
    out(client.create_vote(body))


def cmd_update(args):
    if not args.id:
        out({"success": False, "code": 400, "msg": "请提供 --id（活动 ID）"})
        return
    body = {"id": args.id}
    if args.title:
        body["title"] = args.title
    if args.intro:
        body["intro"] = args.intro
    if args.notice:
        body["notice"] = args.notice
    if args.start:
        body["start_time"] = args.start
    if args.end:
        body["end_time"] = args.end
    if args.multi is not None:
        body["multi"] = 1 if args.multi else 0
    if args.per_user_count is not None:
        body["per_user_count"] = args.per_user_count
    if args.per_user_scope:
        body["per_user_scope"] = args.per_user_scope
    if args.select_min is not None:
        body["select_min"] = args.select_min
    if args.select_max is not None:
        body["select_max"] = args.select_max
    if args.groups is not None:
        body["groups"] = [g.strip() for g in args.groups.split(",") if g.strip()]
    if args.apply is not None:
        body["apply"] = 1 if args.apply else 0
    if args.sponsor:
        body["sponsor_name"] = args.sponsor
    if args.sponsor_tel:
        body["sponsor_tel"] = args.sponsor_tel
    if args.cover is not None:
        body["cover"] = args.cover
    if len(body) <= 1:
        out({"success": False, "code": 400, "msg": "没有提供任何要修改的内容（如 --title / --end / --groups）"})
        return
    out(client.update_vote(body))


def cmd_item_add(args):
    if not args.id:
        out({"success": False, "code": 400, "msg": "请提供 --id（活动 ID）"})
        return
    body = {"id": args.id}
    raw_items = ""
    if args.items_file:
        raw_items = Path(args.items_file).read_text(encoding="utf-8")
    elif args.items:
        raw_items = args.items
    if raw_items:
        try:
            parsed = json.loads(raw_items)
        except ValueError:
            out({"success": False, "code": 400, "msg": "选手列表不是合法 JSON"})
            return
        if not isinstance(parsed, list):
            out({"success": False, "code": 400, "msg": "选手列表需为数组，如 [{\"name\":\"选手一\",\"image\":\"https://...\"}]"})
            return
        body["items"] = parsed
    else:
        if not args.name:
            out({"success": False, "code": 400, "msg": "请提供 --name，或用 --items/--items-file 批量添加"})
            return
        body["items"] = [{"name": args.name, "image": args.image or ""}]
    out(client.item_add(body))


def cmd_item_update(args):
    if not args.id or not args.item_id:
        out({"success": False, "code": 400, "msg": "请提供 --id（活动 ID）和 --item-id（选手 ID，可从 vote-data 结果获取）"})
        return
    body = {"id": args.id, "item_id": args.item_id}
    if args.name:
        body["name"] = args.name
    if args.image:
        body["image"] = args.image
    if len(body) <= 2:
        out({"success": False, "code": 400, "msg": "没有提供任何要修改的内容（--name / --image）"})
        return
    out(client.item_update(body))


def _local_crop(path, tw, th):
    """本地按比例中心裁剪并输出 jpg（与后台轮播图 750:464 强制裁剪等价）。
    需要 Pillow（可选依赖）；未安装或失败返回 None，由服务端做比例校验。"""
    try:
        from PIL import Image
    except Exception:
        return None
    try:
        im = Image.open(path)
        sw, sh = im.size
        tr = tw / th
        if sw / sh > tr:
            nw, nh = int(round(sh * tr)), sh
        else:
            nw, nh = sw, int(round(sw / tr))
        left = (sw - nw) // 2
        top = (sh - nh) // 2
        im = im.convert("RGB").crop((left, top, left + nw, top + nh)).resize((tw, th), Image.LANCZOS)
        import tempfile
        import os as _os
        fd, tmp = tempfile.mkstemp(suffix=".jpg")
        _os.close(fd)
        im.save(tmp, "JPEG", quality=92)
        return tmp
    except Exception:
        return None


def _compress_like_pc(path):
    """对齐 PC 素材库前端压缩（public/mp/index.html:1361 compressImage）：
    宽>1000 → 缩到 1000；PNG→webp(0.82/0.88)、其他→jpg(0.8/0.9)；
    宽<=1000 且 <=200KB 不压；GIF 不压；输出比原图小才采用。需 Pillow。"""
    try:
        from PIL import Image
    except Exception:
        return None
    try:
        import os as _os
        ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
        if ext == "gif":
            return None
        size = _os.path.getsize(path)
        im = Image.open(path)
        w, h = im.size
        MAX_W = 1000
        need = w > MAX_W
        is_png = ext == "png"
        if not need and size <= 200000:
            return None
        if need and is_png and size <= 200000:
            return None
        nw = MAX_W if need else w
        nh = int(round(h * MAX_W / w)) if need else h
        im2 = im.convert("RGBA" if is_png else "RGB")
        if need:
            im2 = im2.resize((nw, nh), Image.LANCZOS)
        import tempfile
        if is_png:
            fmt, quality, suffix = "WEBP", int(round((0.82 if need else 0.88) * 100)), ".webp"
        else:
            fmt, quality, suffix = "JPEG", int(round((0.8 if need else 0.9) * 100)), ".jpg"
        fd, tmp = tempfile.mkstemp(suffix=suffix)
        _os.close(fd)
        try:
            im2.save(tmp, fmt, quality=quality)
        except Exception:
            # 环境不支持 webp 编码时回退 jpg（前端同样特性：canvas 不支持则保持原图，这里保守转 jpg）
            try:
                _os.unlink(tmp)
            except Exception:
                pass
            fd, tmp = tempfile.mkstemp(suffix=".jpg")
            _os.close(fd)
            im2.convert("RGB").save(tmp, "JPEG", quality=quality)
        if _os.path.getsize(tmp) < size:
            return tmp
        _os.unlink(tmp)
        return None
    except Exception:
        return None


def cmd_upload(args):
    if not args.file and not args.url:
        out({"success": False, "code": 400, "msg": "请提供 --file（本地图片文件）或 --url（图片链接）"})
        return
    if args.file and args.url:
        out({"success": False, "code": 400, "msg": "--file 与 --url 二选一"})
        return
    if args.file and not Path(args.file).exists():
        out({"success": False, "code": 400, "msg": "文件不存在：%s" % args.file})
        return
    crop = (args.crop or "").strip().lower()
    file_path = args.file
    crop_arg = ""
    tmp_path = None
    if crop and file_path:
        import re
        m = re.match(r"^(\d{2,4})x(\d{2,4})$", crop)
        if m:
            tmp_path = _local_crop(file_path, int(m.group(1)), int(m.group(2)))
            if tmp_path:
                file_path = tmp_path
    if not tmp_path:
        if crop:
            #本地无法裁剪（未装 Pillow 等）→ 交给服务端做比例校验
            crop_arg = crop
        elif file_path:
            #素材库/选手图链路：与 PC 前端 compressImage 同款压缩
            tmp_c = _compress_like_pc(file_path)
            if tmp_c:
                tmp_path = tmp_c
                file_path = tmp_c
    res = client.upload_image(file_path=file_path, image_url=args.url, crop=crop_arg)
    if tmp_path:
        try:
            import os as _os
            _os.unlink(tmp_path)
        except Exception:
            pass
    out(res)


def cmd_list(args):
    out(client.list_activities(page=args.page, size=args.size, keyword=args.kw or "", status=args.status))


def cmd_vote_data(args):
    out(client.vote_data(args.id, page=args.page, size=args.size))


def cmd_view_data(args):
    out(client.view_data(args.id))


def cmd_group_rename(args):
    body = {"id": args.id, "new_name": args.new_name}
    if args.index is not None:
        body["index"] = args.index
    if args.name:
        body["name"] = args.name
    out(client.group_update(body))


def cmd_material(args):
    out(client.list_material(cate=args.cate, page=args.page, size=args.size))


def main():
    p = argparse.ArgumentParser(prog="caiguwang_cli", description="才谷网投票技能命令行")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_auth = sub.add_parser("auth", help="令牌管理：login / status")
    p_auth.add_argument("action", choices=["login", "status"], nargs="?", default="status")
    p_auth.add_argument("--token", help="访问令牌（login 时可选，不带则交互输入）")
    p_auth.set_defaults(fn=cmd_auth)

    p_search = sub.add_parser("search", help="检索投票模板")
    p_search.add_argument("--kw", help="关键词")
    p_search.add_argument("--page", type=int, default=1)
    p_search.add_argument("--size", type=int, default=10)
    p_search.set_defaults(fn=cmd_search)

    p_create = sub.add_parser("create", help="创建投票活动（--describe 走 AI 生成）")
    p_create.add_argument("--describe", help="一段话描述活动需求（AI 生成）")
    p_create.add_argument("--title", help="活动标题（≤50字）")
    p_create.add_argument("--intro", help="活动说明（必填，长度不限）")
    p_create.add_argument("--notice", help="报名须知")
    p_create.add_argument("--start", help="开始时间 YYYY-MM-DD HH:MM")
    p_create.add_argument("--end", help="结束时间 YYYY-MM-DD HH:MM")
    p_create.add_argument("--multi", action="store_true", help="开启多选投票")
    p_create.add_argument("--per-user-count", type=int, help="每人可投次数（1~20）")
    p_create.add_argument("--per-user-scope", choices=["day", "total"], help="每天 / 活动期间总共")
    p_create.add_argument("--select-min", type=int, help="多选每次最少选几个")
    p_create.add_argument("--select-max", type=int, help="多选每次最多选几个")
    p_create.add_argument("--groups", help="分组名，逗号分隔（2~100 组）")
    p_create.add_argument("--apply", action="store_true", help="开启选手报名")
    p_create.add_argument("--template", type=int, help="模板 ID（search 返回的 template_id）")
    p_create.add_argument("--sponsor", help="主办方名称")
    p_create.add_argument("--sponsor-tel", help="主办方电话")
    p_create.add_argument("--cover", help="活动封面图 URL（建议 750×464 比例）")
    p_create.add_argument("--items", help="选手列表 JSON 字符串")
    p_create.add_argument("--items-file", help="选手列表 JSON 文件路径")
    p_create.set_defaults(fn=cmd_create)

    p_update = sub.add_parser("update", help="修改已创建活动（对话修改）")
    p_update.add_argument("--id", type=int, required=True, help="活动 ID")
    p_update.add_argument("--title", help="活动标题（≤50字）")
    p_update.add_argument("--intro", help="活动说明")
    p_update.add_argument("--notice", help="报名须知")
    p_update.add_argument("--start", help="开始时间 YYYY-MM-DD HH:MM")
    p_update.add_argument("--end", help="结束时间 YYYY-MM-DD HH:MM")
    p_update.add_argument("--multi", dest="multi", action="store_true", default=None, help="改为多选投票")
    p_update.add_argument("--no-multi", dest="multi", action="store_false", help="改为单选投票")
    p_update.add_argument("--per-user-count", type=int, help="每人可投次数（1~20）")
    p_update.add_argument("--per-user-scope", choices=["day", "total"], help="每天 / 活动期间总共")
    p_update.add_argument("--select-min", type=int, help="多选每次最少选几个")
    p_update.add_argument("--select-max", type=int, help="多选每次最多选几个")
    p_update.add_argument("--groups", help="分组名，逗号分隔（整体替换，2~100 组；传空串清空分组）")
    p_update.add_argument("--apply", dest="apply", action="store_true", default=None, help="开启选手报名")
    p_update.add_argument("--no-apply", dest="apply", action="store_false", help="关闭选手报名")
    p_update.add_argument("--sponsor", help="主办方名称（传空串关闭主办方展示）")
    p_update.add_argument("--sponsor-tel", help="主办方电话")
    p_update.add_argument("--cover", help="活动封面图 URL（建议 750×464 比例）")
    p_update.set_defaults(fn=cmd_update)

    p_iadd = sub.add_parser("item-add", help="为活动添加选手（单次最多 200 位）")
    p_iadd.add_argument("--id", type=int, required=True, help="活动 ID")
    p_iadd.add_argument("--name", help="选手名称（单个添加）")
    p_iadd.add_argument("--image", help="选手图片 URL（可选）")
    p_iadd.add_argument("--items", help="批量选手 JSON 字符串")
    p_iadd.add_argument("--items-file", help="批量选手 JSON 文件路径")
    p_iadd.set_defaults(fn=cmd_item_add)

    p_iupd = sub.add_parser("item-update", help="修改选手名称/图片")
    p_iupd.add_argument("--id", type=int, required=True, help="活动 ID")
    p_iupd.add_argument("--item-id", type=int, required=True, help="选手 ID（vote-data 返回里可取）")
    p_iupd.add_argument("--name", help="新名称")
    p_iupd.add_argument("--image", help="新图片 URL")
    p_iupd.set_defaults(fn=cmd_item_update)

    p_up = sub.add_parser("upload", help="上传图片（返回素材 URL，用于选手图片/封面）")
    p_up.add_argument("--file", help="本地图片文件路径")
    p_up.add_argument("--url", help="图片链接（远程抓取）")
    p_up.add_argument("--crop", help="可选裁剪比例，如 750x464（封面图用，与后台轮播图裁剪一致）")
    p_up.set_defaults(fn=cmd_upload)

    p_list = sub.add_parser("list", help="活动列表")
    p_list.add_argument("--page", type=int, default=1)
    p_list.add_argument("--size", type=int, default=10)
    p_list.add_argument("--kw", help="标题关键词")
    p_list.add_argument("--status", choices=["all", "ongoing", "ended", "pending"], default="all")
    p_list.set_defaults(fn=cmd_list)

    p_vd = sub.add_parser("vote-data", help="投票数据（选手榜单）")
    p_vd.add_argument("--id", type=int, required=True, help="活动 ID")
    p_vd.add_argument("--page", type=int, default=1)
    p_vd.add_argument("--size", type=int, default=20)
    p_vd.set_defaults(fn=cmd_vote_data)

    p_view = sub.add_parser("view-data", help="活动整体数据")
    p_view.add_argument("--id", type=int, required=True, help="活动 ID")
    p_view.set_defaults(fn=cmd_view_data)

    p_gr = sub.add_parser("group-rename", help="活动分组改名（不改选手归属，选手按分组序号挂组）")
    p_gr.add_argument("--id", type=int, required=True, help="活动 ID")
    p_gr.add_argument("--index", type=int, help="分组序号（从 0 开始；与 --name 二选一）")
    p_gr.add_argument("--name", help="原分组名（与 --index 二选一）")
    p_gr.add_argument("--new-name", required=True, help="新分组名")
    p_gr.set_defaults(fn=cmd_group_rename)

    p_mat = sub.add_parser("material", help="我的素材列表（URL 可直接用于选手图片/封面）")
    p_mat.add_argument("--cate", help="素材分组 id（不传=全部，0=未分组）")
    p_mat.add_argument("--page", type=int, default=1)
    p_mat.add_argument("--size", type=int, default=20)
    p_mat.set_defaults(fn=cmd_material)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
