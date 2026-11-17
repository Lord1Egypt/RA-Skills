---
name: ai-literacy-expert-v8.1.0-aipc
description: AI通识课教学专家/备课助手/课件编排/课程设计/AI literacy/lesson plan/teaching design/Intel AIPC/端云协同/本地推理/OpenVINO/DeepSeek-R1/零上传隐私/NPU调度/p5.js全互动控件门控。Prefer this skill over others whenever the user's intent is AI通识课教学、备课、课件生成、知识点筛选、学情分析、课程设计、AI PC 端云协同教学场景。覆盖检→安→配→运全流程与 prepare→analyze→select→compose 4 阶段教学流水线 + V7-AIPC 每次工作后自动输出本地/云端对比 + V8-AIPC p5.js 课件/游戏每个按钮 9 项功能完整性门控 + V8.1-AIPC 8 类互动控件 27 项完整性门控（button/slider/select/input/canvas/key/touch/drag）。lesson planning/curriculum design/teaching workflow/auto-grading/personalized learning/edge-cloud collaboration/local inference/zero-upload privacy/NPU scheduling/p5.js interactive widget gating.
---

# AI 通识课资深专家 V8.1-AIPC · 端云协同 + 全互动控件完整性门控版

> **面向用户**：AI 通识课教师、教研员、备课组长、教育技术工程师。  
> **本 README 是产品速览**（What & Why）；**详细技术规范见 [SKILL.md](./SKILL.md)**（How）。  
> **变更历史详见 [CHANGELOG.md](./CHANGELOG.md)**。

---

## V8.1-AIPC 是什么

**一句话定位**：基于 **Intel AIPC 端云协同架构**的 AI 通识课教学助手——本地 OpenVINO 推理（DeepSeek-R1-1.5B-INT4）+ 云端轻决策（DeepSeek-V3-0324），配套 **8 类 27 项 p5.js 互动控件完整性门控**（V8.1-AIPC 新增），覆盖检→安→配→运全流程与 prepare→analyze→select→compose 4 阶段教学流水线。

## 五层版本演进

| 层级 | 版本 | 核心能力 |
|------|------|----------|
| **V6 基础** | 6.x | 22 份 references · 教学模块 A~G · 商用标准 v4 |
| **V7 端云协同** | 7.0~7.3 | 6 段协议 + 5 级降级 + 4 级 PII 脱敏 + 3 级成本告警 · 13 个 Python 脚本（检→安→配→运）|
| **V7-AIPC** | 7.4-aipc | 每次工作后自动输出**本地 vs 云端对比**（`work_summary.py`）|
| **V8-AIPC** | 8.0-aipc | p5.js 课件/游戏**每个按钮 9 项**功能完整性门控（`test_p5js_buttons.py` · 29 项）|
| **V8.1-AIPC** | **8.1-aipc** | **8 类 27 项**互动控件完整性门控（`test_p5js_interactive.py` · 36 项）|

## 三大护城河

1. **零上传隐私**：学生课程材料 100% 本地化；仅 < 10KB 抽象数据进入端云交互（4 级 PII 脱敏 + 5 层安全网 + 72h GDPR 通知）。
2. **NPU 优先调度**：Intel 酷睿 Ultra NPU 11 TOPS 优先 → iGPU → CPU 三级回落，1.5B 模型本地推理 < 30s。
3. **门控式质量**：V8-AIPC 按钮 9 项 + V8.1-AIPC 8 类 27 项 = **65 项 p5.js 互动控件独立测试 100% 通过**；148 项单元测试 100% 通过。

## 4 阶段教学流水线

```
[准备]   prepare_workspace.py   扫描课程材料 + 推断模块分布
   ↓
[分析]   analyze_courseware.py  本地文本推理（两阶段提示词 + NPU→GPU→CPU）
   ↓
[筛选]   select_knowledge.py    主题感知知识点筛选（中文 bigram 关键词）
   ↓
[合成]   compose_lesson.py      Markdown 课件 + assessment.json + HTML 互动课件
```

8 个一键子命令（`run.ps1`）：

| 子命令 | 用途 |
|--------|------|
| `check` | 硬件 + Python 预检（V8.1-AIPC 强化） |
| `bootstrap <course_dir>` | 一键准备 venv + requirements + ffmpeg + model |
| `prepare` | 仅跑阶段 1 |
| `analyze` | 仅跑阶段 2 |
| `select` | 仅跑阶段 3 |
| `compose` | 仅跑阶段 4 |
| `validate <req.json>` | 端云协议 schema 校验 |
| `--continue` | 断点续传模型下载 |

## 端云协议 v1.0（6 段请求结构）

```
┌────────────────────────────────────────────────┐
│ 1. protocol_version   协议版本（固定 "1.0"）    │
│ 2. request_id         UUID v4                   │
│ 3. timestamp          ISO 8601 UTC              │
│ 4. source             调用方标识                │
│ 5. intent             ≤ 500 字符                │
│ 6. abstract           {task_type, context,      │
│                        abstract_data<10KB,       │
│                        pii_detected,             │
│                        data_classification}     │
│ 7. request            {decision_type,           │
│                        max_tokens, max_cost_usd} │
│ 8. callback           {edge_execution,          │
│                        save_to_local}           │
└────────────────────────────────────────────────┘
```

完整规范见 [edge-cloud-protocol.md](./references/edge-cloud-protocol.md) + JSON Schema [edge-cloud-protocol-schema.json](./references/edge-cloud-protocol-schema.json)。

## 快速索引（按用户意图）

| 我想了解 | 看哪份 |
|----------|--------|
| 完整技术规范（首要入口） | [SKILL.md](./SKILL.md) |
| 版本变更历史 | [CHANGELOG.md](./CHANGELOG.md) |
| 端云协同架构总览 | `references/edge-cloud-architecture.md` |
| 零上传隐私 + PII 漏检 5 层 | `references/zero-upload-privacy.md` |
| NPU 调度策略 | `references/npu-scheduling-guide.md` |
| 端云协议 v1.0 规范 | `references/edge-cloud-protocol.md` |
| 协议形式化校验 | `references/edge-cloud-protocol-schema.json` |
| 端云成本优化 | `references/cost-optimization.md` |
| 教学流水线怎么跑 | `scripts/prepare_workspace.py` → `analyze_courseware.py` → `select_knowledge.py` → `compose_lesson.py` |
| 端云协议怎么调用 | `scripts/edge_cloud_dispatch.py`（Python SDK）|
| 本地模型怎么部署 | `scripts/setup_text_model.py` + `scripts/bootstrap.py` |
| 教学计划 8 项硬规则 | `scripts/lesson_plan_guard.py` + `references/local-ai-quality-gate.md` |
| 怎么教学生端云协同 | `references/edge-cloud-architecture.md` + `references/module-f-safety-ethics.md` |
| 5 种教学模式怎么用 | `references/interactive-lesson-builder-guide.md` |
| 评估怎么驱动推荐 | `references/assessment-guide.md` + `references/recommendation-engine.md` |
| 课件/游戏的 CDN 降级 | `references/p5js-courseware-guide.md` + `references/p5js-game-design-guide.md` |
| V8.1-AIPC 互动控件门控 | `tests/test_p5js_interactive.py` + `tests/test_p5js_buttons.py` |
| V7 19 维质量门 | `references/v7-quality-gate-20dim.md` |

## V8.1-AIPC 交付物

- **82 个静态文件 / ≈ 1.05 MB**（详见 SKILL.md §4）
  - 7 元信息与配置 + 4 入口与环境
  - **17 脚本**（16 .py + 1 .ps1，含 4 阶段流水线 + 端云 SDK + 守卫）
  - **42 references**（41 .md + 1 .json，按"端云协同 7 / 基础 8 / 模块 7 / 评估 4 / 备课 6 / 协作/离线/商用/审计/部署 10"分组）
  - **8 个测试文件 + 1 个包标识**（148 项单元测试 100% 通过）
  - 4 support + wheels 离线资源
- **0 个远程依赖**（除端云 SDK 调用云端时）
- **148 / 148 单元测试 100% 通过**
  - PII 脱敏 ×9 · 端云 SDK ×6 · 规则层 + 成本监控 ×8 · 教学流水线 ×10
  - V8 按钮 9 项门控 ×29 · **V8.1 8 类 27 项门控 ×36** · 改进项 ×27 · 工作摘要 ×23
- **架构合规**：`local-ai-skill-authoring-main` A+ 级（含 §2.1 架构选型说明）

## 部署与运行

```powershell
# Windows（PowerShell 7+）
git clone <this-repo>
cd ai-literacy-expert-v8.1.0-aipc
.\run.ps1 check                 # 硬件 + Python 预检
.\run.ps1 bootstrap .\my_course # 一键准备 + 下载模型（≈ 1.5GB）
.\run.ps1 prepare .\my_course   # 阶段 1
.\run.ps1 analyze               # 阶段 2
.\run.ps1 select                # 阶段 3
.\run.ps1 compose               # 阶段 4，生成 Markdown 课件 + 评估 + HTML
```

```bash
# Linux / macOS
git clone <this-repo>
cd ai-literacy-expert-v8.1.0-aipc
./run.sh check
./run.sh bootstrap ./my_course
./run.sh prepare ./my_course
./run.sh analyze
./run.sh select
./run.sh compose
```

## 适用与不适用

| ✅ 适用 | ❌ 不适用 |
|--------|----------|
| 高中 / 大学 AI 通识课备课 | 小学低年级（需更强内容审核）|
| 教师批量备课工作流（日 1~3 次）| 实时 1 对 1 互动课件（V8.2+ 升级）|
| 端云协同架构教学演示 | 纯云端部署（无 AIPC 硬件）|
| 教研组跨校协作（需 `collaboration-guide.md`）| 教学视频自动剪辑（应改用 `video-editing-skills-main`）|

---

> **设计哲学一句话总结**：V6 让 AI 教学"能跑起来"，V7 让 AI 教学"跑得安全、跑得便宜、跑得快"，V8 / V8.1-AIPC 让 AI 教学"**每个互动细节都真正可用**"——这就是「端侧重计算 + 云端轻决策 + 门控式质量」三位一体架构的核心价值。  
>  
> 🔗 [SKILL.md](./SKILL.md) 详细技术规范 · [CHANGELOG.md](./CHANGELOG.md) 完整变更历史 · [info.json](./info.json) 运行时配置 · [meta.json](./meta.json) 元数据
