---
name: "openclaw-codex-collaboration"
version: "1.0.0"
description: "OpenClaw 调度 Codex 开发协作规范：标准调用方式、canary 自检、任务目录结构、提示模板、验证闭环、交接单体系"
---

# OpenClaw 调度 Codex 开发协作规范

> **状态：已验证。** 2026-06-18 BE-003 试跑成功，关键参数位置已确认。

## 一、基本调用方式

```bash
# 开发任务（默认）
codex -a never exec -C "$REPO" -s workspace-write --json -o "$RESULT_FILE" "$PROMPT"

# 只读分析
codex -a never exec -C "$REPO" -s read-only --json -o "$RESULT_FILE" "$PROMPT"
```

**⚠️ 关键：`-a never` 是 Codex 顶层参数，必须放在 `exec` 前面。**

错误写法：`codex exec -a never ...`（会报错或静默阻塞）  
正确写法：`codex -a never exec ...`

## 二、执行前必做：Canary 自检

每次正式开发任务前，先跑一次 canary 验证 Codex 可用：

```bash
codex -a never exec \
  -C "$REPO" \
  -s read-only \
  --json \
  -o "$JOB_DIR/canary-result.md" \
  "只回答：Codex exec canary ok。不要修改文件。" \
  > "$JOB_DIR/canary.jsonl" 2>&1
echo $? > "$JOB_DIR/canary-exit-code.txt"
```

**通过标准：** 退出码 0、canary-result.md 非空、canary.jsonl 非空。

自检失败 → 不得继续安排开发任务，先排查 CLI 参数、登录状态、模型配置、网络。

## 三、任务目录结构

每个项目维护独立目录：

```text
~/.openclaw-codex/projects/{project_name}/
  brief.md              # 项目概要
  architecture.md       # 架构分析
  roadmap.md            # 计划
  tasks/                # 任务拆分
    001-task-name.md
  runs/                 # 执行记录
    20260618-001/
      prompt.md         # Codex 任务提示
      result.md         # Codex 输出（-o 参数）
      codex.jsonl       # Codex 事件日志（--json stdout）
      diff.patch        # git diff
      test.log          # 测试输出
      status.json       # 任务状态
```

## 四、任务提示模板

```text
你是本机工程执行器。请在指定仓库中完成开发任务。

仓库路径：{repo_path}

任务目标：{task_goal}

任务范围：{allowed_scope}

禁止事项：
- 不要修改无关文件
- 不要做 UI 页面设计创意
- 不要执行破坏性 git 操作（reset --hard、push、rebase）
- 不要删除用户未要求删除的文件
- 不要安装依赖，除非任务明确授权
- 不要部署，除非任务明确授权
- 如果需要联网、安装依赖、访问仓库外文件、修改系统配置 → 停止并说明原因

完成要求：
1. 实现代码修改
2. 运行相关验证
3. 输出修改文件列表
4. 输出测试结果
5. 输出剩余风险
6. 如果任务无法完成，说明阻塞原因和需要用户确认的问题

用户原始指令：
{user_message}
```

## 五、执行后必做：零产出检查

每次 Codex 执行后必须检查：

1. 退出码是否为 0
2. `result.md` 是否存在且非空
3. `codex.jsonl` 是否存在且非空
4. `git diff --stat` 是否符合预期

任一失败 → 标记为 `blocked`，不标记为 `completed`。

**零产出处理：**
1. 确认 `-a never` 在 `exec` 前面
2. 检查 `codex --version` 和 `codex exec --help`
3. 用只读 canary 验证
4. canary 成功但任务零产出 → 缩小任务范围重试一次
5. 连续两次零产出 → 暂停并汇报用户

## 六、交接单体系

OpenClaw 与 Codex 之间通过结构化交接单传递需求：

**OpenClaw → Codex（01 交接单）：**
- 接口契约（端点路径、方法、请求/响应 DTO）
- 文件白名单/黑名单
- 验收标准（编译命令、端点数量、DTO 字段完整性）
- 禁止事项（不新增端点、不改变服务归属、不跳过 DTO）

**Codex → OpenClaw（02 执行记录）：**
- 修改文件列表
- 验证结果
- 偏离说明（如有）
- 遗留问题

目录：`outputs/collaboration_inbox/`

## 七、已验证的试跑结果

| 项目 | 日期 | 任务 | 结果 |
|:------|:------|:------|:------|
| LexGuard | 2026-06-18 | BE-003 总览仪表盘 API | ✅ 6/6 文件创建，端点/DTO 完全对齐交接单 |
| LexGuard | 2026-06-18 | Canary 自检 | ✅ 退出码 0，输出正常 |

## 八、已确认的禁忌

- `codex exec -a never` → 报错（参数位置错误）
- 未做 canary 自检 → 不得直接安排开发任务
- 任务退出码非 0 但标记 completed → 禁止
- result.md 为空但标记 completed → 禁止
