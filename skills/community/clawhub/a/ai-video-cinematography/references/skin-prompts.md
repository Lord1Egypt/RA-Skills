# 皮肤真实感提示词指南

## 1. 微观结构与清晰度

| 英文提示词 | 中文释义 | 作用 |
|------------|----------|------|
| Detailed skin texture | 皮肤纹理 | 基础通用，防止皮肤变成纯色色块 |
| Visible pores | 可见毛孔 | **必填**，强制渲染面部细微凹凸感 |
| Large pores | 粗大毛孔 | 比 Visible pores 更激进，适合写实特写/男性 |
| Skin grain | 皮肤颗粒感 | 模拟胶片摄影的颗粒，增加电影质感 |
| Micro-details | 微观细节 | 强调极其细微的表皮起伏 |
| Sharp facial features | 面部特征锐利 | 让五官边缘清晰，避免皮肤和背景糊在一起 |
| Epidermal layer | 表皮层 | 引导 AI 关注生物学上的皮肤表面构造 |
| Peach fuzz / Vellus hair | 面部绒毛/汗毛 | **顶级真实感标志**，逆光下可见脸颊绒毛 |

---

## 2. 物理光影与材质

| 英文提示词 | 中文释义 | 作用 |
|------------|----------|------|
| Subsurface Scattering (SSS) | 次表面散射 | **核心词**，模拟光线进入皮肤后的散射，增加透明感和健康血色 |
| Translucency | 半透明感 | 表达年轻、薄弱皮肤的透明质感 |
| Specular highlights | 镜面高光 | 增强鼻梁、颧骨等部位的高光，增加面部立体感 |
| Oily skin / Greasy | 油性/油腻 | 增加 T 区反光，极度写实，适合表现热/紧张/运动后状态 |
| Hyper-realistic skin shader | 超写实皮肤着色器 | 借用 3D 渲染术语，指示 AI 使用高级渲染逻辑 |
| Rim lighting | 轮廓光 | 与 Peach fuzz 配合使用，勾勒面部金边 |
| Wet skin | 湿润皮肤 | 适合雨天、运动或海边场景，皮肤反光极高 |
| Matte skin | 哑光皮肤 | 减少反光，表现干性皮肤或定妆效果 |

---

## 3. 生理瑕疵与不完美

| 英文提示词 | 中文释义 | 作用 |
|------------|----------|------|
| Freckles | 雀斑 | 增加俏皮感，常用词，可加 Heavy freckles 增强 |
| Hyper-pigmentation | 色素沉着 | 模拟真实肤色斑块，避免单一完美色调 |
| Acne scars / Pockmarks | 痘印/麻坑 | 增加面部坑洼感，适合赛博朋克风格 |
| Moles / Beauty spots | 痣/美人痣 | 打破面部对称性，增加角色辨识度 |
| Discoloration | 变色/肤色不均 | 肤色过渡自然，包含泛红、暗沉等细节 |
| Spider veins | 蜘蛛痣/红血丝 | 常出现在鼻翼或脸颊，极致微观写实 |
| Chapped lips | 干裂嘴唇 | 增加嘴唇纹理，避免像涂了厚重油漆 |
| Dark circles | 黑眼圈 | 表现疲惫、熬夜状态或自然未化妆感 |
| Textured skin | 粗糙皮肤 | 表现老年人或艰辛饱经风霜的角色 |

---

## 4. 肤色与血色

| 英文提示词 | 中文释义 | 作用 |
|------------|----------|------|
| Rosy cheeks | 玫瑰色脸颊 | 自然红润感，表现健康活力 |
| Flushed skin | 潮红皮肤 | 表现害羞、运动后或醉酒状态的血流感 |
| Pale / Pallid | 苍白/无血色 | 适合病态、吸血鬼或高冷风格 |
| Sun-kissed | 阳光亲吻过的 | 健康小麦色，微微光泽，户外/海边风格 |
| Tanned lines | 晒痕 | 极具生活气息，如泳衣晒痕 |
| Mottled skin | 斑驳皮肤 | 常见于老年人或寒冷状态下的皮肤花纹 |
| Veins visibility | 静脉可见 | 手背、太阳穴、脖颈处青筋，增加生物感 |

---

## 5. 年龄与特定状态

| 英文提示词 | 中文释义 | 作用 |
|------------|----------|------|
| Wrinkles | 皱纹 | 老人面部特征 |
| Fine lines | 细纹 | 轻熟龄皮肤 |
| Sagging skin | 皮肤松弛 | 衰老特征 |
| Teenage skin | 青少年皮肤 | 光滑、充满胶原蛋白 |
| Weathered skin | 饱经风霜 | 长期日晒或劳作痕迹 |

---

## 6. 摄影与后期术语

| 英文提示词 | 中文释义 | 作用 |
|------------|----------|------|
| Raw photo | 原片 | 模拟相机直出，无后期修饰，保留噪声和瑕疵 |
| Unedited | 未修图 | 强调真实性，避免磨皮 |
| 8k uhd | 8K 超高清 | 增加整体信息密度 |
| Macro photography | 微距摄影 | 用于眼部、唇部特写，展示极致纹理 |
| Hard focus | 硬调对焦 | 避免柔光滤镜带来的朦胧感 |
| Sweat droplets | 汗珠 | 具体流体细节，不仅仅是发亮 |
| Film grain | 胶片颗粒 | 增加复古/电影质感 |
| Bokeh | 散景 | 背景虚化效果 |

---

## 负面提示词（必加！）

放入 Negative 提示词框：

```
airbrushed, smooth skin, plastic, blur, cartoon, doll, 
fake skin, makeup, filtered, low contrast, flat lighting, 
wax figure, semi-digital art, AI-generated, rendered, 
perfect skin, flawless, porcelain
```

---

## 组合示例

### 写实人像特写
```
Detailed skin texture, Visible pores, Subsurface Scattering, 
Peach fuzz, Rim lighting, Macro photography, Raw photo, 
8k uhd, (你的主体描述)

Negative: airbrushed, smooth skin, plastic, fake skin, cartoon
```

### 电影感肖像
```
Detailed skin texture, Skin grain, Subsurface Scattering, 
Rosy cheeks, Cinematic lighting, Film grain, Hard focus, 
(你的主体描述)

Negative: smooth skin, plastic, wax figure, low contrast
```

### 赛博朋克角色
```
Detailed skin texture, Acne scars, Hyper-pigmentation, 
Veins visibility, Wet skin, Neon lighting, (你的主体描述)

Negative: perfect skin, flawless, porcelain, smooth
```
