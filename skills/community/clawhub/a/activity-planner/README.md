# activity-planner · AI 活动策划方案生成器

[![Security Audit](https://img.shields.io/badge/Security_Audit-Pass-brightgreen)](#)
[![Version](https://img.shields.io/badge/version-0.1.0-blue)](#)
[![ClawHub](https://img.shields.io/badge/ClawHub-activity--planner-orange)](https://clawhub.ai/simonomi2/activity-planner)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](#)

> 一站式 AI 活动策划助手。输入活动类型 + 预算 + 目标人群，3 分钟输出完整可落地方案。

---

## 🎯 What does it do?

从「我要搞个活动」到「拿方案就能干」，全程 AI 驱动：

| 模块 | 产出 |
|---|---|
| 活动定位 | 目标量化 + 受众洞察 + 竞品差异化 |
| 创意概念 | 2-3 个主题方向 + Slogan + 视觉建议 |
| 流程设计 | 预热→执行→延续，精确到分钟的甘特式时间线 |
| 预算分配 | 按类别明细表 + 机动金预留 |
| 宣传推广 | 渠道选择 + 内容规划 + 节奏安排 + 实时监控 |
| 人员分工 | 角色清单 + 职责分工 |
| 物料文案 | 邀请函·海报·社媒·短视频脚本·现场物料 — 可直接复制使用 |
| 话术脚本 | 邀约话术·主持串词·销售转化·客服FAQ |
| 风险预案 | 3-5 个风险点 + 预防措施 + 应急方案 |
| 效果评估 | 量化 KPI + 数据回收方式 + 复盘节点 |

**输出为结构化 HTML 报告，可直接打印或在浏览器中查看。**

---

## 🚀 Quick Start

### 安装

```bash
clawhub skill install simonomi2/activity-planner
```

### 使用

在 WorkBuddy / OpenClaw 中对 agent 说：

```
帮我策划一个新品发布会
- 类型：科技产品线下发布
- 预算：5万
- 目标人群：25-35岁科技爱好者
- 时间：下月第一个周末
- 地点：北京
- 预计参与：200人
```

Agent 会逐项收集信息，然后自动生成完整 HTML 方案报告。

---

## 📋 适用场景

- 🚀 **新品发布会** — 产品定位·传播节奏·媒体接待
- 🎉 **年会/盛典** — 主题·节目流程·互动抽奖
- 🏪 **快闪店** — 选址·场景设计·打卡传播
- 🎫 **促销活动** — 引流·转化·裂变·复购闭环
- 👥 **社群活动** — 线上裂变·线下沙龙·会员日
- 🎪 **展会参展** — 展台设计·互动体验·留资转化

---

## 🛡️ 安全审计

本技能已通过 ClawHub 安全审计（Security Audit）。

没有隐藏的 prompt 注入、数据外发或恶意代码。可放心使用。

---

## 📸 输出预览

> 💡 在此处添加方案输出的 HTML 报告截图

*（方案输出示例稍后补充）*

---

## 📦 技能结构

```
activity-planner/
├── SKILL.md                 ← 技能定义（前端卡片 + 工作流）
├── README.md                ← 本文件
├── assets/
│   └── plan_template.html   ← HTML 输出模板
└── references/
    ├── activity_framework.md     ← 各类型活动策划要点
    ├── budget_guide.md           ← 预算分配参考
    ├── copywriting_templates.md  ← 物料文案模板
    ├── promotion_monitor.md      ← 推广监控体系
    └── script_templates.md       ← 话术脚本模板
```

---

## 🔮 Roadmap

- [ ] v0.2 — 3 套行业预设模板（新品发布 / 节日营销 / 线下沙龙）
- [ ] v0.3 — 支持导出 Markdown / Notion
- [ ] v1.0 — 中英双语支持 + 可视化流程图

---

## 🤝 反馈与贡献

- 🐛 问题反馈：[GitHub Issues](https://github.com/Simonomi2/activity-planner/issues)
- 💬 讨论交流：[OpenClaw Discord](https://discord.gg/openclaw)
- ⭐ 喜欢这个技能？点个 Star 支持一下！

---

## 📄 License

MIT © [Simonomi2](https://clawhub.ai/simonomi2)
