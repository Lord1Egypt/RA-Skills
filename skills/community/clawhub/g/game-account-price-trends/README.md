# 游戏账号行情与挂牌数据 Skill

这是一个 Claude skill，用于基于 `mall.yy.com / gamemarket.yy.com` 公开挂牌样本生成游戏账号行情与挂牌数据报告。

## 适用场景

- 我想看看王者荣耀账号最近的交易行情
- 查一下王者荣耀账号挂牌数据
- 看看和平精英账号价格分布
- 给我一份游戏账号行情报告

如果用户想查“我的号值多少钱 / 帮我估价 / 账号估值”，应使用单账号估值 skill，而不是本 skill。

## 目录结构

```text
mall-market-overview/
├── SKILL.md
├── README.md
└── scripts/
    ├── fetch_mall_trade_data.py
    └── generate_market_overview.py
```

## 为什么使用 Python 脚本

这个 skill 需要在 macOS、Linux 和 Windows 上都能使用。Python 标准库跨平台可用性比 shell 脚本更好；Windows 用户不一定有 Bash 环境，因此这里不使用 `.sh` 作为主入口。

## 本地试用

从仓库根目录运行：

```bash
python3 scripts/fetch_mall_trade_data.py --game 王者荣耀 --page-size 20 --pages-per-sort 1 --sort-profile all > /tmp/mall-market-overview.json
python3 scripts/generate_market_overview.py /tmp/mall-market-overview.json
```

Windows PowerShell 可改用：

```powershell
python scripts/fetch_mall_trade_data.py --game 王者荣耀 --page-size 20 --pages-per-sort 1 --sort-profile all > mall-market-overview.json
python scripts/generate_market_overview.py mall-market-overview.json
```

## 参数

`fetch_mall_trade_data.py` 支持：

- `--page-size <n>`：每页数量，默认 `20`
- `--pages-per-sort <n>`：每个排序视角最多抓取页数，默认 `2`
- `--request-source <value>`：请求来源，默认 `SECLIST`
- `--sort-profile <all|baseline|recent|high_price>`：排序视角，默认 `all`
- `--game <游戏名>`：只查询指定游戏；可重复传多个，例如 `--game 王者荣耀 --game 原神`

排序视角：

- `baseline`：综合排序
- `recent`：最新发布
- `high_price`：价格最高

## 输出说明

报告包含：

- 总览：覆盖游戏、有效样本、均价/中位价/最高价等
- 游戏排行：按样本量汇总各游戏行情
- 单游戏摘要：价格区间、热度、热门区服、热门标签
- 高价样本和人气样本，带 mall.yy.com 详情页链接
- 异常与解读：样本少、存在极端高价、有更多分页等

报告基于挂牌采样，不代表全量市场，也不代表成交价。

## 隐私与安全

脚本不使用 Cookie、登录态或用户浏览器 session headers。
