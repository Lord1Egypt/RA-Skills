---
name: fortune-telling-bazi
description: 八字算命 skill — 支持多人八字存储+联合分析，首次询问生日，后续对话自动附带八字信息。说"停止算命"退出。
---

# fortune-telling-bazi 八字算命

## 核心流程

### 首次启用
1. 用户说「开始算命」→ 调用 `python3 scripts/main.py status`
2. 无用户 → 询问生日（姓名/年份/月份/日期/时间/性别）
3. 调用 `python3 scripts/main.py add <name> <年> <月> <日> <时> <性别>`（分可省略）
4. 本地计算八字（`scripts/calc.py`）→ 保存到 `data/users.json` → 显示摘要
5. 调用 `python3 scripts/main.py active <name>` 激活
6. **标记 `is_active = true`**，此后每条回复注入八字摘要

### 非首次启用
1. 用户说「开始算命」→ `python3 scripts/main.py status`
2. 有记录 → 显示所有已保存用户列表，询问「用哪个/哪几个」
3. 用户选一个或多个人 → `python3 scripts/main.py active <name1,name2,...>`
4. 标记 `is_active = true`，注入对应八字摘要

### 退出
- 用户说「停止算命」→ `is_active = false`

---

## 数据文件

```
data/
├── users.json     # 所有用户的生日+八字（JSON格式）
└── active.json    # 当前激活的用户列表
```

---

## 命令一览

| 命令 | 功能 |
|------|------|
| `python3 scripts/main.py add <name> <year> <month> <day> <time> <gender>` | 添加新用户（time格式：`16` / `16:30` / `下午4` / `晚8`） |
| `python3 scripts/main.py update <name> <year> <month> <day> <time> <gender>` | 更新已有用户 |
| `python3 scripts/main.py list` | 列出所有已保存用户 |
| `python3 scripts/main.py view [name]` | 查看某人八字详情（默认当前激活） |
| `python3 scripts/main.py remove <name>` | 删除某人八字 |
| `python3 scripts/main.py active [name1,name2,...]` | 设置激活用户，多人用逗号分隔 |
| `python3 scripts/main.py status` | 检查激活状态 |
| `python3 scripts/main.py joint [name1,name2]` | 联合分析（默认当前激活用户） |

---

## 八字摘要格式（单人被注入到 context）

```
━━━ 八字信息 ━━━
姓名：{name} | {gender} | 农历{lunar_str}
八字：{year_ganzhi} {month_ganzhi} {day_ganzhi} {hour_ganzhi}
生肖：{shengxiao} | 日主：{me}（{yinyang}）
五行：{wuxing} | {mingge} | 旺衰：{wangshuai}
喜用：{xiyong}
神煞：{shensha}
大运：{current_dayun}（{start_age}-{end_age}岁）
━━━ 八字信息 ━━━
```

---

## 联合分析格式（多人被注入到 context）

```
━━━ 联合分析 ━━━
【{name1}】{gender} | {bazi_str} | {mingge}
【{name2}】{gender} | {bazi_str} | {mingge}
━━━ 合冲刑害 ━━━
年支关系：{analysis}
日支关系：{analysis}（夫妻/伴侣位）
月支关系：{analysis}
━━━ 五行契合 ━━━
{analysis}
━━━ 婚配分析 ━━━
{analysis}（仅两人时）
━━━ 八字信息 ━━━
```

---

## 触发关键词

| 关键词 | 动作 |
|--------|------|
| `开始算命`、`算命`、`看看八字`、`我的八字` | 激活算命流程 |
| `停止算命`、`不算了`、`退出算命` | 退出算命模式 |
| `联合分析`、`合盘`、`双人八字` | 触发联合分析 |
| `添加八字`、`加个人`、`录入八字` | 添加新用户 |
| `查看用户`、`都有谁`、`八字体检` | 列出所有已保存用户 |

---

## 联合分析内容

**地支关系分析：**
- 年支 vs 年支（双方祖辈/原生家庭/根基是否相合）
- 日支 vs 日支（夫妻/伴侣位合冲刑害）
- 月支 vs 月支（父母/环境/外环境关系）

**五行契合分析：**
- 喜用五行是否相生（你生我或我生你为吉）
- 五行是否互补

**婚配分析（仅两人时）：**
- 日支合冲刑害婚姻判断
- 桃花重叠警告
- 天乙贵人重叠吉兆

---

## 技术实现

- **八字计算**：完全本地，不依赖任何远程API
- **依赖库**：`scripts/lunar_core.py` 自包含单文件，提供本地农历换算和四柱计算。
  - 计算范围覆盖 1899-2060 年。
  - 无远程 API、无第三方运行时依赖。

- **lunar_core.py 调试经验（2026-04-26 已修复）**：
  - `jd_greg()` 反算公历年时曾少减 4800，导致 `Solar.toYmd()` 出现 `67870114` 这类错误年份；现已修正 JD → Gregorian 转换。
  - `_from_solar()` 现在按月首 JD 反推真实农历年，避免 11/12 月重复数据和立春年混用；立春年柱判断放在 `_compute()` 中按 solar year 查询 `LICHUN_JD`/`LICHUN_YMD`。
  - 日期比较统一使用 `int(s.toYmd())` / `int(LICHUN_YMD[year])`，exact 年柱用含时分秒的 Julian Day 比较。
  - 三个测试案例：1987/3/14 16:30→丁卯/癸卯/壬戌/戊申；1998/1/19 16:00→丁丑/癸丑/丙寅/丙申；2000/2/1 00:30→己卯/丁丑/己丑/甲子
- **农历计算**：完全自包含的 `lunar_core.py`，基于 LY_DATA V6B 天文表，覆盖 1899-2060 年。

- **命格算法（已验证 12/12 测试全过）**：直接用 `TEN_GOD[日干][月干]` → 格局映射，**一行代码**：
  ```python
  def calc_mingge(day_stem, month_stem):
      return TEN_GOD_TO_GE[TEN_GOD[day_stem][month_stem]]
  ```
  - 9个普通格：正官→正官格，偏官→偏官格，七杀→七杀格，正印→正印格，偏印→偏印格，食神→食神格，伤官→伤官格，正财→正财格，偏财→偏财格
  - 特殊格：比肩→比肩格，劫财→阳刃格
  - **不需要藏干强度表，不需要透干逻辑**
  - "财才格" = "正财格" 的别名（2024/2/10 案例验证）

- **喜用神算法**：
  - 天干强度表（10天干 × 12月令地支）
  - 地支藏干强度表（12地支藏干 × 12月令地支）
  - 同类总分（日主五行 + 生我五行）vs 异类总分（克我 + 我克 + 泄我）
  - 身强 → 宜泄（取异类）；身弱 → 宜扶（取同类）

- **calc.py TEN_GOD table bug（2026-04-26 已修复）**：
  - 100 个条目**全部写错** — 用的是缩写（比/劫/食/伤）而非全称（比肩/劫财/食神/伤官）
  - 修复：替换为完整的十神表（全称版本），重新验证 12 个案例

- **代码位置**：所有 Python 文件统一放在 `scripts/` 下，数据文件放在 `data/` 下。
- **代码架构（6个文件）**：
  ```
  scripts/
  ├── main.py    # CLI 入口，命令路由，时间解析
  ├── calc.py    # 八字计算核心（常量和计算逻辑）
  ├── report.py  # 输出格式化（单人详情 / 联合分析）
  ├── store.py   # 数据存储（users.json / active.json）
  ├── lunar_core.py # 自包含农历/八字底层换算
  └── test_lunar_core.py # 单元测试（12 个固定样例 + 128 个随机日期）
  ```
- **测试命令**：`python3 -m unittest scripts/test_lunar_core.py`
- **已实现功能**：
  - 四柱天干地支（含藏干）
  - 五行纳音
  - 十神（以日干为中心）
  - 地支阴阳
  - 旬空
  - 胎元、胎息、命宫、身宫
  - 大运排盘（10步大运）
  - 神煞：桃花、天乙贵人、驿马、将星、劫煞
  - 旺衰判断（量化算法：月令强度 × 天干 + 藏干权重）
  - 喜用判断
  - 联合分析：合冲刑害、五行相生、婚配

---

## 注意事项

- `python3 scripts/main.py joint` 支持2-N人联合分析，默认用当前激活用户
- 激活多个用户时，所有人的摘要都注入 context
- 若只激活一人，格式同单人摘要
- 注入摘要时放在回复最前面，然后回答问题
- 大运排盘需要性别参数（第7个参数：男=1，女=0）

## 架构可复用性

本 skill 的多人+联合分析架构可复用到其他领域：
- 任何「alias + 结构化数据 + 联合分析」场景都适用
- 核心数据结构：`users.json`（key=alias）、`active.json`（当前激活列表）
- `scripts/main.py`（入口）+ `scripts/calc.py`（计算）+ `scripts/report.py`（展示）+ `scripts/store.py`（存储）+ `scripts/lunar_core.py`（农历换算）
- 联合分析的维度（合冲刑害/五行/喜用等）可根据不同领域替换
