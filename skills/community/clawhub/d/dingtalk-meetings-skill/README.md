# 钉钉会议日程 Skill

通过钉钉日历官方 MCP Server，用自然语言全面管理会议与日程的 Agent Skill。

## 功能特性

- **日程管理**：创建 / 修改 / 删除日程会议，响应日程邀请
- **参会人管理**：添加 / 移除参会人，查看参与人列表及响应状态
- **智能查询**：日程列表与详情、空闲/忙碌时段、智能推荐会议时间
- **会议室管理**：查询空闲会议室、预定会议室、管理会议室分组
- **日历本管理**：列出/搜索日历本、管理共享权限（ACL）
- **附件**：为日程添加钉盘附件

## 兼容性

- 依赖 `dingtalk-calendar` MCP Server（mcpId=1050，StreamableHttp）
- 可选依赖 `dingtalk-contacts` MCP Server（mcpId=2400，按姓名查找参会人）
- 兼容任何支持 MCP 的 Agent：Claude Code、Cursor、VS Code、Roo Code、Gemini CLI、Codex 等

## 快速开始

### 1. 开通钉钉日历 MCP

访问 [钉钉 AIHub 日历页面](https://aihub.dingtalk.com/#/detail?mcpId=1050&detailType=marketMcpDetail)，登录钉钉账号后点击【开通服务】，复制右侧的 StreamableHttp URL。

### 2. 配置 MCP 服务

**Claude Code：**
```bash
claude mcp add --transport http --scope user dingtalk-calendar "<你的 URL>"
```

**其他 Agent：** 参照 [SKILL.md](SKILL.md) 初始化流程中的配置文件写入方案。

### 3. 可选配置通讯录 MCP

如需按姓名查找参会人，同样流程开通 [通讯录 MCP](https://aihub.dingtalk.com/#/detail?mcpId=2400&detailType=marketMcpDetail)（mcpId=2400）。仅创建包含其他参会人的日程时需要。

## 使用示例

```
"帮我创建明天下午2点的周会，拉上张三李四"
"查看我今天的日程安排"
"取消下午的产品评审会"
"帮我看看明天下午哪些会议室是空的"
"我和张三、李四明天什么时候都有空"
```

## 项目结构

```
dingtalk-meetings-skill/
├── SKILL.md                  # Skill 主文件（核心指令）
├── LICENSE                   # MIT License
├── README.md                 # 项目说明
├── .gitignore
├── references/
│   └── mcp-tools.md          # MCP 工具完整速查（24 个日历工具 + 11 个通讯录工具）
└── evals/
    ├── evals.json            # 执行评测用例
    └── trigger-evals.json    # 触发评测用例
```

## 许可证

[MIT License](LICENSE)
