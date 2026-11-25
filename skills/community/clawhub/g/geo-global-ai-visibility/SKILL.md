---
name: geo-global-ai-visibility
version: 1.0.0
display_name: "GEO出海品牌AI曝光检测·ChatGPT｜MaxAEO"
display_name_en: "Global AI Visibility Check · ChatGPT & Perplexity"
description: "给做海外市场的品牌用：到 ChatGPT、Perplexity、Gemini、Google AI Overviews、Google AI Mode、Claude 等海外 AI 真实提问，查你的品牌有没有被推荐、排第几、和哪些竞品一起出现、引用了哪些网站，生成可转发的报告。当用户提到「出海」「海外 GEO」「ChatGPT 推荐」「ChatGPT 排名」「Perplexity」「Google AI Overview」「海外 AI 搜索优化」「独立站 AI 曝光」时使用。由 MaxAEO（maxaeo.cn）提供。"
description_zh: "给做海外市场的品牌用：到 ChatGPT、Perplexity、Gemini、Google AI Overviews、Google AI Mode、Claude 等海外 AI 真实提问，查你的品牌有没有被推荐、排第几、和哪些竞品一起出现、引用了哪些网站，生成可转发的报告。当用户提到「出海」「海外 GEO」「ChatGPT 推荐」「ChatGPT 排名」「Perplexity」「Google AI Overview」「海外 AI 搜索优化」「独立站 AI 曝光」时使用。由 MaxAEO（maxaeo.cn）提供。"
description_en: "For brands selling overseas: ask ChatGPT, Perplexity, Gemini, Google AI Overviews, Google AI Mode and Claude for real, and see whether they recommend your brand, where it ranks and which sites they cite. Provided by MaxAEO."
---
# 出海品牌AI曝光检测

给做海外市场的品牌用：到 ChatGPT、Perplexity、Gemini、Google AI Overviews、Google AI Mode、Claude、Copilot、Grok 真实提问，看海外用户问到你的品类时，AI 推荐了谁、有没有你、排第几、引用了哪些网站。

## 怎么做

1. **用目标市场的语言写问题**，默认英文，口语化、带约束，例如：
   - 品类推荐：「What's the best <category> for <audience/use case>?」
   - 替代：「Any good alternatives to <top competitor> for <use case>?」
   - 口碑：「Is <brand> legit? Any complaints?」
   品牌写海外用的名字，中英文名都写进别名，例如 `--brand "Anker|安克"`。
2. **运行**（默认 ChatGPT、Perplexity、Gemini、Google AI Overviews，每题约 12 点；Claude、Copilot 每次 5 点）：
   `python3 scripts/maxaeo.py ask --platforms chatgpt,perplexity,gemini,google-ai-overview --question "<question 1>" [--question "<question 2>"] --brand "<Brand|别名>"`
3. 按下面「通用规则」处理 Key、确认、取结果，然后生成报告。
4. **用中文给用户结论**：哪些 AI 推荐了他、排第几；没推荐他的推荐了谁；AI 最常引用哪些网站。海外 AI 常引用 Reddit、YouTube、G2 / Capterra 这类评测站、行业媒体和品牌官网，但以本次报告为准。
5. **建议**两三条，例如：在被引用的评测站上建好产品页并积累真实评价、官网补英文的对比页和 FAQ、在 Reddit 相关讨论里以品牌身份如实回答。不要建议刷评价或冒充用户发帖。

## 通用规则

脚本 `scripts/maxaeo.py` 只用 Python 标准库，直接运行。目标是让用户少来回：不要列几套方案让用户挑，不要讲环境变量、命令行、task_id 这类词。

**写问题**：完整的口语句子，不是关键词；保留「求推荐」「靠谱吗」的口气；带上人群、预算、地域等约束，更容易逼出具体品牌。品牌有别名（中英文名、产品名）时用 `|` 连起来，例如 `--brand "伴鱼|PalFish"`。

**先看计划**：不带 `--confirm` 运行只输出计划和点数，不提交。
- **没有 Key**：脚本会输出拿 Key 的四步。用一两句话转告打算问什么、哪几个平台、约多少点，再贴那四步。用户把 `gdev_` 开头的 Key 发过来后运行 `python3 scripts/maxaeo.py set-key <Key>`，保存成功就**直接按刚才说的计划加 `--confirm` 开始**（用户发 Key 就是同意了这次计划）。回复里不要重复完整 Key。
- **有 Key**：一句话问「问 X 个平台、Y 个问题，约 N 点，失败不扣，开始吗？」，同意后加 `--confirm`。所有提问一起提交，一般一两分钟出结果，最多等 5 分钟。没出结果的用脚本给的 `get` 命令取回，**不要重新提问**，那会重复扣点。

**出报告（不扣点）**：读脚本打印的回答，把出现的其他品牌名找出来（同一品牌的不同叫法用 `|` 连起来），运行脚本最后给出的 `report` 命令，加上 `--competitors "竞品A|别名,竞品B"`。它会算出每个品牌被推荐几次、平均排第几，汇总 AI 最常引用的网站，并生成一份 HTML 报告。把报告文件给用户，可以直接打开或转发。不要整段贴回答原文，报告里都有。

**说结论的分寸**：AI 每次回答会有出入。每个平台只问了一次时，说「这次推荐了 / 这次没推荐」，不要说成百分比的「提及率」；问题里本身带了品牌名的，只看口碑，不算排名。用户要稳定结论，建议同一组问题隔天再跑两次，三次都推荐才算「稳定提及」。

**点数**：标准档每次成功 Kimi 20 点，Claude、Copilot 5 点，其余平台 3 点，失败不扣。新账号首次使用送 100 点；不够可以在控制台在线充值（¥100 = 6,000 点起）。点数不够时脚本会提示，照实转告。

**相关技能**：想一次看豆包、DeepSeek、元宝、千问等多个平台，用「AI搜索品牌曝光检测」；看竞品份额用「AI搜索竞品对比」；看 AI 引用了哪些网站用「AI引用信源分析」；看口碑和负面用「AI口碑与负面检测」；做海外市场用「出海品牌AI曝光检测」。用户要在自己程序里接 MaxAEO 开放 API，看 https://maxaeo.cn/docs/developers/ 。
