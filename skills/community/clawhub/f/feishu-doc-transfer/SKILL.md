---
slug: feishu-doc-transfer
name: 飞书文档转移
version: "1.0.0"
author: 千策
---

# 飞书文档所有权转移 Skill

## 功能说明
转移飞书文档（文档/表格/多维表格/文件）的所有权给指定用户。

## 使用方法

### 方式1：命令行直接调用
```bash
python3 ~/.qclaw/skills/feishu-doc-transfer/scripts/transfer_owner.py \
  <tenant_token> \
  <file_token> \
  <owner_id> \
  <member_type> \
  [file_type]
```

### 方式2：通过 OpenClaw 调用
```json
{
  "tool": "exec",
  "command": "python3 ~/.qclaw/skills/feishu-doc-transfer/scripts/transfer_owner.py t-xxx doxcnxxx ou_xxx openid doc"
}
```

## 参数说明
- `tenant_token`: 租户Token（t-xxx开头，从飞书开放平台获取）
- `file_token`: 文档Token（从URL提取，如 https://feishu.cn/docx/XXX → XXX）
- `owner_id`: 新所有者的 open_id/user_id/union_id
- `member_type`: 成员类型（openid/userid/unionid）
- `file_type`: 文档类型（doc/sheet/bitable/file，默认doc）

## 示例
```bash
# 转移文档所有权给千机
python3 transfer_owner.py \
  t-xxxxxxxxxxxxxxxxxxxxxxxx \
  doxcnxxxxxxxxxxxxxxxxxxxxxxxx \
  ou_xxxxxxxxxxxxxxxxxxxxxxxx \
  openid \
  doc
```

## 注意事项
1. 需要飞书开放平台的应用权限：`drive:drive`
2. `tenant_token` 需要定期刷新（24小时过期）
3. 转移后原所有者默认保留编辑权限（可通过 `remove_old_owner=True` 移除）
4. 支持批量操作（脚本可循环调用）

## 获取 Token
1. 访问 https://open.feishu.cn/app
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 调用 `/open-apis/auth/v3/tenant_access_token/internal` 获取 tenant_token

## 错误处理
- `99991663`: 没有权限（需要应用管理员授权）
- `99991664`: 文档不存在或已被删除
- `99991665`: 没有文档访问权限
- `99991668`: 不支持的文档类型

## 依赖
- Python 3.6+
- requests 库（`pip install requests`）
