# claude-memory-graph-audit

> Claude Code skill：审计你的 session memory 目录（`~/.claude/projects/<session>/memory/`）作为知识图谱的健康度，检测断链、孤立页、桥接节点和稀疏聚类。

灵感来自 [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) 的 4 信号知识图谱模型，以及 Andrej Karpathy 在 2024 年提出的 LLM Wiki 设计构想（"知识应该被编译，而不是被检索"）。

## 解决的问题

Claude Code 的 session memory（`~/.claude/projects/<session-uuid>/memory/*.md`）随着会话累积，会出现典型的知识库腐烂模式：

1. **断链**：`[[wikilink]]` 引用了不存在或已重命名的 memory（最常见原因：frontmatter 的 `name:` 字段是 kebab-case，文件名是 snake_case，混用导致）
2. **孤立页**：fact 越加越多但互不引用，相关知识无法通过图谱召回
3. **稀疏聚类**：同一领域的 memory 各自漂着，没形成知识团块
4. **缺桥**：跨领域的关键连接节点缺失，导致跨领域查询召回不全

mempalace 的 `associate` / 语义搜索用的就是这张图，链接质量直接决定召回质量。

## 一键体检

```bash
~/.claude/skills/claude-memory-graph-audit/scripts/audit.sh
```

输出示例：

```
📁 Memory dir: /Users/.../memory
🔢 Nodes: 21

=== 🐛 Broken wikilinks ===
  ✅ none

=== 🏝️ Orphan pages (in=0 AND out=0) ===
  ✅ none

=== ⭐ Hub nodes (in-degree ≥ 3) ===
  ⭐ in=3   feedback_wechat_push_method.md
  ⭐ in=3   reference_html_anything_templates.md

=== 🌉 Bridge candidates (out-degree ≥ 3) ===
  🌉 out=5   project_hk_payroll_wechat.md
  🌉 out=3   project_sapphire_2026_article.md

=== 📊 Summary ===
  Nodes:             21
  Total edges:       23 (unique targets: 15)
  Broken links:      0
  Orphan pages:      0
✅ Graph is healthy.
```

## 安装

```bash
mkdir -p ~/.claude/skills/claude-memory-graph-audit
git clone https://github.com/heavenchenggong/claude-memory-graph-audit.git /tmp/cmga
cp -r /tmp/cmga/* ~/.claude/skills/claude-memory-graph-audit/
chmod +x ~/.claude/skills/claude-memory-graph-audit/scripts/audit.sh
```

或通过 ClawHub：

```bash
clawhub install claude-memory-graph-audit
```

## 触发词

在 Claude Code 里说以下任一话术，会自动激活这个 skill：

- "memory 体检 / 审计 / 健康度"
- "memory 之间关联够不够"
- "用 LLM Wiki 思路看一下 memory"
- "哪些 memory 是孤立的"
- "memory 库越来越散"

## 4 信号思路（简化版）

LLM Wiki 用 4 个信号判断知识节点关联：

| 信号 | 权重 |
|---|---|
| 来源重叠（同源文档衍生） | ×4.0 |
| 直接 `[[wikilink]]` | ×3.0 |
| Adamic-Adar（共同邻居） | ×1.5 |
| 类型亲和（同类页面） | ×1.0 |

对纯文本 memory 库（不含向量库、不跑 LLM），简化为可执行版：

- 直接 wikilink 抽边
- 入度 / 出度 / 双零度判孤立
- 跨聚类的高出度节点判桥接

## 修复原则

1. 写 `[[X]]` 时永远用**文件名**，不是 frontmatter `name:`。这是断链的最大来源
2. 不要为了美观瞎加 link——只加真实存在的语义关系
3. `reference_*` 类工具/基础设施 memory 即使 in=0 但 out>0 是健康的，不要强行接入
4. 修复完一定要复检（重跑 `audit.sh`）

## 何时**不**做

- memory 库 < 10 条：直接读 MEMORY.md 索引就够
- 用户在赶活：不要中途打断
- 同会话内已经做过：别重复

## 适用场景

- 任何用 Claude Code session memory 的用户
- ECC（Everything Claude Code）插件用户
- 把 markdown + frontmatter + `[[wikilink]]` 当个人 wiki 的 Obsidian/Logseq 用户（脚本通用）

## 协议

MIT
