---
name: "cm-invoice-validate"
description: 当用户需要查验发票真伪时使用。触发词包括"查发票""发票查验""验证发票""发票真伪"。
metadata: { "openclaw": { "emoji": "🧾", "requires": { "bins": ["python3"], "env": ["CLAWMATE_API_KEY"] }, "primaryEnv": "CLAWMATE_API_KEY" } }
---

# 发票查验技能

> **禁止在 LLM 对话中暴露 `api_key`。** API Key 从环境变量 `CLAWMATE_API_KEY` 读取。

## 核心规则

**AI 不得读取发票文件内容（PDF/图片）。** 所有文件由 Python 脚本内部处理。AI 只需：获取文件路径 → 传给脚本 → 展示结果。

## 文件访问范围声明

本技能仅读取以下目录中的发票文件：

- 当前工作目录下的 `.clawmate/` 目录（及其子目录）
- 用户明确指定的目录路径

**禁止读取上述范围以外的文件。** 如果用户未指定目录，默认仅扫描 `.clawmate/` 目录。

## 接口信息

- **地址**: `POST https://www.clawmate.net/server/test/Api/InvoiceValidate`
- **脚本**: `scripts/invoice_validate_client.py`
- **API Key 获取**: https://www.clawmate.net/user

## 输入参数

### 发票信息方式（validateMode=1）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `fphm` | string | **是** | 发票号码（传统票 8 位，全电票 20 位） |
| `kprq` | string | **是** | 开票日期，格式 `yyyyMMdd` |
| `fpdm` | string | 否 | 发票代码（10-12 位）。全电票无需传 |
| `kjje` | string | 否 | 不含税金额 |
| `jshj` | string | 否 | 价税合计 |
| `jym` | string | 否 | 校验码（完整值或后 6 位） |

### 文件方式（validateMode=2/3/4）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `validateMode` | int | **是** | `2`=PDF, `3`=图片, `4`=ODF |
| `file` | string | **是** | 发票文件绝对路径 |

> 文件方式无需传其他参数。`validateMode=3/4` 服务端暂不支持。

## 交互流程

```
用户消息 → 智能提取参数 → 判断票种（全电票跳过 fpdm）→ 确认 → 调用 API
```

**参数提取规则：**
- 发票号码：从消息中识别 8 位或 20 位数字
- 开票日期：识别 `yyyyMMdd` / `yyyy-MM-dd` / `yyyy年MM月dd日` 等格式，统一转为 `yyyyMMdd`
- 全电票（20 位号码）自动跳过发票代码询问

**确认格式：**
```
📋 即将查验的发票信息：
- 发票号码：{fphm}
- 开票日期：{kprq}
- 发票代码：{fpdm}（全电票不显示）

确认查验？[A] 确认 [B] 修改
```

## 批量查验

**触发词：** "批量查"、"目录"、"文件夹" + "发票/查验"

**流程：**
1. 询问目录路径，扫描文件（仅限 `.clawmate/` 目录或用户指定目录，递归子目录）
2. 按文件类型处理：
   - PDF/图片 → 直接调用 API（AI 不读取内容）
   - XML/Excel → AI 读取并提取字段
3. 展示汇总列表，用户确认/修改
4. 并行调用（最多 5 个），汇总结果

**结果保存：** `{yyyyMMddHHmmss}-{N}张.md`

## 执行命令

```bash
# 发票信息方式
python scripts/invoice_validate_client.py \
  --fphm "12345678" --kprq "20260424" --fpdm "1100191320"

# PDF 文件方式
python scripts/invoice_validate_client.py --validate-mode 2 --file "/path/to/invoice.pdf"

# JSON 模式（批量查验用）
python scripts/invoice_validate_client.py --fphm "..." --kprq "..." --json
```

## 响应处理

| exit code | 状态 | 处理 |
|-----------|------|------|
| 0 | 查验通过 | 展示发票信息表格 |
| 1 | 查验不通过 | 列出可能原因，建议核实原件 |
| 2 | 服务异常 | 建议稍后重试 |
| 3 | API Key 未设置 | 引导获取 Key |
| 4 | 余额不足 | 提示充值 |
| 5 | 次数超限 | 提示购买套餐 |
| 6 | 参数格式错误 | 指出具体字段问题 |
| 7 | 网络错误 | 检查连接或 API 地址 |
| 8 | 响应异常 | 联系技术支持 |

**响应解读：**
- `resCode=200` → 读取 `data.isSuccess` + `data.validateCode`
- `resCode=400` + `msg` 含"版本过低" → 自动更新技能

### 单张发票信息展示

查验通过后，展示以下字段（有值则显示）：

| 字段 | API 字段 | 说明 |
|------|---------|------|
| 发票代码 | `invoice.InvoiceCode` | 传统票有，全电票无 |
| 发票号码 | `invoice.InvoiceNumber` | |
| 开票日期 | `invoice.InvoiceDate` | |
| 价税合计 | `invoice.Amount` | |
| 不含税金额 | `invoice.TotalPrice` | |
| 税额 | `invoice.TotalTaxPrice` | |
| 销方名称 | `invoice.SellerCompany` / `invoice.InvoiceCompany` | |
| 销方税号 | `invoice.SellerTaxCode` | |
| 销方开户银行 | `invoice.SellerBankName` | |
| 销方银行账号 | `invoice.SellerBankAccount` / `invoice.SellerBankingAccount` | |
| 购方名称 | `invoice.BuyerCompany` | |
| 购方税号 | `invoice.BuyerTaxCode` | |
| 购方开户银行 | `invoice.BuyerBankName` | |
| 购方银行账号 | `invoice.BuyerBankAccount` / `invoice.BuyerBankingAccount` |

**展示格式：**
```
📋 发票信息
| 字段 | 值 |
|------|-----|
| 发票号码 | 26442000004xxxxxx1 |
| 开票日期 | 2026-04-15 |
| 价税合计 | 3544.75 元 |
| 不含税金额 | 3344.10 元 |
| 税额 | 200.65 元 |
| 销方 | 广州xxx科技有限公司 / 9144xxx / 中国银行 / 709469xxx |
| 购方 | 广州yyy数据科技有限公司 / 9144xxx |

═════════════════════════════════════════════
  ✅ 查询状态：发票信息与税局电子信息一致
═════════════════════════════════════════════
```

### 批量查验结果

**汇总摘要：**
```
📊 批量查验结果

总计：{N} 张 | ✅ 通过：{M} 张 | ❌ 失败：{K} 张
消费金额：{totalCharge} 元
```

**结果文件：** `{yyyyMMddHHmmss}-{N}张.md`

文件内容格式（仅展示有值字段）：

```markdown
# 批量查验结果

**总计**：3 张 | **通过**：2 张 | **失败**：1 张  
**消费金额**：0.06 元

---

## 发票1.pdf — ✅ 通过

| 字段 | 值 |
|------|-----|
| 发票号码 | 26442000xxxxxxx61 |
| 开票日期 | 2026-04-15 |
| 价税合计 | 3544.75 元 |
| 不含税金额 | 3344.10 元 |
| 税额 | 200.65 元 |
| 销方名称 | 广州xxx科技有限公司 |
| 销方税号 | 9144************6G |
| 销方开户银行 | 中国银行广州支行 |
| 销方银行账号 | 709469xxxxxx |
| 购方名称 | 广州yyy数据科技有限公司 |
| 购方税号 | 914401xxxxxxxx |

---

## 发票2.pdf — ❌ 失败

查验未通过：查无此票

---

## 发票3.jpg — ✅ 通过

| 字段 | 值 |
|------|-----|
| 发票号码 | 11223344 |
| 开票日期 | 2026-04-16 |
| 价税合计 | 113.00 元 |
```

## 版本过低提示

检测到版本过期时，提示用户手动更新：

```
⚠️ 技能版本过低，请运行以下命令更新：

curl -o /tmp/cm-invoice-validate.zip https://www.clawmate.net/server/test/cm-invoice-validate.zip
mkdir -p ~/.agents/skills/cm-invoice-validate
unzip -o /tmp/cm-invoice-validate.zip -d ~/.agents/skills/cm-invoice-validate/
```

用户确认后再执行更新命令。

## 边界情况

| 情况 | 处理 |
|------|------|
| 用户取消 | 终止操作，不调用 API |
| 日期格式错误 | 提示正确格式，重新询问 |
| 部分字段未填 | 确认时展示已填字段，省略可选字段 |
| 目录不存在/无发票文件 | 提示检查路径 |
| 发票超过 5 张 | 分批执行，每批 5 张并行 |

---

**Version**: 1.0.2 | **更新日期**: 2026-04-28
