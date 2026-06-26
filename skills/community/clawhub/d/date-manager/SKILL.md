---
name: date-manager
description: 私人日期管家。**重要：所有日期计算（包括相差天数、下周一、月末等）必须使用 calc 命令，不要自己计算，避免出错。** 支持公历和农历计算，提供提醒和情感化文案。触发场景：(1)用户提到生日、纪念日、忌日、祭祖、清明等关键词 (2)用户说"记录XXX的生日"、"记一下XXX" (3)用户问"今天有什么日子"、"这周有什么纪念日" (4)用户想查询或管理重要日期 (5)用户问节气、农历转换、法定假日等 (6)用户要求计算日期相关（如相差几天、某天后是几号等)
---

# 全能日期管家

## 数据存储

所有数据保存在 `{SKILL_DIR}/data/dates.json`

## 支持的类型

| 类型 | 说明 | 特殊计算 |
|------|------|----------|
| 生日 | 人物生日 | 计算年龄、同时显示公历农历 |
| 纪念日 | 事件纪念日 | 计算周年，10/20/50年显示婚龄名称 |
| 祭日 | 人物忌日 | 计算周年、情感化提示 |
| 祭祖 | 传统节日祭祖 | 清明、中元等传统节日 |

## ⚠️ 重要：必须使用脚本计算

**禁止大模型自行计算日期！** 所有日期相关计算必须调用脚本，否则容易出错。

| 用户需求 | 正确做法 | 错误做法（禁止） |
|----------|----------|------------------|
| 计算相差几天 | `calc --date 2026-05-01` | 自己算 (2026-05-01 - 今天) |
| 10天后是几号 | `calc --days 10` | 今天 + 10 天 |
| 下周一几号 | `calc --next-monday` | 查日历自己推算 |
| 4月最后一天 | `calc --month-end --month-end-month 4` | 认为4月有30天 |
| 公历转农历 | `convert --solar 1990-05-15` | 自己查万年历 |

## 命令概览

| 命令 | 功能 | 示例 |
|------|------|------|
| `add` | 添加记录 | 添加生日、纪念日、祭日、祭祖 |
| `list` | 查询列表 | 查看所有/按类型筛选 |
| `get` | 查看详情 | 获取单条记录详细信息 |
| `today` | 今日/近期 | 今日和未来N天的日期 |
| `search` | 搜索 | 按名称/关系/备注搜索 |
| `update` | 更新 | 修改日期、提醒、备注等 |
| `delete` | 删除 | 删除记录 |
| `term` | 节气查询 | 24节气日期和倒计时 |
| `convert` | 公历农历互转 | 日期格式转换 |
| `calc` | 日期计算 | 下周一、月始月终等 |
| `holiday` | 法定假日 | 节日倒计时 |

---

## add - 添加记录

### 基本用法

```bash
python {SKILL_DIR}/scripts/date_manager.py add "名称" --type 类型 --date 日期
```

### 公历生日
```bash
python {SKILL_DIR}/scripts/date_manager.py add "妈妈" --type 生日 --date 1980-05-15 --remind 3 --relation 母亲
```

### 农历生日
```bash
python {SKILL_DIR}/scripts/date_manager.py add "爸爸" --type 生日 --lunar 8-10 --remind 5 --relation 父亲
```
格式：`--lunar 月-日`

### 农历纪念日（指定年份）
```bash
python {SKILL_DIR}/scripts/date_manager.py add "结婚纪念日" --type 纪念日 --lunar 8-10 --year 2015 --remind 7 --relation 夫妻
```

### 祭日
```bash
python {SKILL_DIR}/scripts/date_manager.py add "爷爷" --type 祭日 --date 2020-03-15 --remind 2 --relation 祖父
```

### 纪念日
```bash
python {SKILL_DIR}/scripts/date_manager.py add "结婚纪念日" --type 纪念日 --date 2020-09-01 --remind 7 --relation 夫妻
```

### 祭祖（清明等传统节日）
```bash
python {SKILL_DIR}/scripts/date_manager.py add "清明" --type 祭祖 --date 2026-04-04 --remind 7
```

### 参数说明

| 参数 | 说明 | 必填 |
|------|------|------|
| name | 名称（人名/事件名） | ✅ |
| --type | 类型：生日/纪念日/祭日/祭祖 | 默认生日 |
| --date | 公历日期 YYYY-MM-DD | 与--lunar二选一 |
| --lunar | 农历日期 月-日，如 8-10 | 与--date二选一 |
| --year | 农历对应的公历年份 | 可选，配合--lunar使用 |
| --remind | 提前提醒天数 1-30 | 默认7 |
| --relation | 关系/身份 | 可选 |
| --notes | 备注 | 可选 |

---

## list - 查询列表

### 查看所有
```bash
python {SKILL_DIR}/scripts/date_manager.py list
```

### 按类型筛选
```bash
python {SKILL_DIR}/scripts/date_manager.py list --type 生日
python {SKILL_DIR}/scripts/date_manager.py list --type 纪念日
python {SKILL_DIR}/scripts/date_manager.py list --type 祭日
python {SKILL_DIR}/scripts/date_manager.py list --type 祭祖
```

---

## get - 查看详情

### 基本用法
```bash
python {SKILL_DIR}/scripts/date_manager.py get <ID>
```

### 说明
- 获取单条记录的详细信息
- 包含今年日期、倒计时、年龄/周年
- ID 通过 `list` 或 `search` 命令获取

---

## today - 今日/近期查询

### 未来7天（默认）
```bash
python {SKILL_DIR}/scripts/date_manager.py today
```

### 指定天数
```bash
python {SKILL_DIR}/scripts/date_manager.py today --days 30
python {SKILL_DIR}/scripts/date_manager.py today -n 30
```

### 输出说明
- 今日有纪念日时高亮显示
- 未来N天内的日期按倒计时排序
- 显示本月总计数

---

## search - 搜索

### 基本用法
```bash
python {SKILL_DIR}/scripts/date_manager.py search "关键词"
```

### 示例
```bash
python {SKILL_DIR}/scripts/date_manager.py search "妈妈"
python {SKILL_DIR}/scripts/date_manager.py search "结婚"
```

### 说明
- 按名称、关系、备注搜索
- 不区分大小写

---

## update - 更新记录

### 基本用法
```bash
python {SKILL_DIR}/scripts/date_manager.py update <ID> [参数]
```

### 示例
```bash
# 修改日期
python {SKILL_DIR}/scripts/date_manager.py update abc123 --date 1980-05-20

# 修改提醒天数
python {SKILL_DIR}/scripts/date_manager.py update abc123 --remind 5

# 修改关系
python {SKILL_DIR}/scripts/date_manager.py update abc123 --relation 母亲

# 修改备注
python {SKILL_DIR}/scripts/date_manager.py update abc123 --notes "备注信息"
```

### 参数说明

| 参数 | 说明 |
|------|------|
| --date | 修改日期 YYYY-MM-DD |
| --remind | 修改提醒天数 1-30 |
| --relation | 修改关系 |
| --notes | 修改备注 |

---

## delete - 删除记录

### 基本用法
```bash
python {SKILL_DIR}/scripts/date_manager.py delete <ID>
```

### 示例
```bash
python {SKILL_DIR}/scripts/date_manager.py delete abc123
```

---

## term - 节气查询

### 查询下一个节气（默认）
```bash
python {SKILL_DIR}/scripts/date_manager.py term
```

### 查询指定节气
```bash
python {SKILL_DIR}/scripts/date_manager.py term --name 清明
python {SKILL_DIR}/scripts/date_manager.py term -n 小满
```

### 查询所有节气
```bash
python {SKILL_DIR}/scripts/date_manager.py term --all
python {SKILL_DIR}/scripts/date_manager.py term -a
```

### 24节气列表

| 节气 | 日期范围 | 说明 |
|------|----------|------|
| 小寒 | 01-05前后 | 开始进入一年中最寒冷的日子 |
| 大寒 | 01-20前后 | 一年中最冷的时节 |
| 立春 | 02-03/04 | 春季的开始 |
| 雨水 | 02-18/19 | 降雨开始，雨量渐增 |
| 惊蛰 | 03-05/06 | 春雷始鸣，惊醒蛰虫 |
| 春分 | 03-20/21 | 昼夜等长，春季过半 |
| 清明 | 04-04/05 | 天清气明，万物洁齐 |
| 谷雨 | 04-19/20 | 雨生百谷，播种时节 |
| 立夏 | 05-05/06 | 夏季的开始 |
| 小满 | 05-20/21 | 小麦籽粒开始饱满 |
| 芒种 | 06-05/06 | 有芒作物成熟，抢收抢种 |
| 夏至 | 06-20/21 | 白昼最长，夏季过半 |
| 小暑 | 07-06/07 | 暑气渐盛 |
| 大暑 | 07-22/23 | 一年中最热的时节 |
| 立秋 | 08-07/08 | 秋季的开始 |
| 处暑 | 08-22/23 | 暑气消退 |
| 白露 | 09-07/08 | 露凝而白，早晚温差大 |
| 秋分 | 09-22/23 | 昼夜等长，秋季过半 |
| 寒露 | 10-08/09 | 露气寒冷，秋季渐深 |
| 霜降 | 10-23/24 | 天气渐冷，开始降霜 |
| 立冬 | 11-07/08 | 冬季的开始 |
| 小雪 | 11-22/23 | 开始降雪，但雪量不大 |
| 大雪 | 12-06/07 | 雪量增大 |
| 冬至 | 12-21/22 | 白昼最短，冬季过半 |

---

## convert - 公历农历互转

### 公历转农历
```bash
python {SKILL_DIR}/scripts/date_manager.py convert --solar 2026-04-04
python {SKILL_DIR}/scripts/date_manager.py convert -s 1990-05-15
```

### 农历转公历
```bash
# 今年农历八月十五
python {SKILL_DIR}/scripts/date_manager.py convert --lunar 8-15

# 指定年份的农历日期
python {SKILL_DIR}/scripts/date_manager.py convert --lunar 8-10 --year 2015
python {SKILL_DIR}/scripts/date_manager.py convert -l 8-10 -y 2015
```

### 参数说明

| 参数 | 说明 |
|------|------|
| --solar | 公历日期 YYYY-MM-DD（公历转农历） |
| --lunar | 农历日期 月-日（农历转公历） |
| --year | 指定农历年份（默认今年） |

---

## calc - 日期计算

### 计算下周一
```bash
python {SKILL_DIR}/scripts/date_manager.py calc --next-monday
python {SKILL_DIR}/scripts/date_manager.py calc -m
```

### 计算本周星期几
```bash
python {SKILL_DIR}/scripts/date_manager.py calc --week Monday
python {SKILL_DIR}/scripts/date_manager.py calc -w Friday
```

### 计算N天后
```bash
python {SKILL_DIR}/scripts/date_manager.py calc --days 30
python {SKILL_DIR}/scripts/date_manager.py calc -n 100
```

### 计算月末日期
```bash
# 今年当月月末
python {SKILL_DIR}/scripts/date_manager.py calc --month-end

# 指定年月月末
python {SKILL_DIR}/scripts/date_manager.py calc --month-end --month-end-year 2026 --month-end-month 4
```

### 计算月初日期
```bash
# 今年当月月初
python {SKILL_DIR}/scripts/date_manager.py calc --month-start

# 指定年月月初
python {SKILL_DIR}/scripts/date_manager.py calc --month-start --month-start-year 2026 --month-start-month 5
```

### 计算指定日期差
```bash
python {SKILL_DIR}/scripts/date_manager.py calc --date 2026-05-01
```

### 参数说明

| 参数 | 说明 |
|------|------|
| --date | 目标日期 YYYY-MM-DD，计算与今天的差值 |
| --next-monday | 计算下周一 |
| --week | 本周星期几（Monday/Tuesday/Wednesday/Thursday/Friday/Saturday/Sunday） |
| --days | 计算N天后的日期 |
| --month-end | 计算月末日期 |
| --month-end-year | 指定年份（配合--month-end） |
| --month-end-month | 指定月份（配合--month-end） |
| --month-start | 计算月初日期 |
| --month-start-year | 指定年份（配合--month-start） |
| --month-start-month | 指定月份（配合--month-start） |

---

## holiday - 法定假日查询

### 下一个假日（默认）
```bash
python {SKILL_DIR}/scripts/date_manager.py holiday
```

### 下一个假日
```bash
python {SKILL_DIR}/scripts/date_manager.py holiday --next
python {SKILL_DIR}/scripts/date_manager.py holiday -n
```

### 所有假日
```bash
python {SKILL_DIR}/scripts/date_manager.py holiday --all
python {SKILL_DIR}/scripts/date_manager.py holiday -a
```

### 主要法定假日

| 节日 | 日期 | 说明 |
|------|------|------|
| 元旦 | 1月1日 | 新年第一天 |
| 春节 | 农历正月初一 | 最重要的传统节日 |
| 清明节 | 4月4/5日 | 祭祖踏青 |
| 劳动节 | 5月1日 | 国际劳动节 |
| 端午节 | 农历五月初五 | 传统节日 |
| 中秋节 | 农历八月十五 | 团圆节日 |
| 国庆节 | 10月1日 | 国庆节 |

---

## 输出格式规范

### 添加成功（生日）
```
✅ 已添加

| 字段 | 值 |
|------|-----|
| ID | abc123 |
| 类型 | 生日 |
| 名称 | 妈妈 |
| 日期 | 1980-05-15 |
| 提醒 | 提前3天 |
| 关系 | 母亲 |

今年生日：5月15日 | 母亲46岁 | 还有3天
```

### 添加成功（纪念日/婚龄）
```
✅ 已添加

| 字段 | 值 |
|------|-----|
| 类型 | 纪念日 |
| 名称 | 结婚纪念日 |
| 日期 | 农历8月10日 |

距离11周年还有约4个月 | 💍 锡婚
```

### 今日查询
```
📅 4月17日

【今天】
- 暂无重要日子

【未来7天】
- 4月18日 妈妈生日 | 还有1天 | 母亲46岁
- 4月20日 清明祭祖 | 还有3天

【本月共3个】
```

### 祭日文案
```
🌸 爷爷祭日
第3周年 (2020-03-15)
建议：点一支蜡烛，给家人打个电话
```

### 祭祖文案
```
🏮 清明祭祖
还有7天
准备清单：香烛、纸钱、鲜花、供品
```

---

## 婚龄名称对照

| 周年 | 名称 |
|------|------|
| 1年 | 纸婚 |
| 2年 | 布婚 |
| 3年 | 皮婚 |
| 5年 | 木婚 |
| 10年 | 锡婚 |
| 15年 | 水晶婚 |
| 20年 | 瓷婚 |
| 25年 | 银婚 |
| 30年 | 珍珠婚 |
| 40年 | 红宝石婚 |
| 50年 | 金婚 |
| 60年 | 钻石婚 |

---

## 注意事项

1. **路径说明**：`{SKILL_DIR}` 表示 skill 所在目录，使用时替换为实际路径
2. **农历转换**：需要安装 `zhdate` 库（如果不可用则某些功能受限）
3. **节气计算**：需要安装 `chinese-calendar` 库（如果不可用则使用备用数据，允许1-2天误差）
4. 如果用户说"生日"但没给日期，引导用户提供
5. 如果用户说"农历X月X日"，转换为 `--lunar 月-日` 格式
6. 纪念日10周年以上自动标注婚龄名称
7. 生日同时存储公历和农历，自动计算两个日期的倒计时

---

## 安装依赖

```bash
pip install zhdate chinese-calendar
```

如果提示缺少库，运行上述命令安装。