# 快速开始示例

> 一个完整的 4 阶段任务示例，展示如何使用复杂任务指挥子代理技能

---

## 任务概述

**任务**：创建 OpenClaw Skills 封装方法文档和技能

**阶段划分**：
1. 阶段 1：研究 OpenClaw Skills 封装方法
2. 阶段 2：创建技能目录结构
3. 阶段 3：编写 SKILL.md 和参考文档
4. 阶段 4：打包并上传到 Gitee

---

## 步骤 1：初始化任务

### 1.1 创建 task-progress.json

```json
{
  "taskId": "openclaw-skills-research-20260312",
  "taskName": "OpenClaw Skills 封装方法研究和技能创建",
  "status": "in_progress",
  "currentPhase": 1,
  "completedPhases": 0,
  "totalPhases": 4,
  "lastUpdated": "2026-03-12T02:00:00Z",
  "checkpointsDir": "/root/.openclaw/workspace/complex-task-subagent-experience/checkpoints",
  "phases": {
    "phase1": {
      "name": "研究 OpenClaw Skills 封装方法",
      "status": "pending",
      "timeout": 1800000,
      "maxRetries": 3,
      "retries": 0,
      "checkpoint": "phase1-research.json",
      "output": "/root/.openclaw/workspace/research/skills-development/OPENCLAW_SKILLS_封装方法.md"
    },
    "phase2": {
      "name": "创建技能目录结构",
      "status": "pending",
      "timeout": 600000,
      "maxRetries": 3,
      "retries": 0,
      "checkpoint": "phase2-structure.json",
      "output": "/root/.openclaw/workspace/skills/complex-task-subagent/"
    },
    "phase3": {
      "name": "编写 SKILL.md 和参考文档",
      "status": "pending",
      "timeout": 3600000,
      "maxRetries": 3,
      "retries": 0,
      "checkpoint": "phase3-docs.json",
      "output": "/root/.openclaw/workspace/skills/complex-task-subagent/SKILL.md"
    },
    "phase4": {
      "name": "打包并上传到 Gitee",
      "status": "pending",
      "timeout": 300000,
      "maxRetries": 3,
      "retries": 0,
      "checkpoint": "phase4-gitee.json",
      "output": "/root/.openclaw/workspace/skills/complex-task-subagent.skill"
    }
  }
}
```

### 1.2 创建 checkpoints 目录

```bash
mkdir -p /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints
```

### 1.3 配置 Heartbeat

编辑 `HEARTBEAT-TASK.md`（见主 SKILL.md 文档）。

---

## 步骤 2：启动阶段 1

### 2.1 启动子代理

```bash
sessions_spawn \
  --task "研究 OpenClaw Skills 的封装方法，包括：1. 阅读 Skill Creator 的 SKILL.md；2. 学习技能目录结构和打包流程；3. 整理封装方法并输出到 /root/.openclaw/workspace/research/skills-development/OPENCLAW_SKILLS_封装方法.md；4. 完成后写入检查点 /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/phase1-research.json" \
  --label "subagent-research" \
  --runtime "subagent" \
  --mode "run" \
  --timeoutSeconds 1800 \
  --cwd "/root/.openclaw/workspace"
```

### 2.2 子代理完成任务后

子代理应该：

1. 读取相关文档
2. 创建研究报告
3. 写入检查点：

```json
{
  "checkpointId": "phase1-research",
  "phase": "phase1",
  "phaseName": "研究 OpenClaw Skills 封装方法",
  "status": "completed",
  "completedAt": "2026-03-12T02:30:00Z",
  "subagent": "subagent-research",
  "output": "/root/.openclaw/workspace/research/skills-development/OPENCLAW_SKILLS_封装方法.md",
  "result": {
    "success": true,
    "message": "研究完成"
  }
}
```

### 2.3 Heartbeat 检测并推进

Heartbeat 检测到检查点后：

1. 更新 task-progress.json：

```json
{
  "phase1": {
    "status": "completed",
    "completedAt": "2026-03-12T02:30:00Z",
    "subagent": "subagent-research",
    ...
  },
  "completedPhases": 1,
  "currentPhase": 2
}
```

2. 自动启动阶段 2：

```bash
sessions_spawn \
  --task "创建 complex-task-subagent 技能的目录结构，包括：1. 创建 ~/.openclaw/workspace/skills/complex-task-subagent/ 目录；2. 创建子目录：scripts/, references/, assets/；3. 创建 SKILL.md 模板文件；4. 完成后写入检查点 /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/phase2-structure.json" \
  --label "subagent-structure" \
  --runtime "subagent" \
  --mode "run" \
  --timeoutSeconds 600 \
  --cwd "/root/.openclaw/workspace"
```

---

## 步骤 3：继续后续阶段

### 阶段 3：编写文档

```bash
sessions_spawn \
  --task "编写 complex-task-subagent 技能的文档，包括：1. SKILL.md - 包含技能描述、核心原则、工作流程；2. references/quick-start.md - 快速开始示例；3. references/advanced-patterns.md - 高级模式；4. references/troubleshooting.md - 故障排查；5. 完成后写入检查点 /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/phase3-docs.json" \
  --label "subagent-docs" \
  --runtime "subagent" \
  --mode "run" \
  --timeoutSeconds 3600 \
  --cwd "/root/.openclaw/workspace"
```

### 阶段 4：打包和上传

```bash
sessions_spawn \
  --task "打包并上传 complex-task-subagent 技能到 Gitee，包括：1. 打包技能为 .skill 文件；2. 添加到 git；3. 提交并推送；4. 完成后写入检查点 /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/phase4-gitee.json" \
  --label "subagent-gitee" \
  --runtime "subagent" \
  --mode "run" \
  --timeoutSeconds 300 \
  --cwd "/root/.openclaw"
```

---

## 步骤 4：监控任务

### 4.1 查看任务状态

```bash
cat /root/.openclaw/workspace/task-progress.json
```

### 4.2 查看检查点

```bash
ls -la /root/.openclaw/workspace/complex-task-subagent-experience/checkpoints/
```

### 4.3 查看日志

```bash
tail -f /root/.openclaw/workspace/task-monitor.log
```

### 4.4 查看子代理状态

```bash
subagents list
```

---

## 步骤 5：任务完成

当所有阶段完成后：

1. **Heartbeat 检测到所有检查点**

2. **更新任务状态**

```json
{
  "status": "completed",
  "completedPhases": 4,
  "totalPhases": 4
}
```

3. **自动同步到 Gitee**

```bash
cd /root/.openclaw
git add workspace/research/ workspace/skills/
git commit -m "完成：OpenClaw Skills 封装方法研究和技能创建"
git push
```

4. **记录日志**

```bash
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 任务已完成并同步到 Gitee" >> /root/.openclaw/workspace/task-monitor.log
```

---

## 完整流程图

```
主会话启动
   │
   ├─ 创建 task-progress.json
   ├─ 创建 checkpoints 目录
   └─ 配置 Heartbeat
   │
   ▼
阶段 1：研究
   │
   ├─ 启动子代理 subagent-research
   ├─ 子代理完成任务
   ├─ 写入检查点 phase1-research.json
   ├─ Heartbeat 检测到检查点
   ├─ 更新 task-progress.json
   └─ 启动阶段 2
   │
   ▼
阶段 2：创建结构
   │
   ├─ 启动子代理 subagent-structure
   ├─ 子代理完成任务
   ├─ 写入检查点 phase2-structure.json
   ├─ Heartbeat 检测到检查点
   ├─ 更新 task-progress.json
   └─ 启动阶段 3
   │
   ▼
阶段 3：编写文档
   │
   ├─ 启动子代理 subagent-docs
   ├─ 子代理完成任务
   ├─ 写入检查点 phase3-docs.json
   ├─ Heartbeat 检测到检查点
   ├─ 更新 task-progress.json
   └─ 启动阶段 4
   │
   ▼
阶段 4：打包上传
   │
   ├─ 启动子代理 subagent-gitee
   ├─ 子代理完成任务
   ├─ 写入检查点 phase4-gitee.json
   ├─ Heartbeat 检测到检查点
   ├─ 更新 task-progress.json
   └─ 所有阶段完成
   │
   ▼
同步到 Gitee
   │
   ├─ 添加所有修改到 git
   ├─ 提交
   ├─ 推送
   └─ 记录日志
   │
   ▼
任务完成 ✅
```

---

## 注意事项

1. **不要手动修改 task-progress.json** - 由 Heartbeat 自动更新
2. **确保子代理写入检查点** - 这是推进下一阶段的关键
3. **检查 Heartbeat 配置** - 确保检查频率合理
4. **监控任务进度** - 定期检查日志和状态文件
5. **处理超时** - 如果子代理超时，会自动重试

---

**相关文档**：
- [advanced-patterns.md](advanced-patterns.md) - 高级模式
- [troubleshooting.md](troubleshooting.md) - 故障排查
