---
name: gemini-skill
description: 通过 Gemini 官网（gemini.google.com）执行问答与生图操作。用户提到“问问Gemini/让Gemini回答/去Gemini问”，或出现“生图/画图/绘图/nano banana/nanobanana/生成图片”等关键词时触发。默认使用可用模型中最强档（优先 Gemini 3.1 Pro），按任务切换文本问答或图片生成流程，并把结果回传给用户。
---

# Gemini Web Ops

## 核心规则

1. 使用 OpenClaw 内置浏览器，`profile="openclaw"`。
2. 涉及生图关键词（如：生图、绘图、画一张、nano banana）时，优先用无头浏览器流程执行。
3. 文本问答任务（如“问问Gemini xxx”）走 Gemini 文本提问链路。
4. 默认模型：可用列表中最强模型，优先 `Gemini 3.1 Pro`。
5. 执行生图后先向用户回报“正在绘图中”，完成后回传图片。

## 任务分流

- **文本问答**触发词：`问问Gemini`、`让Gemini回答`、`去Gemini问`。
- **生图任务**触发词：`生图`、`画`、`绘图`、`海报`、`nano banana`、`nanobanana`、`image generation`。
- 若请求含糊，先确认：是文本回答还是要出图。

## 标准执行流程

### A. 文本问答
1. 打开 `https://gemini.google.com`。
2. 校验登录态（头像/输入框可见）。
3. 选择最强可用模型（优先 Gemini 3.1 Pro）。
4. 将用户问题原样输入并发送。
5. 等待完整输出，提炼后回传（必要时附原文要点）。

### B. 生图流程
1. 打开 Gemini 页面并确认登录。
2. 选择最强可用模型（优先 Gemini 3.1 Pro）。
3. 将用户提示词原样输入。
4. 开启/勾选图片生成能力（若 UI 有“生成图片/图片”开关）。
5. 发送后立即通知用户：正在绘图中。
6. 结果出现后：
   - 优先用“下载原图”按钮获取原图。
   - 若无下载按钮或失败，可对图片右键另存（通常是标清图）。
7. 把图片返回用户；若有多张，按顺序全部回传。

## 失败回退

1. 元素定位失败：刷新页面后重试一次。
2. 模型不可用：降级到次优 Gemini 模型并告知。
3. 生成超时：回报“仍在生成中”，继续等待一次；再次超时则请用户换短提示词。

## 低 token 优先策略

- 优先使用 `scripts/gemini_ui_shortcuts.js` 的快捷选择器。
- 先 evaluate 批量动作，再 snapshot 精准兜底。
- 避免高频全量快照。

## 参考

- 详细执行与回退：`references/gemini-flow.md`
- 关键词与路由：`references/intent-routing.md`
