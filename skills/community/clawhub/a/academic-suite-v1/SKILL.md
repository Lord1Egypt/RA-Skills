---
name: academic-suite
description: "Complete Academic Research & Writing Suite — One-click installation of the full Academic Pipeline ecosystem with all 8 dependencies. Includes academic-pipeline v3.5, academic-search, deep-research, academic-paper, academic-paper-reviewer, humanizer, humanizer-zh, ima-skills, and integrity_verification_agent."
metadata:
  version: "3.5.0"
  last_updated: "2026-05-14"
  author: "eric-promax"
  license: "MIT"
  suite: true
  dependencies:
    - "ima-skills"
    - "academic-search"
    - "deep-research"
    - "academic-paper"
    - "academic-paper-reviewer"
    - "humanizer"
    - "humanizer-zh"
    - "integrity_verification_agent"
  status: active
  category: "Academic Research"
  tags:
    - academic
    - research
    - writing
    - pipeline
    - paper
    - thesis
    - literature-review
    - peer-review
    - de-ai
---

# Academic Suite v3.5.0 — 一键安装完整学术套件

**元技能包（Meta-Skill Package）**

这是一个元技能包，用于一键安装完整的 Academic Pipeline 生态系统。安装后，您将拥有从零开始到最终论文发表的全流程学术研究与写作能力。

---

## 🎯 快速开始

### 安装（一键完成）

```bash
clawhub install eric-promax/academic-suite
```

安装过程会自动安装以下 8 个依赖技能：

| # | 技能 | 用途 |
|---|------|------|
| 1 | `ima-skills` | IMA 知识库 API 调用（文献库读取） |
| 2 | `academic-search` | 8 大平台文献检索（知网 + Semantic Scholar 等） |
| 3 | `deep-research` | 深度研究分析（13-Agent 团队） |
| 4 | `academic-paper` | 论文撰写/修订/格式化（12-Agent 流程） |
| 5 | `academic-paper-reviewer` | 同行评审（5 人评审团 + Devil's Advocate） |
| 6 | `humanizer` | 英文去 AI 化（24 种模式） |
| 7 | `humanizer-zh` | 中文去 AI 化（23 种模式） |
| 8 | `integrity_verification_agent` | 学术诚信验证（引用 + 数据 100% 核查） |

---

## 📦 包含内容

### 核心编排器
- **academic-pipeline v3.5** — 12 阶段全流程编排器

### 依赖技能（8 个）
- **ima-skills** — IMA 知识库客户端
- **academic-search v1.2.0** — 多源文献检索（8 平台 + 查询扩展 + 两遍搜索）
- **deep-research v2.0** — 深度研究（13-Agent 团队）
- **academic-paper v2.0** — 论文写作（12-Agent 流程）
- **academic-paper-reviewer v1.1** — 同行评审（5 人评审团）
- **humanizer v1.0** — 英文去 AI 化
- **humanizer-zh v1.0** — 中文去 AI 化
- **integrity_verification_agent** — 学术诚信验证

---

## 🚀 使用流程

安装完成后，您可以直接使用自然语言启动学术写作：

### 示例 1：从零开始写论文

```
我要用 Academic Pipeline 写一篇关于"中国股市炒新现象"的 MBA 课程论文，8000 字
```

系统将自动：
1. 询问 5 项配置（IMA 路径、论文类型、字数、内容要求、开题报告）
2. 启动 Stage 1 LITERATURE SEARCH（文献检索）
3. 依次执行 12 个阶段，直到最终 PDF 定稿

### 示例 2：中途进入评审

```
我已经有一份论文草稿，帮我进入评审流程
```

系统将自动：
1. 检测您已有论文草稿
2. 从 Stage 4 INTEGRITY（学术诚信验证）开始
3. 执行后续评审、修订、定稿流程

### 示例 3：修订已有论文

```
我收到了审稿人的修改意见，帮我修订
```

系统将自动：
1. 进入 Stage 7 REVISE（修订模式）
2. 逐条回应审稿意见
3. 执行验证评审 → 最终验证 → 定稿

---

## 📊 12 阶段全景图

```
┌──────────────────────────────────────────────────────────────┐
│  Stage 1   LITERATURE SEARCH (IMA + academic-search)         │
│    ↓ 用户确认                                                │
│  Stage 2   RESEARCH (deep-research)                          │
│    ↓ 用户确认                                                │
│  Stage 3   WRITE (academic-paper)                            │
│    ↓ 用户确认                                                │
│  Stage 4   INTEGRITY ✦ 强制 ✦ (引用/数据 100% 验证)            │
│    ↓ PASS → 继续；FAIL → 修复重验（最多 3 轮）                │
│  Stage 5   REVIEW (5 人同行评审) ✦ 强制 ✦                     │
│    ↓ Accept→Stage 9 / Minor→Stage 7 / Reject→Stage 3        │
│  Stage 6   RE-REVIEW (验证评审) ✦ 强制 ✦                    │
│    ↓ Accept→Stage 9 / Major→Stage 8                         │
│  Stage 7   REVISE (academic-paper revision 模式)              │
│    ↓ 用户确认                                                │
│  Stage 8   RE-REVISE (二次修订，最多 1 轮)                    │
│    ↓ 用户确认                                                │
│  Stage 9   FINAL INTEGRITY ✦ 强制 ✦ (零问题才能过)          │
│    ↓ PASS                                                    │
│  Stage 10  HUMANIZE ✦ 强制 ✦ (去 AI 化处理)                   │
│    ↓ 用户确认去 AI 版本                                       │
│  Stage 11  FINALIZE (academic-paper format-convert)          │
│    ↓ MD+DOCX→LaTeX→PDF                                      │
│  Stage 12  PROCESS SUMMARY (过程记录 PDF)                     │
└──────────────────────────────────────────────────────────────┘
```

**✦ 强制门控**：Stage 4、9（完整性验证）、Stage 5、6（评审决定）、Stage 10（去 AI 化）、Stage 11（终稿）— 不可跳过，必须用户明确确认

---

## 🔧 安装后验证

安装完成后，运行以下命令验证所有技能已正确安装：

```bash
# 检查已安装的学术相关技能
ls ~/.openclaw/workspace/skills/ | grep -E "academic|humanizer|ima|integrity"
```

预期输出：
```
academic-pipeline
academic-search
deep-research
academic-paper
academic-paper-reviewer
humanizer
humanizer-zh
ima-skills
integrity_verification_agent
```

---

## ⚙️ 配置要求

### API 配置（可选但推荐）

| 服务 | 用途 | 配置方式 |
|------|------|---------|
| **IMA 知识库** | 参考文献库存储 | 在 Stage 1 启动时提供路径 |
| **Semantic Scholar API** | 英文文献检索 | 在 academic-search 中配置 |
| **知网（CNKI）** | 中文文献检索 | 通过 Tavily 代理，无需额外配置 |

### 系统要求

| 项目 | 要求 |
|------|------|
| OpenClaw 版本 | v2026.4.21+ |
| Node.js | v22.x |
| 磁盘空间 | ~50MB（所有技能总计） |
| 网络 | 需要访问学术数据库 API |

---

## 📚 文档资源

| 文档 | 链接 |
|------|------|
| **完整使用指南** | https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg |
| **GitHub 仓库** | https://github.com/eric-promax/academic-agents.git |
| **ClawHub 页面** | https://clawhub.ai/eric-promax/academic-suite |

---

## 🐛 故障排除

### 问题 1：安装后提示依赖缺失

**症状：** 启动 Pipeline 时提示某个技能未找到

**解决：**
```bash
# 重新安装学术套件
clawhub install eric-promax/academic-suite --force

# 或手动安装缺失的技能
clawhub install <缺失的技能名>
```

### 问题 2：Stage 1 无法连接 IMA 知识库

**症状：** Stage 1 LITERATURE SEARCH 时 IMA API 调用失败

**解决：**
1. 检查 IMA API Key 是否配置
2. 确认知识库路径正确（如"个人知识库/eric/毕业论文"）
3. 如无 IMA 知识库，输入"无"跳过，直接使用 academic-search

### 问题 3：去 AI 化阶段失败

**症状：** Stage 10 HUMANIZE 报错

**解决：**
```bash
# 检查 humanizer 技能是否安装
ls ~/.openclaw/workspace/skills/ | grep humanizer

# 重新安装 humanizer 套件
clawhub install humanizer
clawhub install humanizer-zh
```

---

## 📝 版本历史

### v3.5.0（2026-05-14）
- ✅ 首次发布 academic-suite 元技能包
- ✅ 整合 8 个依赖技能，一键安装
- ✅ 阶段编号统一为连续整数（1-12）
- ✅ 新增 5 项启动配置询问
- ✅ 新增 Stage 10 HUMANIZE 去 AI 化

### v3.4（2026-04-24）
- ✅ academic-pipeline v3.4 发布
- ✅ 集成 humanizer + humanizer-zh
- ✅ 集成 academic-search（8 平台文献检索）
- ✅ IMA 知识库对接

### v3.3（2026-04-24）
- ✅ 并行化优化（Stage 3 写作阶段）
- ✅ humanizer 集成

### v3.2（2026-04-15）
- ✅ 收敛停止规则
- ✅ 预算透明
- ✅ AI 研究失败模式清单（7 模式）

---

## 📞 支持

| 渠道 | 联系方式 |
|------|---------|
| **GitHub Issues** | https://github.com/eric-promax/academic-agents/issues |
| **ClawHub 讨论区** | https://clawhub.ai/eric-promax/academic-suite/discussions |
| **飞书文档评论** | https://feishu.cn/docx/GRb7dGij9olddExTBsCcpoaCnWg |

---

## 📄 许可证

MIT License

---

**维护者：** 大头虾 (eric-promax)  
**最后更新：** 2026-05-14  
**版本：** 3.5.0

---

*严谨是分析的基础，逻辑是推理的武器。* 🔮
