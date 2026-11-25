---
name: garmin-health-analysis-cn
description: 用自然语言与你的佳明（Garmin）数据对话，专为跑者设计 —— "帮我分析一下上周的比赛数据"、"帮我分析一下最近的身体状况"、"我昨晚睡得怎么样？"。可获取 20 余项健康指标（睡眠阶段、身体电量、心率变异性、最大摄氧量、训练准备度、身体成分、血氧），下载 FIT/GPX 文件进行跑步路线与配速分析，查询任意位置的海拔与配速，并生成可交互的健康仪表盘。从简单的"给我看这周的跑步记录"到深入的"分析我的训练负荷与恢复状况"均可胜任。当用户请求分析跑步或比赛数据时，会自动获取比赛日期前后各 3 天内的全部可获取数据（涵盖跑步记录、健康指标、HRV、身体电量以及其他所有可用数据，确保完整无遗漏），综合分析后生成 HTML 可视化图表，清晰呈现关键指标与趋势。
version: 1.1.1
author: Earthaveeman
metadata: {"clawdbot":{"emoji":"⌚","requires":{"env":["GARMIN_EMAIL","GARMIN_PASSWORD"]},"install":[{"id":"garminconnect","kind":"python","package":"garminconnect","label":"Install garminconnect (pip)"},{"id":"fitparse","kind":"python","package":"fitparse","label":"Install fitparse (pip)"},{"id":"gpxpy","kind":"python","package":"gpxpy","label":"Install gpxpy (pip)"}]}}
---

# 佳明健康数据分析

从佳明 Connect 查询健康指标，并生成可交互的 HTML 图表。本技能主要用于 AI 助手技能（Skill）环境，实现自动化健康监测与主动提醒。

---

## 技能安装步骤（仅需首次执行）

### 1. 安装依赖

```bash
pip3 install garminconnect
```

### 2. 配置账号

提供佳明 Connect 账号信息的方式有三种：

#### 方式 A：AI 助手的技能配置（可选，视平台支持）

如果你使用的 AI 助手支持在技能配置中设置环境变量，可以直接添加。以 OpenClaw 为例，将账号信息添加到 `~/.clawdbot/clawdbot.json`：

```json
{
  "skills": {
    "entries": {
      "garmin-health-analysis-cn": {
        "enabled": true,
        "env": {
          "GARMIN_EMAIL": "your-email@example.com",
          "GARMIN_PASSWORD": "your-password"
        }
      }
    }
  }
}
```

**提示**：以 OpenClaw 为例，也可以通过其界面中的"技能设置"面板进行配置。

#### 方式 B：本地配置文件

在技能目录下创建配置文件：

将本技能安装到你的 AI 助手的技能目录下（目录位置因平台而异，例如 OpenClaw 为 `~/.clawdbot/skills/`，Claude Code 为 `~/.claude/skills/` 等），然后进入技能目录：

```bash
cd <技能目录>/garmin-health-analysis-cn
cp config.example.json config.json
# 编辑 config.json，填入你的邮箱和密码
```

**config.json：**
```json
{
  "email": "your-email@example.com",
  "password": "your-password",
  "is_cn": true
}
```

**说明**：
- `config.json` 已被 git 忽略，不会上传，以保护你的账号安全。
- **中国大陆佳明账户**请将 `is_cn` 设为 `true`，登录时会连接佳明中国服务器（connect.garmin.cn）。
- **国际版账户**请将 `is_cn` 设为 `false`（或删除该字段），登录时会连接国际服务器（connect.garmin.com）。

#### 方式 C：命令行参数

在登录时直接传入账号信息：

```bash
python3 scripts/garmin_auth.py login \
  --email YOUR_EMAIL@example.com \
  --password YOUR_PASSWORD \
  --cn
```

### 3. 登录认证

登录佳明 Connect 并保存会话令牌：

```bash
python3 scripts/garmin_auth.py login
```

账号信息的读取优先级如下：
1. 命令行参数（`--email`、`--password`、`--cn`）
2. 本地配置文件（`config.json`）
3. 环境变量（`GARMIN_EMAIL`、`GARMIN_PASSWORD`）
4. AI 助手的技能配置（若平台支持，如 OpenClaw 的 `skills.entries.garmin-health-analysis-cn.env`）

会话令牌保存在 `~/.garmin-health-analysis-cn/tokens/`（可通过环境变量 `GARMIN_TOKEN_DIR` 自定义位置），并会自动刷新。

**服务器区域（`is_cn`）的一致性保证**：

- 登录成功后，实际使用的区域会随令牌一并持久化到令牌目录下的 `meta.json`（含 `is_cn` 与登录时间）。
- 之后所有脚本复用令牌时，均以 `meta.json` 记录的区域连接对应服务器（即**令牌由哪个域签发，就连接哪个域**），优先级为：`meta.json` > 环境变量 `GARMIN_IS_CN`（`true`/`1` 等）> `config.json` 的 `is_cn`（旧版令牌无 `meta.json` 时的回退）。
- 因此用 `--cn` 登录的中国大陆账户即使没有 `config.json`，复用令牌时也会正确连接 connect.garmin.cn，不会再出现"令牌签发域与复用域错配导致的鉴权失败"。
- 若令牌失效且 `config.json` 中保存了账号密码，脚本会**自动尝试重新登录一次**并刷新令牌，无需手动干预。

查看登录状态：

```bash
python3 scripts/garmin_auth.py status
```

## 获取数据

使用 `scripts/garmin_data.py` 获取 JSON 格式的数据：

```bash
# 睡眠数据（默认最近 7 天）
python3 scripts/garmin_data.py sleep --days 14

# 身体电量（佳明的恢复程度指标）
python3 scripts/garmin_data.py body_battery --days 30

# 心率变异性数据
python3 scripts/garmin_data.py hrv --days 30

# 心率（静息、最高、最低）
python3 scripts/garmin_data.py heart_rate --days 7

# 活动/运动记录
python3 scripts/garmin_data.py activities --days 30

# 压力水平
python3 scripts/garmin_data.py stress --days 7

# 综合摘要（含各项平均值）
python3 scripts/garmin_data.py summary --days 7

# 自定义日期范围
python3 scripts/garmin_data.py sleep --start 2026-01-01 --end 2026-01-15

# 用户资料
python3 scripts/garmin_data.py profile
```

输出为标准输出中的 JSON，可解析后用于回答用户的问题。

## 生成图表

使用 `scripts/garmin_chart.py` 生成可交互的 HTML 可视化图表：

```bash
# 睡眠分析（时长 + 评分）
python3 scripts/garmin_chart.py sleep --days 30

# 身体电量恢复曲线（按数值着色）
python3 scripts/garmin_chart.py body_battery --days 30

# 心率变异性与静息心率趋势
python3 scripts/garmin_chart.py hrv --days 90

# 活动汇总（按类型、卡路里）
python3 scripts/garmin_chart.py activities --days 30

# 完整仪表盘（全部 4 类图表）
python3 scripts/garmin_chart.py dashboard --days 30

# 保存到指定文件
python3 scripts/garmin_chart.py dashboard --days 90 --output ~/Desktop/garmin-health.html
```

图表会自动在默认浏览器中打开。

### 统一报告样式（report_style.py）

所有 HTML 报告（含 AI 自行生成的分析页面）**必须统一采用本技能的标准样式**，标准样式定义在 `scripts/report_style.py`，与 `example/` 目录下的比赛分析报告完全一致：

- **纯内联 SVG 图表**：不使用 Chart.js 或任何 CDN/外部依赖，可离线直接打开；`viewBox` 自适应宽度
- **设计系统**：蓝色渐变（#0d47a1 → #1a73e8 → #2196f3）大圆角 hero 横幅（装饰圆 + tag 徽章 + 大标题 + 黄色 PR 徽章）、蓝色圆角数字块的编号章节标题（h2）+ 灰色说明文字、白色圆角卡片（card）、统计卡片网格（stat，g4/g3/g2 栅格：12.5px 灰标签 / 23px 蓝色大数值 / 灰色小注）
- **组件**：note 提示条（蓝 info / 黄 warn / 绿 good，左侧粗边框）、kv 键值行（虚线分隔）、sleepbar 睡眠阶段堆叠条（深睡 #304ffe / 浅睡 #7ea8ff / REM #ff9e40 / 清醒 #bdbdbd）、sticky 表头表格（hover 行高亮、圆角滚动容器）、灰色免责声明页脚
- **通用图表函数**：`svg_line_chart()`（支持参考区间带、图例、y 轴格式化、tooltip）、`svg_bar_chart()`（支持参考线、柱顶数值、按值着色）、`hero()`、`render_page()`（自动编号章节 + 页脚组装）

在自写生成脚本时，将 `scripts/` 加入 `sys.path` 后导入使用：

```python
from report_style import (C, esc, hms, ms, svg_line_chart, svg_bar_chart,
                          sleep_bar, stat, kv, note, card, grid, chart_cap,
                          hero, render_page)
```

所有页面为中文界面，页脚必须保留免责声明：**"本报告所有数据来自 Garmin Connect 自动记录，分析结果仅供参考，不构成医疗或专业训练建议。"**

## 跑步/比赛数据分析流程

> **触发条件**：当用户请求"分析跑步/比赛数据"时（如"帮我分析一下上周的比赛数据""分析我周日那场半马""看看这次跑步表现怎么样"等任何跑步或比赛分析请求），**必须完整执行以下流程，不得只取单项数据即作答**。

### 第 1 步：确定比赛日期

- 从用户表述中确定比赛/跑步日期 `D`（格式 `YYYY-MM-DD`）。
- 若用户未明确日期（如"上周的比赛"），先用 `python3 scripts/garmin_data.py activities --days 14` 查找候选活动，与用户确认是哪一场；**日期不明确时不得跳过确认直接分析**。

### 第 2 步：计算数据采集范围

- 采集范围为**比赛日期前后各 3 天**：
  - `START = D − 3 天`
  - `END = D + 3 天`
  - 共 7 天（如周日比赛 → 周四至下周三），覆盖赛前准备期与赛后恢复期。
- 日期可用任意方式推算（如 PowerShell：`(Get-Date $D).AddDays(-7).ToString('yyyy-MM-dd')`），或直接手算。

### 第 3 步：获取全部可获取数据（完整无遗漏）

按以下三组脚本依次采集，**所有指标均须获取，不得省略**；某日某项数据缺失可跳过该条，但不得整体跳过某一类。

**A. 基础健康指标**（`garmin_data.py`，支持 `--start/--end` 一次性取整段范围）：

```bash
# 以下 START/END 为第 2 步计算所得
python3 scripts/garmin_data.py activities   --start $START --end $END   # 跑步/活动记录
python3 scripts/garmin_data.py sleep        --start $START --end $END   # 睡眠（时长/阶段/评分）
python3 scripts/garmin_data.py hrv          --start $START --end $END   # 心率变异性（HRV）
python3 scripts/garmin_data.py body_battery --start $START --end $END   # 身体电量
python3 scripts/garmin_data.py heart_rate   --start $START --end $END   # 心率（静息/最高/最低）
python3 scripts/garmin_data.py stress       --start $START --end $END   # 压力水平
python3 scripts/garmin_data.py summary      --start $START --end $END   # 综合摘要（含各项均值）
```

**B. 扩展指标**（`garmin_data_extended.py`，多数按单天 `--date` 查询，需对 `START` 到 `END` 的每一天 `d` 逐日循环调用）：

| 指标 | 命令 | 说明 |
|------|------|------|
| 训练准备度 | `garmin_data_extended.py training_readiness --date $d` | 赛前/赛后准备度 |
| 训练状态 | `garmin_data_extended.py training_status --date $d` | 含训练负荷状态 |
| 最大指标 | `garmin_data_extended.py max_metrics --date $d` | VO2 Max 等 |
| 身体成分 | `garmin_data_extended.py body_composition --date $d` | 体重、体脂、肌肉量 |
| 体重记录 | `garmin_data_extended.py weigh_ins --start $START --end $END` | 体重趋势（支持范围） |
| 血氧 | `garmin_data_extended.py spo2 --date $d` | SPO2 |
| 呼吸 | `garmin_data_extended.py respiration --date $d` | 全天呼吸率 |
| 详细步数 | `garmin_data_extended.py steps --date $d` | 步数明细 |
| 楼层 | `garmin_data_extended.py floors --date $d` | 爬楼层数 |
| 强度分钟 | `garmin_data_extended.py intensity_minutes --date $d` | 中高强度活动时长 |
| 水分摄入 | `garmin_data_extended.py hydration --date $d` | 饮水量 |
| 全天压力详情 | `garmin_data_extended.py stress_detailed --date $d` | 压力时间序列 |
| 日内心率序列 | `garmin_data_extended.py hr_intraday --date $d` | 全天心率曲线 |
| 健身年龄 | `garmin_data_extended.py fitness_age` | 体能年龄（无需逐日） |
| 耐力得分 | `garmin_data_extended.py endurance_score` | 耐力评分（无需逐日） |
| 爬坡得分 | `garmin_data_extended.py hill_score` | 爬坡能力（无需逐日） |

**C. 比赛活动文件**（`garmin_activity_files.py`，针对比赛当日那条跑步活动）：

1. 从第 A 步 `activities` 结果中找到比赛当日目标活动的 `activity_id`。
2. 下载并解析原始文件，获取逐点 GPS、海拔、配速、心率、步频、功率等：

```bash
python3 scripts/garmin_activity_files.py download --activity-id <ID> --format fit
# 默认保存到系统临时目录（下载结果 JSON 的 "file" 字段为实际路径），之后：
python3 scripts/garmin_activity_files.py analyze  --file <下载结果中的文件路径>
python3 scripts/garmin_activity_files.py parse    --file <下载结果中的文件路径>
# 如需查询特定距离/时间点的数据：
python3 scripts/garmin_activity_files.py query --file <下载结果中的文件路径> --distance 5000
```

### 第 4 步：综合分析

结合 `references/health_analysis.md` 的解读框架，对采集到的全部数据进行综合分析，至少覆盖：

- **比赛当日表现**：配速、心率区间、海拔变化、步频、功率（如有）、分段（lap）表现。
- **赛前趋势**：身体电量、HRV、静息心率、睡眠、训练准备度——评估进入比赛时的恢复/准备状态。
- **赛后恢复**：身体电量、HRV、压力、睡眠、静息心率——评估赛后恢复进度与是否出现过度训练信号。
- **关键转折点**：标注比赛日相对于前后各周的指标突变（如 HRV 骤降、身体电量低谷、静息心率回升）。
- 结尾务必声明：分析结果仅供参考，不构成医疗建议。

### 第 5 步：生成 HTML 可视化图表

生成基于 HTML 的可视化图表，清晰呈现关键指标与趋势，便于用户直观理解：

- **方式一（比赛在近期时）**：若比赛日期落在最近 N 天内（`N ≥ 今天 − START`），可直接使用：
  ```bash
  python3 scripts/garmin_chart.py dashboard --days <N> --output ~/Desktop/race-analysis.html
  ```
- **方式二（通用，比赛为历史日期时）**：由于 `garmin_chart.py` 仅支持 `--days`（最近 N 天），无法精确指定历史日期范围。此时应基于第 3 步已采集的 JSON 数据，**导入 `scripts/report_style.py` 组件自行生成 HTML**（禁止使用 Chart.js 等外部依赖），重点呈现：
  - 赛前→比赛→赛后 7 天的**身体电量、HRV、静息心率、睡眠评分、压力**趋势折线图；
  - 比赛当日活动的**配速曲线、心率曲线、海拔剖面**；
  - 关键指标统计卡片（赛前 3 天均值 vs 赛后 3 天均值 vs 比赛日值）；
  - 在图表中**高亮标注比赛日**，便于直观对比前后变化。
- 生成的 HTML 文件应在默认浏览器中打开，并向用户说明文件保存路径。

## 回答问题

| 用户提问 | 执行操作 |
|----------|----------|
| "帮我分析一下上周的比赛数据" / "分析我的半马比赛" 等任何跑步或比赛分析请求 | **必须完整执行上方「跑步/比赛数据分析流程」**：获取比赛日期前后各 3 天（共 7 天）的全部可获取数据 → 综合分析 → 生成 HTML 可视化图表 |
| "帮我分析一下最近的身体状况" | `garmin_data.py summary --days 7`，报告身体电量、睡眠与恢复趋势 |
| "我昨晚睡得怎么样？" | `garmin_data.py summary --days 1`，报告睡眠时长和评分 |
| "最近一个月我的配速有什么变化？" | `garmin_data.py activities --days 30`，分析各项跑步的配速趋势 |
| "我的心率变异性在改善吗？" | `garmin_data.py hrv --days 30`，分析变化趋势 |
| "我的静息心率怎么样？" | `garmin_data.py heart_rate --days 7`，报告平均值和趋势 |

## 核心指标解读

### 身体电量（0-100）
佳明基于心率变异性、压力、睡眠和活动强度计算的综合恢复指标：
- **高（75-100）**：已充分充电，可进行高强度训练
- **中（50-74）**：精力中等，适合常规活动
- **低（25-49）**：精力有限，需要恢复
- **很低（0-24）**：精力耗尽，应以休息为主

### 睡眠评分（0-100）
基于睡眠时长、睡眠阶段和睡眠中断情况的综合睡眠质量评分：
- **优秀（90-100）**：恢复效果最佳的睡眠
- **良好（80-89）**：质量较好，仅有个别小问题
- **一般（60-79）**：尚可，但有改进空间
- **较差（0-59）**：存在明显的睡眠不足

### 心率变异性（HRV）
以毫秒为单位，通常数值越高越好：
- 反映自主神经系统的平衡状态与恢复能力
- 应关注**长期趋势**（数值上升 = 恢复能力改善）
- 受睡眠、压力、训练负荷、疾病等因素影响
- 正常范围因人而异（20-200+ 毫秒）

### 静息心率（次/分）
越低通常代表心血管功能越好（与 `references/health_analysis.md` 保持一致）：
- **运动员**：40-55 次/分
- **经常锻炼的成年人**：55-65 次/分
- **普通成年人**：60-80 次/分
- **缺乏运动者**：70-90 次/分
- 突然升高可能提示压力增大、生病或训练过度

### 压力水平
基于全天心率变异性分析得出：
- **低压力**：休息与恢复时段
- **中等压力**：日常活动状态
- **高压力**：体力活动或精神压力较大

## 健康分析

当用户希望获得健康洞察、理解数据趋势时，请使用 `references/health_analysis.md`，其中包含：
- 有科学依据的各项指标解读方法
- 按年龄和体能水平划分的正常范围
- 模式识别（周趋势、恢复周期、训练负荷平衡）
- 基于数据的可执行建议
- 提示应当休息或就医的预警信号

### 分析流程
1. 获取数据：`python3 scripts/garmin_data.py summary --days N`
2. 阅读 `references/health_analysis.md` 中的解读框架
3. 按分析框架执行：现状 → 趋势 → 模式 → 洞察 → 建议
4. 务必声明：分析结果仅供参考，不构成医疗建议

## 常见问题排查

### 登录认证问题
- **"账号或密码错误"**：核对邮箱和密码，尝试登录佳明 Connect 网页版验证；同时确认 `is_cn` 设置与账号注册区域一致（区域不匹配也会导致登录失败）
- **"令牌已过期" / 反复提示未认证**：脚本会优先按登录时记录的区域（`tokens/meta.json`）复用令牌，并在失效时用 `config.json` 凭据自动重登一次；若仍失败，删除 `~/.garmin-health-analysis-cn/tokens/` 目录后重新运行 `python3 scripts/garmin_auth.py login`（注意带上与账号区域一致的 `--cn` 或在 `config.json` 中正确设置 `is_cn`）
- **旧版令牌区域错配**（曾用 `--cn` 登录但脚本连了国际服务器导致令牌失效）：重新登录一次即可，新版会把区域写入 `meta.json`，之后自动保持一致
- **"请求过于频繁"**：佳明限制了请求频率，请等待几分钟后再试

### 数据缺失
- 部分指标需要特定佳明设备支持（身体电量需要支持心率变异性的设备）
- 未佩戴设备的时间段可能出现数据缺口
- 新账号的历史数据可能较少

### 依赖库问题
- 若 `garminconnect` 导入失败：执行 `pip3 install --upgrade garminconnect`
- 佳明偶尔会调整接口，请求失败时请更新依赖库

## 隐私说明

- 账号令牌仅保存在本地 `~/.garmin-health-analysis-cn/tokens/`（可通过环境变量 `GARMIN_TOKEN_DIR` 自定义），目录下仅含令牌文件与记录登录区域的 `meta.json`（不含密码）
- 会话令牌自动刷新
- 除佳明官方服务器外，不会向任何其他地方发送数据
- 删除令牌目录（含 `meta.json`）即可随时撤销授权

## 对比：佳明 与 Whoop

| 功能 | 佳明 | Whoop |
|------|------|-------|
| **恢复指标** | 身体电量（0-100） | 恢复评分（0-100%） |
| **心率变异性追踪** | 支持（夜间平均值） | 支持（更详细） |
| **睡眠阶段** | 浅睡、深睡、快速眼动、清醒 | 浅睡、慢波睡眠、快速眼动、清醒 |
| **运动记录** | 内置 GPS，多种运动模式 | 训练负荷评分（0-21） |
| **压力** | 全天压力水平 | 不直接监测 |
| **接口** | garminconnect 库 | 官方 OAuth |
| **设备类型** | 手表、运动手环 | 仅腕带式设备 |

## 参考文档

- `references/api.md` —— 佳明 Connect 接口详细说明
- `references/health_analysis.md` —— 有科学依据的健康数据解读方法
- [佳明 Connect](https://connect.garmin.com) —— 官方网页版（中国大陆账户请使用 [connect.garmin.cn](https://connect.garmin.cn)）

## 版本信息

- **创建日期**：2026-11-11
- **作者**：Earthaveeman
- **版本**：1.1.1（2026-11-24 更新，修复令牌生成与复用的服务器区域不一致问题：登录区域持久化到 `tokens/meta.json`，新增 `GARMIN_IS_CN` 环境变量与令牌失效自动重登）
- **历史版本**：1.1.0（2026-11-24，新增 `scripts/report_style.py` 统一报告样式模块：纯内联 SVG、无外部依赖，garmin_chart.py 全面改版为比赛分析报告同款样式，SKILL.md 明确所有 HTML 输出的样式规范）；1.0.2（2026-11-16，新增「跑步/比赛数据分析流程」）；1.0.1（2026-11-12，平台通用化与双区域支持说明）；1.0.0（2026-11-11 首次发布，中国大陆适配版）
- **依赖**：garminconnect、fitparse、gpxpy（Python 库）
- **许可证**：MIT
