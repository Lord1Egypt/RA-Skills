---
name: geo-brand-monitoring
version: 1.1.0
display_name: "GEO品牌监测 · AI搜索品牌曝光检测｜MaxAEO"
display_name_en: "AI Search Brand Visibility & GEO Rank Check"
description: "到豆包、DeepSeek、腾讯元宝、千问、Kimi、文心一言、ChatGPT 等 18 个 AI 平台真实提问，查你的品牌有没有被 AI 推荐、排第几、和哪些竞品一起出现、AI 引用了哪些网页，生成一份可直接转发的 AI 搜索曝光报告。当用户提到「GEO」「生成式引擎优化」「AI搜索优化」「AI 可见度」「让 AI 推荐我的品牌」「品牌在豆包/DeepSeek 里搜不到」「AI 搜索排名」「竞品在 AI 里的曝光」「AI 引用了哪些网站」「AI 怎么评价我的品牌」时使用；也用于编写调用 MaxAEO 开放 API 的代码。由 MaxAEO（maxaeo.cn）提供。"
description_zh: "到豆包、DeepSeek、腾讯元宝、千问、Kimi、文心一言、ChatGPT 等 18 个 AI 平台真实提问，查你的品牌有没有被 AI 推荐、排第几、和哪些竞品一起出现、AI 引用了哪些网页，生成一份可直接转发的 AI 搜索曝光报告。当用户提到「GEO」「生成式引擎优化」「AI搜索优化」「AI 可见度」「让 AI 推荐我的品牌」「品牌在豆包/DeepSeek 里搜不到」「AI 搜索排名」「竞品在 AI 里的曝光」「AI 引用了哪些网站」「AI 怎么评价我的品牌」时使用；也用于编写调用 MaxAEO 开放 API 的代码。由 MaxAEO（maxaeo.cn）提供。"
description_en: "Ask 18 real AI platforms (Doubao, DeepSeek, Yuanbao, Qwen, Kimi, ChatGPT, Perplexity, Gemini and more) and see whether they recommend your brand, where it ranks, which competitors appear alongside it and which web pages they cite, then get a shareable AI search visibility report. Use for GEO (generative engine optimization), AI search optimization, AI visibility, AI rank tracking, competitor share of voice in AI answers, or writing code against the MaxAEO Open API. Provided by MaxAEO."
---
# AI 搜索品牌曝光检测

替用户到真实的 AI 平台提问（国内：豆包、DeepSeek、Kimi、腾讯元宝、千问、文心一言、智谱清言、讯飞星火、秘塔 AI 搜索、小红书点点；海外：ChatGPT、Gemini、Claude、Perplexity、Copilot、Grok、Google AI Mode、Google AI Overviews），告诉用户：AI 有没有推荐他的品牌、排第几、竞品是谁、AI 引用了哪些网站、下一步该去哪补内容。

脚本 `scripts/maxaeo.py` 只用 Python 标准库，直接运行。

## 怎么做

让用户少来回：不要列几套方案让用户挑，不要讲环境变量、命令行、task_id 这类词。

1. **直接定好问题和平台**
   - 问题：用户给了就用原话。只给了品牌，就替他写 1 个真实用户会问的品类问题，不要写成「伴鱼怎么样」。写法：完整口语句子，不是关键词；保留「求推荐」「靠谱吗」的口气；带上人群、预算、地域等约束，更容易逼出具体品牌。例：品牌是伴鱼 →「孩子 6 岁零基础，想找个英语启蒙 APP，有哪些靠谱的推荐？」
   - 用户要看「整体情况」「提及率」时，写 3 个不同角度的问题：品类推荐（有哪些推荐）、对比替代（XX 和 YY 哪个好 / 有没有类似 XX 的）、口碑验证（XX 靠谱吗 / 有什么坑）。
   - 平台：用户点名的照用；没点名用默认的豆包、DeepSeek、腾讯元宝、千问。Kimi 单次 20 点，用户没点名不加。做海外市场的品牌用 `chatgpt,perplexity,gemini,google-ai-overview`。
   - 品牌有别名（中英文名、产品名）时用 `|` 连起来，例如 `--brand "伴鱼|PalFish|伴鱼绘本"`。
2. **运行**（不带 `--confirm` 只输出计划和点数，不提交）：
   `python3 scripts/maxaeo.py ask --question "<问题1>" [--question "<问题2>"] --brand "<品牌|别名>" [--platforms doubao,deepseek]`
3. **没有 Key 时**：脚本会输出计划和拿 Key 的四步。用一两句话转告：打算问什么、哪几个平台、约多少点，再贴那四步。
   用户把 `gdev_` 开头的 Key 发过来后，运行 `python3 scripts/maxaeo.py set-key <Key>`；保存成功就**直接按刚才说的计划加 `--confirm` 开始**（用户发 Key 就是同意了这次计划），不用再问。回复里不要重复完整 Key。
4. **有 Key 时**：一句话问「问 X 个平台、Y 个问题，约 N 点，失败不扣，开始吗？」，同意后加 `--confirm` 运行。所有提问一起提交，一般一两分钟出结果，最多等 5 分钟。
   没出结果的，脚本会给 `get` 命令，之后用它取回；**不要重新提问**，那会重复扣点。
5. **找竞品，生成报告（不扣点）**：读脚本打印的回答，把里面出现的其他品牌名找出来（包括用户提到的竞品；同一品牌的不同叫法用 `|` 连起来），运行脚本最后给出的那条 `report` 命令：
   `python3 scripts/maxaeo.py report --file maxaeo_results/<文件>.json --competitors "斑马|斑马AI课,叽里呱啦,VIPKID"`
   它会算出每个品牌被提到几次、平均排第几，汇总 AI 最常引用的网站，并生成一份 HTML 报告。把报告文件给用户，告诉他可以直接打开或转发。
6. **给用户结论**，几句话就够：
   - 哪些平台推荐了他、排第几；没推荐他的平台推荐了谁；
   - 谁被推荐得最多（和他比差在哪）；
   - AI 最常引用哪些网站，他的官网或相关内容有没有在里面；
   - 一两条具体能做的事，例如「DeepSeek 引用的 3 条都来自知乎，可以在知乎相关问题下补一篇有数据的回答」。
   不要整段贴回答原文，报告里都有。

## 说结论的分寸

AI 每次回答会有出入。每个平台只问了一次时，说「这次提到了 / 这次没提到」，不要说成百分比的「提及率」。用户要稳定结论，建议同一组问题隔天再跑两次，三次都提到才算「稳定提及」。完整的出题配比和评估口径，可以用 MaxAEO 在技能市场上的「AI 搜索引用基线实测 SOP」技能。

## 相关技能

只看某一个平台，用「豆包品牌推荐查询」「DeepSeek品牌推荐查询」等单平台技能；看竞品份额用「AI搜索竞品对比」；看 AI 引用了哪些网站用「AI引用信源分析」；看口碑和负面用「AI口碑与负面检测」；做海外市场用「出海品牌AI曝光检测」。

## 点数

- 标准档每次成功：Kimi 20 点，Claude、Copilot 5 点，其余平台 3 点。失败不扣点。
- 新账号首次使用送 100 点；不够可以在控制台在线充值（¥100 = 6,000 点起）。点数不够时脚本会提示，照实转告。

## 写代码接入时

用户要在自己的程序里接 MaxAEO 开放 API 或 MCP 时，先读 `references/api.md`：鉴权、异步提交与轮询、防止重复扣费的规则、错误码和参考实现都在里面。最新版以 https://maxaeo.cn/docs/developers/ 为准。
