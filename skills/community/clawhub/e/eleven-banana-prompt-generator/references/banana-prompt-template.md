# Banana 提示词模板与示例

## 一、标准结构

Banana (Google Imagen) Prompt 遵循以下结构：

```
[Subject/主体] — who or what is the focus
[Setting/场景] — where is it happening
[Style/风格] — medium and visual style
[Lighting/光线] — lighting mood and quality
[Composition/构图] — camera angle, framing
[Quality/修饰] — technical quality boosters
```

---

## 二、主体描述规范

### 角色图模板
```
[姿态/表情] [服装描述], [发型发色], [瞳色], [人物特征]
```

示例：
```
A young Chinese woman in elegant hanfu, long black hair with jade hairpin, 
soft smile, delicate features, standing in traditional garden, golden hour light
```

### 场景图模板
```
[场景类型], [具体环境细节], [时间段], [天气], [氛围]
```

示例：
```
Ancient Chinese marketplace street, red lanterns hanging, merchants selling goods, 
crowded with people in Tang dynasty costumes, sunset, dust particles in light, cinematic
```

---

## 三、风格关键词库

### 摄影风格
| 关键词 | 效果 |
|--------|------|
| cinematic | 电影感 |
| editorial photography | 杂志大片感 |
| f/1.8 bokeh | 浅景深虚化 |
| golden hour | 黄金时刻光 |
| moody lighting | 情绪光 |
| volumetric light | 体积光 |
| studio lighting | 影棚光 |

### 艺术风格
| 关键词 | 效果 |
|--------|------|
| oil painting style | 油画质感 |
| ink wash painting | 水墨画 |
| anime style | 动漫风（慎用）|
| cel shading | 赛璐璐风格 |
| concept art | 概念设计风 |
| matte painting | 哑光绘画 |

### 画质修饰词
| 关键词 | 效果 |
|--------|------|
| ultra detailed | 超精细 |
| 8K | 高分辨率 |
| masterpiece | 杰作品质 |
| trending on artstation | 艺术感 |
| highly detailed | 高细节 |
| sharp focus | 清晰焦点 |

---

## 四、光线与氛围

```
自然光：natural lighting, soft diffused light, overcast
人造光：neon lights, warm candlelight, blue hour
情绪光：moody, dramatic, ethereal, mysterious
电影光：volumetric fog, rim light, backlit, chiaroscuro
```

---

## 五、负面提示词（Negative Prompt）

```
Blurry, low quality, distorted face, extra limbs, 
deformed hands, bad anatomy, watermark, text, 
logo, signature, cropped, worst quality, low resolution
```

针对动漫/二次元内容，额外添加：
```
anime screenshot, cartoon, illustrated, drawing, sketch
```

---

## 六、分镜素材提示词模板

### 角色特写分镜
```
Close-up shot of [角色名], [表情], [情绪], [光线角度], 
 cinematic, [画面比例如9:16], detailed, 8K
```

### 场景全景分镜
```
Wide establishing shot, [场景描述], [时间/天气], 
[氛围], aerial perspective, cinematic, 9:16
```

### 动作分镜
```
Medium shot, [角色] performing [动作描述], [表情], 
 [周围环境], motion blur effect, cinematic lighting, 9:16
```

### 转场/空镜
```
[场景类型], empty, atmospheric, [天气/时间], 
moody lighting, cinematic drone shot, 9:16
```

---

## 七、短剧常用Banana提示词库

### 古风场景
```
Ancient Chinese palace corridor, red walls, ornate pillars, 
lanterns glowing at dusk, misty atmosphere, cinematic lighting, 9:16
```

### 现代都市
```
Modern Chinese city apartment, floor-to-ceiling windows, 
night view, neon signs reflecting in glass, moody, cinematic, 9:16
```

### 情感/甜宠场景
```
Close-up of two young lovers holding hands in sunflower field, 
golden hour, warm tones, romantic, soft focus, cinematic, 9:16
```

### 悬疑/暗调场景
```
Dark abandoned warehouse, single shaft of light through broken roof, 
mysterious atmosphere, fog, volumetric lighting, cinematic, 9:16
```

### 角色定妆图
```
Studio portrait of [角色描述], [服装细节], [表情], 
professional photography, [背景类型], soft box lighting, 9:16
```
