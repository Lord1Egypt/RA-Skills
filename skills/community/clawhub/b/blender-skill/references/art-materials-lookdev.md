# 材质与 Lookdev

> 数值是可验收的：拿到一个材质，先对表，再看图。
> 核验：2026-11-18

---

## 1. PBR 数值参考表（Principled BSDF）

| 材质 | Metallic | Roughness | 其他 |
|---|---|---|---|
| 抛光金属（铬/铝） | 1.0 | 0.05–0.15 | 干净反射 |
| 拉丝金属 | 1.0 | 0.4–0.6 | 各向异性可选 |
| 粗糙金属（铸铁） | 1.0 | 0.6–0.8 | 加 bump |
| 涂漆金属 | 0.0 | 0.3–0.5 | 底层金属度单独做磨损遮罩 |
| 塑料（光面） | 0.0 | 0.15–0.3 | IOR 1.45–1.5 |
| 塑料（哑光） | 0.0 | 0.5–0.7 | — |
| 橡胶 | 0.0 | 0.7–0.9 | 深色 + 微 bump |
| 皮革（新） | 0.0 | 0.4–0.6 | 法线做粒面 |
| 皮革（旧） | 0.0 | 0.6–0.8 | 加磨损 albedo |
| 混凝土 | 0.0 | 0.8–0.95 | 加脏污 + 气孔 bump |
| 木材（上漆） | 0.0 | 0.3–0.5 | — |
| 木材（原木） | 0.0 | 0.6–0.8 | 顺纹 bump |
| 布料（棉） | 0.0 | 0.8–0.95 | Sheen 0.2–0.4 |
| 天鹅绒 | 0.0 | 0.7–0.9 | Sheen 0.6–1.0 + 深色 |
| 玻璃 | 0.0 | 0.0–0.05 | Transmission 1.0，IOR 1.45–1.52 |
| 磨砂玻璃 | 0.0 | 0.2–0.4 | Transmission 1.0 + Roughness |
| 水 | 0.0 | 0.0–0.05 | Transmission 1.0，IOR 1.33 |
| 皮肤 | 0.0 | 0.4–0.6 | Subsurface 0.1–0.3，SSS Radius 偏红 |
| 眼睛（角膜） | 0.0 | 0.0–0.05 | Transmission 1.0，IOR 1.376 |
| 大理石 | 0.0 | 0.2–0.4 | Subsurface 0.05–0.15 |
| 雪 | 0.0 | 0.6–0.8 | Subsurface 0.2–0.4 |
| 沥青（干） | 0.0 | 0.8–0.95 | — |
| 沥青（湿） | 0.0 | 0.3–0.5 | 变暗 + 低粗糙 |

**规则**
- 非金属 Metallic = 0（除刻意做旧/磨损遮罩）
- Metallic 只有 0 或 1，中间值只应出现在**遮罩过渡**里
- 脏污/磨损是**叠层**（albedo 变暗 + roughness 升高），不是调低 metallic

---

## 2. Master Material 架构

一个可复用节点树，参数暴露在 Group Input：

```
[Principled BSDF]
 ├ Base Color   ← MixRGB(基础色, 磨损色, 磨损遮罩)
 ├ Roughness    ← MapRange(基础粗糙, 磨损粗糙, 磨损遮罩)
 ├ Metallic     ← 基础值 × (1 - 磨损遮罩)
 ├ Normal       ← NormalMap(法线图, strength)
 ├ Emission     ← 自发光色 × 强度 × 遮罩
 └ Alpha        ← 需要时（Clip 优先）
```

暴露参数：`BaseColor / Roughness / Metallic / TextureScale / WearAmount / NormalStrength / EmissiveColor / EmissiveStrength`

**收益**：20 个材质 = 20 个实例，改一次全变。禁止每个材质各搭一套节点。

```python
def make_master_material(name="MAT_Master"):
    mat = bpy.data.materials.new(name)
    if mat.node_tree is None:       # 不无条件赋 use_nodes（6.0 会弃用）
        mat.use_nodes = True
    nt = mat.node_tree
    # 新建材质自带 Output + Principled：按类型取现成的，不重建节点树
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    grp = nt.nodes.new("ShaderNodeGroup")
    # 实际建组在 UI 里更快；脚本只做骨架
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat
```

> 约定：**新建材质**而不是改既有材质，就不需要动用户的节点树；确实要在既有材质上加节点时，只 `nt.nodes.new(...)` 追加，不整体重建（重建会丢掉用户已有的贴图与分组）。

---

## 3. 材质数预算（= draw call 预算）

| 资产 | 材质上限 |
|---|---|
| Hero 道具 | 3–5 |
| 标准道具 | 1–2 |
| 模块件 | 1（共享 atlas） |
| 角色 | 3–8（body / cloth / eye / hair） |
| 环境模块 | 1–2 |

超了怎么办（按优先级）：
1. 合并同材质槽（同参数就合并）
2. 用顶点色/遮罩区分，不用新材质
3. 打 atlas
4. 才考虑减面

---

## 4. Lookdev 循环（截图驱动）

```
1. 定环境：HDRI 或三点光（见 lighting-render.md），先固定不换
2. 基线截图：get_screenshot_of_window_as_image
3. 单通道排查（逐个开关）：
   - 只看 BaseColor（无光照）→ 色相对不对
   - 只看 Roughness → 高光范围对不对
   - 只看 Metallic → 反射强弱
   - 只看 Normal → 细节方向对不对
4. 对照参考图，写下 3 条差距（不写「感觉不对」）
5. 只改 1–2 个参数，重截
6. 最多 3 轮；3 轮不收敛 → 回去改几何或重读参考
```

**关键纪律**：每次只改一件事。同时改 5 个参数等于不知道哪个起作用。

---

## 5. 常见材质问题

| 症状 | 原因 | 修法 |
|---|---|---|
| 塑料感 | Roughness 太低 + Metallic 0 且无微表面 | 提高 roughness 到 0.4+，加法线粒面 |
| 金属发灰 | 环境太弱 / 无反射源 | 加 HDRI 或反射板；检查 Metallic=1 |
| 皮肤蜡感 | SSS 过量 + roughness 太低 | SSS 0.1–0.2，rough 0.5 |
| 玻璃发白 | Transmission 有但 roughness 高 / IOR 错 | rough ≤0.05，IOR 1.45 |
| 布料像塑料 | 无 Sheen、无纹理 | Sheen 0.3，加法线织纹 |
| 边缘死硬 | 无 bevel / 无 edge wear | 加 bevel 或 edge mask 磨损 |
| 整体脏 | AO 过强 / 磨损过多 | AO 只做微弱，磨损集中在凸边 |
| 纹理糊 | TD 低或贴图小 | 见 uv-texture.md |

---

## 6. 节点侧效率规则

- 每个材质 ≤ 60 节点（再复杂就 Bake 成贴图）
- 禁止在材质里做逐像素循环/大量数学（Cycles 会照单执行）
- 纹理坐标统一用 `UVMap`，除非刻意的 world/object 投影
- 共享贴图节点用 `Texture Coordinate` 输出，不要每处新建
- 程序化纹理（Noise/Voronoi）在交付前 **bake 成贴图**（引擎不认程序化）
