# 使用指南

## 前提条件

本服务处理敏感健康数据，**默认要求 API 鉴权**。

```bash
# 设置 API 密钥（启动前必须）
export API_KEY=your_strong_secret_key
```

## 安装

```bash
# 1. 安装依赖
pip install flask

# 2. 下载 app.py 和 core.py
# 3. 运行服务
python app.py
```

所有 API 请求需在 Header 添加 `X-API-Key: your_strong_secret_key`。

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| **API_KEY** | **（必填）无默认值** | **API 鉴权密钥。启动前必须设置，否则服务拒绝启动。** |
| BIND_HOST | 127.0.0.1 | 监听地址（生产部署配合反向代理） |
| GLUCOSE_CRITICAL_LOW | 2.8 | 危急低血糖阈值 (mmol/L) |
| GLUCOSE_CRITICAL_HIGH | 20.0 | 危急高血糖阈值 (mmol/L) |
| GLUCOSE_HYPO | 3.9 | 低血糖警报线 |
| GLUCOSE_HYPER | 13.9 | 高血糖警报线 |
| MAX_BOLUS_INSULIN | 15.0 | 单次大剂量上限 (U) |
| MAX_BASAL_INSULIN | 60.0 | 每日基础量上限 (U) |
| DEFAULT_TARGET_GLUCOSE | 6.0 | 默认目标血糖 |
| PORT | 5000 | 监听端口 |

## 示例流程

```python
import requests
import json

BASE = "http://localhost:5000"

# 1. 设置用户参数（需 X-API-Key header）
requests.post(f"{BASE}/profile", headers={"X-API-Key": "your_key"}, json={
    "user_id": "demo",
    "target_glucose": 6.0,
    "correction_factor": 2.0,
    "carb_ratio": 12.0
})

# 2. 添加记录
requests.post(f"{BASE}/record", headers={"X-API-Key": "your_key"}, json={
    "user_id": "demo",
    "glucose": 8.2,
    "meal_carbs": 50
})

# 3. 获取建议
resp = requests.post(f"{BASE}/advice", headers={"X-API-Key": "your_key"}, json={
    "glucose": 8.2,
    "meal_type": "dinner"
})
print(json.dumps(resp.json(), indent=2))
```

## 生产部署

```bash
# 使用 Gunicorn
pip install gunicorn
export API_KEY=<strong_random_key>
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```
