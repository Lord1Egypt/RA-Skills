## 描述

AI智能设计平台的标签查询

## API

```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/tag/list
```

## 入参

### Query Param

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
|access_token                                      |是| string              | 用户系统配置的令牌|

## 响应

### 数据结构

```javascript
{
  "c": "0",
  "m": "",
  "d": [
    {
      "tagName": "预算范围",
      "type": 0,
      "items": [
        {
          "tagItemId": "3FO4K4VYAW5G",
          "tagItemName": "三万",
          "tagId": "3FO4K4VYAW5G",
          "order": 1
        }
      ],
      "tagId": "3FO4K4VYAW5G",
      "order": 1
    }
  ]
}
```

### 字段说明

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| c | 否 | string | 响应码 |
| m | 否 | string | 响应消息 |
| d | 否 | list&object | 响应数据 |
| d.tagName | 否 | string | 标签名称 |
| d.type | 否 | int | 选择方式 0-单选，1-多选 |
| d.items | 否 | list&object | 标签项集合 |
| d.items.tagItemId | 否 | string | 标签项ID |
| d.items.tagItemName | 否 | string | 标签项名称 |
| d.items.tagId | 否 | string | 标签ID |
| d.items.order | 否 | int | 序列 |
| d.tagId | 否 | string | 标签ID |
| d.order | 否 | int | 序列 |
