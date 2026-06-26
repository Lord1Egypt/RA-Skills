## 描述
创建临摹图导入酷家乐方案任务，返回任务 id
对应轮询接口：【临摹图导入酷家乐方案 - 轮询结果】
## API
```
POST https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/bitmap/import/async
```
## 入参
### Query Param
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌|
|bitmap                                            |是| string              | 临摹图图片 url，需要在公共网络可以直接访问的 HTTP 地址，支持 jpg、jpeg、png、bmp、gif 格式，url 只支持以小写图片格式后缀结尾，不支持其他后缀|
|id|否|string|酷家乐 planId，要导入到已有方案传此值，需要是当前账号下的 bim 方案，否则会报错，留空为创建新方案|
|name|否|string|要创建的方案的名称|
|level_id|否|string|要导入到已有方案的已有楼层传此值，需要是上述 planId 下的有效楼层 id，否则会报错，不传时默认导入到一层，与下面 level_index 参数同时传时 level_index 生效，此参数不生效|
|level_index|否|int|要导入到已有方案的指定楼层（无论此楼层是否已创建）传此值，范围为 [-10,10]（不包括 0），否则会报错，不传时默认导入到一层|
|scale                                             |否| double              | 比例，每像素对应的物理世界毫米数，不传时由模型自动识别|
|target_building_area|否|double|指定导入方案的建筑面积，单位㎡，不传时使用 scale 值对应的比例生成或由模型自动识别|
|model_version|否|int|酷家乐临摹图识别大模型版本，目前有 1、2，默认值 2|
|model_type|否| string|酷家乐临摹图识别大模型类型，目前有 DETECTION（检测模型）、GENERATION（生成式模型），默认值 DETECTION，仅对 model_version = 2 生效|
|need_layout|否|boolean|是否识别平面布置图例，默认值 false|
### Request Header
|参数|是否必须|参数类型|
| ------------ | :------------: | :------------: |
|Content-Type|是| string，固定值 application/json|
### Request Body
```javascript
{
    "min": {
        "x": 16,
        "y": 470
    },
    "max": {
        "x": 604,
        "y": 859
    }
}
```
请求体参数说明：

|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|Request Body(root)|否| object              | 指定图片识别区域的包围盒，不传时识别全图|
|min                                               |是| object              |区域最小点|
|min.x                                             |是| double              | 最小点 x 坐标，单位为像素|
|min.y                                             |是| double              | 最小点 y 坐标，单位为像素|
|max                                               |是| object              | 区域最大点|
|max.x                                             |是| double              | 最大点 x 坐标，单位为像素|
|max.y                                             |是| double              | 最大点 y 坐标，单位为像素|
### 坐标系说明
图片识别区域坐标为图片坐标系（左手系），左上点为原点，向右为 x 正方向，向下为 y 正方向
![临摹图导入指定区域](//qhsaas-oss.kujiale.com/open/platform/plugin/UID_950f5b65_d9ca_47ec_1752155804913.png)
如上图所示，包围盒左上像素点为 min，右下像素点为 max
## 响应
### 数据结构
```javascript
{
    "c": "0",
    "m": "",
    "d": "AAABl_hq5Ios8F3n3YgAAQ"
}
```
### 字段说明
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|c                                                 |否| string              | 状态码，成功为 0，详见下表|
|m                                                 |否| string              | 在失败时返回的便于查看的错误信息|
|d                                                 |否| string              | taskId，用于轮询任务结果|
## 状态码
|状态码|说明|
| ------------ | ------------ |
|0|成功|
|-1|其他错误，请咨询客服或技术支持|
|-2|无法下载图片或图片后缀错误，请检查图片地址合法性和连通性|