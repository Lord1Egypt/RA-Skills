---
name: amemo-find-task
description: 当用户说「查看清单/查询清单/我的待办/查看任务/列出任务」时调用，返回按今日/明日/近期/未来分组的完整待办清单。
---

# amemo-find-task — 查询任务

---

## 接口信息

| 属性 | 值 |
|:-----|:---|
| **路由** | `POST https://skill.amemo.cn/find-task` |
| **Bean** | `TaskBean` |
| **Content-Type** | `application/json` |

---

## 请求参数

> ⚠️ 服务端要求所有字段必须存在。`userToken` 必填且有值，其他字段可选但字段必须存在。

| 参数 | 类型 | 必填 | 说明 |
|:-----|:----:|:----:|:-----|
| `userToken` | str | ✅ | 用户登录凭证 |
| `taskId` | str | — | 按 ID 精确查询，不传则传 `null` |
| `taskTitle` | str | — | 按标题模糊查询，不传则传 `null` |
| `taskTime` | str | — | 按时间筛选，不传则传 `null` |
| `taskEmail` | list[str] | — | 按邮箱筛选，不传则传 `null` |

---

## 请求示例

```bash
# 查询所有任务（所有可选字段传 null）
curl -X POST https://skill.amemo.cn/find-task \
  -H "Content-Type: application/json" \
  -d '{
    "userToken": "<token>",
    "taskId": null,
    "taskTitle": null,
    "taskTime": null,
    "taskEmail": null
  }'

# 按标题查询
curl -X POST https://skill.amemo.cn/find-task \
  -H "Content-Type: application/json" \
  -d '{
    "userToken": "<token>",
    "taskId": null,
    "taskTitle": "报告",
    "taskTime": null,
    "taskEmail": null
  }'
```

---

## 响应数据结构

```json
{
  "code": 200,
  "desc": "success",
  "data": {
    "recommend": [],
    "myFollow": [],
    "todayList": [],
    "tomorrowList": [],
    "recentList": [],
    "finishList": [],
    "futureList": []
  }
}
```

### TaskInfo 任务信息

| 字段 | 类型 | 说明 |
|:-----|:----:|:-----|
| `taskId` | str | 任务唯一标识 |
| `taskTitle` | str | 任务标题 |
| `recentRemindTime` | int | 最近的提醒时间 |

---

## 执行流程

```
1. 识别触发词（查看/查询/列出 + 清单/任务/待办）
    ↓
2. 检查 userToken 是否存在 → 无 token 则引导登录
    ↓
3. 调用 POST /find-task 接口
    ↓
4. 解析返回的 7 个分类列表
    ↓
5. 按优先级分组格式化输出
```

### 分组展示规则

| 优先级 | 分类 | 说明 |
|:------:|:-----|:-----|
| 1 | 今日待办 | 今日必须完成的任务，优先展示 |
| 2 | 明日待办 | 明日计划的任务 |
| 3 | 近期待办 | 未来15天内的任务 |
| 4 | 未来待办 | 15天之后的任务 |
| 5 | 我的收藏 | 用户收藏的重要任务 |
| 6 | 已完成 | 已完成的任务 |

### 空分类处理

| 分类 | 空状态提示 |
|:-----|:----------|
| 今日/明日/近期 | `暂无15天内待办` |
| 未来 | `暂无未来待办` |
| 收藏 | `暂无收藏任务` |
| 已完成 | `暂无已完成任务` |

---

## 输出模板

### 无数据时

```markdown
**📋 暂无待办清单**

> 创建新任务 →
> • 「今天 3 点开会」
> • 「提醒我明天交报告」
```

### 有数据时

```markdown
**✅ 待办清单** · 共 {total} 项

---

### 📅 今日待办
- ⏳ {task1}
- ⏳ {task2}

---

### 📆 明日待办 ({count})
- ⏳ {task1}

---

### 📋 近期待办 ({count})
- ⏳ {task1}

---

### 🔮 未来待办 ({count})
- ⏳ {task1}

---

### ⭐ 收藏 ({count})
- ★ {task1}

---

### ✔ 已完成 ({count})
- ✓ {task1}
```

### 任务项格式

| 类型 | 格式 |
|:---|:---|
| 待做 | `{taskTitle}` |
| 收藏 | `⭐ {taskTitle}` |
| 已完成 | `✓ {taskTitle}` |
| 已过期 | `❌ {taskTitle}` |
