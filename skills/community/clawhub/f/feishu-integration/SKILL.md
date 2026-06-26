---
name: feishu-integration
description: 飞书开放平台完整对接方案，支持文档管理、知识库操作、文件上传、Markdown导入、消息解析、OCR识别、群欢迎机器人等功能。包含tenant_access_token自动刷新机制，所有飞书API调用统一封装。Use when: (1) 需要操作飞书文档/知识库/文件，(2) 需要导入Markdown到飞书，(3) 需要解析飞书消息（富文本/引用/图片OCR），(4) 需要获取tenant_access_token，(5) 群聊新成员欢迎，(6) 任何飞书开放平台API调用。
---

# 飞书开放平台对接 Skill

## 🆕 新增功能

### 群欢迎机器人（2026-03-08）

自动检测并欢迎飞书群聊中的新成员，支持批量@和自定义欢迎语。

**功能特性**：
- ✅ 自动检测新成员（对比群成员列表）
- ✅ 批量@功能（支持 39 人+，分批发送，每批 20 人）
- ✅ 欢迎语模板系统（8 种模板随机选择）
- ✅ 夜间模式（23:00-07:00 静默）
- ✅ 冷却机制（30 分钟内不重复欢迎）
- ✅ 分批发送逻辑

**快速使用**：
```bash
# 自动检测新成员
python3 ~/mo-hub/skills/feishu-integration/scripts/group-welcome.py \
  --chat-id oc_xxx \
  --chat-name "我的群"

# 手动欢迎指定用户（补欢迎）
python3 ~/mo-hub/skills/feishu-integration/scripts/group-welcome.py \
  --chat-id oc_xxx \
  --users ou_user1,ou_user2

# 强制发送（忽略夜间模式和冷却）
python3 ~/mo-hub/skills/feishu-integration/scripts/group-welcome.py \
  --chat-id oc_xxx \
  --force
```

**定时任务配置**（每 30 分钟检查一次）：
```bash
# 编辑 crontab
crontab -e

# 添加定时任务
*/30 * * * * python3 /root/mo-hub/skills/feishu-integration/scripts/group-welcome.py --chat-id oc_xxx --chat-name "群名"
```

### 消息解析模块（2026-03-02）

完整支持飞书消息解析，包括：
- ✅ 富文本消息（post）- 支持 Markdown、代码块、@提及、链接
- ✅ 纯文本消息（text）
- ✅ 交互式卡片（interactive）
- ✅ 图片消息 + OCR 识别（image）
- ✅ 引用回复消息

**快速使用**：
```bash
# 解析消息
source ~/mo-hub/skills/feishu-integration/scripts/feishu-auth.sh
TOKEN=$(get_feishu_token)

python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-message-parser.py \
  "$TOKEN" \
  '{"msg_type":"text","body":{"content":"{\"text\":\"Hello\"}"}}'

# OCR 识别图片
python3 ~/mo-hub/skills/feishu-integration/scripts/feishu-ocr.py \
  "img_v3_xxx" \
  "$TOKEN"
```

详细文档：[references/message-parsing.md](references/message-parsing.md)

---

## ⚠️ 重要：API 速率限制

飞书开放平台有严格的频率限制，**写入大文档时必须注意**：

| 限制类型 | 数值 | 说明 |
|---------|------|------|
| **QPS** | 5 | 每秒最多 5 次请求 |
| **日限额** | 10,000 | 每天最多 10,000 次请求 |
| **文档写入** | 需限速 | 大文档分批写入，每次请求间隔 200ms+ |

### 写入大文档的最佳实践

**❌ 错误做法（会导致内容缺失）**：
```bash
# 连续快速追加，超过 5 QPS
feishu_doc_append "TOKEN" "内容1"  # 第1秒
feishu_doc_append "TOKEN" "内容2"  # 第1秒
feishu_doc_append "TOKEN" "内容3"  # 第1秒
feishu_doc_append "TOKEN" "内容4"  # 第1秒
feishu_doc_append "TOKEN" "内容5"  # 第1秒
feishu_doc_append "TOKEN" "内容6"  # 第1秒 - 触发限流！
```

**✅ 正确做法（添加延迟）**：
```bash
# 每次追加间隔 200ms，确保不超过 5 QPS
feishu_doc_append "TOKEN" "内容1"
sleep 0.2
feishu_doc_append "TOKEN" "内容2"
sleep 0.2
feishu_doc_append "TOKEN" "内容3"
# ...
```

### 批量写入脚本示例

```bash
#!/bin/bash
# 批量写入飞书文档（带速率限制）

DOC_TOKEN="your_doc_token"
CONTENT_FILE="content.txt"  # 每行一个段落

LINE_NUM=0
while IFS= read -r line; do
    # 追加内容
    feishu_doc_append "$DOC_TOKEN" "$line"
    
    # 每5行暂停1秒（确保不超过 5 QPS）
    LINE_NUM=$((LINE_NUM + 1))
    if [ $((LINE_NUM % 5)) -eq 0 ]; then
        sleep 1
    else
        sleep 0.2  # 200ms 间隔
    fi
done < "$CONTENT_FILE"

echo "写入完成，共 $LINE_NUM 段内容"
```

### 错误码 1061045 处理

如果收到 `1061045` 错误（频率限制）：
1. 立即停止当前操作
2. 等待 1-2 秒
3. 降低请求频率后重试
4. 考虑使用 `sleep` 添加间隔

---

## 核心功能

本 Skill 封装了飞书开放平台的主要 API，提供统一的调用接口和 token 管理机制。

### 功能清单

| 功能 | API 端点 | 说明 |
|------|---------|------|
| **Token 管理** | `/auth/v3/tenant_access_token/internal` | 自动获取/刷新 |
| **文档操作** | `/docx/v1/documents/*` | 创建、读取、写入、追加 |
| **知识库** | `/wiki/v2/*` | 空间、节点管理 |
| **云空间** | `/drive/v1/files/*` | 文件上传、文件夹管理 |
| **素材上传** | `/drive/v1/medias/*` | 临时文件上传（用于导入） |
| **导入任务** | `/drive/v1/import_tasks/*` | Markdown/Word/Excel 导入 |
| **群成员管理** | `/im/v1/chats/*/members` | 获取群成员列表 |
| **消息发送** | `/im/v1/messages` | 发送富文本消息、批量@ |
| **群欢迎机器人** | - | 自动检测新成员、发送欢迎语 |

## Token 管理（核心）

### 获取 tenant_access_token

```bash
# 使用脚本获取（推荐）
source /root/mo-hub/skills/feishu-integration/scripts/feishu-auth.sh
TOKEN=$(get_feishu_token)

# 或直接调用
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_a90da2f009f8dbb3",
    "app_secret": "YOUR_SECRET"
  }'
```

### Token 有效期处理

- **有效期**: 2 小时（7200 秒）
- **自动刷新**: 使用 `feishu-auth.sh` 脚本会自动检查并刷新
- **安全存储**: Token 不硬编码，动态获取

## API 调用规范

### 标准请求格式

```bash
# GET 请求
curl -s -X GET "https://open.feishu.cn/open-apis/{API_PATH}" \
  -H "Authorization: Bearer ${TOKEN}"

# POST JSON
curl -s -X POST "https://open.feishu.cn/open-apis/{API_PATH}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{...}'

# POST FormData（文件上传）
curl -s -X POST "https://open.feishu.cn/open-apis/{API_PATH}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "param1=value1" \
  -F "file=@/path/to/file"
```

### 错误处理

| 错误码 | 含义 | 处理建议 |
|-------|------|---------|
| 0 | 成功 | - |
| 1061045 | 频率限制 | 稍后重试 |
| 1062009 | 文件大小不匹配 | 检查 size 参数 |
| 99992402 | 参数验证失败 | 检查必填字段 |
| 9499 | 参数类型错误 | 检查数据类型 |

## 常用操作速查

### 1. 文档操作

```bash
# 读取文档
feishu_doc_read "DOC_TOKEN"

# 写入文档（替换全部内容）
feishu_doc_write "DOC_TOKEN" "## 标题\n\n内容"

# 追加内容（逐个块，保证顺序）
feishu_doc_append "DOC_TOKEN" "### 新标题"
feishu_doc_append "DOC_TOKEN" "- 列表项"
```

### 2. 知识库操作

```bash
# 列出知识空间
feishu_wiki_spaces

# 列出空间节点
feishu_wiki_nodes "SPACE_ID"

# 创建文档
feishu_wiki_create_doc "SPACE_ID" "文档标题"
```

### 3. Markdown 导入

```bash
# 导入 MD 到飞书文档
feishu_import_md "/path/to/file.md" "FOLDER_TOKEN"
```

### 4. 文件上传

```bash
# 上传文件到云空间
feishu_upload_file "/path/to/file" "FOLDER_TOKEN"
```

### 5. 群欢迎机器人

```bash
# 自动检测新成员
python3 ~/mo-hub/skills/feishu-integration/scripts/group-welcome.py \
  --chat-id oc_xxx \
  --chat-name "群名称"

# 手动欢迎指定用户
python3 ~/mo-hub/skills/feishu-integration/scripts/group-welcome.py \
  --chat-id oc_xxx \
  --users ou_user1,ou_user2
```

## 扩展接口

如需添加新接口，按以下模式扩展：

```bash
# 在 scripts/feishu-api.sh 中添加
feishu_new_api() {
  local param1=$1
  local param2=$2
  
  local token=$(get_feishu_token)
  
  curl -s -X POST "https://open.feishu.cn/open-apis/NEW_API_PATH" \
    -H "Authorization: Bearer ${token}" \
    -H "Content-Type: application/json" \
    -d "{
      \"param1\": \"${param1}\",
      \"param2\": \"${param2}\"
    }"
}
```

## 配置文件

编辑 `config/feishu.env` 设置应用信息：

```bash
FEISHU_APP_ID=cli_a90da2f009f8dbb3
FEISHU_APP_SECRET=your_secret_here
```

## 参考文档

详细 API 文档见 `references/` 目录：

- [api-reference.md](references/api-reference.md) - 完整 API 参考
- [token-management.md](references/token-management.md) - Token 管理详解
- [import-workflow.md](references/import-workflow.md) - 文件导入流程

## 依赖

- `curl` - HTTP 请求
- `jq` - JSON 处理（可选，用于格式化输出）

## 安全提醒

- `app_secret` 不要提交到代码仓库
- Token 有效期 2 小时，不要长期缓存
- 敏感操作（删除、权限修改）需二次确认
