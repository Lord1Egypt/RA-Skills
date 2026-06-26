---
outline: deep
---
 # Types


## GeoJSONFeatureI

**`表示一个GeoJSON要素的接口`**<br>

Type: <span>[GeoJSONFeatureI][1]</span>

### Examples

```javascript
GeoJSON.Feature<
 GeoJSON.Geometry & (GeoJSON.Point | GeoJSON.LineString | GeoJSON.Polygon),
 GeoJSON.GeoJsonProperties
>
```

## FearureType

**`基础要素类型`**

Type: <span>(`"circle"` | `"polygon"` | `"polyline"` | `"polygonExtrusion"` | `"symbol"` | `"heatmap"`)</span>

## CapitalizeStr

**`将字符串的第一个字母转换为大写字母`**

Type: <span>[CapitalizeStr][2]</span>

### Examples

```javascript
type CapitalizeStr<Str extends string> =
   Str extends `${infer First}-${infer Rest}`
     ? `${First}${Capitalize<CapitalizeStr<Rest>>}`
     : Str
```

## CapitalizeKey

**`将对象的键的第一个字母转换为大写字母`**

Type: <span>[CapitalizeKey][3]</span>

### Examples

```javascript
type CapitalizeKey<obj extends object> = {
 [Key in keyof obj as CapitalizeStr<Key & string>]: obj[Key]
}
```

## PluginStatus

**`插件状态`**

Type: <span>(`"unavailable"` | `"loading"` | `"loaded"` | `"error"`)</span>

## LngLatLike

**`经度和纬度`**

Type: <span>(\[[number][4], [number][4]] | [LngLat][5] | {lng: [number][4], lat: [number][4]} | {lon: [number][4], lat: [number][4]})</span>

## LngLatBoundsLike

**`经纬度范围`**

Type: <span>([LngLatBounds][6] | \[[LngLatLike][7], [LngLatLike][7]] | \[[number][4], [number][4], [number][4], [number][4]])</span>

## PointLike

**`点`**

Type: <span>([Point][8] | \[[number][4], [number][4]])</span>

## Offset

**`偏移量`**

Type: <span>([number][4] | [PointLike][9] | {: [PointLike][9]})</span>

## ExpressionName

**`表达式名称`**

Type: <span>(`"array"` | `"boolean"` | `"collator"` | `"format"` | `"literal"` | `"number"` | `"number-format"` | `"object"` | `"string"` | `"image"` | `"to-boolean"` | `"to-color"` | `"to-number"` | `"to-string"` | `"typeof"` | `"feature-state"` | `"geometry-type"` | `"id"` | `"line-progress"` | `"properties"` | `"at"` | `"get"` | `"has"` | `"in"` | `"index-of"` | `"length"` | `"slice"` | `"!"` | `"!="` | `"<"` | `"<="` | `"=="` | `">"` | `">="` | `"all"` | `"any"` | `"case"` | `"match"` | `"coalesce"` | `"within"` | `"interpolate"` | `"interpolate-hcl"` | `"interpolate-lab"` | `"step"` | `"let"` | `"var"` | `"concat"` | `"downcase"` | `"is-supported-script"` | `"resolved-locale"` | `"upcase"` | `"rgb"` | `"rgba"` | `"to-rgba"` | `"-"` | `"*"` | `"/"` | `"%"` | `"^"` | `"+"` | `"abs"` | `"acos"` | `"asin"` | `"atan"` | `"ceil"` | `"cos"` | `"e"` | `"floor"` | `"ln"` | `"ln2"` | `"log10"` | `"log2"` | `"max"` | `"min"` | `"pi"` | `"round"` | `"sin"` | `"sqrt"` | `"tan"` | `"zoom"` | `"heatmap-density"`)</span>

## Expression

**`表达式`**

Type: <span>\[[ExpressionName][10], ...[Array][11]\<any>]</span>

## Anchor

**`锚点`**

Type: <span>(`"center"` | `"left"` | `"right"` | `"top"` | `"bottom"` | `"top-left"` | `"top-right"` | `"bottom-left"` | `"bottom-right"`)</span>

## DragPanOptions

**`拖拽平移选项`**

Type: <span>{linearity: [number][4]?, easing: function (t: [number][4]): [number][4]?, deceleration: [number][4]?, maxSpeed: [number][4]?}</span>

### Properties

*   `linearity` **[number][4]?**&#x20;
*   `easing` **function (t: [number][4]): [number][4]?**&#x20;
*   `deceleration` **[number][4]?**&#x20;
*   `maxSpeed` **[number][4]?**&#x20;

## InteractiveOptions

**`交互选项`**

Type: <span>{around: `"center" | "auto"`?}</span>

### Properties

*   `around` **(`"center" | "auto"`)?**&#x20;

## MapboxOptions

**`Mapbox选项`**

### Properties

*   `container` **([string][15] | [HTMLElement][16])** 地图容器
*   `style` **([Style][21] | [string][15] | [undefined][13]) 样式
*   `antialias` **([boolean][12] | [undefined][13])?** 是否开启抗锯齿
*   `attributionControl` **([boolean][12] | [undefined][13])?** 是否开启属性控制
*   `bearing` **([number][4] | [undefined][13])?** 地图旋转角度
*   `bearingSnap` **([number][4] | [undefined][13])?** 地图旋转角度的吸附值
*   `bounds` **([LngLatBoundsLike][14] | [undefined][13])?** 地图的边界
*   `boxZoom` **([boolean][12] | [undefined][13])?** 是否开启框选缩放
*   `center` **([LngLatLike][7] | [undefined][13])?** 地图中心点
*   `clickTolerance` **([number][4] | [undefined][13])?** 点击容差
*   `collectResourceTiming` **([boolean][12] | [undefined][13])?** 是否收集资源时间
*   `crossSourceCollisions` **([boolean][12] | [undefined][13])?** 是否允许跨源碰撞

*   `cooperativeGestures` **[boolean][12]??** 是否启用协作手势
*   `customAttribution` **([string][15] | [Array][11]<[string][15]> | [undefined][13])?** 自定义属性
*   `dragPan` **([boolean][12] | [DragPanOptions][17] | [undefined][13])?** 是否启用拖拽平移
*   `dragRotate` **([boolean][12] | [undefined][13])?** 是否启用拖拽旋转
*   `doubleClickZoom` **([boolean][12] | [undefined][13])?** 是否启用双击缩放
*   `hash` **([boolean][12] | [string][15] | [undefined][13])?** 是否启用hash
*   `fadeDuration` **([number][4] | [undefined][13])?** 淡入淡出时间
*   `failIfMajorPerformanceCaveat` **([boolean][12] | [undefined][13])?** 是否在性能严重下降时停止渲染
*   `fitBoundsOptions` **([FitBoundsOptions][18] | [undefined][13])?** fitBounds选项
*   `interactive` **([boolean][12] | [undefined][13])?** 是否启用交互
*   `keyboard` **([boolean][12] | [undefined][13])?** 是否启用键盘
*   `localFontFamily` **([string][15] | [undefined][13])?** 本地字体族
*   `localIdeographFontFamily` **([string][15] | [undefined][13])?** 本地表意字字体族
*   `maxBounds` **([LngLatBoundsLike][14] | [undefined][13])?** 最大边界
*   `maxPitch` **([number][4] | [undefined][13])?** 最大俯仰角
*   `maxZoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `minPitch` **([number][4] | [undefined][13])?** 最小俯仰角
*   `minZoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `optimizeForTerrain` **([boolean][12] | [undefined][13])?** 是否优化地形
*   `preserveDrawingBuffer` **([boolean][12] | [undefined][13])?** 是否保留绘图缓冲区
*   `pitch` **([number][4] | [undefined][13])?** 俯仰角
*   `projection` **[Projection][19]??** 投影方式
*   `pitchWithRotate` **([boolean][12] | [undefined][13])?** 是否随旋转而俯仰
*   `refreshExpiredTiles` **([boolean][12] | [undefined][13])?** 是否刷新过期瓦片
*   `renderWorldCopies` **([boolean][12] | [undefined][13])?** 是否渲染世界复制品
*   `scrollZoom` **([boolean][12] | [InteractiveOptions][20] | [undefined][13])?** 是否启用滚轮缩放
*   `trackResize` **([boolean][12] | [undefined][13])?** 是否跟踪调整大小
*   `transformRequest` **([TransformRequestFunction][22] | [undefined][13])?** 转换请求函数
*   `touchZoomRotate` **([boolean][12] | [InteractiveOptions][20] | [undefined][13])?** 是否启用触摸缩放旋转
*   `touchPitch` **([boolean][12] | [InteractiveOptions][20] | [undefined][13])?** 是否启用触摸俯仰
*   `zoom` **([number][4] | [undefined][13])?** 缩放级别
*   `maxTileCacheSize` **([number][4] | [undefined][13])?** 最大瓦片缓存大小
*   `accessToken` **([string][15] | [undefined][13])?** 访问令牌
*   `testMode` **([boolean][12] | [undefined][13])?** 是否测试模式
*   `worldview` **([string][15] | [undefined][13])?** 世界视角
*   `showCollisionBoxes` **([boolean][12] | [undefined][13])?** 是否显示碰撞盒

## quat

**`四元数`**

Type: <span>[Array][11]<[number][4]></span>

## vec3

**`三维向量`**

Type: <span>[Array][11]<[number][4]></span>

## FreeCameraOptions

**`自由相机选项`**

### constructor

**`创建FreeCameraOptions的实例`**

#### Parameters

*   `position` **[MercatorCoordinate][23]??**&#x20;
*   `orientation` **[quat][24]??**&#x20;

### position

**`相机位置`**

Type: <span>([MercatorCoordinate][23] | [undefined][13])</span>

### lookAtPoint

**`将相机视角转向某个点`**

#### Parameters

*   `location` **[LngLatLike][7]**&#x20;
*   `up` **[vec3][25]??**&#x20;

Returns **void**&#x20;

### setPitchBearing

**`设置相机的俯仰角和方位角`**

#### Parameters

*   `pitch` **[number][4]**&#x20;
*   `bearing` **[number][4]**&#x20;

Returns **void**&#x20;

## ResourceType

**`资源类型`**

Type: <span>(`"Unknown"` | `"Style"` | `"Source"` | `"Tile"` | `"Glyphs"` | `"SpriteImage"` | `"SpriteJSON"` | `"Image"`)</span>

## RequestParameters

**`请求参数`**

### Properties

*   `url` **[string][15]**&#x20;
*   `credentials` **(`"same-origin"` | `"include"` | [undefined][13])?**&#x20;
*   `method` **(`"GET"` | `"POST"` | `"PUT"` | [undefined][13])?**&#x20;
*   `collectResourceTiming` **([boolean][12] | [undefined][13])?**&#x20;

## TransformRequestFunction

**`将请求参数转换为资源类型`**

Type: <span>function (url: [string][15], resourceType: [ResourceType][26]): [RequestParameters][27]</span>

## PaddingOptions

**`边距选项`**

### Properties

*   `top` **[number][4]**&#x20;
*   `bottom` **[number][4]**&#x20;
*   `left` **[number][4]**&#x20;
*   `right` **[number][4]**&#x20;

## FeatureIdentifier

**`要素标识符`**

### Properties

*   `id` **([string][15] | [number][4] | [undefined][13])?**&#x20;
*   `source` **[string][15]**&#x20;
*   `sourceLayer` **([string][15] | [undefined][13])?**&#x20;

## BoxZoomHandler

**`框选缩放处理器`**

### constructor

**`创建BoxZoomHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### isEnabled

**`是否启用`**

Returns **[boolean][12]**&#x20;

### isActive

**`是否激活`**

Returns **[boolean][12]**&#x20;

### enable

**`启用框选缩放`**

Returns **void**&#x20;

### disable

**`禁用框选缩放`**

Returns **void**&#x20;

## ScrollZoomHandler

**`滚轮缩放处理器`**

### constructor

**`创建ScrollZoomHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### enable

**`启用滚轮缩放`**

#### Parameters

*   `options` **[InteractiveOptions][20]??**&#x20;

Returns **void**&#x20;

### disable

**`禁用滚轮缩放`**

Returns **void**&#x20;

### setZoomRate

**`设置缩放速率`**

#### Parameters

*   `zoomRate` **[number][4]**&#x20;

Returns **void**&#x20;

### setWheelZoomRate

**`设置滚轮缩放速率`**

#### Parameters

*   `wheelZoomRate` **[number][4]**&#x20;

Returns **void**&#x20;

## DragPanHandler

**`拖拽平移处理器`**

### constructor

**`创建DragPanHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### isActive

**`判断是否激活`**

Returns **[boolean][12]**&#x20;

### enable

**`启用拖拽平移`**

#### Parameters

*   `options` **[DragPanOptions][17]??**&#x20;

Returns **void**&#x20;

### disable

**`禁用拖拽平移`**

Returns **void**&#x20;

## DragRotateHandler

**`拖拽旋转处理器`**

### constructor

**`创建DragRotateHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;
*   `options` **{bearingSnap: ([number][4] | [undefined][13])?, pitchWithRotate: ([boolean][12] | [undefined][13])?}?**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### isActive

**`判断是否激活`**

Returns **[boolean][12]**&#x20;

### enable

**`启用拖拽旋转`**

Returns **void**&#x20;

### disable

**`禁用拖拽旋转`**

Returns **void**&#x20;

## KeyboardHandler

**`处理键盘事件的处理器`**

### constructor

**`创建KeyboardHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### enable

**`启用键盘事件处理`**

Returns **void**&#x20;

### disable

**`禁用键盘事件处理`**

Returns **void**&#x20;

### isActive

**`判断是否激活`**

Returns **[boolean][12]**&#x20;

### disableRotation

**`禁用旋转`**

Returns **void**&#x20;

### enableRotation

**`启用旋转`**

Returns **void**&#x20;

## DoubleClickZoomHandler

**`处理双击缩放的处理器`**

### constructor

**`创建DoubleClickZoomHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### enable

**`启用双击缩放`**

Returns **void**&#x20;

### disable

**`禁用双击缩放`**

Returns **void**&#x20;

## TouchZoomRotateHandler

**`处理触摸缩放和旋转的处理器`**

### constructor

**`创建TouchZoomRotateHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### enable

**`启用触摸缩放和旋转`**

#### Parameters

*   `options` **[InteractiveOptions][20]??**&#x20;

Returns **void**&#x20;

### disable

**`禁用触摸缩放和旋转`**

Returns **void**&#x20;

### disableRotation

**`禁用旋转`**

Returns **void**&#x20;

### enableRotation

**`启用旋转`**

Returns **void**&#x20;

## TouchPitchHandler

**`触摸倾斜处理器`**

### constructor

**`创建TouchPitchHandler的实例`**

#### Parameters

*   `map` **[Map][28]**&#x20;

### enable

**`启用触摸倾斜`**

#### Parameters

*   `options` **[InteractiveOptions][20]??**&#x20;

Returns **void**&#x20;

### isActive

**`判断是否激活`**

Returns **[boolean][12]**&#x20;

### isEnabled

**`判断是否启用`**

Returns **[boolean][12]**&#x20;

### disable

**`禁用触摸倾斜`**

Returns **void**&#x20;

## IControl

**`控件接口`**

### Properties

*   `onAdd` **[Function][29]**&#x20;
*   `onRemove` **[Function][29]**&#x20;
*   `getDefaultPosition` **[Function][29]?**&#x20;

## Control

**`控件`**<br>
继承[Evented][30] <br>
实现[IControl][31]

### onAdd

**`添加控件`**

#### Parameters

*   `map` **[Map][28]**&#x20;

Returns **[HTMLElement][16]**&#x20;

### onRemove

**`移除控件`**

#### Parameters

*   `map` **[Map][28]**&#x20;

Returns **void**&#x20;

### getDefaultPosition

**`获取默认位置`**

Type: <span>(function (): [string][15] | [undefined][13])</span>

## PositionOptions

**`位置选项`**

### enableHighAccuracy

**`是否启用高精度`**

Type: <span>([boolean][12] | [undefined][13])?</span>

### timeout

**`超时时间`**

Type: <span>([number][4] | [undefined][13])?</span>

### maximumAge

**`最大缓存时间`**

Type: <span>([number][4] | [undefined][13])?</span>

## FullscreenControlOptions

**`全屏控制选项`**

### Properties

*   `container` **([HTMLElement][16] | null | [undefined][13])?**&#x20;

## PopupOptions

**`弹出框选项`**

### Properties

*   `closeButton` **([boolean][12] | [undefined][13])?** 是否显示关闭按钮
*   `closeOnClick` **([boolean][12] | [undefined][13])?** 是否在点击地图时关闭弹出框
*   `closeOnMove` **([boolean][12] | [undefined][13])?** 是否在移动地图时关闭弹出框
*   `focusAfterOpen` **([boolean][12] | null | [undefined][13])?** 是否在打开弹出框后聚焦
*   `anchor` **([Anchor][32] | [undefined][13])?** 锚点
*   `offset` **([Offset][33] | null | [undefined][13])?** 偏移量
*   `className` **([string][15] | [undefined][13])?** 类名
*   `maxWidth` **([string][15] | [undefined][13])?** 最大宽度

## Style

**`样式`**

### Properties

*   `layers` **[Array][11]<[AnyLayer][34]>** 图层
*   `sources` **[Sources][35]** 数据源
*   `bearing` **([number][4] | [undefined][13])?** 旋转角度
*   `center` **([Array][11]<[number][4]> | [undefined][13])?** 中心点坐标
*   `fog` **([Fog][36] | [undefined][13])?** 雾效
*   `glyphs` **([string][15] | [undefined][13])?** 字体图标
*   `metadata` **any?** 元数据
*   `name` **([string][15] | [undefined][13])?** 名称
*   `pitch` **([number][4] | [undefined][13])?** 俯仰角度
*   `light` **([Light][37] | [undefined][13])?** 光照
*   `sprite` **([string][15] | [undefined][13])?** 精灵图
*   `terrain` **([TerrainSpecification][38] | [undefined][13])?** 地形
*   `transition` **([Transition][39] | [undefined][13])?** 过渡
*   `version` **[number][4]** 版本
*   `zoom` **([number][4] | [undefined][13])?** 缩放等级

## Transition

**`过渡`**

### Properties

*   `delay` **([number][4] | [undefined][13])?** 延迟时间
*   `duration` **([number][4] | [undefined][13])?** 持续时间

## Light

**`光照`**

### Properties

*   `anchor` **((`"map"` | `"viewport"` | [undefined][13]))?** 锚点
*   `position` **([Array][11]<[number][4]> | [undefined][13])?** 位置
*   `position-transition` **([Transition][39] | [undefined][13])?** 位置过渡
*   `color` **([string][15] | [undefined][13])?** 颜色
*   `color-transition` **([Transition][39] | [undefined][13])?** 颜色过渡
*   `intensity` **([number][4] | [undefined][13])?** 强度
*   `intensity-transition` **([Transition][39] | [undefined][13])?** 强度过渡

## Fog

**`雾`**

### Properties

*   `color` **([string][15] | [Expression][40] | [undefined][13])?** 雾的颜色
*   `horizon-blend` **([number][4] | [Expression][40] | [undefined][13])?** 地平线混合
*   `range` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 范围

## Sources

**`数据源`**

## PromoteIdSpecification

**`ID提升规范`**

Type: <span>({: [string][15]} | [string][15])</span>

## AnySourceData

**`数据源`**

Type: <span>([GeoJSONSourceRaw][41] | [VideoSourceRaw][42] | [ImageSourceRaw][43] | [CanvasSourceRaw][44] | [VectorSource][45] | [RasterSource][46] | [RasterDemSource][47] | [CustomSourceInterface][48]<([HTMLImageElement][49] | ImageData | ImageBitmap)>)</span>

## VectorSourceImpl

**Extends VectorSource**

**`矢量数据源`**<br>
继承[VectorSource][45]

### Properties

*   `setTiles` **[Function][29]** 设置瓦片
*   `setUrl` **[Function][29]** 设置URL

## AnySourceImpl

**`任意数据源`**

Type: <span>([GeoJSONSource][50] | [VideoSource][51] | [ImageSource][52] | [CanvasSource][53] | [VectorSourceImpl][54] | [RasterSource][46] | [RasterDemSource][47] | [CustomSource][55]<([HTMLImageElement][49] | ImageData | ImageBitmap)>)</span>

## Source

**`数据源`**

### Properties

*   `type` **(`"vector"` | `"raster"` | `"raster-dem"` | `"geojson"` | `"image"` | `"video"` | `"canvas"` | `"custom"`)** 数据源类型

## GeoJSONSourceRaw

**Extends Source, GeoJSONSourceOptions**

**`GeoJSON数据源`**<br>
继承[GeoJSONSourceOptions][56] <br>
实现[Source][57]

### Properties

*   `type` **(`"geojson"`)** 数据源类型

## GeoJSONSource

**`GeoJSON数据源`**<br>
实现[GeoJSONSourceRaw][41]

### type

**`数据源类型`**

Type: <span>`"geojson"`</span>

### constructor

**`构造函数`**

#### Parameters

*   `options` **[GeoJSONSourceOptions][56]??**&#x20;

### setData

**`设置数据`**

#### Parameters

*   `data` **(GeoJSON.Feature\<GeoJSON.Geometry> | GeoJSON.FeatureCollection\<GeoJSON.Geometry> | [String][15])**&#x20;

Returns **this**&#x20;

### getClusterExpansionZoom

**`获取聚合扩展缩放级别`**

#### Parameters

*   `clusterId` **[number][4]**&#x20;
*   `callback` **function (error: any, zoom: [number][4]): void**&#x20;

Returns **this**&#x20;

### getClusterChildren

**`获取聚合子元素`**

#### Parameters

*   `clusterId` **[number][4]**&#x20;
*   `callback` **function (error: any, features: [Array][11]\<GeoJSON.Feature\<GeoJSON.Geometry>>): void**&#x20;

Returns **this**&#x20;

### getClusterLeaves

**`获取聚合叶子元素`**

#### Parameters

*   `cluserId` **[number][4]**&#x20;
*   `limit` **[number][4]**&#x20;
*   `offset` **[number][4]**&#x20;
*   `callback` **function (error: any, features: [Array][11]\<GeoJSON.Feature\<GeoJSON.Geometry>>): void**&#x20;

Returns **this**&#x20;

## GeoJSONSourceOptionsData

**`GeoJSON数据源选项`**

Type: <span>(GeoJSON.Feature\<GeoJSON.Geometry> | GeoJSON.FeatureCollection\<GeoJSON.Geometry> | GeoJSON.Geometry | [string][15] | [undefined][13])</span>

### Examples

```javascript
type GeoJSONSourceOptionsData =
 | GeoJSON.Feature<GeoJSON.Geometry>
 | GeoJSON.FeatureCollection<GeoJSON.Geometry>
 | GeoJSON.Geometry
 | string
 | undefined
```

## GeoJSONSourceOptions

**`GeoJSON数据源选项`**

### Properties

*   `data` **([GeoJSONSourceOptionsData][58])?** 数据
*   `maxzoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `attribution` **([string][15] | [undefined][13])?** 版权信息
*   `buffer` **([number][4] | [undefined][13])?** 缓冲区大小
*   `tolerance` **([number][4] | [undefined][13])?** 容差
*   `cluster` **([number][4] | [boolean][12] | [undefined][13])?** 是否聚合
*   `clusterRadius` **([number][4] | [undefined][13])?** 聚合半径
*   `clusterMaxZoom` **([number][4] | [undefined][13])?** 聚合最大缩放级别
*   `clusterMinPoints` **([number][4] | [undefined][13])?** 聚合最小点数
*   `clusterProperties` **([object][59] | [undefined][13])?** 聚合属性
*   `lineMetrics` **([boolean][12] | [undefined][13])?** 是否计算线路度量
*   `generateId` **([boolean][12] | [undefined][13])?** 是否生成ID
*   `promoteId` **([PromoteIdSpecification][60] | [undefined][13])?** ID提升规范
*   `filter` **any??** 过滤器

## VideoSourceRaw

**Extends Source, VideoSourceOptions**

**`视频数据源`**<br>
继承[VideoSourceOptions][61] <br>
继承[Source][57]

### Properties

*   `type` **(`"video"`)** 数据源类型

## VideoSource

**`视频数据源`** <br>
实现[VideoSourceRaw][42]

### type

**`数据源类型`**

Type: <span>`"video"`</span>

### constructor

**`创建VideoSource实例`**

#### Parameters

*   `options` **[VideoSourceOptions][61]??**&#x20;

### getVideo

**`获取HTMLVideoElement`**

Returns **[HTMLVideoElement][62]**&#x20;

### setCoordinates

**`设置坐标`**

#### Parameters

*   `coordinates` **[Array][11]<[Array][11]<[number][4]>>**&#x20;

Returns **this**&#x20;

## VideoSourceOptions

**`视频数据源选项`**

### Properties

*   `urls` **([Array][11]<[string][15]> | [undefined][13])?** 视频地址

## ImageSourceRaw

**Extends Source, ImageSourceOptions**

**`图片数据源`** <br>
继承[ImageSourceOptions][63] <br>
继承[Source][57]

### Properties

*   `type` **(`"image"`)** 数据源类型

## ImageSource

**`图片数据源`** <br>
实现[ImageSourceRaw][43]

### type

**`数据源类型`**

Type: <span>`"image"`</span>

### constructor

**`创建ImageSource实例`**

#### Parameters

*   `options` **[ImageSourceOptions][63]??**&#x20;

### updateImage

**`更新图片`**

#### Parameters

*   `options` **[ImageSourceOptions][63]**&#x20;

Returns **this**&#x20;

### setCoordinates

**`设置坐标`**

#### Parameters

*   `coordinates` **[Array][11]<[Array][11]<[number][4]>>**&#x20;

Returns **this**&#x20;

## ImageSourceOptions

**`图片数据源选项`**

### Properties

*   `url` **([string][15] | [undefined][13])?** 图片地址

## CanvasSourceRaw

**Extends Source, CanvasSourceOptions**

**`画布数据源`** <br>
继承[Source][57]
继承[CanvasSourceOptions][64]

### Properties

*   `type` **(`"canvas"`)** 数据源类型

## CanvasSource

**`画布数据源`** <br>
实现[CanvasSourceRaw][44]

### type

**`数据源类型`**

Type: <span>`"canvas"`</span>

### coordinates

**`坐标`**

Type: <span>[Array][11]<[Array][11]<[number][4]>></span>

### canvas

**`画布元素`**

Type: <span>([string][15] | [HTMLCanvasElement][65])</span>

### play

**`播放画布`**

Returns **void**&#x20;

### pause

**`暂停画布`**

Returns **void**&#x20;

### getCanvas

**`获取HTMLCanvasElement`**

Returns **[HTMLCanvasElement][65]**&#x20;

### setCoordinates

**`设置坐标`**

#### Parameters

*   `coordinates` **[Array][11]<[Array][11]<[number][4]>>**&#x20;

Returns **this**&#x20;

## CanvasSourceOptions

**`画布数据源选项`**

### Properties

*   `animate` **([boolean][12] | [undefined][13])?** 是否动画
*   `canvas` **([string][15] | [HTMLCanvasElement][65])** 画布元素

## CameraFunctionSpecification

**`相机函数规范`**

Type: <span>({type: `"exponential"`, stops: [Array][11]<\[[number][4], T]>} | {type: `"interval"`, stops: [Array][11]<\[[number][4], T]>})</span>

## ExpressionSpecification

**`表达式规范`**

Type: <span>[Array][11]\<any></span>

## PropertyValueSpecification

**`属性值规范`**

Type: <span>(T | [CameraFunctionSpecification][66]\<T> | [ExpressionSpecification][67])</span>

## TerrainSpecification

**`地形规范`**

### Properties

*   `source` **[string][15]**&#x20;
*   `exaggeration` **[PropertyValueSpecification][68]<[number][4]>?**&#x20;

## SourceVectorLayer

**`用于矢量图层的源`**

Type: <span>{id: [string][15], fields: Record<[string][15], [string][15]>?, description: [string][15]?, minzoom: [number][4]?, maxzoom: [number][4]?, source: [string][15]?, source\_name: [string][15]?}</span>

### Properties

*   `id` **[string][15]**&#x20;
*   `fields` **Record<[string][15], [string][15]>?**&#x20;
*   `description` **[string][15]?**&#x20;
*   `minzoom` **[number][4]?**&#x20;
*   `maxzoom` **[number][4]?**&#x20;
*   `source` **[string][15]?**&#x20;
*   `source_name` **[string][15]?**&#x20;

## VectorSource

**`矢量源选项`**
继承[Source][57]

### Properties

*   `type` **(`"vector"`)** 数据源类型
*   `format` **(`"pbf"` | [undefined][13])?** 源格式
*   `url` **([string][15] | [undefined][13])?** 源URL
*   `id` **([string][15] | [undefined][13])?** 源ID
*   `name` **([string][15] | [undefined][13])?** 源名称
*   `tiles` **([Array][11]<[string][15]> | [undefined][13])?** 瓦片URL
*   `bounds` **([Array][11]<[number][4]> | [undefined][13])?** 边界
*   `scheme` **(`"xyz"` | `"tms"` | [undefined][13])?** 瓦片方案
*   `minzoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `maxzoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `attribution` **([string][15] | [undefined][13])?** 版权信息
*   `promoteId` **([PromoteIdSpecification][60] | [undefined][13])?** 提升ID规范
*   `vector_layers` **([Array][11]<[SourceVectorLayer][69]> | [undefined][13])?** 矢量图层

## RasterSource

**`栅格源`**
继承[Source][57]

### Properties

*   `name` **[string][15]?** 名称
*   `type` **(`"raster"`)** 数据源类型
*   `id` **[string][15]?** ID
*   `format` **(`"webp"` | [string][15])?** 格式
*   `url` **([string][15] | [undefined][13])?** URL
*   `tiles` **([Array][11]<[string][15]> | [undefined][13])?** 瓦片
*   `bounds` **([Array][11]<[number][4]> | [undefined][13])?** 边界
*   `minzoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `maxzoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `tileSize` **([number][4] | [undefined][13])?** 瓦片大小
*   `scheme` **(`"xyz"` | `"tms"` | [undefined][13])?** 瓦片方案
*   `attribution` **([string][15] | [undefined][13])?** 版权信息

## RasterDemSource

**`栅格DEM源`**
继承[Source][57]

### Properties

*   `name` **[string][15]?** 名称
*   `type` **(`"raster-dem"`)** 数据源类型
*   `id` **[string][15]?** ID
*   `url` **([string][15] | [undefined][13])?** URL
*   `tiles` **([Array][11]<[string][15]> | [undefined][13])?** 瓦片
*   `bounds` **([Array][11]<[number][4]> | [undefined][13])?** 边界
*   `minzoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `maxzoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `tileSize` **([number][4] | [undefined][13])?** 瓦片大小
*   `attribution` **([string][15] | [undefined][13])?** 版权信息
*   `encoding` **(`"terrarium"` | `"mapbox"` | [undefined][13])?** 编码

## CustomSourceInterface

**`自定义源`**

### Properties

*   `id` **[string][15]** ID
*   `type` **(`"custom"`)** 类型
*   `dataType` **(`"raster"`)** 数据类型
*   `minzoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `maxzoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `scheme` **([string][15] | [undefined][13])?** 瓦片方案
*   `tileSize` **([number][4] | [undefined][13])?** 瓦片大小
*   `attribution` **([string][15] | [undefined][13])?** 版权信息
*   `bounds` **(\[[number][4], [number][4], [number][4], [number][4]] | [undefined][13])?** 边界
*   `hasTile` **[Function][29]?** 是否有瓦片
*   `loadTile` **[Function][29]** 加载瓦片
*   `prepareTile` **[Function][29]?** 准备瓦片
*   `unloadTile` **[Function][29]?** 卸载瓦片
*   `onAdd` **[Function][29]?** 添加事件
*   `onRemove` **[Function][29]?** 移除事件

## CustomSource

**`自定义数据源`**
继承[Source][57]

### Properties

*   `id` **[string][15]** ID
*   `type` **(`"custom"`)** 类型
*   `scheme` **[string][15]** 瓦片方案
*   `minzoom` **[number][4]** 最小缩放级别
*   `maxzoom` **[number][4]** 最大缩放级别
*   `tileSize` **[number][4]** 瓦片大小
*   `attribution` **[string][15]** 版权信息
*   `_implementation` **[CustomSourceInterface][48]\<T>** 自定义数据源接口

## Alignment

**`对齐方式`**

Type: <span>(`"map"` | `"viewport"` | `"auto"`)</span>

## MarkerOptions

**`标记选项`**

### Properties

*   `element` **([HTMLElement][16] | [undefined][13])?** 标记元素
*   `offset` **([PointLike][9] | [undefined][13])?** 偏移量
*   `anchor` **([Anchor][32] | [undefined][13])?** 锚点
*   `color` **([string][15] | [undefined][13])?** 颜色
*   `draggable` **([boolean][12] | [undefined][13])?** 是否可拖拽
*   `clickTolerance` **([number][4] | null | [undefined][13])?** 点击容差
*   `rotation` **([number][4] | [undefined][13])?** 旋转角度
*   `rotationAlignment` **([Alignment][70] | [undefined][13])?** 旋转对齐方式
*   `pitchAlignment` **([Alignment][70] | [undefined][13])?** 倾斜对齐方式
*   `scale` **([number][4] | [undefined][13])?** 缩放比例

## EventedListener

**`事件监听器`**

Type: <span>function (object: [Object][59]): any</span>

## StyleOptions

**`样式选项`**

### Properties

*   `transition` **([boolean][12] | [undefined][13])?** 是否启用过渡效果

## MapboxGeoJSONFeature

Mapbox GeoJSON要素

Type: <span>[MapboxGeoJSONFeature][71]</span>

### Examples

```javascript
type MapboxGeoJSONFeature = GeoJSON.Feature<GeoJSON.Geometry> & {
 layer: Layer
 source: string
 sourceLayer: string
 state: { [key: string]: any }
}
```

## EventData

**`事件data`**

Type: <span>{: any}</span>

### Properties

*   `` **any**&#x20;

### Examples

```javascript
type EventData = { [key: string]: any }
```

## MapboxEvent

**`Mapbox事件`**

### type

**`事件类型`**

Type: <span>[string][15]</span>

### target

**`事件目标`**

Type: <span>[Map][28]</span>

### originalEvent

**`原始事件`**

Type: <span>TOrig</span>

## MapMouseEvent

**`地图鼠标事件`**
继承[MapboxEvent][72]

### type

**`鼠标事件类型`**

Type: <span>(`"mousedown"` | `"mouseup"` | `"click"` | `"dblclick"` | `"mousemove"` | `"mouseover"` | `"mouseenter"` | `"mouseleave"` | `"mouseout"` | `"contextmenu"`)</span>

### point

**`鼠标事件发生的点`**

Type: <span>[Point][8]</span>

### lngLat

**`鼠标事件发生的经纬度`**

Type: <span>[LngLat][5]</span>

### preventDefault

**`阻止默认行为`**

Returns **void**&#x20;

### defaultPrevented

**`是否阻止了默认行为`**

Type: <span>[boolean][12]</span>

## MapLayerMouseEvent

**`地图图层鼠标事件`**

Type: <span>[MapLayerMouseEvent][73]</span>

### Examples

```javascript
type MapLayerMouseEvent = MapMouseEvent & {
 features?: MapboxGeoJSONFeature[]
}
```

## MapTouchEvent

**`地图触摸事件`**
继承[MapboxEvent][72]

### type

**`触摸事件类型`**

Type: <span>(`"touchstart"` | `"touchend"` | `"touchcancel"`)</span>

### point

**`触摸事件发生的点`**

Type: <span>[Point][8]</span>

### lngLat

**`触摸事件发生的经纬度`**

Type: <span>[LngLat][5]</span>

### points

**`触摸事件发生的所有点`**

Type: <span>[Array][11]<[Point][8]></span>

### lngLats

**`触摸事件发生的所有经纬度`**

Type: <span>[Array][11]<[LngLat][5]></span>

### preventDefault

**`阻止默认行为`**

Returns **void**&#x20;

### defaultPrevented

**`是否阻止了默认行为`**

Type: <span>[boolean][12]</span>

## MapLayerTouchEvent

**`地图图层触摸事件`**

Type: <span>[MapLayerTouchEvent][74]</span>

### Examples

```javascript
type MapLayerTouchEvent = MapTouchEvent & {
 features?: MapboxGeoJSONFeature[]
}
```

## MapWheelEvent

**`地图滚轮事件`**
继承[MapboxEvent][72]

### type

**`滚轮事件类型`**

Type: <span>`"wheel"`</span>

### preventDefault

**`阻止默认行为`**

Returns **void**&#x20;

### defaultPrevented

**`是否阻止了默认行为`**

Type: <span>[boolean][12]</span>

## MapBoxZoomEvent

**`地图框选事件`**
继承[MapboxEvent][72]

### Properties

*   `type` **(`"boxzoomstart"` | `"boxzoomend"` | `"boxzoomcancel"`)** 框选事件类型
*   `boxZoomBounds` **[LngLatBounds][6]** 框选的经纬度范围

## MapDataEvent

**`地图数据事件`**

Type: <span>([MapSourceDataEvent][75] | [MapStyleDataEvent][76])</span>

## MapStyleDataEvent

**`地图样式数据事件`**
继承[MapboxEvent][72]

### Properties

*   `dataType` **(`"style"`)** 数据类型

## MapSourceDataEvent

**`地图源数据事件`**
继承[MapboxEvent][72]

### Properties

*   `dataType` **(`"source"`)** 数据类型
*   `isSourceLoaded` **[boolean][12]** 地图源是否已加载
*   `source` **[Source][57]** 地图源
*   `sourceId` **[string][15]** 地图源ID
*   `sourceDataType` **(`"metadata"` | `"content"`)** 数据类型
*   `tile` **any** 瓦片
*   `coord` **[Coordinate][77]** 坐标

## Coordinate

**`坐标`**

### Properties

*   `canonical` **[CanonicalCoordinate][78]** 规范化坐标
*   `wrap` **[number][4]** 包裹数
*   `key` **[number][4]** 坐标键

## CanonicalCoordinate

**`规范化坐标`**

### Properties

*   `x` **[number][4]** x坐标
*   `y` **[number][4]** y坐标
*   `z` **[number][4]** z坐标
*   `key` **[number][4]** 坐标键
*   `equals` **[Function][29]** 判断两个规范化坐标是否相等

## MapContextEvent

**`地图WebGL上下文事件`**
继承[MapboxEvent][72]

### Properties

*   `type` **(`"webglcontextlost"` | `"webglcontextrestored"`)** 事件类型

## ErrorEvent

**`地图错误事件`**
继承[MapboxEvent][72]

### type

**`事件类型`**

Type: <span>`"error"`</span>

### error

**`错误对象`**

Type: <span>[Error][79]</span>

## FilterOptions

**`用于过滤的选项`**

### Properties

*   `validate` **([boolean][12] | null | [undefined][13])?** 是否验证

## AnimationOptions

**`动画选项`**

### Properties

*   `duration` **([number][4] | [undefined][13])?** 持续时间
*   `easing` **[Function][29]?** 缓动函数
*   `offset` **([PointLike][9] | [undefined][13])?** 偏移量
*   `animate` **([boolean][12] | [undefined][13])?** 是否动画
*   `essential` **([boolean][12] | [undefined][13])?** 是否必要

## CameraOptions

**`相机选项`**

### Properties

*   `center` **([LngLatLike][7] | [undefined][13])?** 中心点
*   `zoom` **([number][4] | [undefined][13])?** 缩放级别
*   `bearing` **([number][4] | [undefined][13])?** 旋转角度
*   `pitch` **([number][4] | [undefined][13])?** 倾斜角度
*   `around` **([LngLatLike][7] | [undefined][13])?** 围绕点
*   `padding` **([number][4] | [PaddingOptions][80] | [undefined][13])?** 填充

## CameraForBoundsOptions

**`用于边界的相机选项`**
继承[CameraOptions][81]

### Properties

*   `offset` **([PointLike][9] | [undefined][13])?** 偏移量
*   `maxZoom` **([number][4] | [undefined][13])?** 最大缩放级别

## CameraForBoundsOptions

**`用于边界的相机选项`**<br>
继承[CameraOptions][81]

### Properties

*   `offset` **([PointLike][9] | [undefined][13])?** 偏移量
*   `maxZoom` **([number][4] | [undefined][13])?** 最大缩放级别

## CameraForBoundsResult

**`用于边界的相机结果`**

Type: <span>[CameraForBoundsResult][82]</span>

### Examples

```javascript
type CameraForBoundsResult = Required<
   Pick<CameraOptions, "zoom" | "bearing">
 > & {
   center: { lng: number; lat: number }
 }
```

## FlyToOptions

**`用于飞行动画的相机选项`** <br>
继承[AnimationOptions][83] <br>
继承[CameraOptions][81]

### Properties

*   `curve` **([number][4] | [undefined][13])?** 动画曲线的张力
*   `minZoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `speed` **([number][4] | [undefined][13])?** 动画速度
*   `screenSpeed` **([number][4] | [undefined][13])?** 屏幕速度
*   `maxDuration` **([number][4] | [undefined][13])?** 最大动画持续时间
*   `maxDuration` **([number][4] | [undefined][13])?** 最大动画持续时间

## EaseToOptions

**`用于缓动动画的相机选项`** <br>
继承[AnimationOptions][83] <br>
继承[CameraOptions][81]

### Properties

*   `delayEndEvents` **([number][4] | [undefined][13])?** 结束事件的延迟时间

## FitBoundsOptions

**`用于适应边界的相机选项`** <br>
继承[FlyToOptions][84]

### Properties

*   `linear` **([boolean][12] | [undefined][13])?** 是否使用线性过渡
*   `offset` **([PointLike][9] | [undefined][13])?** 相机偏移量
*   `maxZoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `maxDuration` **([number][4] | [undefined][13])?** 最大动画持续时间

## MapEventType

**`地图事件类型`**

Type: <span>{error: [ErrorEvent][85], load: [MapboxEvent][72], idle: [MapboxEvent][72], remove: [MapboxEvent][72], render: [MapboxEvent][72], resize: [MapboxEvent][72], webglcontextlost: [MapContextEvent][86], webglcontextrestored: [MapContextEvent][86], dataloading: [MapDataEvent][87], data: [MapDataEvent][87], tiledataloading: [MapDataEvent][87], sourcedataloading: [MapSourceDataEvent][75], styledataloading: [MapStyleDataEvent][76], sourcedata: [MapSourceDataEvent][75], styledata: [MapStyleDataEvent][76], boxzoomcancel: [MapBoxZoomEvent][88], boxzoomstart: [MapBoxZoomEvent][88], boxzoomend: [MapBoxZoomEvent][88], touchcancel: [MapTouchEvent][89], touchmove: [MapTouchEvent][89], touchend: [MapTouchEvent][89], touchstart: [MapTouchEvent][89], click: [MapMouseEvent][90], contextmenu: [MapMouseEvent][90], dblclick: [MapMouseEvent][90], mousemove: [MapMouseEvent][90], mouseup: [MapMouseEvent][90], mousedown: [MapMouseEvent][90], mouseout: [MapMouseEvent][90], mouseover: [MapMouseEvent][90], movestart: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>, move: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>, moveend: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>, zoomstart: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>, zoom: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>, zoomend: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>, rotatestart: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, rotate: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, rotateend: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, dragstart: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, drag: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, dragend: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, pitchstart: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, pitch: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, pitchend: [MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>, wheel: [MapWheelEvent][94]}</span>

### Properties

*   `error` **[ErrorEvent][85]**&#x20;
*   `load` **[MapboxEvent][72]**&#x20;
*   `idle` **[MapboxEvent][72]**&#x20;
*   `remove` **[MapboxEvent][72]**&#x20;
*   `render` **[MapboxEvent][72]**&#x20;
*   `resize` **[MapboxEvent][72]**&#x20;
*   `webglcontextlost` **[MapContextEvent][86]**&#x20;
*   `webglcontextrestored` **[MapContextEvent][86]**&#x20;
*   `dataloading` **[MapDataEvent][87]**&#x20;
*   `data` **[MapDataEvent][87]**&#x20;
*   `tiledataloading` **[MapDataEvent][87]**&#x20;
*   `sourcedataloading` **[MapSourceDataEvent][75]**&#x20;
*   `styledataloading` **[MapStyleDataEvent][76]**&#x20;
*   `sourcedata` **[MapSourceDataEvent][75]**&#x20;
*   `styledata` **[MapStyleDataEvent][76]**&#x20;
*   `boxzoomcancel` **[MapBoxZoomEvent][88]**&#x20;
*   `boxzoomstart` **[MapBoxZoomEvent][88]**&#x20;
*   `boxzoomend` **[MapBoxZoomEvent][88]**&#x20;
*   `touchcancel` **[MapTouchEvent][89]**&#x20;
*   `touchmove` **[MapTouchEvent][89]**&#x20;
*   `touchend` **[MapTouchEvent][89]**&#x20;
*   `touchstart` **[MapTouchEvent][89]**&#x20;
*   `click` **[MapMouseEvent][90]**&#x20;
*   `contextmenu` **[MapMouseEvent][90]**&#x20;
*   `dblclick` **[MapMouseEvent][90]**&#x20;
*   `mousemove` **[MapMouseEvent][90]**&#x20;
*   `mouseup` **[MapMouseEvent][90]**&#x20;
*   `mousedown` **[MapMouseEvent][90]**&#x20;
*   `mouseout` **[MapMouseEvent][90]**&#x20;
*   `mouseover` **[MapMouseEvent][90]**&#x20;
*   `movestart` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>**&#x20;
*   `move` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>**&#x20;
*   `moveend` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>**&#x20;
*   `zoomstart` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>**&#x20;
*   `zoom` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>**&#x20;
*   `zoomend` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [WheelEvent][93] | [undefined][13])>**&#x20;
*   `rotatestart` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `rotate` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `rotateend` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `dragstart` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `drag` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `dragend` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `pitchstart` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `pitch` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `pitchend` **[MapboxEvent][72]<([MouseEvent][91] | [TouchEvent][92] | [undefined][13])>**&#x20;
*   `wheel` **[MapWheelEvent][94]**&#x20;

## MapLayerEventType

**`地图图层事件类型`**

Type: <span>{click: [MapLayerMouseEvent][73], dblclick: [MapLayerMouseEvent][73], mousedown: [MapLayerMouseEvent][73], mouseup: [MapLayerMouseEvent][73], mousemove: [MapLayerMouseEvent][73], mouseenter: [MapLayerMouseEvent][73], mouseleave: [MapLayerMouseEvent][73], mouseover: [MapLayerMouseEvent][73], mouseout: [MapLayerMouseEvent][73], contextmenu: [MapLayerMouseEvent][73], touchstart: [MapLayerTouchEvent][74], touchend: [MapLayerTouchEvent][74], touchcancel: [MapLayerTouchEvent][74]}</span>

### Properties

*   `click` **[MapLayerMouseEvent][73]**&#x20;
*   `dblclick` **[MapLayerMouseEvent][73]**&#x20;
*   `mousedown` **[MapLayerMouseEvent][73]**&#x20;
*   `mouseup` **[MapLayerMouseEvent][73]**&#x20;
*   `mousemove` **[MapLayerMouseEvent][73]**&#x20;
*   `mouseenter` **[MapLayerMouseEvent][73]**&#x20;
*   `mouseleave` **[MapLayerMouseEvent][73]**&#x20;
*   `mouseover` **[MapLayerMouseEvent][73]**&#x20;
*   `mouseout` **[MapLayerMouseEvent][73]**&#x20;
*   `contextmenu` **[MapLayerMouseEvent][73]**&#x20;
*   `touchstart` **[MapLayerTouchEvent][74]**&#x20;
*   `touchend` **[MapLayerTouchEvent][74]**&#x20;
*   `touchcancel` **[MapLayerTouchEvent][74]**&#x20;

## AnyLayout

**`任意图层布局`**

Type: <span>([BackgroundLayout][95] | [FillLayout][96] | [FillExtrusionLayout][97] | [LineLayout][98] | [SymbolLayout][99] | [RasterLayout][100] | [CircleLayout][101] | [HeatmapLayout][102] | [HillshadeLayout][103] | [SkyLayout][104])</span>

## AnyPaint

**`任意图层绘制`**

Type: <span>([BackgroundPaint][105] | [FillPaint][106] | [FillExtrusionPaint][107] | [LinePaint][108] | [SymbolPaint][109] | [RasterPaint][110] | [CirclePaint][111] | [HeatmapPaint][112] | [HillshadePaint][113] | [SkyPaint][114])</span>

## Layer

**`地图图层`**

### Properties

*   `id` **[string][15]** 图层ID
*   `type` **[string][15]** 图层类型
*   `layout` **([AnyLayout][115] | [undefined][13])?** 图层布局
*   `paint` **([AnyPaint][116] | [undefined][13])?** 图层绘制
*   `ref` **[string][15]?** 引用
*   `source` **([string][15] | [AnySourceData][117] | [undefined][13])?** 数据源
*   `minzoom` **([number][4] | [undefined][13])?** 最小缩放级别
*   `maxzoom` **([number][4] | [undefined][13])?** 最大缩放级别
*   `interactive` **([boolean][12] | [undefined][13])?** 是否可交互
*   `filter` **([Array][11]\<any> | [undefined][13])?** 过滤器
*   `layout` **([AnyLayout][115] | [undefined][13])?** 图层布局
*   `paint` **([AnyPaint][116] | [undefined][13])?** 图层绘制

## BackgroundLayer

**`背景图层`**
继承[Layer][118]

### Properties

*   `type` **(`"background"`)** 图层类型
*   `layout` **([BackgroundLayout][95] | [undefined][13])?** 图层布局
*   `paint` **([BackgroundPaint][105] | [undefined][13])?** 图层绘制

## TCircleLayer

**`圆形图层`**
继承[Layer][118]

### Properties

*   `type` **(`"circle"`)** 图层类型
*   `layout` **([CircleLayout][101] | [undefined][13])?** 图层布局
*   `paint` **([CirclePaint][111] | [undefined][13])?** 图层绘制

## FillExtrusionLayer

**`填充拉伸图层`**
继承[Layer][118]

### Properties

*   `type` **(`"fill-extrusion"`)** 图层类型
*   `layout` **([FillExtrusionLayout][97] | [undefined][13])?** 图层布局
*   `paint` **([FillExtrusionPaint][107] | [undefined][13])?** 图层绘制

## FillLayer

**`填充图层`**
继承[Layer][118]

### Properties

*   `type` **(`"fill"`)** 图层类型
*   `layout` **([FillLayout][96] | [undefined][13])?** 图层布局
*   `paint` **([FillPaint][106] | [undefined][13])?** 图层绘制

## THeatmapLayer

**`热力图层`**
继承[Layer][118]

### Properties

*   `type` **(`"heatmap"`)** 图层类型
*   `layout` **([HeatmapLayout][102] | [undefined][13])?** 图层布局
*   `paint` **([HeatmapPaint][112] | [undefined][13])?** 图层绘制

## HillshadeLayer

**`遮蔽山地图层`**
继承[Layer][118]

### Properties

*   `type` **(`"hillshade"`)** 图层类型
*   `layout` **([HillshadeLayout][103] | [undefined][13])?** 图层布局
*   `paint` **([HillshadePaint][113] | [undefined][13])?** 图层绘制

## LineLayer

**`线图层`**
继承[Layer][118]

### Properties

*   `type` **(`"line"`)** 图层类型
*   `layout` **([LineLayout][98] | [undefined][13])?** 图层布局
*   `paint` **([LinePaint][108] | [undefined][13])?** 图层绘制

## TRasterLayer

**`栅格图层`**
继承[Layer][118]

### Properties

*   `type` **(`"raster"`)** 图层类型
*   `layout` **([RasterLayout][100] | [undefined][13])?** 图层布局
*   `paint` **([RasterPaint][110] | [undefined][13])?** 图层绘制

## TSymbolLayer

**`符号图层`**
继承[Layer][118]

### Properties

*   `type` **(`"symbol"`)** 图层类型
*   `layout` **([SymbolLayout][99] | [undefined][13])?** 图层布局
*   `paint` **([SymbolPaint][109] | [undefined][13])?** 图层绘制

## SkyLayer

**`天空图层`**
继承[Layer][118]

### Properties

*   `type` **(`"sky"`)** 图层类型
*   `layout` **([SkyLayout][104] | [undefined][13])?** 图层布局
*   `paint` **([SkyPaint][114] | [undefined][13])?** 图层绘制

## AnyLayer

**`任意图层`**

Type: <span>([BackgroundLayer][119] | [TCircleLayer][120] | [FillExtrusionLayer][121] | [FillLayer][122] | [THeatmapLayer][123] | [HillshadeLayer][124] | [LineLayer][125] | [TRasterLayer][126] | [TSymbolLayer][127] | [CustomLayerInterface][128] | [SkyLayer][129])</span>

## CustomLayerInterface

**`自定义图层接口`**

### Properties

*   `id` **[string][15]** 图层id
*   `type` **(`"custom"`)** 图层类型
*   `renderingMode` **(`"2d"` | `"3d"` | [undefined][13])?** 渲染模式
*   `onRemove` **[Function][29]?** 移除图层
*   `onAdd` **[Function][29]?** 添加图层
*   `prerender` **[Function][29]?** 预渲染
*   `render` **[Function][29]** 渲染

## StyleFunction

**`样式函数`**

### Properties

*   `property` **([string][15] | [undefined][13])?** 属性
*   `base` **([number][4] | [undefined][13])?** 基础
*   `type` **(`"identity"` | `"exponential"` | `"interval"` | `"categorical"` | [undefined][13])?** 类型
*   `default` **any?** 默认值
*   `colorSpace` **(`"rgb"` | `"lab"` | `"hcl"` | [undefined][13])?** 颜色空间

## Visibility

**`可见性`**

Type: <span>(`"visible"` | `"none"`)</span>

## Layout

**`布局`**

### Properties

*   `visibility` **([Visibility][130] | [undefined][13])?** 可见性

## BackgroundLayout

**`背景布局`**
继承[Layout][131]

## BackgroundPaint

**`背景画笔`**

### Properties

*   `background-color` **([string][15] | [Expression][40] | [undefined][13])?** 背景颜色
*   `background-color-transition` **([Transition][39] | [undefined][13])?** 背景颜色过渡
*   `background-pattern` **([string][15] | [undefined][13])?** 背景图案
*   `background-pattern-transition` **([Transition][39] | [undefined][13])?** 背景图案过渡
*   `background-opacity` **([number][4] | [Expression][40] | [undefined][13])?** 背景透明度
*   `background-opacity-transition` **([Transition][39] | [undefined][13])?** 背景透明度过渡

## FillLayout

**`填充布局`**
继承[Layout][131]

### Properties

*   `fill-sort-key` **([number][4] | [Expression][40] | [undefined][13])?** 填充排序键

## FillPaint

**`填充画笔`**

### Properties

*   `fill-antialias` **([boolean][12] | [Expression][40] | [undefined][13])?** 是否开启抗锯齿
*   `fill-opacity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 填充不透明度
*   `fill-opacity-transition` **([Transition][39] | [undefined][13])?** 填充不透明度过渡
*   `fill-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 填充颜色
*   `fill-color-transition` **([Transition][39] | [undefined][13])?** 填充颜色过渡
*   `fill-outline-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 填充轮廓颜色
*   `fill-outline-color-transition` **([Transition][39] | [undefined][13])?** 填充轮廓颜色过渡
*   `fill-translate` **([Array][11]<[number][4]> | [undefined][13])?** 填充平移
*   `fill-translate-transition` **([Transition][39] | [undefined][13])?** 填充平移过渡
*   `fill-translate-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 填充平移锚点
*   `fill-pattern` **([string][15] | [Expression][40] | [undefined][13])?** 填充图案
*   `fill-pattern-transition` **([Transition][39] | [undefined][13])?** 填充图案过渡

## FillExtrusionLayout

**`用于填充立体建筑物的样式`**
继承[Layout][131]

## FillExtrusionPaint

**`用于填充立体建筑物的样式`**

### Properties

*   `fill-extrusion-opacity` **([number][4] | [Expression][40] | [undefined][13])?** 填充立体建筑物的不透明度
*   `fill-extrusion-opacity-transition` **([Transition][39] | [undefined][13])?** 填充立体建筑物的不透明度过渡
*   `fill-extrusion-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 填充立体建筑物的颜色
*   `fill-extrusion-color-transition` **([Transition][39] | [undefined][13])?** 填充立体建筑物的颜色过渡
*   `fill-extrusion-translate` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 填充立体建筑物的平移
*   `fill-extrusion-translate-transition` **([Transition][39] | [undefined][13])?** 填充立体建筑物的平移过渡
*   `fill-extrusion-translate-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 填充立体建筑物的平移锚点
*   `fill-extrusion-pattern` **([string][15] | [Expression][40] | [undefined][13])?** 填充立体建筑物的图案
*   `fill-extrusion-pattern-transition` **([Transition][39] | [undefined][13])?** 填充立体建筑物的图案过渡
*   `fill-extrusion-height` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 填充立体建筑物的高度
*   `fill-extrusion-height-transition` **([Transition][39] | [undefined][13])?** 填充立体建筑物的高度过渡
*   `fill-extrusion-base` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 填充立体建筑物的底部高度
*   `fill-extrusion-base-transition` **([Transition][39] | [undefined][13])?** 填充立体建筑物的底部高度过渡
*   `fill-extrusion-vertical-gradient` **([boolean][12] | [undefined][13])?** 是否使用垂直渐变填充立体建筑物

## LineLayout

**`用于线条的样式`**
继承[Layout][131]

### Properties

*   `line-cap` **(`"butt"` | `"round"` | `"square"` | [Expression][40] | [undefined][13])?** 线条端点的样式
*   `line-join` **(`"bevel"` | `"round"` | `"miter"` | [Expression][40] | [undefined][13])?** 线条连接点的样式
*   `line-miter-limit` **([number][4] | [Expression][40] | [undefined][13])?** 线条连接点的最大斜接长度
*   `line-round-limit` **([number][4] | [Expression][40] | [undefined][13])?** 线条连接点的最大圆角半径
*   `line-sort-key` **([number][4] | [Expression][40] | [undefined][13])?** 线条的排序关键字

## LinePaint

**`用于线条的绘制样式`**

### Properties

*   `line-opacity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 线条透明度
*   `line-opacity-transition` **([Transition][39] | [undefined][13])?** 线条透明度过渡
*   `line-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 线条颜色
*   `line-color-transition` **([Transition][39] | [undefined][13])?** 线条颜色过渡
*   `line-translate` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 线条平移
*   `line-translate-transition` **([Transition][39] | [undefined][13])?** 线条平移过渡
*   `line-translate-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 线条平移的锚点
*   `line-width` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 线条宽度
*   `line-width-transition` **([Transition][39] | [undefined][13])?** 线条宽度过渡
*   `line-gap-width` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 线条间隔宽度
*   `line-gap-width-transition` **([Transition][39] | [undefined][13])?** 线条间隔宽度过渡
*   `line-offset` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 线条偏移量
*   `line-offset-transition` **([Transition][39] | [undefined][13])?** 线条偏移量过渡
*   `line-blur` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 线条模糊度
*   `line-blur-transition` **([Transition][39] | [undefined][13])?** 线条模糊度过渡
*   `line-dasharray` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 线条虚线样式
*   `line-dasharray-transition` **([Transition][39] | [undefined][13])?** 线条虚线样式过渡
*   `line-pattern` **([string][15] | [Expression][40] | [undefined][13])?** 线条纹理
*   `line-pattern-transition` **([Transition][39] | [undefined][13])?** 线条纹理过渡
*   `line-gradient` **([Expression][40] | [undefined][13])?** 线条渐变

## SymbolLayout

**`符号布局`**
继承[Layout][131]

### Properties

*   `symbol-placement` **(`"point"` | `"line"` | `"line-center"` | [undefined][13])?** 符号放置方式
*   `symbol-spacing` **([number][4] | [Expression][40] | [undefined][13])?** 符号间距
*   `symbol-avoid-edges` **([boolean][12] | [undefined][13])?** 是否避开边缘
*   `symbol-z-order` **(`"viewport-y"` | `"source"` | [undefined][13])?** 符号Z轴顺序
*   `icon-allow-overlap` **([boolean][12] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 是否允许图标重叠
*   `icon-ignore-placement` **([boolean][12] | [Expression][40] | [undefined][13])?** 是否忽略图标布局
*   `icon-optional` **([boolean][12] | [undefined][13])?** 是否可选
*   `icon-rotation-alignment` **(`"map"` | `"viewport"` | `"auto"` | [undefined][13])?** 图标旋转对齐方式
*   `icon-size` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标大小
*   `icon-text-fit` **(`"none"` | `"both"` | `"width"` | `"height"` | [undefined][13])?** 图标文本适配方式
*   `icon-text-fit-padding` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 图标文本适配内边距
*   `icon-image` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标图片
*   `icon-rotate` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标旋转角度
*   `icon-padding` **([number][4] | [Expression][40] | [undefined][13])?** 图标内边距
*   `icon-keep-upright` **([boolean][12] | [undefined][13])?** 图标是否保持垂直
*   `icon-offset` **([Array][11]<[number][4]> | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标偏移量
*   `icon-anchor` **([Anchor][32] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标锚点
*   `icon-pitch-alignment` **(`"map"` | `"viewport"` | `"auto"` | [undefined][13])?** 图标倾斜对齐方式
*   `text-pitch-alignment` **(`"map"` | `"viewport"` | `"auto"` | [undefined][13])?** 文本倾斜对齐方式
*   `text-field` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本内容
*   `text-font` **([Array][11]<[string][15]> | [Expression][40] | [undefined][13])?** 文本字体, 只允许“normal”和“bold”两种
*   `text-size` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本大小，px
*   `text-max-width` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本最大宽度
*   `text-line-height` **([number][4] | [Expression][40] | [undefined][13])?** 文本行高
*   `text-letter-spacing` **([number][4] | [Expression][40] | [undefined][13])?** 文本字间距
*   `text-justify` **(`"auto"` | `"left"` | `"center"` | `"right"` | [Expression][40] | [undefined][13])?** 文本对齐方式
*   `text-anchor` **([Anchor][32] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本锚点
*   `text-max-angle` **([number][4] | [Expression][40] | [undefined][13])?** 文本最大角度
*   `text-rotate` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本旋转角度
*   `text-padding` **([number][4] | [Expression][40] | [undefined][13])?** 文本内边距
*   `text-keep-upright` **([boolean][12] | [undefined][13])?** 文本是否保持垂直
*   `text-transform` **(`"none"` | `"uppercase"` | `"lowercase"` | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本转换方式
*   `text-offset` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 文本偏移量
*   `text-allow-overlap` **([boolean][12] | [undefined][13])?** 文本是否允许重叠
*   `text-ignore-placement` **([boolean][12] | [undefined][13])?** 文本是否忽略布局
*   `text-optional` **([boolean][12] | [undefined][13])?** 文本是否可选
*   `text-radial-offset` **([number][4] | [Expression][40] | [undefined][13])?** 文本径向偏移量
*   `text-variable-anchor` **([Array][11]<[Anchor][32]> | [undefined][13])?** 文本可变锚点
*   `text-writing-mode` **([Array][11]<(`"horizontal"` | `"vertical"`)> | [undefined][13])?** 文本书写方式
*   `symbol-sort-key` **([number][4] | [Expression][40] | [undefined][13])?** 符号排序键

## SymbolPaint

**`符号绘制样式`**

### Properties

*   `icon-opacity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标透明度
*   `icon-opacity-transition` **([Transition][39] | [undefined][13])?** 图标透明度过渡
*   `icon-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标颜色
*   `icon-color-transition` **([Transition][39] | [undefined][13])?** 图标颜色过渡
*   `icon-halo-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标光晕颜色
*   `icon-halo-color-transition` **([Transition][39] | [undefined][13])?** 图标光晕颜色过渡
*   `icon-halo-width` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标光晕宽度
*   `icon-halo-width-transition` **([Transition][39] | [undefined][13])?** 图标光晕宽度过渡
*   `icon-halo-blur` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 图标光晕模糊度
*   `icon-halo-blur-transition` **([Transition][39] | [undefined][13])?** 图标光晕模糊度过渡
*   `icon-translate` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 图标平移
*   `icon-translate-transition` **([Transition][39] | [undefined][13])?** 图标平移过渡
*   `icon-translate-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 图标平移锚点
*   `text-opacity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本透明度
*   `text-opacity-transition` **([Transition][39] | [undefined][13])?** 文本透明度过渡
*   `text-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本颜色
*   `text-color-transition` **([Transition][39] | [undefined][13])?** 文本颜色过渡
*   `text-halo-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本光晕颜色
*   `text-halo-color-transition` **([Transition][39] | [undefined][13])?** 文本光晕颜色过渡
*   `text-halo-width` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本光晕宽度
*   `text-halo-width-transition` **([Transition][39] | [undefined][13])?** 文本光晕宽度过渡
*   `text-halo-blur` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 文本光晕模糊度
*   `text-halo-blur-transition` **([Transition][39] | [undefined][13])?** 文本光晕模糊度过渡
*   `text-translate` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 文本平移
*   `text-translate-transition` **([Transition][39] | [undefined][13])?** 文本平移过渡
*   `text-translate-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 文本平移锚点

## RasterLayout

**`矢量栅格图层布局`**
继承[Layout][131]

## RasterPaint

**`矢量栅格图层绘制`**

### Properties

*   `raster-opacity` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层透明度
*   `raster-opacity-transition` **([Transition][39] | [undefined][13])?** 栅格图层透明度过渡
*   `raster-hue-rotate` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层色相旋转
*   `raster-hue-rotate-transition` **([Transition][39] | [undefined][13])?** 栅格图层色相旋转过渡
*   `raster-brightness-min` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层最小亮度
*   `raster-brightness-min-transition` **([Transition][39] | [undefined][13])?** 栅格图层最小亮度过渡
*   `raster-brightness-max` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层最大亮度
*   `raster-brightness-max-transition` **([Transition][39] | [undefined][13])?** 栅格图层最大亮度过渡
*   `raster-saturation` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层饱和度
*   `raster-saturation-transition` **([Transition][39] | [undefined][13])?** 栅格图层饱和度过渡
*   `raster-contrast` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层对比度
*   `raster-contrast-transition` **([Transition][39] | [undefined][13])?** 栅格图层对比度过渡
*   `raster-fade-duration` **([number][4] | [Expression][40] | [undefined][13])?** 栅格图层淡出时间
*   `raster-resampling` **(`"linear"` | `"nearest"` | [undefined][13])?** 栅格图层重采样方式

## CircleLayout

**`圆形图层布局`**
继承[Layout][131]

### Properties

*   `circle-sort-key` **([number][4] | [Expression][40] | [undefined][13])?** 圆形图层排序关键字

## CirclePaint

**`圆形图层绘制`**

### Properties

*   `circle-radius` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形半径
*   `circle-radius-transition` **([Transition][39] | [undefined][13])?** 圆形半径过渡
*   `circle-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形颜色
*   `circle-color-transition` **([Transition][39] | [undefined][13])?** 圆形颜色过渡
*   `circle-blur` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形模糊度
*   `circle-blur-transition` **([Transition][39] | [undefined][13])?** 圆形模糊度过渡
*   `circle-opacity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形透明度
*   `circle-opacity-transition` **([Transition][39] | [undefined][13])?** 圆形透明度过渡
*   `circle-translate` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 圆形平移
*   `circle-translate-transition` **([Transition][39] | [undefined][13])?** 圆形平移过渡
*   `circle-translate-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 圆形平移锚点
*   `circle-pitch-scale` **(`"map"` | `"viewport"` | [undefined][13])?** 圆形俯仰缩放
*   `circle-pitch-alignment` **(`"map"` | `"viewport"` | [undefined][13])?** 圆形俯仰对齐
*   `circle-stroke-width` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形描边宽度
*   `circle-stroke-width-transition` **([Transition][39] | [undefined][13])?** 圆形描边宽度过渡
*   `circle-stroke-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形描边颜色
*   `circle-stroke-color-transition` **([Transition][39] | [undefined][13])?** 圆形描边颜色过渡
*   `circle-stroke-opacity` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 圆形描边透明度
*   `circle-stroke-opacity-transition` **([Transition][39] | [undefined][13])?** 圆形描边透明度过渡

## HeatmapLayout

**`热力图图层布局`**
继承[Layout][131]

## HeatmapPaint

**`热力图绘制样式`**

### Properties

*   `heatmap-radius` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 热力图半径
*   `heatmap-radius-transition` **([Transition][39] | [undefined][13])?** 热力图半径过渡
*   `heatmap-weight` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 热力图权重
*   `heatmap-intensity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 热力图强度
*   `heatmap-intensity-transition` **([Transition][39] | [undefined][13])?** 热力图强度过渡
*   `heatmap-color` **([string][15] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 热力图颜色
*   `heatmap-opacity` **([number][4] | [StyleFunction][132] | [Expression][40] | [undefined][13])?** 热力图透明度
*   `heatmap-opacity-transition` **([Transition][39] | [undefined][13])?** 热力图透明度过渡

## HillshadeLayout

**`山体阴影图层布局`**
继承[Layout][131]

## HillshadePaint

**`山体阴影绘制样式`**

### Properties

*   `hillshade-illumination-direction` **([number][4] | [Expression][40] | [undefined][13])?** 光照方向，0为正北，90为正东，180为正南，270为正西
*   `hillshade-illumination-anchor` **(`"map"` | `"viewport"` | [undefined][13])?** 光照方向相对于地图还是视口
*   `hillshade-exaggeration` **([number][4] | [Expression][40] | [undefined][13])?** 高程放大系数
*   `hillshade-exaggeration-transition` **([Transition][39] | [undefined][13])?** 高程放大系数过渡
*   `hillshade-shadow-color` **([string][15] | [Expression][40] | [undefined][13])?** 阴影颜色
*   `hillshade-shadow-color-transition` **([Transition][39] | [undefined][13])?** 阴影颜色过渡
*   `hillshade-highlight-color` **([string][15] | [Expression][40] | [undefined][13])?** 高亮颜色
*   `hillshade-highlight-color-transition` **([Transition][39] | [undefined][13])?** 高亮颜色过渡
*   `hillshade-accent-color` **([string][15] | [Expression][40] | [undefined][13])?** 强调颜色
*   `hillshade-accent-color-transition` **([Transition][39] | [undefined][13])?** 强调颜色过渡

## SkyLayout

**`天空图层布局`**
继承[Layout][131]

## SkyPaint

**`用于设置天空的绘制样式`**

### Properties

*   `sky-atmosphere-color` **([string][15] | [Expression][40] | [undefined][13])?** 大气层颜色
*   `sky-atmosphere-halo-color` **([string][15] | [Expression][40] | [undefined][13])?** 大气层光晕颜色
*   `sky-atmosphere-sun` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 太阳位置
*   `sky-atmosphere-sun-intensity` **([number][4] | [Expression][40] | [undefined][13])?** 太阳强度
*   `sky-gradient` **([string][15] | [Expression][40] | [undefined][13])?** 渐变颜色
*   `sky-gradient-center` **([Array][11]<[number][4]> | [Expression][40] | [undefined][13])?** 渐变中心位置
*   `sky-gradient-radius` **([number][4] | [Expression][40] | [undefined][13])?** 渐变半径
*   `sky-opacity` **([number][4] | [Expression][40] | [undefined][13])?** 天空透明度
*   `sky-type` **(`"gradient"` | `"atmosphere"` | [undefined][13])?** 天空类型

## ElevationQueryOptions

**`用于设置获取高程的参数`**

Type: <span>{exaggerated: [boolean][12]}</span>

### Properties

*   `exaggerated` **[boolean][12]**&#x20;

## Projection

**`用于设置地图投影方式的参数`**

### Properties

*   `center` **\[[number][4], [number][4]]?** 投影中心点
*   `parallels` **\[[number][4], [number][4]]?** 投影平行线

[1]: #geojsonfeaturei

[2]: #capitalizestr

[3]: #capitalizekey

[4]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[5]: /jsapi/apis/coordinate/LngLat.html

[6]: /jsapi/apis/coordinate/LngLatBounds.html

[7]: #lnglatlike

[8]: /jsapi/apis/coordinate/Point.html

[9]: #pointlike

[10]: #expressionname

[11]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[12]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[13]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[14]: #lnglatboundslike

[15]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[16]: https://developer.mozilla.org/docs/Web/HTML/Element

[17]: #dragpanoptions

[18]: #fitboundsoptions

[19]: #projection

[20]: #interactiveoptions

[21]: #style

[22]: #transformrequestfunction

[23]: /jsapi/apis/coordinate/MercatorCoordinate.html

[24]: #quat

[25]: #vec3

[26]: #resourcetype

[27]: #requestparameters

[28]: /jsapi/apis/map/Map.html

[29]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/function

[30]: /jsapi/apis/base/Evented.html

[31]: #icontrol

[32]: #anchor

[33]: #offset

[34]: #anylayer

[35]: #sources

[36]: #fog

[37]: #light

[38]: #terrainspecification

[39]: #transition

[40]: #expression

[41]: #geojsonsourceraw

[42]: #videosourceraw

[43]: #imagesourceraw

[44]: #canvassourceraw

[45]: #vectorsource

[46]: #rastersource

[47]: #rasterdemsource

[48]: #customsourceinterface

[49]: https://developer.mozilla.org/docs/Web/API/HTMLImageElement

[50]: #geojsonsource

[51]: #videosource

[52]: #imagesource

[53]: #canvassource

[54]: #vectorsourceimpl

[55]: #customsource

[56]: #geojsonsourceoptions

[57]: #source

[58]: #geojsonsourceoptionsdata

[59]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[60]: #promoteidspecification

[61]: #videosourceoptions

[62]: https://developer.mozilla.org/docs/Web/API/HTMLVideoElement

[63]: #imagesourceoptions

[64]: #canvassourceoptions

[65]: https://developer.mozilla.org/docs/Web/API/HTMLCanvasElement

[66]: #camerafunctionspecification

[67]: #expressionspecification

[68]: #propertyvaluespecification

[69]: #sourcevectorlayer

[70]: #alignment

[71]: #mapboxgeojsonfeature

[72]: #mapboxevent

[73]: #maplayermouseevent

[74]: #maplayertouchevent

[75]: #mapsourcedataevent

[76]: #mapstyledataevent

[77]: #coordinate

[78]: #canonicalcoordinate

[79]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Error

[80]: #paddingoptions

[81]: #cameraoptions

[82]: #cameraforboundsresult

[83]: #animationoptions

[84]: #flytooptions

[85]: #errorevent

[86]: #mapcontextevent

[87]: #mapdataevent

[88]: #mapboxzoomevent

[89]: #maptouchevent

[90]: #mapmouseevent

[91]: https://developer.mozilla.org/docs/Web/API/MouseEvent

[92]: https://developer.mozilla.org/docs/Web/API/TouchEvent

[93]: https://developer.mozilla.org/docs/Web/API/WheelEvent

[94]: #mapwheelevent

[95]: #backgroundlayout

[96]: #filllayout

[97]: #fillextrusionlayout

[98]: #linelayout

[99]: #symbollayout

[100]: #rasterlayout

[101]: #circlelayout

[102]: #heatmaplayout

[103]: #hillshadelayout

[104]: #skylayout

[105]: #backgroundpaint

[106]: #fillpaint

[107]: #fillextrusionpaint

[108]: #linepaint

[109]: #symbolpaint

[110]: #rasterpaint

[111]: #circlepaint

[112]: #heatmappaint

[113]: #hillshadepaint

[114]: #skypaint

[115]: #anylayout

[116]: #anypaint

[117]: #anysourcedata

[118]: #layer

[119]: #backgroundlayer

[120]: #tcirclelayer

[121]: #fillextrusionlayer

[122]: #filllayer

[123]: #theatmaplayer

[124]: #hillshadelayer

[125]: #linelayer

[126]: #trasterlayer

[127]: #tsymbollayer

[128]: #customlayerinterface

[129]: #skylayer

[130]: #visibility

[131]: #layout

[132]: #stylefunction

