# Developer Tool Surface Priority Map

这份 playbook 用来回答：

> 当 AI 可见性结果不理想时，开发者工具团队应该先修哪里，才能最快影响下载、安装、调用和 agent 采用？

不是所有页面都同等重要。对 developer tools、API、SDK、scientific products 来说，优先级通常差异很大。

## 一、先按业务目标拆分

| 目标 | 最先看的 surfaces |
|---|---|
| 提高品牌入选率 | README、品牌定位页、comparison page、benchmark page |
| 提高安装量 | install page、quickstart、package registry、minimal example |
| 提高 API 调用量 | docs 首页、auth page、SDK quickstart、endpoint examples |
| 提高 agent 调用量 | agent docs、integration page、MCP/tool docs、workflow examples |
| 提高长期推荐率 | changelog、release notes、case studies、community examples |

## 二、默认优先级

### P0: 必须先修

| Surface | 为什么重要 | 常见失败症状 |
|---|---|---|
| README hero | 模型与用户都常从这里抽品牌定位 | 知道品牌，不知道适用场景 |
| Install / Quickstart | 决定是否能进入首次成功体验 | 被推荐但没人真正装 |
| Docs homepage | 决定模型能否形成正确入口认知 | 模型给错入口或不给入口 |
| Capability comparison | 决定是否能打赢竞品替代位 | 模型总把竞品放第一 |
| Minimal code example | 决定接入信心 | 模型不敢给具体调用建议 |

### P1: 紧随其后

| Surface | 为什么重要 | 常见失败症状 |
|---|---|---|
| Integration docs | 决定生态理解和 workflow 采用 | 生态分数低，agent 不选你 |
| Benchmark / proof | 决定模型是否敢主推 | 模型只列为候选，不首推 |
| FAQ / troubleshooting | 决定负向认知是否可修复 | 模型反复提部署复杂或不稳定 |
| Changelog / release notes | 决定 freshness | 模型反复引用旧版本信息 |
| Community examples | 决定第三方可引用性 | 模型知道官方说法，不知道真实用例 |

### P2: 放在后面补强

| Surface | 为什么重要 | 常见失败症状 |
|---|---|---|
| Deep tutorials | 提高高级用户留存 | 高级 query 表现弱 |
| Blog / thought leadership | 提高长期实体影响力 | 行业类 query 覆盖不足 |
| Partner / ecosystem pages | 增强关系图谱 | 集成理解不完整 |
| Showcase / gallery | 增强可视案例 | 模型缺少具体实践例子 |

## 三、面向 MinerU 的推荐顺序

### 如果目标是下载 / 安装

1. README hero
2. install page
3. quickstart
4. benchmark page
5. comparison page

### 如果目标是在 RAG / scientific parsing workflow 里被优先选择

1. capability comparison
2. integration docs
3. examples for paper ingestion / markdown / JSON export
4. benchmark page
5. agent-oriented cookbook

## 四、面向 Sciverse API 的推荐顺序

### 如果目标是 API 调用量

1. docs homepage
2. auth + first request page
3. endpoint examples
4. SDK quickstart
5. use-case pages

### 如果目标是 agent invocation

1. workflow examples
2. tool / API boundary page
3. MCP or agent integration page
4. error handling / retry guidance
5. structured response examples

## 五、如何把 source surface 和 query pool 对上

建议每条 query 不只定义 `type`，还额外定义：

- `funnel_stage`
- `target_surface`
- `desired_action`

例如：

| Query 类型 | target_surface | desired_action |
|---|---|---|
| 选型型 query | comparison-page | install |
| 接入型 query | quickstart | api-call |
| agent 型 query | integration-docs | agent-invocation |
| 负向 query | faq | trust-recovery |

这样在 repair 时就不会只知道“哪条 query 差”，还知道“先修哪个页面”。

## 六、每周复盘时该看什么

每周复盘至少回答 4 个问题：

1. 本周最差的 5 条 query 各自指向哪个 source surface？
2. 哪些 source surface 同时影响多个 query？
3. 本周修的是认知问题、安装问题，还是接入问题？
4. 修复动作是否对应最终想提升的业务动作？

## 七、输出模板

每次做 repair planning 时，至少输出：

- Top 3 priority surfaces
- 每个 surface 对应的 Top queries
- 每个 surface 期望影响的业务动作
- T+7 / T+14 要看的验证 query
