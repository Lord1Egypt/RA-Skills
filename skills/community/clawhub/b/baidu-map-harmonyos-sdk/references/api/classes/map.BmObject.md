[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / BmObject

# Class: BmObject

[map](../modules/map.md).BmObject

## Hierarchy

- **`BmObject`**

  ↳ [`Animation`](map.Animation.md)

  ↳ [`TextStyle`](map.TextStyle.md)

  ↳ [`BaseUI`](map.BaseUI.md)

  ↳ [`PopView`](map.PopView.md)

## Table of contents

### Constructors

- [constructor](map.BmObject.md#constructor)

### Properties

- [isDestroyed](map.BmObject.md#isdestroyed)

### Methods

- [setTag](map.BmObject.md#settag)
- [getTag](map.BmObject.md#gettag)
- [setName](map.BmObject.md#setname)
- [getName](map.BmObject.md#getname)
- [destroy](map.BmObject.md#destroy)

## Constructors

### constructor

• **new BmObject**(`objType`, `naInstance`): [`BmObject`](map.BmObject.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `objType` | `number` |
| `naInstance` | `number` |

#### Returns

[`BmObject`](map.BmObject.md)

## Properties

### isDestroyed

• **isDestroyed**: `boolean` = `false`

是否已经被销毁

**`Since`**

1.1.0

## Methods

### setTag

▸ **setTag**(`tag`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag` | `string` |

#### Returns

`void`

___

### getTag

▸ **getTag**(): `string`

#### Returns

`string`

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

___

### getName

▸ **getName**(): `string`

获取名称

#### Returns

`string`

**`Since`**

1.1.0

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

**`Since`**

1.1.0
