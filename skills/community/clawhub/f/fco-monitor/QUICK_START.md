# FC Online官网监控Skill - 快速开始

## 🚀 一键安装
```bash
cd /root/.openclaw/workspace/skills/fco-monitor
./install.sh
```

## 📋 基本使用

### 1. 立即检查官网
```bash
./fco-monitor.sh check-now
```

### 2. 设置定时监控（8:00-23:00，每小时）
```bash
./fco-monitor.sh setup 8 23 60
```

### 3. 查看监控状态
```bash
./fco-monitor.sh status
```

## 🎯 在OpenClaw对话中使用

### 用户指令示例：
```
帮我监控FC Online官网，每天8点到24点整点检查新活动。
```

### 助手自动响应：
1. ✅ 设置定时监控任务
2. 🔍 立即执行第一次检查
3. 📊 返回当前官网状态
4. ⏰ 启动持续监控

## ⚙️ 配置文件
位置：`/root/.openclaw/config/fco-monitor.json`

### 主要配置项：
```json
{
  "checkSchedule": {
    "startHour": 8,      // 开始时间（24小时制）
    "endHour": 23,       // 结束时间
    "intervalMinutes": 60 // 检查间隔
  },
  "keywords": {
    "highPriority": ["26TOTY", "绝版", "TY礼包"],
    "normalPriority": ["赛季", "活动", "更新"]
  }
}
```

## 📊 监控输出示例

### 发现新活动时：
```
🎯 【FC Online新活动通知】
🔥 **高优先级活动**
📅 发布时间：03/20
📝 活动内容：26TOTY绝版礼包上线
🎁 核心奖励：26TY/TYN赛季BEST1人9强球员包
⏰ 限时优惠：3月20日-3月31日折扣阶段
🔗 官网地址：https://fco.qq.com/main.shtml
```

### 无新活动时：
保持安静，不发送通知。

## 🔧 故障排查

### 1. 测试连接
```bash
node openclaw-integration.js test
```

### 2. 查看日志
```bash
node openclaw-integration.js logs 20
```

### 3. 检查cron任务
```bash
openclaw cron list | grep "FC Online"
```

## 📁 文件结构
```
fco-monitor/
├── SKILL.md          # Skill主文档
├── fco-monitor.sh    # 主监控脚本
├── openclaw-integration.js # OpenClaw集成
├── install.sh        # 安装脚本
├── EXAMPLES.md       # 使用示例
├── QUICK_START.md    # 本快速指南
└── README.md         # 说明文档
```

## ⚡ 高级功能

### 自定义检查时间
```bash
# 7:00-24:00，每30分钟检查一次
./fco-monitor.sh setup 7 24 30
```

### 自定义关键词
编辑配置文件，添加关注的关键词。

### JSON格式输出
```bash
./fco-monitor.sh check-now --format json
```

## 📞 支持
- 查看完整文档：`SKILL.md`
- 查看示例：`EXAMPLES.md`
- 查看日志：`/tmp/fco-monitor-*.log`

---

**安装状态**：✅ 已成功安装  
**Skill位置**：`/usr/lib/node_modules/openclaw/skills/fco-monitor`  
**下次检查**：明天 8:00（如果已设置定时任务）