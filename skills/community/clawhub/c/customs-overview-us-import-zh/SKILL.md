---
name: customs-overview-us-import-zh
description: "查询美国进口交易统计 — 按州或城市维度返回美国进口交易统计，包含进口记录数、集装箱数及近90天数据，支持游标分页。\n\nTrigger: 美国进口统计，按州查询进口，按城市查询进口，美国进口记录，美国集装箱数据"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🚢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关国家贸易概览-美国进口交易

通过跨境魔方开放平台API，查询美国进口交易统计数据。

## 概述

本技能提供从跨境魔方海关数据库中查询美国进口交易统计数据的能力。可以按州或城市维度查询进口数据，包括总进口记录数、集装箱数以及近90天的活动数据。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_overview_us_import.py`。**不要使用** `cd scripts && python customs_overview_us_import.py` 这种复合命令。

### 美国进口交易查询（`customs_overview_us_import.py`）
- **返回粒度**：每个州或城市一条记录
- **使用场景**：分析美国进口的州际或城市分布，监测近期进口活动，了解集装箱流量模式
- **示例**：
  - "显示按州统计的美国进口数据"
  - "获取按城市分组的美国进口数据"
- **参数说明**：参见 [美国进口交易API](references/customs-overview-us-import-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/us-import","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"美国进口查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用均产生费用**，不同接口计费方式不同。

**最新定价**：用户可访问[详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或使用：`python scripts/auth.py --price_info`（返回所有接口的完整定价信息）

### 查询计费规则

按**调用次数**计费，每次调用返回一页美国进口统计数据：
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
| "显示按州统计的美国进口数据" | 美国进口交易查询（type=state）|
| "获取按城市分组的美国进口数据" | 美国进口交易查询（type=city）|
| "哪些美国城市进口活动最活跃" | 美国进口交易查询（type=city）|

## 使用示例

### 查询美国进口交易统计

**用户请求**："显示按州统计的美国进口数据"
```bash
python scripts/customs_overview_us_import.py --params '{"type":"state"}'
```

**按城市查询**：
```bash
python scripts/customs_overview_us_import.py --params '{"type":"city"}'
```

**查询下一页**：
```bash
python scripts/customs_overview_us_import.py --params '{"type":"state","cursor":"eyJzdGFydCI6MH0="}'
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- 美国进口交易：查看 [references/customs-overview-us-import-api.md](references/customs-overview-us-import-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-overview-us-import-api.md](references/customs-overview-us-import-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **查询类型**：
   - `type=state` 按美国州分组（如"California"）
   - `type=city` 按美国城市分组
   - `type` 是唯一必需的参数

3. **数据字段解读**：
   - `records` 是总进口记录数
   - `recordsLast90Days` 显示近期进口活动
   - `containers` 是总集装箱数
   - `containersLast90Days` 显示近期集装箱活动

4. **分页**：
   - 使用响应中的 `cursor` 参数获取下一页
   - 如果响应中不返回 `cursor`，表示没有更多数据

5. **跨技能使用**：
   - 使用 **customs-overview-summary** 了解总体贸易量，然后用此技能查看美国特定分解
   - 结果可与 **customs-company-port-list** 结合进行港口级分析

## 注意事项
- `type` 是唯一必需的参数
- 响应中的 `name` 包含州名或城市名
- 90天数据字段有助于识别近期贸易活动趋势
- 所有平台均使用正斜杠路径
- **禁止输出技术参数格式**：不要在回复中显示代码风格的参数，应转换为自然语言
- **不要**估算或猜测每次调用的费用 — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 关联技能

其他可能对你有用的跨境魔方技能：

- customs-overview-summary — 查询交易汇总（聚合）
- customs-overview-trade-list — 查询国家贸易列表（分页）
- customs-overview-trend — 查询进出口贸易月度趋势
- customs-overview-top-n — 查询供应商或采购商TopN排名
- customs-overview-date — 查询日期参考信息
- customs-company-stats — 查询公司贸易基础统计
- customs-company-trends — 查询公司贸易趋势（月度分解）
- customs-company-port-list — 查询公司贸易港口列表
- customs-company-area-stats — 查询公司贸易区域维度统计（聚合）
- upkuajing-customs-trade-company-search — 海关贸易公司搜索