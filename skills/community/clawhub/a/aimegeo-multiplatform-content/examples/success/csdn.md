---
platform: "csdn"
content_type: "tutorial"
title: "为青禾知识卡准备 CSV：用 Python 做本地导入前预检"
topic: "编码、必填列与单批行数检查"
fact_ids: ["F01", "F02", "F03", "F04", "F05", "F06"]
asset_ids: []
---

# 为青禾知识卡准备 CSV：用 Python 做本地导入前预检

准备品牌资料时，可以先用一个本地脚本检查文件结构，再交给写作者核对内容。本文依据青禾知识卡的演示规格编写预检代码，目标是发现编码、表头、空值和行数问题；不会连接产品后台，也不演示一个尚不存在的导入界面。

## 检查约定与环境

按本例规格，输入使用 UTF-8 编码的 CSV，允许 UTF-8 BOM；每批最多 200 行，表头不计入。title 和 source 为必填列，note 可选，额外列可以保留。每条记录须与表头列数相同，重复或空列名需要修正。

运行环境为 Python 3.10 或更高版本，只使用标准库。下面代码仅读取用户指定的 CSV 并打印检查结果，不访问 source 字段里的地址，也不修改原文件。

将以下代码保存为 `preflight.py`：

```python
import csv
import sys
from pathlib import Path


def inspect(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        columns = reader.fieldnames or []
        if not columns or any(not name.strip() for name in columns):
            raise ValueError("表头为空或包含空列名")
        if len(columns) != len(set(columns)):
            raise ValueError("表头有重复列名")
        if not {"title", "source"}.issubset(columns):
            raise ValueError("缺少必填列 title 或 source")
        count = 0
        for count, row in enumerate(reader, start=1):
            if count > 200:
                raise ValueError("超过单批上限 200 行，请按主题拆分")
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"第 {count} 条记录与表头列数不同")
            if not row["title"].strip() or not row["source"].strip():
                raise ValueError(f"第 {count} 条记录的 title 或 source 为空")
        if count == 0:
            raise ValueError("没有资料记录")
        return count


def main():
    if len(sys.argv) != 2:
        print("用法: python3 preflight.py materials.csv", file=sys.stderr)
        return 2
    try:
        count = inspect(sys.argv[1])
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 2
    print(f"OK: {count} 行；必填列 title、source 齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 准备一份可以复现的输入

将以下内容保存为 UTF-8 文件 `materials.csv`。它与本包附带文件一致，只包含演示资料，不涉及真实客户。

```csv
title,source,note
导入格式,青禾产品资料.md,使用 UTF-8 CSV
导入容量,青禾产品资料.md,每批最多 200 行
功能边界,青禾产品资料.md,不支持扫描件 OCR
```

source 中的资料名称供人回查，不是脚本要执行或访问的指令。字段含英文逗号时应使用 CSV 引号包住整个字段；不要为了让检查通过随意删掉正文中的标点或来源内容。

## 运行与判断结果

在保存这两个文件的目录执行：

```sh
python3 preflight.py materials.csv
```

上述输入的预期标准输出为：

```text
OK: 3 行；必填列 title、source 齐全
```

成功退出码是 0。如果删除 source 列再运行，标准错误为 `FAIL: 缺少必填列 title 或 source`，退出码为 2。保留列但把某条记录的 source 写成空格，也会失败，并指明记录序号。遇到编码错误，应从原资料重新导出 UTF-8 文件；不要用忽略解码错误的方式掩盖文字损坏。

如果达到 200 条资料记录，表头不会占用额度；第 201 条触发上限错误。拆分时保留相同表头并按主题安排记录，不要悄悄截断文件后把剩余资料当作已处理。预检只统计 CSV 记录数，带引号字段中的换行不会额外算成一条资料。

## 预检通过后还有什么要做？

这段代码不判断资料真实性，不证明 source 可访问，也不核实数字的统计口径。下一步仍应阅读实际资料，确认来源中有对应表述，再把有效事实交给写作任务。正文里的说明与脚本的成功结果不能混用。

本例不支持扫描件 OCR。扫描图应先完成独立的文字识别和人工复核，而不是把图片路径塞进 CSV 就期待自动提取。本例也不提供云端同步或自动发布；本教程只完成本地预检，不上传文件，不生成文章，也不取得平台回执。

资料依据：随附《青禾知识卡：离线演示产品规格》（QH-DEMO-1）。代码是为该规格独立编写的前置辅助工具，不是商业产品实现或实测证明。
