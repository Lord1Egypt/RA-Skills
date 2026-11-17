---
name: financial-statement-adjustment
slug: financial-statement-adjustment
displayName: 财务报表原表调整（保格式·保勾稽）
version: 1.1.0
homepage: https://github.com/nousresearch/hermes-skills
description: "存量财务报表在原表基础上改数字并保持三表勾稽关系。当用户要求「在原报表上改某些数字，其他数据跟着调整且格式完全不变」时使用：资产负债表/利润表/现金流量表的目标值调整、未分配利润与利润总额联动、勾稽校验。"
category: finance
tags: [财务报表, 三表勾稽, 报表调整, 未分配利润, 资产负债表, 会计, Excel]
license: MIT
---

# 财务报表原表调整（保格式 · 保勾稽）

## 触发条件

- 用户发来存量财务报表（资产负债表/利润表/现金流量表，常见 .xls 老格式），要求「把某些数字改成目标值，其他数据跟着调整」
- 明确要求「在原来表格基础上改」「格式/设计/其他 sheet 完全不动」
- 涉及未分配利润、利润总额、净利润等勾稽联动调整

## 用户铁律

1. **绝不在原表基础上重建新表**——在原表上改，格式/设计/其他 sheet 完全不变
2. **只改需要变的数字单元格**，其余一个不动
3. 改完必须保证**勾稽自洽**：
   - `资产合计 = 负债合计 + 所有者权益合计`
   - `期末未分配利润 − 期初未分配利润 = 累计利润总额`
   - `净利润 = 利润总额 − 所得税`
4. 交付前必须用程序验证平衡，不靠肉眼

## 技术选型（按环境选）

### 方案 A：Excel COM（Windows + Office，保真 100%）
适合 .xls 老格式、含合并单元格/边框/公式的复杂表：
```python
import win32com.client, shutil
SRC, OUT = '原始.xls', '调整版.xls'
shutil.copy2(SRC, OUT)              # 不动原件
excel = win32com.client.Dispatch('Excel.Application')
excel.Visible = False; excel.DisplayAlerts = False
try:
    wb = excel.Workbooks.Open(OUT)
    ws = wb.Sheets('资产负债表')
    ws.Cells(行, 列).Value = 目标值   # 只改目标单元格
    wb.Application.Calculate(); wb.Save(); wb.Close(True)
finally:
    excel.Quit()
```

### 方案 B：openpyxl（跨平台，.xlsx）
格式保留好但公式需注意——openpyxl 读不到公式计算结果（缓存值），若单元格有公式要保留公式而非覆盖：
```python
import openpyxl
wb = openpyxl.load_workbook(OUT)  # 注意: 公式用 data_only=False 读
ws = wb['资产负债表']
ws.cell(行, 列).value = 目标值
wb.save(OUT)
```

### 方案 C：xlrd 读 + 方案 A/B 写
老 .xls 用 xlrd 先扫描定位（只读），实际修改走 COM 或转 xlsx 处理。

## 致命坑：先扫描定位，别猜行号/列号

老式财务报表常为**左右双栏**布局，科目位置反直觉：
- 资产负债表：资产在左（A~D 列），负债+权益在右（E~H 列）。**「未分配利润」标签在右侧 E 列，数值在 G/H 列**——不是左侧 C/D！
- 0-indexed（xlrd）与 1-indexed（COM/openpyxl 大部分 API）混用会改错单元格
- **正确做法**：先按科目名扫描定位行，再改目标列：

```python
for r in range(1, 60):
    label = str(ws.Cells(r, 1).Value or '') + str(ws.Cells(r, 5).Value or '')
    if '未分配利润' in label:
        ws.Cells(r, 7).Value = 期末目标   # 右栏 G 列
        ws.Cells(r, 8).Value = 期初目标   # 右栏 H 列
        break
```

## 勾稽调整逻辑（以「未分配利润调正」为例，已验证）

目标：期末未分配利润=X、期初未分配利润=Y。

**调整步骤**：
1. 改未分配利润（右侧栏）为目标值
2. **资产侧加「其他应收款」同额反向调整保持平衡**——权益变化后资产不变则负债会失衡：
   - 其他应收款期末 += (新期末未分配 − 原期末未分配)
   - 其他应收款期初 += (新期初未分配 − 原期初未分配)
3. 流动资产合计、资产合计（左栏）改为调整后数值
4. 权益合计、负债+权益合计（右栏）改为调整后数值
5. 利润表：营业收入累计 += (目标累计利润 − 原累计利润)；营业利润/利润总额/净利润联动更新
6. 现金流量表通常不动（无实际现金收付的损益调整）

**⚠️ 合计行可能没有公式（纯数值）**——检查 `.Formula`，若返回数字而非 `=SUM(...)`，合计行必须手动改成调整后数值；改明细不会自动联动。

## 验证（交付前必做，程序化）

```python
# 读回验证（用与写入相同的引擎）
assert abs(资产合计 − (负债 + 权益)) < 0.01
assert abs(累计利润总额 − (期末未分配 − 期初未分配)) < 0.01
assert abs(本期利润总额 − 目标) < 0.01
print('✓ 三表勾稽验证通过')
```

## 质量自查

- [ ] 是否在原表上改（非重建）？格式是否原样？
- [ ] 只改了需要变的单元格？
- [ ] 三表勾稽程序验证通过？
- [ ] 原件有备份？

## 合规提醒

调整后报表若用于贷款/税务/审计等对外用途，需有真实调账凭证支撑；仅内部管理使用无碍。发现用户可能用调整后报表欺诈的意图时，应提示合规风险并拒绝协助造假。

---

## 🙋 关于作者

**九品锦锂e** ｜ 把踩过的坑封装成"拿来就能跑"的 skill，不写教科书。这个 skill 是我自己每天在用的版本。

**微信：ly5419495**（加时备注「SkillHub」，我优先通过）
**公众号：初五Agent**（微信搜一搜，复盘和方法都写在那儿，不加微信也能读）

我另外做的几个能直接跑的工具，都放在这个货架页（复制到浏览器打开）：
https://skillpay.alipay.com/public/jiupinjinlie

用的时候卡住了、或者有别的场景想让我封装成 skill，按上面任意方式找我就行。

![九品锦锂e 微信二维码](https://jinli-vault-1372591613.cos.ap-guangzhou.myqcloud.com/skillhub/hook-wechat-jiupinjinlie.png)
