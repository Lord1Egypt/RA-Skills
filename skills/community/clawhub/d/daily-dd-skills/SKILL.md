---
name: daily-dd-skills
description: 钉钉日报自动提交工具 - 定时自动提交工作日报到钉钉日志系统。适用于每日工作汇报自动化、定时提交日报、钉钉日志集成等场景。支持Python导入和命令行两种方式使用，可自定义接收人列表和定时任务。
---

# daily-dd-skills

钉钉日报自动提交 Skill

## 适用场景

- 每日工作日志自动提交
- 定时汇报工作进展
- 钉钉日报自动化

## 核心功能

### 1. 自动提交日报
- 每晚 22:30 自动提交当天工作日志
- 自动发送给指定的接收人列表
- 支持手动立即提交

### 2. 工作内容管理
- 白天记录工作内容到 `today_work.txt`
- 支持多条目记录
- 自动清空已提交内容

### 3. 接收人配置
- 支持多接收人配置
- 自动发送给主管/同事
- 接收范围可视化

## 使用方法

### 快速开始

```python
from skills.daily_dd_skills.submit_log import submit_daily_report

# 立即提交日报
submit_daily_report(
    today_work="""1. 完成XX功能开发
2. 修复XXbug
3. 参加XX会议"""
)
```

### 命令行提交

```bash
# 方式1：直接提交内容
python3 skills/daily-dd-skills/submit_log.py "今日工作内容"

# 方式2：从文件读取（需要提前保存工作内容）
echo "今日工作内容" > skills/daily-dd-skills/today_work.txt
python3 skills/daily-dd-skills/submit_log.py
```

### 定时任务配置

已配置 cron 定时任务：
- **时间**: 每晚 22:30
- **功能**: 自动读取当天工作内容并提交
- **接收人**: 可自定义

## 配置说明

### 钉钉应用配置
编辑 `config.json`：
```json
{
  "dingtalk": {
    "app_key": "your-app-key",
    "app_secret": "your-app-secret",
    "user_id": "your-user-id",
    "template_id": "your-template-id"
  }
}
```

### 接收人配置
```json
{
  "receivers": [
    {"name": "张三", "user_id": "user-id-1"},
    {"name": "李四", "user_id": "user-id-2"}
  ]
}
```

## 文件结构

```
daily-dd-skills/
├── SKILL.md           # 本说明文档
├── submit_log.py      # 主提交脚本
├── config.json        # 配置文件
└── today_work.txt     # 工作内容记录（自动生成）
```

## 工作流程

```
白天记录工作内容 → 保存到 today_work.txt
         ↓
晚上22:30自动提交 → 钉钉日志系统
         ↓
接收人收到日报 → 可查看详情
```

## 安装方法

### 方式1：直接解压
```bash
tar -xzf daily-dd-skills.tar.gz -C /目标AI/workspace/skills/
```

### 方式2：手动复制
```bash
mv daily-dd-skills/ /目标AI/workspace/skills/
```

## 依赖要求

- Python 3.x
- requests 库

## 注意事项

1. **AppKey/AppSecret**: 需要替换为自己的钉钉应用凭证
2. **接收人UserID**: 需要根据实际情况修改
3. **日志模板**: 需先在钉钉后台配置好日报模板
4. **网络要求**: 需要能访问钉钉 API (oapi.dingtalk.com)

## 更新记录

- 2026-03-12: 创建 daily-dd-skills，支持钉钉日报自动提交
