# comprehensive-divination-skill 故障排查与真实 API 入口

> 本文件是 comprehensive-divination-skill/SKILL.md 的补充，记录 SKILL.md 未明确写出但**实际验证可用**的 API 入口、常见踩坑与最小复现命令。
> 写于 2026-06-10，基于 venv `C:\Users\Sprint\AppData\Local\hermes\hermes-agent\venv\`（Python 3.11）+ 系统 Python 3.13 双侧验证。

---

## 1. 安装踩坑

### 1.1 `zhdate` 版本

`requirements.txt` 写的是 `zhdate>=1.0`，但：
- **PyPI Windows 平台最高只有 0.1**
- PyPI 上确实存在 `1.0.macosx-11.0-arm64`（macOS ARM 专用 wheel），但无 Windows 版本
- 直接 `pip install "zhdate>=1.0"` 在 Windows 会失败

**正确安装**：

```bash
# venv 路径（默认 python 解析到的）
C:\Users\Sprint\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m pip install "zhdate==0.1"
# 或系统 Python
C:\Users\Sprint\AppData\Local\Programs\Python\Python313\python.exe -m pip install "zhdate==0.1"
```

API 在 0.1 中已涵盖脚本用到的全部功能：
- `ZhDate.from_datetime(dt)` / `to_datetime()` ✓
- `.leap_month` / `.lunar_year` / `.lunar_month` / `.lunar_day` ✓

### 1.2 venv 缺 pip 引导

Hermes 自带 venv 默认**未装 pip**，`python -m pip` 会报 `No module named pip`。
要先 bootstrap：

```bash
C:\Users\Sprint\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe -m ensurepip
# 成功后 pip 24.0 + setuptools 79.0
```

### 1.3 验证 zhdate 在目标解释器中可用

```bash
python -c "import zhdate; print(zhdate.ZhDate.from_datetime)"
# 若报 ImportError 说明装错了解释器
```

---

## 2. 时间锚定（Step 0 真实流程）

### 2.1 CLI 入口（最方便）

```bash
# 仅冻结时间（默认北京时间）
python scripts/common.py --snapshot

# 冻结 + 城市真太阳时
python scripts/common.py --snapshot --city 成都
# 或直接给经度
python scripts/common.py --snapshot --lon 104.06
```

输出 JSON 关键字段：
- `frozen_at` — ISO 8601 时间戳
- `bj_hour` — 北京时间浮点小时
- `ts_hour` — 真太阳时浮点小时（启用城市时）
- `shichen` / `shichen_idx` — 真太阳时对应的地支名 / 1-12 整数
- `tst_offset_min` — 真太阳时相对北京时间的分钟偏移
- `day_tg` / `day_dz` / `day_gz` — 日干支

### 2.2 Python 入口（agent 复用）

```python
from datetime import datetime
import sys
sys.path.insert(0, r"C:\Users\Sprint\AppData\Local\hermes\skills\comprehensive-divination-skill\scripts")
import common

frozen = datetime.now()
snapshot = common.get_current_lunar_info(dt=frozen, longitude=104.06)
# snapshot 字段与 CLI --snapshot 输出一致
```

### 2.3 跨时辰边界处理

真太阳时可能让时辰**跨越边界**（如北京 16:49 → 成都 15:46 TST，15-17 申时内未跨；若是 17:05 北京 → 16:02 成都 TST 仍在申时）。处理原则：

```python
# 永远用 ts_hour 重新计算时支，不要直接改 bj_hour
shichen_dz, shichen_idx = common.hour_to_shichen(snapshot['ts_hour'])
# 显式给用户展示：
bj_str = f"{int(snapshot['bj_hour']):02d}:{int((snapshot['bj_hour']%1)*60):02d}"
tst_str = f"{int(snapshot['ts_hour']):02d}:{int((snapshot['ts_hour']%1)*60):02d}"
print(f"北京 {bj_str} → 真太阳时 {tst_str}（{snapshot['tst_offset_min']:+.0f} 分钟） | {shichen_dz}时")
```

---

## 3. 各脚本真实公开 API

### 3.1 `common.py`（基础库）

公开常量：`TIANGAN` / `DIZHI` / `DIZHI_WUXING` / `DIZHI_SHICHEN` / `DIZHI_SHENGXIAO` / `TIANGAN_JIGONG` / `WUXING` / `WUXING_SHENG` / `WUXING_KE` / `LIUHE` / `LIUCHONG` / `SANHE` / `XUNKONG_MAP` / `BAGUA_XIANTIAN` / `LIUSHISI_GUA` / `SEASON_WANG` / `_CITY_COORDS`

| 函数 | 签名 | 返回 | 说明 |
|------|------|------|------|
| `hour_to_shichen(hour: float)` | `(name: str, idx: int 1-12)` | 浮点小时 → (地支名, 序号) | **元组**，不是单一索引 |
| `get_wuxing_relation(a, b)` | `'生'/'克'/'被生'/'被克'/'同'` | 五行关系判定 | |
| `get_liuhe(zhi)` / `get_liuchong(zhi)` | `str` | 六合 / 六冲对支 | |
| `get_xunkong(ri_tg, ri_dz)` | `(str, str)` | 旬空地支 | |
| `num_to_gua(num)` | `{'name','symbol','wuxing'}` | 1-8 → 卦 | |
| `get_64gua_name(up, down)` | `str` | 上下卦数 → 卦名 | |
| `get_season(month)` | `dict` (含 `season`/`is_ji_month`/`wang_wuxing`) | 农历月 → 季节 | |
| `get_wuxing_status(wx, season)` | `'旺'/'相'/'休'/'囚'/'死'` | 五行在某季的状态 | |
| `get_city_coordinates(name)` | `dict or None` | 城市名 → 经纬度 | 支持模糊匹配 |
| `correct_to_true_solar(h, m, lon, d)` | `(float, int)` | 北京时间 → 真太阳时 | |
| `get_day_ganzhi(d)` | `(日干, 日支, 日干支)` | | |
| `get_year_ganzhi(year)` / `get_month_ganzhi(year_tg, lunar_month)` | `tuple` | | |
| `solar_to_lunar_date(y, m, d)` | `dict` | 完整农历+干支 | 依赖 zhdate |
| `get_yuejiang_by_solar_term(d)` | `(地支, 月将名)` | 节气 → 月将 | |
| **`get_current_lunar_info(dt, lon, lat)`** | `dict` | **一站式：冻结时间+真太阳时+干支+月将** | agent 复用首选 |

**`hour_to_shichen` 的返回值是元组**，这是个高频踩坑点：

```python
# 错 ❌
hour_idx = common.hour_to_shichen(16)         # 得到 tuple ('申', 9)
common.DIZHI_SHICHEN[hour_idx]               # KeyError: tuple

# 对 ✓
shichen_name, hour_idx = common.hour_to_shichen(16)
common.DIZHI_SHICHEN[shichen_name]            # '15:00-17:00'
```

### 3.2 `xiao_liuren.py`（小六壬）

公开常量：`LIU_GONG`（六宫信息表）

| 函数 | 签名 | 说明 |
|------|------|------|
| `by_month_day_hour(month: int, day: int, hour_idx: int)` | `dict` | **主入口** — 月日时掌诀推算 |
| `by_numbers(n1, n2, ...)` | `dict` | 报数法 |
| `calc_gong(...)` | `int` | 内部计算落宫序号 |
| `get_current_lunar_info(...)` | `dict` | 重导出 common 同名函数 |
| `validate_month/day/hour` | — | 整数范围校验 |

**注意**：SKILL.md 旧版暗示的 `xiao_liuren.calc_xiao_liuren()` **不存在**，正确入口是 `by_month_day_hour`。

最小调用：

```python
import common, xiao_liuren
lunar = common.solar_to_lunar_date(2026, 6, 10)
shichen_name, hour_idx = common.hour_to_shichen(15.77)  # 真太阳时
result = xiao_liuren.by_month_day_hour(lunar['lunar_month'], lunar['lunar_day'], hour_idx)
print(result['result']['name'], '|', result['result']['summary'])
```

### 3.3 `liuyao_yaogua.py`（六爻）

**最佳用法是 CLI**（`--json` 模式直接返回完整装卦 JSON，无需手写断卦逻辑）：

```bash
python scripts/liuyao_yaogua.py --json --day-tg 乙 --day-dz 卯
```

公开常量（agent 复用作断卦参考）：
- `GUA_SYMBOLS` / `GUA_GONG` / `GONG_GUA_LIST` / `NAJIA` / `LIUQIN_RULES`
- `SHI_POSITIONS` / `SHI_YING` / `YING_OFFSET`
- `LIUSHEN` / `WUXING` / `WUXING_SHENG` / `WUXING_KE`

Python 直接调用需先 import 内部函数，建议**优先用 CLI**：

```python
import subprocess, json
out = subprocess.check_output(
    ['python', 'scripts/liuyao_yaogua.py', '--json', '--day-tg', day_tg, '--day-dz', day_dz],
    cwd=r"C:\Users\Sprint\AppData\Local\hermes\skills\comprehensive-divination-skill",
    text=True,
)
result = json.loads(out)
# result 字段：gua_name / gua_gong / gong_wuxing / dong_lines / shi_line / ying_line
#              / lines[{pos, pos_name, yaoxiang, is_dong, tian_gan, di_zhi, wuxing,
#                        liuqin, liushen, shi_ying}] / xunkong
```

### 3.4 `meihua_qigua.py`（梅花易数）

公开常量：`BAGUA` / `DIZHI` / `GUA_NAMES` / `WUXING_KE` / `WUXING_SHENG`

| 函数 | 说明 |
|------|------|
| `by_time(...)` | 时间起卦 |
| `by_numbers(...)` | 报数起卦 |
| `num_to_gua(num)` | 数字 → 卦 |
| `build_result(...)` | 内部构造结果 |
| `get_current_lunar_info(...)` | 重导出 |

### 3.5 `da_liuren.py`（大六壬）

公开常量：`DIZHI` / `DIZHI_WUXING` / `TIANGAN` / `TIANGAN_JIGONG` / `WUXING_KE`

| 函数 | 说明 |
|------|------|
| `build_tiandi_pan(...)` | 天地盘构建 |
| `build_sike(...)` | 四课 |
| `fa_sanzhuan(...)` | 三传（九大法则发传） |
| `get_tianpan_at(...)` | 天盘某时辰位 |
| `get_day_ganzhi(...)` / `get_yuejiang_by_solar_term(...)` / `get_shichen(...)` | 重导出 common |

---

## 4. 断卦常见误区

1. **"用神出现两次"**：本卦中六亲可重复（如本坎为水中官鬼土可在二爻和五爻都出现）。**优先看动爻**，静爻只作辅助参证。
2. **"世爻空亡 = 完蛋"**：空亡要看是否**出空**（走出当前旬）。本课若日干支为乙卯属"甲辰旬"（寅卯空亡），则辰、卯以外的爻不空。`result['xunkong']` 字段会直接给出。
3. **"兄弟持世 = 一定不利"**：兄弟主耗财/竞争，但**兄弟动而化财**反而是好的（得财）。要看动化关系。
4. **六兽 > 五行**：错。**五行生克 + 月建日辰**是根本，六兽只补细节（青龙吉、玄武暗昧等），不能凌驾于用神旺衰。
5. **"动爻多了好"**：本课中动爻 3 个代表**事情未完全定**，不是凶也不是吉，是"未定"。要结合用神是否最终落实判断。
6. **"应期就是某天"**：应期是**窗口期**。本课中"出空日（6/13）+ 用神得生日"叠加是窗口，不是死日期。

---

## 5. 端到端最小验证（应放在 cron 巡检里）

```bash
# 跑通则视为 comprehensive-divination-skill 健康
python -c "
import sys; sys.path.insert(0, r'C:\Users\Sprint\AppData\Local\hermes\skills\comprehensive-divination-skill\scripts')
import common, xiao_liuren
lunar = common.solar_to_lunar_date(2026, 6, 10)
_, hour_idx = common.hour_to_shichen(15.77)
r = xiao_liuren.by_month_day_hour(lunar['lunar_month'], lunar['lunar_day'], hour_idx)
assert r['result']['name'], '占卜结果缺失'
print('OK:', r['result']['name'])
"
```

输出 `OK: 速喜`（或当时实际落宫）即视为通过。

---

## 6. 跟其他 references 的关系

- `references/router/matching-matrix.md` — 决定用哪个术数
- `references/xiao-liuren/method.md` + `liugong.md` — 小六壬断语
- `references/liuyao/method.md` + `najia.md` + `duangua.md` — 六爻完整方法
- `references/meihua-yishu/method.md` — 梅花易数
- `references/da-liuren/method.md` + `sanzhuan-faze.md` + `shier-tianjiang.md` — 大六壬
- `references/core/bagua.md` / `liuqin.md` / `tiangan-dizhi.md` / `yinyang-wuxing.md` — 共用基础
- **本文件** — 实际跑得通所需的踩坑 & 真实 API 索引
