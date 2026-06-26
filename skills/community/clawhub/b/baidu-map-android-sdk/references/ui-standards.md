# 地图 UI 与交互约定

**边界**：检索、路线、选点、弹窗、视野、Logo、布局结构等 UI 规范；开发者无特殊要求时按此实现，具体功能见各功能文档。

## 布局结构

### 常见布局模式

| 模式 | 结构 | 适用场景 |
|------|------|----------|
| 上栏 + 地图 | 根 LinearLayout 垂直：上方输入/筛选区（wrap_content 或固定高度） + MapView（layout_height="match_parent" 或 0dp weight=1） | 路线规划起终点输入、POI 检索城市+关键字、地图类型切换 |
| 地图 + 底栏 | 根 FrameLayout/RelativeLayout：MapView 全屏，底部 LinearLayout（alignParentBottom，固定高度如 200dp）放列表/详情/按钮 | POI 结果列表、路线详情、开始导航 |
| 全屏地图 + 浮动控件 | 根 RelativeLayout：MapView fill_parent，Button/LinearLayout 用 layout_alignParentTop/Right/Bottom + margin 叠在地图上 | 路线节点浏览（上/下一个）、自定义图标、图例 |

### 根容器与 MapView

- **LinearLayout 垂直**：上栏 + MapView 时，MapView 用 `android:layout_height="0dp"` + `android:layout_weight="1"` 占满剩余高度，避免被挤压。
- **RelativeLayout**：底栏用 `android:layout_alignParentBottom="true"`，MapView 与底栏同层且 `layout_above="@id/xxx"` 或底栏在布局顺序上后写即可叠在上层；浮动按钮用 `layout_alignParentRight` + `layout_marginRight`、`layout_alignParentBottom` + `layout_marginBottom` 等。
- **FrameLayout**：MapView 先写占满，再写底部面板（layout_gravity="bottom"），面板需设固定或最大高度，避免盖满地图。
- MapView 必须设 `android:clickable="true"`（或代码 setClickable）以便接收触摸。

### 面板高度建议

| 区域 | 建议 | 说明 |
|------|------|------|
| 顶部单行输入/筛选 | 约 48～56dp | 与触控最小 48dp 一致，多行可 wrap_content 或固定 |
| 底部结果列表 | 约 160～240dp | 可固定 200dp 或占屏比例（如 30%），留出地图视野 |
| 底部单行按钮栏 | 约 56～72dp | 含内边距；若有总里程/时长卡片，卡片在上、按钮在下 |

### setViewPadding 与 Logo

- **含义**：`mBaiduMap.setViewPadding(left, top, right, bottom)` 为地图**可操作与绘制区域**预留内边距，Logo、比例尺、缩放控件、指南针会避开该区域，避免被底部栏/侧栏遮挡。
- **时机**：需在地图加载完成后设置才生效，在 `OnMapLoadedCallback.onMapLoaded()` 中调用，或在地图已显示后（如 onResume 后延迟）设置。
- **取值**：底部有栏时，bottom 设为栏高或「栏高 + 8dp」；左侧/右侧有固定侧栏时按实际宽度设 left/right。
- **与 fitBounds 的 padding 区分**：`setViewPadding` 管的是地图控件与 Logo 的布局；`MapStatusUpdateFactory.newLatLngBounds(bounds, paddingLeft, paddingTop, paddingRight, paddingBottom)` 的四个参数是**视野适配时**四周预留的像素，用于算路/POI 后让路线或点落在可视区内且不贴边。二者可同时使用，勿混用概念。

```java
// 地图加载完成后设置，避免 Logo 被底栏遮挡
mBaiduMap.setOnMapLoadedCallback(() -> {
    int padBottom = (int) (200 * getResources().getDisplayMetrics().density); // 与底栏高度一致
    mBaiduMap.setViewPadding(0, 0, 0, padBottom);
});
```

### 在 MapView 上叠加子 View

- MapView 支持 `addView(child, MapViewLayoutParams)`，用于在图上固定位置叠放说明、图例等。
- `MapViewLayoutParams.Builder()`：`layoutMode(ELayoutMode.absoluteMode)`、`width/height`、`point(Point)`、`align(ALIGN_LEFT, ALIGN_BOTTOM)` 等，确定子 View 的尺寸与对齐方式；对齐基准为 point，常用 `new Point(0, mapView.getHeight())` 配 `ALIGN_LEFT|ALIGN_BOTTOM` 表示左下角。
- 底部预留区域若用 padding 实现，子 View 的 bottom 对齐时高度应 ≤ paddingBottom，否则会压住 Logo。

### 视野适配（fitBounds）

- 算路或 POI 展示后，用 `LatLngBounds.Builder().include(...).include(...).build()` 构造 bounds，再 `MapStatusUpdateFactory.newLatLngBounds(bounds, width, height)` 或 `newLatLngBounds(bounds, paddingLeft, paddingTop, paddingRight, paddingBottom)` 使路线/点落在可视区内。
- 有底部面板时，用四参数版本并设 paddingBottom 为面板高度，避免路线被面板挡住；Overlay 的 `zoomToSpanPaddingBounds(padding, padding, padding, bottomPadding)` 即此用法，见 [route.md](route.md)、[search.md](search.md)。

## 基础规范

| 规范 | 标准 |
|------|------|
| 触控区域 | 可点击元素最小 48×48dp（Material 推荐），保证单指易点 |
| 安全区域 | 尊重 WindowInsets / 状态栏与导航栏，刘海屏预留足够边距 |
| 栅格 | 间距、尺寸优先用 8 的倍数（8、16、24、32dp），便于多密度 |
| 页边距 | 左右 16～24dp，避开屏幕边缘 |
| 字体 | 标题 18～20sp、正文 14～16sp、辅助 12sp；优先使用 Theme 中 textAppearance |
| 圆角 | 卡片/面板 12dp、输入框 8dp、胶囊按钮 radius = height/2 |
| 一致性 | 相似功能样式一致；重要内容放上半屏、主操作易达 |

## 检索与路线面板

| 属性 | 标准值 |
|------|--------|
| 背景 | 浅灰（如 `#F5F5F5`），输入框内白色 |
| 圆角 | 12dp |
| 边距 | 距屏幕左右 16dp，与地图留出间隙 |
| 布局顺序 | 起终点输入在上，算路方式（驾车/步行/骑行/公交）在下 |
| 起终点标识 | 起点左侧绿色或浅蓝圆点，终点左侧橙红圆点；占位符「输入起点」「输入终点」 |
| 算路方式 | 水平排列（RadioGroup / ChipGroup / 横向 RecyclerView），选中项主题色背景、白字，未选白底深灰字 |

## 地点检索（Sug）

| 属性 | 标准值 |
|------|--------|
| 防抖 | 输入延迟约 300ms 再发起检索 |
| 关键字长度 | ≥2 再发起检索 |
| 主标题 | 优先 name/key，否则 address |
| 副标题 | address、区县、tag |
| 列表 | 白色背景、圆角 12dp；行高约 56dp；左侧可加 pin 图标 |
| 边距 | 与检索框水平边距一致（16dp） |

## 路线规划行为

- **自动算路**：起终点都有值后自动算路；切换算路方式后重新算路；默认驾车。
- **底部栏**：路线详情、开始导航等按钮置于底部；总里程/时长卡片在按钮上方，有路线时显示。
- **视野**：算路完成后用 `MapStatusUpdateFactory.newLatLngBounds(bounds, padding)` 或类似方式适配路线与起终点在可视区内，预留边距避免被面板遮挡。

## 地图 Logo 与 padding

- 百度地图 **Logo 不可移除、不可遮挡**。有底部栏或浮动面板时，用 `mBaiduMap.setViewPadding(left, top, right, bottom)` 预留区域，使 Logo、比例尺、指南针落在可显示范围内。
- **setViewPadding** 与 **fitBounds 的 padding** 区分：前者管地图内容与 Logo/控件布局，后者管视野适配时预留的边距；勿混用。
- 底部 padding 尽量小（如 栏高 + 8dp），避免地图被压缩过多。

## 隐私协议弹窗

| 属性 | 标准值 |
|------|--------|
| 时机 | 首次使用前弹窗，用户同意后调用 `setAgreePrivacy(context, true)` |
| 记录 | SharedPreferences 等避免重复弹窗 |
| 未同意 | 检索/路线等对象延迟创建；使用前提示用户同意 |
| 隐私政策 | 弹窗内可点击跳转（如 lbsyun.baidu.com 开放平台隐私条款） |

## 地图选点

- 地图占上半部分，底部列表展示逆地理结果与 POI 列表；选点后地图可居中到该点并更新列表。
- 列表行高约 56～72dp；第一行可为逆地理 address，后续为 POI（name、address）。

## 使用说明

- 开发者有自定义 UI 需求时可偏离此约定。
- 本技能生成界面相关代码时，默认采用上述约定，保证风格统一、易用。
