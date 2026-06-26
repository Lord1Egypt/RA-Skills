# AdMapix — 广告与应用情报数据层 Skill

[English](README.md)

AdMapix 是覆盖 AdMapix 只读 API 的**数据层**。它把自然语言请求转成单次 API 调用，返回**原始结构化 JSON** —— 广告素材、应用/产品信息、排行榜、下载量/收入估算、投放分布、市场元数据。由你的 agent（Claude Code、Codex……）决定调用哪些端点、按需串联、自行分析。不做托管研究、不生成页面 —— 只给你可以自由组合的干净数据。

## 你能拉到什么

- **素材搜索** — 按关键词、广告主、应用、地区、媒体渠道、素材类型（图片/视频/试玩）、行业、日期范围搜索广告创意，可按最新、曝光最多、投放最久排序。每条记录包含素材资源、广告主/应用、首次/最近出现时间、曝光估算等。
- **应用/产品/公司** — 统一产品与公司搜索、完整应用详情、开发者详情、应用画像、相似应用、以及某个包使用的 SDK。
- **排行榜** — App Store / Google Play 榜单（免费/付费/畅销）及通用排行列表，按国家与分类。
- **下载量与收入** — 按时间、明细、国家的下载量与收入估算 *（第三方估算数据，非官方数字）*。
- **投放分布** — 应用在哪些国家、哪些媒体位、用什么素材类型投放。
- **市场** — 跨行业、广告主、渠道的市场级搜索与聚合。
- **元数据** — `filter-options` 返回全部筛选维度（国家、媒体渠道、广告类型、设备、行业 / `tradeLevel`、产品模型……），让 agent 发现有效代码、组装精确查询。

各端点参数与响应字段见 [`references/`](references)；自然语言 → 代码映射（素材类型、行业、国家分组、日期范围、排序、每页数量）见 [`references/param-mappings.md`](references/param-mappings.md)。

## 安装

```bash
npx clawhub install admapix
```

## 配置

1. 前往 [www.admapix.com](https://www.admapix.com) 注册并创建 API Key。
2. 选择一种方式配置：

OpenClaw / ClawHub：

```bash
openclaw config set skills.entries.admapix.apiKey "<你的-key>"
```

通用环境变量：

```bash
export ADMAPIX_API_KEY="<你的-key>"
```

把 key 放进宿主的密钥存储 —— 不要粘贴进聊天、日志或生成内容。

## 使用示例

向 agent 要数据，它会自己选端点并返回原始结果。

| 数据 | 示例指令 |
|------|----------|
| 素材搜索 | 「搜一下 puzzle game 的视频广告」「找东南亚投放的休闲游戏素材」「美国曝光最高的金融类素材」 |
| 应用/产品数据 | 「拉 Temu 的应用详情」「TikTok 的开发者是谁？」「这个 app 用了哪些 SDK？」「找和剪映相似的应用」 |
| 排行榜 | 「美国 App Store 免费榜 Top10」「日本畅销游戏榜」「Google Play 工具榜」 |
| 下载量与收入 | 「Temu 最近 30 天的下载量估算」「SHEIN 各国收入」*（估算）* |
| 投放分布 | 「Temu 主要在哪些国家投广告？」「这个游戏用了哪些广告渠道？」 |
| 市场 | 「东南亚游戏广告市场数据」「金融行业最大的广告主」 |
| 元数据 | 「列出可用的行业 / 国家 / 媒体渠道」（走 filter-options） |

支持**中文**与**英文**输入。

## 工作原理 —— 可组合的数据层

这个 skill 刻意做得很薄：

1. **一次请求一次调用。** 每个动作对应一个 AdMapix 只读端点，原样返回该端点的 JSON —— 不改写、不汇总、不排序。
2. **组合交给 agent。** 多步问题（「Temu 的下载量」「放置少女用了哪些 SDK」）由调用方 agent 解决：先查实体（如 `unified-product-search`），再取指标（如 `download-detail` / `sdk-detail`）。`SKILL.md` 的端点目录加 references 文档把这些链路写清楚了。
3. **元数据是一等公民。** `filter-options` 暴露全部筛选维度，agent 据此组装精确查询（正确的国家码、行业 ID、媒体渠道），而不是猜。
4. **分析留给你。** 对比、趋势、建议都由你的 agent 基于原始数据产出 —— skill 永远不跑托管「深度研究」、不生成 HTML / H5 页面。

这样结果可预测、可审计：你始终看得到底层数据，智能则在你掌控的 agent 里。

> ⚠️ 下载量和收入为第三方**估算**数据，非官方应用商店数字。

## 链接

- 官网：[www.admapix.com](https://www.admapix.com)
- API：[api.admapix.com](https://api.admapix.com)
- GitHub：[github.com/fly0pants/admapix](https://github.com/fly0pants/admapix)

---

由 [妙智盛](https://www.admapix.com) 提供技术支持
