



## 描述 
查询酷家乐户型图库中的户型图，本接口会返回酷家乐户型的一些基本信息。
## API
```
GET https://oauth.kujiale.com/oauth2/openapi/ai-design-skill/floorplan/standard/search
Content-Type: text/plain;charset=utf-8
```
## 入参
### URL Query Param
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|access_token                                      |是| string              | 用户系统配置的令牌|
|start     |是   |int   |拉取列表的偏移量，从0开始。   |
|num       |是   |int   |一次拉取的数量上限，从数据安全以及性能上考虑，num最大值限制为50，如果有拉取更多数据的需求，请发起多次请求。<br/>如果剩余数据量小于num，则会返回全部剩余数据。<br/>比如start=0&num=10表示拉取第1到第10个数据，start=10&num=10表示拉取第11个到第20个数据。   |
|query     |是   |string |查询关键字。 此处需要注意，如果用户输入的为中文，则需要进行额外的UTF-8编码以后再进行请求 |
|area_id    |是   |long   |区域id(国省市区最低级的一个)，全部地区信息见：[点击获取ID附件](//qhstaticssl.kujiale.com/application/json/1747202252338/61C6FC156D73E4E58178DEEF5590076D.json "点击获取ID附件")|
|room_count |否   |int   |卧室数量筛选条件。比如3表示筛选所有前置条件下的三室的户型。目前只支持取值为1、2、3、4、5。   |
|min_area  |否   |long   |建筑面积筛选条件，指定这个参数表示要过滤建筑面积最小为这个值的户型。   |
|max_area  |否   |long   |建筑面积筛选条件，指定这个参数表示要过滤建筑面积最大为这个值的户型。  |
|is_standard |否   |boolean   |是否只查询标准户型数据，不传或者传false会保持和原来一样的返回，传true只会返回标准户型库的户型。  |
|search_type |否|int| 搜索场景(目前支持取值：1（家居云设计4.0）和2（家居云设计5.0+4.0)|
## 响应
### 数据结构
```json
{
  "c": "0",
  "m": "",
  "d": {
    "floorPlans": [
      {
        "planId": "3FO4K6M6OUHP",
        "commName": "申花壹号院",
        "name": "申花壹号院88.00㎡A户型3室2厅2卫",
        "srcArea": 88,
        "area": 79.47,
        "planPic": "https://qhyxpicoss.kujiale.com/fpimg/2015/02/04/VNIW5kN2RXRe_wBBAAAA_800x800.jpg",
		"bedRoomNum": 3,
        "livingRoomNum": 1,
        "batchRoomNum": 2,
        "cookRoomNum": 1,
        "areaId": 2140,
        "province": "浙江",
        "city": "杭州",
        "district": "拱墅",
        "created": 1548300986000,
        "lastModified": 1548259200000
      },
      {
        "planId": "3FO4IQRTWEHD",
        "commName": "코오롱",
        "name": "코오롱",
        "srcArea": 88.23,
        "area": 70.59,
        "planPic": "https://qhtbdoss.kujiale.com/fpimgnew/i/3FO4IQRTWEHD/l/L2KUXMVMDRIAGAABAAAAAAY8.jpg",
        "areaId": 157771,
        "province": "인천광역시",
        "city": "계양구",
        "district": "봉오대로691번길",
        "created": 1586842549000,
        "lastModified": 1586853515000
      },
      {
        "planId": "3FO4IQRU993W",
        "name": "푸른솔_106㎡",
        "srcArea": 68.36,
        "area": 54.68,
        "planPic": "https://qhtbdoss.kujiale.com/fpimgnew/i/3FO4IQRU993W/l/L2KUZBFMDRIAGAABAAAAADI8.jpg",
        "areaId": 153714,
        "province": "경기도",
        "city": "구리시",
        "district": "이문안로155번길",
        "created": 1586842765000,
        "lastModified": 1588139286000
      }
    ],
    "totalCount": 3616
  }
}
```
### 字段说明
|参数|是否必须|参数类型|参数说明|
| ------------ | :------------: | :------------: | ------------ |
|planId   |是   |string   |酷家乐户型图的ID，用来唯一标识一个户型图。   |
|commName |是   |string   |户型所在的小区名字。   |
|name    |是   |string   |户型名。   |
|srcArea |是   |double   |户型的建筑面积，单位为平方米。   |
|area    |是   |double   |户型的套内面积。   |
|planPic |是   |string   |户型图的URL。   |
|bedRoomNum|否   |long   |几室。   |
|livingRoomNum|否   |long   |几厅。  |
|batchRoomNum|否   |long |几卫。   |
|cookRoomNum|否   |long |几厨。   |
|areaId |是   |long   |户型所在区域的id(cityId或districtId)。   |
|province|是   |string   |省份名称。   |
|city|是   |string   |城市名称。   |
|district|否   |string |地区名称。   |
|created|是   |long |创建时间(东八区时间,UTC+8，单位为毫秒)。   |
|lastModified|是 |long |最后更新时间(东八区时间,UTC+8，单位为毫秒)。   |
|totalCount |是   |long   |总行数。   |
