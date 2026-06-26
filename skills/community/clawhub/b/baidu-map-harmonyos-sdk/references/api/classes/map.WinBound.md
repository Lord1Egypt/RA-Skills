[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / WinBound

# Class: WinBound

[map](../modules/map.md).WinBound

地图视口范围数据结构

**`Abstract`**

由屏幕地图位置的像素点确认

**`Since`**

1.0.1

**`Package`**

@bdmap/map

## Table of contents

### Constructors

- [constructor](map.WinBound.md#constructor)

### Accessors

- [left](map.WinBound.md#left)
- [right](map.WinBound.md#right)
- [top](map.WinBound.md#top)
- [bottom](map.WinBound.md#bottom)

### Methods

- [setWinRound](map.WinBound.md#setwinround)
- [setWinRoundLB](map.WinBound.md#setwinroundlb)
- [setWinRoundRT](map.WinBound.md#setwinroundrt)
- [getWidth](map.WinBound.md#getwidth)
- [getInnerWidth](map.WinBound.md#getinnerwidth)
- [getHeight](map.WinBound.md#getheight)
- [getInnerHeight](map.WinBound.md#getinnerheight)
- [getRightSpan](map.WinBound.md#getrightspan)
- [getBottomSpan](map.WinBound.md#getbottomspan)
- [destroy](map.WinBound.md#destroy)
- [toString](map.WinBound.md#tostring)

## Constructors

### constructor

• **new WinBound**(`left?`, `right?`, `top?`, `bottom?`, `width?`, `height?`): [`WinBound`](map.WinBound.md)

设置地图操作区距控件的距离

#### Parameters

| Name | Type |
| :------ | :------ |
| `left?` | `number` |
| `right?` | `number` |
| `top?` | `number` |
| `bottom?` | `number` |
| `width?` | `number` |
| `height?` | `number` |

#### Returns

[`WinBound`](map.WinBound.md)

**`Since`**

1.0.1

## Accessors

### left

• `get` **left**(): `number`

#### Returns

`number`

• `set` **left**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

___

### right

• `get` **right**(): `number`

#### Returns

`number`

• `set` **right**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

___

### top

• `get` **top**(): `number`

#### Returns

`number`

• `set` **top**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

___

### bottom

• `get` **bottom**(): `number`

#### Returns

`number`

• `set` **bottom**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

## Methods

### setWinRound

▸ **setWinRound**(`left`, `right`, `top`, `bottom`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `right` | `number` |
| `top` | `number` |
| `bottom` | `number` |

#### Returns

`void`

___

### setWinRoundLB

▸ **setWinRoundLB**(`left`, `bottom`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `left` | `number` |
| `bottom` | `number` |

#### Returns

`void`

___

### setWinRoundRT

▸ **setWinRoundRT**(`right`, `top`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `right` | `number` |
| `top` | `number` |

#### Returns

`void`

___

### getWidth

▸ **getWidth**(): `number`

#### Returns

`number`

___

### getInnerWidth

▸ **getInnerWidth**(): `number`

#### Returns

`number`

___

### getHeight

▸ **getHeight**(): `number`

#### Returns

`number`

___

### getInnerHeight

▸ **getInnerHeight**(): `number`

#### Returns

`number`

___

### getRightSpan

▸ **getRightSpan**(): `number`

#### Returns

`number`

___

### getBottomSpan

▸ **getBottomSpan**(): `number`

#### Returns

`number`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`
