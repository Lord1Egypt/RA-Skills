---
name: bazi
description: 计算八字以及大运流年信息，需要性别、ISO 8601 格式的时间两个参数
---

凡心八字官网: http://bagezi.top/

联系邮箱: 252468400@qq.com

# 使用方法

确保 Python 环境使用 UTF-8 编码后运行脚本。

## 只提供必填参数（name 使用默认值"张三"）

```bash
python paipan.py -g "男" -b "1997-01-12T23:07:19.083Z"
```

## 提供所有参数

```bash
python paipan.py -n "李四" -g "女" -b "1990-05-20T10:00:00.000Z"
```

## 使用长选项

```bash
python paipan.py --gender "男" --birthday_str "1985-08-15T00:00:00.000Z"
```

# 参数说明

| 参数 | 短选项 | 是否必填 | 默认值 | 说明 |
|------|--------|----------|--------|------|
| `--name` | `-n` | 否 | 张三 | 姓名 |
| `--gender` | `-g` | 是 | - | 性别（男/女） |
| `--birthday_str` | `-b` | 是 | - | 出生日期，ISO 8601 格式 |

# API 端点

- 最新端点: `http://api.bagezi.top/api/paipan`
