# Facetory MCP 工作流参考

## 连接与发现

Facetory 通常在 `http://127.0.0.1:39093/mcp` 提供 Streamable HTTP。优先使用已安装的 MCP 工具和资源；仅在连接器缺失或异常时运行随附诊断脚本。

从服务器读取以下资源，不依赖记忆：

- `facetory://document/current`：活动状态、画布、主题、数量、健康状态、脏状态和精确版本。
- `facetory://capabilities`：当前设备规格和策略限制。
- `facetory://guide/watchface-authoring`：当前领域模型和安全流程。
- `facetory://schema/query-v1`：支持的精确版本查询。
- `facetory://recipe/aod`、`facetory://recipe/export`：当前 AOD/导出约束。

需要完整实体数据时列出资源模板。常见版本化 URI：

```text
facetory://document/{version}/manifest
facetory://document/{version}/themes?limit=50
facetory://document/{version}/themes/{themeId}
facetory://document/{version}/themes/{themeId}/layers?limit=50
facetory://document/{version}/resources?themeId={themeId}&limit=50
facetory://document/{version}/resources/{resourceId}
facetory://document/{version}/assets?limit=50
facetory://document/{version}/validation?limit=20
```

对路径 ID 做百分号编码；在 `nextCursor` 为 null 前保留游标继续读取。

## 工具路由

- `facetory.data_sources.search`：发现可选的小米数据源 ID。
- `facetory.assets.import.plan`：创建可复用的图片、序列、字体或文件资源，不放置图层。
- `facetory.watchface.compose.plan`：创建可见文本、图片、数据元素，或唯一一个 AOD 克隆。
- `facetory.watchface.edit.plan`：移动、排序、隐藏、绑定、替换、删除或设置支持的数据资源样式。
- `facetory.plan.apply`：只应用一次已审核计划。
- `facetory.watchface.review`：验证并渲染精确版本/主题。
- `facetory.project.save`：原位保存已有标题的项目，不等同于另存为。
- `facetory.export.plan`：在允许的规范目标路径预检 Xiaomi BIN/MWZ。

## 新增元素流程

1. 读取当前版本并选择精确主题。
2. 必要时搜索数据源。
3. 使用明确布局和尺寸 Compose 1–4 个元素。
4. 检查 `effects.bindings` 和校验结果。
5. 应用一次。
6. 读取并检查返回的新版本。
7. 需要精确属性时查询新建资源。
8. 保存。

## 修改已有元素流程

1. 查询目标主题图层。
2. 查询每个引用资源，不根据名称猜样式。
3. 在服务器上限内规划一个原子编辑批次。
4. 检查稳定 ID 和目标主题。
5. 应用一次、复查并保存。

## 素材流程

使用规范绝对路径和可选的小写 SHA-256 校验。导入计划会暂存文件并在应用时重新验证身份。若 Facetory 无法读取共享存储，仅在获得明确 root 授权后把所需单个文件复制到应用私有 Projects 目录，再在 MCP 调用中使用 `/data/data/com.astralsight.facetory/...`；实测版本可能不接受等价的 `/data/user/0/...` 拼写。

## 检查与导出

使用代表性 `dataContext` 检查每个主题。返回 PNG 未显示动态文本时，同时核对编辑器画布。导出预检可能执行普通 MCP Review 不包含的设备专属 AOD 调色板/通道检查。在 UI 修改作者、标题、表盘 ID 或其他导出元数据后，重新读取当前版本，因为这些操作会推进不透明版本。
