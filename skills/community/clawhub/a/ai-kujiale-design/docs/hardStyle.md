## 描述
AI智能设计平台的硬装风格获取
## API
```
POST https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/style/list
```
## 入参
### Query Param
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌|
### Request Body
```javascript
{
	"tagItemIds":[
		"3FO3VB26TL0T"
	]
}
```
请求体参数说明：

|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|tagItemIds                                        |否| list&string         | 标签项ID集合|
## 响应
### 数据结构
```javascript
{
  "c": "0",
  "m": "",
  "d": [
    {
      "coverUrl": "https://user-platform-oss.kujiale.com/design-zone/M5XD6ENMDTPHEAABAAAAABQ8.png",
      "styleId": "3FO4K4VY7XHK",
      "styleName": "全量风"
    }
  ]
}
```
### 字段说明
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|c                                                 |否| string              | 响应码|
|m                                                 |否| string              | 响应信息|
|d                                                 |否| list&object         | 响应数据|
|d.coverUrl                                        |否| string              | 封面图|
|d.styleId                                         |否| string              | 风格ID|
|d.styleName                                       |否| string              | 风格名称|
