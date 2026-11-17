# Daily Workflow / 项目记忆工作流 - Security Guide

Version: 4.1.0

## Security Statement / 安全说明

This skill may write project-local workflow notes when the user explicitly requests persistence or an established trigger authorizes it. It is designed for resumability and handoff, not for storing secrets, replacing project governance, or recording confidential source bodies.

本 Skill 只应在项目本地 `Docs/` 中写入工作流笔记，用于恢复上下文和交接，不用于保存密钥、账号凭证或完整敏感资料。

## Allowed Storage / 允许写入范围

Default allowed write scope when no project-owned workflow defines a narrower location:

```text
Docs/
```

Do not write global user state. Do not write outside `Docs/` unless the user explicitly asks as part of the broader task.

Before writing, resolve the actual workspace and repository, preserve dirty changes, identify existing governance ownership, and avoid creating competing state files.

## Sensitive Data Rules / 敏感信息规则

Never record:

- API keys, tokens, passwords, private keys, cookies, OAuth refresh tokens, browser sessions.
- `.env` values or credential files.
- Full private customer records.
- Long confidential source excerpts.
- Large unrelated logs.

If sensitive context is relevant, record a safe summary and the non-secret location where the user can find the source.

## Legacy Migration Safety / 旧版迁移安全

Legacy files may be read for migration, but must not be deleted automatically. If both old and new files exist, ask before merging. Do not migrate secret-like fields.

## Archive Safety / 归档安全

Archiving older status history is allowed only by moving content into `Docs/archive/`. Never delete history automatically.

## Release Checklist / 发布检查

- `SKILL.md` and `SECURITY.md` show version `4.1.0`; generated registry snapshots are excluded from the publish bundle.
- The package uses one bilingual skill, not separate English and Chinese packages.
- Legacy file migration is documented.
- `NEXT_ACTIONS.md` is the primary continuation file, with `SCHEDULE.md` treated as compatibility alias.
- Existing project/governance files remain authoritative; the lightweight profile starts with only `STATUS.md` and `NEXT_ACTIONS.md`.
- Completion, verification, and independent acceptance remain separate.
- No example contains real credentials or private data.
