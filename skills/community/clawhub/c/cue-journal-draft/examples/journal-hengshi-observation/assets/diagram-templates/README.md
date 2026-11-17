# diagram-templates —— 语义图定义范例

`gen_diagram.py` 的输入是这类 JSON。这里放的六份是第 22 期《区域观察》
实际用过的定义，可直接改成新刊的图。**它们是范例，不是成品**——内容必须换成
本期正文里的。

## 结构

```json
{
  "size_mm": [172.0, 107.5],
  "bg": "#FFFFFF",
  "palette": { "primary": "#A10F34", "text": "#000000",
               "meta": "#7F7F7F", "rule": "#D8D8D4", "tint": "#F5F4F1" },
  "blocks": []
}
```

坐标原点在图左上角，单位 mm。`palette` 缺省时用上述默认值，但实际应抄
`stylespec.json` 的色板，图才与刊物是一套。

## 六份范例各自演示什么

| 文件 | 版式 | 看点 |
|---|---|---|
| `fig_0.json` | `columns` + `footer` | 三列并列卡片：主色标题条 + 监管机构小字（`meta`）+「标签 / 内容」条目 |
| `fig_1.json` | `flow` + 两条 `footer(tint)` | 横向流程 + 箭头；补充说明走浅底横带，不与主色带抢视线 |
| `fig_2.json` | `rows` + `footer` | 四条主线：左侧主色标签块（`tag` + `sub`），右侧两条要点 |
| `fig_3.json` | `rows` + `footer` | 同上，用于「制度框架四要素」这类并列维度 |
| `fig_4.json` | `rows` + `footer` | 同上，用于「四项合规要求」 |
| `fig_5.json` | `rows`(3) + `footer(tint)` + `footer` | 行数不足时用浅底横带补齐版面，避免下半页空旷 |

## 用法

```bash
python <skill>/scripts/gen_diagram.py --spec fig_0.json \
    --out images/gen/fig_0.png --pdf images/gen/fig_0.pdf
```

## 内容从哪来

**每条要点都必须取自本期正文**，不要凭图注自由发挥。这正是它比文生图可靠的
另一面：图上每个字都能回正文核对。量化信息（门槛、期限、额度、数量）优先写进图
——那是读者看图真正想拿的东西。

## 放不下怎么办

脚本会告警「内容高 X 超出可用 Y」，说明内容画到框外了。按优先级处理：
精简文案 → 调字号 / `gap_mm` → 加大图幅 `size_mm`。**不要忽略告警。**

## 排版细节已内建，不用手工调

中文标点避头（句号逗号不落行首）；`rows` 标签过长时自动缩一号字，而不是把词断成
两行；`flow` 块内文字垂直居中（否则贴顶、下半留空）；英文单词不拦腰截断。
