# 中国企业报税员 · china-tax-clerk

面向中国大陆常见企业税费的 Agent Skill：核对资料、查证政策、运行确定性计算、生成申报底稿和复核清单。

**v0.1.0 是初始测算版本。** 内置政策快照为 2026-10-10，计算脚本仅接受 2026—2027 年同一年度内的所属期。正式使用前须核验当期政策、地区口径及业务适用条件。2027 年规则依据已公布政策的有效期推算，届时仍需核验。

China mainland tax preparation skill with a local, standard-library Python calculator, policy references, workpaper templates, and synthetic regression tests.

## 能做什么

| 计算模式 | 覆盖内容 |
|---|---|
| `small_vat` | 普通按月/季小规模增值税，分别处理免税与放弃免税交易 |
| `general_vat` | 普通一般计税的销项、进项、转出、留抵及预缴 |
| `cit` | 普通居民企业所得税年度/累计预缴复算、小型微利资格判断 |
| `payroll` | 居民工资累计预扣 |
| `iit_annual` | 居民综合所得年度税额及已缴差额，免办汇算条件需另核 |
| `bonus_compare` | 单笔合格全年一次性奖金的两种计税方案比较 |
| `surcharges` | 普通城建税、教育费附加、地方教育附加 |
| `stamp` | 普通动产买卖合同及资金账簿印花税 |

每种模式的输入口径、资格前提和排除范围见 [计算接口](references/calculator.md)。脚本输出保留输入、公式、政策编号及草稿状态。

## 安装与使用

### ClawHub

已安装并配置 ClawHub CLI 的环境中运行：

```bash
clawhub install china-tax-clerk --version 0.1.0
```

### Codex

将仓库克隆到本机技能目录；目标目录须不存在。如果已经安装，请先比较版本并保留本地修改。

```bash
git clone --branch v0.1.0 --depth 1 https://github.com/KAImomo99/china-tax-clerk.git ~/.codex/skills/china-tax-clerk
```

若设置了自定义 `CODEX_HOME`，使用对应的 `skills/china-tax-clerk` 目录。随后在支持 Agent Skills 的会话中调用：

> 使用 $china-tax-clerk 为我的中国大陆企业核对本期税费，先列出影响计算的缺失资料，再生成计税底稿和申报准备清单。

### 直接运行计算器

Python 3.10+，仅标准库，无需第三方包、API Key 或登录。以下命令在技能目录执行：

```bash
python3 scripts/calculate.py assets/examples.json
python3 scripts/calculate.py /path/to/input.json > /path/to/result.json
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

`assets/examples.json` 是 8 组人工构造的演示数据。实际输入文件、客户资料和输出底稿应保存在仓库之外。

计算脚本本身不联网、不上传资料、不连接税务局。政策查证由运行技能的 Agent 使用其已有搜索/浏览能力完成；本技能不内置搜索服务。正式办税需另行取得相应系统访问权限及用户授权。

## 验证情况与边界

发布前已运行 20 项 `unittest` 测试，覆盖门槛、税率分档、优惠资格、累计预缴、舍入及错误输入；累进税另用独立分段累加方法交叉检查。GitHub Actions 会在 Python 3.10 和 3.13 上运行同一测试集。

这些测试验证的是已实现算法和合成案例。尚未进行真实企业账套试点、税务局系统逐表对照或独立税务专业人员验收；不代表税务机关认可或实际申报成功。

本技能不提供企业登记接口、完整会计账簿系统、发票验真服务或自动报税 API。房地产、出口退税、跨境、非居民、差额征税等特殊业务不在内置计算范围。资料不明时不得以零代替；计税成功不等于政策适用、资料完整或申报完成。

## 文件索引

- [SKILL.md](SKILL.md)：技能入口和工作要求。
- [政策索引](references/policies.md)：官方来源、文号、有效期及规则快照。
- [办税流程](references/workflow.md)：建档、对账、复核、申报映射与归档。
- [工具调研](references/tools.md)：官方渠道和商业工具的适用范围及实测边界。
- [底稿模板](assets/workpaper-template.md)：计算依据、差异、待办与回执记录。
- [测试代码](scripts/test_calculate.py)：可重复执行的合成案例测试。

## 反馈与许可

反馈计算问题时，请提供脱敏或合成的输入、期望结果、实际结果及政策来源，勿提交客户发票、工资表、身份证、银行账户或登录凭据。

代码和原创文档采用 [MIT-0](LICENSE.md)，与 ClawHub 的技能许可要求一致，允许商业使用、修改和分发。外链政策及第三方产品资料归各自权利人所有，不随本仓库重新授权。
