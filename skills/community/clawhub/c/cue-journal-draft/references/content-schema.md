# content.json 字段规范

`content.json` 是**唯一的内容源**：三件套（html / pdf / docx·md）都由它渲染。
改内容只改这一个文件，不要去改渲染产物。

- 完整可运行样例：`assets/templates/content.example.json`
- 想看真实体量（60+ 页 / 40+ 条）：`examples/journal-qiming-regional/`

> 命令里的 `python` 在部分系统上是 `python3`，按你的环境替换。

---

## 1. 顶层结构

```jsonc
{
  "issue": {                      // 刊头信息，封面与页眉用
    "title": "《某刊》 第 22 期底稿",
    "no": "22",
    "yearmonth": "2026 / 08",
    "running_text": "区域观察",   // 页眉跑文；每页可用 page.running 覆盖
    "auto_folio": true            // 必填（强烈建议）：自动编页码并回填目录
  },
  "meta": {                       // 可选。只被 check_freshness.py 读
    "freshness_exceptions": [
      { "match": "标题前缀", "reason": "为什么它不是旧闻（必填，否则门禁不放行）" }
    ]
  },
  "pages": [ /* 见下 */ ]
}
```

| 键 | 必填 | 说明 |
|---|---|---|
| `issue` | 否 | 缺了封面会少期号年月；`--stats` 仍可跑 |
| `issue.auto_folio` | **建议必填** | 设为 `true` 后，`build_draft.py`/`export_pdf.py` 会给 toc/unit_list/article/backcover 自动编号，并把页码**回填目录**（目录项靠 `ref` 找 `anchor`，见 §2）。**漏了它目录页码全是空白**，且页脚无页码 |
| `meta.freshness_exceptions` | 否 | 时效门禁白名单。`match` 是**标题前缀匹配**，写全标题也行；`reason` 必须非空 |
| `pages` | **是** | 一页一个对象，顺序即页码顺序 |

---

## 2. page 通用字段（八种模板共用）

```jsonc
{
  "template": "unit_list",   // cover/quote/masthead/toc/divider/unit_list/article/backcover
  "grid": "A",               // 取 spec.grids 的键；缺省 unit_list→A，article→B
  "folio": "02",             // 页码。留空则由 auto_folio 自动编（cover/divider/masthead 不编）
  "folio_y_mm": 282.0,       // 页码纵向位置，缺省 页高-15mm
  "top_mm": 42.0,            // 本页内容起始高度；缺省 unit_list 42 / article 20
  "cont_top_mm": 22.0,       // 续页起始高度，缺省 22
  "images": { "bg": "path/or/url" },   // 整页底图。有底图时前景色自动切浅色系
  "running": true,           // 本页是否出页眉
  "running_text": "覆盖刊头跑文",
  "foot_text": "页脚文字",
  "fields": { /* 各模板不同，见 §3 */ },
  "units":  [ /* unit_list 用 */ ],
  "blocks": [ /* article 用 */ ]
}
```

**没有底图时颜色会降级**（硬规则 12）：样刊的 `palette.meta` 常是白色（原刊页码压在深色图上），
照抄到无底图的新刊会让页码、目录页码、分隔页标题全部隐形。渲染器已按「本页有无 `images.bg`」
切换两套前景色，交稿前仍要逐页肉眼过一遍。

---

## 3. 八种模板的 `fields`

| template | 字段 | 说明 |
|---|---|---|
| `cover` | `title`/`name`、`org`、`subtitle`/`en`、`issue_no`、`yearmonth`、`year`、`x_mm`（默认36.6）、`y_mm`（默认80） | 期号块位置用 mm 微调 |
| `quote` | `quote`、`source` | 第三方评价/引言页 |
| `masthead` | `title`（默认"编辑部"）、`names:[]`、`note`（支持 `<br>`） | 编委会 |
| `toc` | `title`（默认 CONTENTS）、`groups:[{no,title,items:[{title,page\|ref}]}]` | 目录；页码要与正文对得上 |
| `divider` | `label`/`section`、`no`、`subtitle` | 分隔页；`label` 为空则整页留白 |
| `unit_list` | `banner`（图）、`kicker`、`section`（栏目标题）、`dek`（导语） | 内容在 `units[]` |
| `article` | `hero`（图）、`section`、`title`、`byline`、`abstract` | 内容在 `blocks[]` |
| `backcover` | `title`、`contacts:[{name, lines:[]}]` | 封底联系方式 |

目录项有两种等价写法：`page` 写死页码；`ref` 写**锚点**（对应某页的 `anchor` 字段），
页码由渲染器查 `anchor_map` 解析。**`page` 优先，没有才落 `ref`**。
用 `ref` 的好处是页码永远对得上，加页改版不用手改目录。
`build_draft.py` / `export_pdf.py` 都支持；`export_editable.py` 导出的是
`page or ref`，`import_docx.py` 按形态判回（纯数字/区间算页码，其余算锚点）。

`unit_list` 的 `units[]`：

```jsonc
{
  "title": "香港：发布《稳定币条例》配套指引",   // 标题
  "meta":  "2026.04.10 香港金融管理局",          // 日期+来源行；check_freshness 从这里取日期
  "body":  "第一段。\n\n第二段。",                // 双换行分段
  "cta":   "阅读原文",                            // 固定收尾
  "image": "images/fig-01.png"                    // 可选
}
```

`article` 的 `blocks[]`（`type` 决定样式）：

| type | 渲染成 |
|---|---|
| `p`（默认） | 正文段 |
| `h1` / `h2` | 一/二级小标题 |
| `li` | 项目符号 |
| `quote` | 引文块 |
| `note` | 注释块 |
| `figure` | 图位；`src` 有值则出图，无值出「图位待补：<caption>」占位框 |
| `disclaimer` | 免责声明 |

`figure` 的 `caption` 出图注，`alt` 只在没 caption 时兜底当占位文字。

---

## 4. 图片路径规则

`img_src()` 的处理顺序：

1. `http://` `https://` `data:` 开头 → 原样输出（可直接放 base64）；
2. 本地文件**存在** → 转成 `file:///绝对路径`（换机器也能打开，前提是图跟着走）；
3. 其他（含**路径写错的本地文件**）→ 原样输出，渲染出来就是坏图。

所以：图用**相对路径**并放在 content.json 同级目录下最稳；写绝对 Windows 路径也能用，
但一换机器就碎。图还没到位就留 `""`，`figure` 会画占位框，不会静默空白。

---

## 5. 自检

```bash
python scripts/build_draft.py --spec stylespec.json --content content.json --out out/ --stats
# unknown:[...] 非空 = 有 template 写错（八个之外），那几页会是空的
# overflow:[...] 非空 = 内容超出该页，被 overflow:hidden 静默裁掉
# 达成率任一项 <60% = FAIL

python scripts/check_freshness.py --content content.json --issue-date 2026-09-17 --window 6
# ERROR(FUTURE) 必须改；WARN(STALE) 要么删要么写 meta.freshness_exceptions
```

**分页溢出是静默的**（`.page{overflow:hidden}`），肉眼扫一眼容易漏——`--stats` 的
`overflow` 和页数是唯一可靠信号。若页数比预期少很多，多半是 `top_mm` / 单元 meta 行
高度算漏了，见 `build_draft.py` 的 `head_height_mm()` 注释。
