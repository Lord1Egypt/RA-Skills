---
name: feishu-log
description: 飞书日志记录 - 用户主动提供日志内容，智能整理、结构化、层次化后写入飞书文档，不使用固定模板。使用场景：(1) 会议记录，(2) 项目日志，(3) 工作复盘，(4) 重要事件记录
metadata:
  openclaw:
    emoji: 📝
    requires:
      bins: ["node", "curl", "jq"]
---

# 飞书日志记录技能

## 📖 功能

用户主动提供日志内容，**智能整理、结构化、层次化后写入飞书文档**：
- ✅ 接收用户提供的日志内容（文本、会议记录、事件描述等）
- ✅ **不使用固定模板，根据内容智能整理**
- ✅ 结构化层次化组织内容（保留所有关键细节）
- ✅ 使用飞书原生块格式（Block-based）写入内容
- ✅ 创建飞书云盘文件夹（**日志/XX 年/XX 月/XX 日/log/**）
- ✅ 创建飞书在线文档（主题 + 时间戳）
- ✅ 自动跳过已存在的文件夹（复用已有文件夹）
- ✅ 同一天可以有多个文件
- ✅ **添加用户为协作者（full_access 权限）**

## 🎯 使用场景

- **会议记录** - 记录会议内容、决策、行动项
- **项目日志** - 记录项目进展、里程碑、问题
- **工作复盘** - 记录每日/每周工作总结
- **重要事件** - 记录关键决策、客户沟通、突发事件
- **学习笔记** - 记录培训内容、技术分享

## 🔧 使用方式

### 方式 1: 对话中使用（推荐）

用户直接提供日志内容，例如：

```
请记录今天的会议内容：
- 会议主题：[主题名称]
- 时间：[日期和时间]
- 参会人员：[人员名单]
- 主要内容：[讨论要点]
- 决策事项：[达成的决策]
- 下一步：[行动计划]
```

```
帮我记录项目进展：
- 项目名称：[项目名称]
- 当前阶段：[项目阶段]
- 已完成：[完成的工作]
- 遇到问题：[遇到的挑战]
- 下一步计划：[后续安排]
```

```
记录今天的工作：
- 完成的工作项 1
- 完成的工作项 2
- 参加的会议
- 遇到的问题和解决方案
```

## 📋 工作流程

### 步骤 1: 接收并理解内容
- 阅读用户提供的全部内容
- 理解内容主题和关键信息
- 识别内容类型（会议/项目/工作/其他）

### 步骤 2: 智能整理与结构化
**不使用固定模板**，而是：
1. **提取关键信息**
   - 时间、地点、人员
   - 主题、背景、目标
   - 关键决策、行动项

2. **层次化组织**
   - 按逻辑关系组织内容
   - 使用合适的标题层级（H1/H2/H3）
   - 相关事项归类到同一章节

3. **保留所有细节**
   - 不丢失用户提供的任何重要信息
   - 保持原始表述的准确性
   - 补充必要的上下文

### 步骤 3: 确认当前日期
- 获取当前日期（年 - 月-日）
- 用于文件夹命名和文档标题

### 步骤 4: 创建/复用文件夹结构
```
飞书云盘/
└── 日志/
    └── 2026 年/
        └── 03 月/
            └── 04 日/
                └── log/
                    ├── 2026-03-04 华为会议.docx
                    └── 2026-03-04 信誉库节点网络配置.docx
```

**逻辑**:
1. 检查"日志"文件夹是否存在 → 不存在则创建
2. 检查"2026 年"文件夹是否存在 → 不存在则创建
3. 检查"03 月"文件夹是否存在 → 不存在则创建
4. 检查"04 日"文件夹是否存在 → 不存在则创建
5. 检查"log"文件夹是否存在 → 不存在则创建
6. **已存在的文件夹直接复用**
7. **添加用户为所有文件夹的协作者（full_access）**

### 步骤 5: 创建文档
- 文档标题格式：`YYYY-MM-DD 主题`
- 同一天可以有多个文件（不同主题）
- **添加用户为协作者（full_access 权限）**

### 步骤 6: 写入内容（飞书块格式）
使用飞书原生块格式写入**结构化后的内容**：
- **文本块**（block_type: 2）- 普通段落
- **标题块**（block_type: 3/4/5）- H1/H2/H3 标题
- **列表块**（block_type: 12）- 无序列表
- **表格块**（简化处理）- 数据表格
- **引用块**（block_type: 14）- 引用内容
- **分割线**（block_type: 6）- 视觉分隔

## 🔐 所需权限

### 应用身份权限（使用 tenant_access_token）

**重要**：本技能使用 **`tenant_access_token`**（应用级令牌），无需用户授权即可使用。

| 权限 | 说明 |
|------|------|
| `drive:drive` | 查看、评论、编辑和管理云空间中所有文件 |
| `drive:file` | 上传、下载文件到云空间 |
| `docx:document` | 创建及编辑新版文档 |
| `space:folder:create` | 创建云空间文件夹 |
| `docs:permission.member:add` | 添加协作者权限 |

### 权限申请链接
```
https://open.feishu.cn/app/YOUR_APP_ID/auth?q=drive:drive,drive:file,docx:document,space:folder:create,docs:permission.member:add
```

### Token 获取方式

技能自动使用 `tenant_access_token`，无需手动配置：

```javascript
// 内部实现：使用 APP_ID 和 APP_SECRET 获取 tenant_access_token
async function getTenantToken() {
  const result = await httpRequest('POST', '/auth/v3/tenant_access_token/internal/', {
    body: { app_id: CONFIG.APP_ID, app_secret: CONFIG.APP_SECRET }
  });
  return result.tenant_access_token;
}
```

**Token 有效期**：2 小时（自动刷新）

## ⚠️ 配置参数

**重要说明**：本技能使用 **`tenant_access_token`**（应用级令牌），所有配置通过环境变量设置。

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `FEISHU_APP_ID` | 飞书应用 ID | 必填（从.env 文件加载） |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | 必填（从.env 文件加载） |
| `DEFAULT_OWNER_ID` | 协作者 user_id（用户的 open_id） | 必填（从.env 文件加载） |
| `ROOT_LOG_FOLDER_NAME` | 日志根文件夹名称 | 可选，默认：工作日志 |

### 环境变量设置方式

**方式 1：在 `.env` 文件中配置（推荐）**
```bash
# ~/.openclaw/workspace/.env
FEISHU_APP_ID="your_app_id"
FEISHU_APP_SECRET="your_app_secret"
DEFAULT_OWNER_ID="your_open_id"
ROOT_LOG_FOLDER_NAME="工作日志"
```

**方式 2：在 Shell 中导出**
```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
export DEFAULT_OWNER_ID="your_open_id"
```

## 🔑 如何获取 Open ID

### 方法 1: 通过 API 获取
```bash
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}' | jq -r '.tenant_access_token')

curl -s "https://open.feishu.cn/open-apis/contact/v3/users?user_id_type=open_id&page_size=10" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.items[] | {open_id, user_id}'
```

### 方法 2: 从消息事件中获取
消息 payload 中的 `sender.open_id`

### 方法 3: 从飞书开发者后台查看
应用管理 > 权限管理 > 已授权用户

---

## 📊 输出结果

成功时返回：
```json
{
  "success": true,
  "date": "2026-03-04",
  "title": "华为会议记录",
  "folder": {
    "root": "日志",
    "year": "2026 年",
    "month": "03 月",
    "day": "04 日",
    "subfolder": "log",
    "token": "fld_xxx"
  },
  "document": {
    "title": "2026-03-04 华为会议记录",
    "document_id": "doxxx",
    "url": "https://feishu.cn/docx/doxxx",
    "existed": false,
    "permission_added": true
  },
  "permissions": {
    "folders_checked": 5,
    "user_has_full_access": true
  }
}
```

## ⚠️ 重要注意事项

### 🔑 使用 tenant_access_token（重要）

**本技能使用 `tenant_access_token`（应用级令牌），而非 `user_access_token`。**

**优势**：
- ✅ 无需用户授权，应用自动获取
- ✅ 有效期 2 小时，自动刷新
- ✅ 权限范围：应用级别权限
- ✅ 安全性更高，不依赖用户会话

**工作流程**：
```
环境变量 (FEISHU_APP_ID, FEISHU_APP_SECRET)
    ↓
getTenantToken() 获取 tenant_access_token
    ↓
所有 API 调用使用该 token
    ↓
飞书 API 返回结果
```

### `feishu_doc` 工具的 `create` 动作限制

**问题**: `feishu_doc` 的 `create` 动作**不支持 `content` 参数**，只会创建空文档。

**正确用法**:
```javascript
// ❌ 错误：create 不会写入内容
feishu_doc action=create title="文档标题" content="..."

// ✅ 正确：先 create 再 write
feishu_doc action=create title="文档标题"
feishu_doc action=write doc_token="<document_id>" content="..."
```

**修复方案**:
1. 使用 `create` 创建文档，获取 `document_id`
2. 使用 `write` 写入内容到该文档
3. 或者直接使用 `write` 到已有文档

## 🐛 常见错误

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 99991400 | 应用频率限制 | 降低调用频率 |
| 1310213 | 权限不足 | 检查文件夹访问权限 |
| 1061004 | 禁止访问 | 确认应用权限配置 |
| 99991661 | 缺少 access token | 重新获取 token |
| 1770001 | 参数无效 | 检查块格式 |
| **文档内容为空** | **create 动作不处理 content** | **改用 create + write 组合** |

## ✅ 已修复问题

| 问题 | 状态 | 说明 |
|------|------|------|
| 有序列表块格式错误 | ✅ 已修复 | 改为使用文本块渲染 |
| 内容写入失败 | ✅ 已修复 | 优化块解析器 |
| 权限管理 | ✅ 正常 | 添加用户为协作者（full_access） |
| 文件夹复用 | ✅ 正常 | 已存在的文件夹直接复用 |
| **固定模板限制** | ✅ 已移除 | **改为智能整理内容** |

## 💡 最佳实践

1. **提供充足信息** - 用户输入越详细，整理效果越好
2. **保留原始细节** - 结构化时不丢失关键信息
3. **层次化组织** - 按逻辑关系组织内容
4. **文件夹复用** - 已存在的文件夹不重复创建
5. **权限检查** - 确保用户在所有文件夹中是协作者
6. **同天多文件** - 同一天的不同主题创建不同文档
7. **标题清晰** - 文档标题包含日期和主题，便于检索

## 📁 文件夹结构说明

### 目录层级
```
飞书云盘/
└── 日志/                    # 根文件夹
    └── 2026 年/              # 年份文件夹
        └── 03 月/            # 月份文件夹
            └── 04 日/        # 日期文件夹
                └── log/      # 日志子文件夹
                    ├── 2026-03-04 华为会议.docx
                    └── 2026-03-04 项目进展.docx
```

### 命名规范
- **年份文件夹**: `YYYY 年`
- **月份文件夹**: `MM 月`
- **日期文件夹**: `DD 日`
- **日志子文件夹**: `log`
- **文档标题**: `YYYY-MM-DD 主题`

## 🔑 权限管理说明

### 权限方案：协作者方式
- 机器人保持资源所有权
- 用户获得 `full_access` 权限（可管理）
- 用户可以查看、编辑、删除、分享
- 无需转移所有权

### 添加协作者 API
```http
POST https://open.feishu.cn/open-apis/drive/v1/permissions/:token/members
Content-Type: application/json
Authorization: Bearer {tenant_access_token}

{
  "member_type": "openid",
  "member_id": "ou_xxx",
  "perm": "full_access"
}
```

**请求参数**:
| 参数 | 说明 |
|------|------|
| `member_type` | `"openid"` |
| `member_id` | 用户的 open_id |
| `perm` | `full_access`（可管理） |

**URL 参数**:
| 参数 | 说明 |
|------|------|
| `type` | 资源类型（folder/docx） |

### 权限级别说明
| 权限级别 | 可执行操作 |
|---------|-----------|
| `full_access` | 查看、编辑、删除、分享、添加协作者 |
| `edit` | 查看、编辑、评论 |
| `view` | 查看、评论 |

---

## 🤖 AI 处理指令

当用户请求记录日志时，按以下流程处理：

### 1. 理解内容
- 仔细阅读用户提供的内容
- 识别关键信息（时间、人员、主题、事项等）
- 理解内容的逻辑结构

### 2. 智能整理（不使用模板）
**根据内容特点进行整理**：
- 提取并突出关键信息
- 按逻辑关系组织章节
- 相关内容归类到同一部分
- 使用合适的标题层级
- **不套用固定模板**

### 3. 结构化示例

**示例 1：会议记录**
```markdown
# 2026-03-04 华为会议

## 📋 会议信息
- 时间：2026-03-04 上午
- 参会方：华为
- 主题：信誉库节点网络配置

## 💬 讨论内容
[根据实际讨论内容整理]

## ✅ 决策事项
[提取的决策]

## 📌 下一步
[行动项]
```

**示例 2：项目进展**
```markdown
# 2026-03-04 项目进展

## 📊 当前状态
[项目状态]

## ✅ 已完成
[完成的工作]

## ⚠️ 问题与挑战
[遇到的问题]

## 📋 下一步计划
[后续安排]
```

### 4. 确认日期
- 获取当前日期
- 用于文件夹路径和文档标题

### 5. 文件夹操作
- 创建/获取：`日志` → `YYYY 年` → `MM 月` → `DD 日` → `log`
- 已存在则复用
- 添加用户为所有文件夹的协作者

### 6. 文档操作
- 创建文档（标题：`YYYY-MM-DD 主题`）
- 写入结构化内容
- 添加用户为协作者

### 7. 反馈确认
- 告知用户文档已创建
- 提供文档链接
- 确认用户拥有完整权限

---

**技能位置**: `~/.openclaw/workspace/skills/feishu-log/`
