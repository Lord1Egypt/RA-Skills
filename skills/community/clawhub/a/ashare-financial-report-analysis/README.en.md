# clawhub

#### Description
A股上市公司财报结构化拆解系统 - 16节固定模板+8条核验纪律+多数据源(Tushare/akshare/baostock/东方财富)，跨季度可比的财报分析框架

#### Software Architecture
Hermes Agent Skill architecture: SKILL.md (main) + references/

#### Installation

1.  Clone this repo
2.  Copy `SKILL.md` to your Hermes Agent skills directory
3.  Copy `references/` alongside it

#### Instructions

1.  Load the skill in Hermes Agent
2.  Provide stock code and reporting period (e.g., "拆解德方纳米2025年年报")
3.  Agent fetches financial statements, fills 16-section template, runs 8 verification rules
4.  Review the structured earnings analysis report

#### Contribution

1.  Fork the repository
2.  Create Feat_xxx branch
3.  Commit your code
4.  Create Pull Request
