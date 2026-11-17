# blender-mcp-plus 工具清单（28）

所有工具经 MCP 客户端调用，最终通过 `localhost:9876` 作用于正在运行的 Blender。
除注明外均无需参数即可列出能力；调用前确认 Blender 已打开且官方 MCP 插件已启用。

## 官方 Blender Lab 工具（26）

### 代码执行

| 工具 | 说明 |
|---|---|
| `execute_blender_code` | 在当前 Blender 会话执行任意 `bpy` Python 代码。最通用，建模/材质/动画/批量处理都靠它 |
| `execute_blender_code_for_cli` | 后台（无界面）Blender 实例执行代码。适合批处理/CI；需要 `BLENDER_PATH` |

### 工程体检（各含 `_for_cli` 后台版本）

| 工具 | 说明 |
|---|---|
| `get_blendfile_summary_datablocks` | 数据块总览（物体/材质/贴图/集合等计数） |
| `get_blendfile_summary_missing_files` | 缺失的外部文件清单 |
| `get_blendfile_summary_of_linked_libraries` | 链接库信息 |
| `get_blendfile_summary_path_info` | 工程路径信息 |
| `get_blendfile_summary_usage_guess` | 工程用途推测 |

### 场景读取

| 工具 | 说明 |
|---|---|
| `get_objects_summary` | 场景物体摘要（名称/类型/变换） |
| `get_object_detail_summary` | 单个物体完整细节（修改器/材质/网格数据） |

### 文档检索（内置 Blender Python API 参考与用户手册 RST 全文）

| 工具 | 说明 |
|---|---|
| `get_python_api_docs` | 按标识符取 API 文档 |
| `search_api_docs` | 全文检索 Python API |
| `search_manual_docs` | 全文检索用户手册 |

### 观察与渲染

| 工具 | 说明 |
|---|---|
| `get_screenshot_of_window_as_image` | 整个 Blender 窗口截图 |
| `get_screenshot_of_area_as_image` | 指定区域（如 3D 视图）截图 |
| `get_screenshot_of_window_as_json` | 窗口结构化信息（非图像） |
| `render_viewport_to_path` | 渲染视口到文件（EEVEE/Cycles 按工程设置） |
| `render_thumbnail_to_path` | 渲染缩略图 |

### 视图导航

| 工具 | 说明 |
|---|---|
| `jump_to_view3d_object_by_name` | 3D 视图聚焦到指定物体 |
| `jump_to_view3d_object_data_by_name` | 聚焦到物体数据 |
| `jump_to_tab_by_name` | 切换到指定标签页 |
| `jump_to_tab_by_space_type` | 按空间类型切换标签页 |

## 本仓库新增（2）：Poly Haven 资产库

免费 CC0 资产（500+ 模型、HDRI、贴图），**无需 API key**，按下载量排序。

### search_assets

| 参数 | 取值 | 说明 |
|---|---|---|
| `query` | 字符串 | 搜索关键词 |
| `asset_type` | `models` / `hdris` / `textures` / `all` | 资产类型，默认 `all` |
| `category` | 字符串 | 分类过滤 |
| `limit` | 整数 | 返回数量 |
| `min_size_m` | 浮点 | 最小真实世界尺寸（米） |

### import_asset

| 参数 | 取值 | 说明 |
|---|---|---|
| `id` | 字符串 | Poly Haven 资产 ID（如 `ArmChair_01`，来自搜索结果） |
| `asset_type` | `models` / `hdris` / `textures` | 类型 |
| `resolution` | `1k` / `2k` / `4k` / `8k` | 贴图/HDRI 分辨率 |
| `target_size` | 浮点（米） | 模型导入后缩放到的目标尺寸 |
| `apply_to` | 字符串 | 贴图材质赋给的目标物体名 |
| `strength` | 浮点 | HDRI 环境光强度（默认 1.0） |

行为：模型下载 glTF 导入（可缩放）；HDRI 下载 EXR/HDR 设为世界环境；
贴图下载 diffuse 图并新建材质赋给目标物体。

## 工具选用建议

- **不确定怎么做** → `execute_blender_code`（先 `get_objects_summary` 了解场景）
- **要做视觉验证** → `get_screenshot_of_area_as_image` 或 `render_viewport_to_path`
- **查 Blender API 用法** → `search_api_docs` / `search_manual_docs`（本地内置，快且全）
- **要免费资产** → `search_assets` 找到 ID → `import_asset` 导入
- **批处理/无人值守** → `*_for_cli` 系列（需 `BLENDER_PATH`）

## 已知限制

- 官方插件 socket 无鉴权，仅 localhost；不要转发端口
- `execute_blender_code` 有任意代码执行权限，不可信 `.blend` 不要打开执行
- HDRI/贴图下载需要联网（Poly Haven）；模型导入走 glTF
