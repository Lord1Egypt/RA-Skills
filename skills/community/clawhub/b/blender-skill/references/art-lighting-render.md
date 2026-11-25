# 灯光 / 相机 / 渲染 / 合成

> 核验：2026-11-18

---

## 1. 三点光（基础）

| 灯 | 位置 | 强度关系 | 作用 |
|---|---|---|---|
| Key（主光） | 相机 30–45° 侧上 | 基准 = 1.0 | 定形 |
| Fill（辅光） | 相机另一侧，低 | 0.3–0.5 × Key | 提暗部 |
| Rim（轮廓） | 背后上方 | 0.5–1.5 × Key | 分离背景 |

**常见错误**：Fill 太强 → 平的、没有体积；Rim 太弱 → 主体糊在背景里。

变体：
- **恐怖/悬疑**：Key 极窄（spot），Fill 0，Rim 冷蓝，主体大面积欠曝
- **产品/展示**：大面光 + 反射板，几乎无阴影
- **户外日光**：单 Sun + HDRI 天空，无人工三点

---

## 2. 色温参考

| 光源 | 色温 (K) |
|---|---|
| 烛光 | 1800–2000 |
| 白炽灯 / 钨丝 | 2700–3200 |
| 暖白 LED | 3000–3500 |
| 中性白 LED | 4000 |
| 日光（清晨/黄昏） | 3500–4500 |
| 正午日光 | 5500 |
| 阴天 | 6500–7500 |
| 蓝调时刻 | 8000–10000 |
| 月光（视觉惯例） | 8000–12000（偏冷蓝） |

**用法**：主光暖（3200K）+ 环境冷（6500K）→ 天然冷暖分离，比调色快。

Blender 里设：`light.data.temperature = 3200`（需 `use_temperature = True`）。

---

## 3. HDRI / 世界

| 用途 | 强度 |
|---|---|
| 纯环境光（室内） | 0.3–1.0 |
| 户外日光 | 1.0–3.0 |
| 仅反射（关掉漫反射可见性） | 强度照旧，Ray Visibility 里取消 Diffuse |

- 高动态范围 HDRI（32-bit .exr / .hdr），不要用 8-bit 图冒充
- 世界光过强会洗掉方向性 → 加 Sun 提供主方向
- 室内场景用「HDRI + portal 面光进窗」最省事
- 需要可见天空但不要照明：World 里 `Light Path → Is Camera Ray` 混合两套环境

### 3.1 大气 / 雾：**别挂 World Volume**（实测坑，2026-11-18）

```
❌ World 节点里接 Volume Scatter → EEVEE 把整块背景吃掉
   实测（5.3.0 / 5.2.4，EEVEE）：sky = #C9B48E、strength 2.4，渲染出来平均亮度 0.0003 —— 全黑
   原因：EEVEE 的世界体积不参与「背景表面」着色，相机看到的是纯体积；Cycles 才收敛到天空色
✅ 用体积盒：一个包住主体的立方体 + Volume Scatter 材质（density 同值）
   两个引擎一致、可选中删除、可按场景缩放；本技能 style_presets.py 的 FOG_Style 即此实现
```

- 体积盒尺寸 ≈ 相机到主体距离 × 1.6，别做成无限大（会连同天空一起糊掉）
- `Anisotropy 0.2–0.4` 给「前向散射」雨雾感；0 是均匀散射（更平的霾）
- 雾色必须比天空亮一点或同色偏冷，否则雾看起来像脏污
- EEVEE 要阴影穿透雾 → `Render Properties > Volumes > Volumetric Shadows` 打开，代价是采样翻倍
- 密度参考：轻霾 0.005–0.01｜雨雾 0.02–0.04｜浓雾/恐怖 0.05–0.12

---

## 4. 相机

| 用途 | 焦段（全画幅等效） |
|---|---|
| 广角环境/建筑 | 14–24 mm |
| 常规叙事 | 35–50 mm |
| 人像/产品 | 85–135 mm |
| 特写微距 | 100 mm macro |

其他：
- 景深 `f/2.8`（特写）～ `f/8`（场景）；`f/11+` 才有明显星芒（需 aperture blades）
- 相机高度：人眼 1.6–1.7 m（默认视角）；俯拍 2.5 m+；儿童视角 1.0 m
- 构图：主体偏离中心 1/3 线；不要水平线切脖子
- 命名 `CAM_Shot_01`，焦距写进名字备注或用 marker

```python
cam_data = bpy.data.cameras.new("CAM_Shot_01")
cam_data.lens = 50
cam = bpy.data.objects.new("CAM_Shot_01", cam_data)
bpy.context.scene.collection.objects.link(cam)
bpy.context.scene.camera = cam
```

---

## 5. 采样与性能

| 引擎 | 场景 | 采样 |
|---|---|---|
| Cycles | 预览 | 32–64 |
| Cycles | 生产静帧 | 512–2048（+ denoise） |
| Cycles | 动画 | 128–256 + denoise（帧间稳定优先） |
| Eevee | 预览 | TAA 16–32 |
| Eevee | 生产 | TAA 64 + shadow 2048+ |

优化顺序（先做便宜的）：
1. 降 bounces（Diffuse 2 / Glossy 3 / Transmission 8 / Volume 0–1）
2. 开 adaptive sampling（noise threshold 0.01–0.05）
3. 开 denoise（OIDN，动画用帧间稳定）
4. 缩分辨率再放大（仅预览）
5. 才考虑降采样数

```python
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 512
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 6
sc.cycles.use_adaptive_sampling = True
sc.cycles.adaptive_threshold = 0.02
```

> 5.2 / 5.3 差异：`sc.cycles.*` 属性稳定。Eevee 在 4.2 后是 `BLENDER_EEVEE_NEXT`，5.x 里引擎标识为 `BLENDER_EEVEE_NEXT`（4.1 及以前是 `BLENDER_EEVEE`）→ 写死字符串前先 `[i.identifier for i in sc.render.bl_rna.properties['engine'].enum_items]` 查。

---

## 6. 色彩管理

| 项 | 值 |
|---|---|
| View Transform | **AgX**（5.x 默认；比 Filmic 保高光更好） |
| Look | None（生产）/ AgX - Punchy（展示） |
| Exposure | 0（靠灯光调，不靠曝光补偿） |
| Display Device | sRGB |

规则：
- 不要用 Standard 做写实渲染（高光直接切白）
- 对比度在合成里加，不在 view transform 里
- 保存为 16-bit EXR 或 8-bit PNG（展示）

---

## 7. 渲染通道（Passes）

必需：
| Pass | 用途 |
|---|---|
| Combined | 成图 |
| Depth (Z) | 景深/雾 |
| Normal | 重打光/后期 |
| AO | 接触阴影 |
| Cryptomatte (Object/Material) | 精确抠图 |
| Mist | 大气 |

按需：Diffuse/Glossy Color（重打光）、Emission、Shadow、Vector（运动模糊）。

```python
vl = bpy.context.view_layer
vl.use_pass_z = True
vl.use_pass_normal = True
vl.use_pass_combined = True
vl.use_pass_cryptomatte_object = True
vl.use_pass_mist = True
```

---

## 8. 合成栈（顺序）

```
1. 降噪（如未在渲染时做）
2. 曝光/白平衡校正
3. AO / 接触阴影叠加（Multiply，低不透明度）
4. 雾/大气（按 Z 深度）
5. 辉光（Glare，高光阈值 1.0+）
6. 色彩平衡 / 曲线
7. 暗角（Vignette，极轻）
8. 颗粒（Grain，0.5–2%）
9. 输出
```

**纪律**：合成只做「相机/镜头能产生的事」。不要用后期修模型的错。

---

## 9. 无头渲染（批处理）

```bash
"C:\Users\haowe\.octop\agents\6WBCS2\generated\blender53\blender-5.3.0-windows-x64\blender.exe" ^
  --background "scene.blend" ^
  --python-expr "import bpy; s=bpy.context.scene; s.render.filepath=r'C:\out\shot_01.png'; bpy.ops.render.render(write_still=True)"
```

MCP 里的对应工具：
- `render_viewport_to_path` —— 视口快渲（快，非最终质量）
- `render_thumbnail_to_path` —— 缩略图（验收留证）
- `get_screenshot_of_window_as_image` —— 窗口截图（比对循环用这个）

⚠️ 无头模式下**视口截图不可用**（没有 UI）；无头只能走 `bpy.ops.render.render`。

---

## 10. 灯光审计清单

- [ ] 每个灯有 `LGT_` 命名，且在 `COL_Lights`
- [ ] 无 `Light.001` 之类默认名
- [ ] Key 有明确方向（不是全域平光）
- [ ] 有冷暖对比（除风格需要）
- [ ] 主体无死黑（暗部有信息）
- [ ] 无过曝白块（除刻意高光/光源）
- [ ] 阴影不穿帮（无 floating shadow）
- [ ] HDRI/World 强度已固定，未随意调
- [ ] 相机焦距/高度符合叙事
- [ ] View Transform = AgX
