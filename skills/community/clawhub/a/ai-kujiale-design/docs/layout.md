## 描述

AI智能设计平台支持客户调用进行智能布局

## API

```
POST https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/customize-layout
```

## 入参

### Query Param

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
|access_token                                      |是| string              | 用户系统配置的令牌|

### Request Body

```javascript
{
    "designId": "",
    "tagIds": [
        ""
    ],
    "styleId":"",
    "customStyleId":"",
    "applyDecorationStyle":false,
    "buildCeiling": true,
    "autoDesign" : false,
    "platform": 3
}
```

请求体参数说明：

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| designId | 是 | string | 方案ID |
| tagIds | 是 | list&string | 标签项列表 |
| styleId| 是 | string | 硬装风格ID |
| customStyleId| 是 | string| 定制风格ID |
| applyDecorationStyle| 是 | boolean | 是否使用硬装风格 |
| buildCeiling | 否 | boolean |是否生成吊顶 |
| autoDesign| 否 | boolean | 是否继续进行自动设计 |
| platform| 是 | integer | 创建的平台，在这里写死3传递 |

## 响应

### 数据结构

```javascript
{
	"d":"3FO4LW0CK4B8",
	"m":"",
	"c":"0"
}
```

### 字段说明

| 参数 | 是否必须 | 参数类型 | 参数说明 |
| --- | :---: | :---: | ---- |
| c | 是 | string | 响应码 |
| m | 是 | string | 响应信息,如果响应码是"-1"且响应信息是"个人商业化功能余额不足"的时候需要给到用户信息"您当前可用核豆已用尽，点击链接完成订阅或充值后，重新触发生成即可" |
| d | 是 | string | 方案ID |
