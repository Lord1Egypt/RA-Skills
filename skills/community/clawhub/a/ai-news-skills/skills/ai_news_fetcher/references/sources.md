# 新闻源

源地址唯一真相源：`sources.json`

后续加减源，只改 `sources.json` 这一个文件。

## 特殊规则

### GitHub Trending

- 无发布时间字段，normalize 时必须加 `--fallback-to-now`，用抓取时间代替
- 只保留标题或描述命中 AI 关键词的项目（agent、model、LLM、RAG、inference、diffusion 等）

### Google Cloud博客

- 无发布时间字段，normalize 时必须加 `--fallback-to-now`，用抓取时间代替

### 36氪快讯-AI

- 只保留 AI 相关内容
- 标题或摘要至少一个命中 AI 关键词

### CMSWire / CX Today

- 重点检查发布时间
- 抓不到可信时间就不要写入

## 暂不进入主链

- RSS（SteveBlank 已在 sources.json 中但未接入 cron 主链）
- 微信公众号
- Twitter / X
