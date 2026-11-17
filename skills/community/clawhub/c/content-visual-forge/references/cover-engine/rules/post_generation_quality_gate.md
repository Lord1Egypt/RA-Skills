# Post Generation Quality Gate

## 每次生成后必须检查
### 文字检查
- 主标题是否正确
- 是否有错字
- 是否有半残字
- 是否有主标题以外中文小字
- 是否有书脊字、便签字、笔记字、地图字

### 构图检查
- 标题区是否干净
- 画面是否过满
- 主视觉是否清晰
- 缩略图是否可读

### 风格检查
- 是否符合文章情绪
- 是否过度科技感
- 是否廉价营销海报感
- 是否存在版权/IP 风险

## 结果
- pass：可以使用
- minor_revision：可以微调
- regenerate_required：必须返工

## 状态动作

| 结果 | 动作 |
|---|---|
| `pass` | 允许交付；正式封面必须同步标题排版规格与 Run Log |
| `minor_revision` | 只允许局部修正，最多 2 次；不得改变 Source Lock 主线 |
| `regenerate_required` | 不得交付；按问题回到内容分析、风格路由、Prompt Builder 或背景重生成 |

如果出现可读小字、错别字、半残字、标题错误、参考图复制或版权/IP 风险，最低结果为 `regenerate_required`。
