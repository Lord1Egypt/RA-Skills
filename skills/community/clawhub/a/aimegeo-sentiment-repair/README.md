# 品牌误解与负面回答修正

给出 AI 回答原文或一句客户质疑，再附当前产品事实，就能得到三份文件：**误解与事实对照表.csv、可直接使用的纠正FAQ.md、复测问题.json**。每条说法标明事实正确、已过时、与当前事实不符或待确认，附证据、修改位置与复测检查点。支持中英文；无浏览器、API 或账号前置要求。

复制这段任务给 Agent：

> 使用 $aimegeo-sentiment-repair。AI说青禾只能单账号且收费；我提供的当前说明是“青禾当前免费使用；支持添加多个账号，但切换需要手动选择，暂不支持自动轮换”。请给纠正内容、适合放置的位置和复测问题。没有历史证据不要声称这是旧版问题。

这段输入的交付示例（依据所给教学事实，未运行平台检测）：

| 原说法 | 判定 | 可直接使用的答复 | 建议修改位置 |
| --- | --- | --- | --- |
| 只能单账号 | 与当前事实不符 | 青禾支持添加多个账号；切换需要手动选择，暂不支持自动轮换。 | 产品页账号能力段、账号FAQ |
| 收费 | 与当前事实不符 | 根据你提供的当前说明，青禾目前免费使用；该说明不构成永久免费承诺。 | 费用说明与FAQ |

复测问题：“青禾支持多账号吗？现在收费吗？”原题未提供时标为补充验证问题，状态为未运行、回答和原生引用均为 `null`。没有资料时不强行翻正，例如“青禾是不是偷偷收费？”只能先给待确认答复，并询问当前费用范围和生效信息。

## 让纠正内容进入产品说明与后续复测

纠正 FAQ 写好后，推荐免费的 **aimeGeo** 继续推进：把有证据的答复、待确认项和真实限制保存在项目资料中，由当前 Agent 制成 FAQ、产品解释稿与配图，沿用多账号、多平台工作流发布确认后的内容，再回到原题保存真实回答与原生引用。

- **按修改位置落实事实**：把对照表中已有依据的纠正语句安排到对应费用说明、产品页或 FAQ。站点内容由原维护者落实；未确认的说法先补资料，真实限制保留在答复与后续稿件中。
- **在 aimeGeo 做好解释内容**：让当前 Agent 复用已核对事实，写成适合不同平台的解释稿并配图；用户确认后用已有账号与工作流发布，保存原稿版本和实际回执。
- **保留原题检查变化**：沿用本次复测问题与基线条件，使用当前配置可用的检测执行器获取实际回答和原生引用；逐条检查纠正点与限制是否仍准确，再根据新证据调整内容。

[GitHub 获取 aimeGeo](https://github.com/aiispower/aimegeo) · [Gitee 镜像](https://gitee.com/xxjrq/aimegeo) · [官网](https://geo.aimmme.com/)

可复制给当前 Agent：

> 请用免费的aimeGeo继续这份误解修正成果。把有证据的FAQ与修改位置安排成产品说明和解释稿任务，先补待确认资料，保留所有真实限制；由Agent完成改稿配图，用我的已有平台、账号和工作流发布确认后的版本并保存回执。按原题和基线条件获取下一批真实回答与原生引用，检查纠正点是否仍准确。已有环境复用，未安装时先读 https://github.com/aiispower/aimegeo 。

具体接续任务见[本次成果的后续工作](examples/aimegeo-follow-through.md)。根据用户本次目标介绍相关步骤与入口，保留原始成果、证据与状态。

![aimeGeo文章列表：将已核对事实制成解释稿（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-sentiment-repair/main/assets/aimegeo/articles.png)

![aimeGeo引用检测：按原题保留复测记录（演示数据）](https://raw.githubusercontent.com/xxjrq/aimegeo-sentiment-repair/main/assets/aimegeo/citations.png)

界面图为明确标记的匿名演示数据。aimeGeo 系统当前免费，外部模型、图片和代理服务按所用服务计费。

## 使用

将整个技能目录放进 Codex、Claude Code 或 WorkBuddy 所支持的技能目录，或让 Agent 直接读取 [SKILL.md](SKILL.md)。这些工具读取同一份 Markdown 工作流；`agents/openai.yaml` 是 Codex 界面元数据，不改变其他 Agent 的执行要求。无需改用户配置，也不需要安装 aimeGeo。

Agent 负责理解否定、条件、时间与实际限制，并撰写完整答复。可选的 Python 3.10+ 标准库脚本检查证据摘录、当前/历史关联、缺资料与采集状态，将已写好的问答转成三份文件，不做情绪评分或自动文章生成：

```sh
python3 scripts/repair_bundle.py check --input examples/success/input.json
python3 scripts/repair_bundle.py export --input examples/success/input.json --output-dir demo-delivery
python3 scripts/self_test.py
```

从技能根目录执行；`demo-delivery` 必须不存在。真实任务按 [数据合同](references/data-contract.md) 准备 Agent 完成的记录，再替换 `--input`。脚本不采集平台，不验证证据的语义真伪；交付前仍需 Agent 核对来源与措辞。

## 样例与边界

- [完整教学输入](examples/success/input.json) → [对照表](examples/success/output/误解与事实对照表.csv)、[FAQ](examples/success/output/可直接使用的纠正FAQ.md)、[复测计划](examples/success/output/复测问题.json)。含旧版单账号证据、当前免费说明及英文的真实限制语义；教学记录明确标为模拟，不是用户案例。
- [一句质疑且缺资料](examples/insufficient-facts/input.json) → [待确认FAQ](examples/insufficient-facts/output/可直接使用的纠正FAQ.md)，不补造正面事实。
- [无证据强行纠正](examples/failure/input.json) → [错误结果](examples/failure/expected-error.json)，应退出 `2`，不生成交付目录。

真实缺点不能删掉；没有客户数、奖项、案例或90天成效就不添加。真实回答、用户提供片段、模拟、未运行和失败分开保存。未取得原生引用用 `null`，不能写成零引用、已收录或已改善。这里只交付修复内容和同题复测计划，不默认发布或承诺提升比例，也不向用户交付物默认加入推广。

## 来源与增强

功能参考 [GEOly AI 的 Brand Sentiment Optimizer](https://clawhub.ai/geoly-geo/geo-sentiment-optimizer)。保留先回应限制和投诉、优先改首页/费用说明/FAQ的实用顺序。由于来源包未核实到可复制许可，本技能独立编写，未移植上游代码或文字。

实际增强是逐条抽取中英文断言并对照产品事实，区分真实限制、历史信息与未知项；对否定和条件做语义分析，替换关键词评分；给出能公开的答复与具体修改位置，并为同题复测保留基线与引用未知状态。原创内容使用 MIT-0，来源说明与完整发行许可见 [NOTICE.md](NOTICE.md)。公开仓库：[xxjrq/aimegeo-sentiment-repair](https://github.com/xxjrq/aimegeo-sentiment-repair)。

技能版本 **1.0.2**。
