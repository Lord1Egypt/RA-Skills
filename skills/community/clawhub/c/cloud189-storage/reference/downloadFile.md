---
name: downloadFile
description: 下载天翼云盘文件。当用户需要下载云盘中的文件时，请使用此技能。适用于需要获取文件下载链接的场景。
---

# 云盘文件下载功能指南

本技能帮助你获取天翼云盘文件的下载链接，并下载文件到本地。

## 前提条件

- 你需要获取天翼云盘的用户accesstoken
- 需要使用支持查看网络请求的浏览器或工具（推荐 Chrome 浏览器的开发者工具）
- 需要先确定要下载的文件，获取文件ID或文件路径

## 注意事项

- accesstoken 有一定的有效期，过期后需要重新登录获取
- 如果未找到 accesstoken，请引导用户重新登录获取
- fileId和filePath二选一，至少提供一个,可以先看看前面结果里面是否已经包含了fileId或filePath
- 如果用户没有fileId或filePath，则可以通过其他SKILL（如searchFiles、listFiles）获取
- 下载链接可能有时效性，建议及时下载
- 需要确保用户有权限访问该文件

## 使用步骤

### 1. 用户已完成登录并拿到天翼云盘的 accesstoken
### 2. 确定要下载的文件：
   - 如果用户已经知道fileId，直接使用
   - 如果用户不知道，需要先通过以下方式获取：
     - 使用searchFiles SKILL搜索文件，获取fileId
     - 使用listFiles SKILL列出文件列表，获取fileId
     - 使用queryFolder SKILL查询目录，结合文件名获取filePath
### 3. 调用获取文件信息接口：
   - 使用fileId调用接口获取文件信息
   - 从响应中提取fileDownloadUrl（文件下载地址）
### 4. 使用下载地址下载文件：
   - 将fileDownloadUrl提供给用户
   - 用户可以通过浏览器或其他下载工具下载文件

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
| functionName | String | 必须 | 功能意图名称，固定为`getFileInfo` |
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
| fileId | Long | 可选 | 文件ID |


## 响应数据说明

解析data字段后，可获取以下信息：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| fileId | Long | 文件ID |
| fileName | String | 文件名 |
| filePath | String | 文件路径 |
| fileSize | Long | 文件大小（字节） |
| fileType | Integer | 文件类型 |
| mediaType | Integer | 媒体类型 |
| lastOpTime | Date | 最后操作时间 |
| parentId | Long | 父文件夹ID |
| starLabel | Long | 是否星标：1-是，0-否 |
| fileDownloadUrl | String | **文件下载地址**（核心字段） |
| shootTime | String | 图片拍摄时间 |
| parentFolderListAO | Object | 父文件夹列表 |

## 天翼云盘的SKILL统一接口调用示例

### 示例 1：使用fileId下载文件

用户输入：`下载文件ID为123456的文件`

接口参数：
```json
{
    "accessToken": "xxx",
    "functionName": "getFileInfo",
    "functionData": "{\"fileId\": \"42535120948116167\"}"
}
```

响应结果：
```json
{
    "errCode": 0,
    "errMsg": "成功",
    "errTips": null,
    "data": "{\"res_code\": 0, \"res_message\": \"成功\",\"createDate\":\"2024-01-10 17:01:12\",\"fileDownloadUrl\":\"https://download.cloud.189.cn/file/downloadFile.action?dt=51&expired=1775110594873&sk=1312ed3b-03a9-479a-bd42-d02c8d821e3c_app&ufi=423071110947043520&zyc=5&token=cloud3&sig=CvUxWvckzOgNjnSHnJsayHuGLIw%3D\",\"filePath\":\"/AI/AI 大模型应用开发实战营/README.txt\",\"id\":\"423071110947043520\",\"lastOpTime\":1704877272000,\"lastOpTimeStr\":\"2024-01-10 17:01:12\",\"md5\":\"C3C7F5D50844FBDA3EFCBE7A53B2A9A3\",\"mediaType\":4,\"name\":\"README.txt\",\"parentId\":\"824901110916781980\",\"rev\":1704877272000,\"size\":136}\n"
}
```

## curl调用示例

```bash
curl --location --request POST 'https://api.cloud.189.cn/smart/server/api/open/cloud/skills' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'xkey: e87f4d25953fg' \
--data-raw '{
    "accessToken": "xxxx",
    "functionName": "getFileInfo",
    "functionData": "{\"fileId\":123456}"
}'
```

## 错误处理

| 错误码 | 错误信息 | 排查建议 |
|--------|----------|----------|
| 0 | 成功 | 操作成功 |
| PermissionDenied | 权限拒绝 | 当遇到此错误时，必须明确告知用户：本技能只能在"我的应用/云盘智能体"目录下进行文件下载，请确保您查询的文件位于该目录下。 |
