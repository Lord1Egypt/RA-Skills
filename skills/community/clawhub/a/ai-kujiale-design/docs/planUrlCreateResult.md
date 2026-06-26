## 描述
轮询临摹图导入酷家乐方案任务结果，返回方案 id 和楼层 id
对应任务创建接口：【临摹图导入酷家乐方案 - 创建任务】
## API
```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/bitmap/floorplan-import/status
```
## 入参
### Query Param
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌|
|task_id                                            |是| string              |对应创建任务接口返回的任务 id|
### Request Header
|参数|是否必须|参数类型|
| ------------ | :------------: | :------------: |
|Content-Type|是| string，固定值 application/json|
## 响应
### 数据结构
```javascript
{
    "c": "0",
    "m": "",
    "d": {
        "planId": "3FO4M42KW0BB",
        "levelId": "NBXJMF5MDSZFQAABAAAAACY8"
    }
}
```
### 字段说明
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|c                                                 |否| string              | 状态码，成功为 0，详见下表|
|m                                                 |否| string              | 在失败时返回的便于查看的错误信息|
|d                                                 |否| object              | 结果对象|
|d.planId                                          |否| string              | 导入的酷家乐方案的 id|
|d.levelId                                         |否| string              | 导入的酷家乐方案的对应楼层的 id|
## 状态码
|状态码|说明|
| ------------ | ------------ |
|0|成功|
|-1|其他错误，请咨询客服或技术支持|
|-2|任务进行中，请稍后继续轮询 |
|-3|无法找到任务，任务已过期或者 task_id 错误|
|-4|非法参数 model_version，请检查是否在指定范围|
|-5|自动识别比例失败，请检查图片是否是户型图|
|-6|非法楼层参数，请检查是否在指定范围|