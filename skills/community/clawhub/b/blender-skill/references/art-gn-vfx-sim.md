# 几何节点 / 程序化 / FX / 物理

> 核验：2026-11-18 · 5.3 基准（Lists / Bundles 可用），5.2 兼容写法单列

---

## 1. 节点组规范（可复用才叫资产）

| 规则 | 说明 |
|---|---|
| 命名 `GN_<功能>_v01` | 版本号必带，改逻辑就升版 |
| Group Input 全暴露 | 尺寸/数量/随机种子/材质/开关 都要能从外面调 |
| Random Seed 必须暴露 | 否则不可复现 |
| 内部不硬编码对象引用 | 需要对象就从 Input 传；写死对象 = 换场景就崩 |
| 输出单一 | 一个组只做一件事（scatter / 建筑 / 管线 分开） |
| 文档注释 | 组内加 Frame + 文字说明参数含义 |

```python
def new_gn_group(name="GN_Scatter_v01"):
    ng = bpy.data.node_groups.new(name, 'GeometryNodeTree')
    ng.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
    ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
    gi = ng.nodes.new("NodeGroupInput")
    go = ng.nodes.new("NodeGroupOutput")
    return ng
```

---

## 2. 常用生成器（要能直接跑）

### 2.1 表面散射（石头/草/杂物）
```
输入：Surface(Geometry) / InstanceObject / Density / ScaleMin / ScaleMax / Seed
链路：Distribute Points on Faces → Instance on Points(rotation 随机) → Realize? (仅当需编辑)
     Normal → Align Euler to Vector（让实例贴合表面法线）
```
| 参数 | 建议 |
|---|---|
| Density | 地面碎石 0.5–5 / 草丛 20–200 / 落叶 1–10（每 m²） |
| Scale 范围 | 0.7–1.3 倍基准（太大就假） |
| 上限 | 用 `Instance` 不 Realize；> 10 万实例考虑分块 |

### 2.2 模块化建筑（procedural building）
```
Grid(尺寸) → Instance 楼层模块 → 按层高堆叠 → 随机破形（阳台/窗型）
```
关键：**用 collection instance**（`Collection Info`），不要生成实体几何 —— 方便后面手工替换单体。

### 2.3 管道/线缆（curve driven）
```
Curve(手工画) → Curve to Mesh(profile) → 法兰/接头 按长度分布
```
规则：弯管半径 ≥ 3× 管径，否则视觉折断；接头处留 2–5 cm 直段。

### 2.4 岩石/地形破碎
```
Icosphere → 顶点位移(Noise, scale 0.5–2) → Decimate 或 Remesh
```
判据：不能是「圆球加了噪声」—— 要有明确平面切割感（用 Boolean 切面）。

### 2.5 参数化围栏 / 台阶 / 楼梯
用 `Repeat Zone`（5.x）按长度重复；每段间距参数化。

---

## 3. 5.3 新特性（5.2 无，需守卫）

| 特性 | 用途 | 守卫 |
|---|---|---|
| **Lists**（socket type `NodeSocketList` 等） | 一个组处理多个几何/多个值 | `bpy.app.version >= (5, 3, 0)` |
| **Bundles** | 多类型数据打包传递 | 同上 |
| **For Each Element** zone | 逐元素处理 | 同上 |

```python
IS_53 = bpy.app.version >= (5, 3, 0)

def new_socket(ng, name, in_out='INPUT', stype='NodeSocketGeometry'):
    try:
        return ng.interface.new_socket(name, in_out=in_out, socket_type=stype)
    except Exception:
        # 4.x 旧签名兜底
        return ng.interface.new_socket(name=name, in_out=in_out, socket_type=stype)
```
⚠️ 别在 5.2 兼容代码里引用 `NodeSocketList` —— 直接 AttributeError/无法创建。

---

## 4. 性能规则

| 问题 | 判据 | 处置 |
|---|---|---|
| 实例 vs 实体 | 实体化后 > 5 万面 | 保 `Instance on Points`，不 Realize |
| 节点求值卡 | 改一个参数 > 2 s | 减 Distribute 密度、拆组、关视图显示 |
| 场景膨胀 | .blend > 500 MB | 用 `Library Override` / 分离 .blend |
| 导出巨慢 | 导出 > 5 min | 导出前 Apply 成静态网格（不导出 GN 依赖） |
| 视口卡 | FPS < 15 | 用 `Simplify`（视口 subdivision 0） |

**硬规则**：交付给引擎前，GN 结果必须 **Apply 成真实网格**（引擎不读 Blender GN）。保留 GN 的原始版本另存。

---

## 5. FX / 物理

| 类型 | 用途 | 关键参数 |
|---|---|---|
| 刚体（Rigid Body） | 破碎、堆叠、倒塌 | Mass、Friction 0.3–0.7、Bounciness 0–0.2、Collision Shape |
| 布料（Cloth） | 旗帜、窗帘、衣物 | Quality 5–15、Mass 0.3、Structural/Shear/Bending |
| 流体（Mantaflow / 5.x） | 水、烟、火 | Domain 分辨率 128–512（越高越慢，指数增长） |
| 软体（Soft Body） | 果冻、软垫 | Goal、Stiffness |
| 粒子 | 火花、尘、雨 | Emission 数量、Lifetime、Renderer |
| Cell Fracture（插件） | 破碎 | Source 面数、Noise |

### 烘焙（Bake）纪律
- 物理必须先 **Bake** 再渲染/导出，不依赖实时求值
- Bake 目录写进 Brief（默认 `//cache/<sim>/`），否则换机器全丢
- 帧范围固定，改范围要重烘
- 5.3 与 5.2 的 fluid/mantaflow 属性有差异，写脚本前先 dump `dir(domain)` 确认

---

## 6. FX 交付清单

- [ ] 模拟已 Bake，缓存目录随工程一起交付或重建脚本齐全
- [ ] 帧范围与镜头一致
- [ ] 破碎/布料无穿模（抽 10 帧检查）
- [ ] 需要进引擎的 FX → 转为骨骼动画 / VAT / 顶点动画贴图 / 序列帧
- [ ] 计算量已记录（渲染时间/内存），方便排期
