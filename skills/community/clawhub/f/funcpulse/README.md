# FuncPulse - PRD/测试用例到代码变更的智能验证助手

FuncPulse 用于验证“需求和测试用例是否真的被代码实现覆盖”。它会分析 PRD、测试用例和多仓库代码变更，生成需求-用例-代码追踪矩阵、覆盖率、缺陷优先级、复现步骤、修复建议和标准化业务测试验证报告。

> 适合提测验收、需求回归、用例评审、多仓库联调、测试报告生成和 QA 质量复盘。

## 为什么值得收藏

- **需求不漏测**：把 PRD 需求点逐条映射到测试用例和代码实现。
- **多仓库友好**：适合前端、后端、网关、配置、任务脚本等跨仓库联动场景。
- **报告可交付**：直接生成业务测试验证报告，包含覆盖率、缺陷和追踪矩阵。
- **缺陷更清晰**：输出严重程度、关联需求、关联用例、复现步骤和修复建议。
- **验收更高效**：帮助测试、研发、产品快速判断“这次改动是否满足需求”。

## 典型使用场景

| 场景 | FuncPulse 能做什么 |
| --- | --- |
| 提测验收 | 检查需求点是否被代码和测试用例覆盖 |
| PRD 评审后 | 从需求中提取验证点，发现测试设计缺口 |
| 多仓库联调 | 分析跨仓库变更对业务流程和测试用例的影响 |
| 回归测试 | 识别需要重点回归的需求、接口和链路 |
| 测试报告 | 生成标准 Markdown 报告，便于归档和同步 |

## 快速开始

在支持 ClawHub/OpenClaw Skill 的环境中安装后，直接用自然语言触发：

```text
使用 funcpulse 分析这份 PRD 和当前代码变更，判断测试用例覆盖是否完整。
```

```text
用 FuncPulse 对这次多仓库改动生成业务测试验证报告，列出未覆盖需求和高优先级缺陷。
```

本地脚本使用方式：

```bash
cd .joycode/skills/funcpulse
node scripts/generate-validation-report.js requirements/ProductRequirements.md
node scripts/generate-validation-report.js test-cases/LoginTestCases.md --repos ../frontend,../backend
```

## 输出内容

- 需求拆解：从 PRD/用例中抽取关键验收点
- 代码映射：定位实现仓库、模块、文件和变更点
- 覆盖分析：已覆盖、未覆盖、部分覆盖和冗余用例
- 缺陷列表：关键/高/中/低优先级分类
- 追踪矩阵：需求 ID、用例 ID、代码位置、验证结果
- 交付报告：标准 Markdown 业务测试验证报告

## 关键词

`Requirements Traceability` `PRD Analysis` `Test Case Validation` `Coverage Gap` `Multi Repo Analysis` `QA Report` `Acceptance Testing` `Regression Testing` `Defect Analysis`

## 文件结构

```text
funcpulse/
├── SKILL.md
├── README.md
├── package.json
├── scripts/
│   └── generate-validation-report.js
└── references/
    ├── test-validation-report.md
    ├── qa-analysis-methods.md
    ├── multi-repo-analysis.md
    └── test-case-traceability.md
```

## 使用建议

1. 给 FuncPulse 提供 PRD、测试用例、仓库路径或 Git Diff，结果会更具体。
2. 在提测前使用，能提前发现需求未实现和用例未覆盖。
3. 多仓库项目建议明确前端、后端、配置仓库路径。
4. 将追踪矩阵作为测试验收和发布复盘的统一证据。
## ClawHub 搜索词覆盖

FuncPulse 覆盖这些高意图场景：`PRD分析`、`测试用例验证`、`需求覆盖率`、`Requirements Traceability`、`Coverage Gap`、`多仓库测试`、`提测验收`、`需求回归`、`追踪矩阵`、`业务测试报告`、`缺陷分析`、`验收测试`。

## 30秒价值说明

如果你需要证明“需求已经被代码实现、测试用例已经覆盖关键路径”，FuncPulse 会把 PRD、用例和代码变更串成可追踪证据。它帮助测试、研发和产品在提测验收时快速发现未覆盖需求和业务缺陷。

## 金融AI增强方向

FuncPulse 会持续增强金融 AI 验证：金融结果影响、AI/模型链路、审计证据、合规控制、客户伤害、模型超时/低置信度/RAG 检索失败等覆盖维度。
