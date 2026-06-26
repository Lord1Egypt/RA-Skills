---
name: searchImages
description: 引导用户使用天翼云盘的智能图片搜索功能。当用户需要搜索天翼云盘的图片时，请使用此技能。适用于需要调用天翼云盘智能搜索接口的场景。
---

# 智能图片搜索功能指南

本技能帮助你使用天翼云盘的智能图片搜索功能。

## 前提条件

- 你需要获取天翼云盘的用户accesstoken
- 需要使用支持查看网络请求的浏览器或工具（推荐 Chrome 浏览器的开发者工具）

## 注意事项

- accesstoken 有一定的有效期，过期后需要重新登录获取
- 如果未找到 accesstoken，请引导用户重新登录获取

## 使用步骤

### 1. 用户已完成登录并拿到天翼云盘的 accesstoken
### 2. 询问用户关于智能图片搜索的相关信息：
   - 搜索图片的语句（text），必选
   - 当前页（pageNum），可选，默认值为1
   - 每页数量（pageSize），可选，默认值为10
   - 搜索类型（searchType），值指定为1不允许修改
### 3. 根据上述用户输入信息，将参数组装为JSON字符串，然后调用天翼云盘的统一Skill接口，完成智能图片搜索
### 4. 如果用户需要展示图片，在响应体的icon字段中有缩略图URL，可以直接展示给用户

## 天翼云盘的SKILL统一接口调用规范

- 接口地址： `https://api.cloud.189.cn/smart/server/api/open/cloud/skills`
- 请求方式：POST
- 请求Content-Type：application/json;charset=UTF-8
- 响应Content-Type：application/json
- 字符编码：UTF-8

### 请求头参数

| 字段名 | 类型 | 是否必须 | 描述 |
|--------|------|---------|------|
| Content-Type | String | 必须 | 固定值：application/json;charset=UTF-8 |
| xkey | String | 必须 | 固定值：e87f4d25953fg，为天翼云盘技能统一标识 |

### 请求参数

| 字段名 | 类型 | 是否必须 | 描述 |
|--------|------|------|------|
| accessToken | String | 必须 | 用户的天翼云盘鉴权Token |
| functionName | String | 必须 | 功能意图名称，固定为`searchByText` |
| functionData | String | 必须 | 原本开放接口的传参，需要JSON字符串格式 |

### 响应参数

| 字段名 | 类型 | 描述 |
|--------|------|------|
| errCode | Integer | 错误码，0表示成功 |
| errMsg | String | 错误信息 |
| errTips | String | 错误提示 |
| data | String | 原本开放接口的响应体（JSON字符串格式） |

说明：响应体中的data字段才是原本开放接口的响应体，需要解析该JSON字符串获取实际结果。

## functionData参数说明

functionData字段需要传入原本开放接口的参数，格式为JSON字符串：

| 字段名 | 类型 | 是否必须 | 描述 |
|--------|------|------|------|
| text | String | 必须 | 搜索图片的关键词 |
| pageNum | Integer | 可选 | 当前页，默认值为1 |
| pageSize | Integer | 可选 | 每页数量，默认值为10 |
| searchType | Integer | 可选 搜索类型，固定为1 |

## 天翼云盘的SKILL统一接口调用示例

### 示例 1：智能图片搜索-纯语义查询

用户输入：`搜索包含风景的图片`

接口参数：
```json
{
    "accessToken": "xxx",
    "functionName": "searchByText",
    "functionData": "{\"text\":\"船\"}"
}
```

响应结果：
```json
{
    "errCode": 0,
    "errMsg": "成功",
    "errTips": null,
    "data": "{\"code\":\"0\",\"msg\":\"SUCCESS\",\"data\":{\"cloudBaseFile\":[{\"userFileId\":\"924501226096717818\",\"userId\":\"300001556256633\",\"fileName\":\"wx20251222093605.jpg\",\"lowerFileNameMd5\":\"6F715D54A750E0D6C7BCB18475B705E0\",\"parentId\":\"424241226031384139\",\"md5\":\"AAAACD679779D41B9AF86E2B2023B426\",\"fileSize\":7111634,\"createTime\":\"2025-12-22 09:36:13\",\"modifyTime\":\"2025-12-22 09:36:13\",\"icon\":{\"smallUrl\":\"https://preview.cloud.189.cn/image/imageAction?param=7C5B0D0010B11D80628189042C71528306654B5A9D3355A02FB21D2BE53214E1EC9E2627D4B75182551BDE74BB987FCF519448C7B6EA9D3B38DAC0B4D74E1F62C6E4988C02EA02E24D41182FB5E33E7ABD3562F144B175928E7E820CD228AC954D8D375ED2D2AF4839B6FAE9859F970B75AE2ADC\",\"mediumUrl\":null,\"largeUrl\":\"https://preview.cloud.189.cn/image/imageAction?param=769895277FCE777850A9F9F02A52280BEC88107637DFBCFECF41FD1A01B33824420342F2407091EE5EEA323117EE22024CE838F50CE16D921C5134F73AB0234822B6662FAF769A8FFBEF0A6CB9A4F02F9789A5C86BE2BC373F003AD38B9AF328A933AD29601FF85E50B2BCEA9176D52BC9179B4E\",\"max600\":null},\"distance\":0.0691},{\"userFileId\":\"224851226095996591\",\"userId\":\"300001556256633\",\"fileName\":\"wx20251222092957_2.jpg\",\"lowerFileNameMd5\":\"BD2622BE75AA68C960CA7CA8F62065FA\",\"parentId\":\"424241226031384139\",\"md5\":\"FD52D55F7539DDEF2B258232C81A7B05\",\"fileSize\":7074924,\"createTime\":\"2025-12-22 09:30:04\",\"modifyTime\":\"2025-12-22 09:30:04\",\"icon\":{\"smallUrl\":\"https://preview.cloud.189.cn/image/imageAction?param=B8B6AF7E89BC4066DB5A3BE8C90EB3049C537CA8159B9703CBDAA0BF9779390EC7635D9BA63C3483133E62DC0B5DF13CC514FB6FE1E831FA0BBC1CABCFB9E7FA7986AC18C5A5AF23EE94DCBF7E4B07ACC739FE9462552E37D84DF1B8626109D4634251A8847E05B2A4CA9EC13A0E3C8614D8884A\",\"mediumUrl\":null,\"largeUrl\":\"https://preview.cloud.189.cn/image/imageAction?param=077BA47A8F7ABD0096478FC5555ED3F5EEE8DA65142B3D4AEAD816C845ED9C029E0A1CB8B9F4FF618407B73F1586D2CB6BBB29E525A8A38D7B680CF47FFBE627F51FC53224A157D06F1684815424D0911C84F4220328E43E135B689B1186176F49EAE310F3E2285C3481B3BBFCB8BB2733E6BB97\",\"max600\":null},\"distance\":0.0673}],\"familyBaseFile\":[],\"remainValue\":49}}"
}
```

## curl调用示例

```bash
curl --location --request POST 'https://api.cloud.189.cn/smart/server/api/open/cloud/skills' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'xkey: e87f4d25953fg' \
--data-raw '{
    "accessToken": "xxxx",
    "functionName": "searchByText",
    "functionData": "{\"text\":\"风景\"}"
}'
```

## 错误处理

| 错误码 | 错误信息 | 错误描述 | 排查建议 |
|--------|----------|----------|----------|
| 0 | 成功 | 操作成功 | - |
| 400 | UserNotReady | 搜图未开通 | 提醒用户在天翼云盘客户端开通智能搜图功能 |
| 400 | Pendding | 用户图片还未解析完成 | 提醒用户"图片还未解析完成，稍后重试。" |
