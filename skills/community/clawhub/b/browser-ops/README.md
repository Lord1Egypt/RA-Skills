# browser-ops

给 AI Agent 的网页访问路由表。全 CLI 架构，零 MCP 依赖，省 75% 上下文 token。

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](SKILL.md)

```
WebFetch ($0) → opencli web read ($0) → Firecrawl → agent-browser → browser-use ($0.05/步)
```

能用 HTTP 就不开浏览器，能用 opencli 就不用 browser-use。

## Quick Start

```bash
npm i -g @jackwener/opencli
# Chrome 装 OpenCLI Browser Bridge 扩展
opencli doctor  # 三个 OK 才能用
```

```bash
# 读内网页面（Cookie 零配置，直连 Chrome）
opencli web read --url "https://internal-site.com"

# 75 站点结构化数据
opencli twitter trending
opencli zhihu hot
opencli hackernews top
```

只需装 opencli。其他工具全部按需。

## 四层路由

| 层 | 场景 | 工具 | 费用 |
|----|------|------|------|
| **搜索** | 没有 URL，要找信息 | WebSearch → Tavily → Brave API → opencli search | $0-0.008 |
| **提取** | 有 URL，要内容 | WebFetch → opencli web read → Firecrawl | $0-0.001 |
| **交互** | 有 URL，要操作页面 | opencli operate → agent-browser → browser-use | $0-0.05 |
| **反爬** | 被拦截了 | Zendriver | $0 |

每次网页任务从最便宜的开始，命中就停。违反顺序 = 浪费钱。

## 核心工具

### opencli — Cookie 零配置，75 站点

通过 Chrome Extension Bridge 直连浏览器，天然复用 Cookie/登录态。

```bash
opencli web read --url "https://internal-site.com"     # 读内网页面
opencli operate open "url" && opencli operate state    # 浏览器交互
opencli list                                           # 查看所有 75 站点适配器
```

### agent-browser — @e1 Ref 引用，录制，标注截图

元素定位基于 Accessibility Tree，页面重渲染后 `@e1` 引用不变。

```bash
agent-browser open "url" && agent-browser snapshot -i  # 打开 + 快照
agent-browser click @e2 / fill @e3 "hello"             # Ref 操作
agent-browser screenshot --annotate /tmp/a.png         # 标注截图
agent-browser record start                            # 录制
```

### browser-use — AI 自主操作

自然语言驱动，LLM 自主规划步骤。每步 $0.01-0.05。

```bash
browser-use -p "去 example.com 注册账号"
browser-use --connect -p "任务"                        # 连接已运行 Chrome
```

## 交互工具对比

| 维度 | opencli operate | agent-browser | browser-use |
|------|----------------|---------------|-------------|
| 适合 | ≤3 步简单操作 | 复杂/精确操作 | AI 自主多步 |
| 元素定位 | [N] 编号 | @e1 Ref (稳定) | LLM 自主识别 |
| Cookie | Chrome 直连 | --profile | --connect |
| 标注截图 | — | `--annotate` | — |
| 录制回放 | — | `record` | — |
| 命令数 | 17 | 60+ | CLI 模式 |
| 费用/步 | $0 | $0 | $0.01-0.05 |

## 升级信号

| 当前工具返回 | 升级到 | 命令 |
|------------|--------|------|
| WebFetch → 403/302 登录页 | opencli web read | `opencli web read --url "url"` |
| WebFetch → 空/SPA 空壳 | Firecrawl | `firecrawl scrape "url"` |
| opencli → exit 77 | 手动登录 | Chrome 里重新登录后重试 |
| 需要点击/填表 | opencli operate | `opencli operate open "url"` |
| 编号 [N] 不稳定 | agent-browser | `agent-browser snapshot -i` |
| 多步复杂任务 | browser-use | `browser-use -p "任务"` |
| Cloudflare 拦截 | Zendriver | `python3 -c "import zendriver..."` |

## 为什么全 CLI 不用 MCP

MCP 工具定义常驻上下文（每个 ~250 tokens）。Playwright MCP 21 工具 = 5,250 tokens 每轮都占着。CLI 方式命令写在 SKILL.md 里，只在触发时加载。省 75% 上下文。

## Project Structure

```
browser-ops/
├── SKILL.md              # AI 路由决策指南（核心）
├── task_suite.yaml        # 21 个评估任务
├── scripts/
│   ├── sync-cookies.sh    # Cookie 同步/导入/导出/健康检查
│   ├── web-read.sh        # 三层读取回退链
│   ├── web-search.sh      # 三层搜索回退链
│   └── web-trending.sh    # 8 平台热榜回退链
├── references/
│   ├── routing.md         # 路由决策树详解
│   ├── setup.md           # 安装与配置
│   ├── opencli-usage.md   # opencli 三层用法
│   ├── state-management.md # Cookie 状态管理
│   └── anti-detection.md  # 反爬策略
├── evals/                 # 触发匹配评估
└── tests/                 # 9 个测试模块
```

## 已知限制

- opencli 依赖 Chrome Extension + Chrome 运行
- Tavily/Firecrawl 需 API key，未配置时回退 WebSearch/WebFetch
- agent-browser 和 opencli operate 可以同时运行，但操作同一个 tab 时注意冲突
- Cookie = 快照，SSO token 过期需回 Chrome 重新登录

## License

[MIT](LICENSE)
