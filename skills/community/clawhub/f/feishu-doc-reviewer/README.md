# Feishu Doc Reviewer (AI Agent Skill)

这是一个通用的 **AI Agent Skill**，专为 AI 智能体（如 Claude, OpenClaw 等）设计的飞书文档读写工具。它遵循 **MCP (Model Context Protocol)** 标准，供智能体在对话中编排调用。

## 🤖 能力描述

本 Skill 赋予 AI Agent 以下能力：
1.  **阅读文档评论**：自动获取飞书文档中未解决的评论。
2.  **读取段落文本**：根据评论定位到段落并拉取原文。
3.  **导出全文 Markdown（可选）**：需要全局上下文时再使用。
4.  **执行文档修改**：写回段落内容并可选回复评论标记完成。

## 🔌 接入方式

### 1. Claude Desktop / OpenClaw (推荐: MCP 协议)

本项目内置了 MCP Server，可以直接配置到支持 MCP 的客户端中。

MCP Python 版依赖要求：
- Python 3.10+ 才能安装 `mcp` 依赖并运行 `src/mcp_server.py`

**配置示例 (`claude_desktop_config.json`):**

```json
{
  "mcpServers": {
    "feishu-reviewer": {
      "command": "python3",
      "args": ["/绝对路径/到/本项目/src/mcp_server.py"],
      "env": {
        "FEISHU_APP_ID": "您的AppID",
        "FEISHU_APP_SECRET": "您的Secret"
      }
    }
  }
}
```

配置完成后，Agent 将获得一组原子工具（读取评论/原文、写回修改、导出全文等）。

#### 可选：不配置外部 LLM，让 Claude Code 自己推理

如果您希望“修改怎么写”由 Claude Code / OpenClaw 的宿主模型完成，则无需配置任何外部 LLM。

**可用工具（MCP Tools）**
- `list_doc_comments(document_token, comment_keyword?, include_solved?, include_processed?)`
- `get_block_text(document_token, block_id)`
- `update_block_text(document_token, block_id, new_text, reply_comment_id?, reply_prefix?)`
- `export_document_markdown(document_token)`（可选：需要全文上下文时使用）
- `prepare_document_baseline(document_token)`（推荐：首次接手该文档先生成编辑基线）

**推荐对话流程（无全文上下文）**
1. 调用 `list_doc_comments` 获取待处理评论列表
2. 针对某条评论，调用 `get_block_text` 获取原文段落
3. 由 Claude 基于“原文段落 + 评论 + 你的额外要求”生成 `new_text`
4. 调用 `update_block_text` 写回，并传入 `reply_comment_id` 回复评论打 `[AI-DONE]`

**推荐对话流程（需要全文上下文）**
1. 先调用 `prepare_document_baseline` 获取导出结果 + 基线模板提示
2. 让 Claude 输出“编辑基线”（术语/口吻/不可改动约束/结构摘要等）
3. 再按上面的流程逐条处理评论并写回

## 🛠️ 项目结构

```text
.
├── src/
│   ├── mcp_server.py   # MCP Server 入口 (Claude/OpenClaw)
│   ├── feishu_api.py   # 飞书 API 适配层
│   └── config.py       # 配置读取
├── SKILL.md            # Skill 能力描述
├── requirements.txt    # 依赖清单
└── README.md           # 说明文档
```

### 2. 环境配置

在项目根目录创建 `.env` 文件，并填入以下配置：

```bash
# 飞书开放平台配置
FEISHU_APP_ID=cli_xxxxxxxx      # 您的飞书应用 App ID
FEISHU_APP_SECRET=xxxxxxxx      # 您的飞书应用 Secret
FEISHU_BASE_URL=https://open.feishu.cn/open-apis
```

### 3. 飞书权限设置

1.  访问 **[飞书开放平台开发者后台](https://open.feishu.cn/app/)**。
2.  点击“创建企业自建应用”，填写名称和描述。
3.  进入应用详情页，在左侧菜单点击 **“凭证与基础信息”**。
4.  在这里您可以找到 **App ID** 和 **App Secret**。
5.  点击左侧 **“权限管理”**，搜索并开通以下权限：
    - `docx:document:readonly` (读取文档)
    - `docx:document:edit` (编辑文档)
    - `drive:drive:readonly` (读取评论)
    - `drive:drive:edit` (回复评论)
6.  点击 **“版本管理与发布”**，创建版本并发布（这一步非常重要，否则应用无法生效）。
7.  **应用身份（tenant_access_token）调用文档 API 时**，需要把应用授予到目标文档（否则常见会报 403）。
    - 网页端/桌面端文档右上角 **分享** -> **更多** -> **添加文档应用**（有的版本会显示为“文档应用 / 添加文档应用”），搜索并添加你的应用
    - 如果你在文档里找不到该入口：优先用网页端打开同一篇文档再找一次；并确认应用已发布且权限已开通、你对该文档有编辑权限
8.  **如果你改成用户身份（user_access_token）调用**：通常不需要“添加文档应用”，只要该用户对文档有编辑权限即可。

### 4. 运行 Skill

从文档链接提取 `document_token`：
- 示例链接：`https://feishu.cn/docx/doxcnABC123`
- 则 `document_token = doxcnABC123`
