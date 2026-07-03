#!/usr/bin/env python3
"""飞书文档所有权批量转移工具。

用法:
  python3 transfer_owner.py --target ou_xxx --all          # 转移所有AI创建的文档
  python3 transfer_owner.py --target ou_xxx --list         # 只列出，不转移
  python3 transfer_owner.py --target ou_xxx --token bitable:TOKEN  # 转移指定文件
"""
import argparse
import json
import subprocess
import sys


def lark_api(method, path, data=None):
    cmd = ["lark-cli", "api", method, path]
    if data:
        cmd += ["--data", json.dumps(data)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": result.stdout or result.stderr}


def list_root_files():
    resp = lark_api("GET", "/open-apis/drive/v1/files?folder_token=0")
    items = resp.get("data", {}).get("items", [])
    results = []
    for item in items:
        results.append({
            "name": item.get("name"),
            "type": item.get("type"),
            "token": item.get("token"),
            "owner_id": item.get("owner_id"),
        })
    return results


def transfer_owner(file_type, token, target_id, member_type="openid"):
    data = {
        "type": file_type,
        "token": token,
        "owner": {
            "member_type": member_type,
            "member_id": target_id,
        },
        "remove_old_owner": False,
        "cancel_notify": False,
    }
    return lark_api("POST", "/open-apis/drive/permission/member/transfer", data)


def get_file_info(file_type, token):
    resp = lark_api("GET", f"/open-apis/drive/v1/files/{file_type}:{token}")
    return resp.get("data", {}).get("file", {})


def main():
    parser = argparse.ArgumentParser(description="飞书文档所有权转移")
    parser.add_argument("--target", required=True, help="目标用户ID (open_id)")
    parser.add_argument("--member-type", default="openid", help="ID类型 (默认 openid)")
    parser.add_argument("--token", help="转移指定文件，格式 type:token")
    parser.add_argument("--all", action="store_true", help="转移根目录所有文件")
    parser.add_argument("--list", action="store_true", help="只列出，不转移 (dry-run)")
    parser.add_argument("--ai-owner", help="只转移此所有者的文件 (可选过滤)")
    args = parser.parse_args()

    if args.token:
        parts = args.token.split(":", 1)
        file_type, token = parts[0], parts[1]
        info = get_file_info(file_type, token)
        owner = info.get("owner_id", "unknown")
        fname = info.get("name", file_type)
        print(f"  文件: {fname}")
        print(f"  类型: {file_type}")
        print(f"  当前所有者: {owner}")

        if not args.list:
            resp = transfer_owner(file_type, token, args.target, args.member_type)
            if resp.get("code") == 0:
                print(f"  转移成功 -> {args.target}")
            else:
                print(f"  转移失败: {resp}")
        else:
            print(f"  [DRY-RUN] 将转移到 {args.target}")
        return

    if args.all:
        print("扫描飞书根目录...")
        files = list_root_files()
        print(f"共找到 {len(files)} 个文件\n")

        ai_owner = args.ai_owner
        transferred = 0
        skipped = 0
        failed = 0

        for f in files:
            name = f["name"]
            ftype = f["type"]
            token = f["token"]
            owner = f["owner_id"]

            info = get_file_info(ftype, token)
            real_owner = info.get("owner_id", owner)
            ftype_from_info = info.get("type", ftype)

            is_ai = not real_owner.startswith("ou_")
            tag = "AI" if is_ai else "人类"
            print(f"  [{tag}] {name} ({ftype_from_info}) 所有者={real_owner}")

            if ai_owner and real_owner != ai_owner:
                skipped += 1
                print("    跳过（所有者不匹配）")
                continue

            if not is_ai and not ai_owner:
                skipped += 1
                print("    跳过（已是人类所有者）")
                continue

            if not args.list:
                resp = transfer_owner(ftype_from_info, token, args.target, args.member_type)
                if resp.get("code") == 0:
                    transferred += 1
                    print(f"    转移成功 -> {args.target}")
                else:
                    failed += 1
                    msg = resp.get("msg", resp)
                    print(f"    转移失败: {msg}")
            else:
                print(f"    [DRY-RUN] 将转移到 {args.target}")
                transferred += 1
            print()

        print(f"\n=== 汇总 ===")
        print(f"  转移: {transferred}")
        print(f"  跳过: {skipped}")
        print(f"  失败: {failed}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
