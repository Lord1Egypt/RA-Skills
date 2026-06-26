# ShareSDK 一键集成配置模板

> **按需配置原则**：只填写需要启用的平台，未填写的平台将不会出现在配置中

---

## 基础信息（必填）

### MobSDK 基础配置

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | MobSDK应用Key，从MobTech官网获取 | |
| appSecret | MobSDK应用密钥 | |

---

## 分享平台配置

> **只填写需要启用的平台**，未填写 = 不启用

---

### 微信系列

#### 微信（好友）

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 微信应用ID | |
| appSecret | 微信应用密钥 | |
| userName | 微信小程序原始ID（分享小程序时需要） | |
| path | 小程序页面路径 | |
| withShareTicket | 是否带shareTicket | |
| miniprogramType | 小程序类型（0正式版、1开发版、2体验版） | |
| bypassApproval | 是否绕过审核（默认false） | |

#### 微信朋友圈

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 微信应用ID（与微信相同） | |
| appSecret | 微信应用密钥 | |
| bypassApproval | 是否绕过审核（默认false） | |

#### 微信收藏

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 微信应用ID（与微信相同） | |
| appSecret | 微信应用密钥 | |
| bypassApproval | 是否绕过审核（默认false） | |

---

### 腾讯系

#### QQ

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | QQ互联应用ID | |
| appKey | QQ互联应用Key | |
| shareByAppClient | 是否使用客户端分享（默认true） | |
| bypassApproval | 是否绕过审核（默认false） | |

#### QZone

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | QQ互联应用ID | |
| appKey | QQ互联应用Key | |
| shareByAppClient | 是否使用客户端分享（默认true） | |
| bypassApproval | 是否绕过审核（默认false） | |

#### 腾讯微博

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | 腾讯微博AppKey | |
| appSecret | 腾讯微博AppSecret | |
| callbackUri | 回调地址 | |

---

### 新浪系

#### 新浪微博

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | 新浪微博 App Key | |
| appSecret | 新浪微博 App Secret | |
| callbackUri | 回调地址 | |
| shareByAppClient | 是否使用客户端分享（默认true） | |

---

### 国外主流平台

#### Facebook

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Facebook App ID | |
| appSecret | Facebook App Secret | |
| callbackUri | 回调地址 | |
| faceBookLoginProtocolScheme | 登录协议Scheme | |
| faceBookAppType | App类型（默认game） | |
| shareByAppClient | 是否使用客户端分享 | |

#### Twitter / X

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Twitter App Key | |
| appSecret | Twitter App Secret | |
| callbackUri | 回调地址 | |
| IsUseV2 | 是否使用API v2（默认true） | |
| shareByAppClient | 是否使用客户端分享 | |
| bypassApproval | 是否绕过审核 | |

#### Instagram

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | Instagram App ID | |
| appSecret | Instagram App Secret | |
| callbackUri | 回调地址 | |

#### Google+

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | Google Client ID | |
| appSecret | Google Client Secret | |
| callbackUri | 回调地址 | |
| shareByAppClient | 是否使用客户端分享 | |

---

### 其他平台

#### 短信

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| （无需配置） | - | - |

#### 邮件

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| （无需配置） | - | - |

#### 复制链接

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| （无需配置） | - | - |

#### 人人网

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 人人网应用ID | |
| appKey | 人人网应用Key | |
| appSecret | 人人网应用密钥 | |

#### 开心网

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | 开心网AppKey | |
| appSecret | 开心网AppSecret | |
| callbackUri | 回调地址 | |

#### 豆瓣

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | 豆瓣AppKey | |
| appSecret | 豆瓣AppSecret | |
| callbackUri | 回调地址 | |

#### 有道云笔记

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| hostType | 服务器类型（product/sandbox/china） | |
| appKey | 有道云笔记AppKey | |
| appSecret | 有道云笔记AppSecret | |
| callbackUri | 回调地址 | |

#### 印象笔记

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| hostType | 服务器类型（product/sandbox/china） | |
| appKey | 印象笔记AppKey | |
| appSecret | 印象笔记AppSecret | |
| shareByAppClient | 是否使用客户端分享 | |

#### LinkedIn

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | LinkedIn App Key | |
| appSecret | LinkedIn App Secret | |
| callbackUri | 回调地址 | |
| shareByAppClient | 是否使用客户端分享 | |

#### Foursquare

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | Foursquare App ID | |
| appSecret | Foursquare App Secret | |
| callbackUri | 回调地址 | |

#### Pinterest

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | Pinterest App ID | |

#### Flickr

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Flickr App Key | |
| appSecret | Flickr App Secret | |
| callbackUri | 回调地址 | |

#### Tumblr

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Tumblr App Key | |
| appSecret | Tumblr App Secret | |
| callbackUri | 回调地址 | |

#### Dropbox

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Dropbox App Key | |
| appSecret | Dropbox App Secret | |
| callbackUri | 回调地址 | |

#### VKontakte

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | VKontakte App ID | |

#### 易信

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 易信应用ID | |
| bypassApproval | 是否绕过审核 | |

#### 易信朋友圈

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 易信应用ID | |
| bypassApproval | 是否绕过审核 | |

#### 明道

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | 明道AppKey | |
| appSecret | 明道AppSecret | |
| callbackUri | 回调地址 | |

#### Line

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | Line App ID | |
| appSecret | Line App Secret | |
| callbackUri | 回调地址 | |
| callbackscheme | 回调协议 | |

#### KakaoTalk

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | KakaoTalk App Key | |
| shareByAppClient | 是否使用客户端分享 | |

#### KakaoStory

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | KakaoStory App Key | |

#### WhatsApp

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| （无需配置） | - | - |

#### Pocket

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Pocket App Key | |

#### Instapaper

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Instapaper App Key | |
| appSecret | Instapaper App Secret | |

#### Facebook Messenger

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | Facebook Messenger App ID | |
| bypassApproval | 是否绕过审核 | |

#### Telegram

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appKey | Telegram App Key | |
| callbackUri | 回调地址 | |

#### 支付宝

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 支付宝App ID | |

#### 支付宝朋友圈

| 配置项 | 说明 | 您的信息 |
| ------ | ---- | -------- |
| appId | 支付宝App ID | |

---

## 配置说明

1. **appKey/appSecret**: 从 [MobTech官网](https://www.mob.com/) 注册应用获取
2. **sortId**: 用于控制平台在分享面板中的排序顺序，数字越小越靠前（自动生成）
3. **enable**: 设置为 `true` 启用该平台（自动设置）
4. **bypassApproval**: 部分平台支持绕过审核，仅限分享文字和图片

---
根据启用的平台，前往对应开放平台创建应用：

| 平台 | 开放平台地址 |
|------|-------------|
| 微信/微信朋友圈/微信收藏 | https://open.weixin.qq.com |
| QQ | https://connect.qq.com |
| 新浪微博 | https://open.weibo.com |
| Facebook | https://developers.facebook.com |
| Twitter | https://developer.twitter.com |
| Instagram | https://developers.instagram.com |

> **填写完成后，告诉我"填写好了"，我将自动完成集成配置**
