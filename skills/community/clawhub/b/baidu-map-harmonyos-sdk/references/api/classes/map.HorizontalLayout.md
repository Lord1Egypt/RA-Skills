[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / HorizontalLayout

# Class: HorizontalLayout

[map](../modules/map.md).HorizontalLayout

水平布局

**`Since`**

1.2.0

## Hierarchy

- [`BaseGroupUI`](map.BaseGroupUI.md)

  ↳ **`HorizontalLayout`**

## Table of contents

### Constructors

- [constructor](map.HorizontalLayout.md#constructor)

### Properties

- [WRAP\_CONTENT](map.HorizontalLayout.md#wrap_content)
- [isDestroyed](map.HorizontalLayout.md#isdestroyed)

### Methods

- [addView](map.HorizontalLayout.md#addview)
- [removeAllViews](map.HorizontalLayout.md#removeallviews)
- [addEventListener](map.HorizontalLayout.md#addeventlistener)
- [removeEventListener](map.HorizontalLayout.md#removeeventlistener)
- [fireEvent](map.HorizontalLayout.md#fireevent)
- [setBackground](map.HorizontalLayout.md#setbackground)
- [hasBackgroundResource](map.HorizontalLayout.md#hasbackgroundresource)
- [setBackgroundColor](map.HorizontalLayout.md#setbackgroundcolor)
- [hasBackgroundColor](map.HorizontalLayout.md#hasbackgroundcolor)
- [setWidth](map.HorizontalLayout.md#setwidth)
- [setHeight](map.HorizontalLayout.md#setheight)
- [setGravity](map.HorizontalLayout.md#setgravity)
- [setPadding](map.HorizontalLayout.md#setpadding)
- [setMargin](map.HorizontalLayout.md#setmargin)
- [setVisibility](map.HorizontalLayout.md#setvisibility)
- [setClickable](map.HorizontalLayout.md#setclickable)
- [setDescription](map.HorizontalLayout.md#setdescription)
- [getDescription](map.HorizontalLayout.md#getdescription)
- [setTag](map.HorizontalLayout.md#settag)
- [getTag](map.HorizontalLayout.md#gettag)
- [setName](map.HorizontalLayout.md#setname)
- [getName](map.HorizontalLayout.md#getname)
- [destroy](map.HorizontalLayout.md#destroy)

## Constructors

### constructor

• **new HorizontalLayout**(): [`HorizontalLayout`](map.HorizontalLayout.md)

构造函数

#### Returns

[`HorizontalLayout`](map.HorizontalLayout.md)

**`Since`**

1.2.0

#### Overrides

[BaseGroupUI](map.BaseGroupUI.md).[constructor](map.BaseGroupUI.md#constructor)

## Properties

### WRAP\_CONTENT

▪ `Static` **WRAP\_CONTENT**: `number` = `-2`

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[WRAP_CONTENT](map.BaseGroupUI.md#wrap_content)

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

是否已经被销毁

**`Since`**

1.1.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[isDestroyed](map.BaseGroupUI.md#isdestroyed)

## Methods

### addView

▸ **addView**(`child`, `index?`): `void`

添加UI

#### Parameters

| Name | Type |
| :------ | :------ |
| `child` | [`BaseUI`](map.BaseUI.md) |
| `index?` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[addView](map.BaseGroupUI.md#addview)

___

### removeAllViews

▸ **removeAllViews**(): `void`

移除所有UI

#### Returns

`void`

**`Since`**

1.2.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[removeAllViews](map.BaseGroupUI.md#removeallviews)

___

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

[BaseGroupUI](map.BaseGroupUI.md).[addEventListener](map.BaseGroupUI.md#addeventlistener)

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

[BaseGroupUI](map.BaseGroupUI.md).[removeEventListener](map.BaseGroupUI.md#removeeventlistener)

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

[BaseGroupUI](map.BaseGroupUI.md).[fireEvent](map.BaseGroupUI.md#fireevent)

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

[BaseGroupUI](map.BaseGroupUI.md).[setBackground](map.BaseGroupUI.md#setbackground)

___

### hasBackgroundResource

▸ **hasBackgroundResource**(): `boolean`

是否设置了背景填充纹理

#### Returns

`boolean`

**`Since`**

1.1.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[hasBackgroundResource](map.BaseGroupUI.md#hasbackgroundresource)

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

[BaseGroupUI](map.BaseGroupUI.md).[setBackgroundColor](map.BaseGroupUI.md#setbackgroundcolor)

___

### hasBackgroundColor

▸ **hasBackgroundColor**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[hasBackgroundColor](map.BaseGroupUI.md#hasbackgroundcolor)

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

[BaseGroupUI](map.BaseGroupUI.md).[setWidth](map.BaseGroupUI.md#setwidth)

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

[BaseGroupUI](map.BaseGroupUI.md).[setHeight](map.BaseGroupUI.md#setheight)

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

[BaseGroupUI](map.BaseGroupUI.md).[setGravity](map.BaseGroupUI.md#setgravity)

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

[BaseGroupUI](map.BaseGroupUI.md).[setPadding](map.BaseGroupUI.md#setpadding)

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

[BaseGroupUI](map.BaseGroupUI.md).[setMargin](map.BaseGroupUI.md#setmargin)

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

[BaseGroupUI](map.BaseGroupUI.md).[setVisibility](map.BaseGroupUI.md#setvisibility)

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

[BaseGroupUI](map.BaseGroupUI.md).[setClickable](map.BaseGroupUI.md#setclickable)

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

[BaseGroupUI](map.BaseGroupUI.md).[setDescription](map.BaseGroupUI.md#setdescription)

___

### getDescription

▸ **getDescription**(): `string`

获取描述约定

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[getDescription](map.BaseGroupUI.md#getdescription)

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

[BaseGroupUI](map.BaseGroupUI.md).[setTag](map.BaseGroupUI.md#settag)

___

### getTag

▸ **getTag**(): `string`

#### Returns

`string`

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[getTag](map.BaseGroupUI.md#gettag)

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

[BaseGroupUI](map.BaseGroupUI.md).[setName](map.BaseGroupUI.md#setname)

___

### getName

▸ **getName**(): `string`

获取名称

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[getName](map.BaseGroupUI.md#getname)

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[BaseGroupUI](map.BaseGroupUI.md).[destroy](map.BaseGroupUI.md#destroy)
