# USER.md — 日记追踪状态追加内容

在现有 `USER.md` 末尾追加以下内容：

```markdown
## Diary

> last_update: 2026-01-01 00:00
> i_have_read_my_last_diary: true

`diary/` 目录下的文件列表由系统自动维护。
```

**字段说明：**
- `last_update` — 最后写日记的时间，每次写完更新为当前时间
- `i_have_read_my_last_diary` — 标记用户是否已读最后一篇日记
  - 每次写完新日记 → 设为 `false`
  - 用户看过之后 → 设为 `true`

**自动化规则：**
1. 写完日记后，自动更新 `last_update` 为当前时间，将 `i_have_read_my_last_diary` 设为 `false`
2. 用户确认已读日记后，将 `i_have_read_my_last_diary` 设为 `true`