[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / CompassLayer

# Class: CompassLayer

[map](../modules/map.md).CompassLayer

## Hierarchy

- `default`

  ↳ **`CompassLayer`**

## Table of contents

### Constructors

- [constructor](map.CompassLayer.md#constructor)

### Accessors

- [visible](map.CompassLayer.md#visible)
- [x](map.CompassLayer.md#x)
- [y](map.CompassLayer.md#y)
- [hideTime](map.CompassLayer.md#hidetime)

### Methods

- [setName](map.CompassLayer.md#setname)
- [getName](map.CompassLayer.md#getname)
- [getLayerId](map.CompassLayer.md#getlayerid)
- [setVisible](map.CompassLayer.md#setvisible)
- [clear](map.CompassLayer.md#clear)
- [update](map.CompassLayer.md#update)
- [setData](map.CompassLayer.md#setdata)
- [getData](map.CompassLayer.md#getdata)

## Constructors

### constructor

• **new CompassLayer**(`compass`, `basemap`): [`CompassLayer`](map.CompassLayer.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `compass` | `default` |
| `basemap` | `default` |

#### Returns

[`CompassLayer`](map.CompassLayer.md)

#### Overrides

BaseLayer.constructor

## Accessors

### visible

• `get` **visible**(): `boolean`

获取图层当前状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseLayer.visible

• `set` **visible**(`val`): `void`

设置图层当前状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseLayer.visible

___

### x

• `get` **x**(): [`Nullable`](../modules/map.md#nullable)\<`number`\>

获取指北针X轴像素坐标
since 1.0.0

#### Returns

[`Nullable`](../modules/map.md#nullable)\<`number`\>

• `set` **x**(`val`): `void`

设置指北针X轴像素坐标
since 1.0.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`Nullable`](../modules/map.md#nullable)\<`number`\> |

#### Returns

`void`

___

### y

• `get` **y**(): [`Nullable`](../modules/map.md#nullable)\<`number`\>

获取指北针Y轴像素坐标
since 1.0.0

#### Returns

[`Nullable`](../modules/map.md#nullable)\<`number`\>

• `set` **y**(`val`): `void`

设置指北针Y轴像素坐标
since 1.0.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`Nullable`](../modules/map.md#nullable)\<`number`\> |

#### Returns

`void`

___

### hideTime

• `get` **hideTime**(): `number`

获取隐藏动画时间
since 1.0.0

#### Returns

`number`

• `set` **hideTime**(`val`): `void`

设置隐藏动画时间
since 1.0.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

## Methods

### setName

▸ **setName**(`name`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `name` | `string` |

#### Returns

`void`

#### Inherited from

BaseLayer.setName

___

### getName

▸ **getName**(): `string`

#### Returns

`string`

#### Inherited from

BaseLayer.getName

___

### getLayerId

▸ **getLayerId**(): `number`

#### Returns

`number`

#### Inherited from

BaseLayer.getLayerId

___

### setVisible

▸ **setVisible**(`visible`): `void`

设置图层当前状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `visible` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseLayer.setVisible

___

### clear

▸ **clear**(): `void`

#### Returns

`void`

#### Inherited from

BaseLayer.clear

___

### update

▸ **update**(): `void`

主动调用绘制一次图层数据

#### Returns

`void`

#### Inherited from

BaseLayer.update

___

### setData

▸ **setData**(`strJson`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `strJson` | `string` |

#### Returns

`void`

#### Inherited from

BaseLayer.setData

___

### getData

▸ **getData**(): `string`

#### Returns

`string`

#### Inherited from

BaseLayer.getData
