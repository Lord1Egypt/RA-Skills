# reports/

运行 `./agent.sh book <书名>` 之后，两件套会输出到这里：

- `<书名>-<日期>.html` — HTML 研究报告（含 Mermaid 人物关系图）
- `chat-弹药库-<书名>-v1.md` — Markdown 弹药库（3 开场 + 6 故事 + 5 反问 + 3 收尾）

**本目录默认是空的**。`book-report` 是通用工具，不带任何预生成示例——想看产物长什么样，自己跑：
```bash
./agent.sh book <任意书名> --author <作者>
```

## 文件命名规则

- HTML 报告：`<书名>-<YYYY-MM-DD>.html`（每天跑覆盖）
- 弹药库：`chat-弹药库-<书名>-v1.md`（v1 是模板版本号；以后模板升级到 v2 会变成 v2）

## 想清空历史产物

```bash
rm reports/*.html reports/*.md
```

不放心的话加 `-i` 逐个确认。
