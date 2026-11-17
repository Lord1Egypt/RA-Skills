---
name: customs-analysis-trends-zh
description: "查询分析报告-贸易趋势 — 查询指定HS编码在最近N个月的进出口贸易趋势数据。\n\nTrigger: 贸易趋势，进出口分析，HS编码趋势，月度贸易数据，贸易时间序列分析"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📈","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关分析报告-贸易趋势

通过跨境魔方开放平台API，查询进出口贸易趋势数据。

## 概述

本技能提供指定HS编码在最近N个月的进出口贸易趋势数据。返回出口和进口数据，包含月度贸易次数、数量、重量、金额、采购商和供应商数量等信息。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_analysis_trends.py`。**不要使用** `cd scripts && python customs_analysis_trends.py` 这种复合命令。

### 趋势查询（`customs_analysis_trends.py`）
- **返回粒度**：月度聚合的进出口数据
- **使用场景**：分析特定产品随时间变化的贸易趋势，了解季节性模式，比较进出口活动
- **示例**：
  - "显示HS编码04021000最近12个月的贸易趋势"
  - "获取产品04021000从中国的进出口趋势"
- **参数说明**：参见 [贸易趋势API](references/customs-analysis-trends-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/trends","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"贸易趋势查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用均产生费用**，不同接口计费方式不同。

**最新定价**：用户可访问[详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或使用：`python scripts/auth.py --price_info`（返回所有接口的完整定价信息）

### 查询计费规则

按**调用次数**计费，每次调用返回一页趋势数据：
- 每次API调用都会产生费用
- **执行前：**
  1. 告知用户本次查询将产生费用
  2. 停止，等待用户在单独的消息中明确确认，然后执行脚本

### 费用确认原则

**任何产生费用的操作都必须先告知用户并等待用户明确确认。不得在通知用户的同一条消息中执行。**

## 工作流程

### 决策指南

| 用户意图 | 使用API |
|---------|--------|
| "显示HS编码04021000最近12个月的贸易趋势" | 趋势查询 |
| "这个产品的贸易随时间如何变化？" | 趋势查询 |
| "比较产品04021000的出口和进口" | 趋势查询 |

## 使用示例

### 查询贸易趋势

**用户请求**："显示HS编码04021000最近12个月的贸易趋势"
```bash
python scripts/customs_analysis_trends.py --params '{"hscode":"04021000","recentMonths":12}'
```

**按国家筛选查询**：
```bash
python scripts/customs_analysis_trends.py --params '{"hscode":"04021000","countryCode":"CN","recentMonths":12}'
```

**查询下一页**：
```bash
python scripts/customs_analysis_trends.py --params '{"hscode":"04021000","recentMonths":12,"cursor":"eyJpZCI6MX0="}'
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- 贸易趋势：查看 [references/customs-analysis-trends-api.md](references/customs-analysis-trends-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-analysis-trends-api.md](references/customs-analysis-trends-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **参数说明**：
   - `hscode` 和 `recentMonths` 是必填参数
   - `countryCode` 是可选的 — 省略则获取该HS编码的全球趋势

3. **跨技能使用**：
   - 先使用 **customs-analysis-hscode-search** 和 **customs-analysis-hscode-detail** 查找并了解HS编码
   - 结合 **customs-analysis-area** 获取地理分布，或 **customs-analysis-trade-percent** 获取公司级分解

## 注意事项
- `hscode` 和 `recentMonths` 是必填参数
- 响应中包含 `exportData` 和 `importData` 两个维度的月度数据
- `month` 是YYYYMM格式（如"202406"）
- 所有平台均使用正斜杠路径
- **禁止输出技术参数格式**：不要在回复中显示代码风格的参数，应转换为自然语言
- **不要**估算或猜测每次调用的费用 — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 关联技能

其他可能对你有用的跨境魔方技能：

- customs-analysis-area — 查询贸易区域分布（按HS编码）
- customs-analysis-trade-percent — 查询各公司贸易占比
- customs-analysis-hscode-search — 搜索HS编码（按产品和关键字）
- customs-analysis-hscode-detail — 查询HS编码详细描述
- customs-overview-trend — 查询进出口贸易月度趋势
- customs-overview-summary — 查询国家贸易概览汇总
- customs-company-trends — 查询公司贸易趋势（月度分解）
- customs-company-stats — 查询公司贸易基础统计
- customs-company-product-list — 查询公司产品列表
- upkuajing-customs-trade-company-search — 海关贸易公司搜索