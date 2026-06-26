# 配置字段说明

本文档详细说明 `Auto-Backup-Openclaw-User-Data` 技能的所有配置字段。

---

## 配置文件位置

```
~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/config.json
```

---

## 配置结构

```json
{
  "version": "1.1.0",
  "createdAt": "2026-04-14T15:00:00+08:00",
  "updatedAt": "2026-04-14T15:00:00+08:00",

  "backup": { ... },
  "schedule": { ... },
  "output": { ... },
  "retention": { ... },
  "notification": { ... },
  "logging": { ... }
}
```

---

## 字段说明

### 顶层字段

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `version` | string | 是 | "1.1.0" | 配置文件版本 |
| `createdAt` | string | 否 | - | 创建时间（ISO 8601） |
| `updatedAt` | string | 否 | - | 最后更新时间（ISO 8601） |

---

### backup 备份配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `mode` | string | 是 | "full" | 备份模式：`full`（全量）或 `partial`（选择性） |
| `targets` | array | 否 | [...] | 选择性备份时的目标目录列表 |
| `exclude` | array | 否 | [...] | 排除的目录名列表 |
| `excludePatterns` | array | 否 | [...] | 排除的文件名模式（支持通配符） |
| `sensitiveExcludeSuggestion` | array | 否 | [...] | 敏感文件建议排除列表 |
| `sensitiveExcludeDirectories` | array | 否 | [...] | 敏感目录建议排除列表 |
| `enableSensitiveExclude` | boolean | 否 | false | 是否启用敏感文件排除 |

#### mode 备份模式

- `full`：全量备份 `.openclaw` 目录
- `partial`：选择性备份，只备份 `targets` 中指定的目录

#### targets 备份目标

仅在 `mode: "partial"` 时生效，可用的目标目录：

```
workspace       # 主工作空间
workspace-1     # 1工作空间
workspace-2     # 2工作空间
workspace-3     # 3工作空间
memory          # 记忆文件
```

#### exclude 排除目录

默认排除的目录：

```
logs               # 日志目录
cache              # 缓存目录
tmp                # 临时目录
node_modules       # Node.js 依赖
```

#### excludePatterns 排除模式

支持通配符：

```
*.log              # 所有 .log 文件
*.tmp              # 所有 .tmp 文件
.DS_Store          # macOS 系统文件
Thumbs.db          # Windows 缩略图缓存
```

#### sensitiveExcludeSuggestion 敏感文件建议列表

默认敏感文件模式（仅在启用时生效）：

```
*.key              # 密钥文件
*.pem              # PEM证书文件
*.p12              # PKCS#12证书
*.pfx              # PFX证书
.env               # 环境变量文件
.env.local         # 本地环境变量
.env.*.local       # 环境变量文件变体
credentials.json   # 凭证文件
secrets.json       # 密钥文件
*.token            # Token文件
*.secret           # 密钥文件
*_token.json       # Token JSON文件
id_rsa             # SSH私钥
id_dsa             # DSA私钥
*.ppk              # PuTTY私钥
```

#### sensitiveExcludeDirectories 敏感目录建议列表

默认敏感目录（仅在启用时生效）：

```
credentials        # 凭证目录
secrets            # 密钥目录
.ssh               # SSH配置目录
.gnupg             # GPG配置目录
```

#### enableSensitiveExclude 启用敏感文件排除

- `true`：启用敏感文件排除（将建议列表合并到exclude中）
- `false`：不启用敏感文件排除（默认值）

**注意**：启用后，`sensitiveExcludeSuggestion` 和 `sensitiveExcludeDirectories` 中的内容将被添加到 `exclude` 和 `excludePatterns` 中。

---

### schedule 定时配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | 是 | true | 是否启用定时备份 |
| `cron` | string | 是 | "0 3 * * *" | cron 表达式 |
| `timezone` | string | 否 | "Asia/Shanghai" | 时区 |
| `lastRun` | string | 否 | null | 上次执行时间 |

#### cron 表达式格式

```
分钟 小时 日期 月份 星期
  *    *    *    *    *

示例：
"0 3 * * *"      # 每天凌晨 3:00
"0 4 * * *"      # 每天凌晨 4:00
"0 3 * * 0"      # 每周日凌晨 3:00
"0 3 1 * *"      # 每月 1 日凌晨 3:00
"*/30 * * * *"   # 每 30 分钟
```

---

### output 输出配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `path` | string | 是 | ... | 备份文件存储路径 |
| `naming` | object | 否 | {...} | 命名规则 |
| `encryption` | object | 否 | {...} | 加密配置 |

#### naming 命名规则

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `prefix` | string | "auto-backup-openclaw-user-data" | 文件名前缀 |
| `includeVersion` | boolean | true | 是否包含 OpenClaw 版本号 |
| `includeSequence` | boolean | true | 是否包含当日序号 |

#### 命名格式

```
{prefix}_{YYYYMMDD}_{HHMM}_{version}_{序号}.zip

示例：
auto-backup-openclaw-user-data_20260326_0300_v2026.3.23-2_01.zip
```

#### encryption 加密配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | 否 | false | 是否启用加密 |
| `password` | string | 否 | null | 加密密码（启用时必填） |
| `algorithm` | string | 否 | "aes-256" | 加密算法（默认AES-256） |
| `reminderShown` | boolean | 否 | false | 是否已显示密码提醒 |

**加密说明**：
- 使用AES-256加密算法保护备份文件
- 密码存储在配置文件中，请妥善保管配置文件
- 建议将密码备份到密码管理器或其他安全位置

**密码设置方式**：
1. **自定义密码**：用户输入密码（至少8位）
2. **随机密码**：系统生成16位随机密码

**解密兼容性**：
- ✅ 支持：7-Zip, WinRAR, PeaZip
- ❌ 不支持：macOS Finder原生解压, Windows资源管理器原生解压

**风险提示**：
- 密码丢失将无法解密备份文件
- 配置文件损坏或丢失将无法找回密码
- 建议备份密码到安全位置

---

### retention 保留策略配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | 是 | true | 是否启用保留策略 |
| `mode` | string | 是 | "count" | 清理模式：`days` 或 `count` |
| `days` | number | 否 | 30 | 保留天数（mode=days 时） |
| `count` | number | 否 | 10 | 保留份数（mode=count 时） |

#### mode 清理模式

- `days`：按天数清理，保留最近 N 天的备份
- `count`：按份数清理，保留最近 N 份备份

---

### notification 通知配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | 是 | true | 是否启用通知 |
| `channels` | array | 是 | ["feishu"] | 通知渠道列表 |
| `targets` | object | 否 | {} | 推送目标配置 |
| `onSuccess` | boolean | 否 | true | 备份成功时发送通知 |
| `onFailure` | boolean | 否 | true | 备份失败时发送通知 |

#### channels 可用渠道

```
feishu       # 飞书
telegram     # Telegram
discord      # Discord
slack        # Slack
```

**注意**：需要先在 OpenClaw 中配置相应的渠道。

#### targets 推送目标配置

`targets` 字段用于指定每个渠道的具体推送目标（用户或群组）：

```json
{
  "targets": {
    "feishu": [
      { "type": "group", "id": "oc_xxx", "name": "开发群" },
      { "type": "user", "id": "ou_xxx", "name": "主人" }
    ],
    "telegram": [
      { "type": "group", "id": "-100xxx", "name": "通知群" },
      { "type": "user", "id": "123456789", "name": "用户名" }
    ]
  }
}
```

**字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | string | 目标类型：`group`（群组）或 `user`（用户） |
| `id` | string | 目标 ID（飞书群组为 `oc_xxx`，用户为 `ou_xxx`） |
| `name` | string | 目标名称（用于显示，可选） |

**如何获取推送目标**：

1. 运行 `/backup_config` 进入交互式配置
2. 选择通知渠道后，系统会自动列出可用的推送目标
3. 从列表中选择需要的目标

**注意事项**：
- 如果未配置 `targets`，系统会尝试通过当前对话发送通知
- 推送目标来自 `~/.openclaw/openclaw.json` 中的 `bindings` 配置
- 群组 ID 需要是完整的 ID（如 `oc_xxx`），不能是群名称

---

### logging 日志配置

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `enabled` | boolean | 是 | true | 是否启用日志 |
| `level` | string | 否 | "info" | 日志级别 |
| `maxSize` | string | 否 | "10MB" | 单个日志文件最大大小 |
| `maxFiles` | number | 否 | 5 | 保留的日志文件数量 |

#### level 日志级别

```
DEBUG    # 调试信息
INFO     # 一般信息
WARN     # 警告信息
ERROR    # 错误信息
```

---

## 配置示例

### 最小配置

```json
{
  "version": "1.1.0",
  "backup": {
    "mode": "partial"
  },
  "schedule": {
    "enabled": true,
    "cron": "0 3 * * *"
  },
  "output": {
    "path": "~/.openclaw/workspace/Auto-Backup-Openclaw-User-Data/backups"
  },
  "retention": {
    "enabled": true,
    "mode": "count",
    "count": 10
  },
  "notification": {
    "enabled": true,
    "channels": ["feishu"]
  },
  "logging": {
    "enabled": true
  }
}
```

### 完整配置

```json
{
  "version": "1.1.0",
  "createdAt": "2026-04-14T15:00:00+08:00",
  "updatedAt": "2026-04-14T15:00:00+08:00",

  "backup": {
    "mode": "partial",
    "targets": [],  // ← 改为空数组，首次加载时动态检测
    "exclude": ["logs", "cache", "tmp", "node_modules"],
    "excludePatterns": ["*.log", "*.tmp", ".DS_Store", "Thumbs.db"],

    // 敏感文件排除建议列表（默认不启用）
    "sensitiveExcludeSuggestion": [
      "*.key", "*.pem", "*.p12", "*.pfx",
      ".env", ".env.local", ".env.*.local",
      "credentials.json", "secrets.json",
      "*.token", "*.secret", "*_token.json",
      "id_rsa", "id_dsa", "*.ppk"
    ],
    "sensitiveExcludeDirectories": [
      "credentials", "secrets", ".ssh", ".gnupg"
    ],
    "enableSensitiveExclude": false
  },
  
  "schedule": {
    "enabled": true,
    "cron": "0 3 * * *",
    "timezone": "Asia/Shanghai",
    "lastRun": null
  },
  
  "output": {
    "path": "D:/Backups/openclaw",
    "naming": {
      "prefix": "auto-backup-openclaw-user-data",
      "includeVersion": true,
      "includeSequence": true
    },
    "encryption": {
      "enabled": false,
      "password": null,
      "algorithm": "aes-256",
      "reminderShown": false
    }
  },
  
  "retention": {
    "enabled": true,
    "mode": "days",
    "days": 30,
    "count": 10
  },
  
  "notification": {
    "enabled": true,
    "channels": ["feishu", "telegram"],
    "targets": {
      "feishu": [
        { "type": "group", "id": "oc_xxx", "name": "开发群" }
      ],
      "telegram": [
        { "type": "group", "id": "-100xxx", "name": "通知群" }
      ]
    },
    "onSuccess": true,
    "onFailure": true
  },
  
  "logging": {
    "enabled": true,
    "level": "info",
    "maxSize": "10MB",
    "maxFiles": 5
  }
}
```

---

## 配置验证

修改配置后，运行以下命令验证：

```
/backup_config
选择 [4] 查看当前配置
```

如果配置格式错误，系统会自动使用默认配置并提示错误信息。

---

## 获取帮助

如果以上方法无法解决问题：

1. 查看完整日志文件
2. 在 GitHub 提交 Issue
3. 联系作者：jack698698@gmail.com

---

**文档版本**：v1.1.0.20260414
**更新日期**：2026-04-14
**作者**：水木开发团队-Jack·Huang