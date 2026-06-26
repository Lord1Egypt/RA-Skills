---
name: coros-data-skill
description: 查询高驰（COROS）运动手表的运动数据。当用户询问"高驰(COROS)运动数据"、"高驰(COROS)跑步记录"等相关问题时触发。
---

## 功能说明

本 skill 通过调用 COROS 官方 API，实现以下功能：

1. **账号登录**：使用 COROS 账号（手机号/邮箱）和 MD5 加密密码登录，获取 `accessToken`。
2. **查询运动活动列表**：按日期范围查询跑步相关活动记录，支持以下运动模式：
   - `100` - 户外跑步
   - `101` - 室内跑步
   - `102` - 越野跑
   - `103` - 跑步机

## 环境变量配置

在 `scripts/.env` 文件中配置以下变量：

```env
COROS_ACCOUNT=<你的 COROS 账号（手机号或邮箱）>
COROS_PASSWORD=<账号密码的 MD5 加密值>
```

## 使用方式

```js
import { CorosClient } from "./coros.js";

const client = new CorosClient(process.env.COROS_ACCOUNT, process.env.COROS_PASSWORD);
await client.login();

// 查询指定日期范围内的跑步活动（日期格式：YYYYMMDD）
const activities = await client.fetchActivity("20260303", "20260307");
activities.forEach(activity => {  
  console.log("date:",activity.date, "distance:",activity.distance); 
});
```

## API 说明

| 方法 | 参数 | 说明 |
|------|------|------|
| `login()` | 无 | 登录并初始化鉴权 axios 实例 |
| `fetchActivity(startDay, endDay)` | `startDay`: 开始日期（YYYYMMDD）<br>`endDay`: 结束日期（YYYYMMDD） | 查询指定日期范围内的跑步活动列表，默认查询 `20260303` ~ `20260307` |

## 工具方法（util.js）

### 生成加密密码

使用 `genHashedPassword` 将明文密码转换为 MD5 加密值，用于配置 `COROS_PASSWORD` 环境变量：

```js
import { genHashedPassword } from "./util.js";

const hashedPassword = genHashedPassword("your_plain_password");
console.log(hashedPassword); // 输出 MD5 加密后的密码，填入 .env 的 COROS_PASSWORD
```

### 计算某时间段总跑量

使用 `computeDistance` 对 `fetchActivity` 返回的活动列表求总距离（单位：米），再转换为公里：

```js
import { CorosClient } from "./coros.js";
import { computeDistance } from "./util.js";

const client = new CorosClient(process.env.COROS_ACCOUNT, process.env.COROS_PASSWORD);
await client.login();

// 查询指定日期范围内的跑步活动
const activities = await client.fetchActivity("20260101", "20260310");

// 计算总跑量（distance 单位为米，除以 1000 转换为公里）
const totalMeters = computeDistance(activities);
console.log(`总跑量：${(totalMeters / 1000).toFixed(2)} km`);
```

## 工具方法 API 说明

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `genHashedPassword(password)` | `password`: 明文密码 | `string` MD5 加密后的密码 | 用于生成 `.env` 中 `COROS_PASSWORD` 的值 |
| `computeDistance(activities)` | `activities`: 活动列表数组 | `number` 总距离（单位：米） | 对活动列表中所有 `distance` 字段求和 |
