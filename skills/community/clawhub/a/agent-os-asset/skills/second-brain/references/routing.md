# Routing / 路由

English is normative; ZH-CN is paired. / 英文为规范文本；简体中文为配对译文。

Start with one to three focused queries against the primary index. Use terms from the user's request, then broaden with domain synonyms only when results are weak.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 先对主索引执行一到三个聚焦查询。优先使用用户请求中的词，只有结果较弱时才使用领域同义词扩展。

- Working style and tool preferences: query the named tool, workflow, preference, or decision.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 工作方式与工具偏好：查询点名的工具、workflow、偏好或决策。
- Coding support: query the language, framework, architecture, module, error, or testing practice.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 编程支持：查询语言、framework、architecture、module、error 或测试实践。
- AI/ML research: query the model, method, benchmark, paper title, or research topic.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: AI/ML 研究：查询 model、method、benchmark、论文标题或研究主题。
- Product and business: query the product, customer problem, metric, experiment, market, or decision.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 产品与业务：查询产品、客户问题、metric、experiment、market 或决策。
- Reports and research collections: query the separately configured report index with `--index "$SECOND_BRAIN_REPORT_INDEX"`.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 报告与研究集合：使用 `--index "$SECOND_BRAIN_REPORT_INDEX"` 查询单独配置的报告索引。
- Books and long-form notes: query the title, author, theme, or principle only when the user asks for reading-derived context.
<!-- bilingual-compat: paired English translation appears immediately above. -->
- ZH-CN: 书籍与长文笔记：仅当用户需要阅读所得 context 时，查询标题、作者、主题或原则。

Prefer authored or curated material over raw imports:
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 优先使用原创或精选材料，而不是原始导入：

1. Explicit decisions and authored notes.
<!-- bilingual-compat: paired English translation appears immediately above. -->
   ZH-CN: 明确决策与原创笔记。
2. Curated evergreen notes.
<!-- bilingual-compat: paired English translation appears immediately above. -->
   ZH-CN: 精选 evergreen 笔记。
3. Validated `.agent.md` summaries.
<!-- bilingual-compat: paired English translation appears immediately above. -->
   ZH-CN: 已验证的 `.agent.md` 摘要。
4. Raw inbox or imported material.
<!-- bilingual-compat: paired English translation appears immediately above. -->
   ZH-CN: 原始 inbox 或导入材料。

Use `--explain-routing` when federated project-index selection needs verification. Use `--workspace` to constrain a named project and `--asset-indexes never` when only the primary vault should be searched.
<!-- bilingual-compat: paired English translation appears immediately above. -->
ZH-CN: 需要验证联邦项目索引选择时使用 `--explain-routing`；使用 `--workspace` 约束指定项目，仅搜索主知识库时使用 `--asset-indexes never`。
