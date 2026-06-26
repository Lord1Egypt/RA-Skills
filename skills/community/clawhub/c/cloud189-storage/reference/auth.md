---
name: auth
description: 引导用户登录天翼云盘获取鉴权accessToken。当用户提到天翼云盘、Cloud189、获取云盘权限、需要云盘授权、登录天翼云盘、获取云盘访问令牌、需要云盘accessToken等关键词时，请使用此skill来帮助用户完成鉴权流程。即使没有明确提及天翼云盘，如果用户需要云盘文件操作或云盘API访问，也应该先触发此skill进行鉴权。
---

# 天翼云盘鉴权流程

本skill用于引导用户完成天翼云盘的OAuth2鉴权流程，获取accessToken用于后续的云盘API调用。

## 鉴权流程概述

天翼云盘使用OAuth2授权码模式，需要用户手动获取授权码，然后通过API交换获取accessToken。

## 步骤1：引导用户获取授权码

向用户提供以下指引：

```markdown
请按照以下步骤获取天翼云盘授权码：

1. 在浏览器中打开以下链接：
   https://cloud.189.cn/web/ecloud-auth/index.html

2. 使用您的天翼云盘账号登录

3. 登录成功后，页面会显示一个授权码（authCode），请复制这个授权码
```

等待用户确认已经获取到授权码。

## 步骤2：收集用户授权码

提示用户输入刚刚复制的授权码：

```markdown
请将您获取到的授权码粘贴到下面：
```

等待用户提供授权码。

## 步骤3：获取accessToken

使用用户提供的授权码调用天翼云盘API获取accessToken：

**API请求：**
- 方法：GET
- URL：`https://api.cloud.189.cn/open/oauth2/getAccessTokenByCloudCode?authCode={用户提供的授权码}`

**预期响应：**
```json
{
    "errCode": "0",
    "errMsg": "SUCCESS",
    "data": {
        "accessToken": "实际的accessToken字符串"
    }
}
```

**错误处理：**
- 如果 `errCode` 不为 "0"，显示错误信息：`{errMsg}`
- 常见错误码：
  - 非零值：授权码无效或已过期

## 步骤4：保存accessToken

成功获取到accessToken后，将其保存到用户的内存或配置文件中，以便后续的云盘API调用使用。

建议的保存方式：
- 将accessToken保存为环境变量或项目配置
- 告知用户accessToken已保存，可以用于后续的云盘操作

**重要提示：**
- accessToken具有有效期，过期后需要重新获取
- 建议用户妥善保管accessToken，不要泄露给他人

## 使用示例

获取到accessToken后，可以在后续的云盘API请求中作为鉴权参数使用，例如：

```
Authorization: Bearer {accessToken}
```

或在请求参数中：
```
?accessToken={accessToken}
```

## 用户提示模板

在流程中可以使用的中文提示：

- "正在为您启动天翼云盘鉴权流程..."
- "请打开浏览器访问上述链接，完成登录后复制授权码"
- "请粘贴您的授权码，我将继续为您获取accessToken"
- "鉴权成功！您的accessToken已保存，可以开始使用云盘功能了"
- "鉴权失败：{错误信息}，请检查授权码是否正确或是否已过期"
