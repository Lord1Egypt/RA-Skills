#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""unpack.py — 把一枚样容器（`samples/<名>.json`）铺回 runner 要的形状。零网络、纯 stdlib。

    python3 unpack.py <样容器.json> <落点根目录>      # 铺一枚，打印铺出的目录
    python3 unpack.py --all <fixtures 目录> <落点根>   # 铺全量

**生成器的等价自证与 runner 用的是同一枚函数**（`materialize()`）：容器形制与散件形制
由同一处代码保证不分家——两处各写一遍铺法，迟早一副真一副假。

容器是**纯文本**（ASCII-only JSON）：渠道对包内扩展名有白名单，二进制档案（tar/zip 一族）
属拒收面，所以语料并进样文件、共享件留在 `_shared/` 以允许类型散放，不再封档。
"""
from __future__ import annotations

import json
import pathlib
import sys

FIELDS = (("cmd.txt", "cmd_raw"), ("expect.txt", "expect_raw"), ("shared.txt", "shared_raw"))


def materialize(sample: pathlib.Path, dest_root: pathlib.Path) -> pathlib.Path:
    """铺一枚样。返回该样目录。键缺一个即报错——容器写坏了不算「样本来就这样」。

    【M250】容器顶层不是对象（数组／字符串／数字／布尔／null 五形）时走可读句、不抛 Traceback：
    点名是哪枚容器、实收到什么类型；措辞与本件既有出口同族（`容器铺回失败：…`）。
    正常路径（对象容器）行为一字未改。
    """
    s = json.loads(sample.read_text(encoding="utf-8"))
    if not isinstance(s, dict):
        raise ValueError(f"顶层是 JSON {type(s).__name__}，本件只收对象（一枚样一个容器对象）")
    name = s["name"]
    d = dest_root / name
    d.mkdir(parents=True, exist_ok=True)
    for rel in s.get("dirs", []):
        (d / rel).mkdir(parents=True, exist_ok=True)
    for key, field in FIELDS:
        if field in s:
            (d / key).write_text(s[field], encoding="utf-8")
    for rel, text in sorted(s.get("files", {}).items()):
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return d


def laid_files(root: pathlib.Path) -> dict:
    return {f.relative_to(root).as_posix(): f for f in sorted(root.rglob("*")) if f.is_file()}


def main(argv) -> int:
    if len(argv) >= 2 and argv[0] == "--all":
        fix, dest = pathlib.Path(argv[1]), pathlib.Path(argv[2])
        dest.mkdir(parents=True, exist_ok=True)
        n = 0
        for sp in sorted((fix / "samples").glob("*.json")):
            try:
                materialize(sp, dest)
            except Exception as e:
                # 失败也要可复现：只报**包内相对名**，不把临时根印进 runner 的输出（双跑不可 diff）
                print(f"容器铺回失败：samples/{sp.name}（{type(e).__name__}: {str(e)[:120]}）", file=sys.stderr)
                return 1
            n += 1
        return 0                        # 成功态零输出：runner 的报账面必须与散件时代逐字节同
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        out = materialize(pathlib.Path(argv[0]), pathlib.Path(argv[1]))
    except ValueError as e:                     # 非对象容器／坏 JSON：一句人话＋退码 1，不抛 Traceback
        print(f"容器铺回失败：{argv[0]}（{type(e).__name__}: {str(e)[:160]}）", file=sys.stderr)
        return 1
    print(out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
