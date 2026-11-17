#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vault_cli.py — 本地凭据保险库 CLI（开源版）
================================================================================
基于公开标准 KeePass 格式（.kdbx），封装常用操作，开箱即用：
  create / add / list / get / remove / backup

定位：这是一个**可以直接用**的轻量本地密码管理器（MIT 开源）。
- 数据文件为业界标准 .kdbx（KeePass 生态全平台可读：KeePassXC / KeePassHO / Strongbox…）
- 主密码绝不落盘、不进日志；优先从环境变量 VAULT_PASSPHRASE 读取，否则交互输入
- list 永不显示密码；get 取字段仅供本机使用

用法示例：
  export VAULT_PASSPHRASE='你的主密码'
  python vault_cli.py create --vault brain_vault.kdbx
  python vault_cli.py add --vault brain_vault.kdbx --title "微信" --username "wechat_id" --url "https://weixin.qq.com"
  python vault_cli.py list --vault brain_vault.kdbx
  python vault_cli.py get --vault brain_vault.kdbx --title "微信" --field username
  python vault_cli.py backup --vault brain_vault.kdbx --out ./backup

依赖：pip install pykeepass  （见 requirements.txt）
"""
import argparse
import getpass
import hashlib
import os
import shutil
import sys
import tempfile

try:
    from pykeepass import create_database, PyKeePass
    from pykeepass.exceptions import CredentialsError
except ImportError:
    sys.stderr.write("缺少依赖 pykeepass，请先安装：pip install -r requirements.txt\n")
    sys.exit(2)


def _master_password(interactive: bool = True, confirm: bool = False) -> str:
    """主密码：优先环境变量 VAULT_PASSPHRASE，否则交互输入（绝不落盘/进日志）。

    confirm=True 时（用于 create）要求输入两次且一致，避免输错导致建库后打不开。
    """
    p = os.environ.get("VAULT_PASSPHRASE")
    if p:
        return p
    if not interactive:
        sys.stderr.write("缺少主密码：请设置环境变量 VAULT_PASSPHRASE，或使用交互输入。\n")
        sys.exit(2)
    if confirm:
        p1 = getpass.getpass("主密码: ")
        p2 = getpass.getpass("再次输入主密码: ")
        if not p1:
            sys.stderr.write("主密码不能为空\n")
            sys.exit(2)
        if p1 != p2:
            sys.stderr.write("两次输入不一致，请重试。\n")
            sys.exit(2)
        return p1
    p = getpass.getpass("主密码: ")
    if not p:
        sys.stderr.write("主密码不能为空\n")
        sys.exit(2)
    return p


def _open(vault: str, keyfile: str = None, interactive: bool = True):
    if not os.path.exists(vault):
        sys.stderr.write(f"保险库不存在：{vault}（请先 create）\n")
        sys.exit(2)
    if keyfile and not os.path.exists(keyfile):
        sys.stderr.write(f"密钥文件不存在：{keyfile}\n")
        sys.stderr.write("提示：--keyfile 必须是已存在的文件（与建库时一致）。若丢失密钥文件，见 FAQ「恢复密钥文件也丢了怎么办」。\n")
        sys.exit(2)
    mp = _master_password(interactive)
    try:
        return PyKeePass(vault, password=mp, keyfile=keyfile)
    except CredentialsError:
        sys.stderr.write("主密码不正确，或密钥文件不匹配（若已设置密钥文件，请用 --keyfile 指定）。\n")
        sys.exit(2)
    except Exception as exc:
        sys.stderr.write(f"打开保险库失败：{vault}\n")
        sys.stderr.write(f"原因：{exc}\n")
        sys.stderr.write("提示：文件可能已损坏，或格式非 .kdbx。可尝试用备份文件恢复（见 backup 命令）。\n")
        sys.exit(2)


def _need(vault: str):
    if not vault:
        sys.stderr.write("缺少 --vault 参数\n")
        sys.exit(2)


def cmd_create(args):
    _need(args.vault)
    if os.path.exists(args.vault):
        sys.stderr.write(f"文件已存在，不覆盖：{args.vault}\n")
        sys.exit(2)
    if args.keyfile and not os.path.exists(args.keyfile):
        sys.stderr.write(f"密钥文件不存在：{args.keyfile}\n")
        sys.stderr.write("提示：--keyfile 必须是已存在的文件（建库时即作为双因子绑定）。若还没有密钥文件，请先用 create 建普通库，或用其他方式生成密钥文件。\n")
        sys.exit(2)
    mp = _master_password(args.interactive, confirm=True)
    try:
        kp = create_database(args.vault, password=mp, keyfile=args.keyfile)
        kp.save()
    except Exception as exc:
        sys.stderr.write(f"创建保险库失败：{args.vault}\n")
        sys.stderr.write(f"原因：{exc}\n")
        sys.exit(2)
    print(f"[ok] 已创建保险库：{args.vault}")


def cmd_add(args):
    _need(args.vault)
    kp = _open(args.vault, args.keyfile, args.interactive)
    group = kp.root_group
    if args.group:
        g = kp.find_groups_by_name(args.group, first=True)
        group = g if g else kp.add_group(kp.root_group, args.group)
    if kp.find_entries_by_title(args.title, first=True) is not None:
        sys.stderr.write(f"条目已存在：{args.title}\n")
        sys.exit(2)
    kp.add_entry(group, title=args.title, username=args.username,
                 password=args.password or "", url=args.url or "")
    try:
        kp.save()
    except Exception as exc:
        sys.stderr.write(f"保存失败：{args.vault}\n")
        sys.stderr.write(f"原因：{exc}\n")
        sys.stderr.write("提示：检查库文件所在目录是否有写权限、磁盘空间是否充足。\n")
        sys.exit(2)
    print(f"[ok] 已添加条目：{args.title}")


def cmd_list(args):
    _need(args.vault)
    kp = _open(args.vault, args.keyfile, args.interactive)
    rows = []
    for e in kp.entries:
        if args.group and (e.group.name != args.group):
            continue
        rows.append((e.group.name, e.title, e.username or "", e.url or ""))
    if not rows:
        print("（无条目）")
        return
    print(f"{'分组':<16}{'标题':<24}{'用户名':<20}{'URL'}")
    for g, t, u, url in rows:
        print(f"{g:<16}{t:<24}{u:<20}{url}")


def cmd_get(args):
    _need(args.vault)
    kp = _open(args.vault, args.keyfile, args.interactive)
    e = kp.find_entries_by_title(args.title, first=True)
    if e is None:
        sys.stderr.write(f"未找到条目：{args.title}\n")
        sys.exit(2)
    field = (args.field or "username").lower()
    if field == "password":
        print(e.password or "")
    elif field == "username":
        print(e.username or "")
    elif field == "url":
        print(e.url or "")
    else:
        sys.stderr.write("--field 可选：username / password / url\n")
        sys.exit(2)


def cmd_remove(args):
    _need(args.vault)
    kp = _open(args.vault, args.keyfile, args.interactive)
    e = kp.find_entries_by_title(args.title, first=True)
    if e is None:
        sys.stderr.write(f"未找到条目：{args.title}\n")
        sys.exit(2)
    kp.delete_entry(e)
    try:
        kp.save()
    except Exception as exc:
        sys.stderr.write(f"保存失败：{args.vault}\n")
        sys.stderr.write(f"原因：{exc}\n")
        sys.exit(2)
    print(f"[ok] 已删除条目：{args.title}")


def cmd_backup(args):
    _need(args.vault)
    if not os.path.exists(args.vault):
        sys.stderr.write(f"保险库不存在：{args.vault}\n")
        sys.exit(2)
    try:
        os.makedirs(args.out, exist_ok=True)
        dst = os.path.join(args.out, os.path.basename(args.vault))
        shutil.copy2(args.vault, dst)
        h = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    except Exception as exc:
        sys.stderr.write(f"备份失败：{args.vault}\n")
        sys.stderr.write(f"原因：{exc}\n")
        sys.stderr.write("提示：检查 --out 目录是否可写、源库文件是否可读。\n")
        sys.exit(2)
    print(f"[ok] 已备份：{dst}")
    print(f"     SHA-256: {h}")


def main():
    ap = argparse.ArgumentParser(prog="vault_cli", description="本地凭据保险库 CLI（.kdbx 标准格式）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def add_common(p):
        p.add_argument("--vault", required=True, help=".kdbx 保险库路径")
        p.add_argument("--keyfile", default=None, help="密钥文件路径（可选，双因子）")
        p.add_argument("--interactive", action="store_true", help="允许交互输入主密码")

    p = sub.add_parser("create", help="新建保险库")
    add_common(p)
    p.set_defaults(fn=cmd_create)

    p = sub.add_parser("add", help="添加条目")
    add_common(p)
    p.add_argument("--title", required=True, help="条目标题（如 微信）")
    p.add_argument("--username", default="", help="用户名 / 账号")
    p.add_argument("--password", default="", help="密码（留空则存空值；建议配合环境变量使用）")
    p.add_argument("--url", default="", help="URL")
    p.add_argument("--group", default="", help="分组（不存在则自动创建）")
    p.set_defaults(fn=cmd_add)

    p = sub.add_parser("list", help="列出条目（不显示密码）")
    add_common(p)
    p.add_argument("--group", default="", help="只列出指定分组")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("get", help="取出条目的某个字段")
    add_common(p)
    p.add_argument("--title", required=True, help="条目标题")
    p.add_argument("--field", default="username", help="字段：username / password / url")
    p.set_defaults(fn=cmd_get)

    p = sub.add_parser("remove", help="删除条目")
    add_common(p)
    p.add_argument("--title", required=True, help="条目标题")
    p.set_defaults(fn=cmd_remove)

    p = sub.add_parser("backup", help="备份保险库文件并打印 SHA-256")
    add_common(p)
    p.add_argument("--out", required=True, help="备份输出目录")
    p.set_defaults(fn=cmd_backup)

    args = ap.parse_args()
    try:
        args.fn(args)
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.stderr.write("\n已取消操作。\n")
        sys.exit(130)
    except Exception as exc:
        sys.stderr.write(f"操作失败：{exc}\n")
        sys.stderr.write("提示：可先检查库文件是否可读写、磁盘空间是否充足，或尝试 backup 恢复。\n")
        sys.exit(2)


if __name__ == "__main__":
    main()
