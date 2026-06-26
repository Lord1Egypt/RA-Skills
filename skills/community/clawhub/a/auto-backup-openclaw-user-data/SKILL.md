---
name: auto-backup-openclaw-user-data
description: |
  OpenClaw 用户数据自动备份技能。支持全量/选择性备份、定时执行、ZIP 压缩、日志记录、消息通知和保留策略管理。
  
  **触发场景**：
  (1) 用户要求备份 OpenClaw 数据
  (2) 用户要求设置定时备份
  (3) 用户询问备份配置、状态、日志
  (4) 用户执行 /backup_now、/backup_status、/backup_config、/backup_list、/backup_clean 等命令
  (5) HEARTBEAT 触发定时备份检查
---

# Auto Backup OpenClaw User Data

OpenClaw 用户数据自动备份技能。

## 版本

- **当前版本**：v1.1.0.20260414
- **更新日期**：2026-04-14

## 功能

- **自动备份**：定时备份 `.openclaw` 目录
- **选择性备份**：支持全量或部分备份（交互式选择文件/文件夹）
- **ZIP 压缩**：自动压缩并按规则命名
- **定时执行**：支持 HEARTBEAT 心跳和 Cron 定时任务两种方式
- **日志记录**：完整记录执行过程
- **消息通知**：支持多渠道推送结果（需配置推送目标）
- **保留策略**：自动清理旧备份

## v1.1.0 新特性

### 工作空间自动检测
首次配置时自动检测所有workspace目录和memory目录，无需手动配置备份目标。适配多Agent工作环境，避免遗漏备份。

### 敏感文件安全提醒
新增敏感文件识别和提醒机制（密钥、凭证、环境变量等），默认不强制排除，遵循"只做提醒，不做限制"原则，让用户自主决定备份范围。

### 标准化入口改进
创建标准Node.js模块入口（index.js），完整导出所有接口，消除"可疑技能"标记，符合OpenClaw安全最佳实践。

### 配置自动迁移
支持从v1.0.2自动升级到v1.1.0，自动补全缺失配置字段，保留原有配置，零停机平滑升级。

---

## 工作空间自动检测

首次配置时，系统会自动检测您的OpenClaw工作空间：

**检测内容**：
- 所有 `workspace-*` 目录
- `memory` 目录
- 写入配置文件作为默认值

**建议**：首次使用交互式配置确认检测结果。

详见：[README.md工作空间检测章节](README.md#工作空间自动检测)

---

## ⚠️ 安全警告

### 敏感文件风险

备份可能包含敏感文件（密钥、环境变量、凭证等）。

**默认行为**：不强制排除，仅排除临时文件。

**如何启用**：交互式配置Step 7或手动编辑配置文件。

详见：[README.md安全警告章节](README.md#安全警告)

## 命令

| 命令 | 功能 |
|------|------|
| `/backup_now` | 立即执行备份 |
| `/backup_status` | 查看备份状态 |
| `/backup_config` | 配置向导 |
| `/backup_list` | 列出备份文件 |
| `/backup_clean` | 清理旧备份 |

## 定时任务配置

支持两种定时执行方式：

1. **HEARTBEAT 心跳**：适用于周期性监控检查，详见 `HEARTBEAT_prompt_example.md`
2. **Cron 定时任务**：适用于精确时间执行，详见 `cron_prompt_example.md`

## 配置

配置文件位置：`~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/config.json`

### 消息通知配置

```json
{
  "notification": {
    "enabled": true,
    "channels": ["feishu", "telegram"],
    "targets": {
      "feishu": [
        { "type": "group", "id": "oc_xxx", "name": "开发群" },
        { "type": "user", "id": "ou_xxx", "name": "用户名" }
      ],
      "telegram": [
        { "type": "group", "id": "-100xxx", "name": "通知群" }
      ]
    },
    "onSuccess": true,
    "onFailure": true
  }
}
```

**注意**：消息通知需要在 OpenClaw 中先配置对应的通信渠道，详见 `references/config-schema.md`。

详细配置说明：见 [references/config-schema.md](references/config-schema.md)

## 故障排查

常见问题：见 [references/troubleshooting.md](references/troubleshooting.md)

## 升级指南

### 从 v1.0.2 升级到 v1.1.0

**推荐升级方式**：卸载旧版本后重新安装

```bash
# 卸载旧版本
openclaw skill uninstall auto-backup-openclaw-user-data

# 安装新版本
openclaw skill install auto-backup-openclaw-user-data
```

**原因**：获得完整的v1.1.0默认配置，包括工作空间自动检测、敏感文件建议列表、encryption配置字段。

### 配置自动迁移

保留现有配置的用户，系统会自动补全v1.1.0新增字段，无需手动修改配置。

### 升级后重要变更

1. **backup.mode默认值**：从"full"（全量备份）改为"partial"（选择性备份）
2. **工作空间检测**：从硬编码改为动态自动检测
3. **敏感文件提醒**：新增建议排除列表（默认不启用）

**建议**：升级后运行 `/backup_config` 重新确认备份目标，并根据安全需求决定是否启用敏感文件排除。

### 兼容性

- ✅ 配置兼容：v1.0.2配置自动补全新字段
- ✅ 备份兼容：备份文件格式完全兼容
- ✅ 命令兼容：所有 `/backup_*` 命令保持不变
- ✅ 定时兼容：HEARTBEAT和Cron配置无需修改

详细升级说明：见 [README.md升级指南](README.md#升级指南)

## 更新日志

### v1.1.0.20260414 (2026-04-14) - 安全优化版本

**脚本入口改进**：
- 创建标准`index.js`入口文件，完整导出所有接口
- 导出`runCommand`函数，确保命令正常调用
- 消除"可疑技能"标记

**工作空间动态检测**：
- 新增`detectWorkspaces()`函数，首次配置自动检测workspace
- 修复硬编码targets问题

**敏感文件处理**：
- 添加敏感文件建议列表配置（默认不启用）
- 遵循"只做提醒，不做限制"原则

**文档完善**：
- 添加工作空间动态检测和安全警告说明

### v1.0.2.20260331 (2026-03-31)

- 新增：HEARTBEAT 心跳定时任务模板（`HEARTBEAT_prompt_example.md`）
- 新增：Cron 定时任务模板（`cron_prompt_example.md`）
- 新增：选择性备份交互式文件选择功能
- 新增：文件选择确认/重新选择功能
- 优化：交互式配置步骤从 6 步调整为 7 步
- 优化：选择性备份时列出 `~/.openclaw/` 目录文件清单
- 文档：README.md 和 USAGE.md 新增定时任务配置说明

### v1.0.1.20260326 (2026-03-26)

- 新增：消息推送目标配置功能
- 新增：读取 OpenClaw 配置自动获取可用推送目标
- 新增：推送失败时通过当前对话提醒用户
- 优化：`/backup_list` 只显示本 skill 产生的备份文件
- 优化：交互式配置增加推送目标选择步骤

### v1.0.0.20260326 (2026-03-26)

- 初始版本发布