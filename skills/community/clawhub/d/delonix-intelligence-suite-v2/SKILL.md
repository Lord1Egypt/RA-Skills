---
name: delonix-intelligence-suite-v2
description: |
  德胧AI龙虾军团舆情情报综合工具箱 v2.0。整合 miaoda搜索 + BettaFish开源舆情引擎 + 飞书精美卡片 + 抖音/视频平台监控 + AI风险分析与防控预案生成。
  
  触发词：舆情、情报、网情、监控、风险分析、抖音监控、酒店风险、德胧舆情、竞品动态、行业预警
  
  三大核心能力：
  1. 外网信息采集（miaoda搜索主力 + BettaFish扩展）
  2. 精美飞书卡片输出（可视化日报）
  3. AI风险分析+防控预案（舆情驱动决策）
override-tools:
  - web_search
---

# 德胧舆情情报综合工具箱 v2.0

> 德胧AI龙虾军团专属舆情情报系统
> 版本：v2.0 | 日期：2026-04-19 | 作者：晁留柱的助手（小柱）
> 整合：miaoda-web-search + BettaFish + 飞书卡片 + AI风险分析

---

## 🔧 核心架构

```
德胧舆情情报综合工具箱 v2.0
├── 数据源层
│   ├── miaoda-web-search（主力）→ 关键词搜索 + AI摘要
│   ├── BettaFish扩展 → 30+平台深度采集（微博/小红书/抖音/快手/知乎）
│   └── 视频平台专项 → 抖音/快手/B站 视频舆情
├── 处理层
│   ├── 关键词模板（华住/锦江/亚朵/德胧/首旅如家）
│   ├── 视频舆情过滤（抖音含"德胧"关键字）
│   ├── 热度排序（按发布时间/媒体权重）
│   └── 去重+排重
├── AI分析层
│   ├── 舆情分类（投诉/安全/服务/运营/AI）
│   ├── 风险评级（高危/中危/低危）
│   └── 防控预案生成（针对同类舆情）
├── 输出层
│   ├── 飞书精美卡片（日报/突发/预警）
│   └── 结构化数据表 → 入库分析
└── 自动化层
    └── cron每日9:00自动采集推送
```

---

## ⚡ 快速使用

### 舆情采集（基础）

```bash
# 酒店舆情搜索
miaoda-studio-cli search-summary --query "华住 回访电话 隐私泄露 2026年4月"

# 抖音/视频平台舆情
miaoda-studio-cli search-summary --query "抖音 德胧 开元名都 投诉" --instruction "重点关注视频内容，提炼视频核心观点"

# 竞品动态
miaoda-studio-cli search-summary --query "锦江 AI动态定价 2026" --instruction "提取AI覆盖数据、效果数据、竞品对比"
```

### 风险分析（AI驱动）

```
触发词：风险分析、防控预案、规避建议

输入：舆情数据（投诉内容/事件描述）
输出：
1. 风险评级（高危/中危/低危）
2. 风险归因（根因分析）
3. 防控预案（具体措施）
4. 预警指标（监控阈值）
```

---

## 🛠️ 工具一：miaoda-web-search（主力·已集成）

### 简介
妙搭内置网页搜索工具，通过 `miaoda-studio-cli search-summary` 实现。

### 命令格式
```
miaoda-studio-cli search-summary --query "关键词" [--instruction "AI处理指令"] [--output text|json]
```

### 参数说明

| 参数 | 说明 | 必需 |
|------|------|------|
| `--query` | 搜索关键词（1-500字符） | 是 |
| `--instruction` | AI处理指令 | 否 |
| `--output` | 输出格式：text/json | 否 |

---

## 🛠️ 工具二：BettaFish 微舆系统（扩展）

### 简介
**BettaFish（微舆）** 是GitHub上最强的开源舆情分析系统（666ghj/BettaFish），支持30+平台深度采集。

### 仓库信息
```
GitHub: https://github.com/666ghj/BettaFish
Star: 17k+
语言: Python3
架构: 多Agent + LLM + NLP
```

### 核心能力

| 能力 | 说明 |
|------|------|
| 平台覆盖 | 微博/小红书/抖音/快手/B站/知乎/公众号等30+ |
| AI分析 | 情感分析/话题聚类/传播路径/趋势预测 |
| 多模态 | 突破图文限制，深度解析短视频内容 |
| Agent协作 | 多Agent辩论机制，链式思维碰撞 |
| 报告生成 | 自动生成专业舆情分析报告 |

### 安装状态
⚠️ **待安装** - 受网络限制，pip/GitHub下载可能超时。

### 安装步骤（网络恢复后）

```bash
# 方式1：pip安装
pip install bettafish

# 方式2：源码克隆
git clone git@github.com:666ghj/BettaFish.git /tmp/BettaFish
cd /tmp/BettaFish
pip install -r requirements.txt

# 方式3：Docker（推荐）
docker pull bettafish/bettafish:latest
docker run -d bettafish/bettafish
```

### 使用示例

```bash
# 基础舆情分析
bettafish analyze --keyword "华住 酒店 投诉" --platforms weibo,xiaohongshu,douyin

# 视频平台专项
bettafish analyze --keyword "德胧" --platforms douyin,kuaishou,bilibili --video-only

# 风险报告生成
bettafish report --type risk --output json

# 竞品对比分析
bettafish compare --brands 华住,锦江,亚朵 --metric reputation
```

### BettaFish + miaoda 协同方案

```
阶段1（当前）：miaoda快速搜索
└── 负责：关键词搜索、AI摘要、实时热点发现

阶段2（扩展）：BettaFish深度分析
└── 负责：30+平台结构化采集、情感分析、风险评级、视频舆情

协同流程：
用户请求 → miaoda快速发现 → BettaFish深度分析 → AI风险评估 → 飞书卡片输出
```

---

## 🛠️ 工具三：抖音/视频平台专项监控

### 视频舆情特点

| 特点 | 说明 |
|------|------|
| 传播速度快 | 视频发酵速度远超图文 |
| 匿名性强 | 博主身份难追溯 |
| 情绪化 | 视觉冲击更强，负面情绪放大 |
| 二次创作 | 易引发模仿和扩散 |

### 抖音舆情关键词模板

```bash
# 德胧品牌词
miaoda-studio-cli search-summary --query "抖音 开元名都 德胧 投诉"
miaoda-studio-cli search-summary --query "抖音 钛唐酒店 德胧 差评"
miaoda-studio-cli search-summary --query "抖音 德胧集团 酒店 卫生"

# 竞品酒店视频舆情
miaoda-studio-cli search-summary --query "抖音 华住 酒店 隐私 泄露"
miaoda-studio-cli search-summary --query "抖音 桔子水晶 酒店 投诉"
```

### 视频舆情分级

| 级别 | 特征 | 响应时间 |
|------|------|----------|
| P0红色 | 视频播放量>10万、负面评论>1000 | 30分钟内 |
| P1橙色 | 播放量>1万、负面评论>100 | 2小时内 |
| P2黄色 | 播放量>1000、有扩散趋势 | 4小时内 |
| P3蓝色 | 普通投诉视频 | 24小时内 |

---

## 🛠️ 工具四：飞书精美卡片生成器

### 飞书卡片模板 v2.0

基于 `ritaswc/lark-card-message-builder` 和飞书官方Card JSON 2.0结构。

**精美卡片JSON结构**：

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "template": "red",
    "title": {"content": "🔥 酒店舆情日报 | 2026-04-19", "tag": "plain_text"}
  },
  "elements": [
    {"tag": "markdown", "content": "**<text_tag color='red'>🔴 超级热点</text_tag> [标题]**\n\n[内容]"},
    {"tag": "hr"},
    {"tag": "markdown", "content": "**<text_tag color='orange'>🟠 投诉数据</text_tag>**\n\n• [投诉1]\n• [投诉2]"},
    {"tag": "hr"},
    {"tag": "markdown", "content": "**<text_tag color='green'>🟡 风险分析</text_tag>**\n\n[AI分析内容]"},
    {"tag": "note", "content": "🦞 德胧AI龙虾军团 | v2.0", "quoteless": false}
  ]
}
```

### 飞书Markdown语法要点

| 要素 | 语法 | 注意 |
|------|------|------|
| 标题 | `**加粗文字**` | ❌ 不支持 `# ## ###` |
| 标签 | `<text_tag color='red'>` | 颜色：red/orange/yellow/green/blue/purple |
| 链接 | `[文本](url)` | - |
| 分割线 | `---` | - |
| 列表 | `• 项目` 或 `1. 项目` | bullet list更稳定 |
| 彩色文本 | `<font color='red'>文字</font>` | - |

### 发送精美卡片

```bash
# 使用 feishu_im_user_message 工具
# msg_type: interactive
# content: JSON字符串（见上方模板）
```

---

## 🛠️ 工具五：AI风险分析与防控预案

### 风险分析流程

```
舆情数据输入
    ↓
① 舆情分类（5类）
    ├─ 投诉类（服务/卫生/退改）
    ├─ 安全类（隐私/消防/事故）
    ├─ 服务类（态度/效率/承诺）
    ├─ 运营类（加盟/关店/业绩）
    └─ AI类（定价/隐私/自动化）
    ↓
② 风险评级
    ├─ 高危（媒体曝光>5家/投诉量>100）
    ├─ 中危（媒体曝光>2家/投诉量>30）
    └─ 低危（个别投诉/无媒体曝光）
    ↓
③ 根因分析（5Why）
    ↓
④ 防控预案生成
    ├─ 预防措施
    ├─ 监控指标
    ├─ 应急预案
    └─ 责任人
    ↓
⑤ 输出飞书卡片
```

### 风险分析Prompt模板

```
请分析以下舆情事件，生成风险报告：

## 舆情内容
[粘贴舆情内容]

## 分析要求
1. 风险评级（高危/中危/低危）
2. 风险归因（根因分析，5Why法）
3. 防控预案：
   - 预防措施（具体可执行）
   - 监控指标（可量化）
   - 应急预案（触发条件+处置流程）
4. 同类舆情规避建议

## 输出格式
请用飞书Markdown格式输出，包含：
- 风险评级（高危用🔴标记）
- 根因分析
- 防控预案（表格形式）
- 规避建议
```

### 防控预案示例

| 类别 | 预防措施 | 监控指标 | 应急预案 |
|------|----------|----------|----------|
| 隐私泄露 | 回访电话需用户授权、话术标准化 | 投诉量>5/月 | 立即下架回访、隐私合规培训 |
| 卫生投诉 | 客房SOP增加抽查频次 | 差评率>2% | 门店深度清洁、公开道歉 |
| 强制好评 | 禁止任何形式强制、投诉零容忍 | 投诉量>3/月 | 涉事员工追责、品牌公开澄清 |

---

## 📋 德胧专属关键词库 v2.0

### 企业监控（扩展）

| 企业 | 品牌词 | 投诉关键词 |
|------|--------|------------|
| 华住会 | 华住、桔子、汉庭、全季、海友、漫心、美居 | 隐私、泄露、好评、威胁 |
| 锦江集团 | 锦江、锦江酒店、锦鲲 | 定价、加盟、解约 |
| 亚朵 | 亚朵、Atour | 服务、卫生、退改 |
| 首旅如家 | 首旅如家、如家、和颐 | 卫生、安全、投诉 |
| 德胧 | 开元名都、钛唐、开元酒店 | [德胧专属] |

### 视频平台关键词

| 平台 | 搜索关键词 | 重点关注 |
|------|------------|----------|
| 抖音 | 开元名都+投诉、德胧+曝光、钛唐+差评 | 视频评论、博主观点 |
| 快手 | 酒店+投诉、德胧+事件 | 老铁文化、传播速度 |
| B站 | 酒店行业、隐私泄露、酒店评测 | UP主深度测评 |
| 小红书 | 酒店体验、投诉笔记、酒店避雷 | 素人笔记、真实体验 |

### 事件类型关键词

| 类型 | 关键词组合 |
|------|------------|
| 隐私安全 | 隐私泄露、信息泄露、摄像头、入住记录 |
| 服务质量 | 卫生差、前台态度、虚假宣传、货不对板 |
| 会员权益 | 积分清零、会员降级、权益缩水、取消优惠 |
| 价格问题 | 临时涨价、差价、取消扣款、价格欺诈 |
| 安全事故 | 消防隐患、安全事故、食物中毒、意外伤害 |

---

## ⏰ 自动化配置

### Cron：每日舆情日报

```javascript
{
  "name": "德胧舆情日报v2.0",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行德胧舆情日报v2.0采集：\n1. miaoda搜索今日最新舆情（华住/锦江/亚朵/德胧）\n2. 抖音/视频平台专项搜索（抖音+快手+B站）\n3. AI风险分析（高危舆情生成防控预案）\n4. 生成飞书精美卡片（日报格式）\n5. 发送私信到 ou_fc1e75d64fec6e10ce94a51adc6f6409"
  },
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "ou_fc1e75d64fec6e10ce94a51adc6f6409"
  }
}
```

### Cron：突发舆情预警

```javascript
{
  "name": "德胧突发舆情预警",
  "schedule": {
    "kind": "cron",
    "expr": "0 */2 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行突发舆情检查：\n1. 搜索最新抖音/视频平台舆情（含'德胧'关键字）\n2. 检查P0/P1级风险\n3. 如有突发高危舆情，立即生成预警卡片发送私信"
  },
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "ou_fc1e75d64fec6e10ce94a51adc6f6409"
  }
}
```

---

## 🔄 迭代计划

### v2.0（当前）
- [x] miaoda-web-search 集成
- [x] BettaFish 扩展指南
- [x] 抖音/视频平台专项监控
- [x] 飞书精美卡片模板 v2.0
- [x] AI风险分析Prompt模板
- [ ] BettaFish 本地部署（待网络恢复）
- [ ] 防控预案数据库

### v3.0（计划中）
- [ ] BettaFish 本地化部署
- [ ] 抖音API官方接入（需企业认证）
- [ ] 可视化舆情仪表盘
- [ ] 微信视频号监控

### v4.0（长期）
- [ ] 实时预警Webhook推送
- [ ] 竞品对比分析报告
- [ ] 季度舆情白皮书

---

## 🦞 部署指南

### 一键安装（本Skill）

```bash
# 1. 复制Skill到OpenClaw目录
cp -r delonix-intelligence-suite-v2/ ~/workspace/agent/skills/

# 2. 重启OpenClaw
openclaw gateway restart

# 3. 验证
miaoda-studio-cli search-summary --query "测试" --instruction "验证工具是否正常"
```

### BettaFish安装（网络恢复后）

```bash
# 克隆BettaFish
git clone git@github.com:666ghj/BettaFish.git /tmp/BettaFish

# 安装依赖
cd /tmp/BettaFish
pip install -r requirements.txt

# 配置API Key（用于LLM分析）
export OPENAI_API_KEY="your-key"
export BETTAFISH_CONFIG="/path/to/config.yaml"
```

---

## ⚠️ 注意事项

1. **网络限制**：GitHub HTTPS可能超时，优先使用SSH克隆
2. **数据合规**：采集内容仅用于内部分析，不可公开传播
3. **频率控制**：搜索请求间隔建议>3秒
4. **视频舆情**：抖音等平台可能需要Cookie认证
5. **内容审核**：AI分析结果需人工核实

---

## 📞 技术支持

- SKILL作者：晁留柱的助手（小柱）
- 版本：v2.0
- 更新：2026-04-19
- GitHub：github.com/chaoliuzhu65-tech/delonix-web-intelligence
- 共享池：德胧AI协同知识共享池
