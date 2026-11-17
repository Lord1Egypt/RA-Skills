# Agnes Video V2.0 提示词指南

## 提示词结构

高质量的视频生成提示词应包含以下要素：

```
[主体] + [动作] + [场景] + [镜头运动] + [光线] + [风格]
```

### 各要素说明

| 要素 | 作用 | 示例 |
|------|------|------|
| 主体 | 描述画面中的主要对象 | "A young astronaut" |
| 动作 | 描述主体的动作 | "walking across a red desert planet" |
| 场景 | 描述环境或背景 | "dust blowing in the wind" |
| 镜头运动 | 指定摄像机运动 | "slow cinematic tracking shot" |
| 光线 | 描述光线条件 | "dramatic sunset lighting" |
| 风格 | 指定艺术风格 | "realistic sci-fi style" |

## 文生视频示例

### 人物动作

```
A young astronaut walking across a red desert planet, 
dust blowing in the wind, 
slow cinematic tracking shot, 
dramatic sunset lighting, 
realistic sci-fi style
```

### 场景动画

```
A serene Japanese garden with cherry blossoms, 
petals falling gently in the breeze, 
slow pan across the koi pond, 
soft morning light filtering through trees, 
peaceful and meditative atmosphere
```

### 产品展示

```
A luxury watch rotating slowly on a black velvet surface, 
studio lighting highlighting the details, 
smooth 360-degree rotation, 
professional product photography style, 
clean and elegant composition
```

## 图生视频示例

### 人物动画

```
Animate the character with subtle breathing motion, 
hair moving gently in the wind, 
background lights flickering softly, 
while keeping the face and outfit consistent
```

### 场景动画

```
Bring this landscape to life with flowing water, 
moving clouds and shifting shadows, 
gentle camera movement, 
maintain the original composition and lighting
```

### 产品动画

```
Animate this product with smooth rotation, 
subtle reflections and highlights, 
professional studio lighting, 
keep the product details sharp and clear
```

## 多图视频示例

### 场景过渡

```
Use the first image as the starting scene and the second image as the target scene, 
create a smooth transformation with consistent lighting, 
natural motion, and cinematic pacing
```

### 角色转换

```
Transform the character from the first image to the second image, 
maintain consistent character identity, 
smooth morphing transition, 
professional quality, cinematic style
```

## 关键帧动画示例

### 动作序列

```
Create a smooth transition from the first keyframe to the second keyframe, 
maintaining character identity, 
consistent camera angle, 
natural motion between scenes
```

### 场景变化

```
Transition smoothly between the two keyframes, 
preserve the overall composition, 
natural lighting changes, 
cinematic quality
```

## 镜头运动关键词

### 摄像机运动

- `tracking shot` - 跟踪镜头
- `pan shot` - 摇镜头
- `tilt shot` - 俯仰镜头
- `dolly shot` - 推拉镜头
- `crane shot` - 升降镜头
- `steadicam shot` - 稳定器镜头
- `handheld shot` - 手持镜头
- `aerial shot` - 航拍镜头

### 运动速度

- `slow motion` - 慢动作
- `fast motion` - 快动作
- `smooth` - 平滑
- `dynamic` - 动态
- `gentle` - 轻柔
- `dramatic` - 戏剧性

## 动作描述关键词

### 人物动作

- `walking` - 走路
- `running` - 跑步
- `turning` - 转身
- `looking` - 看
- `smiling` - 微笑
- `talking` - 说话
- `gesturing` - 手势
- `breathing` - 呼吸

### 自然运动

- `flowing` - 流动
- `swaying` - 摇摆
- `floating` - 漂浮
- `falling` - 下落
- `rising` - 上升
- `expanding` - 扩展
- `contracting` - 收缩
- `pulsing` - 脉冲

## 光线效果

- `golden hour` - 黄金时刻
- `blue hour` - 蓝色时刻
- `soft lighting` - 柔光
- `dramatic lighting` - 戏剧性光照
- `backlit` - 逆光
- `rim light` - 轮廓光
- `volumetric lighting` - 体积光
- `cinematic lighting` - 电影级光照
- `flickering` - 闪烁
- `shifting shadows` - 移动阴影

## 风格关键词

### 摄影风格

- `cinematic` - 电影级
- `documentary` - 纪录片
- `commercial` - 商业
- `artistic` - 艺术
- `realistic` - 写实
- `stylized` - 风格化

### 艺术风格

- `anime` - 动漫
- `comic book` - 漫画
- `painterly` - 绘画风格
- `illustration` - 插画
- `concept art` - 概念艺术
- `fantasy` - 奇幻

## 质量关键词

- `high quality` - 高质量
- `professional` - 专业
- `cinematic quality` - 电影级质量
- `smooth motion` - 平滑运动
- `consistent lighting` - 一致的光照
- `sharp details` - 锐利细节
- `natural motion` - 自然运动

## 负面提示词

某些元素可能需要排除：

- `no text` - 无文字
- `no watermark` - 无水印
- `no distortion` - 无变形
- `stable camera` - 稳定镜头
- `consistent character` - 一致的角色

## 提示词优化技巧

1. **动作明确**：清晰描述主体要做什么动作
2. **镜头指定**：明确摄像机如何运动
3. **光线控制**：描述光线变化和氛围
4. **一致性**：强调保持角色和场景一致
5. **自然运动**：使用"natural"、"smooth"等关键词
6. **质量要求**：添加质量相关的关键词

## 常见错误避免

1. **避免过度复杂**：不要在一个提示词中描述太多动作
2. **保持一致性**：确保角色和场景在帧间保持一致
3. **合理时长**：根据动作复杂度选择合适的时长
4. **帧数规则**：严格遵循 `8n + 1` 帧数规则
