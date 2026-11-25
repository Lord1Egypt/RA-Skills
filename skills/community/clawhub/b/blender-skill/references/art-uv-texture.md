# UV 与贴图：接缝 / 密度 / 打包 / UDIM / 烘焙 / ORM / 图集

> 核验：2026-11-18

---

## 1. 接缝（Seams）规则

### 该放的位置
| 位置 | 理由 |
|---|---|
| 后脑 / 脊柱中线 | 正常视角看不到 |
| 内臂 / 内腿 | 自然遮挡 |
| 物体底面 | 永远看不到 |
| 硬表面板材接缝 / 倒角内侧 | 视觉上本来就该有线 |
| 袖口 / 腰带 / 领口 | 真实服装走线 |
| 90° 转折棱 | 直角处 UV 拉伸最小 |

### 禁止位置
| 位置 | 后果 |
|---|---|
| 脸部正面 | 贴花/法线错位明显 |
| 主要可见大平面 | 接缝变成一条亮线/暗线 |
| 形变关节中心（肘/膝正面） | 拉伸把接缝拉成带 |
| 高曲率球面正脸 | 极点严重拉伸 |

### 判据
展开后**棋盘格检查**：所有面棋盘格接近正方形；拉伸超过 2:1 就要重新切缝。

---

## 2. 纹理密度（Texel Density / TD）

### 计算
```
对象级：TD = sqrt(UV_area) / sqrt(world_area) × 贴图分辨率
即：TD(px/m) = 贴图边长(px) × UV 边长的归一化长度 / 对应世界长度(m)
```

### 实操流程（Blender 内置）
```
1. 材质设棋盘格贴图（Checker，20×20 格，每格 = 1/20 贴图 = 物理尺寸已知）
2. 选中 UV 岛 → UV Editor → Image → 打开棋盘格
3. 目测/量测：一格棋盘对应多少米
4. 目标：Hero 512–1024 px/m（2k 图上，1 m 长的面对应 ~1/2 到 1/4 贴图边长）
```

### 目标表
| 等级 | TD | 2k 贴图下 1 m 面占 UV |
|---|---|---|
| Hero | 512–1024 px/m | 25–50% |
| 标准 | 256–512 px/m | 12.5–25% |
| 背景 | 128–256 px/m | 6–25% |
| 移动 | 128–256 px/m | — |

### 跨物件一致
同一场景里所有「同级」资产的 TD 必须一致，否则贴图锐度不匹配，一眼看出拼贴。做法：**以 Hero 的 TD 为基准，其他资产按其等级偏移**，在 Brief 里写死。

```python
# 按目标 TD 缩放 UV（近似：整体等比缩放所有 UV）
def scale_uv_to_td(obj, factor):
    me = obj.data
    for layer in me.uv_layers:
        for d in layer.data:
            d.uv = (d.uv[0] * factor, d.uv[1] * factor)
```
> 注意：整模型等比缩放只解决「整体偏大/偏小」，不解决**同模型内岛间不一致**。后者必须逐岛调整。

---

## 3. 打包（Packing）

| 参数 | 值 |
|---|---|
| margin | 0.002–0.01（模型越大 margin 越大；2048 贴图约 4–20 px） |
| lightmap margin | ≥ 0.02（UE/Unity 烘焙光照要求） |
| pack 效率目标 | > 75%（UV 覆盖面积 / 0–1 面积） |
| 旋转 | 允许（`rotate=True`）提升效率 |
| 合并通道 | 允许 UDIM 前先按材质分块 |

```
bpy.ops.uv.pack_islands(rotate=True, margin=0.005)
```
5.3 / 5.2 参数一致。UI 里 `margin_method='SCALED'` 更可控。

### 效率低怎么办
1. 旋转岛（长条竖放）
2. 合并小岛（同一材质的相邻面）
3. 拆分过大的岛（大平面拆成几张 tiling）
4. 用 trim sheet 替代独立 UV（见 §7）

---

## 4. UDIM

| 场景 | 用 UDIM |
|---|---|
| 单资产贴图 > 4k | 是 |
| 影视级角色/大场景 | 是 |
| 游戏资产 | 否（用 atlas / trim） |

- 命名：`T_Asset_1001_BC.png`（UE 用 `_1001` 后缀，Mari/Substance 用 `.1001`）
- 每张 tile 有自己的 TD 基准，跨 tile 必须一致
- 导出 FBX 时 UDIM 不保留 → 游戏交付前必须转 atlas
- Blender 里 `bpy.ops.uv.pack_islands` 支持跨 tile 打包（`udim_source` 参数）

---

## 5. 烘焙（Baking）

### 通用设置
| 项 | 值 |
|---|---|
| 引擎 | Cycles（CPU 更稳，GPU 快） |
| Samples | 法线/AO 32–64；曲率 16；颜色 128+ |
| Margin (extend) | 4–16 px（`bake.margin = 8`） |
|  cage | 用 cage 对象或 `cage_extrusion` 手动控制射线距离 |
| 采样 | 关掉 denoise（法线会被抹平） |

### 常见 bake 类型
| 类型 | 来源 | 用途 |
|---|---|---|
| Normal | 高模 → 低模 | 细节保留 |
| AO | 高模/低模 | 阴影与磨损遮罩 |
| Curvature | 高模 | 边缘磨损遮罩 |
| Thickness | 低模 | 次表面/透光 |
| Position | 低模 | 程序化遮罩 |
| ID / Material | 低模 | 分区上色 |
| Height/Displacement | 高模 | 视差/置换 |

### 顺序（关键）
```
1. 低模 UV 完成 + TD 校准
2. 高模与低模对齐（同位置同尺寸）
3. 低模加 cage（或 cage_extrusion ≈ 高低模最大间距的 1.2 倍）
4. 先烘 Normal（最容易暴露问题：错位/翻转/缺失）
5. 再烘 AO / Curvature / Thickness
6. 全部烘完做「翻转检查」：法线图蓝底（128,128,255）为主，红绿不偏
```

### 法线图判据
- 底色接近 (128,128,255)
- 无黑斑（无命中）、无彩色噪点（cage 穿模）
- 切线空间：**OpenGL (+Y up)** 或 **DirectX (−Y up)** —— 按目标引擎选（UE 默认 DirectX，Unity/Godot OpenGL）
- 混合设置：`bpy.context.scene.render.bake.normal_space = 'TANGENT'`，`normal_r/g/b` 通道映射按引擎调

---

## 6. ORM / 通道打包

| 打包方案 | 通道 |
|---|---|
| **ORM**（UE 标准） | R = AO，G = Roughness，B = Metallic |
| **MRAO**（部分管线） | R = Metallic，G = Roughness，B = AO |
| **RMA** | R = Roughness，G = Metallic，B = AO |
| Unity Mask Map | R = Metallic，G = AO，B = Detail，A = Smoothness |
| Unity HDRP Mask | R = Metallic，G = AO，B = Detail Mask，A = Smoothness |

> 选定一种，写进 Brief，全项目一致。混用会在引擎里「金属度突然反了」。

### Blender 里合成
```
1. 三个灰度图各烘一张
2. 用 Combine Color / Separate Color 节点拼成一张
3. 或直接 Image Editor → 通道视图分别粘贴
4. 输出 PNG 8-bit（法线不要用 8-bit 有损压缩，用 PNG 或 16-bit）
```

---

## 7. Atlas 与 Trim Sheet

### Atlas（图集）
- 适用：一组小道具、模块件、植被
- 做法：所有件 UV 打包进同一 0–1 → 共享一张贴图 + 一个材质
- 收益：draw call 从 N 降到 1
- 代价：改一件要重打全图 → 定稿后才做 atlas

### Trim Sheet
- 适用：建筑、硬表面、大面积重复细节
- 做法：把边饰/板缝/材质条带做在一张长条贴图上，模型 UV 横向对齐到对应条带
- 规格：2048 或 4096，条带高度按实际世界尺寸换算（如 0.5 m 条带 = 贴图 1/8 高）
- 收益：一套建筑只用 1 张 4k 贴图

---

## 8. 贴图导出

| 平台 | 格式 | 注意 |
|---|---|---|
| PC/主机 | PNG（法线）/ TGA 或 PNG（颜色） | 法线不用 JPEG |
| 移动 | ASTC / ETC2 | 按引擎导入设置 |
| UE | PNG/TGA 导入后转 BC | sRGB 只勾颜色图，法线/ORM **不勾** |
| Unity | PNG/TGA，Normal map 类型指定 | sRGB 同上 |
| Godot | PNG | — |

**sRGB 规则**：颜色类（BaseColor / Emissive）勾 sRGB；数据类（Normal / Roughness / Metallic / AO / Height / Mask）**不勾**。搞反 = 材质数值全错。

---

## 9. 贴图命名

```
T_<Asset>_<Type>[_<UDIM>].png
Type: BC (BaseColor) | N (Normal) | ORM | R | M | AO | E (Emissive) | H (Height) | D (Displacement) | S (Subsurface)
例：T_Crate_Wood_01_BC.png
```

---

## 10. 常见缺陷对照

| 症状 | 原因 | 修法 |
|---|---|---|
| 贴图模糊 | TD 太低 / UV 岛太小 | 提高 TD 或换大贴图 |
| 接缝亮线 | 边缘 padding 不足 | margin ≥ 8 px，UV 岛别贴 0–1 边 |
| 拉伸条纹 | 接缝位置错 / 岛形长条 | 重切缝，长条岛旋转 |
| 镜像贴图文字反了 | 对称件共享 UV | 镜像件独立 UV 或翻转 |
| 法线图有彩色噪点 | cage 穿模 / 高低模错位 | 加 cage，缩 ray distance |
| 引擎里材质发灰 | sRGB 勾错 | 数据图不勾 sRGB |
| 金属不亮 | ORM 通道顺序反 | 统一 ORM 口径 |
| AO 有黑块 | 烘 AO 时 high/low 距离过大 | 减小 cage，或 AO 从低模烘 |
| lightmap 有接缝 | margin 不足 | lightmap margin ≥ 0.02 |
