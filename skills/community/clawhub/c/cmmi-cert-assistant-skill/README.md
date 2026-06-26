# CMMI V3.0 认证助手 | CMMI V3.0 Certification Assistant

## 中文介绍 | Chinese Introduction

CMMI V3.0 认证助手是一个专为项目经理（PM）和 EPG 团队设计的 AI Skill，帮助团队高效通过 CMMI V3.0 认证评估。

### 核心功能

1. **自动 PA 匹配** — 上传项目文档，自动识别对应的 CMMI V3.0 实践域（Practice Area）
2. **差距分析** — 分析当前文档与实践要求的差距，指出缺失证据
3. **文档自动生成** — 基于配置驱动模板，一键生成符合 CMMI V3.0 规范的合规文档（支持 .docx 格式）
4. **PA 知识库查询** — 内置全部 31 个 PA 的详细知识库，支持自然语言查询

### 支持的成熟度等级

| 等级 | 名称 | 支持状态 |
|------|------|----------|
| ML2 | 管理级 | ✅ 全面支持 |
| ML3 | 定义级 | ✅ 全面支持 |
| ML4 | 量化管理级 | ✅ 支持 |
| ML5 | 优化级 | ✅ 支持 |

### 覆盖的 PA（共 31 个）

**核心 PA（17 个）**：CAR、CM、DAR、EST、GOV、II、MC、MPM、OT、PAD、PCM、PLAN、PQA、PR、RDM、RSK、VV

**领域特定 PA（14 个）**：TS、PI（Development）；DM、DQ（Data）；WE（People）；ESAC（Safety）；ESEC、MST（Security）；SDM、STSM、IRP、CONT（Services）；SAM（Suppliers）；EVW（Virtual）

### 使用方式

上传项目文档（如需求文档、项目计划、测试报告等），Skill 将自动：
1. 匹配最相关的 PA
2. 给出差距分析
3. 生成符合 CMMI V3.0 规范的合规文档

---

## English Introduction

CMMI V3.0 Certification Assistant is an AI Skill designed for Project Managers (PM) and EPG teams to efficiently prepare for CMMI V3.0 appraisals.

### Core Features

1. **Automatic PA Matching** — Upload project documents, automatically identify corresponding CMMI V3.0 Practice Areas (PA)
2. **Gap Analysis** — Analyze gaps between current documents and practice requirements, pinpoint missing evidence
3. **Automatic Document Generation** — Configuration-driven templates generate CMMI V3.0 compliant documents (.docx format) with one click
4. **PA Knowledge Base Query** — Built-in detailed knowledge base for all 31 PAs, supports natural language queries

### Supported Maturity Levels

| Level | Name | Support Status |
|-------|------|-----------------|
| ML2 | Managed | ✅ Fully Supported |
| ML3 | Defined | ✅ Fully Supported |
| ML4 | Quantitatively Managed | ✅ Supported |
| ML5 | Optimizing | ✅ Supported |

### Covered PAs (31 total)

**Core PAs (17)**: CAR, CM, DAR, EST, GOV, II, MC, MPM, OT, PAD, PCM, PLAN, PQA, PR, RDM, RSK, VV

**Domain-Specific PAs (14)**: TS, PI (Development); DM, DQ (Data); WE (People); ESAC (Safety); ESEC, MST (Security); SDM, STSM, IRP, CONT (Services); SAM (Suppliers); EVW (Virtual)

### How to Use

Upload a project document (e.g., requirements doc, project plan, test report), and the Skill will:
1. Match the most relevant PA(s)
2. Provide gap analysis
3. Generate a CMMI V3.0 compliant document

---

## 技术说明 | Technical Notes

- **配置驱动架构**：文档结构由 `pa_config.json` 定义，修改配置即可调整所有 PA 的文档模板，无需修改代码
- **自动触发**：上传文档后自动执行 PA 匹配和文档生成，无需手动确认（格式争议时除外）
- **无 PA 标记输出**：生成的合规文档标题干净，不包含 PA 引用标记（如 "RDM 1.1"）
- **Configuration-Driven**: Document structures are defined in `pa_config.json`. Modify the config to adjust document templates for all PAs without code changes.
- **Auto-Trigger**: PA matching and document generation execute automatically upon document upload, no manual confirmation needed (except for format ambiguities).
- **Clean Output**: Generated compliant documents have clean titles without PA reference markers (e.g., "RDM 1.1").
