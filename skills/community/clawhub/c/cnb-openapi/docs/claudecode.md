### 安装 Skills

将仓库克隆到 Claude 的 skills 目录：

```bash
git clone https://cnb.cool/cnb/sdk/cnb-openapi-skills ~/.claude/skills/cnb-openapi-skills
```

或者使用 pnpx skills 命令安装:
```bash
pnpx skills add https://cnb.cool/cnb/sdk/cnb-openapi-skills.git -a claude-code
```

### 使用 /plugins 安装 Hooks

如需完整功能（包括自动路由和元认知触发），请使用 Claude Code 的插件系统：

```bash
# 第一步：添加 marketplace
/plugin marketplace add https://cnb.cool/cnb/sdk/cnb-openapi-skills.git

# 第二步：安装插件（包含 hooks）
/plugin install cnb-openapi@cnb-openapi-skills
```

### 环境变量

安装插件后，仍需配置环境变量：

```bash
export CNB_TOKEN="your_cnb_token_here"
# 可选：自定义 API 地址（默认为 https://api.cnb.cool）
export CNB_API_ENDPOINT="https://api.cnb.cool"
```

Windows 用户请参考 [README](../README.md) 中的 Windows 环境变量配置说明。
