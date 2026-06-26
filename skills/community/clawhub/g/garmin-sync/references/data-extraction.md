# Garmin Connect 每日摘要页面 — 数据提取参考

## 页面结构

每日摘要页面 URL:
```
https://connect.garmin.cn/app/daily-summary/10037590?date=YYYY-MM-DD
```

登录后直接导航即可，会话 cookie 持久化，无需每次输入验证码。

## 关键元素 ref（2026-05-20 实测）

### 活动区域
- `ref=13_44` — 标题 "每日摘要"
- `ref=13_45` — 日期选择器 `05/20/2026`
- `ref=13_47` — "今天" 按钮
- `ref=13_48` / `13_49` — "先前" / "继续" 导航

### 步数（最重要）
```
ref=13_230: "步数" 标签
ref=13_230 后续: "14,509" 步数
ref=13_230: "距离" → "12.3" km
ref=13_239: "每日平均" → "15,806"
ref=13_244: "编辑步数目标" 按钮
```

### 心率
```
ref=13_161: 心率图标 + "55 bpm" 静息
ref=13_167: Help Icon
ref=13_178: "52 bpm" 静止 + "168 bpm" 最高
ref=13_178: "查看详情" 按钮
```

### 身体电池
```
ref=13_180: 身体电池图标 + "18/100"
ref=13_190: "充能" + "+78"
ref=13_191: "耗能" + "-67"
ref=13_191: "查看详情" 链接
```

### 压力
```
ref=13_193: 压力图标 + "25" 平均 + "休息" 状态
ref=13_207: 低 9时47分 / 中 4时6分 / 高 1时25分
ref=13_207: "查看详情" 链接
```
**注意**: 时间格式是"X时Y分"，需转换为分钟：`低=587分钟，中=246分钟，高=85分钟`

### 强度分钟
```
ref=13_228: "今日中等强度" → "110"
ref=13_228: "今日高强度" → "8" + "x2"（可能表示2倍）
ref=13_227: "编辑强度活动时间目标" 按钮
ref=13_228: "周目标" → "300"
```
**active_minutes = moderate_min + vigorous_min**（这里是110+8=118，但通常要+走路等其他活跃分钟）

### 楼层
```
ref=13_247: 楼层图标 + "17" 上 / "14" 下
ref=13_256: "每日平均" → "20"
ref=13_261: "编辑爬楼层数目标" 按钮
```

### 活动记录
```
ref=13_121: "动作" 标签
ref=13_127: "佛山市 跑步" 链接 + "6.67 公里" + "53:14" 时间 + "7:59 /公里" 配速
ref=13_141: "查看活动" 按钮
```

## 主页数据（对比参考）

主页 `/app/home` 显示昨天（5/19）数据：
```
步数: 14,183（超标102%）
距离: 12.3 km
睡眠分数: 72 / 6时2分
身体电量: +52 / -50
心率: 57 静止 / 143 最高
过去7天平均: 步数16,023 / 心率55 / 睡眠63平均
```

## 活动页面 `/app/activities`

列出最近活动列表，每个活动：
- 日期标签（5月20日/19日等）
- 活动名称（佛山市 跑步）
- 距离（6.67 公里）
- 时间（53:14）
- 配速（7:59 /公里）
- 累计爬升（6 米）
- 平均心率（157 bpm）

## 提取 JS 模板

```javascript
// 提取所有数字（用于快速扫描）
var nums = document.body.innerText.match(/\d{1,3}(?:,\d{3})+/g);

// 定位特定区块
var blocks = {};
['步数','心率','身体电量','压力','强度','楼层','睡眠','卡路里'].forEach(k => {
  var idx = document.body.innerText.indexOf(k);
  if (idx > -1) blocks[k] = document.body.innerText.substring(idx, idx+200);
});

// 从 ref 区域提取（推荐）
function getRefText(ref) {
  var el = document.querySelector('[data-ref="' + ref + '"]') ||
           Array.from(document.querySelectorAll('*')).find(e => e.getAttribute('data-ref') === ref);
  return el ? el.innerText : 'not found';
}
```

## 数据写入 SQL

```python
data = {
    'date': 'YYYY-MM-DD',
    'steps': 14509,
    'distance_km': 12.3,
    'calories_kcal': 2713.0,  # 从主页估算或留空
    'active_minutes': 118,     # moderate + vigorous
    'resting_hr': 55,
    'floors': 17.0,
    'stress_low': 587,
    'stress_medium': 246,
    'stress_high': 85,
    'stress_avg': 25,
    'body_battery_start': 18,   # 起床值
    'body_battery_end': 18,     # 睡前值
    'body_battery_charged': 78,
    'body_battery_drained': 67,
    'moderate_min': 110,
    'vigorous_min': 8,
    'intensity_goal': 300,
}

# UPDATE
set_clause = ','.join([f"{k}=?" for k in data.keys()])
c.execute(f"UPDATE daily_summary SET {set_clause} WHERE date=?", tuple(data.values())+(data['date'],))

# INSERT activity
c.execute("INSERT OR REPLACE INTO activities(date,activity_type,distance_km,duration_min) VALUES(?,?,?,?)",
          (data['date'], 'running', 6.67, 53))
```