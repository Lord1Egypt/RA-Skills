# Code-to-Skill · 建筑规范转换器 (1.0.5, self-contained)

将建筑设计规范、国家标准（GB）、行业规程、法律法规的 **PDF** 转化为结构化的、可查询的 AI Skill：按触发条件索引每一条条文，保留「应 / 宜 / 可 / 不应 / 不得」法律效力措辞原文，提取数据表格为结构化 JSON，绘制跨规范引用关系图。

## 特性

- **索引而非概括**：每条编号条文都是可检索目标，法律措辞原文保留。
- **表格即数据**：耐火等级、防火间距、疏散宽度等表 → `.json`（程序查询）+ `.md`（阅读）。
- **强制力审计**：标注每条条文的强制等级（应 / 不应 / 不得 / 宜 / 可）。
- **自包含引擎**：内置 `scripts/extract.py` + `book_to_skill/`，无需外部安装 `book-to-skill`。
- **安全扫描**：自带 `tools/scan_generated_skill.py` 对生成的规范 Skill 做安全 + 强制力审计。

## 快速使用

提供规范 PDF 后，由 Agent 按 `SKILL.md` 的 Step 0–10 流程执行：

1. 输入验证：提供规范 PDF 路径（不要只给编号凭记忆编造）。
2. 文本提取：`python3 <skill>/scripts/extract.py <规范.pdf> --mode text --install-missing ask`
3. 结构分析 → 生成 `clauses/`（条文原文）+ `tables/`（.json/.md）+ `cross-refs.md` + `mandatory-map.md`
4. 安全扫描：`python3 <skill>/tools/scan_generated_skill.py <生成的规范skill目录>`

## 依赖

- 本地 Python 3.8+
- 可选 `poppler-utils`（`pdftotext`）提升表格 / 版式提取质量；缺省自动回退 `pypdf` / `pdfminer`

## 目录结构

```
code-to-skill/
├── SKILL.md                 # 主说明（frontmatter + Step 0–10）
├── README.md
├── CHANGELOG.md
├── _meta.json              # 发布元数据
├── skill-card.md            # 技能卡片
├── references/              # 参考与设计说明
├── scripts/
│   └── extract.py           # 自包含 PDF 提取入口
├── book_to_skill/           # 内置提取引擎
│   ├── cli.py  config.py  sanitize.py  dependencies.py  utils.py  exceptions.py
│   └── parsers/             # calibre / epub / pdf / docx / rtf / html / text
└── tools/
    └── scan_generated_skill.py  # 安全扫描 + 强制力审计
```

## License

MIT-0（详见 `skill-card.md`）
