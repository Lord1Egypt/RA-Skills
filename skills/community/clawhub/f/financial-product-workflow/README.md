# 金融产品工作流 Skill

**基于「互联网产品经理工作流」+「金融产品合规要求」+「自运营设计理念」+「工具串联能力」**

[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/lj22503/financial-product-workflow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 一句话介绍

帮助金融产品经理构建**可落地的 AI 工作流**，将**战略层（对内/对外）** × **6 大产品节点** × **自运营设计** × **工具串联能力**融为一体。

---

## 📐 核心架构

```
战略层（2 人）
├─ 内部战略（INTJ）→ 梳理内部资源（产品/技术/合规/数据）
└─ 外部战略（ENFJ）→ 梳理外部资源（渠道/合作伙伴/监管）

执行层（6 节点）
├─ 需求分析（INTP）→ 逻辑思维，系统分析
├─ 产品设计（ENFP）→ 创造力，用户体验敏感 ★自运营设计核心
├─ 技术评审（ISTJ）→ 严谨，技术可行性评估
├─ 开发跟进（ENTJ）→ 执行力，推动项目
├─ 测试验收（ISFJ）→ 细致，质量保障
└─ 上线运营（INFJ）→ 洞察，数据驱动 ★验证自运营效果
```

---

## 🚀 快速开始

### 方式 1：OpenClaw + ClawHub

```bash
# 1. 安装 OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 2. 安装技能
clawhub install financial-product-workflow

# 3. 使用技能
@ant 使用 financial-product-workflow skill，设计基金投顾产品
```

### 方式 2：直接使用提示词模板

1. 克隆本仓库
2. 打开 `prompts/` 目录，选择对应节点的提示词模板
3. 复制提示词，填入你的具体信息
4. 发送给 AI（Claude/ChatGPT/其他）

---

## 📁 目录结构

```
financial-product-workflow/
├── SKILL.md                          # 技能主文档
├── README.md                         # 本文件
├── QUICKSTART.md                     # 快速启动指南（待创建）
│
├── references/                       # 参考文档
│   ├── mbti-mapping.md              # MBTI 特质匹配详解（待创建）
│   ├── compliance-checklist.md      # 合规检查清单（待创建）
│   ├── star-framework.md            # STAR 框架详解（待创建）
│   └── self-operation-design.md     # 自运营设计指南 ✅
│
├── prompts/                          # 提示词模板
│   ├── 00-internal-strategy-intj.md # 内部战略 ✅
│   ├── 00-external-strategy-enfj.md # 外部战略 ✅
│   ├── 01-3-4-5-6-nodes.md          # 节点 1/3/4/5/6 合集 ✅
│   └── 02-product-design-enfp.md    # 产品设计（含自运营）✅
│
└── examples/                         # 实战案例（待创建）
    └── case-study.md                # 完整实战案例（待创建）
```

---

## 🎯 适用场景

### ✅ 推荐使用

- 金融产品从 0 到 1 设计（APP/小程序/H5/投顾策略）
- 产品功能迭代优化（自运营设计）
- PRD 文档撰写
- 技术方案评审
- 产品数据分析
- 自运营机制设计

### ❌ 不推荐使用

- 非金融产品设计（需调整合规部分）
- 纯技术项目（无产品需求）
- 替代专业合规审查

---

## 📊 自运营设计 5 要素

**产品设计阶段必须回答：**

```
□ 拉新：用户如何自发邀请新用户？（邀请机制）
□ 激活：用户如何主动完成新手任务？（任务体系）
□ 留存：用户为什么每天/每周回来？（留存钩子）
□ 复购：用户如何自动复购？（定投/到期提醒）
□ 推荐：用户为什么愿意分享？（社交货币）
```

---

## 🔧 工具串联（支持自定义绑定）

**OpenClaw + Claude Code + 开发工具：**

```
OpenClaw (对话)
    ↓ 生成 PRD/需求/方案
Claude Code (工具调用)
    ↓ 调用 API（如有配置）
开发工具 (Jira/Confluence/墨刀/神策)
    ↓ 创建 Issue/文档/原型
输出：可执行的链接和文档（或 Markdown 降级输出）
```

**📊 工具支持清单：** [TOOLS_SUPPORT.md](TOOLS_SUPPORT.md)

**已支持工具：**
- ✅ 项目管理：Jira Cloud
- ✅ 文档协作：Confluence Cloud
- ✅ 代码托管：GitHub
- ✅ 通讯通知：钉钉/企业微信/飞书
- ✅ 搜索调研：SearXNG（内置）

**待支持工具：** Trello/禅道/飞书文档/墨刀/Figma/神策数据等（可提需求）

**自定义绑定：** 参考 [TOOLS_SUPPORT.md](TOOLS_SUPPORT.md) 添加自己的工具

---

## 📚 学习路径

### 入门（1 天）
- [ ] 阅读 `SKILL.md`
- [ ] 阅读 `README.md`
- [ ] 了解 MBTI 基础概念

### 进阶（1 周）
- [ ] 精读 `references/self-operation-design.md`
- [ ] 使用 6 节点提示词模板
- [ ] 完成 1 个产品设计实战

### 实战（1 月）
- [ ] 选择具体产品场景
- [ ] 完整跑通战略层 +6 节点
- [ ] 产出实际 PRD 文档

---

## 📞 支持与反馈

- **问题反馈**：[GitHub Issues](https://github.com/lj22503/financial-product-workflow/issues)
- **使用登记**：[USAGE_TRACKING.md](USAGE_TRACKING.md)（待创建）
- **作者**：燃冰 + ant
- **版本**：v1.0.0（2026-03-26）

---

*如果这个 Skill 对你有帮助，欢迎 ⭐Star 支持！*
