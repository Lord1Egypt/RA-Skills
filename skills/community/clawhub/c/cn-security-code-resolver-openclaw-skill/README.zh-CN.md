# cn-security-code-resolver

一个用于 **OpenClaw** 的中国证券代码解析 Skill。

作用：根据中文标的名称，自动解析出对应的 **A股 / ETF / 基金** 交易代码，并尽量补全标准交易代码格式。

## 适用场景

适用于以下任务：
- 根据中文名称查询证券代码
- 给持仓清单、观察名单补全标的代码
- 将 JSON / Markdown / 文档中的中文标的名称转换成可交易代码
- 确认某个标的是股票、ETF 还是基金

例如：
- 红利ETF华泰柏瑞 → `510880.SH`
- 苏美达 → `600710.SH`
- 中国海油 → `600938.SH`
- 海油发展 → `600968.SH`
- 中海油服 → `601808.SH`

## 包含内容

- `SKILL.md`：Skill 使用说明
- `scripts/resolve_cn_security.py`：核心解析脚本
- `references/eastmoney-api.md`：东方财富 suggest API 参考说明

## 使用方法

### 单个查询

```bash
python3 scripts/resolve_cn_security.py "中国海油"
```

### 批量查询

```bash
python3 scripts/resolve_cn_security.py "红利ETF华泰柏瑞" "苏美达" "中国海油" "海油发展" "中海油服"
```

## 输出示例

```json
[
  {
    "query": "中国海油",
    "resolved": {
      "name": "中国海油",
      "code": "600938",
      "standardCode": "600938.SH",
      "exchangeSuffix": "SH",
      "securityTypeName": "沪A",
      "quoteId": "1.600938"
    }
  }
]
```

## 数据来源

当前版本默认使用 **东方财富公开搜索接口（suggest API）** 进行解析。

## 注意事项

- 默认优先返回 **中国内地市场** 对应代码
- 如果同名标的存在 A股 / 港股 / 基金等多种结果，应结合 `securityTypeName` 做确认
- 本 Skill 适合做“标的识别”，不负责实时行情、估值和交易建议
