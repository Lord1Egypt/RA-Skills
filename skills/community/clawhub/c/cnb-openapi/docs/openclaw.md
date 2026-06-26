### 安装

将仓库克隆到 OpenClaw 的 skills 目录：

```bash
git clone https://cnb.cool/cnb/sdk/cnb-openapi-skills ~/.openclaw/skills/cnb-openapi-skills
```

### 配置环境变量

在终端或 shell 配置文件中设置环境变量：

```bash
export CNB_TOKEN="your_cnb_token_here"
# 可选：自定义 API 地址（默认为 https://api.cnb.cool）
export CNB_API_ENDPOINT="https://api.cnb.cool"
```

### 使用

安装完成后，OpenClaw 会自动加载 `SKILL.md` 作为技能文档。当你在对话中涉及 CNB 平台操作时（如查询仓库、管理 Issue、操作合并请求等），OpenClaw 会自动调用该技能。

示例提问：

- "帮我查看 cnb/feedback 仓库的 Issue 列表"
- "帮我在 my-org/my-repo 仓库创建一个 Issue，标题为「Bug 修复」"
- "查看 cnb/feedback 仓库的分支列表，告诉我默认分支是什么"
- "帮我获取 my-org/my-repo 仓库最新的合并请求"

### 更新

```bash
cd ~/.openclaw/skills/cnb-openapi-skills && git pull
```
