# Code Research Crafter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](README.md) | [简体中文](README.zh-CN.md)

> 研究代码库，撰写专业的 RFC 提案并发布到 GitHub。

## 什么是 Code Research Crafter？

**Code Research Crafter** 是一个综合性技能，提供结构化的 6 阶段工作流，用于深度代码库研究和专业 RFC 提案撰写。它通过基于证据的技术写作，弥合代码分析与社区参与之间的鸿沟。

## 核心特性

- **系统化代码分析** — 通过结构化方法论探索和理解复杂代码库
- **学术研究集成** — 查找和引用相关论文、算法和现有技术
- **社区情报** — 分析 GitHub Issues、讨论和维护者反馈
- **架构设计** — 创建分层解决方案，包含数据模型和分阶段实施计划
- **专业文档生成** — 生成多语言结构化技术文档
- **RFC 发布** — 通过 `gh` CLI 为开源社区撰写和提交专业 RFC
- **错误韧性** — 每个阶段都有优雅降级方案，工具或数据不可用时自动回退

## 6 阶段工作流

### 阶段 1：问题发现与代码分析
识别目标领域，执行深度代码分析，并用量化指标记录发现。输出 `research-context.md`。

### 阶段 2：学术与社区研究
搜索学术论文，提取关键见解，分析 GitHub 社区讨论。追加到 `research-context.md`。

### 阶段 3：解决方案设计
定义设计原则，构建分层解决方案，设计数据模型，规划实施阶段。**检查点：需用户批准后才继续。**

### 阶段 4：文档生成
生成具有适当结构和引用的综合技术文档。语言自适应：中文项目双语，国际项目纯英文。

### 阶段 5：RFC 撰写
按照开源社区标准撰写专业 RFC Markdown 文档。使用 `references/rfc-template.md` 模板。

### 阶段 6：GitHub 发布
通过 `gh` CLI（首选）、GitHub API 或手动说明作为备选，提交 RFC 到 GitHub。

## 何时使用此技能

在以下情况下使用 Code Research Crafter：

- 分析开源代码库并提出增强建议
- 以学术严谨性研究技术问题
- 基于证据决策设计系统架构
- 为开源社区创建专业 RFC
- 用适当引用记录复杂技术提案

**不适用于：** 简单代码审查、Bug 修复、一般问答、快速代码搜索。

## 文件结构

```
code-research-crafter/
├── SKILL.md                            # 核心技能定义
├── references/
│   ├── rfc-template.md                 # RFC 写作模板
│   ├── academic-research-guide.md      # 学术研究方法论
│   └── architecture-patterns.md       # 经过验证的设计模式
├── LICENSE.txt
├── README.md
└── README.zh-CN.md
```

## 示例输出

此技能已成功用于创建：

- **记忆整合 RFC** — 结合 Zettelkasten + PPR + 睡眠整合方法
- **多智能体协作 RFC** — 包含能力画像和共享黑板架构
- **时间衰减错误修复** — 扩展日期模式识别
- **i18n 翻译改进** — 用于配置界面

## 设计原则

1. **基于证据的分析** — 引用具体代码位置并量化问题
2. **学术严谨性** — 引用近期论文（2024-2025）并正确标注来源
3. **以人为本的设计** — 使用组织类比，设计渐进式采用方案
4. **成本意识** — 跟踪 Token/性能影响，设计高效方案
5. **社区参与** — 引用现有问题并邀请协作
6. **错误韧性** — 每个阶段都有优雅降级方案

## v1.1.0 更新内容

- **改进 `description`** — 添加明确的 `Use when` / `NOT for` 触发短语，提升自动发现准确性
- **`context: fork`** — 隔离执行，不污染主对话上下文
- **扩展工具依赖** — 添加 `gh` CLI 用于可靠的 GitHub 发布
- **指令性工作流步骤** — 将模糊描述替换为编号的可操作步骤
- **每阶段错误处理** — 工具或数据不可用时的优雅降级方案
- **阶段 3 检查点** — 进入文档生成前需用户批准
- **渐进式加载** — 详细参考内容移至 `references/` 目录
- **语言自适应文档** — 中文项目双语，国际项目纯英文
- **多重发布备选** — `gh` CLI → GitHub API → 手动说明

## 工具与资源

- **代码分析**：`glob`、`grep`、`read`
- **学术研究**：`WebSearch`、`WebFetch`
- **文档生成**：`python-docx` 用于专业文档生成（可选）
- **发布**：`gh` CLI（首选）、GitHub API、浏览器自动化（备选）
- **版本控制**：`git`、`desktop_terminal_execute`

## 安装

```bash
# 克隆此仓库
git clone https://github.com/zz0116/code-research-crafter.git

# 放入技能目录
cp -r code-research-crafter ~/.openclaw/skills/
```

## 快速开始

1. **确定目标** — 选择要研究的代码库或技术问题
2. **遵循工作流** — 系统地完成 6 个阶段
3. **在检查点审核** — 在文档生成前审核方案设计
4. **参与社区** — 分享你的 RFC 并收集反馈

## 许可证

本项目采用 MIT 许可证 — 详见 [LICENSE.txt](LICENSE.txt) 文件。
