# 百度语音 API 凭证

> ⚠️ 请填入你自己的百度智能云 API 凭证。免费注册即可获取。

## 注册步骤

1. 访问 https://console.bce.baidu.com/ai/#/ai/speech/app/list
2. 注册/登录百度智能云
3. 创建应用 → 领取免费额度（新用户有免费额度）
4. 复制 API Key 和 Secret Key 填入下方

## TTS（文本转语音）

- **API Key:** （在此填入）
- **Secret Key:** （在此填入）
- **接口地址:** https://tsn.baidu.com/text2audio

## 使用说明

- 先调用 token 接口获取 access_token：https://openapi.baidu.com/oauth/2.0/token
- token 有效期 30 天，过期需重新获取
- 若不配置，听力模块自动降级为"自念模式"（AI 展示原文 → 用户闭眼自念 → 写下）
