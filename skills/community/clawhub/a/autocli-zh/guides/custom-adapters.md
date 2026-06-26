# Custom Adapters

在 autocli 已明确是目标执行路径，但 `--help` 中仍找不到满足用户目标的现成命令时使用本文件。

进入本流程前，必须先明确告知并获得用户同意：
- 本流程可能读取当前浏览器桥接状态、登录态页面内容、XHR/Fetch 请求或页面内状态数据。
- 本流程会在 `~/.autocli/adapters/` 下写入 YAML 适配器，属于用户主目录持久化修改。

未获同意，不得进入 `generate / explore / cascade / evaluate / intercept / tap` 或写入 `~/.autocli/*`。

## 默认流程

1. 先确认目标网站 URL 与本轮目标。
2. 优先尝试：

```bash
autocli generate <url> --goal "<目标>"
```

3. 若自动生成不足，再按需使用：

```bash
autocli explore <url>
autocli cascade <url>
```

4. 若仍不足，再在以下目录创建 YAML 适配器：

```text
~/.autocli/adapters/<site>/
```

5. 创建后，用对应命令做最小验证。
6. 若适配器已可用，再视情况按 `guides/reference-bootstrap.md` 的模板补写 `references/<target>.md`，沉淀该目标的高频命令模式与最小说明。

## 何时优先手写浏览器型 YAML

满足以下信号时，优先手写浏览器型最小 YAML，而不是继续执着于接口发现：
- `generate` 没发现可用 API endpoint
- `explore` 能读到页面标题或基本 DOM，但没有现成接口
- 页面更像门户首页、卡片流、服务端渲染列表或内容聚合首页
- 目标是提取页面上已经可见的列表内容，而不是调站点内部 API

这类页面通常更适合：
- `navigate`
- `evaluate`
- 少量 `select / map / limit`

## 最小 YAML 示例

在 `~/.autocli/adapters/` 下创建 YAML 文件即可添加自定义适配器，例如：

```yaml
# ~/.autocli/adapters/mysite/hot.yaml
site: mysite
name: hot
description: My site hot posts
strategy: public
browser: false

args:
  limit:
    type: int
    default: 20
    description: Number of items

columns: [rank, title, score]

pipeline:
  - fetch: https://api.mysite.com/hot
  - select: data.posts
  - map:
      rank: "${{ index + 1 }}"
      title: "${{ item.title }}"
      score: "${{ item.score }}"
  - limit: "${{ args.limit }}"
```

常见顶层字段：
- `site`：站点名
- `name`：命令名
- `description`：命令描述
- `strategy`：执行策略
- `browser`：是否依赖浏览器
- `args`：参数定义
- `columns`：默认输出列
- `pipeline`：执行流水线

## 高频步骤

最常用的一线组合通常是：
- `fetch`：发起 HTTP 请求
- `navigate`：导航到页面
- `evaluate`：在浏览器中执行 JS
- `select`：选取嵌套数据
- `map`：映射字段
- `limit`：截断结果

## 高频表达式

先记住这些就够：

```text
${{ args.limit }}
${{ item.title }}
${{ index + 1 }}
${{ item.subtitle || 'N/A' }}
${{ item.title | truncate(30) }}
```

更多步骤、过滤器、配置、架构与源码定位，读取：

```text
guides/custom-adapters-reference.md
```

## 最小要求

- 优先自动生成，手写 YAML 作为兜底。
- 适配器创建后必须做最小验证。
- 不把未验证的适配器当作已完成交付。
- 优先把目标压成最小可用流水线，不一开始就堆复杂步骤。
- 若后续需要沉淀 target 卡，按 `guides/reference-bootstrap.md` 的模板写，不把旧制度内容带回去。
