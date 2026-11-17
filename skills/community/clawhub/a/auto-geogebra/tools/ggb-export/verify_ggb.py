#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 .ggb 文件结构：ZIP 内应含 geogebra.xml；统计元素类型。"""
import collections
import os
import re
import sys
import zipfile


def check(path):
    print("=====", path)
    if not os.path.exists(path):
        print("  文件不存在")
        return False
    size = os.path.getsize(path)
    try:
        z = zipfile.ZipFile(path)
        names = z.namelist()
    except Exception as e:
        print("  不是有效 ZIP：%s" % e)
        return False
    print("  大小: %d bytes" % size)
    print("  ZIP 内容:", names)
    ok = "geogebra.xml" in names
    if ok:
        x = z.read("geogebra.xml").decode("utf-8")
        types = collections.Counter(re.findall(r'<element[^>]*type="([^"]+)"', x))
        print("  geogebra.xml: %d bytes；元素统计: %s" % (len(x), dict(types)))
        commands = re.findall(r'<command name="([^"]+)"', x)
        print("  命令调用数: %d（前 10 个: %s）" % (len(commands), commands[:10]))
    else:
        print("  [FAIL] 缺少 geogebra.xml")
    return ok


if __name__ == "__main__":
    allok = True
    for p in sys.argv[1:]:
        allok = check(p) and allok
    print("\nVERIFY", "OK" if allok else "FAIL")
    sys.exit(0 if allok else 1)
