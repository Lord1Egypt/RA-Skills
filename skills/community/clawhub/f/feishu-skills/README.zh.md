中文 | [English](README.md)

# feishu-skills

适用于 [OpenClaw](https://github.com/openclaw/openclaw) 和 [EnClaws](https://github.com/hashSTACS-Global/EnClaws) 的完整飞书集成技能包。

让 AI Agent 能够读写飞书文档、发送消息、管理日历、任务和多维表格 —— 全部基于**用户个人 OAuth Token**（而非 Bot Owner 权限），无需管理员授权。

---

## 30 秒接入飞书

> **告别手动创建应用。** 飞书扫一次码，Bot 自动创建并配置完成。

安装技能包后，只需对 Agent 说：

```
帮我配置飞书插件
```

Agent 会生成一个二维码链接 → 你用飞书扫码确认 → Bot 凭据自动写入 OpenClaw 配置。搞定。

详见 [feishu-quick-setup](#包含的技能)。

---

## 安装

```bash
git clone https://github.com/hashSTACS-Global/feishu-skills.git
cd feishu-skills
node install.js
```

---

## 包含的技能

| 技能 | 说明 |
|---|---|
| **feishu-quick-setup** | 一键配置飞书插件 —— 扫码自动创建 Bot 并写入 OpenClaw 配置 |
| **feishu-auth** | OAuth Device Flow 授权中枢，被所有其他技能共享 |
| **feishu-create-doc** | 使用 Markdown 内容创建飞书云文档 |
| **feishu-fetch-doc** | 读取飞书云文档 / Wiki 页面 |
| **feishu-search-doc** | 搜索云文档、知识库空间/节点，或在云盘目录下按名称筛选 |
| **feishu-update-doc** | 更新飞书云文档（追加或覆盖内容块） |
| **feishu-im-read** | 读取飞书 IM 聊天记录 |
| **feishu-chat** | 搜索群组、获取群详情、列出群成员 |
| **feishu-calendar** | 创建 / 查询 / 更新日历事件 |
| **feishu-task** | 创建 / 查询 / 更新任务和任务清单 |
| **feishu-bitable** | 多维表格应用、数据表、字段、记录、视图的完整增删改查 |
| **feishu-docx-download** | 下载飞书 Wiki 中的附件文件并提取正文文本，支持 docx/pdf/pptx/xlsx/xls/html/rtf/epub/txt/csv 等格式 |
| **feishu-drive** | 云盘文件夹操作（当前支持列出目录、创建文件夹） |
| **feishu-image-ocr** | 通用图片 OCR 文字识别，调用飞书 OCR API，支持中英文混排，纯 Node.js 实现，零额外依赖 |
| **feishu-search-user** | 按关键词模糊搜索用户、获取当前用户自己的信息、按 `user_id` / `union_id` 精确查询指定用户 |
| **feishu-sheet** | 飞书电子表格（Sheets）读写工具，支持 info / read / write / append / find / create / export |
| **feishu-wiki** | 飞书知识库管理，支持知识空间增删查，以及节点增删查/移动/复制 |

---

## 环境要求

- **Node.js** ≥ 18（使用内置 `fetch`）
- 已安装 **[OpenClaw](https://github.com/openclaw/openclaw)** 或 **[EnClaws](https://github.com/hashSTACS-Global/EnClaws)**
- 一个飞书应用，并开通以下权限（详见[配置](#配置)）：
  - `docs:doc`、`wiki:wiki:readonly`、`drive:drive`
  - `im:message`、`im:message:readonly`
  - `calendar:calendar`
  - `task:task`
  - `bitable:app`

---

## 配置

### OpenClaw

在 `~/.openclaw/openclaw.json` 中添加 `channels.feishu` 配置：

```json
{
  "channels": {
    "feishu": {
      "appId": "cli_xxxxxxxxxxxxxxxx",
      "appSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  },
  "tools": {
    "deny": [
      "feishu_doc",
      "feishu_create_doc",
      "feishu_fetch_doc",
      "feishu_update_doc",
      "feishu_wiki",
      "feishu_wiki_*",
      "feishu_drive_*",
      "feishu_search_doc_wiki",
      "feishu_chat",
      "feishu_chat_members",
      "feishu_im_*",
      "feishu_bitable_*",
      "feishu_calendar_*",
      "feishu_task_*",
      "feishu_pre_auth"
    ],
    "exec": {
      "security": "full",
      "ask": "off"
    }
  }
}
```

> **⚠️ 重要：`tools` 必须放在顶层，不能放在 `channels.feishu` 内部。**
> OpenClaw 的 `channels.feishu.tools` 使用的是另一套 schema（仅支持布尔开关），将 `deny` 放在那里会被**静默忽略**，导致内置插件工具仍然激活，Agent 会跳过本技能包。

> **为什么需要 `tools.deny`？** OpenClaw 内置了飞书插件工具（`feishu_doc` 等）。本技能包以更丰富的用户级 OAuth 版本替代了这些工具。禁用内置工具可确保 Agent 优先使用本技能包。

> **为什么需要 `tools.exec`？** 本技能包通过 `exec` 工具执行 Node.js 脚本。如果不配置 `"security": "full"` 和 `"ask": "off"`，exec 工具可能被限制或每次执行都需手动确认。

### EnClaws

凭据通过环境变量（`FEISHU_APP_ID`、`FEISHU_APP_SECRET`）自动注入，无需手动配置。

---

## 认证流程

本技能包使用 **飞书 OAuth Device Flow** —— 每个用户只需授权一次，Token 保存在本地 `feishu-auth/.tokens/<open_id>/`。

**首次使用流程：**
1. 用户向 Agent 发起请求（如：创建文档）
2. 脚本返回 `{"error": "auth_required"}` 并附带授权链接
3. Agent 向用户展示授权卡片/链接
4. 用户点击并在飞书中完成授权
5. Agent 自动重试原始操作
6. Token 保存后，后续调用对用户完全透明

**Token 生命周期：**
- Access Token 通过 Refresh Token 自动续期，无需重新授权
- Token 按用户（`open_id`）和应用（`appId`）分别存储
- 仅在 Refresh Token 过期时（约 30 天不活跃）需要重新授权

---

## 凭据解析优先级

脚本按以下顺序查找应用凭据：

1. **环境变量** `FEISHU_APP_ID` + `FEISHU_APP_SECRET` ← EnClaws 自动注入
2. **`feishu-auth/config.json`** ← 手动单应用配置
3. **`~/.openclaw/openclaw.json`** → `channels.feishu.appId/appSecret` ← OpenClaw 标准配置

---

## 使用示例

安装完成后，直接用自然语言与 Agent 对话：

```
帮我创建一个飞书文档，标题"Q1 OKR"，内容是...
读一下这个飞书文档：https://xxx.feishu.cn/docx/...
查看我今天的日程
帮我创建一个任务：明天下午3点前提交报告
在这个多维表格里新增一条记录：...
帮我下载这个飞书 Wiki 附件并告诉我里面写了什么：https://xxx.feishu.cn/wiki/...
```

---

## 项目结构

```
feishu-skills/
├── feishu-auth/              # 授权中枢（所有技能共享）
│   ├── SKILL.md
│   ├── auth.js               # Device Flow 发起 + 轮询
│   └── token-utils.js        # Token 读写/刷新工具函数
├── feishu-create-doc/
│   ├── SKILL.md
│   └── create-doc.js
├── feishu-fetch-doc/
│   ├── SKILL.md
│   └── fetch-doc.js
├── feishu-search-doc/
│   ├── SKILL.md
│   └── search-doc.js
├── feishu-update-doc/
│   ├── SKILL.md
│   └── update-doc.js
├── feishu-im-read/
│   ├── SKILL.md
│   └── im-read.js
├── feishu-chat/
│   ├── SKILL.md
│   └── chat.js
├── feishu-calendar/
│   ├── SKILL.md
│   └── calendar.js
├── feishu-task/
│   ├── SKILL.md
│   └── task.js
├── feishu-bitable/
│   ├── SKILL.md
│   └── bitable.js
├── feishu-docx-download/
│   ├── SKILL.md
│   ├── download-doc.js
│   └── extract.js
├── feishu-drive/
│   ├── SKILL.md
│   └── drive.js
├── feishu-image-ocr/
│   ├── SKILL.md
│   └── ocr.js                # 飞书 OCR API 调用
├── feishu-search-user/
│   ├── SKILL.md
│   └── search-user.js        # 按姓名搜索飞书用户
├── feishu-sheet/
│   ├── SKILL.md
│   └── sheet.js              # 电子表格读写/查找/创建/导出
├── feishu-wiki/
│   ├── SKILL.md
│   └── wiki.js               # 知识库空间与节点管理
└── install.js                # 跨平台安装脚本
```

---

## 兼容性

| 运行环境 | 状态 |
|---|---|
| [OpenClaw](https://github.com/openclaw/openclaw)（原版） | ✅ 完全支持 |
| [EnClaws](https://github.com/hashSTACS-Global/EnClaws) | ✅ 完全支持 |
| macOS | ✅ |
| Linux | ✅ |
| Windows | ✅ |

