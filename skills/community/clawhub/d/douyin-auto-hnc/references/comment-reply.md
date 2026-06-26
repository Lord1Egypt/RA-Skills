# 评论导出与自动回复

## 完整流程

编排器 `douyin_full_orchestrator.py` 的 `run()` 在发布完成后自动执行：

```
export_comments() → build_reply_plan() → reply_comments()
```

## 路径

- **导出脚本：** `{creator_tools}/src/export-douyin-comments.mjs`
- **回复脚本：** `{creator_tools}/src/reply-douyin-comments.mjs`
- **输出目录：** `{comments_output}`

以上变量取自 CONFIG.md，由 `scripts/setup.py` 自动解析。

## 单独导出评论

```bash
node "{creator_tools}/src/export-douyin-comments.mjs" \
  --out "{comments_output}/unreplied-comments.json" \
  --limit 50
```

## 单独执行回复

```bash
node "{creator_tools}/src/reply-douyin-comments.mjs" \
  --limit 20 \
  --keep-open \
  --out "{comments_output}/reply-result.json" \
  --timeout 600000 \
  -- "{comments_output}/auto-reply-plan.json"
```

> 注意：回复操作需要已登录 Chrome 浏览器，不要加 `--headless`。

## 回复分类规则

| 类型 | 关键词 | 回复风格 |
|------|--------|---------|
| q（问答） | how/what/why/怎么/如何/请问/教程 | 引导看视频/下次覆盖 |
| t（感谢） | thank/great/helpful/有用 | 感谢支持 |
| n（负面） | bad/wrong/fake/垃圾/骗人 | 中性感谢 |
| f（关注） | follow/粉丝/关注 | 欢迎关注 |
| d（默认） | 其他 | 简短肯定 |

## 数据库查询

```bash
sqlite3 "{chatgroup_db}" "SELECT * FROM comments LIMIT 10"
```

comments 表字段：`item_id`、`username`、`text`、`reply_status`（pending/sent/failed）
