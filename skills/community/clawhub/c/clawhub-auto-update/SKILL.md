---
name: clawhub-auto-update
description: 自动检查并更新ClawHub已安装技能。有更新时通知用户，支持手动和定时运行。
---

# ClawHub Auto Update

自动检查并更新已安装的ClawHub技能。

## 功能

1. **检查更新**：对比本地版本与ClawHub最新版本
2. **批量更新**：自动更新所有可更新的技能
3. **通知用户**：有更新时推送通知
4. **定时运行**：支持cron定时检查

## 实际使用

### 方式1：运行脚本自动检查+更新
```bash
bash ~/.openclaw/workspace/skills/clawhub-auto-update/scripts/check-update.sh
```

### 方式2：定时运行（推荐）

添加到crontab：
```bash
# 每周日凌晨3点检查更新
0 3 * * 0 bash ~/.openclaw/workspace/skills/clawhub-auto-update/scripts/check-update.sh >> ~/.openclaw/logs/skill-update.log 2>&1
```

### 方式3：手动更新
```bash
npx clawhub update --all
```

## 输出格式

更新时输出：
```
🔄 检查技能更新...
✅ skill-name: 1.0.0 → 1.1.0 已更新
📊 共检查 X 个技能，Y 个可更新
```

## 集成到主流程

在 auto-learn.sh 中添加：
```bash
# 每周日检查技能更新
if [ "$(date +%w)" = "0" ]; then
  echo "🔄 检查技能更新..."
  npx clawhub update --all >> ~/.openclaw/logs/skill-update.log 2>&1
fi
```

## 注意事项

- 需要先登录ClawHub：`npx clawhub login`
- 更新会覆盖本地修改（如果有）
- 建议先备份重要配置
