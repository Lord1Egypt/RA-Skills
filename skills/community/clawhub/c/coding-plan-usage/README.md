# coding-plan-usage-skill

这是为[coding-plan-usage](https://github.com/jeeaay/coding-plan-usage)的技能文档

## 一些说明

如果使用脚本安装失败运行 把这个文档给AI, 让AI下载安装依赖

### 依赖关系

- `coding-plan-usage` 运行时依赖 [agent-browser](https://github.com/vercel-labs/agent-browser)
- 只有在 `coding-plan-usage` 报错“找不到 agent-browser”时，才进入依赖安装流程
- 若仅在沙盒环境出现 `Executable doesn't exist ...` 等错误，优先视为沙盒限制，先让用户在真实环境验证

### 可以配置的项目

在脚本`.env`中配置以下变量，优先会读取`scripts/.env`文件，默认不会创建这个文件。

```bash
# agent-browser 可执行文件路径；为空时默认使用系统 PATH 中的 agent-browser
AGENT_BROWSER_PATH=

# 是否开启有界面模式（true/false）；调试建议 true，后台运行建议 false
AGENT_BROWSER_DEV_MODE=false

# 会话名称；保持固定可复用登录态（cookies/localStorage）
AGENT_BROWSER_SESSION_NAME=

```

### 缺少 agent-browser 时的处理

当 `coding-plan-usage` 输出类似“agent-browser not found”时，执行：

```bash
npm install -g agent-browser
agent-browser -V
```

返回示例：

```bash
agent-browser 0.17.1
```
