---
name: searchFiles
description: 搜索天翼云盘文件。当用户需要在指定目录下搜索文件或文件夹时，请使用此技能。适用于需要按文件名搜索文件的场景。
---

# 搜索云盘文件功能指南

本技能帮助你在天翼云盘的指定目录下搜索文件或文件夹，并获取文件详细信息。

## 前提条件

- 你需要获取天翼云盘的用户accesstoken
- 需要使用支持查看网络请求的浏览器或工具（推荐 Chrome 浏览器的开发者工具）
- 需要先获取目标文件夹的ID（可通过queryFolder SKILL获取）

## 注意事项

- accesstoken 有一定的有效期，过期后需要重新登录获取
- 如果未找到 accesstoken，请引导用户重新登录获取
- fileName和folderId为必填参数
- recursive参数默认为0，表示只查询当前层级的文件；如果要递归查询子目录下的所有文件，需要传1
- 当fileName为空时，接口会返回指定条件下的所有文件和文件夹
- 接口支持分页，通过pageNum和pageSize参数控制
- 本技能只能在"我的应用/云盘智能体"目录下进行文件搜索。当搜索结果为空时，需要告知用户：在"我的应用/云盘智能体"目录下未找到匹配的文件，请确保文件存在于该目录中。

## 使用步骤

### 1. 用户已完成登录并拿到天翼云盘的 accesstoken
### 2. 获取目标文件夹ID：
   - 如果用户未指定文件夹，调用queryFolder SKILL获取默认目录ID（"我的应用/云盘智能体"）
   - 如果用户指定了文件夹路径或ID，使用指定的folderId
### 3. 询问用户关于搜索文件的相关信息：
   - 文件名（fileName），必须，要搜索的文件名或关键词
   - 文件夹ID（folderId），必须，搜索的目录ID
   - 是否递归查询（recursive），可选，传0或1，默认为0（只查询当前层级），传1表示递归查询子目录下的所有文件
### 4. 根据上述用户输入信息，将参数组装为JSON字符串，然后调用天翼云盘的统一Skill接口，完成搜索文件

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
| functionName | String | 必须 | 功能意图名称，固定为`searchFiles` |
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
| fileName | String | 必须 | 文件名，要搜索的文件名或关键词 |
| folderId | String | 必须 | 文件夹ID，搜索的目录ID |
| recursive | Integer | 可选 | 是否递归（1:是, 0:否），默认为0，传1表示递归查询子目录下的所有文件 |

## 响应数据说明

解析data字段后，可获取以下信息：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| folderList | Array | 文件夹列表 |
| folderList[0].folderId | String | 文件夹ID |
| folderList[0].folderName | String | 文件夹名称 |
| fileList | Array | 文件列表 |
| fileList[0].fileId | String | 文件ID |
| fileList[0].fileName | String | 文件名 |
| fileList[0].size | Long | 文件大小 |
| fileList[0].createDate | String | 创建时间 |
| fileList[0].lastOpTime | String | 最后操作时间 |
| count | Long | 总记录数 |

## 天翼云盘的SKILL统一接口调用示例

### 示例 1：递归搜索文件（包含子目录）

用户输入：`在文件夹id为-11下递归搜索包含"aaa"的所有文件，包括子目录中的文件`

接口参数：
```json
{
    "accessToken": "xxx",
    "functionName": "searchFiles",
    "functionData": "{\"folderId\": \"-11\", \"fileName\": \"aaa\"}"
}
```

响应结果：
```json
{
    "errCode": 0,
    "errMsg": "成功",
    "errTips": null,
    "data": "{\"res_code\": 0, \"res_message\": \"成功\",\"count\":3,\"fileList\":[],\"folderList\":[{\"createDate\":\"2025-11-28 15:57:47\",\"fileCata\":1,\"fileCount\":2,\"fileListSize\":0,\"id\":\"923931222660000792\",\"lastOpTime\":\"2025-12-01 10:08:04\",\"name\":\"aaa\",\"parentId\":\"323931222660000789\",\"rev\":\"20251201100804\",\"starLabel\":2},{\"createDate\":\"2025-11-28 15:53:37\",\"fileCata\":1,\"fileCount\":0,\"fileListSize\":0,\"id\":\"325001222597130536\",\"lastOpTime\":\"2025-11-28 15:53:37\",\"name\":\"aaa\",\"parentId\":-15,\"rev\":\"20251128155337\",\"starLabel\":2},{\"createDate\":\"2023-03-30 19:54:25\",\"fileCata\":1,\"fileCount\":3,\"fileListSize\":0,\"id\":\"92398158307573871\",\"lastOpTime\":\"2023-03-30 19:54:25\",\"name\":\"aaa\",\"parentId\":\"62412158307492859\",\"rev\":\"20230330195425\",\"starLabel\":2}]}\n"
}
```

## curl调用示例

```bash
curl --location --request POST 'https://api.cloud.189.cn/smart/server/api/open/cloud/skills' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'xkey: e87f4d25953fg' \
--data-raw '{
    "accessToken": "xxxx",
    "functionName": "searchFiles",
    "functionData": "{\"fileName\":\"文档\",\"folderId\":\"789012\",\"recursive\":1}"
}'
```

## 错误处理

| 错误码 | 错误信息 | 排查建议 |
|--------|----------|----------|
| 0 | 成功 | 操作成功 |
| PermissionDenied | 权限拒绝 | 当遇到此错误时，必须明确告知用户：本技能只能在"我的应用/云盘智能体"目录下进行文件查询，请确保查询的文件位于该目录下。 |