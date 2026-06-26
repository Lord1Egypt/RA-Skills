---
name: garmin-sync
description: "Garmin Connect 数据同步技能：通过浏览器自动化抓取当日健康数据（步数/心率/睡眠/压力/身体电池等）并写入本地和服务器数据库。当 OAuth 返回 403 时，优先使用用户已登录的 Chrome session 绕过限制，无需每次输入验证码。触发场景：'同步佳明数据'、'同步今天的佳明数据'、'抓取佳明实时数据'。"
---

# Garmin Sync

通过浏览器自动化同步 Garmin Connect 当日健康数据。

## 核心流程

1. **检查 session** → 用 `profile="user"` 尝试已登录的 Chrome session
2. **抓数据** → 直接从 Garmin Connect 每日摘要页面提取指标
3. **写 DB** → 更新本地 + 服务器 `garmin.db`
4. **git 同步** → 提交到两个 remote

## Step 1：检查现有 Session

```javascript
browser(action="tabs", profile="user")
```

检查是否有 garmin.cn 已登录的 tab：
- 有 → 直接用 `profile="user"` 打开每日摘要页面
- 无 → 启动 `profile="openclaw"` 执行完整登录流程

## Step 2：导航到每日摘要

已登录时，直接导航：

```javascript
browser(action="navigate", targetId="garmin", profile="user", url="https://connect.garmin.cn/app/daily-summary/10037590?date=YYYY-MM-DD")
```

## Step 3：提取页面数据

用 JS 遍历 `innerText`，提取关键指标：

```javascript
// 提取所有含数字的行
var text = document.body.innerText;
var lines = text.split('\n');

// 定位关键区块
var blocks = {};
['步数','心率','身体电量','压力','强度','楼层','睡眠','卡路里'].forEach(k => {
  var idx = text.indexOf(k);
  if (idx > -1) blocks[k] = text.substring(idx, idx+300);
});
JSON.stringify(blocks);  // 返回给 Python 处理
```

**每日摘要页面数据定位**（实测 ref）：
- 步数: `14,509` — 下方紧跟"距离" `12.3` km
- 心率: `55 bpm` 静息 / `52 bpm` 静止 / `168 bpm` 最高
- 身体电池: `18/100`，`+78` 充能，`-67` 耗能
- 压力: `25` 平均 / 低 `9时47分` / 中 `4时6分` / 高 `1时25分`
- 强度分钟: `110` 中等 + `8` 高强度，周目标 `300`
- 楼层: `17` 上 / `14` 下

## Step 4：写入数据库

```python
data = {
    'date': 'YYYY-MM-DD',
    'steps': 14509, 'distance_km': 12.3, 'calories_kcal': 2713.0,
    'active_minutes': 118, 'resting_hr': 55, 'floors': 17.0,
    'stress_low': 587, 'stress_medium': 246, 'stress_high': 85, 'stress_avg': 25,
    'body_battery_start': 18, 'body_battery_end': 18,
    'body_battery_charged': 78, 'body_battery_drained': 67,
    'moderate_min': 110, 'vigorous_min': 8, 'intensity_goal': 300,
    'spo2_avg': 94, 'respiration': 18,
}
```

```python
# 写入本地和服务器
dbs = [
    "/root/.openclaw/workspace/workplan-repo/projects/运动与健康/佳明数据/garmin.db",
    "ubuntu@124.221.34.26:/var/www/workplan-backend/projects/运动与健康/佳明数据/garmin.db"
]
```

## Step 5：完整登录流程（如需 MFA）

当 session 失效时：

1. 打开登录页
   ```javascript
   browser(action="open", label="garmin", url="https://connect.garmin.cn/signin")
   ```

2. JS 注入填表
   ```javascript
   document.querySelector('#email').value = '634194250@qq.com';
   document.querySelector('#password').value = 'Yjh199548';
   Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('Sign In')).click();
   ```

3. 等 MFA 页面（URL → `/mfa`），让用户输入验证码

4. 注入验证码并提交
   ```javascript
   document.getElementById('securityCode').value = 'XXXXXX';
   Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Next').click();
   ```

5. 等待跳转 `/app/home`，session 保持约 7 天

## 数据库 Schema

```sql
daily_summary: id, date, steps, distance_km, calories_kcal, active_minutes, resting_hr,
               floors, stress_low, stress_medium, stress_high, stress_avg,
               body_battery_start, body_battery_end, body_battery_charged, body_battery_drained,
               spo2_avg, spo2_low, respiration, hydration_ml, hydration_goal,
               moderate_min, vigorous_min, intensity_goal, highly_active_sec, created_at

activities: id, date, activity_type, distance_km, duration_min, created_at
```

## 快速命令

```
# 检查 session
browser(action="tabs", profile="user")

# 已登录 → 直接抓今天数据
browser(action="navigate", targetId="garmin", profile="user", url="https://connect.garmin.cn/app/daily-summary/10037590?date=2026-05-20")

# 提取数据（返回给 Python 处理）
JS: JSON.stringify(blocks) from innerText analysis

# 写入本地 + 服务器 DB
python3 scripts/sync_day.py YYYY-MM-DD steps distance_km calories active_minutes resting_hr floors

# git 同步
git add garmin.db && git commit -m "sync: YYYY-MM-DD 数据" && git push origin master && git push tencent master
```

## 注意事项

- **MFA**: 用户提供验证码后立即注入，不要等待太久（验证码有时效）
- **不要重复触发 login()**: 会导致之前所有验证码失效，系统发新验证码给用户
- **session 有效期**: Chrome session 登录后约 7 天有效
- **压力时间转换**: `"9时47分"` → `587` 分钟（9×60+47）
- **活跃分钟**: `active_minutes = moderate_min + vigorous_min`（不是 total day active）