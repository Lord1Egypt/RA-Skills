# Garmin Connect API 文档

## 认证

所有请求携带：
```
Authorization: Bearer <JWT_TOKEN>
nk: NT
Accept: application/json
```

## 基础信息

| 项目 | 值 |
|------|---|
| API Base | `https://connect.garmin.cn` |
| 用户ID | 从用户信息API获取 |
| 日期格式 | `YYYY-MM-DD`（本地时间） |

## API 端点

### 用户信息

```
GET /userprofile-service/userprofile/user-settings
```

响应：
```json
{
  "userId": 116181268,
  "displayName": "YangXing",
  "email": "2461252@qq.com",
  "firstName": "",
  "lastName": ""
}
```

### 每日摘要

```
GET /daily-summary-api/summary/daily/{date}
```

主要字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| totalSteps | int | 当日总步数 |
| totalDistance | int | 距离（米） |
| activeKilocalories | int | 消耗卡路里 |
| totalFloorsAscended | int | 爬楼层数 |
| sleepingDuration | str | 睡眠时长（秒） |
| restingHeartRate | int | 静息心率 |

### 活动列表

```
GET /activitylist-service/activities/{userId}?limit=10&start=0
```

主要字段：
| 字段 | 类型 | 说明 |
|------|------|------|
| startTimeLocal | str | 开始时间 |
| activityType.typeKey | str | 运动类型 |
| distance | float | 距离（米） |
| duration | float | 时长（秒） |
| activeKilocalories | int | 卡路里 |

### 心率数据

```
GET /usersummaryservice/api/summary/{userId}/daily/{date}
```

字段：
| 字段 | 说明 |
|------|------|
| restingHeartRate | 静息心率 |
| averageRestingHeartRate | 平均静息心率 |
| minHeartRate | 最低心率 |
| maxHeartRate | 最高心率 |

## Python 调用模板

```python
import requests

class GarminClient:
    def __init__(self, jwt, user_id=None):
        self.jwt = jwt
        self.headers = {
            'Authorization': f'Bearer {jwt}',
            'nk': 'NT',
            'Accept': 'application/json'
        }
        self.base = 'https://connect.garmin.cn'
        if user_id:
            self.user_id = user_id
        else:
            self.user_id = self.get_user_id()
    
    def get_user_id(self):
        r = requests.get(
            f'{self.base}/userprofile-service/userprofile/user-settings',
            headers=self.headers
        )
        return r.json()['userId']
    
    def daily_summary(self, date):
        r = requests.get(
            f'{self.base}/daily-summary-api/summary/daily/{date}',
            headers=self.headers
        )
        return r.json()
    
    def activities(self, limit=10):
        r = requests.get(
            f'{self.base}/activitylist-service/activities/{self.user_id}',
            params={'limit': limit},
            headers=self.headers
        )
        return r.json()
```
