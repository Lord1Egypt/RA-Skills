---
name: airilab
description: 统一调用 AiriLab 图像生成与任务管理能力（MJ 创意渲染 workflowId=0、创意放大 workflowId=16、氛围转换 workflowId=13），并自动处理登录鉴权、项目选择、任务提交、状态轮询与结果回推。用户提到 Midjourney/MJ 文生图、参考图生成、放大超分/4K、天气季节昼夜氛围转换，以及“登录AiriLab、选择/切换项目、查询job状态/结果”等请求时使用。
---

# AiriLab Skill

## 目标
- 将 AiriLab SaaS 的多接口流程封装为可对话调用的单一技能。
- 在调用图像能力前，自动保证登录态与项目上下文有效。
- 通过后台 worker 追踪异步任务并主动回推结果。

## 能力范围
- 鉴权：手机号 + 验证码登录，持久化 token。
- 项目管理：拉取团队/项目、选择项目、持久化项目上下文。
- 图像工作流：
  - `workflowId=0` MJ 创意渲染（文生图/参考图生成）
  - `workflowId=16` 创意放大
  - `workflowId=13` 氛围转换（天气/季节/光照语义转换）
- 异步任务：提交后轮询状态，完成后拉取记录并通知用户。

## 触发规则
当用户表达以下任一意图时自动触发：
- MJ 创意渲染：文生图、概念图、效果图、参考图生成、多图出图。
- 创意放大：清晰度增强、超分辨率、长边 4K 放大、细节/纹理增强。
- 氛围转换：天气/季节/昼夜切换，提升画面氛围、故事感和视觉张力。
- AiriLab 流程操作：登录、验证码、选择项目、切换项目、查询任务状态、拉取任务结果。

强触发关键词（任一命中即可）：
- MJ/渲染类：`mj`、`midjourney`、`文生图`、`渲染`、`概念图`、`效果图`、`参考图出图`、`生成4张`
- 放大类：`创意放大`、`放大`、`高清`、`超分`、`4k`、`长边4k`、`细节增强`、`纹理增强`
- 氛围类：`氛围转换`、`atmosphere`、`天气切换`、`季节切换`、`白天转夜景`、`晴天`、`雨天`、`雪景`
- 流程类：`airilab登录`、`验证码登录`、`选择项目`、`切换项目`、`projectId`、`jobId`、`任务状态`、`查询结果`

高置信触发语句示例：
- “用 MJ 生成 4 张现代建筑外立面概念图。”
- “把这张图做创意放大，长边 4K，细节和质感增强。”
- “把这张白天街景转成雨夜氛围，保留构图。”
- “帮我登录 AiriLab，然后列出项目让我选一个。”
- “这个 jobId 帮我查下状态，完成后把结果发我。”

触发优先级：
1. 用户上传图像且包含“放大/氛围转换/改图”语义 -> 优先匹配 `workflowId=16` 或 `workflowId=13`。
2. 无上传图像但包含“生成/渲染/MJ”语义 -> 匹配 `workflowId=0`。
3. 包含“登录/项目/job 状态/结果”语义 -> 进入鉴权、项目或异步任务查询流程。

不触发条件（避免误触发）：
- 用户仅讨论通用设计理论、审美评价，不要求生成/改图/放大/状态查询。
- 用户请求与 AiriLab 无关的纯文本任务（翻译、总结、写作）且未提及图像工作流。

## 前置条件（强约束）
1. 调用任何 AiriLab 接口前必须检查登录态。
2. 提交图像任务前必须存在已选项目（`teamId/projectId/projectName`）。
3. 登录失效时必须引导手机号验证码登录，不要求用户提供 token。

## 工作流参数约束

### 1) MJ 创意渲染（`workflowId=0`）
- 必填：`prompt`
- 可选：`referenceImage`（最多 3 张）、`imageCount`（1-4）

### 2) 创意放大（`workflowId=16`）
- 必填：`baseImage`
- 可选：`width`、`height`

### 3) 氛围转换（`workflowId=13`）
- 必填：`baseImage`
- 可选：`prompt`、`referenceImage`（最多 1 张）、`imageCount`

## 多语言文案规范
以下文案用于能力介绍展示，字段名固定，换行统一使用 `\n`。

### 1) MJ 创意渲染（`workflowId=0`）
```yaml
desc: "The most creative and aesthetic AI model for fast, high-quality concept visuals."
descCN: "美学和创意性最强的AI模型，快速生成高质量概念意向图"
descFR: "Le modèle d’IA le plus créatif et esthétique pour générer rapidement des visuels conceptuels de haute qualité."
```

### 2) 创意放大（`workflowId=16`）
```yaml
content: "4K Long-Edge Upscale with Enhanced Details and Texture"
contentCN: "放大至长边4K\n增强细节和质感"
contentFR: "Agrandissement 4K (côté long) avec amélioration des détails et des textures"
```

### 3) 氛围转换（`workflowId=13`）
```yaml
heading: "Atmosphere swift"
headingCN: "氛围转换"
headingFR: "Atmosphère rapide"
content: "Quickly switch between weather and seasons\nApplicable scenarios: Rapidly enhance atmospheric expression, improve the narrative and visual tension of the proposal."
contentCN: "快速切换画面天气、季节\n适用场景：快速提升氛围表达，提升方案故事感与视觉张力"
contentFR: "Changez rapidement entre la météo et les saisons\nScénarios applicables : Améliorez rapidement l'expression atmosphérique, améliorez la narration et la tension visuelle de la proposition."
```

## 异步任务处理（强约束）
轮询任务状态与查询生成记录必须分离：
- 轮询状态接口：`GET /api/Universal/Job/{jobId}`
  - 状态字段来源：`data.status`
- 记录查询接口：`POST /api/CrudRouters/getOneRecord`
  - 仅在状态为 `completed` 后调用

脚本职责：
- `scripts/check_status.py`：只做状态轮询，输出 `status:<value>`。
- `scripts/fetch.py`：只做记录查询，返回生成 URL 列表等结果。
- `scheduler/worker.py`：负责任务生命周期与通知。
- 任务提交成功后必须立即结束本轮对话，并明确告知用户“后台完成后会自动通知”。

## 本地持久化
- 运行根目录：优先使用环境变量 `AIRILAB_HOME`，未设置时默认 `~/.openclaw/skills/airilab`。
- `config/.env`：token 与登录相关信息。
- `config/project_config.json`：当前项目上下文。
- `scheduler/jobs.db`：异步任务状态。
- `scheduler/worker.log`：worker 运行日志。
- `scheduler/worker.pid`：worker 单实例锁文件。

## 运行命令
```bash
# 安装依赖
python -m pip install -r ~/.openclaw/skills/airilab/requirements.txt

# 查看配置状态
python ~/.openclaw/skills/airilab/core/config.py status

# 查看运行健康状态（token/project/worker/jobs）
python ~/.openclaw/skills/airilab/core/config.py health

# 一键健康检查（状态 + worker + 最近日志）
~/.openclaw/skills/airilab/scripts/health.sh

# 安装后初始化（依赖 + worker + 自启动）
~/.openclaw/skills/airilab/scripts/post-install.sh

# 启动后台 worker
~/.openclaw/skills/airilab/scripts/start-worker.sh
```

## 故障处理
- `missing_token`：引导用户登录。
- `missing_project`：引导用户选择项目。
- `timeout` / 轮询超时：任务标记失败并通知用户重试。
- 记录查询 `success=false`：按失败处理，不得误判成功。

## 相关文件
- `core/config.py`
- `core/auth.py`
- `core/project.py`
- `core/upload.py`
- `core/api.py`
- `scripts/check_status.py`
- `scripts/fetch.py`
- `scheduler/worker.py`
- `SPEC.md`

## Agent 执行约束（强约束）

### 1) 执行责任
- Agent 必须直接执行可执行步骤，不得把可执行命令转嫁给用户。
- 禁止输出“你可以手动执行…/请你在终端执行…”这类兜底话术，除非明确出现权限/环境阻塞且无法由 Agent 代执行。
- 登录场景下，Agent 只向用户索取最小必要输入：`phone`、`code`；拿到后立即自行执行登录命令。

### 2) 路径解析与工作目录
- `skill_root`：以当前 `SKILL.md` 所在目录为准，不依赖对话中的硬编码路径。
- `runtime_root`：优先 `AIRILAB_HOME`，未设置时使用 `~/.openclaw/skills/airilab`。
- Agent 执行命令时必须使用绝对路径，且 `cwd` 设置为 `skill_root`，避免 `cd` 到错误目录。

### 3) 命令调用规范
- 登录：`python core/auth.py login --phone <phone> --code <code>`（由 Agent 执行）
- 状态：`python core/config.py status`（由 Agent 执行）
- 健康：`python core/config.py health` 或 `scripts/health.sh`（由 Agent 执行）
- 启动 worker：`scripts/start-worker.sh`（由 Agent 执行）

### 4) 对话输出规范
- 当缺少参数时，只提问缺失参数，不提供“手动执行命令”替代方案。
- 执行后返回结果摘要（成功/失败、关键字段、下一步），不要只返回命令文本。
- 若必须让用户介入，只允许两类：输入验证码、确认业务选择（例如项目选择）。
