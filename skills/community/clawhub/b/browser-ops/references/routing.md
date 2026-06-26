# 路由决策树

> 与 SKILL.md 保持一致。SKILL.md 是权威源。

## 四层模型

| 层 | 工具 | 场景 |
|----|------|------|
| **搜索层** | Tavily / Exa / Brave / WebSearch / opencli \<platform\> | 没有 URL，需要找信息 |
| **提取层** | WebFetch / opencli web read / Firecrawl | 有 URL，要内容 |
| **交互层** | opencli operate / agent-browser / browser-use | 有 URL，要操作页面 |
| **反爬层** | Zendriver | 被拦截 |

## 搜索层路由

```
要搜索？
├─ 实时新闻/深度 → Tavily (search_depth: advanced, 返回 answer + results)
├─ 语义/概念 → Exa MCP (neural search, 代码/论文质量高)
├─ 通用 → Brave Search (独立索引) / WebSearch (内置免费)
├─ 平台内 → opencli <platform> search (75 站点)
└─ fallback → opencli google search
```

### 搜索工具选择依据

- **Tavily**: AI Agent 事实标准，LangChain 默认，返回结构化 answer，1000 次/月免费
- **Exa**: 语义搜索最强，适合概念性问题和代码搜索
- **Brave**: Anthropic 官方推荐 MCP，独立索引不依赖 Google/Bing
- **WebSearch**: 内置零成本，通用性最好
- **opencli google search**: 实际 Google 结果，但高频 CAPTCHA

## 提取层路由

```
有 URL？
├─ 公开网页 → WebFetch ($0)
├─ 403/SSO → opencli web read (Chrome 登录态)
├─ 要深度提取 (JS 渲染/PDF/结构化) → Firecrawl scrape
├─ 批量站点 → Firecrawl crawl (异步)
└─ 已知平台 → opencli <platform> <cmd>
```

## 交互层路由

```
要交互？
├─ 简单 (点击/填表/截图, Cookie 直连) → opencli operate
├─ 复杂 (Ref 引用/录制/批量/标注截图) → agent-browser
├─ AI 自主多步 → browser-use -p "任务"
└─ 未知 DOM → Stagehand act/extract
```

### opencli operate vs agent-browser

| 维度 | opencli operate | agent-browser |
|------|----------------|---------------|
| 命令数 | 17 个 | 60+ 个 |
| 元素定位 | `[1]` 编号（可能变） | `@e1` Ref 引用（稳定） |
| Cookie | Chrome 直连零配置 | `--profile` / `--auto-connect` |
| 标注截图 | ❌ | ✅ `--annotate` |
| 录制回放 | ❌ | ✅ `record` |
| 批量命令 | ❌ | ✅ `batch` |
| DOM diff | ❌ | ✅ `diff` |
| iOS 测试 | ❌ | ✅ `-p ios` |
| 安装依赖 | 同 opencli | 独立 npm 包 |

**简单规则**: 3 步以内用 opencli operate，需要 Ref 引用或录制用 agent-browser。

## 降级模式

opencli 不可用时（Extension 没装 / Chrome 没开）:
- 搜索: Tavily / Exa / Brave / WebSearch
- 提取: WebFetch / Firecrawl
- 交互: browser-use / agent-browser（独立 Chromium）
- 反爬: Zendriver

> See also: `setup.md`（安装）, `state-management.md`（Cookie）
