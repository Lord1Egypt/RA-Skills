---
name: cinescope
description: 智能影评评估 - 多源数据采集 + 六维分析 + 动态权重评分
version: "1.0.0"
author: OpenClaw User
license: MIT
---
  智能影评评估 Skill。当用户提到任何电影并希望了解其评价、值不值得看、口碑如何、打几分时，必须使用此 Skill。
  触发词包括但不限于：影评、评分、推荐、值得看吗、好看吗、烂番茄、豆瓣分、口碑、分析这部电影。
  即使用户只是随口提到一部电影名称并带有疑问语气，也应主动触发此 Skill。
  此 Skill 会执行多源数据采集、六维结构化分析、动态权重评分，并生成带证据级别标注的完整影评报告（含六维蛛网图）。
---

# CineScope · 多源证据驱动影评系统

## 核心原则

- **证据优先**：所有评分必须有来源支撑，不凭空打分
- **来源透明**：标注每条判断基于哪一级证据
- **动态权重**：按影片类型自动调整六维权重
- **默认防剧透**：除非用户明确要求，不披露关键剧情反转
- **局限声明**：新片/冷门片样本不足时必须预警

---

## Step 0 · 意图解析与实体确认

用户输入电影名后，先执行以下检查：

1. **歧义消除**：若电影名存在重名（如《沙丘》《蜘蛛侠》），自动优先选取最新或最热版本，并在报告开头注明"本报告评估的是：[完整片名 + 年份 + 导演]"
2. **关注点提取**：若用户指定关注方向（如"我主要关心剧本"），在对应维度加权输出，并在报告末尾提示
3. **剧透模式确认**：默认防剧透开启；若用户明确说"可以剧透"或"分析结局"，则切换至剧透模式

---

## Step 1 · 并行数据采集

### 搜索工具优先级

| 优先级 | 工具 | 用途 | 说明 |
|--------|------|------|------|
| **主搜索** | `tavily-search` | 核心数据采集 | AI 优化搜索，返回简洁相关结果 |
| **备用搜索** | `博查 API (Bocha)` | 补充检索 | Tavily 异常时使用，国内访问稳定 |

**调用策略：**
1. 优先使用 `tavily-search` 进行主检索（支持 `--deep` 深度搜索）
2. 如 Tavily API 异常/无结果，降级使用 `博查 API`（Endpoint: `https://api.bocha.cn/v1/web-search`）
3. 需要获取具体页面内容时，使用 `tavily-search extract` 或 `web_fetch`

---

### 并行检索执行

使用上述搜索工具并行检索以下来源，**每次至少覆盖 L1+L3+L4 三层**：

### 数据源分层

| 层级 | 平台 | 权重 | 采集内容 |
|------|------|------|----------|
| **L1 专业权威** | 豆瓣、IMDb、Rotten Tomatoes、Metacritic | 40% | 评分数值 + Top 专业长评摘要 |
| **L2 垂直媒体** | Variety、好莱坞报道者、影视工业网、知名影评公众号 | 20% | 技术维度（摄影/剪辑/音效）专业解读 |
| **L3 大众口碑** | 猫眼、淘票票、IMDb 用户评分 | 20% | 普通观众体感、娱乐性评价 |
| **L4 社交舆情** | 微博、小红书、Twitter/X、Reddit | 20% | 实时情绪、争议点、高频关键词 |

### 归一化规则

将各平台分数统一映射至 **100 分制**：

| 平台 | 原始制 | 换算公式 |
|------|--------|----------|
| 豆瓣 | 10 分制 | × 10 |
| IMDb | 10 分制 | × 10 |
| Rotten Tomatoes | 百分制（新鲜度%） | 直接使用；Audience Score 单独列出 |
| Metacritic | 100 分制 | 直接使用 |
| 猫眼/淘票票 | 10 分制 | × 10 |

---

### 搜索命令示例

```bash
# Tavily 主搜索（推荐）
node {baseDir}/../tavily-search/scripts/search.mjs "夜王 电影 豆瓣评分" -n 10
node {baseDir}/../tavily-search/scripts/search.mjs "夜王 2026 春节档 影评" --deep

# Tavily 内容提取（获取具体页面）
node {baseDir}/../tavily-search/scripts/extract.mjs "https://movie.douban.com/subject/xxx/"

# 博查 API 备用搜索
# （当 Tavily API 异常时使用）
# API 文档：https://open.bochaai.com/
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${BOCHA_API_KEY}" \
  -d '{"query":"夜王 电影 豆瓣评分"}'
```

---

## Step 2 · 证据分级

采集完成后，对所有材料按以下标准分级，**评分时必须标注证据级别**：

| 级别 | 定义 | 举例 |
|------|------|------|
| **A 级** | 专业影评、权威平台高质量长评（200 字以上）、行业媒体深度分析 | 豆瓣热门长评、Metacritic 媒体评 |
| **B 级** | 高赞用户长评、较完整的大众观后感 | IMDb 用户长评、猫眼精选评论 |
| **C 级** | 社媒短评、热搜话题、碎片化舆情 | 微博超话、小红书笔记、Twitter 短评 |

> **原则**：结论越重要，所需证据级别越高。仅有 C 级证据支撑的判断，必须注明"（基于社媒舆情，稳定性较低）"

---

## Step 3 · 六维动态权重评估

### 3.1 按影片类型自动选择权重方案

在执行评分前，先判断影片类型，选择对应权重表：

#### 商业片 / 类型片（动作、喜剧、爱情、惊悚等）

| 维度 | 权重 | 核心考察点 |
|------|------|------------|
| 剧本与叙事 Script & Story | 20% | 逻辑自洽、节奏把控、冲突设计 |
| 视听语言 Visuals & Audio | 20% | 特效质感、摄影、配乐、沉浸感 |
| 表演质感 Acting | 15% | 角色契合度、情绪爆发力 |
| 导演掌控 Direction | 10% | 场面调度、完成度 |
| 情感共鸣 Emotional Resonance | 20% | 爆点/燃点/泪点、观影爽感 |
| 大众娱乐性 Entertainment | 15% | 观影门槛、话题度、值回票价感 |

#### 作者电影 / 艺术片

| 维度 | 权重 | 核心考察点 |
|------|------|------------|
| 剧本与叙事 Script & Story | 25% | 叙事野心、人物弧光、台词深度 |
| 视听语言 Visuals & Audio | 20% | 摄影语言、美学风格、音效设计 |
| 表演质感 Acting | 20% | 情感真实性、内敛张力、群像刻画 |
| 导演掌控 Direction | 20% | 风格统一性、主题深度、作者表达 |
| 情感共鸣 Emotional Resonance | 10% | 观影后劲、余韵、思想冲击 |
| 创新与价值 Innovation | 5% | 题材突破、文化输出、影史意义 |

#### 动画片

| 维度 | 权重 | 核心考察点 |
|------|------|------------|
| 剧本与叙事 Script & Story | 20% | 故事完整性、情节推进效率 |
| 视听语言 Visuals & Audio | 25% | 视觉创意、动画质量、色彩美学 |
| 表演质感 Acting | 10% | 配音契合度、角色生动性 |
| 导演掌控 Direction | 15% | 节奏控制、场景设计 |
| 情感共鸣 Emotional Resonance | 20% | 全年龄共情、情感完成度 |
| 受众适配度 Audience Fit | 10% | 儿童友好度、成人深度层次 |

### 3.2 单维评分规则

每个维度输出：

```
[维度名]：X/10
证据级别：A/B/C
评语：2-3 句，说明得分理由，引用具体评论观点（不直接大段摘抄）
```

---

## Step 4 · 风险机制

在生成报告前，检查并触发以下预警：

| 风险类型 | 触发条件 | 处理方式 |
|----------|----------|----------|
| **争议预警** | 专业口碑（L1）与大众/社媒口碑（L3+L4）归一化分差 > 15 分 | 在报告顶部添加 ⚠️ 争议预警模块 |
| **样本不足预警** | 上映不足 2 周 或 豆瓣评分人数 < 1 万 | 标注"当前结论时效性强，建议上映 1 个月后复评" |
| **水军/控评识别** | 短期内评分异常波动，或极端评价占比过高 | 取中位数而非均值，注明"存在疑似控评，数据仅供参考" |
| **时效标注** | 所有报告 | 报告末尾注明"评分基于 [日期] 前的口碑数据" |

---

## Step 5 · 综合评分计算

```
口碑基础分 = L1×0.4 + L2×0.2 + L3×0.2 + L4×0.2  （归一化至 100 分）

六维加权分 = Σ（各维度得分×10 × 对应权重）  （即 100 分制）

综合总分 = 口碑基础分 × 0.4 + 六维加权分 × 0.6
```

> **重要原则**：平台数据是参考证据，不直接决定最终分。六维分是 Claude 基于证据的独立判断，权重更高。

---

## Step 6 · 结构化输出报告

按以下固定结构输出，**不得省略任何模块**：

---

### 📋 影片基本信息
片名 | 年份 | 导演 | 主演 | 类型 | 片长

---

### ⚠️ 争议预警（如触发）
说明专业口碑与大众口碑的分歧所在及可能原因

---

### 📊 一句总评（The Verdict）
用一句话精准定位影片（例："工业完成度极高但主题表达流于表面的商业续作"）

---

### 🌐 平台评分快照

| 平台 | 原始评分 | 归一化 (100 分) | 样本规模 |
|------|----------|---------------|----------|
| 豆瓣 | X.X/10 | XX | X 万人 |
| IMDb | X.X/10 | XX | X 万人 |
| Rotten Tomatoes 专业 | XX% | XX | XX 篇 |
| Rotten Tomatoes 观众 | XX% | XX | X 万人 |
| Metacritic | XX/100 | XX | XX 篇 |
| 猫眼 | X.X/10 | XX | X 万人 |

**口碑基础分**：XX/100

---

### 🕸️ 六维雷达评分

| 维度 | 得分 | 证据级别 | 简评 |
|------|------|----------|------|
| 剧本与叙事 | X/10 | A/B/C | ... |
| 视听语言 | X/10 | A/B/C | ... |
| 表演质感 | X/10 | A/B/C | ... |
| 导演掌控 | X/10 | A/B/C | ... |
| 情感共鸣 | X/10 | A/B/C | ... |
| [第六维度] | X/10 | A/B/C | ... |

**六维加权分**：XX/100（使用 [商业片/作者电影/动画片] 权重方案）

紧接评分表之后，输出六维可视化图表。**根据平台能力选择输出格式**：

#### 可视化输出策略

| 平台类型 | 输出格式 | 说明 |
|----------|----------|------|
| **支持 HTML/JS** | Chart.js 雷达图 | 完整交互式图表 |
| **纯文本平台**（飞书/微信/短信） | ASCII 字符画雷达图 | 兼容性最好 |
| **支持 Markdown** | 条形图 + 表格 | 清晰易读 |

---

#### 方案 A：Chart.js 雷达图（支持 HTML 的平台）

- 使用 Chart.js radar 类型
- 维度标签与评分表保持一致（6 个维度，顺序相同）
- 数据范围：0–10，步进 2
- 配色：`#534AB7`（紫色系，fill 透明度 0.18）
- 禁用 Chart.js 默认图例，在图表下方输出自定义 HTML 图例
- Canvas 外层 div：`max-width: 520px; height: 420px; margin: 0 auto`

```html
<div style="position: relative; width: 100%; max-width: 520px; margin: 0 auto; height: 420px;">
  <canvas id="radarChart"></canvas>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 8px; font-size: 12px; color: var(--color-text-secondary);">
  <span style="display: flex; align-items: center; gap: 4px;">
    <span style="width: 10px; height: 10px; border-radius: 2px; background: #5340b7;"></span>
    《片名》六维评分
  </span>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const labels = ['剧本与叙事','视听语言','表演质感','导演掌控','情感共鸣','[第六维度]'];
const data = [D1, D2, D3, D4, D5, D6]; // 替换为实际得分
new Chart(document.getElementById('radarChart'), {
  type: 'radar',
  data: {
    labels: labels,
    datasets: [{
      label: '得分',
      data: data,
      backgroundColor: 'rgba(83, 74, 183, 0.18)',
      borderColor: '#534AB7',
      borderWidth: 2,
      pointBackgroundColor: '#534AB7',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 5,
      pointHoverRadius: 7
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: ctx => ' ' + ctx.raw.toFixed(1) + ' / 10' } }
    },
    scales: {
      r: {
        min: 0, max: 10,
        ticks: { stepSize: 2, font: { size: 11 }, color: '#888780', backdropColor: 'transparent' },
        pointLabels: { font: { size: 13 }, color: '#444441' },
        grid: { color: 'rgba(136,135,128,0.25)' },
        angleLines: { color: 'rgba(136,135,128,0.25)' }
      }
    }
  }
});
</script>
```

---

#### 方案 B：ASCII 字符画雷达图（纯文本平台，如飞书/微信）

**当平台不支持 HTML/JavaScript 时，使用以下文本格式：**

```
                    《片名》六维评分雷达图

                          剧本与叙事
                              10
                               │
                         8 ────┼──── 8
                               │    
                    视听   6 ──┼── 6   视听
                              4│    
                               │    
                  表演 6 ──────┼───── 7 表演
                               │    
                              4│    
                    导演   6 ──┼── 6   导演
                               │    
                         2 ────┼──── 2
                               │    
                          情感共鸣 ─── 大众娱乐性

    数值表：
    维度         得分    评级
    ──────────────────────────
    剧本与叙事    X.X    ★★★★☆
    视听语言      X.X    ★★★★☆
    表演质感      X.X    ★★★★☆
    导演掌控      X.X    ★★★★☆
    情感共鸣      X.X    ★★★★☆
    大众娱乐性    X.X    ★★★★☆
```

---

#### 方案 C：条形图（推荐用于飞书等 IM 平台）

**最清晰易读的格式，推荐作为默认输出：**

```
📊《片名》六维评分

剧本与叙事   ███████░░░  X.X/10  ★★★★☆
视听语言     ████████░░  X.X/10  ★★★★☆
表演质感     ███████░░░  X.X/10  ★★★★☆
导演掌控     ███████░░░  X.X/10  ★★★★☆
情感共鸣     ███████░░░  X.X/10  ★★★★☆
大众娱乐性   ████████░░  X.X/10  ★★★★☆

▓ 图例：█ 得分  ░ 未得分
```

**条形图生成规则：**
- 每格代表 1 分，共 10 格
- `█` 表示得分部分（每 1 分 = 1 个 █）
- `░` 表示未得分部分
- 小数处理：≥0.5 进位，<0.5 舍去

---

### 🎯 综合总分

**XX.X / 100**

---

### 🗣️ 舆论场摘要

**专业媒体怎么说**（主要基于 A 级证据）：
[2-3 句，概括专业影评人的核心共识——夸什么、批什么]

**大众观众怎么说**（主要基于 B 级证据）：
[2-3 句，概括普通观众的主要感受]

**社交媒体在讨论什么**（C 级证据，波动性较高）：
- 正向高频词：[词 1、词 2、词 3...]
- 负向高频词：[词 1、词 2、词 3...]
- 主要争议点：[简述]

---

### ✍️ 深度解析（默认防剧透）

选取 1-2 个最值得展开的维度（亮点或槽点），各写一段深度分析。
**不披露关键剧情反转、结局、重要角色死亡**。
如需完整剧情分析，请告知"可以剧透"。

---

### 👥 观影建议

**适合人群**：[具体描述，如"科幻类型片爱好者"、"原著党"、"家庭观影"]
**不适合人群**：[具体描述，如"对逻辑漏洞敏感的观众"、"不耐慢节奏者"]
**观影环境建议**：[如"建议 IMAX"、"流媒体即可"、"适合独自观看"]

---

### 📌 局限声明

- 数据截止时间：[日期]
- 样本状态：[充足 / 不足，说明原因]
- 特殊干扰：[如存在控评、粉黑大战、档期炒作，在此注明]

---

## 异常处理规则

| 情况 | 处理方式 |
|------|----------|
| 某平台数据无法获取 | 在快照表中标注"数据不可用"，不伪造评分 |
| 影片尚未上映 | 说明"暂无观众评价"，仅分析预告片、主创背景、提前场口碑 |
| 冷门片/老片数据稀少 | 降低 L3/L4 权重，提升 A 级证据权重，并声明局限 |
| 敏感题材（政治/宗教/历史） | 仅陈述多方评价观点，不输出单一价值判断 |
| 用户追问某维度 | 针对该维度补充更多 A/B 级证据，给出更详细分析 |
| **Tavily API 异常** | 自动降级使用 `博查 API` 作为备用搜索源 |
| **搜索结果不足** | 尝试 `tavily-search --deep` 深度搜索或扩大检索词范围 |

---

## 配置要求

| 配置项 | 说明 | 是否必需 |
|--------|------|----------|
| `TAVILY_API_KEY` | Tavily API 密钥（从 https://tavily.com 获取） | ✅ 必需 |
| `BOCHA_API_KEY` | 博查 AI 搜索 API 密钥（备用搜索） | ⚠️ 推荐配置 |

> **注意**：
> 1. 如未配置 `TAVILY_API_KEY`，需在系统环境变量中添加后才能正常使用搜索功能
> 2. 博查 API 作为备用搜索源，推荐配置以确保 Tavily 异常时可降级使用
> 3. 博查 API 申请地址：https://open.bochaai.com/

---

## 博查 API 快速配置

### 1. 获取 API Key

访问博查开放平台 https://open.bochaai.com/ 注册并获取 API Key

### 2. 配置环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export BOCHA_API_KEY="your-bocha-api-key"

# 或临时配置
export BOCHA_API_KEY="your-bocha-api-key"
```

### 3. 调用示例

```bash
# Web Search API
curl -X POST "https://api.bocha.cn/v1/web-search" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"夜王 电影 豆瓣评分"}'

# Reranker API（可选，用于语义排序）
curl -X POST "https://api.bocha.cn/v1/rerank" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $BOCHA_API_KEY" \
  -d '{"query":"夜王 影评","documents":["文档 1","文档 2"]}'
```

### 4. 免费额度

- 注册即送免费额度
- 具体额度请查看官网最新政策：https://open.bochaai.com/

### 5. API 文档

- Web Search API: `https://api.bocha.cn/v1/web-search`
- Reranker API: `https://api.bocha.cn/v1/rerank`
- 开放平台：https://open.bochaai.com/
