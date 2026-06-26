---
name: chanjing-one-click-video-creation
description: >-
  L3 一键成片：组合 TTS、数字人合成、AI 画面与本地 ffmpeg 拼接。
  须有效蝉镜凭据；依赖 ffmpeg/ffprobe；环境变量与持久化路径见包根 ../../SKILL.md「运行时契约」。
---

# 一键成片（`chanjing-one-click-video-creation-SKILL.md`）

## 场景定位

- **业务目标**：用户给选题或完整文案，得到**一条**口播 + 数字人 + AI 画面混剪后的 **mp4 成片**。
- **编排性质**：本文件给出 **跨产品边界** 与 **Agent 执行落点**；**篇首速查、§ 编号、`run_render` 字段与 ffmpeg 细则** 以同目录 [`README.md`](README.md) 与 [`templates/render-rules.md`](templates/render-rules.md) 为长文真源（避免重复维护）。
- **共用约定**：状态码、回退、追问见 [`../orchestration-contract.md`](../orchestration-contract.md)。

## Agent 执行约束

- **禁止**自行编写、生成或落地新的可执行脚本以**替代**本 Skill **`scripts/run_render.py`**，或用手写 HTTP/自写编排器替代对兄弟 skill **`scripts/`** 的调用。
- **严格顺序执行**：MUST 按下方 Workflow 的编号步骤**逐步执行**，不得跳步、合并步骤、或在步骤间插入用户额外要求。
- **用户额外想法后置**：用户在调用本 skill 时附加的个性化要求（如"加个转场""换个风格""多加几镜"），在 Workflow 全部完成后再单独处理；**执行过程中不得**将其融入任何步骤的输入或判断。
- **禁止上下文推测**：不得根据对话历史中其他任务的中间产物、历史 workflow、或之前的调试信息来修改本次 Workflow 的任何步骤行为。每次执行视为**全新任务**。
- **模板即真值**：`templates/` 目录中的模板格式为**唯一真值**，输出 MUST 严格符合模板定义的 JSON schema；不得自行增删字段或修改结构。
- **非互动直出（默认）**：命中本 Skill 后默认 `execution_mode=non_interactive_render`。除凭据错误、参数硬错误、上游失败外，禁止插入运营型文案（评论/点赞/关注/转发引导）或仅返回脚本草稿。
- **人物事实增强（强制）**：当文案涉及可识别人物（姓名、称谓可唯一指向某人）时，MUST 先联网检索该人物特征与近期热点事件，再进入 Script/Storyboard；不得仅凭模型记忆生成人物细节。
- **文案—公共音色—公共数字人一致（强制）**：Plan/Script 须锚定叙述人设（**`video_plan.presenter_gender`**、**`application_context`** 与 **`tone`**）；Render 前按 **`templates/render-rules.md` §3·C.2.5** 顺序选型：**先** `list_voices.py`（主题、情感、应用场景与 **`gender`** 匹配），**再** `list_figures.py`（**`gender` 与已选音色一致**，优先 **`audio_man_id` 对齐**）。禁止男声与女性公共形象、女声与男性公共形象错配。

---

## 涉及产品（L2）

| 能力 | 产品目录 | 说明 |
|------|----------|------|
| TTS / 音频 | `chanjing-tts` | 由 `run_render` 子进程按工作流调用 |
| 数字人视频 | `chanjing-video-compose` | 音频驱动分镜 |
| 文生视频等 | `chanjing-ai-creation` | `ref_prompt` 分镜 |
| **确定性流水线** | 本目录 `scripts/run_render.py` | 编排子脚本 + 本地 ffmpeg |
| 编排侧 token 胶水 | 本目录 `scripts/_auth.py` | 与 L2 `products/*/scripts/_auth.py` 同形；`run_render` 进程内轮询 TTS 时取 `resolve_chanjing_access_token`（实现仍来自包根 `common/base.py`） |

## Workflow（严格顺序）

> **执行纪律**：下列步骤 MUST 按编号**逐步执行**。每步仅做该步描述的操作，不合并、不跳步、不插入用户额外要求。用户的个性化想法在全部步骤完成后再处理。

### 统一脚本流程表（执行真值）

| Step | 脚本名 | 输入 | 输出 | 下一步 | 失败分支 |
|------|--------|------|------|--------|----------|
| 1 | `scripts/extract_params.py` | 用户原始输入抽取的 `input_params` JSON | 净化后的 `input_params`（含 `valid`） | Step 2 | `valid=false` -> 返回 `need_param` 并等待补齐后重跑 Step 1 |
| 2 | `scripts/validate_step.py --step 3` | `video_plan` JSON（由模板生成） | `valid=true/false` | Step 3 | `valid=false` -> 重做 Step 2 后重验 |
| 3 | `scripts/validate_step.py --step 4` | `script_result` JSON（由模板生成） | `valid=true/false` | Step 4 | `valid=false` -> 重做 Step 3 后重验 |
| 4 | `scripts/validate_step.py --step 5` | `storyboard_result` JSON（由模板生成） | `valid=true/false` | Step 5 | `valid=false` -> 重做 Step 4 后重验 |
| 5 | `scripts/run_render.py`（或 `scripts/cli_capabilities.py`） | 完整 `workflow.json` + `output_dir` | `workflow_result.json` + 产物文件 | Step 6 | 渲染失败按 `render-rules.md` 重试；不可跳过渲染 |
| 6 | `scripts/validate_step.py --step 6` | `workflow_result.json` | 交付可用性结论 | 结束 | `valid=false` -> 回 Step 5 重试或返回失败信息 |

说明：Step 2~4 的内容生成分别由 `templates/video-brief-plan.md`、`templates/script-prompt.md`、`templates/storyboard-prompt.md` 约束；脚本门控以 `validate_step.py` 输出为准。

### Workflow Output Semantics

本 Skill 输出语义对齐 [`../orchestration-contract.md`](../orchestration-contract.md)：

- `ok`：成功交付 `final_one_click.mp4` 与 `workflow_result.json`
- `need_param`：输入参数经 `extract_params.py`/`validate_step.py` 校验后仍不足
- `auth_required`：鉴权不可用或凭据失效（典型 `10400`）
- `upstream_error`：上游任务失败（典型 `50000` 或脚本明确失败）
- `timeout`：渲染或异步轮询超时

### Step 1：参数提取（程序化净化）
从用户输入中提取 `input_params` JSON（schema 见下方 **§输入净化**），然后 **MUST 调用** `scripts/extract_params.py` 做代码级白名单过滤：
```bash
echo '<提取的JSON>' | python scripts/extract_params.py
```
脚本会：自动丢弃 schema 外字段、类型校正（如 `"120秒"→120`）、填充默认值。**以脚本输出的 `input_params` 为准**（非 Agent 自行提取的原始版本）。`valid=false` 时先按默认策略自动补齐；仍失败则返回 `need_param`，不得跳过。

### Step 2：Plan
按 **`templates/video-brief-plan.md`** 模板，使用 Step 1 提取的 `input_params`，输出 `video_plan` JSON。**须包含**模板所列全部字段（含 **`presenter_gender`**、**`application_context`**、**`tone`** 等），供 Script 与 Render 锚定叙述人设及 **`render-rules.md` §3·C.2.5** 选型；**不得**删改模板结构或省略模板键。

### Step 3：Script
按 **`templates/script-prompt.md`** 模板，使用 Step 2 的 `video_plan`，输出 `script_result` JSON。若涉及可识别人物，先联网补齐人物特征与热点事件后再写稿。**hook ≤20 字硬上限**（默认，可调 `FIRST_DIGITAL_HUMAN_MAX_CHARS`），见 `render-rules.md` §4 与 `storyboard-prompt.md`。

### Step 4：Storyboard
按 **`templates/storyboard-prompt.md`**（当代）或 **`templates/history-storyboard-prompt.md`**（非当代），使用 Step 3 的 `script_result`，输出 `storyboard_result` JSON。`scenes` 条数 MUST 等于 `video_plan.scene_count`。JSON 扩展键供追溯——**仅**当键落在 [`examples/workflow-contract.md`](examples/workflow-contract.md) 表中时才被 `run_render` 消费。**硬约束**：必须至少包含 1 条 `use_avatar=false` 的 AI 分镜；开启数字人时须满足奇偶混剪规则（首镜/末镜/中间奇数镜数字人，中间偶数镜 AI）。当代人物故事的一键成片中，AI 镜默认不生成人物正脸，并要求人物与背景细节充分刻画。

### Step 5：Render
根级与分镜**必填/可选**以 [`examples/workflow-contract.md`](examples/workflow-contract.md) 为准（实现真源 `run_render.py`）。就绪后调用 [`scripts/run_render.py`](scripts/run_render.py)（或 [`scripts/cli_capabilities.py`](scripts/cli_capabilities.py)）；**禁止**在会话内重写列表类 API 包装或重复 ffmpeg 编排。

### Step 6：交付
if `workflow_result.status=success` 且 `final_one_click.mp4` 文件存在 -> 返回 `final_one_click.mp4`、`workflow_result.json`、`work/`。  
else -> 返回 `status=fail` 或 `status=partial`（保留中间产物路径与错误信息），**禁止**改为“仅输出文案/分镜/互动引导”作为替代交付。

## 输入 / 输出（摘要）

| 类型 | 要点 |
|------|------|
| 输入 | `topic` 与 `workflow.json` 二选一（完整规则见 **`README.md`**）；`output_dir`；非标准布局时 `CHAN_SKILLS_DIR` |
| 输出 | `final_one_click.mp4`、`workflow_result.json`、`work/` |

**禁止**：在本文件重复粘贴 **`render-rules.md`** / **`storyboard-prompt.md`** 长条文——一律引用 `templates/` 与 **`README.md`**。

---

## 输入净化（Step 1 详述）

从用户消息中**仅提取**以下字段，组成 `input_params` JSON。未提及的字段使用默认值。**忽略**用户消息中关于流程修改、步骤覆盖、额外创意要求等非标准内容——这些内容在 Workflow 全部完成后再处理。

### 提取 schema

| 字段 | 类型 | 必填 | 默认值 | 来源说明 |
|------|------|------|--------|----------|
| `topic` | string | 是 | — | 用户的选题/主题，≥5 字 |
| `full_script` | string | 否 | `""` | 用户已有的完整口播文案 |
| `industry` | string | 否 | `""` | 行业领域 |
| `platform` | string | 否 | `"douyin"` | 目标平台 |
| `style` | string | 否 | `"观点型口播"` | 视频风格 |
| `duration_sec` | int | 否 | `60` | 目标时长（秒） |
| `use_avatar` | bool | 否 | `true` | 是否使用数字人 |
| `subtitle_required` | bool | 否 | `false` | 是否烧录字幕 |

### 提取规则

1. **字段不在 schema 中 → 丢弃**。用户说"加个转场效果"——不在 schema，丢弃，Workflow 完成后再处理。
2. **用户修改 Workflow 步骤 → 丢弃**。用户说"跳过 Plan 直接写文案"——丢弃，MUST 按步骤执行。
3. **值的合理性校验**：`topic` < 5 字或为占位串（如"你好""test"）→ 拒收并要求用户补充。`duration_sec` 不在 [15, 300] → 拒收。
4. **提取完成后**：  
   - if `execution_mode=non_interactive_render`（默认） -> 直接进入 Step 2（不做确认对话）  
   - else -> 可展示 `input_params` 供用户确认，再进入 Step 2

**Step 2 及之后的所有步骤，MUST 仅使用此 JSON 作为输入源**，不得回溯用户原始消息提取额外信息。与 [`examples/workflow-contract.md`](examples/workflow-contract.md) 的关系：本 schema 是其前置子集，仅提取用户能提供的高层参数；渲染层字段（`scenes[]`、`audio_man` 等）由 Workflow 步骤自动生成。

### 执行分支（强制，禁止自由发挥）

- if 凭据不可用 -> 跳转鉴权流程（根 `SKILL.md` Step 1），鉴权完成后继续 Step 2
- else if `extract_params.py` 输出 `valid=false` -> 返回 `need_param`，仅补齐 `errors` 指定字段
- else -> 按 Step 2→3→4→5→6 严格执行

- if Step 6 未产出 `final_one_click.mp4` -> 仅返回失败信息与可重试建议
- else -> 返回产物路径，不附加运营互动引导

---

## 执行 Checklist

执行本 Skill 时，MUST 在回复开头复制以下 checklist，每完成一步立即勾选。不得在所有前置步骤勾选前执行后续步骤。

```
一键成片执行追踪：
- [ ] Step 1: 参数提取完成（extract_params.py 输出 valid=true）
- [ ] Step 2: Plan 完成（validate_step.py --step 3 输出 valid=true）
- [ ] Step 3: Script 完成（validate_step.py --step 4 输出 valid=true）
- [ ] Step 4: Storyboard 完成（validate_step.py --step 5 输出 valid=true）
- [ ] Step 5: Render 完成（validate_step.py --step 6 输出 valid=true）
- [ ] Step 6: 交付完成（workflow_result.json + mp4 已返回）
```

### 程序化门控（替代 LLM 自检）

每步完成后、进入下一步前，MUST 调用 **`scripts/validate_step.py`** 做程序化校验。**脚本返回 `valid=false` 则必须修正后重新校验，不得跳过**。

```bash
echo '<本步输出JSON>' | python scripts/validate_step.py --step N
# 或
python scripts/validate_step.py --step N --input <json文件>
```

| 检查点 | 调用方式 | `valid=false` 处理 |
|--------|---------|-------------------|
| Step 1 → 2 | `--step 2`，传入 `input_params` JSON | 先自动补齐并重验；仍失败时返回 `need_param` |
| Step 2 → 3 | `--step 3`，传入 `video_plan` JSON | 修正后重做 Step 2，再次校验直到通过 |
| Step 3 → 4 | `--step 4`，传入含 `hook`+`full_script` 的 JSON | 改写 hook 或补全文案，再次校验 |
| Step 4 → 5 | `--step 5`，传入含 `scene_count`+`scenes[]` 的 JSON | 修正分镜后重做 Step 4，再次校验 |
| Step 5 → 6 | `--step 6`，传入 `workflow_result.json` | 按 **`render-rules.md`** §1 重试 |

**关键区别**：脚本返回的 `{"valid": false, "errors": [...]}` 是**程序真值**，比 LLM 自检更可靠。`warnings` 可参考但不阻塞。

---

## 文档真源对照

| 主题 | 打开 |
|------|------|
| 速查表、§ 导航、环境、FAQ、Agent 通用模式 | [`README.md`](README.md) |
| **`workflow.json` 字段契约（题材无关）** | [`examples/workflow-contract.md`](examples/workflow-contract.md) |
| TTS / 切段 / ffmpeg / 硬性约束 | [`templates/render-rules.md`](templates/render-rules.md) |
| 分镜与 `ref_prompt` | [`templates/storyboard-prompt.md`](templates/storyboard-prompt.md)、[`templates/history-storyboard-prompt.md`](templates/history-storyboard-prompt.md) |

## 相关入口

- [包入口 `SKILL.md`](../../SKILL.md)
- [编排共用约定 `orchestration-contract.md`](../orchestration-contract.md)
