# 设计师情报站 - 使用示例

## 基本用法

### 生成日报

```
请生成今日的设计师情报日报
```

**输出格式**: 结构化表格格式（v1.3.1+）
- 领域拆分展示（手机/AI/智能硬件/设计）
- 表格呈现每条情报
- 超链接 100% 覆盖
- 趋势洞察分点展示

### 生成周报

```
请生成本周的设计师情报周报
```

**输出格式**: 结构化表格格式（v1.3.1+）
- 本周头条 Top5
- 领域汇总表格
- 深度趋势洞察
- 设计机会识别

### 领域查询

```
查询今日 AI 领域的重要动态
查询本周手机领域的新品发布
```

---

## 完整输出示例

### 📊 日报示例（结构化表格格式）

```markdown
# 📊 AI/硬件/手机情报日报

**日期**: 2026 年 3 月 23 日  
**覆盖时段**: 3 月 22 日 -3 月 23 日  
**情报官**: 梨然 - 阿里版  
**筛选标准**: 大厂动态 | 趋势洞察 | 设计哲学 | 竞品策略 | 判断力提升

---

### 🔴 今日头条（P0 级·S 级情报）

| 公司/机构 | 事件 | 影响 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| 大疆 DJI | [大疆正式起诉影石，6 项专利纠纷引爆无人机市场](https://www.huxiu.com/article/4844500.html) | 中国智能硬件头部企业首次正面专利交锋 | 虎嗅网 | 1+4 |
| Samsung | [Galaxy S26 原生支持 AirDrop](https://www.theverge.com/tech/898815/samsung-quick-share-airdrop-support-galaxy-s26) | Android 厂商首次原生支持苹果专有协议 | The Verge | 1+2 |

---

### 📱 手机领域

| 公司 | 动态 | 关键信息 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| 华为 | [问界 M6/M8 等多车型搭载 896 线激光雷达](https://www.ifanr.com/) | 896 线双光路图像级激光雷达，智能驾驶感知升级 | 爱范儿 | 1+2 |
| 华为 | [畅享 90 Pro Max 发布，8500mAh 电池](https://www.ifanr.com/) | 华为首款 WiFi7 手机，「跨天级超长续航」 | 爱范儿 | 1 |

---

### 🤖 AI 领域

#### 大模型进展

| 公司/机构 | 模型/技术 | 亮点 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| Cursor | [承认 Composer 2 基于中国 Moonshot AI 的 Kimi 2.5](https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/) | 估值$293 亿的美国明星初创承认使用中国开源模型 | TechCrunch | 2+4 |
| NVIDIA | [Vera Rubin 架构算力平台](https://www.jiqizhixin.com/) | GTC 大会发布，支持更大规模 AI 模型训练 | 机器之心 | 1+2 |

#### AI 应用/产品

| 公司 | 产品 | 功能 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| OpenArt+Fanvue | [AI Personality of the Year 奖项](https://www.theverge.com/ai-artificial-intelligence/898781/ai-personality-of-the-year-influencer-contest) | AI 网红经济商业化，$20,000 奖金 | The Verge | 2 |
| GitHub | [TradingAgents 多智能体金融交易框架 38K+ stars](https://github.com/trending) | 多 Agent 协作在垂直领域落地验证 | GitHub Trending | 2+5 |

---

### 🔌 智能硬件

| 公司 | 产品 | 功能 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| 宇树科技 | [四足 + 人形机器人](https://www.pingwest.com/a/312363) | 全球第一量产规模，持续盈利数亿 | 品玩 | 1+2 |
| 博匠智能 | [建造机器人](https://www.pingwest.com/a/312353) | 建筑业机器人应用，即将发布 | 品玩 | 2 |

---

### 🎨 设计领域

| 类型 | 动态 | 来源 | 条件 |
| --- | --- | --- | --- |
| 空间设计 | [Walter Van Beirendonck 设计太空主题儿童游乐空间](https://www.dezeen.com/2026/03/23/walter-van-beirendonck-space-themed-playscape-belgian-arts-campus/) | Dezeen | 3+5 |
| 办公设计 | [Snøhetta 设计台中金融办公室](https://www.dezeen.com/2026/03/22/good-finance-office-snohetta-taichung/) | Dezeen | 3+4 |
| AI 伦理 | [游戏《Crimson Desert》开发商为使用 AI 艺术道歉](https://www.theverge.com/games/898771/crimson-desert-dev-apologizes-ai-art) | The Verge | 3+5 |

---

### 💡 趋势洞察

#### 1. 智能硬件进入「专利深水区」

**观察**: 大疆正式起诉影石（6 项专利纠纷，法院已立案），影石遭核心供应商「排他」施压。

**洞察**: 智能硬件行业从「野蛮生长」进入「规范发展」阶段，专利成为竞争武器。

**建议**: 
- 设计团队需建立 IP 审查流程，提前评估专利风险
- 关注机器人 HMI 设计机会（宇树科技验证商业化）

#### 2. AI 伦理从讨论走向行动

**观察**: 出版业（Hachette 撤回 AI 生成小说）和游戏业（Crimson Desert 开发商道歉）率先建立 AI 使用边界。

**洞察**: AI 伦理不再是空泛讨论，行业开始建立具体边界。

**建议**: 
- 设计师应建立个人/团队 AI 使用伦理准则
- 明确标注 AI 生成内容，建立审核流程

#### 3. 关怀设计成为新热点

**观察**: Core77 读者项目涌现关怀设计案例（痴呆症患者 AI 助手、老年人专用指甲剪）。

**洞察**: 设计从「商业导向」转向「社会价值导向」，老龄化社会催生关怀设计需求。

**建议**: 
- 关注老年人、残障人士等特定群体需求
- 将关怀设计思维融入日常项目

---

### 💡 今日设计思考

> **当专利战遇上 AI 伦理，设计师如何平衡创新与风险？**

今日两条主线——大疆影石专利战和 AI 伦理争议——揭示了一个共同趋势：**行业从野蛮生长进入规范发展阶段**。

1. **创新需要边界意识** — 专利风险评估成为设计流程的必要环节
2. **AI 使用需要透明化** — 明确标注、建立审核、尊重版权
3. **新机会在规范中诞生** — 专利规避设计、AI 伦理咨询等新服务需求

---

### 📅 明日关注

- [ ] [大疆 Avata 360 发布](https://www.huxiu.com/article/4844500.html)（3 月 26 日，直接对标影石影翎）
- [ ] [大疆影石专利案涉案专利详情曝光](https://www.huxiu.com/article/4844500.html)（评估设计影响范围）
- [ ] [AI 网红奖项参赛情况和评选标准](https://www.theverge.com/ai-artificial-intelligence/898781/ai-personality-of-the-year-influencer-contest)（$20,000 奖金）
- [ ] [Samsung AirDrop 功能用户体验反馈](https://www.theverge.com/tech/898815/samsung-quick-share-airdrop-support-galaxy-s26)（韩国今日推送）
- [ ] [宇树科技产品设计细节和 HMI 方案](https://www.pingwest.com/a/312363)（全球第一量产规模）

---

### 📌 附：今日排除内容（不符合筛选标准）

| 内容 | 排除原因 |
| --- | --- |
| 联想焕新季营销稿 | 纯市场宣传，无实质设计/体验创新 |
| PITAKA 哈佛联名手机壳 | 常规周边产品，无趋势意义 |
| 多数融资八卦 | 无战略意义的早期融资传闻 |
| 成品油价格调控 | 与设计师无关的宏观经济政策 |

---

*本报告由 AI 自动生成，重大信息建议人工核实*  
*筛选标准执行：共收录 24 条情报，排除~60 条纯营销/常规更新内容，通过率 28%*
```

---

### 📊 周报示例（结构化表格格式）

```markdown
# 📊 AI/硬件/手机情报周报

**日期**: 2026 年 3 月 23 日  
**覆盖时段**: 3 月 17 日 -3 月 23 日（2026-W12）  
**情报官**: 梨然 - 阿里版  

---

### 🔥 本周头条 Top5（P0 级·S 级情报）

| 排名 | 公司/机构 | 事件 | 影响评级 | 来源 | 条件 |
| --- | --- | --- | --- | --- | --- |
| 1 | 大疆 DJI | [大疆正式起诉影石，6 项专利纠纷](https://www.huxiu.com/article/4844500.html) | ⭐⭐⭐ | 虎嗅网 | 1+4 |
| 2 | NVIDIA | [GTC 大会发布 Vera Rubin 架构](https://www.jiqizhixin.com/) | ⭐⭐⭐ | 机器之心 | 1+2 |
| 3 | 宇树科技 | [四足 + 人形机器人量产规模全球第一](https://www.pingwest.com/a/312363) | ⭐⭐ | 品玩 | 1+2 |
| 4 | Samsung | [Galaxy S26 原生支持 AirDrop](https://www.theverge.com/tech/898815/samsung-quick-share-airdrop-support-galaxy-s26) | ⭐⭐ | The Verge | 1+2 |
| 5 | OpenArt+Fanvue | [AI Personality of the Year 奖项](https://www.theverge.com/ai-artificial-intelligence/898781/ai-personality-of-the-year-influencer-contest) | ⭐⭐ | The Verge | 2 |

---

### 📱 手机领域

| 公司 | 动态 | 关键信息 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| 华为 | [问界 M6/M8 等多车型搭载 896 线激光雷达](https://www.ifanr.com/) | 896 线双光路图像级激光雷达 | 爱范儿 | 1+2 |
| 华为 | [畅享 90 Pro Max 发布，8500mAh 电池](https://www.ifanr.com/) | 华为首款 WiFi7 手机 | 爱范儿 | 1 |

**本周焦点**: 跨生态互联（Samsung-AirDrop）+ 超长续航（华为 8500mAh）

---

### 🤖 AI 领域

#### 大模型进展

| 公司/机构 | 模型/技术 | 亮点 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| Cursor | [承认 Composer 2 基于中国 Moonshot AI 的 Kimi 2.5](https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/) | 估值$293 亿的初创承认使用中国开源模型 | TechCrunch | 2+4 |
| NVIDIA | [Vera Rubin 架构算力平台](https://www.jiqizhixin.com/) | GTC 大会发布 | 机器之心 | 1+2 |

#### AI 应用/产品

| 公司 | 产品 | 功能 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| OpenArt+Fanvue | [AI Personality of the Year 奖项](https://www.theverge.com/ai-artificial-intelligence/898781/ai-personality-of-the-year-influencer-contest) | $20,000 奖金，ElevenLabs 支持 | The Verge | 2 |
| GitHub | [TradingAgents 多智能体金融交易框架 38K+ stars](https://github.com/trending) | 多 Agent 协作在垂直领域落地 | GitHub Trending | 2+5 |

**本周焦点**: AI 伦理从讨论走向行动（出版业/游戏业）+ 多 Agent 垂直领域落地

---

### 🔌 智能硬件

| 公司 | 产品 | 功能 | 来源 | 条件 |
| --- | --- | --- | --- | --- |
| 宇树科技 | [四足 + 人形机器人](https://www.pingwest.com/a/312363) | 全球第一量产规模，持续盈利数亿 | 品玩 | 1+2 |
| 博匠智能 | [建造机器人](https://www.pingwest.com/a/312353) | 建筑业机器人应用 | 品玩 | 2 |

**本周焦点**: 机器人商业化验证成功（宇树科技盈利）

---

### 🎨 设计领域

| 类型 | 动态 | 来源 | 条件 |
| --- | --- | --- | --- |
| 空间设计 | [Walter Van Beirendonck 设计太空主题儿童游乐空间](https://www.dezeen.com/2026/03/23/walter-van-beirendonck-space-themed-playscape-belgian-arts-campus/) | Dezeen | 3+5 |
| 办公设计 | [Snøhetta 设计台中金融办公室](https://www.dezeen.com/2026/03/22/good-finance-office-snohetta-taichung/) | Dezeen | 3+4 |
| AI 伦理 | [游戏《Crimson Desert》开发商为使用 AI 艺术道歉](https://www.theverge.com/games/898771/crimson-desert-dev-apologizes-ai-art) | The Verge | 3+5 |

**本周焦点**: AI 伦理争议（游戏/出版业）+ 时尚设计师跨界空间设计

---

### 💡 深度趋势洞察

#### 一、智能硬件进入「专利深水区」

##### 📊 事实层（观察）

大疆正式起诉影石（6 项专利纠纷，法院已立案），影石遭核心供应商「排他」施压（7 家光学镜头、8 家结构件、3 家屏幕、2 家电池）。

**关键信号**:
- 信号 1: 大疆影石专利战开启（6 项专利纠纷）
- 信号 2: 影石遭供应商「排他」施压（18 家核心供应商）
- 信号 3: 宇树科技机器人商业化验证成功（持续盈利数亿）

**信号强度评估**:

| 信号 | 弱 → 强 | 评估 |
|------|--------|------|
| 专利战 | ████████░░ | 强（头部企业正面交锋） |
| 供应链压力 | ███████░░░ | 强（核心供应商站队） |
| 商业化验证 | ████████░░ | 强（持续盈利） |

---

##### 🧠 解读层（分析）

**为什么现在发生？**

1. **行业成熟**: 智能硬件从「野蛮生长」进入「规范发展」
2. **竞争加剧**: 头部企业用专利武器保护创新
3. **资本压力**: 影石上市后需要新故事（无人机百亿市场）

**驱动因素分析**:

| 因素 | 影响力 | 说明 |
|------|--------|------|
| 技术驱动 | ⭐⭐⭐⭐ | 传感器/算力/算法成熟 |
| 市场驱动 | ⭐⭐⭐ | 企业降本增效需求 |
| 竞争驱动 | ⭐⭐⭐⭐⭐ | 大疆影石正面交锋 |

**行业影响链**:

```
大疆起诉影石 
  → 供应链「站队」压力
    → 影石生产受限，成本上升
      → 价格战升级
        → 行业利润进一步挤压
          → 后来者进入门槛提高
```

---

##### 🔮 预判层（预测）

**短期（1-3 个月）**: 
- 更多智能硬件企业加强专利布局
- 设计团队需建立 IP 审查流程

**中期（3-12 个月）**: 
- 专利交叉许可可能出现
- 机器人 HMI 设计需求增长

**长期（1-3 年）**: 
- 行业形成专利交叉许可格局
- 后来者进入门槛提高

**不确定性因素**:
- 诉讼结果（影石败诉可能失去竞争资格）
- 供应链「站队」持续时间
- 资本市场态度

**关键观察指标**:
- [ ] 大疆 Avata 360 发布（3 月 26 日）价格和销量
- [ ] 影石反诉或和解声明
- [ ] 影石供应链调整进展

---

### 🎯 设计机会识别

| 机会领域 | 机会描述 | 优先级 | 时间窗口 | 所需能力 |
|----------|----------|--------|----------|----------|
| 机器人 HMI 设计 | 宇树科技等验证商业化，机器人交互设计需求增长 | 高 | 6-12 个月 | 运动控制理解、安全设计 |
| 专利规避设计 | 大疆影石战引发 IP 风险评估需求 | 高 | 3-6 个月 | 专利分析、设计创新 |
| AI 伦理咨询 | 内容行业建立 AI 使用规范 | 中 | 6-12 个月 | 伦理框架、审核流程 |

---

### ⚠️ 风险预警

| 风险 | 影响程度 | 可能性 | 应对建议 |
|------|----------|--------|----------|
| 专利纠纷限制设计自由度 | 高 | 中 | 建立 IP 审查流程，提前评估 |
| AI 生成内容版权纠纷 | 中 | 高 | 明确标注，建立审核机制 |
| 供应链依赖风险 | 中 | 中 | 多元化技术选型 |

---

### 📅 下周关注

#### 重要事件日历

| 日期 | 事件 | 类型 | 关注理由 |
|------|------|------|----------|
| 3/26 | 大疆 DJI Avata 360 发布 | 硬件 | 直接对标影石影翎 |
| 3/26 | 谷歌 AI 发布会 | AI | 可能有 AI 助手新动态 |
| 3/28 | Figma 社区大会 | 设计 | AI 设计工具更新 |

#### 持续关注列表

- [ ] 大疆影石专利案涉案专利详情
- [ ] Samsung AirDrop 功能用户体验反馈
- [ ] AI 网红奖项参赛情况和评选标准
- [ ] 宇树科技产品设计细节和 HMI 方案

---

### 📚 本周精选链接

#### 必读文章（深度分析）

- [大疆鏖战影石](https://www.huxiu.com/article/4844500.html) — 虎嗅网深度报道
- [Cursor admits its new coding model was built on top of Moonshot AI's Kimi](https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/) — TechCrunch
- [AI influencer awards season is upon us](https://www.theverge.com/ai-artificial-intelligence/898781/ai-personality-of-the-year-influencer-contest) — The Verge

#### 值得体验的产品

- [TradingAgents](https://github.com/TauricResearch/TradingAgents) — 多智能体金融交易框架
- [MoneyPrinterV2](https://github.com/FujiwaraChoki/MoneyPrinterV2) — AI 短视频生成工具

---

### 📊 本周统计

| 指标 | 数值 | 环比 |
|------|------|------|
| 监测源数量 | 25 个 | +3 |
| 收录情报数 | 35 条 | +7 |
| S 级情报 | 5 条 | - |
| A 级情报 | 10 条 | +2 |
| B 级情报 | 20 条 | +5 |
| 筛选通过率 | 15% | -1% |

**领域分布**:

| 领域 | 数量 | 占比 |
|------|------|------|
| AI | 15 条 | 43% |
| 手机 | 6 条 | 17% |
| 硬件 | 8 条 | 23% |
| 设计 | 6 条 | 17% |

---

*本报告由 AI 自动生成，重大信息建议人工核实*  
*筛选标准执行：共收录 35 条情报，排除~150 条纯营销/常规更新内容，通过率 15%*
```

---

## 筛选条件详解

情报必须满足以下**至少一个**条件：

| 条件 | 说明 | 示例 |
|------|------|------|
| **知名大厂动态** | 苹果/谷歌/微软/阿里/腾讯/字节/华为/小米的重大发布 | 苹果发布会、谷歌 I/O |
| **趋势洞察** | OS、AI 语音助手、人机交互、AI 趋势、硬件发展的新方向 | AI 设计工具、新交互方式 |
| **设计哲学启发** | 品牌理念、设计哲学、叙事逻辑 | 设计思想深度文章 |
| **竞品策略分析** | 设计策略、体验差异、创新思路 | 竞品对比分析 |
| **设计判断力提升** | 深度分析、设计趋势报告、用户行为研究 | 趋势报告、用户研究 |

---

## 排除内容

以下内容**不会**出现在情报中：

- ❌ 纯市场宣传（新闻稿、广告）
- ❌ 常规版本更新（小版本号迭代）
- ❌ 融资八卦（未经证实的传闻）
- ❌ 参数对比（跑分、规格表）
- ❌ 营销话术（"革命性"、"颠覆性"等）

---

## 使用技巧

### 1. 定时查看
- 日报：每日 19:00 自动推送
- 周报：每周一 9:00 自动推送

### 2. 定向查询
```
查询今日 AI 领域动态
查询本周设计领域更新
查询手机领域新品
```

### 3. 深度分析
```
分析本周 AI 设计工具趋势
对比苹果和谷歌的设计策略
```

---

*设计师情报站 - 为设计师打造的行业情报分析工具*  
*最后更新：2026-03-23 (v1.3.1)*
