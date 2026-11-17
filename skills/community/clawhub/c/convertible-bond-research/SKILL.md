---
name: convertible-bond-research
description: 以可转债为切入点的企业综合研究工作流。当用户要求研究可转债、筛选转债、分析下修/强赎博弈、做转债投资分析、或从转债角度研究一家企业时使用此 skill。覆盖从转债筛选、单券深度分析、下修博弈评估、正股业务、行业可比、行业周期、正股估值到投资小结的完整链条。关键词：可转债研究、转债筛选、下修分析、强赎博弈、转股溢价率、纯债价值、正股估值、PE PB 历史分位、隐含波动率、转债投资小结、anchor-bond。
agent_created: true
---

# Convertible Bond Research

## Overview

以可转债为切入点对企业做综合研究的工作流。核心思路：可转债条款（下修/强赎/回售）往往是企业基本面和资本运作意图的高信号线索，从转债切入能快速锁定有事件催化或基本面边际变化的标的，再延伸到正股业务和行业周期，最终形成"转债博弈 + 正股基本面 + 行业周期"三位一体的投资判断。

适用场景：用户给出一批筛选条件找转债、点名研究某只转债、问某转债下修/强赎可能性、要求做转债或正股的投资小结。

## Prerequisites

本技能的 Step 1-3 和 Step 7 转债视角依赖 `anchor-bond` MCP 提供转债结构化数据。开始工作流前必须确认已安装并启用。

### 检测方法

用 ToolSearch 加载 `mcp__anchor-bond__bond_list`。如果工具不可用，或连接器状态显示 `anchor-bond: disconnected`，说明未安装或未启用，按下方步骤引导用户安装后再继续。

### 安装步骤

引导用户完成以下 4 步：

1. **获取 API 密钥**：登录 [anchor-data.cn](https://www.anchor-data.cn)，进入「API 密钥」页面（`/api-keys`），点击生成，拿到格式为 `anchor_xxxxxx` 的密钥。⚠️ 明文只显示一次，需立即复制保存。每账号最多 3 把密钥，限速 30 次/分钟。

2. **配置 MCP**：读取 `~/.workbuddy/mcp.json`（若不存在则新建），将以下配置合并到 `mcpServers` 中（勿覆盖已有服务器）：

```json
{
  "mcpServers": {
    "anchor-bond": {
      "url": "https://api.anchor-data.cn/api/mcp",
      "headers": {
        "Authorization": "Bearer anchor_xxxxxx"
      }
    }
  }
}
```

3. **启用连接器**：配置写入后不会自动激活。引导用户打开 WorkBuddy 右上角连接器管理页面，找到 `anchor-bond`，点击「Trust」启用。

4. **验证**：启用后重新调用 `mcp__anchor-bond__bond_list`（无参数即可），确认返回转债数据正常。

详细安装指南参见 [锚点数据 MCP 介绍](https://www.anchor-data.cn/blog/anchor-mcp-intro)。

## Workflow

按以下 8 步推进，根据用户需求可跳过或合并步骤。每一步产出阶段性结果，最终整合为投资小结。

### Step 1: 转债筛选（bond_list）

⚠️ 开始前先确认 anchor-bond MCP 已安装并启用（见 Prerequisites）。如果工具不可用，暂停工作流，引导用户完成安装后再继续。

用 `mcp__anchor-bond__bond_list` 按条件筛选全市场可转债。常见筛选维度：

- 条款状态：`filters.repairStatuses`（下修）、`filters.redeemStatuses`（强赎），取值 `COUNTING`/`PROPOSED`/`NOT_TRIGGERED`/`POSTPONED`
- 价格：`filters.priceMax` / `priceMin`（单位：元）
- 规模：`filters.balanceMax` / `balanceMin`（单位：**亿元**，不是元）
- 剩余期限：`filters.remainDaysMin` / `remainDaysMax`（单位：天，半年=183）
- 评级：`filters.ratingMin` / `ratingMax` 或 `filters.creditRatings` 白名单
- 行业/地域：`filters.industry` / `filters.provincialName`

排序用 `sort.field`（如 `currentPrice`/`transferPremiumRatio`/`expireYield`）+ `sort.order`。`pageSize` 上限 50。结果默认按转股溢价率升序（最便宜在前）。

产出：符合条件的转债列表，重点标注触发进度最高、价格最低、规模最小的标的。

### Step 2: 单券深度分析（bond_lookup + bond_terms + bond_detail）

对重点标的并行拉取三类数据：

- `mcp__anchor-bond__bond_lookup`（6位代码）：单券快照，含现价/转股价值/溢价率/YTM/纯债价值/期权价值/评级/剩余规模/剩余天数/下次付息日等 20+ 指标。
- `mcp__anchor-bond__bond_terms`（代码数组，最多20只）：条款摘要，含强赎/下修/回售触发状态字符串、转股期、触发价。
- `mcp__anchor-bond__bond_detail`（代码 + scopes）：深度数据。scopes 可选 `bondTopHolders`（十大持有人，含多季度）、`transferPriceHistory`（转股价调整历史）、`rate`（票息结构）、`indicator`（日度技术指标）。

⚠️ `bond_detail` 返回数据量大（常超 10 万字符），会自动落盘到 tool-results 目录。用 Grep 定位 section（`"transferPriceHistory":` / `"rate":` / `"indicator":` 等行号），再用 Read 分块读取。十大持有人取最新季度（`endDate` 最大的一组）。

条款触发状态格式 `N/M|K`：N=已连续达标天数，M=窗口期天数，K=需达标天数。触发进度 = N/K。状态 `COUNTING`=计数中，`PROPOSED`=已公告，`NOT_TRIGGERED`=未触发。

产出：单券详细分析报告（HTML），含档案卡、三大条款进度条、估值收益、转股价历史、票息、十大持有人、近期走势图。

### Step 3: 下修/强赎博弈评估

对下修或强赎做多因素定性概率评估。详见 `references/bond-analysis-framework.md` 的评估模型。

核心框架——下修三阶段概率：
1. 条款触发：看触发进度 N/K，正股价 vs 触发价的缺口
2. 董事会提议：看动机（偿债压力/回售压力/亏损）vs 压制（无下修先例/周期性）
3. 股东大会通过：看大股东配合度（需 2/3 通过，持债大股东回避表决）

支持/压制因素清单：触发进度、回售期临近、偿债压力、剩余期限、下修先例、大股东配合度（待验证）、每股净资产限制下修底价（待验证）、行业周期性。

产出：概率评估可视化（评分卡 + 三阶段概率条 + 因素表），给出综合实施概率区间。

### Step 4: 正股业务分析（WebSearch）

anchor-bond 不覆盖正股基本面，用 WebSearch 补充。查询模板：`<公司名> <代码> 主营业务 产品 产业链`。

提取要点：成立时间/上市时间/总部、主营产品及营收占比、产业链位置、产能规模、下游应用、最新年报营收/净利/现金流、特色（如循环经济/技术优势）。

关联到 Step 3：正股亏损/现金流承压会增强下修动机（"被动还债痛感"）。

### Step 5: 行业可比公司（WebSearch）

查询模板：`<行业> 上市公司 产能排名 <年份>`。按产能/规模排序全部同行，按可比性分档：

- **强可比**：产能/规模接近、业务结构相似、纯同业
- **中可比**：业务结构可比但规模差异大
- **弱可比/行业锚点**：体量差大或业务多元，仅用于判断行业方向

标注各家最新营收/净利/产能/市值，重点对比目标公司与强可比公司的经营处境。

### Step 6: 行业周期与需求结构（WebSearch）

行业周期三维分析：
- **价格**：年度均价走势，定位周期高低点。查询 `<行业> 价格走势 <年份范围> 元/吨`
- **产能产量**：产能利用率反映过剩程度。查询 `<行业> 产能 产量 产能利用率 <年份>`
- **企业利润**：主要上市公司年报利润对比。查询 `<行业龙头> <公司> 年报 营收 净利润`

需求结构拆解：下游各领域占比，标注哪些绑定核心驱动（如钛白粉 60% 绑涂料、24% 直接绑地产）。查询 `<行业> 下游需求结构 应用占比`。

周期定位：判断当前处于"高点/回落/底部/回升"的哪个阶段，以及回升的性质（需求驱动 vs 成本倒逼/供给收缩）。

### Step 7: 正股估值分析（westock-data + WebSearch）

对正股做相对估值，结合 Step 5 的可比公司和 Step 6 的周期定位，判断正股当前估值贵贱。详见 `references/stock-valuation-framework.md`。

四个分析维度：

1. **横向对比**：正股 vs 强可比公司的 PE-TTM / PB / PS-TTM / EV-EBITDA，计算折溢价。低 ROE 但高 PE = 贵；高 ROE 低 PE = 便宜
2. **纵向分位**：当前 PE/PB vs 自身 3 年/5 年历史分位（westock-data 获取）。<20% 为低位，>80% 为高位
3. **周期调整**：结合 Step 6 周期定位解读估值——周期底部低 PE 可能是价值陷阱，底部高 PE 可能是反转信号。周期品优先看 PB 和 EV/EBITDA，PE 容易反向
4. **转债视角**：转股价值与溢价率（anchor-bond 已提供）、隐含波动率（BS 反推 vs 正股历史波动率）、期权价值占比对比

⚠️ 亏损企业 PE 不适用，改用 PB/PS。westock-data 不可用时降级用 WebSearch 查估值数据。

产出：估值评分卡（横向/纵向/周期调整/转债视角四维），给出正股估值【便宜/合理/偏贵】判断 + 合理价格区间 + 对转债价格的影响。

### Step 8: 投资小结整合

将前 7 步成果整合为投资小结（HTML）。结构：

1. **投资摘要**：一段话结论 + 四个判断卡（正股/转债/事件概率/估值）
2. **标的速览**：正股+转债关键指标对照表
3. **估值评分卡**：横向对比/纵向分位/周期调整/转债视角四维，合理价格区间
4. **多空因素**：绿色多头逻辑卡 + 红色空头风险卡
5. **核心催化剂**：下修/强赎博弈专题（三阶段概率图）
6. **情景分析**：乐观/中性/悲观三档，各给概率和价格区间
7. **行业背景**：周期位置一句话
8. **关注节点与监测指标**：事件时间线 + 持续跟踪指标
9. **结论**：适合的投资者类型 + 操作建议（风险预算、仓位）

报告用 Chart.js 画图（概率柱状图、走势线等），中国股市惯例：涨红跌绿。

## Key Tools

- `mcp__anchor-bond__bond_list`：全市场筛选
- `mcp__anchor-bond__bond_lookup`：单券快照（6位代码）
- `mcp__anchor-bond__bond_terms`：批量条款状态
- `mcp__anchor-bond__bond_detail`：深度数据（落盘后 Grep+Read 分块）
- `mcp__anchor-bond__bond_search`：按债券简称查代码
- `westock-data` skill：正股估值数据（PE/PB/PS/EV-EBITDA、历史分位、波动率），Step 7 加载
- `WebSearch`：正股基本面、行业数据、可比公司、估值语境

## Resources

### references/
- `bond-analysis-framework.md`：可转债分析框架详解——anchor-bond 工具参数、条款术语、下修评估多因素模型、估值指标含义、情景分析框架。做 Step 2-3 时加载参考。
- `industry-research-framework.md`：行业研究框架——周期分析维度、需求结构拆解法、可比公司分档法、WebSearch 查询关键词模板。做 Step 5-6 时加载参考。
- `stock-valuation-framework.md`：正股估值框架——westock-data 查询模板、相对估值指标适用场景、横向对比与纵向分位方法、周期调整估值解读、转债视角估值（隐含波动率/期权价值）、估值评分卡输出格式。做 Step 7 时加载参考。

## Notes

- anchor-bond 只覆盖转债侧，正股基本面（大股东结构/BPS/现金流）必须用 WebSearch 补充，这些是下修概率的关键修正项。
- 正股估值（Step 7）依赖 Step 5 可比公司和 Step 6 周期定位，不可跳级。亏损企业 PE 不适用改用 PB/PS；周期品优先看 PB 和 EV/EBITDA，PE 容易反向。westock-data 不可用时降级用 WebSearch。
- 投资小结必须含"待验证项"说明，诚实标注哪些关键变量未覆盖，避免给出过度确定的判断。
- 所有报告为研究参考，不构成投资建议，需在页脚标注风险提示。
