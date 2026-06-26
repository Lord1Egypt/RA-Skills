---
name: beawan-stock-report
description: 查询A股上市公司财务报告分析地址，支持一季报、中报、三季报、年报
version: 1.0.0
author: beawan
---

# 碧湾股票报告查询

查询A股上市公司的财务报告分析地址。

## 配置

使用前需要设置您的 APIKEY：

先去应用市场下载碧湾App，登录后点击头像->碧湾Skills获取

```
APIKEY: <your-api-key>
```

## 接口说明

**查询报告地址**

```
GET http://api.beawan.com/beawanSkill/api/skill/report
Header: X-API-KEY: <your-api-key>
```

参数：

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| comCode | string | 股票代码 | 000001 |
| year | int | 年份 | 2024 |
| type | string | 报告类型 | 年报 |

报告类型取值：`一季报` / `中报` / `三季报` / `年报`

#### 参数说明
- &zwnj;**type**&zwnj; (string, required): 报告类型的中文名称。
    - &zwnj;**重要**&zwnj;：请直接传递中文字符串，例如 "中报"、"年报"。
    - &zwnj;**禁止**&zwnj;：不要传递十六进制编码（如 0xe4...）、Unicode 转义序列或 URL 编码后的字符串。
    - &zwnj;**示例**&zwnj;：如果用户查询“中报”，参数值应为 `"中报"`。

**返回示例：**

```json
{
  "code": 0,
  "data": {
    "url": "http://api.beawan.com/industry/html/load?name=jm43RF6Yb*K8GjWoO9VbDYxmHGa5rwppT97kMmM4mgM="
  }
}
```

## 使用示例

查询平安银行 2024 年年报：

```
GET http://api.beawan.com/beawanSkill/api/skill/report?comCode=000001&year=2024&type=年报
X-API-KEY: sk-your-api-key-here
```

查询贵州茅台 2024 年中报：

```
GET http://api.beawan.com/beawanSkill/api/skill/report?comCode=600519&year=2024&type=中报
X-API-KEY: sk-your-api-key-here
```
