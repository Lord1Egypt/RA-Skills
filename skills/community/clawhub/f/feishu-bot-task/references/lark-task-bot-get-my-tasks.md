# task +bot-get-my-tasks

> **功能**：Bot 身份查询自己作为负责人的任务列表。
> **背景**：标准的 `+get-my-tasks` 使用 v2 接口，只支持用户身份。Bot 身份调用会失败。本命令使用 v1 接口，Bot 身份可以正常使用。

> **前置条件**：请先阅读 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，了解认证、身份选择和权限处理规则。

## 背景说明

飞书任务的 `GET /task/v2/tasks` 接口（v2）在设计上映射为"用户的任务列表"，因此不支持 Bot 身份调用。而 `GET /task/v1/tasks` 接口（v1）没有这个限制，Bot 身份可以直接查询。

本命令通过直接调用 v1 接口，解决 Bot 身份无法获取任务列表的问题。

## 推荐命令

```bash
# 查询 Bot 负责的所有任务（自动分页，最多20页）
python3 skills/lark-task/scripts/lark-task-bot-list.py
```

## 使用流程

1. 直接执行 Python 脚本
2. 解析 JSON 返回结果
3. 展示任务标题、GUID、截止时间、负责人等关键信息

## 输出格式

脚本返回 JSON 格式：
```json
{
  "code": 0,
  "data": {
    "items": [
      {
        "id": "任务GUID",
        "summary": "任务标题",
        "due": {"time": "1234567890", "is_all_day": true},
        "members": [{"id": "open_id", "role": "assignee", "type": "user/app"}],
        "followers": [{"id": "open_id"}],
        "create_time": "创建时间戳",
        "complete_time": "完成时间戳（0表示未完成）"
      }
    ],
    "total": 10
  }
}
```

## 适用场景

- Bot 作为包工头，需要查询自己派发了哪些任务
- Agent 团队中，主 Agent 查询各个子 Agent 的任务进度
- 定时巡检任务完成状态

## 注意事项

- 本命令使用 v1 接口，响应格式与 v2 不同
- Bot 身份（tenant_access_token）由脚本自动处理，无需额外配置
- 凭证从环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 读取，默认使用当前飞书机器人的应用凭证
