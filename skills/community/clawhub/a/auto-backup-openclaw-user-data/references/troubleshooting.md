# 故障排查指南

本文档提供 `Auto-Backup-Openclaw-User-Data` 技能的常见问题排查方法。

---

## 目录

1. [安装问题](#安装问题)
2. [备份执行问题](#备份执行问题)
3. [定时任务问题](#定时任务问题)
4. [通知问题](#通知问题)
5. [配置问题](#配置问题)
6. [日志查看](#日志查看)

---

## 安装问题

### Q: 安装后命令无响应

**症状**：执行 `/backup_now` 等命令没有任何响应。

**排查步骤**：

1. 检查 skill 是否正确安装
   ```
   查看目录：~/.agents/skills/auto-backup-openclaw-user-data/
   ```

2. 检查 SKILL.md 是否存在
   ```
   文件路径：~/.agents/skills/auto-backup-openclaw-user-data/SKILL.md
   ```

3. 重启 OpenClaw
   ```bash
   openclaw restart
   或
   openclaw gateway restart
   ```

### Q: 首次使用提示配置文件错误

**症状**：提示配置文件不存在或格式错误。

**原因**：首次使用时，系统会自动创建默认配置文件。

**解决方案**：
- 正常情况下系统会自动创建配置
- 如果手动创建了配置文件，请确保 JSON 格式正确
- 运行 `/backup_config` 选择 [3] 重置为默认配置

---

## 备份执行问题

### Q: 备份失败，提示 "磁盘空间不足"

**错误信息**：`ENOSPC: no space left on device`

**解决方案**：

1. 清理磁盘空间
2. 更改备份存储路径
   ```
   /backup_config
   选择修改存储路径
   ```
3. 调整保留策略，减少保留的备份数量

### Q: 备份失败，提示 "权限不足"

**错误信息**：`EACCES: permission denied`

**解决方案**：

1. 检查目标目录权限
   ```bash
   # Linux/macOS
   ls -la ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/
   
   # Windows (以管理员身份运行)
   icacls "%USERPROFILE%\.openclaw\workspace\Auto-Backup-Openclaw-User-Data"
   ```

2. 以管理员/root 权限运行（不推荐常规操作）

3. 更改备份存储路径到有权限的目录

### Q: 部分文件被跳过

**症状**：备份完成但提示 "跳过 N 个文件"。

**原因**：
- 文件被其他程序占用
- 文件不存在或已删除
- 文件匹配排除规则

**解决方案**：

1. 查看日志了解具体跳过的文件
   ```
   日志位置：~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log
   ```

2. 如果是正常占用（如正在写入的日志），无需处理

3. 如果需要备份被跳过的文件，检查排除规则配置

### Q: 备份速度很慢

**可能原因**：
- 备份文件数量多
- 文件体积大
- 磁盘性能低

**优化方案**：

1. 使用选择性备份，减少备份目标
   ```
   /backup_config
   设置 mode: "partial"
   ```

2. 增加排除规则
   ```json
   "exclude": ["logs", "cache", "tmp", "node_modules", "dist", "build"]
   ```

3. 使用更快的存储介质（如 SSD）

---

## 定时任务问题

### Q: 定时备份没有执行

**排查步骤**：

1. 检查定时任务是否启用
   ```
   /backup_status
   查看 "定时备份" 状态
   ```

2. 检查 cron 表达式是否正确
   ```
   /backup_config
   查看 schedule.cron 配置
   ```

3. 检查 HEARTBEAT 是否配置
   ```
   查看：~/.openclaw/HEARTBEAT.md
   ```

4. 查看 lastRun 时间
   ```
   /backup_status
   查看 "上次执行" 时间
   ```

### Q: 想要修改备份时间

**解决方案**：

1. 运行配置命令
   ```
   /backup_config
   ```

2. 修改 cron 表达式
   ```
   凌晨 2 点：0 2 * * *
   凌晨 4 点：0 4 * * *
   中午 12 点：0 12 * * *
   ```

---

## 通知问题

### Q: 没有收到通知

**排查步骤**：

1. 检查通知是否启用
   ```
   /backup_status
   查看 "通知渠道"
   ```

2. 检查 OpenClaw 渠道配置
   ```
   OpenClaw 需要先配置飞书/Telegram 等渠道
   配置文件：~/.openclaw/openclaw.json
   ```

3. 检查通知配置
   ```json
   "notification": {
     "enabled": true,
     "channels": ["feishu"],
     "targets": {
       "feishu": [
         { "type": "group", "id": "oc_xxx", "name": "群名" }
       ]
     },
     "onSuccess": true,
     "onFailure": true
   }
   ```

4. 检查是否配置了推送目标
   - 运行 `/backup_config` 进入交互式配置
   - 在 Step 5 选择通知渠道后，确保选择了具体的推送目标

### Q: 提示"渠道未配置"或"推送失败"

**原因**：
- OpenClaw 中未启用对应渠道
- 推送目标 ID 不正确
- 渠道配置不完整

**解决方案**：

1. 检查 OpenClaw 配置
   ```
   查看 ~/.openclaw/openclaw.json 中的 channels 部分
   确保对应渠道 enabled: true
   ```

2. 重新配置推送目标
   ```
   /backup_config
   选择 [1] 交互式配置
   按步骤选择正确的推送目标
   ```

3. 手动添加推送目标
   ```json
   "notification": {
     "targets": {
       "feishu": [
         { "type": "group", "id": "oc_你的群ID", "name": "群名称" }
       ]
     }
   }
   ```

### Q: 如何获取群组 ID 或用户 ID？

**飞书群组 ID**：
1. 在飞书群聊中，点击群设置
2. 查看群信息，找到群 ID（格式：`oc_xxx`）

**飞书用户 ID**：
1. 在飞书中查看用户资料
2. 找到 Open ID（格式：`ou_xxx`）

**Telegram 群组 ID**：
1. 将 @userinfobot 添加到群组
2. 它会返回群组 ID（格式：`-100xxx`）

### Q: 想要关闭通知

**解决方案**：

修改配置文件：
```json
"notification": {
  "enabled": false
}
```

或运行：
```
/backup_config
选择 [1] 交互式配置
在通知渠道步骤不选择任何渠道
```

---

## 配置问题

### Q: 配置文件格式错误

**症状**：提示配置文件 JSON 格式无效。

**解决方案**：

1. 使用 JSON 验证工具检查格式
   - 确保 JSON 中字符串使用双引号
   - 确保最后一项后没有多余的逗号
   - 确保括号配对正确

2. 重置配置
   ```
   /backup_config
   选择 [3] 重置为默认配置
   ```

### Q: 工作空间targets为空或不正确（v1.1.0新增）

**症状**：首次配置后targets为空或缺少某些workspace。

**原因**：v1.1.0版本新增工作空间动态检测功能，首次配置时会自动检测~/.openclaw/目录中的所有workspace-*目录和memory目录。

**解决方案**：

1. 检查检测结果
   ```
   /backup_config
   选择 [4] 查看当前配置
   查看 backup.targets 字段
   ```

2. 手动调整targets
   ```json
   {
     "backup": {
       "targets": ["workspace", "workspace-01", "workspace-02", "memory"]
     }
   }
   ```

3. 使用交互式配置确认
   ```
   /backup_config
   选择 [1] 交互式配置
   Step 1.1 会列出实际存在的workspace供选择
   ```

### Q: 敏感文件是否应该启用排除？（v1.1.0新增）

**症状**：不确定是否需要启用敏感文件排除功能。

**说明**：
- **默认行为**：系统默认不启用敏感文件排除，仅排除临时文件（logs、cache、tmp等）
- **建议**：根据实际需求自主选择是否启用

**决策建议**：
- ✅ **启用排除**：如果备份可能泄露给他人，建议启用，保护敏感数据
- ⚠️ **不启用**：如果备份仅自己使用且妥善保管，可不启用，完整备份所有数据

**如何启用**：
```
/backup_config
选择 [1] 交互式配置
Step 7: 敏感文件排除配置
选择 [1] 启用排除
```

**手动配置**：
```json
{
  "backup": {
    "enableSensitiveExclude": true,
    "excludePatterns": [
      "*.log", "*.tmp", ".DS_Store", "Thumbs.db",
      "*.key", "*.pem", "*.p12", "*.pfx",
      ".env", ".env.local", "credentials.json", "secrets.json"
    ],
    "exclude": ["logs", "cache", "tmp", "node_modules", ".ssh", ".gnupg"]
  }
}
```

### Q: 想要修改配置但不知道格式

**解决方案**：

1. 查看当前配置
   ```
   /backup_config
   选择 [4] 查看当前配置
   ```

2. 查看配置字段说明
   ```
   参考：references/config-schema.md
   ```

---

## 日志查看

### 日志位置

```
~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log
```

### 查看方法

**Linux/macOS**：
```bash
# 查看最新 100 行
tail -100 ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log

# 实时查看
tail -f ~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backup.log
```

**Windows (PowerShell)**：
```powershell
# 查看最新 100 行
Get-Content "$env:USERPROFILE\.openclaw\workspace\Auto-Backup-Openclaw-User-Data\backup.log" -Tail 100

# 实时查看
Get-Content "$env:USERPROFILE\.openclaw\workspace\Auto-Backup-Openclaw-User-Data\backup.log" -Wait
```

### 日志级别

```
[DEBUG] 调试信息（默认不显示）
[INFO]  一般信息
[WARN]  警告信息
[ERROR] 错误信息
```

### 日志示例

```
[2026-03-26 15:30:00.123] [INFO]  [Backup] 开始执行备份任务
[2026-03-26 15:30:00.456] [INFO]  [Backup] 备份目标: 1 个目录
[2026-03-26 15:30:01.789] [INFO]  [Backup] 共收集到 1234 个文件
[2026-03-26 15:30:15.345] [INFO]  [Compressor] 压缩完成: auto-backup-...zip (125.6 MB)
[2026-03-26 15:30:15.678] [INFO]  [Backup] 备份完成！耗时: 15555ms
```

---

## 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|----------|------|----------|
| `ENOENT` | 文件或目录不存在 | 检查路径是否正确 |
| `EACCES` | 权限不足 | 检查文件权限 |
| `ENOSPC` | 磁盘空间不足 | 清理磁盘或更换路径 |
| `EBUSY` | 文件被占用 | 关闭占用文件的程序 |
| `EMFILE` | 打开文件过多 | 减少备份文件数量 |

---

## 获取帮助

如果以上方法无法解决问题：

1. 查看完整日志文件
2. 在 GitHub 提交 Issue
3. 联系作者：jack698698@gmail.com

---

**文档版本**：v1.1.0  
**更新日期**：2026-04-14  
**作者**：水木开发团队-Jack·Huang