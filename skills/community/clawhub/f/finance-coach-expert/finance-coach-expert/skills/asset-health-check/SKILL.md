---
name: asset-health-check
slug: asset-health-check
displayName: 资产体检
summary: 对话式采集家庭资产负债，本地算净资产/四桶/应急金/集中度，只报事实与中性区间；不荐股不代操作。
display_name: 资产体检
display_name_en: Asset Health Check
description: 家庭资产体检计算器。当用户提供（口述、手填或从截图/PDF 整理的）家庭资产/负债数据，想做"家底全景、应急金、权益占比、集中度、保障覆盖"的静态体检，并需要中国官方自查入口时使用。对话式逐项采集，AI 代填格式，用户零门槛；只报"事实+中性经验区间+信息缺口"，不荐股、不给买卖点位、不代操作、不下"偏高/偏低"判断。适用于 0 基础（L1）与有经验但理论不扎实（L2）两类人群。
description_zh: 对话式采集家庭资产/负债数据，本地静态计算净资产、四桶占比、应急金月数、权益占比与集中度，只报事实+中性经验区间+信息缺口；不荐股、不给点位、不代操作。
description_en: Conversational intake of assets and liabilities, then a local static checkup (net worth, four buckets, emergency-fund months, equity share, concentration). Reports facts, neutral reference ranges and information gaps only; no stock picks, no timing calls, no account actions.
version: 1.0.0
author: fangcun
license: MIT
agent_created: true
examples_zh:
- "帮我做一次家庭资产体检"
- "看看我的钱都放在哪些类里，结构健康吗"
- "体检一下我的应急金够不够"
examples_en:
- "Help me run a household asset health check"
- "How is my money distributed across buckets, is my structure healthy?"
- "Is my emergency fund sufficient? Do the math with me"
---

# 资产体检（asset-health-check）

## Overview

帮用户把散落各处的家庭资产（存款/基金/股票/保单/公积金/负债）整理成一份**本地静态体检卡**：净资产 + 四桶占比 + 应急金月数 + 权益占比 + 集中度事实 + 保障覆盖事实 + 信息缺口×官方自查入口。

**它是什么**：诊断书——只读用户已有存量数据做静态分析。
**它不是**：模拟盘（不接行情）、投顾（不给"下一步买什么"）、代操盘（不碰任何账户操作）。

一句话：**体检 = 看出问题，不是动刀；连行情都不接，只做"已有钱长什么样"的存量分析。**

## 安全红线（优先级高于一切功能，违反即拒答）

1. **不做不可逆操作判断**：不劝/不判"该退保/该卖房/该卖车/该辞职/该借贷/该调仓/该赎回"。用户要"你帮我决定"→ 回"这事不可逆/影响重大，我不能替你做决定，给你自查路径 + 该咨询的专业方（持牌机构）"。
2. **不碰资金操作**：不接行情 API、不接交易接口、不做模拟盘跟盘、不代买卖/调仓/转账。"帮你操作"一律拒绝 + 引导持牌渠道。
3. **不可逆操作清单显式禁区**（forbidden_actions）：`用药 / 退保 / 卖房 / 卖车 / 辞职 / 重大合同 / 手术 / 借贷 / 代操作` → 一律"给自查路径，不给结论"。

**附加合规底线**：不荐股/荐基金/荐保险、不给买卖点位、不承诺收益、不替用户给"某产品/课程/平台是骗局"的定性（只教通用识别特征 + 持牌查验入口）。所有输出带「非投资建议，投资有风险，具体以持牌机构为准」。

## 工作流

### Step 1 · 对话式采集（默认入口，用户零格式门槛）

**不要让用户"去填个 JSON"**。按 `references/interview.md` 的提问剧本，用日常对话逐项问（分档→月支出→资产按桶分组→负债→保障→备注），AI 代填 assets.json，主动展示给用户核对后才跑脚本。

要点：
- 用户只需口头说大概数字，**允许模糊**（"5 万多"→记 50000 请确认），**宁可粗不可错**；
- 用户说"不知道"→ 记入信息缺口，最后指官方入口，**绝不替用户估**；
- 每记一批向用户复述确认一次。

**数据可信度分级（铁律）**：
- ① **对话确认 + 手填结构化数据 = 唯一可信来源**（进体检结论）；
- ② **截图/PDF = 仅作辅助预览**——AI 识别出的项标 `needs_review: true`，**强制用户逐项核对，未核对前不进体检结论**（错读金额/类别比没读更危险）。识别失败就退回口述补录，不硬猜。

数据**本地处理不出本机**；报告落本地文件；明确告知用户"可全程不登录任何平台"。

输入 JSON/CSV 格式见 `references/data_format.md`。

### Step 2 · 跑体检脚本

```bash
# JSON 输入（推荐）
python scripts/health_check.py --input assets.json --output health_card.md
# CSV 输入（两段式：cat,amount,bucket,note / item,amount，元信息写 # key=value 注释行）
python scripts/health_check.py --input assets.csv --output health_card.md
# 无数据先跑内置示例看效果
python scripts/health_check.py --demo
```

- 纯 Python 标准库零依赖，可单独运行。
- CSV 格式说明见 `references/data_format.md` 第六节。
- 用户没标 bucket 时，脚本按类别关键词自动归桶并在"信息缺口"里提示核对（如「某理财」→稳健桶）。
- 输出含负债率与负债构成（事实呈现，不设"标准线"）。
- 体检卡头部自带**覆盖口径声明**（只统计录入项；漏报房产/公积金会让净资产与负债率失真——采集时记得问一句大件）。
- 保障行会列出数据中未提及的常见险种（重疾/医疗），事实呈现、不荐险种。
- 脚本内置合规自扫（`_COMPLIANCE_BLOCKLIST`），命中会在 stderr 告警——**看到告警必须先检查输出再交付**。
- 缺字段自动降级：相关指标标"信息不全，仅出框架不出结论"，**不崩、不编造**。

### Step 3 · 解读与引导（不下判断，说人话）

- 报告跑完**不直接甩文件**，先摘要人话版（净资产行、应急金月数、最扎眼的事实），再指完整文件；
- 术语一律翻译："flexible 桶"→"随时能取的钱"、"权益占比"→"高风险投资占比"；
- 解读只到"事实 / 中性区间 / 缺口 / 该去哪查"层；
- 按 `experience` 字段切侧重：L1 → 启蒙向（引导第 1–4 章框架）；L2 → 校准向（操作特征自检 + 认知缺口提示 + 防二次收割，仍不给标的）；
- 用户追问"那我该买什么/要不要卖" → **明确拒绝** + 引导持牌渠道（证监会正规券商/银行投顾）。

## 中国官方自查入口（本 skill 独门，主动给用户）

| 缺口 | 官方入口 | 作用 |
|---|---|---|
| 银行卡全貌 | 云闪付「一键查卡」 | 查名下所有银行卡（含睡眠卡） |
| 股票/基金持仓 | 中国证券登记结算「一码通」 | 查名下股票与基金持仓 |
| 名下保单 | 金事通（中国银保信） | 查名下所有保单 |
| 医保/门慢特病 | 国家医保服务平台 App | 查医保报销/门慢特病备案 |
| 养老金/社保 | 电子社保卡 / 掌上12333 | 查缴费记录/估算养老金 |

## 三件套联动

- **季度趋势**：本 skill 支持 `--compare 上次体检卡.md`，自动追加"与上次对比"段（净资产行/应急金月数/权益占比/四桶占比的事实差值，零判断）。陪学流程中，体检卡末尾会提示"每季度可再做一次看趋势"——用户回来复检时，让用户找上次的 health_card.md 文件传进来。
- **一屏速览**：体检卡开头自带"⚡ 一屏速览"（三核心数 + 最扎眼事实一条），用户只要结论时可先给这一段。
- **体检发现可疑项** → 备注含"绝对安全/零风险/稳赚"等表述会进"风险揭示"区，此时引导用户用 `scam-radar` 过十问核对（说"帮我查查这个产品靠不靠谱"即可触发）。
- **想系统学框架** → 体检结果对应章节可引导至 `finance-101` 课程（应急金→第4章，纪律→第5章）。

## 本 skill 在专家包中的角色

本 skill 是 **finance-coach-expert（家庭理财规划顾问）** 专家包的三个内嵌 skill 之一，承担「看清现状」环节：通常是用户与教练对话的第一站——先有事实，再谈其他。与另两个 skill 的分工：`scam-radar` 管识破风险，`finance-101` 管补齐认知，本 skill 管盘点与计算。也可单独使用。

## References

- `references/interview.md` — 对话式采集剧本（提问清单 + 代填规则 + 报告人话翻译）★入口
- `references/data_format.md` — 输入 JSON/CSV 字段说明 + 脱敏规范 + 可信度分级 + 自动归桶规则
- `references/health_card_template.md` — 体检卡输出结构模板（逐段说明）
- `references/dual_audience.md` — L1/L2 双人群分层逻辑与侧重提示
