---
name: comprehensive-divination-skill
version: 1.0.1
critical_instructions:
  - "MANDATORY: Before casting any divination, you MUST complete the 'Mandatory Workflow Checkpoints' section below in order. Do not skip any checkbox."
  - "MANDATORY: You MUST ask the user to confirm: (1) which divination method to use, (2) the city/location for true solar time calibration. Do not guess either."
  - "MANDATORY: Do not proceed to Step 0 (time anchor) until both confirmations above are collected."
  - "MANDATORY: Use the `clarify` tool to ask these checkpoint questions. Do not just narrate the questions in text without calling the tool."
description: 算卦综合 Skill，提供小六壬、六爻纳甲、梅花易数、大六壬四种算卦方法。含智能路由（根据问题自动推荐方法）、基础知识库（天干地支、阴阳五行、八卦、六亲）、以及可独立调用的 Python 计算脚本。所有涉时方法已升级为基于 zhdate 的精确农历/节气/干支计算。触发关键词：算、占卜、卜卦、算算、测算、求测、预测、小六壬、六爻、梅花易数、大六壬、马前课、掐指、摇卦、铜钱卦、起卦、断卦。
description_en: "A comprehensive Chinese metaphysics Skill that integrates four classical divination methods — Xiao Liu Ren (小六壬), Liu Yao Na Jia (六爻纳甲), Mei Hua Yi Shu (梅花易数), and Da Liu Ren (大六壬). Features an intelligent routing matrix that auto-recommends the optimal method based on question complexity, decision importance, time-sensitivity, and domain. All time-sensitive methods use zhdate for precise lunar calendar / solar-term / ganzhi calculation. Includes true solar time correction for any city. Triggers: divination, fortune telling, oracle, I Ching, hexagram, Meihua, Liu Yao, Da Liu Ren, predict."
author: comprehensive-divination-skill contributors
license: MIT
tags:
  - divination
  - i-ching-systems
  - i-ching
  - liu-yao
  - mei-hua
  - xiao-liu-ren
  - da-liu-ren
  - bazi
  - ganzhi
  - 玄学
  - 占卜
  - 算命
---

# 算卦综合 Skill

本 Skill 整合四种主流算卦方法（小六壬、六爻、梅花易数、大六壬），按"智能路由 → 按需加载 → 执行算卦"的流程工作。

## 📑 Quick Navigation

| 你想知道... | 跳到 |
|---|---|
| 🚦 **执行前必看**（4 个硬约束 Checkpoint + 反模式）| [MANDATORY WORKFLOW CHECKPOINTS](#-mandatory-workflow-checkpoints) ← **必读** |
| ⚠️ **当前实现关键点**（北京时间基准 / 跨日处理）| [重大变更](#-重大变更当前实现) |
| 🪤 **执行前必读**（11 条已知坑 + 实战术）| [已知陷阱](#-已知陷阱执行前必读) |
| 🏗️ **架构 + 路由** | [架构总览](#架构总览) → [路由与工作流](#路由与工作流skillmd-主指令) |
| 📚 **方法细节** | [各方法执行流程](#各方法执行流程) |
| 🛠️ **脚本使用** | [脚本速查](#脚本速查) |
| ➕ **扩新术种** | [扩展指南](#扩展指南) |
| 🌍 **海外用户** | [README § 🌍 International Users](README.md#-international-users--international-users) |
| 📂 **真实案例** | [examples/re-consultation-comparison.md](examples/re-consultation-comparison.md) |

## 🚦 MANDATORY WORKFLOW CHECKPOINTS

> **这段是硬约束**。在执行任何算卦之前，**必须**按顺序完成下列每一项。任何一项跳过都视为违反本 SKILL。

**🔴 在使用 `clarify` 工具问完这两个问题之前，禁止调用任何 `--snapshot` 或起卦脚本。**

- [ ] **Checkpoint 1: 确认起卦方法**
  - **动作**：用 `clarify` 工具问用户："用哪种方法算这个卦？"，提供 4 个选项（六爻/梅花/小六壬/大六壬）+ 推荐
  - **禁止**：❌ 不要直接挑一个方法开算 ❌ 不要假设"用户上次用了六爻这次也用"
  - **例外**：仅当用户**自己已明确说**"用六爻算"时，可跳过

- [ ] **Checkpoint 2: 确认城市/经度（真太阳时校准）**
  - **动作**：用 `clarify` 工具问用户："你当前所在城市？"，提供 5 个选项（成都/北京/上海/手动经度/跳过）
  - **禁止**：❌ 不要基于"用户历史对话常用 X 城市"猜测 ❌ 不要默认"用户在成都"
  - **例外**：仅当用户**自己已明确说**"我在 X"时，可跳过

- [ ] **Checkpoint 3: 报告校正结果**
  - **动作**：向用户展示：📍 城市（经度） + 北京时间 → 真太阳时 + 偏移分钟数 + 时辰
  - **目的**：让用户**看到**校正结果再继续（避免默默算错）

- [ ] **Checkpoint 4: 起卦 + 解读 + 免责声明**
  - **必须输出**：⏱ 时间标注 + 🎯 方法说明 + ⚠️ 末尾免责声明
  - **禁止**：❌ 不要省略免责声明（这是本 SKILL 的合规底线）

**📋 实际执行的指令模板**：

```
[第 0 步] 完成上述 4 个 Checkpoint
[第 1 步] 加载 router/matching-matrix.md
[第 2 步] 加载方法对应的 references
[第 3 步] 调用 scripts/* Python 脚本
[第 4 步] 输出卦象 JSON + 解读 + 应期 + 免责声明
```

**❌ 反模式（绝不能这样）**：
- 跳过 Checkpoint 1 直接挑方法
- 跳过 Checkpoint 2 猜城市
- 跳过 Checkpoint 3 不展示校正结果
- 跳过 Checkpoint 4 的免责声明
- 用纯文字描述要问什么问题（必须用 `clarify` 工具实际调用）

## ⚠️ 重大变更（当前实现）

**时间基准改为"北京时间（UTC+8）"**，不再用 `datetime.now()` 拿本地挂钟时间。

- **影响**：海外用户（西经/东经区域）能拿到**正确的当地 TST**，不会"跨日错位"
- **API**：
  - `get_beijing_time()` —— 强制取北京时间（零网络依赖）
  - `longitude_to_true_solar(bj_dt, lon)` —— 北京时间 + 经度 → 当地 TST
  - `datetime_to_shichen(dt)` —— datetime → 十二时辰
  - `get_full_pipeline(dt=None, longitude=None)` —— 一站式 pipeline
- **向后兼容**：`get_current_lunar_info()` 入参/返回字段不变，内部已改用新 pipeline
- **SKILL 流程推荐写法**：
  ```python
  from common import get_beijing_time, get_full_pipeline
  bj = get_beijing_time()                    # 北京时间
  info = get_full_pipeline(longitude=104.06) # 成都 TST
  ```
- **跨日处理**：TST 校正后 `tst_datetime` 可能落在前一天/后一天（如北京时间 6/15 06:00 → 纽约 TST 6/14 17:00），**这是天文事实不是 bug**

## ⚠️ 已知陷阱（执行前必读）

1. **`zhdate` 版本现实与文档不符**：`requirements.txt` 写的是 `zhdate>=1.0`，但 PyPI 上 Windows 平台**最高只有 0.1**（1.0 只发了 macOS ARM wheel，无 Windows 版本）。可直接装 `pip install zhdate==0.1`，API 兼容。脚本实际用到的 `ZhDate.from_datetime / to_datetime / leap_month / lunar_year/month/day` 在 0.1 中全部存在，已端到端验证。
2. **默认 `python` 解析到 Hermes venv，但 venv 没装 pip 也没装第三方包**。直接 `python scripts/...` 会报 `ModuleNotFoundError`。先 bootstrap：`python -m ensurepip` 然后 `python -m pip install zhdate==0.1`。
3. **`common.hour_to_shichen(hour)` 返回的是 `(地支名字符串, 1-12 整数)` 元组**，不是直接的索引。用法是 `shichen_name, hour_idx = common.hour_to_shichen(hour)`。对应的字典是 `common.DIZHI_SHICHEN`（key=地支名字符串），不是按整数索引。
4. **`xiao_liuren` 的入口是 `by_month_day_hour(month, day, hour_idx)`**，不是 SKILL 旧版暗示的 `calc_xiao_liuren()`。`calc_gong` / `LIU_GONG` / `by_numbers` 都在，但前两者是内部辅助。
5. **`liuyao_yaogua.py --json --day-tg 乙 --day-dz 卯` 端到端可用**，输出包含世应、动爻、六亲、六神、旬空，可直接喂给 LLM 断卦。**不要**用 `--auto`（不会取冻结时间）。
6. **断卦时优先看动爻、月建、日辰三件事**，六兽只作辅助（参考 `references/liuyao/duangua.md`）。凡遇"用神两次出现"（如本卦二爻+五爻都是官鬼）应取**动爻**为主静爻为辅。
7. **真太阳时校正跨时辰边界**时（如 16:49 北京 → 15:46 成都 TST），必须用**校正后的浮点小时**重新跑 `hour_to_shichen`；申时(15-17)未跨则沿用原时辰。已校正的 `snapshot['shichen']`/`shichen_idx` 就是结果。
8. **TST 校准对海外用户是错的**（已修复）：`get_current_lunar_info` 早期版本把 `datetime.now()` 拿到的本地挂钟**直接当成北京时间**再做 `(经度-120°)*4分钟` 修正，纽约用户传 `--lon -74.006` 会得到错的"申时"而非真实的"寅时"。**当前实现改为**：先取北京时间（`datetime.utcnow() + 8h`）→ 再用经度做 TST 校准 → 跨日自动处理。
9. **重复复卦会"卦气散"**：传统易学里对同一事反复起卦（3+ 次）会让信号失真。本 skill 工作流在路由层有"已问过同类问题 → 建议改用别的方法或休息"的设计意图，但**当前还没硬限**。操作建议：复卦前先回顾前 N 次结论；若前 3 次信号一致，**别再问**。如果前 3 次信号矛盾，可换方法或等 24 小时再问。
10. **"算卦综合"是过宽的命名**（已修复）：SKILL 早期版本标题/description 写"国学占卜综合"，会让 marketplace 用户以为涵盖紫微/八字/奇门/太乙，实际只覆盖 4 种起卦方法。当前统一改为"算卦综合"，命名匹配实际能力。
11. **网络降级有 0.3-0.8s 延迟**：`--city` 未知城市名时，会调用 Open-Meteo Geocoding API（urllib 标准库，无需 requests）。首次查询慢，**结果会缓存到 `scripts/_geo_cache.json`，下次 0ms 命中**。完全离线场景下网络降级会失败，应**改用 `--lon` 传经度**。**网络调用与 zhdate 安装、起卦计算完全独立**，最坏情况（没网+没缓存+没坐标）只是 city 查询失败，**不会影响核心起卦流程**。
12. **`_geo_cache.json` 跟踪进 git**：该文件已加入 `.gitignore`（每用户本地缓存不同），但首先生成时会创建。

完整排查细节、API 真实签名见 `references/comprehensive-divination-skill-pitfalls.md`。

## 实战陷阱（复占 4 次后总结）

下列条目来自实际多日复占同一事件积累的教训，与第 1-7 条同等优先级：

8. **复占必须换变量。** 同一问题反复起卦 → 卦气散 → 结论模糊。合法复占 = 换角度（如"会不会过"→"HR 多久回音"）。用户焦虑反复问同一事时，**劝停比继续起卦更负责**。
9. **日期先算后用。** 用户描述"上上周四"等相对时间时，先用 `date` 算术出绝对日期再起卦。**错一天月令可能跨**，整个旺衰判断会错。
10. **跨月令 = 月柱换 = 五行背景改。** 芒种/大雪等节气交月后，月干支与月令五行全变。`common.py --snapshot` 返回的 `month_gz` 是权威源，不要凭"calendar 是几月"判断。
11. **完整起卦流程（7 步）**：
    1. `python common.py --snapshot --city 城市` 冻结时间（**第一步必须做**）
    2. 四维分析（领域/重要度/时效/复杂度）→ 选方法
    3. 用户确认方法后，若未提供城市则补问
    4. 按需加载 `references/<method>/`
    5. 调用 `<method>.py` 显式传参（**不要 `--auto`**）
    6. 综合 references + 五行 + 动爻月建日辰 解读
    7. 输出含时间标注 + 方法说明 + 末尾免责声明
12. **跨时区警告必须醒目。** 真太阳时校正跨过时辰边界（如 16:49 北京→15:46 成都 申→未），必须用 `tst_offset_min` 重新跑 `hour_to_shichen`，**不能沿用原时辰**。

> 复占实战补充（2026-06-15）：上面 4 条坑（复占换变量 / 日期先算 / 跨月令 / 完整流程）来自用户连续 4 天问"某公司一面是否通过"的实战总结。当用户**反复问同一事**时，把"卦气已散、该用行动替代"明确说出来，比继续起第 5 卦更负责。

## 架构总览

```
用户输入 "帮我算个事"
  ↓
【第零层：时间锚定】立即冻结当前时间（datetime.now()），防止流程延迟导致边界时刻漂移
  ↓
【第一层：路由判断】加载 references/router/matching-matrix.md
  ├── 问题分析（复杂程度 / 决策重要性 / 时效性 / 领域）
  ├── 四维加权评分 → 推荐最优方法
  └── 用户确认使用哪种方法
  ↓
【Step 5.5：真太阳时校准】询问用户当前所在城市 → 城市→经纬度 → 对冻结时间做真太阳时校正
  ├── 若用户跳过（不提供位置）：默认北京时间（东经 120°）
  ├── 若用户在已知城市列表中：自动查表获得经纬度
  └── 若用户提供具体经纬度：直接使用
  ↓
【第二层：按需加载】只加载选取方法所需的 references
  ├── 小六壬：references/xiao-liuren/method.md + references/xiao-liuren/liugong.md
  ├── 六爻：references/liuyao/method.md + references/liuyao/najia.md + references/liuyao/duangua.md
  ├── 梅花易数：references/meihua-yishu/method.md
  ├── 大六壬：references/da-liuren/method.md + references/da-liuren/shier-tianjiang.md + references/da-liuren/sanzhuan-faze.md
  └── 所有方法共用：references/core/ 中的基础知识（按需读取单份文件）
  ↓
【第三层：执行占卜】
  ├── 确定性计算（干支查找、掌诀推算、摇卦模拟）
  │     → 优先调用 scripts/ 中的 Python 脚本，传入已校正的时间参数
  └── 解读性断语（五行生克、六亲应期）→ AI 基于 references 内容推理
  ↓
输出结果（含真太阳时校正标注）
```

## 路由与工作流（SKILL.md 主指令）

### 触发条件

当用户提出占卜相关请求且未指定具体方法时，触发路由模式。
若用户已明确指定方法（如"用六爻算"、"小六壬起一卦"），跳过路由直接进入对应方法。

### 路由步骤

**Step 0 — 时间锚定（必须最先执行）**：

当用户触发占卜（无论是否指定方法），立即冻结当前时间。注意：不要调用 `datetime.now()` 后再执行其他操作——必须在流程入口第一时间锚定。

Python 端执行：
```bash
python scripts/common.py --snapshot [--city 城市名] [--lon 东经]
```
若用户尚未提供位置，先行冻结（不含 TST），待第 1.5 层补充位置后再重新计算。

返回的 JSON 结构包含：`frozen_at`（ISO 8601 时间戳）、`bj_hour`（北京时间）、`ts_hour`（真太阳时，若已提供位置）、`shichen`、`shichen_idx` 等全部字段。

**Step 1 — 加载路由矩阵**：读取 `references/router/matching-matrix.md`

**Step 2 — 四维分析**：从用户问题中提取：
- 复杂程度（简单是非题=1 / 多因素交叉=2 / 系统性推演=3）
- 决策重要性（日常琐事=1 / 中等决策=2 / 重大决策=3）
- 时效要求（即时=3 / 可等=2 / 不急=1）
- 问题领域（出行/寻物/运势/感情/事业/健康/投资/搬迁/随机）

**Step 3 — 加权评分**：按维度权重（决策35% + 复杂25% + 领域25% + 时效15%）计算各方法总分

**Step 4 — 特殊规则**：
- 用户报了数字 → 梅花易数 ×1.5 加分
- 用户指定了日期 → 大六壬 ×1.5 加分
- 问题 < 5字 → 小六壬 ×1.5 加分
- 已指定方法 → 直接放行

**Step 5 — 输出推荐**：排名 + 评分理由，等待用户确认

**Step 5.5 — 真太阳时校准（用户确认方法后、执行前）**：

在用户确认占卜方法后、开始执行前，询问位置：

> 请告知你当前所在的城市（如：成都），用于真太阳时校准。
> 若跳过，默认使用北京时间（东经 120°）。

处理逻辑：
- 用户提供城市名 → 调用 `scripts/common.py --snapshot --city <城市>` 重新获取含 TST 的时间快照
- 用户提供经纬度 → 调用 `scripts/common.py --snapshot --lon <东经>`
- 用户跳过 → 使用 Step 0 中无校正的快照，标注"基于北京时间"
- 城市不在已知列表 → 告知"未知城市，请输入当地东经（如成都=104.06）"

校正完成后，展示给用户确认：
> 📍 成都（104.06°E）真太阳时修正：
> 北京时间 15:22 → 真太阳时 14:21（−61 分钟）
> 时辰：申时 → **未时**（已跨边界）

**Step 6 — 按需加载**：加载选取方法所需的 references（同原第二层）

### 各方法执行流程

#### 小六壬
1. 使用 Step 0/5.5 已校正的农历月日时（或接受用户报数）
2. 执行掌诀推算：月→日→时三步定位
3. 读取 `references/xiao-liuren/liugong.md` 获取落宫断语
4. 可选：调用 `scripts/xiao_liuren.py` 明确传入 `-m -d -t` 参数（而非 `--auto`）

#### 六爻
1. 模拟铜钱摇卦六次（随机 3 bit × 6），或直接调用 `scripts/liuyao_yaogua.py --json`
2. 确定本卦 → 装卦（纳甲+六亲+世应+六神；日干支使用已冻结快照中的值）
3. 读取 `references/liuyao/najia.md` 获取纳甲表
4. 读取 `references/core/liuqin.md` 获取六亲定义
5. 读取 `references/liuyao/duangua.md` 执行断卦规则
6. 综合五行生克 + 六兽 + 时间应期 → 输出解读

#### 梅花易数
1. 确定起卦方式（时间法/报数法/物象法）
2. 若用时间法：使用已校正的真太阳时年支+月+日+时计算上卦、下卦、动爻
3. 读取 `references/core/bagua.md` 获取八卦对照表
4. 确定体卦、用卦、互卦、变卦
5. 体用五行生克判断 + 卦辞引用 → 输出解读
6. 可选：调用 `scripts/meihua_qigua.py` 明确传入参数

#### 大六壬
1. 确定月将（按节气）+ 时辰（使用已校正的真太阳时时辰）
2. 构建天地盘矩阵
3. 确定四课
4. 按九大法则发传（读取 `references/da-liuren/sanzhuan-faze.md`）
5. 天将布局（读取 `references/da-liuren/shier-tianjiang.md`）
6. 综合断课 → 输出事态三阶段

### 基础知识加载策略

`references/core/` 中的文件按实际需要加载，不一次性全部读取：
- 涉及天干地支计算 → 读 `core/tiangan-dizhi.md`
- 涉及五行生克 → 读 `core/yinyang-wuxing.md`
- 涉及八卦/六十四卦 → 读 `core/bagua.md`
- 涉及六亲/用神 → 读 `core/liuqin.md`

### 输出规范

所有占卜结果应包含以下元素：

1. **时间标注**：显示冻结时间、地点、真太阳时校正信息
   ```
   ⏱ 起卦时间：2026-05-29 15:22（北京时间）
   📍 成都（104.06°E）真太阳时：14:21（−61 分钟）
   🕐 时辰：未时
   ```

2. **方法说明**：标注使用的占卜方法及依据

3. **免责声明**（末尾必加）：
   > 占卜结果仅供参考，请结合实际情况理性判断。

### 脚本使用指南

`scripts/` 目录提供可独立调用的 Python 脚本（依赖 `zhdate` 库，需在 venv 中运行）。

**时间锚定（最先调用）**：
```bash
# 冻结时间 + 成都真太阳时
python scripts/common.py --snapshot --city 成都
# 仅冻结时间，不校准时区
python scripts/common.py --snapshot
```

**占卜脚本**：

| 脚本 | 功能 | 推荐调用方式（已校正） | Python 直接调用（agent 复用） |
|------|------|----------------------|-------------------------------|
| `common.py` | 干支/五行/农历/月将 + 真太阳时校正 + 城市坐标查询 | `--snapshot --city 成都` | `common.get_current_lunar_info(dt=frozen, longitude=104.06)` |
| `xiao_liuren.py` | 小六壬掌诀推算 | `-m {lunar_month} -d {lunar_day} -t {corrected_hour}` | `xiao_liuren.by_month_day_hour(month, day, hour_idx)` |
| `liuyao_yaogua.py` | 六爻摇卦 + 纳甲装卦 | `--json --day-tg {snapshot.day_tg} --day-dz {snapshot.day_dz}` | `liuyao_yaogua.<主函数>`（见 pitfalls.md） |
| `meihua_qigua.py` | 梅花易数起卦 | `-d {solar_date} -t {corrected_hour}` | `meihua_qigua.by_time(...)` 或 `by_numbers(...)` |
| `da_liuren.py` | 大六壬天地盘 + 四课三传 | `-d {solar_date} -t {corrected_hour}` | `da_liuren.build_tiandi_pan(...)`、`build_sike(...)`、`fa_sanzhuan(...)` |

> **重要**：占卜脚本的 `--auto` 模式始终使用 `datetime.now()`，不会取已冻结的快照。
> 在 SKILL 工作流中，应从 Step 0 的快照中提取已校正的参数，显式传递给脚本。

所有脚本的农历转换基于 `zhdate` 库；月将按节气判定；日干支自动推算。安装依赖：

```bash
pip install -r requirements.txt
```

唯一外部依赖为 `zhdate`（PyPI 包），其余均为 Python 标准库，无系统工具依赖。可 zip 打包后在其他设备直接导入使用。

## 故障排查与真实 API 入口

- `references/comprehensive-divination-skill-pitfalls.md` — 安装踩坑、venv 引导、每个脚本的**真实公开 API 入口与签名**、断卦常见误区、与 `references/router/matching-matrix.md` 配合使用。

### 扩展指南

新增术种（如奇门遁甲）时：
1. 在 `references/` 下新增子目录（如 `qimen-dunjia/`）
2. 在 `scripts/` 下新增计算脚本
3. 更新本 SKILL.md 的触发关键词和路由逻辑
4. 更新 `references/router/matching-matrix.md` 的评分矩阵
