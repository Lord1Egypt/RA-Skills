---
name: crs-tax-calculator
description: CRS境外补税计算工具 - 上传券商月结单PDF/Excel，AI自动解析交易数据，FIFO/ACB成本法计算资本利得，生成Excel税务审计底稿。支持多文件年度汇总。
version: 3.4.0
metadata:
  openclaw:
    requires:
      env:
        - CRS_API_KEY
      bins:
        - python3
    primaryEnv: CRS_API_KEY
    emoji: "🧾"
    homepage: https://wealthlplantation.com/api
---

# CRS 境外补税计算工具

上传券商月结单（PDF/Excel），自动计算中国CRS境外补税或加拿大CRA税务申报所需的资本利得。

## 前提条件

**CRS API Key**：在 https://wealthlplantation.com 注册并购买套餐后，在用户中心生成 API Key。

AI 文档解析由服务端完成，用户无需提供任何额外的 AI 密钥。

## 环境变量设置

运行前必须设置 `CRS_API_KEY` 环境变量。如果用户未设置，**你必须主动引导用户完成以下步骤**：

### 步骤 0：检查环境变量

```bash
echo "CRS_API_KEY=${CRS_API_KEY:-(未设置)}"
```

如果显示"未设置"，引导用户：

1. **获取 API Key**：如果用户还没有 API Key，告知他们在 https://wealthlplantation.com 注册账户（免费送 20 页体验额度），然后在用户中心生成 API Key
2. **设置环境变量**：让用户在当前终端会话中设置：

```bash
export CRS_API_KEY="用户提供的key"
```

如果用户希望永久生效，可以手动将上述行添加到 `~/.zshrc` 或 `~/.bashrc`。

设置完成后验证：`echo $CRS_API_KEY`，确认已生效再继续。

## 数据安全

- 上传的文件仅用于 AI 解析交易数据，**处理完成后立即丢弃，不做任何存储**
- 服务端不保存文件内容，仅记录处理日志（文件名、页数、耗时）
- AI 解析由服务端安全调用，用户无需提供自己的 AI 密钥
- API 端点 `api.wealthlplantation.com` 由 wealthlplantation.com 运营，TLS 加密传输

## ⚠️ 重要：文件处理规则

**严禁读取或查看文件内容！** 你（AI agent）绝对不能用任何方式读取、查看、cat、head、base64 命令查看 PDF 或 Excel 文件的内容。这些文件是二进制的券商月结单，读取它们会消耗巨量 tokens 导致超限。

正确做法：只收集文件路径，然后调用本 skill 自带的 `do_audit.py` 脚本，由脚本在内部处理编码和 API 调用。

## ⚠️ 重要：Token 节约规则

为了最大限度节约 Token 消耗，你**必须**遵守以下规则：
1. **不要**在对话中内联编写 Python 代码。使用本 skill 自带的 `do_audit.py` 脚本
2. 调用脚本时只传文件路径参数，不要在命令中嵌入任何额外代码
3. 报告结果时只摘要关键数字，不要复述脚本的完整输出

## 使用方法

### 步骤 1：收集同一年度的所有月结单文件路径

向用户询问要处理的文件。收集所有文件的**完整路径**。

**重要：同一年度的所有月结单必须一起提交，才能保证数据准确。** 例如，如果用户有2025年1月到12月的月结单，应该全部一起处理。

### 步骤 2：定位 do_audit.py 脚本

本 skill 包含一个独立的 Python CLI 脚本 `do_audit.py`。查找顺序：

```bash
# 查找 skill 目录下的 do_audit.py
SCRIPT=$(find ~/.claude/skills/crs-tax-calculator ~/.openclaw/skills/crs-tax-calculator -name "do_audit.py" 2>/dev/null | head -1)
echo "Script: $SCRIPT"
```

如果找不到脚本，提示用户重新安装此 skill（通过 ClawHub 或 Claude Code 的 `/install` 命令），脚本包含在 skill 包内。

### 步骤 3：运行脚本

```bash
python3 "$SCRIPT" /path/to/file1.pdf /path/to/file2.pdf --method FIFO --output /path/to/output/dir
```

参数说明：
- 文件路径：直接列出所有月结单文件的完整路径
- `--method FIFO`：中国税务（默认）；`--method ACB`：加拿大税务
- `--output`：指定 Excel 输出目录（默认保存到第一个输入文件所在目录）

**一行命令即可，无需编写任何额外代码。**

### 步骤 4：报告结果

脚本执行完后，**简要**告知用户：
- 生成了哪些 Excel 文件（文件名和路径）
- 每个年度的记录数、净损益（CNY）和估算税额
- 剩余配额
- 任何审计问题或警告

如果有错误，根据错误码提供建议：
- `UNAUTHORIZED`：API Key 无效，需要在 wealthlplantation.com 获取
- `QUOTA_EXCEEDED`：配额不足，需要购买更多页数
- `GEMINI_API_ERROR`：AI 解析服务暂时不可用，请稍后重试
- `CALCULATION_ERROR`：计算错误，可能是文件内容无法识别

## 支持的文件类型

- `.pdf` — PDF 月结单
- `.xlsx` — Excel 文件（月结单或历史审计底稿）
- `.csv` — CSV 文件
- `.png`, `.jpg` — 图片格式的对账单

## 支持的券商

盈立证券(uSMART)、长桥证券(Longbridge)、富途证券(Futu/Moomoo)、老虎证券(Tiger)、盈透证券(IBKR)、卓锐证券(Zircon) 等主流券商的月结单。

## 定价

按页计费，购买后永久有效：

| 套餐 | 价格 | 页数 |
|------|------|------|
| 免费体验 | $0 | 20页 |
| 个人版 | $9.99 | 100页 |
| 家庭版 | $19.99 | 300页 |
| 尊享版 | $29.99 | 500页 |
| 企业版 | $49.99 | 1000页 |

详情和购买：https://wealthlplantation.com/pricing

## 输出内容

生成的 Excel 审计底稿包含：
- 交易明细表（买入/卖出/股息/利息/IPO）
- FIFO 或 ACB 成本匹配明细
- 汇率换算（PBOC 人民币 / Bank of Canada 加元）
- 税务摘要（应税收入、资本利得、预扣税抵扣）
- 审计问题清单
