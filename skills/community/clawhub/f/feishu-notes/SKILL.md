---
name: feishu-docs
description: Read, write, and manage Feishu (飞书) documents via the Open API. Supports creating documents, reading content, appending text, and auto-refreshing OAuth tokens. Documents are created in the user's personal cloud drive under a designated folder.
metadata:
  openclaw:
    emoji: "📄"
    requires: {}
    install:
      - id: setup
        kind: manual
        label: "飞书开放平台配置"
        steps:
          - "访问 https://open.feishu.cn → 创建企业自建应用"
          - "获取 App ID + App Secret"
          - "添加权限：drive:drive（云盘完全读写）+ docx:document（文档读写）"
          - "配置重定向 URL：https://open.feishu.cn/cli/callback"
          - "发布版本并授权到企业"
---

# Feishu Docs Skill

飞书文档读写工具。支持在用户的个人云盘内创建、读取、写入文档，自动管理 OAuth 续期。

## 🚀 快速开始（5 分钟）

跟着这 7 步走，小白也能配置好。

---

### 第 1 步：创建飞书应用

1. 打开 https://open.feishu.cn → 点击 **创建企业自建应用**
2. 取个名字，比如 `My Notes`，点确定
3. 创建成功后，在 **凭证与基础信息** 里找到 **App ID** 和 **App Secret**，复制下来

---

### 第 2 步：开通权限

左侧菜单 → **权限管理** → 搜索并添加 2 个权限：

| 权限名称 | 搜索关键词 |
|---|---|
| `drive:drive`（云盘完全读写） | 搜索 `drive` |
| `docx:document`（文档读写） | 搜索 `docx` |

勾选后点 **批量开通**。

---

### 第 3 步：设置重定向 URL

左侧菜单 → **安全设置** → **重定向 URL** → 添加：

```
https://open.feishu.cn/cli/callback
```

---

### 第 4 步：保存凭证到本地

打开终端，执行以下命令（换成你自己的 App ID 和 Secret）：

```bash
echo 'FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxxxxxx' >> ~/.openclaw/.feishu_env
echo 'FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxx' >> ~/.openclaw/.feishu_env
chmod 600 ~/.openclaw/.feishu_env
```

---

### 第 5 步：修改文件夹 ID（可选）

如果你想把笔记归纳到指定文件夹：

1. 打开飞书云盘 → 新建一个文件夹（比如 `Ace笔记`）
2. 进入文件夹 → 复制浏览器地址栏末尾的那串 ID（类似 `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
3. 编辑 `scripts/feishu_docs.py`，找到 `ACE_FOLDER_TOKEN` 换成你的文件夹 ID

> 不改也没关系，文档会默认创建在云盘根目录。

---

### 第 6 步：发布应用并授权

1. 回到飞书开发者后台 → **版本管理与发布** → 创建版本（版本号写 `1.0.0`）→ 提交审核
2. 审核通过后，打开飞书 → **工作台** → 搜索你的应用 → 点击 **安装**

---

### 第 7 步：授权你的账号

先加载凭证，然后运行授权命令：

```bash
source ~/.openclaw/.feishu_env
cd ~/.openclaw/workspace
python3 scripts/feishu_docs.py token
```

终端会输出一个链接 → 浏览器打开它 → 扫码登录飞书 → 授权后会跳转 → 地址栏 `?code=xxx` 那串复制下来 → 粘贴到终端回车。

看到 `Token 刷新成功！` 就搞定了。

### ✅ 测试

```bash
source ~/.openclaw/.feishu_env
cd ~/.openclaw/workspace
python3 scripts/feishu_docs.py create "Hello World"
```

返回一个飞书链接，点开能看到文档 → 配置成功 🎉

---

## 使用方式

### 支持的脚本操作

```bash
python3 scripts/feishu_docs.py list                    # 列出云盘最近文档
python3 scripts/feishu_docs.py read <doc_id>           # 读取文档内容
python3 scripts/feishu_docs.py create <title>          # 创建文档
python3 scripts/feishu_docs.py write <doc_id> <text>        # 追加文本段落
python3 scripts/feishu_docs.py bold <doc_id> <text>         # 追加加粗文本
python3 scripts/feishu_docs.py heading <doc_id> <text> [level=2]  # 追加标题（level=2为H2，3为H3）
python3 scripts/feishu_docs.py token                   # 查看/刷新 token 状态
python3 scripts/feishu_docs.py code <doc_id> <text>    # 追加代码块（纯文本，不带 style 字段）
python3 scripts/feishu_docs.py image <doc_id> <url>    # 从网址插入图片
```

### 通过 Agent 使用

安装此 Skill 后，你的 Agent 可以理解这些指令：

```
"记到飞书：今天的会议纪要写了xxx"
"把上周的分析报告追加到笔记里"
"帮我创建一篇周报笔记"
"读取笔记内容给我看看"
"把这张截图插进文档"
```

Agent 会自动完成创建文档、格式化内容、插入图片等操作。

---

## 前置条件（详细版）

### 飞书应用配置

使用前需要完成一次性的飞书开放平台配置：

1. **创建应用**：访问 https://open.feishu.cn → 创建企业自建应用
2. **获取凭证**：应用详情 → 凭证与基础信息 → 记录 App ID 和 App Secret
3. **开通权限**（应用身份权限 + 用户身份权限）：
   - `drive:drive` — 云盘完全读写
   - `docx:document` — 文档读写
4. **配置安全设置**：重定向 URL 添加 `https://open.feishu.cn/cli/callback`
5. **发布版本**：创建版本号（如 1.0.0）并提交审批
6. **企业授权**：飞书管理后台 → 工作台 → 应用管理 → 安装并授权

### 凭证配置

将 App ID 和 App Secret 存入环境变量或配置文件：

```bash
# 方式一：环境变量
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"

# 方式二：配置文件（推荐，chmod 600）
echo 'FEISHU_APP_ID=your_app_id' >> ~/.openclaw/.feishu_env
echo 'FEISHU_APP_SECRET=your_app_secret' >> ~/.openclaw/.feishu_env
chmod 600 ~/.openclaw/.feishu_env
```

### OAuth 授权

用户需通过 OAuth 授权获取 `user_access_token`，使文档创建在个人云盘：

1. 生成授权链接（由工具自动生成或手动拼接）
2. 用户点击链接 → 飞书登录授权
3. 授权成功后复制跳转链接中的 `code` 参数
4. 工具自动换取 `access_token` + `refresh_token`

## 权限与安全规则

- **文件夹范围**：仅限指定的文件夹内操作（通过 `FEISHU_FOLDER_TOKEN` 环境变量配置）
- **禁止操作**：不可查看/编辑/移动/删除指定文件夹以外的文档
- **删除保护**：删除文档需获得用户明确确认
- **多笔记**：不同题材可在文件夹下创建多篇笔记

## 涉及的飞书 API

| 端点 | 用途 |
|---|---|
| `POST /auth/v3/tenant_access_token/internal` | 获取应用 Token |
| `POST /authen/v1/access_token` | OAuth 换取用户 Token |
| `POST /authen/v1/refresh_access_token` | 刷新用户 Token |
| `POST /docx/v1/documents` | 创建文档 |
| `GET /docx/v1/documents/:id/blocks/:id` | 读取文档标题 |
| `GET /docx/v1/documents/:id/blocks/:id/children` | 读取文档内容（分页） |
| `POST /docx/v1/documents/:id/blocks/:id/children` | 追加内容块 |
| `DELETE /drive/v1/files/:id?type=docx` | 删除文档 |
| `POST /drive/v1/files/:id/move` | 移动文档到文件夹 |

## 文档格式化规范

### 标题体系

```
H1 = 日期（当天笔记标题）
H2 = 数字序号 + 独立内容标题
H3 = 内容内短标题
```

### 内容格式

- CLI 命令/代码 → 飞书代码块（block_type=14），注意不要加 `style` 字段，API 会拒绝
- 步骤流程 → 编号列表（1. 2. 3.）
- Emoji 仅用于以下场景：

  | Emoji | 场景 |
  |---|---|
  | ⚠️ | 注意事项、警告 |
  | 💡 | 重点提示、诀窍 |
  | ✅ | 完成状态 |
  | 🔒 | 安全相关 |
  | 🚀 / ✨ | 标题或里程碑 |

- **加粗**：关键术语、重要结论、核心数字 — 使用 `text_element_style.bold: true`
- 🔴 **颜色标签**：H3 标题前可用颜色 emoji 区分模块，正文中红色/橙色用于警示性重点
- `行内代码`：文件名、命令、参数、API 端点 — 使用 `text_element_style.inline_code: true`

### 表格规范

- 首行表头自动加粗（bold=True）
- 每格仅含一个文本块，无多余空行
- 行数列数无限制，超大表格（50行+）创建前会警示
- 创建方式：block_type=31，使用 PATCH 更新单元格内容

### 图片插入（3 步流程）

飞书 Docx API 不支持一步创建带图的图片块，需分三步：

1. **创建空图片块** — POST children，image: {} 必须为空对象
2. **上传图片** — upload_all，parent_node 设为图片块 ID
3. **PATCH 绑定** — replace_image 传入原始 file_token

注意事项：
- 不需要 image/ 前缀，用原始 file_token 即可
- upload 的 parent_node 是图片块 ID，不是文档 ID
- file_token 字段在 create 时 API 接受但不存储
- token 字段在 create 时直接报 invalid param
