---
name: beergaao
description: A股/港股/美股量化分析工具，提供技术分析、策略生成、回测验证和风险管理功能
version: 3.2.6
metadata: {"openclaw": {"requires": {"env": ["TUSHARE_TOKEN"]}, "primaryEnv": "TUSHARE_TOKEN"}}
---

# BeerGaao 股票量化分析师

BeerGaao 是一个专为 股票市场设计的量化分析 Agent 工具集，为 AI Agent 提供标准化的股票分析能力。

## BeerGaao 可以成为你的：

- 💰 **自动量化工厂**：10+ 传统策略 + ML 策略 + 集成引擎，自动生成交易信号
- 🤖 **智能分析 Agent**：支持自然语言交互，一键完成股票技术分析
- 📊 **多数据源网关**：整合 Tushare、东方财富、Yahoo Finance（选装）、长桥 OpenAPI（选装）
- 🔬 **因子研究平台**：因子 IC 分析、策略归因、参数自动校准
- 📈 **回测验证系统**：三年历史数据回测，胜率 50%+，夏普比率 1.0+

## 可用工具

| 工具 | 功能 | 参数 |
|------|------|------|
| `analyze_stock` | 完整技术分析（策略+集成+ML+IC+校准） | `code` |
| `get_quote` | 实时行情报价 | `code` |
| `analyze_market` | 大盘环境分析 | — |
| `get_money_flow` | 资金流向 | `code` |
| `get_sector_flow` | 板块资金排名 | `limit` |
| `get_dragon_tiger` | 龙虎榜数据 | — |
| `full_review` | 完整复盘 | `watchlist` |
| `backtest_bt` | Backtrader 专业回测 | `code,strategy,start,end,cash` |
| `strategy_attribution` | 策略归因分析 | `days` |
| `check_correlation` | 相关性检查 | `codes` |
| `circuit_breaker_check` | 熔断检查 | — |
| `get_market_breadth` | 市场广度指标 | — |

## 调用示例

**用户："分析一下贵州茅台的走势"**
→ 调用 `analyze_stock("600519.SH")`

**用户："今天大盘怎么样"**
→ 调用 `analyze_market()`

**用户："招商银行资金流向"**
→ 调用 `get_money_flow("600036.SH")`

**用户："复盘一下"**
→ 调用 `full_review()`

**用户："用MACD策略回测招商银行"**
→ 调用 `backtest_bt("600036.SH", "MACDStrategy", "2023-01-01", "2026-04-30")`

## 信号类型

- **买入** — 多源共识置信度 ≥ 0.6
- **卖出** — 卖出信号共识 > 买入信号
- **观察** — 有买入信号但置信度 0.4-0.6
- **持有** — 无明确方向信号

## 支持的股票代码格式

- A股：`600036.SH`（上海）、`000001.SZ`（深圳）、`300750.SZ`（创业板）
- 港股：`0700.HK`
- 美股：`AAPL.US`

## 安装使用

```bash
git clone https://github.com/GanJiaKouN16/BeerGaao.git
cd BeerGaao
pip install -r requirements.txt
cp config.example.env config.env
# 编辑 config.env 填入 TUSHARE_TOKEN
```

## 配置要求

| 变量 | 说明 | 必需 |
|------|------|------|
| `TUSHARE_TOKEN` | Tushare API token（只读） | 是 |
| `LONGPORT_APP_KEY` | 长桥 App Key | 否 |
| `LONGPORT_APP_SECRET` | 长桥 App Secret | 否 |
| `LONGPORT_ACCESS_TOKEN` | 长桥 Access Token（建议只读） | 否 |

## 安全说明

> ⚠️ **重要安全提示**

**凭证安全（强制要求）：**
- 所有 API 凭证**必须**通过环境变量提供，代码中**不包含**任何硬编码的 token 或 secret
- `providers.py` 中所有凭证均通过 `self._config.longport_access_token` 等配置属性读取，最终来源为环境变量
- 东方财富 API 的 `ut` 参数通过 `EASTMONEY_UT` 环境变量配置（有默认值，通常无需修改）
- 使用前请确保已设置以下环境变量：
  - `TUSHARE_TOKEN`：Tushare API token（必填）
  - `LONGPORT_APP_KEY`：长桥 App Key（可选）
  - `LONGPORT_APP_SECRET`：长桥 App Secret（可选）
  - `LONGPORT_ACCESS_TOKEN`：长桥 Access Token（可选，建议只读权限）
- 技能启动时会自动检查必填凭证是否存在，缺失时会抛出明确的错误提示
- `config.env` 已被 `.gitignore` 排除，**绝不提交到版本控制系统**

**数据安全：**
- 本工具仅读取公开市场数据，**不执行实际交易**
- SQLite 数据库默认存储在项目 `.data/` 目录下（可通过 `DB_PATH` 环境变量自定义），已被 `.gitignore` 排除
- 数据库文件权限已设置为仅 owner 可读写（600），目录权限设置为 700
- 如需清除历史分析数据，删除 `.data/` 目录或指定的 `DB_PATH` 文件即可
- 不要加载来源不明的模型文件，模型加载有路径白名单保护

**模型安全：**
- 仅加载项目 `models/` 目录内本地生成的模型文件
- 禁止加载外部输入、网络下载或用户提供的任意模型文件
- 所有模型加载均通过 `load_model_safe()` 安全函数，自动执行路径白名单校验和文件完整性检查
- joblib 底层使用 pickle，存在反序列化风险，请勿加载不可信文件

**运行环境：**
- 建议在虚拟环境中安装运行
- 仅从官方仓库克隆代码：`https://github.com/GanJiaKouN16/BeerGaao.git`
- 定期轮换 API 密钥，移除不再使用的旧凭证

## 输出格式

所有工具返回统一格式：

```json
{"tool": "工具名", "status": "success | error", "data": {...}}
```

## ⚖️ Legal Disclaimer

The BeerGaao is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringence. The BeerGaao is aimed to facilitate research and development process in the financial industry and not ready-to-use for any financial investment or advice. Users shall independently assess and test the risks of the BeerGaao in a specific use scenario, ensure the responsible use of AI technology, including but not limited to developing and integrating risk mitigation measures, and comply with all applicable laws and regulations in all applicable jurisdictions. The BeerGaao does not provide financial opinions or reflect the opinions of GanJiaKouN16, nor is it designed to replace the role of qualified financial professionals in formulating, assessing, and approving finance products. The inputs and outputs of the BeerGaao belong to the users and users shall assume all liability under any theory of liability, whether in contract, torts, regulatory, negligence, products liability, or otherwise, associated with use of the BeerGaao and any inputs and outputs thereof.
