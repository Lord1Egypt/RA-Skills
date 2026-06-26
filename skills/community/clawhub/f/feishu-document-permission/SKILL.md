---
name: feishu-document-permission
description: "设置飞书云文档为'获得链接的任何人可查看'，解决外部用户无法访问飞书文档的问题。适用于需要将飞书文档分享给组织外人员的场景。"
---

# 飞书文档权限设置技能

## 功能
设置飞书云文档为"获得链接的任何人可查看"，使外部用户（如鲲哥）能够访问文档。

## 触发场景
- 创建飞书文档后需要发送给外部用户
- 收到反馈说文档没有权限访问
- 需要批量检查/修复多个文档权限

## 输入参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `doc_token` | string | ✅ | 飞书文档 token（从文档链接提取） |
| `verify_only` | boolean | ❌ | 仅验证不修复（默认 false） |

**示例：**
```
doc_token: KTVQdB0NfohPjzxC8QOchE25nJd
verify_only: false
```

## 使用方式

### 方式 1：直接调用（推荐）
```
请设置飞书文档权限，doc_token: KTVQdB0NfohPjzxC8QOchE25nJd
```

### 方式 2：创建文档后自动调用
在创建飞书文档的 cron 任务或子代理中，完成后立即调用此技能：
```
1. 创建飞书文档 → 获得 doc_token
2. 写入文档内容
3. 调用 feishu-document-permission 技能设置权限
4. 验证权限生效
5. 发送邮件/消息通知
```

## API 调用流程

### 步骤 1：获取 tenant_access_token
```bash
APP_ID="cli_a9217db4a3f59cb6"
APP_SECRET="G34RRAc41XOY7vb2a7NmMgwl5chruBmo"

TENANT_TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"$APP_ID\",
    \"app_secret\": \"$APP_SECRET\"
  }" | jq -r '.tenant_access_token')
```

### 步骤 2：验证当前权限
```bash
curl -X GET "https://open.feishu.cn/open-apis/drive/v2/permissions/${DOC_TOKEN}/public?type=docx" \
  -H "Authorization: Bearer $TENANT_TOKEN" | jq .
```

**期望返回：**
```json
{
  "code": 0,
  "data": {
    "permission_public": {
      "link_share_entity": "anyone_readable",
      "external_access_entity": "open"
    }
  }
}
```

### 步骤 3：设置权限（如需要）
```bash
curl -X PATCH "https://open.feishu.cn/open-apis/drive/v2/permissions/${DOC_TOKEN}/public?type=docx" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -d '{
    "external_access_entity": "open",
    "link_share_entity": "anyone_readable"
  }'
```

**关键参数：**
- `type=docx` — **必须指定**，否则 API 不识别（v1 API 不支持 docx）
- `external_access_entity: "open"` — 允许分享到组织外
- `link_share_entity: "anyone_readable"` — 获得链接的任何人可查看

### 步骤 4：记录日志
```bash
echo "$(date): 文档 ${DOC_TOKEN} 权限已设置为 anyone_readable" >> memory/feishu_permission_log.md
```

## 错误 API（不要使用！）

以下 API 都返回 404 或无效参数：
- ❌ `PUT /docx/v1/documents/{id}/setting`
- ❌ `POST /docx/v1/documents/{id}/collaborators`
- ❌ `GET /docx/v1/documents/{id}/share`
- ❌ `PATCH /docx/v1/documents/{id}`
- ❌ `PUT /docx/v1/documents/{id}/share/link`

**正确 API：** `PATCH /drive/v2/permissions/:token/public?type=docx`

## 验证清单

执行完成后必须确认：
- [ ] API 返回 `code: 0`
- [ ] `link_share_entity` = `"anyone_readable"`
- [ ] `external_access_entity` = `"open"`
- [ ] 日志已记录到 `memory/feishu_permission_log.md`
- [ ] 如有外部收件人，邮件中确认"文档已设置为公开可读"

## 历史教训（2026-04-08 ~ 2026-04-13）

### 第一次犯错（2026-04-08）
- **问题：** 磁带产业调研文档，鲲哥打不开
- **根因：** 创建文档时只给内部用户加权限，没有设置链接分享
- **修复：** 调用飞书 API 设置权限
- **教训：** 飞书文档发外部人必须设置 `link_share_entity: anyone_readable`

### 第二次犯错（2026-04-12）
- **问题：** HDD 产能售罄文档，鲲哥再次打不开
- **根因：** 口头说"已设置"，实际未调用 API
- **教训：** 不能想当然，必须调用 API 并验证

### 第三次犯错（2026-04-13）
- **问题：** 同一文档，鲲哥第三次投诉
- **根因：** 重复犯错，没有建立验证机制
- **智哥批评：** "你怎么反复出这个问题"
- **修复：** 创建子代理研究正确 API，找到 v2 API
- **核心教训：**
  1. 不能想当然 — "调用 API" ≠ "成功"
  2. 必须验证 — 用 GET 请求检查返回值
  3. 建立机制 — 不能只靠"记住教训"，要固化到技能中

## 相关文件
- **技能位置：** `~/.openclaw/skills/feishu-document-permission/SKILL.md`
- **检查脚本：** `/home/harrot/.openclaw/workspace/scripts/check-feishu-permission.sh`
- **权限日志：** `/home/harrot/.openclaw/workspace/memory/feishu_permission_log.md`
- **错误记录：** `/home/harrot/.openclaw/workspace/.learnings/ERRORS.md`（2026-04-13 条目）

## 注意事项
1. **必须用 v2 API** — `/drive/v2/permissions/:token/public?type=docx`，v1 不支持 docx
2. **必须验证** — 设置后用 GET 请求检查返回值，不能假设成功
3. **必须记录** — doc_token 和权限状态记到日志，方便追溯
4. **外部用户场景** — 只有需要发给外部用户（如鲲哥）时才设置公开权限
5. **内部文档** — 如只需内部访问，不要设置公开权限

## 示例对话

**用户：** 刚创建了飞书文档，要发给鲲哥，doc_token 是 ABC123xyz
**悠悠：** 好的，我来设置文档权限为公开可读。

（调用 API 设置权限）

**悠悠：** ✅ 权限已设置成功！
- 文档链接：https://feishu.cn/docx/ABC123xyz
- 权限：获得链接的任何人可查看
- 已记录到权限日志

现在鲲哥可以打开链接查看文档了。

---

**版本：** v1.0.0（2026-04-13 创建）  
**作者：** 悠悠  
**最后更新：** 2026-04-13
