# Clash Auto Switch

> 自动切换 Clash 代理节点的脚本工具，支持 Linux / macOS / Windows 和 OpenClaw Skill

[English](./README.md) | [中文](./README_zh.md)

## 功能

- ✅ 健康检查：测试当前代理连通性
- ✅ 自动切换：检测到故障时自动切换到最佳节点
- ✅ 区域优先：优先选择新加坡/日本/香港/美国节点
- ✅ 手动切换：支持切换到指定节点或区域
- ✅ OpenClaw Skill：支持在 OpenClaw 中直接调用

## 支持平台

| 平台 | 脚本 | 说明 |
|------|------|------|
| 🐧 Linux / macOS | `clash-switch.sh` | Bash 脚本 |
| 🐧 Linux / macOS | `clash-switch-v2.sh` | 增强版 (日志+状态) |
| 🪟 Windows | `clash-switch.ps1` | PowerShell 脚本 |
| 🌐 跨平台 | `clash-switch.py` | Python 脚本 (推荐) |
| 🤖 OpenClaw | Skill | `/clash` 命令 |

## 快速开始

### Python (推荐，跨平台)

```bash
# 安装依赖
pip install requests

# 设置环境变量
export CLASH_API="http://127.0.0.1:58871"
export CLASH_SECRET="your-secret"

# 列出代理组
python clash-switch.py --list

# 健康检查
python clash-switch.py --health

# 自动切换
python clash-switch.py --auto
```

### OpenClaw Skill

```bash
/clash health    # 健康检查
/clash list     # 列出节点
/clash auto     # 自动切换
/clash status   # 查看状态
/clash sg       # 切换到新加坡
```

## 安装

### OpenClaw Skill

```bash
npx clawdhub install clash-auto-switch
```

### 手动安装

```bash
# Clone 仓库
git clone https://github.com/adminlove520/clash-auto-switch.git
cd clash-auto-switch

# 使用 Python 版本
pip install requests
python clash-switch.py --help
```

## 配置

### 环境变量

| 变量 | 默认值 | 说明 |
|------|---------|------|
| `CLASH_API` | `http://127.0.0.1:58871` | Clash API 地址 |
| `CLASH_SECRET` | - | API 密钥 (必填) |
| `CLASH_PROXY` | `http://127.0.0.1:7890` | 代理地址 |

### 配置文件

复制 `config.example.sh` 为 `config.sh` 并修改：

```bash
CLASH_API="http://127.0.0.1:58871"
CLASH_SECRET="your-secret"
```

## 使用方法

### Python 版本

```bash
# 列出所有代理组
python clash-switch.py --list

# 健康检查
python clash-switch.py --health

# 自动切换到最佳节点
python clash-switch.py --auto

# 查看状态
python clash-switch.py --status

# 切换到指定节点
python clash-switch.py --switch ChatGPT "新加坡-优化-Gemini-GPT"

# 区域快速切换
python clash-switch.py --sg    # 新加坡
python clash-switch.py --us    # 美国
python clash-switch.py --jp    # 日本
python clash-switch.py --hk    # 香港
```

### OpenClaw Skill

```
/clash health    # 健康检查
/clash list     # 列出节点
/clash auto     # 自动切换
/clash status   # 查看状态
/clash sg       # 切换到新加坡
/clash us       # 切换到美国
```

### Bash 版本 (Linux/macOS)

```bash
chmod +x clash-switch.sh

./clash-switch.sh check    # 健康检查
./clash-switch.sh auto    # 自动切换
./clash-switch.sh list   # 列出节点
```

### PowerShell 版本 (Windows)

```powershell
.\clash-switch.ps1 check   # 健康检查
.\clash-switch.ps1 auto    # 自动切换
.\clash-switch.ps1 list    # 列出节点
```

## 定时任务

### Linux crontab

```bash
# 每 15 分钟检查一次
*/15 * * * * /path/to/clash-switch.sh auto >> /var/log/clash-switch.log 2>&1
```

### Windows 计划任务

```powershell
Register-ScheduledTask -TaskName "ClashAutoSwitch" -Trigger (New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)) -Action (New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\path\to\clash-switch.py --auto") -RunLevel Highest
```

### OpenClaw Cron

```json
{
  "name": "clash-health-check",
  "schedule": {
    "kind": "every",
    "everyMs": 900000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "/clash auto"
  },
  "sessionTarget": "isolated"
}
```

## 支持的代理组

- ChatGPT
- Copilot
- GLOBAL
- Netflix
- Steam
- Telegram
- TikTok
- Twitter
- WhatsApp
- 境内使用
- 海外使用
- 节点选择
- 谷歌服务
- 微软服务
- 苹果服务

## 自动切换逻辑

1. 检查当前代理健康状态（测试 Telegram/Google/Anthropic）
2. 如果不健康，遍历所有节点
3. 测试每个节点的延迟
4. 优先选择优先区域的节点（日本/新加坡/香港/美国）
5. 切换到最佳节点
6. 重新检查健康状态

## 项目结构

```
clash-auto-switch/
├── clash-switch.sh        # Bash 原版
├── clash-switch-v2.sh    # Bash 增强版
├── clash-switch.ps1      # PowerShell 版
├── clash-switch.py      # Python 跨平台版 (推荐)
├── config.example.sh     # 配置示例
├── SKILL.md             # OpenClaw Skill 文档
├── skills/
│   └── clash-auto-switch/
│       ├── SKILL.md
│       ├── clash.py
│       └── requirements.txt
├── README.md            # English
├── README_zh.md        # 中文
└── CHANGELOG.md        # 更新日志
```

## License

MIT

## 作者

- GitHub: [@adminlove520](https://github.com/adminlove520)

## 更新日志

See [CHANGELOG.md](./CHANGELOG.md)

## 文档

- [OpenClaw Skill 安装指南](./docs/openclaw.md) - 详细的 OpenClaw 安装配置
- [原始 README](./README.md)
