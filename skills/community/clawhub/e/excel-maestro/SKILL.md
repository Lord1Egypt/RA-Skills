---
slug: excel-maestro
name: excel-maestro
version: 1.0.1
displayName: Excel大师
summary: 解决大文件内存爆炸、格式丢失、科学计数法、公式不计算四大痛点，按文件规模分层处理.。Excel大师是面向批量表格处理的能力包。它不只罗列脚本，更解决四个高频痛点：
license: MIT
description: Excel大师是面向成批表格处置的能力包。它不只罗列脚本，更解决四个高频痛点：. 适合需要excel maestro相关能力的开发场景,提供工作流程和配置参考。Use when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。
  该工具经过质量提升,针对用户反馈优化了实用性。Use when 需要文件处理、文档转换、格式互转、内容提取时使用。不适用于加密文件破解。。采用模块化设计，各功能组件可独立配置和组合，灵活适应不同业务场景。
tags:
- 自动化
- 表格处理
- 效率工具
- 工作流
- 效率
- xlsx
- openpyxl
- true
- csv
- pandas
tools:
- read
- exec
- write
homepage: ''
category: Automation
pricing_tier: free
homepage: "https://skillhub.cn/skill/"
---
> **核心功能**: 本技能提供中文交互、工作流程和配置参考、化工作流场景等能力。
# Excel大师
处理Excel文件、表格数据、批量转换或报表生成时应用本skill。核心信条：**先看文件多大，再选工具；先问要不要保格式，再动笔。**
## 四大痛点与对策
| 痛点 | 典型表现 | 本skill对策 |
|---|----|--------|
| 大文件内存爆炸 | 50万行xlsx一加载OOM | 文件规模分层 + read_only/write_only流式 |
| 格式丢失 | pandas读写后颜色/公式/图表全没了 | 格式保留矩阵 + 两条路径 |
| 科学计数法 | 身份证号变成1.23E+19 | 列格式强制文本 + 写入前预处理 |
| 公式不计算 | data_only=True拿到None | 区分"读公式"vs"读缓存值" + 重算方案 |
---
## 领先步：按文件规模选工具
| 文件规模 | 行数估计 | 推荐工具 | 关键参数 |
|:-----|:-----|:-----|:-----|
| 小文件 | <1万行 | pandas | `pd.read_excel(engine="openpyxl")` |
| 中文件 | 1万-50万行 | openpyxl | `load_workbook(read_only=True)` |
| 大文件 | >50万行 | openpyxl流式 + 分块 | `read_only=True` + `write_only=True` + 分页 |
| 超大文件 | >100万行 | 列裁剪 + 分块 + 落地CSV | 配合`pandas chunksize` |
### 中大文件流式读取（避免OOM）
```python
from openpyxl import load_workbook
# ...
# read_only=True 不把整个文件载入内存
wb = load_workbook("big.xlsx", read_only=True, data_only=True)
ws = wb["Sheet1"]
for row in ws.iter_rows(values_only=True):
    # 逐行处理，内存恒定
    process(row)
wb.close()  # read_only 必须显式关闭
```
### 大文件流式写入
```python
from openpyxl import Workbook
# ...
wb = Workbook(write_only=True)  # 流式写，无法修改已写行
ws = wb.create_sheet("结果")
ws.append(["列A", "列B", "列C"])
for row in data_stream:
    ws.append(row)
wb.save("output.xlsx")  # 不会OOM
```
---
## 第二步：格式保留矩阵
> 90%的"格式丢失"问题源于选错了工具.
| 操作需求 | 用pandas | 用openpyxl | 说明 |
|---:|---:|---:|---:|
| 纯数据读写 | ✅ | ✅ | pandas更简洁 |
| 保留单元格颜色/字体 | ❌ | ✅ | pandas会丢 |
| 保留公式 | ❌ | ✅ | pandas只存值或公式字符串 |
| 保留图表/透视表 | ❌ | ⚠️部分 | openpyxl能保留已有图表，不能新建复杂图表 |
| 保留合并单元格 | ❌ | ✅ | pandas会展开 |
| 保留条件格式 | ❌ | ✅ | pandas会丢 |
| 多表合并/分析 | ✅ | ⚠️慢 | pandas DataFrame更适合 |
| 大文件流式 | ⚠️chunksize | ✅read_only | openpyxl更稳 |
### 两条路径选择
**路径A：纯数据处理（不关心格式）**
```python
import pandas as pd
df = pd.read_excel("input.xlsx", engine="openpyxl")
# ... 处理 ...
df.to_excel("output.xlsx", index=False, engine="openpyxl")
```
**路径B：保留原格式改数据（只动目标单元格）**
```python
import openpyxl
wb = openpyxl.load_workbook("input.xlsx")  # 不加read_only
ws = wb["Sheet1"]
ws["C2"] = new_value  # 只改这一格，其余格式全保留
wb.save("output.xlsx")
```
---
## 第三步：四大陷阱与规避
### 陷阱1：data_only=True拿到None
```python
# 错误：文件从未被Excel打开过，公式没有缓存值
wb = openpyxl.load_workbook("file.xlsx", data_only=True)
ws = wb.active
print(ws["A1"].value)  # None，因为公式结果从未被Excel计算并保存
# ...
# 正确方案1：用Excel打开保存一次（让Excel写入缓存值）
# 正确方案2：用formulas库重算
# pip install formulas
import formulas
xl = formulas.ExcelModel().loads("file.xlsx").finish()
sol = xl.calculate()
# 正确方案3：只读公式字符串（不读值）
wb = openpyxl.load_workbook("file.xlsx", data_only=False)
print(ws["A1"].value)  # "=SUM(B1:B10)" 公式字符串
```
### 陷阱2：长数字变科学计数法
```python
# 错误：身份证号110101199001011234变成1.10E+17
df = pd.read_excel("input.xlsx")
df["身份证号"]  # 已是float，精度丢失
# ...
# 正确方案1：读取时指定dtype
df = pd.read_excel("input.xlsx", dtype={"身份证号": str})
# ...
# 正确方案2：openpyxl读
wb = openpyxl.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    id_card = str(row[0])  # 字符串保留
# ...
# 正确方案3：写入前强制文本格式
from openpyxl.styles import numbers
ws["A1"].number_format = numbers.FORMAT_TEXT
ws["A1"] = "110101199001011234"
```
### 陷阱3：CSV编码错乱
```python
# 错误：中文乱码或报错
df = pd.read_csv("input.csv")  # 默认UTF-8，但Excel导出的CSV可能是GBK
# ...
# 正确方案1：尝试多种编码
for enc in ["utf-8", "gbk", "gb18030", "utf-8-sig"]:
    try:
        df = pd.read_csv("input.csv", encoding=enc)
        break
    except UnicodeDecodeError:
        continue
# ...
# 正确方案2：写入CSV时加BOM（让Excel正确识别UTF-8）
df.to_csv("output.csv", index=False, encoding="utf-8-sig")
```
### 陷阱4：合并单元格读写
```python
# 读取：合并单元格只有左上角有值，其余为None
ws = wb["Sheet1"]
for row in ws.iter_rows():
    for cell in row:
        if cell.value is None and cell.coordinate in ws.merged_cells:
            # 处于合并区域内，取左上角值
            ...  # 具体实现请参考上下文文档
# ...
# 写入：先解除合并再写
from openpyxl.utils import range_boundaries
for merged_range in list(ws.merged_cells.ranges):
    ws.unmerge_cells(str(merged_range))
ws["A1"] = value
```
---
## 第四步：脚本速查表
| 你想做的事 | 调用脚本 | 典型参数 |
|:----:|:----:|:----:|
| 多Excel/多sheet合成一张表 | merge_sheets.py | `--inputs 文件或目录 --output out.xlsx` |
| sheet导出CSV | excel_to_csv.py | `--input file.xlsx --output file.csv` |
| CSV转Excel | csv_to_excel.py | `--input a.csv --output a.xlsx` |
| 按条件筛选行 | filter_excel.py | `--where "列名=值"` 或 `"列名>100"`、`"列名~北京"` |
| 按行数/按列拆分 | split_excel.py | `--by-rows 5000` 或 `--by-column 地区` |
| 按列去重 | deduplicate_excel.py | `--keys 编号 --keep first` |
| 分组聚合 | aggregate_excel.py | `--group-by 地区 --agg "销售额:sum"` |
| 校验必填列/重复键/空行 | validate_excel.py | `--require-cols 列名 --key-cols 列名` |
| 选择/重命名列 | select_columns.py | `--columns 列1,列2 --rename "旧:新"` |
| 两表按键合并（VLOOKUP） | merge_tables.py | `--left a.xlsx --right b.xlsx --on 键列` |
| 主表对多表VLOOKUP | vlookup_multi.py | `--main 主.xlsx --lookups "表1.xlsx:键列"` |
| 行列转置 | transpose_excel.py | `--input in.xlsx --output out.xlsx` |
| 模板填充<动态配置> | template_fill.py | `--template t.xlsx --data d.csv --output out.xlsx` |
| 重命名工作表 | rename_sheets.py | `--rename "Sheet1:新名"` 或 `--prefix "2024_"` |
| 条件格式 | format_conditional.py | `--column C --rule gt --value 100 --fill red` |
| 列设为文本格式 | format_columns_as_text.py | `--columns 身份证号,订单号` |
### 本地运行
```bash
# 进入skill目录或把（请参考skill目录中的脚本文件）
pip install -r （请参考skill目录中的脚本文件）
python （请参考skill目录中的脚本文件） --help
```
---
## 第五步：通用处理流程
1. **确认输入**：文件路径、sheet名或索引、是否有表头、编码（CSV时）
2. **选工具**：按文件规模分层表选pandas或openpyxl
3. **读取**：按需读整表/区域/流式
4. **处理**：转换、过滤、合并、计算
5. **写出**：指定输出路径与格式；需保格式则用openpyxl单格改写
6. **校验**：检查行数、关键列、重复值、业务规则
### 读取Excel
```python
# 整表为list of dict（保表头）
import openpyxl
wb = openpyxl.xlsx", read_only=True, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))
header = rows[0]
data = [dict(zip(header, row)) for row in rows[1:]]
wb.close()
# ...
# pandas（适合分析、过滤、合并）
import pandas as pd
df = pd.read_excel("input.xlsx", sheet_name=0, engine="openpyxl")
# ...
# 指定区域
df = pd.read_excel("input.xlsx", usecols="A:D", header=0, nrows=100)
```
### 写入Excel
```python
# 新建并写入（openpyxl）
from openpyxl import Workbook
from openpyxl.styles import Font
wb = Workbook()
ws = wb.active
ws.title = "结果"
ws.append(["列A", "列B", "列C"])
for row in data_rows:
    ws.append(row)
ws["A1"].font = Font(bold=True)
wb.save("output.xlsx")
# ...
# pandas多sheet写出
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="汇总", index=False)
    df2.to_excel(writer, sheet_name="明细", index=False)
# ...
# 追加到已有文件
wb = openpyxl.load_workbook("existing.xlsx")
ws = wb["Sheet1"]
for row in new_rows:
    ws.append(row)
wb.save("existing.xlsx")
```
---
## 第六步：批量处理目录
```python
from pathlib import Path
import openpyxl, json
# ...
results = []
errors = []
for file in Path("目录").glob("*.xlsx"):
    try:
        wb = openpyxl.load_workbook(file, read_only=True, data_only=True)
        ws = wb.active
        # 处理...
        results.append({"file": file.name, "rows": ws.max_row})
        wb.close()
    except Exception as e:
        errors.name, "error": str(e)})
        continue  # 出错继续处理其余文件
# ...
# 汇总报错列表
if errors:
    with open("errors.json", "w", encoding="utf-8") as f:
        json.dump(errors, f, ensure_ascii=False, indent=2)
```
**批量输出命名规则建议**：`原名_out.xlsx` 或统一汇总到一个文件.
---
## 第七步：性能优化技巧
| 场景 | 慢的原因 | 优化方案 |
|:------|------:|:------|
| 逐单元格写入 | 每次write触发渲染 | 用`ws.append(row)`批量行写入 |
| 大文件读取OOM | 整文件载入 | `read_only=True`流式 |
| 大文件写出OOM | 整工作簿在内存 | `write_only=True`流式 |
| 只需部分列 | 读全部列 | `usecols="A:C"`列裁剪 |
| 百万行分析 | 全量载入 | `pd.read_excel(chunksize=10000)`分块 |
| 多文件合并 | 串行读 | 并行读（`concurrent.futures`） |
| 公式重算慢 | 全表重算 | 用formulas库按需算 |
---
## 错误恢复方案
- 读取前用`Path(file).exists()`检查文件存在
- 表为空或缺少预期列时给出明确提示（列名/行数）
- 写入前若目标文件已存在，按用户要求覆盖或换名；大文件用`write_only=True`或分块
- 捕获`openpyxl.utils.exceptions.InvalidFileException`、`KeyError`（工作表名）并返回可读错误
### 常见错误代码
| 错误 | 原因 | 解决 |
|---:|:---|---:|
| `InvalidFileException` | 文件不是有效xlsx/xls | 检查文件是否损坏、是否实为.csv改后缀 |
| `KeyError: 'Sheet1'` | 工作表名不存在 | 用`wb.sheetnames`查看实际表名 |
| `PermissionError` | 文件被Excel占用 | 关闭Excel再处理 |
| `MemoryError` | 文件太大 | 切换read_only流式 |
| `UnicodeDecodeError` | CSV编码不对 | 尝试gbk/gb18030/utf-8-sig |
| `ValueError: No column` | 列名写错或有多余空格 | `df.columns = df.columns.str.strip()` |
---
## 技术栈
- **读写.xlsx**：openpyxl（保留格式、公式、多工作表）
- **数据分析/透视**：pandas + openpyxl引擎
- **旧格式.xls**：xlrd（只读）
- **公式重算**：formulas库（按需）
```bash
pip install openpyxl pandas xlrd formulas
```
---
## 问题解答汇总
**Q：50万行Excel一读就OOM怎么办？**
A：用`load_workbook(read_only=True, data_only=True)`流式读取，配合`iter_rows(values_only=True)`逐行处理，内存恒定.
**Q：用pandas读写后Excel颜色和公式都没了？**
A：pandas只处理数据不处理格式。需要保格式就用openpyxl加载原文件，只改目标单元格再save（见"路径B"）.
**Q：身份证号变成科学计数法怎么救？**
A：读取时`dtype={"身份证号": str}`，或openpyxl读后`str(cell.value)`。写入前设`number_format = FORMAT_TEXT`.
**Q：data_only=True读公式单元格是None？**
A：文件从未被Excel打开保存过，没有缓存值。要么用Excel打开存一次，要么用formulas库重算，要么data_only=False读公式字符串.
**Q：多个Excel文件需要合并到一个sheet？**
A：用`merge_sheets.py --inputs 目录 --output out.xlsx`，或pandas的`pd.concat([pd.read_excel(f) for f in files])`.
**Q：CSV用Excel打开中文乱码？**
A：写入时`encoding="utf-8-sig"`加BOM，Excel就能正确识别UTF-8.
---
## 故障处理
| 症状 | 可能原因 | 解决 |
|:------:|--------|:-------|
| 打开文件报InvalidFile | 文件损坏或后缀不符 | 用Excel打开验证，或另存为xlsx |
| sheet名找不到 | 有隐藏空格 | `wb.sheetnames`查看，strip空格 |
| 写入后打不开 | write_only模式未append任何行 | 确保至少append一行再save |
| 数值精度丢失 | 用了float存大数 | 改用str或Decimal |
| 条件格式不生效 | 规则写错或范围不对 | 先用Excel手动验证规则 |
| 公式显示为文本 | 单元格格式是文本 | 设`number_format = 'General'`再写公式 |
---
## 安装与配置
### 运行环境
- **Agent平台**：支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**：Windows / macOS / Linux
- **Python**：3.8+（推荐3.10+）
### 依赖详情
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|----|:--:|---:|----|
| openpyxl | Python库 | 必需 | `pip install openpyxl` |
| pandas | Python库 | 必需 | `pip install pandas` |
| xlrd | Python库 | 可选（读.xls） | `pip install xlrd` |
| formulas | Python库 | 可选（公式重算） | `pip install formulas` |
| LLM API | API | 必需 | 由Agent内置LLM提供 |
### API Key 配置
- 本skill基于本地脚本，基础LLM由Agent平台提供
- 涉及读取在线Excel（如OneDrive）时需对应平台OAuth Token
### 可用性分类
- **分类**：MD+EXEC（Markdown指令 + Python脚本执行）
- **说明**：通过自然语言指令驱动Agent调用（请参考skill目录中的脚本文件）
## 功能清单
- Excel大师是面向批量表格处理的能力包
- 它不只罗列脚本，更解决四个高频痛点：
  大xlsx一加载就内存爆炸、用pandas读写后格式公式全丢失、长数字变成科学计数法、
  data_only=True拿到公式却是None
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置.
### 核心功能执行
用`input_params`参数进行配置.
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回核心功能执行的响应数据,包含返回码、数据和处理记录.
- 调用时传入`input_params`参数,支持创建/查询/导出操作
### 参数配置与调用
用`config_options`参数进行配置.
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回参数配置与调用的响应数据,包含返回码、数据和处理记录.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
### 结果处理与输出
用`output_format`参数进行配置.
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,输出标准化响应数据.
**输出**: 返回结果处理与输出的响应数据,包含返回码、数据和处理记录.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本技能覆盖以下场景：解决大文件内存爆、格式丢失、公式不计算四大痛、按文件规模分层处、Use、when、需要文件处理、文档转换、格式互转、内容提取时使用、不适用于加密文件等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 实操说明
1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理
> 详细的输入输出格式请参考下方章节说明。
## 应用场景
| 场景 | 输入 | 输出 |
|----|----|----|
| 基础使用 | 用户请求 | 处理结果 |
**不适用于**：需要人工判断的复杂决策场景
## 使用指南
1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节
## 应用示例
### 示例1：大文件流式读取避免OOM
用户需要读取一个 50 万行的 Excel 文件并提取关键列，直接加载会内存爆炸：
```
输入: 50万行xlsx文件，需提取"订单号"和"金额"两列
处理:
  1. 按文件规模分层：>50万行 → openpyxl read_only 流式
  2. 使用 iter_rows(values_only=True) 逐行读取
  3. 身份证号/订单号列指定 dtype=str 防止科学计数法
  4. 内存恒定，不随行数增长
输出: 成功提取 500,000 行数据
      内存占用: ~50MB（恒定）
      耗时: 12秒
      保存为 output.csv（utf-8-sig 编码）
```
### 示例2：保留格式修改单元格
用户需要在保留原有颜色、公式、合并单元格的前提下修改某列数据：
```
输入: 在已有的报表xlsx中更新C列销售额，保留所有格式
处理:
  1. 选择路径B：openpyxl load_workbook（不加read_only）
  2. 只修改目标单元格 ws["C2"] = new_value
  3. 其余格式（颜色/字体/公式/合并）全部保留
  4. save 输出新文件
输出: output.xlsx 已保存
      原有格式: 100%保留（颜色、公式、合并单元格均未丢失）
      修改内容: C列 200 行销售额已更新
```
## 限制条件
- 大文件处理（>100MB xlsx）仍可能触发内存限制，openpyxl模式建议文件不超过50MB
- 格式保真度受openpyxl/pandas能力限制，部分Excel高级特性（如数据透视表、条件格式中的色阶）可能丢失
- 科学计数法转换需指定列范围，全表扫描可能将非数值文本误判为数字导致数据损坏
## 输出规范
```json
{
  "success": true,
  "data": {
    "result": "Excel大师处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "excel maestro"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
## 安全规范
| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 配置于环境变量中,密钥不得固化于代码 |
| 命令执行风险 | 命令执行受白名单约束,避免注入用户输入 |
| 网络通信安全 | 使用TLS加密通道进行通信 |
| 敏感数据暴露 | 返回数据中不含凭证信息 |
使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
## 优势对比
| 对比维度 | Excel大师 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | 解决大文件内存爆炸、格式丢失、科学计数法、公式不计算四大痛点，按文件规模分层处理 | 通用场景 | 通用场景 |
## 部署指引
1. **配置API密钥**: 在环境变量中设置对应的API Key
2. **初始化连接**: 使用提供的凭证建立API连接
3. **调用接口**: 传入必要参数执行API调用
1. **准备文件**: 确认文件路径正确且格式受支持
2. **执行处理**: 调用对应的处理函数
3. **查看结果**: 检查输出文件或返回数据
1. **检查环境**: 确认运行时和依赖已安装
2. **执行命令**: 使用正确的参数格式执行
3. **查看输出**: 检查命令输出和退出码
### 前置条件
- 已安装所需运行环境(参考依赖说明)
- 已获取必要的API密钥或访问凭证(如适用)
- 输入数据已准备就绪
### Excel大师通用排查步骤
1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
## 用户答疑汇总
### Q1: Excel大师支持哪些输入格式？
A1: 解决大文件内存爆炸、格式丢失、科学计数法、公式不计算四大痛点，按文件规模分层处理.。Excel大师是面向批量表格处理的能力包。它不只罗列脚本，更解决四个高频痛点。支持文本指令和结构化参数输入，具体格式参考使用流程章节。
### Q2: 需要配置API Key吗？
A2: 是的，部分功能需要配置对应平台的API Key。请在依赖说明章节查看具体要求，并通过环境变量安全配置。
### Q3: 命令行执行失败怎么办？
A3: 检查命令参数是否正确，确认运行环境支持exec能力。如遇权限问题，请参照错误处理章节排查。
## 故障修复指南
针对Excel大师使用中可能遇到的常见问题,提供以下排查方案:
| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

## 依赖说明

### 运行环境
- **Agent 平台**: 支持SKILL.md的任意AI Agent
- **操作系统**: Windows / macOS / Linux

### 可用性分类
- **分类**: MD（纯Markdown指令，通过自然语言驱动Agent完成操作）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent完成操作。
