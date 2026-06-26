# Feishu API Notes for Bitable Permission Checker

## 字段类型参考

| type 值 | ui_type    | 说明 |
|---------|------------|------|
| 1       | Text       | 文本 |
| 2       | Number     | 数字 |
| 3       | SingleSelect | 单选 |
| 4       | MultiSelect | 多选 |
| 5       | DateTime   | 日期 |
| 7       | Checkbox   | 复选框 |
| 11      | User       | 人员 |
| 15      | URL        | 超链接 |
| 1001    | CreatedTime | 创建时间 |
| 1002    | ModifiedTime | 修改时间 |

「链接地址」列在原表中 type=1（Text），内容为纯文本 URL。

## feishu_fetch_doc 返回格式

### 成功（可读）
```json
{
  "success": true,
  "message": "Document fetched successfully",
  "doc_id": "xxx",
  "title": "文档标题",
  "total_length": 1234,
  "markdown": "..."
}
```

### 失败（无权/不存在）
```json
{
  "success": false,
  "error": "[NETWORK:5002] Failed to get child blocks\n💡 ...",
  "message": "...\n🔗 Caused by: forBidden"
}
```

### 限流
```json
{
  "success": false,
  "error": "[NETWORK:5002] Failed to get child blocks\n💡 ...",
  "message": "...\n🔗 Caused by: request trigger frequency limit"
}
```

## URL 解析规则

从「链接地址」列提取 doc_id：

```
https://asiainfo.feishu.cn/docx/FyttdcBTZoBqwTxlPtzcS0o5nIe
                                          ^ doc_id = "FyttdcBTZoBqwTxlPtzcS0o5nIe"

https://asiainfo.feishu.cn/wiki/WatPwWAAmi8NiQk2LV0ccrp7nrc?renamingWikiNode=false
                                          ^ doc_id = "WatPwWAAmi8NiQk2LV0ccrp7nrc"
```

注意：wiki URL 中的 `?` 后参数（`renamingWikiNode`, `from`, `create_from` 等）**不影响** doc_id 提取，直接取路径段即可。

## 频率限制策略

飞书云文档 API 的 `fetch_doc` 走的是 `docx/v1/documents/{doc_id}/blocks` 接口，单应用有 QPS 限制。实测最佳策略：

- 每批并发 ≤ 10 个请求
- 触发限流后，等待 3 秒再重试该批次
- 重试仍限流 → 等待 5 秒再重试一次
- 最终仍失败 → 标记为无权限（forBidden 等错误码同理）

## 常见错误码

| 错误信息关键词 | 含义 | 处理 |
|---|---|---|
| `forBidden` | 无读取权限 | 记为无权限 |
| `request trigger frequency limit` | 频率限制 | 等待后重试 |
| `document not found` | 文档不存在 | 记为无权限 |
| `NETWORK:5002` | 通用网络错误 | 重试一次 |
