# 🏢 企服助手 Skill

> 专业的园区企业服务智能助手（完全自包含版 v2.0.0）

---

## 简介

企服助手是一个专为园区企业服务设计的智能助手，可以帮助你完成：

- 📊 **客户管理** — 档案管理、画像分析、风险提醒
- 💰 **费用催缴** — 监控逾期、分级提醒、跟进记录
- 🔧 **工单分派** — 自动分派、SLA监控、超时升级
- 📦 **库存监控** — 水位监控、补货提醒、出入库管理
- 📝 **续租预警** — 提前预警、生成续租方案
- 🤝 **C+服务** — 需求挖掘、服务匹配、资源调度
- 📋 **走访管理** — 计划生成、任务提醒、记录归档
- 📈 **KPI报告** — 自动生成、趋势分析

---

## 快速安装

### 方式一：WorkBuddy 一键安装（推荐）

在 WorkBuddy 对话框中输入：

```
@WorkBuddy 安装技能 enterprise-service-assistant
```

### 方式二：手动安装

1. 将 `enterprise-service-assistant` 文件夹复制到：
   ```
   ~/.workbuddy/skills/enterprise-service-assistant/
   ```

2. 重启 WorkBuddy 会话

3. 首次启动时，按照引导完成配置

---

## 首次配置

启动后，企服助手会自动检测到你是新用户，并展示配置引导。

### 必填项
- 项目名称
- 数据文件路径（Excel）

### 可选项
- 企微 Webhook（用于消息推送）
- 隐私脱敏规则
- 业务技能开关

### 配置步骤

1. 复制模板：
   ```
   knowledge/TEMPLATE.md → knowledge/PROJECT_KB.md
   ```

2. 填写信息：
   ```markdown
   - 项目名称: [你的项目名]
   - 数据文件路径: [你的Excel文件完整路径]
   ```

3. 验证配置：
   ```
   @企服助手 知识库已配置，帮我验证一下
   ```

---

## 使用示例

| 命令 | 功能 |
|------|------|
| `@企服助手 查询客户 A栋-601` | 查询客户信息 |
| `@企服助手 客户画像 示例企业` | 查看客户画像 |
| `@企服助手 催缴检查` | 检查费用收缴状态 |
| `@企服助手 库存检查` | 检查库存水位 |
| `@企服助手 续租检查` | 检查合同到期情况 |
| `@企服助手 创建工单 A栋-601 水管漏水` | 创建报修工单 |

---

## 文件结构

```
enterprise-service-assistant/
├── SKILL.md                ← 技能说明和触发词
├── AGENTS.md               ← 通用配置
├── SOUL.md                 ← 人格设定
├── IDENTITY.md             ← 身份设定
├── TOOLS.md                ← 工具说明
├── AGENT.json              ← 技能元数据
├── scripts/                ← 📂 核心业务逻辑（Python脚本）
│   ├── data_manager.py
│   ├── fee_calculator.py
│   ├── contract_renewal.py
│   ├── visit_manager.py
│   └── ...（共22个脚本）
├── knowledge/              ← 📂 项目知识库
│   ├── PROJECT_KB.md       ← 你的项目配置（核心！）
│   ├── TEMPLATE.md         ← 配置模板
│   ├── ONBOARDING.md       ← 首次引导
│   ├── INSTALL.md          ← 安装指南
│   └── HOW_TO_SHARE.md     ← 分享指南
└── README.md               ← 本文件
```

**关键区分**：
- 通用文件（SKILL.md, AGENTS.md 等） → 随 Skill 分享，不需要修改
- 项目知识库（knowledge/） → 每个用户独立，包含你的项目数据配置

---

## 依赖技能

企服助手核心逻辑已完全自包含（`scripts/` 目录），以下技能为可选增强：

| 技能 | 用途 |
|------|------|
| `docx` | Word 文档处理（可选） |
| `pdf` | PDF 文档处理（可选） |
| `xlsx` | Excel 表格处理（可选） |
| `tencent-docs` | 腾讯文档 MCP 工具（可选） |
| `online-search` | 联网搜索（可选） |
| `agent-browser` | 浏览器自动化（可选） |

---

## 常见问题

### Q: 我的 Excel 格式和模板不一样怎么办？
A: 在 `PROJECT_KB.md` 中描述你的工作表结构即可，助手会自动适配。

### Q: 可以不用企微通知吗？
A: 可以。通知渠道是可选的，没有 Webhook 也能使用查询功能。

### Q: 数据安全吗？
A: 所有数据都在你的本地电脑上，不会上传到云端。助手只读取你指定的文件。

### Q: 如何分享给其他同事？
A: 参考 `knowledge/HOW_TO_SHARE.md`，将技能包文件夹打包分享即可。

---

## 技术支持

如有问题，请查阅：
- `knowledge/ONBOARDING.md` — 新用户引导
- `knowledge/INSTALL.md` — 安装指南
- `knowledge/HOW_TO_SHARE.md` — 分享指南

---

**让企服助手帮你提升服务效率！** 🚀
