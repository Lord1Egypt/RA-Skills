---
name: fx-converter
description: "实时汇率换算（ECB 欧洲央行参考汇率，免费无 Key）。支持美元/人民币/欧元/日元等 20+ 主要货币互转、批量列出、金额换算。"
homepage: https://www.frankfurter.app/
metadata:
  {
    "openclaw":
      {
        "emoji": "💱",
        "install":
          [
            {
              "id": "curl",
              "kind": "brew",
              "formula": "curl",
              "bins": ["curl"],
              "label": "Install curl",
            },
            {
              "id": "python3",
              "kind": "apt",
              "formula": "python3",
              "bins": ["python3"],
              "label": "Install python3",
            },
          ],
      },
  }
---

# fx-converter.sh 实时汇率换算

实时汇率查询与换算，数据源为 **Frankfurter API**（欧洲央行 ECB 每日参考汇率），
免费、无需 API Key、覆盖 30+ 货币。

## 用法

```bash
fx-converter.sh USD CNY              # 1 USD = ? CNY
fx-converter.sh USD CNY 100          # 100 USD = ? CNY
fx-converter.sh USD                  # 列出 USD 兑主要货币
fx-converter.sh --list               # 列出支持的货币
fx-converter.sh --help               # 帮助
```

## 支持货币

美元 USD、人民币 CNY、欧元 EUR、日元 JPY、英镑 GBP、港币 HKD、新台币 TWD、
韩元 KRW、新加坡元 SGD、澳元 AUD、加元 CAD、瑞郎 CHF、新西兰元 NZD、
泰铢 THB、马币 MYR、卢比 INR、卢布 RUB、雷亚尔 BRL、墨西哥比索 MXN、
兰特 ZAR、瑞典克朗 SEK、挪威克朗 NOK、丹麦克朗 DKK

## 说明

- 汇率来自 ECB（欧洲央行），每日更新
- 支持任意金额（整数/小数）
- 小众货币组合若不支持，会提示用 USD 中转
