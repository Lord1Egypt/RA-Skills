---
name: claude-memory-graph-audit
description: |
  审计并修复 Claude Code 的 session memory 目录（如 ~/.claude/projects/<session>/memory/）作为知识图谱的健康度。
  触发场景：
  - 用户说"体检/审计/检查我的 memory"、"memory 库健康度"、"哪些 memory 是孤立的"
  - 用户说"用 LLM Wiki 思路看一下 MEMORY"、"我的 memory 之间关联够不够"
  - 用户怀疑 [[wikilink]] 写错了、或 memory 文件越来越多但越来越散
  做的事：检测断链、孤立页、桥接节点、稀疏聚类，并提议或直接修复链接。
author: Heaven Gong
version: 1.0.0
date: 2026-05-30
---

# Claude Memory Graph Audit

## 问题

Claude Code 的 session memory（`~/.claude/projects/<session-uuid>/memory/*.md`）在长期使用中会出现典型的知识库腐烂模式：

1. **断链**：`[[wikilink]]` 引用了不存在或已重命名的 memory（常因 frontmatter 的 `name:` 字段是 kebab-case 而文件名是 snake_case 导致命名混用）
2. **孤立页**：fact 越加越多但互不引用，相关知识无法通过图谱召回
3. **稀疏聚类**：同一领域的 memory 各自漂着，没形成知识团块
4. **缺桥**：跨领域的关键连接节点缺失，导致跨领域查询召回不全

mempalace 的 `associate` / 语义搜索用的就是这张图，链接质量直接决定召回质量。

## 何时触发

| 场景 | 信号 |
|---|---|
| 用户主动问 | "memory 体检 / 审计 / 健康度 / 孤立"、"用 LLM Wiki 思路看一下 memory" |
| Claude 自己警觉 | 一次会话写了 ≥3 个新 memory；用户提到他不知道某个旧 fact 还在 |
| 周期性维护 | 用户说"清理一下 memory"或 ≥20 条 memory 一次都没维护过 |

## 解法（4 信号思路，借用自 LLM Wiki / nashsu/llm_wiki）

LLM Wiki 用 4 个信号判断节点关联：source-overlap ×4.0、wikilink ×3.0、Adamic-Adar ×1.5、type-affinity ×1.0。
对纯文本 memory 库，简化成可执行版：

### 步骤 1：清点节点

```bash
MEM_DIR="${1:-$HOME/.claude/projects/$(ls -t $HOME/.claude/projects | head -1)/memory}"
cd "$MEM_DIR"
ls *.md | grep -v MEMORY.md
```

每个 `.md` 文件 = 一个节点。`MEMORY.md` 是索引，不算节点。

### 步骤 2：抽边（直接 wikilink 信号）

```bash
grep -h -oE '\[\[[a-z_-]+\]\]' *.md | sort -u
```

每条 `[[X]]` = 一条出边，目标是文件 `X.md`。

### 步骤 3：四种诊断

**(a) 断链** — link 指向不存在的文件：
```bash
for link in $(grep -h -oE '\[\[[a-z_-]+\]\]' *.md | sed 's/\[\[//;s/\]\]//' | sort -u); do
  [ -f "${link}.md" ] || echo "❌ broken: [[$link]] in $(grep -l "\[\[$link\]\]" *.md | tr '\n' ' ')"
done
```
最常见的两种断链：(1) wikilink 用了 frontmatter `name:` (kebab-case) 而非文件名 (snake_case)，(2) 历史 rename 没同步引用。

**(b) 孤立页（双零度）** — `in=0` 且 `out=0`：
```bash
for f in *.md; do
  [ "$f" = "MEMORY.md" ] && continue
  base="${f%.md}"
  out=$(grep -oE '\[\[[a-z_-]+\]\]' "$f" | sort -u | wc -l | tr -d ' ')
  in=$(grep -l -E "\[\[$base\]\]" *.md 2>/dev/null | grep -v "^$f$" | wc -l | tr -d ' ')
  [ "$out" = "0" ] && [ "$in" = "0" ] && echo "🏝️ orphan: $f"
done
```
注意：`reference_*` 工具/基础设施类 memory 即使 in=0 但 out>0 是健康的——它们靠 description 直接被语义搜索召回，不需要别的 memory 引用。**真正不健康的是双零度**。

**(c) Hub 节点** — in-degree ≥ 3，是图谱的承重墙：
```bash
for f in *.md; do
  base="${f%.md}"
  in=$(grep -l -E "\[\[$base\]\]" *.md | grep -v "^$f$" | wc -l | tr -d ' ')
  [ "$in" -ge 3 ] && echo "⭐ hub (in=$in): $f"
done
```

**(d) 桥接节点** — out-degree ≥ 3 且涉及多个聚类。手动判定：看一个文件的 out-link 是否跨了"内容 / 工具 / 项目"等不同语义聚类。这种节点要保护好，删了会断很多语义路径。

### 步骤 4：修复

**修断链**（无风险）：
```bash
# 把 [[old-name]] 全局换成 [[new-name]]
grep -l "\[\[old-name\]\]" *.md | xargs sed -i '' 's/\[\[old-name\]\]/[[new-name]]/g'
```

**接孤立页**（要思考）：
对每个孤立页，回答两个问题：
- 它服务于哪个 active 项目？→ 在末尾加 `服务于 [[project_xxx]]`
- 它依赖什么基础事实？→ 在末尾加 `参考 [[feedback_xxx]] [[reference_xxx]]`

格式约定：
```markdown
**相关：**
- [[other_memory]] — 一句话说明关系
```

不要在文件中间加 link——放末尾"相关"段，用户和未来的你扫一眼就知道。

### 步骤 5：复检

跑步骤 3 (a) 和 (b)，确认断链=0、双零度孤立=0。报告改善：工作边数 / 断链率 / 孤立数 三个指标即可。

## 修复原则

1. **不要为了美观瞎加 link**——只加真实存在的语义关系（项目用 fact、fact 服务项目、工具被工作流依赖）
2. **kebab vs snake**：写 `[[X]]` 时永远用**文件名**，不是 frontmatter `name:`。这是断链的最大来源
3. **保护工具类 memory 的 in=0 状态**：reference_* 类 memory 通过 description 被语义搜索直接召回，不需要被引用
4. **批改完一定要复检**——sed 全局替换可能误伤其他相似字符串

## 何时**不**做

- memory 库 < 10 条：直接读 MEMORY.md 索引就够
- 用户在赶活：不要中途打断去做体检
- 已经在做体检的同一会话内：别重复做

## 参考

- 灵感：nashsu/llm_wiki 的 4 信号知识图谱（来源重叠×4.0 / wikilink×3.0 / Adamic-Adar×1.5 / 类型亲和×1.0）
- 灵感：Karpathy 2024 LLM Wiki 设计文档（"知识应该被编译，而不是被检索"）
- 实践案例：见 [[reference_ecc_installation]] 用户使用的 memory 系统结构
