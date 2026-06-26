[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Building

# Class: Building

[map](../modules/map.md).Building

覆盖物基类

**`Abstract`**

提供覆盖物基础的操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Prism`](map.Prism.md)

  ↳ **`Building`**

## Table of contents

### Constructors

- [constructor](map.Building.md#constructor)

### Properties

- [uuid](map.Building.md#uuid)
- [type](map.Building.md#type)
- [eventListener](map.Building.md#eventlistener)
- [isDestroyed](map.Building.md#isdestroyed)

### Accessors

- [typeName](map.Building.md#typename)
- [visible](map.Building.md#visible)
- [zIndex](map.Building.md#zindex)

### Methods

- [toDrawItem](map.Building.md#todrawitem)
- [getFloorHeight](map.Building.md#getfloorheight)
- [floorHeight](map.Building.md#floorheight)
- [setFloorHeight](map.Building.md#setfloorheight)
- [getHasFloor](map.Building.md#gethasfloor)
- [hasFloor](map.Building.md#hasfloor)
- [setHasFloor](map.Building.md#sethasfloor)
- [getFloorColor](map.Building.md#getfloorcolor)
- [floorColor](map.Building.md#floorcolor)
- [setFloorColor](map.Building.md#setfloorcolor)
- [getLastFloorHeight](map.Building.md#getlastfloorheight)
- [lastFloorHeight](map.Building.md#lastfloorheight)
- [getFloorSideTextureImage](map.Building.md#getfloorsidetextureimage)
- [floorSideTextureImage](map.Building.md#floorsidetextureimage)
- [setFloorSideTextureImage](map.Building.md#setfloorsidetextureimage)
- [getBuildingFloorAnimateType](map.Building.md#getbuildingflooranimatetype)
- [buildingFloorAnimateType](map.Building.md#buildingflooranimatetype)
- [setBuildingFloorAnimateType](map.Building.md#setbuildingflooranimatetype)
- [getIsAnimation](map.Building.md#getisanimation)
- [isAnimation](map.Building.md#isanimation)
- [setIsAnimation](map.Building.md#setisanimation)
- [getBuildingInfo](map.Building.md#getbuildinginfo)
- [buildingInfo](map.Building.md#buildinginfo)
- [setBuildingInfo](map.Building.md#setbuildinginfo)
- [getIsRoundedCorner](map.Building.md#getisroundedcorner)
- [isRoundedCorner](map.Building.md#isroundedcorner)
- [setIsRoundedCorner](map.Building.md#setisroundedcorner)
- [getRoundedCornerRadius](map.Building.md#getroundedcornerradius)
- [roundedCornerRadius](map.Building.md#roundedcornerradius)
- [setRoundedCornerRadius](map.Building.md#setroundedcornerradius)
- [destroy](map.Building.md#destroy)
- [putPointsInfoIntoBundle](map.Building.md#putpointsinfointobundle)
- [addEventListener](map.Building.md#addeventlistener)
- [removeEventListener](map.Building.md#removeeventlistener)
- [addDragListener](map.Building.md#adddraglistener)
- [removeDragListener](map.Building.md#removedraglistener)
- [getDragListener](map.Building.md#getdraglistener)
- [fireEvent](map.Building.md#fireevent)
- [getType](map.Building.md#gettype)
- [setAnimation](map.Building.md#setanimation)
- [getAnimation](map.Building.md#getanimation)
- [setVisible](map.Building.md#setvisible)
- [getVisible](map.Building.md#getvisible)
- [alpha](map.Building.md#alpha)
- [getAlpha](map.Building.md#getalpha)
- [setAlpha](map.Building.md#setalpha)
- [startLevel](map.Building.md#startlevel)
- [getStartLevel](map.Building.md#getstartlevel)
- [setStartLevel](map.Building.md#setstartlevel)
- [endLevel](map.Building.md#endlevel)
- [showLevel](map.Building.md#showlevel)
- [getEndLevel](map.Building.md#getendlevel)
- [setShowLevel](map.Building.md#setshowlevel)
- [setEndLevel](map.Building.md#setendlevel)
- [clickable](map.Building.md#clickable)
- [getClickable](map.Building.md#getclickable)
- [setClickable](map.Building.md#setclickable)
- [setZIndex](map.Building.md#setzindex)
- [getZIndex](map.Building.md#getzindex)
- [setExtraInfo](map.Building.md#setextrainfo)
- [getExtraInfo](map.Building.md#getextrainfo)
- [getBmDrawItem](map.Building.md#getbmdrawitem)
- [update](map.Building.md#update)
- [remove](map.Building.md#remove)
- [isRemoved](map.Building.md#isremoved)
- [toString](map.Building.md#tostring)
- [height](map.Building.md#height)
- [setHeight](map.Building.md#setheight)
- [getHeight](map.Building.md#getheight)
- [points](map.Building.md#points)
- [setPoints](map.Building.md#setpoints)
- [getPoints](map.Building.md#getpoints)
- [topFaceColor](map.Building.md#topfacecolor)
- [setTopFaceColor](map.Building.md#settopfacecolor)
- [getTopFaceColor](map.Building.md#gettopfacecolor)
- [sideFaceColor](map.Building.md#sidefacecolor)
- [setSideFaceColor](map.Building.md#setsidefacecolor)
- [getSideFaceColor](map.Building.md#getsidefacecolor)
- [customSideImage](map.Building.md#customsideimage)
- [setCustomSideImage](map.Building.md#setcustomsideimage)
- [getCustomSideImage](map.Building.md#getcustomsideimage)

## Constructors

### constructor

• **new Building**(`opt`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `opt` | `IBuildingOption` |

#### Returns

[`Building`](map.Building.md)

#### Overrides

[Prism](map.Prism.md).[constructor](map.Prism.md#constructor)

## Properties

### uuid

• **uuid**: `string`

#### Inherited from

[Prism](map.Prism.md).[uuid](map.Prism.md#uuid)

___

### type

• **type**: `default`

#### Inherited from

[Prism](map.Prism.md).[type](map.Prism.md#type)

___

### eventListener

• **eventListener**: `TOverlayListener` = `{}`

#### Inherited from

[Prism](map.Prism.md).[eventListener](map.Prism.md#eventlistener)

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

#### Inherited from

[Prism](map.Prism.md).[isDestroyed](map.Prism.md#isdestroyed)

## Accessors

### typeName

• `get` **typeName**(): `string`

#### Returns

`string`

#### Inherited from

Prism.typeName

___

### visible

• `get` **visible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

Prism.visible

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

Prism.visible

___

### zIndex

• `get` **zIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

Prism.zIndex

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

Prism.zIndex

## Methods

### toDrawItem

▸ **toDrawItem**(): `Promise`\<`void`\>

#### Returns

`Promise`\<`void`\>

#### Overrides

[Prism](map.Prism.md).[toDrawItem](map.Prism.md#todrawitem)

___

### getFloorHeight

▸ **getFloorHeight**(): `number`

#### Returns

`number`

___

### floorHeight

▸ **floorHeight**(`floor_height`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `floor_height` | `number` |

#### Returns

[`Building`](map.Building.md)

___

### setFloorHeight

▸ **setFloorHeight**(`floor_height`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `floor_height` | `number` |

#### Returns

`void`

___

### getHasFloor

▸ **getHasFloor**(): `boolean`

#### Returns

`boolean`

___

### hasFloor

▸ **hasFloor**(`has_floor`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `has_floor` | `boolean` |

#### Returns

[`Building`](map.Building.md)

___

### setHasFloor

▸ **setHasFloor**(`has_floor`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `has_floor` | `boolean` |

#### Returns

`void`

___

### getFloorColor

▸ **getFloorColor**(): ``null`` \| `ColorType`

#### Returns

``null`` \| `ColorType`

___

### floorColor

▸ **floorColor**(`floor_color`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `floor_color` | `ColorType` |

#### Returns

[`Building`](map.Building.md)

___

### setFloorColor

▸ **setFloorColor**(`floor_color`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `floor_color` | `ColorType` |

#### Returns

`void`

___

### getLastFloorHeight

▸ **getLastFloorHeight**(): `number`

#### Returns

`number`

___

### lastFloorHeight

▸ **lastFloorHeight**(`last_floor_height`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `last_floor_height` | `number` |

#### Returns

[`Building`](map.Building.md)

___

### getFloorSideTextureImage

▸ **getFloorSideTextureImage**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

___

### floorSideTextureImage

▸ **floorSideTextureImage**(`image`): `Promise`\<`undefined` \| [`Building`](map.Building.md)\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `image` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`Promise`\<`undefined` \| [`Building`](map.Building.md)\>

___

### setFloorSideTextureImage

▸ **setFloorSideTextureImage**(`image`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `image` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

___

### getBuildingFloorAnimateType

▸ **getBuildingFloorAnimateType**(): ``null`` \| [`FloorAnimateType`](../enums/map.FloorAnimateType.md)

#### Returns

``null`` \| [`FloorAnimateType`](../enums/map.FloorAnimateType.md)

___

### buildingFloorAnimateType

▸ **buildingFloorAnimateType**(`type`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`FloorAnimateType`](../enums/map.FloorAnimateType.md) |

#### Returns

[`Building`](map.Building.md)

___

### setBuildingFloorAnimateType

▸ **setBuildingFloorAnimateType**(`type`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`FloorAnimateType`](../enums/map.FloorAnimateType.md) |

#### Returns

`void`

___

### getIsAnimation

▸ **getIsAnimation**(): `boolean`

#### Returns

`boolean`

___

### isAnimation

▸ **isAnimation**(`is_animation`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `is_animation` | `boolean` |

#### Returns

[`Building`](map.Building.md)

___

### setIsAnimation

▸ **setIsAnimation**(`is_animation`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `is_animation` | `boolean` |

#### Returns

`void`

___

### getBuildingInfo

▸ **getBuildingInfo**(): ``null`` \| [`BuildingInfo`](../interfaces/base.BuildingInfo.md)

#### Returns

``null`` \| [`BuildingInfo`](../interfaces/base.BuildingInfo.md)

___

### buildingInfo

▸ **buildingInfo**(`info`): `Promise`\<`undefined` \| [`Building`](map.Building.md)\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `info` | [`BuildingInfo`](../interfaces/base.BuildingInfo.md) |

#### Returns

`Promise`\<`undefined` \| [`Building`](map.Building.md)\>

___

### setBuildingInfo

▸ **setBuildingInfo**(`info`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `info` | [`BuildingInfo`](../interfaces/base.BuildingInfo.md) |

#### Returns

`void`

___

### getIsRoundedCorner

▸ **getIsRoundedCorner**(): `boolean`

#### Returns

`boolean`

___

### isRoundedCorner

▸ **isRoundedCorner**(`is_rounded`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `is_rounded` | `boolean` |

#### Returns

[`Building`](map.Building.md)

___

### setIsRoundedCorner

▸ **setIsRoundedCorner**(`is_rounded`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `is_rounded` | `boolean` |

#### Returns

`void`

___

### getRoundedCornerRadius

▸ **getRoundedCornerRadius**(): `number`

#### Returns

`number`

___

### roundedCornerRadius

▸ **roundedCornerRadius**(`radius`): [`Building`](map.Building.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius` | `number` |

#### Returns

[`Building`](map.Building.md)

___

### setRoundedCornerRadius

▸ **setRoundedCornerRadius**(`radius`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius` | `number` |

#### Returns

`void`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`

**`Description`**

building 销毁

**`Time`**

2025-06-12

#### Overrides

[Prism](map.Prism.md).[destroy](map.Prism.md#destroy)

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

[Prism](map.Prism.md).[putPointsInfoIntoBundle](map.Prism.md#putpointsinfointobundle)

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

[Prism](map.Prism.md).[addEventListener](map.Prism.md#addeventlistener)

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

[Prism](map.Prism.md).[removeEventListener](map.Prism.md#removeeventlistener)

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

[Prism](map.Prism.md).[addDragListener](map.Prism.md#adddraglistener)

___

### removeDragListener

▸ **removeDragListener**(): `void`

移除拖拽监听器

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

[Prism](map.Prism.md).[removeDragListener](map.Prism.md#removedraglistener)

___

### getDragListener

▸ **getDragListener**(): [`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

获取拖拽监听器

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

**`Since`**

2.0.3

#### Inherited from

[Prism](map.Prism.md).[getDragListener](map.Prism.md#getdraglistener)

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

[Prism](map.Prism.md).[fireEvent](map.Prism.md#fireevent)

___

### getType

▸ **getType**(): `default`

#### Returns

`default`

#### Inherited from

[Prism](map.Prism.md).[getType](map.Prism.md#gettype)

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

[Prism](map.Prism.md).[setAnimation](map.Prism.md#setanimation)

___

### getAnimation

▸ **getAnimation**(): [`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Inherited from

[Prism](map.Prism.md).[getAnimation](map.Prism.md#getanimation)

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

[Prism](map.Prism.md).[setVisible](map.Prism.md#setvisible)

___

### getVisible

▸ **getVisible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getVisible](map.Prism.md#getvisible)

___

### alpha

▸ **alpha**(`alpha`): [`Building`](map.Building.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Building`](map.Building.md)

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[alpha](map.Prism.md#alpha)

___

### getAlpha

▸ **getAlpha**(): `number`

获取透明度

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getAlpha](map.Prism.md#getalpha)

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

[Prism](map.Prism.md).[setAlpha](map.Prism.md#setalpha)

___

### startLevel

▸ **startLevel**(`startLevel`): [`Building`](map.Building.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Building`](map.Building.md)

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[startLevel](map.Prism.md#startlevel)

___

### getStartLevel

▸ **getStartLevel**(): `number`

获取覆盖物开始显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getStartLevel](map.Prism.md#getstartlevel)

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

[Prism](map.Prism.md).[setStartLevel](map.Prism.md#setstartlevel)

___

### endLevel

▸ **endLevel**(`endLevel`): [`Building`](map.Building.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Building`](map.Building.md)

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[endLevel](map.Prism.md#endlevel)

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

[Prism](map.Prism.md).[showLevel](map.Prism.md#showlevel)

___

### getEndLevel

▸ **getEndLevel**(): `number`

获取marker结束显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getEndLevel](map.Prism.md#getendlevel)

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

[Prism](map.Prism.md).[setShowLevel](map.Prism.md#setshowlevel)

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

[Prism](map.Prism.md).[setEndLevel](map.Prism.md#setendlevel)

___

### clickable

▸ **clickable**(`isClickable`): [`Building`](map.Building.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Building`](map.Building.md)

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[clickable](map.Prism.md#clickable)

___

### getClickable

▸ **getClickable**(): `boolean`

获取是否可点击状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getClickable](map.Prism.md#getclickable)

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

[Prism](map.Prism.md).[setClickable](map.Prism.md#setclickable)

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

[Prism](map.Prism.md).[setZIndex](map.Prism.md#setzindex)

___

### getZIndex

▸ **getZIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getZIndex](map.Prism.md#getzindex)

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

[Prism](map.Prism.md).[setExtraInfo](map.Prism.md#setextrainfo)

___

### getExtraInfo

▸ **getExtraInfo**(): `AnyObject`

获取覆盖物属性数据

#### Returns

`AnyObject`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[getExtraInfo](map.Prism.md#getextrainfo)

___

### getBmDrawItem

▸ **getBmDrawItem**(): `undefined` \| `default`

#### Returns

`undefined` \| `default`

#### Inherited from

[Prism](map.Prism.md).[getBmDrawItem](map.Prism.md#getbmdrawitem)

___

### update

▸ **update**(): `void`

#### Returns

`void`

#### Inherited from

[Prism](map.Prism.md).[update](map.Prism.md#update)

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

[Prism](map.Prism.md).[remove](map.Prism.md#remove)

___

### isRemoved

▸ **isRemoved**(): `undefined` \| `boolean`

获取是否移除状态

#### Returns

`undefined` \| `boolean`

**`Since`**

1.0.0

#### Inherited from

[Prism](map.Prism.md).[isRemoved](map.Prism.md#isremoved)

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

#### Inherited from

[Prism](map.Prism.md).[toString](map.Prism.md#tostring)

___

### height

▸ **height**(`height`): [`Building`](map.Building.md)

设置3D棱柱高度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `height` | `number` | 高度 |

#### Returns

[`Building`](map.Building.md)

#### Inherited from

[Prism](map.Prism.md).[height](map.Prism.md#height)

___

### setHeight

▸ **setHeight**(`height`): `void`

设置3D棱柱高度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `height` | `number` | 高度 |

#### Returns

`void`

#### Inherited from

[Prism](map.Prism.md).[setHeight](map.Prism.md#setheight)

___

### getHeight

▸ **getHeight**(): `number`

获取高度

#### Returns

`number`

高度

#### Inherited from

[Prism](map.Prism.md).[getHeight](map.Prism.md#getheight)

___

### points

▸ **points**(`points`): `undefined` \| [`Building`](map.Building.md)

设置3D棱柱坐标点列表

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] | 设置3D棱柱坐标点列表 |

#### Returns

`undefined` \| [`Building`](map.Building.md)

#### Inherited from

[Prism](map.Prism.md).[points](map.Prism.md#points)

___

### setPoints

▸ **setPoints**(`points`): `void`

设置3D棱柱坐标点列表

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] | 设置3D棱柱坐标点列表 |

#### Returns

`void`

#### Inherited from

[Prism](map.Prism.md).[setPoints](map.Prism.md#setpoints)

___

### getPoints

▸ **getPoints**(): ``null`` \| [`LatLng`](base.LatLng.md)[]

获取棱柱坐标点

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)[]

棱柱坐标点列表

#### Inherited from

[Prism](map.Prism.md).[getPoints](map.Prism.md#getpoints)

___

### topFaceColor

▸ **topFaceColor**(`topFaceColor`): [`Building`](map.Building.md)

设置3D棱柱顶面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `topFaceColor` | `ColorType` | 3D棱柱顶面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

[`Building`](map.Building.md)

#### Inherited from

[Prism](map.Prism.md).[topFaceColor](map.Prism.md#topfacecolor)

___

### setTopFaceColor

▸ **setTopFaceColor**(`topFaceColor`): `void`

设置3D棱柱顶面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `topFaceColor` | `ColorType` | 3D棱柱顶面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

`void`

#### Inherited from

[Prism](map.Prism.md).[setTopFaceColor](map.Prism.md#settopfacecolor)

___

### getTopFaceColor

▸ **getTopFaceColor**(): `ColorType`

获取3D棱柱顶面颜色

#### Returns

`ColorType`

3D棱柱顶面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前

#### Inherited from

[Prism](map.Prism.md).[getTopFaceColor](map.Prism.md#gettopfacecolor)

___

### sideFaceColor

▸ **sideFaceColor**(`sideFaceColor`): [`Building`](map.Building.md)

设置3D棱柱侧面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `sideFaceColor` | `ColorType` | 3D棱柱侧面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

[`Building`](map.Building.md)

#### Inherited from

[Prism](map.Prism.md).[sideFaceColor](map.Prism.md#sidefacecolor)

___

### setSideFaceColor

▸ **setSideFaceColor**(`sideFaceColor`): `void`

设置3D棱柱侧面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `sideFaceColor` | `ColorType` | 3D棱柱侧面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

`void`

#### Inherited from

[Prism](map.Prism.md).[setSideFaceColor](map.Prism.md#setsidefacecolor)

___

### getSideFaceColor

▸ **getSideFaceColor**(): `ColorType`

获取3D棱柱侧面颜色

#### Returns

`ColorType`

3D棱柱侧面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前

#### Inherited from

[Prism](map.Prism.md).[getSideFaceColor](map.Prism.md#getsidefacecolor)

___

### customSideImage

▸ **customSideImage**(`customSideImage?`): `Promise`\<`undefined` \| [`Building`](map.Building.md)\>

设置3D棱柱自定义侧面纹理图片

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `customSideImage?` | [`ImageEntity`](map.ImageEntity.md) | 纹理图片需要256 * 256 |

#### Returns

`Promise`\<`undefined` \| [`Building`](map.Building.md)\>

#### Inherited from

[Prism](map.Prism.md).[customSideImage](map.Prism.md#customsideimage)

___

### setCustomSideImage

▸ **setCustomSideImage**(`customSideImage`): `void`

设置3D棱柱自定义侧面纹理图片

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `customSideImage` | [`ImageEntity`](map.ImageEntity.md) | 纹理图片需要256 * 256 |

#### Returns

`void`

#### Inherited from

[Prism](map.Prism.md).[setCustomSideImage](map.Prism.md#setcustomsideimage)

___

### getCustomSideImage

▸ **getCustomSideImage**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

获取自定义侧面纹理图片

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

纹理图片

#### Inherited from

[Prism](map.Prism.md).[getCustomSideImage](map.Prism.md#getcustomsideimage)
