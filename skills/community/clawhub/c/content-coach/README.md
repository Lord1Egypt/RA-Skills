# 🎬 Content Coach — 自媒体创作教练

> **基于 Alex Hormozi、Justin Welsh、Dan Koe、MrBeast 四大方法论，一个帮你从0到1做好自媒体的 AI 技能。**

本技能是 **[OpenClaw](https://openclaw.ai)** (开源 AI 个人助手) 的 Skill 扩展包。安装后，你的 AI 助手将化身自媒体创作教练，提供从定位、内容生产到商业变现的全周期辅导。

---

## ✨ 它能帮你什么

| 场景 | 它会怎么做 |
|------|-----------|
| "我不知道做什么方向" | 定位诊断 → 帮你找到高价值窄赛道 |
| "发了没人看" | Hook分析 → 优化标题/封面/前5秒 |
| "怎么做内容" | 脚本模板 → 给可直接套用的公式 |
| "怎么变现" | 路径规划 → 从免费到付费的阶梯设计 |
| "没动力做了" | 心法辅导 → 你缺的不是能力，是系统 |

---

## 📦 安装

### 前提条件
- 安装 [OpenClaw](https://docs.openclaw.ai)（2026.4+）
- 推荐配合 Claude Code / DeepSeek / GPT-4 使用

### 方式一：从 ClawHub 安装（推荐）
```bash
openclaw skills install content-coach
```

### 方式二：手动安装
```bash
git clone https://github.com/Yushuo-AIcoder/content-coach.git
# 将 content-coach 目录放到 workspace/skills/ 下
# 重启 OpenClaw，技能自动加载
```

安装后运行 `openclaw skills list`，看到 ✅ `content-coach` 即成功。

---

## 📂 技能结构

```
content-coach/
├── SKILL.md                              ← 核心入口，自动诊断+按需加载
├── references/
│   ├── positioning.md                    ← 定位框架（找交集×定角度×窄化）
│   ├── content-production.md             ← 内容生产（三种模式×脚本模板×复用系统）
│   ├── hook-retention.md                 ← Hook与留存（MrBeast 黄金法则）
│   ├── monetization.md                   ← 变现路径（四层阶梯×Hormozi模型）
│   ├── energy-system.md                  ← 能量管理（上班族内容创作指南）
│   ├── mentality.md                      ← 创作心法（克服拖延与自我怀疑）
│   ├── masters.md                        ← 四大方法论速览
│   └── stage-diagnosis.md               ← 阶段性诊断（0→1→2→3 阶段）
└── scripts/                              ← 留给你以后加工具脚本
```

### 设计原则
- **按需加载**：SKILL.md 仅做导航，各模块拆分到 `references/`，减少不必要的 token 消耗
- **渐进披露**：AI 助手先判断用户阶段，再仅加载对应参考文件
- **可扩展**：`scripts/` 留空，方便你日后加入脚本化工具（如数据抓取、批量生成等）

---

## 🧠 方法论来源

| 大师 | 专长 | 对你最有用 |
|------|------|-----------|
| **Alex Hormozi** | 商业×内容获客 | 如何把内容变成生意引擎 |
| **Justin Welsh** | Solo 创作者路径 | 有全职工作怎么做内容 |
| **Dan Koe** | 意义感×创作哲学 | 找到你真正在乎的东西 |
| **MrBeast** | 内容节奏×Hook框架 | 为什么观众不划走 |

---

## 🔧 如何贡献

欢迎 PR！你可以在以下方向贡献：

- 📝 **新增 reference**：某个平台（抖音/小红书/B站）的专项运营指南
- 🛠️ **加入脚本**：数据分析、批量生成、RSS 监控等工具脚本
- 🌍 **多语言**：SKILL.md 英文版

---

## 📄 许可

MIT — 随意使用、修改、分发。

---

## 🙋 关于

本技能由 [@小福](https://github.com/Yushuo-AIcoder) 创建，灵感来自 榆烁 的自媒体创作需求。

> *"你不是没天赋，是没系统。"*
