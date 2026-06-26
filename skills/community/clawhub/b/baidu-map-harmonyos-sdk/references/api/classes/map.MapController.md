[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / MapController

# Class: MapController

[map](../modules/map.md).MapController

## Table of contents

### Properties

- [instance](map.MapController.md#instance)
- [baseMap](map.MapController.md#basemap)
- [mapClickListener](map.MapController.md#mapclicklistener)
- [mapViewId](map.MapController.md#mapviewid)
- [filesDir](map.MapController.md#filesdir)
- [cacheDir](map.MapController.md#cachedir)
- [densityDPI](map.MapController.md#densitydpi)
- [dpiScale](map.MapController.md#dpiscale)
- [isDestroy](map.MapController.md#isdestroy)

### Accessors

- [mapOptions](map.MapController.md#mapoptions)
- [maxZoom](map.MapController.md#maxzoom)
- [minZoom](map.MapController.md#minzoom)
- [bmMapCtr](map.MapController.md#bmmapctr)

### Methods

- [getInstance](map.MapController.md#getinstance)
- [alignParameters](map.MapController.md#alignparameters)
- [getMapControlHandle](map.MapController.md#getmapcontrolhandle)
- [getMapViewCtrlInstance](map.MapController.md#getmapviewctrlinstance)
- [createOverlayLayer](map.MapController.md#createoverlaylayer)
- [addOverlay](map.MapController.md#addoverlay)
- [removeOverlay](map.MapController.md#removeoverlay)
- [removeOverlays](map.MapController.md#removeoverlays)
- [getOverlayLayer](map.MapController.md#getoverlaylayer)
- [getOverlayLayers](map.MapController.md#getoverlaylayers)
- [getOverlays](map.MapController.md#getoverlays)
- [getOverlaysAll](map.MapController.md#getoverlaysall)
- [removeOverlayLayer](map.MapController.md#removeoverlaylayer)
- [setViewport](map.MapController.md#setviewport)
- [getViewport](map.MapController.md#getviewport)
- [fitVisibleMapRect](map.MapController.md#fitvisiblemaprect)
- [setViewPadding](map.MapController.md#setviewpadding)
- [setGeoRoundLimit](map.MapController.md#setgeoroundlimit)
- [getZoomUnits](map.MapController.md#getzoomunits)
- [getLayerByTag](map.MapController.md#getlayerbytag)
- [setLocation](map.MapController.md#setlocation)
- [clearCustomLocation](map.MapController.md#clearcustomlocation)
- [setLocationConfig](map.MapController.md#setlocationconfig)
- [setLocationInfo](map.MapController.md#setlocationinfo)
- [pixel2ll](map.MapController.md#pixel2ll)
- [pixel2bdll](map.MapController.md#pixel2bdll)
- [ll2pixel](map.MapController.md#ll2pixel)
- [bdll2pixel](map.MapController.md#bdll2pixel)
- [addEventListener](map.MapController.md#addeventlistener)
- [removeEventListener](map.MapController.md#removeeventlistener)
- [fireMapEvent](map.MapController.md#firemapevent)
- [addOverlayEventListener](map.MapController.md#addoverlayeventlistener)
- [removeOverlayEventListener](map.MapController.md#removeoverlayeventlistener)
- [fireOverlayEvent](map.MapController.md#fireoverlayevent)
- [setOnTouchMessageListener](map.MapController.md#setontouchmessagelistener)
- [changeMapStatusReason](map.MapController.md#changemapstatusreason)
- [triggerMapLoadFinish](map.MapController.md#triggermaploadfinish)
- [setDEMEnable](map.MapController.md#setdemenable)
- [addTileLayer](map.MapController.md#addtilelayer)
- [removeTileLayer](map.MapController.md#removetilelayer)
- [switchLayer](map.MapController.md#switchlayer)
- [setMaxZoom](map.MapController.md#setmaxzoom)
- [setMinZoom](map.MapController.md#setminzoom)
- [zoomTo](map.MapController.md#zoomto)
- [zoomInOne](map.MapController.md#zoominone)
- [zoomOutOne](map.MapController.md#zoomoutone)
- [getZoom](map.MapController.md#getzoom)
- [setMapCenter](map.MapController.md#setmapcenter)
- [setMapCenterWithOffset](map.MapController.md#setmapcenterwithoffset)
- [getCenter](map.MapController.md#getcenter)
- [getRotate](map.MapController.md#getrotate)
- [getPerPixelMc](map.MapController.md#getperpixelmc)
- [enableGesturesRotate](map.MapController.md#enablegesturesrotate)
- [disableGesturesRotate](map.MapController.md#disablegesturesrotate)
- [enableGesturesZoom](map.MapController.md#enablegestureszoom)
- [disableGesturesZoom](map.MapController.md#disablegestureszoom)
- [enableGesturesDrag](map.MapController.md#enablegesturesdrag)
- [disableGesturesDrag](map.MapController.md#disablegesturesdrag)
- [enableGesturesPich](map.MapController.md#enablegesturespich)
- [disableGesturesPich](map.MapController.md#disablegesturespich)
- [switchIndoorFloor](map.MapController.md#switchindoorfloor)
- [getIndoorInfo](map.MapController.md#getindoorinfo)
- [initCustomStyle](map.MapController.md#initcustomstyle)
- [setMapLanguage](map.MapController.md#setmaplanguage)
- [getMapLanguage](map.MapController.md#getmaplanguage)
- [setCustomStylePath](map.MapController.md#setcustomstylepath)
- [setCustomStyleById](map.MapController.md#setcustomstylebyid)
- [setCustomStyleEnable](map.MapController.md#setcustomstyleenable)
- [showBaseIndoorMap](map.MapController.md#showbaseindoormap)
- [isBaseIndoorMapMode](map.MapController.md#isbaseindoormapmode)
- [isBaseIndoorMapShow](map.MapController.md#isbaseindoormapshow)
- [setMapThemeScene](map.MapController.md#setmapthemescene)
- [getMapThemeScene](map.MapController.md#getmapthemescene)
- [showTrafficMap](map.MapController.md#showtrafficmap)
- [switchDayOrDarkTheme](map.MapController.md#switchdayordarktheme)
- [setGestureConfig](map.MapController.md#setgestureconfig)
- [getGestureConfig](map.MapController.md#getgestureconfig)
- [showLayers](map.MapController.md#showlayers)
- [showLayersByTag](map.MapController.md#showlayersbytag)
- [setVirtualPoiShowEnable](map.MapController.md#setvirtualpoishowenable)
- [getVirtualPoiShowEnable](map.MapController.md#getvirtualpoishowenable)
- [setLittle3DEnable](map.MapController.md#setlittle3denable)
- [setEnableOverLook](map.MapController.md#setenableoverlook)
- [getSkyOffset](map.MapController.md#getskyoffset)
- [getLayerIDByTag](map.MapController.md#getlayeridbytag)
- [set3DModelEnable](map.MapController.md#set3dmodelenable)
- [setHouseHeightEnable](map.MapController.md#sethouseheightenable)
- [setOnBackOrForeground](map.MapController.md#setonbackorforeground)
- [setBaiduHeatMapEnabled](map.MapController.md#setbaiduheatmapenabled)
- [addHeatMap](map.MapController.md#addheatmap)
- [startHeatMapFrameAnimation](map.MapController.md#startheatmapframeanimation)
- [stopHeatMapFrameAnimation](map.MapController.md#stopheatmapframeanimation)
- [setHeatMapFrameAnimationIndex](map.MapController.md#setheatmapframeanimationindex)
- [removeHeatMap](map.MapController.md#removeheatmap)
- [updateHeatMap](map.MapController.md#updateheatmap)
- [addHexagonMap](map.MapController.md#addhexagonmap)
- [removeHexagonMap](map.MapController.md#removehexagonmap)
- [customParticleEffectByType](map.MapController.md#customparticleeffectbytype)
- [closeParticleEffectByType](map.MapController.md#closeparticleeffectbytype)
- [showParticleEffectByType](map.MapController.md#showparticleeffectbytype)
- [snapshot](map.MapController.md#snapshot)
- [setMapType](map.MapController.md#setmaptype)
- [setMapClickListener](map.MapController.md#setmapclicklistener)
- [setBgkColor](map.MapController.md#setbgkcolor)
- [resetBgkColor](map.MapController.md#resetbgkcolor)
- [setForceUseBgkColor](map.MapController.md#setforceusebgkcolor)
- [showPoiMarkerPop](map.MapController.md#showpoimarkerpop)
- [onceDraw](map.MapController.md#oncedraw)
- [refresh](map.MapController.md#refresh)
- [destroy](map.MapController.md#destroy)
- [cleanUp](map.MapController.md#cleanup)
- [onWillDisappear](map.MapController.md#onwilldisappear)

## Properties

### instance

▪ `Static` **instance**: [`MapController`](map.MapController.md)

___

### baseMap

• **baseMap**: [`Maybe`](../modules/map.md#maybe)\<[`BaseMap`](map.BaseMap.md)\>

___

### mapClickListener

• **mapClickListener**: ``null`` \| [`IMapClickListener`](../interfaces/map.IMapClickListener.md) = `null`

___

### mapViewId

• `Readonly` **mapViewId**: `string` = `''`

地图唯一标识

___

### filesDir

• `Readonly` **filesDir**: `string` = `''`

沙盒文件目录

___

### cacheDir

• `Readonly` **cacheDir**: `string` = `''`

沙盒缓存目录

___

### densityDPI

• `Readonly` **densityDPI**: `number` = `1`

设备的像素密度

___

### dpiScale

• `Readonly` **dpiScale**: `number` = `1`

适配比例

___

### isDestroy

• **isDestroy**: `boolean` = `false`

## Accessors

### mapOptions

• `get` **mapOptions**(): [`MapOptions`](map.MapOptions.md)

获取地图配置类

#### Returns

[`MapOptions`](map.MapOptions.md)

**`Since`**

1.0.0

• `set` **mapOptions**(`mapOptions`): `void`

设置地图配置类

#### Parameters

| Name | Type |
| :------ | :------ |
| `mapOptions` | [`MapOptions`](map.MapOptions.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### maxZoom

• `get` **maxZoom**(): `number`

获取当前地图最大缩放级别

#### Returns

`number`

**`Since`**

1.0.0

• `set` **maxZoom**(`zoom`): `void`

设置地图最大缩放级别

#### Parameters

| Name | Type |
| :------ | :------ |
| `zoom` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### minZoom

• `get` **minZoom**(): `number`

获取地图最小缩放级别

#### Returns

`number`

**`Since`**

1.0.0

• `set` **minZoom**(`zoom`): `void`

设置地图最小缩放级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `zoom` | `number` | 最小级别，范围3-21 |

#### Returns

`void`

**`Since`**

1.0.0

___

### bmMapCtr

• `get` **bmMapCtr**(): [`Maybe`](../modules/map.md#maybe)\<`default`\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<`default`\>

## Methods

### getInstance

▸ **getInstance**(`bmController`, `context`): [`MapController`](map.MapController.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `bmController` | `default` |
| `context` | `Context` |

#### Returns

[`MapController`](map.MapController.md)

___

### alignParameters

▸ **alignParameters**(): `void`

#### Returns

`void`

___

### getMapControlHandle

▸ **getMapControlHandle**(): `undefined` \| `number`

#### Returns

`undefined` \| `number`

___

### getMapViewCtrlInstance

▸ **getMapViewCtrlInstance**(): `undefined` \| `number`

#### Returns

`undefined` \| `number`

___

### createOverlayLayer

▸ **createOverlayLayer**(`belowId?`): `undefined` \| [`OverlayLayer`](map.OverlayLayer.md)

创建覆盖物图层

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `belowId` | `number` | `0` |

#### Returns

`undefined` \| [`OverlayLayer`](map.OverlayLayer.md)

**`Since`**

1.2.3

___

### addOverlay

▸ **addOverlay**(`overlay`): `void`

添加地图覆盖物

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `overlay` | [`Overlay`](map.Overlay.md) | 覆盖物对象 |

#### Returns

`void`

**`Since`**

1.0.0

___

### removeOverlay

▸ **removeOverlay**(`overlay`): `void`

移除地图覆盖物

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `overlay` | [`Overlay`](map.Overlay.md) | 覆盖物对象 |

#### Returns

`void`

**`Since`**

1.0.0

___

### removeOverlays

▸ **removeOverlays**(`type?`): `void`

按类别移除地图覆盖物

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type?` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) | 覆盖物类型 |

#### Returns

`void`

**`Since`**

1.0.2

___

### getOverlayLayer

▸ **getOverlayLayer**(): [`OverlayLayer`](map.OverlayLayer.md)

获取默认覆盖物图层

#### Returns

[`OverlayLayer`](map.OverlayLayer.md)

**`Since`**

1.2.3

___

### getOverlayLayers

▸ **getOverlayLayers**(): [`OverlayLayer`](map.OverlayLayer.md)[]

获取所有覆盖物图层

#### Returns

[`OverlayLayer`](map.OverlayLayer.md)[]

**`Since`**

2.0.3

___

### getOverlays

▸ **getOverlays**(`type?`): [`Overlay`](map.Overlay.md)[]

获取默认覆盖物图层中的覆盖物

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type?` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) | 指定覆盖物类型 |

#### Returns

[`Overlay`](map.Overlay.md)[]

**`Since`**

2.0.3

___

### getOverlaysAll

▸ **getOverlaysAll**(`type?`): [`Overlay`](map.Overlay.md)[]

获取所有覆盖物图层中的覆盖物

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type?` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) | 指定覆盖物类型 |

#### Returns

[`Overlay`](map.Overlay.md)[]

**`Since`**

2.0.3

___

### removeOverlayLayer

▸ **removeOverlayLayer**(`layer`): `void`

移除覆盖物图层

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | [`OverlayLayer`](map.OverlayLayer.md) |

#### Returns

`void`

**`Since`**

1.2.3

___

### setViewport

▸ **setViewport**(`points`, `options?`): `void`

根据地理坐标设置地图最佳视野

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] | 坐标序列点 |
| `options?` | [`IViewportOption`](../interfaces/map.IViewportOption.md) | 可选配置 |

#### Returns

`void`

**`Since`**

1.1.0

___

### getViewport

▸ **getViewport**(`points`, `options?`): [`IViewportFit`](../interfaces/map.IViewportFit.md)

根据地理坐标获取地图最佳视野

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`Bounds`](base.Bounds.md) \| [`LatLng`](base.LatLng.md)[] | 坐标序列点 |
| `options?` | [`IViewportOption`](../interfaces/map.IViewportOption.md) | 可选配置 |

#### Returns

[`IViewportFit`](../interfaces/map.IViewportFit.md)

表示地图的中心点，偏移量和级别

**`Since`**

1.1.0

___

### fitVisibleMapRect

▸ **fitVisibleMapRect**(`bounds`, `insets`, `withAnimated`): `void`

据当前mapView的窗口大小，预留insets指定的边界区域后，将mapRect指定的地理范围显示在剩余的区域内，并尽量充满

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bounds` | [`Bounds`](base.Bounds.md) | 要显示的地图范围 |
| `insets` | [`WinBound`](map.WinBound.md) | 屏幕四周预留的边界大小 |
| `withAnimated` | `boolean` | - |

#### Returns

`void`

**`Since`**

1.1.0

___

### setViewPadding

▸ **setViewPadding**(`left`, `right`, `top`, `bottom`): `void`

设置地图操作区距控件的距离

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `right` | `number` |
| `top` | `number` |
| `bottom` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### setGeoRoundLimit

▸ **setGeoRoundLimit**(`bounds`): `void`

设置地图操作区地理显示范围

#### Parameters

| Name | Type |
| :------ | :------ |
| `bounds` | [`Bounds`](base.Bounds.md) |

#### Returns

`void`

**`Since`**

1.2.0

___

### getZoomUnits

▸ **getZoomUnits**(`zoom`): `number`

根据级别获取1像素对应的MC单位

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `zoom` | [`Nullable`](../modules/map.md#nullable)\<`number`\> | 级别 |

#### Returns

`number`

___

### getLayerByTag

▸ **getLayerByTag**(`tag`): [`Nullable`](../modules/map.md#nullable)\<[`TLayer`](../modules/map.md#tlayer) \| [`TLayer`](../modules/map.md#tlayer)[]\>

获取图层实例对象

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `tag` | [`LayerTag`](../enums/map.SysEnum.LayerTag.md) | 图层标记 |

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`TLayer`](../modules/map.md#tlayer) \| [`TLayer`](../modules/map.md#tlayer)[]\>

___

### setLocation

▸ **setLocation**(`opts`): `void`

更新定位图层数据

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`ILocation`](../interfaces/map.ILocation.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### clearCustomLocation

▸ **clearCustomLocation**(): `void`

#### Returns

`void`

___

### setLocationConfig

▸ **setLocationConfig**(`opts`): `void`

更新定位图层设置

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`ILocationConfig`](../interfaces/map.ILocationConfig.md) |

#### Returns

`void`

**`Since`**

2.0.0

___

### setLocationInfo

▸ **setLocationInfo**(`data`, `config?`): `void`

更新定位图层信息

#### Parameters

| Name | Type |
| :------ | :------ |
| `data` | [`ILocation`](../interfaces/map.ILocation.md) |
| `config?` | [`ILocationConfig`](../interfaces/map.ILocationConfig.md) |

#### Returns

`void`

**`Since`**

2.0.0

___

### pixel2ll

▸ **pixel2ll**(`left`, `top`): [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

屏幕像素坐标转地理坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `top` | `number` |

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

**`Since`**

1.2.2

___

### pixel2bdll

▸ **pixel2bdll**(`left`, `top`): [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

屏幕像素坐标转百度地理坐标

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `left` | `number` | 像素坐标left |
| `top` | `number` | 像素坐标top |

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

**`Since`**

1.0.0

___

### ll2pixel

▸ **ll2pixel**(`latLng`, `height?`): [`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\>

地理坐标转屏幕像素坐标

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | `undefined` | - |
| `height` | `number` | `0` | 高度，默认0 |

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\>

**`Since`**

1.2.2

___

### bdll2pixel

▸ **bdll2pixel**(`latLng`, `height?`): [`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\>

百度地理坐标转屏幕像素坐标

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | `undefined` | - |
| `height` | `number` | `0` | 高度，默认0 |

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\>

**`Since`**

1.0.0

___

### addEventListener

▸ **addEventListener**(`model`, `fun`): `void`

注册地图事件

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `model` | [`MapEvent`](../enums/map.SysEnum.MapEvent.md) | 地图事件名称 |
| `fun` | [`Callback`](../modules/map.md#callback)\<[`TMapViewEvent`](../modules/map.md#tmapviewevent)\> | 回调响应函数 |

#### Returns

`void`

**`Since`**

1.0.0

___

### removeEventListener

▸ **removeEventListener**(`model`, `fun`): `void`

移除地图事件

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `model` | [`MapEvent`](../enums/map.SysEnum.MapEvent.md) | 地图事件名称 |
| `fun` | [`Callback`](../modules/map.md#callback)\<[`TMapViewEvent`](../modules/map.md#tmapviewevent)\> | 回调响应函数 |

#### Returns

`void`

**`Since`**

1.0.0

___

### fireMapEvent

▸ **fireMapEvent**(`model`, `content`, `reason?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | [`MapEvent`](../enums/map.SysEnum.MapEvent.md) |
| `content` | [`TMapViewEvent`](../modules/map.md#tmapviewevent) |
| `reason?` | [`MapStatusChangeReason`](../enums/map.SysEnum.MapStatusChangeReason.md) |

#### Returns

`void`

___

### addOverlayEventListener

▸ **addOverlayEventListener**(`type`, `model`, `fun`): `void`

添加覆盖物类型统一事件

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) | 覆盖物类型 |
| `model` | [`OverlayEvent`](../enums/map.SysEnum.OverlayEvent.md) | 事件类型 |
| `fun` | [`Callback`](../modules/map.md#callback)\<[`EventOverlayBundle`](../interfaces/map.EventOverlayBundle.md)\> | 回调响应函数 |

#### Returns

`void`

**`Since`**

1.1.2

___

### removeOverlayEventListener

▸ **removeOverlayEventListener**(`type`, `model`, `fun`): `void`

移除覆盖物类型统一事件

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) | 覆盖物类型 |
| `model` | [`OverlayEvent`](../enums/map.SysEnum.OverlayEvent.md) | 事件类型 |
| `fun` | [`Callback`](../modules/map.md#callback)\<[`EventOverlayBundle`](../interfaces/map.EventOverlayBundle.md)\> | 回调响应函数 |

#### Returns

`void`

**`Since`**

1.1.2

___

### fireOverlayEvent

▸ **fireOverlayEvent**(`type`, `model`, `content`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) |
| `model` | [`OverlayEvent`](../enums/map.SysEnum.OverlayEvent.md) |
| `content` | [`EventOverlayBundle`](../interfaces/map.EventOverlayBundle.md) |

#### Returns

`void`

___

### setOnTouchMessageListener

▸ **setOnTouchMessageListener**(`listener`): `void`

设置手势移动监听事件

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | [`OnTouchListener`](../interfaces/map.OnTouchListener.md) |

#### Returns

`void`

**`Since`**

1.2.3

___

### changeMapStatusReason

▸ **changeMapStatusReason**(`reason`): `void`

主动改变状态原因

#### Parameters

| Name | Type |
| :------ | :------ |
| `reason` | [`MapStatusChangeReason`](../enums/map.SysEnum.MapStatusChangeReason.md) |

#### Returns

`void`

**`Since`**

1.2.3

___

### triggerMapLoadFinish

▸ **triggerMapLoadFinish**(): `void`

触发地图加载完成回调
内部方法，由MapLoadStateHandler调用

#### Returns

`void`

___

### setDEMEnable

▸ **setDEMEnable**(`isEnabled`): `void`

地形图

#### Parameters

| Name | Type |
| :------ | :------ |
| `isEnabled` | `boolean` |

#### Returns

`void`

___

### addTileLayer

▸ **addTileLayer**(`layer`): `void`

添加瓦片图层

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

`void`

**`Since`**

1.2.0

___

### removeTileLayer

▸ **removeTileLayer**(`layer`): `void`

移除瓦片图层

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

`void`

**`Since`**

1.2.0

___

### switchLayer

▸ **switchLayer**(`sourceLayer`, `targetLayer`): `any`

交换图层位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `sourceLayer` | `number` |
| `targetLayer` | `number` |

#### Returns

`any`

**`Since`**

1.2.2

▸ **switchLayer**(`sourceLayer`, `targetLayer`): `any`

交换图层位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `sourceLayer` | `default` |
| `targetLayer` | `default` |

#### Returns

`any`

**`Since`**

1.2.2

___

### setMaxZoom

▸ **setMaxZoom**(`zoom`): `void`

设置地图最大缩放级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `zoom` | `number` | 最大级别，范围3-21 |

#### Returns

`void`

**`Since`**

1.0.0

___

### setMinZoom

▸ **setMinZoom**(`zoom`): `void`

设置地图最小缩放级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `zoom` | `number` | 最小级别，范围3-21 |

#### Returns

`void`

**`Since`**

1.0.0

___

### zoomTo

▸ **zoomTo**(`level?`, `center?`, `screenOffset?`): `void`

更新地图到指定等级

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `level` | `number` | `3` | 地图等级，默认为3 |
| `center?` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> | `undefined` | 地图缩放位置地理坐标，可选 |
| `screenOffset?` | [`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\> | `undefined` | 地图缩放位置像素坐标，可选 |

#### Returns

`void`

**`Since`**

1.0.0

___

### zoomInOne

▸ **zoomInOne**(`center?`, `screenOffset?`): `void`

放大地图一级

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `center?` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> | 放大中心点，可选 |
| `screenOffset?` | [`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\> | 地图缩放位置像素坐标，可选 |

#### Returns

`void`

**`Since`**

1.0.0

___

### zoomOutOne

▸ **zoomOutOne**(`center?`, `screenOffset?`): `void`

缩小地图一级

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `center?` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> | 缩小中心点 |
| `screenOffset?` | [`Nullable`](../modules/map.md#nullable)\<[`number`, `number`]\> | 地图缩放位置像素坐标 |

#### Returns

`void`

**`Since`**

1.0.0

___

### getZoom

▸ **getZoom**(): `number`

获取当前地图等级

#### Returns

`number`

**`Since`**

1.0.0

___

### setMapCenter

▸ **setMapCenter**(`center`, `zoom?`, `isAnimate?`, `animationTime?`): `void`

根据经纬度设置并更新地图中心点

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `center` | [`ISetCenter`](../modules/map.md#isetcenter) | `undefined` | 移动到新的地图窗口中心点位置 |
| `zoom` | [`Nullable`](../modules/map.md#nullable)\<`number`\> | `undefined` | 缩放等级 |
| `isAnimate` | `boolean` | `true` | 是否启用动画过度 |
| `animationTime` | `number` | `300` | 动画时间 |

#### Returns

`void`

**`Since`**

1.0.0

___

### setMapCenterWithOffset

▸ **setMapCenterWithOffset**(`center`, `offset`, `zoom`, `isAnimate?`, `animationTime?`): `void`

根据经纬度设置并更新地图中心点

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `center` | [`ISetCenter`](../modules/map.md#isetcenter) | `undefined` | 移动到新的地图窗口中心点位置 |
| `offset` | [`Point`](base.Point.md) | `undefined` | 偏移量，单位像素坐标 |
| `zoom` | [`Nullable`](../modules/map.md#nullable)\<`number`\> | `undefined` | 缩放等级 |
| `isAnimate` | `boolean` | `true` | 是否启用动画过度 |
| `animationTime` | `number` | `300` | 动画时间 |

#### Returns

`void`

**`Since`**

1.1.0

___

### getCenter

▸ **getCenter**(`options?`): [`LatLng`](base.LatLng.md) \| [`Point`](base.Point.md)

获取地图中心点
默认为经纬度坐标，若配置mercator参数为true则返回墨卡托坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `options?` | [`Nullable`](../modules/map.md#nullable)\<[`IGetPoint`](../interfaces/map.IGetPoint.md)\> |

#### Returns

[`LatLng`](base.LatLng.md) \| [`Point`](base.Point.md)

**`Since`**

1.0.0

___

### getRotate

▸ **getRotate**(): `number`

获取旋转角

#### Returns

`number`

**`Since`**

1.0.0

___

### getPerPixelMc

▸ **getPerPixelMc**(): `number`

获取每像素代表多少墨卡托

#### Returns

`number`

**`Since`**

1.0.0

___

### enableGesturesRotate

▸ **enableGesturesRotate**(): `void`

允许手势触发地图旋转

#### Returns

`void`

**`Since`**

1.0.0

___

### disableGesturesRotate

▸ **disableGesturesRotate**(): `void`

不允许手势触发地图旋转

#### Returns

`void`

**`Since`**

1.0.0

___

### enableGesturesZoom

▸ **enableGesturesZoom**(): `void`

允许手势触发地图缩放

#### Returns

`void`

**`Since`**

1.0.0

___

### disableGesturesZoom

▸ **disableGesturesZoom**(): `void`

不允许手势触发地图缩放

#### Returns

`void`

**`Since`**

1.0.0

___

### enableGesturesDrag

▸ **enableGesturesDrag**(): `void`

允许手势触发地图拖动

#### Returns

`void`

**`Since`**

1.0.0

___

### disableGesturesDrag

▸ **disableGesturesDrag**(): `void`

不允许手势触发地图拖动

#### Returns

`void`

**`Since`**

1.0.0

___

### enableGesturesPich

▸ **enableGesturesPich**(): `void`

允许手势触发地图倾斜

#### Returns

`void`

**`Since`**

1.0.0

___

### disableGesturesPich

▸ **disableGesturesPich**(): `void`

不允许手势触发地图倾斜

#### Returns

`void`

**`Since`**

1.0.0

___

### switchIndoorFloor

▸ **switchIndoorFloor**(`floor`, `uid`): `void`

设置显示楼层

#### Parameters

| Name | Type |
| :------ | :------ |
| `floor` | `string` |
| `uid` | `string` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getIndoorInfo

▸ **getIndoorInfo**(`uid?`): [`Nullable`](../modules/map.md#nullable)\<[`IndoorFloorBundles`](../interfaces/map.IndoorFloorBundles.md)\>

获取建筑楼层数据

#### Parameters

| Name | Type |
| :------ | :------ |
| `uid?` | [`Nullable`](../modules/map.md#nullable)\<`string`\> |

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`IndoorFloorBundles`](../interfaces/map.IndoorFloorBundles.md)\>

**`Since`**

1.0.0

___

### initCustomStyle

▸ **initCustomStyle**(`r_path`, `callback`, `overwrite?`): `void`

设置地图样式

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `r_path` | `string` | `undefined` | rawfile样式文件路径 |
| `callback` | [`Callback`](../modules/map.md#callback)\<`void`\> | `undefined` | 回调函数 |
| `overwrite` | `boolean` | `false` | 是否覆盖已经存在的样式 |

#### Returns

`void`

**`Since`**

1.0.0

___

### setMapLanguage

▸ **setMapLanguage**(`language`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `language` | [`MapLanguage`](../enums/map.MapLanguage.md) |

#### Returns

`void`

___

### getMapLanguage

▸ **getMapLanguage**(): `number`

#### Returns

`number`

___

### setCustomStylePath

▸ **setCustomStylePath**(`src`, `resPath?`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `src` | `string` |
| `resPath?` | `string` |

#### Returns

`boolean`

___

### setCustomStyleById

▸ **setCustomStyleById**(`styleId`, `styleCallBack?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `styleId` | `string` |
| `styleCallBack?` | [`CustomMapStyleCallBack`](../interfaces/map.CustomMapStyleCallBack.md) |

#### Returns

`void`

___

### setCustomStyleEnable

▸ **setCustomStyleEnable**(`enable`): `boolean`

地图切换显示个性化样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

`boolean`

**`Since`**

1.0.0

___

### showBaseIndoorMap

▸ **showBaseIndoorMap**(`bShow`): `void`

设置室内地图显示

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bShow` | `boolean` | 是否显示 |

#### Returns

`void`

___

### isBaseIndoorMapMode

▸ **isBaseIndoorMapMode**(): `boolean`

检查是否处于室内地图模式

#### Returns

`boolean`

是否处于室内地图模式

___

### isBaseIndoorMapShow

▸ **isBaseIndoorMapShow**(): `boolean`

检查室内地图是否显示

#### Returns

`boolean`

室内地图是否显示

___

### setMapThemeScene

▸ **setMapThemeScene**(`themeId`, `sceneId`): `void`

设置地图主题场景

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `themeId` | `number` | 主题ID |
| `sceneId` | `number` | 场景ID |

#### Returns

`void`

___

### getMapThemeScene

▸ **getMapThemeScene**(): `undefined` \| ``null`` \| `NAThemeScene`

获取地图主题场景

#### Returns

`undefined` \| ``null`` \| `NAThemeScene`

地图主题场景

___

### showTrafficMap

▸ **showTrafficMap**(`bShow`): `void`

显示交通图层

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bShow` | `boolean` | 是否显示 |

#### Returns

`void`

___

### switchDayOrDarkTheme

▸ **switchDayOrDarkTheme**(`theme`, `isDarkMode`): `void`

切换日间/夜间主题

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `theme` | `number` | 主题ID |
| `isDarkMode` | `boolean` | 是否为暗黑模式 |

#### Returns

`void`

___

### setGestureConfig

▸ **setGestureConfig**(`config`): `void`

设置手势配置

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `config` | `IGestureConfig` | 手势配置 |

#### Returns

`void`

___

### getGestureConfig

▸ **getGestureConfig**(): ``null`` \| `IGestureConfig`

获取手势配置

#### Returns

``null`` \| `IGestureConfig`

手势配置

___

### showLayers

▸ **showLayers**(`layerId`, `bShow`): `void`

显示/隐藏图层

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `layerId` | `number` | 图层ID |
| `bShow` | `boolean` | 是否显示 |

#### Returns

`void`

___

### showLayersByTag

▸ **showLayersByTag**(`layerTag`, `bShow`): `void`

根据标签显示/隐藏图层

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `layerTag` | `string` | 图层标签 |
| `bShow` | `boolean` | 是否显示 |

#### Returns

`void`

___

### setVirtualPoiShowEnable

▸ **setVirtualPoiShowEnable**(`bShow`): `void`

设置虚拟POI显示是否启用

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bShow` | `boolean` | 是否显示 |

#### Returns

`void`

___

### getVirtualPoiShowEnable

▸ **getVirtualPoiShowEnable**(): `boolean`

获取虚拟POI显示是否启用

#### Returns

`boolean`

是否启用虚拟POI显示

___

### setLittle3DEnable

▸ **setLittle3DEnable**(`enable`): `void`

设置小地图3D效果

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `enable` | `boolean` | 是否启用 |

#### Returns

`void`

___

### setEnableOverLook

▸ **setEnableOverLook**(`bCanOverLook`): `void`

设置是否允许俯视

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bCanOverLook` | `boolean` | 是否允许俯视 |

#### Returns

`void`

___

### getSkyOffset

▸ **getSkyOffset**(): `number`

获取天空偏移

#### Returns

`number`

天空偏移值

___

### getLayerIDByTag

▸ **getLayerIDByTag**(`tag`): `number`

根据标签获取图层ID

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `tag` | `string` | 图层标签 |

#### Returns

`number`

图层ID

___

### set3DModelEnable

▸ **set3DModelEnable**(`isEnable`): `void`

设置3D模型显示是否启用

#### Parameters

| Name | Type |
| :------ | :------ |
| `isEnable` | `boolean` |

#### Returns

`void`

**`Since`**

2.0.0

___

### setHouseHeightEnable

▸ **setHouseHeightEnable**(`isEnable`): `void`

设置建筑高度显示是否启用

#### Parameters

| Name | Type |
| :------ | :------ |
| `isEnable` | `boolean` |

#### Returns

`void`

**`Since`**

2.0.2

___

### setOnBackOrForeground

▸ **setOnBackOrForeground**(`isForeground`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isForeground` | `boolean` |

#### Returns

`void`

___

### setBaiduHeatMapEnabled

▸ **setBaiduHeatMapEnabled**(`enabled`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enabled` | `boolean` |

#### Returns

`void`

___

### addHeatMap

▸ **addHeatMap**(`heatmap`): `void`

添加自定义热力图

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `heatmap` | [`HeatMap`](map.HeatMap.md) | 自定义热力图 |

#### Returns

`void`

___

### startHeatMapFrameAnimation

▸ **startHeatMapFrameAnimation**(): `void`

开始热力图帧动画

#### Returns

`void`

___

### stopHeatMapFrameAnimation

▸ **stopHeatMapFrameAnimation**(): `void`

停止热力图帧动画

#### Returns

`void`

___

### setHeatMapFrameAnimationIndex

▸ **setHeatMapFrameAnimationIndex**(`index`): `void`

设置热力图帧

#### Parameters

| Name | Type |
| :------ | :------ |
| `index` | `number` |

#### Returns

`void`

___

### removeHeatMap

▸ **removeHeatMap**(`heatmap`): `void`

移除自定义热力图

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `heatmap` | [`HeatMap`](map.HeatMap.md) | 自定义热力图 |

#### Returns

`void`

___

### updateHeatMap

▸ **updateHeatMap**(`heatmap`): `void`

更新热力图

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `heatmap` | [`HeatMap`](map.HeatMap.md) | 热力图对象 |

#### Returns

`void`

___

### addHexagonMap

▸ **addHexagonMap**(`hexagonMap`): `void`

添加蜂窝热力图

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `hexagonMap` | [`HexagonMap`](map.HexagonMap.md) | 蜂窝热力图 |

#### Returns

`void`

___

### removeHexagonMap

▸ **removeHexagonMap**(`hexagonMap`): `void`

移除蜂窝热力图

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `hexagonMap` | [`HexagonMap`](map.HexagonMap.md) | 蜂窝热力图 |

#### Returns

`void`

___

### customParticleEffectByType

▸ **customParticleEffectByType**(`particleEffectType`, `particleOptions`): `Promise`\<`boolean`\>

自定义粒子效果

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `particleEffectType` | [`ParticleEffectType`](../enums/map.SysEnum.ParticleEffectType.md) | 效果类型 |
| `particleOptions` | [`ParticleOptions`](map.ParticleOptions.md) | 粒子效果 |

#### Returns

`Promise`\<`boolean`\>

___

### closeParticleEffectByType

▸ **closeParticleEffectByType**(`particleEffectType`): `void`

关闭粒子效果

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `particleEffectType` | [`ParticleEffectType`](../enums/map.SysEnum.ParticleEffectType.md) | 效果类型 |

#### Returns

`void`

___

### showParticleEffectByType

▸ **showParticleEffectByType**(`particleEffectType`): `boolean`

显示粒子效果

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `particleEffectType` | [`ParticleEffectType`](../enums/map.SysEnum.ParticleEffectType.md) | 效果类型 |

#### Returns

`boolean`

___

### snapshot

▸ **snapshot**(`region?`): `Promise`\<`PixelMap`\>

发起地图截图

#### Parameters

| Name | Type |
| :------ | :------ |
| `region?` | `any` |

#### Returns

`Promise`\<`PixelMap`\>

___

### setMapType

▸ **setMapType**(`type`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`MapType`](../enums/map.SysEnum.MapType.md) |

#### Returns

`void`

___

### setMapClickListener

▸ **setMapClickListener**(`listener`): `void`

注册点击事件

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `listener` | [`IMapClickListener`](../interfaces/map.IMapClickListener.md) | 回调响应函数 |

#### Returns

`void`

**`Since`**

2.0.0

___

### setBgkColor

▸ **setBgkColor**(`color`): `void`

设置背景色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

2.0.3

___

### resetBgkColor

▸ **resetBgkColor**(): `void`

重置背景色

#### Returns

`void`

**`Since`**

2.0.3

___

### setForceUseBgkColor

▸ **setForceUseBgkColor**(`isUse`): `void`

设置是否强制使用背景色

#### Parameters

| Name | Type |
| :------ | :------ |
| `isUse` | `boolean` |

#### Returns

`void`

**`Since`**

2.0.3

___

### showPoiMarkerPop

▸ **showPoiMarkerPop**(`bShow`): `void`

设置 POI 标记弹窗的显示/隐藏状态
注意：此方法仅在中文语言环境下生效，其他语言环境下调用无效

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bShow` | `boolean` | 是否显示 POI 气泡，true 表示显示，false 表示隐藏 |

#### Returns

`void`

**`Since`**

1.0.0

___

### onceDraw

▸ **onceDraw**(): `void`

主动调用绘制一次

#### Returns

`void`

**`Since`**

1.0.2

___

### refresh

▸ **refresh**(): `void`

#### Returns

`void`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`

___

### cleanUp

▸ **cleanUp**(): `void`

清理地图内部实例

#### Returns

`void`

___

### onWillDisappear

▸ **onWillDisappear**(): `void`

销毁地图控制器实例
如果使用Navigation框架，需要在onWillDisappear中调用此方法，进行销毁

#### Returns

`void`
