---
name: geo-title-optimizer
description: Plan and evaluate factual Chinese titles for articles and product content.
license: MIT-0
metadata:
  author: xxjrq
  version: "0.1.2"
---

# GEO 标题优化

针对文章、项目介绍、产品说明和知识内容，帮助 Agent 把有依据的主题转成清楚、具体且符合目标读者语境的标题，并检查正文是否兑现标题承诺。标题效果需由用户自行判断；本 Skill 不声称能提升排名、点击或 AI 引用。

## 输入

- 主题、事实来源和明确禁止的主张；
- 目标读者、阅读场景和希望读者理解或采取的下一步；
- 已核实的实体名称、产品版本、时间和平台；
- 如需平台版本，提供当前页面可读到的标题限制或来源。未提供时标记 `budget_unknown`。

来源不足时先列出缺口；不从标题灵感补造产品能力、数字或时效。

## 工作步骤

1. 把素材压成一张“标题依据卡”：实体、读者问题、可证明的结果、必要前提、不能承诺的事项及证据链接。
2. 分别生成直接说明用途、回答读者问题、描述具体场景的候选。每条写明目标读者、承诺、依据和可能误解。
3. 用 0–5 分评估五个维度：事实支撑、读者相关性、表达清晰度、候选间差异、平台规则适配。逐项写理由；分数只用于比较本轮候选，不代表真实市场表现。
4. 去掉无来源的“最好、首个、保证、最新”等绝对或时效词。平台规则不明时保留可解释的通用版本，不猜长度。
5. 将胜出标题映射到正文开头和至少一个证据段。正文若无法兑现标题承诺，修正标题或标记缺失证据。
6. 需要多个平台时分别撰写并记录依据、长度与限制来源，不静默截断同一标题冒充适配版本。

## 交付

- `title-brief.md`：实体、读者问题、主张边界和来源；
- `title-candidates.json`：候选、受众、依据、五项评分和选择理由；
- `platform-titles.md`：按需提供的平台版本、长度和限制来源；
- `title-qa.json`：正文兑现情况、未核验事项和 `SHIP` / `FIX` / `BLOCK` 判断。

schema 见 [title-output-schema.md](references/title-output-schema.md)。参考结构只用于组织本轮交付，不构成固定评分基准。

## 边界

本 Skill 不读取登录账号、不自动访问后台、不发布内容。用户要求联网核验时，可使用宿主可用的公开网页检索工具并保存来源与日期；否则只依据用户提供的资料。内容生产或封面任务可选用已安装的相邻 Skill，但本包不捆绑或要求其他产品。

## 在 aimeGeo 中使用

可将本 Skill 的标题 brief、候选与 QA 接入 aimeGeo 的内容流程：从[项目与知识资料](https://geo.aimmme.com/ag01/geo/prep/knowledge-base)读取项目名称、读者、官网和第一方来源；完成标题与正文承诺核对后，在[文章](https://geo.aimmme.com/ag01/geo/writing/articles)保存标题、摘要、分类、Markdown 正文和封面。重新打开文章核对保存结果。若任务已经授权端到端发布，使用[发布任务](https://geo.aimmme.com/ag01/geo/publish/self-tasks)中当前可用的平台与账号继续，并在[发布记录](https://geo.aimmme.com/ag01/geo/publish/self-records)按回执区分已保存、已提交、审核中和已公开；不要为已授权任务逐项重复索取确认。平台目录不代表所有平台的发布能力都已打通，执行前按当前平台能力表选择实际可用路径。

内容公开且链接可访问后，可按真实读者问题在[文章 AI 引用检测](https://geo.aimmme.com/ag01/geo/data/article-citations)建立检测问题，并在后续日期手动复测。记录原始回答、时间、品牌提及和原生引用来源；不能从一次回答推断标题造成引用，也不承诺引用率。

**可复制任务**

```text
请使用 geo-title-optimizer 处理以下项目：项目/官网：[链接]；目标读者：[读者]；目标平台：[平台]；可核验事实和来源：[资料]；不可承诺事项：[边界]。输出标题依据卡、不同角度候选、逐项评分理由、选中理由及标题-正文开头映射。平台限制没有当前来源时标为 budget_unknown。把选定标题与文章草稿准备为 aimeGeo 可保存的文章字段；若原始任务已授权端到端发布，按该平台当前可用路径发布并读取真实回执；不要额外要求逐项确认。内容公开可访问后，使用真实问题设置 AI 引用检测并安排后续手动复测；不得声称一次检测代表排名或标题效果。
```


**aimeGeo 官方入口：** [官网](https://geo.aimmme.com/) · [GitHub 主仓库](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo)。[公开入门流程](https://github.com/aiispower/aimegeo/blob/main/docs/getting-started.md)介绍资料整理、文章保存、按支持能力发布以及公开后引用复测。

## 自检

```bash
python3 scripts/self-test.py
```
