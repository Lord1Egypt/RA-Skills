# audit-exec - Exec 命令审计技能

审计 OpenClaw 执行的所有 exec 命令，识别高风险操作，白名单过滤后生成报告。

## 使用方法

```
执行审计
```

或者手动运行：
```bash
python C:\Users\zhengzhicheng\.openclaw\workspace\skills\audit-exec\audit_transcript.py
```

## 功能说明

### 1. 审计范围
- 解析 transcript JSONL 文件获取完整 exec 命令记录
- 支持自定义天数范围（默认最近 1 天）
- 搜索所有会话的 transcript

### 2. 风险识别规则

#### 🔴 高风险 (Red Line) - 命中直接标红
| 风险类型 | Linux | Windows |
|---------|-------|---------|
| 级联删除 | `rm -rf`、`find -delete` | `del /s /q`、`Remove-Item -Recurse -Force` |
| 防火墙 | iptables、ufw | `netsh advfirewall`、`Set-NetFirewallRule` |
| 注册表 | 修改 /etc/* | `reg add`、`reg delete` |
| 启动项 | cron、rc.local | `bcdedit`、`schtasks /create` |
| 密钥泄露 | 读取私钥/API Key 文件 | 同左 |

#### 🟡 中风险 (Yellow Line) - 标黄记录
| 风险类型 | Linux | Windows |
|---------|-------|---------|
| 提权执行 | sudo | runas、Start-Process -Verb RunAs |
| 外部下载 | curl、wget | Invoke-WebRequest、iwr、bitsadmin |
| 安装软件 | apt/pip/npm install -g | choco install、winget install、pip install |

### 3. 白名单管理
- 白名单文件：`skills/audit-exec/whitelist.txt`
- 每行一个规则，格式：`pattern -> 说明`
- `#` 开头 = 注释

## 文件结构

```
skills/audit-exec/
├── SKILL.md              # 本说明文件
├── whitelist.txt         # 白名单配置
└── audit_transcript.py   # 审计脚本
```

## 报告示例

```
==================================================
       [Exec Command Audit Report]
==================================================
Date: 2026-03-20
Platform: Windows / Linux
Scope: Last 1 day

Total: 30 exec commands
  [HIGH] High Risk: 0
  [MEDIUM] Medium Risk: 1
  [LOW] Low Risk: 8
  [OK] Whitelisted: 21

--------------------------------------------------
[MEDIUM] Medium Risk Commands - Logged
--------------------------------------------------
[00:54:41] pip install python-pptx -q
    Reason: Python 包安装

--------------------------------------------------
[OK] Whitelisted (21 commands)
--------------------------------------------------
[00:55:28] python analyze_ppt.py
    Whitelist: PPT分析脚本，安全

==================================================
审计完成
==================================================
```

## 白名单格式说明

```
# 格式: pattern -> 说明
# 以 # 开头的是注释

# Python 脚本
email-check.py -> 邮件检查脚本，安全
analyze_ppt*.py -> PPT分析脚本，安全

# 系统命令
Get-ChildItem -> 目录查看，安全
Get-Content -> 读取文件内容，安全
```

## 注意事项

1. **Transcript 路径**：脚本自动查找最新的 transcript 文件
2. **编码问题**：Windows GBK 编码下 emoji 可能显示乱码，但不影响功能
3. **白名单匹配**：使用正则表达式匹配，支持模糊匹配
