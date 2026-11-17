# StyleSpec 字段定义

`stylespec.json` 是 +learn 的产出、+draft 的输入。脚本产出的只是**草稿**，你需要把它规范化成下面这套字段。凡是 `*_guess` 结尾的字段都是机器的猜测，定稿时要么确认、要么改掉。

## 顶层结构

```jsonc
{
 "meta":    { /* 期刊身份 */ },
 "canvas":   { /* 开本与出血 */ },
 "palette":  { /* 色板 */ },
 "typography": { /* 字体与字号 */ },
 "chrome":   { /* 每页固定件 */ },
 "grids":   { /* 版心网格 */ },
 "page_templates": [ /* 页面模板 —— 几何层 */ ],
 "fixed_pieces": [ /* 固定文案件 */ ],
 "semantic":  { /* 语义层，enrich_from_omni.py 追加；可缺省 */ },
 "scale_baseline": { /* 篇幅基线，量级门禁的分母 */ }
}
```

> `semantic` 段是 Omni 富文本通道的产物，`build_draft.py` 读取时忽略它，只服务于 `+plan`/`+draft` 的写稿环节。
> 几何层的 `page_templates` / `grids` / `chrome` 不会被它覆写。

## semantic — 语义层（Omni 富文本）

由 `scripts/enrich_from_omni.py` 生成，字段定义：

```jsonc
{
 "source":            { "md": "result_xxx.md", "characters_raw": 163167 },
 "headings":          55,
 "contents":          { "parts": [{"id":"01","name":"法规动态"}],
                        "entries": [{"title":"解码机遇：…","page":19,"part_id":"02"}] },
 "section_tree":      { "front_matter": [...], "back_matter": [...],
                        "parts": {"01": {"units":[
                          {"title":"…","role":"article|entry","chars_own":25,"chars_total":2854,
                           "toc_page":19,"matched_by":"contents|dateline|heuristic",
                           "meta":{"date_iso":"2026-04-30","authors_candidates":["韦思远"],
                                   "dateline_template":"<DATE> 韦思远 黄启明"},
                           "subheads":[{"title":"前言：…","chars":352}]}]}},
                        "tree_confidence": "high|media|low" },
 "unit_metrics":      { "all_units": {"n":12,"min":1365,"median":5107,"max":6848},
                        "per_part": {"深度观察": {…}} },
 "fixed_pieces":      { "running_head_candidates":[{"text":"区域观察","count":82}],
                        "cta_candidates":[{"text":"阅读原文","count":34}],
                        "disclaimer_candidates":[], "contact_list":["北京总部","上海分所"] },
 "paragraph_units":   [ {"kind":"lead_date_entry","count":34,"split_regex":"^20\\d{2}年\\d{1,2}月\\d{1,2}日[,，]",
                         "chars":{"n":34,"median":268,"min":81,"max":392},"samples":[...]} ],
 "terms":             { "statutes_top":[{"name":"稳定币条例","n":3}], "terms_top":[...] },
 "capability_notes":  { "has_images_in_text": false, "has_html_table": true, "has_gfm_table": false },
 "outline_nodes":     [ /* read_outline 原始节点，可选 */ ]
}
```

字段使用要点：

- `tree_confidence` = `low` 时禁止据此写稿，必须人工划定单元边界。
- `chars_total` 是「单元自身 + 全部分节」的字数，用它做 UnitPattern 的篇幅约束；`chars_own` 只是标题区。
- `role`：`article`（有分节、篇幅大）/ `entry`（无分节、导语式短条），两者写 UnitPattern 的方式完全不同。
- `matched_by` = `heuristic` 说明没命中目录也没命中日期题头，属兜底猜测，要复核。
- `authors_candidates` 由连写汉字串按 2/3 字切分得到，**永远是候选**，写稿前必须跟用户核对人名。
- `paragraph_units[].split_regex` 可直接用来切分正文、逐条套 UnitPattern 生成。
- `capability_notes.has_images_in_text` 恒为 `false` 时可确信：配图信息只能来自几何层 `image_slots`。

## meta — 期刊身份

| 字段 | 类型 | 说明 |
|---|---|---|
| `name` | str | 刊名全称 |
| `short_name` | str | 页眉用的短名（往往比刊名短） |
| `publisher` | str | 出版主体 |
| `frequency` | enum | `monthly` / `bimonthly` / `quarterly` / `irregular` |
| `issue_rule` | str | 期号规则，如「总第 N 期；每年 6 期」 |
| `date_rule` | str | 封面日期写法，如「2026 / 04」 |
| `page_offset` | int | **物理页 − 印刷页**。目录页码全靠它 |
| `audience` | enum | `clients` / `internal` / `industry` / `mixed` |

## canvas — 开本与出血

| 字段 | 示例 | 说明 |
|---|---|---|
| `size_mm` | `[210, 297]` | 成品尺寸 |
| `bleed_mm` | `3` | 出血；封面常被另一版心沿用，需另行确认 |
| `binding` | `saddle` / `perfect` | 骑马钉 / 胶装 |
| `safe_mm` | `10` | 订口安全边 |

## palette — 色板

```jsonc
"palette": {
 "roles": { "primary": "#A10F34", "text": "#000000",
       "text-secondary": "#3E3E3E", "meta": "#7F7F7F" },
 "print": { "primary": { "cmyk": [0, 91, 79, 37], "pantone": "..." } },
 "notes": "底色与反白区块按样张目测"
}
```
角色至少要有：`primary` / `text` / `text-secondary` / `meta`。有反白区再加 `on-primary`（通常是白）。

## typography — 字体与字号

| 字段 | 示例 | 说明 |
|---|---|---|
| `families` | `["PingFang SC", "Trebuchet MS"]` | 中文在前，数字/西文在后 |
| `body_size_pt` | `10.4` | 正文字号 |
| `leading` | `2.15` | 行距倍数 |
| `para_space_mm` | `0` | 段间距；中文刊常见 0（靠行距撑开） |
| `scale` | `{ "cover_year": 21.5, "toc_no": 27, "section": 18, "article_title": 15.5, "quote": 14.1, "byline": 10.4 }` | **按角色存字号**，不要只存一串孤立 pt 值 |

## chrome — 每页固定件

```jsonc
"chrome": {
 "running_text": "区域观察",
 "running_pos": { "right_mm": 189.5, "top_mm": 13.9, "size_pt": 9.9, "color": "primary" },
 "logo":     { "file": "logo.svg", "x_mm": 10.8, "y_mm": 9.0, "w_mm": 55.1 },
 "folio":    { "y_mm": 275.6, "align": "right", "size_pt": 10.4, "color": "meta" }
}
```

## grids — 版心网格

```jsonc
"grids": {
 "A": { "left_mm": 31.7, "right_mm": 175.6, "top_mm": 30, "bottom_mm": 275, "use": "栏目页：动态 / 业绩 / 新闻" },
 "B": { "left_mm": 19.0, "right_mm": 191.0, "top_mm": 20, "bottom_mm": 274, "use": "文章页：深度内容正文" }
}
```
**双栏刊物**写成 `{"columns": 2, "gutter_mm": 6, "left_mm": ..., "right_mm": ...}`。

## page_templates — 页面模板

```jsonc
{
 "id": "unit_list",
 "component": "unit_list",    // 对应 build_draft.py 的 8 个组件之一
 "grid": "A",
 "slots": [
  { "id": "banner", "kind": "image", "x_mm": 14, "y_mm": 31, "w_mm": 182, "h_mm": 92, "role": "hero" },
  { "id": "deco",  "kind": "image", "x_mm": 27, "y_mm": 152, "w_mm": 1.6, "h_mm": 8.2, "role": "decoration" }
 ],
 "typography": { "title": 10.4, "section": 18 },
 "unit": "U1"           // 关联的 UnitPattern 编号
}
```
`component` 只能取：`cover` / `quote` / `masthead` / `toc` / `divider` / `unit_list` / `article` / `backcover`。

## fixed_pieces — 固定文案件

```jsonc
[
 { "id": "editorial", "cycle": "reuse-check", "text": "《某刊》编辑部 …" },
 { "id": "disclaimer", "cycle": "conditional",
  "condition": "内容涉及基金 / 证券 / 收益率时",
  "text": "重要提示：投资涉及风险……" },
 { "id": "cta_readmore","cycle": "per-unit", "unit": "U1", "text": "阅读原文" }
]
```
`cycle`：`every-issue`（每期照抄）/ `reuse-check`（沿用但要核对）/ `per-unit`（每个单元必有）/ `conditional`（条件触发）。

---

## scale_baseline — 篇幅基线（量级门禁的分母）

`build_draft.py --stats` 拿它算达成率，**任一项 <60% 直接判 FAIL**（硬规则 11、20）。
门禁**只认下面四个键名**，写别的名字会被静默忽略。

```jsonc
{
 "pages":    91,      // 自动：extract_style.py 写入 —— 样例物理页数
 "chars":    56000,   // 自动：extract_style.py 写入 —— 样例正文汉字总数
 "articles": 6,       // 人工补 —— 长文章篇数（逻辑篇数，不是物理页数）
 "units":    73,      // 人工补 —— 短条目单元总数（可选；短条目型刊物必填）
 "source":   "第21期实测：PyMuPDF 抽全文 56133 字 / 91 页；02 启明观察 6 篇"
}
```

| 键 | 谁写 | 量纲 | 不填的后果 |
|---|---|---|---|
| `pages` | 自动 | 物理页数 | — |
| `chars` | 自动 | 正文汉字总数 | — |
| `articles` | **人工补** | 逻辑篇数 | 门禁不覆盖文章数，「6 篇的栏只交 1 篇」照样通过 |
| `units` | **人工补** | 单元条数 | 短条目型刊物最容易量级不足，却测不出来 |

`source` 是给后人看的出处——写明「哪一期、怎么测的」；改基线值时必须同步改它。

## content.json — build_draft.py 的输入

```jsonc
{
 "issue": { "title": "...", "running_text": "..." },
 "pages": [
  { "template": "cover",   "images": {"bg": "cover.jpg"},
   "fields": {"issue_no": "第22 期", "yearmonth": "2026 / 08", "year": "2026", "x_mm": 36.6, "y_mm": 80} },
  { "template": "unit_list", "grid": "A", "folio": "02",
   "fields": {"section": "港澳地区法规动态", "banner": "b.jpg"},
   "units": [{"title": "…", "body": "…\n\n…", "cta": "阅读原文", "image": ""}] },
  { "template": "article",  "grid": "B", "folio": "20",
   "fields": {"hero": "h.jpg", "title": "…", "byline": "2026.08.30 张三 李四"},
   "blocks": [{"type": "h1|h2|p|li|quote|figure|caption|note|disclaimer", "text": "…", "src": "", "caption": ""}] },
  { "template": "backcover",
   "fields": {"contacts": [{"name": "北京总部", "lines": ["电话：…", "邮箱：…"]}]} }
 ]
}
```

块类型 `type` 一览：`h1`（主色小标题）/ `h2`（次级小标题）/ `p`（正文）/ `li`（项目符号）/ `quote`（引文竖线块）/ `figure` + `caption`（图与图注）/ `note`（致谢、脚注）/ `disclaimer`（免责声明块）。
正文支持极简富文本：`**加粗**`、换行 `\n`。
