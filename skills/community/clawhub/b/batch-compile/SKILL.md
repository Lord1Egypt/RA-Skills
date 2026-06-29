---
name: batch_compile
description: Batch-compile existing Gitea, Obsidian Git, or manual zip material sources into personal or team knowledge bases with preview, confirmation, job tracking, source archiving, codebase overview generation, and import reports.
---

# Skill: batch_compile - 批量知识编译

## 用途

把已有资料源一次性编译进个人或团队知识库，解决“知识库不应该从 0 一条条上传”的问题。

第一版支持：

- Gitea 仓库资料源
- Obsidian Git 仓库资料源，本质仍是 Gitea 仓库
- 手动上传 zip 资料包，一次性导入，不默认开启自动更新

核心流程：

```text
确定目标库 -> 选择项目 -> 扫描资料源 -> 预览 -> 用户确认 -> 分批编译 -> 导入报告
```

确认前不得写入目标知识库。

## 触发条件

Activate when:

- 用户说“批量编译这个 Gitea 仓库”
- 用户说“接入这个资料仓库”
- 用户说“初始化团队知识库，这是资料仓库”
- 用户说“这是我的 Obsidian Git 仓库”
- 用户上传 zip 并要求批量导入

Do NOT activate when:

- 用户只上传单个 PDF/Word/文本，交给 `ingest_document`
- 用户只是查询知识库，交给 `query_kb`
- 用户未注册，先交给 `init_workspace`

## 目标库判断

OpenClaw 字段映射：

- `SenderId`：触发导入的人 open_id
- `ChatType`：`direct` 或 `group`
- `GroupSubject`：群聊 chat_id
- `MessageSid`：消息 id，用于审计
- `MessageThreadId`：消息线程 id，如果 OpenClaw 提供则写入 job，用于后续回帖/通知
- `AccountId`：OpenClaw 账号标识，如果 OpenClaw 提供则写入 job

私聊用户且未明确目标时，必须询问：

```text
你希望导入到哪里？
1. 我的个人知识库
2. 团队知识库：<team_name>
```

规则：

- 群聊触发时，必须用 `GroupSubject -> chat_bindings.json -> team_id` 路由到当前群绑定团队。
- 群聊未绑定团队：拒绝批量编译，提示管理员先绑定本群。
- 群聊中不能导入个人知识库。
- 群聊中的 Gitea/Obsidian Git 长期资料源仍然要求发送者 `SenderId` 是团队管理员。
- 个人资料源：用户本人可接入。
- 团队长期资料源：只有团队管理员可接入。
- Obsidian Git 默认导入个人知识库；若导入团队库，需要二次确认。
- 手动 zip 是一次性资料包，默认 `auto_update=false`。

## 项目选择

目标是团队知识库时，必须确认项目：

```text
这批资料属于哪个项目？
1. general（团队公共资料）
2. 选择已有项目
3. 创建新项目
```

普通成员不能创建新项目；只有团队管理员可以。创建新项目时调用：

```bash
python3 scripts/create_project.py --open_id <SenderId> \
  --project_name "<项目名称>" \
  --brief "<项目说明>"
```

## 扫描资料源

Gitea / Obsidian Git：

```bash
python3 scripts/scan_source.py --source_url "<Gitea repo URL>" \
  --source_type gitea_repo \
  --save_to /tmp/paperkb/scan.json
```

手动 zip：

```bash
python3 scripts/scan_zip.py --zip_file "<上传的zip路径>" \
  --source_label "<资料包名称>" \
  --max_files 1000 \
  --max_file_mb 80 \
  --max_total_mb 500 \
  --max_compression_ratio 100 \
  --save_to /tmp/paperkb/scan.json
```

扫描脚本只读取资料源，不写知识库。输出包括：

- 文件统计
- 每个文件的 `action`
- 跳过原因
- README / 代码 / 依赖 / 文档分类
- `current_fingerprints`
- Gitea 源的 `latest_commit`

文件动作：

- `document`：逐篇编译 summary
- `code_context`：进入代码仓库总览
- `dependency_context`：进入代码仓库总览的环境部分
- `skip`：跳过并写入报告

## 预览

扫描后必须向用户展示预览，并等待“开始编译”等明确确认。
在飞书中优先发送互动卡片，而不是让用户手打“开始编译”。如果脚本返回 `interactive_card`，OpenClaw 需要把它作为飞书互动卡片发送；按钮回调中的 `start_batch:<task_id>` 对应调用 `run_batch.py`，`cancel_batch:<task_id>` 对应调用 `cancel_task.py`。
收到任意 batch 卡片按钮回调时，也可以先调用 `resolve_card_action.py --action_value <CardActionValue>`，再按返回的 `command` 和 `args` 执行；如果返回 `sender_arg=confirmed_by`，必须把当前 `SenderId` 作为 `--confirmed_by` 传入。

预览至少包括：

- 资料源名称和目标知识库
- 各类可编译文件数量
- 跳过文件数量和主要原因
- 是否会生成代码总览
- 自动更新是否开启
- 预计写入的项目空间

## 分批编译

确认后先登记资料源并创建确认任务：

```bash
python3 scripts/prepare_batch.py \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --message_sid <MessageSid> \
  --message_thread_id <MessageThreadId> \
  --account_id <AccountId> \
  --scan_file /tmp/paperkb/scan.json \
  --target_scope team \
  --target_kb_owner <owner> \
  --target_kb_repo <repo> \
  --target_team_id <team_id> \
  --target_project_id <project_id>
```

用户确认后创建 job：

```bash
python3 scripts/run_batch.py --task_id <task_id> \
  --confirmed_by <SenderId> \
  --batch_size 100
```

创建 job 后必须自动派后台 worker，不能再询问用户“派后台 worker / 当前会话一篇一篇来 / 暂停”。后台 worker 是默认策略。

派出后台 worker 后，立刻记录 worker 信息：

```bash
python3 scripts/record_worker_spawn.py --job_id <job_id> \
  --child_session_key <child_session_key> \
  --run_id <run_id> \
  --task_name "<task_name>" \
  --spawn_status spawned
```

后台 worker 自动取下一步：

```bash
python3 scripts/batch_worker.py --job_id <job_id> --claim
```

只有在调试或 OpenClaw worker 不可用时，才允许人工直接循环取下一批：

```bash
python3 scripts/get_next_batch.py --job_id <job_id>
```

`--claim` / `get_next_batch.py` 只代表文件被领取，不代表完成。每个文件必须调用 `mark_file_result.py` 写入结果后，才算真正处理完成。

对每个返回文件：

1. Gitea 源调用 `fetch_source_file.py --ref <source_ref>` 下载源文件；zip 源直接使用 `local_path`。
2. 根据文件类型判断资料类型，调用 `render_summary_template.py` 获取结构模板；把返回 JSON 里的 `rules`、`quality_checklist`、`must_capture_fields` 和 `markdown_template` 一起交给 MiniMax，提取文本后让 MiniMax 按模板生成 summary。
3. 调 `check_duplicate.py` 查重。
4. 调 `ingest_document/scripts/save_document.py` 或同等保存脚本写入知识库，并传入 `--source_file_path` 归档原文。
5. 调 `mark_file_result.py` 记录结果。

生成每篇 summary 前调用：

```bash
python3 scripts/render_summary_template.py \
  --type_key <paper|survey|project|doc|experiment|meeting|codebase|note> \
  --title "<标题>" \
  --project_id <project_id> \
  --source_id "<source_id>" \
  --source_path "<source_path>" \
  --source_url "<source_url>" \
  --source_commit "<source_commit>" \
  --save_to /tmp/paperkb/summary_template.json
```

MiniMax 必须按模板填写，不得删除章节；原文没有的信息填“未提及”，不确定但有原文线索时写“资料显示不完整：<线索>”。每篇都必须保留“知识库定位”“证据索引”“关键词与实体”“来源与可追溯信息”。模板重点：

- `paper`：研究问题、任务边界、贡献、方法流程、数据/指标/基线、结果、消融、失败案例、局限、可复用点。
- `survey`：范围、资料来源可信度、分类框架、结论证据、关键数据、主要方案、机会、风险、信息缺口、团队启发。
- `project`：目标场景、功能边界、架构、运行方式、依赖、许可证、成熟度、复现风险、安全隐私风险、改造成本。
- `doc`：适用版本、前置条件、概念、流程/API/命令/配置、示例、约束、排错、项目关系。
- `experiment`：假设、成功标准、变量和对照、环境、代码 commit、数据/模型、结果、异常、产物、下一步行动。
- `meeting`：参会人、议题、讨论分歧、决定、行动项、风险阻塞、开放问题、项目页更新建议。
- `codebase`：仓库目标、入口、目录结构、模块、调用链、配置、外部服务、运行测试、复现风险、改造建议。
- `note`：背景、触发材料、核心想法、依据、假设、不确定点、关联知识、行动项、待验证问题。

有代码文件时：

1. 调 `build_code_pack.py` 生成 code pack。
2. 调 `render_summary_template.py --type_key codebase` 获取代码仓库总览模板，让 MiniMax 生成代码总览。
3. 调 `compile_codebase.py --job_id <job_id>` 保存到 `summaries/codebases/` 并标记 job。

全部完成后：

```bash
python3 scripts/finalize_batch.py --job_id <job_id>
```

`finalize_batch.py` 会先检查：

- 所有 `document_files` 都已有 `file_results`
- 没有仍处于 claimed 状态的文件
- 有代码文件时已经生成 `codebase_result`

检查通过后才把 `file_fingerprints` 和 `last_commit` 写回 `sources.json`，供后续增量扫描使用。

## 完成通知

不要依赖后台子会话自动发完成消息。完成通知由 OpenClaw 控制台的定时任务主动轮询：

```bash
python3 scripts/notify_jobs.py
```

返回 `notifications` 后，OpenClaw 定时任务逐条调用飞书发消息工具，把 `message` 发给 `target`。发送成功后调用：

```bash
python3 scripts/notify_jobs.py --mark_sent --job_id <job_id>
```

发送失败时调用：

```bash
python3 scripts/notify_jobs.py --mark_failed --job_id <job_id> \
  --error "<发送失败原因>"
```

`finalize_batch.py` 会在 job 进入 `completed`、`partial`、`failed`、`cancelled` 或 `timed_out` 后把 `notify_status` 置为 `pending`。定时通知任务负责补发，直到 `notified=true`。

## 脚本清单

- `create_project.py`：团队管理员创建项目空间
- `scan_source.py`：扫描 Gitea 仓库文件树并分类
- `scan_zip.py`：带数量/大小上限地安全解压并扫描手动上传 zip
- `chat_context.py`：解析 OpenClaw 群聊上下文和群绑定
- `fetch_source_file.py`：按 ref 下载资料源中的单个文件
- `build_code_pack.py`：扫描代码/README/依赖并生成 code pack
- `render_summary_template.py`：输出不同资料类型的结构化 summary 模板
- `summary_templates.py`：维护资料类型模板和生成规则
- `prepare_batch.py`：登记资料源并创建确认任务
- `resolve_card_action.py`：解析批量编译卡片按钮
- `cancel_task.py`：取消待确认的批量编译任务
- `run_batch.py`：确认后创建批量编译 job
- `record_worker_spawn.py`：记录后台 worker 子会话信息
- `batch_worker.py`：返回下一步应执行的批量动作
- `get_next_batch.py`：从 job 中取下一批待处理文件
- `mark_file_result.py`：记录单个源文件成功/失败/跳过
- `finalize_batch.py`：完成任务并把 fingerprints/commit 写回资料源
- `notify_jobs.py`：列出待发送的 job 完成通知，并标记发送成功或失败
- `compile_codebase.py`：保存代码总览
- `save_import_report.py`：保存导入报告
- `continue_job.py`：更新 job 进度
- `check_duplicate.py`：批量处理前查重
- `permissions.py`：校验目标库、团队成员、团队管理员等权限
- `cards.py`：生成飞书互动卡片 payload

OpenClaw 仍需负责语义步骤：读取文本、调用 MiniMax 生成 summary/codebase/report 草稿，并调用保存脚本写入 Gitea。
