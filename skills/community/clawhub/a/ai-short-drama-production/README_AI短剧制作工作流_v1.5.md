# AI短剧制作工作流 SKILL v1.5

## 这次升级：剧本到视频生成的完整执行链

v1.5 把原先分散的模块串成了一条可执行链路：

`项目配置 → 故事开发 → 分集/留存 → 场景/分镜 → 角色一致性 → 任务构建 → 付费前预演 → Seedance提交 → 轮询下载 → 配音字幕口型 → 剪辑交付`

## 新增内容

### 1. 全链路执行手册

新增 `references/end-to-end-orchestration.md`，明确每个阶段的：

- 输入
- 输出文件
- 质量闸门
- 付费生成条件
- 失败停止条件

### 2. 安全 Seedance 客户端

新增 `scripts/seedance_client.py`，支持：

- `dry-run`：只检查任务数量和参数，不调用付费接口
- `submit`：必须同时提供 `--execute --confirm-paid` 才会提交
- `poll`：轮询任务状态并下载成功视频
- `status`：查看任务状态统计

默认限制单个提交批次，不允许误操作直接批量烧额度。

### 3. 本地角色参考图自动嵌入

如果任务使用本地参考图，可以在提交时加：

```powershell
--embed-local-refs
```

客户端会把 `meta.reference_paths` 转成 Base64 data URI，再发送给 Seedance。不会把本地路径直接写入请求。

### 4. 任务状态台账

每次提交和轮询都会保存：

- custom_id
- provider task_id
- 状态
- 视频URL
- 下载路径
- 错误信息
- 任务参数摘要

不会把 API Key 或完整 Base64 写入状态文件。

### 5. 与现有工具串联

- `scaffold_project.py`：建项目
- `validate_project.py`：检查项目结构
- `audit_retention.py`：检查钩子和催更设计
- `build_seedance_tasks.py`：从分镜表生成 JSONL
- `seedance_client.py`：预演、提交、轮询、下载

## 快速使用

```powershell
# 1. 建项目
python C:\Users\ASUS\.codex\skills\ai-short-drama-production\scripts\scaffold_project.py "E:\项目目录" --project-name "新短剧" --episodes 20 --series "main"
```

```powershell
# 2. 校验项目
python C:\Users\ASUS\.codex\skills\ai-short-drama-production\scripts\validate_project.py "E:\项目目录"
```

```powershell
# 3. 构造任务
python C:\Users\ASUS\.codex\skills\ai-short-drama-production\scripts\build_seedance_tasks.py --shot-manifest "E:\项目目录\06_shots\shot_manifest.csv" --project-profile "E:\项目目录\project_profile.json" --output "E:\项目目录\06_shots\tasks.jsonl"
```

```powershell
# 4. 只预演
python C:\Users\ASUS\.codex\skills\ai-short-drama-production\scripts\seedance_client.py dry-run --tasks "E:\项目目录\06_shots\tasks.jsonl"
```

```powershell
# 5. 明确授权后提交
python C:\Users\ASUS\.codex\skills\ai-short-drama-production\scripts\seedance_client.py submit --tasks "E:\项目目录\06_shots\tasks.jsonl" --state "E:\项目目录\06_shots\generation_state.json" --output-dir "E:\项目目录\06_shots\raw_generations" --execute --confirm-paid --limit 1 --embed-local-refs
```

```powershell
# 6. 轮询并下载
python C:\Users\ASUS\.codex\skills\ai-short-drama-production\scripts\seedance_client.py poll --state "E:\项目目录\06_shots\generation_state.json" --download-dir "E:\项目目录\06_shots\raw_generations"
```

## 当前火猴总盘

已生成：

- `project_profile.json`
- `01_story/retention_plan.csv`
- `06_shots/shot_manifest.csv`：45镜
- `07_audio/voice_timeline.csv`：45条
- `06_shots/seedance_tasks_preview.jsonl`：45条任务预览
- `validate_project.py`：PASS
- `audit_retention.py`：PASS
- `seedance_client.py dry-run`：可读取45条任务

注意：火猴部分镜头使用本地参考图，正式提交时必须加 `--embed-local-refs`；当前火山方舟账户仍需先处理欠费。

`© 2026 火焰广告 版权所有。`
