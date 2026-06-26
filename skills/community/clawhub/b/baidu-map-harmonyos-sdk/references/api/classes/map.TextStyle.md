[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / TextStyle

# Class: TextStyle

[map](../modules/map.md).TextStyle

文本样式设置

**`Since`**

1.1.0

## Hierarchy

- [`BmObject`](map.BmObject.md)

  ↳ **`TextStyle`**

## Table of contents

### Constructors

- [constructor](map.TextStyle.md#constructor)

### Properties

- [isDestroyed](map.TextStyle.md#isdestroyed)

### Methods

- [setTextColor](map.TextStyle.md#settextcolor)
- [setTextSize](map.TextStyle.md#settextsize)
- [setBorderColor](map.TextStyle.md#setbordercolor)
- [setBorderWidth](map.TextStyle.md#setborderwidth)
- [setFontOption](map.TextStyle.md#setfontoption)
- [getIdentifier](map.TextStyle.md#getidentifier)
- [clone](map.TextStyle.md#clone)
- [setTag](map.TextStyle.md#settag)
- [getTag](map.TextStyle.md#gettag)
- [setName](map.TextStyle.md#setname)
- [getName](map.TextStyle.md#getname)
- [destroy](map.TextStyle.md#destroy)

## Constructors

### constructor

• **new TextStyle**(): [`TextStyle`](map.TextStyle.md)

#### Returns

[`TextStyle`](map.TextStyle.md)

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

### setTextColor

▸ **setTextColor**(`argb`): `void`

设置文字颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setTextSize

▸ **setTextSize**(`size`): `void`

设置文字大小

#### Parameters

| Name | Type |
| :------ | :------ |
| `size` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setBorderColor

▸ **setBorderColor**(`argb`): `void`

设置描边颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.1.0

___

### setBorderWidth

▸ **setBorderWidth**(`width`): `void`

设置描边宽度

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### setFontOption

▸ **setFontOption**(`option`): `void`

设置字体样式类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`FontOption`](../enums/map.SysEnum.FontOption.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### getIdentifier

▸ **getIdentifier**(): `number`

获取唯一id

#### Returns

`number`

___

### clone

▸ **clone**(): [`TextStyle`](map.TextStyle.md)

克隆一份新样式

#### Returns

[`TextStyle`](map.TextStyle.md)

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
