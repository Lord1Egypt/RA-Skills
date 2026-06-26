# 3D Material Standards — AI 生成质量验收指南

三维动画的材质是决定"真实感"还是"塑料感"的核心。本文档定义 Pixar 风格 3D 渲染的材质标准，以及 AI 生成中的常见错误。

---

## 1. 皮肤 Skin Material

### 1.1 合格标准

**写实 pores + texture**
- 毛孔清晰可见，密度自然（不是均匀分布，有疏密变化）
- 眼角、法令纹、嘴角有细微凹陷
- T 区（额头、鼻子、下巴）有轻微油光，但不是"磨皮感"
- 年龄相关的特征（细纹、眼袋）按角色设定保留

**Subsurface Scattering (SSS) 近似效果**
- 皮肤对光有轻微透射（耳朵边缘、薄皮肤区域可见）
- 户外光：皮肤偏暖（阳光色温）
- 室内/背光：皮肤偏冷（环境光反射）

**眼神光**
- 存在但不过于锐利
- 双眼神光位置一致（除非特殊光照）
- Pixar 风格的眼神光比实拍"干净"，但不是镜面反射那种锐利

### 1.2 AI 生成常见错误

| 错误 | 原因 | 修正方向 |
|------|------|----------|
| 皮肤过于光滑/磨皮 | prompt 含 "smooth skin"、"beauty retouching" | 加 "detailed pores"、"skin texture"、"no skin smoothing" |
| 眼神光过于锐利 | prompt 用 "sharp catchlights" | 改为 "soft eye catchlights"、"natural eye highlights" |
| 皮肤无 pores | prompt 缺 "pores"、"texture" | 加 "realistic pores"、"skin texture"、"subsurface scattering" |
| 皮肤 CG 感过重 | 材质颗粒度与场景不统一 | 统一渲染风格描述 |
| 局部过曝（鼻子/额头） | 光比过大 | 补充 "soft rim light"、"balanced lighting" |

### 1.3 Prompt 关键词库

**正向（加分项）**：
```
subsurface scattering skin, detailed pores, skin texture,
realistic skin material, soft skin shader, natural pores distribution,
warm skin tones, skin with slight translucency
```

**负向（避错项）**：
```
smooth skin, beauty retouching, soft focus skin,
plastic skin, porcelain skin, overly polished skin
```

---

## 2. 服装 Fabric Material

### 2.1 合格标准

**重力垂坠 Gravity-Affected Draping**
- 裙摆、袖口自然下垂
- 静止状态下无"悬浮"感
- 站立时裙摆/裤脚有自然堆叠

**褶皱 Wrinkle Physics**
- 关节处（肘、膝、胯）有弯曲褶皱
- 褶皱有随机性（非对称、非机械）
- 静态褶皱（穿着痕迹）与动态褶皱（运动）有区别

**面料质感 Fabric Material**
- 丝绸：柔和反光，low roughness，高流动性
- 棉麻：漫反射为主，无明显高光，粗糙度高
- 皮革：中等 roughness，有纹理 displacement
- 金属/铠甲：low roughness，high reflectivity，环境反射清晰

**接缝与细节**
- 接缝线可见（非纯色贴图）
- 织理/纹理有深度（normal map/displacement 感）
- 纽扣、花纹、刺绣有立体感

### 2.2 AI 生成常见错误

| 错误 | 原因 | 修正方向 |
|------|------|----------|
| 服装像贴图覆盖 | prompt 缺 "cloth simulation"、"gravity-affected" | 加 "3D fabric simulation"、"gravity-affected draping" |
| 褶皱过于对称/机械 | prompt 缺 "natural wrinkles"、"random wrinkles" | 加 "natural wrinkles"、"organic folds" |
| 服装无重力感 | 布料模拟缺失 | 加 "fabric with weight"、"heavy silk" |
| 面料质感模糊 | prompt 缺具体面料描述 | 加 "cotton fabric"、"silk dress"、"leather armor" |
| 古风服装过新 | 无穿着痕迹 | 加 "worn fabric"、"natural aging"（按题材） |

### 2.3 Prompt 关键词库

**正向（加分项）**：
```
cloth simulation, gravity-affected fabric, natural wrinkles,
realistic draping, fabric with weight, cloth physics,
organic folds at joints, worn fabric texture, detailed seams,
silk with natural sheen, cotton fabric with texture
```

**负向（避错项）**：
```
flat texture, floating fabric, static cloth,
symmetrical wrinkles, perfect unworn fabric
```

---

## 3. 环境 Environment Material

### 3.1 合格标准

**体积光 Volumetric Lighting**
- 光束可见，有尘埃/微粒散射（god rays）
- 体积雾（volumetric fog）可见光路
- 散射强度与光源强度成正比

**接触阴影 Contact Shadow + Ambient Occlusion (AO)**
- 角色脚下有阴影
- 道具与地面/台面接触处有暗化
- 物体之间的缝隙有 AO 加深

**空间纵深 Space Depth**
- 前中后景有明确层次
- 景深效果（Z-depth blur）区分前后
- 背景物体有适当模糊（不是全画幅清晰）

**材质统一性**
- 所有物体材质颗粒度一致
- 无局部过曝/欠曝
- 色彩空间统一（无色偏）

### 3.2 AI 生成常见错误

| 错误 | 原因 | 修正方向 |
|------|------|----------|
| 物体飘浮 | 无 contact shadow | 加 "contact shadow"、"ground shadow"、"AO" |
| 无体积光 | prompt 缺 "volumetric" | 加 "volumetric lighting"、"god rays"、"atmospheric fog" |
| 光线平面感 | 光照计算不足 | 加 "ray tracing"、"cinematic lighting"、"area light" |
| 背景与前景割裂 | 渲染风格/深度不一致 | 统一 "same render engine"、"consistent materials" |
| 室内无 AO | 环境遮蔽缺失 | 加 "ambient occlusion"、"detailed shadow" |

### 3.3 Prompt 关键词库

**正向（加分项）**：
```
volumetric lighting, god rays, atmospheric fog, dust particles in light,
contact shadow, ambient occlusion, detailed AO,
cinematic depth of field, foreground background blur,
ray tracing quality, consistent render engine, studio lighting
```

**负向（避错项）**：
```
flat lighting, no shadows, floating objects,
harsh lighting, overexposed, inconsistent depth
```

---

## 4. 综合质量验收表

### 每帧必查

| 检查项 | 标准 | 不合格表现 |
|--------|------|------------|
| 皮肤 pores | 有真实毛孔，无磨皮 | 皮肤光滑/柔光 |
| 皮肤 SSS | 光线有透射感 | 皮肤像塑料/橡胶 |
| 眼神光 | 存在但不过锐 | 过锐/不存在/双侧不一致 |
| 服装重力 | 有垂坠感 | 飘浮/贴图感 |
| 褶皱 | 非对称/有随机性 | 对称/机械/缺失 |
| 接触阴影 | 脚下/接触面有阴影 | 飘浮感 |
| 体积光 | 光束/散射可见 | 平面光/无光束 |
| 材质统一 | 所有物体颗粒度一致 | 部分CG感/部分真实感 |
| 景深 | 有前后虚实 | 全画面清晰或全模糊 |

### 仙侠/古风专项

| 检查项 | 标准 |
|--------|------|
| 服装朝代 | 交领/圆领/直裾/曲裾等符合设定 |
| 发型/头饰 | 有历史依据 |
| 色彩基调 | 青灰/水墨（仙侠）vs 浓烈饱和（武侠）|
| 仙气氛围 | 体积光是否强化了"仙"的感觉 |
| 武器/道具 | 有材质感和物理接触阴影 |

---

## 5. AI 3D 生成错误案例与修正

### 案例 1：皮肤磨皮感
**不合格 Prompt**：`beautiful woman, smooth skin, soft lighting, portrait`

**修正 Prompt**：`Pixar style 3D render, detailed pores, skin texture, subsurface scattering skin, no skin smoothing, cinematic lighting`

### 案例 2：服装飘浮
**不合格 Prompt**：`character wearing flowing red dress, dramatic pose`

**修正 Prompt**：`Pixar style 3D render, cloth simulation, gravity-affected red silk dress, natural drape, realistic wrinkles at joints, contact shadow on floor`

### 案例 3：无体积光
**不合格 Prompt**：`warrior in ancient temple, dramatic lighting`

**修正 Prompt**：`Pixar style 3D render, warrior in ancient Chinese temple, volumetric god rays through dust particles, atmospheric fog, strong contact shadows, ambient occlusion, cinematic lighting`

### 案例 4：眼神光过锐
**不合格 Prompt**：`character portrait, sharp catchlights in eyes`

**修正 Prompt**：`Pixar style 3D portrait, soft natural eye catchlights, detailed pores skin, warm cinematic lighting`
