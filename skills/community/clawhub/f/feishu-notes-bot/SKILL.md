---
name: Feishu Notes Bot
slug: feishu-notes-bot
version: 1.0.0
changelog: 初始版本 - 飞书笔记机器人
description: 通过飞书机器人创建、查询和管理笔记，支持飞书消息交互和云文档同步。
homepage: https://open.feishu.cn/
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
      bins:
        - curl
    os:
      - linux
      - darwin
      - win32
---

# Feishu Notes Bot - 飞书笔记机器人

通过飞书机器人实现笔记的创建、查询和管理，支持飞书消息交互和云文档同步。

## 🎯 功能特性

### 核心功能
- 📝 **创建笔记** - 在飞书聊天中快速创建笔记
- 🔍 **搜索笔记** - 搜索本地和飞书云文档中的笔记
- 📊 **查看行动项** - 查询待办事项列表
- 📋 **会议记录** - 结构化会议笔记并同步到飞书文档
- 🔔 **消息通知** - 飞书消息提醒和推送

### 支持的笔记类型
| 类型 | 命令示例 | 存储位置 |
|------|---------|---------|
| 会议笔记 | "记录会议：项目进度会" | 飞书云文档 + 本地 |
| 快速笔记 | "记一下：明天买咖啡" | 本地 |
| 日记 | "写日记" | 本地 |
| 项目笔记 | "项目更新：A 项目进度" | 飞书云文档 |
| 行动项 | "待办：下周完成报告" | 本地 actions.md |

---

## ⚙️ 配置步骤

### 第 1 步：飞书应用配置

1. **访问飞书开放平台：**
   ```
   https://open.feishu.cn/
   ```

2. **创建企业自建应用：**
   - 登录飞书管理后台
   - 进入「开发者后台」
   - 创建企业自建应用
   - 应用名称：Notes Bot

3. **配置应用权限：**
   
   进入「权限管理」，添加以下权限：
   
   | 权限 | 权限标识 | 用途 |
   |------|---------|------|
   | 发送消息 | `im:message` | 发送笔记通知 |
   | 读取/创建文档 | `docx:docs` | 管理飞书文档 |
   | 云空间访问 | `docx:drive` | 访问云文档 |
   | 机器人功能 | `im:chat` | 群组消息交互 |
   | 知识库 | `wiki:wiki` | 知识库管理 |

4. **获取凭证：**
   - App ID（格式：`cli_xxxxxxxxxxxx`）
   - App Secret（一串加密字符）

5. **配置机器人：**
   - 进入「机器人」功能
   - 启用机器人
   - 配置回调地址（可选）

---

### 第 2 步：配置到 OpenClaw

**方法 A：使用配置文件**

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "appId": "cli_your_app_id",
          "appSecret": "your_app_secret",
          "dmPolicy": "pairing"
        }
      },
      "enabled": true
    }
  }
}
```

**方法 B：使用环境变量**

```bash
export FEISHU_APP_ID="cli_your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

---

### 第 3 步：配置笔记存储路径

编辑 `~/notes/config.md`：

```markdown
# Platform Routing
meetings: feishu-doc      # 会议笔记存飞书文档
decisions: local          # 决策记录存本地
projects: feishu-doc      # 项目笔记存飞书文档
journal: local            # 日记存本地
quick: local              # 快速笔记存本地
```

---

## 💬 飞书机器人使用方式

### 私聊机器人

在飞书中私聊 Notes Bot，发送：

```
记录会议：项目进度汇报
时间：今天下午 3 点
参会：张三、李四、王五
内容：讨论了 A 项目开发进度，决定下周上线
```

机器人会自动：
1. 创建结构化会议笔记
2. 保存到飞书云文档
3. 提取行动项
4. 返回文档链接

---

### 群聊机器人

在飞书群聊中 @Notes Bot：

```
@Notes Bot 创建会议笔记
```

机器人会引导填写会议信息。

---

### 快捷命令

| 命令 | 功能 |
|------|------|
| `/note <内容>` | 创建快速笔记 |
| `/meeting <主题>` | 创建会议笔记 |
| `/todo <任务>` | 添加行动项 |
| `/search <关键词>` | 搜索笔记 |
| `/actions` | 查看待办事项 |
| `/help` | 显示帮助 |

---

## 🔌 API 集成

### 飞书 API 基础用法

**获取访问令牌：**
```bash
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_xxx",
    "app_secret": "xxx"
  }'
```

**发送消息：**
```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "user_id",
    "msg_type": "interactive",
    "content": "{\"title\":\"笔记已创建\",\"content\":\"...\"}"
  }'
```

**创建飞书文档：**
```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "会议笔记",
    "parent_folder": "folder_id"
  }'
```

---

## 📁 文件结构

```
feishu-notes-bot/
├── SKILL.md                 # 本文件
├── scripts/
│   ├── create_note.py       # 创建笔记脚本
│   ├── sync_to_feishu.py    # 同步到飞书
│   └── send_notification.py # 发送通知
├── templates/
│   ├── meeting.md           # 会议笔记模板
│   ├── decision.md          # 决策记录模板
│   └── quick.md             # 快速笔记模板
└── config/
    ├── feishu_example.json  # 飞书配置示例
    └── routing_example.md   # 路由配置示例
```

---

## 🎯 使用场景

### 场景 1：会议记录
1. 会议中打开飞书
2. 私聊 Notes Bot 记录要点
3. 会后自动生成结构化笔记
4. 同步到飞书云文档分享给参会者

### 场景 2：待办管理
1. 随时发送待办事项
2. 自动记录到 actions.md
3. 定期推送待办提醒
4. 完成后标记状态

### 场景 3：知识沉淀
1. 项目讨论时记录决策
2. 自动分类到项目笔记
3. 同步到飞书知识库
4. 团队可搜索查阅

---

## ⚠️ 注意事项

1. **权限配置：** 确保飞书应用有文档读写权限
2. **网络访问：** 需要能访问飞书 API（国内可直连）
3. **凭证安全：** App Secret 不要公开分享
4. **速率限制：** 飞书 API 有调用频率限制

---

## 📞 故障排查

### 问题：无法发送消息
**检查：**
- 飞书应用权限是否配置
- App ID/Secret 是否正确
- 网络是否通畅

### 问题：文档创建失败
**检查：**
- 是否有 docx:docs 权限
- 父文件夹 ID 是否正确
- 文档标题是否合规

### 问题：机器人无响应
**检查：**
- 机器人是否启用
- 回调地址是否配置（如需要）
- Gateway 是否运行

---

## 🔗 相关资源

- 飞书开放平台：https://open.feishu.cn/
- 飞书 API 文档：https://open.feishu.cn/document/
- notes 技能：~/skills/notes/
- feishu-doc 技能：~/skills/feishu-doc/

---

*版本：1.0.0 | 更新时间：2026-03-04*
