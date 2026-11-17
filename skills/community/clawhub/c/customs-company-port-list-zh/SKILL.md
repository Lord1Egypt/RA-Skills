---
name: customs-company-port-list-zh
description: "查询公司海关贸易港口列表数据 — 获取港口的贸易次数、金额和占比，用于物流分析。\n\nTrigger: 海关港口列表，分页港口查询，公司贸易港口详情，进出口港口分析，贸易物流下钻"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"⚓","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# 海关公司贸易港口列表

通过跨境魔方开放平台API，查询公司分页的港口贸易数据。

## 概述

本技能提供从跨境魔方海关数据库中查询公司分页港口贸易数据的能力。给定公司ID和公司类型，返回港口列表及其贸易统计数据，包括交易次数、金额、数量、重量和占比。

## 运行脚本

### 环境设置

1. **检查Python版本**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`
运行示例：`python scripts/*.py`

**重要提示**：始终使用直接的脚本调用方式，如 `python scripts/customs_company_port_list.py`。**不要使用** `cd scripts && python customs_company_port_list.py` 这种复合命令。

### 公司贸易港口列表查询（`customs_company_port_list.py`）
- **返回粒度**：每个港口一条记录
- **使用场景**：浏览公司的贸易港口及详细统计，分析物流路线和港口级贸易量
- **示例**：
  - "列出公司100001作为供应商的贸易港口"
  - "查看公司100001作为采购商的港口贸易详情"
- **参数说明**：参见 [公司贸易港口列表API](references/customs-company-port-list-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/customs/company/port/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"公司贸易港口列表查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 费用

**所有API调用均产生费用**，不同接口计费方式不同。

**最新定价**：用户可访问[详细价格说明](https://www.upkuajing.com/web/openapi/price.html)
或使用：`python scripts/auth.py --price_info`（返回所有接口的完整定价信息）

### 查询计费规则

按**调用次数**计费，每次调用返回一页公司的港口列表：
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
| "列出公司100001作为供应商的贸易港口" | 公司贸易港口列表查询 |
| "查看公司100001的港口贸易分解" | 公司贸易港口列表查询 |

## 使用示例

### 查询公司贸易港口列表

**用户请求**："列出公司100001作为供应商的贸易港口"
```bash
python scripts/customs_company_port_list.py --params '{"companyId":100001,"companyType":1}'
```

**查询下一页**：
```bash
python scripts/customs_company_port_list.py --params '{"companyId":100001,"companyType":1,"cursor":"eyJsYXN0X2lkIjogMTAwMX0="}'
```

**带筛选条件查询**：
```bash
python scripts/customs_company_port_list.py --params '{"companyId":100001,"companyType":1,"dateStart":1700000000000,"dateEnd":1735689599999,"countryCodes":["KR"]}'
```

## 错误处理

- **API密钥无效/不存在**：检查 `~/.upkuajing/.env` 文件中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数错误**：**必须首先查看 references/ 目录下对应的API文档**，从文档中获取正确的参数名称和格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API文档参考

- 公司贸易港口列表：查看 [references/customs-company-port-list-api.md](references/customs-company-port-list-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 最佳实践

1. **检查API文档**：
   - **执行查询前，务必先查看对应的API参考文档**
   - 查看 [references/customs-company-port-list-api.md](references/customs-company-port-list-api.md)
   - 不要猜测参数名称，从文档中获取准确的参数名称和格式

2. **分页**：
   - 使用响应中的 `cursor` 参数获取下一页
   - 如果响应中不返回 `cursor`，表示没有更多数据

3. **数据解读**：
   - `percentTrade` 是贸易占比（百分比数值，如45.67表示45.67%）
   - `port` 是港口名称（如"BUSAN"）

4. **跨技能使用**：
   - 公司ID可以从 **customs-company-stats** 或 **upkuajing-customs-trade-company-search** 获取
   - 结果中的港口名称可用于筛选 **customs-company-trends** 和 **customs-company-partner-stats** 的数据

## 注意事项
- `companyType` 决定公司角色（1=供应商，2=采购商）
- 使用 `cursor` 进行分页 — 它是一个 base64 编码的字符串
- 所有平台均使用正斜杠路径
- **禁止输出技术参数格式**：不要在回复中显示代码风格的参数，应转换为自然语言
- **不要**估算或猜测每次调用的费用 — 使用 `python scripts/auth.py --price_info` 获取准确定价信息
- **不要**猜测参数名称，从文档中获取准确的参数名称和格式

## 关联技能

其他可能对你有用的跨境魔方技能：

- customs-company-area-stats — 查询公司贸易区域维度统计
- customs-company-area-list — 查询公司贸易区域列表
- customs-company-hscode-stats — 查询公司贸易HS编码维度统计
- customs-company-hscode-list — 查询公司贸易HS编码列表
- customs-company-product-list — 查询公司贸易产品列表
- customs-company-stats — 查询公司贸易基础统计
- customs-company-trends — 查询公司贸易趋势（月度分解）
- customs-company-partner-stats — 查询公司贸易伙伴分布
- upkuajing-customs-trade-company-search — 海关贸易公司搜索
- upkuajing-global-company-people-search — 统一全球企业与联系人搜索