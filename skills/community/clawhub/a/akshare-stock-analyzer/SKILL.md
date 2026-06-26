---
name: akshare-stock-analyzer
description: >
  使用本 skill 自带的 fetch.py 和 analyze.py，对 A 股个股做短期趋势分析。
  Use this skill whenever the user asks to analyze A-share stocks, ETFs (like A500/159339),
  check short-term trend (bullish/bearish/sideways), weekly and today change, signals (buy/sell/hold),
  or score stocks based on recent performance.
---

# Akshare Stock Analyzer Skill

Skill 名称（推荐对外叫法）：
- 中文：Akshare A 股盘中 + 趋势分析助手
- 英文：Akshare-Stock-Analyzer

一个可单独开源、独立使用的“股票短期分析”技能，目录内自带完整脚本：
- 拉取行情 + 计算指标（scripts/fetch.py）
- 应用自定义周+当天规则生成趋势/信号/评分（scripts/analyze.py）
- 数据源封装（scripts/tx_provider.py 和 scripts/sina_provider.py）
- 获取单只股票当日最新行情快照（scripts/today.py）

## 何时使用（When to use）

在这些场景下，应该触发/使用本 skill：
- 用户说：分析某只 A 股/ETF 的近期走势、空头/多头趋势、风险情况
- 用户希望基于最近一周和当天的表现，判断：
  - `trend`（多头/空头/震荡）
  - `weekly_change_pct` / `today_change_pct`
  - `signal`（buy/sell/hold）
  - `score`（0~10 短期强弱评分）
- 用户提到：
  - “帮我看这只股票最近怎么样”
  - “这票现在是多头还是空头”
  - “最近一周跌这么多要不要走人”
  - “用之前那套策略分析一下 A500、招商银行、方大炭素”等

不适用的场景：
- 纯宏观新闻解读、公司基本面深度研究、不需要技术指标的长线判断
- 与 A 股无关的资产（例如美股、期货、加密货币），除非你另外扩展脚本

## 依赖脚本与环境（Existing workflow & environment）

本 skill 目录自带以下 Python 脚本（均在 scripts/ 子目录下）：

- scripts/fetch.py
  - 提供 `fetch_with_indicators(symbol_or_name, start_date, end_date, adjust, prefer)`
  - 负责：
    - 通过新浪优先、腾讯兜底的方式拉取日线行情
    - 统一输出中文列：日期、开盘、收盘、最高、最低、成交量
    - 计算：MA7 / MA14 / MA20 / MA60、MACD(12,26,9) 的 DIF/DEA/MACD、RSI14

- scripts/analyze.py
  - 提供：
    - `analyze_single(ts_code: str, df: pd.DataFrame) -> AnalysisResult`
    - `AnalysisResult` 字段已在文件顶部详细注释，包括：
      - `trend` / `weekly_change_pct` / `today_change_pct`
      - `macd_*` / `rsi_*`
      - `signal` / `score`
      - 均线结构与扩展字段：`ma_pattern` / `ma_bias` / `ma_values` / `ma_spread`
      - 趋势强度与风险相关：`trend_strength` / `reversal_hint` / `risk_level`
    - 更完整的字段说明见：`scripts/analyze_result.md`，可作为下游解读/LLM 的 schema 参考。
  - 也提供命令行用法示例（可选）：
    - `python scripts/strategy_analyzer.py 招商银行 --days 120`

- scripts/tx_provider.py / scripts/sina_provider.py

- scripts/today.py
  - 提供 `get_today_quote(symbol_or_name)`：
    - 使用 `ak.stock_zh_a_spot` 获取全市场实时行情，然后按代码或名称筛选单只股票；
    - 返回字段包含：最新价、涨跌幅、成交量、最高、最低；
  - 也支持 CLI：`python scripts/today.py <symbol>`，直接在终端输出今日行情快照（盘中）。

运行本 skill 需要外部环境已安装：
- Python 3.9+
- 第三方库：`akshare`、`pandas`

## 输入（Inputs）

从用户对话中，尽量提取这些信息：

- 必填：
  - 股票代码或名称，例如：
    - "招商银行"、"600036"、"方大炭素"、"159339"、"A500" 等
- 可选：
  - 时间范围：
    - 显式开始/结束日期：YYYYMMDD 或 YYYY-MM-DD
    - 或者“最近 N 天”：例如最近 60/120 个交易日
  - 复权方式：不复权 / 前复权 / 后复权（"", "qfq", "hfq"）
  - 数据源优先级：新浪("sina") 或 腾讯("tx")

缺省策略：
- 若用户未指定时间范围，默认用最近 120 个自然日对应的交易日数据。
- 若用户未指定数据源，默认优先新浪。
- 若用户未指定复权方式，默认不复权。

## 工作步骤（Workflow）

本 skill 分为两个典型使用场景，请不要混用：

- **今日盘中行情查看**：
  - 只关心“今天涨跌多少、量价情况如何”的盘中快照；
  - 直接调用 `scripts/today.py`：
    - 例如：`python scripts/today.py 方大炭素`
    - 内部仅使用 `ak.stock_zh_a_spot` 拉当前实时盘口，不经过 `fetch.py` / `analyze.py`；
  - 对输出的“最新价 / 涨跌幅 / 成交量 / 最高 / 最低”做简单解读即可。

- **日线趋势 / 策略分析**：
  - 需要结合最近一周 + 当天的日线数据，判断趋势、signal、score 等；
  - 才使用 `fetch.py` + `analyze.py` 这一整套日线分析流程（见下文步骤 1~5）。

当是“趋势 / 策略分析”场景时，按以下步骤工作：

1. **解析用户意图和参数**
   - 从自然语言中解析出：
     - `symbol_or_name`
     - 时间范围（`start_date`/`end_date` 或 `days`）
     - `prefer`（sina/tx）和 `adjust`（"", "qfq", "hfq"）
   - 若信息缺失，向用户简短追问（优先问股票代码/名称）。

2. **获取行情+指标数据**
   - 尽量以“导入模块 + 调用函数”的方式使用现有代码：
  - 从 `scripts/fetch.py` 导入 `fetch_with_indicators`。
     - 调用：
       - 显式日期：
         - `fetch_with_indicators(symbol_or_name, start_date, end_date, adjust, prefer)`
       - 仅天数：
         - 先根据当前日期计算 start/end 字符串，再调用上面的函数。
    - 如需快速验证，也可以使用 CLI 方式：
     - 在 skill 根目录下执行：
       - `python scripts/fetch.py <symbol> --days 120 --prefer sina --adjust ""`
   - 若数据拉取失败（网络错误、接口异常、代码错误），应：
     - 把错误信息简要反馈给用户
     - 不要编造分析结果

3. **调用策略分析引擎**
   - 优先方式：在 Python 环境中导入并直接调用：
  - `from scripts.analyze import analyze_single`
     - `res = analyze_single(ts_code=symbol_or_name, df=df_with_indicators)`
    - 或使用 CLI：
     - 在 skill 根目录下执行：
       - `python scripts/analyze.py <symbol> --days 120 --prefer sina --adjust ""`
   - 获取 `AnalysisResult`，可以通过：
     - `asdict(res)` 形式转换为普通字典，方便解读字段。
     - 字段含义与推荐用法详见 `scripts/analyze_result.md`，便于后续自动化/NL 解读。

4. **解释字段并生成自然语言结论**
   - 至少解释这些核心字段：
     - `trend`：当前是多头/空头/震荡趋势，简要说明依据（近期一周涨跌幅）。
     - `weekly_change_pct`：最近一周涨跌幅（%），说明“这一周整体是涨还是跌、多大幅度”。
     - `today_change_pct`：今天相对昨天的涨跌幅（%），说明“今天是大涨/小涨/小跌/大跌”。
     - `signal`：当前信号是 buy / sell / hold，并说明触发的逻辑大致是什么。
     - `score`：所在区间（例如 0~2 很弱、3~5 一般、6~8 偏强、9~10 很强）。
   - 如用户关心，也可以简要提及：
     - `macd_strength`, `macd_momentum`, `rsi_zone`, `rsi_trend` 等作为辅助参考；
     - 均线结构与趋势强度：`ma_pattern` / `ma_bias` / `ma_spread` / `trend_strength`；
     - 风险与拐点：`reversal_hint` / `risk_level`，用于说明是否存在顶部/底部预警或趋势过度发散等风险。
   - 若需要更系统、模板化的“交易员风格”解读，可在执行完 `analyze.py` 后，将 `asdict(res)` 结果连同 `scripts/analyze_result.md` 的字段说明，交给专门的解读模块（例如 `scripts/analyze_data.md` 中描述的规范）生成文本。

5. **输出格式**
   - 使用简洁的中文分点说明：
     - 一条描述当前趋势（多头/空头/震荡）
     - 一条描述周涨跌幅 + 今日涨跌幅
     - 一条说明 signal 和 score 的含义（例如“当前属明显空头，短期不建议参与”）
     - 一条风险提示：本分析基于技术指标和短期价格表现，不构成投资建议。

## 输出示例（示意）

> 趋势：空头（bearish）。最近一周累计下跌约 13.9%，整体处在明显下跌通道。
>
> 涨跌情况：今天相对昨天约 -2.5%，延续下跌，未见有效止跌信号。
>
> 信号与评分：signal = sell，score = 1（0~10 中偏底部区间，短期状态较差）。
>
> 结论：这只股票当前短期趋势偏弱，风险较高，不适合作为当前关注重点标的，如已持有可考虑减仓或观望处理。以上仅为技术面参考，不构成投资建议。

## 注意事项（Safety / Caveats）

- 所有结论仅基于技术指标和短期价格表现，不考虑公司基本面、消息面等因素。
- 在表述时避免使用“必然、肯定、保证”等绝对化措辞，使用“偏强/偏弱/倾向于”等表述。
- 明确提醒用户：
  - 本结论不构成投资建议。
  - 投资决策需结合自身风险承受能力和更多信息谨慎判断。
