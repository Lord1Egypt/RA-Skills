---
name: cross-session-memory
description: 给 AI agent/bot 做跨会话持久记忆的分层混合方案。当用户要"给 bot 加记忆""让 agent 记住之前的事""跨会话上下文持久化""记忆去重/断链/陈旧检查"，或要搭一个有长期记忆的 agent 时使用。方案=markdown 真理源(人可读可手改) + SQLite 派生索引(选择性召回) + 生命周期检查(断链/重复/陈旧)，纯标准库零依赖。
---

# 跨会话文件式记忆（分层混合）Skill

## 解决什么问题
纯文件记忆的召回是"全量读索引 + 凭关键词碰"，事实一多就烧 context、漏召回、去重靠手、断链没人查、陈旧事实误导。本 Skill 把召回从"全量塞"变成"选择性取"，并自动做生命周期维护。

## 三层架构

### 第一层：markdown 真理源（不动）
每个事实一个 `.md`，frontmatter 带 `name / description / type / updated`，正文写事实。
- 人能读、git 能 diff、可跨 bot 同步；
- `MEMORY.md` 是人看的索引（一行一个指针）。
`type` 取值：`user`（用户画像）/ `project`（进行中工作，会过时）/ `reference`（外部指针，较稳定）。

### 第二层：派生索引（脚本构建）
`scripts/build_index.py` 扫描 memory 目录，解析 frontmatter，写入 `memory.db`（SQLite，标准库）。
`scripts/recall.py "<词1 词2 ...>"` 做选择性召回：按词 AND 匹配 name+description+body，返回 top-k 文件路径，按需再 Read 全文。**从全量塞 context 变成按需取。**

### 第三层：生命周期检查（修三个老坑）
`scripts/lint.py` 一次输出三类问题：
- **断链**：`[[name]]` 目标不存在；
- **重复**：description 相同的事实；
- **陈旧**：`type: project` 且 `updated` 超过 N 个月 → 召回时附"【请先核实此事实是否仍成立，文件/函数/flag 可能已变】"。

## 工作流程
1. 搭记忆目录：放若干 `<slug>.md` + 一个 `MEMORY.md` 索引。
2. `python scripts/build_index.py <memory_dir>` 建索引。
3. 召回：`python scripts/recall.py <memory_dir> "句法 GPT2" --k 5`。
4. 体检：`python scripts/lint.py <memory_dir> --stale-months 3`。
5. 日常：增删事实后重跑 build（recall 检测到 .md 比 db 新会自动重建）。

## 关键原则
- **真理源始终是 .md**：db 只是派生物，可随时删了重建，绝不手改 db。
- **召回后核实**：对 `type:project` 的陈旧事实，应用前先核实文件/函数/flag 是否还在。
- **零依赖**：只用 Python 标准库（sqlite3），受限网络/不装包环境直接跑。
- **中文友好**：召回用子串匹配（LIKE 语义），不做分词，中文不漏匹配。

## 使用样例
见 `examples/sample-memory/`。演示命令：
```bash
python scripts/build_index.py examples/sample-memory
python scripts/recall.py examples/sample-memory "句法 GPT2"
python scripts/lint.py examples/sample-memory --stale-months 3
```
