[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / BaseMap

# Class: BaseMap

[map](../modules/map.md).BaseMap

BaseMap 类用于管理地图的基本操作。
该类扩展了基线引擎BaseMap，提供了额外的功能和接口，以便于处理更多类型的图层和覆盖物.

## Table of contents

### Constructors

- [constructor](map.BaseMap.md#constructor)

### Accessors

- [baselineBaseMap](map.BaseMap.md#baselinebasemap)

### Methods

- [setMapLanguage](map.BaseMap.md#setmaplanguage)
- [showPOIMarkerPop](map.BaseMap.md#showpoimarkerpop)
- [getMapLanguage](map.BaseMap.md#getmaplanguage)
- [getMapViewCtrlInstance](map.BaseMap.md#getmapviewctrlinstance)
- [getMapControlHandle](map.BaseMap.md#getmapcontrolhandle)
- [addTileLayer](map.BaseMap.md#addtilelayer)
- [updateTileLayer](map.BaseMap.md#updatetilelayer)
- [cleanSDKTileCache](map.BaseMap.md#cleansdktilecache)
- [createAddLayer](map.BaseMap.md#createaddlayer)
- [setGestureEnable](map.BaseMap.md#setgestureenable)
- [setGestureConfig](map.BaseMap.md#setgestureconfig)
- [setMinLevel](map.BaseMap.md#setminlevel)
- [setMaxLevel](map.BaseMap.md#setmaxlevel)
- [setDBClickEnable](map.BaseMap.md#setdbclickenable)
- [setTouchNearly](map.BaseMap.md#settouchnearly)
- [setMapStatus](map.BaseMap.md#setmapstatus)
- [updateShowCustomLayer](map.BaseMap.md#updateshowcustomlayer)
- [showPoiMarker](map.BaseMap.md#showpoimarker)
- [showIndoorPoiMarker](map.BaseMap.md#showindoorpoimarker)
- [fetchMapStatus](map.BaseMap.md#fetchmapstatus)
- [getMapOptions](map.BaseMap.md#getmapoptions)
- [relativePixel](map.BaseMap.md#relativepixel)
- [showLayer](map.BaseMap.md#showlayer)
- [updateLayer](map.BaseMap.md#updatelayer)
- [addLayer](map.BaseMap.md#addlayer)
- [removeLayer](map.BaseMap.md#removelayer)
- [clearLayer](map.BaseMap.md#clearlayer)
- [getOverlays](map.BaseMap.md#getoverlays)
- [findOverlayByName](map.BaseMap.md#findoverlaybyname)
- [zoom](map.BaseMap.md#zoom)
- [setMapStatusLimits](map.BaseMap.md#setmapstatuslimits)
- [rotatePlus](map.BaseMap.md#rotateplus)
- [overlookingPlus](map.BaseMap.md#overlookingplus)
- [setPixelToCenter](map.BaseMap.md#setpixeltocenter)
- [getZoomToBoundF](map.BaseMap.md#getzoomtoboundf)
- [registMapViewListener](map.BaseMap.md#registmapviewlistener)
- [getDefaultCompassLayer](map.BaseMap.md#getdefaultcompasslayer)
- [getDefaultLocationLayer](map.BaseMap.md#getdefaultlocationlayer)
- [showTrafficMap](map.BaseMap.md#showtrafficmap)
- [showBaseIndoorMap](map.BaseMap.md#showbaseindoormap)
- [setBaseMapLayerEnable](map.BaseMap.md#setbasemaplayerenable)
- [isBaseIndoorMapMode](map.BaseMap.md#isbaseindoormapmode)
- [isBaseIndoorMapShow](map.BaseMap.md#isbaseindoormapshow)
- [setEnableOverLook](map.BaseMap.md#setenableoverlook)
- [switchIndoorFloor](map.BaseMap.md#switchindoorfloor)
- [getIndoorInfo](map.BaseMap.md#getindoorinfo)
- [changeCustomStyle](map.BaseMap.md#changecustomstyle)
- [initCustomStyle](map.BaseMap.md#initcustomstyle)
- [setCustomStyleEnable](map.BaseMap.md#setcustomstyleenable)
- [getNearlyObjID](map.BaseMap.md#getnearlyobjid)
- [setOnBackOrForeground](map.BaseMap.md#setonbackorforeground)
- [set3DModelEnable](map.BaseMap.md#set3dmodelenable)
- [setHouseHeightEnable](map.BaseMap.md#sethouseheightenable)
- [showParticleEffectByType](map.BaseMap.md#showparticleeffectbytype)
- [closeParticleEffectByType](map.BaseMap.md#closeparticleeffectbytype)
- [customParticleEffectByType](map.BaseMap.md#customparticleeffectbytype)
- [addHexagonMapData](map.BaseMap.md#addhexagonmapdata)
- [setBaiduHeatMapEnabled](map.BaseMap.md#setbaiduheatmapenabled)
- [clearHexagonLayerCache](map.BaseMap.md#clearhexagonlayercache)
- [setHexagonMapEnabled](map.BaseMap.md#sethexagonmapenabled)
- [clearHeatMapLayerCache](map.BaseMap.md#clearheatmaplayercache)
- [initHeatMapData](map.BaseMap.md#initheatmapdata)
- [updateHeatMapData](map.BaseMap.md#updateheatmapdata)
- [setHeatMapEnabled](map.BaseMap.md#setheatmapenabled)
- [startHeatMapFrameAnimation](map.BaseMap.md#startheatmapframeanimation)
- [stopHeatMapFrameAnimation](map.BaseMap.md#stopheatmapframeanimation)
- [setHeatMapFrameAnimationIndex](map.BaseMap.md#setheatmapframeanimationindex)
- [geoPoint3toScreenLocation](map.BaseMap.md#geopoint3toscreenlocation)
- [setDEMEnable](map.BaseMap.md#setdemenable)
- [setBgkColor](map.BaseMap.md#setbgkcolor)
- [resetBgkColor](map.BaseMap.md#resetbgkcolor)
- [setForceUseBgkColor](map.BaseMap.md#setforceusebgkcolor)

## Constructors

### constructor

• **new BaseMap**(`baselineBaseMap`): [`BaseMap`](map.BaseMap.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `baselineBaseMap` | `default` |

#### Returns

[`BaseMap`](map.BaseMap.md)

## Accessors

### baselineBaseMap

• `get` **baselineBaseMap**(): `default`

#### Returns

`default`

## Methods

### setMapLanguage

▸ **setMapLanguage**(`language`, `needCleanCache`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `language` | `number` |
| `needCleanCache` | `boolean` |

#### Returns

`boolean`

___

### showPOIMarkerPop

▸ **showPOIMarkerPop**(`isShow`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isShow` | `boolean` |

#### Returns

`void`

___

### getMapLanguage

▸ **getMapLanguage**(): `number`

#### Returns

`number`

___

### getMapViewCtrlInstance

▸ **getMapViewCtrlInstance**(): `number`

#### Returns

`number`

___

### getMapControlHandle

▸ **getMapControlHandle**(): `number`

#### Returns

`number`

___

### addTileLayer

▸ **addTileLayer**(`layer`, `addSDKTileBundle`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |
| `addSDKTileBundle` | `AddSDKTileBundle` |

#### Returns

`boolean`

___

### updateTileLayer

▸ **updateTileLayer**(`layer`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

`void`

___

### cleanSDKTileCache

▸ **cleanSDKTileCache**(`layer`): ``null`` \| `number`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

``null`` \| `number`

___

### createAddLayer

▸ **createAddLayer**(`eUpdataType`, `ulTimerEscap`, `tag`): `number`

#### Parameters

| Name | Type |
| :------ | :------ |
| `eUpdataType` | `number` |
| `ulTimerEscap` | `number` |
| `tag` | `string` |

#### Returns

`number`

___

### setGestureEnable

▸ **setGestureEnable**(`canMoving?`, `canZoom?`, `canRotate?`, `canOverLook?`): `void`

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `canMoving` | `boolean` | `true` |
| `canZoom` | `boolean` | `true` |
| `canRotate` | `boolean` | `true` |
| `canOverLook` | `boolean` | `true` |

#### Returns

`void`

___

### setGestureConfig

▸ **setGestureConfig**(`bundle`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | `AnyObject` |

#### Returns

`void`

___

### setMinLevel

▸ **setMinLevel**(`level`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `level` | `number` |

#### Returns

`void`

___

### setMaxLevel

▸ **setMaxLevel**(`level`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `level` | `number` |

#### Returns

`void`

___

### setDBClickEnable

▸ **setDBClickEnable**(`enable`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

`void`

___

### setTouchNearly

▸ **setTouchNearly**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

___

### setMapStatus

▸ **setMapStatus**(`bundle`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | [`MapStatusBundle`](../interfaces/map.MapStatusBundle.md) |

#### Returns

`void`

___

### updateShowCustomLayer

▸ **updateShowCustomLayer**(`bundle`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | [`MapOptionBundle`](../interfaces/map.MapOptionBundle.md) |

#### Returns

`void`

___

### showPoiMarker

▸ **showPoiMarker**(`isShow`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isShow` | `boolean` |

#### Returns

`void`

___

### showIndoorPoiMarker

▸ **showIndoorPoiMarker**(`isShow`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isShow` | `boolean` |

#### Returns

`void`

___

### fetchMapStatus

▸ **fetchMapStatus**(): `NativeMapStatusBundle`

#### Returns

`NativeMapStatusBundle`

___

### getMapOptions

▸ **getMapOptions**(): `default`

#### Returns

`default`

___

### relativePixel

▸ **relativePixel**(`ll`): [`number`, `number`]

#### Parameters

| Name | Type |
| :------ | :------ |
| `ll` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> |

#### Returns

[`number`, `number`]

___

### showLayer

▸ **showLayer**(`layerId`, `bShow`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layerId` | `number` |
| `bShow` | `boolean` |

#### Returns

`void`

___

### updateLayer

▸ **updateLayer**(`layer`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

`void`

___

### addLayer

▸ **addLayer**(`layer`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

`void`

___

### removeLayer

▸ **removeLayer**(`layer`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layer` | `default` |

#### Returns

`boolean`

___

### clearLayer

▸ **clearLayer**(`layerId`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `layerId` | `number` |

#### Returns

`void`

___

### getOverlays

▸ **getOverlays**(): `List`\<`default`\>

#### Returns

`List`\<`default`\>

___

### findOverlayByName

▸ **findOverlayByName**(`name`): ``null`` \| `default`

#### Parameters

| Name | Type |
| :------ | :------ |
| `name` | `string` |

#### Returns

``null`` \| `default`

___

### zoom

▸ **zoom**(`mapStatus`, `level`, `ptOffset?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `mapStatus` | [`MapStatus`](map.MapStatus.md) |
| `level` | `number` |
| `ptOffset` | [`number`, `number`] |

#### Returns

`void`

___

### setMapStatusLimits

▸ **setMapStatusLimits**(`b`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `b` | `default` |

#### Returns

`void`

___

### rotatePlus

▸ **rotatePlus**(`deg`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `deg` | `number` |

#### Returns

`void`

___

### overlookingPlus

▸ **overlookingPlus**(`deg`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `deg` | `number` |

#### Returns

`void`

___

### setPixelToCenter

▸ **setPixelToCenter**(`left`, `top`, `isAnimate`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `top` | `number` |
| `isAnimate` | `boolean` |

#### Returns

`void`

___

### getZoomToBoundF

▸ **getZoomToBoundF**(`bundle`, `screenBd?`): `number`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | `default` |
| `screenBd?` | `default` |

#### Returns

`number`

___

### registMapViewListener

▸ **registMapViewListener**(`mapListener`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `mapListener` | `default` |

#### Returns

`void`

___

### getDefaultCompassLayer

▸ **getDefaultCompassLayer**(): ``null`` \| `default`

#### Returns

``null`` \| `default`

___

### getDefaultLocationLayer

▸ **getDefaultLocationLayer**(): ``null`` \| `default`

#### Returns

``null`` \| `default`

___

### showTrafficMap

▸ **showTrafficMap**(`bShow`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bShow` | `boolean` |

#### Returns

`void`

___

### showBaseIndoorMap

▸ **showBaseIndoorMap**(`bShow`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bShow` | `boolean` |

#### Returns

`void`

___

### setBaseMapLayerEnable

▸ **setBaseMapLayerEnable**(`enable`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

`void`

___

### isBaseIndoorMapMode

▸ **isBaseIndoorMapMode**(): `boolean`

#### Returns

`boolean`

___

### isBaseIndoorMapShow

▸ **isBaseIndoorMapShow**(): `boolean`

#### Returns

`boolean`

___

### setEnableOverLook

▸ **setEnableOverLook**(`bCanOverLook`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bCanOverLook` | `boolean` |

#### Returns

`void`

___

### switchIndoorFloor

▸ **switchIndoorFloor**(`obj`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `obj` | [`Nullable`](../modules/map.md#nullable)\<`IndoorBundle`\> |

#### Returns

`void`

___

### getIndoorInfo

▸ **getIndoorInfo**(`obj`): [`IndoorFloorBundles`](../interfaces/map.IndoorFloorBundles.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `obj` | [`Nullable`](../modules/map.md#nullable)\<`IndoorBundle`\> |

#### Returns

[`IndoorFloorBundles`](../interfaces/map.IndoorFloorBundles.md)

___

### changeCustomStyle

▸ **changeCustomStyle**(`resourceManager`, `overwrite`, `r_path`, `path`, `callback`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `resourceManager` | `ResourceManager` |
| `overwrite` | `boolean` |
| `r_path` | `string` |
| `path` | `string` |
| `callback` | [`Callback`](../modules/map.md#callback)\<`void`\> |

#### Returns

`void`

___

### initCustomStyle

▸ **initCustomStyle**(`path`, `res_path?`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `path` | `string` |
| `res_path?` | `string` |

#### Returns

`boolean`

___

### setCustomStyleEnable

▸ **setCustomStyleEnable**(`enable`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `number` |

#### Returns

`boolean`

___

### getNearlyObjID

▸ **getNearlyObjID**(`x`, `y`, `radius`): ``null`` \| `string`

#### Parameters

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |
| `radius` | `number` |

#### Returns

``null`` \| `string`

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

### set3DModelEnable

▸ **set3DModelEnable**(`isEnable`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isEnable` | `boolean` |

#### Returns

`void`

___

### setHouseHeightEnable

▸ **setHouseHeightEnable**(`isEnable`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isEnable` | `boolean` |

#### Returns

`void`

___

### showParticleEffectByType

▸ **showParticleEffectByType**(`type`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`ParticleEffectType`](../enums/map.SysEnum.ParticleEffectType.md) |

#### Returns

`boolean`

___

### closeParticleEffectByType

▸ **closeParticleEffectByType**(`type`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`ParticleEffectType`](../enums/map.SysEnum.ParticleEffectType.md) |

#### Returns

`void`

___

### customParticleEffectByType

▸ **customParticleEffectByType**(`type`, `options`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`ParticleEffectType`](../enums/map.SysEnum.ParticleEffectType.md) |
| `options` | `object` |

#### Returns

`boolean`

___

### addHexagonMapData

▸ **addHexagonMapData**(`bundle`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | `HexagonMapBundle` |

#### Returns

`void`

___

### setBaiduHeatMapEnabled

▸ **setBaiduHeatMapEnabled**(`enabled`, `type`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enabled` | `boolean` |
| `type` | `number` |

#### Returns

`void`

___

### clearHexagonLayerCache

▸ **clearHexagonLayerCache**(): `void`

#### Returns

`void`

___

### setHexagonMapEnabled

▸ **setHexagonMapEnabled**(`enabled`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enabled` | `boolean` |

#### Returns

`void`

___

### clearHeatMapLayerCache

▸ **clearHeatMapLayerCache**(): `void`

#### Returns

`void`

___

### initHeatMapData

▸ **initHeatMapData**(`bundle`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | `HeatMapBundle` |

#### Returns

`void`

___

### updateHeatMapData

▸ **updateHeatMapData**(`bundle`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | `HeatMapBundle` |

#### Returns

`void`

___

### setHeatMapEnabled

▸ **setHeatMapEnabled**(`enabled`, `data?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `enabled` | `boolean` |
| `data?` | `string` |

#### Returns

`void`

___

### startHeatMapFrameAnimation

▸ **startHeatMapFrameAnimation**(): `void`

#### Returns

`void`

___

### stopHeatMapFrameAnimation

▸ **stopHeatMapFrameAnimation**(): `void`

#### Returns

`void`

___

### setHeatMapFrameAnimationIndex

▸ **setHeatMapFrameAnimationIndex**(`idx`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `idx` | `number` |

#### Returns

`void`

___

### geoPoint3toScreenLocation

▸ **geoPoint3toScreenLocation**(`x`, `y`, `z`): ``null`` \| `NativePoint`

#### Parameters

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |
| `z` | `number` |

#### Returns

``null`` \| `NativePoint`

___

### setDEMEnable

▸ **setDEMEnable**(`isEnable`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isEnable` | `boolean` |

#### Returns

`void`

___

### setBgkColor

▸ **setBgkColor**(`r`, `g`, `b`, `a`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `r` | `number` |
| `g` | `number` |
| `b` | `number` |
| `a` | `number` |

#### Returns

`void`

___

### resetBgkColor

▸ **resetBgkColor**(): `void`

#### Returns

`void`

___

### setForceUseBgkColor

▸ **setForceUseBgkColor**(`use`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `use` | `boolean` |

#### Returns

`void`
