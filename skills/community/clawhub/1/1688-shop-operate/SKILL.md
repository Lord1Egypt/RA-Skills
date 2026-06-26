---
name: 1688-shop-operate
description: |
  1688 店铺经营健康诊断 —— 全面诊断店铺经营健康状况。
  工具能力：核心指标对比同行同层、流量结构分析、行业交易排名、客户画像分析，自动识别瓶颈并给出改善建议。
  触发词：店铺诊断、经营诊断、健康诊断、店铺分析、经营分析、店铺健康。
metadata: {"openclaw": {"emoji": "🏥", "requires": {"bins": ["python"]}}}
---

## 环境准备

统一入口：`python3 {baseDir}/cli.py <command> [options]` 尽量使用绝对路径执行脚本

### Windows 权限问题（仅 Windows 用户需要）

若 skills 目录缺少执行权限（提示"拒绝访问"），需先将目录拷贝到 workspace 再操作：

```cmd
xcopy /E /I /Y "<skills目录路径>" "%USERPROFILE%\workspace\1688-auth-skill-for-wukong"
cd /d "%USERPROFILE%\workspace\1688-auth-skill-for-wukong"
```

> `/E` 递归复制所有子目录，`/I` 目标不存在时自动创建，`/Y` 覆盖时不询问确认。
> 拷贝完成后，后续所有命令均在 workspace 路径下执行。

首次使用前，在项目根目录执行：

```bash
pip install -r requirements.txt
# 若上述命令不可用，尝试：
pip3 install -r requirements.txt
```
依赖列表：仅使用 python3 标准库，无需额外安装第三方包。

## AK 安全说明

> ⚠️ **AK 是访问 1688 接口的唯一凭证，请妥善保管，避免泄漏。**

- AK 在本地以**设备绑定加密**方式存储（PBKDF2 派生密钥 + 流加密 + HMAC 校验），加密文件拷贝到其他机器后**无法解密**
- 不要将 AK 明文粘贴到聊天记录、截图、日志或版本控制中
- 不要将 `ak_store.json` 或 `.device_id` 上传到任何云端或共享目录
- 如怀疑 AK 已泄漏，立即执行 `cli.py configure --clear` 清除本地存储，并前往 [clawhub.1688.com](https://clawhub.1688.com/) 重新获取

## 命令速查

### AK 管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `get_ak` | 获取AK | `cli.py get_ak` |
| `set_ak` | 手动设置AK（已有 AK 时使用） | `cli.py configure YOUR_AK` |
| `reset_ak` | 重置AK | `cli.py configure --reset YOUR_NEW_AK` |
| `clear_ak` | 清除AK | `cli.py configure --clear` |
| `status_ak` | 检查AK状态 | `cli.py configure --status` |

### 店铺经营健康诊断

| 命令 | 说明 | 示例 |
|------|------|------|
| `get_core_metrics` | 获取店铺核心指标同行对比及趋势数据 | `cli.py get_core_metrics -d RECENT_7` |
| `get_traffic_structure` | 获取店铺流量结构数据 | `cli.py get_traffic_structure -d RECENT_7` |
| `get_transaction_ranking` | 获取行业交易排名数据 | `cli.py get_transaction_ranking -d RECENT_7` |
| `get_customer_profile` | 获取客户画像数据 | `cli.py get_customer_profile -d RECENT_7` |

所有命令输出 JSON：`{"success": bool, "markdown": str, "data": {...}}`

**展示时直接输出 `markdown` 字段，Agent 分析追加在后面，不得混入其中。**

## 使用流程

Agent 根据用户意图**直接执行对应命令**。
各命令在 AK 缺失等情况下会自行返回明确错误，Agent 按下方「异常处理」应对即可。

**店铺健康诊断使用指引**：
- 当用户要求店铺诊断、经营分析、同行对比时，需并行调用以下 4 个命令获取数据：
  - `get_core_metrics` — 核心指标同行对比及趋势
  - `get_traffic_structure` — 流量结构分析
  - `get_transaction_ranking` — 行业交易排名（⚠️ 仅支持 RECENT_7 / RECENT_30）
  - `get_customer_profile` — 客户画像
- 公共可选参数：
  - `--date_type` / `-d`：日期类型，默认 `RECENT_7`
  - `--device` / `-v`：设备类型，默认 `ALL`
- 获取数据后由 LLM 综合分析生成诊断报告，详见下方「店铺健康诊断流程」

## 数据查询命令详细说明

### get_core_metrics — 核心指标同行对比及趋势

```bash
python3 {baseDir}/cli.py get_core_metrics [--date_type <DATE_TYPE>] [--device <DEVICE>]
```

**返回字段映射**：

| 返回区块 | 含义 | 用途 |
|---------|------|------|
| `core_metrics` | 7项核心指标的本店值、同行同层平均、评级（优秀/持平/略低/极低） | 快速定位落后指标 |
| `trend` | 各指标的环比、同期对比、较同行变化率 | 判断趋势方向 |

**core_metrics 中的 metric_code 取值**：

| metric_code | 指标名 |
|-------------|--------|
| `impression` | 展现次数 |
| `visitor` | 访客数 |
| `page_view` | 浏览量 |
| `click_cvr` | 点击转化率 |
| `pay_cvr` | 支付转化率 |
| `buyer_count` | 支付买家数 |
| `pay_amount` | 支付金额 |

**rating 评级含义**：

| 评级 | 含义 | ratio_to_peer 参考范围 |
|------|------|----------------------|
| 优秀 | 高于同行同层平均 | >= 1.1 |
| 持平 | 接近同行同层平均 | 0.9 - 1.1 |
| 略低 | 低于同行同层平均 | 0.5 - 0.9 |
| 极低 | 远低于同行同层平均 | < 0.5 |

**trend 字段结构**：

| 子字段 | 含义 | 计算基准 |
|--------|------|---------|
| `year_on_year` | 年同比 | RECENT_1: 今天 vs 去年同一天；RECENT_7: 本周 vs 去年同一周；RECENT_30: 本月 vs 去年同一月 |
| `week_on_week` | 周期环比 | RECENT_1: 今天 vs 昨天；RECENT_7: 本周 vs 上周；RECENT_30: 本月 vs 上月 |
| `vs_peer_avg` | 较同行平均的变化率 | 本店变化率 vs 同行平均变化率 |
| `vs_peer_good` | 较同行优秀的变化率 | 本店变化率 vs 同行优秀变化率 |

> **⚠️ 注意**：`trend` 数据并非完全覆盖 `core_metrics` 的全部 7 项指标，实际返回的趋势指标为：`impression`（展现次数）、`visitor`（访客数）、`page_view`（浏览量）、`click_cvr`（点击转化率）、`buyer_count`（支付买家数），以及额外的 `ad_impression`（广告展现）。**缺失** `pay_cvr`（支付转化率）和 `pay_amount`（支付金额）的趋势数据。

### get_traffic_structure — 流量结构数据

```bash
python3 {baseDir}/cli.py get_traffic_structure [--date_type <DATE_TYPE>] [--device <DEVICE>]
```

**返回字段映射**：

| 返回区块 | 含义 | 用途 |
|---------|------|------|
| `traffic` | 流量来源排行、新老访客比、PC/无线占比、跳失率、入店搜索词 | 分析流量结构健康度 |

### get_transaction_ranking — 行业交易排名

```bash
python3 {baseDir}/cli.py get_transaction_ranking [--date_type <DATE_TYPE>] [--device <DEVICE>]
```

**⚠️ 日期类型限制**：仅支持 `RECENT_7` 和 `RECENT_30`，不支持 `RECENT_1`。若用户请求近1天数据，行业定位章节应跳过。

**返回字段映射**：

| 返回字段 | 含义 | 用途 |
|---------|------|------|
| `industry_name` | 所属行业名称 | 行业定位 |
| `my_pay_amount` | 本店支付金额 | 行业排名依据 |
| `industry_rank` | 行业排名 | 行业地位评估 |
| `industry_total` | 行业店铺总数 | 排名百分位计算 |
| `rank_percentile` | 排名百分位（如 0.25 表示前25%） | 行业相对位置 |
| `benchmark` | TOP标杆数据（top3_avg、top10_avg、top100_avg） | 与标杆差距对比 |

**benchmark 字段结构**：

| 子字段 | 含义 |
|--------|------|
| `top3_avg` | 行业TOP3平均支付金额 |
| `top10_avg` | 行业TOP10平均支付金额 |
| `top100_avg` | 行业TOP100平均支付金额 |

### get_customer_profile — 客户画像数据

```bash
python3 {baseDir}/cli.py get_customer_profile [--date_type <DATE_TYPE>] [--device <DEVICE>]
```

**返回字段映射**：

| 返回区块 | 含义 | 用途 |
|---------|------|------|
| `customer` | 支付买家/L会员/客户数 vs 同行优秀、回头率、新老客 GMV 构成、客单价 | 分析客户结构 |

## 安全声明

| 风险级别 | 命令 | Agent 行为 |
|---------|------|-----------|
| **只读** | get_core_metrics | 可直接执行，无需确认 |
| **只读** | get_traffic_structure | 可直接执行，无需确认 |
| **只读** | get_transaction_ranking | 可直接执行，无需确认 |
| **只读** | get_customer_profile | 可直接执行，无需确认 |

## 店铺健康诊断流程

### 规范约束

1. **禁止编造数据**：所有数据必须通过 CLI 命令获取真实数据
2. **数据格式**：金额保留 2 位小数并使用千分位格式（如 ¥125,000.00），百分比保留 1 位小数
3. **错误处理**：命令返回错误或数据为空时，对应章节标注"数据暂不可用"，不要用假数据填充
4. **精简输出**：表格数据完整展示，文字分析聚焦瓶颈识别和改善方向，每个瓶颈的改善建议控制在 1-2 条

### Step 1 — 确定查询参数

默认使用 `RECENT_7`（近 7 天）数据，设备类型默认 `ALL`。接受用户指定 `date_type` 和 `device`。

### Step 2 — 并行获取诊断数据

以下四个命令可**并行执行**，它们之间无数据依赖：

```bash
python3 {baseDir}/cli.py get_core_metrics --date_type <DATE_TYPE> --device <DEVICE>
python3 {baseDir}/cli.py get_traffic_structure --date_type <DATE_TYPE> --device <DEVICE>
python3 {baseDir}/cli.py get_transaction_ranking --date_type <DATE_TYPE> --device <DEVICE>
python3 {baseDir}/cli.py get_customer_profile --date_type <DATE_TYPE> --device <DEVICE>
```

错误处理规则：
- **`get_transaction_ranking`**：执行失败或数据为空/不含 `industry_name` → 跳过"行业定位"章节
- **其他命令返回错误**：对应报告章节标注"数据暂不可用"，其余章节正常生成

### Step 3 — LLM 分析推理

此步为 LLM 推理环节，不调用脚本：

**指标评估**（数据来源：`get_core_metrics`）：
- 遍历 `core_metrics`，重点标注 `rating` 为"略低"和"极低"的指标
- 结合 `trend` 数据判断趋势方向（改善中 / 恶化中 / 稳定）

**流量结构分析**（数据来源：`get_traffic_structure`）：
- 基于 `traffic` 数据，分析来源集中度（是否过度依赖单一渠道）
- 评估新老访客比例是否健康（新客占比过高说明老客留存差）
- 跳失率是否偏高、人均浏览量是否合理

**行业定位**（数据来源：`get_transaction_ranking`）：
- ⚠️ **数据可用性检查**：
  - 命令执行失败 → 跳过此模块
  - 返回数据中无 `industry_name` 字段 → 跳过此模块
  - 数据正常 → 基于返回数据，展示行业名称、排名、百分位、标杆对比
- 数据正常时，分析要点：
  - 根据 `industry_rank` 和 `industry_total` 计算排名百分位
  - 对比 `benchmark.top3_avg/top10_avg/top100_avg`，评估与标杆差距
  - 判断行业地位（头部/中上部/中部/下部）及提升空间

**客户健康度**（数据来源：`get_customer_profile`）：
- 基于 `customer` 数据，对比同行优秀水平
- 分析复购率、新老客 GMV 结构

**瓶颈诊断结论**（综合四个命令全部数据）：
- 综合以上数据，识别 1-3 个核心瓶颈，按严重程度排序
- 每个瓶颈需有数据支撑（引用具体指标和数值）
- 针对每个瓶颈给出 1-2 条可落地的改善方向

### Step 4 — 生成诊断报告

按下方报告模板组织数据，输出完整诊断报告。

**章节生成规则**：
- **"一、核心指标 vs 同行同层"**：必选章节
- **"二、流量结构分析"**：必选章节
- **"行业定位章节"**：如果 `get_transaction_ranking` 返回错误或数据为空，**直接跳过此章节**，后续章节顺序自动调整（客户健康度变为"三"、瓶颈诊断变为"四"）
- **"客户健康度章节"**：必选章节。若行业定位章节跳过，则编号为"三"；否则编号为"四"
- **"瓶颈诊断章节"**：必选章节。若行业定位章节跳过，则编号为"四"；否则编号为"五"

### Phase 2：交互深入分析

输出诊断报告后，在末尾追加交互引导：

```
---

如需深入了解某个方面（流量优化 / 转化提升 / 客户运营），或希望基于诊断结论生成月度经营规划，请告知。
```

用户可以：
- 针对某个瓶颈要求更详细的分析和建议
- 要求聚焦某个维度（如流量、客户）做深入分析
- 要求生成月度经营规划（引导至月度规划 skill）

交互跟进时复用已获取的数据，不重新调用脚本。

## 诊断报告输出格式

采用**模块化输出**，每个模块用 HTML 注释标记边界和结构化元数据，便于 UI 层按模块拆分渲染。HTML 注释在 Markdown 渲染时不可见，不影响阅读体验。

### 模块标记规范

- `<!-- MODULE: 模块名 -->` 和 `<!-- /MODULE: 模块名 -->` 标记模块边界
- `<!-- KEY: value -->` 标记模块内的结构化决策值
- 模块内部使用标准 Markdown 格式（表格、引用、列表等）
- 所有金额单位为元，保留2位小数，千分位格式
- 百分比保留1位小数

## 报告模板

```markdown
# 店铺经营健康诊断报告（{start_date} 至 {end_date}）

<!-- MODULE: diagnosis -->
<!-- DATE_RANGE: {start_date} 至 {end_date} -->
<!-- DATE_TYPE: {date_type} -->
<!-- BOTTLENECKS: ["瓶颈一", "瓶颈二"] -->

## 一、核心指标 vs 同行同层

| 指标 | 本店 | 同行同层均值 | 达标率 | 评级 |
|------|------|------------|--------|------|
| 展现次数 | {my_value} | {peer_avg} | {ratio_to_peer}% | {rating_emoji} {rating} |
| 访客数 | {my_value} | {peer_avg} | {ratio_to_peer}% | {rating_emoji} {rating} |
| 浏览量 | {my_value} | {peer_avg} | {ratio_to_peer}% | {rating_emoji} {rating} |
| 点击转化率 | {my_value}% | {peer_avg}% | {ratio_to_peer}% | {rating_emoji} {rating} |
| 支付转化率 | {my_value}% | {peer_avg}% | {ratio_to_peer}% | {rating_emoji} {rating} |
| 支付买家数 | {my_value} | {peer_avg} | {ratio_to_peer}% | {rating_emoji} {rating} |
| 支付金额 | ¥{my_value} | ¥{peer_avg} | {ratio_to_peer}% | {rating_emoji} {rating} |

> 达标率 = 本店 / 同行同层均值。评级标准：✅优秀(>=110%) | 🔶持平(90%-110%) | 🔻略低(50%-90%) | ❌极低(<50%)

## 二、流量结构分析

**来源分布**：

| 流量来源 | 访客数 | 占比 |
|---------|--------|------|
| {source_1} | {visitors} | {ratio}% |
| {source_2} | {visitors} | {ratio}% |
| ... | ... | ... |

**关键指标**：

| 指标 | 数值 | 判断 |
|------|------|------|
| 新访客占比 | {new_visitor_ratio}% | {LLM判断} |
| 跳失率 | {bounce_rate}% | {LLM判断} |
| 人均浏览量 | {avg_page_per_visit} | {LLM判断} |

**入店热搜词 TOP5**：{keyword_1}、{keyword_2}、{keyword_3}、{keyword_4}、{keyword_5}

## 三、行业定位

**所属行业**：{industry_name}

**行业排名数据**：

| 指标 | 数值 |
|------|------|
| 支付金额 | ¥{my_pay_amount} |
| 行业排名 | 第 {industry_rank} 名 |
| 行业店铺总数 | {industry_total} 家 |
| 排名百分位 | {rank_percentile_display}（前{rank_percentile_percent}%） |

**标杆对比**：

| 标杆层级 | 平均支付金额 | 与本店差距 |
|---------|------------|----------|
| TOP3 平均 | ¥{top3_avg} | 本店仅为标杆的 {gap_to_top3}% |
| TOP10 平均 | ¥{top10_avg} | 本店仅为标杆的 {gap_to_top10}% |
| TOP100 平均 | ¥{top100_avg} | 本店仅为标杆的 {gap_to_top100}% |

## 四、客户健康度

| 指标 | 本店 | 同行优秀 | 差距 |
|------|------|---------|------|
| 支付买家数 | {my_value} | {peer_excellent} | {gap_description} |
| L会员买家数 | {my_value} | {peer_excellent} | {gap_description} |
| 客户数 | {my_value} | {peer_excellent} | {gap_description} |
| 买家回头率 | {my_value}% | {peer_excellent}% | {gap_description} |

**新老客贡献**：新客 ¥{new_customer_gmv}（{new_customer_ratio_display}） / 老客 ¥{old_customer_gmv}（{old_customer_ratio_display}） | 客单价 ¥{avg_order_value}

## 五、瓶颈诊断与改善方向

{LLM 基于以上所有数据推理生成，格式如下：}

**核心瓶颈**：

1. **{瓶颈一名称}**（{严重程度}）
   - 数据依据：{具体指标和数值}
   - 改善方向：{1-2条可落地建议}

2. **{瓶颈二名称}**（{严重程度}）
   - 数据依据：{具体指标和数值}
   - 改善方向：{1-2条可落地建议}

3. **{瓶颈三名称}**（{严重程度}）（如有）
   - 数据依据：{具体指标和数值}
   - 改善方向：{1-2条可落地建议}

<!-- /MODULE: diagnosis -->
```

**模板使用说明**：

- **标题日期范围**：从 API 返回的 `date_range.start_date` 和 `date_range.end_date` 提取，格式如 "店铺经营健康诊断报告（2026-04-09 至 2026-04-15）"
- `<!-- DATE_RANGE -->` 和 `<!-- DATE_TYPE -->` 标记数据的时间范围和类型，供 UI 层展示
- `<!-- BOTTLENECKS -->` 标记 LLM 识别的核心瓶颈列表（JSON 数组），供 UI 层提取用于高亮展示
- **章节编号动态调整**：若行业定位数据不可用，跳过该章节后，客户健康度编号变为"三"，瓶颈诊断编号变为"四"
- **行业定位章节字段计算**：
  - `rank_percentile_display`：将 `rank_percentile`（如 0.2521）转为百分比显示（如 "25.21%"）
  - `rank_percentile_percent`：取百分位的整数部分（如 25）
  - `gap_to_top3/10/100`：计算本店支付金额占标杆的百分比，公式为 `my_pay_amount / benchmark.top3_avg * 100`，保留1位小数
- 诊断模块中的评级标签使用 emoji 区分：✅ 优秀、🔶 良好、🔻 略低、❌ 极低
- 瓶颈诊断和改善建议由 LLM 基于数据推理生成，非固定文案
- 所有表格中的金额和百分比均来自 API 返回，不得编造
- 合计行由 LLM 基于返回数据汇总计算

## 使用原则

1. **必须查询真实数据**：通过 CLI 命令获取真实数据，不要编造
2. **并行执行**：Step 2 的四个数据命令可并行执行以提高效率，任一命令失败不阻塞其余命令
3. **日期类型限制**：`get_transaction_ranking` 仅支持 `RECENT_7` 和 `RECENT_30`，不支持 `RECENT_1`。若用户请求近1天数据，行业定位章节应跳过
4. **瓶颈需有数据支撑**：每个瓶颈结论必须引用具体指标和数值，不可泛泛而谈
5. **改善方向需可落地**：给出的改善建议应具体、可执行，而非空泛的战略描述
6. **诊断结果供下游使用**：诊断结果自动持久化，可被「月度经营规划」skill 读取作为前置输入
7. **禁止内容**：不输出数据来源、生成时间等元信息；不输出与经营诊断无关的内容

## 环境变量（.env）

项目根目录的 `.env` 文件存储 skill 基础信息，供埋点上报等模块读取。发布到不同环境时可直接替换该文件中的变量值。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_NAME` | `1688-open-skill-template` | skill 名称 |
| `SKILL_VERSION` | `1.0.0` | skill 版本号 |
| `SKILL_CHANNEL` | `clawhub` | 发布渠道 |

> 已存在的系统环境变量优先级高于 `.env`，CI/CD 注入的变量不会被覆盖。

## 埋点上报

每次 CLI 命令执行时，自动向 skill 网关上报一次调用记录，用于统计 skill 调用次数。

- **实现位置**：`scripts/_tracker.py` → `report_skill_usage()`，在 `cli.py` 的 `main()` 中每次命令执行后自动调用
- **上报接口**：`POST /api/reportSkillsUsage/1.0.0`
- **上报参数**：

  | 参数 | 值来源 | 说明 |
  |------|--------|------|
  | `apiName` | 固定 `null` | 固定传 null |
  | `skillsName` | `.env` `SKILL_NAME` | skill 名称 |
  | `version` | `.env` `SKILL_VERSION` | skill 版本号 |
  | `scene` | 固定 `CLI` | 固定值 |
  | `channel` | `.env` `SKILL_CHANNEL` | 发布渠道 |

- **失败处理**：上报失败静默忽略，不影响主流程

## 执行前置（首次命中能力时必须）

- 首次执行 `configure` 前：先完整阅读 `references/capabilities/configure.md`
- 首次执行店铺健康诊断前：先完整阅读以下文档
  - `references/capabilities/get_core_metrics.md`
  - `references/capabilities/get_traffic_structure.md`
  - `references/capabilities/get_transaction_ranking.md`
  - `references/capabilities/get_customer_profile.md`
- 同一会话内后续重复调用可复用已加载知识；仅在规则冲突或文档更新时重读。

## 授权链接处理（browser_use）

`get_ak` 和 `authorize` 命令输出一条 JSON 后**立即退出**，回调服务器作为独立后台进程继续运行（最长 300 秒）。

**输出格式**：
```json
{
  "pending": true,
  "action": "browser_use",
  "url": "https://...",
  "markdown": "授权链接已生成！请使用 browser_use 工具打开以下链接完成授权..."
}
```

> ⚠️ **强制动作**：输出中只要出现 `"action": "browser_use"`，Agent **必须立即**调用 `browser_use` 工具打开 `url` 字段中的链接，不得跳过、延迟或用其他方式替代。

**Agent 处理流程**：
1. 读到 `"action": "browser_use"` → **立即**用 `browser_use` 工具导航到 `url`，并向用户展示 `markdown` 字段内容。
2. 在页面中完成登录和授权操作（AK 模式：复制 AK；OAuth 模式：点击授权确认）。
3. 授权完成后，浏览器页面会自动将结果回调给后台服务器（`localhost`），服务器直接将 AK/Token 写入本地存储。
4. browser_use 返回后，调用 `python3 cli.py configure --status` 确认 AK 是否已保存成功。

**注意事项**：
- 命令本身只输出这一条 JSON，**不会有第二条结果 JSON**，无需继续等待命令输出。
- 授权回调目标是 `localhost`，browser_use 执行环境必须能访问本机回调端口（8080–8089）。
- 若 300 秒内未完成授权，后台服务进程自动退出，下次运行 `get_ak` 时会自动清理并重新启动。
- **禁止**调用系统浏览器、`open` 命令或任何其他方式替代 browser_use。

## 异常处理

任何命令输出 `success: false` 时：

1. **先输出 `markdown` 字段**（已包含用户可读的错误描述）
2. **再根据关键词追加引导**：

| markdown 关键词 | Agent 额外动作 |
|----------------|--------------|
| "AK 未配置" 或 "AK 未就绪" 或 "签名无效" 或 "401" | **停止一切搜索尝试**，优先执行 `python3 cli.py get_ak` 自动获取 AK；如自动获取失败，引导用户前往 https://clawhub.1688.com/ 登录后右上角点击🔑复制获取ak内容后提交给agent执行configure命令 `python3 cli.py configure YOUR_AK` |
| "参数缺失" | 提示用户补充缺失参数后重试 |
| "date_type" 或 "device" 参数错误 | 提示用户使用合法的参数值 |
| "限流" 或 "429" | 建议用户等待 1-2 分钟后重试 |
| 其他 | 仅输出 markdown 即可 |

## 参数补齐引导话术

> "店铺健康诊断默认使用近 7 天数据。你也可以指定时间范围（近 1 天 / 近 7 天 / 近 30 天）和设备类型（全部 / PC / 无线）。"

### macOS Keychain 权限错误（错误码 -67674）

当 Python 首次访问 macOS Keychain 时，系统会弹出授权对话框。如果用户未授权或权限被拒绝，会出现此错误。

**解决方案**：
1. 当系统弹出「python3 想要访问钥匙串」对话框时，输入密码并点击「始终允许」
2. 如果对话框未弹出，打开「钥匙串访问」应用手动添加权限

### AK 配置持续失败（开启完全授权访问模式）

若执行 `configure` 后 AK 仍无法写入或读取，可能是运行本 skill 的软件未开启完全授权访问模式，导致 skill 进程无法访问本地文件。

**解决方案**：在运行本 skill 的软件（如悟空、QoderWork等）的设置中，开启「自动授权访问」模式后重新执行 `configure` 命令。

### 免责声明：
1、您理解并同意，技能运行结果和输出内容可能因适用的AI agent、大模型不同而产生差异或幻觉，请您对重要的信息进行甄别核实。
2、您应妥善保管您的Access Key（AK），这是您运行1688技能的身份凭证，请勿提供给第三人，避免身份凭证泄露造成损失。
3、您下载安装1688技能运行时应始终保持其完整性，不得擅自篡改技能的代码、相关文件或其他内容，否则1688不对技能运行结果和输出内容承担任何法律责任。
4、受限于当前技术发展，我们无法保证技能所有运行结果、输出内容的准确性、真实性、时效性，请您谨慎核实技能运行结果和输出内容，除法律规定由我们承担赔偿责任的场景外，我们不承担其他赔偿责任。