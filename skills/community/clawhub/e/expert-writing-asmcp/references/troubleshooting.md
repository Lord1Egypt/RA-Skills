# 排障指南

## 常见错误速查

| 错误现象 | 可能原因 | 处理方式 |
|---------|---------|---------|
| `cannot unmarshal string into Go struct` | source_ranges JSON 格式错误 | 使用 `[{"id":"短ID","type":"doc"}]` 格式 |
| mcporter call 超时 | 正文生成超过 60 秒 | 加大 `--timeout 180000` |
| 正文变成提纲格式 | 用了 `__全文写作__3` 而不是 `__大纲写作__1` | 正文必须用 `__大纲写作__1` |
| 目录创建失败 | docid 为空或格式错误 | 确认父目录 GNS 正确 |
| index-check 返回 0% | 索引服务未完成 | 等待 30 秒后重试 |
| `401 Unauthorized` | Token 过期 | 更新 mcporter.json Token 并重启 daemon |

---

## 技能名与 times 参数对照

| 任务 | skill_name | times | 说明 |
|------|-----------|-------|------|
| 生成大纲 | `__全文写作__3` | `0` | 生成章节结构 |
| 生成正文 | `__大纲写作__1` | `1` | 基于大纲写完整正文 |

**常见错误**：生成正文时用了 `__全文写作__3`，导致输出变成"本节将介绍..."的提纲格式，而不是完整正文。

---

## 超时问题

### 现象
```
Error: mcporter call failed: context deadline exceeded
```

### 原因
正文生成属于长耗时调用，默认 60 秒不够。

### 解决

**方式一：调用时加参数**
```bash
mcporter call anyshare-asmcp.smart_assistant \
  --timeout 180000 \
  access_token:"$ACCESS_TOKEN" \
  ...
```

**方式二：配置环境变量**
编辑 `~/.openclaw/config.toml`：
```toml
[skills.entries.expert-writing-asmcp]
env.MCPORTER_CALL_TIMEOUT = "300000"  # 5 分钟，毫秒
```

---

## source_ranges JSON 格式错误

### 现象
```
cannot unmarshal string into Go struct
```

### 原因
source_ranges 参数格式不符合要求。

### 正确格式
```json
[{"id":"2DDD46B195F24BCEB238DB59151CD15E","type":"doc"}]
```

### 常见错误
```json
# ❌ 错误：完整 docid
[{"id":"gns://FC1B4FE2/.../2DDD46B195F24BCEB238DB59151CD15E","type":"doc"}]

# ✅ 正确：只有 id（最后一段）
[{"id":"2DDD46B195F24BCEB238DB59151CD15E","type":"doc"}]
```

---

## 大纲未确认就写正文

### 现象
用户反馈"不是我想要的大纲，但已经生成正文了"

### 解决
严格遵守 C4 门闩：必须用户明确回复"确认，开始写正文"后才能调用 `__大纲写作__1`。

批量/定时场景：跳过无法确认的文件，标记为"待确认"。

---

## 401 Unauthorized

**处理步骤**：

1. 更新 `~/.openclaw/workspace/config/mcporter.json` 中的 Authorization 字段
2. 重启 daemon：`mcporter daemon restart`
3. 验证：`mcporter call anyshare-asmcp.doc_lib_owned`
