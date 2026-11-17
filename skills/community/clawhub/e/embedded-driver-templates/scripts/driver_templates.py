#!/usr/bin/env python3
"""嵌入式驱动模板库 CLI：9 款预验证驱动查询 + 外设初始化顺序层。

用法：
  python driver_templates.py list                       # 列出 9 款驱动
  python driver_templates.py get hc05                   # 查驱动全文（meta+.h+.c+md）
  python driver_templates.py wiring mpu6050             # 接线与避坑
  python driver_templates.py api                        # 外设用法总览（初始化硬要求）
  python driver_templates.py api-get mpu6050            # 单驱动初始化要求全文
  python driver_templates.py demo                       # 跑内置示例

引擎与 mcu-debug-mcp v4.5.4 core.py 同源（S2）；驱动数据同一份内容。
"""

from __future__ import annotations

import argparse
import sys

from engine import (driver_list, driver_get, driver_wiring,
                    peripheral_api_brief, peripheral_api_get, __version__)


def main(argv=None):
    p = argparse.ArgumentParser(description="嵌入式驱动模板库", prog="driver_templates")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="列出全部预验证驱动")
    g = sub.add_parser("get", help="驱动全文（验证记录+源码+文档）")
    g.add_argument("name")
    w = sub.add_parser("wiring", help="接线与避坑（wiring.md）")
    w.add_argument("name")
    sub.add_parser("api", help="外设初始化顺序总览")
    ap = sub.add_parser("api-get", help="单驱动外设初始化要求全文")
    ap.add_argument("name")
    sub.add_parser("demo", help="跑内置示例")
    p.add_argument("--version", action="version", version=__version__)
    a = p.parse_args(argv)

    if a.cmd == "list":
        out = driver_list()
    elif a.cmd == "get":
        out = driver_get(a.name)
    elif a.cmd == "wiring":
        out = driver_wiring(a.name)
    elif a.cmd == "api":
        out = peripheral_api_brief()
    elif a.cmd == "api-get":
        out = peripheral_api_get(a.name)
    else:
        out = (driver_list() + "\n\n" + driver_wiring("hc05")
               + "\n\n" + peripheral_api_brief())
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
