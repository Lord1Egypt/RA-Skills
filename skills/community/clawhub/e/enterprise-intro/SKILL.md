---
name: enterprise-intro
version: 1.0.1
description: >
  企业百科生成技能 - 基于多维企业数据生成专业的企业洞察简介报告。
  Use when: 用户需要生成企业信用分析报告、商业调研报告、投资尽调报告，或需要快速了解一家企业的综合信息。
  NOT for: 实时股票行情查询、个人征信查询、非中国大陆企业查询、需要最新财务数据（API数据可能有滞后）。
argument-hint: [企业名称]
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
metadata:
  openclaw:
    requires:
      env:
        - CHINADAAS_UID
        - CHINADAAS_KEY
        - CHINADAAS_BASE_URL
    primaryEnv: CHINADAAS_KEY
    emoji: "📊"
    homepage: https://qibook.com
---

# 企业百科生成技能

你是一位资深的企业信用分析师和大数据挖掘专家，擅长洞察企业价值，能够将多维信息转化为观点清晰、通俗易懂的商业报告。

## 数据与隐私声明

本技能需要调用外部 API 获取企业数据，使用前请了解以下信息：

### 外部网络请求

- **API 服务商**：企百科（https://qibook.com）
- **请求行为**：脚本会向 `CHINADAAS_BASE_URL` 指定的外部服务器发送 HTTPS 请求
- **传输数据**：查询的企业名称将被发送至 API 服务器
- **认证方式**：使用 `CHINADAAS_UID` 和 `CHINADAAS_KEY` 进行 API 身份认证

### 环境变量配置

使用本技能前，需要在 [企百科](https://qibook.com) 注册账号并获取 API 凭证，然后配置以下环境变量：

| 环境变量 | 说明 | 获取方式 |
|---------|------|---------|
| `CHINADAAS_UID` | API 用户 ID | 在企百科平台注册后获取 |
| `CHINADAAS_KEY` | API 密钥 | 在企百科平台注册后获取 |
| `CHINADAAS_BASE_URL` | API 基础 URL | 企百科平台提供 |

### 数据安全提示

- 请妥善保管 API 凭证，避免泄露
- 查询内容会传输至第三方服务，请勿查询敏感或机密企业信息
- 建议在信任企百科（qibook.com）服务后再使用本技能

## 核心能力

基于企业多维数据，生成名为《企业百科》的企业洞察简介，帮助以下读者群体快速、深刻地了解目标企业：
- 社会公众
- 金融投资/银行从业者
- 法律从业者
- 企业交易对手

## 支持的主体类型

根据不同主体类型，使用相应的报告模板：

| 主体类型 | 模板文件 | 说明 |
|---------|---------|------|
| 普通企业 | [templates/company.md](templates/company.md) | 完整的企业百科报告 |
| 分支机构 | [templates/branch.md](templates/branch.md) | 分支机构简介 |
| 政府机构 | [templates/organization/government.md](templates/organization/government.md) | 政府组织简介 |
| 医院 | [templates/organization/hospital.md](templates/organization/hospital.md) | 医疗机构简介 |
| 律师事务所 | [templates/organization/law_firm.md](templates/organization/law_firm.md) | 律所简介 |
| 学校 | [templates/organization/school.md](templates/organization/school.md) | 教育机构简介 |
| 社会组织 | [templates/organization/social.md](templates/organization/social.md) | 社会组织简介 |
| 其他组织 | [templates/organization/other.md](templates/organization/other.md) | 其他类型组织 |
| 个体工商户 | [templates/personal.md](templates/personal.md) | 个体户简介 |

## 数据处理流程

### 一体化脚本架构

使用 `scripts/` 目录下的21个一体化脚本获取并处理企业数据。每个脚本整合了 API 调用和数据后处理，提供统一的 `fetch(entname: str) -> str` 接口：

| 脚本 | 功能 | 说明 |
|------|------|------|
| s01_entity_info.py | 主体信息 | 企业基本工商信息、经营范围、资质等 |
| s02_listed_info.py | 上市信息 | 上市公司信息、股票代码、上市板块等 |
| s03_financial_info.py | 财务信息 | 财务指标、盈利能力、偿债能力等 |
| s04_debt_financing.py | 债权融资 | 债券发行、银行贷款等融资信息 |
| s05_risk_data.py | 风险大数据 | 风险事件、司法案件、行政处罚等 |
| s06_sentiment.py | 舆情信息 | 新闻舆情、媒体报道分析 |
| s08_controller.py | 实际控制人 | 股权穿透、实际控制人识别 |
| s09_related_parties.py | 关联方信息 | 关联企业、关联交易分析 |
| s10_customers.py | 客户/供应商 | 主要客户和供应商信息 |
| s11_operations.py | 企业经营动态 | 经营变更、业务动态 |
| s12_investment.py | 投融资事件 | 股权投融资、并购重组等 |
| s13_history.py | 历史大数据 | 历史工商变更、发展沿革 |
| s14_bidding.py | 招投标活动 | 中标、投标信息 |
| s15_group_info.py | 集团信息 | 集团架构、母子公司关系 |
| s16_portrait.py | 综合画像 | 企业属性画像、经营画像 |
| s17_ip.py | 知识产权 | 专利、商标、著作权等 |
| s18_innovation.py | 科创能力评估 | 科技创新能力、研发投入 |
| s19_shell_company.py | 空壳公司识别 | 空壳公司风险识别 |
| s20_risk_assessment.py | 风险评测 | 信用风险、欺诈风险评级 |
| s21_investment_query.py | 投资任职查询 | 法人投资任职情况 |

共享工具函数位于 `scripts/base.py`。

### 使用示例

```python
# 方式一：导入单个脚本
from scripts.s01_entity_info import fetch
result = fetch("企业名称")

# 方式二：通过统一入口
from scripts import fetch_entity_info, fetch_listed_info
result1 = fetch_entity_info("企业名称")
result2 = fetch_listed_info("企业名称")

# 方式三：批量获取
from scripts import fetch_multiple, fetch_all
# 获取指定维度
results = fetch_multiple(['entity_info', 'listed_info', 'financial_info'], "企业名称")
# 获取所有维度
all_results = fetch_all("企业名称")
```

### 命令行使用

```bash
# 运行单个脚本
python -m scripts.s01_entity_info <企业名称>
python -m scripts.s08_controller <企业名称>
```

## 目录结构

```
entintro_skill/
├── SKILL.md                # 技能定义文件
├── templates/              # 报告模板
│   ├── company.md          # 普通企业模板
│   ├── branch.md           # 分支机构模板
│   ├── personal.md         # 个体工商户模板
│   └── organization/       # 各类组织机构模板
├── references/             # 参考标准文档
├── examples/               # 示例
│   ├── sample_company_report.md  # 示例报告
│   └── data/               # 测试数据
└── scripts/                # 一体化数据脚本
    ├── __init__.py         # 统一入口
    ├── base.py             # 共享工具函数（API调用、数据格式化）
    ├── s01_entity_info.py  # 主体信息
    ├── s02_listed_info.py  # 上市信息
    ├── s03_financial_info.py # 财务信息
    ├── s04_debt_financing.py # 债权融资
    ├── s05_risk_data.py    # 风险大数据
    ├── s06_sentiment.py    # 舆情信息
    ├── s08_controller.py   # 实际控制人
    ├── s09_related_parties.py # 关联方信息
    ├── s10_customers.py    # 客户/供应商
    ├── s11_operations.py   # 企业经营动态
    ├── s12_investment.py   # 投融资事件
    ├── s13_history.py      # 历史大数据
    ├── s14_bidding.py      # 招投标活动
    ├── s15_group_info.py   # 集团信息
    ├── s16_portrait.py     # 综合画像
    ├── s17_ip.py           # 知识产权
    ├── s18_innovation.py   # 科创能力评估
    ├── s19_shell_company.py # 空壳公司识别
    ├── s20_risk_assessment.py # 风险评测
    └── s21_investment_query.py # 投资任职查询
```

## 参考标准

生成报告时需参考以下行业标准（位于 `references/` 目录）：
- 企业行业分类标准
- 企业绿色产业评估标准
- 人工智能行业标准
- 空壳公司判定标准
- 受益所有人标准
- 核心企业判定标准

## 输出规范

### 字数限制（必须严格遵守）
| 输入数据量 | 报告字数上限 |
|-----------|-------------|
| ≤ 15000字 | 1500字 |
| 15001~20000字 | 2500字 |
| ≥ 20001字 | 3500字 |

### 内容原则
1. **成品定位**：报告是最终成品，可直接交付使用
2. **扫读友好**：关键结论前置，句子平均长度 ≤ 20词
3. **数据驱动**：所有分析必须基于数据事实，禁止杜撰
4. **客观中立**：保持分析立场客观，避免主观臆断
5. **专业表达**：专业但不晦涩，避免AI味道

### 禁止事项
- 禁止简单罗列数据
- 禁止重复相同数据
- 禁止使用模糊词汇（"建议"、"可能"、"应考虑"等）
- 禁止超过字数上限

## 示例输出

- 示例报告位于 `examples/sample_company_report.md`
- 测试数据位于 `examples/data/`（按企业名称分组）

## 使用方式

```
/entintro [企业名称]
```

或直接提供企业数据 JSON，技能将自动识别主体类型并生成相应报告。
