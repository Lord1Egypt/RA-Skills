# 媒体池机制（Media Pool）

> 解决"通稿转载小站不被搜索引擎有效索引"的结构性漏稿问题（2026-08 一次实战 7 家漏检的根因）。转载追踪类任务必用。

## 机制

维护一个**按域名资产化的媒体清单**（YAML），对池内每个域名执行三路定向扫描，不依赖通用索引碰运气：

- **路线 A**：`gnews_query.py --site <domain> --query <关键词>`（快，但 GNews 不索引的站点无效）
- **路线 B**：curl/WebFetch 抓频道列表页或站内搜索页，grep 事件指纹词（标题短语+正文独特句）；只覆盖近 1-2 页，时效窗约 1 周
- **路线 C**：`baidu_search.py --query "<媒体名>+<主题>"`（gnews_not_indexed 站点强制必走；中转链接 `--resolve` 解析直链）

**扫描节奏**：发布日 T+1 首扫 → T+3 补扫（捕获延迟发布，实测 Techweb 延迟 3 天、中国日报网 T+3）→ T+7 增量复跑终扫。

## 池实例格式

池实例由各任务/项目自建维护（本 skill 不内置池，避免跨项目数据耦合）。示例实例：

- `<workspace>/config/syndication-pool.yaml`（v1.3，40+ 域名，含 GNews 可索引性实测标注）

模板结构：

```yaml
version: 1.x
updated: YYYY-MM-DD

tier1_syndication:      # 通稿分发池（按媒体类型分组）
  portal:               # 综合门户
    - { name: 媒体名, domain: example.com, note: "可选备注" }
  it_vertical: [...]    # IT 垂直
  tech_media: [...]     # 科技新媒体
  finance: [...]        # 财经
  official_self: [...]  # 官方自有渠道
tier2_mainstream: [...] # 主流观察池（深度稿潜在对象）
wechat_accounts: [...]  # 公众号分发渠道

gnews_indexed: [...]    # 实测 GNews site: 查询有效
gnews_not_indexed: [...]  # 实测未被收录，路线 B/C 必走

scan_rules:
  route_a: 'gnews_query.py --site {domain}'
  route_b: 'curl/WebFetch 抓 list_page + 指纹 grep'
  route_c: 'baidu_search.py --query "{媒体名}+{主题}"'
  hard_rule: "任何单一通道无结果 ≠ 未发布；三路全无才可写待核验"
  schedule: "T+1 / T+3 / T+7"
```

## 池的滚动扩充

每次 campaign 结束后回填：

1. PR 媒介回传的历史通稿分发清单（按域名沉淀，标注来源 campaign）
2. 新发现的收稿站-门户号分发链（如 IT时代网→网易号、科技快报网→搜狐号——改标题版经收稿站中转）
3. GNews 可索引性实测结果（indexed / not_indexed 分组）

## 与三要素验证的关系

媒体池只解决**发现**；池内发现的每个候选 URL 仍必须过 `fingerprint_check.py` 三要素验证才能入库。外部清单（PR 媒介回传）同样仅作待验证队列。
