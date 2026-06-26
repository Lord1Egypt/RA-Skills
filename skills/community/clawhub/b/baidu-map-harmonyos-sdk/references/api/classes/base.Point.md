[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / Point

# Class: Point

[base](../modules/base.md).Point

**`Fileoverview`**

定义点坐标

**`Version`**

1.1

**`Description`**

百度墨卡托表示的地理坐标点结构,以mi为单位  如 x:12958087 y:4826077

**`Date`**

2024-3-07

## Table of contents

### Constructors

- [constructor](base.Point.md#constructor)

### Accessors

- [x](base.Point.md#x)
- [y](base.Point.md#y)
- [z](base.Point.md#z)

### Methods

- [setXY](base.Point.md#setxy)
- [setXYZ](base.Point.md#setxyz)
- [copy](base.Point.md#copy)
- [offset](base.Point.md#offset)
- [equals](base.Point.md#equals)
- [clone](base.Point.md#clone)
- [toString](base.Point.md#tostring)

## Constructors

### constructor

• **new Point**(`x`, `y`, `z?`): [`Point`](base.Point.md)

坐标点构造函数

#### Parameters

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |
| `z?` | `number` |

#### Returns

[`Point`](base.Point.md)

**`Since`**

1.0.1

## Accessors

### x

• `get` **x**(): `number`

#### Returns

`number`

• `set` **x**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

___

### y

• `get` **y**(): `number`

#### Returns

`number`

• `set` **y**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

___

### z

• `get` **z**(): `number`

#### Returns

`number`

• `set` **z**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

## Methods

### setXY

▸ **setXY**(`x`, `y`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |

#### Returns

`void`

___

### setXYZ

▸ **setXYZ**(`x`, `y`, `z`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |
| `z` | `number` |

#### Returns

`void`

___

### copy

▸ **copy**(`point`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `point` | [`Point`](base.Point.md) |

#### Returns

`void`

___

### offset

▸ **offset**(`dx`, `dy`, `dz?`): `void`

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `dx` | `number` | `undefined` |
| `dy` | `number` | `undefined` |
| `dz` | `number` | `0` |

#### Returns

`void`

___

### equals

▸ **equals**(`point`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `point` | [`Point`](base.Point.md) |

#### Returns

`boolean`

___

### clone

▸ **clone**(): [`Point`](base.Point.md)

#### Returns

[`Point`](base.Point.md)

___

### toString

▸ **toString**(): `string`

#### Returns

`string`
