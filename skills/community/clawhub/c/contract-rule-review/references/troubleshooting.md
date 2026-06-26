# 排障指南

## 常见错误速查

| 错误现象 | 可能原因 | 处理方式 |
|---------|---------|---------|
| `401 Unauthorized` | Token 过期 | 更新 mcporter.json 的 Token，重启 daemon |
| `dir_create` 返回空 docid | 父目录 docid 错误 | 检查父目录是否已存在且正确 |
| `folder_sub_objects` 返回空 | 查询参数含中文名 | 需使用真实 UUID 查询，不能用中文路径 |
| `file_osendupload` 超时 | 网络不稳定 | 重试上传，上传有幂等性 |
| `index-check` 一直 0% | 索引服务忙碌 | 等待 30 秒后重试，上限 600 秒 |
| `smart_assistant` 返回空 | 文件未索引完成 | 确认 index-check 达到 100% 再调用 |
| `curl: PUT` 失败 | 文件名含中文/特殊字符 | 使用 `cat "$FILE" \| curl ... -T -` 代替 `curl --data-binary` |
| ACL 权限错误 | macOS 文件有 ACL | 用 `cp` 复制文件后上传副本 |

---

## 401 Unauthorized

**原因**：Token 过期或无效。

**处理步骤**：

1. 更新 Token 到 `~/.openclaw/workspace/config/mcporter.json`：

```bash
# 编辑 mcporter.json 中的 Authorization 字段
# 或使用 mcporter 配置命令
```

2. 重启 daemon：

```bash
mcporter daemon restart
```

3. 验证：

```bash
mcporter call anyshare-asmcp.doc_lib_owned
```

---

## dir_create 返回空 docid

**原因**：父目录 docid 不正确，或名称冲突。

**排查步骤**：

1. 确认父目录 docid 是否为完整 GNS（`gns://...` 格式）
2. 用 `folder_sub_objects` 确认父目录下确实有该名称的目录
3. 避免用中文名称拼接——始终用 `folder_sub_objects` 返回的真实 docid

---

## 文件名含中文/特殊字符导致 curl PUT 失败

**原因**：macOS 上 `curl --data-binary @"$FILE"` 对含中文路径的文件有解析问题。

**解决方案**：

```bash
# ❌ 错误
curl -X PUT -T "$LOCAL_FILE" "$URL"

# ✅ 正确：用 cat 管道代替
cat "$LOCAL_FILE" | curl -X PUT -T - "$URL"
```

---

## ACL 权限错误

**原因**：macOS 文件带有扩展 ACL，`chmod`/`xattr` 可能无法完全移除。

**现象**：上传时提示权限不足，但文件本身可读。

**解决**：复制文件后上传副本（`cp` 自动去除 ACL）：

```bash
cp "$LOCAL_FILE" "/tmp/$(basename "$LOCAL_FILE")"
# 然后上传 /tmp/ 中的副本
```

---

## 索引服务超时

**原因**：文件较大或索引服务忙碌。

**默认策略**：
- 轮询间隔：5 秒
- 最大等待：600 秒
- 超时后继续执行（不阻塞后续文件）

---

## smart_assistant 返回空内容

**排查顺序**：

1. 确认 `index-check` 返回 `process=100`
2. 确认 `source_ranges[].id` 为文件短 ID（不是完整 docid）
3. 确认 `temporary-area` 上传成功（code=0）
4. 检查 AnyShare 是否在限流（返回 429）

---

## cron 任务超时

**原因**：`timeoutSeconds` 设置过短，任务未完成就被 kill。

**解决**：将 cron job 的 `timeoutSeconds` 设为 0（无限制）或较大值（如 1800）。

```bash
# 查看当前值
cron get 833a0659-0f8b-4822-aa00-076f994a28a7

# 更新为无限制
cron update <jobId> --timeout 0
```

---

## 目录结构不符

**要求**：

```
合同审阅/
└── YYYY-MM-DD/           # 日期目录
    └── 合同名称/          # 合同名称目录
        ├── 合同原文/     # 必须有「合同原文」子目录
        │   └── 原文件
        └── 审阅报告.md   # 直接在合同名称目录下
```

**常见错误**：
- 审阅报告上传到了「合同原文/」目录（❌）
- 没有创建「合同原文/」子目录（❌）
