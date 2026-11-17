---
name: customs-overview-date-zh
description: "查询日期参考信息 — 返回去年年份、上月月份、去年当月月份等日期参考值，用于贸易查询。\n\nTrigger: 日期参考, 去年年份, 上月月份, 去年当月, 贸易查询日期, 参考日期信息"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📅","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关国家贸易概览-日期相关

通过跨境魔方开放平台API，查询日期参考信息。

## 概述

本技能提供从跨境魔方系统查询日期参考值的能力。返回去年年份、上月年月和去年当月的年月值。这些参考日期在构建其他海关概览技能（交易汇总、国家贸易列表、进出口趋势等）的查询时非常有用。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_overview_date.py`。**不要使用** `cd scripts && python customs_overview_date.py` 这种复合命令。

### 日期参考查询（`customs_overview_date.py`）
- **返回粒度**：每次查询返回一组日期参考值
- **使用场景**：获取构建贸易查询所需的参考日期，查找用于概览查询的去年年份值，查找用于趋势查询的上月月份值
- **示例**：
  - "查询最新的贸易数据月份"
  - "获取海关概览查询的参考日期"
- **参数说明**：参见 [日期参考API](references/customs-overview-date-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/overview/date","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"日期概览查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用均产生费用**，不同接口计费方式不同。

**最新定价**：用户可访问[详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或使用：`python scripts/auth.py --price_info`（返回所有接口的完整定价信息）

### 查询计费规则

按**调用次数**计费，每次调用返回一组日期参考值：
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
| "获取海关概览的参考日期" | 日期参考查询 |
| "查询贸易数据的年份和月份值" | 日期参考查询 |
| "查找有可用贸易数据的最近月份" | 日期参考查询 |

## 使用示例

### 查询日期参考

**用户请求**："获取海关概览的参考日期"
```bash
python scripts/customs_overview_date.py --params '{}'
```

响应提供：
- `yesteryear`：去年年份（如2025）
- `lastMonth`：上月月份（如202604）
- `yesteryearMonth`：去年当月月份（如202504）

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- 日期相关：查看 [references/customs-overview-date-api.md](references/customs-overview-date-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-overview-date-api.md](references/customs-overview-date-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **无需业务参数**：
   - 传入空JSON对象 `{}` 作为参数
   - 该接口没有业务请求参数

3. **使用结果**：
   - 使用 `yesteryear` 作为 **customs-overview-summary**、**customs-overview-trade-list** 和 **customs-overview-top-n** 的 `year` 参数
   - 使用 `lastMonth` 和 `yesteryearMonth` 作为 **customs-overview-trend** 的 `startDate`/`endDate` 参考
   - 日期参考值是根据当前日期由系统计算的

4. **跨技能使用**：
   - 在进行其他概览查询前，使用此技能获取正确的日期值
   - 当用户未指定精确年份或月份时尤其有用

## 注意事项
- 无需业务参数 — 传入空JSON对象 `{}` 即可
- `yesteryear` 是上一个日历年份（4位数字）
- `lastMonth` 是上一个日历月份（6位年月格式）
- `yesteryearMonth` 是去年同月的年月值
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
- customs-overview-us-import — 查询美国进口交易统计
- customs-company-stats — 查询公司贸易基础统计
- customs-company-trends — 查询公司贸易趋势（月度分解）
- customs-company-partner-stats — 查询公司贸易伙伴分布
- customs-company-area-stats — 查询公司贸易区域维度统计（聚合）
- upkuajing-customs-trade-company-search — 海关贸易公司搜索