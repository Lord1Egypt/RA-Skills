# API 规格

## 基础 URL

```
http://localhost:5000
```

## 鉴权（可选）

设置环境变量启用：

```bash
export ENABLE_AUTH=true
export API_KEY=your_secret_key
```

请求头添加 `X-API-Key: your_secret_key`。

---

## 1. 健康检查

```
GET /api/health
```

**响应：**
```json
{
  "status": "active",
  "version": "2.0-safe"
}
```

---

## 2. 用户参数管理

### 获取参数

```
GET /api/profile?user_id=<id>
```

### 更新参数

```
POST /api/profile
Content-Type: application/json

{
  "user_id": "user001",
  "target_glucose": 6.0,
  "correction_factor": 2.5,
  "carb_ratio": 10.0,
  "medications": ["insulin", "metformin"]
}
```

**参数范围：**
| 参数 | 范围 |
|------|------|
| target_glucose | 4.0 - 10.0 mmol/L |
| correction_factor | 1.0 - 20.0 |
| carb_ratio | 5.0 - 30.0 |

---

## 3. 添加记录

```
POST /api/record
Content-Type: application/json

{
  "user_id": "user001",
  "glucose": 7.2,
  "meal_carbs": 45,
  "exercise_minutes": 30,
  "insulin_dose": 4.0,
  "notes": "餐后2小时"
}
```

**危急值告警：** 血糖 <2.8 或 >20.0 时自动记录审计日志。

---

## 4. 血糖建议

```
POST /api/advice/glucose
Content-Type: application/json

{
  "glucose": 6.5,
  "meal_type": "lunch"
}
```

**响应：**
```json
{
  "glucose": 6.5,
  "level": "info",
  "message": "...",
  "diet": {
    "carb_recommendation": "45-60g",
    "advice": "先吃蔬菜，后吃主食"
  },
  "exercise": {
    "safety": "安全",
    "advice": "适合中等强度运动，注意补水。"
  },
  "disclaimer": "本建议基于通用临床指南，请结合医生意见使用。"
}
```

**危急值响应示例：**
```json
{
  "glucose": 2.5,
  "level": "critical",
  "action": "立即就医",
  "immediate_steps": "1. 若意识清醒... 2. ...",
  "disclaimer": "危急情况！本建议不替代急救，请立即采取行动。"
}
```

---

## 5. 胰岛素计算

```
POST /api/insulin/calculate
Content-Type: application/json

{
  "user_id": "user001",
  "current_glucose": 9.0,
  "carbs_grams": 60,
  "on_board_insulin": 2.0
}
```

---

## 6. 风险报告

```
GET /api/risk/user001
```

---

## 7. 最近摘要

```
GET /api/summary/user001
```

---

## 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（已启用鉴权时） |
