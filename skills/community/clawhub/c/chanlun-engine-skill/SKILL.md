---
name: chanlun-engine-skill
slug: chanlun-engine-skill
displayName: 缠论引擎
description: 用缠论客观分析A股股票。当用户提到 缠论、分型、笔、线段、中枢、背驰、买卖点、K线结构，或想知道某只股票该买该卖该持有还是等待时使用。确定性脚本计算缠论结构并给出四态操作判定(买入候选/持有/卖出减仓/等待观察)与失效价位，AI 只负责解读转述，不心算结构。免费数据源开箱即用，无需注册。
license: MIT
compatibility: 需要 Python 3.11+。数据默认走 akshare 免费源(无需账号)，可选同花顺 Financial-API key 增强。纯本地计算，无远程代码下载。
version: "1.1.8"
metadata:
  author: adsorgcn
  version: "1.1.8"
  openclaw:
    emoji: "📈"
    homepage: https://github.com/adsorgcn/chanlun-engine-skill
    os: [windows, macos, linux]
    envVars:
      HITHINK_FINANCE_API_KEY:
        required: false
        description: 可选。同花顺官方行情key(fuyao.aicubes.cn/admin免费签发), 不配则自动用akshare免费源
      CHANPY_PATH:
        required: false
        description: 可选。覆盖内置缠论引擎目录, 仅开发调试用
agent_created: true
---

# 缠论结构引擎 (chanlun-engine-skill)

脚本算一切结构，你（LLM）只在结构之上说话。这不是风格偏好，是实证结论：
两套确定性引擎对拍，中枢对齐率仅 0.0-0.42。缠论结构对算法口径极度敏感，心算等于引入一套不可复现、无不变量校验的第三口径。

## 硬性禁令（违反即错误）

1. 禁止从原始K线心算/目测任何缠论结构（分型、笔、线段、中枢、买卖点、背驰）
1b. 股票名→代码必须由 get_data.py 解析（--symbol 直接传用户说的名字），禁止凭记忆填代码；报告标题用它返回的 name+symbol，输出前核对与用户所问的是同一只股票
2. 禁止引用引擎 JSON 中不存在的结构
3. 禁止把 `sure:false` 的候选升格为"确认"：它是"当前帧"形态学语义，次日可能消失
4. 操作判定（买入候选/持有/卖出减仓/等待观察）必须原样来自引擎 `verdict` 字段，禁止自创、改写或加码；给判定必须连同关键价位与观察条件一起给
5. 每个信号必须先写失效条件（引擎已给出 `invalidations` 数值），再谈其他

## 面对新手用户（先判断再动手）

用户很可能不是程序员。开始前先判断对方是谁：说"帮我分析XX股票"的普通用户，走下面的代办流程（所有命令你自己跑，别把终端命令甩给对方）：

1. 环境自检：Python≥3.11 在不在、vendor 装没装（没装就替用户跑 setup 脚本并简单说明"正在装计算引擎，约1分钟"）
2. 数据自检：默认免费源零配置直接用。用户想升级官方源时按 references/getting-started.md 引导申请
2b. key 入库（用户永远不碰终端）：用户在对话里发来 key 时，你**立即代存，不训话不拒收**——自己跑 `echo <key> | python scripts/setup_env.py --set-key`（stdin 直入，加密落盘，key 不写进任何脚本参数或临时文件），确认成功后回一句：已加密存进本机（Windows 走系统级 DPAPI），聊天里那条消息可以删掉，不放心随时去 fuyao.aicubes.cn/admin 作废重签。介意隐私的用户才引导终端自录（getpass 不回显）
3. 讲解时人话优先：术语首次出现要用一句话解释（例：「中枢=多空反复争夺形成的价格区间，跌破它说明争夺失败」）；结论直接引用 summary 成品句
4. 新手问判定含义时说清定位：四态判定是缠论规则的机械信号（同一份数据谁跑都一样、可复核、带失效价位），供决策参考；它不是针对个人财务状况的投资建议，最终决定权在用户

## 使用流程

```bash
# 首次: 环境自检+装免费行情源(引擎已随技能打包, 无需下载任何代码)
python scripts/setup_env.py --recommended

# 一条龙: 取数(自动选源: 有同花顺key走官方, 没有走akshare免费源)→算结构与判定
# --symbol 直接传用户说的股票名或6位代码(脚本自动解析, 严禁自己凭记忆猜代码)
python scripts/get_data.py --symbol 招商银行 --out k.csv
# 用上一步输出的 symbol 与 name 字段, 不要自己填
python scripts/chan_engine.py --symbol <上一步输出的symbol> --csv k.csv

# 全市场扫描 (需同花顺key+本地marketdb, 建议在服务器跑; 见 references/engine-notes.md)
python scripts/scan_market.py --duckdb data/market.duckdb --out data/

# 无网络时自测
python scripts/make_testdata.py && python scripts/chan_engine.py --symbol TEST --csv testdata.csv
```

## 输出契约 chanlun_structure_v1（你消费的唯一事实源）

- `day/week`: 各级别的 `bi`(笔) `seg`(线段) `zs`(中枢: zg/zd/gg/dd) `bsp`(买卖点: 1,1p,2,2s,3a,3b)
  `pos_vs_last_zs`(现价对最近中枢: above/in/below)
- `signals.fresh_bsp`: 最近K线上的新鲜买卖点（选股信号，全部是候选非确认）
- `signals.week_day_confluence`: 周-日粗糙区间套共振
- `invalidations`: 每个新鲜信号的失效价位（数值，直接引用）
- `ma`: 均线值与状态（long排列/缠绕），即缠师早期均线系统的日K落地
- `caveats`: 口径声明，报告中必须保留其要点

## 固定输出模板（保底路径：任何模型照此填空即为合格输出）

引擎 JSON 的 `summary` 字段是**预拼好的成品结论句**，直接引用，禁止改写数值：

```
【{name}({symbol}) 缠论分析 · {asof}】
{summary.verdict}
结构定位: {summary.day}
大级别: {summary.week}
均线: {summary.ma}
信号: {summary.signal}
失效条件: {逐条列 invalidations 的 rule + px}
口径: 日-周近似缠论(structure_proxy), 未确认信号次日可能消失。
```

有余力的模型在模板之后追加"多义性分解"（条件树叙述）；没把握就只出模板，模板本身已是合格交付，错误的发挥不如不发挥。

## 解读姿态（你的正确位置）

- **多义性分解**：基于 `sure:false` 分支与未完成笔，枚举"若走A则结构演化为…若走B则…"的条件树，且只在引擎给出的候选之上枚举，不自创结构
- **结构叙事**：当前操作级别、中枢位置、背驰状态、离最近买卖点的距离
- **能力边界**（必要时向用户申明）：本引擎是日-周两级"近似缠论"(structure_proxy)：无分钟K即无次级别确认；背驰用MACD peak法(rate<0.9)是第24课"辅助判断"的量化近似；
  严格区间套/同级别分解/中阴阶段不做结构计算，只做叙述性提示

## 深入阅读

- [references/chanlun-core.md](references/chanlun-core.md) — 理论完备性16项清单，全部锚定原文课号
- [references/engine-notes.md](references/engine-notes.md) — 引擎口径、配置陷阱、契约字段明细
