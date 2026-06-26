# 可灵 O1 视频生成 — 提示词编写规范

## 提示词公式
主体 + 动作 + 场景 + 镜头 + 光影 + 氛围 + 时长

## 镜头运动
zoom in, zoom out, orbit (环绕), pan left/right (平移), tilt up/down (俯仰), dolly in/out (推拉), crane shot (摇臂), tracking shot (跟踪), fixed/static (固定机位), first-person POV

## 运动速度
slow (缓慢), smooth (平滑), fast (快速), gradual (渐进), abrupt (突然), steady (稳定), accelerating (加速)

## 核心规则
- 每段提示词只描述一个主要动作，避免在同一提示词中描述多个复杂动作
- 动作描述要具体明确，避免模糊抽象的表述
- 时序清晰: 先描述起始状态，再描述运动过程

## 图生视频格式
"主体 + 运动, 背景 + 运动"
例如: "The woman turns her head slowly to the left, the cherry blossoms in the background drift downward gently"

## 多模态编辑
支持图片/视频/文字输入的编辑指令:
- 图片输入: 描述希望图片中的元素如何运动
- 视频输入: 描述希望对视频进行的修改（风格转换、元素替换等）
- 文字输入: 完整的场景描述

## 光影与氛围词汇
- 光影: golden hour glow, moonlit, neon-lit, candlelit, silhouette, dappled sunlight, dramatic shadows, soft ambient light
- 氛围: dreamy, mysterious, energetic, serene, melancholic, epic, intimate, nostalgic, futuristic
- 天气: misty, rainy, snowy, foggy, stormy, clear sky, overcast, sunset clouds

## 视频时长建议
- 简单动作: 3-5 秒
- 中等复杂度: 5-8 秒
- 复杂场景: 8-10 秒

## 示例
"A cat slowly walks across a moss-covered stone bridge in a misty forest. The camera tracks the cat from the side at a low angle. Soft dappled sunlight filters through the canopy. Dreamy, serene atmosphere. Gentle mist drifts across the foreground. Smooth, steady camera movement."
