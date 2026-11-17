---
name: cn-holidays
description: "中国法定节假日查询（数据源 Nager.Date，免费无 Key）。支持查询全年节假日、指定月份、指定日期是否放假。"
homepage: https://date.nager.at/
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
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

# cn-holidays.sh 中国节假日查询

查询中国法定节假日安排，数据源为 **Nager.Date** 公共节假日 API（免费、无需 Key）。

## 用法

```bash
cn-holidays.sh              # 今年所有法定节假日
cn-holidays.sh 2026         # 指定年份
cn-holidays.sh 2026-10      # 指定月份
cn-holidays.sh 2026-10-01   # 指定日期是否放假
cn-holidays.sh --help       # 帮助
```

## 示例

```bash
cn-holidays.sh 2026-10-01   # 🎉 2026-10-01 是法定节假日：国庆节
cn-holidays.sh 2026-10      # 列出 2026 年 10 月所有节假日
```

## 说明

- 返回中国法定节假日（元旦、春节、清明、劳动节、端午、中秋、国庆等）
- 注意：Nager.Date 提供的是节假日日期，不包含调休安排（补班日期），
  具体放假调休以国务院通知为准
