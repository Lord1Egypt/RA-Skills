---
name: getFolderInfo
description: 获取默认目录id，或者查询天翼云盘目录并获取文件夹ID时使用，支持通过路径或ID查询，为空时获取默认文件夹。
---

# 查询目录

## 功能说明

本功能用于查询天翼云盘目录信息并获取文件夹ID，支持通过文件夹路径或文件夹ID进行查询。当用户未提供路径时，会自动获取默认文件夹"我的应用/云盘智能体"。

## 前提条件

- 用户已登录天翼云盘并获取了有效的鉴权Token
- 了解需要查询的文件夹路径或ID

## 注意事项

- 用户只能在默认文件夹"我的应用/云盘智能体"下查询目录
- 当提供的路径不以"我的应用/云盘智能体"开头时，系统会自动拼接完整路径
- 如果folderId和folderPath都为空，会尝试获取默认文件夹

## 使用步骤

1. **登录天翼云盘**：获取有效的鉴权Token
2. **准备查询参数**：
   - 提供文件夹路径（folderPath）或文件夹ID（folderId）
   - 路径为空时，系统会获取默认文件夹
3. **调用查询接口**：通过统一Skill接口发送请求
4. **获取结果**：查询成功后，获取文件夹ID和其他详细信息

## 统一接口调用规范

### 接口地址
```
https://api.cloud.189.cn/smart/server/api/open/cloud/skills
```

### 请求方式
- POST

### 请求头参数

| 字段名 | 类型 | 是否必须 | 描述 |
|--------|------|---------|------|
| Content-Type | String | 必须 | 固定值：application/json;charset=UTF-8 |
| xkey | String | 必须 | 固定值：e87f4d25953fg，为天翼云盘技能统一标识 |

### 请求参数

| 字段名 | 类型 | 是否必须 | 描述 |
|--------|------|---------|------|
| accessToken | String | 必须 | 用户的天翼云盘鉴权Token |
| functionName | String | 必须 | 功能意图名称，固定为`getFolderInfo` |
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

| 字段名 | 类型 | 是否必须 | 描述 | 示例值 |
|--------|------|---------|------|--------|
| folderId | Long | 可选 | 文件夹ID | 123456 |
| folderPath | String | 可选 | 文件夹路径 | 我的应用/云盘智能体/目录1 |

**注意**：folderId或folderPath至少有一个必须非空；如果都存在，folderId参数有效。

## 调用示例

### 示例1：通过路径查询目录

#### 请求示例
```json
{
    "accessToken": "xxx",
    "functionName": "getFolderInfo",
    "functionData": "{\"folderPath\":\"我的应用/云盘智能体/测试目录\"}"
}
```

#### 响应示例
```json
{
    "errCode": 0,
    "errMsg": "",
    "errTips": "",
    "data": "{\"fileId\":123456,\"fileName\":\"测试目录\",\"filePath\":\"我的应用/云盘智能体/测试目录\",\"createTime\":\"2023-07-01 12:00:00\",\"lastOpTime\":\"2023-07-01 12:00:00\",\"parentId\":789012}"
}
```

### 示例2：获取默认文件夹

#### 请求示例
```json
{
    "accessToken": "xxx",
    "functionName": "getFolderInfo",
    "functionData": "{}"
}
```

#### 响应示例
```json
{
    "errCode": 0,
    "errMsg": "",
    "errTips": "",
    "data": "{\"fileId\":999999,\"fileName\":\"云盘智能体\",\"filePath\":\"我的应用/云盘智能体\",\"createTime\":\"2023-01-01 00:00:00\",\"lastOpTime\":\"2023-01-01 00:00:00\",\"parentId\":888888}"
}
```

### curl命令示例
```bash
curl -X POST "https://api.cloud.189.cn/smart/server/api/open/cloud/skills" \
  -H "Content-Type: application/json;charset=UTF-8" \
  -H "xkey: e87f4d25953fg" \
  -d '{"accessToken": "xxx", "functionName": "getFolderInfo", "functionData": "{\"folderPath\":\"我的应用/云盘智能体/测试目录\"}"}'
```

## 错误处理

| 错误码 | 错误信息 | 排查建议 |
|--------|----------|----------|
| 0 | 成功 | 操作成功 |
| PermissionDenied | 权限拒绝 | 当遇到此错误时，必须明确告知用户：本技能只能在"我的应用/云盘智能体"目录下进行目录查询，请确保查询的目录位于该目录下。 |
