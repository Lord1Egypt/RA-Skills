---
name: chatmosp-kmc-simulator
description: |
  chatMOSP 系统的 KMC（动力学蒙特卡洛）模拟引擎。调用 kmc_standalone.py 通过 Wine
  环境运行 Windows 版 main.exe，执行催化剂表面反应动力学模拟，产出 TOF、覆盖度等
  动力学结果，并通过 utils/plot_kmc_data.py 生成 coverage.png, coverage_steps.png,
  tof.png, tof_time.png 共 4 张图像。
  触发场景：parameter-builder 完成 KMC 参数构建并经用户确认后，由本技能执行 KMC 模拟。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_cn.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-kmc-simulator

## 1. 核心职责

1. 检查并管理 Wine 环境（KMC 引擎依赖）
2. 准备 KMC 输入文件（从 MOSP_database 复制模板 + 用户指定步数/温度/分压）
3. 执行 KMC 模拟并监控进度
4. 步数预警（≥ 2000 万步时提醒用户）
5. 生成 TOF、覆盖度图与 CSV 数据
6. 步数不足或失败时自动重新绘图

## 2. 前置条件

- ✅ MSR 任务已完成（如果需要从 MSR 团簇开始）
- ✅ parameter-builder 已完成 KMC 参数构建
- ✅ 用户已通过 5 选项确认（详见 parameter-builder §KMC 参数展示格式）
- ✅ Wine 环境已安装（首次运行时检查并提示安装）
- ✅ MSR 生成的 ini.xyz 已复制到 KMC 任务目录（如适用）
- ✅ 已安装外部 `mosp-for-chatMOSP`，且存在 `kmc_standalone.py`、`MOSP_database/`、`engine/main.exe`
- ❌ 禁止绕过 parameter-builder 手动构建 KMC 参数
- ❌ 禁止复用 MSR 的 input.json——KMC 必须独立准备完整参数

## 3. Wine 环境

KMC 引擎是 Windows 版 main.exe，需要 Wine 运行。

### 3.1 检查 Wine

```bash
which wine64 || which wine
```

### 3.2 安装 Wine（Ubuntu/Debian）

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine64 wine32
```

### 3.3 自动环境检查

- ✅ Wine 已安装 → 正常执行
- ⚠️ Wine 未安装 → 提示安装指导
- ❌ 版本不兼容 → 提示升级

## 4. 步数警告

KMC 步数 ≥ 2000 万时，执行前必须提醒用户：

```
⚠️ 计算时间提醒：
当前 KMC 步数为 {N} 步，预计计算时间约 {estimated_hours} 小时。
（参考：2000 万步约 12 小时，4000 万步约 24 小时）
是否继续执行 KMC 模拟？
```

| 步数 | 预计时间 |
|------|----------|
| 2,000 万（20M） | ~12 小时 |
| 4,000 万（40M） | ~24 小时或更长 |
| 更多 | 线性增长 |

注意：选择多个条件（如多温度对比）时，每个条件都要单独计算，总时间成倍增加。

## 5. 输入契约（input.json 必含字段）

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| Element | string | 金属元素（Pd、Pt、Au 等） |
| Lattice constant | string | 晶格常数（Å） |
| Crystal structure | string | 晶体结构（FCC、BCC、HCP） |
| Temperature | string | 温度（K） |
| Pressure | string | 压力（Pa） |
| flag_MSR | boolean | 必须 false |
| flag_KMC | boolean | 必须 true |
| KMC | object | KMC 参数对象 |

### KMC 对象内必含字段

| 字段 | 类型 | 说明 |
|------|------|------|
| nLoop | string | 模拟步数 |
| record_int | string | 记录间隔 |
| nspecies | number | 物种数量 |
| nproducts | number | 产物数量 |
| nevents | number | 反应事件数 |
| nevents_mob | number | 移动事件数 |
| s1 / s2 | string | 物种 1/2 定义（JSON 字符串） |
| p1 | string | 产物 1 定义（JSON 字符串） |
| e1 ~ e7 | string | 反应事件 1~7（JSON 字符串） |
| li | array | 晶格相互作用矩阵 |

> ⚠️ **关键**：气体熵 `s1.S_gas` / `s2.S_gas` 必须与 MSR 的 `Gas1_S` / `Gas2_S` 保持一致（用相同公式计算）。

## 6. 目录结构

KMC 任务目录必须在 MSR 目录下：

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── KMC_{步数}steps/             ← KMC 任务目录
    ├── input.json                ← 在 INPUT 外面
    ├── ini.xyz                   ← 从 MSR 复制
    ├── coverage.png              ← 运行后生成
    ├── coverage_steps.png        ← 运行后生成
    ├── tof.png                   ← 运行后生成
    ├── tof_time.png              ← 运行后生成
    ├── INPUT/                    ← 运行前应为空
    └── OUTPUT/                   ← 运行后填充
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

> ⚠️ **重要**：
> - `ini.xyz` 和 `input.json` 必须放在 `INPUT/` 外面（`kmc_standalone.py` 会清空 `INPUT/OUTPUT`）
> - 运行前确保 `INPUT/` 和 `OUTPUT/` 为空

## 7. 执行步骤

### 步骤 1：创建 KMC 任务目录

```bash
mkdir -p OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/KMC_{步数}steps/INPUT
mkdir -p OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/KMC_{步数}steps/OUTPUT
```

### 步骤 2：复制结构文件

```bash
cp OUTPUT/{msr_task_name}/ini.xyz OUTPUT/{msr_task_name}/KMC_{步数}steps/ini.xyz
```

### 步骤 3：准备 input.json

```bash
# 从 MOSP_database 复制模板（不要手动创建）
cp mosp-for-chatMOSP/MOSP_database/{metal}-{reaction}.json \
   OUTPUT/{msr_task_name}/KMC_{步数}steps/input.json

# 调整字段：
# - nLoop: 用户指定的步数
# - T: 用户指定的温度
# - gas_pp: 用户指定的气体分压
# - record_int: 记录间隔
# - s1.S_gas / s2.S_gas: 用 parameter-builder §7.1 公式重算
```

### 步骤 4：展示参数给用户确认

使用 parameter-builder §KMC 参数展示格式（5 选项）。

### 步骤 5：检查 Wine + 步数警告

- 检查 Wine 环境
- 步数 ≥ 2000 万时弹窗警告

### 步骤 6：执行 KMC

```bash
python3 {mosp_root}/kmc_standalone.py \
  --xyz OUTPUT/{任务目录}/ini.xyz \
  --json OUTPUT/{任务目录}/input.json \
  --out-dir {任务目录}
```

其中 `{mosp_root}` 通常是 `$HOME/.openclaw/workspace/mosp-for-chatMOSP`
或 `$OPENCLAW_WORKSPACE/mosp-for-chatMOSP`。运行前必须确认该目录存在。

注意：`--out-dir` 传任务目录名即可（如 `{msr_task_name}/KMC_{步数}steps`）。
脚本会自动放到 `OUTPUT/` 下；即使误带 `OUTPUT/` 前缀也会自动去重，不会产生
`OUTPUT/OUTPUT/` 重复结构。

## 8. 输出文件

| 文件 | 位置 | 说明 |
|------|------|------|
| coverage.png | KMC 任务目录 | 覆盖度 vs 时间 |
| coverage_steps.png | KMC 任务目录 | 覆盖度 vs 步数 |
| tof.png | KMC 任务目录 | TOF vs 时间 |
| tof_time.png | KMC 任务目录 | TOF vs 步数 |
| coverage.csv | OUTPUT/ | 覆盖率数据 |
| tof.csv | OUTPUT/ | TOF 数据 |
| site_tof.csv | OUTPUT/ | 位点 TOF 数据 |
| rec_cov.data | OUTPUT/ | 覆盖度记录（KMC 引擎原始输出） |
| rec_event.data | OUTPUT/ | 事件记录 |
| rec_site_spc.data | OUTPUT/ | 位点物种记录 |

### 8.1 发送图片给用户（飞书）

> ⚠️ **一次只发一张图**：飞书 message 工具每次 attach 只能带 1 张图片，
> 多发会静默丢失。KMC 完成后必须分 4 次发送，每次标注序号。

发送顺序和内容：

1. 图 1/4：Coverage vs Time（覆盖度 vs 时间） — `coverage.png`
2. 图 2/4：Coverage vs Steps（覆盖度 vs 步数） — `coverage_steps.png`
3. 图 3/4：TOF vs Time（TOF vs 时间） — `tof.png`
4. 图 4/4：TOF vs Steps（TOF vs 步数） — `tof_time.png`

每条消息示例：
```
message(action=send, message="图 1/4：Coverage vs Time",
         attachments=[{filePath:"...coverage.png", type:"image"}])
```

## 9. 输出检查与自动重绘

KMC 完成后（尤其是用户问"任务是否结束"时），必须检查并按需重绘图像：

```bash
KMC_TASK_DIR="KMC 任务目录"
KMC_OUTPUT="$KMC_TASK_DIR/OUTPUT"

# 1. 检查数据文件
if [ ! -f "$KMC_OUTPUT/rec_cov.data" ] || \
   [ ! -f "$KMC_OUTPUT/rec_event.data" ] || \
   [ ! -f "$KMC_OUTPUT/rec_site_spc.data" ]; then
  echo "❌ 数据文件不存在，KMC 模拟可能未完成"
  exit 1
fi

# 2. 检查步数一致性
EXPECTED=$(grep -E "^[0-9]+\s+! Num of steps" "$KMC_TASK_DIR/INPUT/input.txt" | awk '{print $1}')
ACTUAL=$(tail -n 1 "$KMC_OUTPUT/rec_event.data" | awk '{print $2}')

if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "❌ 预期步数 $EXPECTED，实际 $ACTUAL，KMC 未成功完成"
  exit 1
fi

# 3. 检查图像（4 张），缺失则重绘
if [ -f "$KMC_TASK_DIR/coverage.png" ] && \
   [ -f "$KMC_TASK_DIR/coverage_steps.png" ] && \
   [ -f "$KMC_TASK_DIR/tof.png" ] && \
   [ -f "$KMC_TASK_DIR/tof_time.png" ]; then
  echo "✅ 图像已存在"
else
  python3 ../../utils/plot_kmc_data.py "$KMC_OUTPUT"
  echo "✅ 图像已重绘"
fi
```

绘图脚本位置：`mosp-for-chatMOSP/utils/plot_kmc_data.py`

## 10. 错误处理

| 错误 | 处理 |
|------|------|
| 步数不匹配 | 提示用户检查 KMC 日志，可能未跑完 |
| 数据文件缺失 | KMC 未成功完成，检查 run.log |
| Lattice constant 缺失 | 从 MOSP_database 复制完整模板，不要手动创建 |
| INPUT/OUTPUT 目录缺失 | 创建 KMC 任务目录时一起创建 |
| ini.xyz 缺失 | 从 MSR 任务目录复制 |
| Wine 缺失 | 提示安装指导 |
| KMC 段错误 | Wine 版本不兼容，提示升级 |

## 11. 跨技能衔接

- **MSR → KMC**：MSR 完成后产出 ini.xyz。本技能独立从 MOSP_database 取完整 KMC 参数，不复用 MSR 的 input.json。
- **参数修改时**：用户改温度 → parameter-builder 必须按 §7.5 重算气体熵。
- **长任务查询**：用户问"任务是否结束" → 执行 §9 检查脚本，必要时重绘图像。

## 12. 依赖

- **mosp-for-chatMOSP** — KMC 引擎（已克隆，含 main.exe）
- **chatmosp-parameter-builder** — 参数构建与气体熵计算
- **chatmosp-file-organizer** — 目录创建
- **chatmosp-input-coordinator** — 任务入口
- **Wine** — 运行 Windows 版 main.exe（必需）

## 13. 文件结构

```
chatmosp-kmc-simulator/
├── SKILL.md       # 本文件（中文）
└── SKILL_cn.md    # 英文版
```

## 14. 示例

```
用户: 对 Pt 纳米颗粒进行 CO 氧化 KMC 模拟，850K，150Pa，2000 万步

系统: [识别为 KMC → parameter-builder 查参数 → 展示 5 选项 →
      用户确认 → 检查 Wine 已装 → ⚠️ 2000 万步约 12 小时，警告 →
      用户再次确认 → 准备 input.json → 调 kmc_standalone.py →
      监控进度 → 检查输出 → 生成 4 张图像 → 逐张发送展示结果]
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
