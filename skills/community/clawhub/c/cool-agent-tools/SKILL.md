---
name: agent-tools
description: AI Agent 通用工具集 - 提供系统监控、日志分析、进程管理、文件处理、网络诊断等实用命令封装，帮助 agent 高效完成日常运维和数据处理任务。
metadata:
  {
    openclaw: {
      version: "1.0.0",
      author: "CooL神",
      tags: ["tools", "agent", "system", "utility"]
    }
  }
---

# agent-tools

AI Agent 通用工具集，让 CooL神 拥有瑞士军刀般的实用能力。

## 工具清单

### 🔍 系统监控

| 命令 | 说明 |
|------|------|
| `top` | 查看系统进程/资源占用 |
| `htop` | 交互式进程查看（需安装） |
| `df -h` | 磁盘空间使用情况 |
| `du -sh *` | 当前目录各文件夹大小 |
| `free -h` | 内存使用情况 |
| `uptime` | 系统运行时间和负载 |

### 🌐 网络诊断

| 命令 | 说明 |
|------|------|
| `curl -I <url>` | 检查 URL 可达性（只取 header） |
| `ping -c 4 <host>` | 测试网络连通性 |
| `nslookup <domain>` | DNS 解析查询 |
| `netstat -tuln` | 查看监听端口 |
| `ifconfig / ip addr` | 查看网络接口 |

### 📁 文件处理

| 命令 | 说明 |
|------|------|
| `find . -name "*.log" -mtime -7` | 7天内修改过的日志文件 |
| `find . -size +100M` | 查找大于 100MB 的文件 |
| `ls -laSh` | 按大小排序显示文件 |
| `wc -l <file>` | 统计文件行数 |
| `grep -r "error" ./logs/` | 递归搜索日志中的错误 |
| `tail -f <file>` | 实时跟踪文件变化 |
| `tar -czvf archive.tar.gz ./dir/` | 压缩目录 |
| `tar -xzvf archive.tar.gz` | 解压 tar.gz |

### 🐳 容器/Docker

| 命令 | 说明 |
|------|------|
| `docker ps` | 查看运行中的容器 |
| `docker ps -a` | 查看所有容器（含停止） |
| `docker logs --tail 100 <container>` | 查看容器最近日志 |
| `docker images` | 查看镜像列表 |
| `docker system df` | 磁盘使用情况 |

### 📊 日志分析

| 命令 | 说明 |
|------|------|
| `journalctl -u <service> --since "1 hour ago"` | 查看服务最近日志 |
| `dmesg \| tail -50` | 内核日志 |
| `tail -n 100 /var/log/syslog` | 系统日志 |

### ⚙️ 进程管理

| 命令 | 说明 |
|------|------|
| `pkill <name>` | 按名称杀死进程 |
| `pgrep -f <name>` | 查找进程 PID |
| `kill -9 <pid>` | 强制终止进程 |
| `nohup <cmd> &` | 后台运行（断开 SSH 仍保持） |

### 🛠️ Git 操作

| 命令 | 说明 |
|------|------|
| `git status` | 查看工作区状态 |
| `git log --oneline -10` | 最近 10 次提交 |
| `git diff` | 查看未暂存的修改 |
| `git branch -a` | 查看所有分支 |

### 🔧 实用脚本

```bash
# 清理旧日志（保留最近 7 天）
find /var/log -name "*.log" -mtime +7 -delete

# 找出占用空间最大的目录（深度 2）
du -h --max-depth=2 / | sort -hr | head -20

# 杀掉所有名为 python 的进程
pkill -f python

# 实时查看 access.log 最新 50 行
tail -50f /var/log/nginx/access.log

# 检查 URL 是否返回 200
curl -s -o /dev/null -w "%{http_code}" https://example.com
```

## 使用方式

agent-tools 不需要特殊触发指令。在分析系统问题、执行运维任务时，直接调用对应命令即可。

**示例场景：**
- "帮我看看服务器负载" → 执行 `uptime && free -h`
- "检查网站能不能访问" → 执行 `curl -I https://example.com`
- "找出哪些文件占空间" → 执行 `du -sh *` 按大小排序
- "清理 7 天前的日志" → 执行 `find ... -mtime +7 -delete`

---

_让 CooL神 成为一个真正的全能助手_