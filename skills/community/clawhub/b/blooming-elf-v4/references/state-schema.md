# plants.json 状态文件 Schema（v4 单一事实来源 · 多实例版）

> 本文件是 blooming-elf v4 的**唯一可变状态源**。markdown 档案由它生成，日志文档是历史，均不反向写入状态。
> 每次状态变更后必跑 `scripts/commit_state.py`（校验 + 原子提交 + 备份轮转）。

## 顶层结构（多实例）

```json
{
  "version": 4,
  "updated_at": "2026-07-29",
  "instances": [
    {
      "elf": "绿灵",
      "user": "十一一",
      "remind_time": "10:00",
      "city": "武汉",
      "climate": "亚热带季风气候",
      "env": "室内",
      "plants": [ /* 见下 */ ]
    },
    {
      "elf": "花灵",
      "user": "十一一",
      "remind_time": "20:00",
      "city": "西安",
      "climate": "温带季风气候",
      "env": "室内",
      "plants": [ /* 见下 */ ]
    }
  ]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version | int | ✅ | 固定 4 |
| updated_at | string(ISO) | ✅ | 最后更新日期 |
| instances | array | ✅ | 多精灵实例数组（绿灵/花灵…） |
| instances[].elf | string | ✅ | 精灵名（品牌吉祥物，用户可自定义） |
| instances[].user | string | ✅ | 用户名 |
| instances[].remind_time | string(HH:MM) | ✅ | 该实例提醒时间 |
| instances[].city | string | 推荐 | 城市（用于气候/季节系数） |
| instances[].climate | string | 推荐 | 气候类型 |
| instances[].env | string | 推荐 | 室内/室外/阳台 |
| instances[].location | string | 推荐 | 摆放地点（家里/公司…），驱动「微气候提醒」与就近提醒时间 |
| instances[].microclimate | object | 可选 | **该 location 实测环境档案**（见下）；浇水/喷雾判断**优先用实测**，城市天气仅降级兜底 |
| instances[].pets | object | 可选 | 宠物：`{"cats": bool, "dogs": bool, "birds": [种名]}`；任一为真则触发对应毒性告警 |
| instances[].plants | array | ✅ | 该实例植物状态数组 |

> **向后兼容**：若文件顶层直接含 `user` + `plants`（无 `instances`），视为单实例，校验时自动归一为 `instances[0]`。

## plants[] 元素字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| key | string | ✅ | **唯一**标识，建议 `{植物名}-{序号}`，如 `绿萝-1` |
| name | string | ✅ | 植物名 |
| category | string | ✅ | 土培 / 吸水盆 / 水培 / 鲜切花 / **水养**（提交时归一为水培） |
| status | string | 可选 | `正常`(默认) / `休眠` / `停水观察` / `已弃`；`已弃`不提醒不计数 |
| last_water | string(ISO) | 推荐 | 上次浇水/换水日 `YYYY-MM-DD` |
| next_water | string(ISO) | 推荐 | 下次浇水/换水日预测上限 `YYYY-MM-DD` |
| water_interval_max | int | 推荐 | 浇水间隔上限（天），土湿优先时作为上界参考 |
| light | string | 推荐 | 散射光/喜光/喜暴晒/耐阴 |
| position | string | 可选 | 桌面/西窗边/东窗边… |
| fertilizer_last | string(ISO) | 可选 | 上次施肥 |
| fertilizer_next | string(ISO) | 可选 | 下次施肥 |
| pot | string | 可选 | 花盆类型 |
| difficulty | int | 可选 | 1–10 |
| pet_toxic | string | 可选 | 🐾 旗：`🚫对猫致命` / `⚠️对猫狗有毒` / `⚠️对猫狗有毒(轻度)` / 空 |
| pet_toxic_bird | string | 可选 | 🐦 旗：`🐦对鸟有毒` / 空（养鸟家庭告警，见安全红线） |
| self_watering_warn | string | 可选 | `⚠️吸水盆不匹配` |
| note | string | 可选 | 简短标签，不写长文本 |

## location 环境档案（microclimate · v4.0.4 新增）

> **核心原则**：浇水/喷雾判断**优先用本 location 实测环境**；城市天气（climate/季节系数）仅在 `microclimate` 缺失或 `measured_at` 过期（>7 天）时降级兜底，并标注"（城市估算，建议补实测）"。
> 直接回应"别刻板用城市天气推算"——公司西晒、暴雨实测蒸发慢等室内真实条件优先。

| 字段 | 类型 | 说明 |
|------|------|------|
| measured_temp | number | 实测温度（°C），如公司 7/22 暴雨 27.1°C |
| measured_humidity | number | 实测湿度（%），如 79% |
| west_sun | bool/string | 是否有西晒（true / 描述，如"西窗 14-17 点拉帘"） |
| ac | string | 空调/暖气情况（如"中央空调制冷差""夏天常开"） |
| ventilation | string | 通风情况（如"四窗全开""角落闷"） |
| measured_at | string(ISO) | 实测日期；>7 天视为过期，降级城市天气 |
| source | string | `实测` / `城市估算`（无实测时由城市气候推导，标 low-confidence） |

```json
"microclimate": {
  "measured_temp": 27.1, "measured_humidity": 79,
  "west_sun": "西窗 14-17 点拉帘", "ac": "中央空调制冷差",
  "ventilation": "四窗全开", "measured_at": "2026-07-22", "source": "实测"
}
```

## 鲜切花专用字段

| 字段 | 类型 | 说明 |
|------|------|------|
| bought_at | string(ISO) | 购入日 |
| survive_days | int | 存活天数 = 发现死亡日 − 购入日 |
| water_level | string | 浅水/低水位/深水 |
| status | string | 统一用主表 status 字段：`正常` / `休眠` / `停水观察` / `已弃`（🔴已丢=已弃，不提醒） |

## 设计要点

1. **key 是稳定主键**，重命名植物时保留 key，只改 `name`，避免历史日志失联。
2. **日期全部 ISO** `YYYY-MM-DD`，禁止 `M/D`。这是根治格式乱的硬约束。
3. `next_water` 是**预测上限**，实际触发以查土湿为准（落地专家点 2/11/14）。
4. **多实例隔离**：每个 `elf` 独立 `plants` 与 `remind_time`；查询/提醒按 `elf` 分别算，互不串。
5. **location 实测环境优先**：浇水/喷雾判断先看 `microclimate`（实测温度/湿度/西晒/空调/通风）；无实测或过期 >7 天才用城市天气兜底，并标注 low-confidence。公司 vs 家里温湿度不同 → 各 location 各记一份，不套同一城市值。
6. 校验失败 = 文件不健康，**禁止回复"已记"**，先修正。
7. 跨会话：每次启动读本文件，MEMORY.md 只存配置路径。

## 空模板（首次建档 Write 内容）

```json
{
  "version": 4,
  "updated_at": "YYYY-MM-DD",
  "instances": [
    {
      "elf": "绿灵",
      "user": "{用户名}",
      "remind_time": "{时间}",
      "city": "{城市}",
      "climate": "{气候}",
      "env": "{室内/室外/阳台}",
      "location": "{家里/公司}",
      "microclimate": {
        "measured_temp": 27.1, "measured_humidity": 79,
        "west_sun": "西窗 14-17 点拉帘", "ac": "中央空调制冷差",
        "ventilation": "四窗全开", "measured_at": "YYYY-MM-DD", "source": "实测"
      },
      "plants": []
    }
  ]
}
```
