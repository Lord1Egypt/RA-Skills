---
name: customs-overview-trend-zh
description: "查询进出口贸易趋势数据 — 按月份维度返回指定时间范围内的贸易总量趋势数据，支持游标分页。\n\nTrigger: 贸易趋势，进出口趋势，月度贸易量，贸易时间序列，贸易日期范围查询"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📈","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关国家贸易概览-进出口趋势

通过跨境魔方开放平台API，查询进出口贸易趋势数据。

## 概述

本技能提供从跨境魔方海关数据库中查询进出口贸易趋势数据的能力。给定时间范围（起始和结束月份），返回分页的月度贸易总量列表，帮助分析贸易模式和季节性趋势。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_overview_trend.py`。**不要使用** `cd scripts && python customs_overview_trend.py` 这种复合命令。

### 进出口趋势查询（`customs_overview_trend.py`）
- **返回粒度**：每个月一条记录
- **使用场景**：分析贸易随时间的变化趋势，发现季节性模式，比较月度贸易量
- **示例**：
  - "显示2025年1月到12月中国到美国的贸易趋势"
  - "获取2025年中国和美国之间的月度贸易量"
- **参数说明**：参见 [进出口趋势API](references/customs-overview-trend-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/trend","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"贸易趋势查询失败，服务端异常"}'
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
| "显示2025年1月到12月中国到美国的贸易趋势" | 进出口趋势查询 |
| "获取2025年中国和美国之间的月度贸易量" | 进出口趋势查询 |
| "逐月比较贸易量" | 进出口趋势查询 |

## 使用示例

### 查询进出口趋势

**用户请求**："显示2025年1月到12月中国到美国的贸易趋势"
```bash
python scripts/customs_overview_trend.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202512}'
```

**查询下一页**：
```bash
python scripts/customs_overview_trend.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202512,"cursor":"eyJzdGFydCI6MH0="}'
```

**查询特定季度**：
```bash
python scripts/customs_overview_trend.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","startDate":202501,"endDate":202503}'
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- 进出口趋势：查看 [references/customs-overview-trend-api.md](references/customs-overview-trend-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-overview-trend-api.md](references/customs-overview-trend-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **日期格式**：
   - 使用6位年月格式（如202501表示2025年1月）
   - `startDate` 和 `endDate` 都是必填参数

3. **分页**：
   - 使用响应中的 `cursor` 参数获取下一页
   - 如果响应中不返回 `cursor`，表示没有更多数据

4. **跨技能使用**：
   - 使用 **customs-overview-summary** 获取高级别年度数据，然后用此技能查看月度分解
   - 结合 **customs-company-trends** 进行公司级趋势分析

## 注意事项
- `startDate` 和 `endDate` 都是必填参数
- 响应中的 `tradeDate` 是年月格式（如202501）
- `tradeTotal` 是该月的贸易总量
- 所有平台均使用正斜杠路径
- **禁止输出技术参数格式**：不要在回复中显示代码风格的参数，应转换为自然语言
- **不要**估算或猜测每次调用的费用 — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 关联技能

其他可能对你有用的跨境魔方技能：

- customs-overview-summary — 查询交易汇总（聚合）
- customs-overview-trade-list — 查询国家贸易列表（分页）
- customs-overview-top-n — 查询供应商或采购商TopN排名
- customs-overview-us-import — 查询美国进口交易统计
- customs-overview-date — 查询日期参考信息
- customs-company-stats — 查询公司贸易基础统计
- customs-company-trends — 查询公司贸易趋势（月度分解）
- customs-company-partner-stats — 查询公司贸易伙伴分布
- customs-company-area-stats — 查询公司贸易区域维度统计（聚合）
- upkuajing-customs-trade-company-search — 海关贸易公司搜索