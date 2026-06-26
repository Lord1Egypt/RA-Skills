# clawpage-skill（中文说明）

英文版本见：[../README.md](../README.md)。

`clawpage-skill` 用于把长文本快速转成可交互的 Clawpage 页面。
你可以直接描述目标页面，skill 会自动路由到创建/更新页面或模板流程，并发布可访问 URL。

官网：`https://clawpage.ai`

## 可以完成什么

- 将长篇股票市场分析转成图表化仪表盘
- 生成洞察页、工具页、互动页
- 基于 `pageId` 更新已有页面
- 发布时控制有效期与访问口令

## 安装

本仓库是 **Claude Code plugin**。所有运行时通过 [`@clawpage.ai/cli`](https://www.npmjs.com/package/@clawpage.ai/cli) npm 包跑（`npx -y` 自动拉取），你只需要安装本 plugin。

### Claude Code

```text
/plugin marketplace add https://github.com/clawpage/clawpage-marketplace
/plugin install clawpage@clawpage-marketplace
```

或者本地测试：`claude --plugin-dir /path/to/clawpage-skill`。

### Codex

```bash
git clone https://github.com/clawpage/clawpage-skill ~/.codex/skills/clawpage
```

仓库根有 `SKILL.md`（symlink 到 `skills/clawpage-skill/SKILL.md`），Codex 的 flat-skill 发现会原生识别。

### Gemini CLI

```bash
gemini extensions install https://github.com/clawpage/clawpage-skill
```

仓库根有 `gemini-extension.json`，Gemini 注册为 extension；router skill 通过 `skills/clawpage-skill/SKILL.md` 自动发现。

### OpenClaw

```bash
openclaw skills install clawpage-skill
```

OpenClaw 在自带的 plugin 注册表里按名解析并装到当前后端 coding CLI。

## 首次认证

加载 skill 后，对它说一声：

```text
使用 clawpage-skill 完成 init
```

会自动执行 `npx -y @clawpage.ai/cli init`，注册新账号并把 token 写到 `~/.clawpage/keys.local.json`。之后无论从哪个目录调用 skill，都能直接用。

如果想手动设 token：

```bash
mkdir -p ~/.clawpage
cat > ~/.clawpage/keys.local.json <<'EOF'
{
  "clawpage": {
    "token": "sk_xxx",
    "apiHost": "https://api.clawpage.ai"
  }
}
EOF
```

## 场景示例：长股票分析文本 → 生动图表页

```text
使用 clawpage-skill 把下面这段股票分析长文做成可视化页面：
1) 提炼 5 个核心结论
2) 展示 KPI 和 7D/30D/90D 趋势切换
3) 移动端优先
4) 发布并返回 rootUrl、accessUrl、pageId、expiresAt
```

常见处理流程：
- 自动选模板（如 `stock-analysis-terminal`）
- 把长文结构化为摘要、风险、观察模块
- `npx -y @clawpage.ai/cli scaffold stock-analysis-terminal <page-name>` 生成 `~/.clawpage/pages/<page-name>/`
- `npx -y @clawpage.ai/cli publish --page-dir <page-name>` 发布并返回链接 + 有效期

## 模板目录

随 `@clawpage.ai/cli` 发布。运行时查看：`npx -y @clawpage.ai/cli scaffold --list`。

- `stock-analysis-terminal`
- `insight-collection-hub`
- `utility-workbench`
- `concept-animation-lab`
- `mini-game-arcade`
- `general_template`

## 常用命令

dry-run（不发布、不需 token）：

```bash
npx -y @clawpage.ai/cli scaffold general_template /tmp/preview
npx -y @clawpage.ai/cli publish --page-dir /tmp/preview --title "Preview" --dry-run
```

发布（裸名 → `~/.clawpage/pages/<name>`；以 `./` 开头则按 cwd 处理）：

```bash
npx -y @clawpage.ai/cli publish \
  --page-dir my-dashboard \
  --title "My Page" \
  --subtitle "Optional"
```

子命令完整参考见 [`@clawpage.ai/cli` 主页](https://www.npmjs.com/package/@clawpage.ai/cli)。

## 占位符与多语言

文档外，项目中的中文描述已替换为英文大写占位符。
Skill 规则要求 LLM 在发布前根据用户偏好语言填充这些占位符内容。

## 安全提示

- `~/.clawpage/keys.local.json` 是你的 owner token (`sk_*`)。不要提交，不要贴到公开页面 JS（会泄漏整个账号）。
- cwd 下的 `./keys.local.json` 优先级高于全局，用于按项目隔离账号。

## License

本项目采用 MIT-0（MIT No Attribution）开源协议，详见 `../LICENSE`。
