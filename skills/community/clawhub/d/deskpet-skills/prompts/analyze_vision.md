# 多模态视觉分析提示词（analyze_vision.md）

用于 OpenClaw 调用多模态模型分析桌宠摄像头截图。要求模型**只输出 JSON**。

> 提示：也可直接运行 `python3 analyze.py --image <图片>` 自动打印本提示词。

## 中文版（推荐用于本项目）

```text
你是一个桌宠系统的视觉感知模块。请分析这张图片，只输出 JSON，不要输出任何其他内容。

要求：
1. present（bool）：画面中是否有人（人脸）。
2. emotion（string）：画面中人的情绪，只允许取以下值之一：
   happy, sad, angry, surprised, fearful, disgusted, neutral, worried, sleepy, excited。
   如果没人，取 "neutral"。
3. emotion_confidence（float）：对情绪的置信度，0 到 1。
4. colors（array）：画面中占比最高的 3 种颜色，每项为
   {"name": "<中文颜色名>", "hex": "#RRGGBB", "ratio": <0到1的占比>}。

输出格式（严格）：
{"present": true, "emotion": "happy", "emotion_confidence": 0.9, "colors": [{"name": "蓝色", "hex": "#1E6EDC", "ratio": 0.4}]}
```

## English Version

```text
You are the vision perception module of a desktop-pet emotion companion system.
Analyze the image and output JSON only. No other text.

Rules:
1. present (bool): is there a human face in the frame?
2. emotion (string): one of happy, sad, angry, surprised, fearful, disgusted,
   neutral, worried, sleepy, excited. Use "neutral" when no face is present.
3. emotion_confidence (float): 0 to 1.
4. colors (array): top-3 dominant colors as
   {"name": "<color name>", "hex": "#RRGGBB", "ratio": <0 to 1>}.

Strict output example:
{"present": true, "emotion": "happy", "emotion_confidence": 0.9, "colors": [{"name": "blue", "hex": "#1E6EDC", "ratio": 0.4}]}
```

## 调用流程（OpenClaw 侧）

```text
1. 运行：python3 capture.py --outdir captures
   → 得到图片路径（stdout JSON 的 path 字段）
2. 将本提示词 + 图片 交给多模态模型，得到回答文本
3. 将回答保存到 model_answer.txt
4. 运行：python3 analyze.py --image <path> --model-output model_answer.txt
   → 得到规范化后的严格 JSON，供记忆/反馈模块使用
```
