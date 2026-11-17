# alibaba.1688.customer.attr.field.config

获取当前商家可用的筛选维度（生效的自定义属性列表 + 可用标签列表）。

## 前置条件

- AK 由框架通过环境变量 ALI_1688_AK 自动注入

## 参数

| 参数 | CLI 选项 | 类型 | 必传 | 说明 |
|------|----------|------|------|------|
| raw | `--raw` | flag | 否 | 返回精简后的完整配置数据；默认仅返回 markdown |

## 返回字段

| 字段 | 类型 | 说明 |
|------|------|------|
| data.activeAttrs | Array | 生效的自定义属性列表 |
| data.activeAttrs[].attrKey | String | 属性编码（直接作为 filters[].field 的值，不加 attr_ 前缀） |
| data.activeAttrs[].attrLabel | String | 属性显示名 |
| data.activeAttrs[].attrType | String | 属性类型：string/number/date/boolean |
| data.filterableTags | Array | 可用标签列表 |
| data.filterableTags[].tag | String | 标签编码 |
| data.filterableTags[].label | String | 标签显示名 |

## 典型用法

```bash
python3 {baseDir}/cli.py alibaba.1688.customer.attr.field.config
```

## 输出格式

- 默认模式：返回 `success` 和 `markdown`，不返回完整配置数据。
- `--raw` 模式：返回 `success` 和精简后的 `data.activeAttrs` / `data.filterableTags`，不返回 `markdown`。
