# 状态契约

状态 schema 版本为 1，所有时间使用 UTC ISO 8601。

- `sources`：保存每个 URL、Feed 或 Gist 作者的 cursor、etag、last_modified 与最近成功时间。
- `items`：保存 source_key、revision、内容/语义哈希、规范 URL、状态与概念指纹。
- `concepts`：保存规范名、首选来源、`exported` / `published` 状态与可选 message_id。
- `pending_scan`：本轮来源状态快照；只有 selection 校验成功后才提交。

主路径为：

`discovered -> rejected | exported -> published`

其中 `published` 是可选状态，默认流程在 `exported` 结束。相同 revision、内容哈希、
语义哈希或已导出的概念指纹不得重复输出。空选择提交来源游标，但不发布。

状态更新必须在同目录写临时文件，完成 flush/fsync 后用 `os.replace` 原子替换。
未知 schema、JSON 损坏或字段类型错误时停止，不得静默重置。状态中不得保存正文、
token、cookie、open_id 或其他凭证。
