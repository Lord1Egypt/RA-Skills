# Feishu Progress Heartbeat

飞书长任务进度心跳播报技能。

## 功能

当飞书会话中有长运行任务时，自动每 3 分钟发送一次进度更新，包含：
- 简短阶段标签
- 预估完成百分比
- 当前状态说明

## 使用场景

- 长运行文档生成任务
- 批量数据处理
- 多步骤工作流
- 用户询问"还在运行吗？"

## 文件结构

```
feishu-progress-heartbeat/
├── SKILL.md          # 技能定义
└── README.md         # 本文档
```

## 相关技能

- `feishu-task-status` — 任务状态检查
- `feishu-parallel-dispatch` — 并行任务分发
- `feishu-task-control` — 任务控制（停止/清理）

## 中文说明

主要技能定义见 [SKILL.md](./SKILL.md)。
