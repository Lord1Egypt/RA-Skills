---
name: continuous-openclaw-config-guard
description: OpenClaw configuration rollback guardian with automatic backup and recovery. Monitors openclaw.json for changes, creates backups before modifications, restarts the gateway, and automatically rolls back if no message activity is detected within a configurable timeout (default 5 minutes). Provides safety net for risky configuration changes, gateway configuration testing, or any edits to openclaw.json that might break the system. Use when: (1) Editing openclaw.json and want automatic rollback protection, (2) Testing new gateway configurations safely, (3) Need automatic backup before config changes, (4) Want peace of mind when modifying OpenClaw settings.

---

# OpenClaw 配置回滚守护

**适用且测试过linux系统。**

## 功能

1. **监控配置文件** - 持续监控 `~/.openclaw/openclaw.json`
2. **自动备份** - 配置修改前自动创建备份
3. **自动重启网关** - 配置修改后自动重启网关
4. **消息验证** - 一段时间内未收到消息则自动回滚
5. **自动恢复** - 回滚后自动重启网关

## 文件结构

```
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/
├── scripts/
    ├── guard.sh                          # 守护脚本（核心）
    └── continuous-openclaw-config-guard.service.txt     # systemd 服务文件
├── SKILL.md                         # 本说明文件
├── guard.log                         # 运行日志
├── guard.pid                         # 进程ID文件
└── backups/                          # 备份目录
    ├── openclaw.json.20250310160000
    ├── openclaw.json.20250310160500
    └── openclaw.json.rollback.20250310161000
```

## 环境变量

可以通过环境变量自定义配置。

### 必须修改的变量

| 变量           | 默认值                                                  | 说明         | 为什么需要修改                                               |
| -------------- | ------------------------------------------------------- | ------------ | ------------------------------------------------------------ |
| `SESSION_FILE` | `~/.openclaw/agents/huoxiaoxing/sessions/sessions.json` | 会话文件路径 | **必须修改！** 默认值中的 `huoxiaoxing` 是开发者的 agent 名称，其他用户需要改成自己的 agent 名称才能正确检测消息活动 |

### 通常不需要修改的变量

如果你的 OpenClaw 安装路径或者agent的工作空间不同，需要修改以下变量。

| 变量             | 默认值                                                       | 说明                |
| ---------------- | ------------------------------------------------------------ | ------------------- |
| `CONFIG_FILE`    | `~/.openclaw/openclaw.json`                                  | 要监控的配置文件    |
| `BACKUP_DIR`     | `~/.openclaw/workspace/skills/continuous-openclaw-config-guard/backups` | 备份存放目录        |
| `LOG_FILE`       | `~/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.log` | 日志文件路径        |
| `PID_FILE`       | `~/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.pid` | PID文件路径         |
| `OPENCLAW_BIN`   | `~/.npm-global/bin/openclaw`                                 | OpenClaw 可执行文件 |
| `WAIT_TIME`      | `300`                                                        | 等待验证时间（秒）  |
| `CHECK_INTERVAL` | `10`                                                         | 检查间隔（秒）      |

### 使用环境变量示例

```bash
# 修改 SESSION_FILE（必须！）
SESSION_FILE=~/.openclaw/agents/your-agent-name/sessions/sessions.json ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s

# 监控不同的配置文件
CONFIG_FILE=/path/to/custom.json ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s

# 自定义等待时间（600秒=10分钟）
WAIT_TIME=600 ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s

# 修改 OpenClaw 命令路径（如果安装位置不同）
OPENCLAW_BIN=/path/to/your/openclaw.bash ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s

# 组合使用
SESSION_FILE=~/.openclaw/agents/your-agent/sessions/sessions.json WAIT_TIME=600 ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s
```

## 使用方法

### 方式一：systemd 服务（推荐）

作为系统服务运行，开机自启，崩溃自动重启。**systemd 只管理守护进程的启动/停止，其他操作（回滚、列备份等）直接用手动命令。**

#### 修改服务文件

**使用前必须修改** `continuous-openclaw-config-guard.service.txt` 中的以下内容：

1. **ExecStart/ExecStop 路径** - 改为你的实际安装路径
2. **User** - 改为你的用户名
3. **WorkingDirectory** - 改为你的实际安装路径
4. **环境变量** - 特别是 `SESSION_FILE` 中的 agent 名称

```ini
[Service]
ExecStart=/你的/实际/路径/scripts/guard.sh -s
ExecStop=/你的/实际/路径/scripts/guard.sh -k
User=你的用户名
WorkingDirectory=/你的/实际/路径
Environment="SESSION_FILE=/home/你的用户名/.openclaw/agents/你的agent名/sessions/sessions.json"
```

#### 安装服务

```bash
# 1.添加脚本执行权限
chmod +x ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh

# 2. 先编辑服务文件，修改上述内容
nano ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/continuous-openclaw-config-guard.service.txt

# 3. 复制服务文件到 systemd 目录
sudo cp ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/continuous-openclaw-config-guard.service.txt /etc/systemd/system/continuous-openclaw-config-guard.service

# 4. 重新加载 systemd
sudo systemctl daemon-reload

# 5. 启动服务
sudo systemctl start continuous-openclaw-config-guard

# 6. 查看状态
sudo systemctl status continuous-openclaw-config-guard

# 7. 开机自启（可选）
sudo systemctl enable continuous-openclaw-config-guard
```

#### 管理服务（仅启动/停止/重启）

```bash
# 启动守护进程
sudo systemctl start continuous-openclaw-config-guard

# 停止守护进程
sudo systemctl stop continuous-openclaw-config-guard

# 重启守护进程
sudo systemctl restart continuous-openclaw-config-guard

# 查看日志
sudo journalctl -u continuous-openclaw-config-guard -f

# 查看所有日志
sudo journalctl -u continuous-openclaw-config-guard
```

#### 其他操作（直接用手动命令）

即使使用 systemd，以下命令仍然可以直接使用：

```bash
# 立即回滚到最新备份并重启网关
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -r

# 列出所有备份（带备注）
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -l

# 查看帮助
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -h
```

### 方式二：手动运行

适合临时测试或不使用 systemd 的系统。所有操作都通过脚本命令完成。

#### 启动守护（后台运行）

```bash
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s
```

#### 启动守护，自定义等待时间（10分钟）

```bash
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -s -w 600
```

#### 停止守护

```bash
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -k
```

#### 立即回滚到最新备份并重启网关

```bash
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -r
```

#### 列出所有备份（带备注）

```bash
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -l
```

#### 查看帮助

```bash
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -h
```

## 完整工作流程

```
1. 守护进程启动
           ↓
2. 创建初始备份（若无备份）
           ↓
3. 持续监控 openclaw.json 修改时间
           ↓ 检测到修改
4. 重启网关
           ↓
    ┌──────┴──────┐
    │ 重启成功？   │
    ├──────┬──────┤
    │ 是   │  否  │
    ↓      ↓      │
5. 开始计时   6. 立即回滚 ←┘
   等待消息验证   并重启网关
   （WAIT_TIME）    ↓
    ↓               └─────┐
    ┌──────┴──────┐       │
    │             │       │
 收到消息       超时       │
    │             │       │
验证成功      验证失败     │
    │             │       │
创建新备份    回滚配置     │
（作为新基准） 并重启网关   │
    ↓             ↓       │
    └─────┬───────┘       │
          ↓               │
    返回步骤3，继续监控────┘
```

## 备份说明

- **备份时机**：守护进程启动时创建初始备份，配置被修改且验证成功后自动备份
- **备份内容**：成功运行的配置文件
- **备份命名**：`openclaw.json.YYYYMMDDHHMMSS`
- **回滚记录**：回滚时会保存当前配置为 `openclaw.json.rollback.YYYYMMDDHHMMSS`

## 日志查看

### systemd 方式（推荐）

```bash
# 实时查看日志
sudo journalctl -u continuous-openclaw-config-guard -f

# 查看最近100行
sudo journalctl -u continuous-openclaw-config-guard -n 100

# 查看今天所有日志
sudo journalctl -u continuous-openclaw-config-guard --since today

# 查看完整日志
sudo journalctl -u continuous-openclaw-config-guard
```

### 手动运行方式

```bash
# 实时查看日志
tail -f ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.log

# 查看最近100行
tail -100 ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.log

# 搜索关键词
grep "回滚" ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.log
```

## 注意事项

- 首次启动会自动创建初始备份
- 每次成功验证后会创建新的基准备份
- **回滚时会自动重启网关**，无需手动操作
- 使用 systemd 时，日志由 journald 管理；手动运行时，日志写入 `guard.log`
- **修改环境变量后，需要重启服务生效**：`sudo systemctl restart continuous-openclaw-config-guard`
- **SESSION_FILE 必须正确设置**，否则无法检测消息活动，会导致配置修改后总是回滚

## 故障排查

### 服务无法启动

```bash
# 查看详细错误信息
sudo systemctl status continuous-openclaw-config-guard

# 查看启动日志
sudo journalctl -u continuous-openclaw-config-guard -n 50
```

### 检查脚本权限

```bash
chmod +x ~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh
```

### 手动测试脚本

```bash
# 先手动运行测试，确认脚本正常
~/.openclaw/workspace/skills/continuous-openclaw-config-guard/scripts/guard.sh -h
```

### 无法顺利执行

仔细检查scripts文件夹下guard.sh和continuous-openclaw-config-guard.service.txt的各个参数特别是环境变量，确保配置与你的实际环境一致。

