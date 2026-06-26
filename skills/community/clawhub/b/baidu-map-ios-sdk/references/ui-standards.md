# 地图 UI 标准

**边界**：检索、路线、选点、弹窗、视野、Logo 等 UI 规范；开发者无特殊要求时按此实现，具体功能见各功能文档。

## 基础规范

| 规范 | 标准 |
|------|------|
| 触控区域 | 可点击元素最小 44×44pt，保证单指易点 |
| 安全区域 | 尊重 Safe Area，刘海屏顶部预留约 44pt |
| 栅格 | 间距、尺寸优先用 8 的倍数（8、16、24、32pt），便于多倍屏 |
| 页边距 | 左右 16～24pt，避开屏幕边缘 |
| 字体 | 优先系统字体；标题 17～19pt、正文 15～16pt、辅助 12～14pt |
| 圆角 | 面板 12pt、输入框 8pt、胶囊按钮 height/2 |
| 一致性 | 相似功能元素样式一致；重要内容放上半屏偏左 |

---

## 检索面板

| 属性 | 标准值 |
|------|--------|
| 背景 | 浅灰 (0.96, 0.97, 0.98)，起终点输入框内为白色 |
| 圆角 | 12pt |
| 阴影 | 轻微阴影 |
| 边距 | 距屏幕左右 16pt |
| 布局顺序 | 起终点检索框在上，算路方式在下 |

---

## 地点检索（Sug）

| 属性 | 标准值 |
|------|--------|
| 防抖 | 输入延迟约 0.25s 再发起检索 |
| 关键字长度 | ≥2 再发起检索 |
| 主标题 | 优先 key，否则 address |
| 副标题 | address、城市+区、tag |
| 背景 | 白色、圆角 12pt |
| 分隔线 | 左侧留空约 50pt |
| 单元格 | 15pt 字体、深灰文字 |
| 布局对齐 | 检索框与结果列表同水平边距（16pt）；左侧图标区约 50pt，文字起始对齐 |
| 行前图标 | 每行结果前可加地点 pin 图标（如 SF Symbol mappin.circle.fill），居中于 50pt 区域 |
| 性能 | 延后 `becomeFirstResponder` 至下一 RunLoop；避免在 viewDidAppear 中自定义 searchBar 内部结构 |
| 提示条文案 | 宜简短，如「以下结果超过200米，请确认」，避免冗长占空间 |
| 键盘避让 | 键盘弹出时列表**必须**做避让（如监听 UIKeyboardWillShow/Hide，设置 tableView.contentInset.bottom = 键盘高度），避免结果被键盘遮挡 |
| 列表文案 | 副标题单行截断；出入口标签可去掉冗余「选择」等字，仅保留名称与比例等关键信息；子节点（出入口）**优先显示 showName（简称）**，无则用 name，见 [search.md](search.md) |

**Sug 与无经纬度首条**：Sug 第一条可能为无经纬度的关键词联想（如输入「肯」出「肯德基」），不对应确切 POI。**不过滤**该条；用户点击时将其作为**关键词填入检索框并继续 Sug 检索**，而非选点。无结果时可用 POI 检索继续搜。详见 [search.md](search.md)。

---

## 路线规划

### 起终点输入框

| 属性 | 标准值 |
|------|--------|
| 起点标识 | 左侧浅蓝圆点 (0.35, 0.65, 0.95) 或绿色 (0.2, 0.8, 0.4) |
| 终点标识 | 左侧橙红圆点 (0.95, 0.3, 0.25) |
| 占位符 | 「输入起点」「输入终点」 |
| 样式 | 无边框、白色背景、圆角 8pt |
| 字体 | 15pt 系统字体 |
| 位置 | 检索面板顶部 |

### 算路方式选择器

| 属性 | 标准值 |
|------|--------|
| 形式 | UIScrollView + 胶囊按钮（水平滚动） |
| 选项 | 驾车 \| 步行 \| 骑行（可扩展公交、新能源等） |
| 选中样式 | 科技蓝背景 (0, 0.55, 0.95)、白字 |
| 未选样式 | 白底、深灰字 (0.3, 0.3, 0.35) |
| 高度 | 36pt，圆角 = height/2（胶囊形） |
| 位置 | 检索框下边 |

### 路线规划布局

- **检索面板**：起终点输入在上，算路方式在下；可隐藏主标题、整体上移以扩大地图可视区
- **底部栏**：路线详情、模拟行驶按钮置于屏幕底部；总里程时间卡片在按钮上方，有路线时显示
- **自动算路**：起终点都有值后直接算路；切换算路方式后直接算路；重选起终点后按当前算路方式算路；算路方式默认驾车
- **模拟导航**：点击「模拟行驶」可跳转至独立模拟导航页，全屏展示路线与小车动画，提供「返回」「停止模拟」操作
- **可选**：详情按钮、骑行类型切换（普通/电动车）

### 公交多方案

TableView 展示每条方案的时长、距离、换乘概要；选中后绘制路线并适配视野。

---

## 配色（地图科技感）

路线规划相关采用蓝色系，适配地图场景与科技感：

| 用途 | RGB（0～1） | 说明 |
|------|-------------|------|
| 路线详情按钮 | 白底 + 浅蓝描边 (0.4, 0.7, 1.0) + 科技蓝字；无路线时禁用 | 描边样式 |
| 模拟行驶（可用） | (0, 0.55, 0.95) | 科技蓝 |
| 模拟行驶（禁用） | (0.9, 0.93, 0.96) | 浅蓝灰 |
| 停止模拟 | (0.95, 0.35, 0.2) | 橙红 |
| 算路方式选中项 | (0, 0.55, 0.95) | 科技蓝 |
| 算路方式未选 | 白底 + 深灰字 (0.3, 0.3, 0.35) | — |

起终点圆点：起点浅蓝 (0.35, 0.65, 0.95) 或绿 (0.2, 0.8, 0.4)，终点橙红 (0.95, 0.3, 0.25)。

---

## 按钮

| 按钮 | 样式 |
|------|------|
| 路线详情 | 白底、浅蓝描边、蓝色文字；胶囊圆角；有路线时可用，点击跳转路线详情页 |
| 模拟行驶（可用） | 科技蓝背景、白字；胶囊圆角；点击跳转模拟导航页 |
| 模拟行驶（禁用） | 浅蓝灰背景、半透明白字 |
| 停止模拟 | 橙红背景、白字（在模拟导航页） |
| 字体 | 16pt Medium |

## 总里程时间卡片

| 属性 | 标准值 |
|------|--------|
| 位置 | 底部栏内、按钮上方 |
| 背景 | 白色、圆角 12pt、轻微阴影 |
| 时长 | 大号粗体 20pt，如「22小时54分」 |
| 里程 | 13pt 浅灰，如「2185公里」 |
| 路线类型 | 12pt 浅灰，如「驾车」「步行」「骑行」 |
| 显示时机 | 有路线时显示 |

---

## 地图选点

| 属性 | 标准值 |
|------|--------|
| 布局 | 地图占上半部分，底部 TableView 约 160pt |
| 列表行高 | 约 75pt |
| 第一行 | 逆地理 address（可加【】标题） |
| 后续行 | poiList 中的 POI（name、address、pt） |
| 选点动画 | regionWillChange 标注跳起，regionDidChange 落下 |

---

## 隐私协议弹窗

| 属性 | 标准值 |
|------|--------|
| 时机 | 首次使用前弹窗，用户同意后调用 `setAgreePrivacy:YES` |
| 记录 | NSUserDefaults 避免重复弹窗 |
| 未同意 | 检索对象延迟创建；使用检索前提示用户同意 |
| 隐私政策 | 弹窗内可跳转，地址见 project-config |

---

## 起终点与覆盖物

| 属性 | 标准值 |
|------|--------|
| 起终点图标 | 添加顺序：路线→起终点→小车；**须优先使用** [assets](assets.md) 的 **icon_start、icon_end**，无纹理时再自绘/纯色；scaleX/scaleY 根据实际图片尺寸与地图 zoomLevel 做视觉适配 |
| 路线纹理 | **须优先使用** BMKPolylineView.textureImage（图片宽高 2 的 n 次幂）或 BMKMultiTexturePolylineView+路况纹理；无纹理时再用 strokeColor。线宽 8pt。 |
| 路线小车纹理 | **必须优先使用**技能 [assets](assets.md) 提供的纹理（icon_car / car_triangle / track_car）；无纹理时才用颜色或自绘 |
| 算路页 | 不添加 carMarker，polyline.animation = nil，静态展示 |
| 路线线宽 | 8pt |
| 路名字体 | 22pt，黑字白边；路线路名**使用 BMKTextPathMarker** 沿路径绘制，见 [overlays.md](overlays.md) |
| 拐角 | 圆角 |

---

## 路线视野适配（必须考虑）

有路线绘制时**必须**做视野适配。**仅用 fitVisibleMapRect 的 edgePadding**，与 mapPadding 分开（mapPadding 管 Logo/指南针）。

| 场景 | edgePadding |
|------|-------------|
| 路线全屏 | 上下约 80、左右约 40 |
| 标注可见 | 左右约 50、上下约 40 |
| 路线规划 | 顶部留检索面板+50+marker 尺寸，底部留底部栏+20+marker 尺寸，左右约 50+marker 尺寸 |
| marker 预留 | 起终点图标约 44pt，fitVisibleMapRect 的 edgePadding 需预留，避免被 UI 遮挡 |

---

## 地图 Logo、指南针与 mapPadding（Logo 不能被遮挡）

**mapPadding** 与 **fitVisibleMapRect edgePadding** 解决不同问题，勿混用：

| 用途 | 方法 | 说明 |
|------|------|------|
| 指南针、Logo 遮挡 | `setMapPadding` | 影响指南针、Logo、比例尺位置，使其避开 UI 区域 |
| 路线视野适配 | `fitVisibleMapRect:edgePadding:` | 控制路线、起终点在可见区域内的适配，含 UI 边距和 marker 尺寸 |

百度地图 Logo **不可移除、不允许遮挡**，有地图且存在浮动栏/底部栏时**必须**通过 setMapPadding 预留边界。当有浮动栏时，用 `setMapPadding` 预留边界；**底部预留尽量小**（如 barH + 4），使 Logo 更靠下、避免喧宾夺主：

```objc
// 顶部预留检索面板，底部预留尽量小使 Logo 更靠下
[_mapView setMapPadding:UIEdgeInsetsMake(topPad, 0, barH + 4, 0)];
```

---

## Logo 与比例尺布局

**默认问题**：比例尺与 Logo 同在左下角时会重叠，需手动设置 `mapScaleBarPosition` 使比例尺在 Logo 上方。

**SDK 内部**（updateLogoPosition）：Logo 在内容区 `(mapW, mapH)` 内布局；LeftBottom 时全面屏 `logoOrigin = (mapW*0.05, mapH - logoH - mapH*0.03)`，非全面屏 `(0, mapH - logoH)`；最终 frame 加 `mapPadding.left/top`。

**推荐实现**：`logoPosition = BMKLogoPositionLeftBottom`，在 `mapViewDidFinishLoading` 与 `viewDidLayoutSubviews` 中调用 `layoutScaleBarAboveLogo`：

```objc
- (void)layoutScaleBarAboveLogo {
    if (!self.mapView) return;
    UIEdgeInsets pad = self.mapView.mapPadding;
    CGFloat mapW = CGRectGetWidth(self.mapView.bounds) - pad.left - pad.right;
    CGFloat mapH = CGRectGetHeight(self.mapView.bounds) - pad.top - pad.bottom;
    CGFloat logoX = mapW * 0.05;   // 与 SDK LeftBottom 全面屏一致
    CGFloat logoH = 28;
    CGFloat logoBottomMargin = mapH * 0.03;
    CGFloat logoTop = mapH - logoH - logoBottomMargin;
    CGSize scaleSize = self.mapView.mapScaleBarSize;
    if (scaleSize.height <= 0) scaleSize.height = 22;
    CGFloat gap = 6;
    CGFloat y = logoTop - scaleSize.height - gap;
    if (y < 8) y = 8;
    CGFloat x = pad.left + logoX;  // 比例尺左边与 Logo 左边对齐
    self.mapView.mapScaleBarPosition = CGPointMake(x, y);
}
```

---

## 手势与 ScrollView

地图嵌入横向 ScrollView（如 Tab 切换）时，多手势同时识别；ScrollView 关闭 delaysContentTouches 便于响应。

---

## 3D 与动画

| 场景 | 标准值 |
|------|--------|
| 3D 模型展示 | zoomLevel 18、overlooking -30、关闭 3D 楼块 |
| 算路页 | 路线和小车无动画，静态展示；polyline.animation = nil，不添加 carMarker |
| 模拟行驶页 | 路线纹理已走过置灰、未走过原色；小车沿轨迹动画 |

---

## 按参考 UI 图严格写布局（通用提示词）

有参考 UI 图时，可用以下要求约束大模型，避免实现过于简单或不美观：

1. **像素级对齐**：边距、圆角、字号、行高须与图中一致或按比例换算（有设计稿标注时写出换算规则）。
2. **视觉层级**：区分主标题 / 副标题 / 辅助文字的字重、字号、颜色；按钮、卡片、分割线要有明确层级和对比。
3. **禁止简化**：图中的阴影、圆角、描边、图标、留白都要体现，不用「简单列表」「普通按钮」敷衍。
4. **配色与风格**：从图中提取主色、辅色、背景色、边框色并用常量命名；整页风格统一（如科技感 / 简约）。
5. **输出要求**：先列出从图中读出的关键尺寸和样式（边距、圆角、字号、颜色），再写代码；代码中禁止魔法数字，须用有意义的常量或设计 token。

**简短版提示词**（可放入系统提示或规则）：

> 按参考 UI 图严格实现：边距/圆角/字号/颜色与图一致；区分标题与正文层级；保留阴影、描边、图标等细节；禁止简化或「差不多就行」；尺寸和颜色用命名常量，不写魔法数字。

**避免的说法**：❌「参考一下这个图」❌「风格类似即可」❌「做一个简单的 XXX 页面」  
**建议的说法**：✅「严格按照附图实现，边距、圆角、字号、颜色与图一致」✅「先列出从图中提取的尺寸和配色，再写布局代码」

---

## 使用说明

- 开发者有自定义 UI 需求时，可偏离此标准
- 本技能生成代码时，默认采用上述标准，保证界面专业统一
