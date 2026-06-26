---
name: amemo-last-data
description: 当用户说「今日健康简报」「健康日报」「健康总览」「今日健康情况」时调用，获取全部类型最新健康数据并生成综合评估报告。
---

# amemo-last-data — 查询最新数据

## 接口信息

- **路由**: POST https://skill.amemo.cn/last-data
- **Bean**: DataBean
- **Content-Type**: application/json

## 请求参数

> **注意**：服务端要求所有字段必须存在。`userToken` 必填，`dataType` 可选但字段必须存在（可传 `null`）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userToken | str | **是** | 用户登录凭证 |
| dataType | str | 否 | 数据类型（用于筛选最新记录），不传则传 `null` |

## 请求示例

```bash
# 获取所有类型最新数据（健康简报场景，dataType 传 null）
curl -X POST https://skill.amemo.cn/last-data \
  -H "Content-Type: application/json" \
  -d '{"userToken": "<token>", "dataType": null}'
```

## 响应示例

```json
{"code": 200, "desc": "success", "data": {...}}
```

## 注意事项

- 所有字段必须存在，即使不传值也要传 `null`
- 与 `amemo-find-data` 不同，此接口只返回最新的记录
- `dataType` 传 `null` 则返回所有类型中最新的数据

## 执行流程（由主模块调度）

### 执行步骤

```
1. 识别触发词（健康简报/健康总览/健康情况）
    ↓
2. 检查 userToken 是否存在
    ├── 无 token → 引导登录流程
    ↓
3. 调用接口（dataType 传 null，获取所有类型最新数据）
    ↓
4. 解析返回数据
    ├── 步数：steps, stepGoal
    ├── 睡眠：sleepHours, sleepQuality
    ├── 血氧：oxygen
    ├── 血压：systolic, diastolic
    ├── 心率：heartRate
    └── 消耗：calorie, calorieGoal
    ↓
5. 生成健康简报（按下方模板）
```

### 健康简报生成

解析返回数据后，按模板生成简报。完整模板、判断规则、评语生成详见 [health-templates.md](references/health-templates.md)。

简要流程：

```
1. 从 data 提取各指标值
2. 按 health-templates.md 中的判断规则确定每项状态
3. 匹配对应评语
4. 综合评估（great/good/needs_attention/poor）
5. 生成改善建议
6. 按 Markdown 模板输出
```

### 无数据时回复

```
暂无今日健康数据。

请确保：
• amemo 服务已启动并正常运行
• 已记录今日的健康数据
• 已完成登录认证

尝试：查看我的步数数据
```
