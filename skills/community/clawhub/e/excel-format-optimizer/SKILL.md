---
name: excel-format-optimizer
description: "Excel 格式优化工具：提升字体可读性、统一边框样式、调整列宽行高和缩放比例。当用户提到 Excel 字体太小、阅读体验差、边框太丑、格式需要美化、表格不好看时触发。适用于 Windows 桌面端阅读场景。"
---

# Excel 格式优化器

针对已有 Excel 文件进行格式优化，重点解决 **字体太小、边框不统一、列宽不合理、无缩放设置** 等桌面端阅读体验问题。

## 适用场景

- 用户收到他人制作的 Excel，字体太小看不清
- 表格边框风格混乱（有的有框有的没框、粗细不一）
- 需要统一字体、字号、列宽、行高
- 需要调整缩放比例和视图设置

## 前置条件

### openpyxl 安装

openpyxl 通常不在默认环境中，需要安装：

```bash
# 国内环境 pypi.org 经常超时，直接用清华镜像
cd "C:\Users\17551\.workbuddy\binaries\python\envs\default"
./Scripts/pip.exe install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 30
```

### Python 运行时

使用 managed Python（非系统 Python）：

```
C:\Users\17551\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

## 工作流程

### 第 1 步：诊断现有格式

先读取文件，全面了解当前格式状态，**不要跳过这一步直接改**：

```python
import openpyxl

wb = openpyxl.load_workbook(path)
for sn in wb.sheetnames:
    ws = wb[sn]
    # 检查：max_row, max_column, merged_cells
    # 检查：column_dimensions（列宽）
    # 检查：row_dimensions（行高）
    # 检查：每个单元格的 font（name, size, bold, color）
    # 检查：每个单元格的 alignment（horizontal, vertical, wrap_text）
    # 检查：fill（start_color, patternType）
    # 检查：border（left/right/top/bottom 的 style）
    # 检查：sheet_view.zoomScale, freeze_panes
```

**关键检查项：**
1. 字体大小分布（找出最小和最大字号）
2. 字体是否混用（如 Aptos + 宋体）
3. 哪些列没有设置宽度（会显示默认窄列）
4. 边框风格是否统一（thin/medium 混用、部分单元格无框）
5. 是否有合并单元格（修改时需特别注意）
6. 是否有公式（必须保留，不能误删）

### 第 2 步：制定优化方案

根据诊断结果，确定优化策略。以下是推荐默认值：

#### 字体优化

| 原字号 | 新字号 | 说明 |
|--------|--------|------|
| >= 18  | 22     | 主标题 |
| >= 16  | 18     | 小标题/总分 |
| >= 10  | 12     | 正文 |
| >= 9   | 11     | 脚注 |
| < 9    | 12     | 异常小字 |

- **Windows 环境**：统一字体为 `微软雅黑`（渲染清晰、兼容性好）
- **Mac 环境**：统一字体为 `PingFang SC`

#### 列宽优化

- 根据 sheet 内容和列数，为每一列设置合理宽度
- **必须检查**：有些列在原文件中没有设置 `column_dimensions`，需要手动补齐
- 正文列宽度建议 20-30，长文本列 50-100，编号/序号列 8-12

#### 行高优化

- 按原行高 × 1.25 放大（适配更大字号）
- 如原行高未设置（None），给默认值 20

#### 缩放比例

- 设为 110%（`sheet_view.zoomScale = 110`）

#### 冻结窗格（谨慎使用）

- **重要教训**：冻结窗格可能导致用户打开文件后体验异常（冻结行数过多占屏）
- 如需设置，只冻结表头行（1-2 行），不要冻结多行
- **建议默认不设置**，除非用户明确要求

### 第 3 步：执行优化

```python
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from copy import copy

wb = openpyxl.load_workbook(src)

TARGET_FONT = '微软雅黑'  # Windows

def new_font_size(old_size):
    if old_size >= 18:
        return 22
    elif old_size >= 16:
        return 18
    elif old_size >= 10:
        return 12
    elif old_size >= 9:
        return 11
    else:
        return 12

for sn in wb.sheetnames:
    ws = wb[sn]

    # 1. 遍历所有单元格，更新字体和字号
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, max_col=ws.max_column):
        for cell in row:
            f = cell.font
            cell.font = Font(
                name=TARGET_FONT,
                size=new_font_size(f.size),
                bold=f.bold,
                italic=f.italic,
                color=f.color.rgb if f.color else 'FF222222',
                underline=f.underline,
                strike=f.strike,
                vertAlign=f.vertAlign
            )
            # 保留原有对齐方式，但确保 vertical 和 wrap_text 有值
            a = cell.alignment
            cell.alignment = Alignment(
                horizontal=a.horizontal,
                vertical=a.vertical if a.vertical else 'center',
                wrap_text=a.wrap_text if a.wrap_text is not None else True,
                text_rotation=a.text_rotation,
                indent=a.indent,
                shrink_to_fit=a.shrink_to_fit
            )

    # 2. 设置列宽（每个 sheet 不同）
    col_widths = {...}  # 根据诊断结果设置
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # 3. 放大行高
    for row_num in range(1, ws.max_row + 1):
        rd = ws.row_dimensions.get(row_num)
        if rd and rd.height:
            ws.row_dimensions[row_num].height = round(rd.height * 1.25, 1)

    # 4. 设置缩放
    ws.sheet_view.zoomScale = 110
    ws.sheet_view.zoomScaleNormal = 110

wb.save(dst)
```

### 第 4 步：边框美化（按需）

当用户反馈"边框太丑"时，对特定区域进行边框统一：

```python
thin = Side(style='thin', color='FFD9D9D9')      # 浅灰细线
medium = Side(style='medium', color='FFAAAAAA')   # 中灰粗线
header_fill = PatternFill(start_color='FFF2F2F2', end_color='FFF2F2F2', patternType='solid')

# 遍历目标区域，统一边框
for row in ws.iter_rows(min_row=start, max_row=end, min_col=1, max_col=max_col):
    for cell in row:
        top, bottom, left, right = thin, thin, thin, thin
        # 区块标题行：加粗上下边框 + 浅灰底色
        if cell.row in header_rows:
            top, bottom = medium, medium
            cell.fill = header_fill
        # 最后行：底部加粗
        if cell.row == last_row:
            bottom = medium
        cell.border = Border(left=left, right=right, top=top, bottom=bottom)
```

**边框美化原则：**
- 使用浅灰色（#D9D9D9 / #AAAAAA）代替默认黑色，视觉更柔和
- 数据行统一细边框，区块标题用粗边框分隔
- 合并单元格区域加浅灰底色突出分区

### 第 5 步：验证

保存后必须验证：

```python
wb2 = openpyxl.load_workbook(dst)
for sn in wb2.sheetnames:
    ws = wb2[sn]
    # 1. 验证公式未丢失
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str) and cell.value.startswith('='):
                print(f'{cell.coordinate}: {cell.value}')
    # 2. 验证合并单元格
    print(f'Merged: {list(ws.merged_cells.ranges)}')
    # 3. 验证字体
    print(f'Font: {ws["A1"].font.name}, sz={ws["A1"].font.size}')
    # 4. 验证缩放
    print(f'Zoom: {ws.sheet_view.zoomScale}')
```

## 踩坑记录与避坑指南

### 坑 1：pypi.org 超时

**现象**：`pip install openpyxl` 超时失败，报 `ReadTimeoutError` 或 `SSLEOFError`

**原因**：国内网络访问 pypi.org 不稳定

**解决**：使用清华镜像
```bash
./Scripts/pip.exe install openpyxl -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 30
```

### 坑 2：文件被占用导致 PermissionError

**现象**：`wb.save(path)` 报 `PermissionError: [Errno 13] Permission denied`

**原因**：文件正在被腾讯文档编辑器或 Excel 打开预览，文件锁未释放

**解决**：另存为新文件名（如 `_v2.xlsx`），不要尝试关闭用户的编辑器
```python
dst = path.replace('.xlsx', '_v2.xlsx')
wb.save(dst)
```

### 坑 3：冻结窗格导致体验问题

**现象**：设置 `freeze_panes` 后，用户打开文件反馈"出现冻结情况"

**原因**：冻结行数过多（如冻结了 8 行含标题+信息行+表头），占据大量屏幕空间

**解决**：
- 默认不设置冻结窗格
- 如用户要求，只冻结 1-2 行表头
- 用户反馈后立即移除：`ws.freeze_panes = None`

### 坑 4：openpyxl 不保留公式计算结果

**现象**：用 openpyxl 保存后，公式单元格可能显示为 0 或空白

**原因**：openpyxl 保存公式为字符串，不计算结果。需要 Excel/WPS 打开后自动重算

**解决**：
- 不要用 `data_only=True` 加载（会把公式替换为值并永久丢失公式）
- 保存后提醒用户用 Excel/WPS 打开即可自动重算
- 如需验证公式值，使用 xlsx skill 中的 `scripts/recalc.py`（需要 LibreOffice）

### 坑 5：字体名混用

**现象**：原文件中不同单元格使用不同字体（如 Aptos + 宋体），统一后仍有残留

**解决**：遍历所有单元格强制设置 `name=TARGET_FONT`，不要只改部分

### 坑 6：部分列没有设置宽度

**现象**：优化后发现某些列仍然很窄

**原因**：原文件中部分列的 `column_dimensions` 未设置，openpyxl 不会自动补齐

**解决**：在诊断阶段检查所有列是否有宽度设置，对缺失的列手动赋值

## 输出文件命名

- 优化版：`{原文件名}_优化版.xlsx`
- 如遇文件锁：`{原文件名}_优化版_v2.xlsx`（递增版本号）

## 优化检查清单

- [ ] 所有单元格字体已统一为目标字体
- [ ] 正文字号 >= 12pt
- [ ] 所有列都有明确的宽度设置
- [ ] 行高已按比例放大
- [ ] 缩放比例已设置（110%）
- [ ] 公式全部保留（未丢失）
- [ ] 合并单元格未受损
- [ ] 边框风格统一（无残留旧样式）
- [ ] 文件可正常打开（无损坏）
