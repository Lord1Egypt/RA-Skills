---
name: b2b-lead-generation-zh
description: "B2B线索生成工具集，聚合海关贸易情报、全球企业深度背调与LinkedIn职业人脉数据。分析HS编码市场分布/趋势/占比、剖析任一公司的贸易规模/伙伴/产品/港口、获取宏观国家级贸易概览与Top买家/供应商、开展公司深度背调（员工、股东/UBO、决策人）并绘制LinkedIn职业人脉图谱（同事、校友、履历与学历）。\n\nTrigger: B2B线索生成, 海关贸易分析, HS编码搜索, 贸易地区分布, 进出口趋势, 公司贸易占比, 企业贸易统计, 贸易伙伴分析, 宏观贸易概览, Top买家供应商, 美国进口数据, 全球企业搜索, 公司员工名单, 股东UBO, 人物搜索, 同事校友, 工作经历学历, 学校详情, 尽职调查背调, LinkedIn找公司, LinkedIn找人, 职业人脉图谱, 高管猎头, 海外线索生成, 跨境供应商寻源"
metadata: {"version":"1.0.1","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🎯","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# B2B 线索生成（Lead Generation）

聚合技能：**海关贸易情报** + **全球企业深度背调** + **LinkedIn 职业人脉**。3 大数据源、38 个脚本，按域索引路由。

## 概览

三大数据源，各由一个域索引（意图->脚本决策表）承载：

| 数据源 | 解决什么问题 | 索引 |
|--------|-------------|------|
| 海关 - HS编码分析 | 某产品（HS编码）的市场分布/趋势/占比 | [indexes/customs-analysis.md](indexes/customs-analysis.md) |
| 海关 - 公司贸易 | 单个公司的贸易规模、伙伴、产品、港口、趋势 | [indexes/customs-company.md](indexes/customs-company.md) |
| 海关 - 宏观概览 | 国家级贸易总量、Top买家/供应商、美国进口 | [indexes/customs-overview.md](indexes/customs-overview.md) |
| 全球企业 - 深度 | 工商信息、股东/UBO、员工、决策人（全球企业库） | [indexes/global-depth.md](indexes/global-depth.md) |
| LinkedIn | 职业人脉：公司、人物、同事、校友、履历 | [indexes/linkedin.md](indexes/linkedin.md) |

## 运行脚本

### 环境准备

1. **检查 Python**：`python --version`
2. **安装依赖**：`pip install -r requirements.txt`

脚本目录：`scripts/*.py`

**重要**：始终用直接调用方式，如 `python scripts/customs_analysis_area.py`。**不要**用 `cd scripts && python customs_analysis_area.py` 这类 shell 复合命令。

### 如何选脚本

1. 把用户意图对应到上表的某个**数据源**。
2. 打开对应的 `indexes/<域>.md` —— 它是意图->脚本决策表，把每个意图精确到唯一脚本。
3. 打开该脚本的 `references/<xxx>-api.md` 获取准确参数名/格式 —— **切勿猜测参数**。

## 路由决策树

| 用户意图 | 路由到 |
|---------|--------|
| 分析某 HS 编码的市场分布/趋势/占比/概览 | [indexes/customs-analysis.md](indexes/customs-analysis.md) |
| 剖析某公司的贸易规模/伙伴/产品/港口/趋势 | [indexes/customs-company.md](indexes/customs-company.md) |
| 宏观国家级贸易概览/Top买家供应商/美国进口 | [indexes/customs-overview.md](indexes/customs-overview.md) |
| 公司工商/股东UBO/员工/决策人（背调） | [indexes/global-depth.md](indexes/global-depth.md) |
| LinkedIn 公司/人物/职业人脉/履历学历 | [indexes/linkedin.md](indexes/linkedin.md) |

### 跨技能转交（本技能不含的能力）

以下属 standalone 配套技能，用户需要时转交：

| 用户想要 | 转交到 |
|---------|--------|
| 找有**真实贸易记录**的买家/供应商（贸易记录搜索） | `upkuajing-customs-trade-company-search`（= `upkuajing-trade-company-search`） |
| **快速**查公司/人 + 联系方式（浅层快查） | `upkuajing-company-people-search`（= `upkuajing-global-company-people-search`） |
| 触达前校验/清洗联系方式 | `b2b-outreach`（phone/email/domain 校验）或 `upkuajing-contact-info-validity-check` |
| 找到线索后发邮件/短信/地图采集商户 | `b2b-outreach` |

## 组合工作流（跨数据源，仅聚合技能可做到）

1. **找海外买家全链路**（跨技能）：`upkuajing-customs-trade-company-search`（找有贸易记录的买家）-> 本技能 `global-depth`/`linkedin`（找决策人）-> `b2b-outreach` 校验联系方式 -> `b2b-outreach` 触达。
2. **供应商背调**：`global-depth`（`global_company_search` -> `company_shareholder_list` / `company_employee_list`）-> `customs-company`（`customs_company_stats` 看真实贸易规模）。
3. **人才 mapping**：`linkedin`（`linkedin_company_employee_list`）-> `linkedin_person_experience_list` / `linkedin_person_education_list`（背调）。
4. **先量后打**：`customs-overview`（`summary`/`top_n` 估算市场规模）-> `customs-analysis`（`trade_percent` 找头部玩家）-> `global-depth`（背调头部玩家）。

## API 密钥与充值

本技能需要 API 密钥，存储在 `~/.upkuajing/.env`：
```bash
cat ~/.upkuajing/.env
```
```
UPKUAJING_API_KEY=your_api_key_here
```

### 未设置 API 密钥
先检查 `~/.upkuajing/.env` 是否有 `UPKUAJING_API_KEY`。若没有，提示用户选择：
1. 用户已有：用户提供（手动写入 `~/.upkuajing/.env`）
2. 用户没有：用 `auth.py --new_key` 申请（自动保存到 `~/.upkuajing/.env`）

等待用户选择。

### 账户充值
当 API 返回余额不足时：
1. 创建充值订单（`auth.py --new_rec_order`）
2. 把支付页面 URL 发给用户，引导其打开并支付；用户确认成功后再继续。

### 获取账户信息
`python scripts/auth.py --account_info`

新申请的密钥需在 [跨境魔方开放平台](https://developer.upkuajing.com/) 注册绑定。

### **上报Skill调用异常**
当API调用失败或返回异常数据（服务端错误、超时、响应格式错误等）时，先用自然语言向用户解释异常情况，并询问是否需要上报给平台追踪；用户确认后才执行上报：
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/customs/analysis/area","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"海关区域分布查询失败，服务端异常"}'
```
- **不要上报正常业务情况**（余额不足、API密钥无效、参数错误等），按各自原有流程处理
- 异常上报不产生查询费用
- **参数说明**：参见 [异常上报API](references/skill-error-report-api.md)

## 计费

**所有 API 调用均收费**，不同接口计费方式不同。

**最新定价**：访问 [详细价格说明](https://www.upkuajing.com/web/openapi/price.html)，或运行：
```bash
python scripts/auth.py --price_info
```
（返回全部接口定价 —— 聚合版 auth.py 优先拉取全量定价列表，必要时回退到按原始技能名逐一查询。）

### 计费规则（概要）
- **query_count 搜索**（4 个脚本：`global_company_search`、`global_company_person_search`、`linkedin_company_search`、`linkedin_person_search`）：按调用次数计费 = `ceil(query_count / 20)`；每次返回最多 20 条（`query_count` 范围 20–1000）。当 `query_count > 20` 时，先告知用户预计调用次数。
- **其余脚本**（customs 分析/公司/宏观；global/linkedin 列表与详情接口）：**按次计费**。游标分页脚本每次返回一页——传入上次响应的 `cursor` 获取下一页；单记录脚本（统计、汇总、日期、学校详情）每次返回一条。
- **所有调用均收费**——本技能没有免费查询。
- 各接口计费细则见对应 `references/<xxx>-api.md`。

### 计费确认原则

**任何收费操作必须先告知用户并在单独的消息中等待明确确认，不得在通知的同一消息中执行。** 当 `query_count` 超过一页时，先告知用户预计调用次数。

## 错误处理

- **API 密钥无效/不存在**：检查 `~/.upkuajing/.env` 中的 `UPKUAJING_API_KEY`
- **余额不足**：引导用户充值
- **参数无效**：**必须先查 `references/` 下对应 API 文档**，从文档获取正确参数名/格式，不要猜测
- **Skill调用异常/响应异常**：先友好告知用户，经用户确认后用 `python scripts/error_report.py` 上报给平台（参见 [上报Skill调用异常](#上报skill调用异常)）

### API 文档参考

**customs-analysis**（路由：[indexes/customs-analysis.md](indexes/customs-analysis.md)）
- [area](references/customs-analysis-area-api.md) | [hscode-detail](references/customs-analysis-hscode-detail-api.md) | [hscode-search](references/customs-analysis-hscode-search-api.md) | [overview](references/customs-analysis-overview-api.md) | [trade-percent](references/customs-analysis-trade-percent-api.md) | [trends](references/customs-analysis-trends-api.md)

**customs-company**（路由：[indexes/customs-company.md](indexes/customs-company.md)）
- [area-list](references/customs-company-area-list-api.md) | [area-stats](references/customs-company-area-stats-api.md) | [hscode-list](references/customs-company-hscode-list-api.md) | [hscode-stats](references/customs-company-hscode-stats-api.md) | [partner-stats](references/customs-company-partner-stats-api.md) | [port-list](references/customs-company-port-list-api.md) | [product-list](references/customs-company-product-list-api.md) | [stats](references/customs-company-stats-api.md) | [trends](references/customs-company-trends-api.md)

**customs-overview**（路由：[indexes/customs-overview.md](indexes/customs-overview.md)）
- [date](references/customs-overview-date-api.md) | [summary](references/customs-overview-summary-api.md) | [top-n](references/customs-overview-top-n-api.md) | [trade-list](references/customs-overview-trade-list-api.md) | [trend](references/customs-overview-trend-api.md) | [us-import](references/customs-overview-us-import-api.md)

**global-depth**（路由：[indexes/global-depth.md](indexes/global-depth.md)）
- [global-company-list](references/global-company-list-api.md) | [company-employee-list](references/company-employee-list-api.md) | [company-shareholder-list](references/company-shareholder-list-api.md) | [global-company-person-list](references/global-company-person-list-api.md) | [person-colleague-list](references/person-colleague-list-api.md) | [person-alumni-list](references/person-alumni-list-api.md) | [person-experience-list](references/person-experience-list-api.md) | [person-education-list](references/person-education-list-api.md) | [school-detail](references/school-detail-api.md)

**linkedin**（路由：[indexes/linkedin.md](indexes/linkedin.md)）
- [linkedin-company-list](references/linkedin-company-list-api.md) | [linkedin-company-employee-list](references/linkedin-company-employee-list-api.md) | [linkedin-person-list](references/linkedin-person-list-api.md) | [linkedin-person-colleague-list](references/linkedin-person-colleague-list-api.md) | [linkedin-person-alumni-list](references/linkedin-person-alumni-list-api.md) | [linkedin-person-experience-list](references/linkedin-person-experience-list-api.md) | [linkedin-person-education-list](references/linkedin-person-education-list-api.md) | [linkedin-school-detail](references/linkedin-school-detail-api.md)
- 异常上报：查看 [references/skill-error-report-api.md](references/skill-error-report-api.md)

## 注意事项

- `countryType`：`1` = 出口国（供应商），`2` = 进口国（买家）。
- ID 按数据源隔离：global-depth 的 `pid`/`hid` 与 LinkedIn 的 `pid`/`hid` 不通用 —— 一次调查保持在单一数据源内。
- 大型**搜索**查询（global/linkedin `*_search`）返回 `task_id` + `file_url`；用 `--task_id` 续跑可追加数据。customs 与列表类脚本用**游标**分页--把上次响应返回的 `cursor` 放入 `--params` 获取下一页。
- `task_data/` 按 UUID 子目录存放结果。
- 所有平台文件路径使用正斜杠。
- **禁止输出技术参数格式**：回复中把代码式参数转为自然语言。
- **不要**估算每次调用费用 —— 用 `auth.py --price_info` 获取准确定价。
- **不要**猜测参数名 —— 先读 `references/<xxx>-api.md`。

## 关联技能

其他可能有用的 UpKuaJing 技能：

- b2b-outreach - 发邮件/短信、地图采集商户、校验联系方式（phone/email/domain）
- upkuajing-customs-trade-company-search（= upkuajing-trade-company-search）- 搜索有真实海关贸易记录的公司
- upkuajing-company-people-search（= upkuajing-global-company-people-search）- 快速浅层查公司/人 + 联系方式
- upkuajing-contact-info-validity-check - 独立校验联系方式（phone/email/domain）
- upkuajing-email-tool - 独立的邮件发送与任务跟踪
- upkuajing-sms-tool - 独立的短信发送与任务跟踪
- upkuajing-map-merchants-search - 独立的 Google Maps 商户采集
