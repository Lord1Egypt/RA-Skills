

## 描述
校验版本
## API
```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/version/check
```
## 入参
### Query Param
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|version                                           |是| string              | 当前skill的版本号信息|
|access_token                                      |是| string              | 用户系统配置的令牌|
## 响应
### 数据结构
```javascript
{
	"d":{
		"action":"",
		"version":null,
		"isLastest":"",
		"latestVersion":null
	},
	"m":null,
	"c":null
}
```
### 字段说明
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|c                                                 |是| string              | null|
|m                                                 |是| string              | null|
|d                                                 |是| object              | null|
|d.version                                         |否| string              | 当前用户版本|
|d.isLastest                                       |否| boolean             | 是否最新版本|
|d.latestVersion                                   |否| string              | 最新版本版本号|
|d.action                                          |否| int                 | 版本拦截行为，如果是0表示版本校验通过，如果是1表示当前版本已经不是最新版本但任然可以继续使用，如果是2则表示当前版本已经被禁用，用户需要重新安装最新版的skill进行使用，否则终止流程|
