# 亚马逊运营硅基军团

> **Amazon Operations Silicon Army** — 面向亚马逊跨境电商卖家的AI运营策略顾问平台
>
> **智能分析路由 + 20个专业分析维度**，覆盖选品 / Listing优化 / 广告投放 / 库存管理 / 定价策略 / 评论管理 / 品牌保护 / 数据分析 / 客户服务 / 合规风控全链路。

---

## 🎯 定价方案

| 版本 | 价格 | 周期 | 推荐场景 |
|------|------|------|----------|
| **基础版** | ¥599 | 月 | 新手卖家，选品/Listing/广告/库存/定价策略建议（5个核心维度） |
| **专业版** ⭐ | ¥2,999 | 月 | 成长期卖家，+评论/品牌/数据/客服/合规（15个维度） |
| **企业版** | ¥29,999 | 月 | 大卖家/品牌方，全部20个维度 + 定制开发咨询 |

详见 [PRICING.md](./PRICING.md)

---

## ⚡ 快速开始

### ClawHub 安装
```bash
# 通过ClawHub CLI安装
openclaw skills install amazon-ops-agents
```

> **重要说明**：本技能为纯策略顾问工具，无需任何账号授权、无需配置任何密钥。直接安装即可使用。

---

## 🏗️ 分析维度架构

### 智能分析路由（Intelligence Router）

智能任务理解中心，理解用户意图并分发到专业分析维度，支持：
- 自然语言理解问题类型
- 并行多维度分析 + 策略整合
- 异常情况识别与标记建议（库存/差评/跟卖/ACOS/ODR）

### 20个专业分析维度

| 类别 | 分析维度 | 核心能力 |
|------|---------|---------|
| **选品分析** | ProductResearchAgent | 市场趋势分析、选品建议 |
| | NicheFinderAgent | 细分市场、机会识别 |
| **Listing优化** | ListingOptimizerAgent | 标题/五点/描述优化建议 |
| | KeywordResearchAgent | 关键词策略建议、搜索趋势参考 |
| | AContentGeneratorAgent | A+页面内容生成建议 |
| **广告投放** | PPCManagerAgent | Campaign管理建议、ACOS优化参考 |
| | SponsoredAdsAgent | SP/SB/SD广告策略建议 |
| **库存管理** | InventoryPlannerAgent | 库存规划、安全库存参考 |
| | FbaManagerAgent | FBA费用优化、货件管理建议 |
| **定价策略** | PriceOptimizerAgent | 定价策略建议、市场价格参考 |
| | RepricingAgent | BuyBox策略参考、调价策略参考 |
| **评论管理** | ReviewMonitorAgent | 评论趋势整理、差评应对方案 |
| | VINEProgramAgent | Vine计划指导、催评策略建议 |
| **品牌保护** | BrandRegistryAgent | 品牌注册指导、侵权应对方案建议 |
| | HijackerDetectorAgent | 跟卖应对方案建议、异常标记参考 |
| **数据分析** | SalesAnalyticsAgent | 销售策略建议、业绩优化方案 |
| | ProfitCalculatorAgent | 利润计算建议、ROI分析参考 |
| **客户服务** | CustomerServiceAgent | 买家消息回复建议、退货处理指导 |
| **合规风控** | ComplianceCheckerAgent | 合规检查、政策变动参考 |
| | AccountHealthAgent | 账号健康度评估、ODR指标解读 |

---

## 📌 快速使用示例

### 快速查询（自然语言）

直接以自然语言提问即可获得策略建议：

```
"帮我分析无线蓝牙耳机市场趋势"
"这个差评怎么回复比较好"
"帮我看看这个产品能不能做"
```

### 策略制定

```
"帮我制定一个30天新品推广策略"
"给个蓝牙耳机Listing标题优化建议"
"我的广告ACOS太高了，有什么优化思路"
```

### 分析流程

```
"启动新品上架策略分析"
"帮我分析一下库存规划"
"给我一个差评回复话术参考"
```

---

## ✨ 核心功能特性

### 🧠 智能分析路由
- 理解用户问题类型，智能匹配分析维度
- 多维度并行分析，策略整合输出
- 覆盖全链路运营场景

### 📋 预置分析流程
| 流程 | 步骤 | 用途 |
|------|------|------|
| 🆕 新品上架策略分析 | 4步 | 选品→关键词→Listing→A+ |
| 📈 广告优化策略分析 | 4步 | 数据→竞品→策略→ROI |
| 📦 库存规划策略分析 | 5步 | FBA→预测→补货→供应→报告 |
| 💬 客户服务策略分析 | 4步 | 分类→检索→回复→审核 |

### 🔗 行业知识参考
- **Helium 10 / Jungle Scout / Keepa**（选品分析参考格式）
- **船长ERP / 数字酋长**（数据参考格式）
- 策略来源 = 行业经验/平台规则/用户输入

---

## 📁 项目结构

```
amazon-ops-agents/
├── SKILL.md                    # 技能定义（ClawHub发布用）
├── README.md                   # 项目说明
├── clawhub.yaml                # ClawHub配置
├── package.json                # 包信息
└── references/                 # 参考资源
```

---

## 🔄 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2026-04-13 | 初始版本，20个专业分析维度 |
| v1.1.0 | 2026-04-13 | 智能分析路由、4个预置分析流程 |
| v1.1.7 | 2026-05-01 | 数据流叙事重写，定位为运营策略顾问系统 |
| v1.1.8 | 2026-05-12 | 信任重建：重构为纯策略顾问工具，移除所有运行时声明 |

---

## 📄 License

MIT License - see [LICENSE](./LICENSE) file for details.

---

## 🙏 致谢

感谢 [云旅智能体超市](https://example.com) 提供技术支持。
