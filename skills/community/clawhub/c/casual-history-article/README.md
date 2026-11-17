# casual-history-article

> 把历史、宗教、地理、人物和流行文化写成有现场感、幽默克制且事实可核的中文微信公众号文章。

一个面向 AI 写作 Agent 的 skill：当用户要求写历史文化科普、以热点或旅行经历讲历史、改写历史文章开头与结尾，或需要「休闲历史配图」同调文案时使用。它把采写流程、叙事结构、句子节奏与幽默分寸都固化成可复用的规则。

## Features

- **现场感开场**：从热点 / 亲历瞬间 / 流行文化入口拉读者进门，而非百科定义。
- **事实骨架 + 故事血肉**：素材卡模板（核心困惑 / 时间线 / 人物 / 现场 / 影响 / 误解 / 证据），每条事实至少一个可靠来源。
- **回环式地图**：6–8 节弹性叙事，开头物件结尾再次出现，留下值得回答的问题。
- **语气控制**：用缓冲词 / 态度标注 / 主动承认局限，让判断不像说教，自动避开「我们必须」「值得注意的是」等教导句。
- **敏感话题对比结构**：殖民 / 种族 / 阶级 / 文化冲突用「既不…也不…」同权重对比呈现多面，不替读者下结论。
- **手机端排版**：每段 ≤3 句、每节 300–600 字，让眼睛能呼吸。
- **分寸守门**：虚构角色只做文化入口并标注；宗教 / 族群 / 苦难不嘲弄受害者；幽默落在自己的无知与类比上。
- **发布前 60 秒检查**：12 条清单兜底事实、来源、结构与边界。

## Quick Start

```bash
# Clone the collection repo, then use skills/casual-history-article
git clone https://github.com/Songhonglei/better-article-writing.git
```

## Usage

详细使用方法见 [SKILL.md](./SKILL.md)。在你的 Agent 中触发示例：

> 用 casual-history-article 写一篇讲「泉州为什么叫光明之城」的公众号文章，从一次逛清净寺的经历开场。

## Install in your AI agent

| Agent | Install |
|---|---|
| WorkBuddy | 复制到 `~/.workbuddy/skills/casual-history-article/` |
| Claude Code | 复制到 `~/.claude/skills/casual-history-article/` |
| Cursor | 复制到 `.cursor/skills/casual-history-article/` |
| OpenClaw | `clawhub install casual-history-article` |

## License

MIT (see [LICENSE](./LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the full version history.
