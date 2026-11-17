# edit-cover（尽力而为）

优先在 `post-video.mjs --yes` 里、点击「发布」之前换封面。这个脚本只补已经发出的视频笔记。

```bash
node skills/xiaohongshu-ego/scripts/edit-cover.mjs \
  --note-id <noteId> \
  --cover /absolute/path/to/cover-3x4.png \
  --expect-account "听懂AI"
```

没有 `--yes`：检查登录，打印计划（含封面路径和 update URL），退出码 `3`，不上传。

有 `--yes` 时：

1. 打开 `https://creator.xiaohongshu.com/publish/update?id=<noteId>&noteType=video`（笔记管理 → 编辑 会到这个地址）。
2. 核对 `--expect-account`。
3. 页面如果是「加载失败」，退出码 `1`，不点发布。
4. 悬停主封面卡片点「编辑封面」，`setInputFiles` 到弹窗里 `.upload-btn input.upload-input`，等「完成」可用后点它。不用 PK 槽。
5. 主封面预览发生变化才点发布。否则不点。
6. 点页脚上文本正好是「发布」的按钮。

2026-11-04 在笔记 `6aeae281000000000e00cb56` 上核对过这条路径。保存后笔记可能重新「审核中」，角标可能是「封面PK中」。另一条笔记曾从笔记管理消失，更新页显示「加载失败」。所以这不是主路径，失败了不要再发一条新笔记。
