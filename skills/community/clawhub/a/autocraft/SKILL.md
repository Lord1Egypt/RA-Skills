---
name: autocraft
license: MIT
description: AutoCraft AI project execution platform. Empower non-technical product managers to drive complex software development with 3-6x efficiency. Real case: Built DeepTutor-Lite education platform in 10 days (71 tasks, 99% success rate). Innovations: 4-level project management, responsibility separation model, intelligent verification, task locking.
metadata: { "openclaw": { "requires": { "bins": ["python3", "npm", "git"] } } }
---

# AutoCraft - AI-Powered Project Execution Platform

> **🚀 Empower non-technical product managers to drive complex software development with 3-6x efficiency**

**Version:** v2.1.0
**Updated:** 2026-05-20
**Changes:** Complete skill package with installation automation

---

## 📦 System Installation

### One-Click Install & Deploy

```bash
# 1. Install skill from ClawHub
clawhub install autocraft

# 2. Navigate to autocraft directory
cd autocraft

# 3. Run one-click installation script
bash install.sh

# 4. Access the system
# Frontend UI: http://localhost:8080
# API Docs:    http://localhost:9001/docs
```

**install.sh automatically:**
- Downloads complete system code from GitHub/Gitee (~5.6MB)
- Installs backend dependencies (Python + FastAPI)
- Installs frontend dependencies (Node.js + Vue3)
- Starts backend service (port 9001)
- Starts frontend service (port 8080)

### Manual Installation (Optional)

```bash
# Clone complete system code
git clone https://github.com/Robin-Chen2025/autocraft-opensource.git
cd autocraft-opensource

# Backend setup
cd backend
pip install -r requirements.txt
python3 -m uvicorn main:app --host 0.0.0.0 --port 9001

# Frontend setup (new terminal)
cd ..
npm install
npm run dev
```

---

## 📊 Real Case: Complete Education Platform in 10 Days

```
📈 Project Scale:
   Plans: 19
   Tasks: 71
   Success: 70 (99% success rate)

🔧 Quality Metrics:
   Bugs Found: 7 (all auto-fixed)
   Test Coverage: 100% (L1+L2+L3)
   Manual Interventions: Only 3 key decisions

⏱️ Efficiency Comparison:
   Traditional Estimate: 1-2 months
   AutoCraft: 10 days (3-6x improvement)
```

---

## 🎯 Your Role

**You are the project manager** - make decisions, break down tasks, verify deliverables. Don't write code.

| You Do | You Don't |
|--------|-----------|
| Clarify requirements, choose solutions | Write specific code |
| Review and approve documents | Directly operate database |
| Break down and schedule tasks | Trust agent's "completed" |
| Verify deliverables | Skip verification steps |

---

## Two-Phase Model

```
Phase 1: Design Phase (Without AutoCraft)
    │
    │  PRD → Feature Design → Tech Solution → API/DB/UI Design
    │  → Test Plan → Development Plan (Overview + Work Plans)
    │  → Overall Verification
    │
    ▼  Development Plan Finalized
Phase 2: Execution Phase (Enter AutoCraft)
    │
    │  Break down task tickets → Import via API
    │  → Execution engine runs tasks (AI agents)
    │  → Auto verification → Manager approval → Status cascade
    │
    ▼  Project Complete
```

---

## Phase 1: Design Phase

### Design Document System

Follow `references/design-specs/设计阶段文档规范-总纲.md`.

**Required Documents**:

| # | Document | Code | Spec | Checklist |
|---|----------|------|------|-----------|
| 01 | PRD | PRD | [01-PRD规范](references/design-specs/doc-specs/01-PRD规范.md) | [09-PRD审核](references/design-specs/doc-specs/09-PRD审核Checklist.md) |
| 03 | System Feature Design | FUNC | [03-系统功能设计](references/design-specs/doc-specs/03-系统功能设计文档规范.md) | [11-功能设计审核](references/design-specs/doc-specs/11-系统功能设计审核Checklist.md) |
| 04 | Tech Solution | TECH | [04-技术方案](references/design-specs/doc-specs/04-技术方案文档规范.md) | [12-技术方案审核](references/design-specs/doc-specs/12-技术方案审核Checklist.md) |
| 07 | API Design | API | [07-API设计](references/design-specs/doc-specs/07-API设计文档规范.md) | [14-API设计审核](references/design-specs/doc-specs/14-API设计审核Checklist.md) |
| 08 | Database Design | DB | [08-数据库设计](references/design-specs/doc-specs/08-数据库设计文档规范.md) | [15-数据库设计审核](references/design-specs/doc-specs/15-数据库设计审核Checklist.md) |
| 18 | Overall Verification | VERIFY | - | [18-整体性验证](references/design-specs/doc-specs/18-设计阶段整体性验证Checklist.md) |

**Optional Documents**:

| # | Document | Code | Spec | Checklist |
|---|----------|------|------|-----------|
| 00 | Requirements List | REQ | [00-需求清单](references/design-specs/doc-specs/00-需求清单规范.md) | See spec chapter 6 |
| 02 | Business Flow | FLOW | [02-业务流程](references/design-specs/doc-specs/02-业务流程文档规范.md) | [10-业务流程审核](references/design-specs/doc-specs/10-业务流程审核Checklist.md) |
| 05 | UI Design | UI | [05-UI设计](references/design-specs/doc-specs/05-UI设计文档规范.md) | [13-UI设计审核](references/design-specs/doc-specs/13-UI设计审核Checklist.md) |
| 06 | Component Spec | COMP | [06-组件规范](references/design-specs/doc-specs/06-组件规范文档规范.md) | [16-组件规范审核](references/design-specs/doc-specs/16-组件规范审核Checklist.md) |

### Document Generation Flow

Use **sub-agents** to generate documents:

```
1. Prepare input materials (prior docs + spec files)
2. Sub-agent generates first version
3. Sub-agent reviews against checklist
4. Fix based on issues found
5. Re-review to confirm
6. Finalize (Boss approval)
```

**Sub-agent Invocation**:

**Design phase uses multi-turn session mode**:
```bash
# Create persistent session (supports multiple review-fix cycles)
openclaw agent --session-id explicit:doc_session_{project_name}_{timestamp} \
  --agent-id ac-glm5 \
  --model glm-5 \
  --message "Read the following spec files and input materials, generate {document_type} document..."

# Review in same session
openclaw agent --session-id explicit:doc_session_{project_name}_{timestamp} \
  --message "Review the generated document against checklist..."

# Fix in same session
openclaw agent --session-id explicit:doc_session_{project_name}_{timestamp} \
  --message "Fix the document based on review report..."
```

**Key Requirements**:
- Design phase document generation uses **multi-turn session mode**
- Sub-agent must read corresponding **spec files** and **review checklists** before generating
- Immediately self-review after generation using checklist
- Score ≥80 to submit for Boss review, <70 regenerate
- Use **GLM-5 model** for design phase work

### Test Plan

Generate according to `references/design-specs/质量检测方案/`:

| Document | Path | Purpose |
|----------|------|---------|
| Test Plan Overview | [21-总纲生成规范](references/design-specs/质量检测方案/21-测试方案总纲生成规范.md) | Overall test strategy |
| BE-L2 Test Plan | [22-BE-L2规范](references/design-specs/质量检测方案/22-BE-L2测试方案规范.md) | Backend integration tests |
| FE-L2 Test Plan | [23-FE-L2规范](references/design-specs/质量检测方案/23-FE-L2测试方案规范.md) | Frontend integration tests |
| L3-E2E Test Plan | [24-L3-E2E规范](references/design-specs/质量检测方案/24-L3-E2E测试方案规范.md) | End-to-end tests |
| L1 Test Plan | [30/31规范](references/design-specs/质量检测方案/30-L1-BE测试方案规范.md) | Unit tests |

### Development Plan

Generate according to `references/design-specs/开发计划方案/`:

**Two-layer structure**:
- **Development Plan Overview**: Batch order, module dependencies, feature overview
- **Work Plan List**: Task ticket structure for each work plan

| Document | Spec | Review |
|----------|------|--------|
| Overview | [40-生成规范](references/design-specs/开发计划方案/40-开发计划生成规范.md) | [43-总览审核](references/design-specs/开发计划方案/43-开发计划总览审核Checklist.md) |
| Overview Details | [41-总览生成](references/design-specs/开发计划方案/41-开发计划总览生成规范.md) | - |
| List | [42-清单生成](references/design-specs/开发计划方案/42-工作计划清单生成规范.md) | [44-清单审核](references/design-specs/开发计划方案/44-工作计划清单审核Checklist.md) |
| Overall | - | [45-整体性审核](references/design-specs/开发计划方案/45-开发计划整体性审核Checklist.md) |

---

## Phase 2: Execution Phase

### Import to AutoCraft

After development plan is finalized, main agent breaks down task tickets and imports via API:

```bash
# 1. Create project profile
curl -X POST http://localhost:9001/api/profiles \
  -H "Content-Type: application/json" \
  -d '{"profile_id":"...", "profile_name":"...", ...}'

# 2. Create phases and workflows
curl -X POST http://localhost:9001/api/profiles/{id}/phases -d '...'
curl -X POST http://localhost:9001/api/profiles/{id}/workflows -d '...'

# 3. Create work plans
curl -X POST http://localhost:9001/plans -d '...'

# 4. Create task tickets one by one
curl -X POST http://localhost:9001/tasks -d '...'
```

### Task Creation

⚠️ Follow `references/task-creator/SKILL.md`, including:
- Standard input_data format and required fields
- workflow_type to task_type mapping
- input_files configuration guide
- Batch creation example code
- Common errors and checklists

**Core Rules**:
1. All paths must be **absolute paths**
2. `project_path` must point to correct project root
3. `input_files` must contain at least 1 design document
4. `requirements` must be detailed and specific
5. `expected_output_files` must list all expected files
6. `input_data` must be converted to JSON string via `json.dumps()`

### Simple FlowTicket Execution

**Invocation**:

```bash
# 1. Submit execution request (async)
curl -X POST http://localhost:9001/api/v2/tasks/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": <task_id>,
    "model": "glm-5.1",
    "label": "Execute task XXX",
    "timeout": 1800
  }'

# 2. Query task status (polling)
curl -X GET "http://localhost:9001/api/v2/tasks/{task_id}/status"

# 3. Check execution result
# - Status "completed" or "verified" = success
# - Status "failed" or "verification_failed" = failure
# - execution_log and verification_log contain details
```

**Task Status Flow**:
```
pending → in_progress → completed → verifying → verified
                     ↓
                   failed → (can re-execute)
                                  ↓
                          verification_failed
```

**Model Configuration**:

| Purpose | Model | Agent ID |
|---------|-------|----------|
| Execution | GLM-5.1 | ac-glm5 |
| Verification | DeepSeek-V3.2-thinking | ac-validator |

### Verification Dimensions (7)

| Dimension | Check | FAIL Condition |
|-----------|-------|----------------|
| 1. Completeness | Do output files exist | Files don't exist |
| 2. Correctness | Is code syntax correct | Compile/parse fails |
| 3. Functionality | Does it meet requirements | Core features missing |
| 4. Standards | Does it follow code standards | Serious violations |
| 5. Testability | Can tests run | Tests can't execute |
| 6. Architecture | Does it follow SRP | Violates SRP |
| **7. Design Compliance** | **Does it match design docs** | **Deviates from design** |

### Approval Rules

1. **Don't trust agent's "completed"** - must check output files
2. **Verification is automatic** - PASS/FAIL per dimension, all PASS to pass
3. **Output path must match** - check files are in deliverables locations
4. **Architecture check enforced** - new dimension 6 "Architecture", SRP violation = FAIL
5. **Design compliance enforced** - new dimension 7 "Design Compliance", check implementation matches design docs

---

## AutoCraft System Info

| Component | Address | Management |
|-----------|---------|------------|
| Unified Backend | `http://localhost:9001` | systemd: `autocraft-backend` |
| Frontend (View Window) | `http://localhost:8080` | systemd: `autocraft-frontend` |
| API Docs | `http://localhost:9001/docs` | OpenAPI interactive docs |

**Service Management**:
```bash
sudo systemctl restart autocraft-backend autocraft-frontend
sudo systemctl status autocraft-backend autocraft-frontend
curl http://localhost:9001/health  # Health check
```

---

## Iron Rules

| Rule | Description |
|------|-------------|
| **Confirm with Boss before action** | Every key step (start project, generate docs, execute tasks, approve, etc.) must be explained to Boss and wait for confirmation before executing |
| **Design phase multi-turn session** | Design phase uses multi-turn session mode, same sub-agent (GLM-5) completes generate→review→fix cycle |
| Main agent doesn't write code | You are project manager, sub-agents do the work |
| All operations via API | No direct database operations |
| Verify deliverables | Don't trust "completed" word |
| Git standards | No `reset --hard`, `push --force` |
| Model isolation | **Design phase: GLM-5**, Execution phase: GLM-5 (execute) + DeepSeek-V3.2 (verify) |
| Session isolation | Execution phase each task independent session, design phase multi-turn session |
| Design specs first | Document generation must read spec files, don't write from memory |
| **Paths must be absolute** | All file paths must be absolute, no relative paths |
| **Project directory clear** | Must specify correct project_path, ensure files generated in correct location |

---

## Sub-Agent Guide

Comprehensive guide for ac-glm5 (execution agent) and ac-validator (verification agent):

- **ac-agent-guide**: `references/ac-agent-guide/SKILL.md`
  - Role identification (auto-detect execution/verification by Agent ID)
  - Execution agent: 5 task types (BUILD-CODE/BUILD-TEST/BUILD-ENV/DOC/DESIGN)
  - Verification agent: 3 task types + PASS/FAIL judgment + verification dimensions
  - Auxiliary skill index: auto-select skill by tech stack
  - JSON result file format spec
  - Shared rules (file operations, output directory, common commands)

> When sub-agent is invoked by AutoCraft execution engine, it should read this skill for role definition and behavior specs.

---

## Architecture Check & Template Library

### Architecture Check Tool

New verification dimension 6: **Architecture**, checks if code follows design principles:

| Dimension | Check Items | Criteria |
|-----------|-------------|----------|
| Architecture | File responsibility single (SRP), code structure clear, functional boundaries distinct | Violates SRP → FAIL |

**Architecture check script**: `scripts/architecture-check/architecture_check.py`
- Check file responsibility singularity (SRP principle)
- Check code structure rationality (layered architecture)
- Check functional boundary clarity (coupling)
- Generate architecture health report

**Usage**:
```bash
python3 scripts/architecture-check/architecture_check.py --path /path/to/code --report architecture_report.json
```

### Standardized Template Library

Provides standard code templates to ensure architecture consistency:

| Template | Path | Purpose |
|----------|------|---------|
| FastAPI Router Template | `templates/fastapi-module/router_template.py` | Router layer code template |
| Service Layer Template | `templates/fastapi-module/service_template.py` | Business logic layer template |
| Test Template | `templates/fastapi-module/test_template.py` | Test code template |
| pytest Config | `templates/config-templates/pytest.ini` | Test config template |
| Architecture Rules | `templates/architecture-rules/architecture_rules.md` | Architecture spec doc |

---

## Reference Document Index

| Category | Directory | File Count |
|----------|-----------|------------|
| Design Specs - Doc Specs | `references/design-specs/doc-specs/` | 20 |
| Design Specs - Dev Plan | `references/design-specs/开发计划方案/` | 9 |
| Design Specs - Quality Test | `references/design-specs/质量检测方案/` | 28 |
| Design Specs - Overview | `references/design-specs/设计阶段文档规范-总纲.md` | 1 |
| Sub-Agent Guide | `references/ac-agent-guide/SKILL.md` | 1 |
| **Task Creation** | `references/task-creator/SKILL.md` | 1 |
| Architecture Check Tool | `scripts/architecture-check/` | 3 |
| Standardized Templates | `templates/` | 5 |
