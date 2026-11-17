---
name: electrical-schematic-review
description: "Review electrical schematics from EPLAN and similar CAD tools against standardized checklists"
tags: [domain-specific, electrical, visual, template-based, file-based]
version: 1.0.0

# 电气原理图AI审图技�?
## 概述

本技能用于系统化审查电气原理图，覆盖安全回路、主回路、控制回路、PLC/IO、伺服驱动、通信网络等模块，输出标准化的审图报告（PDF或Excel）�?
## 适用场景

- 新项目电气设计完成后，出图前的自�?- 老项目改造后的图纸复�?- 安全合规性检查（急停、安全门、安全控制器�?- 设计质量评审
- 填写用户提供的Excel评审记录�?
## 输入要求

| 输入 | 格式 | 说明 |
|------|------|------|
| 电气原理�?| PDF（EPLAN导出�?| 支持任意页数，小型设�?0-20页，大型设备200+�?|
| 审图检查清�?| Excel或内�?| 用户可提供Excel模板，或使用内置清单 |
| 项目信息 | 文本 | 项目名称、版本、电源规格等 |

## 审图工作流程

### 1. 项目信息收集

首先确认以下信息�?- 项目名称
- 图纸版本
- 图纸总页�?- 电源规格（AC380V/DC48V/DC24V等）
- 设备类型（巡检机器人、自动插管机、包装机等）
- 主要元器件（PLC、伺服、IO模块等）

### 2. 图纸结构分析

使用PyMuPDF读取PDF，识别图纸结构：

```python
import fitz  # PyMuPDF
doc = fitz.open(pdf_path)
for page in doc:
    text = page.get_text()
    # 分析每页内容
```

典型电气原理图结构：
```
├─ 封面/目录�?-5页）
├─ 网络拓扑�?├─ 电柜布局�?├─ 主回路（断路器、接触器、滤波器、伺服驱动）
├─ 24V电源分配
├─ 低压负载
├─ 按钮及指示灯
├─ PLC/IO系统（输�?输出�?├─ 伺服/变频器回�?├─ 通信设备（工控机�?G CPE等）
└─ 端子�?电缆�?```

### 3. 按检查清单逐项审查

读取内置检查清单：`references/checklist.md`

按以下优先级审查�?
#### 🔴 Critical（必须修改，涉及安全�?
重点关注�?- **急停回路**：是否通过安全控制�?安全继电器？是否双通道�?- **安全�?*：门锁控制是否使用安全继电器？状态反馈是否接入安全输入？
- **浪涌保护**：主回路是否配置SPD�?- **接地**：PE排连接是否完整？

#### 🟠 Major（重要问题，影响功能�?
重点关注�?- 伺服驱动器进线电抗器
- 滤波器接�?- 电源冗余设计
- 远程IO独立供电
- 制动电阻（垂直轴必须配置�?
#### 🟡 Minor（一般问题，建议修改�?
- 标注规范�?- 编号连续�?- 图纸完整�?- 审核签名

#### 💡 Suggestion（优化建议）

- 能耗监�?- 远程监控
- 预防性维�?
### 4. 生成审图报告

#### 方式A：填写Excel评审记录�?
如果用户提供了Excel评审清单�?
```python
from openpyxl import load_workbook

wb = load_workbook(excel_path)
ws = wb.active

# 填写评审结果（只修改指定列，不改格式�?ws.cell(row=row, column=5).value = '通过/不通过/不适用/待确�?  # 评审结果
ws.cell(row=row, column=6).value = '问题描述'  # 备注
ws.cell(row=row, column=7).value = 'Critical/Major/Minor/Suggestion'  # 问题级别

# 设置颜色
if level == 'Critical':
    cell.fill = PatternFill(start_color='FF4444', end_color='FF4444', fill_type='solid')
```

**⚠️ 重要：不要取消合并单元格，保持原Excel格式�?*

#### 方式B：生成PDF审图报告

使用内置脚本生成PDF报告�?
```bash
python scripts/gen_report_pdf.py
```

报告结构�?1. 封面（项目信�?+ 问题汇总）
2. Critical问题详情
3. Major问题详情
4. Minor问题列表
5. Suggestion列表
6. 总结

## 审图要点速查

### 安全回路审查要点

| 检查项 | 合格标准 | 常见问题 |
|--------|----------|----------|
| 急停回路 | 通过安全控制器，双通道 | 直接接PLC/IO输入 |
| 安全�?| 安全继电器控制，双通道反馈 | 普通IO控制 |
| SPD | Type 2，带后备保护 | 未配�?|
| 接地 | PE排完整，短粗导线 | 接地不明�?|

### 主回路审查要�?
| 检查项 | 合格标准 | 常见问题 |
|--------|----------|----------|
| 进线电抗�?| 每台伺服前端配置 | 未配�?|
| 滤波�?| G端子接PE | 接地未标�?|
| 电源冗余 | 关键回路有备�?| 单电�?|
| 制动电阻 | 垂直轴必须配�?| 未配�?|

### PLC/IO审查要点

| 检查项 | 合格标准 | 常见问题 |
|--------|----------|----------|
| 远程IO供电 | 独立24V电源 | 与PLC共用 |
| 诊断功能 | 配置IO诊断 | 未配�?|
| 变量�?| 输入输出点有变量�?| 未标�?|
| 备用IO | 预留10-20% | 未预�?|

## 相关文件

- 检查清单：`references/checklist.md`
- PDF报告脚本：`scripts/gen_report_pdf.py`

## 依赖�?
```bash
pip install PyMuPDF openpyxl reportlab
```
