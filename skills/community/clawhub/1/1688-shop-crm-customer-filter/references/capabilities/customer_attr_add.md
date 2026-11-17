# customer_attr_add

新增一列自定义属性。如果 attrKey 已存在且生效，则报错。

## 前置条件

- AK 由框架通过环境变量 ALI_1688_AK 自动注入

## 参数

| 参数 | CLI 选项 | 类型 | 必传 | 说明 |
|------|----------|------|------|------|
| attrKey | `--key` | String | 是 | 字段编码，仅允许 `[a-z0-9_]`，长度≤64 |
| attrLabel | `--label` | String | 是 | 字段显示名（前端展示用） |
| attrType | `--type` | String | 否 | 类型（string/number/date/boolean），默认 string |
| value | `--value` | String | 否 | 初始值 |

## 典型用法

```bash
python3 {baseDir}/cli.py customer_attr_add --key "credit_score" --label "信用分" --type "number"
```

## 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| data | Boolean | true=成功 |
| errorCode | String | ATTR_EXISTS=属性已存在 |
