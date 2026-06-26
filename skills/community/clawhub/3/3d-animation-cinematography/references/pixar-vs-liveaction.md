# Pixar-Style 3D vs Live-Action Cinematography

## 为什么 Pixar 3D 和实拍需要完全不同的 Prompt 逻辑

实拍（Live-Action）和 CG 三维动画（Pixar Style）虽然都能呈现"真实"，但底层物理完全不同。Prompt 构建如果混用，会导致质感错位。

---

## 1. 物理基础差异

### 实拍：真实光学成像
- 光线来自真实光源（太阳、灯）
- 阴影由真实物体遮挡产生，衰减自然
- 材质反射是真实光线交互
- 相机是真实机械，镜头有真实光学特性

### Pixar 3D：渲染引擎计算
- 光线由渲染器计算（Arnold、RenderMan、Cycles 等）
- 阴影是光线追踪（Ray Tracing）或光栅化（Rasterization）的近似
- 材质是 shader 定义的光线交互规则
- 相机是虚拟的，焦距/光圈是数学参数

**结果**：两者外观可以接近，但"接近"不等于"相同"。AI 生成如果混淆两者逻辑，会产生"四不像"结果。

---

## 2. 核心差异详解

### 2.1 材质渲染 Material Rendering

#### 实拍材质
- 皮肤：真实 pores、毛孔、皮脂反光，有血管隐约可见
- 服装：真实面料，纤维质感，磨损自然
- 环境：真实物体，灰尘、划痕、岁月痕迹

#### Pixar 3D 材质
- 皮肤：写实 pores + texture，但整体 CG 光泽统一；sub-surface scattering 模拟皮肤透光感
- 服装：有重力物理模拟，褶皱由 topology 和 cloth simulation 计算
- 环境：统一渲染引擎，材质颗粒度一致，无真实灰尘/划痕随机性

**Prompt 差异**：
- 实拍方向：`realistic skin, natural pores, candid photography`
- Pixar 3D 方向：`Pixar style, 3D render, subsurface scattering skin, detailed pores, clean CG aesthetic`

### 2.2 接触阴影 Contact Shadow

#### 实拍阴影
- 真实光学阴影，边缘由光源大小决定（硬阴影=点光源，软阴影=面光源）
- 阴影有自然衰减
- 接触阴影真实但可能不完美（地面不平、鞋子形状）

#### Pixar 3D 阴影
- Ambient Occlusion (AO) 环境遮蔽：物体接触面有额外暗化
- Contact Shadow 接触阴影：角色与地面/道具接触处强化阴影
- 阴影可以比实拍更"精确"（因为是计算的，不是光学的）

**为什么重要**：AI 生成如果缺少接触阴影，物体看起来会"飘"在空中。这是 Pixar 3D 质量的关键指标。

**Prompt 关键词**：
```
strong contact shadows, detailed ambient occlusion, ground shadow,
no floating objects, objects touching the surface
```

### 2.3 布料物理 Fabric Physics

#### 实拍服装
- 真实重力、纤维弹性、风力影响
- 褶皱由真实折叠、压迫产生
- 穿着痕迹（肘部、膝盖、臀部）自然形成

#### Pixar 3D 服装
- Cloth Simulation（布料模拟）计算垂坠
- 褶皱由 mesh topology 和物理参数决定
- 可以比实拍更"整洁"（风格化选择），但必须有物理感

**Prompt 关键词**：
```
cloth simulation, gravity-affected fabric, natural wrinkles,
fabric with weight, realistic draping, no flat texture
```

**常见错误 Prompt**（导致贴图感）：
- `wearing silk dress` → 只描述了材质，没有物理
- `dress with flowing fabric` → 流动感但不一定有重力

**正确方向**：
- `cloth simulation, gravity-affected silk dress, natural drape, realistic wrinkles at joints`

### 2.4 体积光 Volumetric Lighting

#### 实拍体积光
- 真实空气中的尘埃、水汽散射
- 光束可见（god rays）
- 散射强度由介质密度决定

#### Pixar 3D 体积光
- Volumetric Fog/Scattering 渲染
- 光束由体积雾（volumetric fog）计算
- 可以比实拍更"干净"或更"戏剧化"（风格化调整）

**Prompt 关键词**：
```
volumetric lighting, god rays, dust particles in light beam,
atmospheric fog, light scattering, visible light shafts
```

---

## 3. Prompt 构建原则

### 3.1 不要混用实拍和 3D 渲染描述

| 实拍描述 | 对应 Pixar 3D 描述 |
|----------|-------------------|
| cinematic lighting | 3D cinematic lighting, ray tracing |
| film grain | clean CG aesthetic |
| handheld camera | stable virtual camera |
| natural pores | detailed pores, subsurface scattering |
| candid | stylized animation, Pixar aesthetic |

### 3.2 Pixar 3D Prompt 结构

推荐结构：
```
[题材/场景] + Pixar style, 3D render, [渲染引擎关键词] +
[相机/镜头描述] + [光影描述：体积光/接触阴影] +
[材质描述：皮肤/服装/环境] + [情绪氛围]
```

示例：
```
A warrior in ancient Chinese armor, Pixar style, 3D render,
cinematic lighting, volumetric light shafts through mist,
subsurface scattering skin with detailed pores,
cloth simulation on armor fabric, strong contact shadows,
low angle shot, dramatic atmosphere, 4K
```

### 3.3 仙侠/古风专项

仙侠/古风的 Pixar 3D 化需要额外注意：
- 体积光是"仙气"的主要来源，必须强调
- 色彩偏青灰/低饱和（不同于武侠的浓烈）
- 服装要有"非真实"的美感（丝绸+魔法光泽）

---

## 4. 质量判断

### Pixar 质感通过条件
1. ✅ 皮肤 pores + texture 存在，无磨皮柔光
2. ✅ 接触阴影存在（脚下、物体接触面）
3. ✅ 体积光可见（光束/尘埃散射）
4. ✅ 服装有重力垂坠感，褶皱物理合理
5. ✅ 无物体飘浮感
6. ✅ 材质颗粒度统一

### 不合格标志
- ❌ 皮肤过于光滑（磨皮感）→ 混入实拍风格
- ❌ 无接触阴影 → 渲染深度不足
- ❌ 服装无重力感 → 缺少 cloth simulation
- ❌ 光线过于平面 → volumetric lighting 缺失
- ❌ 眼神光过于锐利 → 真实眼睛没有这种眼神光
