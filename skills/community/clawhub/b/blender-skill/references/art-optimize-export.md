# 优化 / LOD / 碰撞 / 引擎导出

> 核验：2026-11-18 · 参数以 Blender 5.3 导出器为准（5.2 一致，差异处标注）

---

## 1. 优化审计（按顺序做，先便宜后贵）

| 序 | 动作 | 收益 | 风险 |
|---|---|---|---|
| 1 | 删内部面 / 不可见面 | 高 | 低（注意透明处会看穿） |
| 2 | 合并同材质（→ draw call 降） | 高 | 低 |
| 3 | 打 atlas / trim sheet | 高 | 中（要重 UV） |
| 4 | 手工减面（剪影不变） | 中 | 中 |
| 5 | Decimate（LOD1+ 才用） | 中 | 高（LOD0 别用） |
| 6 | 换贴图分辨率（按视距） | 中 | 低 |
| 7 | 减少骨骼数 / 权重影响 | 中 | 中 |
| 8 | 用实例替代复制 | 高（内存） | 低 |

**汇报口径**：优化前后都要有数字（三角数 / 材质数 / 贴图总字节 / 骨骼数）。没有数字的「优化了」不算。

```python
def audit(objs):
    tris = mats = 0
    for o in objs:
        if o.type != 'MESH': continue
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
        mats += len([m for m in o.data.materials if m])
    return dict(objects=len(objs), tris=tris, material_slots=mats,
                unique_materials=len({m.name for o in objs if o.type=='MESH' for m in o.data.materials if m}))
```

---

## 2. LOD 生成

### 手工（推荐 LOD0→1）
```
1. 复制 LOD0 对象（不改原件）
2. 删微 greeble / 小 bevel / 内部结构
3. 大平面减边（Dissolve Edges）
4. 保轮廓：Silhouette 检查（每级截图对比）
5. 重命名 SM_X_LOD1，材质槽保持一致
```

### 自动（快速出 LOD2/3）
```python
def make_lod(obj, ratio, name_suffix):
    lod = obj.copy(); lod.data = obj.data.copy()
    lod.name = obj.name + name_suffix
    lod.data.name = lod.name
    m = lod.modifiers.new("Decimate", 'DECIMATE')
    m.decimate_type = 'COLLAPSE'
    m.ratio = ratio
    m.use_collapse_triangulate = True
    bpy.context.collection.objects.link(lod)
    return lod
```

### 比例与距离
| LOD | 三角比 | UE Screen Size | 建议做法 |
|---|---|---|---|
| LOD0 | 100% | 1.0–0.5 | 原模型 |
| LOD1 | 40–60% | 0.5–0.25 | 手工删细节 |
| LOD2 | 15–30% | 0.25–0.1 | Decimate 0.25 |
| LOD3 | 5–10% | 0.1–0.0 | Decimate 0.08 / billboard |

**硬规则**：LOD 命名 `SM_Name_LOD0`…（UE 自动识别）；各 LOD 材质槽数一致；LOD 原点一致（否则切换跳位）。

---

## 3. 碰撞体（Collision）

| 类型 | 用途 | UE 命名 | Unity |
|---|---|---|---|
| 盒 | 箱子、门、墙 | `UBX_SM_Name_01` | 用 BoxCollider 组件 |
| 球 | 球、桶 | `USP_SM_Name_01` | SphereCollider |
| 胶囊 | 角色、柱 | `UCX_`（引擎自动生成胶囊） | CapsuleCollider |
| 凸包 | 不规则道具 | `UCX_SM_Name_01`（**必须凸**） | MeshCollider(Convex) |
| 逐面 | 静态环境 | 引擎内生成（不建议导出） | MeshCollider |

规则：
- 碰撞体**必须比可见网格简单**（面数 1/10 以下），并且**略大** 0.5–2 cm（防止视觉穿插）
- 碰撞体放 `COL_Collision`，命名带 `_COL` / `UCX_`
- 非凸网格做 `UCX_` 会失败 → 拆成多个凸块
- 载具：底盘一个盒 + 四轮各一个圆柱/球

```python
def make_box_collider(src, name=None):
    import bpy
    from mathutils import Vector
    bb = [src.matrix_world @ Vector(c) for c in src.bound_box]
    xs=[v.x for v in bb]; ys=[v.y for v in bb]; zs=[v.z for v in bb]
    bpy.ops.mesh.primitive_cube_add(size=1)
    o = bpy.context.object
    o.name = name or (src.name + "_COL")
    o.scale = ((max(xs)-min(xs))/2, (max(ys)-min(ys))/2, (max(zs)-min(zs))/2)
    o.location = ((max(xs)+min(xs))/2, (max(ys)+min(ys))/2, (max(zs)+min(zs))/2)
    bpy.ops.object.transform_apply(scale=True)
    return o
```

---

## 4. FBX 导出参数

**先选定导出对象，再调导出器**（`use_selection=True` 只认当前选中的对象，导出器本身不会替你挑集合）：

```python
import bpy

# 只选中 COL_Export 里的对象，并先取消集合外的选择
# （导出器只认选择状态，先前选中的其它对象会被一起导出）
def select_collection(col_name="COL_Export"):
    col = bpy.data.collections[col_name]
    wanted = set(col.all_objects)
    for ob in bpy.context.view_layer.objects:
        if ob not in wanted:
            ob.select_set(False)        # 只改选择状态，不改数据
    for ob in wanted:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = next(iter(wanted), None)

select_collection()
```

然后调导出器（同一段脚本里，不要中间切换选择）：

```python
bpy.ops.export_scene.fbx(
    filepath=r"C:\out\SM_Name.fbx",
    use_selection=True,              # 只导上面 select_collection() 选中的
    object_types={'MESH','ARMATURE','EMPTY'},
    apply_unit_scale=True,           # Apply Unit 开
    apply_scale_options='FBX_SCALE_ALL',   # Apply Scalings = FBX All
    axis_forward='-Z', axis_up='Y',  # 游戏口径
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    use_tspace=True,                 # 切线空间（法线贴图必须）
    add_leaf_bones=False,            # UE/Unity 都不需要
    primary_bone_axis='Y', secondary_bone_axis='X',
    use_armature_deform_only=False,
    bake_anim=True,
    bake_anim_use_all_actions=True,  # 批量导动作
    bake_anim_use_nla_strips=True,
    bake_anim_simplify_factor=0.0,
    path_mode='COPY',                # Path Mode Copy
    embed_textures=False,
)
```

| 项 | 游戏标准值 |
|---|---|
| Scale | 1.0 |
| Apply Scalings | FBX All |
| Forward / Up | −Z / Y |
| Apply Unit | ON |
| Path Mode | Copy |
| Add Leaf Bones | OFF |
| Smoothing | Face（或 Edge，按需） |
| Tangents | ON |

> ⚠️ 5.2 / 5.3 的 fbx 导出器参数一致；`bake_anim_*` 系列在 3.6+ 改名后一直稳定。若报 `TypeError: unexpected keyword`，用 `bpy.ops.export_scene.fbx.get_rna_type().properties` dump 一次确认。

---

## 5. glTF / GLB

```python
# 依赖上面 select_collection("COL_Export") 的选择状态
bpy.ops.export_scene.gltf(
    filepath=r"C:\out\SM_Name.glb",
    export_format='GLB',
    use_selection=True,
    export_yup=True,             # +Y Up（glTF 规范）
    export_apply=True,           # 应用修改器
    export_texcoords=True, export_normals=True, export_tangents=True,
    export_materials='EXPORT',
    export_cameras=False, export_lights=False,
    export_animations=True,
    export_animation_mode='ACTIONS',
    export_skins=True,
    export_image_format='AUTO',  # 或 'JPEG'/'WEBP' 压体积
)
```
规则：GLB 单文件便于分发；纹理超过 2k 时考虑 `export_image_format='WEBP'`；引擎导入时注意 Unity 的 glTF 需第三方包（Unity 官方支持有限）→ **Unity 首选 FBX**。

---

## 6. USD / Alembic

| 格式 | 用途 | 关键点 |
|---|---|---|
| USD (.usdc) | 影视管线、UE USD 工作流、大场景分层 | 支持分层/引用；材质走 MaterialX/UsdPreviewSurface |
| Alembic (.abc) | 缓存（FX、布料、破碎） | 无材质无绑定，纯几何流；面数大 |

```python
# USD
bpy.ops.wm.usd_export(filepath=r"C:\out\scene.usdc", selected_objects_only=True,
                      export_materials=True, export_texcoords=True, export_normals=True,
                      export_animation=False)
# Alembic（烘焙缓存）
bpy.ops.wm.alembic_export(filepath=r"C:\out\sim.abc", selected=True, start=1, end=120,
                          flatten=False, apply_subdiv=False, export_hair=True)
```
> USD 导出器参数在 4.x→5.x 有改名历史 → 调用前 dump 一次 `bpy.ops.wm.usd_export.get_rna_type().properties.keys()`。

---

## 7. 引擎侧要点

### Unreal Engine 5
| 项 | 值 |
|---|---|
| 导入 | FBX（首选）；勾 `Combine Meshes` OFF（分件导入） |
| 缩放 | FBX 单位 cm 出问题 → 导入时 `Convert Scene` 开 |
| 材质 | Blender Principled → UE 材质表达式自动映射；ORM 通道需手工接（R=AO/G=Rough/B=Metal） |
| 碰撞 | `UCX_` 自动生成；否则手动加 |
| LOD | 命名 `_LOD0..N` 自动识别，或用 LOD Group 面板 |
| 光照 | Nanite 可吃高模（但 LOD 仍需）；Lumen 需距离场 |
| sRGB | BaseColor/Emissive 勾；Normal/ORM 不勾 |
| 顶点数上限 | 单 mesh 建议 < 500k（Nanite 另算） |

### Unity 6
| 项 | 值 |
|---|---|
| 导入 | FBX；`Scale Factor 1`，`Convert Units` 开 |
| 朝向 | Blender −Y 前 → Unity +Z 前，导入器自动处理 |
| 材质 | 需重建 URP/HDRP 材质（Principled 不完全映射） |
| Mask Map | HDRP: R=Metal G=AO B=Detail A=Smooth；URP Lit 用 Metallic+Smoothness |
| 碰撞 | `_COL` 后缀不自动识别 → 手动挂 Collider 或用脚本批量 |
| LOD | LOD Group 组件手工配（或 `_LOD0..N` + 脚本） |
| 法线 | Unity 用 OpenGL 风格（+Y）→ Blender 烘的 OpenGL 法线直接用；DirectX 需翻绿通道 |

### Godot 4
| 项 | 值 |
|---|---|
| 导入 | GLB 首选（Godot 原生支持最好） |
| 材质 | Principled → StandardMaterial3D 基本对齐 |
| 碰撞 | `-col` / `-colonly` 后缀约定，或 `-convcol`（凸包） |
| 缩放 | 1 unit = 1 m，与 Blender 一致 |
| 动画 | GLB 内嵌动画可直接用 AnimationPlayer |

---

## 8. 导出验证矩阵（每次交付必做）

| 检查 | 怎么查 | 失败症状 |
|---|---|---|
| 缩放正确 | 引擎里对比人形标尺 | 模型巨大/微小 |
| 朝向正确 | 引擎里看前向箭头 | 模型背对/躺倒 |
| 枢轴正确 | 旋转看是否绕预期点 | 绕世界原点转 |
| 法线正确 | 引擎里单面光照射 | 局部黑面/翻转 |
| 材质完整 | 检查 UV/贴图引用 | 洋红/灰白 |
| 材质数对 | 引擎统计 | 莫名多出材质槽 |
| 动画完整 | 播放每个 Action | 动画丢失/错位 |
| 骨骼上限 | 引擎报错 | "too many influences" |
| 碰撞体 | 走进去试 | 穿墙/悬空 |
| LOD 切换 | 拉远看 | 突跳/消失 |
| 文件体积 | `dir` | 超预算（贴图未压） |

---

## 9. 交付目录约定

```
out/
├── SM_Name.fbx
├── T_Name_BC.png / _N.png / _ORM.png
├── SM_Name_LOD0..3.fbx（或单文件多层）
├── SM_Name_COL.fbx（若需独立）
└── README.md  ← 引擎、缩放、朝向、枢轴、材质通道、已知缺陷
```
`README.md` 是交付的一部分，不写等于把问题丢给下游。
