# Changelist entry template

Pick ONE language variant matching the target project's docs language and delete the other.

## 中文

```markdown
# {一句话摘要：动词开头，说清改了什么行为}

- 日期：{YYYY-MM-DD}
- 作者：{人类负责人：与 git author 一致或按项目约定；单人项目可省略此行}
- 范围：{主要改动文件列表}

## 问题 / 根因

{观察到的现象 → 定位到的根因。引用具体文件与行为链路，不要只写"有个 bug"。}

## 改动

{按文件或主题列出关键改动，附关键 diff 片段；说明每处改动解决根因的哪一环。}

## 设计决策 / 取舍

{为什么选这个方案、放弃了什么、兼容性与迁移如何处理、回退条件。}

## 验证

- {真实命令} → {真实结果（退出码 / 通过数）}
```

## English

```markdown
# {one-line summary: verb-first, states the behavior change}

- Date: {YYYY-MM-DD}
- Author: {human owner of the task; matches the commit's git author or the project convention; omit for single-person projects}
- Scope: {main files changed}

## Problem / Root cause

{Observed symptom → actual root cause, with file references and the behavior path, not just "there was a bug".}

## Changes

{Key changes per file or theme, with key diff snippets; tie each change to the part of the root cause it fixes.}

## Decisions / Trade-offs

{Why this approach, what was rejected, compat/migration handling, rollback conditions.}

## Validation

- {real command} → {real result (exit code / pass count)}
```
