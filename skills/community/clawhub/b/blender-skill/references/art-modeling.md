# 建模：通用 / 硬表面 / 道具 / 车辆 / 环境 / 植被 / 角色 / 生物 / 雕刻 / 重拓扑

> 每条都给「判断依据 + 手段 + 数值」。bpy 片段按 5.3 写，5.2 差异单独标注。
> 核验：2026-11-18

---

## 1. 通用建模纪律

| 项 | 规则 |
|---|---|
| 拓扑 | 硬表面四边为主，允许三角在不可见面；形变区必须全四边 |
| 面密度 | 曲率高处密、平坦处疏；不允许全模型统一细分 |
| 支撑边 | 需要保持硬边的位置放双支撑边（间距 ≈ bevel 宽度） |
| 网格卫生 | 无零面积面、无非流形、无内部隐藏面（内部面删掉） |
| 修改器顺序 | Mirror → Bevel → Boolean → Weighted Normal → Subdivision |
| 法线 | 硬表面靠 Weighted Normal + 30° 阈值，不靠 `use_auto_smooth`（4.1 起已移除） |

### 检查用 bpy
```python
import bpy, bmesh

def mesh_stats(obj):
    me = obj.data
    me.calc_loop_triangles()
    bm = bmesh.new(); bm.from_mesh(me)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    loose_v = sum(1 for v in bm.verts if not v.link_edges)
    loose_e = sum(1 for e in bm.edges if not e.link_faces)
    # 5.2 也支持 bmesh.ops.remove_doubles 的距离探测
    res = bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-4)
    dup = len(res.get("targetmap", {}))
    bm.free()
    return dict(tris=len(me.loop_triangles), verts=len(me.vertices),
                non_manifold=non_manifold, loose_verts=loose_v,
                loose_edges=loose_e, dup_candidates=dup)
```

### 平滑着色（跨版本写法）
```python
def shade_smooth_auto(obj, angle_deg=30.0):
    me = obj.data
    if hasattr(me, "use_auto_smooth"):          # ≤ 4.0 遗留
        me.use_auto_smooth = True
        me.auto_smooth_angle = __import__("math").radians(angle_deg)
        for p in me.polygons: p.use_smooth = True
    else:                                        # 4.1+ / 5.2 / 5.3
        for p in me.polygons: p.use_smooth = True
        mod = obj.modifiers.get("Smooth by Angle") or obj.modifiers.new("Smooth by Angle", 'NODES')
        # 官方 assets 里的节点组；不存在时退化到手工 sharp_edge
        try:
            mod.node_group = bpy.data.node_groups.get("Smooth by Angle")
        except Exception:
            pass
        if mod.node_group is None:
            import math
            for e in me.edges:
                pass  # 退路：用 bpy.ops.object.shade_smooth_by_angle(angle=...)
```
> 实操更省事：`bpy.ops.object.shade_smooth_by_angle(angle=radians(30))`（4.1+ 与 5.2/5.3 都在）。

---

## 2. 硬表面（面板线 / 布尔 / bevel）

### 顺序（不能乱）
```
块面 → 面板线 → 布尔（live）→ apply scale → bevel → weighted normal → 导出前 apply
```

### 布尔纪律
| 规则 | 理由 |
|---|---|
| cutter 全部放 `COL_Booleans`，`hide_render=True` | 不污染导出集合 |
| 布尔保持 **live**（不立刻 apply） | 改形状成本低 |
| 布尔前 **Apply Scale** | 非均匀 scale 下布尔结果错位 |
| cutter 必须封闭（manifold） | 开放 cutter 产生破面 |
| 布尔后 bevel，不是前 | 前 bevel 会在切割处飞边 |
| 多切割用 Exact 求解器（`solver='EXACT'`） | Fast 在共面情况翻车 |
| cutter 比目标**深进去**（不要正好共面） | 共面 = 面重叠 = 引擎闪面 |

```python
def add_boolean(target, cutter, op='DIFFERENCE'):
    m = target.modifiers.new("Bool_" + cutter.name, 'BOOLEAN')
    m.operation = op
    m.object = cutter
    m.solver = 'EXACT'            # 5.2 / 5.3 一致
    cutter.hide_render = True
    cutter.display_type = 'WIRE'
    return m
```

### 面板线做法（三选一）
1. **Inset + 下沉**：`bpy.ops.mesh.inset(thickness=0.005, depth=-0.002)` —— 最快，适合块面
2. **Knife Project / Bisect**：精确直线分割，适合机械
3. **Boolean cutter 阵列**：重复板缝，参数化最好

板缝宽度参考：**0.001–0.003 m**（1–3 mm）。小于 1 mm 在实际视距看不见，白加面。

### Weighted Normal
```
修改器 Weighted Normal：Weight 50（常规）/ 100（极端硬边），Keep Sharp 勾选，Threshold 30°
```
> 用在 bevel 之后、导出之前。不加 Weighted Normal 的 bevel 模型在低角度光下会出现「脏面」。

---

## 3. 道具（Props）

| 分级 | 三角数 | 材质 | 贴图 | 做法 |
|---|---|---|---|---|
| Hero（手持/近景） | 2,000–8,000 | 2–4 | 2k | 全手工，bevel 齐，可拆件 |
| 标准（场景交互） | 500–2,000 | 1–2 | 1k | 手工块面 + 少量 greeble |
| 背景填充 | 100–500 | 1 | 512 | 剪影正确即可，细节全贴图 |
| 微物（螺栓/硬币） | 20–100 | 1（共享 atlas） | 256 | 一个 mesh + 实例阵列 |

**道具必检**：枢轴在手/落地点、朝向 −Y、scale 已 apply、无内部面。

---

## 4. 车辆（Vehicles）

| 分级 | 三角数 | 说明 |
|---|---|---|
| Hero（过场特写） | 80,000–200,000 | 可开合门/引擎盖、内饰、轮毂细节 |
| Gameplay 可驾驶 | 30,000–80,000 | 内饰简化、轮子独立对象 |
| 背景 | 5,000–15,000 | 剪影 + 贴图假细节 |

### 硬规则
- **轮子必须独立对象**，枢轴在轮心，命名 `SM_Vehicle_Wheel_FL`（FL/FR/RL/RR）
- 车体枢轴在**四轮触地面中心**（不是几何中心），否则悬挂/物理不对
- 玻璃单独材质（Transmission 或 masked），不与车漆同一材质槽
- 门/盖若需动画：单独对象 + 铰链枢轴，或在骨架里做
- 尺度校验：紧凑 4.2 m / 轿车 4.6 m / SUV 4.8 m / 卡车 7–12 m 长，宽 1.8–2.0 m，高 1.4–1.6 m
- 对称建模 + Mirror，镜像后 Apply（负缩放是导出杀手）

---

## 5. 环境 / 建筑

### 尺度（写实）
| 项 | 值 |
|---|---|
| 层高（楼板到楼板） | 3.0–3.5 m；净高 2.4–3.0 m |
| 门洞 | 0.9 × 2.1 m（双开 1.6 × 2.1） |
| 窗台高 | 0.9 m；窗高 1.2–1.5 m |
| 走廊宽 | ≥ 1.5 m（压迫感 1.2–1.5） |
| 台阶 | 踏面 0.28–0.30 m，踢面 0.16–0.18 m |
| 栏杆高 | 1.0–1.1 m |
| 砖 | 0.215 × 0.065 × 0.1025 m（含灰缝 10 mm） |

### 模块化（kit-bash）
```
1. 定网格：2 m 或 4 m 模数（内墙 2 m、外立面 4 m），0.5 m 子网格
2. 做一个「母版墙」（含门洞/窗洞变量）→ 全 PASS 后复制
3. 所有模块共享 1 张 atlas 或 1 张 trim sheet → 材质数 = 1
4. 接缝藏在柱/转角/踢脚线处
5. 用 collection instance 摆，不 copy 实体
```

| 模块件 | 三角数 |
|---|---|
| 2 m 墙段 | 200–800 |
| 地砖 2×2 m | 100–400 |
| 门框 | 200–600 |
| 楼梯段 | 500–2,000 |
| 英雄建筑段（近景可走） | 5,000–20,000 |

### 拆件判据
墙先拆成「结构层 / 装饰层 / 破坏层」三组：破坏层单独对象，方便做破损变体与 LOD。

---

## 6. 植被

| 类型 | 三角数 | 手段 |
|---|---|---|
| 树（写实近景） | 5,000–15,000 | 手工主干 + 卡片/枝簇 |
| 树（中景） | 1,000–3,000 | 3–5 张交叉卡片 |
| 树（远景） | 100–500 | billboard 双面片 |
| 灌木 | 300–1,500 | 球形壳 + alpha 卡片 |
| 草（每株） | 2–50 | 3–6 片叶几何，GN scatter |
| 落地碎叶 | 20–100 | 实例 |

### 规则
- **alpha 必须 `Clip`（alpha clip / masked），不用 `Blend`** —— blend 排序问题在引擎里无解
- 卡片法线朝相机方向校正（GN 里对齐视图或用双面）
- 风动靠顶点着色器/GN，不靠骨骼
- 植被集合 `COL_Foliage_*`，远景单独 collection 便于切 LOD/剔除

---

## 7. 角色 / 生物

### 阶段
```
剪影（Stage 2）→ 中模 → 高模雕刻 → 重拓扑 → UV → 材质 → 绑定 → 动画
```

### 比例（写实成年，头高 = 1 unit）
| 部位 | 头高数 |
|---|---|
| 全身 | 7.5（写实）/ 8（英雄）/ 6（风格化）/ 4–5（卡通） |
| 肩宽 | 2 |
| 手臂长（肩到腕） | 3 |
| 腿长（髋到地） | 4 |
| 眼高 | 6.7（写实） |

### 面数
| 等级 | 三角数 |
|---|---|
| Hero 可玩 | 50,000–100,000 |
| 标准 NPC | 20,000–40,000 |
| 群演 | 5,000–10,000 |
| 移动端 | 15,000–30,000 |

### 面部
- 眼窝/嘴部环路必须**全四边**，密度最高
- 嘴角到鼻翼有明确 loop；眼睑双环
- 面部单独材质（可做 blend shape / 表情）
- 眼球：球体 + 独立材质（角膜透明层可选）

### 生物（非人）
- 四足：肩胛与髋部极点位置决定形变，先定骨骼再定拓扑
- 翼/鳍：膜状部分单独对象 + 布料或骨骼链
- 尾巴：骨骼链 ≥ 4 段，根部粗尖端细

---

## 8. 雕刻（Sculpt）

| 阶段 | 笔刷 |
|---|---|
| 大形 | Draw / Clay Strips / Grab（低细分 + Dyntopo 关） |
| 中形 | Clay / Crease / Pinch |
| 细节 | Dam Standard / Alpha 贴图 / Surface Noise |
| 皮肤 | Multires + 分层（先大后小，不同层不混） |

规则：
- **先 Dyntopo 或低模 + Multires，不要一上来高细分全局**（面数爆炸，改不动）
- 分层雕刻：每层只做一件事，方便回退
- 对称用 Mirror（X），破对称放在最后
- 高模必须能重拓扑回低模；不能重拓扑的雕刻 = 不能进管线

---

## 9. 重拓扑（Retopology）

### 极点数管理（决定形变质）
| 位置 | 极点数 | 规则 |
|---|---|---|
| 头顶 | 3–5 边 pole | 极点在头顶最不显眼 |
| 肩部 | 隐藏 3 边 pole 在三角肌后 | 不放在肩峰 |
| 膝窝/肘窝 | pole 放褶皱深处 | 不放关节正面 |
| 面部 | 眼周/嘴周尽量无 pole | 极点移到耳后/发际线 |
| 硬表面 | 允许 pole 在平面内 | 不放曲面上 |

### 流程
```
1. 高模冻结（hide 高模，新建 retopo mesh，开 Snap to Face + Shrinkwrap 辅助）
2. 先主干环（躯干/四肢/关节），再补细节
3. 关节处 3 环（上/中/下），中间环在关节轴
4. 全四边，pole 数最少
5. 完成后 Shrinkwrap → 投影细节 → 烘焙法线
6. 面数落进 standards.md 预算
```

### 判据
- 关节弯 90° 不塌陷、不穿插
- 极点数 ≤ 顶点数的 5%
- 形变区无三角

---

## 10. bpy 落地片段（MCP 里直接用）

```python
import bpy, math

# 建 collection 骨架
def ensure_collection(name, parent=None):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(col)
    return col

# 应用变换（导出前必做）
def apply_all_transforms(objs):
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

# 三角数统计
def tris(objs):
    n = 0
    for o in objs:
        if o.type != 'MESH': continue
        o.data.calc_loop_triangles()
        n += len(o.data.loop_triangles)
    return n

# 硬边倒角 + 权重法线
def bevel_and_wn(obj, width=0.005, seg=2):
    b = obj.modifiers.new("Bevel", 'BEVEL')
    b.width = width; b.segments = seg; b.limit_method = 'ANGLE'; b.angle_limit = math.radians(30)
    wn = obj.modifiers.new("WeightedNormal", 'WEIGHTED_NORMAL')
    wn.keep_sharp = True; wn.weight = 50
```

> ⚠️ 5.2 / 5.3 差异：以上全部可用。唯一注意 `use_auto_smooth` 在 4.1 已移除，别写。
