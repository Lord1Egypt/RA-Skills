
# Intervals.icu API 文档摘要

本文档总结了 Intervals.icu API 的关键端点和数据结构，供 `fitness-personal-assistant` 技能使用。

## 基本信息

- **Base URL**: `https://intervals.icu/api/v1`
- **Authentication**: Basic Auth (Username: `API_KEY`, Password: `YOUR_API_KEY`) 或 Bearer Token。

## 关键端点

### 1. 运动员信息 (Athlete)

-   **获取运动员详情**: `GET /athlete/{id}`
    -   获取运动员的详细信息，包括心率区间、功率区间等设置。
-   **获取运动员摘要**: `GET /athlete/{id}/athlete-summary`
    -   获取运动员的健康和体能摘要（Fitness, Fatigue, Form 等）。

### 2. 活动 (Activities)

-   **列出活动**: `GET /athlete/{id}/activities`
    -   参数: `oldest` (ISO-8601), `newest` (ISO-8601)。
    -   返回指定日期范围内的活动列表。
-   **获取单个活动**: `GET /activity/{id}`
    -   参数: `intervals` (boolean, 是否包含间隔数据)。
-   **上传活动**: `POST /athlete/{id}/activities`
    -   上传 .fit, .tcx, .gpx 等文件。

### 3. 事件与训练计划 (Events & Library)

-   **列出事件**: `GET /athlete/{id}/events`
    -   参数: `oldest`, `newest`。
    -   获取日历上的事件（计划的训练、笔记等）。
-   **创建事件**: `POST /athlete/{id}/events`
    -   在日历上创建新的训练或笔记。
-   **列出训练库**: `GET /athlete/{id}/workouts`
    -   获取运动员训练库中的所有训练。

### 4. 健康数据 (Wellness)

-   **获取健康记录**: `GET /athlete/{id}/wellness/{date}`
-   **更新健康记录**: `PUT /athlete/{id}/wellness/{date}`
    -   更新体重、静息心率、睡眠、HRV 等数据。

## 关键数据结构

### Activity (活动)
-   `id`: String
-   `start_date_local`: String (ISO-8601)
-   `type`: String (Run, Ride, Swim etc.)
-   `moving_time`: Integer (seconds)
-   `distance`: Float (meters)
-   `total_elevation_gain`: Float (meters)
-   `average_heartrate`: Integer
-   `average_watts`: Integer
-   `icu_training_load`: Integer (TSS)

### Wellness (健康)
-   `id`: String (Date ISO-8601)
-   `weight`: Float
-   `restingHR`: Integer
-   `hrv`: Float
-   `sleepSecs`: Integer
-   `sleepScore`: Float

### Event (事件/计划训练)
-   `id`: Integer
-   `category`: String (WORKOUT, NOTE, etc.)
-   `start_date_local`: String
-   `name`: String
-   `description`: String (支持结构化训练描述)

## 示例用法

### 获取最近的活动
```http
GET /api/v1/athlete/{id}/activities?oldest=2023-01-01&newest=2023-01-31
```

### 获取健康摘要
```http
GET /api/v1/athlete/{id}/athlete-summary
```

### 创建计划训练
```http
POST /api/v1/athlete/{id}/events
Content-Type: application/json

{
  "category": "WORKOUT",
  "start_date_local": "2023-10-27T10:00:00",
  "name": "Intervals",
  "description": "Warmup\n- 10m 50%\n\nMain Set\n- 5x 3m 100%\n- 3m 50%\n\nCooldown\n- 10m 50%",
  "type": "Ride"
}
```
