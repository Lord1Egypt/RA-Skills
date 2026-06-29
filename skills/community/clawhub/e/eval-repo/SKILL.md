---
name: eval_repo
description: Fetch GitHub repository metadata and project files, generate an evidence-based repository evaluation, and save the evaluation into the target knowledge base.
---

# Skill: eval_repo — GitHub 仓库评估

## 用途

当用户发 GitHub 仓库并要求“评估/值不值得/能不能复现/环境怎么配”时，抓取 README、依赖和元信息，结合目标知识库上下文生成评估报告并保存。

## 触发条件

Activate when:

- 消息包含 GitHub repo 链接
- 且包含“评估、值不值、有没有用、能不能复现、环境怎么配、要不要深入”等意图

Do NOT activate when:

- 用户只是说“存一下这个 repo” → `ingest_document`
- 用户发 Gitea 资料仓库要求批量编译 → `batch_compile`

## 执行流程

### 1. 抓取 GitHub 信息

```bash
python3 scripts/fetch_github.py --url "<github repo url>"
```

脚本返回 `text_path`，里面包含 README、依赖文件和仓库元信息。

### 2. 确定保存目标

先解析目标：

```bash
python3 scripts/resolve_eval_target.py \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid>
```

目标规则：

- 私聊默认个人库
- 用户明确贡献团队库时保存团队库
- 用户明确双写时保存两个库
- 群聊时必须通过 `GroupSubject -> chat_bindings.json` 找到团队，默认保存到该团队知识库
- 群聊不允许保存到个人知识库

### 3. OpenClaw + MiniMax 生成评估 Markdown

必须包含：

- 三档结论：值得深入 / 选择性参考 / 暂不建议
- 与研究方向相关性
- README/依赖/活跃度/许可证/复现风险
- 与知识库已有资料关系
- 来源链接

### 4. 保存评估

```bash
python3 scripts/save_eval.py \
  --owner <owner> --repo <repo> \
  --title "<标题>" \
  --eval_file /tmp/paperkb/draft_eval.md \
  --brief "<简介>" \
  --keywords "关键词1,关键词2" \
  --score 8 \
  --source_url "<github url>"
```

## 回复

回复必须给：

- 结论
- 相关性
- 复现风险
- 保存链接

## 脚本清单

- `resolve_eval_target.py`：解析私聊/群聊保存目标
- `chat_context.py`：解析 OpenClaw 群聊上下文和群绑定
- `fetch_github.py`：抓取 GitHub 仓库信息
- `save_eval.py`：保存 GitHub 评估
