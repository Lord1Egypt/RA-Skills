# A 股行情 Skill - 实时获取 A 股股票行情

使用腾讯财经免费 API，无需 API Key。

## 安装

```bash
# 创建符号链接（需要 sudo 密码）
sudo ln -sf ~/.openclaw/workspace/skills/a-stock-market/a-stock.py /usr/local/bin/a-stock

# 或者直接在技能目录运行
python3 ~/.openclaw/workspace/skills/a-stock-market/a-stock.py sh600519
```

## 用法

```bash
# 查询单只股票
a-stock sh600519        # 贵州茅台
a-stock sz000858        # 五粮液

# 查询多只股票
a-stock sh600519 sz000858 sh000300

# 查询指数
a-stock sh000001        # 上证指数
a-stock sz399001        # 深证成指
a-stock sh000300        # 沪深 300
```

## 股票代码格式

- **上交所**: `sh` + 6 位数字
  - `sh600519` 贵州茅台
  - `sh601318` 中国平安
  - `sh000001` 上证指数

- **深交所**: `sz` + 6 位数字
  - `sz000858` 五粮液
  - `sz300750` 宁德时代
  - `sz399001` 深证成指

## 输出示例

```
📈 贵州茅台 (sh600519)
   现价：1680.00  +1.23%
   开盘：1665.00  最高：1685.00  最低：1660.00
   昨收：1659.50
   成交量：12345 手  成交额：20678 万
```

## 数据来源

腾讯财经免费 API: `https://qt.gtimg.cn/q={股票代码}`

- 实时更新（交易时间内）
- 无需 API Key
- 支持 A 股所有股票和指数
