---
name: listFiles
description: 查询天翼云盘目录下文件列表。当用户需要查看指定文件夹中的文件和子文件夹时，请使用此技能。适用于需要获取文件列表信息的场景。
---

# 查询目录下文件列表功能指南

本技能帮助你查询天翼云盘指定目录下的文件和文件夹列表，并获取文件详细信息。

## 前提条件

- 你需要获取天翼云盘的用户accesstoken
- 需要使用支持查看网络请求的浏览器或工具（推荐 Chrome 浏览器的开发者工具）
- 需要先获取目标文件夹的ID（可通过queryFolder或createFolder SKILL获取）

## 注意事项

- accesstoken 有一定的有效期，过期后需要重新登录获取
- 如果未找到 accesstoken，请引导用户重新登录获取
- folderId为必填参数，需要先通过其他SKILL获取
- 递归查询仅支持PC端同步盘，其他客户端不支持
- 默认每页返回200条记录，最大支持1000条
- 本技能只能在"我的应用/云盘智能体"目录下进行文件查询，如果用户尝试查询其他目录的文件，会返回权限错误。当遇到权限错误时，必须明确告知用户只能在"我的应用/云盘智能体"目录下查询文件
- 如果用户查询的文件夹下没有文件，会返回空列表。需要告知用户：在"我的应用/云盘智能体"目录下没有文件。

## 使用步骤

### 1. 用户已完成登录并拿到天翼云盘的 accesstoken
### 2. 获取目标文件夹ID：
   - 如果用户提供了相对路径和文件夹名称，先调用queryFolder SKILL获取文件夹ID
   - 如果用户直接提供了文件夹ID，则直接使用
### 3. 询问用户关于查询文件列表的相关信息：
   - 文件夹ID（folderId），必须，目标文件夹的ID
   - 是否递归查询（recursive），可选，传0或1，默认为0（不递归）
### 4. 根据上述用户输入信息，将参数组装为JSON字符串，然后调用天翼云盘的统一Skill接口，完成查询文件列表

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
| functionName | String | 必须 | 功能意图名称，固定为`listFiles` |
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
| folderId | String | 必须 | 文件夹ID |
| recursive | String | 可选 | 是否递归获取（仅PC端同步盘支持），传0或1，默认为0 |

## 响应数据说明

解析data字段后，可获取以下信息：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| fileListAO.fileList | Array | 文件列表 |
| fileListAO.fileList[0].id | Long | 文件ID |
| fileListAO.fileList[0].name | String | 文件名 |
| fileListAO.fileList[0].size | Long | 文件大小 |
| fileListAO.fileList[0].createDate | String | 创建时间 |
| fileListAO.fileList[0].lastOpTime | String | 最后操作时间 |
| fileListAO.folderList | Array | 文件夹列表 |
| fileListAO.folderList[0].id | Long | 文件夹ID |
| fileListAO.folderList[0].name | String | 文件夹名称 |
| fileListAO.count | Long | 总记录数 |
| lastRev | Long | 最后操作版本号 |

## 天翼云盘的SKILL统一接口调用示例

### 示例 1：查询指定文件夹下的所有文件和文件夹

用户输入：`查看文件夹id为824901110916781980下的所有文件和文件夹`

接口参数：
```json
{
    "accessToken": "xxx",
    "functionName": "listFiles",
    "functionData": "{\"folderId\": \"824901110916781980\"}"
}
```

响应结果：
```json
{
    "errCode": 0,
    "errMsg": "成功",
    "errTips": null,
    "data": "{\"res_code\": 0, \"res_message\": \"成功\",\"fileListAO\":{\"count\":18,\"fileList\":[{\"createDate\":\"2024-01-10 17:01:12\",\"fileCata\":1,\"id\":\"423071110947043520\",\"lastOpTime\":\"2024-01-10 17:01:12\",\"md5\":\"C3C7F5D50844FBDA3EFCBE7A53B2A9A3\",\"mediaType\":4,\"name\":\"README.txt\",\"rev\":\"20240110170112\",\"size\":136,\"starLabel\":2}],\"fileListSize\":1,\"folderList\":[{\"createDate\":\"2024-01-10 17:01:11\",\"fileCata\":1,\"fileCount\":2,\"fileListSize\":0,\"id\":\"124901110916782145\",\"lastOpTime\":\"2024-01-10 17:01:11\",\"name\":\"0712-大模型基础：初探大模型-起源与发展\",\"parentId\":\"824901110916781980\",\"rev\":\"20240110170111\",\"starLabel\":2},{\"createDate\":\"2024-01-10 17:01:10\",\"fileCata\":1,\"fileCount\":2,\"fileListSize\":0,\"id\":\"424901110916782136\",\"lastOpTime\":\"2024-01-10 17:01:11\",\"name\":\"0716-大模型基础：GPT模型家族&提示学习\",\"parentId\":\"824901110916781980\",\"rev\":\"20240110170111\",\"starLabel\":2},{\"createDate\":\"2024-01-10 17:01:10\",\"fileCata\":1,\"fileCount\":2,\"fileListSize\":0,\"id\":\"124901110916782109\",\"lastOpTime\":\"2024-01-10 17:01:10\",\"name\":\"0726-大模型应用最佳实践\",\"parentId\":\"824901110916781980\",\"rev\":\"20240110170110\",\"starLabel\":2}],\"lastRev\":20260402142423}"
}
```

### 示例 2：分页查询文件列表

用户输入：`查看文件夹789012下的文件，每页显示10条，查看第2页`

接口参数：
```json
{
    "accessToken": "xxxx",
    "functionName": "listFiles",
    "functionData": "{\"folderId\":\"789012\",\"pageNum\":2,\"pageSize\":10}"
}
```

响应结果：
```json
{
    "errCode": 0,
    "errMsg": "",
    "errTips": "",
    "data": "{\"fileListAO\": {\"fileList\": [{\"id\": 123466, \"name\": \"文档11.pdf\"}], \"folderList\": [], \"count\": 25}, \"lastRev\": 1620000000000}"
}
```

### 示例 3：递归查询文件列表（仅PC端同步盘支持）

用户输入：`递归查看文件夹789012下的所有文件`

接口参数：
```json
{
    "accessToken": "xxxx",
    "functionName": "listFiles",
    "functionData": "{\"folderId\":\"789012\",\"recursive\":\"1\"}"
}
```

响应结果：
```json
{
    "errCode": 0,
    "errMsg": "",
    "errTips": "",
    "data": "{\"fileListAO\": {\"fileList\": [{\"id\": 123456, \"name\": \"文档1.pdf\"}, {\"id\": 123457, \"name\": \"子文件夹/文档2.pdf\"}], \"folderList\": [{\"id\": 789013, \"name\": \"子文件夹\"}], \"count\": 3}, \"lastRev\": 1620000000000}"
}
```

## curl调用示例

```bash
curl --location --request POST 'https://api.cloud.189.cn/smart/server/api/open/cloud/skills' \
--header 'Content-Type: application/json;charset=UTF-8' \
--header 'xkey: e87f4d25953fg' \
--data-raw '{
    "accessToken": "xxxx",
    "functionName": "listFiles",
    "functionData": "{\"folderId\":\"789012\"}"
}'
```

## 错误处理

| 错误码 | 错误信息 | 排查建议 |
|--------|----------|----------|
| 0 | 成功 | 操作成功 |
| PermissionDenied | 权限拒绝 | 当遇到此错误时，必须明确告知用户：本技能只能在"我的应用/云盘智能体"目录下进行文件查询，请确保查询的文件夹位于该目录下。 |