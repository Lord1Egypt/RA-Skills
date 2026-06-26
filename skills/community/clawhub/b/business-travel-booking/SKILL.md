---
name: fb-booking-skill
description: Booking.com国际酒店预订助手，支持全球酒店搜索、房型查询、价格对比、预订管理。Invoke when user wants to search international hotels, book hotels on Booking.com, or manage Booking.com reservations.
version: 1.0.0
metadata: {"openclaw": {"emoji": "🌍", "category": "travel", "tags": ["Booking", "国际酒店", "海外酒店", "缤客", "全球预订"], "requires": {"bins": ["python3"]}, "required": true}}
---
# Booking.com国际酒店预订助手 (fb-booking-skill)

## 技能描述

Booking.com国际酒店预订助手，支持全球200+国家和地区酒店搜索、房型查询、价格对比、预订管理。提供多语言、多币种支持，适合出境游、商务差旅等国际出行场景。

---

⚠️ 【重要约束】
- 必须调用Booking.com Affiliate API或合作伙伴API获取数据
- 禁止自行编造酒店信息、价格或评论
- 国际酒店价格以当地货币显示，需标注汇率参考
- 接口返回什么数据就展示什么，不要修改

---

## 技能概述

基于Booking.com API开发的国际酒店预订技能，支持：
- 全球酒店搜索（200+国家/地区）
- 多语言酒店信息展示
- 多币种价格显示
- 实时房态查询
- 预订创建与管理
- 免费取消政策查询

## 技能能力

### 核心能力

1. **全球酒店搜索**：支持按城市、地标、酒店名称搜索
2. **多语言支持**：中文、英文、日文、韩文等多语言展示
3. **多币种显示**：支持CNY、USD、EUR、JPY等货币
4. **房型详情**：床型、面积、设施、政策等详细信息
5. **预订管理**：创建订单、查询订单、取消订单

### 触发条件

1. **国际酒店搜索**：当用户搜索海外酒店、Booking酒店时
   - 支持城市名（英文/中文）
   - 支持地标（如东京塔、埃菲尔铁塔）
   - 支持酒店名称

2. **展示格式示例**：
   ```
   🌍 Booking.com - 东京酒店（3月15日入住）
   
   | 序号 | 酒店名称 | 评分 | 区域 | 价格/晚 |
   |:---:|---------|:---:|------|---:|
   | 1 | 东京站酒店 | 9.2 | 千代田区 | ¥1,280 |
   | 2 | 新宿格拉斯丽酒店 | 8.8 | 新宿区 | ¥980 |
   
   💡 回复"序号"查看房型详情
   💡 价格已含税费，支持免费取消
   ```

## 对接信息

### 基础配置

- API文档：https://distribution-xml.booking.com/json/bookings.getHotels
- 认证方式：API Key
- 支持格式：JSON/XML
- 速率限制：1000次/小时

### 支持功能

| 功能 | API端点 | 说明 |
|:---|:---|:---|
| 酒店搜索 | getHotels | 按城市/坐标搜索 |
| 酒店详情 | getHotelDescription | 酒店详细信息 |
| 房型查询 | getRoomAvailability | 实时房态和价格 |
| 预订创建 | makeReservation | 创建预订 |
| 订单查询 | getReservation | 查询订单详情 |
| 取消预订 | cancelReservation | 取消预订 |

## 核心接口列表

### 一、查询类接口

| 接口名称 | 核心用途 | 必选参数 |
|---------|---------|---------|
| search_booking_hotels | 搜索Booking酒店 | city_ids, checkin, checkout |
| get_booking_hotel_detail | 获取酒店详情 | hotel_id, language |
| get_booking_room_availability | 查询房型可用性 | hotel_id, checkin, checkout |
| get_booking_reviews | 获取酒店评论 | hotel_id, language |

### 二、预订类接口

| 接口名称 | 核心用途 | 必选参数 |
|---------|---------|---------|
| create_booking_reservation | 创建预订 | hotel_id, room_id, guest_info |
| get_booking_reservation | 查询预订 | reservation_id |
| cancel_booking_reservation | 取消预订 | reservation_id |

## 数据字段说明

### 酒店信息

```json
{
  "hotel_id": "123456",
  "name": "Hotel Granvia Tokyo",
  "name_cn": "东京站酒店",
  "address": "1-9-1 Marunouchi, Chiyoda-ku",
  "city": "Tokyo",
  "country": "Japan",
  "zip": "100-0005",
  "latitude": 35.6812,
  "longitude": 139.7671,
  "review_score": 9.2,
  "review_count": 8542,
  "star_rating": 4,
  "currency": "JPY",
  "min_rate": 25000
}
```

### 房型信息

```json
{
  "room_id": "987654",
  "name": "Deluxe Double Room",
  "name_cn": "豪华双人间",
  "bed_type": "1 extra-large double bed",
  "size": 28,
  "max_occupancy": 2,
  "facilities": ["Air conditioning", "Free WiFi", "TV"],
  "cancellation_policy": "Free cancellation",
  "meal_plan": "Breakfast included",
  "price": 28000
}
```

## 多语言支持

| 语言代码 | 语言 |
|:---|:---|
| zh | 中文 |
| en | 英文 |
| ja | 日文 |
| ko | 韩文 |
| fr | 法文 |
| de | 德文 |
| es | 西班牙文 |

## 多币种支持

| 币种代码 | 币种 |
|:---|:---|
| CNY | 人民币 |
| USD | 美元 |
| EUR | 欧元 |
| JPY | 日元 |
| KRW | 韩元 |
| GBP | 英镑 |
| HKD | 港币 |

## 响应规则

### 成功响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "hotel_id": "123456",
    "name": "东京站酒店",
    "address": "东京都千代田区丸之内1-9-1",
    "review_score": 9.2,
    "rooms": [
      {
        "room_id": "987654",
        "name": "豪华双人间",
        "price": 28000,
        "currency": "JPY"
      }
    ]
  }
}
```

### 失败响应

```json
{
  "code": 500,
  "msg": "Hotel not found",
  "data": null
}
```
