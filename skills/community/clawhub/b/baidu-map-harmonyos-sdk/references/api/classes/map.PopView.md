[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / PopView

# Class: PopView

[map](../modules/map.md).PopView

消息框

**`Since`**

1.1.0

## Hierarchy

- [`BmObject`](map.BmObject.md)

  ↳ **`PopView`**

## Table of contents

### Constructors

- [constructor](map.PopView.md#constructor)

### Properties

- [isDestroyed](map.PopView.md#isdestroyed)

### Methods

- [addEventListener](map.PopView.md#addeventlistener)
- [removeEventListener](map.PopView.md#removeeventlistener)
- [fireEvent](map.PopView.md#fireevent)
- [setView](map.PopView.md#setview)
- [getView](map.PopView.md#getview)
- [setLocated](map.PopView.md#setlocated)
- [setOffsetX](map.PopView.md#setoffsetx)
- [setOffsetY](map.PopView.md#setoffsety)
- [setVisibility](map.PopView.md#setvisibility)
- [setShowLevel](map.PopView.md#setshowlevel)
- [setCollisionBehavior](map.PopView.md#setcollisionbehavior)
- [setCollisionPriority](map.PopView.md#setcollisionpriority)
- [setScale](map.PopView.md#setscale)
- [setScaleX](map.PopView.md#setscalex)
- [setScaleY](map.PopView.md#setscaley)
- [setOpacity](map.PopView.md#setopacity)
- [setDescription](map.PopView.md#setdescription)
- [getDescription](map.PopView.md#getdescription)
- [setTag](map.PopView.md#settag)
- [getTag](map.PopView.md#gettag)
- [setName](map.PopView.md#setname)
- [getName](map.PopView.md#getname)
- [destroy](map.PopView.md#destroy)

## Constructors

### constructor

• **new PopView**(): [`PopView`](map.PopView.md)

#### Returns

[`PopView`](map.PopView.md)

#### Overrides

[BmObject](map.BmObject.md).[constructor](map.BmObject.md#constructor)

## Properties

### isDestroyed

• **isDestroyed**: `boolean` = `false`

是否已经被销毁

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[isDestroyed](map.BmObject.md#isdestroyed)

## Methods

### addEventListener

▸ **addEventListener**(`model`, `fun`): `void`

添加监听事件

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `CommonEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.1.0

___

### removeEventListener

▸ **removeEventListener**(`model`, `fun`): `void`

移除监听事件

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `CommonEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.1.0

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

___

### setView

▸ **setView**(`view`): `void`

设置视图内容

#### Parameters

| Name | Type |
| :------ | :------ |
| `view` | [`BaseUI`](map.BaseUI.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### getView

▸ **getView**(): [`Maybe`](../modules/map.md#maybe)\<[`BaseUI`](map.BaseUI.md)\>

设置视图内容

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`BaseUI`](map.BaseUI.md)\>

**`Since`**

1.1.0

___

### setLocated

▸ **setLocated**(`located`): `void`

设置显示位置，描述相对于Marker的位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `located` | [`Located`](../enums/map.SysEnum.Located.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setOffsetX

▸ **setOffsetX**(`offsetX`, `scaleMode?`): `void`

设置X轴偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `offsetX` | `number` |
| `scaleMode?` | [`ScaleMode`](map.SysEnum.ScaleMode.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setOffsetY

▸ **setOffsetY**(`offsetY`, `scaleMode?`): `void`

设置Y轴偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `offsetY` | `number` |
| `scaleMode?` | [`ScaleMode`](map.SysEnum.ScaleMode.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setVisibility

▸ **setVisibility**(`visibility`): `void`

设置是否显示

#### Parameters

| Name | Type |
| :------ | :------ |
| `visibility` | [`Visibility`](../enums/map.SysEnum.Visibility.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setShowLevel

▸ **setShowLevel**(`from`, `to`): `void`

设置当前视图地图层级显示范围

#### Parameters

| Name | Type |
| :------ | :------ |
| `from` | `number` |
| `to` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setCollisionBehavior

▸ **setCollisionBehavior**(`behavior`): `void`

设置碰撞行为

#### Parameters

| Name | Type |
| :------ | :------ |
| `behavior` | [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setCollisionPriority

▸ **setCollisionPriority**(`priority`): `void`

设置当前视图的碰撞优先级
仅当「CollisionBehavior == HIDE_BY_PRIORITY」时生效

#### Parameters

| Name | Type |
| :------ | :------ |
| `priority` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setScale

▸ **setScale**(`scale`): `void`

设置XY方向相同的缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scale` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setScaleX

▸ **setScaleX**(`scaleX`): `void`

设置X方向缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scaleX` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setScaleY

▸ **setScaleY**(`scaleY`): `void`

设置Y方向缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scaleY` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setOpacity

▸ **setOpacity**(`opacity`): `void`

设置透明度

#### Parameters

| Name | Type |
| :------ | :------ |
| `opacity` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setDescription

▸ **setDescription**(`description`): `void`

设置描述约定

#### Parameters

| Name | Type |
| :------ | :------ |
| `description` | `string` |

#### Returns

`void`

**`Since`**

1.1.0

___

### getDescription

▸ **getDescription**(): `string`

获取描述约定

#### Returns

`string`

**`Since`**

1.1.0

___

### setTag

▸ **setTag**(`tag`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag` | `string` |

#### Returns

`void`

#### Inherited from

[BmObject](map.BmObject.md).[setTag](map.BmObject.md#settag)

___

### getTag

▸ **getTag**(): `string`

#### Returns

`string`

#### Inherited from

[BmObject](map.BmObject.md).[getTag](map.BmObject.md#gettag)

___

### setName

▸ **setName**(`name`): `void`

设置名称

#### Parameters

| Name | Type |
| :------ | :------ |
| `name` | `string` |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[setName](map.BmObject.md#setname)

___

### getName

▸ **getName**(): `string`

获取名称

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[getName](map.BmObject.md#getname)

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[destroy](map.BmObject.md#destroy)
