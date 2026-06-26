---
outline: deep
---
 # Map


## Map

**`地图类，表示页面上渲染的地图区域`** <br>

> 继承[Evented][1]

### Examples

```javascript
const map = new DiMap.Map({
  container: "container",
  style: "dimap://styles/normal",
  center: [116.39, 39.9],
  zoom: 10
})
map.on("load", () => {
  console.log("map loaded")
})
```

### constructor

**`构造一个地图实例`**

#### Parameters

*   `options` **[MapboxOptions][2]?** 地图选项

### showTerrainWireframe

**`控制地形网格线框的可见性。`**

Type: <span>[boolean][3]</span>

### showTileBoundaries

**`设置是否显示瓦片边界。`**

Type: <span>[boolean][3]</span>

### showCollisionBoxes

**`设置是否显示碰撞检测边界。`**

Type: <span>[boolean][3]</span>

### showPadding

**`设置是否显示地图填充边界。`**

Type: <span>[boolean][3]</span>

### repaint

**`设置是否重绘地图。`**

Type: <span>[boolean][3]</span>

### scrollZoom

**`地图滚轮缩放处理程序`**

Type: <span>[ScrollZoomHandler][4]</span>

### boxZoom

**`地图框选缩放处理程序`**

Type: <span>[BoxZoomHandler][5]</span>

### dragRotate

**`地图拖动旋转处理程序`**

Type: <span>[DragRotateHandler][6]</span>

### dragPan

**`地图拖动平移处理程序`**

Type: <span>[DragPanHandler][7]</span>

### keyboard

**`地图键盘操作处理程序`**

Type: <span>[KeyboardHandler][8]</span>

### doubleClickZoom

**`地图双击缩放处理程序`**

Type: <span>[DoubleClickZoomHandler][9]</span>

### touchZoomRotate

**`地图触摸缩放旋转处理程序`**

Type: <span>[TouchZoomRotateHandler][10]</span>

### touchPitch

**`地图触摸俯仰处理程序`**

Type: <span>[TouchPitchHandler][11]</span>

## 操作控件

### addControl

**`添加一个控件`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `control` | 是 | [Control][12] \| [IControl][13] | 待添加的控件 |
| `position` | 否 | `"top-right" \| "top-left" \| "bottom-right" \| "bottom-left"` | 控件在地图中的位置 |

Returns **[Map][14]** 返回当前地图实例

### removeControl

**`移除一个控件`**

#### Parameters

*   `control` **([Control][12] | [IControl][13])** 待移除的控件

Returns **[Map][14]** 返回当前地图实例

### hasControl

**`检查地图实例是否包含指定控件`**

#### Parameters

*   `control` **[IControl][13]** 待检查的控件

Returns **[boolean][3]** 若包含则返回 true，否则返回 false

### getContainer

**`获取包含地图的容器元素。`**

Returns **[HTMLElement][15]** 包含地图的容器元素。

### getCanvasContainer

**`获取包含地图画布的容器元素。`**

Returns **[HTMLElement][15]** 包含地图画布的容器元素。

### getCanvas

**`获取地图的画布元素。`**

Returns **[HTMLCanvasElement][16]** 地图的画布元素。

## 操作地图实例

### resize

**`调整地图容器的大小`**

#### Parameters

*   `eventData` **[EventData][17]?** 可选参数，包含 width 和 height 属性，表示调整后的大小

Returns **[Map][14]** 返回当前地图实例

### getBounds

**`获取当前地图视野内所有图层的边界范围`**

Returns **[LngLatBounds][18]** 返回 LngLatBounds 类型的对象，表示边界范围

### getMaxBounds

**`获取地图的最大边界范围`**

Returns **([LngLatBounds][18] | null)** 若已设置则返回 LngLatBounds 类型的对象，否则返回 null

### setMaxBounds

**`设置地图的最大边界范围`**

#### Parameters

*   `lnglatbounds` **[LngLatBoundsLike][19]?** 可选参数，表示最大边界范围

Returns **[Map][14]** 返回当前地图实例

### setMinZoom

**`设置地图的最小缩放级别`**

#### Parameters

*   `minZoom` **([number][20] | null)?** 可选参数，表示最小缩放级别

Returns **[Map][14]** 返回当前地图实例

### getMinZoom

**`获取地图的最小缩放级别`**

Returns **[number][20]** 返回最小缩放级别

### setMaxZoom

**`设置地图的最大缩放级别`**

#### Parameters

*   `maxZoom` **([number][20] | null)?** 可选参数，表示最大缩放级别

Returns **[Map][14]** 返回当前地图实例

### getMaxZoom

**`获取地图的最大缩放级别`**

Returns **[number][20]** 返回最大缩放级别

### setMinPitch

**`设置地图的最小倾斜度`**

#### Parameters

*   `minPitch` **([number][20] | null)?** 可选参数，表示最小倾斜度

Returns **[Map][14]** 返回当前地图实例

### getMinPitch

**`获取地图的最小倾斜度`**

Returns **[number][20]** 返回最小倾斜度

### setMaxPitch

**`设置地图的最大倾斜度`**

#### Parameters

*   `maxPitch` **([number][20] | null)?** 可选参数，表示最大倾斜度

Returns **[Map][14]** 返回当前地图实例

### getMaxPitch

**`获取地图的最大倾斜度`**

Returns **[number][20]** 返回最大倾斜度

### getRenderWorldCopies

**`获取当前地图是否启用世界地图复制`**

Returns **[boolean][3]** 若启用则返回 true，否则返回 false

### setRenderWorldCopies

**`启用或禁用地图的世界地图复制功能`**

#### Parameters

*   `renderWorldCopies` **[boolean][3]?** 可选参数，表示是否启用世界地图复制

Returns **[Map][14]** 返回当前地图实例

## 坐标转换

### project

**`将经纬度坐标转换为屏幕坐标`**

#### Parameters

*   `lnglat` **[LngLatLike][21]** 待转换的经纬度坐标

Returns **[Point][22]** 返回 Point 类型的对象，表示屏幕坐标

### unproject

**`将屏幕坐标转换为经纬度坐标`**

#### Parameters

*   `point` **[PointLike][23]** 待转换的屏幕坐标

Returns **[LngLat][24]** 返回 LngLat 类型的对象，表示经纬度坐标

### getProjection

**`获取地图投影方式`**

Returns **[Projection][25]** 返回地图的投影方式

### setProjection

**`设置地图投影方式`**

#### Parameters

*   `projection` **([Projection][25] | [string][26])** 要设置的投影方式或投影名称

Returns **[Map][14]** 返回地图实例，方便链式调用

## 地图移动状态

### isMoving

**`检查地图是否正在移动`**

Returns **[boolean][3]** 若正在移动则返回 true，否则返回 false

### isZooming

**`检查地图是否正在缩放`**

Returns **[boolean][3]** 若正在缩放则返回 true，否则返回 false

### isRotating

**`检查地图是否正在旋转`**

Returns **[boolean][3]** 若正在旋转则返回 true，否则返回 false

## 监听地图事件

### Examples

```javascript
| 事件名称                                                   | 是否支持绑定到 `layerId`     |
|-----------------------------------------------------------|---------------------------|
| [`mousedown`](#map.event:mousedown)                       | yes                       |
| [`mouseup`](#map.event:mouseup)                           | yes                       |
| [`mouseover`](#map.event:mouseover)                       | yes                       |
| [`mouseout`](#map.event:mouseout)                         | yes                       |
| [`mousemove`](#map.event:mousemove)                       | yes                       |
| [`mouseenter`](#map.event:mouseenter)                     | yes (必须）                |
| [`mouseleave`](#map.event:mouseleave)                     | yes (必须）                |
| [`click`](#map.event:click)                               | yes                       |
| [`dblclick`](#map.event:dblclick)                         | yes                       |
| [`contextmenu`](#map.event:contextmenu)                   | yes                       |
| [`touchstart`](#map.event:touchstart)                     | yes                       |
| [`touchend`](#map.event:touchend)                         | yes                       |
| [`touchcancel`](#map.event:touchcancel)                   | yes                       |
| [`wheel`](#map.event:wheel)                               |                           |
| [`resize`](#map.event:resize)                             |                           |
| [`remove`](#map.event:remove)                             |                           |
| [`touchmove`](#map.event:touchmove)                       |                           |
| [`movestart`](#map.event:movestart)                       |                           |
| [`move`](#map.event:move)                                 |                           |
| [`moveend`](#map.event:moveend)                           |                           |
| [`dragstart`](#map.event:dragstart)                       |                           |
| [`drag`](#map.event:drag)                                 |                           |
| [`dragend`](#map.event:dragend)                           |                           |
| [`zoomstart`](#map.event:zoomstart)                       |                           |
| [`zoom`](#map.event:zoom)                                 |                           |
| [`zoomend`](#map.event:zoomend)                           |                           |
| [`rotatestart`](#map.event:rotatestart)                   |                           |
| [`rotate`](#map.event:rotate)                             |                           |
| [`rotateend`](#map.event:rotateend)                       |                           |
| [`pitchstart`](#map.event:pitchstart)                     |                           |
| [`pitch`](#map.event:pitch)                               |                           |
| [`pitchend`](#map.event:pitchend)                         |                           |
| [`boxzoomstart`](#map.event:boxzoomstart)                 |                           |
| [`boxzoomend`](#map.event:boxzoomend)                     |                           |
| [`boxzoomcancel`](#map.event:boxzoomcancel)               |                           |
| [`webglcontextlost`](#map.event:webglcontextlost)         |                           |
| [`webglcontextrestored`](#map.event:webglcontextrestored) |                           |
| [`load`](#map.event:load)                                 |                           |
| [`render`](#map.event:render)                             |                           |
| [`idle`](#map.event:idle)                                 |                           |
| [`error`](#map.event:error)                               |                           |
| [`data`](#map.event:data)                                 |                           |
| [`styledata`](#map.event:styledata)                       |                           |
| [`sourcedata`](#map.event:sourcedata)                     |                           |
| [`dataloading`](#map.event:dataloading)                   |                           |
| [`styledataloading`](#map.event:styledataloading)         |                           |
| [`sourcedataloading`](#map.event:sourcedataloading)       |                           |
| [`styleimagemissing`](#map.event:styleimagemissing)       |                           |
```

### on

**`绑定地图事件处理程序。`**


#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][26] \| [MapLayerEventType][55] \| [MapEventType][56] | 要绑定的事件类型。 |
| `layer` | 否 | [string][26] \| ReadonlyArray<[string][26]>| 事件将被应用到的图层的名称或名称数组。（仅 [MapLayerEventType][55] 需要此参数） |
| `listener` | 是 | [Function][27] | 事件触发时要调用的回调函数。 |

Returns **[Map][14]** 该地图的实例。

### once

**`在地图上添加一次性事件监听器，当事件触发时，监听器将自动从地图中移除`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][26] \| [MapLayerEventType][55] \| [MapEventType][56] | 要监听的事件类型 |
| `layer` | 否 | [string][26] \| ReadonlyArray<[string][26]> | 事件将被应用到的图层的名称或名称数组（MapLayerEventType 和异步监听 MapEventType 需要传入此参数） |
| `listener` | 否 | `function (ev: any): void` | 事件触发时要调用的回调函数 |

Returns 

  **[Map][14]** 返回地图实例，方便链式调用

  **[Promise][28]\<any>**&#x20;返回一个 Promise，以便异步等待事件的第一个参数

### off

**`从地图中移除事件监听器`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `type` | 是 | [string][26] \| [MapLayerEventType][55] \| [MapEventType][56] | 要移除的事件类型 |
| `layer` | 否 | [string][26] \| ReadonlyArray<[string][26]> | 事件被应用到的图层的名称或名称数组（仅 [MapLayerEventType][55] 需要此参数） |
| `listener` | 否 | `function (ev: any): void` | 要移除的特定监听器函数（如省略则移除该类型的所有监听器） |

Returns **[Map][14]** 返回地图实例，方便链式调用

## 地图元素查询

### queryRenderedFeatures

**`查询指定点或框范围内的渲染要素`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `pointOrBox` | 否 | [PointLike][23] \| [[PointLike][23], [PointLike][23]] | 指定点或框范围 |
| `options` | 否 | [Object][29] | 可选参数对象 |
| `options.layers` | 否 | [Array][30]<[string][26]> | 指定查询的图层 |
| `options.filter` | 否 | [Array][30] | 过滤查询结果的函数数组 |
| `options.limit` | 否 | [number][20] | 查询结果的最大数量 |
| `options.offset` | 否 | [number][20] | 查询结果的偏移量 |

Returns **[Array][30]<[MapboxGeoJSONFeature][31]>** 渲染要素数组

### querySourceFeatures

**`查询指定数据源的 features`**

#### Parameters
#### `querySourceFeatures` 方法 - 查询指定数据源的要素

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `sourceID` | 是 | [string][26]| 数据源的 ID |
| `parameters` | 否 | [object][29] | 过滤选项 |
| `parameters.sourceLayer` | 否 | [string][26]｜ [undefined][34] | 源图层名称 |
| `parameters.filter` | 否 | any[]｜ [undefined][34] | 过滤条件数组 |
| `parameters.validate` | 否 | [FilterOptions][32]| 是否验证过滤条件 |

Returns **[Array][30]<[MapboxGeoJSONFeature][31]>** 匹配的 features 数组

## 操作地图样式表

### setStyle

**`设置地图的样式`**

#### Parameters
#### `setStyle` 方法 - 设置地图的样式

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `style` | 是 | [Style][33] \| [string][26] | 新的地图样式 |
| `options` | 否 | [object][29] | 可选配置项 |
| `options.diff` | 否 | [boolean][3]\| [undefined][34] | 是否使用差分算法来比较和更新新旧样式 |
| `options.localIdeographFontFamily` | 否 | [string][26] \| [undefined][34] | 中文本地字体的名称 |

Returns **[Map][14]** 当前地图对象

### getStyle

**`返回地图当前使用的样式。`**

Returns **[Style][33]** 当前地图的样式。

### isStyleLoaded

**`判断地图的样式是否已加载完毕。`**

Returns **[boolean][3]** 如果样式已加载完毕，则返回true；否则返回false。

## 操作地图数据源

### addSource

**`添加地图数据源。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | 是 | [string][26] | 数据源的唯一标识符 |
| `source` | 是 | [AnySourceData][35] | 数据源配置对象 |

Returns **[Map][14]** 当前地图实例。

### isSourceLoaded

**`判断指定的地图数据源是否已经加载完毕。`**

#### Parameters

*   `id` **[string][26]** 数据源的唯一标识符。

Returns **[boolean][3]** 如果数据源已加载完毕，则返回true；否则返回false。

### areTilesLoaded

**`判断所有地图瓦片是否已经加载完毕。`**

Returns **[boolean][3]** 如果所有地图瓦片都已经加载完毕，则返回true；否则返回false。

### removeSource

**`移除指定的地图数据源。`**

#### Parameters

*   `id` **[string][26]** 数据源的唯一标识符。

Returns **[Map][14]** 当前地图实例。

### getSource

**`获取指定的地图数据源对象。`**

#### Parameters

*   `id` **[string][26]** 数据源的唯一标识符。

Returns **([AnySourceImpl][36] | [undefined][34])** 指定的地图数据源对象，如果不存在则返回undefined。

## 操作图像

### addImage

**`添加一个新的图片到地图中。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `name` | 是 | [string][26] | 图片的唯一标识符 |
| `image` | 是 | [HTMLImageElement][37] \| ArrayBufferView \| {width: [number][20], height: [number][20], data: ([Uint8Array][38] \| [Uint8ClampedArray][39])} \| ImageData \| ImageBitmap | 图片数据 |
| `options` | 否 | [Object][29] | 可选项 |
| `options.pixelRatio` | 否 | [number][20] | 像素比例，默认值为1 |
| `options.sdf` | 否 | [boolean][3] | 是否使用SDF渲染，默认值为false |
| `options.stretchX` | 否 | [Array][30]<\[[number][20], [number][20]]> | 横向拉伸范围 |
| `options.stretchY` | 否 | [Array][30]<\[[number][20], [number][20]]> | 纵向拉伸范围 |
| `options.content` | 否 | [[number][20], [number][20], [number][20], [number][20]] | 图片内容区域 |

Returns **void**&#x20;

### updateImage

**`更新地图中指定名称的图片。`**

#### Parameters

#### `updateImage` 方法 - 更新地图中指定名称的图片

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `name` | 是 | [string][26] | 图片的唯一标识符 |
| `image` | 是 | [HTMLImageElement][37] \| ArrayBufferView \| {width: [number][20], height: [number][20], data: ([Uint8Array][38] \| [Uint8ClampedArray][39])} \| ImageData \| ImageBitmap | 新的图片数据 |

Returns **void**&#x20;

### hasImage

**`判断地图中是否存在指定名称的图片。`**

#### Parameters

*   `name` **[string][26]** 图片的唯一标识符。

Returns **[boolean][3]** 存在返回true，不存在返回false。

### removeImage

**`删除地图中指定名称的图片。`**

#### Parameters

*   `name` **[string][26]** 图片的唯一标识符。

Returns **void**&#x20;

### loadImage

**`加载图片并调用回调函数。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `url` | 是 | [string][26] | 图片的URL |
| `callback` | 是 | [Function][27] | 回调函数，如果加载失败则传入错误对象，否则传入图片对象 |

Returns **void**&#x20;

### listImages

**`获取所有已加载的图像的名称列表。`**

Returns **[Array][30]<[string][26]>** 包含所有已加载的图像名称的数组。

## 操作图层

### addLayer

**`添加一个图层到地图中。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layer` | 是 | [AnyLayer][40] | 要添加到地图中的图层 |
| `before` | 否 | [string][26] | 在此图层之前插入的另一个图层的ID |

Returns **[Map][14]** 该地图的实例。

### moveLayer

**`将指定图层移动到另一个图层之前。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | 是 | [string][26] | 要移动的图层的ID |
| `beforeId` | 否 | [string][26] | 目标位置之前的另一个图层的ID |

Returns **[Map][14]** 该地图的实例。

### removeLayer

**`从地图中删除指定的图层。`**

#### Parameters

*   `id` **[string][26]** 要删除的图层的ID。

Returns **[Map][14]** 该地图的实例。

### getLayer

**`获取指定的图层对象。`**

#### Parameters

*   `id` **[string][26]** 要获取的图层的ID。

Returns **[AnyLayer][40]** 指定的图层对象。

### setFilter

**`为指定的图层设置过滤器。`**

#### Parameters
#### `setFilter` 方法 - 为指定的图层设置过滤器

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layer` | 是 | [string][26] | 要设置过滤器的图层的ID |
| `filter` | 否 | [Array][30]\<any> \| [boolean][3] \| null  | 过滤器函数或布尔表达式，设为null可删除现有过滤器 |
| `options` | 否 | [FilterOptions][32] \| null  | 过滤器选项 |

Returns **[Map][14]** 该地图的实例。

### setLayerZoomRange

**`设置指定图层的缩放级别范围。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layerId` | 是 | [string][26] | 要设置缩放级别范围的图层的ID |
| `minzoom` | 是 | [number][20] | 允许图层显示的最小缩放级别 |
| `maxzoom` | 是 | [number][20] | 允许图层显示的最大缩放级别 |

Returns **[Map][14]** 该地图的实例。

### getFilter

**`获取指定图层的过滤器。`**

#### Parameters

*   `layer` **[string][26]** 要获取过滤器的图层的ID。

Returns **[Array][30]\<any>** 该图层的过滤器。

### setPaintProperty

**`为指定图层设置指定属性的绘制属性。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layer` | 是 | [string][26]| 要设置绘制属性的图层的ID |
| `name` | 是 | [string][26] | 要设置的绘制属性的名称 |
| `value` | 是 | `any` | 要设置的绘制属性的值 |
| `options` | 否 | [FilterOptions][32] \| null | 设置绘制属性的选项 |

Returns **[Map][14]** 该地图的实例。

### getPaintProperty

**`获取指定图层的指定绘制属性的值。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layer` | 是 | [string][26] | 要获取绘制属性值的图层的ID |
| `name` | 是 | [string][26] | 要获取的绘制属性的名称 |

Returns **any** 指定的绘制属性的值。

### setLayoutProperty

**`为指定图层设置指定属性的布局属性。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layer` | 是 | [string][26] | 要设置布局属性的图层的ID |
| `name` | 是 | [string][26] | 要设置的布局属性的名称 |
| `value` | 是 | `any` | 要设置的布局属性的值 |
| `options` | 否 | [FilterOptions][32] \| null | 设置布局属性的选项 |

Returns **[Map][14]** 该地图的实例。

### getLayoutProperty

**`获取指定图层的指定布局属性的值。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `layer` | 是 | [string][26] | 要获取布局属性的图层的ID |
| `name` | 是 | [string][26] | 要获取的布局属性的名称 |

Returns **any** 指定图层的指定布局属性的值。

## 操作地图样式属性

### setLight

**`设置地图的灯光。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `light` | 是 | [Light][41] | 要设置的灯光 |
| `options` | 否 | [FilterOptions][32] | 设置灯光的选项 |

Returns **[Map][14]** 该地图的实例。

### getLight

**`获取地图的灯光。`**

Returns **[Light][41]** 地图的灯光。

### setTerrain

**`设置地图的地形。`**

#### Parameters

*   `terrain` **([TerrainSpecification][42] | null)?** 要设置的地形规范。

Returns **[Map][14]** 该地图的实例。

### getTerrain

**`获取地图的地形。`**

Returns **([TerrainSpecification][42] | null)** 地图的地形规范。

### getFog

**`获取地图雾效对象，如果没有设置雾效则返回 null`**

Returns **([Fog][43] | null)** 返回地图雾效对象或 null

### setFog

**`设置地图雾效`**

#### Parameters

*   `fog` **[Fog][43]** 要设置的雾效对象

Returns **[Map][14]** 返回地图实例，方便链式调用

## 操作地图元素状态

### setFeatureState

**`设置指定要素的状态。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `feature` | 是 | [FeatureIdentifier][44] \| [MapboxGeoJSONFeature][31] | 要设置状态的要素标识符或 GeoJSON 要素 |
| `state` | 是 | [Object][29]<[string][26], any> | 要为要素设置的状态对象 |

Returns **void**&#x20;

### getFeatureState

**`获取指定要素的状态。`**

#### Parameters

*   `feature` **([FeatureIdentifier][44] | [MapboxGeoJSONFeature][31])** 要获取状态的要素标识符或 GeoJSON 要素。

Returns **[Object][29]<[string][26], any>** 要素的状态对象。

### removeFeatureState

**`从指定要素中删除指定的状态属性，或从指定要素中删除所有状态属性。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `target` | 是 | [FeatureIdentifier][44] \| [MapboxGeoJSONFeature][31] | 要从中删除状态属性的要素标识符或 GeoJSON 要素 |
| `key` | 否 | [string][26] | 要删除的状态属性的键。如果未指定，则删除所有状态属性 |

Returns **void**&#x20;

## 地图生命周期

### loaded

**`检查地图是否已加载。`**

Returns **[boolean][3]** 如果地图已加载，则为 true；否则为 false。

### remove

**`从页面中删除地图。`**

Returns **void**&#x20;

### triggerRepaint

**`重新绘制地图。`**

Returns **void**&#x20;

## 操作相机视角

### queryTerrainElevation

**`查询给定点的地形高程。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `lngLat` | 是 | [LngLatLike][21] | 要查询高程的点的地理坐标 |
| `options` | 否 | [ElevationQueryOptions][45] | 查询高程的选项 |

Returns **([number][20] | null)** 给定点的地形高程（单位：米）。如果查询失败，则返回 null。

### getCenter

**`获取地图的中心点坐标。`**

Returns **[LngLat][24]** 地图中心点的经纬度坐标。

### setCenter

**`将地图中心点设置为指定坐标。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `center` | 是 | [LngLatLike][21] | 新的地图中心点的经纬度坐标 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### panBy

**`以指定的像素偏移量平移地图。`**

#### Parameters

| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `offset` | 是 | [PointLike][23] | 像素坐标的偏移量，指定为`{ x, y }`|
| `options` | 否 | [AnimationOptions][46] | 平移动画的选项 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### panTo

**`将地图中心点平移到指定的经纬度坐标。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `lnglat` | 是 | [LngLatLike][21] | 目标中心点的经纬度坐标 |
| `options` | 否 | [AnimationOptions][46] | 平移动画的选项 |
| `eventdata` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### getZoom

**`获取地图的当前缩放级别。`**

Returns **[number][20]** 当前缩放级别。

### setZoom

**`将地图的缩放级别设置为指定的级别。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `zoom` | 是 | [number][20] | 目标缩放级别 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### zoomTo

**`缩放地图以达到指定的缩放级别。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `zoom` | 是 | [number][20] | 目标缩放级别 |
| `options` | 否 | [AnimationOptions][46] | 缩放动画的选项 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### zoomIn

**`将地图的缩放级别增加一级。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 否 | [AnimationOptions][46] | 缩放动画的选项 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### zoomOut

**`将地图的缩放级别减少一级。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 否 | [AnimationOptions][46] | 缩放动画的选项 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### getBearing

**`获取地图的当前方向（以度数为单位）。`**

Returns **[number][20]** 当前方向的角度（以度数为单位）。

### setBearing

**`将地图的方向设置为指定的角度（以度数为单位）。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `bearing` | 是 | [number][20] | 目标方向的角度（以度数为单位） |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### getPadding

**`获取地图填充区域的大小，单位为像素。`**

Returns **[PaddingOptions][47]** 当前填充区域的大小。

### setPadding

**`将地图填充区域设置为指定大小，单位为像素。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `padding` | 是 | [PaddingOptions][47] | 目标填充区域的大小 |
| `eventData` | 否 | [EventData][17] | 传递给事件处理程序的事件数据 |

Returns **[Map][14]** 该地图的实例。

### rotateTo

**`旋转地图，使其朝向指定方向。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `bearing` | 是 | [number][20] | 旋转后地图的方向（以度为单位，正北方向为0度，顺时针旋转） |
| `options` | 否 | [AnimationOptions][46] | 旋转动画的选项 |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### resetNorth

**`重置地图的方向为正北方向。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 否 | [AnimationOptions][46] | 旋转动画的选项 |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### resetNorthPitch

**`重置地图的方向和倾斜角度为初始状态。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 否 | [AnimationOptions][46] \| null | 重置动画的选项 |
| `eventData` | 否 | [EventData][17]\| null | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### snapToNorth

**`旋转地图，使其方向朝向正北方向。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 否 | [AnimationOptions][46] | 旋转动画的选项 |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### getPitch

**`获取地图的倾斜角度。`**

Returns **[number][20]** 地图的倾斜角度（以度为单位）。

### setPitch

**`设置地图的倾斜角度。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `pitch` | 是 | [number][20] | 要设置的倾斜角度（以度为单位） |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### cameraForBounds

**`计算缩放和中心点以匹配给定的边界。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `bounds` | 是 | [LngLatBoundsLike][19] | 匹配的边界 |
| `options` | 否 | [CameraForBoundsOptions][48] | 计算相机选项 |

Returns **([CameraForBoundsResult][49] | [undefined][34])** 一个包含缩放、中心点和边框信息的对象。

### fitBounds

**`调整视野以适合指定的地理边界。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `bounds` | 是 | [LngLatBoundsLike][19] | 地理边界 |
| `options` | 否 | [FitBoundsOptions][50] | 拟合边界选项 |
| `eventData` | 否 | [EventData][17] | 触发事件的数据 |

Returns **[Map][14]** 该地图的实例。

### fitScreenCoordinates

**`调整视野以适合两个屏幕点之间的地理边界，使其呈现在窗口的正面。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `p0` | 是 | [PointLike][23] | 屏幕上的点的像素坐标 |
| `p1` | 是 | [PointLike][23] | 屏幕上的点的像素坐标 |
| `bearing` | 是 | [number][20] | 视角的旋转方向（以度为单位） |
| `options` | 否 | `any` | 可选参数 |
| `eventData` | 否 | [EventData][17] | 触发事件的数据 |

Returns **[Map][14]** 该地图的实例。

### jumpTo

**`立即跳转到指定的地图状态，没有动画过渡。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 是 | [CameraOptions][51] | 指定的地图状态 |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### getFreeCameraOptions

**`获取自由摄像机模式的选项。`**

Returns **[FreeCameraOptions][52]** 自由摄像机模式的选项。

### setFreeCameraOptions

**`设置自由摄像机模式的选项。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 是 | [FreeCameraOptions][52] | 自由摄像机模式的选项 |
| `eventData` | 否 | [Object][29] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### easeTo

**`平滑地过渡到指定的地图状态。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 是 | [EaseToOptions][53] | 指定的地图状态 |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### flyTo

**`平滑地飞行到指定的地图状态。`**

#### Parameters
| 参数名 | 必选 | 类型 | 描述 |
| :--- | :--- | :--- | :--- |
| `options` | 是 | [FlyToOptions][54] | 指定的地图状态 |
| `eventData` | 否 | [EventData][17] | 触发事件时的数据 |

Returns **[Map][14]** 该地图的实例。

### isEasing

**`是否正在进行平滑的过渡动画。`**

Returns **[boolean][3]** 如果正在进行平滑的过渡动画，则为 true，否则为 false。

### stop

**`停止当前正在进行的平滑过渡动画。`**

Returns **[Map][14]** 该地图的实例。

[1]: /jsapi/apis/base/Evented.html

[2]: /jsapi/apis/types/Types.html#mapboxoptions

[3]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Boolean

[4]: /jsapi/apis/types/Types.html#scrollzoomhandler

[5]: /jsapi/apis/types/Types.html#boxzoomhandler

[6]: /jsapi/apis/types/Types.html#dragrotatehandler

[7]: /jsapi/apis/types/Types.html#dragpanhandler

[8]: /jsapi/apis/types/Types.html#keyboardhandler

[9]: /jsapi/apis/types/Types.html#doubleclickzoomhandler

[10]: /jsapi/apis/types/Types.html#touchzoomrotatehandler

[11]: /jsapi/apis/types/Types.html#touchpitchhandler

[12]: /jsapi/apis/types/Types.html#control

[13]: /jsapi/apis/types/Types.html#icontrol

[14]: #map

[15]: https://developer.mozilla.org/docs/Web/HTML/Element

[16]: https://developer.mozilla.org/docs/Web/API/HTMLCanvasElement

[17]: /jsapi/apis/types/Types.html#eventdata

[18]: /jsapi/apis/coordinate/LngLatBounds.html

[19]: /jsapi/apis/types/Types.html#lnglatboundslike

[20]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Number

[21]: /jsapi/apis/types/Types.html#lnglatlike

[22]: /jsapi/apis/coordinate/Point.html

[23]: /jsapi/apis/types/Types.html#pointlike

[24]: /jsapi/apis/coordinate/LngLat.html

[25]: /jsapi/apis/types/Types.html#projection

[26]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/String

[27]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Statements/function

[28]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Promise

[29]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object

[30]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Array

[31]: /jsapi/apis/types/Types.html#mapboxgeojsonfeature

[32]: /jsapi/apis/types/Types.html#filteroptions

[33]: /jsapi/apis/types/Types.html#style

[34]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/undefined

[35]: /jsapi/apis/types/Types.html#anysourcedata

[36]: /jsapi/apis/types/Types.html#anysourceimpl

[37]: https://developer.mozilla.org/docs/Web/API/HTMLImageElement

[38]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array

[39]: https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Uint8ClampedArray

[40]: /jsapi/apis/types/Types.html#anylayer

[41]: /jsapi/apis/types/Types.html#light

[42]: /jsapi/apis/types/Types.html#terrainspecification

[43]: /jsapi/apis/types/Types.html#fog

[44]: /jsapi/apis/types/Types.html#featureidentifier

[45]: /jsapi/apis/types/Types.html#elevationqueryoptions

[46]: /jsapi/apis/types/Types.html#animationoptions

[47]: /jsapi/apis/types/Types.html#paddingoptions

[48]: /jsapi/apis/types/Types.html#cameraforboundsoptions

[49]: /jsapi/apis/types/Types.html#cameraforboundsresult

[50]: /jsapi/apis/types/Types.html#fitboundsoptions

[51]: /jsapi/apis/types/Types.html#cameraoptions

[52]: /jsapi/apis/types/Types.html#freecameraoptions

[53]: /jsapi/apis/types/Types.html#easetooptions

[54]: /jsapi/apis/types/Types.html#flytooptions

[55]:/jsapi/apis/types/Types.html#maplayereventtype

[56]:/jsapi/apis/types/Types.html#mapeventtype

