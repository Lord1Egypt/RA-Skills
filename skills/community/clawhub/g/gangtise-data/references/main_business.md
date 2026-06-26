# 主营构成 API（Open API · main-business）

## 简介

通过 Gangtise Open API 查询上市公司**主营构成**（按产品/行业/地区等指标），脚本 **`scripts/main_business.py`**。

默认拉取文档中的**全部业务指标字段**；`breakdown` 不传时，对 **product、industry、region** 三种维度**并发**请求，合并为一张表，并以列 **「分行业/分产品/分地区」** 区分维度。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `-sd` / `--start-date` | 否 | 开始日期 `yyyy-MM-dd`。未指定时默认约为**结束日往前三年**。 |
| `-ed` / `--end-date` | 否 | 结束日期 `yyyy-MM-dd`。未指定时默认**今天**。 |
| `--securities` | 否* | **完整证券代码**，逗号分隔。 |
| `--securities-file` | 否* | CSV 须含列 **`security_code`**。 |
| `--breakdown` | 否 | `product` / `industry` / `region`。**不传**则三种维度并发全取。 |
| `--period` | 否 | 仅 **Q2** 或 **Q4**；见上表。不传则不限定报告期。 |

\* 须至少提供 `--securities` 或 `--securities-file` 之一。

## 约束与说明

- **仅支持完整证券代码**。
- 与 skills-backend 版「主营业务」的列名、接口不同，本脚本以 **Open API** 返回字段映射为中文列为主。

## 调用示例

```bash
python3 scripts/main_business.py --securities 000651.SZ
```

```bash
python3 scripts/main_business.py --securities 600519.SH --breakdown product
```

```bash
python3 scripts/main_business.py --securities-file ./codes.csv --period Q4
```

## 返回说明

- **成功**：在 `workspace/gangtise/main_business/` 下生成 **`main_business_*.csv`**。
- **失败**：如未配置授权、证券无效、无数据、`--period` 不是 Q2/Q4 等。

## 返回数据示例（CSV 列）

| security_abbr | security_code | date | 分行业/分产品/分地区 | 报告期 | 主营业务名称 | 营业收入 | … |
|---------------|----------------|------|----------------------|--------|--------------|----------|---|
| … | 000651.SZ | … | 分产品 | … | 空调 | … | … |

（`date` 对应接口中的报告期截止日期字段；具体列以 `fieldList` 与映射为准。）
