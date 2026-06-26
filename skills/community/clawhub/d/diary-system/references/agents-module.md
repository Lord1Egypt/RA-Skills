# AGENTS.md — 启动检查规则追加内容

在现有 `AGENTS.md` 的 "Every Session" 部分，追加第 5 步：

```markdown
## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`
5. **Diary check**: 如果 `i_have_read_my_last_diary` 为 `false`，开场 MUST 问用户："我昨天写了篇日记，想看吗？"（用用户的语言）
```

**注意：** 第 5 步只在 `i_have_read_my_last_diary` 为 `false` 时触发。如果用户已读，开场时无需提及日记。