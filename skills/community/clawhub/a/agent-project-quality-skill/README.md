# Project Quality Governance 🧭

> 一套面向 Codex 与工程 Agent 的开源质量治理 Skill，让技术规范、Bug/优化日志与验证流程保持清晰、可检索、可追踪。

它把成熟工程团队的文档治理方法压缩成一条轻量工作流：**先读取核心规则，再按任务精准定位，最后按风险完成验证**。既减少无效上下文与重复检查，也不会覆盖项目历史或虚构证据。

## ✨ 为什么值得使用

- 🛡️ **核心规则前置**：安全、数据、权限、范围和验证底线始终位于规范顶部。
- 🎯 **按任务精准读取**：通过目录与任务路由，只加载当前工作真正需要的章节。
- 🧠 **控制上下文成本**：为入口文件、活动日志和终端输出建立明确预算。
- 🐞 **Bug 与优化分治**：两类记录拥有不同字段，同时共享统一状态索引。
- 🗂️ **活动记录与历史归档分离**：日常开发保持轻量，需要追溯时再按 ID 定向读取。
- 🧪 **L1 / L2 / L3 分层验收**：根据实际风险选择验证强度，而不是每次都运行全量检查。
- 🔍 **自动一致性校验**：检查标题层级、ID、字段、证据、时间与归档唯一性。
- 📌 **尊重项目事实**：保留历史、修正关系与替代关系，不伪造时间和测试证据。
- 🌍 **语言自适应**：根据目标项目语言生成对应规范，适合不同团队与工程环境。

## ⚙️ 工作原理

```text
📦 检查现有仓库
        ↓
🛡️ 提取每次必读的核心规则
        ↓
🗺️ 建立“任务类型 → 必读章节”路由
        ↓
📝 规范 Bug / 优化记录与活动索引
        ↓
🧪 按风险选择 L1 / L2 / L3 验收
        ↓
🔍 运行只读校验器
        ↓
✅ 输出可维护、可追踪的质量治理体系
```

### 📖 渐进式读取

```markdown
日常任务：核心规则 + 当前模块章节 + 活动日志

历史追溯：按 ID 或关键词读取对应归档

发布阶段：读取发布候选 + 执行 L3 完整验收
```

这种结构避免 Agent 每次重新扫描整份规范与全部历史，让开发过程更接近线性推进：

```text
定位 → 修改 → 定向验证 → 记录结果 → 交付
```

## 🚀 快速开始

### 1. 获取 Skill

```bash
git clone https://github.com/WuWorks/Agent-Project-quality-Skill.git
```

将仓库文件夹复制到 Codex skills 目录并重启 Codex，也可以直接阅读 `SKILL.md` 了解完整适用范围。

### 2. 调用示例

```text
使用 project-quality-governance 审查并优化当前项目的技术规范、Bug/优化日志和验证流程。
```

Skill 会先检查现有结构，再以最小改动补齐治理体系，不会擅自重写已有项目历史。

## 🧪 分层验收模型

| 等级 | 适用场景 | 典型验证 |
| --- | --- | --- |
| 🟢 L1 | 文案、样式、局部文档调整 | 差异检查与受影响内容确认 |
| 🟡 L2 | 单一模块逻辑或结构修改 | 相关测试，必要时执行构建 |
| 🔴 L3 | 高风险变更或正式发布边界 | 全量测试、检查、构建与交付验收 |

> Git 提交本身不会自动升级为 L3；验证等级由真实风险决定。

## 🔍 文档校验器

校验器只读取显式指定的文件并输出诊断，**不会自动修改项目文档**：

```bash
node scripts/validate-quality-docs.mjs \
  --spec path/to/technical-spec.md \
  --log path/to/active-log.md \
  --archives path/to/archive-1.md,path/to/archive-2.md \
  --agents path/to/agent-entrypoint.md \
  --workflow path/to/workflow.md
```

可通过 `--config path/to/config.json` 配置：

- 🆔 Bug 与优化 ID 前缀
- 🏷️ 类型与内容标签
- ✅ 完成状态和必填证据
- 📣 发布文案要求
- 📚 活动记录数量上限
- 📏 入口文件与上下文预算
- 🧱 标题层级和章节编号规则

运行校验器测试：

```bash
node --test scripts/validate-quality-docs.test.mjs
```

## 🗂️ 项目结构

```text
project-quality-governance/
├─ SKILL.md                         # Skill 入口与任务路由
├─ README.md                        # 开源项目说明
├─ CHANGELOG.md                     # 版本更新记录
├─ LICENSE                          # Apache-2.0
├─ agents/
│  └─ openai.yaml                   # Agent 展示信息
├─ references/
│  ├─ technical-spec-architecture.md
│  ├─ issue-and-improvement-log.md
│  └─ verification-workflow.md
└─ scripts/
   ├─ validate-quality-docs.mjs
   └─ validate-quality-docs.test.mjs
```

## ✅ 适用范围

适合：

- 创建、审查或重构技术规范
- 建立 Bug 与优化日志
- 设计分层验收和开发流程
- 控制 Agent 上下文与验证成本
- 检查工程文档结构和事实一致性

不适合：

- 普通营销文案
- 无结构的随手笔记
- 与工程质量治理无关的内容编辑

## 🔐 隐私与边界

- 不要求上传项目文件。
- 不读取未授权的私有研究、密钥或敏感资料。
- 不为了补全文档而虚构历史时间、负责人或验证证据。
- 校验脚本只读检查，不会自动改写用户文档。

## 📦 版本与许可

- 🏷️ [查看 Releases](https://github.com/WuWorks/Agent-Project-quality-Skill/releases)
- 📝 [查看更新日志](CHANGELOG.md)
- ⚖️ 基于 [Apache License 2.0](LICENSE) 开源发布

如果这个 Skill 对你的工程协作有帮助，欢迎 ⭐ Star、提交 Issue 或参与改进。
