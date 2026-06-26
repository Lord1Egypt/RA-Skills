[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LabelUI

# Class: LabelUI

[map](../modules/map.md).LabelUI

设置文本UI

**`Since`**

1.1.0

## Hierarchy

- [`BaseUI`](map.BaseUI.md)

  ↳ **`LabelUI`**

## Table of contents

### Constructors

- [constructor](map.LabelUI.md#constructor)

### Properties

- [isDestroyed](map.LabelUI.md#isdestroyed)

### Methods

- [addEventListener](map.LabelUI.md#addeventlistener)
- [removeEventListener](map.LabelUI.md#removeeventlistener)
- [fireEvent](map.LabelUI.md#fireevent)
- [setBackground](map.LabelUI.md#setbackground)
- [hasBackgroundResource](map.LabelUI.md#hasbackgroundresource)
- [setBackgroundColor](map.LabelUI.md#setbackgroundcolor)
- [hasBackgroundColor](map.LabelUI.md#hasbackgroundcolor)
- [setWidth](map.LabelUI.md#setwidth)
- [setHeight](map.LabelUI.md#setheight)
- [setGravity](map.LabelUI.md#setgravity)
- [setPadding](map.LabelUI.md#setpadding)
- [setMargin](map.LabelUI.md#setmargin)
- [setVisibility](map.LabelUI.md#setvisibility)
- [setClickable](map.LabelUI.md#setclickable)
- [setDescription](map.LabelUI.md#setdescription)
- [getDescription](map.LabelUI.md#getdescription)
- [setText](map.LabelUI.md#settext)
- [getText](map.LabelUI.md#gettext)
- [setStyle](map.LabelUI.md#setstyle)
- [getStyle](map.LabelUI.md#getstyle)
- [setMinLines](map.LabelUI.md#setminlines)
- [setMaxLines](map.LabelUI.md#setmaxlines)
- [setTag](map.LabelUI.md#settag)
- [getTag](map.LabelUI.md#gettag)
- [setName](map.LabelUI.md#setname)
- [getName](map.LabelUI.md#getname)
- [destroy](map.LabelUI.md#destroy)

## Constructors

### constructor

• **new LabelUI**(): [`LabelUI`](map.LabelUI.md)

构造函数

#### Returns

[`LabelUI`](map.LabelUI.md)

**`Since`**

1.1.0

#### Overrides

[BaseUI](map.BaseUI.md).[constructor](map.BaseUI.md#constructor)

## Properties

### isDestroyed

• **isDestroyed**: `boolean` = `false`

是否已经被销毁

**`Since`**

1.1.0

#### Inherited from

[BaseUI](map.BaseUI.md).[isDestroyed](map.BaseUI.md#isdestroyed)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[addEventListener](map.BaseUI.md#addeventlistener)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[removeEventListener](map.BaseUI.md#removeeventlistener)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[fireEvent](map.BaseUI.md#fireevent)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setBackground](map.BaseUI.md#setbackground)

___

### hasBackgroundResource

▸ **hasBackgroundResource**(): `boolean`

是否设置了背景填充纹理

#### Returns

`boolean`

**`Since`**

1.1.0

#### Inherited from

[BaseUI](map.BaseUI.md).[hasBackgroundResource](map.BaseUI.md#hasbackgroundresource)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setBackgroundColor](map.BaseUI.md#setbackgroundcolor)

___

### hasBackgroundColor

▸ **hasBackgroundColor**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[BaseUI](map.BaseUI.md).[hasBackgroundColor](map.BaseUI.md#hasbackgroundcolor)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setWidth](map.BaseUI.md#setwidth)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setHeight](map.BaseUI.md#setheight)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setGravity](map.BaseUI.md#setgravity)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setPadding](map.BaseUI.md#setpadding)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setMargin](map.BaseUI.md#setmargin)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setVisibility](map.BaseUI.md#setvisibility)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setClickable](map.BaseUI.md#setclickable)

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

#### Inherited from

[BaseUI](map.BaseUI.md).[setDescription](map.BaseUI.md#setdescription)

___

### getDescription

▸ **getDescription**(): `string`

获取描述约定

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[BaseUI](map.BaseUI.md).[getDescription](map.BaseUI.md#getdescription)

___

### setText

▸ **setText**(`text`): `void`

设置文本

#### Parameters

| Name | Type |
| :------ | :------ |
| `text` | `string` |

#### Returns

`void`

**`Since`**

1.1.0

___

### getText

▸ **getText**(): `string`

获取文本

#### Returns

`string`

**`Since`**

1.1.0

___

### setStyle

▸ **setStyle**(`style`): `void`

设置文字样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `style` | [`TextStyle`](map.TextStyle.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### getStyle

▸ **getStyle**(): [`Maybe`](../modules/map.md#maybe)\<[`TextStyle`](map.TextStyle.md)\>

获取文字样式

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`TextStyle`](map.TextStyle.md)\>

**`Since`**

1.1.0

___

### setMinLines

▸ **setMinLines**(`minLines`): `void`

设置最小行数

#### Parameters

| Name | Type |
| :------ | :------ |
| `minLines` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setMaxLines

▸ **setMaxLines**(`maxLines`): `void`

设置最大行数

#### Parameters

| Name | Type |
| :------ | :------ |
| `maxLines` | `number` |

#### Returns

`void`

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

[BaseUI](map.BaseUI.md).[setTag](map.BaseUI.md#settag)

___

### getTag

▸ **getTag**(): `string`

#### Returns

`string`

#### Inherited from

[BaseUI](map.BaseUI.md).[getTag](map.BaseUI.md#gettag)

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

[BaseUI](map.BaseUI.md).[setName](map.BaseUI.md#setname)

___

### getName

▸ **getName**(): `string`

获取名称

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[BaseUI](map.BaseUI.md).[getName](map.BaseUI.md#getname)

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[BaseUI](map.BaseUI.md).[destroy](map.BaseUI.md#destroy)
