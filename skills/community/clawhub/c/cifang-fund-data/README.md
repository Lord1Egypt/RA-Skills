# cifang-fund-data

A股场内基金（ETF / LOF）行情数据获取Skill, 可用于openclaw, claude hermes, claude code等智能体。基于[次方量化](https://www.cifangquant.com) API，支持历史行情、实时行情和收益率排行查询。

## 前置条件

- [次方量化](https://www.cifangquant.com) VIP 账号及 API Key
- 设置环境变量：

```bash
export CIFANG_API_KEY="your-api-key"
```

## 作为 Claude Code 技能使用

安装后，直接用自然语言与 Claude 对话即可触发技能：

```
获取沪深300ETF（510300）2024年全年的历史行情，使用前复权
比较510300和510500过去一年的表现，计算收益率和最大回撤
查找所有沪深300相关的ETF基金
获取国投白银LOF（161226）和黄金ETF（518880）的实时行情
获取近1月收益率最高的前10只场内基金排行
```

## 作为 Python 脚本使用

脚本位于 [scripts/fetch_fund_data.py](scripts/fetch_fund_data.py)，支持命令行调用。

### 查询基金列表

```bash
# 使用 --api-key（推荐）
python scripts/fetch_fund_data.py --api-key "your-api-key" list --keyword 沪深300

# 或使用环境变量
python scripts/fetch_fund_data.py list --keyword 沪深300
```

### 获取历史行情

```bash
python scripts/fetch_fund_data.py history 510300 510500 \
  --start-date 2024-01-01 \
  --end-date 2024-12-31 \
  --adjust qfq \
  --format readable
```

`--format` 可选值：

| 值 | 说明 |
|---|---|
| `raw` | API 原始数组格式 |
| `readable` | 转换为命名字段的对象格式（默认） |
| `stats` | 汇总统计（收益率、波动率、最大回撤） |

### 获取实时行情

```bash
# 指定基金
python scripts/fetch_fund_data.py spot 161226 518880

# 全量返回（约10秒）
python scripts/fetch_fund_data.py spot
```

### 获取场内基金排行

```bash
python scripts/fetch_fund_data.py rank --sort-by 1yzf --sort-order desc --limit 20
```

`--sort-by` 可选值：`zzf`(近1周) / `1yzf`(近1月) / `3yzf`(近3月) / `6yzf`(近6月) / `1nzf`(近1年) / `2nzf`(近2年) / `3nzf`(近3年) / `jnzf`(今年来) / `lnzf`(成立以来)

### 搜索基金

```bash
python scripts/fetch_fund_data.py search 黄金
```

## API 速查

| 接口 | 端点 | 关键参数 |
|---|---|---|
| 基金列表 | `GET /api/fund/list` | `key_word` |
| 历史行情 | `GET /api/fund/hist_em` | `symbol`(最多50个), `start_date`, `end_date`, `adjust` |
| 实时行情 | `GET /api/fund/spot` | `symbol`(可选，不传返回全量，延迟≤2分钟) |
| 场内排行 | `GET /api/fund/exchange_rank` | `sort_by`, `sort_order`, `limit` |

认证方式：请求头 `x-api-key: YOUR_API_KEY`

完整 API 文档见 [references/api_reference.md](references/api_reference.md)。

## 历史行情数据字段

API 返回数组格式，各索引含义如下：

| 索引 | 字段 | 说明 |
|---|---|---|
| 0 | date | 交易日期 YYYY-MM-DD |
| 1 | open | 开盘价 |
| 2 | close | 收盘价 |
| 3 | high | 最高价 |
| 4 | low | 最低价 |
| 5 | change_percent | 涨跌幅 (%) |
| 6 | volume | 成交量 |

## 复权说明

| 参数值 | 含义 |
|---|---|
| `none` | 不复权（原始价格） |
| `qfq` | 前复权，以当前价格为基准向前调整（长期分析推荐） |
| `hfq` | 后复权，以历史价格为基准向后调整 |

## 错误处理

| HTTP 状态码 | 原因 | 处理方式 |
|---|---|---|
| 401 | API Key 无效或未提供 | 检查 `CIFANG_API_KEY` 环境变量 |
| 400 | 参数格式错误 | 检查日期格式（YYYY-MM-DD）和代码格式 |
| 404 | 基金代码不存在 | 先用列表接口确认代码 |
| 429 | 请求频率超限 | 降低请求频率 |

## 许可证

本项目采用 [MIT No Attribution License (MIT-0)](https://spdx.org/licenses/MIT-0.html)。
完整协议文本见 [`LICENSE`](LICENSE) 文件。
