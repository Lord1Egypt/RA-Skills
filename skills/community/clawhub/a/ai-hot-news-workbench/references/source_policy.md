# AI Hot News Source Policy

## Preferred Sources

Use these source classes in order:

1. Primary sources: company blogs, official release notes, research lab announcements, arXiv papers, regulator pages, court filings, standards bodies, GitHub release pages, Chinese regulator pages, Chinese company announcements, model cards, and open-source release pages.
2. Reputable reporting: The Verge, TechCrunch, Wired, Bloomberg, Reuters, Financial Times, The Information, MIT Technology Review, VentureBeat, Ars Technica.
3. China-region reporting and discovery: 36Kr, InfoQ 中文, 机器之心, 量子位, 雷峰网, 爱范儿, 钛媒体, 晚点 LatePost, 财新, 澎湃科技, cnBeta, 少数派, GitHub Trending China, ModelScope, Hugging Face Chinese model pages, official WeChat posts when available through web mirrors.
4. Discovery feeds: Hacker News, Product Hunt, GitHub Trending, Hugging Face papers/models, Papers with Code, Reddit AI communities, social posts from verified researchers or company leaders.

## Query Patterns

Use multiple queries to avoid source bias:

- "AI news today model release"
- "OpenAI Google Anthropic Meta AI release latest"
- "site:openai.com/blog OR site:anthropic.com/news OR site:deepmind.google news AI"
- "AI regulation copyright safety latest"
- "arXiv AI agent LLM multimodal robotics latest"
- "Hugging Face trending models today"
- "中国 AI 今日 大模型 发布"
- "人工智能 大模型 监管 备案 最新"
- "DeepSeek 通义千问 文心一言 腾讯混元 豆包 Kimi 最新"
- "site:36kr.com AI 大模型 OR site:infoq.cn 人工智能 OR site:leiphone.com AI"
- "ModelScope 魔搭 大模型 最新"

## Hotness Scoring

Use a 10-point score:

- 3 points for freshness in the last 24 hours.
- 2 points for strong source quality.
- 2 points for practical impact on builders, companies, or users.
- 1 point for novelty.
- 1 point for social or market attention.
- 1 point for follow-up value.

For China-region candidates, also consider:

- Whether the item affects Chinese developers, enterprises, consumers, or regulation.
- Whether it covers domestic foundation models, AI applications, chips, cloud infrastructure, robotics, autonomous driving, or government policy.
- Whether a Chinese-language report is confirmed by an official announcement or a second reputable source.
- Whether the story is actually about China. Chinese-language coverage of OpenAI, Anthropic, Google, Nvidia, or other foreign companies should remain in the global ranking unless it has concrete China-market, supply-chain, regulatory, or developer-ecosystem relevance.

Do not include weak rumors unless they are already shaping decisions. Mark rumors or single-source claims as "待确认".

## Deduplication

Group by the real-world event:

- Same model release covered by many outlets is one item.
- Product launch plus pricing details can be one item unless pricing is a separate major change.
- Research paper plus company blog about the same result is one item.
- Chinese and English reports about the same China-region event are one item; cite the primary Chinese source first when it adds local detail.

Use the strongest source link first and add secondary links only when they add facts.

## Workbench Delivery Standard

The final output should be readable in under three minutes. Use Chinese. Keep claims specific: name the organization, model/product/policy, date, and concrete change. Include a "中国区动态" section whenever credible China-region items exist. Avoid generic phrases like "AI continues to develop rapidly" unless tied to a fact.
