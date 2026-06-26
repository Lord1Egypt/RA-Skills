[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Bd\_3DModel

# Class: Bd\_3DModel

[map](../modules/map.md).Bd_3DModel

3DModel覆盖物

**`Abstract`**

提供3DModel覆盖物创建、操作方法

**`Since`**

2.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Bd_3DModel`**

## Table of contents

### Constructors

- [constructor](map.Bd_3DModel.md#constructor)

### Properties

- [uuid](map.Bd_3DModel.md#uuid)
- [type](map.Bd_3DModel.md#type)
- [eventListener](map.Bd_3DModel.md#eventlistener)
- [isDestroyed](map.Bd_3DModel.md#isdestroyed)

### Accessors

- [typeName](map.Bd_3DModel.md#typename)
- [visible](map.Bd_3DModel.md#visible)
- [zIndex](map.Bd_3DModel.md#zindex)

### Methods

- [setModelPath](map.Bd_3DModel.md#setmodelpath)
- [setModelName](map.Bd_3DModel.md#setmodelname)
- [setPosition](map.Bd_3DModel.md#setposition)
- [setScale](map.Bd_3DModel.md#setscale)
- [setZoomFixed](map.Bd_3DModel.md#setzoomfixed)
- [setRotate](map.Bd_3DModel.md#setrotate)
- [setOffset](map.Bd_3DModel.md#setoffset)
- [setBM3DModelType](map.Bd_3DModel.md#setbm3dmodeltype)
- [setSkeletonAnimationEnable](map.Bd_3DModel.md#setskeletonanimationenable)
- [setAnimationRepeatCount](map.Bd_3DModel.md#setanimationrepeatcount)
- [setAnimationSpeed](map.Bd_3DModel.md#setanimationspeed)
- [setAnimationIndex](map.Bd_3DModel.md#setanimationindex)
- [getModelPath](map.Bd_3DModel.md#getmodelpath)
- [getModelName](map.Bd_3DModel.md#getmodelname)
- [getPosition](map.Bd_3DModel.md#getposition)
- [getScale](map.Bd_3DModel.md#getscale)
- [isZoomFixed](map.Bd_3DModel.md#iszoomfixed)
- [getRotateX](map.Bd_3DModel.md#getrotatex)
- [getRotateY](map.Bd_3DModel.md#getrotatey)
- [getRotateZ](map.Bd_3DModel.md#getrotatez)
- [getOffsetX](map.Bd_3DModel.md#getoffsetx)
- [getOffsetY](map.Bd_3DModel.md#getoffsety)
- [getOffsetZ](map.Bd_3DModel.md#getoffsetz)
- [getBM3DModelType](map.Bd_3DModel.md#getbm3dmodeltype)
- [isSkeletonAnimationEnable](map.Bd_3DModel.md#isskeletonanimationenable)
- [getAnimationRepeatCount](map.Bd_3DModel.md#getanimationrepeatcount)
- [getAnimationSpeed](map.Bd_3DModel.md#getanimationspeed)
- [getAnimationIndex](map.Bd_3DModel.md#getanimationindex)
- [startAnimation](map.Bd_3DModel.md#startanimation)
- [pauseAnimation](map.Bd_3DModel.md#pauseanimation)
- [resumeAnimation](map.Bd_3DModel.md#resumeanimation)
- [cancelAnimation](map.Bd_3DModel.md#cancelanimation)
- [getDrawItem](map.Bd_3DModel.md#getdrawitem)
- [toString](map.Bd_3DModel.md#tostring)
- [putPointsInfoIntoBundle](map.Bd_3DModel.md#putpointsinfointobundle)
- [addEventListener](map.Bd_3DModel.md#addeventlistener)
- [removeEventListener](map.Bd_3DModel.md#removeeventlistener)
- [addDragListener](map.Bd_3DModel.md#adddraglistener)
- [removeDragListener](map.Bd_3DModel.md#removedraglistener)
- [getDragListener](map.Bd_3DModel.md#getdraglistener)
- [fireEvent](map.Bd_3DModel.md#fireevent)
- [getType](map.Bd_3DModel.md#gettype)
- [setAnimation](map.Bd_3DModel.md#setanimation)
- [getAnimation](map.Bd_3DModel.md#getanimation)
- [setVisible](map.Bd_3DModel.md#setvisible)
- [getVisible](map.Bd_3DModel.md#getvisible)
- [alpha](map.Bd_3DModel.md#alpha)
- [getAlpha](map.Bd_3DModel.md#getalpha)
- [setAlpha](map.Bd_3DModel.md#setalpha)
- [startLevel](map.Bd_3DModel.md#startlevel)
- [getStartLevel](map.Bd_3DModel.md#getstartlevel)
- [setStartLevel](map.Bd_3DModel.md#setstartlevel)
- [endLevel](map.Bd_3DModel.md#endlevel)
- [showLevel](map.Bd_3DModel.md#showlevel)
- [getEndLevel](map.Bd_3DModel.md#getendlevel)
- [setShowLevel](map.Bd_3DModel.md#setshowlevel)
- [setEndLevel](map.Bd_3DModel.md#setendlevel)
- [clickable](map.Bd_3DModel.md#clickable)
- [getClickable](map.Bd_3DModel.md#getclickable)
- [setClickable](map.Bd_3DModel.md#setclickable)
- [setZIndex](map.Bd_3DModel.md#setzindex)
- [getZIndex](map.Bd_3DModel.md#getzindex)
- [setExtraInfo](map.Bd_3DModel.md#setextrainfo)
- [getExtraInfo](map.Bd_3DModel.md#getextrainfo)
- [getBmDrawItem](map.Bd_3DModel.md#getbmdrawitem)
- [update](map.Bd_3DModel.md#update)
- [remove](map.Bd_3DModel.md#remove)
- [isRemoved](map.Bd_3DModel.md#isremoved)
- [destroy](map.Bd_3DModel.md#destroy)

## Constructors

### constructor

• **new Bd_3DModel**(`opts`): [`Bd_3DModel`](map.Bd_3DModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`I3DModelOption`](../interfaces/map.I3DModelOption.md) |

#### Returns

[`Bd_3DModel`](map.Bd_3DModel.md)

#### Overrides

Overlay.constructor

## Properties

### uuid

• **uuid**: `string`

#### Inherited from

[Overlay](map.Overlay.md).[uuid](map.Overlay.md#uuid)

___

### type

• **type**: `default`

#### Inherited from

[Overlay](map.Overlay.md).[type](map.Overlay.md#type)

___

### eventListener

• **eventListener**: `TOverlayListener` = `{}`

#### Inherited from

[Overlay](map.Overlay.md).[eventListener](map.Overlay.md#eventlistener)

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

#### Inherited from

[Overlay](map.Overlay.md).[isDestroyed](map.Overlay.md#isdestroyed)

## Accessors

### typeName

• `get` **typeName**(): `string`

#### Returns

`string`

#### Inherited from

Overlay.typeName

___

### visible

• `get` **visible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

Overlay.visible

• `set` **visible**(`val`): `void`

设置显示状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

Overlay.visible

___

### zIndex

• `get` **zIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

Overlay.zIndex

• `set` **zIndex**(`val`): `void`

设置覆盖物显示层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

Overlay.zIndex

## Methods

### setModelPath

▸ **setModelPath**(`modelPath`): `Promise`\<`void`\>

设置模型文件路径（必填）

#### Parameters

| Name | Type |
| :------ | :------ |
| `modelPath` | `string` |

#### Returns

`Promise`\<`void`\>

**`Throws`**

路径为空时抛异常

___

### setModelName

▸ **setModelName**(`modelName`): `void`

设置模型文件名（必填）

#### Parameters

| Name | Type |
| :------ | :------ |
| `modelName` | `string` |

#### Returns

`void`

**`Throws`**

名称为空时抛异常

___

### setPosition

▸ **setPosition**(`position`): `void`

设置模型经纬度（必填）

#### Parameters

| Name | Type |
| :------ | :------ |
| `position` | [`LatLng`](base.LatLng.md) |

#### Returns

`void`

**`Throws`**

坐标为空时抛异常

___

### setScale

▸ **setScale**(`scale`): `void`

设置缩放比例（默认1.0）

#### Parameters

| Name | Type |
| :------ | :------ |
| `scale` | `number` |

#### Returns

`void`

___

### setZoomFixed

▸ **setZoomFixed**(`zoomFixed`): `void`

设置是否固定缩放（不随地图缩放变化）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `zoomFixed` | `boolean` | true=固定缩放；false=随地图缩放（默认） |

#### Returns

`void`

___

### setRotate

▸ **setRotate**(`rotateX`, `rotateY`, `rotateZ`): `void`

设置旋转角度（X/Y/Z轴，取值范围0~360°）

#### Parameters

| Name | Type |
| :------ | :------ |
| `rotateX` | `number` |
| `rotateY` | `number` |
| `rotateZ` | `number` |

#### Returns

`void`

___

### setOffset

▸ **setOffset**(`offsetX`, `offsetY`, `offsetZ`): `void`

设置偏移量（X/Y/Z轴，像素单位）

#### Parameters

| Name | Type |
| :------ | :------ |
| `offsetX` | `number` |
| `offsetY` | `number` |
| `offsetZ` | `number` |

#### Returns

`void`

___

### setBM3DModelType

▸ **setBM3DModelType**(`bm3DModelType`): `void`

设置模型类型（默认.obj）

#### Parameters

| Name | Type |
| :------ | :------ |
| `bm3DModelType` | [`BM3DModelType`](../enums/map.SysEnum.BM3DModelType.md) |

#### Returns

`void`

___

### setSkeletonAnimationEnable

▸ **setSkeletonAnimationEnable**(`isAnimation`): `void`

启用/禁用骨骼动画（仅GLTF模型支持）

#### Parameters

| Name | Type |
| :------ | :------ |
| `isAnimation` | `boolean` |

#### Returns

`void`

___

### setAnimationRepeatCount

▸ **setAnimationRepeatCount**(`animationRepeatCount`): `void`

设置动画重复次数（0=无限循环）

#### Parameters

| Name | Type |
| :------ | :------ |
| `animationRepeatCount` | `number` |

#### Returns

`void`

___

### setAnimationSpeed

▸ **setAnimationSpeed**(`animationSpeed`): `void`

设置动画播放速度（1.0=正常速度）

#### Parameters

| Name | Type |
| :------ | :------ |
| `animationSpeed` | `number` |

#### Returns

`void`

___

### setAnimationIndex

▸ **setAnimationIndex**(`animationIndex`): `void`

设置动画索引（指定播放哪个动画）

#### Parameters

| Name | Type |
| :------ | :------ |
| `animationIndex` | `number` |

#### Returns

`void`

___

### getModelPath

▸ **getModelPath**(): `undefined` \| `string`

#### Returns

`undefined` \| `string`

___

### getModelName

▸ **getModelName**(): `undefined` \| `string`

#### Returns

`undefined` \| `string`

___

### getPosition

▸ **getPosition**(): `undefined` \| [`LatLng`](base.LatLng.md)

#### Returns

`undefined` \| [`LatLng`](base.LatLng.md)

___

### getScale

▸ **getScale**(): `number`

#### Returns

`number`

___

### isZoomFixed

▸ **isZoomFixed**(): `boolean`

#### Returns

`boolean`

___

### getRotateX

▸ **getRotateX**(): `number`

#### Returns

`number`

___

### getRotateY

▸ **getRotateY**(): `number`

#### Returns

`number`

___

### getRotateZ

▸ **getRotateZ**(): `number`

#### Returns

`number`

___

### getOffsetX

▸ **getOffsetX**(): `number`

#### Returns

`number`

___

### getOffsetY

▸ **getOffsetY**(): `number`

#### Returns

`number`

___

### getOffsetZ

▸ **getOffsetZ**(): `number`

#### Returns

`number`

___

### getBM3DModelType

▸ **getBM3DModelType**(): [`BM3DModelType`](../enums/map.SysEnum.BM3DModelType.md)

#### Returns

[`BM3DModelType`](../enums/map.SysEnum.BM3DModelType.md)

___

### isSkeletonAnimationEnable

▸ **isSkeletonAnimationEnable**(): `boolean`

#### Returns

`boolean`

___

### getAnimationRepeatCount

▸ **getAnimationRepeatCount**(): `number`

#### Returns

`number`

___

### getAnimationSpeed

▸ **getAnimationSpeed**(): `number`

#### Returns

`number`

___

### getAnimationIndex

▸ **getAnimationIndex**(): `number`

#### Returns

`number`

___

### startAnimation

▸ **startAnimation**(): `void`

启动轨迹动画

#### Returns

`void`

___

### pauseAnimation

▸ **pauseAnimation**(): `void`

暂停轨迹动画

#### Returns

`void`

___

### resumeAnimation

▸ **resumeAnimation**(): `void`

恢复轨迹动画

#### Returns

`void`

___

### cancelAnimation

▸ **cancelAnimation**(): `void`

取消轨迹动画

#### Returns

`void`

___

### getDrawItem

▸ **getDrawItem**(): `undefined` \| `default`

获取底层绘制项

#### Returns

`undefined` \| `default`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

#### Overrides

[Overlay](map.Overlay.md).[toString](map.Overlay.md#tostring)

___

### putPointsInfoIntoBundle

▸ **putPointsInfoIntoBundle**(`points`, `b`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] |
| `b` | `undefined` |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[putPointsInfoIntoBundle](map.Overlay.md#putpointsinfointobundle)

___

### addEventListener

▸ **addEventListener**(`model`, `fun`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.0.1

**`History`**

包1.0.0 版本中 model:string , 取值范围 'CLICK'、'TOUCH'

#### Inherited from

[Overlay](map.Overlay.md).[addEventListener](map.Overlay.md#addeventlistener)

___

### removeEventListener

▸ **removeEventListener**(`model`, `fun`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.0.1

**`History`**

包1.0.0 版本中 model:string , 取值范围 'CLICK'、'TOUCH'

#### Inherited from

[Overlay](map.Overlay.md).[removeEventListener](map.Overlay.md#removeeventlistener)

___

### addDragListener

▸ **addDragListener**(`listener`): `void`

添加拖拽监听器，当前仅支持Marker、Label

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | [`OverlayDragListener`](../interfaces/map.OverlayDragListener.md) |

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

[Overlay](map.Overlay.md).[addDragListener](map.Overlay.md#adddraglistener)

___

### removeDragListener

▸ **removeDragListener**(): `void`

移除拖拽监听器

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

[Overlay](map.Overlay.md).[removeDragListener](map.Overlay.md#removedraglistener)

___

### getDragListener

▸ **getDragListener**(): [`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

获取拖拽监听器

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

**`Since`**

2.0.3

#### Inherited from

[Overlay](map.Overlay.md).[getDragListener](map.Overlay.md#getdraglistener)

___

### fireEvent

▸ **fireEvent**(`model`, `content`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` |
| `content` | [`EventOverlayBundle`](../interfaces/map.EventOverlayBundle.md) |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[fireEvent](map.Overlay.md#fireevent)

___

### getType

▸ **getType**(): `default`

#### Returns

`default`

#### Inherited from

[Overlay](map.Overlay.md).[getType](map.Overlay.md#gettype)

___

### setAnimation

▸ **setAnimation**(`animation`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `animation` | [`Animation`](map.Animation.md) |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[setAnimation](map.Overlay.md#setanimation)

___

### getAnimation

▸ **getAnimation**(): [`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Inherited from

[Overlay](map.Overlay.md).[getAnimation](map.Overlay.md#getanimation)

___

### setVisible

▸ **setVisible**(`val`): `void`

设置显示状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setVisible](map.Overlay.md#setvisible)

___

### getVisible

▸ **getVisible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getVisible](map.Overlay.md#getvisible)

___

### alpha

▸ **alpha**(`alpha`): [`Bd_3DModel`](map.Bd_3DModel.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Bd_3DModel`](map.Bd_3DModel.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[alpha](map.Overlay.md#alpha)

___

### getAlpha

▸ **getAlpha**(): `number`

获取透明度

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getAlpha](map.Overlay.md#getalpha)

___

### setAlpha

▸ **setAlpha**(`alpha`): `void`

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setAlpha](map.Overlay.md#setalpha)

___

### startLevel

▸ **startLevel**(`startLevel`): [`Bd_3DModel`](map.Bd_3DModel.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Bd_3DModel`](map.Bd_3DModel.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[startLevel](map.Overlay.md#startlevel)

___

### getStartLevel

▸ **getStartLevel**(): `number`

获取覆盖物开始显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getStartLevel](map.Overlay.md#getstartlevel)

___

### setStartLevel

▸ **setStartLevel**(`startLevel`): `void`

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setStartLevel](map.Overlay.md#setstartlevel)

___

### endLevel

▸ **endLevel**(`endLevel`): [`Bd_3DModel`](map.Bd_3DModel.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Bd_3DModel`](map.Bd_3DModel.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[endLevel](map.Overlay.md#endlevel)

___

### showLevel

▸ **showLevel**(`from`, `to`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `from` | `number` |
| `to` | `number` |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[showLevel](map.Overlay.md#showlevel)

___

### getEndLevel

▸ **getEndLevel**(): `number`

获取marker结束显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getEndLevel](map.Overlay.md#getendlevel)

___

### setShowLevel

▸ **setShowLevel**(`from`, `to`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `from` | `number` |
| `to` | `number` |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[setShowLevel](map.Overlay.md#setshowlevel)

___

### setEndLevel

▸ **setEndLevel**(`endLevel`): `void`

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setEndLevel](map.Overlay.md#setendlevel)

___

### clickable

▸ **clickable**(`isClickable`): [`Bd_3DModel`](map.Bd_3DModel.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Bd_3DModel`](map.Bd_3DModel.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[clickable](map.Overlay.md#clickable)

___

### getClickable

▸ **getClickable**(): `boolean`

获取是否可点击状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getClickable](map.Overlay.md#getclickable)

___

### setClickable

▸ **setClickable**(`isClickable`): `void`

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setClickable](map.Overlay.md#setclickable)

___

### setZIndex

▸ **setZIndex**(`val`): `void`

设置覆盖物显示层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setZIndex](map.Overlay.md#setzindex)

___

### getZIndex

▸ **getZIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getZIndex](map.Overlay.md#getzindex)

___

### setExtraInfo

▸ **setExtraInfo**(`extraInfo`): `void`

设置覆盖物属性数据

#### Parameters

| Name | Type |
| :------ | :------ |
| `extraInfo` | `AnyObject` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setExtraInfo](map.Overlay.md#setextrainfo)

___

### getExtraInfo

▸ **getExtraInfo**(): `AnyObject`

获取覆盖物属性数据

#### Returns

`AnyObject`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getExtraInfo](map.Overlay.md#getextrainfo)

___

### getBmDrawItem

▸ **getBmDrawItem**(): `undefined` \| `default`

#### Returns

`undefined` \| `default`

#### Inherited from

[Overlay](map.Overlay.md).[getBmDrawItem](map.Overlay.md#getbmdrawitem)

___

### update

▸ **update**(): `void`

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[update](map.Overlay.md#update)

___

### remove

▸ **remove**(`noUpdate?`): `void`

移除覆盖物

#### Parameters

| Name | Type |
| :------ | :------ |
| `noUpdate?` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[remove](map.Overlay.md#remove)

___

### isRemoved

▸ **isRemoved**(): `undefined` \| `boolean`

获取是否移除状态

#### Returns

`undefined` \| `boolean`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[isRemoved](map.Overlay.md#isremoved)

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[destroy](map.Overlay.md#destroy)
