---
name: customs-company-stats-zh
description: 调取海关进出口数据获取企业基础贸易统计信息，整理出企业贸易频次、出货数量、货物重量、交易金额以及合作客商总数，帮助外贸从业者评估企业整体交易规模和客户布局情况。
metadata: {"version":"1.0.2","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"📊","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关公司贸易基础统计查询

使用跨境魔方开放平台API从海关数据查询公司的贸易基础统计信息。

## 概述

本技能提供对跨境魔方海关公司贸易基础统计数据的查询。通过公司ID（companyId）和公司类型，获取公司的贸易汇总统计数据，包括交易次数、总重量、总数量、总金额、合作伙伴数量及交易时间范围等。

## 脚本运行

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要**：始终使用直接脚本调用，如 `python scripts/customs_company_stats.py`。**不要使用** shell 复合命令如 `cd scripts && python customs_company_stats.py`

### 公司贸易基础统计查询 (`customs_company_stats.py`)
- **返回粒度**：每条记录对应一家公司的贸易统计数据汇总
- **适用场景**：查看公司的整体贸易概况，了解交易规模和合作伙伴数量
- **示例**：
  - "查询公司100001的供应商贸易统计数据"
  - "查询公司100001的采购商贸易统计数据"
- **参数**：查看参数说明 [公司贸易基础统计 API](references/customs-company-stats-api.md)

## API密钥与充值
使用此技能需要API密钥。API密钥保存在 `~/.upkuajing/.env` 文件中：
```bash
cat ~/.upkuajing/.env
```
**文件内容示例**：
```
UPKUAJING_API_KEY=your_api_key_here
```
### **未设置API密钥**
请先检查 `~/.upkuajing/.env` 文件是否有 UPKUAJING_API_KEY;
如果未设置 UPKUAJING_API_KEY API密钥，请提示并让用户选择：
1. 用户有，由用户提供(手动添加到 ~/.upkuajing/.env 文件)
2. 用户没有，你可使用接口进行申请（`auth.py --new_key`），申请到新密钥后，会自动保存到 ~/.upkuajing/.env
等待用户选择；

### **账户充值**
如果调用接口响应账户余额不足时，需说明并引导用户进行账户充值：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 根据订单响应，发送支付页面URL给用户，引导用户打开地址付款，付款成功后告诉你；

### **获取账户信息**
可通过此脚本，获取UPKUAJING_API_KEY对应的账户信息 `auth.py --account_info`

## API密钥与跨境魔方账号
- 新申请的API密钥：在[跨境魔方开放平台](https://developer.upkuajing.com/)注册、登录后进行账号绑定

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/customs/company/stats","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"公司贸易基础统计查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用都会产生费用**，不同接口计费方式不同。

**最新价格**：用户可访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或者使用：`python scripts/auth.py --price_info`（返回接口完整定价）

### 查询计费规则

按**调用次数**计费，每次调用返回一家公司的贸易统计数据：
- 每次API调用产生一次费用
- **执行前必须：**
  1. 告知用户本次查询会产生费用
  2. 停止，等待用户在独立消息中明确确认后，再执行脚本

### 费用确认原则

**任何会产生费用的操作，都必须先告知、等待用户明确确认，不得在告知的同一条消息中直接执行。**

## 工作流程

### 决策指南

| 用户意图 | 使用API |
|---------|--------|
| "查询公司100001的供应商贸易统计数据" | 公司贸易基础统计查询 |
| "查询公司100001的采购商贸易统计数据" | 公司贸易基础统计查询 |

## 使用示例

### 查询公司贸易基础统计

**用户请求**："查询公司100001的供应商贸易统计数据"
```bash
python scripts/customs_company_stats.py --companyId 100001 --companyType 1
```

**用户请求**："查询公司100001的采购商贸易统计数据"
```bash
python scripts/customs_company_stats.py --companyId 100001 --companyType 2
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：**必须先查看 references/ 目录下的对应 API 文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API Documentation Reference

- 公司贸易基础统计：查看 [references/customs-company-stats-api.md](references/customs-company-stats-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **查看API文档**：
   - **执行查询前，必须先查看对应的 API 参考文档**
   - 查看 [references/customs-company-stats-api.md](references/customs-company-stats-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **数据解读**：
   - `countTrade` 为总交易次数
   - `countWeight`、`countQuantity`、`countAmount` 为汇总总量
   - `countPartner` 为不重复的贸易伙伴数量
   - `earliestTradeDate` 和 `latestTradeDate` 定义了公司的贸易活动时间范围

3. **跨技能使用**：
   - 结果中的公司ID可与 **customs-company-trends** 配合查询月度贸易趋势
   - 也可与 **customs-company-partner-stats** 配合查询贸易伙伴分布数据

## 注意事项
- `companyType` 决定了公司的角色（1=供应商，2=采购商）
- `earliestTradeDate` 为日期字符串（如 "2020-01-15"），`latestTradeDate` 为毫秒级时间戳
- 文件路径在所有平台上都使用正斜杠
- **禁止输出技术参数格式**：不要在回复中展示代码样式的参数，应将其转换为自然语言
- **不要估算或猜测每次调用的费用** — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 相关技能

其他您可能会用到的跨境魔方技能：

- customs-company-trends — 海关公司贸易趋势查询
- customs-company-partner-stats — 海关公司贸易伙伴趋势查询
- upkuajing-customs-trade-company-search — 海关贸易企业搜索
- upkuajing-global-company-people-search — 全来源统一的企业与人物搜索
- global-company-search — 全球企业库找公司
- global-company-person-search — 全球企业库找人
- global-company-shareholder — 全球企业库股东查询
- global-company-employee — 全球企业库员工查询
- upkuajing-contact-info-validity-check — 联系方式有效性检测
- phone-validity-check — 电话号码有效性检测
