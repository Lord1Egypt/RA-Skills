---
name: customs-overview-top-n-zh
description: "查询供应商或采购商TopN排名 — 按国家维度和年份返回供应商或采购商的贸易量排名列表，支持游标分页。\n\nTrigger: 供应商排名，采购商排名，Top供应商，Top采购商，贸易量排名，公司TopN"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏆","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关国家贸易概览-采供商TopN

通过跨境魔方开放平台API，查询供应商或采购商TopN排名数据。

## 概述

本技能提供从跨境魔方海关数据库中查询供应商或采购商TopN排名的能力。给定起运国、抵运国、年份和公司类型，返回按贸易量排名的公司列表，包含季度和月度贸易统计。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_overview_top_n.py`。**不要使用** `cd scripts && python customs_overview_top_n.py` 这种复合命令。

### 采供商TopN查询（`customs_overview_top_n.py`）
- **返回粒度**：每个公司一条记录
- **使用场景**：查找贸易路线中的顶级供应商或采购商，识别关键贸易伙伴，分析市场集中度
- **示例**：
  - "显示2025年从中国到美国的前10大供应商"
  - "列出2025年从中国进口到美国的前10大采购商"
- **参数说明**：参见 [采供商TopN API](references/customs-overview-top-n-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/top-n","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Top N查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用均产生费用**，不同接口计费方式不同。

**最新定价**：用户可访问[详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或使用：`python scripts/auth.py --price_info`（返回所有接口的完整定价信息）

### 查询计费规则

按**调用次数**计费，每次调用返回一页TopN排名数据：
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
| "显示2025年从中国到美国的前10大供应商" | TopN查询（companyType=1） |
| "列出2025年从中国进口到美国的前10大采购商" | TopN查询（companyType=2） |
| "查找中国出口到美国的最大出口商" | TopN查询（companyType=1） |

## 使用示例

### 查询采供商TopN

**用户请求**："显示2025年从中国到美国的顶级供应商"
```bash
python scripts/customs_overview_top_n.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025,"companyType":1}'
```

**查询顶级采购商**：
```bash
python scripts/customs_overview_top_n.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025,"companyType":2}'
```

**查询下一页**：
```bash
python scripts/customs_overview_top_n.py --params '{"originCountryCode":"CN","arrivalCountryCode":"US","year":2025,"companyType":1,"cursor":"eyJzdGFydCI6MH0="}'
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- 采供商TopN：查看 [references/customs-overview-top-n-api.md](references/customs-overview-top-n-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-overview-top-n-api.md](references/customs-overview-top-n-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **公司类型**：
   - `companyType=1` 表示供应商（出口方/卖方）
   - `companyType=2` 表示采购商（进口方/买方）

3. **分页**：
   - 使用响应中的 `cursor` 参数获取下一页
   - 如果响应中不返回 `cursor`，表示没有更多数据

4. **跨技能使用**：
   - 先用 **customs-overview-summary** 获取概览，再深入查看顶级公司
   - 结果中的公司ID可在 **customs-company-stats** 或 **customs-company-trends** 中使用
   - 结果中的公司名称可在 **upkuajing-customs-trade-company-search** 中搜索

## 注意事项
- `year` 和 `companyType` 都是必填参数
- `companyId` 是公司在跨境魔方数据库中的内部ID
- `latestTradeDate` 是Unix毫秒级时间戳
- 所有平台均使用正斜杠路径
- **禁止输出技术参数格式**：不要在回复中显示代码风格的参数，应转换为自然语言
- **不要**估算或猜测每次调用的费用 — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 关联技能

其他可能对你有用的跨境魔方技能：

- customs-overview-summary — 查询交易汇总（聚合）
- customs-overview-trade-list — 查询国家贸易列表（分页）
- customs-overview-trend — 查询进出口贸易月度趋势
- customs-overview-us-import — 查询美国进口交易统计
- customs-overview-date — 查询日期参考信息
- customs-company-stats — 查询公司贸易基础统计
- customs-company-trends — 查询公司贸易趋势（月度分解）
- customs-company-partner-stats — 查询公司贸易伙伴分布
- customs-company-area-stats — 查询公司贸易区域维度统计（聚合）
- upkuajing-customs-trade-company-search — 海关贸易公司搜索