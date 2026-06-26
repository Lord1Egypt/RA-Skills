---
name: douyin-posting
description: >
  协助用户将本地或用户提供的视频发布到抖音账号。包含上传流程说明、开放平台 API 使用指引及发布前检查。Use when: 用户要发抖音、上传视频到抖音、把视频发到抖音、post to Douyin、抖音发布。NOT for: 抖音视频下载、抖音数据分析、非发布类抖音操作。
---

# douyin posting Skill 使用指南

# 抖音视频发布

## 何时使用

- 用户说「帮我把这个视频发到抖音」「上传到抖音」「发抖音」
- 用户提供视频文件并希望发布到抖音
- 用户询问如何用代码/脚本把视频发到抖音
- 用户说「这是抖音 openId / accessToken，配置上去」或「记录下来」「保存一下」
- 用户问「怎么获取 openId / accessToken」「如何授权」「怎么拿到 token」等

## 配置并记录 openId、accessToken

**当用户提供 openId 和 accessToken 并要求「配置上去」或「记录下来」时：**

1. 将用户提供的 **openId** 和 **accessToken** 写入项目根目录的 **`.env`** 文件。
2. 格式为（不要有多余引号或空格）：
   ```
   DOUYIN_OPEN_ID=用户提供的openId
   DOUYIN_ACCESS_TOKEN=用户提供的accessToken
   ```
3. 若 `.env` 已存在，则只更新上述两个变量，保留其它变量不变。
4. 告知用户：「已把 openId 和 accessToken 写入项目下的 .env，会一直保留，之后发抖音会优先用这份配置。」

项目中的 `index.js` 会自动读取 `.env`，无需用户再手动设置环境变量。

## 使用前必须检查

**在协助发布（尤其是调用 API/脚本）之前，必须先确认用户是否具备：**

- **openId**：用户唯一标识（通过抖音开放平台 OAuth 获取）
- **accessToken**：用户授权 access_token（同上）

若用户尚未提供或未获取这两项，应**先引导用户**按下面「如何获取 openId 与 accessToken」完成授权；若用户表示要「配置上去」「记录下来」，则按上节「配置并记录 openId、accessToken」写入 `.env`，不要直接执行上传/发布代码。

## 如何获取 openId 与 accessToken（直接引导）

**当用户没有 openId/accessToken 且需要发抖音时，按以下步骤引导用户完成授权并拿到凭证。可逐条回复或给出链接与命令。**

### 第一步：创建应用并配置（若尚未有）

1. 打开 [抖音开放平台](https://partner.open-douyin.com/) 并登录。
2. 进入「管理中心」→「应用管理」→「创建应用」，选择「移动应用」或「网站应用」等（根据实际类型）。
3. 在应用详情里找到 **client_key**（应用唯一标识）和 **client_secret**（密钥），后续要用。
4. 在应用里配置 **重定向地址 redirect_uri**：必须是 **HTTPS** 的完整 URL（不支持 http、localhost）。若本地开发，可用 [ngrok](https://ngrok.com/)、[cpolar](https://www.cpolar.com/) 等把本机端口映射为 https 地址，并把该地址填到开放平台「重定向地址」中。
5. 申请发布视频能力：在「能力管理」→「能力实验室」中申请「**代替用户发布内容到抖音**」，审核通过后才有发布权限。授权时需勾选对应 scope（见下）。

### 第二步：让用户打开授权页拿到 code

6. 拼出授权 URL（把下面参数换成用户自己的值）：
   ```
   https://open.douyin.com/platform/oauth/connect/?client_key=你的client_key&response_type=code&scope=user_info,video.create&redirect_uri=你的redirect_uri的URL编码&state=任意字符串
   ```
   - `scope` 至少包含 `user_info,video.create`（发布视频需要）。
   - `redirect_uri` 必须与开放平台里配置的完全一致，若含特殊字符需做 URL 编码。
7. 让用户用浏览器打开该 URL，扫码或登录抖音并同意授权。
8. 授权成功后页面会跳转到 `redirect_uri?code=xxx&state=xxx`，从地址栏或回调页拿到 **code**（code 约 10 分钟有效，且只能用一次）。

### 第三步：用 code 换 openId 和 accessToken

9. 调用接口用 code 换 token：
   - 接口：`POST https://open.douyin.com/oauth/access_token/`
   - Content-Type：`application/x-www-form-urlencoded`
   - Body 参数：`client_key`、`client_secret`、`code`、`grant_type=authorization_code`
10. 响应里会包含 **open_id**、**access_token**、**refresh_token**、**expires_in**（access_token 约 15 天有效）。把 **open_id** 和 **access_token** 给用户，或按用户要求写入项目 `.env`（见上节「配置并记录 openId、accessToken」）。

**项目内已提供脚本**：用户若已配置好 `.env` 中的 `DOUYIN_CLIENT_KEY`、`DOUYIN_CLIENT_SECRET`、`REDIRECT_URI`，拿到 code 后可在项目根目录执行：
```bash
node scripts/get-douyin-token.js <用户拿到的code>
```
脚本会输出 open_id 和 access_token，并询问是否写入 `.env`，从而完成「直接引导」获取并记录凭证。

### 官方文档链接（可发给用户）

- [抖音获取授权码](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/douyin-get-permission-code)
- [获取 access_token](https://developer.open-douyin.com/docs/resource/zh-CN/dop/develop/openapi/account-permission/get-access-token)

## 核心流程

1. **确认 openId 与 accessToken**（见上「使用前必须检查」）
2. **确认素材**
   - 视频文件路径或用户已提供的视频
   - 标题、话题、封面（可选）、可见范围等发布参数

3. **发布方式二选一**
   - **手动发布**：引导用户使用抖音/抖音创作者中心网页或 App，按步骤上传并填写标题、话题等。
   - **开放平台发布**：若用户需要自动化，指引使用抖音开放平台（创作服务平台）的「发布视频」相关 API；需先完成企业/个人开发者认证与授权。

4. **发布前检查**
   - 视频格式与时长符合抖音规范（常见：MP4，建议时长与尺寸参考当前平台规则）
   - 标题、话题无违规词
   - 若用 API，确认已获取有效 access_token 及发布权限

## 开放平台 API 要点

- 抖音创作服务平台/开放平台提供「发布视频」类 API，需 OAuth 授权。
- 典型步骤：获取用户授权 → 换取 access_token → 调用上传接口（先上传视频文件得到 video_id，再调用发布接口传入 video_id 与标题、封面等）。
- 具体 endpoint、参数以官方文档为准；回复用户时给出文档链接与关键参数说明，不编造 API 路径。

## 回复原则

- 用户仅问「怎么发抖音」：优先给出**手动发布**的简短步骤（App/网页入口 + 上传、填标题、选话题、发布）。
- 用户明确要**自动化/脚本/API**：说明需用开放平台，并列出步骤（认证、授权、上传接口、发布接口），可写示例调用流程（伪代码或示例请求），并提醒查阅最新官方文档。
- **若用户没有 openId 或 accessToken**：按本 Skill 中「如何获取 openId 与 accessToken（直接引导）」逐步引导（创建应用、配置 redirect_uri、拼授权链接、用户扫码拿 code、用 code 换 token）；必要时可代用户拼好授权 URL 或说明运行 `node scripts/get-douyin-token.js <code> --write` 完成换取并写入 .env。
- 若用户未提供视频文件，先提示准备视频再继续。

## 示例话术

- 「要发抖音的话，可以：1）在抖音 App 里点「+」选本地上传；2）或用电脑打开抖音创作者中心网页上传。你这段视频打算用啥标题和话题？」
- 「用接口发抖音需要先在抖音开放平台创建应用并拿到授权，然后用上传接口拿到 video_id，再调发布接口。」
- 用户提供 openId/accessToken 并说配置上去时：「已把 openId 和 accessToken 写入项目下的 .env，会一直保留，之后发抖音会优先用这份配置。」
