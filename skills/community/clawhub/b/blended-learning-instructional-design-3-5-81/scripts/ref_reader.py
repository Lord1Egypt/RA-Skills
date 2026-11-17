# -*- coding: utf-8 -*-
"""
混合式教学设计创新大赛参赛小帮手 · 参考资料读取器

用途
----
本技能的参考资料（方法论、布卢姆动词表、字段说明、常见问题、产物预览、页脚说明）
统一存放在 references/ 目录下，以专用格式保存，**不能用普通文件读取工具直接打开**。
本脚本负责把它们还原为可阅读、可复制的 JSON / Markdown 文本。

用法（在技能根目录执行）
------------------------
    python scripts/ref_reader.py                      # 列出全部可读取的参考资料
    python scripts/ref_reader.py methodology          # 输出指定资料的 JSON 原文
    python scripts/ref_reader.py methodology --md     # 输出为 Markdown，更易读
    python scripts/ref_reader.py faq --out D:/tmp/faq.json   # 存为文件后再查看
    python scripts/ref_reader.py methodology bloom_reference # 一次读多份

参数说明
--------
    <名称>        参考资料名称，可省略 .json 后缀
                  （methodology / bloom_reference / design_plan_guide / faq
                   / output_preview / footer_note）
    --md          以 Markdown 文本输出（默认输出 JSON）
    --out <路径>  把结果写入指定文件，而不是打印到屏幕
    --list        仅列出可读取的参考资料
    --help        显示本说明

运行环境
--------
仅需 Python 3.7 及以上，不依赖任何第三方库。
Windows 一般用 python，macOS / Linux 一般用 python3。

什么时候读什么
--------------
- 撰写 design_data.json 各栏内容之前：读 design_plan_guide、methodology（按需分节）。
- 撰写「学习目标」时：读 bloom_reference。
- 想先了解生成出来的文档长什么样：读 output_preview。
- 出现报错，或使用者提出疑问时：读 faq。
- 需要查看 / 修改页脚署名、版权、费用提示文字时：读 footer_note。

读取失败怎么办
--------------
- 提示「找不到 python / python3」：电脑尚未安装 Python 3.7 及以上，安装后重试。
- 提示「找不到参考资料」：名称拼写有误，先不加参数运行本脚本可列出全部名称。
- 提示「文件损坏 / 完整性校验未通过」：技能包不完整或被改动，重新安装本技能即可恢复。
- 无论何种原因，都不要因为读取失败就跳过参考资料、凭经验生成内容。
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _refs  # noqa: E402

EXIT_OK = 0
EXIT_READ_FAIL = 1
EXIT_BAD_ARGS = 2


def list_refs():
    out = ["可读取的参考资料（在技能根目录执行）：", ""]
    for name, desc in _refs.REF_ITEMS:
        mark = "" if _refs.exists(name) else "（文件缺失）"
        out.append("  python scripts/ref_reader.py %-17s %s%s" % (name, desc, mark))
    out.append("")
    out.append("加 --md 可输出 Markdown 格式；加 --out <路径> 可保存为文件。")
    return "\n".join(out)


def read_one(name, as_md):
    """读取一份资料，返回文本。"""
    data = _refs.load(name)
    if as_md:
        return _refs.to_markdown(data)
    return json.dumps(data, ensure_ascii=False, indent=2)


def main(argv):
    as_md = False
    out_path = None
    names = []
    i = 1
    while i < len(argv):
        a = argv[i]
        if a in ("--md", "-m"):
            as_md = True
        elif a in ("--out", "-o"):
            i += 1
            if i >= len(argv):
                print("缺少 --out 后面的文件路径。")
                print("示例：python scripts/ref_reader.py faq --out D:/tmp/faq.json")
                return EXIT_BAD_ARGS
            out_path = argv[i]
        elif a in ("--list", "-l", "list"):
            print(list_refs())
            return EXIT_OK
        elif a in ("--help", "-h"):
            print(__doc__)
            return EXIT_OK
        elif a.startswith("-"):
            print("无法识别的参数：%s" % a)
            print("查看用法：python scripts/ref_reader.py --help")
            return EXIT_BAD_ARGS
        else:
            names.append(a)
        i += 1

    if not names:
        print(list_refs())
        return EXIT_OK

    chunks = []
    for name in names:
        try:
            chunks.append(read_one(name, as_md))
        except _refs.RefMissing:
            print("找不到参考资料「%s」。当前可读取的参考资料如下：" % name)
            print()
            print(list_refs())
            return EXIT_READ_FAIL
        except _refs.RefError as e:
            print("参考资料「%s」读取失败：%s" % (name, e))
            print("请确认技能包完整、未被改动；若仍失败，重新安装本技能即可恢复。")
            return EXIT_READ_FAIL

    text = "\n\n".join(chunks)
    if out_path:
        try:
            parent = os.path.dirname(os.path.abspath(out_path))
            if parent and not os.path.isdir(parent):
                os.makedirs(parent, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print("写入文件失败：%s" % e)
            print("请换一个可写入的路径后重试。")
            return EXIT_READ_FAIL
        print("已写入：%s" % out_path)
    else:
        print(text)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv))
