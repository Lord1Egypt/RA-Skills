# 佳明 Connect 接口参考（非官方）

本文档说明通过 `garminconnect` Python 库访问的非官方佳明 Connect 接口。

## 重要提示

- **非官方接口**：佳明并未向个人用户提供公开接口，该库是对其网页版功能的逆向实现。
- **可能失效**：佳明随时可能调整接口，导致库不可用
- **请求频率限制**：佳明实施了频率限制，请求过于频繁可能导致账号被临时封禁
- **官方替代方案**：佳明 Health API 仅面向企业合作开放

## 登录认证

### 依赖库：`garminconnect`
```bash
pip3 install garminconnect
```

### 认证流程
1. 使用邮箱/密码登录
2. 由库完成 OAuth 令牌交换
3. 令牌保存后可用于恢复会话
4. 令牌过期后自动刷新

### 会话管理
```python
from garminconnect import Garmin

# 首次登录
client = Garmin(email, password)
client.login()

# 保存令牌以便复用
oauth1 = client.garth.oauth1_token
oauth2 = client.garth.oauth2_token

# 恢复会话
client = Garmin()
client.garth.oauth1_token = oauth1
client.garth.oauth2_token = oauth2
```

> 提示：中国大陆账户需使用 `Garmin(email, password, is_cn=True)`，连接佳明中国服务器（connect.garmin.cn）。

## 核心接口

### 用户资料
```python
# 姓名
client.get_full_name()

# 用户摘要（每日统计）
client.get_user_summary("2026-01-25")
```

### 睡眠数据
```python
# 每日睡眠详情
client.get_sleep_data("2026-01-25")
```

**返回结构：**
```json
{
  "sleepTimeSeconds": 28800,      // 总睡眠时长（秒）
  "deepSleepSeconds": 7200,       // 深睡（秒）
  "lightSleepSeconds": 14400,     // 浅睡（秒）
  "remSleepSeconds": 7200,        // 快速眼动睡眠（秒）
  "awakeSleepSeconds": 1800,      // 清醒时间（秒）
  "sleepScores": {
    "overall": {"value": 85},     // 综合睡眠评分（0-100）
    "duration": {...},
    "quality": {...}
  },
  "restlessMoments": 12,          // 不安（翻身）次数
  "avgSleepHeartRate": 52,        // 睡眠期间平均心率
  "avgSleepHRV": 45,              // 睡眠期间平均心率变异性
  "avgSleepRespiration": 14       // 呼吸频率（次/分）
}
```

### 心率变异性数据
```python
# 每日心率变异性摘要
client.get_hrv_data("2026-01-25")
```

**返回结构：**
```json
{
  "hrvSummary": {
    "lastNightAvg": 45,             // 昨晚心率变异性平均值（毫秒）
    "lastNight5MinHigh": 68,        // 5 分钟最高值
    "lastNight5MinLow": 28,         // 5 分钟最低值
    "weeklyAvg": 42,                // 7 天滚动平均值
    "baselineBalancedLow": 38,      // 个人基准下限
    "baselineBalancedHigh": 48,     // 个人基准上限
    "status": "BALANCED"            // 状态：平衡（BALANCED）、失衡（UNBALANCED）、较差（POOR）、偏低（LOW）
  }
}
```

### 身体电量
```python
# 每日身体电量读数（时间序列）
client.get_body_battery("2026-01-25")
```

**返回结构：**
```json
[
  {
    "timestamp": 1737849600000,     // Unix 时间戳（毫秒）
    "value": 85,                    // 身体电量数值（0-100）
    "charged": 45,                  // 夜间充电量
    "drained": 15                   // 相比上一点的耗电量
  }
  // ... 全天更多读数
]
```

### 心率
```python
# 每日心率摘要
client.get_heart_rates("2026-01-25")
```

**返回结构：**
```json
{
  "restingHeartRate": 52,           // 静息心率（次/分）
  "maxHeartRate": 165,              // 当日最高心率
  "minHeartRate": 48                // 当日最低心率
}
```

### 压力水平
```python
# 每日压力数据
client.get_stress_data("2026-01-25")
```

**返回结构：**
```json
{
  "avgStressLevel": 35,             // 全天平均压力（0-100）
  "maxStressLevel": 78,             // 压力峰值
  "restStressLevel": 15,            // 休息时压力
  "activityStressLevel": 65,        // 活动时压力
  "lowStressDuration": 14400,       // 低压力（0-25）时长（秒）
  "mediumStressDuration": 28800,    // 中压力（26-50）时长（秒）
  "highStressDuration": 7200        // 高压力（51-100）时长（秒）
}
```

### 活动
```python
# 获取指定日期范围内的活动
client.get_activities_by_date("2026-01-01", "2026-01-31", activitytype="")
```

**返回结构：**
```json
[
  {
    "activityId": 123456789,
    "activityType": {
      "typeKey": "running",
      "typeId": 1
    },
    "activityName": "晨跑",
    "startTimeLocal": "2026-01-25 07:30:00",
    "duration": 3600,               // 时长（秒）
    "distance": 10000,              // 距离（米）
    "calories": 650,                // 消耗卡路里
    "averageHR": 152,               // 平均心率
    "maxHR": 178,                   // 最高心率
    "elevationGain": 120,           // 累计爬升（米）
    "averageSpeed": 2.78,           // 速度（米/秒）
    "averageRunningCadence": 165    // 步频（步/分）
  }
]
```

### 步数与每日汇总
```python
# 每日统计摘要
client.get_user_summary("2026-01-25")
```

**返回结构：**
```json
{
  "totalSteps": 12543,
  "totalKilocalories": 2456,
  "activeKilocalories": 856,
  "bmrKilocalories": 1600,
  "intensityMinutesGoal": 150,
  "vigorousIntensityMinutes": 35,
  "moderateIntensityMinutes": 85
}
```

## 数据可用性

### 所需设备功能

| 指标 | 所需硬件 |
|------|----------|
| **睡眠阶段** | 较新的佳明手表（2018 年及以后） |
| **身体电量** | 支持 Firstbeat 且可测心率变异性的设备 |
| **心率变异性** | 配备光学心率传感器的设备 |
| **压力** | 支持全天心率监测的设备 |
| **最大摄氧量** | 具备 GPS + 心率的运动记录 |
| **呼吸频率** | 较新的设备（Fenix 6 及以上、Venu 2 及以上等） |

### 历史数据
- 大多数指标：可查询账号全部历史
- 心率变异性：旧设备可能受限
- 身体电量：需要兼容设备支持

## 请求频率限制

佳明对其接口实施了频率限制：

**实测限制：**
- 约 10 分钟内 50-100 次请求（视情况浮动）
- 请求过于频繁会触发 IP/账号临时封禁
- 封禁通常持续 15-60 分钟

**最佳实践：**
- 尽可能将数据缓存到本地
- 避免过度轮询（数据更新每小时最多查询一次）
- 尽量使用日期范围查询，而不是逐日循环请求
- 批量请求之间增加延时（1-2 秒）

## 错误处理

### 常见错误

**认证失败**
```
GarminConnectAuthenticationError
```
- 账号或密码错误
- 账号被锁定
- 开启了两步验证（暂不支持）

**连接错误**
```
GarminConnectConnectionError
```
- 网络问题
- 佳明服务器故障
- 触发频率限制

**无数据**
- 返回 `None` 或空列表
- 设备未佩戴
- 用户设备不支持该指标
- 该日期没有数据

## 依赖库文档

- **库名**：garminconnect（通过 `pip3 install garminconnect` 安装）
- 注意：该库为社区维护的非官方库，佳明接口变更时需更新库版本

## 替代方案：佳明官方 Health API

面向企业/商业用途：
- **佳明 Health API**：需要签订合作协议
- **适用场景**：应用集成、健康平台
- **不适用**：个人业余项目

更多信息：https://www.garmin.com/en-US/health-enterprise/

## 与 Whoop 接口对比

| 功能 | 佳明（非官方） | Whoop（官方） |
|------|----------------|---------------|
| **认证方式** | 邮箱/密码 | OAuth 2.0 |
| **稳定性** | 可能随时失效 | 稳定、有版本管理 |
| **频率限制** | 未公开（约 10 分钟 50 次） | 已公开（每小时 200 次） |
| **数据范围** | 全部历史 | 全部历史 |
| **技术支持** | 社区维护的库 | 官方支持 |
| **服务条款** | 灰色地带 | 官方支持 |

## 服务条款注意事项

**重要提示**：使用非官方接口可能违反佳明的服务条款，请自行承担风险：

- 仅限**个人使用**
- 不要以此为基础开发商业产品
- 不要进行过量抓取
- 生产环境请考虑佳明官方 Health API

## 提升稳定性的建议

1. **积极缓存**：数据保存到本地，仅请求新的日期
2. **错误恢复**：失败时按指数退避策略重试
3. **关注库更新**：留意 GitHub 上的破坏性变更
4. **准备备用方案**：接口失效时可从佳明 Connect 网页版手动导出 CSV
5. **使用前先验证**：与佳明 Connect 网页版核对数据准确性

## 常用资源

- [佳明 Connect 网页版](https://connect.garmin.com)：官方界面
- [佳明官方论坛](https://forums.garmin.com)：官方社区支持
