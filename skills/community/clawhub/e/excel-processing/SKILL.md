---
name: excel-processing
description: "Excel 处理——用 Python（openpyxl）批量新建、读取、筛选、追加、合并 .xlsx，不弄坏公式、日期和格式。当用户说「用Python处理Excel」「批量合并Excel」「公式读出来是None」「日期变成数字了」时使用。"
author: Captain
version: 0.1.0
display_name: "Excel 处理"
display_name_en: "Excel Processing"
description_zh: "Excel 处理：用 openpyxl 批量创建、读取、修改 .xlsx。七段本机跑通的代码覆盖新建带格式的表、按表头名筛选、追加行、写公式、日期写法、合并单元格与冻结窗格、多表合并；另列数字存成文本、日期变序列号、公式读成字符串、大文件内存等 8 个坑的症状和修法。"
description_en: "Batch-create, read, filter, append and merge .xlsx files with Python and openpyxl without breaking formulas, dates or formatting, with seven locally tested recipes and the eight most common pitfalls."
tags:
  - "Excel 处理"
  - "Excel"
  - "openpyxl"
  - "Python处理Excel"
  - "批量合并Excel"
  - "xlsx"
  - "表格自动化"
  - "办公自动化"
  - "spreadsheet"
examples_zh:
  - "用Python批量合并几十个Excel表，每个表列顺序还不一样"
  - "openpyxl写进去的公式，读出来怎么是None"
  - "Excel里的日期用Python读出来变成46289了"
---

# Excel 处理

定位一句话：**用代码改 Excel，难处不在读写，在于别把公式、日期、格式弄坏。** 下面每段代码都用 openpyxl 3.1.5、Python 3.12 在本机按顺序跑通过。

何时用：要用 Python 批量新建、读取、筛选、追加、合并 .xlsx；或者表格经过脚本处理后出了怪事，比如日期变成 46289、公式读出来是 None、合并单元格读成空。

## 先判断：文件、数据量、结果给谁

```
文件格式   .xlsx/.xlsm 直接处理；.xls 是老格式，openpyxl 打不开，先在 Excel 或 WPS 里另存为 .xlsx
里面有什么 有宏、图表、形状、表单控件的文件，只另存新文件，处理完在 Excel 里打开核对
数据量     几万行以内用普通模式；十万行以上，读用 read_only=True，写用 write_only=True
结果给谁   给人看：表头样式、冻结窗格、筛选按钮、列宽、数字格式都要做
           给程序读：一行一条记录，一列一个字段，不合并单元格，不夹小计行和空行
原件       永远另存为新文件，原件只读
```

检查点：动手前写下四样东西，输入文件和工作表名、表头在第几行、要输出什么、输出文件名。处理流程固定为五步：判断，挑下面对应的代码改，另存新文件，在 Excel 里打开核对，交付运行摘要。

## 七段代码：新建、筛选、追加、公式、日期、合并冻结、多表合并

每段存成一个 .py 文件，放在同一个文件夹里按编号顺序跑，后面几段要用到第一段生成的 sales.xlsx。先确认装了 openpyxl：`python3 -c "import openpyxl"` 不报错就行。

**① 新建带表头和格式的表**

```python
# 01_create.py 新建带表头和格式的表
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

rows = [(date(2026, 9, 1), "华东", "小王", 12, 358.5),
        (date(2026, 9, 2), "华南", "小李", 5, 1299),
        (date(2026, 9, 3), "华东", "小张", 30, 89.9)]
wb = Workbook()
ws = wb.active
ws.title = "明细"
ws.append(["日期", "区域", "销售", "数量", "单价", "金额"])
for r, row in enumerate(rows, start=2):
    ws.append([*row, f"=D{r}*E{r}"])                # 金额写成公式
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="305496")
    cell.alignment = Alignment(horizontal="center")
for r in range(2, ws.max_row + 1):
    ws.cell(r, 1).number_format = "yyyy-mm-dd"
    ws.cell(r, 5).number_format = ws.cell(r, 6).number_format = "#,##0.00"
for col, width in zip("ABCDEF", (12, 8, 8, 6, 10, 12)):
    ws.column_dimensions[col].width = width
ws.freeze_panes = "A2"                              # 冻结表头；写 "B2" 连第一列一起冻结
ws.auto_filter.ref = ws.dimensions                  # 表头加筛选按钮
wb.save("sales.xlsx")
print("已生成 sales.xlsx", ws.dimensions)
```

数字格式常用三种：`#,##0.00` 千分位两位小数，`0.0%` 百分比，`yyyy-mm-dd` 日期。颜色写 6 位十六进制。

**② 读取并按条件筛选**

```python
# 02_filter.py 按表头名读取、按条件筛选，结果另存
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")                    # 读到的是公式文本；要缓存值用 data_only=True
ws = wb["明细"]
header = [str(c.value).strip() for c in ws[1]]
col = {name: i for i, name in enumerate(header)}    # 按列名取值，列顺序变了也不怕
hits = [list(row) for row in ws.iter_rows(min_row=2, values_only=True)
        if row[col["区域"]] == "华东" and (row[col["数量"]] or 0) >= 10]
print("命中", len(hits), "行；金额列读到", repr(hits[0][col["金额"]]))

out = wb.create_sheet("华东10件以上")
out.append(header)
for row in hits:
    row[col["金额"]] = round(row[col["数量"]] * row[col["单价"]], 2)  # 公式搬家行号会错位，改写成数值
    out.append(row)
    out.cell(out.max_row, 1).number_format = "yyyy-mm-dd"
wb.save("sales_filtered.xlsx")                      # 另存，原件不动
```

按表头名建索引，别写死列号。含公式的行搬到别处行号会错位（原第 4 行的 `=D4*E4` 到了新表第 3 行，算的是空格子），所以这里写成数值。要保留公式就用 `openpyxl.formula.translate` 里的 Translator：`Translator("=D4*E4", origin="F4").translate_formula("F3")` 得到 `=D3*E3`。

**③ 追加行**

```python
# 03_append.py 接在最后一条真实数据后面追加，沿用上一行的格式
from copy import copy
from datetime import date
from openpyxl import load_workbook

wb = load_workbook("sales.xlsx")
ws = wb["明细"]
last = max(c.row for c in ws["A"] if c.value is not None)   # 不直接信 ws.max_row
new_rows = [(date(2026, 9, 4), "华南", "小李", 3, 1299),
            (date(2026, 9, 4), "华东", "小王", 20, 358.5)]
for r, values in enumerate(new_rows, start=last + 1):
    for c, v in enumerate([*values, f"=D{r}*E{r}"], start=1):
        cell, above = ws.cell(r, c, v), ws.cell(r - 1, c)
        cell.number_format, cell.font = above.number_format, copy(above.font)
ws.auto_filter.ref = f"A1:F{r}"
wb.save("sales_appended.xlsx")
print("写入第", last + 1, "到", r, "行")
```

`ws.max_row` 会被有格式的空行撑大：实测给 A200 设个数字格式，max_row 就变成 200，`ws.append` 会写到第 201 行，所以按关键列找最后一行。`append` 不带格式，要自己复制。中间插行要小心，`insert_rows` 不改公式引用、不挪合并区域（实测 `=SUM(A1:A2)` 插行后原样不动），宁可在末尾追加再排序。

**④ 写公式**

```python
# 04_formula.py 写公式，并亲眼看到 openpyxl 不算公式
from openpyxl import load_workbook
from openpyxl.utils import FORMULAE

wb = load_workbook("sales.xlsx")
ws = wb["明细"]
n = ws.max_row
ws[f"E{n + 1}"], ws[f"F{n + 1}"] = "合计", f"=SUM(F2:F{n})"
ws["G1"] = "大单"
for r in range(2, n + 1):
    ws[f"G{r}"] = f'=IF(F{r}>=1000,"是","否")'        # 英文函数名、英文逗号和引号
ws["I1"], ws["I2"] = "华东合计", '=SUMIFS(F:F,B:B,"华东")'
print("XLOOKUP 在 openpyxl 函数表里：", "XLOOKUP" in FORMULAE)  # False，要写成 =_xlfn.XLOOKUP(...)
wb.save("sales_formula.xlsx")
cached = load_workbook("sales_formula.xlsx", data_only=True)["明细"]
print("合计格的缓存值：", cached[f"F{n + 1}"].value)         # None，还没有软件算过它
```

openpyxl 只把公式文本写进文件，**自己不计算**，所以 `data_only=True` 读刚写的文件得到 None。它保存时默认带「打开时全部重算」标记（`wb.calculation.fullCalcOnLoad` 为 True），Excel 打开就会算。Python 这边要值，要么在 Python 里算好写数值，要么在 Excel 里打开保存一次再用 `data_only=True` 读。公式写英文函数名、英文逗号和引号；XLOOKUP、IFS、TEXTJOIN、FILTER 等新函数不在 openpyxl 的函数表里，按 openpyxl 文档要写成 `=_xlfn.XLOOKUP(...)`，否则 Excel 可能显示 #NAME?。

**⑤ 日期的正确写法**

```python
# 05_dates.py 日期的对与错；把读到的各种「日期」统一成 date
from datetime import date, datetime
from openpyxl import Workbook, load_workbook
from openpyxl.utils.datetime import from_excel

wb = Workbook()
ws = wb.active
ws["A1"] = date(2026, 9, 24)                        # 对：真日期，能排序、筛选、相减
ws["A1"].number_format = 'yyyy"年"m"月"d"日"'        # 只改显示，值还是日期
ws["A2"] = "2026-09-24"                             # 错：这是文本，按日期筛选时筛不到
ws["A3"] = 46289                                    # 别的系统导出的序列号，也是这一天
wb.save("dates.xlsx")


def to_date(v):
    """datetime、序列号、常见文本日期统一成 date；认不出来原样返回，留给人看"""
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, (int, float)) and 20000 < v < 80000:     # 约 1954 年到 2119 年
        return from_excel(v).date()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y年%m月%d日"):
        try:
            return datetime.strptime(str(v).strip(), fmt).date()
        except ValueError:
            pass
    return v


for c in load_workbook("dates.xlsx").active["A"]:
    print(c.coordinate, repr(c.value), "日期格式" if c.is_date else "非日期格式", "→", to_date(c.value))
```

写 `date` 或 `datetime` 对象，openpyxl 自动配 `yyyy-mm-dd`（datetime 配 `yyyy-mm-dd h:mm:ss`）；要显示成「2026年9月24日」只改 number_format，别转成字符串存。读回来一律是 datetime；格式被改成「常规」的日期读出来是 46289 这类序列号，用 `from_excel` 转；文本日期按几种常见写法逐个试，认不出的原样返回。

**⑥ 合并单元格与冻结窗格**

```python
# 06_merge_freeze.py 合并单元格、冻结窗格；读数据前先拆开再填满
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment

wb = Workbook()
ws = wb.active
for row in [["9 月各区域汇总"], ["区域", "城市", "金额"], ["华东", "杭州", 1200],
            ["华东", "苏州", 800], ["华南", "广州", 950]]:
    ws.append(row)
ws.merge_cells("A1:C1")                             # 标题横跨三列
ws["A1"].alignment = Alignment(horizontal="center")
ws.merge_cells("A3:A4")                             # 两个「华东」合成一格，只留左上角的值
ws.freeze_panes = "B3"                              # 冻结前两行和第一列
wb.save("merged.xlsx")

wb = load_workbook("merged.xlsx")
ws = wb.active
print("拆开前 A4 =", ws["A4"].value)
for rng in [r for r in ws.merged_cells.ranges if r.min_row >= 3]:   # 标题不动，只拆数据区
    value = ws.cell(rng.min_row, rng.min_col).value
    ws.unmerge_cells(str(rng))
    for row in ws.iter_rows(min_row=rng.min_row, max_row=rng.max_row,
                            min_col=rng.min_col, max_col=rng.max_col):
        for cell in row:
            cell.value = value
print("拆开后 A4 =", ws["A4"].value)
wb.save("merged_filled.xlsx")
```

合并后只有左上角有值，其他格变成只读的 MergedCell，读出来是 None，往里写会报 `AttributeError: 'MergedCell' object attribute 'value' is read-only`（实测）。要筛选、排序、汇总，先拆开填满。`freeze_panes = "B3"` 冻结的是 B3 上方的行和左侧的列。

**⑦ 多表合并成一张**

```python
# 07_combine.py 把 parts/ 下所有 .xlsx 的所有工作表，按表头名合并成一张
from datetime import date
from pathlib import Path
from openpyxl import Workbook, load_workbook

demo = {"华东": [["日期", "销售", "金额"], [date(2026, 9, 1), "小王", 358.5]],
        "华南": [["销售", "金额", "日期"], ["小李", 1299, date(2026, 9, 2)]],
        "华北": [["日期", "销售", "金额", "备注"], [date(2026, 9, 4), "小赵", 450, "补录"]]}
Path("parts").mkdir(exist_ok=True)                  # 演示数据：列顺序不同，一个多出「备注」
for name, rows in demo.items():
    part = Workbook()
    for row in rows:
        part.active.append(row)
    part.save(f"parts/{name}.xlsx")

columns, records = [], []
for path in sorted(Path("parts").glob("*.xlsx")):
    if path.name.startswith("~$"):                  # Excel 打开文件时留下的锁文件
        continue
    book = load_workbook(path, read_only=True, data_only=True)
    for sheet in book.worksheets:
        rows = sheet.iter_rows(values_only=True)
        header = [str(h).strip() if h is not None else "" for h in next(rows, ())]
        columns += [h for h in dict.fromkeys(header) if h and h not in columns]
        for row in rows:
            if any(v is not None for v in row):     # 跳过整行空白
                records.append({**dict(zip(header, row)), "来源": f"{path.stem}/{sheet.title}"})
    book.close()

out = Workbook()
ws = out.active
ws.append(columns + ["来源"])
for rec in records:
    ws.append([rec.get(h) for h in columns + ["来源"]])
    if "日期" in columns:
        ws.cell(ws.max_row, columns.index("日期") + 1).number_format = "yyyy-mm-dd"
ws.freeze_panes = "A2"
out.save("combined.xlsx")
print(len(records), "行；列：", columns + ["来源"])
```

按表头名对齐，不按列位置，列顺序不同、有的表多一列都能合；「来源」列用来追溯到文件和工作表。`data_only=True` 读到的是上次在 Excel 里保存时的缓存值，没被 Excel 保存过的文件公式列是 None。「金额」和「金额(元)」这类近似表头，先统一名字再合并，脚本不替你猜。

前七段一次跑完：

```bash
for f in 0[1-7]_*.py; do echo "== $f"; python3 "$f" || break; done
```

本机实测：② 打印出公式文本 '=D2*E2'，④ 打印 False 和 None，⑤ 三种写法都统一成 2026-09-24，⑥ 拆开前后 A4 分别是 None 和「华东」，⑦ 合并出 3 行 5 列。

## 最常见的 8 个坑

| # | 坑 | 症状 | 修法 |
|---|---|---|---|
| 1 | 数字存成文本 | 单元格左上角有绿三角，SUM 偏小，排序成 1、10、2 | 写入前转成数字（下面的 to_number）。工号、邮编要保留前导 0，故意存文本并设 `number_format = "@"`；身份证号 18 位，超过 Excel 的 15 位有效数字，必须存文本 |
| 2 | 日期变序列号或文本 | 读出 46289，或读出字符串 '2026-09-24' | 写 date 对象再配 number_format；读用 ⑤ 的 to_date |
| 3 | 公式读出来是字符串或 None | 默认读到 '=D2*E2'，data_only=True 读到 None | openpyxl 不算公式：在 Python 里算，或在 Excel 里打开保存后再读 |
| 4 | 大文件吃内存 | 几十万行时又慢又占内存 | 读用 read_only=True 逐行读、用完 close()；写用 write_only=True 只追加。实测 20 万行 2 列，普通模式读取峰值内存约 229 MB，read_only 约 49 MB |
| 5 | 覆盖原文件后东西没了 | 形状不见了，宏没了 | openpyxl 自带的警告写明形状和绘图读不进来，另存后会丢；.xlsm 要加 keep_vba=True。永远另存新文件，并在 Excel 里核对 |
| 6 | 合并单元格读成空 | 只有左上角有值，写入报 AttributeError | 先拆开填满，见 ⑥ |
| 7 | 数据追加到很远的地方 | 新数据出现在第 201 行甚至更远 | max_row 被有格式的空行撑大，按关键列找最后一行，见 ③ |
| 8 | .xls 打不开 | 报 InvalidFileException：openpyxl does not support the old .xls file format | 在 Excel 或 WPS 里另存为 .xlsx |

坑 1 和坑 4 的修法代码：

```python
# 08_pitfalls.py 文本数字转回数字；大文件用流式读写
import re
from openpyxl import Workbook, load_workbook


def to_number(v):
    """「1,234」「 88 」「12.5%」转成数字，转不了原样返回；工号、邮编、身份证号别过这个函数"""
    if isinstance(v, str):
        s = v.strip().replace(",", "").replace("，", "")
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d+(\.\d+)?%?", s):
            return float(s.rstrip("%")) / (100 if s.endswith("%") else 1)
    return v


print([to_number(v) for v in ["1,234", " 88 ", "12.5", "12.5%", "-3", "N/A"]])

big = Workbook(write_only=True)                     # 只写模式：只能 append，内存占用小
sheet = big.create_sheet("数据")
sheet.append(["序号", "金额"])
for i in range(1, 200001):
    sheet.append([i, i % 97])
big.save("big.xlsx")
book = load_workbook("big.xlsx", read_only=True)    # 只读模式：逐行流式读取，用完要 close
print("20 万行合计", sum(row[1] for row in book["数据"].iter_rows(min_row=2, values_only=True)))
book.close()
```

```bash
python3 08_pitfalls.py
```

本机输出 `[1234, 88, 12.5, 0.125, -3, 'N/A']` 和 `20 万行合计 9599502`，写加读 20 万行约 3 秒。

## 输出契约

1. **一个能直接跑的 .py**，只依赖 openpyxl 和标准库；开头注释写清输入文件、工作表、表头行、输出文件。
2. **只写新文件**，文件名带用途后缀（_filtered、_combined），原件不动。
3. **运行摘要**：读入多少行、写出多少行、跳过多少空行、哪些表头对不上、哪些单元格没能转成数字或日期（列出坐标，不悄悄吞掉）。
4. **公式提醒**：哪些列是公式，要在 Excel 里打开才看得到结果。
5. **抽查建议**：随机挑 3 行，和原表逐格对照。

## 边界与不做什么

- 只处理 .xlsx/.xlsm；.xls、.xlsb、Numbers 文件先用对应软件另存为 .xlsx。
- 不写 VBA 宏，不创建或修改透视表、切片器、图表、形状。
- 带打开密码的文件不处理，也不尝试破解；请用户在 Excel 里用自己的密码解除后另存。
- Excel 单个工作表最多 1,048,576 行、16,384 列，数据逼近上限时改用 CSV 或数据库。
- 只做数据整理，不替用户下财务、税务、审计结论，这些找对应的专业人员。
- 表里有身份证号、手机号等个人信息时只在本机处理，交付的样例、截图和日志要打码。
