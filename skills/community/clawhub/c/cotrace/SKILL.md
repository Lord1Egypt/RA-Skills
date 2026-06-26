---
name: cotrace
version: 1.2.0
description: >
  工作轨迹采集：通过 Pieces + Cotrace 自动采集用户日常工作活动，获取个人上下文。
  Triggers: cotrace, pieces, 工作记录, 最近做了什么, 今天做了什么, trace, 采集, 轨迹.
  NOT for: 任务管理(use auwomo-task), 消息发送(use auwomo-message).
metadata:
  openclaw:
    requires:
      bins:
        - ftc
---

# cotrace

基于 Pieces OS + Cotrace 的工作轨迹自动采集能力。用于获取用户的实际工作活动数据。

注意：工具返回的时间戳为 UTC 格式（以 Z 结尾）。展示给用户时需转换为本地时区。如果用户使用中文，可假定为北京时间（UTC+8）。

## 触发条件

- 用户说"帮我看看最近做了什么"
- 用户说"查一下我今天的工作记录"
- 需要获取用户实际工作活动数据时

## 排除场景

- 任务创建/更新/汇报 → 转到 `auwomo-task`
- 发消息 → 转到 `auwomo-message`
- Cotrace 未安装或不可用 → 引导安装（见 references/install.md）

## 健康检查

执行以下命令确认 Cotrace 服务可用：

```bash
ftc health cotrace
```

如果输出不包含 `"ok":true`，参考 [install.md](references/install.md) 排查。

## 工作流程

1. **查询摘要**：用 `get_workstream_summaries` 按时间范围搜索工作记录
2. **获取详情**：用 `get_workstream_summaries_details` 根据返回的 ID 获取完整内容（含 AI 标注）

## 命令速查表

### 1. 查询工作摘要

```bash
echo '{"tool":"get_workstream_summaries","args":{"created":{"from":"<ISO_START>","to":"<ISO_END>"}}}' | ftc call cotrace
```

`created.from` 和 `created.to` 均为可选（ISO 8601 格式），按需使用。

### 2. 获取详细内容

```bash
echo '{"tool":"get_workstream_summaries_details","args":{"identifiers":["<UUID_1>","<UUID_2>"]}}' | ftc call cotrace
```

## 示例

用户问："我今天做了什么？"

```bash
# 1. 查询今天的记录
echo '{"tool":"get_workstream_summaries","args":{"created":{"from":"2026-05-13T00:00:00Z","to":"2026-05-13T23:59:59Z"}}}' | ftc call cotrace

# 2. 获取详细内容
echo '{"tool":"get_workstream_summaries_details","args":{"identifiers":["<返回的ID>"]}}' | ftc call cotrace
```

## 参考文档路由

| 场景 | 文档 |
|------|------|
| 首次安装配置 | [install.md](references/install.md) |
| 健康检查失败 / 服务不可用 | [install.md](references/install.md) |
