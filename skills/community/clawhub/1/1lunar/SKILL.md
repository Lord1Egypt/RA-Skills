---
name: 1lunar
description: "查询中国农历日期。将公历日期转换为农历年、月、日、节气等。使用场景：用户问'今天是农历多少'、'查询2024年春节是哪天'、'2024年中秋节对应的公历日期'等。"
---

# 中国农历查询

使用 `chinese-lunar-calendar` npm 包进行公历与农历的相互转换。

## 安装

首次使用需安装依赖：

```bash
cd /tmp && npm install chinese-lunar-calendar
```

## 查询公历对应的农历

```bash
# 查询公历日期对应的农历
node -e "
const { getLunar } = require('/tmp/node_modules/chinese-lunar-calendar/src/lunar_calendar.js');
const result = getLunar(2024, 1, 15);
console.log('公历 2024-01-15 => 农历:', result.lunarYear + result.lunarMonth + '月' + result.lunarDate + '日');
console.log('完整信息:', JSON.stringify(result, null, 2));
"
```

**返回字段说明：**
- `lunarYear` - 农历年（甲子年格式，如"癸卯年"）
- `lunarMonth` - 农历月份
- `lunarDate` - 农历日期
- `isLeap` - 是否闰月
- `zodiac` - 生肖
- `solarTerm` - 节气（如有）
- `dateStr` - 简写（如"腊月初五"）

## 常用节日查询

| 农历节日 | 公历参考（2024年） |
|---------|-------------------|
| 春节 | 2024-02-10 |
| 元宵节 | 2024-02-24 |
| 清明节 | 2024-04-04 |
| 端午节 | 2024-06-10 |
| 中秋节 | 2024-09-17 |
| 重阳节 | 2024-10-11 |

## 示例对话

**用户**: "今天农历几号？"

```bash
# 获取今天日期
node -e "
const { getLunar } = require('/tmp/node_modules/chinese-lunar-calendar/src/lunar_calendar.js');
const today = new Date();
const result = getLunar(today.getFullYear(), today.getMonth() + 1, today.getDate());
console.log('今天是农历: ' + result.lunarYear + result.lunarMonth + '月' + result.lunarDate + '日 (' + result.zodiac + '年)');
"
```

**用户**: "2024年春节是哪天？"

```bash
# 春节是农历正月初一
# 反查：2024年正月初一对应的公历
# 已知2024年春节是2024-02-10
echo "2024年春节: 2024-02-10 (癸卯年正月初一)"
```
