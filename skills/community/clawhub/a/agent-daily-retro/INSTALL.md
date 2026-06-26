# Agent Retro 安装部署指南

## 📋 系统要求

### **环境要求**
- **操作系统**：Linux (Ubuntu/Debian/CentOS)
- **Python版本**：Python 3.8+
- **OpenClaw版本**：2026.3.13+
- **权限**：root或sudo权限

### **依赖检查**
```bash
# 检查Python版本
python3 --version

# 检查OpenClaw安装
openclaw --version

# 检查工作区目录
ls -la ~/.openclaw/workspace/
```

## 🚀 安装步骤

### **步骤1：下载技能包**
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills

# 下载或复制技能文件
# （如果已存在，跳过此步）
```

### **步骤2：配置飞书机器人**
1. **创建飞书机器人**
   - 进入飞书开放平台
   - 创建自定义机器人
   - 获取webhook地址

2. **更新配置文件**
```bash
# 编辑配置文件
nano ~/.openclaw/workspace/skills/agent-retro/config.json

# 更新feishu.webhook字段
"feishu": {
  "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_ID",
  "enabled": true,
  "message_type": "interactive"
}
```

### **步骤3：权限设置**
```bash
# 确保有写入权限
chmod 755 ~/.openclaw/workspace/memory
chmod 644 ~/.openclaw/workspace/skills/agent-retro/*.py

# 设置执行权限
chmod +x ~/.openclaw/workspace/skills/agent-retro/agent_retro.py
```

### **步骤4：测试安装**
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/agent-retro

# 测试配置加载
python3 -c "import json; config=json.load(open('config.json')); print('配置加载成功:', config['skill_name'])"

# 测试会话解析
python3 session_analyzer_v2.py

# 测试完整流程（手动执行一次复盘）
python3 agent_retro.py
```

## ⏰ 定时任务配置

### **自动配置（推荐）**
技能已通过cron技能自动配置定时任务：
- **执行时间**：每天00:05（北京时间）
- **任务ID**：JOB-A2A8（Agent每日复盘）
- **输出渠道**：飞书 + 控制台

### **手动配置（备用）**
```bash
# 编辑crontab
crontab -e

# 添加以下行
5 0 * * * cd /root/.openclaw/workspace/skills/agent-retro && python3 agent_retro.py >> /var/log/agent_retro.log 2>&1
```

### **验证定时任务**
```bash
# 查看cron任务
crontab -l | grep agent_retro

# 查看cron日志
grep CRON /var/log/syslog | tail -10

# 手动触发测试
python3 agent_retro.py --force
```

## 🔧 配置详解

### **config.json 完整配置**
```json
{
  "skill_name": "agent-retro",
  "version": "1.0.0",
  "description": "Agent每日复盘系统",
  "author": "夸夸 (基于Tangc的SKILL.md实现)",
  
  "settings": {
    "default_agent_id": "main",
    "retro_time": "00:05",
    "timezone": "Asia/Shanghai",
    "backup_enabled": true,
    "lock_enabled": true,
    "analysis_dimensions": [
      "yesterday_actions",
      "right_things",
      "wrong_things",
      "improvements",
      "user_profile",
      "agent_profile"
    ],
    "core_files_to_update": [
      "MEMORY.md",
      "USER.md",
      "SOUL.md",
      "AGENTS.md"
    ],
    "output_channels": ["feishu", "console", "file"]
  },
  
  "paths": {
    "workspace": "~/.openclaw/workspace",
    "sessions_dir": "~/.openclaw/agents/{agent_id}/sessions",
    "memory_dir": "~/.openclaw/workspace/memory",
    "lock_prefix": "AGENT_RETRO_DONE_"
  },
  
  "feishu": {
    "webhook": "YOUR_WEBHOOK_URL",
    "enabled": true,
    "message_type": "interactive"
  },
  
  "session_schema": {
    "type_field": "type",
    "message_field": "message",
    "role_field": "role",
    "content_field": "content",
    "timestamp_field": "timestamp",
    "tool_calls_field": "tool_calls"
  }
}
```

## 🧪 测试验证

### **测试1：基础功能测试**
```bash
# 测试配置加载
python3 -c "
import json, sys
sys.path.insert(0, '.')
from agent_retro import AgentRetroConfig
config = AgentRetroConfig()
print(f'✅ 配置加载成功: {config.config[\"skill_name\"]} v{config.config[\"version\"]}')
"

# 测试会话分析器
python3 session_analyzer_v2.py
```

### **测试2：完整流程测试**
```bash
# 手动执行复盘（今天的数据）
python3 agent_retro.py --date $(date +%Y-%m-%d)

# 检查输出文件
ls -la ~/.openclaw/workspace/memory/*.md | tail -5

# 检查飞书消息
# 查看飞书群组是否收到消息
```

### **测试3：防重复锁测试**
```bash
# 第一次执行
python3 agent_retro.py

# 第二次执行（应该被阻止）
python3 agent_retro.py

# 强制执行（使用--force参数）
python3 agent_retro.py --force
```

## 🚨 故障排除

### **常见问题1：权限不足**
```
错误：Permission denied
解决：chmod 755 ~/.openclaw/workspace/memory
```

### **常见问题2：飞书webhook无效**
```
错误：飞书消息发送失败
解决：检查webhook地址，确保机器人已添加到群组
```

### **常见问题3：会话文件找不到**
```
错误：No session files found
解决：检查 ~/.openclaw/agents/main/sessions/ 目录
```

### **常见问题4：定时任务未执行**
```
错误：cron任务未触发
解决：检查系统时间、cron服务状态、日志文件
```

## 📊 监控与维护

### **日志文件**
```bash
# 查看执行日志
tail -f /var/log/agent_retro.log

# 查看错误日志
grep -i error /var/log/agent_retro.log
```

### **性能监控**
```bash
# 查看执行时间
grep "执行时间" /var/log/agent_retro.log

# 查看内存使用
ps aux | grep agent_retro
```

### **数据清理**
```bash
# 清理旧的备份文件（保留最近7天）
find ~/.openclaw/workspace -name "*.bak.*" -mtime +7 -delete

# 清理旧的锁文件（保留最近30天）
find ~/.openclaw/workspace/memory -name "AGENT_RETRO_DONE_*.md" -mtime +30 -delete
```

## 🔄 升级指南

### **备份现有配置**
```bash
# 备份配置文件
cp ~/.openclaw/workspace/skills/agent-retro/config.json config.json.backup

# 备份定时任务
crontab -l > crontab.backup
```

### **更新技能文件**
```bash
# 下载新版本
cd ~/.openclaw/workspace/skills
rm -rf agent-retro
# 解压新版本

# 恢复配置
cp config.json.backup agent-retro/config.json

# 重新设置权限
chmod +x agent-retro/*.py
```

### **验证升级**
```bash
# 测试新版本
cd agent-retro
python3 agent_retro.py --test

# 检查定时任务
crontab -l | grep agent_retro
```

## 📞 技术支持

### **获取帮助**
1. 查看日志文件：`/var/log/agent_retro.log`
2. 检查配置文件：`config.json`
3. 测试基础功能：`python3 test_retro.py`

### **报告问题**
- **问题描述**：详细描述问题现象
- **复现步骤**：如何重现问题
- **环境信息**：系统版本、Python版本
- **日志文件**：相关错误日志

---

**安装完成标志**：
1. ✅ 配置文件正确
2. ✅ 飞书消息测试成功
3. ✅ 手动执行复盘成功
4. ✅ 定时任务配置正确
5. ✅ 第二天00:05自动执行成功