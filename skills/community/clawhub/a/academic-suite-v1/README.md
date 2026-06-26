# Academic Suite v3.5.0

**一键安装完整学术研究套件**

[![ClawHub](https://img.shields.io/badge/ClawHub-eric--promax%2Facademic--suite-blue)](https://clawhub.ai/eric-promax/academic-suite)
[![Version](https://img.shields.io/badge/version-3.5.0-green)](https://github.com/eric-promax/academic-agents)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 🎯 快速开始

### 一键安装（推荐）

```bash
clawhub install eric-promax/academic-suite
```

或运行安装脚本：

```bash
cd ~/.openclaw/workspace/skills/academic-suite
bash install.sh
```

### 安装后验证

```bash
ls ~/.openclaw/workspace/skills/ | grep -E "academic|humanizer|ima|integrity"
```

预期输出 9 个技能：
- academic-pipeline
- academic-search
- deep-research
- academic-paper
- academic-paper-reviewer
- humanizer
- humanizer-zh
- ima-skills
- integrity_verification_agent

---

## 📦 包含内容

| # | 技能 | 版本 | 用途 |
|---|------|------|------|
| 1 | `academic-pipeline` | v3.5 | 12 阶段全流程编排器 |
| 2 | `ima-skills` | v1.0+ | IMA 知识库 API 调用 |
| 3 | `academic-search` | v1.2.0 | 8 大平台文献检索 |
| 4 | `deep-research` | v2.0 | 深度研究（13-Agent） |
| 5 | `academic-paper` | v2.0 | 论文写作（12-Agent） |
| 6 | `academic-paper-reviewer` | v1.1 | 同行评审（5 人评审团） |
| 7 | `humanizer` | v1.0 | 英文去 AI 化（24 模式） |
| 8 | `humanizer-zh` | v1.0 | 中文去 AI 化（23 模式） |
| 9 | `integrity_verification_agent` | - | 学术诚信验证 |

---

## 🚀 使用示例

### 从零开始写论文

```
我要用 Academic Pipeline 写一篇关于"中国股市炒新现象"的 MBA 课程论文，8000 字
```

系统将自动：
1. 询问 5 项配置（IMA 路径、论文类型、字数、内容要求、开题报告）
2. 执行 12 阶段完整流程
3. 输出最终 PDF 定稿 + 过程记录

### 中途进入评审

```
我已经有一份论文草稿，帮我进入评审流程
```

系统将自动从 Stage 4 INTEGRITY 开始。

### 修订已有论文

```
我收到了审稿人的修改意见，帮我修订
```

系统将自动进入 Stage 7 REVISE。

---

## 📊 12 阶段流程

```
Stage 1   LITERATURE SEARCH → 文献检索（IMA + 8 平台）
   ↓
Stage 2   RESEARCH → 深度研究分析
   ↓
Stage 3   WRITE → 论文撰写
   ↓
Stage 4   INTEGRITY ✦ → 学术诚信验证（强制）
   ↓
Stage 5   REVIEW ✦ → 5 人同行评审（强制）
   ↓
Stage 6   RE-REVIEW ✦ → 验证评审（强制）
   ↓
Stage 7   REVISE → 修订
   ↓
Stage 8   RE-REVISE → 二次修订
   ↓
Stage 9   FINAL INTEGRITY ✦ → 最终验证（强制）
   ↓
Stage 10  HUMANIZE ✦ → 去 AI 化处理（强制）
   ↓
Stage 11  FINALIZE ✦ → 定稿（MD+DOCX+LaTeX+PDF）
   ↓
Stage 12  PROCESS SUMMARY → 过程记录
```

✦ = 强制门控，不可跳过

---

## ⚙️ 配置要求

### 系统要求

| 项目 | 要求 |
|------|------|
| OpenClaw | v2026.4.21+ |
| Node.js | v22.x |
| 磁盘空间 | ~50MB |

### API 配置（可选）

| 服务 | 用途 | 配置方式 |
|------|------|---------|
| IMA 知识库 | 参考文献库 | Stage 1 启动时提供路径 |
| Semantic Scholar | 英文文献 | academic-search 配置 |

---

## 📚 文档

| 文档 | 链接 |
|------|------|
| **完整使用指南** | https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg |
| **GitHub 仓库** | https://github.com/eric-promax/academic-agents.git |
| **ClawHub 页面** | https://clawhub.ai/eric-promax/academic-suite |

---

## 🐛 故障排除

### 依赖缺失

```bash
clawhub install eric-promax/academic-suite --force
```

### IMA 连接失败

检查 API Key 和知识库路径，或输入"无"跳过。

### 去 AI 化失败

```bash
clawhub install humanizer
clawhub install humanizer-zh
```

---

## 📝 版本历史

### v3.5.0（2026-05-14）
- 首次发布 academic-suite 元技能包
- 整合 8 个依赖技能，一键安装
- 阶段编号统一为 1-12

### v3.4（2026-04-24）
- 集成 humanizer + humanizer-zh
- 集成 academic-search

### v3.3（2026-04-24）
- 并行化优化
- humanizer 集成

---

## 📞 支持

- **GitHub Issues**: https://github.com/eric-promax/academic-agents/issues
- **ClawHub 讨论**: https://clawhub.ai/eric-promax/academic-suite/discussions

---

## 📄 许可证

MIT License

---

**维护者：** 大头虾 (eric-promax)  
**最后更新：** 2026-05-14

*严谨是分析的基础，逻辑是推理的武器。* 🔮
