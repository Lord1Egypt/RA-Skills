[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / BaseUI

# Class: BaseUI

[map](../modules/map.md).BaseUI

UI基类

**`Since`**

1.1.0

## Hierarchy

- [`BmObject`](map.BmObject.md)

  ↳ **`BaseUI`**

  ↳↳ [`LabelUI`](map.LabelUI.md)

  ↳↳ [`ImageUI`](map.ImageUI.md)

  ↳↳ [`BaseGroupUI`](map.BaseGroupUI.md)

## Table of contents

### Constructors

- [constructor](map.BaseUI.md#constructor)

### Properties

- [isDestroyed](map.BaseUI.md#isdestroyed)

### Methods

- [addEventListener](map.BaseUI.md#addeventlistener)
- [removeEventListener](map.BaseUI.md#removeeventlistener)
- [fireEvent](map.BaseUI.md#fireevent)
- [setBackground](map.BaseUI.md#setbackground)
- [hasBackgroundResource](map.BaseUI.md#hasbackgroundresource)
- [setBackgroundColor](map.BaseUI.md#setbackgroundcolor)
- [hasBackgroundColor](map.BaseUI.md#hasbackgroundcolor)
- [setWidth](map.BaseUI.md#setwidth)
- [setHeight](map.BaseUI.md#setheight)
- [setGravity](map.BaseUI.md#setgravity)
- [setPadding](map.BaseUI.md#setpadding)
- [setMargin](map.BaseUI.md#setmargin)
- [setVisibility](map.BaseUI.md#setvisibility)
- [setClickable](map.BaseUI.md#setclickable)
- [setDescription](map.BaseUI.md#setdescription)
- [getDescription](map.BaseUI.md#getdescription)
- [setTag](map.BaseUI.md#settag)
- [getTag](map.BaseUI.md#gettag)
- [setName](map.BaseUI.md#setname)
- [getName](map.BaseUI.md#getname)
- [destroy](map.BaseUI.md#destroy)

## Constructors

### constructor

• **new BaseUI**(`objType`, `instance`): [`BaseUI`](map.BaseUI.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `objType` | `number` |
| `instance` | `default` |

#### Returns

[`BaseUI`](map.BaseUI.md)

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

注册事件

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` \| `CommonEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.1.0

___

### removeEventListener

▸ **removeEventListener**(`model`, `fun`): `void`

移除事件

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` \| `CommonEvent` |
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
| `model` | `OverlayEvent` \| `CommonEvent` |
| `content` | [`EventOverlayBundle`](../interfaces/map.EventOverlayBundle.md) |

#### Returns

`void`

___

### setBackground

▸ **setBackground**(`drawableRes`, `buildNinePatch?`): `void`

设置视图控件的背景纹理

#### Parameters

| Name | Type |
| :------ | :------ |
| `drawableRes` | [`ImageEntity`](map.ImageEntity.md) |
| `buildNinePatch?` | [`INinePatch`](../interfaces/map.INinePatch.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### hasBackgroundResource

▸ **hasBackgroundResource**(): `boolean`

是否设置了背景填充纹理

#### Returns

`boolean`

**`Since`**

1.1.0

___

### setBackgroundColor

▸ **setBackgroundColor**(`argb`): `void`

设置背景填充颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.1.0

___

### hasBackgroundColor

▸ **hasBackgroundColor**(): `boolean`

#### Returns

`boolean`

___

### setWidth

▸ **setWidth**(`width`): `void`

设置控件视图宽度

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setHeight

▸ **setHeight**(`height`): `void`

设置控件视图高度

#### Parameters

| Name | Type |
| :------ | :------ |
| `height` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setGravity

▸ **setGravity**(`gravity`): `void`

设置绘制内容位于控件视图的位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `gravity` | [`Gravity`](../enums/map.SysEnum.Gravity.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setPadding

▸ **setPadding**(`left`, `top`, `right`, `bottom`): `void`

设置相对于自身的内容位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `top` | `number` |
| `right` | `number` |
| `bottom` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setMargin

▸ **setMargin**(`left`, `top`, `right`, `bottom`): `void`

设置相对于父布局的视图位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `top` | `number` |
| `right` | `number` |
| `bottom` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setVisibility

▸ **setVisibility**(`visibility`): `void`

设置是否可显示

#### Parameters

| Name | Type |
| :------ | :------ |
| `visibility` | [`Visibility`](../enums/map.SysEnum.Visibility.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setClickable

▸ **setClickable**(`clickable`): `void`

设置当前视图UI是否可被点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `clickable` | `boolean` |

#### Returns

`void`

**`Default`**

```ts
clickable = false
```

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
