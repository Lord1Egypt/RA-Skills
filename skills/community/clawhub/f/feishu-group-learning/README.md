# Feishu Group Learning

自动分析飞书群消息，提取学习点和进化建议的 OpenClaw 技能。

## 功能

- 自动监控飞书群消息
- 语义分析提取关键信息
- 生成学习建议和进化方向
- 每6小时自动运行

## 安装

```bash
clawhub install feishu-group-learning
```

## 配置

编辑 `config.json`:

```json
{
  "chats": [
    {"id": "oc_xxx", "name": "群名称"}
  ],
  "schedule": "0 */6 * * *"
}
```

## 使用

```bash
# 手动运行
bash analyze.sh

# 自动运行（通过 cron）
openclaw cron add --name "group-learning" --schedule "0 */6 * * *" --command "bash analyze.sh"
```

## 作者

Vita虾助理
