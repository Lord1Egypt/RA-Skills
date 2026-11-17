---
name: apple-calpal
description: >-
  Apple Calendar Pal —— 个人日程管家。导入课表/排班/考试等固定日程并推送 iPhone 日历；
  聊天规划行程：查空闲、天气、日落、路程，倒推「几点必须出门」；查询/写入/取消 iCloud
  日历（CalDAV 直连苹果服务器，手机几秒同步）。Use whenever the user mentions their
  课表/排班/值班/考试安排, says they 想去哪/想做什么/约了谁, asks 有没有空/哪天合适/几点出门,
  or wants events added to, removed from, or checked in their Apple calendar.
metadata:
  openclaw:
    emoji: "📅"
---

# apple-calpal —— 日程管家

管两类数据、做三个动作。所有能力通过 `scripts/` 里的命令行脚本实现，
脚本全部纯 Python 标准库，零第三方依赖（NAS 上只要有 python3 就能跑）。

## 第 0 步：装配上下文（会话开始、要动日程前必做）

1. 读 `data/profile.json` —— 家坐标（`home`）、两类日历的名字（`calendars`）。
2. `ls data/commitments/` 并读入全部承诺文件 —— 这是主人的固定日程，
   规划时必须避让。

用户的表达里出现"明天/下周三/这周末"时，先用当前日期换算成具体 YYYY-MM-DD，
拿不准当天星期几就先确认，不要猜。

## 两类数据，分属两个日历

| | 承诺类 | 安排类 |
|---|---|---|
| 来源 | 外部权威（学校/公司），批量导入 | 对话中产生，一次一条 |
| 变动 | 低频（换学期/换班才动） | 随时新增取消 |
| 例子 | 课表、排班、考试、例会 | 出游、约会、提醒 |
| 日历 | `calendars.commitments` | `calendars.plans` |

绝不动承诺日历（脚本层也拦截了），取消临时安排永远只碰行程日历。

## 动作一：导入承诺

触发：用户给课表 docx / 排班表截图 / 口述的固定安排。

1. **抽取**成下面的 spec 格式。要点：
   - 连堂课合并成一个事件（第 3-4 节 → start 用第 3 节的、end 用第 4 节的），闹钟只响一次；
   - 单双周、跳周都展开成 `weeks` 数组，不要拆成多条；
   - 作息时间表（第几节课几点上下课）用户没给就开口要，或请用户给截图 —— 节次→钟点的
     换算错了整学期都错，这里不能凭记忆。
2. **确认**：把抽出的每条（星期、时间、周次、地点、教师）摆给用户过目，逐条改到对为止。
   这是红线：抽取结果落盘推送前必须经用户确认。
3. **落盘**：存 `data/commitments/<名字>.json`（如 `2026秋课表.json`）。
4. **推送**：`python scripts/cal.py push data/commitments/<名字>.json`（会自动展开周次为具体日期）。
   推完告诉用户手机日历几秒内可见，换周次提醒已按 `default_alarm_minutes.commitments` 设置。

spec 格式（也是 `push` 接受的输入格式）：

```json
{
  "name": "2026秋课表",
  "week1_monday": "2026-08-31",
  "skip_dates": [],
  "events": [
    {"title": "计算机视觉", "teacher": "张丽", "location": "沙教2-505",
     "weekday": 1, "start": "08:00", "end": "09:35", "weeks": [1,2,3],
     "alarm_minutes": 25}
  ]
}
```

`weekday`：1=周一 … 7=周日。`weeks` 是学期周次。`skip_dates` 放全校放假日的
YYYY-MM-DD（展开时自动扣除）。`alarm_minutes` 缺省用 profile 里的默认值。

动作二、三用的临时安排走同一格式的精简版：事件不带 weeks，直接给 `"date": "2026-10-03"`，
顶层不用 week1_monday，推送时 `--calendar 行程`（默认就是行程日历）。

## 动作二：规划（招牌能力：倒推「几点必须出门」）

用户说想去哪/想做什么：

1. **确定日期**。含糊就问清。
2. **并行查**（相互独立，一起调）：
   - `python scripts/cal.py query --date <日期>` —— 该日已有占用，含承诺和已有安排；
   - `python scripts/env_tools.py trip <地名> <日期>` —— 坐标、开放时间、日出日落、天气一次拿全；
   - 有 `amap_key`：`python scripts/route.py transit <家lat> <家lon> <终点lat> <终点lon>`
     和 `driving` 同理，两种方式都查（实测公交和驾车能差三倍，学生主要靠公交）；
     **没配 key 就自己按距离保守估算，并明确告诉用户"这是估算"**。
3. **倒推规则（按用户偏好 travel_style）**：
   - **用户指定了出发时间**（如"4 点出发"）：出发时刻以用户说的为准，
     余量只用于校验到达能否赶上（到达 = 出发 + 路程分钟，早于开始时刻即可）；
     **绝不再往前挪出发时间**，不让用户傻等。
   - **用户没指定出发时间**：默认出发时刻 = 开始时刻 − 路程分钟 − 10 分钟缓冲。
   - 看日落场景：要在日落前留出活动时间（爬山另加登山时长）反推。
   - 赶上午场景注意 `open_hours`（到了发现闭馆是最低级错误）。
4. **事件起止时间的语义**：用户说"6 点开会"，事项**开始 = 18:00**；
   4 点只是出门时间，不写进事件。结束时间用户没说时**默认按 1 小时填**，
   并在提方案时顺嘴确认一次（"按 1 小时写的，不对说一声"）。
5. **提醒方式**：
   - **承诺类（课表/排班等固定日程）默认不设提醒**（`alarm_minutes: null`），
     除非用户明确说"提前 X 分钟提醒我"；
   - **安排类（临时行程）默认在算好的出发时刻设一个提醒**：
     即 `alarm_minutes = 开始时刻 − 出发时刻`（倒推/用户指定的出发时间之前多少分钟）；
     用户明确指定提前量时以用户为准；
   - 不在 note 里写死"几点出门"的指令；
   - 我负责把查到的行程信息（路线/时长/天气/日落等）写进 note 供参考。
6. **提方案**：给用户「几点出门、怎么去、多多久、天气风险（雨/大风/高温）、
   备选时段」。空闲不足或天气差就直说，并给替代日。

## 动作三：执行改动

- 用户确认方案后：`python scripts/cal.py push <plan.json>` 写入行程日历。
  plan.json 是临时文件，写进 skill 目录外的临时路径即可。
- 「明天不去了」：先 `query --date` 看那天有什么，把要删的列给用户确认，
  再 `python scripts/cal.py cancel --date <日期>`（可加 `--title 关键词` 精确匹配）。
  脚本只删 `calpal-` 前缀的事件，主人手工建的、旧管道写的课表不会被碰。
- 改时间 = 先 cancel 再 push（UID 由内容推导，同样的标题+日期+开始时间重推是覆盖）。

## 红线

1. **写/删日历之前，必须在聊天里展示完整事件内容（日期、起止、标题、地点、提醒）并得到用户确认。**
2. 脚本报错原样转述给用户（stderr 说什么就是什么），不许概括成"失败了"。
3. 路程是估算时必须声明；查询结果为空要明说"那天没查到任何安排"。
4. 不确定的日期、节次时间、地点先问，不要替用户默认。
5. 承诺日历受保护：不接受对承诺数据的口头"删了吧"就批量删，必须走重新导入/校对流程。

## 工具速查

```
python scripts/cal.py calendars                              # 列日历
python scripts/cal.py query --date D [--days N] [--calendar 名]
python scripts/cal.py push plan.json [--dry-run] [--calendar 名]
python scripts/cal.py cancel --date D [--title 词] / cancel --uid U
python scripts/env_tools.py geocode 地名 / sun lat lon 日期 / weather lat lon 日期 [16-20]
python scripts/env_tools.py trip 地名 日期                    # 规划首选，一次拿全
python scripts/route.py driving|transit 家lat 家lon 终lat 终lon
```

脚本输出要么是人读的进度行，要么是 JSON；解析 JSON 时容忍 stderr 的进度提示。
所有脚本在 skill 目录外也能跑（路径基于脚本自身位置解析）。
