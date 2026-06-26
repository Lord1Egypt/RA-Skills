---
name: tool-api-reference
title: API 接口参考清单
description: 自由行旅游出行管家所需的完整 API 接口清单，包含接口地址、请求参数、返回格式和使用示例
author: 汪小玲 (苏英)
department: 飞猪-CTO 线 - 技术质量 - 服务质量
version: 1.0
created_at: 2026-04-01
tags:
  - API
  - 接口文档
  - 工具参考
---

# API 接口参考清单

## 目录

1. [飞猪内部 API](#1-飞猪内部-api)
2. [阿里云 AI 服务](#2-阿里云 ai-服务)
3. [钉钉开放平台](#3-钉钉开放平台)
4. [第三方服务](#4-第三方服务)
5. [自研服务](#5-自研服务)

---

## 1. 飞猪内部 API

### 1.1 订单中心

#### 查询订单列表

```http
GET https://open.fliggy.com/order/api/v1/list
Content-Type: application/json
Authorization: Bearer ${ACCESS_TOKEN}

Request:
{
  "user_id": "2214118900513",
  "trip_status": "pending",  // pending/traveling/completed
  "product_types": ["flight", "hotel", "tour", "transfer"],
  "date_range": {
    "start": "2026-04-01",
    "end": "2026-04-30"
  }
}

Response:
{
  "code": 200,
  "data": {
    "orders": [
      {
        "order_id": "ORDER123456",
        "type": "flight",
        "status": "paid",
        "service_time": "2026-04-10T10:30:00+08:00",
        "amount": 258000,  // 分
        "traveler_info": {
          "names": ["张父", "李母"]
        }
      }
    ],
    "total": 5
  }
}
```

#### 获取订单详情

```http
GET https://open.fliggy.com/order/api/v1/detail/{order_id}

Response:
{
  "code": 200,
  "data": {
    "order_id": "ORDER123456",
    "type": "flight",
    "product_name": "北京 - 昆明 往返机票",
    "service_details": {
      "flight_no": "CA1234",
      "departure": {
        "airport": "PEK",
        "terminal": "T3",
        "time": "2026-04-10T10:30:00+08:00"
      },
      "arrival": {
        "airport": "KMG",
        "terminal": "T1",
        "time": "2026-04-10T13:45:00+08:00"
      },
      "passengers": [
        {"name": "张父", "id_type": "身份证", "id_no": "510***********1234"},
        {"name": "李母", "id_type": "身份证", "id_no": "510***********5678"}
      ]
    },
    "contact_info": {
      "airline_service": "95583",
      "transfer_service": {
        "driver_name": "王师傅",
        "driver_phone": "138****5678",
        "car_plate": "京 A·XXXXX"
      }
    }
  }
}
```

---

### 1.2 行程单生成

#### 生成 H5 行程单

```http
POST https://fliggy.com/api/itinerary/generate/h5
Content-Type: application/json

Request:
{
  "trip_id": "TRIP20260401001",
  "order_ids": ["ORDER123456", "ORDER789012"],
  "message_from_child": "亲爱的爸爸妈妈...",
  "voice_message_url": "https://oss.fliggy.com/voice/xxx.mp3",
  "share_settings": {
    "enable_wechat": true,
    "enable_dingtalk": true,
    "enable_qrcode": true
  }
}

Response:
{
  "code": 200,
  "data": {
    "itinerary_id": "ITINERARY20260401001",
    "h5_url": "https://fliggy.com/itinerary/h5/xxx",
    "qr_code": "data:image/png;base64,...",
    "preview_image": "https://img.fliggy.com/preview/xxx.jpg",
    "created_at": "2026-04-01T15:30:00+08:00"
  }
}
```

---

### 1.3 评价系统

#### 提交评价

```http
POST https://fliggy.com/api/review/submit
Content-Type: application/json

Request:
{
  "order_id": "ORDER123456",
  "traveler_id": "2214118900513",
  "rating": 5,
  "dimension_ratings": {
    "punctuality": 5,
    "attitude": 5,
    "driving": 5,
    "cleanliness": 5
  },
  "tags": ["准时", "态度好", "驾驶平稳"],
  "comment": "司机师傅很准时，提前 10 分钟就到了",
  "media": [
    {
      "type": "image",
      "url": "https://img.fliggy.com/review/xxx.jpg"
    }
  ]
}

Response:
{
  "code": 200,
  "data": {
    "review_id": "REVIEW20260401001",
    "status": "published",  // published/pending/under_review
    "credit_delta": +5,
    "published_at": "2026-04-01T16:00:00+08:00"
  }
}
```

---

## 2. 阿里云 AI 服务

### 2.1 智能语音交互

#### 语音外呼

```http
POST https://voice.cn-shanghai.aliyuncs.com/2018-05-18/outbound/calls
Content-Type: application/json
Authorization: ACS ${ACCESS_KEY_ID}:${SIGNATURE}

Request:
{
  "CalledNumber": "138****5678",
  "CalledShowNumber": "95XXX",
  "TtsCode": "VOICE_20260401001",
  "Variables": {
    "driver_name": "王师傅",
    "pickup_time": "明天上午 8 点",
    "pickup_location": "小区北门"
  }
}

Response:
{
  "Code": "OK",
  "Message": "成功",
  "Data": {
    "CallId": "CALL20260401001",
    "Status": "INITIATING"
  }
}
```

#### 语音识别（ASR）

```http
POST https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/transcription
Content-Type: application/octet-stream
X-NLS-Token: ${TOKEN}

Request: PCM 音频流

Response:
{
  "status": "completed",
  "result": {
    "text": "没问题，都记下了。明天 8 点小区北门见。",
    "confidence": 0.95
  }
}
```

---

### 2.2 NLP 服务

#### 情感分析

```http
POST https://nlp.cn-shanghai.aliyuncs.com/sentiment/analyze
Content-Type: application/json
Authorization: Bearer ${TOKEN}

Request:
{
  "text": "司机师傅很准时，提前 10 分钟就到了，车也很干净，开得很稳",
  "type": "general"
}

Response:
{
  "code": 200,
  "data": {
    "sentiment": "positive",
    "score": 0.92,
    "confidence": 0.96,
    "keywords": [
      {"word": "准时", "sentiment": "positive", "score": 0.95},
      {"word": "干净", "sentiment": "positive", "score": 0.88},
      {"word": "稳", "sentiment": "positive", "score": 0.90}
    ]
  }
}
```

#### 关键词提取

```http
POST https://nlp.cn-shanghai.aliyuncs.com/keywords/extract
Content-Type: application/json

Request:
{
  "text": "导游讲解很专业，但是时间安排有点紧，老人跟不上节奏",
  "limit": 5
}

Response:
{
  "code": 200,
  "data": {
    "keywords": [
      {"word": "导游", "weight": 0.85},
      {"word": "专业", "weight": 0.78},
      {"word": "时间安排", "weight": 0.72},
      {"word": "老人", "weight": 0.65}
    ]
  }
}
```

---

### 2.3 视觉智能

#### 人脸识别

```http
POST https://vision.cn-shanghai.aliyuncs.com/face/detect
Content-Type: application/json

Request:
{
  "image_url": "https://img.fliggy.com/photo/xxx.jpg",
  "attributes": ["quality", "emotion", "pose"]
}

Response:
{
  "code": 200,
  "data": {
    "faces": [
      {
        "face_id": "FACE001",
        "bounding_box": {"x": 100, "y": 150, "width": 200, "height": 250},
        "quality": {
          "clarity": 0.88,
          "brightness": 0.75,
          "overall_score": 0.85
        },
        "pose": {
          "yaw": 5.2,
          "pitch": -3.1,
          "roll": 1.5,
          "frontal_score": 0.92
        }
      }
    ],
    "face_count": 1
  }
}
```

#### 场景分类

```http
POST https://vision.cn-shanghai.aliyuncs.com/image/classify/scene
Content-Type: application/json

Request:
{
  "image_url": "https://img.fliggy.com/photo/xxx.jpg",
  "limit": 3
}

Response:
{
  "code": 200,
  "data": {
    "scenes": [
      {"label": "attraction", "name": "景点", "confidence": 0.92},
      {"label": "outdoor", "name": "户外", "confidence": 0.78},
      {"label": "building", "name": "建筑", "confidence": 0.65}
    ]
  }
}
```

---

### 2.4 视频云

#### AI 视频生成

```http
POST https://video.cn-shanghai.aliyuncs.com/ai/generate
Content-Type: application/json

Request:
{
  "template_id": "warm_family_version",
  "materials": {
    "photos": [
      {"url": "https://img.fliggy.com/photo/001.jpg", "duration": 5},
      {"url": "https://img.fliggy.com/photo/002.jpg", "duration": 4}
    ],
    "videos": [
      {"url": "https://video.fliggy.com/clip/001.mp4", "trim": [0, 10]}
    ]
  },
  "music": {
    "music_id": "MUSIC001",
    "volume": 0.6
  },
  "settings": {
    "resolution": "1080p",
    "fps": 30,
    "format": "mp4",
    "filters": ["warm_memory"],
    "transitions": ["cross_dissolve"]
  }
}

Response:
{
  "code": 200,
  "data": {
    "job_id": "JOB20260401001",
    "status": "processing",
    "estimated_time": 300,  // 秒
    "progress": 0
  }
}

// 轮询进度
GET https://video.cn-shanghai.aliyuncs.com/ai/job/JOB20260401001

Response:
{
  "code": 200,
  "data": {
    "job_id": "JOB20260401001",
    "status": "completed",
    "progress": 100,
    "result": {
      "video_url": "https://video.fliggy.com/result/xxx.mp4",
      "cover_url": "https://img.fliggy.com/cover/xxx.jpg",
      "duration": 195,  // 秒
      "file_size": 52428800  // 字节
    }
  }
}
```

---

## 3. 钉钉开放平台

### 3.1 消息推送

#### 发送工作通知

```http
POST https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2
Content-Type: application/json
access_token: ${ACCESS_TOKEN}

Request:
{
  "agent_id": 123456,
  "userid_list": "2214118900513",
  "msgtype": "markdown",
  "markdown": {
    "title": "行程提醒",
    "text": "## 📅 Day 2 · 大理古城一日游\n\n**时间**: 2026-04-11 星期六  \n**天气**: 多云 15-23℃\n\n⏰ **08:30** 酒店大堂集合  \n👨‍🦰 导游：王导 138****5678\n\n[查看详情](https://fliggy.com/itinerary/xxx)"
  }
}

Response:
{
  "errcode": 0,
  "errmsg": "ok",
  "task_id": 123456789
}
```

---

## 4. 第三方服务

### 4.1 高德地图 API

#### 地点搜索

```http
GET https://restapi.amap.com/v3/place/text?key=${KEY}&keywords=大理古城&city=大理&output=json

Response:
{
  "status": "1",
  "pois": [
    {
      "name": "大理古城",
      "location": "100.164912,25.694826",
      "address": "大理市一塔路 42 号"
    }
  ]
}
```

#### 路径规划

```http
GET https://restapi.amap.com/v3/direction/driving?origin=100.164912,25.694826&destination=100.152345,25.703456&key=${KEY}

Response:
{
  "status": "1",
  "route": {
    "distance": 3500,  // 米
    "duration": 720,   // 秒
    "paths": [...]
  }
}
```

---

### 4.2 中国气象网

#### 天气预报

```http
GET http://www.nmc.cn/rest/weather?stationId=56778

Response:
{
  "code": 200,
  "data": {
    "city": "大理",
    "forecasts": [
      {
        "date": "2026-04-11",
        "weather": "多云",
        "temp_high": 23,
        "temp_low": 15,
        "wind": "西南风 2-3 级"
      }
    ]
  }
}
```

---

## 5. 自研服务

### 5.1 授权服务

#### 生成电子授权书

```http
POST https://fliggy.com/api/auth/letter/generate
Content-Type: application/json

Request:
{
  "trip_id": "TRIP20260401001",
  "child_info": {
    "name": "张女士",
    "phone": "139****1234",
    "id_no": "510***********9999"
  },
  "traveler_info": {
    "name": "张父",
    "phone": "138****5678",
    "id_no": "510***********1234",
    "relation": "父女"
  },
  "order_ids": ["ORDER123456", "ORDER789012"],
  "validity_period": {
    "start": "2026-04-10",
    "end": "2026-04-15"
  }
}

Response:
{
  "code": 200,
  "data": {
    "letter_id": "AUTH20260401001",
    "letter_url": "https://fliggy.com/auth/letter/xxx",
    "qr_code": "data:image/png;base64,...",
    "verification_code": "8866",
    "pdf_download": "https://fliggy.com/auth/letter/xxx.pdf"
  }
}
```

---

### 5.2 航班动态监控

#### 查询航班状态

```http
GET https://fliggy.com/api/flight/status?flight_no=CA1234&date=2026-04-10

Response:
{
  "code": 200,
  "data": {
    "flight_no": "CA1234",
    "status": "delayed",  // on_time/delayed/cancelled/landed
    "scheduled_departure": "2026-04-10T10:30:00+08:00",
    "estimated_departure": "2026-04-10T14:30:00+08:00",
    "delay_reason": "流量控制",
    "gate": "C12",
    "terminal": "T3"
  }
}
```

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

---

## 调用频率限制

| API 类别 | 频率限制 | 备注 |
|---------|---------|------|
| 飞猪订单 API | 100 次/分钟 | 按用户维度 |
| 阿里云 NLP | 50 次/秒 | 按账号维度 |
| 阿里云语音 | 10 次/秒 | 外呼呼叫 |
| 钉钉消息推送 | 200 次/秒 | 按应用维度 |
| 高德地图 API | 100 次/秒 | 按 Key 维度 |
| 视频生成 | 10 次/分钟 | 异步任务 |

---

**文档维护者**: 汪小玲 (苏英)  
**最后更新**: 2026-04-01
