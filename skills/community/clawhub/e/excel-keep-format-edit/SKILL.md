---
name: excel-keep-format-edit
slug: excel-keep-format-edit
displayName: Excel原表改数字不破格式·财务三表勾稽自动保
description: >-
  客户拿来一张老报表说「就在原表上改个数，格式一点都不要动」——用 openpyxl 重建一次，字体、边框、合并单元格、条件格式、列宽全丢，客户一打开就知道这不是他原来那张表。

  正确做法：**用 Excel COM 打开原文件的副本，只改目标单元格的值，其余原样保留。**

  这套 skill 解决三个真痛点：
  - **格式零丢失**：复制原件再改，不重建工作簿
  - **别猜行号**：先扫科目名定位实际行列再改（附「资产负债表是左右双栏、科目在 E 列、数值在 G/H 列」这个反复踩的坑）
  - **改完保勾稽**：财务三表调整后自动校验「资产=负债+所有者权益」，不是改完就交

  适用：审计调整分录、财务测算、错账更正、报表科目重分类。
  环境：Windows + Office（用 pywin32 调 COM）。

  触发词：Excel改数字、保格式修改、原表修改、不动格式、xls修改、财务三表、资产负债表调整、勾稽关系、审计调整。
version: 1.1.0
author: 九品锦锂e
summary: 用Excel COM只改目标单元格，字体边框合并条件格式列宽全不动；改完校验三表勾稽。
license: MIT
metadata:
  version: "1.1.0"
---
# 原xls保格式修改（Excel COM）

## 触发条件
- 用户/客户要求"在原表基础上改，格式/设计一模一样不要动，其他表格不要调整"
- 财务三表调整：改未分配利润/利润总额后保持资产=负债+权益勾稽
- 拿到.xls老格式报表要改数字，不能重建

## 铁律：不要用openpyxl重建
openpyxl重建xlsx会丢原表格式/样式/布局——客户一打开就看出来"不是原来的表"。
**必须用 Excel COM 打开原文件copy，只改目标单元格，其余原样保留。**

## 环境（Windows）
```bash
# pywin32 装在 hermes venv（系统python没有！）
python -m pip install pywin32
# 运行脚本也用 hermes venv 的 python（系统python import不到win32com）
```

## 核心流程

### 1. 先复制原件再改
```python
import shutil
shutil.copy2(SRC, OUT)   # 原件不动，改OUT
```

### 2. 用COM打开+扫描定位行/列（别猜行号！）
```python
import win32com.client
excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = False; excel.DisplayAlerts = False
wb = excel.Workbooks.Open(OUT)
ws = wb.Sheets('资产负债表')
# 扫A列/E列找科目名，打印实际行列
for r in range(1, 60):
    a = str(ws.Cells(r, 1).Value or ''); e = str(ws.Cells(r, 5).Value or '')
    if '未分配利润' in a or '未分配利润' in e:
        print(r, a, e, ws.Cells(r,7).Value)  # G/H列是右侧数值
```
⚠️ **左右双栏报表（资产负债表）科目在E列、数值在G/H列**——"未分配利润"在右侧G34/H34，不是C/D！
⚠️ xlrd 0-indexed vs COM 1-indexed，行号差1——必须用label扫描确认。

### 3. 只改目标单元格
```python
ws.Cells(13, 3).Value = 4307698.97    # 其他应收款期末(左栏C)
ws.Cells(34, 7).Value = 1052736.98    # 未分配利润期末(右栏G)
wb.Application.Calculate()
wb.Save(); wb.Close(True); excel.Quit()
```

### 4. ⚠️ 原xls往往没有公式——合计行必须手动算好写进去
小企业准则导出的xls合计行常是**数值不是SUM公式**，改明细后合计不会自动变。
调整后必须手动算：
- 资产合计 = 流动资产 + 非流动资产
- 权益合计 = 实收资本 + 未分配利润
- 负债+权益 = 负债合计 + 权益合计 = 资产合计 ✅ 验证平衡
- 利润表：营业利润 = 收入-成本-管理-财务；利润总额 = 营业利润+营业外收入；净利润 = 利润总额-所得税

### 5. 验证平衡
```python
assert abs(ws.Cells(36,3).Value - ws.Cells(36,7).Value) < 0.01  # 资产=负债+权益
```

## 财务三表调整常见方案（2026-08实测）
目标：未分配利润调正（如期末105万/期初79万），利润总额=期末-期初差。
- **资产负债表**：只调"其他应收款"（资产方）同额增加 → 资产=负债+权益自动平衡
- **利润表**：调"营业收入"（或管理费用）使利润总额=未分配利润差；本期利润另定
- **现金流量表**：无现金收付的损益调整，通常不动
- 勾稽验证：`期末未分配 - 期初未分配 == 累计利润总额`

## 坑与解决
1. pywin32只装hermes venv → 系统python `import win32com` 报No module named 'pywintypes'；用venv python
2. `python -I` 隔离模式读不到site-packages → 直接运行不带-I
3. COM读原值显示0 → 行号对错（xlrd 0-indexed vs COM 1-indexed），label扫描定位
4. 改完验证时发现没生效 → 检查改的是左栏还是右栏（C/D vs G/H）
5. 杀python进程前确认CommandLine（webapp/网关也是python进程）

---

## 🙋 关于作者

**九品锦锂e** ｜ 把踩过的坑封装成"拿来就能跑"的 skill，不写教科书。这个 skill 是我自己每天在用的版本。

**微信：ly5419495**（加时备注「SkillHub」，我优先通过）
**公众号：初五Agent**（微信搜一搜，复盘和方法都写在那儿，不加微信也能读）

我另外做的几个能直接跑的工具，都放在这个货架页（复制到浏览器打开）：
https://skillpay.alipay.com/public/jiupinjinlie

用的时候卡住了、或者有别的场景想让我封装成 skill，按上面任意方式找我就行。

![九品锦锂e 微信二维码](https://jinli-vault-1372591613.cos.ap-guangzhou.myqcloud.com/skillhub/hook-wechat-jiupinjinlie.png)
