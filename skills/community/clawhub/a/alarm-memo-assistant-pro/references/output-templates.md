# Output Templates

## 创建提醒成功

```md
# 已创建提醒

- 标题：{title}
- 时间：{time}
- 重复：{repeat}
- 备注：{note}
- 存储：{storage}
- 调度状态：{scheduleStatus}
- 自动发送：{deliveryStatus}

## 后续可做
- 修改时间
- 改成重复提醒
- 加入今日任务清单
```

## 记录备忘录成功

```md
# 已记录备忘录

- 标题：{title}
- 分类：{category}
- 标签：{tags}
- 存储：{storage}

## 内容
{body}

## 可选后续
- 为这条备忘加提醒
- 转成待办
```

## 今日任务摘要

```md
# 今日任务摘要

## 今天到期
{dueToday}

## 高优先级
{highPriority}

## 逾期未完成
{overdue}

## 可顺延事项
{reschedulable}

## 建议
{advice}
```
