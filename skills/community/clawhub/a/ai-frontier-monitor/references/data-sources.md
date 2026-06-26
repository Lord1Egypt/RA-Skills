# 数据源参考

## RSS 源（11 个）

| 源 | URL | 关键词过滤 |
|---|---|---|
| OpenAI Blog | https://openai.com/blog/rss.xml | enterprise, customer, agent |
| Microsoft AI | https://blogs.microsoft.com/ai/feed | enterprise, copilot, agent |
| AWS ML Blog | https://aws.amazon.com/blogs/machine-learning/feed/ | enterprise, customer, deployment |
| Techmeme | https://www.techmeme.com/feed.xml | — |
| Product Hunt | https://www.producthunt.com/feed | — |
| HN Show | https://hnrss.org/show | — |
| HN Ask | https://hnrss.org/ask | — |
| HN Frontpage | https://hnrss.org/frontpage | enterprise AI |
| HN Enterprise AI | https://hnrss.org/newest?q=enterprise+AI+agent | — |
| HN AI Production | https://hnrss.org/newest?q=AI+production+deployment | — |
| Dev.to AI | https://dev.to/feed/tag/aigents | — |

## 36氪热榜 API

- **URL**: `https://openclaw.36krcdn.com/media/hotlist/{YYYY-MM-DD}/24h_hot_list.json`
- **方式**: GET，无需认证
- **更新**: 每小时
- **字段**: rank(1-15), title, author, publishTime, content, url

## arXiv API

- **端点**: `https://export.arxiv.org/api/query?search_query=cat:{CATEGORY}&sortBy=submittedDate&sortOrder=descending&max_results={N}`
- **监控类别**: cs.AI, cs.LG, cs.CL
- **命名空间**: `atom:http://www.w3.org/2005/Atom`

## GitHub Trending

- **URL**: `https://github.com/trending?since=daily`
- **方式**: HTML 解析（按 `<article>` 分割）
- **AI 关键词**: ai, llm, gpt, agent, transformer, rag, mcp, claude, openai, pytorch
