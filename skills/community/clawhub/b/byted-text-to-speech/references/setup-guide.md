# Byted-Text-to-Speech — 服务开通与凭证申请指南

本文档帮助从零开始申请和配置 Byted-Text-to-Speech 依赖的火山引擎豆包语音合成 API 服务。

## 概览

```
注册账号 → 开通服务 → 获取 API Key → 配置环境变量 → 调用 API
  (1次)      (1次)        (1次)          (1次)         (随时)
```

整个流程约 5~10 分钟。

---

## 第一步：注册火山引擎账号

> 已有账号可跳过。

1. 访问 https://www.volcengine.com
2. 点击右上角【注册】
3. 使用手机号注册（也支持飞书、抖音等第三方账号）
4. 首次登录控制台需完成**实名认证**

---

## 第二步：开通豆包语音合成服务

1. 访问 [豆包语音-产品简介](https://www.volcengine.com/docs/6561/1257543) 了解产品能力
2. 进入 [豆包语音控制台](https://console.volcengine.com/speech/new/setting/apikeys)
3. 按页面引导完成服务开通

---

## 第三步：获取 API Key

1. 打开 [API Key 管理页](https://console.volcengine.com/speech/new/setting/apikeys)
2. 点击【创建 API Key】
3. 复制生成的 API Key

---

## 第四步：配置环境变量

将获取的凭证写入 workspace 根目录下的 `.env` 文件：

```bash
# 必填
MODEL_SPEECH_API_KEY=你的API_Key

# 可选（一般无需修改）
# MODEL_SPEECH_API_BASE=openspeech.bytedance.com
# MODEL_SPEECH_TTS_RESOURCE_ID=seed-tts-2.0
```

---

## 验证配置

```bash
cd skills/byted-text-to-speech
python3 scripts/text_to_speech.py -t "你好，语音合成测试。"
```

如果返回 `"status": "success"` 并生成音频文件，说明配置成功。

---

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| `PermissionError: MODEL_SPEECH_API_KEY 需在环境变量中配置` | 检查 `.env` 文件中是否配置了 `MODEL_SPEECH_API_KEY` |
| API 返回 401/403 | 检查 API Key 是否正确、服务是否已开通 |
| API 返回 429 | 请求频率超限，稍后重试 |
