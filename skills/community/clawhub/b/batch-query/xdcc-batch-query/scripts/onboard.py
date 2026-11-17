#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
onboard.py — 小递查查批量查询「完整闭环」编排器（面向客户）

一条命令走完：确保凭据（没有就引导注册/登录）→ 校验可用 → 批量查询并导出。

设计目标（客户视角）：
  · 零基础也能用：没有凭据时自动拉起注册引导（页面内有分步横幅）；
  · 闭环：注册完直接就能查，不用手动搬运密钥；
  · 任何卡点都有会话内的兜底排查提示（不含任何外部联系方式）。

用法：
  # 1) 仅确保凭据就绪（无凭据会拉起注册向导，需客户提供手机号+密码）
  python onboard.py --phone 138xxxx --password '****'

  # 2) 一次性闭环：注册（如需）+ 直接批量查询
  python onboard.py --phone 138xxxx --password '****' --file orders.txt --output result

  # 3) 已有凭据，直接查
  python onboard.py --file orders.txt --output result

  # 4) 只校验凭据是否可用
  python onboard.py --validate-only
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    load_creds, cs_hint, validate_track_creds, DEFAULT_TEST_NO,
)


def _validate(creds, test_no=None):
    """试跑一单确认凭据可用于批量查询。返回 (ok, message)。"""
    return validate_track_creds(creds, test_no or DEFAULT_TEST_NO)


def _ensure_creds(args):
    """确保凭据存在且可用。返回 creds dict 或 None（并给出提示）。"""
    creds_path = args.creds
    creds = load_creds(creds_path)
    if creds.get("XDCC_PLATFORM_ID") and creds.get("XDCC_API_KEY") and creds.get("XDCC_MEMBER_ID"):
        ok, msg = _validate(creds)
        if ok:
            print(f"[凭据就绪] 已加载 {creds_path}（PlatformID={creds['XDCC_PLATFORM_ID']}）")
            return creds
        print(f"[凭据失效] 现有凭据校验未通过：{msg}", file=sys.stderr)
        print("将尝试重新注册/登录以刷新凭据…", file=sys.stderr)

    # 需要注册/登录
    if not args.phone or not args.password:
        print("\n⚠️ 尚未配置小递查查凭据，且未提供手机号/密码，无法自动注册。", file=sys.stderr)
        print("请向客户索取：① 手机号 ② 密码（客户自行在小递查查注册设置的）。", file=sys.stderr)
        print("然后重试：", file=sys.stderr)
        print(f"  python onboard.py --phone <客户手机号> --password <客户密码> [--file 订单.txt]", file=sys.stderr)
        print(cs_hint("缺少注册所需的手机号/密码"), file=sys.stderr)
        return None

    print("[未检测到凭据] 启动注册引导向导…")
    # 懒加载 Playwright 依赖（仅注册时需要）
    try:
        from guided_register import run as guided_run
    except ImportError as e:
        print(f"[失败] 缺少 Playwright：{e}", file=sys.stderr)
        print("请先安装：pip install playwright && playwright install chromium", file=sys.stderr)
        print(cs_hint("运行环境缺少浏览器自动化依赖"), file=sys.stderr)
        return None

    rc = guided_run(
        mode=args.mode, phone=args.phone, password=args.password,
        no_autofill=False, timeout=args.timeout,
        creds_path=creds_path, chrome_path=args.chrome_path, quiet=False,
    )
    if rc != 0:
        print("\n[失败] 注册引导未成功生成凭据，无法继续。", file=sys.stderr)
        print(cs_hint("注册引导未成功"), file=sys.stderr)
        return None

    creds = load_creds(creds_path)
    ok, msg = _validate(creds)
    if not ok:
        print(f"\n[失败] 新凭据校验未通过：{msg}", file=sys.stderr)
        print(cs_hint(f"新凭据校验未通过：{msg}"), file=sys.stderr)
        return None
    print(f"[凭据就绪] {creds_path}（PlatformID={creds['XDCC_PLATFORM_ID']}）")
    return creds


def _do_query(creds, args):
    import batch_query as bq
    # 复用 batch_query 的输入解析：构造一个最小 args 对象
    class _A:
        pass
    a = _A()
    a.file = args.file
    a.nos = args.nos
    a.telmap = args.telmap
    a.tel = args.tel
    try:
        items = bq.parse_input(a)
    except (OSError, UnicodeDecodeError) as e:
        print(f"错误: 读取输入失败：{e}", file=sys.stderr)
        print("请检查 --file / --telmap 路径是否存在，且文件为 UTF-8 编码。", file=sys.stderr)
        print(cs_hint("输入文件读取失败"), file=sys.stderr)
        return 2
    if not items:
        print("错误: 未解析到任何运单号。请通过 --file / --nos 提供。", file=sys.stderr)
        return 2
    warn = bq.warn_missing_tel(items)
    if warn:
        sys.stderr.write(warn + "\n")
    print(f"[批量查询] 共 {len(items)} 个单号，开始并发查询…")
    results = bq.batch_query(
        creds["XDCC_PLATFORM_ID"], creds["XDCC_API_KEY"], creds["XDCC_MEMBER_ID"],
        items, concurrency=args.concurrency, timeout=args.timeout_q, progress=not args.quiet,
    )
    agg = bq.build_aggregate(results)
    if args.output:
        fmt = args.format
        if fmt in ("json", "all"):
            bq.write_json(args.output + ".json", results, agg)
        if fmt in ("csv", "all"):
            bq.write_csv(args.output + ".csv", results)
        if fmt in ("txt", "all"):
            bq.write_report_txt(args.output + ".report.txt", results, agg)
        print(f"[已导出] {args.output}.json / .csv / .report.txt")
    if args.pretty or not args.output:
        print(bq.format_aggregate(agg))
        if args.pretty:
            print("\n" + "=" * 48 + "\n逐单明细\n" + "=" * 48)
            for r in results:
                print(f"\n--- {r['no']} ---")
                if r["ok"]:
                    print(bq.format_text(r["summary"]))
                else:
                    print(f"查询失败：Code={r['code']} {r['message']}")
    return 0 if not agg["failed"] else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="小递查查批量查询 完整闭环编排器")
    p.add_argument("--creds", default=os.path.expanduser("~/.workbuddy/xdcc-credentials.env"),
                   help="凭据路径（默认 ~/.workbuddy/xdcc-credentials.env）")
    p.add_argument("--mode", choices=["register", "login"], default="register",
                   help="无凭据时使用的模式（默认 register）")
    p.add_argument("--phone", help="注册/登录手机号（无凭据时用于引导注册）")
    p.add_argument("--password", help="注册/登录密码（无凭据时用于引导注册）")
    p.add_argument("--timeout", type=int, default=600, help="注册引导等待秒数")
    p.add_argument("--chrome-path", default=None, help="Chrome 可执行文件路径")
    p.add_argument("--validate-only", action="store_true", help="仅校验凭据是否可用后退出")
    # 批量查询参数（透传给 batch_query）
    q = p.add_argument_group("批量查询（可选；提供即查询）")
    q.add_argument("--file", help="批量文件：每行 单号 或 单号,手机后四位")
    q.add_argument("--nos", help="内联单号：逗号/空格分隔")
    q.add_argument("--telmap", help="手机号映射 CSV：表头 no,tel")
    q.add_argument("--tel", default="", help="全局默认手机号后四位")
    q.add_argument("--concurrency", type=int, default=5, help="并发数（默认5，上限20）")
    q.add_argument("--timeout-q", dest="timeout_q", type=int, default=8, help="单请求超时秒数")
    q.add_argument("--output", help="输出基名（配合 --format 生成文件）")
    q.add_argument("--format", default="all", choices=["json", "csv", "txt", "all"])
    q.add_argument("--pretty", action="store_true", help="向 stdout 打印可读明细")
    q.add_argument("--quiet", action="store_true", help="不打印进度")
    args = p.parse_args(argv)

    print("=" * 56)
    print("  小递查查批量查询 · 完整闭环")
    print("=" * 56)

    creds = _ensure_creds(args)
    if not creds:
        return 1

    if args.validate_only:
        print("\n✅ 凭据校验通过，可直接用于批量查询。")
        return 0

    if not (args.file or args.nos or args.telmap):
        print("\n✅ 凭据就绪。请提供运单号开始批量查询，例如：")
        print(f"  python onboard.py --file orders.txt --output result")
        return 0

    return _do_query(creds, args)


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
