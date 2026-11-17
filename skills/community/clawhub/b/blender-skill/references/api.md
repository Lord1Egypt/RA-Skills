# Blender API Compatibility Notes

Version guards for code sent through `execute_blender_code`. **Production baseline: Blender 5.3 (5.3.0, released 2026-11-10); compatibility floor: 5.2 LTS (5.2.4).** These notes describe the official Blender Python API, not a separate server.

## Blender 5.1 API Compatibility Notes

### Action Layered Structure (Breaking Change)

In Blender 5.1, `Action.fcurves` was removed. The new layered animation system uses:

```python
# ❌ Old (5.0 and earlier)
fcurves = action.fcurves

# ✅ Blender 5.1+
fcurves = action.layers[0].strips[0].channelbags[0].fcurves
```

### Brush API: `use_*` → `stroke_method` Enum

```python
# ❌ Old (5.0)
brush.use_airbrush = True

# ✅ 5.1+
brush.stroke_method = 'AIRBRUSH'  # Options: AIRBRUSH, SPACE, ANCHORED, LINE, CURVE, DRAG_DOT
```

### VSE Time Property Renames

| Old (5.0) | New (5.1) |
|-----------|-----------|
| `frame_final_duration` | `duration` |
| `frame_final_start` | `left_handle` |
| `frame_final_end` | `right_handle` |
| `frame_duration` | `content_duration` |

### Principled BSDF Input Renames

| Old (5.0) | New (5.1) |
|-----------|-----------|
| `inputs['Transmission']` | `inputs['Transmission Weight']` |
| `inputs['Emission']` | `inputs['Emission Color']` + `inputs['Emission Strength']` |

### Other 5.1 Changes
- `sculpt.sample_color` → `paint.sample_color`
- `bpy.app.cachedir` — new standard cache directory
- `bpy.app.handlers.exit_pre` — new exit handler
- Python 3.13 runtime

---

## Blender 5.2 LTS Compatibility Notes (LTS — **兼容下限**)

> Blender 5.2 LTS 已发布（最新补丁 **5.2.4**，2026-11-10）。自 2026-11-12 起 5.2 **不再是生产基准**，而是**兼容下限** —— 这些破坏性变更仍是「从 5.1/4.x 往上迁」与「向下兼容 5.2」的必读项。

### 🔴 Breaking Changes (12 total — all Beta confirmed)

#### 1. Geometry Nodes Modifier API Rewrite

```python
# ❌ 5.1 and earlier
modifier["SocketName"] = 5.0
modifier["SocketName_use_attribute"] = True
modifier["SocketName_attribute_name"] = "some_input"

# ✅ 5.2+
modifier.properties.inputs.SocketName.value = 5.0
modifier.properties.inputs.SocketName.type = "ATTRIBUTE"
modifier.properties.inputs.SocketName.attribute_name = "some_input"
modifier.properties.outputs.SocketName.attribute_name = "some_output"

# ✅ Compatible pattern
import bpy
if bpy.app.version >= (5, 2, 0):
    val = modifier.properties.inputs.SocketName.value
else:
    val = modifier["SocketName"]
```

#### 2. Principled BSDF Node Renamed
- `Transmission` → `Transmission Weight`
- Already applies from 5.1; ensure plugin references match

#### 3. `paint.eraser_brush` API Removed
- No longer needs manual setting; last eraser brush auto-activates

#### 4. Automasking → MeshAutomaskingSettings (17 properties migrated)

```python
# ❌ Old
brush.use_automasking_topology = True
brush.automasking_cavity_factor = 0.5

# ✅ 5.2+
brush.mesh_automasking_settings.use_automasking_topology = True
brush.mesh_automasking_settings.cavity_factor = 0.5
```

All 17 properties: `use_automasking_topology`, `use_automasking_face_sets`, `use_automasking_boundary_edges`, `use_automasking_boundary_face_sets`, `use_automasking_cavity`, `use_automasking_cavity_inverted`, `use_automasking_start_normal`, `use_automasking_view_normal`, `automasking_boundary_edges_propagation_steps`, `automasking_cavity_factor`, `automasking_cavity_blur_steps`, `automasking_cavity_curve`, `automasking_cavity_curve_op`, `automasking_start_normal_limit`, `automasking_start_normal_falloff`, `automasking_view_normal_limit`, `automasking_view_normal_falloff`

#### 5. VSE `strip.use_linear_modifiers` Removed
#### 6. VSE `timecode files` Feature Removed
#### 7. `UILayout.template_palette` `color` Parameter Removed
#### 8. Compare / Random Value Node Socket Identifiers Changed
#### 9. Asset Library Index Shift — "All Libraries" and "Essentials" now occupy first two indices
#### 10. Evaluated Meshes Naming Change — Geo Nodes created meshes no longer share object's original mesh name
#### 11. Brush `use_*` → `stroke_method` (see 5.1 section above)
#### 12. VSE Time Property Renames (see 5.1 section above)

---

### 🟢 High-Value New APIs (5.2 LTS)

#### Python API
| API | Description |
|-----|-------------|
| `bpy.data.all_ids` | Single iterator over ALL data-blocks |
| `WindowManager.reports` | Read-only reports list with session-wide unique uid |
| `bpy.data.libraries.load()` input | Now exposes nested library paths |
| `Window.screenshot()` | Get window pixel data without saving to file |
| `gpu.init()` | Initialize GPU backend in `--background` mode |
| `mathutils` slice step | `vector[begin:end:step]` for Vector/Matrix/Color/Euler |
| Blender Arrays slice step | `image.pixels[begin:end:step]` — e.g., `pixels[3::4]` for alpha channel |
| `path_foreach` options | EXPAND_TOKENS, EXPAND_SEQUENCES, EXPAND_CACHES |
| Annotations API | `frame.strokes.new()`, `stroke.points.add(count, pressure, strength)`, `stroke.points.remove(index)`, `frame.strokes.remove(stroke)` |
| `UILayout.link` / `textbox` | Styled link buttons and multi-line text buttons |
| `imbuf` extended | Pixel-level image access, format conversion, buffer protocol |
| Node panel collapse | Programmatically open/close node panels from Python |
| Node Tool input values | Set Node Tool parameters programmatically in 5.2 |

#### Geometry Nodes
| Node / Feature | Description |
|----------------|-------------|
| **Physics (experimental)** | XPBD Solver, Cloth Dynamics modifier, Hair Dynamics, Effector system |
| **Mesh Bevel** | Long-awaited procedural bevel node |
| **Geometry Bundles** | Set/Get Geometry Bundle — attach arbitrary data (fields, closures) to geometry |
| **Lists data type** | New core type alongside single/field/grid — Length, Get, Filter, Sort |
| **Sample Sound Frequencies** | Audio-driven animation without keyframe baking |
| **PCA** | Principal Component Analysis for auto-alignment |
| **Transfer Attributes** | Transfer attributes between two geometries |
| **3D ↔ Screen Space** | Bundled transform nodes (3D to Screen, Screen to 3D, Project with Depth) |
| **Collection Children** | Recursive access to collection children as lists |
| **Empty Objects** | Geo Nodes modifiers on Empty objects |
| **Capture Attribute Selection** | Selection input for efficiency |
| **NURBS Order/Weight** | Set NURBS Order and Weight nodes |
| **Scene Frame default input** | Float/int sockets default to current frame |
| **Self-object default** | Object sockets can default to self-object |
| **Merge by Distance split** | Now: Merge Points + Cluster by Distance + Cluster by Connected |

#### Cycles
| Feature | Description |
|---------|-------------|
| **Texture Cache** | `.tx` files reduce memory 34-77% in texture-heavy scenes. Enable: Performance > Texture Cache + Auto Generate. CLI: `blender scene.blend --command maketx` |
| **Raycast Attributes** | Access attributes at intersection point (Cycles only) |
| **SSS Negative Anisotropy** | Principled/Subsurface BSDF: -1 to 1 range |
| **World Cast Shadows** | World can now cast shadows |
| **OSL GPU** | Texture cache improves OSL performance + adds GPU support |
| **Simplify Texture Resolution** | Percentage-based texture scaling (50%, 25%) |

#### EEVEE
| Feature | Description |
|---------|-------------|
| **Shader Raycast** | Screen-space raytracing node |
| **Light Path Intensity** | Global indirect light intensity control |
| **Texture pool -40%** | Vulkan: 406MB → 245MB |

#### Grease Pencil
| Feature | Description |
|---------|-------------|
| **Fill Tool Delaunay** | New Delaunay solver: precise geometry, auto gap detection, scale-independent, faster |
| **Draw Tool curves** | Bézier / Catmull-Rom / NURBS curve types |
| **Line Materials placement** | Count / Density / Radius modes with randomization |
| **`layer.layer_masks` API** | Add/remove layer masks via Python |

#### Video Sequencer
| Feature | Description |
|---------|-------------|
| **Compositor Effect Strip** | Use compositor node trees for VSE transitions/effects (0/1/2 inputs + fader) |
| **Compositor GPU acceleration** | In VSE modifiers |
| **`strip.connections`** | API to find connected strips |

#### Sculpt
| Feature | Description |
|---------|-------------|
| **Scene Project brush** | Displace vertices toward other objects (like Shrinkwrap) |
| **Add Primitive in Sculpt Mode** | Cube/Cone/Cylinder directly in sculpt |
| **Color Filter unified color** | Uses scene unified colors; Ctrl-X quick fill |
| **Dyntopo confirmation removed** | No more confirmation dialog when switching back to Sculpt |
| **Voxel Remesher attribute interpolation** | Smooth vertex/corner attribute interpolation |

#### Assets
| Feature | Description |
|---------|-------------|
| **Online Asset Library** | Browse and download from remote hosted libraries |
| **Asset Library index shift** | "All Libraries" and "Essentials" now at indices 0 and 1 |

#### Other
| Feature | Description |
|---------|-------------|
| **LoopTools built-in** | Circle/Space/Flatten now native — no addon needed |
| **Hydra 2.0 API** | OpenUSD provides abstraction layer |
| **Animation +125%** | Action evaluation 32.8→74.1 fps (4 threads) |
| **Gaussian Smooth F-Curve** | Non-destructive curve smoothing modifier |

---

## Blender 5.3 Compatibility Notes (正式版 — 2026-11-10 发布，**生产基准**)

> **5.3 已于 2026-11-10 正式发布**（5.3.0；同日 5.2.4 / 4.5.16 也发布）。`download.blender.org/release/Blender5.3/` 有包、Gitea tag `v5.3.0` 存在、`.msi` 200 → 三件套全绿。
> **现行口径**：新代码按 **5.3** 写（不再叫「前瞻」），**每条 5.3 路径必须留 5.2 回退**；`bl_info["blender"] = (5, 2, 0)`。5.4 处于 Alpha（until 2027-02-03），**只用 `hasattr` 兜底、不基于它开发**。
> 📝 最后核验：**2026-11-12**（`/api/5.3/` 的 `5.2 to 5.3` 章节 133 条，连续第 7 轮零变更；完整条目与迁移清单见 `knowledge/blender/api-changes-5.3.md`）

### 🔴 5.3 Breaking Changes（8 组，详见知识库）

> 📝 最后扫描：2026-09-07 11:00 — 完整官方 change_log 核实

#### GPU 兼容性变更 (09-06)
```python
# ⚠️ gpu.types.GPUBatch.draw_instanced 行为变更
# 现在优先使用 gpu_InstanceIndex（包含 base_instance）
# 与 Metal/Vulkan 内部工作方式对齐
# commit: 6f64632716
# 影响：使用自定义 GPU 着色器的插件需要测试兼容性
```

#### 🔴 NodesModifier.panels 移除 (09-07 新发现！关键！)
```python
# ❌ 5.2 及更早
modifier.panels  # 访问 Geo Nodes 修饰器的面板属性

# ✅ 5.3+ — 已移除！
# Geo Nodes 修饰器不再有 panels 属性
# 兼容写法：
import bpy
if bpy.app.version >= (5, 3, 0):
    # 使用 modifier.properties.inputs/outputs 替代
    pass
else:
    panels = modifier.panels
```

#### 🔴 Theme API 移除 (09-07 新发现)
```python
# ❌ 以下主题属性在 5.3 中已移除：
# ThemeFileBrowser.selected_file
# ThemeSpaceGeneric.header_text / header_text_hi / title
# ThemeSpaceGradient.header_text / header_text_hi / title

# 影响：自定义主题插件需要移除对这些属性的引用
```

#### Brush Unified Input 属性重命名 (4 项，09-07 修正映射)

```python
# ❌ 5.2 及更早
brush.use_inverse_smooth_pressure = True

# ✅ 5.3+（09-07 官方确认的新名称）
brush.use_smooth_pressure = True        # ← use_inverse_smooth_pressure 重命名而来
brush.use_unified_input_samples = True  # ← 新增统一输入属性
brush.use_unified_strength = True       # ← 新增统一强度属性
brush.use_unified_weight = True         # ← 新增统一权重属性

# 兼容写法：
import bpy
if bpy.app.version >= (5, 3, 0):
    brush.use_smooth_pressure = True
else:
    brush.use_inverse_smooth_pressure = True
```

#### PreferencesExperimental 重命名 (1 项)
```python
# ❌ 5.2
prefs.experimental.use_sculpt_texture_paint

# ✅ 5.3+
prefs.experimental.use_3d_texture_paint
```

#### PreferencesSystem 重命名 (1 项)
```python
# ❌ 5.2
prefs.system.geometry_nodes_stack_limit

# ✅ 5.3+
prefs.system.nodes_stack_limit
```

#### 🔴 SpaceOutliner 过滤器重命名 (10 项，09-23 补充来源信息！关键！)
```python
# ❌ 5.2 及更早
outliner.use_sort_alpha = True  # 单个属性控制字母排序

# ✅ 5.3+ — 拆分为 10 个独立过滤器属性！
# 每个对象类型/数据类型都有独立的过滤器控制
outliner.use_filter_object_materials = True
outliner.use_filter_object_modifiers = True
outliner.use_filter_object_constraints = True
outliner.use_filter_object_shape_keys = True
outliner.use_filter_object_vertex_groups = True
outliner.use_filter_object_data = True
outliner.use_filter_object_animation = True
outliner.use_filter_bone_collections = True
outliner.use_filter_pose_bones = True
outliner.use_filter_grease_pencil_effects = True

# 兼容写法：
import bpy
if bpy.app.version >= (5, 3, 0):
    # 使用新的独立过滤器
    outliner.use_filter_object_materials = True
else:
    # 旧版本使用 use_sort_alpha
    outliner.use_sort_alpha = True
```

#### 🔴 UserAssetLibrary 属性重命名 (3 项，09-23 补充来源信息！)
```python
# ❌ 5.2 及更早
library.path = "/path/to/asset"

# ✅ 5.3+ — 拆分为 3 个独立属性
library.auth_token = "token"  # 认证令牌
library.invalid_uuid = "uuid"  # 无效 UUID
library.uuid = "uuid"  # 资产库 UUID

# 兼容写法：
import bpy
if bpy.app.version >= (5, 3, 0):
    # 使用新的独立属性
    library.auth_token = token
    library.uuid = uuid
else:
    # 旧版本使用 path
    library.path = path
```

#### 🔴 函数签名变更（2026-10-05 新增发现！易静默出错）

```python
# ❌ 旧签名（≤5.2）
bpy.types.ObjectConstraints.new(type)                 # 只传 type
bpy.types.PoseBoneConstraints.new(type)
layout.textbox(data, property, initial_visible_lines, placeholder, text_ctxt, translate)

# ✅ 5.3+
bpy.types.ObjectConstraints.new(type, name)           # 多了一个 name
bpy.types.PoseBoneConstraints.new(type, name)
layout.textbox(data, property, text, text_ctxt, translate,
               initial_visible_lines, placeholder)    # ⚠️ 位置参数被重排！

# 安全做法：全部改用关键字传参
layout.textbox(data, property, text=text, text_ctxt="", translate=False,
               initial_visible_lines=3, placeholder="")

# WindowManager.popover / popover_begin__internal：新增 auto_keymap 参数
bpy.context.window_manager.popover(draw_func, ui_units_x=8, keymap="", from_active_button=False, auto_keymap=True)
```

**影响**：任何按位置传参调用 `textbox` / `textbox_with_state` / `Constraints.new` 的插件，在 5.3 上会**静默传错值**或抛 `TypeError`。

#### 🟢 2026-10-05 其他新增（精选）

| API | 说明 | 插件价值 |
|-----|------|----------|
| `BlendFileColorspace.is_failed_opencolorio_config` / `ocio_config_path` / `ocio_config_source` | OCIO 配置诊断 | 色彩管线插件能定位色彩管理失败原因 |
| `MaterialGPencilStyle.gradient` | GP 材质渐变 | Grease Pencil 材质插件 |
| `SpaceOutliner.show_users_column` / `sort_method` | 大纲用户列 / 排序方式 | 大纲 UI 插件 |
| `UILayout.label_markdown` | UI 渲染 Markdown 文本 | 帮助/文档类面板 |

### 🟡 5.3 High-Value New APIs (精选)

#### Python API 新增 (09-11 完整扫描 - 4 项新增，累计 50+ 项)

**🔥 最新新增（09-11）:**

| API | 说明 | 插件开发价值 |
|-----|------|----------|
| **RenderEngine.bl_write_viewport_depth** | 自定义渲染引擎写入视口深度缓冲 | 自定义渲染器插件 |
| **FileHandler.label_with_extensions** | 文件处理器显示带扩展名的标签 | 导入/导出插件 |
| **UILayout.label_markdown** | UI 布局中渲染 Markdown 格式文本 | UI 插件增强 |
| **CyclesPreferences.has_dlss_gpu_devices** | DLSS GPU 设备检测 | 渲染设置插件 |
| **CyclesRenderSettings.preview_denoising_upscale_quality** | 预览降噪升级质量 | 渲染控制插件 |
| **RegionView3D.use_view_flip_x** | 视口水平翻转 | 视口控制插件 |
| **SpaceNodeOverlay.show_text_info** | 节点叠加层文本信息 | 节点编辑器插件 |

**📋 之前扫描的高价值新增（插件开发必备）:**

| API | 说明 | 插件开发价值 |
|-----|------|----------|
| **Project API** | `BlendData.project` / `project_init()` / `project_clear()` | 项目管理插件 |
| `Preferences.use_project_auto_save` | 项目自动保存设置 | 项目管理集成 |
| **Render Pause/Resume** | `RenderEngine.view_pause()` / `view_resume()` | 渲染控制插件 |
| `RegionView3D.pause_render` / `support_pause_render` | 视口渲染暂停 | 视口控制插件 |
| `CYCLES.view_pause` / `view_resume` | Cycles 渲染暂停 | 渲染控制插件 |
| **Scene Compositor Effects** | `Scene.compositor_effects` | 场景级合成效果 |
| `CompositorNodeTree.allow_usage_in_scene_compositor_effect` | 允许节点树用于场景合成 | 合成插件 |
| **ID deep_hash** | `ID.deep_hash` 基于内容的哈希 | 数据块去重/缓存 |
| **Outliner 11 细粒度过滤器** | `use_filter_object_materials/modifiers/constraints/shape_keys/vertex_groups/data/animation` + `use_filter_bone_collections/pose_bones/grease_pencil_effects` | 大纲视图插件 |
| **⚠️ Outliner 过滤器重命名** | `use_sort_alpha` → 10 个 `use_filter_*` 属性（破坏性变更！） | 大纲插件迁移 |
| `UILayout.template_compositor_strip_inputs` | 合成器 Strip 输入模板 | VSE 插件 |
| `UILayout.template_scene_compositor_effects` | 场景合成效果模板 | 合成 UI 插件 |
| `RegionView3D.view_camera_roll` | 相机旋转控制 | 相机控制插件 |
| `Window.global_areas` | 全局区域访问 | 窗口管理插件 |

**📦 Asset Library 增强 (09-07 新发现):**

| API | 说明 | 插件开发价值 |
|-----|------|----------|
| `UserAssetLibrary.auth_token` | 资产库认证令牌 | 在线资产库插件 |
| `UserAssetLibrary.use_auth_token` | 启用认证 | 在线资产库插件 |
| `UserAssetLibrary.uuid` / `invalid_uuid` | 资产库 UUID | 资产库管理 |
| `UserAssetLibrary.is_project_defined` | 项目定义的资产库 | 项目资产管理 |
| `AssetMetaData.webpage` | 资产网页链接 | 资产浏览器插件 |

**🎨 Brush 增强 (09-07 新发现):**

| API | 说明 | 插件开发价值 |
|-----|------|----------|
| `Brush.curve_auto_smooth` | 自动平滑曲线 | 笔刷插件 |
| `Brush.curve_hardness` | 硬度曲线 | 笔刷插件 |
| `Brush.curve_spacing` | 间距曲线 | 笔刷插件 |
| `Brush.use_unified_color` | 统一颜色 | 笔刷插件 |
| `Brush.use_unified_size` | 统一尺寸 | 笔刷插件 |
| `BrushCapabilitiesSculpt.has_tip_roundness` | 笔尖圆润度能力 | 雕刻插件 |

**🔧 其他新增 (09-07 扫描):**

| API | 说明 | 插件开发价值 |
|-----|------|----------|
| `Object.convert_rotation_mode()` | 旋转模式转换 | 动画插件 |
| `PoseBone.convert_rotation_mode()` | 骨骼旋转模式转换 | 动画插件 |
| `ViewLayerEEVEE.denoising_store_passes` | 降噪存储通道 | EEVEE 渲染插件 |
| `ViewLayerEEVEE.denoising_pass_use_albedo_roughness_weighting` | 降噪权重 | EEVEE 渲染插件 |
| `PreferencesEdit.clamp_strips_by_default` | VSE Strip 默认限制 | VSE 插件 |
| `PreferencesEdit.default_strip_length` | VSE 默认 Strip 长度 | VSE 插件 |
| `PreferencesSystem.use_rt_shadows` | 光线追踪阴影 | 渲染设置插件 |
| `Region.search_filter` | 区域搜索过滤 | UI 插件 |
| `ToolSettings.use_transform_data_pivot` | 变换数据枢轴 | 变换工具插件 |
| `Collection.importer` | 集合导入器 | 导入插件 |
| `CollectionImport.filepath` | 导入文件路径 | 导入插件 |
| `Scene.wrap_timeline_navigation` | 时间线循环导航 | 动画插件 |
| `SpaceDopeSheetEditor.cache_compositor` | 合成缓存 | 动画/合成插件 |
| `RenderSettings.use_compositor_frames_cache` | 合成帧缓存 | 渲染插件 |
| `SceneEEVEE.time_limit` | EEVEE 时间限制 | EEVEE 渲染插件 |
| `SpaceOutliner.expand_on_focus` | 大纲展开行为 | 大纲 UI 插件 |
| `SpaceProperties.show_properties_compositor` | 显示合成属性 | 属性 UI 插件 |
| `BrushGpencilSettings.use_cyclic_stroke` | Grease Pencil 循环笔触 | GP 笔刷插件 |
| `PointCloud.type` | 点云类型属性 | 点云数据处理插件 |

**🆕 最新新增 (09-23 扫描 - 8 项):**

| API | 说明 | 插件开发价值 |
|-----|------|----------|
| `CollectionChild.sort_index` | 集合子对象排序索引 | 集合管理插件 |
| `CollectionObject.sort_index` | 集合对象排序索引 | 集合管理插件 |
| `CollectionObject.parented_sort_index` | 集合对象父级排序索引 | 集合管理插件 |
| `ColorManagedInputColorspaceSettings.interop_id` | 输入色彩空间互操作ID | 色彩管理插件 |
| `ColorManagedSequencerColorspaceSettings.interop_id` | 序列编辑器色彩空间互操作ID | 色彩管理/序列编辑器插件 |
| `CompositorNodeConvertColorSpace.from_interop_id` | 色彩空间转换节点源互操作ID | 合成节点插件 |
| `CompositorNodeConvertColorSpace.to_interop_id` | 色彩空间转换节点目标互操作ID | 合成节点插件 |
| `SpaceOutliner.sort_method` | 大纲排序方法 | 大纲 UI 插件 |

#### Geometry Nodes 新增 (09-06 扫描)
| 节点/功能 | 说明 | 插件开发价值 |
|-----------|------|----------|
| **Combine List** | 合并多个列表 | 列表数据处理增强 |
| **Get Vector Component** | 通过整数索引获取 x/y/z 分量 | 向量操作简化 |
| **Rasterize Points** | 将点转换为栅格（光栅化） | 点云→网格转换 |
| **Deactivate Voxels** | 从体积栅格中移除活动体素 | 体积数据处理 |
| **Grid Topology Boolean** | 活动栅格体素的布尔运算 | 体积建模 |
| **NURBS input nodes** | NURBS 输入节点组 | NURBS 曲线控制 |
| Curve to Mesh "Miter Scale" | 斜接缩放选项 | 曲线转网格控制 |
| Curve to Tube "Miter Scale" | 斜接缩放选项 | 管道建模 |
| Realize Instances "Preserve Normals" | 保留负变换行列式实例的法线 | 实例化处理 |
| GP data input nodes | Grease Pencil 数据输入节点 | GP 数据处理 |
| Grid sampling modes | 改进的二次/三次采样模式 | 栅格采样质量 |

### 完整变更记录

详见工作区知识库 `references/api.md` 与 `references/changelog.md`

---
