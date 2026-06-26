### 安装

将仓库克隆到 CodeBuddy 的 skills 目录：

```bash
git clone https://cnb.cool/cnb/sdk/cnb-openapi-skills ~/.codebuddy/skills/cnb-openapi-skills
```

### 配置环境变量

CodeBuddy 的环境变量读取机制比较特殊，**不能通过在终端中临时 `export` 的方式设置**。在终端中 `export` 的变量仅对当前 shell 会话生效，CodeBuddy 执行命令时使用的是独立的 shell 环境，无法读取到这些临时变量。

正确的设置方式是将环境变量写入 shell 配置文件，然后**重启 CodeBuddy（重启 IDE）**使其生效：

```bash
# 将以下内容添加到 ~/.zshrc（macOS）或 ~/.bashrc（Linux）中
echo 'export CNB_TOKEN="your_cnb_token_here"' >> ~/.zshrc
# 可选：自定义 API 地址（默认为 https://api.cnb.cool）
echo 'export CNB_API_ENDPOINT="https://api.cnb.cool"' >> ~/.zshrc
```

修改完成后，**必须重启 IDE**，CodeBuddy 才能读取到新的环境变量。

> **注意**：仅执行 `source ~/.zshrc` 只对当前终端会话生效，CodeBuddy 仍然无法识别。必须重启 IDE 才能让 CodeBuddy 的执行环境加载到最新的配置。

### 使用

安装完成后，CodeBuddy 会自动加载 `SKILL.md` 作为技能文档。当你在对话中涉及 CNB 平台操作时（如查询仓库、管理 Issue、操作合并请求等），CodeBuddy 会自动调用该技能。

> **注意**：默认的 Ask 模式不会帮你执行命令，只会给出对应的命令行说明。如果需要实际执行命令（如调用 API、创建 Issue 等），请切换到 **Craft** 或 **Agent** 模式。

示例提问：

- "帮我查看 cnb/feedback 仓库的 Issue 列表"
- "帮我在 my-org/my-repo 仓库创建一个 Issue，标题为「Bug 修复」"
- "查看 cnb/feedback 仓库的分支列表，告诉我默认分支是什么"
- "帮我获取 my-org/my-repo 仓库最新的合并请求"

### 更新

```bash
cd ~/.codebuddy/skills/cnb-openapi-skills && git pull
```
