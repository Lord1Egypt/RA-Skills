# lunar-python API 使用规范

> **创建日期**: 2026-05-22  
> **版本**: V3.0.2  
> **适用范围**: 黄历脚本中 lunar-python 库的正确使用

---

## ⚠️ 核心教训

**`Lunar.fromYmd` 的参数是农历日期，不是公历！**

这是 lunar-python 最容易踩的坑。API 命名明确区分：
- `Solar.fromYmd(y, m, d)` → 输入**公历**年月日
- `Lunar.fromYmd(y, m, d)` → 输入**农历**年月日

---

## ✅ 正确用法

### 公历 → 农历（最常见）

```python
from lunar_python import Solar

# 公历 2026年5月30日 → 农历
solar = Solar.fromYmd(2026, 5, 30)
lunar = solar.getLunar()

# 获取农历信息
year_gz = lunar.getYearInGanZhi()    # 年柱
day_gz = lunar.getDayInGanZhi()      # 日柱
yi = lunar.getDayYi()                 # 宜
ji = lunar.getDayJi()                 # 忌
```

### 农历 → 公历

```python
from lunar_python import Lunar

# 农历 2026年四月初五 → 公历
lunar = Lunar.fromYmd(2026, 4, 5)
solar = lunar.getSolar()

year = solar.getYear()    # 2026
month = solar.getMonth()  # 5
day = solar.getDay()      # 30
```

---

## ❌ 常见错误

### 错误 1：把公历日期传给 Lunar.fromYmd

```python
# ❌ 错误！把公历 5月30日 当成农历 5月30日
lunar = Lunar.fromYmd(2026, 5, 30)
# 2026年农历五月只有29天，直接抛异常：
# Exception: only 29 days in lunar year 2026 month 5
```

### 错误 2：即使没报错，数据也是错的

```python
# ❌ 错误！5月23日没报错，但查的是农历五月二十三，不是公历5月23日
lunar = Lunar.fromYmd(2026, 5, 23)
# 干支、宜忌、生肖全对应错误的农历日期
```

---

## 📋 API 速查表

| 需求 | 正确 API | 示例 |
|------|---------|------|
| 公历→农历 | `Solar.fromYmd(y,m,d).getLunar()` | ✅ |
| 农历→公历 | `Lunar.fromYmd(y,m,d).getSolar()` | ✅ |
| 年柱 | `lunar.getYearInGanZhi()` | "丙午" |
| 月柱 | 根据节气计算（不用 lunar-python） | "己巳" |
| 日柱 | `lunar.getDayInGanZhi()` | "辛酉" |
| 宜 | `lunar.getDayYi()` | ["嫁娶", "祭祀", ...] |
| 忌 | `lunar.getDayJi()` | ["开市", "入宅", ...] |
| 节气 | `lunar.getJieQi()` | "清明" 或 None |
| 彭祖百忌 | `lunar.getPengZuGan()` + `getPengZuZhi()` | |
| 纳音 | `lunar.getDayNaYin()` | "石榴木" |
| 星宿 | `lunar.getXiu()` | "角木蛟" |
| 建除十二值星 | `lunar.getZhiXing()` | "执" |

---

## 🔧 月柱计算注意事项

lunar-python 的 `getMonthInGanZhi()` 返回的是**农历月**干支，不是**节气月**干支。

黄历需要使用节气月（以立春/惊蛰等为界），脚本中通过 `get_month_ganzhi_by_jieqi()` 函数手动计算。

---

## 📝 修复记录

| 日期 | 问题 | 修复 |
|------|------|------|
| 2026-05-22 | `Lunar.fromYmd` 误用导致 5月30日+ 越界 | 改为 `Solar.fromYmd().getLunar()` |
| 2026-04-12 | `getMonthInGanZhi()` 返回农历月干支 | 改为节气月计算 |

---

*最后更新：2026-05-22*  
*数字化专班 - 商业航天数字化转型*
