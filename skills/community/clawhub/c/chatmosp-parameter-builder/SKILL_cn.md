---
name: chatmosp-parameter-builder
description: |
  chatMOSP 系统的参数构建与管理中心。负责 MSR / KMC 任务的参数查询、智能补全、
  气体熵计算、MSR↔KMC 相互作用参数转换、参数完整性处理。
  触发场景：input-coordinator 识别任务后、计算引擎执行前，需要构建或调整参数；
  或用户查询/修改当前任务参数。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_cn.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-parameter-builder

## 1. 核心职责

1. 智能参数补全：从 MOSP_database 搜索匹配模板 → 替换温度 → 计算气体熵
2. MSR / KMC 参数分离：两套参数完全独立，互不混用
3. 5 选项确认流程：每次构建参数后必须让用户确认
4. 气体熵计算：按温度自动计算 8 种气体的熵值
5. 相互作用参数转换：MSR 满吸附格式 ↔ KMC 单原子格式（文献默认 KMC）
6. 参数缺失处理：调用 literature-search 补全关键参数
7. 温度替换：用户改温度时自动重算气体熵
8. 参数验证：格式、范围、一致性、完整性检查

## 2. ⚠️ 强制流程：参数确认

无论用户请求多么明确，参数构建完成后必须展示并等待用户确认。

### 2.1 5 个选项

1. ✅ 确认 — 使用这些参数继续
2. ✏️ 修改 — 调整特定参数（温度/压强/气体分压/团簇尺寸/气体种类）
3. 📊 对比 — 多个条件对比（多温度/多压强/多团簇尺寸/多气体分压组合）
4. 🔄 切换计算模式 — 在 MSR 和 KMC 之间切换
5. ❌ 取消任务，更换体系 — 更换金属或气体体系

只有用户选择选项 1 后，才能执行计算。

## 3. MSR / KMC 参数分离原则

| 任务 | 来源 | 不应包含 |
|------|------|----------|
| MSR | MOSP_database 的 MSR 部分 + Gas + Adsorption | KMC 字段 |
| KMC | MOSP_database 的 KMC 部分（含 nspecies、s1/s2、p1、e1-e7、li 全套） | MSR 字段 |

> ⚠️ **关键**：MSR 的 `input.json` 和 KMC 的 `input.json` 是**两个独立文件，不能复用**。

## 4. MSR 参数展示模板

展示时必须使用以下格式，不得自创：

```
📊 MSR参数已准备好，请确认：

【基本信息】
- 金属元素：{metal}
- 温度：{T} K ({T-273}°C)
- 压力：{P} Pa
- 团簇半径：{R} Å
- 晶体结构：{structure}

【气体环境】
- {Gas1} 分压：{pp1}%
- {Gas2} 分压：{pp2}%

【气体熵值】（已自动计算）
- {Gas1} 熵值：{S1} eV/K ({T}K 计算值)
- {Gas2} 熵值：{S2} eV/K ({T}K 计算值)

【表面晶面参数】
- {facet1} 晶面：表面能 {γ1} eV/Å²
- {facet2} 晶面：表面能 {γ2} eV/Å²
- {facet3} 晶面：表面能 {γ3} eV/Å²（最稳定）

【表面吸附参数】（从 input.json 的 Adsorption 字段读取）
{facet1} 晶面：
  - {Gas1} 吸附能：E_ads = {E1} eV
  - {Gas2} 吸附能：E_ads = {E2} eV
{facet2} 晶面：
  - {Gas1} 吸附能：E_ads = {E3} eV
  - {Gas2} 吸附能：E_ads = {E4} eV
{facet3} 晶面：
  - {Gas1} 吸附能：E_ads = {E5} eV
  - {Gas2} 吸附能：E_ads = {E6} eV

【相互作用矩阵】（从 input.json 读取）
{facet1} 晶面：CO-CO={w1}, CO-O={w2}, O-O={w3}
{facet2} 晶面：CO-CO={w4}, CO-O={w5}, O-O={w6}
{facet3} 晶面：CO-CO={w7}, CO-O={w8}, O-O={w9}

【输出设置】
- 任务目录：{task_name}
- 生成文件：input.json, ini.xyz, {task_name}_cluster.xyz, faceinfo.txt,
  structure.png, rotation.gif

请选择：
1. ✅ 确认 - 使用这些参数继续执行 MSR 计算
2. ✏️ 修改 - 调整特定参数（温度/压强/气体分压/团簇尺寸/气体种类）
3. 📊 对比 - 多个条件对比（多温度/多压强/多团簇尺寸/多气体分压组合）
4. 🔄 切换到 KMC
5. ❌ 取消任务，更换体系
```

> ⚠️ **单位说明**：`Gas1_pp` / `Gas2_pp` 是**百分比 (%)**，不是压力值。展示时必须带 % 号。

## 5. KMC 参数展示模板

```
📊 KMC参数已准备好，请确认：

【基本信息】
- 任务类型：KMC（动力学蒙特卡洛模拟）
- 反应：{reaction}
- 温度：{T} K ({T-273}°C)
- 压力：{P} Pa
- 气体分压：{Gas1} {pp1}%, {Gas2} {pp2}%

【团簇信息】（来自 MSR 结果）
- 金属元素：{metal}
- 团簇半径：{R} Å
- 原子数量：{N} 个
- 晶体结构：{structure}
- MSR 任务目录：{msr_task_name}

【模拟参数】
- 模拟步数：{steps} 步
- 记录间隔：每 {record_int} 步一次
- 物种数量：{nspecies} 种
- 反应事件：{nevents} 种

【物种定义】
- s1: {name1}（{role1}）
- s2: {name2}（{role2}）
- ...

【产物定义】
- p1: {product_name}（事件 X、Y 生成）

【反应机制】（简要）
- {mechanism_brief}

【输出设置】
- KMC 任务目录：{msr_task_name}/KMC_{steps}steps/
- 生成文件：input.json, coverage.png, coverage_steps.png, tof.png, tof_time.png, ...

请选择：
1. ✅ 确认 - 使用这些参数继续执行 KMC 模拟
2. ✏️ 修改 - 调整特定参数（步数/温度/压强/气体分压/记录间隔）
3. 📊 对比 - 多个条件对比（多步数/多温度/多压强/多气体分压组合）
4. 🔄 切换到 MSR
5. ❌ 取消任务，更换体系

建议：
- 快速测试可先跑 10 万步
- 500 万步可获得较准确统计，但耗时更长
```

## 6. 智能参数补全流程

```
用户输入
  → 提取参数（金属、温度、气体、压力、步数、尺寸、分压）
  → 搜索 MOSP_database 匹配（金属 + 气体组合）
  → 加载匹配 example 文件
  → 替换用户指定参数（温度、步数、压力等）
  → 计算气体熵（按用户温度）
  → 检查参数完整性
  → 展示给用户确认（5 选项）
```

### 6.1 搜索匹配规则

- **金属匹配**：精确匹配（Pd、Pt、Au、Cu、Ni 等）
- **气体匹配**：气体种类集合匹配（CO+O₂ → CO 氧化环境）
- **最佳匹配**：选择金属和气体匹配度最高的 example
- **默认来源**：`mosp-for-chatMOSP/MOSP_database/`

### 6.2 优先级

1. 用户指定参数 > MOSP_database 默认值 > 系统默认值
2. 用户未指定 → 用 example 的默认值
3. example 也没 → 用系统预设（pressure=101325Pa, radius=20Å, steps=1000000）

## 7. 气体熵计算系统

### 7.1 公式

```
S(J/K/mol) = a × T^b
S(eV/K)   = (a × T^b) / 96485
```

- `a, b` 是气体特定参数（见下表）
- `T` 是温度（K）
- `96485` 是 J→eV 转换因子

### 7.2 8 种气体参数表

| 气体 | a | b |
|------|------|------|
| H₂ | 41.362 | 0.201 |
| N₂ | 82.394 | 0.148 |
| O₂ | 90.454 | 0.143 |
| CO₂ | 76.458 | 0.181 |
| CO | 85.142 | 0.147 |
| NO | 93.121 | 0.143 |
| H₂O | 64.234 | 0.18665 |
| NO₂ | 93.02 | 0.1668 |

参数通过 0~6000K 范围拟合获得，无温度范围限制。

### 7.3 计算示例

CO 在 473K：

```
S(J/K/mol) = 85.142 × 473^0.147 ≈ 210.5 J/K/mol
S(eV/K)   = 210.5 / 96485 ≈ 0.00218 eV/K
```

### 7.4 字段对应

| 任务 | 气体熵字段 |
|------|------------|
| MSR | `Gas1_S` / `Gas2_S` |
| KMC | `s1.S_gas` / `s2.S_gas` |

> ⚠️ **关键原则**：MSR 和 KMC 的气体熵必须用相同公式、相同值。

### 7.5 温度修改时必须重算

用户在确认阶段选"修改"并改温度 → 必须按 §7.1 重算每个气体的熵值并更新字段。

示例：温度从 500K 改 800K

- CO：S(500K) ≈ 0.002200 eV/K → S(800K) ≈ 0.002357 eV/K ✅
- O₂：S(500K) ≈ 0.002285 eV/K → S(800K) ≈ 0.002446 eV/K ✅

## 8. 温度替换

example 文件温度 T_example → 用户温度 T_user：

1. 更新 Temperature = T_user
2. 按 §7 重算气体熵
3. 保持其他参数（表面能、吸附能、w 矩阵等不随温度变化）

## 9. 相互作用参数转换（MSR ↔ KMC）

> ⚠️ **重要默认值**：所有文献检索返回的相互作用参数**默认视为 KMC 格式**（单个相邻原子相互作用）。如果用作 MSR 任务参数，自动转换为 MSR 格式，但必须提醒用户检查文献确认是否真的是单原子相互作用。

> **触发条件**：只对文献检索返回的参数触发；MOSP_database 自带参数不处理（假设正确）。

### 9.1 格式定义

| 格式 | 含义 | 数值范围 |
|------|------|----------|
| MSR | 满吸附总相互作用能 | 通常 > 0.5 eV（绝对值） |
| KMC | 单个相邻原子相互作用 | 通常 < 0.3 eV（绝对值） |

### 9.2 默认处理流程（文献参数）

1. 文献检索返回参数 → 默认假设为 KMC 格式
2. 自动转换为 MSR 格式（如需用作 MSR 参数）
3. 向用户展示原文数值 + 转换后数值 + 转换公式
4. 提醒用户检查文献：

```
⚠️ 相互作用参数已自动从 KMC 格式转换为 MSR 格式。
请检查原始文献，确认是单个相邻原子相互作用（per-adjacent-atom），
而不是满吸附总相互作用（full-adsorption）。

转换公式：MSR参数 = KMC参数 × 相邻位点数
- (100) 晶面：× 4
- (110) 晶面：× 2
- (111) 晶面：× 6
```

### 9.3 转换公式

**MSR 参数 = KMC 参数 × 相邻位点数**

| 晶面 | 相邻位点数 |
|------|------------|
| (100) | 4 |
| (110) | 2 |
| (111) | 6 |

### 9.4 转换示例（KMC → MSR，自动）

| 晶面 | 原 KMC 值 | 转换后 MSR 值 |
|------|-----------|---------------|
| (100) | -0.149 | -0.596（×4） |
| (110) | -0.159 | -0.318（×2） |
| (111) | -0.168 | -1.008（×6） |

### 9.5 转换时机

- **MSR 任务 + 文献参数（默认 KMC 格式）** → 自动转为 MSR + 提醒用户
- **KMC 任务 + 文献参数（默认 KMC 格式）** → 不转换
- **MOSP_database 自带参数** → 不处理（假设正确）

## 10. 参数完整性处理

搜索到 example 后必须做完整性检查：

### 10.1 关键参数缺失（E_ads、w、gamma 等）

**步骤 1**：告知用户 "{metal}.json 缺少关键数据（吸附能、相互作用矩阵）"

**步骤 2**：提供 4 个选项：

1. 文献检索补全（开放获取期刊：Nature Communications, Science Advances, PNAS, ACS Central Science, Chemical Science）
2. 文献检索补全（付费期刊：Science, Nature, JACS, Angewandte Chemie）
3. 用户直接指定参数
4. 取消任务，更换体系

**步骤 3**：选项 1/2 → 调用 literature-search；选项 3 → 等用户输入；选项 4 → 结束任务

### 10.2 次要参数缺失（Gas1_S、Gas2_S 等）

- 可自动计算（按 §7.1 公式）
- 告知用户"部分参数使用默认值或自动计算"

### 10.3 文献检索后必须重算气体熵

文献检索返回的参数不包含气体熵。无论完整性评分多少，组装 `input.json` 前必须按 §7.1 重算。

## 11. KMC input.json 必含字段

### 11.1 顶层字段

| 字段 | 类型 | 示例 |
|------|------|------|
| Element | string | `"Pt"` |
| Lattice constant | string | `"3.9239"` |
| Crystal structure | string | `"FCC"` |
| Temperature | string | `"850"` |
| Pressure | string | `"150"` |
| flag_MSR | boolean | false |
| flag_KMC | boolean | true |
| KMC | object | `{...}` |

### 11.2 KMC 对象内字段

| 字段 | 类型 | 说明 |
|------|------|------|
| nLoop | string | 总模拟步数 |
| record_int | string | 记录间隔 |
| nspecies | number | 物种数量 |
| nproducts | number | 产物数量 |
| nevents | number | 反应事件数 |
| nevents_mob | number | 移动事件数 |
| s1 / s2 | string | 物种 1/2 定义（JSON 字符串） |
| p1 | string | 产物 1 定义（JSON 字符串） |
| e1 ~ e7 | string | 反应事件 1~7（JSON 字符串） |
| li | array | 晶格相互作用矩阵 |

## 12. 参数单位速查

### MSR 参数

| 字段 | 单位 | 说明 |
|------|------|------|
| Element | 无 | Pd、Pt、Au |
| Lattice constant | Å | 晶格常数 |
| Pressure | Pa | 系统压力 |
| Temperature | K | 温度 |
| Radius | Å | 团簇半径 |
| Gas_pp | % | 分压百分比 |
| Gas_S | eV/K | 气体熵 |
| Face.gamma | eV/Å² | 表面能 |
| Face.E_ads | eV | 吸附能 |
| Face.S_ads | eV/K | 吸附熵 |
| Face.w | eV | 相互作用矩阵元 |

### KMC 参数

| 字段 | 单位 | 说明 |
|------|------|------|
| nLoop | 步数 | 模拟步数 |
| record_int | 步数 | 记录间隔 |
| mass | amu | 分子质量 |
| PP_ratio | % | 分压比例 |
| S_ads | eV/K | 吸附熵 |
| S_gas | eV/K | 气体熵 |
| Ea_diff | eV | 扩散活化能 |
| sticking | 0-1 | 粘附系数 |
| E_ads_para | eV | 吸附能参数 |
| BEP_para | eV | BEP 关系参数 |
| li | eV | 晶格相互作用矩阵 |

## 13. 错误处理

| 情况 | 处理 |
|------|------|
| 未找到匹配 example | 调用 literature-search 检索 |
| 关键参数缺失 | 提示用户并提供 4 个选项（见 §10.1） |
| 温度未指定 | 默认 500K，但需用户确认 |
| 压力未指定 | 默认 101325 Pa |
| 团簇尺寸未指定 | 默认 20 Å（MSR）或 50 Å（KMC） |
| 步数未指定 | 默认 1000000 |
| 气体种类与分压不匹配 | 提示用户检查 |

## 14. 跨技能衔接

- **input-coordinator → 本技能**：任务识别后路由到本技能
- **本技能 → literature-search**：参数缺失时调用（详见 literature-search）
- **本技能 → msr-generator**：用户确认后交付 MSR 参数
- **本技能 → kmc-simulator**：用户确认后交付 KMC 参数
- **MSR ↔ KMC 衔接**：MSR 完成后，KMC 独立从 MOSP_database 取参数，不复用 MSR `input.json`

## 15. 依赖

- **chatmosp-input-coordinator** — 任务入口
- **chatmosp-literature-search** — 参数缺失时检索
- **chatmosp-file-organizer** — 获取 MOSP_database 路径
- **chatmosp-msr-generator** — MSR 计算接收方
- **chatmosp-kmc-simulator** — KMC 模拟接收方

## 16. 文件结构

```
chatmosp-parameter-builder/
├── SKILL.md       # 本文件（中文）
└── SKILL_cn.md    # 英文版
```
## ChatMOSP 配套技能

本技能属于 ChatMOSP 技能组。完整功能需要在 ClawHub 中安装以下配套技能：

- chatmosp-input-coordinator
- chatmosp-parameter-builder
- chatmosp-msr-generator
- chatmosp-kmc-simulator
- chatmosp-literature-search
- chatmosp-file-organizer

如果缺少必要的配套技能，请先提示用户从 ClawHub 安装缺失的 ChatMOSP 技能后再继续。GitHub 仓库只作为备用安装方式。
