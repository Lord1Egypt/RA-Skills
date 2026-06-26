---
name: tool-api-reference-emergency-v3
title: 紧急救助与健康档案 API（v3.0 新增）
description: 自由行旅游出行管家 v3.0 新增的紧急救助 API 和健康档案 API，专为老年人旅行安全设计
author: 汪小玲 (苏英)
department: 飞猪 -CTO 线 - 技术质量 - 服务质量
version: 3.0
created_at: 2026-04-01
tags:
  - 紧急救助
  - 健康档案
  - API
  - 老年友好
---

# 紧急救助与健康档案 API（v3.0 新增）

## 概述

v3.0 版本新增两大类 API，专为老年人旅行安全保障设计：

1. **紧急救助服务** - 处理健康异常、迷路走失、防诈骗等紧急情况
2. **健康档案服务** - 管理老年人健康信息、病史、用药记录

---

## 1. 紧急救助服务 ⭐

### 1.1 一键呼叫 120

**场景**：父母突发严重疾病或遭遇意外，需要立即送医

```http
POST https://fliggy.com/api/emergency/call120
Content-Type: application/json
Priority: URGENT

Request:
{
  "trip_id": "TRIP20260401001",
  "traveler_info": {
    "name": "张父",
    "age": 65,
    "phone": "138****5678"
  },
  "location": {
    "latitude": 25.694826,
    "longitude": 100.164912,
    "address": "云南省大理市大理古城人民路",
    "poi": "大理古城南门附近"
  },
  "emergency_type": "medical",  // medical/accident/lost/other
  "symptoms": ["chest_pain", "shortness_of_breath", "dizziness"],
  "severity": "critical",  // mild/moderate/critical
  "health_profile": {
    "chronic_conditions": ["高血压", "糖尿病"],
    "allergies": ["青霉素"],
    "regular_medications": ["降压药"]
  },
  "contacts_to_notify": [
    {"name": "张女士", "relation": "女儿", "phone": "139****1234"},
    {"name": "李导游", "role": "地接导游", "phone": "138****5678"}
  ]
}

Response:
{
  "code": 200,
  "data": {
    "emergency_id": "EMG20260401001",
    "ambulance_called": true,
    "ambulance_no": "云 L·120345",
    "eta_minutes": 8,
    "hospital_info": {
      "name": "大理市第一人民医院",
      "address": "大理市人民南路 123 号",
      "distance_km": 2.5,
      "emergency_phone": "0872-2123456"
    },
    "contacts_notified": [
      {"name": "张女士", "status": "called", "time": "2026-04-11T10:35:00+08:00"},
      {"name": "李导游", "status": "called", "time": "2026-04-11T10:35:05+08:00"}
    ],
    "guide_dispatched": {
      "name": "李导游",
      "phone": "138****5678",
      "eta_minutes": 5
    },
    "insurance_notified": true,
    "case_number": "INS20260401001"
  }
}
```

---

### 1.2 健康状态上报

**场景**：父母自述不适或智能手表检测到异常体征

```http
POST https://fliggy.com/api/emergency/health-report
Content-Type: application/json

Request:
{
  "traveler_id": "2214118900513",
  "trip_id": "TRIP20260401001",
  "vital_signs": {
    "heart_rate": 95,  // 次/分钟
    "blood_pressure": {"systolic": 150, "diastolic": 95},
    "blood_sugar": 8.5,  // mmol/L
    "body_temperature": 37.2,  // ℃
    "oxygen_saturation": 96  // %
  },
  "symptoms": ["dizziness", "fatigue"],
  "self_assessment": "有点累，头有点晕",
  "measurement_time": "2026-04-11T14:30:00+08:00",
  "device_source": "smart_watch"  // smart_watch/manual_input
}

Response:
{
  "code": 200,
  "data": {
    "report_id": "HEALTH20260401001",
    "risk_level": "moderate",  // normal/mild/moderate/critical
    "assessment": "血压偏高，建议休息观察",
    "recommendations": [
      "在休息区坐下休息 15 分钟",
      "喝点温水，吃点糖果或饼干",
      "避免剧烈运动",
      "30 分钟后复测血压"
    ],
    "alert_triggered": true,
    "alerts_sent_to": [
      {"name": "地接导游", "method": "dingtalk"},
      {"name": "子女", "method": "phone_call"}
    ],
    "follow_up_scheduled": "2026-04-11T15:00:00+08:00"
  }
}
```

---

### 1.3 迷路定位与接应

**场景**：父母在景区或城市迷路，找不到集合点

```http
POST https://fliggy.com/api/emergency/lost-help
Content-Type: application/json

Request:
{
  "traveler_id": "2214118900513",
  "trip_id": "TRIP20260401001",
  "location": {
    "latitude": 25.703456,
    "longitude": 100.152345,
    "accuracy_meters": 10,
    "last_update": "2026-04-11T15:30:00+08:00"
  },
  "surrounding_landmarks": ["工商银行", "大理国际大酒店"],
  "panic_level": "high",  // low/medium/high
  "group_status": "alone"  // alone/with_group
}

Response:
{
  "code": 200,
  "data": {
    "help_id": "LOST20260401001",
    "guide_dispatched": {
      "name": "李导游",
      "phone": "138****5678",
      "current_location": {"latitude": 25.702123, "longitude": 100.153456},
      "distance_meters": 150,
      "eta_minutes": 3
    },
    "instructions_for_traveler": [
      "请在原地不要移动",
      "寻找附近的工商银行标志",
      "如果看到穿红色马甲的工作人员，就是他",
      "保持电话畅通"
    ],
    "backup_contacts_notified": [
      {"name": "旅行社负责人", "phone": "139****9999"},
      {"name": "子女", "phone": "139****1234"}
    ]
  }
}
```

---

### 1.4 防诈骗预警干预

**场景**：检测到父母可能被带入购物陷阱或遭遇诈骗

```http
POST https://fliggy.com/api/emergency/fraud-alert
Content-Type: application/json

Request:
{
  "traveler_id": "2214118900513",
  "trip_id": "TRIP20260401001",
  "alert_type": "forced_shopping",  // forced_shopping/scam_medical/fake_lottery/other
  "location": {
    "poi": "XX 玉石店",
    "address": "大理市 XX 路 XX 号"
  },
  "risk_evidence": [
    "偏离预定行程路线 2 公里",
    "停留时间超过 90 分钟",
    "检测到异常大额消费意向"
  ],
  "intervention_required": true
}

Response:
{
  "code": 200,
  "data": {
    "alert_id": "FRAUD20260401001",
    "intervention_actions": [
      {
        "action": "voice_reminder",
        "target": "traveler",
        "content": "叔叔阿姨，这个购物点不在行程内...",
        "status": "sent"
      },
      {
        "action": "guide_dispatch",
        "guide_name": "李导游",
        "status": "dispatched"
      },
      {
        "action": "notify_child",
        "contact": "张女士",
        "status": "called"
      }
    ],
    "shopping_spot_warning": {
      "is_authorized": false,
      "complaint_count": 15,
      "risk_level": "high"
    }
  }
}
```

---

## 2. 健康档案服务 ⭐

### 2.1 创建健康档案

**场景**：子女为父母建立健康档案，包含病史、过敏史、用药记录

```http
POST https://fliggy.com/api/health/profile/create
Content-Type: application/json

Request:
{
  "user_id": "2214118900513",
  "travelers": [
    {
      "name": "张父",
      "age": 65,
      "gender": "male",
      "id_no": "510***********1234",
      "phone": "138****5678",
      
      "chronic_conditions": [
        {
          "condition": "高血压",
          "diagnosed_year": 2015,
          "medications": ["硝苯地平缓释片"],
          "dosage": "每天 1 次，每次 1 片"
        },
        {
          "condition": "2 型糖尿病",
          "diagnosed_year": 2018,
          "medications": ["二甲双胍"],
          "dosage": "每天 2 次，每次 0.5g"
        }
      ],
      
      "allergies": [
        {
          "type": "drug",
          "substance": "青霉素",
          "reaction": "皮疹、呼吸困难"
        }
      ],
      
      "surgical_history": [
        {
          "procedure": "阑尾炎手术",
          "year": 2010,
          "hospital": "成都市第一人民医院"
        }
      ],
      
      "regular_medications": [
        {
          "name": "硝苯地平缓释片",
          "dosage": "每天 1 次，每次 1 片",
          "purpose": "降血压"
        },
        {
          "name": "二甲双胍",
          "dosage": "每天 2 次，每次 0.5g",
          "purpose": "降血糖"
        }
      ],
      
      "emergency_contact": {
        "name": "张女士",
        "relation": "女儿",
        "phone": "139****1234"
      },
      
      "preferred_hospital": {
        "name": "成都市第一人民医院",
        "address": "成都市高新区万象北路 18 号",
        "phone": "028-81234567"
      }
    }
  ]
}

Response:
{
  "code": 200,
  "data": {
    "profile_id": "PROFILE20260401001",
    "created_at": "2026-04-01T10:00:00+08:00",
    "travelers_count": 2,
    "qr_code": "data:image/png;base64,...",
    "emergency_card_url": "https://fliggy.com/health/card/xxx.pdf"
  }
}
```

---

### 2.2 查询健康档案

```http
GET https://fliggy.com/api/health/profile/{profile_id}
Authorization: Bearer ${TOKEN}

Response:
{
  "code": 200,
  "data": {
    "profile_id": "PROFILE20260401001",
    "travelers": [
      {
        "name": "张父",
        "age": 65,
        "chronic_conditions": [...],
        "allergies": [...],
        "medications": [...],
        "emergency_contact": {...}
      }
    ],
    "last_updated": "2026-04-01T10:00:00+08:00"
  }
}
```

---

### 2.3 更新健康数据

```http
PUT https://fliggy.com/api/health/profile/{profile_id}/update
Content-Type: application/json

Request:
{
  "traveler_id": "2214118900513",
  "updates": {
    "vital_signs_history": [
      {
        "timestamp": "2026-04-11T14:30:00+08:00",
        "heart_rate": 95,
        "blood_pressure": {"systolic": 150, "diastolic": 95},
        "blood_sugar": 8.5
      }
    ],
    "new_diagnosis": null,
    "medication_changes": null
  }
}

Response:
{
  "code": 200,
  "data": {
    "update_id": "UPDATE20260401001",
    "updated_fields": ["vital_signs_history"],
    "updated_at": "2026-04-11T14:35:00+08:00"
  }
}
```

---

## 调用频率限制

| API 类别 | 频率限制 | 备注 |
|---------|---------|------|
| **紧急救助 API** | **无限制** | **优先保障，任何情况下都可调用** |
| **健康档案 API** | **1000 次/分钟** | 按用户维度 |

---

## 错误码说明

| 错误码 | 说明 | 处理方式 |
|-------|------|---------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | 检查请求参数 |
| 401 | 认证失败 | 刷新 Token |
| 403 | 权限不足 | 申请权限 |
| 404 | 资源不存在 | 检查资源 ID |
| 429 | 请求频率超限 | 降低调用频率 |
| 500 | 服务器内部错误 | 重试或联系技术支持 |
| 503 | 服务不可用 | 切换备用服务 |

**紧急救助特殊规则**：
- 即使认证失败，也会先执行救助再补验证
- 网络不佳时自动切换短信通道
- 7x24 小时服务保障，无维护窗口

---

**文档维护者**: 汪小玲 (苏英)  
**所属部门**: 飞猪 -CTO 线 - 技术质量 - 服务质量  
**创建日期**: 2026-04-01  
**版本**: v3.0（父母视角重构）