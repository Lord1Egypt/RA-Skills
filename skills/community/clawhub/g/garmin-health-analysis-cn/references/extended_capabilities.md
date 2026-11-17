# 佳明进阶功能说明

本技能现已支持**全面的健康追踪、按时间点查询和活动文件分析**。

## 🎯 按时间点查询

可以提出类似这样的问题：
- "昨天下午 3 点我的心率是多少？"
- "今天上午 10 点半我的压力水平是多少？"
- "中午时我的身体电量是多少？"

### 用法

```bash
# 查询指定时间的心率
python3 scripts/garmin_query.py heart_rate "15:00" --date 2026-01-24

# 压力水平
python3 scripts/garmin_query.py stress "14:30"

# 身体电量
python3 scripts/garmin_query.py body_battery "10:00" --date 2026-01-23

# 指定时间的步数
python3 scripts/garmin_query.py steps "17:00"
```

**支持的时间格式：**
- `15:00`、`15:30:45`（24 小时制）
- `2026-01-24 15:30`（完整日期时间）

## 📊 扩展指标

### 训练与运动表现

```bash
# 训练准备度（每日准备度评分）
python3 scripts/garmin_data_extended.py training_readiness

# 训练状态（训练负荷、最大摄氧量趋势）
python3 scripts/garmin_data_extended.py training_status

# 耐力评分
python3 scripts/garmin_data_extended.py endurance_score

# 爬坡评分
python3 scripts/garmin_data_extended.py hill_score

# 峰值指标（最大摄氧量等）
python3 scripts/garmin_data_extended.py max_metrics

# 体能年龄
python3 scripts/garmin_data_extended.py fitness_age
```

### 身体成分与健康

```bash
# 身体成分（体重、体脂率、肌肉量、BMI）
python3 scripts/garmin_data_extended.py body_composition --date 2026-01-24

# 体重记录历史
python3 scripts/garmin_data_extended.py weigh_ins --start 2026-01-01 --end 2026-01-24

# 血氧（SPO2）
python3 scripts/garmin_data_extended.py spo2 --date 2026-01-24

# 呼吸频率（全天呼吸速率）
python3 scripts/garmin_data_extended.py respiration
```

### 活动指标

```bash
# 详细步数（时间序列）
python3 scripts/garmin_data_extended.py steps --date 2026-01-24

# 爬楼层数
python3 scripts/garmin_data_extended.py floors

# 活动强度分钟数（高强度/中等强度）
python3 scripts/garmin_data_extended.py intensity_minutes

# 饮水量记录
python3 scripts/garmin_data_extended.py hydration

# 详细压力（全天时间序列）
python3 scripts/garmin_data_extended.py stress_detailed

# 全天逐条心率数据（全部心率采样点）
python3 scripts/garmin_data_extended.py hr_intraday
```

## 🗺️ 活动文件分析（FIT/GPX）

下载并分析活动文件，可以回答类似这样的问题：
- "跑到 2 公里处时我的海拔是多少？"
- "心率超过 160 时我的配速是多少？"
- "在地图上展示我的跑步路线"

### 下载活动文件

```bash
# 下载 FIT 文件
python3 scripts/garmin_activity_files.py download --activity-id 12345678 --format fit

# 下载 GPX 文件（用于 GPS 路线可视化）
python3 scripts/garmin_activity_files.py download --activity-id 12345678 --format gpx

# 下载 TCX 文件
python3 scripts/garmin_activity_files.py download --activity-id 12345678 --format tcx
```

### 解析活动文件

```bash
# 解析 FIT 文件（详细指标）
python3 scripts/garmin_activity_files.py parse --file /tmp/activity_12345678.fit

# 解析 GPX 文件（GPS 轨迹）
python3 scripts/garmin_activity_files.py parse --file /tmp/activity_12345678.gpx
```

**FIT 文件中包含：**
- GPS 坐标（经纬度）
- 海拔/高度
- 心率
- 踏频/步频（跑步为步/分，骑行为单位转/分）
- 功率（瓦特，骑行数据）
- 速度与配速
- 温度
- 分圈数据

### 查询活动数据

```bash
# 跑到 1500 米处时我的心率/海拔是多少？
python3 scripts/garmin_activity_files.py query --file /tmp/activity_12345678.fit --distance 1500

# 活动中某一时刻的数据是多少？
python3 scripts/garmin_activity_files.py query --file /tmp/activity_12345678.fit --time "2026-01-24T10:15:30"
```

### 综合分析活动

```bash
# 获取全面的统计信息
python3 scripts/garmin_activity_files.py analyze --file /tmp/activity_12345678.fit
```

**返回内容：**
- 平均/最高/最低心率
- 累计爬升/最高/最低海拔
- 平均/最高速度
- 平均步频/踏频
- 平均/最大功率（骑行）
- 总距离
- 时长

## 🔍 使用场景

### 健康监测
- "过去一个月我的最大摄氧量有什么变化？"
- "我的体能年龄和实际年龄相比如何？"
- "给我看训练负荷趋势"
- "昨晚睡眠期间我的血氧是多少？"

### 活动分析
- "在地图上显示我昨天的跑步路线"
- "在最陡的上坡路段我的心率是多少？"
- "结合海拔曲线展示我每公里的配速"
- "我的步频与心率有什么关联？"
- "这次比赛的后半程掉速了多少？"

### 恢复追踪
- "我今天的训练准备度如何？"
- "昨天我的身体电量是从什么时候开始下降的？"
- "这周我积累了多少活动强度分钟数？"

### 时间序列分析
- "画出我早上 8 点到晚上 6 点的心率曲线"
- "展示整个工作日期间的压力水平"
- "我的身体电量是什么时候充满的？"

## 📦 依赖库

```bash
pip3 install garminconnect fitparse gpxpy
```

- **garminconnect**：佳明 Connect 接口封装库
- **fitparse**：解析 FIT 文件（佳明的二进制格式）
- **gpxpy**：解析 GPX 文件（GPS 轨迹格式）

## 🛠️ 进阶技巧

### 获取活动 ID

活动 ID 可以在佳明 Connect 网页地址中看到：
```
https://connect.garmin.com/modern/activity/12345678
                                        ^^^^^^^^
```

也可以通过程序获取：
```bash
python3 scripts/garmin_data.py activities --days 7
# 在每条活动记录中查找 "activity_id" 字段
```

### 批量处理

```bash
# 获取近期活动 ID
activities=$(python3 scripts/garmin_data.py activities --days 7 | jq -r '.activities[].activityId')

# 批量下载所有 FIT 文件
for id in $activities; do
  python3 scripts/garmin_activity_files.py download --activity-id $id --format fit
done
```

### 可视化创意

1. **路线地图**：用 GPX 文件配合 Leaflet.js 或高德地图绘制
2. **海拔剖面图**：绘制海拔与距离的关系曲线
3. **心率分区**：按心率区间为路线着色
4. **配速热力图**：展示最快与最慢的路段
5. **配速/步频相关性**：跑步经济性分析

## 🚀 未来可扩展的方向

可能的新增功能：
- [ ] 路线可视化自动化
- [ ] 训练计划追踪
- [ ] 训练建议
- [ ] 装备追踪与磨损分析
- [ ] 天气与运动表现的相关性分析
- [ ] 社交挑战与勋章
- [ ] 生理周期追踪
- [ ] 孕期追踪
- [ ] 比赛成绩预测准确度追踪
