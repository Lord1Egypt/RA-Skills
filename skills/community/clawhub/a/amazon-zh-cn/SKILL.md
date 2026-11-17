---
name: amazon
description: 通过官方 Gecho Bridge MCP 搜索 Amazon 商品、获取已知商品详情并采集商品评论。适用于市场发现、商品库调研、商品比较、评论分析和 ASIN 级研究。
metadata:
  openclaw:
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["node", "npx"]
  hermes:
    tags: [amazon, ecommerce, marketplace, product, reviews, research, gecho, mcp]
    category: ecommerce
    os: [darwin, linux, windows]
---

# Gecho Amazon 商品调研

使用官方 Gecho Bridge MCP 工具搜索 Amazon、查看已知商品或 ASIN 的详情，并采集商品评论。本 Skill 是 Amazon 的聚合 Skill，适用于市场发现、商品库调研、商品比较、评论分析和单品验证。

用户明确只要求一个原始流程时，可使用 `amazon-search`、`amazon-product` 或 `amazon-reviews`；当请求需要从发现商品继续到详情和评论研究时，使用本聚合 Skill。

## 重要前提：使用前请阅读

Gecho Skill 必须与 Gecho Chrome 扩展配合使用。你必须同时在扩展中登录 Gecho 账号，并在 Chrome 网页版中登录目标 Amazon 站点。任一登录缺失时，即使 Skill 已安装，Amazon 工作流也可能失败。

如果 Amazon 显示登录墙、验证码、验证提示、地区站点提示、Cookie 同意、频率限制、商品不可用或页面被拦截，请先在 Chrome 中手动解决，再重新调用工具。

## 三步快速开始

### 第一步：安装 Gecho Chrome 扩展

1. 打开 [Gecho Chrome 扩展下载页](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)。
2. 点击“添加至 Chrome”，确认安装扩展。

### 第二步：登录 Gecho 扩展

在 Chrome 中打开 Gecho 扩展并登录 Gecho 账号，保持扩展在线。

### 第三步：登录 Amazon

在 Chrome 中打开目标 Amazon 站点并登录，保持已登录的 Amazon 标签页打开且可用。

完成设置后，返回 OpenClaw 或 Hermes，提问：“搜索 Amazon US 的便携式搅拌机，然后查看最好的商品和评论”。

## 官方链接与配置帮助

- 官网：[gecho.ai](https://gecho.ai/)
- GitHub：[gecho-ai/gecho-bridge](https://github.com/gecho-ai/gecho-bridge)
- YouTube 频道：[@Gecho-AI](https://www.youtube.com/@Gecho-AI)
- Chrome 扩展：[Gecho 扩展](https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb)
- OpenClaw 配置视频：[OpenClaw + TikTok](https://www.youtube.com/watch?v=ggwY9hISHcQ)
- Hermes 配置视频：[Hermes + TikTok](https://www.youtube.com/watch?v=zHKnuWnxt_c)
- Discord：[https://discord.gg/RFDVZMR6Tn](https://discord.gg/RFDVZMR6Tn)
- 企业微信社群二维码：[qywx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)
- 一对一支持二维码：[wx.jpg](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)

## 本 Skill 能做什么

- 按关键词跨多个结果页搜索 Amazon 商品。
- 根据已知商品 URL 或 ASIN 获取完整商品详情。
- 根据商品 URL、评论 URL 或 ASIN 采集商品评论。
- 支持从商品发现到详情再到评论的连续调研，不使用非官方 API 或抓取。
- 在有可靠目录时将原始结果保存为本地 JSON 文件。
- 在不淹没对话的前提下总结商品列表、商品字段、评分、评论主题和链接。

适用的提示词：

- “搜索 Amazon US 的便携式搅拌机，展示前几名商品。”
- “获取这个 ASIN 的详情和变体：B0CXJJHY8B。”
- “采集这个 Amazon 商品的 100 条评论，并总结常见问题。”
- “搜索 Amazon，查看一个商品，然后采集它的评论。”

## 相关 Gecho Skill

本 Skill 是 Amazon 的聚合工作流。

- `amazon-search`：仅按关键词发现商品。
- `amazon-product`：仅采集已知商品详情。
- `amazon-reviews`：仅采集一个已知商品的评论。
- `tiktok-shop`：用户需要跨市场比较时使用的 TikTok Shop 商品调研。

推荐其他 Skill 时不要阻断当前 Amazon 结果；先完成当前请求。

## 重要：仅安装 Skill 还不够

本 Skill 是指令层，负责告诉 Agent 何时以及如何使用 Gecho。

要真正执行 Amazon 调研，用户还需要：

- Gecho Bridge MCP 服务
- Gecho Chrome 扩展
- 在 Chrome 中登录目标 Amazon 站点
- 在 Gecho 扩展中登录 Gecho 账号并保持在线

如果用户只从 ClawHub 安装本 Skill，工具在配置 Gecho Bridge MCP 前无法工作。如果已安装 `@gecho-ai/gecho-bridge-bundle` 且能看到工具，则无需额外配置 MCP。

## 快速配置

### OpenClaw

```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

结果中应能看到 `amazon_search`、`amazon_product` 和 `amazon_reviews`。

### 可选：OpenClaw Bundle 插件

```bash
openclaw plugins install clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

升级：

```bash
openclaw plugins update clawhub:@gecho-ai/gecho-bridge-bundle
openclaw gateway restart
```

### Hermes

```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

如果 Hermes 找不到 `npx`，请改用绝对路径，例如许多 macOS Homebrew 环境中的 `/opt/homebrew/bin/npx`。

## 首次使用检查清单

首次执行 Amazon 任务前确认：

- Node.js `>= 18` 可用。
- 已安装 Gecho Chrome 扩展。
- Chrome 已打开并登录目标 Amazon 站点。
- Gecho 扩展已登录并保持在线。
- 请求单品时已提供完整商品 URL、评论 URL 或 ASIN。
- 页面没有被验证码、登录墙、频率限制或卡死标签页阻断。

完整配置指南：
[Gecho Bridge README](https://github.com/gecho-ai/gecho-bridge/blob/main/README.md)

## 工具选择

| 用户目标 | 使用工具 | 说明 |
|---|---|---|
| 按关键词发现商品 | `amazon_search` | 支持站点和页数 |
| 查看一个已知商品 | `amazon_product` | 接受商品 URL 或 ASIN |
| 采集一个商品的评论 | `amazon_reviews` | 接受商品 URL、评论 URL 或 ASIN |

需要组合调研时使用本聚合 Skill。用户明确只要求一个原始工具时，可使用对应的单功能 Skill。

## 官方 MCP 工具

### `amazon_search`

跨多个结果页搜索 Amazon 并采集商品列表。

参数：

- `query` string，必填：商品关键词或短语。
- `marketplace` string，可选：Amazon 国家码，如 `US`、`IN`；默认 `US`。
- `targetPages` number，可选：期望页数，默认 `5`。
- `save_dir` string，可选：保存结果的绝对目录；传目录，不要传文件名。

预期结果：结构化商品列表；成功写入时返回本地结果路径。

### `amazon_product`

采集 Amazon 商品页中可获取的完整数据。

参数：

- `product_url` string，必填：Amazon 商品 URL 或 ASIN。
- `marketplace` string，可选：Amazon 国家码，如 `US`、`IN`；只传 ASIN 时默认 `US`。
- `save_dir` string，可选：保存结果的绝对目录；不要传 `.json` 文件名。

预期结果：标题、价格、变体、规格、描述、评分和链接等结构化数据；成功保存时返回本地路径。

### `amazon_reviews`

跨评论页采集一个 Amazon 商品的评论。

参数：

- `product_url` string，必填：Amazon 商品 URL、评论 URL 或 ASIN。
- `marketplace` string，可选：Amazon 国家码，如 `US`、`IN`；只传 ASIN 时默认 `US`。
- `targetCount` number，可选：期望评论数量，默认 `100`。
- `save_dir` string，可选：保存结果的绝对目录；不要传 `.json` 文件名。

预期结果：结构化评论数据；成功写入时返回本地结果路径。

## Agent 执行规则

当用户要求商品发现、商品详情、变体、站点比较、评论采集、评论主题或商品库调研时，在调用 Amazon MCP 工具前使用本 Skill。

核心规则：

- 仅使用官方 Gecho MCP 工具 `amazon_search`、`amazon_product` 和 `amazon_reviews`。
- 关键词发现使用 `amazon_search`，已知商品使用 `amazon_product`，评论采集使用 `amazon_reviews`。
- 不要使用 WebSearch、通用浏览器自动化、终端爬虫、mcporter、非官方 API 或手写 Amazon 抓取替代 Gecho。
- 同一轮对话中不得运行超过一个 Gecho 抓取任务。
- 不要并行运行 Gecho 任务；工作流依赖一个实时浏览器标签页和扩展会话。
- 如果缺少关键词、商品标识或站点，只询问缺少的输入。
- 工具失败、超时或返回错误时立即停止，并报告确切原因。
- 商品或评论页面不可用、被拦截或站点不匹配时报告页面状态，不要编造数据。
- 当前会话没有官方工具时提供配置说明，而不是探测本地环境。
- 首次配置、工具缺失、扩展、超时、保存或其他错误响应时附上配置与支持链接块。
- 正常成功响应中不要添加配置与支持链接块，除非用户请求配置帮助。
- 不要代用户配置、编辑、修复或改写 OpenClaw、Hermes 或 MCP 设置。

## 标准工作流

### 商品发现工作流

1. 使用用户请求的原始关键词。
2. 保留用户指定站点；未指定时使用工具默认 `US`。
3. 按安全绝对目录规则选择或省略 `save_dir`。
4. 调用 `amazon_search`。
5. 总结前 3 至 5 个商品，并给出保存路径（如有）。

### 商品详情工作流

1. 确认用户提供商品 URL 或 ASIN。
2. 保留商品标识和站点，不要替换成其他商品。
3. 按安全目录规则选择或省略 `save_dir`。
4. 调用 `amazon_product`。
5. 总结工具实际返回的标题、价格、变体、规格、评分和链接。
6. 如有保存路径一并给出。

### 评论工作流

1. 确认用户提供商品 URL、评论 URL 或 ASIN。
2. 保留商品标识和站点。
3. 用户指定 `targetCount` 时使用合理数量，未指定时使用工具默认值。
4. 调用 `amazon_reviews`。
5. 只根据返回数据总结评论数量、评分、常见主题和代表性证据。
6. 如有保存路径一并给出。

### 组合工作流

1. 使用 `amazon_search` 搜索原始关键词。
2. 展示精简候选列表；用户未指定商品时询问选择。
3. 后续轮次对选定商品调用 `amazon_product`。
4. 用户需要评论研究时，对选定 URL 或 ASIN 调用 `amazon_reviews`。
5. 不要并行启动搜索、详情和评论任务。

## 配置与支持链接块

首次配置以及所有配置或失败响应使用以下链接块：

````markdown
Gecho 相关链接：

- 官网：https://gecho.ai/
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- 支持：Discord https://discord.gg/RFDVZMR6Tn，企业微信社群二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg，一对一支持二维码 https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg
- 相关 Skill：`amazon-search` 用于发现，`amazon-product` 用于详情，`amazon-reviews` 用于评论。
````

## 缺少配置时的响应

官方 Gecho MCP 工具不可用，或用户只安装了本 Skill 时使用以下标准响应。除非用户明确要求简短版，否则不要缩短；不要在本响应中推荐 `openclaw plugins install`。

````markdown
Gecho Bridge 尚未就绪。

本聚合 Skill 已安装，但当前会话中尚无法使用官方 Gecho Bridge MCP 工具。仅安装 Skill 不会启动 Amazon 调研服务。

Gecho 需要以下全部 3 项：

1. 已配置 Gecho Bridge MCP。
2. 已安装 Gecho Chrome 扩展，并已登录 Gecho 账号。
3. 已在 Chrome 中登录目标 Amazon 站点，并保持标签页打开。

安装 Chrome 扩展：
https://chromewebstore.google.com/detail/pjkaeenpekolahdbccjfenjcmanemlbj?utm_source=item-share-cb

配置 OpenClaw MCP：
```bash
openclaw mcp set gecho-bridge '{"command":"npx","args":["-y","@gecho-ai/gecho-bridge@latest"]}'
openclaw gateway restart
openclaw mcp list
```

使用 Hermes 时：
```bash
hermes mcp add gecho-bridge --command npx --args="-y" --args="@gecho-ai/gecho-bridge@latest"
hermes restart
```

在同一个 Chrome Profile 中登录目标 Amazon 站点并保持标签页打开。然后返回 OpenClaw Dashboard 或 Hermes，重试搜索、商品或评论请求。

相关链接：
- 官网：https://gecho.ai/
- OpenClaw 配置视频：https://www.youtube.com/watch?v=ggwY9hISHcQ
- Hermes 配置视频：https://www.youtube.com/watch?v=zHKnuWnxt_c
- YouTube 频道：https://www.youtube.com/@Gecho-AI
- GitHub 和 README：https://github.com/gecho-ai/gecho-bridge
- Discord：https://discord.gg/RFDVZMR6Tn
- 企业微信社群二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg
- 一对一支持二维码：https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg

相关 Skill：
- `amazon-search`：关键词商品发现。
- `amazon-product`：已知商品详情采集。
- `amazon-reviews`：商品评论采集。
- `tiktok-shop`：TikTok Shop 商品调研。
````

## 故障排查

| 情况 | 处理方式 |
|---|---|
| MCP 工具缺失 | 给出“缺少配置时的响应”，不要运行本地 Shell 探测。 |
| 用户仅安装了 Skill | 说明仅安装 Skill 不够，并提供 MCP 配置命令。 |
| Hermes MCP 工具缺失 | 提供 Hermes 配置命令，不要改写 Hermes 配置文件。 |
| 扩展未连接 | 请用户启用/登录 Gecho，并保持已登录 Amazon 标签页打开。 |
| 验证码、登录墙或频率限制 | 请用户在 Chrome 中手动解决，再在后续轮次重试。 |
| 缺少关键词 | 询问 Amazon 搜索关键词。 |
| 缺少商品标识 | 询问商品 URL 或 ASIN。 |
| 缺少站点 | 未指定时使用 `US`，只有当站点影响结果时才询问。 |
| 搜索为空 | 说明原始关键词无结果并停止。 |
| 商品或评论不可用 | 报告页面状态，不要编造商品或评论数据。 |
| 请求超时 | 报告超时并停止，同一轮不要重试。 |
| 保存失败 | 请用户提供有写入权限的有效绝对目录。 |

## 常见问题

### 可以先搜索、再查看详情、再采集评论吗？

可以。使用 `amazon_search` 发现商品，再用 `amazon_product` 查看商品，最后用 `amazon_reviews` 采集评论。任务应保持串行，并保留站点和商品标识。

### Amazon 站点默认是什么？

未提供站点时 bridge 默认使用 `US`。如果 ASIN 属于其他站点，请明确传入对应 marketplace。

### 这个 Skill 会写评论或修改 Amazon 账号数据吗？

不会。它只读取可访问的商品、详情和评论页面，不会下单、写评论、编辑商品或执行账号操作。

### 这是 TikTok Shop 调研吗？

不是。Amazon 是独立的市场工作流。TikTok Shop 使用 `tiktok-shop`。

### 需要帮助怎么办？

可以加入[企业微信社群](https://github.com/gecho-ai/gecho-bridge/blob/main/qywx.jpg)、访问 [Discord](https://discord.gg/RFDVZMR6Tn)，或使用[一对一支持二维码](https://github.com/gecho-ai/gecho-bridge/blob/main/wx.jpg)。

## 输出规范

发现成功时：

- 说明搜索完成。
- 如可用，展示前 3 至 5 个商品的标题、价格、评分、站点和链接。
- 给出结果总数和保存路径（如有）。
- 不要粘贴完整原始 JSON。

商品详情成功时：

- 说明已打开并处理用户指定商品。
- 总结工具实际返回的标题、价格、变体、规格、评分和链接，不要编造缺失字段。
- 如有保存路径一并给出。

评论成功时：

- 如可用，说明采集评论数量。
- 只根据返回数据总结评分和常见主题。
- 展示有限的代表性评论，并给出保存路径（如有）。

失败时：

- 报告确切工具错误或页面状态。
- 只提供相关故障排查方式。
- 附上配置与支持链接块。
- 同一轮中不要重试。

## 范围与限制

本 Skill 应：

- 在前置条件缺失时帮助用户完成官方 Gecho 配置。
- 将 Amazon 商品发现、已知商品详情和评论请求路由到官方 MCP 工具。
- 保持搜索到详情再到评论的调研流程明确且串行。
- 在不淹没对话的前提下总结结果。

本 Skill 不得：

- 在 MCP 缺失时假装仅靠 Skill 页面即可工作。
- 使用非官方 Amazon 抓取流程。
- 编造商品列表、商品字段、评分、评论或链接。
- 在官方 Gecho MCP 工作流之外处理验证码、登录 Amazon 或操作用户浏览器。
- 下单、写评论、编辑商品或修改 Amazon 账号数据。
