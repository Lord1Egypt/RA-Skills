# Catch My Skill

自动检测本地与线上 skill 版本差异

## 功能

- 📋 维护本地 skill 列表
- ⏰ 定时检查版本
- 🔔 版本落后提醒

## 安装

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/russellfei/catch-my-skill
```

## 使用

```bash
# 首次初始化（从 ClawHub 拉取全部）
node index.js init

# 检查版本
node index.js check

# 删除不想要的
node index.js remove <skill-name>

# 查看列表
node index.js local
```

## 定时任务

已自动添加到 crontab（每30分钟检查）

## 作者

russellfei
