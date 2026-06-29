# 常见问题（FAQ）

> 本文件收录 everything-search-breadmemory 技能的常见问题与解答。
> AI 执行时遇到疑问，优先查阅本文件。

---

Q: es.exe 搜索结果不全怎么办？

A：确认 Everything 服务正在运行（任务栏托盘图标是否绿色）。若服务正常，检查 es.exe 路径是否正确，或运行 `python {SKILL_DIR}/scripts/es_search.py search "关键词" --path "C:/限定路径"` 缩小范围。

---

Q: 面包屑条目过多，如何高效检索特定条目？

A：使用 `python {SKILL_DIR}/scripts/breadcrumb.py search "关键词"` 做全文检索；或用 `--tag` 过滤特定标签。建议定期运行 `python {SKILL_DIR}/scripts/topology_donut.py generate` 生成知识图谱，自动发现条目间的逻辑关联。

---

Q: 艾宾浩斯复习间隔可以自定义吗？修改后会影响已有条目吗？

A：可以。编辑 `scripts/ebbinghaus.py` 中的 `INTERVALS` 常量（默认 `[1, 2, 4, 7, 14, 30, 60, 120]`）。调整后，已存在条目的复习间隔不受影响，仅新创建的条目会使用新间隔。

---

Q: everything-search-breadmemory 的数据存储在哪里？可以改用其他路径吗？

A：数据默认存储在 `~/.everything_search/` 目录（用户主目录下的隐藏目录）。如需修改路径，需同步修改 `scripts/` 下所有脚本中的 `DATA_DIR` 变量，确保指向同一新路径，然后手动迁移 `breadcrumb.json` 等数据文件。

---

Q: 拓扑甜甜圈（Topology Donut）生成的关联图谱有什么用？

A："甜甜圈"是知识关联图谱的比喻——每个面包屑条目是"糖粒"，条目之间的逻辑关联是"糖霜"。脚本会自动发现 5 种关联类型（`tag_cluster`、`content_bridge`、`source_family`、`sequential_chain`、`conceptual_hierarchy`），形成 4 种拓扑结构（`closed`、`nested`、`branching`、`chain`），帮助发现知识间的隐藏联系，辅助复习时触类旁通。

---

## 渐进式说明

本技能采用渐进式 MD 体系，详细 FAQ 见本文件。
SKILL.md 仅概述核心能力，不展开 FAQ 细节。
