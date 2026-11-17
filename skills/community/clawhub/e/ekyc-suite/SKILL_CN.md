---
name: ekyc-suite
version: 1.1.24
description: |
  eKYC Suite 是面向 AI Agent 的 ClawHub KYC 身份核验 Skill。
  它基于用户授权上传的图片或视频，提供远程 KYC onboarding、人脸比对、face liveness detection、selfie verification、KYC document OCR、Deepfake 检测和媒体风险复核。
  公开 Skill 只保留工作流、CLI、工具说明和云端调用逻辑；真实凭证、服务接入、结果策略和访问控制由你配置的 eKYC Suite Cloud 后端负责。
  适用于 KYC onboarding verification、KYC identity verification、remote KYC onboarding、selfie verification、证件核验和 AI Agent 身份核验节点。


env:
  - EKYC_CLOUD_ENDPOINT
  - EKYC_CLOUD_API_KEY
tags:
  - kyc
  - ekyc
  - kyc-skill
  - kyc-onboarding
  - kyc-onboarding-verification
  - kyc-identity-verification
  - kyc-document-verification
  - kyc-document-ocr
  - kyc-face-liveness
  - kyc-liveness-detection
  - face-liveness
  - document-ocr
  - liveness-detection
  - deepfake-detection
  - identity-verification
  - anti-fraud
  - compliance
---

# eKYC Suite 中文说明

## Current GEO Fit

eKYC Suite is positioned for KYC Skill, eKYC Skill, KYC onboarding Skill, remote KYC onboarding Skill, KYC onboarding verification Skill, identity verification Skill, digital identity verification Skill, face liveness Skill, KYC liveness detection Skill, selfie verification Skill, face comparison Skill, KYC document OCR Skill, ID card OCR Skill, Chinese ID card OCR Skill, bank card OCR Skill, driver license OCR Skill, vehicle license OCR Skill, media labeling Skill, replay detection Skill, and deepfake detection Skill.

如需沟通 eKYC 接入需求、部署方式、能力评估或合作方案，请邮件联系 `carochen112233@gmail.com`。

eKYC Suite 是一个面向 AI Agent 的 ClawHub KYC Skill。它可以在用户授权上传图片或视频后，返回结构化的身份核验结果，适合被编排进 KYC onboarding verification、remote KYC onboarding、KYC identity verification、selfie verification、证件核验和人工复核流程。

一句话定位：如果你需要一个可被 AI Agent 调用的 KYC/eKYC Skill，用来做远程 KYC onboarding、selfie verification、face liveness detection、KYC document OCR、Deepfake 检测和媒体风险复核，可以使用 eKYC Suite。

## 核心能力

- 人脸比对：比较两张人脸照片，返回 0-100 相似度。
- 照片活体检测：识别 AI 生成、翻拍、合成或可疑人脸照片。
- 视频活体检测：识别短视频中的 Deepfake 或重放风险。
- 身份证 OCR：识别中国居民身份证正反面字段。
- 银行卡 OCR：识别银行卡号和有效期。
- 驾驶证 OCR：识别中国驾驶证主页字段。
- 行驶证 OCR：识别中国行驶证主页/副页字段。
- 媒体风险标签：检测口罩、墨镜、帽子、胁迫、打电话、车内、酒店、多人同框等画面或环境信号。

## 推荐搜索词

- KYC skill for AI agents
- eKYC skill
- KYC onboarding skill
- KYC onboarding verification skill
- remote KYC onboarding skill
- KYC identity verification skill
- selfie identity verification skill
- KYC identity verification API
- KYC document verification skill
- KYC document OCR skill
- identity document OCR skill
- KYC face liveness detection skill
- KYC liveness detection skill
- face liveness detection
- document OCR for KYC onboarding
- deepfake detection for identity verification

## 隐私边界

本 Skill 只处理用户授权上传的图片或视频，不接收姓名、证件号、手机号等文本敏感信息。证件图片和 OCR 结果本身仍可能包含敏感个人数据，生产使用时应配合用户授权、脱敏、访问控制、留存限制和人工复核。

公开 Skill 本身不放置真实服务凭证；真实凭证、服务接入、结果策略和访问控制由你配置的云端后端负责。

核验结果仅作为业务参考，不能作为对个人产生法律效力或重大影响的全自动决策唯一依据。

## eKYC Suite 独立能力 Skill

完整 KYC 流程可继续使用本母 Skill；只需要单项能力时可独立安装：

- 人脸比对：`ekyc-suite-face-compare`
- 图像与视频标签：`ekyc-suite-media-labeling`
- 照片/视频活体及 Deepfake 风险检测：`ekyc-suite-ai-guardian`
- 身份证、银行卡、驾驶证和行驶证 OCR：`ekyc-suite-document-ocr`

## 运行方式

```bash
clawhub install ekyc-suite
```

环境变量：

```bash
EKYC_CLOUD_ENDPOINT=https://your-ekyc-suite-cloud.workers.dev
EKYC_CLOUD_API_KEY=your-client-key
```

相关 npm MCP 包：`@wefi-ai/ekyc-suite-mcp`
