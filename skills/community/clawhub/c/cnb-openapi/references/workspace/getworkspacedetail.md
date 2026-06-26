# GetWorkspaceDetail

## 原始 Swagger
https://api.cnb.cool/#/operations/GetWorkspaceDetail

## 接口描述
根据流水线sn查询云原生开发访问地址。Query cloud-native development access address by pipeline SN.
## 接口权限
repo-cnb-detail:r
## 请求信息

**请求方法：** GET

**请求地址：** ${CNB_API_ENDPOINT}/{repo}/-/workspace/detail/{sn}

### 请求头

| 请求头 | 值 | 必填 | 描述 |
|--------|----|----|------|
| Accept | application/vnd.cnb.api+json | 是 | 指定接受的响应格式 |
| Authorization | Bearer $CNB_TOKEN | 是 | 身份认证令牌 |


### 路径参数

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| repo | 字符串 | 是 | Repo path|
| sn | 字符串 | 是 | SN|
## 响应信息


**响应类型：** dto.WorkspaceDetailResult

**响应结构：**
```json
{
  "codebuddy": "string", // CodeBuddy 国际版客户端 remote-ssh 访问 schema 地址
  "codebuddycn": "string", // CodeBuddy 国内版客户端 remote-ssh 访问 schema 地址
  "cursor": "string", // Cursor 客户端 remote-ssh 访问 schema 地址
  "jetbrains": {}, // jetbrains 系列 ide 的 jetbrains gateway 访问 schema 地址，环境内有安装 JetBrains 系列 ide 才会有
  "jumpUrl": "string", // 选择入口页面 url
  "remoteSsh": "string", // remote-ssh 连接地址
  "ssh": "string", // ssh 登录命令
  "vscode": "string", // VSCode 客户端 remote-ssh 访问 schema 地址
  "vscode-insiders": "string", // Vscode 预览版客户端 remote-ssh 访问 schema 地址
  "webide": "string" // WebIDE 访问 url
}
```
## 请求示例

### cURL 示例

```bash
curl -X GET \
  "${CNB_API_ENDPOINT}/{repo}/-/workspace/detail/{sn}" \
  -H "Accept: application/vnd.cnb.api+json" \
  -H "Authorization: Bearer $CNB_TOKEN" \
```
