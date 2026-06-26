# FC Online官网监控Skill使用示例

## 示例1：基本监控设置

### 场景
用户想要监控FC Online官网，每天8点到23点每小时检查一次新活动。

### 命令
```bash
# 设置定时监控
./fco-monitor.sh setup 8 23 60

# 或使用Node版本
node openclaw-integration.js setup 8 23 60
```

### 输出
```
⏰ 设置监控: 8:00-23:00, 间隔60分钟
✅ 监控设置成功
📅 创建cron任务: 0 8-23 * * *
```

### 效果
- 每天8:00开始，23:00结束
- 每小时整点检查一次官网
- 发现新活动时自动通知

## 示例2：立即检查官网

### 场景
用户想立即查看当前官网有什么新活动。

### 命令
```bash
# 立即检查
./fco-monitor.sh check-now

# 或使用Node版本
node openclaw-integration.js check-now
```

### 输出示例（有新活动）
```
🎯 【FC Online新活动通知】

🔥 **高优先级活动**
📅 发布时间：03/19
📝 活动内容：26TOTY和TOTYN赛季绝版活动公告

📢 常规活动
📅 发布时间：03/18
📝 活动内容：25UCL赛季携手全新玩法，福利升级同步上线！

---
📊 统计：高优先级活动 1 个，常规活动 1 个
🔗 官网地址：https://fco.qq.com/main.shtml
⏰ 检查时间：2026-03-19 20:30:00
```

### 输出示例（无新活动）
```
ℹ️ 无新活动
```

## 示例3：查看监控状态

### 场景
用户想查看当前监控任务的运行状态。

### 命令
```bash
./fco-monitor.sh status
```

### 输出
```
📊 FC Online监控状态
   运行时间：8:00 - 23:00
   检查间隔：60分钟
   最后日志：/tmp/fco-monitor-2026-03-19.log
   最后检查：2026-03-19 20:30:00
```

## 示例4：在OpenClaw对话中使用

### 场景
用户在OpenClaw对话中想要使用监控功能。

### 用户指令
```
帮我监控FC Online官网，每天8点到24点整点检查新活动。
```

### 助手响应
```
好的！我来为您设置FC Online官网监控：

1. ✅ 已设置定时任务：每天8:00-23:00整点检查
2. 🔍 立即执行第一次检查...
3. 📊 当前官网状态：26TOTY绝版活动将于明天（3月20日）上线

监控已启动！每小时会自动检查官网，发现新活动时会立即通知您。
```

### 后续自动通知
当监控发现新活动时，会自动发送：
```
🎯 【FC Online新活动通知】
📅 活动时间：2026-03-20 至 2026-03-31
💰 活动类型：26TOTY绝版礼包
🎁 核心奖励：26TY/TYN赛季BEST1人9强球员包
⏰ 限时优惠：3月20日-3月31日折扣阶段
🔗 详情链接：https://fco.qq.com/...
```

## 示例5：自定义监控配置

### 场景
用户想要更频繁的检查，并且只关注特定类型活动。

### 步骤
1. **编辑配置文件**
```bash
# 编辑配置文件
nano /root/.openclaw/config/fco-monitor.json
```

2. **修改配置**
```json
{
  "fcoMonitor": {
    "enabled": true,
    "checkSchedule": {
      "startHour": 7,
      "endHour": 24,
      "intervalMinutes": 30  # 每30分钟检查一次
    },
    "notification": {
      "enabled": true,
      "format": "detailed",
      "onlyNewActivities": true
    },
    "keywords": {
      "highPriority": [
        "26TOTY",
        "绝版",
        "TY礼包",
        "限时折扣"
      ],
      "normalPriority": [
        "赛季",
        "活动"
      ]
    }
  }
}
```

3. **重新启动监控**
```bash
./fco-monitor.sh setup 7 24 30
```

## 示例6：故障排查

### 场景
监控没有正常工作，用户想要排查问题。

### 排查步骤
1. **测试连接**
```bash
node openclaw-integration.js test
```
输出：`✅ 官网可正常访问`

2. **查看日志**
```bash
# 查看最近20条日志
node openclaw-integration.js logs 20
```

3. **手动测试检查**
```bash
./fco-monitor.sh check-now
```

4. **检查cron任务**
```bash
# 查看OpenClaw的cron任务
openclaw cron list
```

## 示例7：集成到其他系统

### 场景
用户想要将监控结果发送到其他系统（如Discord、Slack）。

### 解决方案
1. **修改通知配置**
```json
{
  "notification": {
    "enabled": true,
    "format": "json",  // 输出JSON格式
    "webhook": {
      "enabled": true,
      "url": "https://discord.com/api/webhooks/...",
      "format": "discord"
    }
  }
}
```

2. **自定义输出处理**
```bash
# 获取JSON格式的输出
./fco-monitor.sh check-now --format json | jq .
```

## 示例8：批量历史检查

### 场景
用户想要检查过去几天的活动变化。

### 解决方案
```bash
# 创建检查脚本
cat > check-history.sh << 'EOF'
#!/bin/bash
for day in {1..7}; do
  date=$(date -d "$day days ago" +%Y-%m-%d)
  echo "=== 检查 $date ==="
  # 这里可以模拟不同日期的检查
  ./fco-monitor.sh check-now
  echo ""
done
EOF

chmod +x check-history.sh
./check-history.sh
```

## 最佳实践

### 1. 监控时间设置
- **游戏更新时间**：设置在北京时间10:00、14:00、19:00等游戏常见更新时间点
- **活动上线时间**：重点关注周四、周五（常见活动更新日）
- **维护时间**：避开游戏维护时段（通常周二凌晨）

### 2. 关键词优化
- **赛季相关**：26TOTY、TOTYN、25UCL、马年赛季
- **活动类型**：绝版、限时、折扣、礼包、返利
- **重要节点**：版本更新、赛季结束、新赛季开始

### 3. 通知策略
- **高优先级**：绝版活动、限时折扣立即通知
- **中优先级**：常规活动每日汇总通知
- **低优先级**：资讯类内容可选通知

### 4. 性能优化
- **检查频率**：非高峰时段可降低频率
- **缓存策略**：缓存已检查内容，避免重复处理
- **错误处理**：网络异常时自动重试，避免频繁失败

## 常见问题

### Q1：监控没有发现新活动？
A：检查关键词配置，确保包含最新活动名称。

### Q2：通知格式不符合需求？
A：修改配置文件中的`format`选项，支持`simple`、`detailed`、`json`格式。

### Q3：想要监控其他网站？
A：可以修改配置文件中的URL，但需要调整内容解析逻辑。

### Q4：如何备份监控数据？
A：日志文件在`/tmp/fco-monitor-*.log`，配置文件在`/root/.openclaw/config/fco-monitor.json`。

---

**更多问题？** 请查看SKILL.md文档或联系维护者。