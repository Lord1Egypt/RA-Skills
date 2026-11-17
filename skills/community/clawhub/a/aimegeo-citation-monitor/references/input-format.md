# 输入格式与统计口径

脚本接受一个 UTF-8 JSON 对象。由 Agent 从用户导出材料转换，不要求用户手写全部字段。原文、原生引用和采集事实保持不变；无法确定的信息用下述未知值表达，不猜测。

## 顶层配置

| 字段 | 类型与含义 |
| --- | --- |
| `schema_version` | 整数 `1` |
| `dataset_kind` | `observed`：用户提供或实际采集的真实记录；`simulated`：演示或合成数据。不能为获得百分比把合成记录标为真实 |
| `brand.name` | 目标品牌完整名称 |
| `brand.aliases` | 可选字符串列表；仅加入用户确认指向该品牌的称呼 |
| `brand.domains` | 至少一个归属域名；仅主机名，无协议、路径、端口或通配符。使用 `idna` 的非过渡 UTS #46／IDNA2008；`faß.de` 与 `xn--fa-hia.de` 等价，与 `fass.de` 不同 |
| `brand.include_subdomains` | 可选布尔值，默认 `true`；允许 `docs.example.com` 匹配 `example.com` |
| `platforms` | 去重的平台 ID 字符串列表；平台 ID 必须代表实际服务，不能把同一个服务包装成多个平台 |
| `queries` | 非空问题数组，各含唯一 `id`、完整 `text`、`category`；可选 `priority` 为 `normal`／`high`／`critical`，`expected_native_citation` 为布尔值（默认 `false`） |
| `runs` | 非空批次数组，每批含唯一 `id`、有时区的 `started_at`、`records` 数组 |

每个批次共计划 `len(platforms) × len(queries)` 条记录。所有批次使用同一份计划，未给的计划项自动生成 `not_run`。若平台范围或问题计划变化，分别运行分析并由 Agent 解释差异；不能把不存在的原计划凭空补成旧批次计划。分类和预期引用仅帮助分组与排查，不是“应该被引用”的事实证据。

时间采用带时区的 ISO 8601，例如 `2026-10-08T09:00:00+08:00`。历史按批次开始时间排序；按类别／平台分别汇总各批次。批次可代表一天，也可代表一次人工复测；脚本不猜日期分组、不读取隐藏缓存。

## 每条记录

| 字段 | 规则 |
| --- | --- |
| `platform`、`query_id` | 必须在计划内，同批次同平台同题只允许一条；重复／重试用新批次保留 |
| `status` | `success`、`error`、`timeout`、`not_run` 或 `simulated` |
| `query` | 成功／模拟记录必填：实际发送的完整题文。题目变了也保留原文，不能改成计划题文来配对 |
| `answer` | 成功／模拟必填，非空的原始回答文本；不包括用户提示词。失败／未运行不得填回答 |
| `citations` | 成功／模拟必有此键：原生引用列表，或 `null` 表示未取得。列表项可为 URL 字符串或含 `url` 的对象；其他原生字段原样保留。URL 须为无用户信息的绝对 HTTP(S) 地址 |
| `collected_at` | 成功／模拟必填：有时区的实际采集时间；模拟样例中只是演示时刻 |
| `conditions` | 成功／模拟必填：`model`、`search_mode`、`context`，均为非空字符串。未知填写字面值 `unknown` |
| `source` | 除 `not_run` 外必填；`not_run` 可省略或为 `null`，此时报告显示“无采集来源”。提供对象时所有状态均须含合法 `kind`（`export`／`api`／`browser`／`simulation`）、非空 `executor`（真实执行器或 `unknown`）和非空 `reference`（例如导出文件及记录 ID）；不完整或非法来源退出 2 |
| `reason` | `error`／`timeout`／`not_run` 必填；模拟可选。只写实际观察到的原因，不猜网络、账号或平台故障 |

`context` 建议用 `fresh` 表示新会话；复用上下文时用已核实的完整前置消息快照标识。同一会话 ID 不能证明两次上下文相同。不确定则填 `unknown`，本批指标仍可用，但排除前后配对。`search_mode` 记录实际联网／搜索开关或模式名称，不能把联网设置不明标为已开启。

证据引用使用用户可回读的文件记录号或私有证据别名。不要把凭据、Cookie、浏览器环境标识或私密分享链接写进公开交付。脚本保留整个 `raw_record`；转换时先确认原始记录中只含本次分析所需的资料。

一个可直接试用的最小输入（**模拟**，无真实采集）：

```json
{
  "schema_version": 1,
  "dataset_kind": "simulated",
  "brand": {"name": "青禾工具", "aliases": ["青禾"], "domains": ["example.com"]},
  "platforms": ["demo-platform"],
  "queries": [{"id": "q1", "text": "青禾工具是什么？", "category": "品牌"}],
  "runs": [{
    "id": "demo",
    "started_at": "2026-10-08T09:00:00+08:00",
    "records": [{
      "platform": "demo-platform",
      "query_id": "q1",
      "query": "青禾工具是什么？",
      "status": "simulated",
      "collected_at": "2026-10-08T09:00:00+08:00",
      "source": {"kind": "simulation", "executor": "offline-fixture", "reference": "fixture:q1"},
      "conditions": {"model": "demo-model", "search_mode": "demo-search", "context": "fresh"},
      "answer": "青禾工具是演示中虚构的知识整理产品。",
      "citations": [{"url": "https://example.com/guide", "title": "模拟说明页"}]
    }]
  }]
}
```

## 如何计数

| 指标 | 分子 | 分母／未知规则 |
| --- | --- | --- |
| 提及率 | 真实有效回答中至少命中一个品牌名／别名的回答数 | 真实 `success` 回答数；无有效回答则计数和比率均为 `null` |
| 原生域名引用率 | 原生列表至少一个 URL 匹配归属域名的回答数 | 真实成功且 `citations` 为列表的回答数；全部 `null` 则 N/A |
| 同题提及变化 | 配对后两侧各自提及计数、增失 | 两侧均真实成功，且比较条件一致已知的配对数 |
| 同题引用变化 | 配对后两侧各自引用计数、增失 | 在上述配对中，两侧 `citations` 都为列表的配对数 |

一次回答多次提及或多个官网引用均只贡献一个回答计数。无提及也可能有官网引用，两者独立。引用率分母不是“已提及数”，JSON 字段 `native_citation_rate` 与报告使用同一口径。

品牌匹配对回答做 Unicode NFKC 与大小写归一化；英文／数字别名检查词边界，中文按连续文字匹配。它是显式文本命中，不能自动消除同名歧义、判断正面情绪或识别所有语义指代。Agent 应复核过短或歧义别名，报告按用户确认的配置统计。

引用只解析 URL 的主机名。`evil-example.com`、`example.com.evil.invalid`、其他站点路径或查询参数里的 `example.com` 均不匹配。URL 不发请求，重定向不展开；第三方原生引用可保留但不算官网域名命中。正文链接不等于平台原生引用。`first_native_position` 是原生列表首个匹配位置（从 1 起），不是回答中的名次；原生列表无可靠顺序时由 Agent 说明该位置没有排序含义。

`dataset_kind: simulated` 中的成功记录统一转为模拟状态；单条 `status: simulated` 也不会进入真实分母。模拟命中仅见 `simulation_preview`，正式的 `mentioned`／`native_cited` 等为 `null`。错误、超时、未运行记录同样不填布尔零引用。

## 比较与交付

`--before` 和 `--after` 必须一起提供，指向存在的批次，且前者时间早于后者。完整题文、平台、来源种类／执行器及 `model`／`search_mode`／`context` 必须一致；未知模型、上下文、搜索或执行器排除配对。两侧原生引用未知时只排除引用比较，仍可比较提及。

`comparison.mention` 和 `comparison.native_citation` 各有 `paired`、`before_count`、`after_count`、`gained`、`lost`、`delta_percentage_points`。百分点为 `(after_count - before_count) / paired × 100`，不是相对增长百分比。配对数为 0 时所有计数／比率／变化均为 `null`，不是“无变化”。每个问题的两种比较结果与各自排除原因见 `comparison.pairs`。

三份产物固定为：

- `前后对照报告.md`：历史、平台／类别表、同题比较、逐项来源和限制；无批次选择时保留历史汇总。
- `逐平台问题结果.json`：全部统计及逐项 `raw_record`、匹配引用、来源、原因和配对；可追溯到用户导出记录。
- `未成功采集清单.md`：错误、超时、未运行、模拟，以及成功但引用未知的记录；引用未知项仍保留提及结果。

输入错误退出码为 2，包括重复 JSON 键、重复记录、未计划平台／问题、非法域名／引用 URL、缺少引用键、空成功回答及缺少采集来源。任意层级的数字（包括原生引用的额外字段）须为有限值；`NaN`、`Infinity`、`-Infinity` 以及 `1e309` 等溢出为非有限值的指数均拒绝。不会用错误输入生成业务报告或改动已有输出。输出目录非空也退出 2，保留原文件。全采集失败是合法业务结果，仍退出 0 并交付 N/A 报告。
