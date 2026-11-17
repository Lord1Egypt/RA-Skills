# 网站模式（source.type = site）

把**在线文档站**做成学习卡片的一套流程。与「书籍模式」共用后半段（items → 翻译 → 渲染 → 推送），
只有「拆解」这一步不同。

## 一、抓取（两条通道互相印证）

```bash
python fetch_site.py --base-url https://docs.example.com --slug mydocs \
    --include /start /concepts \
    --exclude / /start/hubs /start/docs-directory \
    --limit 300
```

| 通道 | 作用 |
|---|---|
| A：`sitemap.xml` | 全量、权威。自动找 `/sitemap.xml`，也支持 `sitemapindex` 嵌套 |
| B：首页导航链接 | 补 sitemap 漏掉的新页面 |

要点：
- **正文优先抓 `<url>.md`**（很多文档站提供 Markdown 源），比抓 HTML 干净得多；抓不到再退化为 HTML。
- **必须剔除导航页/索引页**（`/`、`/hubs`、`/docs-directory` 这类），否则会混进一堆无内容的卡片。
- 配图落盘为**扁平化命名**：`/assets/a/b.png` → `_assets_a_b.png`，与渲染层的图片映射约定一致。
- 输出 `books/<slug>/raw/pages/*.md`、`raw/imgs/*`、`catalog.json`。

抓完先看 `sections` 统计，**与用户确认「章节范围 + 卡片总数」**后再往下走。

## 二、生成内容源（items）

`catalog.json` 是清单（idx / section / title / url），`items` 是**内容源**（唯一事实源）。
每页生成一个 item：

```json
{
  "id": "oc-009", "idx": 9, "chapter": "开始 · Overview",
  "topic": "Features",
  "coreIdea": "一段话核心观点（原文语言）",
  "explanation": "正文（原文语言，按空行分段）",
  "quote": "金句（可选）",
  "points": ["要点1", "要点2"],
  "terminology": ["Gateway", "Control UI"],
  "relatedLinks": [{"text": "Getting started", "href": "https://…"}],
  "link": "https://docs.example.com/concepts/features"
}
```

- `idx` = **清单绝对序号**（跳过也占号），用于卡片标记与笔记录入。
- 内容多时改用**分章节布局**：`items/index.json` + `items/ch01.json`…（`items_io.py` 统一读，
  上层无感知）。生成完写一次 `items/index.json` 即可。
- 正文里保留 MDX 标签没关系——渲染层的 `clean_mdx()` 会处理；但**不要手工删掉带 `title` 的标签**，
  那会丢掉引子文字。

## 三、索引与推送

```bash
python book_setup.py gen-index mydocs     # 生成卡片顺序 index.json（同时初始化 progress.json）
python push_card.py list-next --book mydocs --n 10
python push_card.py next --book mydocs --n 5     # 批量取 5 张
python render.py --type long-study --payload p.json --zh z.json --out card.png
python render.py --type pdf-bilingual --payload p.json --out card.pdf --assets books/mydocs/raw/imgs
python push_card.py mark --book mydocs --ids oc-009,oc-010,oc-011,oc-012,oc-013 success
```

> `index.json`（卡片顺序）与 `items/index.json`（内容源章节索引）**是两个不同的文件**，别混。

## 四、增量更新

站点加页时：
1. 重跑 `fetch_site.py`（`--urls-file` 可只喂新增 URL，更快）；
2. 把新页面追加到 `catalog.json` / 内容源（**保持 idx 连续、已有编号不变**）；
3. 重跑 `gen-index`；进度靠 `progress.json` 的 `lastPushedId` 继续，不会重推。
