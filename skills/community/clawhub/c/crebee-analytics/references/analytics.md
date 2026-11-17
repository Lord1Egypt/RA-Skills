# 发布数据分析

## 先判断统计口径

CreBee 的数据分析分为两种互不替代的模式。先根据用户问题选择模式，不要把两类指标相加、互算环比或写成同一种数据。

### 账号经营与生涯视角

使用平台的 `DataOverview` 查看账号资产、长期经营位置和账号间差异。适合回答“哪个账号长期表现更好”“账号整体盘子如何”“各账号有什么长期优势”。

不同平台的 `DataOverview` 并不都等于历史累计：有的平台返回历史累计，有的平台只提供 7/30/90 天，有的平台接受起止日期，还有的平台在同一响应中混合累计值和昨日值。CLI 会在报告每个账号的数据源中保存真实周期说明，HTML 也会逐账号展示。形成结论时必须使用该说明，不能统一写成“全生命周期累计”。平台概览通常按日更新，完整数据常截止昨日，具体以报告标注为准。

### 周期发布作品即时表现

先按发布时间筛选一个范围内的发布记录，再尽量调用平台 `SingleDataOverview` 类能力获取这些作品截至查询时的最新累计数据。适合回答“最近 30 天发的内容现在表现怎样”“哪些账号、平台和选题更好”“下周期应该验证什么”。

这里的“30 天播放”表示“最近 30 天发布的作品截至现在的累计播放”，不是这 30 天内新增的播放。平台可能不允许查询很久以前的作品；CLI 会保留发布记录快照作为回退，并在 `instantCoverage` 中标明即时查询成功、空数据、失败和回退数量。

## 负数指标口径

部分平台返回的是标注统计周期内的**净变化**，不是绝对累计总量。此类指标出现负数时，表示该指标在这段时间内减少，不能写成“总量为负”或“数据异常”。

- 收藏为 `-12`：这段时间取消收藏数量比新增收藏数量多 12。
- 点赞为 `-5`：这段时间取消点赞数量比新增点赞数量多 5。

保留负号并按“净减少”解释；不要归零、取绝对值后当作新增，也不要据此断言平台接口错误。若无法从 `semantics`、`fieldGuide` 或事实句确认某字段是净变化还是绝对值，必须如实说明口径不明，不能自行套用这条解释。

## 使用顺序

1. 用户未限制账号范围时默认分析全部已连接账号；用户点名账号但无法唯一定位时，运行 `accounts list --status connected` 并让用户选择准确账号。
2. 取数前固定询问下列展示方式和数据范围。两个问题放在同一条消息中，展示方式必须排在第一；用户已经明确的选择不要重复询问。

   **问题 1：报告怎么展示？**
   - A. **CreBee 内置模板（推荐）**：生成快、样式统一，图表和运营点评位置固定，适合直接查看和汇报。
   - B. **由当前 Agent 自定义生成**：可以自由调整布局、指标和分析方式，但生成时间更长、消耗的 Token 更多。

   **问题 2：想分析哪类数据？**
   - A. **综合分析**：同时查看账号长期经营情况，以及近 30 天发布内容在平台上的最新表现。
   - B. **账号经营数据**：查看账号长期经营状态、粉丝、受众和收益。平台通常每天 12 点左右更新昨日数据，具体统计周期会在报告中标明。
   - C. **发布记录数据**：按发布时间筛选内容，并读取这些内容在平台当前的最新数据快照。时间范围决定选择哪些作品，不代表这段时间新增了多少播放或互动。

   提示用户按 `1A，2A` 这种格式回答，不要把“模板还是原始数据”改写成没有优缺点的开放式问题。

3. 只有问题 2 选择 C 时，继续询问问题 3；选择 A 时固定使用近 30 天发布记录，选择 B 时不询问时间。

   **问题 3：想查看哪个时间范围？**
   - A. 近 7 天。
   - B. 本月：本月 1 日至今天。
   - C. 本季度：本季度首日至今天。
   - D. 今年：当年 1 月 1 日至今天。
   - E. 自定义时间：继续询问开始日期和结束日期。

4. 必要选择未确定前不得执行取数命令。根据选择使用下方确定映射，不要自行发明模式、模板或范围：
   - `1A + 2A`：`analytics report --template operations-dashboard`
   - `1A + 2B`：`analytics report --template account-lifecycle-dashboard`
   - `1A + 2C`：`analytics report --template publication-period-dashboard`，附加问题 3 对应的范围。
   - `1B + 2A`：`analytics report --mode combined --range 30d --output data`
   - `1B + 2B`：`analytics report --mode account-lifecycle --output data`
   - `1B + 2C`：`analytics report --mode publication-period --output data`，附加问题 3 对应的范围。

   问题 3 选择近 7 天时使用 `--range 7d`；本月、本季度、今年和自定义时间都换算为用户本地日期的 `--start YYYY-MM-DD --end YYYY-MM-DD`。

5. 检查 stdout 的 `status`、`warnings`、`errors`、`callBudget` 和 `nextAction`。出现错误时停止业务调用，并按 [troubleshooting.md](troubleshooting.md) 处理。
6. 使用模板时，读取 `artifacts.commentaryBrief`，只基于各 section 的证据生成局部点评；使用 `--output data` 时直接读取 `artifacts.data`。
7. 模板路径下把点评写入 `artifacts.commentaryDraft` 后执行 `analytics commentary`，由 CLI 安全地放入对应图表右侧。

`analytics report` 会按所选模式一次获取全部相关维度。不要先生成简版报告，也不要自行追加第二轮分析命令。

所有命令中的 `<skill-directory>` 都表示当前 Skill 根目录的真实绝对路径，由宿主按自身的 Skill 资源定位方式解析。

## 三种 HTML 看板

需要核对模板能力时可以查看模板列表；该命令不请求业务接口，不消耗调用次数：

```text
crebee analytics templates
```

### 综合运营决策看板

```text
crebee analytics report --template operations-dashboard
```

同时生成账号经营概览和近 30 天发布作品即时表现，两部分使用独立标题和口径说明。作品区域可在 HTML 中切换近 7 天与近 30 天，切换不会再次调用接口。

### 账号经营与生涯看板

```text
crebee analytics report --template account-lifecycle-dashboard
```

一次获取账号概览和账号趋势等平台实际支持的经营数据，不请求发布记录。该模式的周期由平台能力决定，不接受 `--range`、`--start`、`--end` 或 `--compare`。报告必须逐账号说明真实统计周期和数据新鲜度。用户画像、受众分布和收益数据不在看板中展示，需要时用 `--output data` 取原始数据自行解析。

### 周期发布表现看板

```text
crebee analytics report --template publication-period-dashboard
crebee analytics report --template publication-period-dashboard --range 7d
crebee analytics report --template publication-period-dashboard --start 2026-08-01 --end 2026-08-24
```

默认获取近 30 天，也接受问题 3 选择的时间范围。CLI 按发布时间筛选发布记录，并对可查询作品补充平台当前最新数据。所选范围超过 7 天时，HTML 可切换近 7 天与完整所选范围；切换不会再次调用接口。Top 作品深度数据和互动反馈不在看板中展示，需要时用 `--output data` 获取。

## 不生成 HTML 时的模式

只获取账号经营数据：

```text
crebee analytics report --mode account-lifecycle
```

获取自定义发布时间范围内的作品及其即时数据：

```text
crebee analytics report --mode publication-period --start 2026-08-01 --end 2026-08-24
```

同时获取两种口径：

```text
crebee analytics report --mode combined --range 30d
```

指定账号或平台时可添加：

```text
--accounts "账号ID1,账号ID2"
--platforms "douyin,xiaohongshu"
```

账号 ID 必须来自 `accounts list`，不能用账号名称代替。

## 交给 Agent 自建展示

用户选择由当前 Agent 生成展示报表时，在任意 `--mode` 后追加 `--output data`：

```text
crebee analytics report --mode publication-period --range 30d --output data
crebee analytics report --mode account-lifecycle --output data
crebee analytics report --mode combined --output data
```

取数过程、调用预算和平台覆盖判断与生成报告完全一致，但 CLI 不做聚合和渲染。`artifacts.data`（`analytics-data.json`）是唯一数据源：

- `accounts[].sources`：账号生涯视野。逐账号逐来源的归一化指标、事实句和平台特有结构，`semantics` 是该来源的真实统计周期与新鲜度声明。
- `contentRecords`：发布记录视野。全量作品记录（每账号最多 50 条），指标已被即时数据覆盖的作品使用最新快照。
- `previous`：仅在传了 `--compare previous` 时存在，是上一周期 content 维度的原始结果。
- `dataQuality`、`failures`、`warnings`、`callBudget`：数据质量、失败明细与真实调用次数。
- `fieldGuide`：文件自带的字段字典。归一指标的中文含义、`contentRecords` 各字段说明，以及 `platformDetails` 的解读纪律——它是平台原生键名的压缩结构，各平台键不同，不确定时以 `metrics` 和 `facts` 为准，不要按字段名猜含义。

约束：

- `--output data` 与 `--template` 互斥；用户需要先明确选择展示方式。
- 数据只提供一次，不要再次运行取数命令；缺失范围按 `dataQuality` 和 `failures` 如实说明。
- 展示报表的统计口径必须沿用每个来源的 `semantics`，不要把账号经营指标和周期作品即时指标混算。

## Agent 分区点评

使用模板生成报告后会得到：

- `commentary-brief.json`：每个点评槽位的任务、允许使用的证据引用和已聚合证据。
- `commentary-draft.json`：Agent 应填写的结构化输出骨架。
- `report.html`：未填写点评时仍可直接查看，右侧显示 CLI 的确定性数据解读。

Agent 只读取 brief 中需要的 section，不要加载全部原始响应。填写每个需要点评的槽位：

- `headline`：一句明确结论。
- `observations`：1 到 3 条直接对应证据的观察。
- `comparison`：口径、样本或跨平台比较边界；没有时删除该字段。
- `action`：可验证的下一步；没有足够证据时删除该字段。
- `confidence`：只允许 `high`、`medium`、`low`。
- `evidenceRefs`：只能使用当前槽位列出的引用。

完成后执行：

```text
crebee analytics commentary --run "<runId>" --input "<commentary-draft.json 的绝对路径>"
```

该命令不请求平台数据、不消耗调用次数。CLI 会校验 runId、槽位、证据引用、长度和结构，转义文本后把局部点评放在对应客观图表右侧。`executive` 只用于跨两个以上模块才能成立的总体概览，不能重复所有局部结论。

禁止行为：

- 不把账号经营指标和周期作品即时指标相加或互相计算增长率。
- 不让点评引用其他槽位没有提供的证据。
- 不输出 HTML、脚本或样式到点评文件。
- 不把跨平台相关性写成平台优劣、算法规律或因果关系。

## 调用次数与作品覆盖

周期模式先按账号查询一次发布记录，再补充作品即时数据。每个账号最多处理 50 条可查询作品；`content-detail` 可能包含单作品趋势等高成本接口，因此固定对播放/阅读最高的 3 条作品执行深度分析。这个上限由 CLI 控制，Agent 不传数量参数。

账号经营模式会请求账号概览、趋势、受众和收益；周期发布模式会请求发布记录、作品即时数据、Top 作品深度数据和互动反馈；综合模式执行两者并自动复用同一个平台接口能够同时提供的结果。**例外：使用 HTML 模板时只请求核心维度**（受众画像、收益、互动反馈、Top 作品深度都不请求也不展示），需要这些数据时用 `--output data` 获取。平台未提供某个维度时记录到 `capabilityCoverage.unsupported`，不把“不支持”伪装成请求失败。

不同平台的即时接口和深度接口批量能力不同，因此真实调用次数必须读取 CLI 返回的 `callBudget`，不要自行按作品数量估算。没有作品 ID、平台不支持或较早作品无法查询时，报告会区分 warning、失败和发布记录回退。

## 报告字段与数据质量

优先读取 `report.md` 或 `report.json`，只有核对具体记录时才读取脱敏后的 `raw-<platform>.json`。

- `mode`：当前统计模式。
- `range`：周期发布记录的发布时间范围；账号经营模式中不代表所有平台的真实概览周期。
- `overall`、`byAccount`、`byPlatform`、`topContents`：仅由周期发布作品数据形成。
- `accounts[].sources[].semantics`：每个数据源的真实数据集、周期、新鲜度和截止时间说明。
- `dataQuality.instantCoverage`：可查询作品、已请求、成功、失败、不可用和回退数量。
- `accountCoverage`、`capabilityCoverage`：账号成功/失败和平台能力支持范围。
- `callBudget`：预计、完成和失败调用数。

`empty` 表示请求成功但没有业务数据；`partial` 表示部分请求失败。失败不能改写成“没有数据”，发布记录回退也不能写成即时接口成功。

## 形成结论

面向运营负责人输出时按以下层级组织：

1. 总体概览：只写跨多个模块共同支持的判断。
2. 账号经营：逐账号说明真实周期，再比较资产规模或长期位置。
3. 周期发布：比较作品总量、单条效率、账号、平台和内容方向，明确这是当前累计快照。
4. 局部建议：紧贴对应图表，给出证据、边界、置信度和下一步验证动作。
5. 数据质量：说明失败、空数据、即时覆盖和回退范围。

策略建议用于缩小下一周期的验证范围，不是平台算法结论。样本不足时降低置信度；跨平台指标口径不同，应优先在同平台、同账号类型和相近内容形式内复核。
