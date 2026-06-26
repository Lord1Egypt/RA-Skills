



## 描述
通过指定户型ID创建一个装修方案，返回新创建的方案ID，该指定户型将从户型阶段升级到装修阶段；如果该户型已经是装修阶段，则接口会返回对应的已生成的方案ID。
户型ID可以是任意户型ID，如果户型属于当前指定用户，则会把当前户型升级到装修阶段；如果该户型不属于当前指定用户，则会复制一份户型给当前用户，并且基于复制户型升级到装修阶段。
## API
```
POST https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/design/creation
Content-Type: text/plain;charset=utf-8
```
## 入参
### URL Query Param
|参数   |是否必须   |参数类型   |参数说明   |例子|
| ------------ | :------------: | :------------: | ------------ | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌|
|plan_id   |是   |string   |酷家乐户型图ID。可从[获取户型](https://www.kujiale.com/op/api/doc/redirect?doc_id=11 "获取户型")相关接口中获得。   |3FO4I4VH740D|
|name    |否   |String   |复制后的方案的方案名称，默认不传会以酷家乐系统默认名字为准，例如：（原方案名）+副本的规则，或其他默认规则（视酷家乐系统迭代而定）。   | （原方案名）+copy|
## 响应
### 数据结构
```javascript
{
  "c": "0",
  "m": "",
  "d": "3FO4K4VXY2IW"
}
```
### 字段说明
返回该户型对应的装修阶段的方案ID。