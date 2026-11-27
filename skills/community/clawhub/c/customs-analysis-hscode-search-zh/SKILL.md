---
name: customs-analysis-hscode-search-zh
description: "搜索分析报告-HS编码 — 根据产品名称和HS编码关键字搜索匹配的HS编码列表。\n\nTrigger: HS编码搜索，产品HS编码查询，海关编码搜索，查找HS编码，关税编码搜索"
metadata: {"version":"1.0.2","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🔍","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关分析报告-HS编码搜索

通过跨境魔方开放平台API，搜索HS编码。

## 概述

本技能允许你通过产品名称和HS编码关键字搜索匹配的HS编码列表。找到的HS编码可用于其他分析报告技能。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_analysis_hscode_search.py`。**不要使用** `cd scripts && python customs_analysis_hscode_search.py` 这种复合命令。

### HS编码搜索（`customs_analysis_hscode_search.py`）
- **返回粒度**：一个或多个匹配的HS编码
- **使用场景**：按产品名称查找HS编码，查询海关分类编码，搜索关税编码
- **示例**：
  - "搜索奶粉的HS编码"
  - "查找以0402开头的HS编码"
- **参数说明**：参见 [HS编码搜索API](references/customs-analysis-hscode-search-api.md)

## API密钥与充值

本技能需要API密钥。API密钥存储在 `~/.upkuajing/.env` 文件中：
```bash
cat ~/.upkuajing/.env
```
**文件内容示例**：
```
UPKUAJING_API_KEY=your_api_key_here
```
### **API密钥未设置**
首先检查 `~/.upkuajing/.env` 文件中是否有 UPKUAJING_API_KEY；
如果未设置，请让用户选择：
1. 用户已有密钥：用户提供（手动添加到 ~/.upkuajing/.env 文件）
2. 用户没有密钥：通过界面申请（`auth.py --new_key`），新密钥会自动保存到 ~/.upkuajing/.env
等待用户选择；

### **账户充值**
当API响应提示余额不足时，解释并引导用户充值：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 根据订单响应，发送支付页面URL给用户，引导用户打开URL并支付，用户确认支付成功后继续；

### **获取账户信息**
使用以下命令获取 UPKUAJING_API_KEY 的账户信息：`auth.py --account_info`

## API密钥与跨境魔方账户
- 新申请的API密钥：前往[跨境魔方开放平台](https://developer.upkuajing.com/)注册登录，然后绑定账户

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/hscode/search","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"HS编码搜索查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用均产生费用**，不同接口计费方式不同。

**最新定价**：用户可访问[详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或使用：`python scripts/auth.py --price_info`（返回所有接口的完整定价信息）

### 查询计费规则

按**调用次数**计费，每次调用返回一页HS编码搜索结果：
- 每次API调用都会产生费用
- **执行前：**
  1. 告知用户本次查询将产生费用
  2. 停止，等待用户在单独的消息中明确确认，然后执行脚本

### 费用确认原则

**任何产生费用的操作都必须先告知用户并等待用户明确确认。不得在通知用户的同一条消息中执行。**

### 套餐计费与余额降级

搜索/海关/地图接口**默认走套餐**：脚本会自动携带 `"planMode": 2`。

- **套餐不可用**（无有效套餐或额度已用完）：脚本在业务执行前停止，不会产生扣费；stdout 会输出一行以 `PLAN_UNAVAILABLE ` 开头的 JSON，退出码为 **3**。**禁止自动重试**。
- **先询问用户**：用自然语言说明原因（无套餐 / 额度用完及恢复时间），说明改用余额将按接口定价扣费（单价用 `python scripts/auth.py --price_info` 查询），然后等待用户在独立消息中明确回复。
- **用户同意**：用同一条命令加环境变量 `UPKUAJING_PLAN_MODE=1` 重跑（PowerShell：`$env:UPKUAJING_PLAN_MODE='1'`），成功后向用户展示 `fee` 扣费信息。
- **用户拒绝**：本次不执行、不扣费；给出「稍后重试 / 升级套餐 / 使用余额」三个出口，同一轮不要重复弹窗。
- **改余额后仍余额不足**（95）：提示充值并停止，不再重试。
- **批量调用前**：先用 `python scripts/auth.py --plan_quota` 预检额度（档位上限用 `--plan_config`）；`available=0` 或目标窗口 `remaining=0` 时，直接先问是否用余额，避免必然失败的调用。
- **调用成功**：把 stderr 中 `[套餐]` 开头的用量信息转述给用户。
- **禁止**静默改走余额，**禁止**向用户暴露内部错误码原文。

完整契约见 [references/plan-billing.md](references/plan-billing.md)

## 工作流程

### 决策指南

| 用户意图 | 使用API |
|---------|--------|
| "搜索奶粉的HS编码" | HS编码搜索 |
| "查找以0402开头的HS编码" | HS编码搜索 |
| "查找产品的关税编码" | HS编码搜索 |

## 使用示例

### 搜索HS编码

**用户请求**："搜索奶粉以0402开头的HS编码"
```bash
python scripts/customs_analysis_hscode_search.py --params '{"product":"milk powder","hscode":"0402"}'
```

**查询下一页**：
```bash
python scripts/customs_analysis_hscode_search.py --params '{"product":"milk powder","hscode":"0402","cursor":"eyJpZCI6MX0="}'
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **套餐不可用（退出码 3 / `PLAN_UNAVAILABLE`）**：说明原因并询问是否改用余额，不要自动重试；参见 [套餐计费与余额降级](references/plan-billing.md)
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- HS编码搜索：查看 [references/customs-analysis-hscode-search-api.md](references/customs-analysis-hscode-search-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)
- 套餐计费与余额降级：[references/plan-billing.md](references/plan-billing.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-analysis-hscode-search-api.md](references/customs-analysis-hscode-search-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **搜索参数**：
   - `product` 和 `hscode` 都是必填参数
   - 同时提供产品名称和HS编码前缀可获得最佳结果

3. **跨技能使用**：
   - 使用找到的HS编码通过 **customs-analysis-hscode-detail** 获取编码描述
   - 使用找到的HS编码通过 **customs-analysis-trends** 或 **customs-analysis-area** 进行详细分析

## 注意事项
- `product` 和 `hscode` 都是必填参数
- 响应中的 `list` 包含匹配的HS编码字符串列表
- 所有平台均使用正斜杠路径
- **禁止输出技术参数格式**：不要在回复中显示代码风格的参数，应转换为自然语言
- **不要**估算或猜测每次调用的费用 — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 关联技能

其他可能对你有用的跨境魔方技能：

- customs-analysis-hscode-detail — 查询HS编码详细描述
- customs-analysis-trends — 查询进出口贸易趋势（按HS编码）
- customs-analysis-area — 查询贸易区域分布（按HS编码）
- customs-analysis-trade-percent — 查询各公司贸易占比
- customs-overview-summary — 查询国家贸易概览汇总
- customs-overview-trend — 查询进出口贸易月度趋势
- customs-company-hscode-list — 查询公司HS编码列表
- customs-company-product-list — 查询公司产品列表
- customs-company-stats — 查询公司贸易基础统计
- upkuajing-customs-trade-company-search — 海关贸易公司搜索