
## 描述
拉取指定方案下的渲染图列表v2，返回结果的默认排序是按照渲染图的创建时间从先到后排。
相较于v1支持了多语言并且新增了3个字段，是否进行美化，灯光模板id，灯光模板名称。
权限控制：商家只可获取自己账号体系下生成的方案的渲染图列表。
## API
```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/renderpic/list
Content-Type: text/plain;charset=utf-8
```
## 入参
注意此接口调用的时候不需要appuid，因此按照无appuid的方式进行鉴权sign
### URL Query Param
|参数   |是否必须   |参数类型   |参数说明   |例子|
| ------------ | :------------: | :------------: | ------------ | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌| xxxxxxx|
|design_id   |是   |string   |酷家乐方案ID。在[获取方案](https://www.kujiale.com/op/api/doc/redirect?doc_id=8 "获取方案")相关接口以及[生成方案](https://www.kujiale.com/op/api/doc/redirect?doc_id=24 "生成方案")接口中可以获得。  |3FO4I4VH740D|
|start   |是   |int   |拉取列表的偏移量，从0开始。   |0|
|num   |是   |int   |一次拉取的数量上限，从数据安全以及性能上考虑，num最大值限制为50，如果有拉取更多数据的需求，请发起多次请求。<br/>如果剩余数据量小于num，则会返回全部剩余数据。<br/>比如start=0&num=10表示拉取第1到第10个数据，start=10&num=10表示拉取第11个到第20个数据。   |10|
## 响应
### 数据结构
```javascript
{
  "c": "0",
  "m": "",
  "d": {
    "count": 1,
    "hasMore": true,
    "result": [
      {
        "created": 1426830582000,
        "img": "http://qhyxpic.oss.kujiale.com/rbet/2015/03/24/NSHMYLE7TQWA5J3CEY888888_800x600.jpg",
        "panoLink": "https://www.kujiale.com/xiaoguotu/pano/3FO4JLKQ5P95",
        "picId": "3FO4K5M8YDHR",
        "picType": 0,
        "picDetailType": 0,
        "roomName": "客厅",
        "level": 1,
	"roomIndex":987892,
	"roomTypeId":22,
	"hasPs": false,
        "lightStyleId": 0,
        "lightStyleName": "手动灯光",
        "favorite": false
      }
    ],
    "totalCount": 52
  }
}
```
### 字段说明
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|picId   |是   |string   |渲染图ID。   |
|picType   |是   |int   |渲染图类型。0表示普通渲染图，1表示全景图，3表示俯视图。   |
|picDetailType   |是   |int   |渲染图类型细分。取值枚举见附录。   |
|roomName   |是   |string   |渲染图所属房间的名字。   |
|img   |是   |string   |渲染图URL。   |
|panoLink   |否   |string   |全景图的链接地址。当渲染图是全景图类型的时候，这个字段会存在。   |
|created   |是   |long   |渲染图的创建时间。   |
|level   |否   |int   |渲染图所在房间的楼层信息，正为地上，负为地下室，不存在0层。理论上每个图片都会有楼层信息，但是当渲染图所在房间进过户型编辑被删除后，即无法通过图片识别到房间，则无法通过房间识别到对应的楼层。因此在渲染图所在楼层可能存在没有的情况。   |
|roomIndex   |是   |long   |渲染图的户型内的唯一识别id。 |
|roomTypeId   |是   |long   |渲染图房间类型Id|
|hasPs   |否   |boolean   |是否进行过美化 |
|lightStyleId   |否   |int   |灯光模板id|
|lightStyleName   |否   |string   |灯光模板名称 |
|favorite|否   |boolean   |是否是精选 |
