# easyserp

![easyserp icon](https://raw.githubusercontent.com/aiispower/easyserp/main/assets/easyserp-icon.png)

![easyserp and easybrSearch family banner](https://raw.githubusercontent.com/aiispower/easyserp/main/assets/easy-search-family-banner.png)

用 Google 和 Bing 搜索 API，为 AI Agent 和自动化任务提供结构化网页结果。支持 **2000 QPS**；在 [控制台](https://serp.skyvora.cc)注册一次赠送 **1000 次搜索**，之后 **¥2/1000 次**。赠送额度为一次性，不是每月额度。

[GitHub](https://github.com/aiispower/easyserp) · [Download Skill ZIP](https://github.com/aiispower/easyserp/releases) · [Free easybrSearch](https://github.com/aiispower/easybrSearch)

## 开始使用

在控制台注册并创建 API key，然后将密钥放入环境变量（不要粘贴到聊天或命令参数中）：

```sh
export EASYSERP_API_KEY='你的密钥'
```

把本仓库中的 `skills/easyserp/` 安装为 Agent Skill，或在支持 Skill 的 Agent 中按需调用。Skill 会运行随包提供的 CLI，用户无需编写集成代码：

```text
使用 easyserp 搜索 Google 和 Bing 上关于 [主题] 的资料，比较结果并保留来源链接。
```

也可从源码目录直接运行 CLI：

```sh
node scripts/cli.mjs search "solar power" --engine google --region US --format markdown
node scripts/cli.mjs batch ./queries.json --concurrency 4
node scripts/cli.mjs request REQUEST_ID
```

`request` 用于查看 queued/running 的待处理请求。网络结果未知时保留 request ID 和幂等键，按指南恢复，不要换新键重复发起。

## 选择适合的工具

- **easyserp**：适合可重复、结构化或程序化的 Google/Bing 网页搜索。CLI、MCP 与 API 使用同一按量计费服务。
- **[easybrSearch](https://github.com/aiispower/easybrSearch)**：免费的浏览器研究 Skill/CLI，复用已连接的浏览器搜索网站、自媒体和代码项目，并读取选定页面。源码：[GitHub](https://github.com/aiispower/easybrSearch)，[Gitee](https://gitee.com/xxjrq/easybrSearch)。它不需要 easyserp API key，也不包含 easyserp 的 API 配额。

两者可按任务互补：用 easybrSearch 做广泛的站点探索和阅读；需要程序化 Google/Bing 结果时用 easyserp。更多检索资料要继续用于选题、内容制作与多平台发布时，可选用 [aimeGeo](https://geo.aimmme.com/) 的相关工作流。

## 开发者与集成

HTTP API、MCP stdio、本地安装与 SDK 说明见[集成指南](https://github.com/aiispower/easyserp/blob/main/docs/INTEGRATIONS.md)；完整字段和恢复约定见 [API 参考](https://github.com/aiispower/easyserp/blob/main/docs/API.md)。SDK 是给开发者的可选集成方式，普通用户优先使用 Skill 或 CLI。

开源客户端、CLI、MCP 适配器和 Skill 使用 MIT 许可；托管搜索服务按量计费。市场提交及上架状态见[渠道与发布材料](https://github.com/aiispower/easyserp/blob/main/docs/MARKETPLACE.md)，仅在实际提交后更新。

English: [README.en.md](README.en.md).
