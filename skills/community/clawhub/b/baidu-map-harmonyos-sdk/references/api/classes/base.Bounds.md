[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / Bounds

# Class: Bounds

[base](../modules/base.md).Bounds

## Table of contents

### Constructors

- [constructor](base.Bounds.md#constructor)

### Accessors

- [minX](base.Bounds.md#minx)
- [minY](base.Bounds.md#miny)
- [maxX](base.Bounds.md#maxx)
- [maxY](base.Bounds.md#maxy)
- [midX](base.Bounds.md#midx)
- [midY](base.Bounds.md#midy)

### Methods

- [isEmpty](base.Bounds.md#isempty)
- [equals](base.Bounds.md#equals)
- [containsBounds](base.Bounds.md#containsbounds)
- [getCenter](base.Bounds.md#getcenter)
- [intersects](base.Bounds.md#intersects)
- [containsPoint](base.Bounds.md#containspoint)
- [extend](base.Bounds.md#extend)
- [getSouthWest](base.Bounds.md#getsouthwest)
- [getNorthEast](base.Bounds.md#getnortheast)
- [setSouthWest](base.Bounds.md#setsouthwest)
- [setNorthEast](base.Bounds.md#setnortheast)
- [clone](base.Bounds.md#clone)
- [toString](base.Bounds.md#tostring)

## Constructors

### constructor

• **new Bounds**(`sw?`, `ne?`): [`Bounds`](base.Bounds.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `sw?` | [`LatLng`](base.LatLng.md) |
| `ne?` | [`LatLng`](base.LatLng.md) |

#### Returns

[`Bounds`](base.Bounds.md)

## Accessors

### minX

• `get` **minX**(): `number`

获取minX

#### Returns

`number`

___

### minY

• `get` **minY**(): `number`

获取minY

#### Returns

`number`

___

### maxX

• `get` **maxX**(): `number`

获取maxX

#### Returns

`number`

___

### maxY

• `get` **maxY**(): `number`

获取maxY

#### Returns

`number`

___

### midX

• `get` **midX**(): `number`

#### Returns

`number`

___

### midY

• `get` **midY**(): `number`

#### Returns

`number`

## Methods

### isEmpty

▸ **isEmpty**(): `boolean`

矩形区域是否为空

#### Returns

`boolean`

是否为空

___

### equals

▸ **equals**(`other`): `boolean`

当且仅当此矩形中的两点参数都等于其他矩形的两点参数时，返回`true`

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `other` | [`Bounds`](base.Bounds.md) | 对比的矩形区域 |

#### Returns

`boolean`

___

### containsBounds

▸ **containsBounds**(`bounds`): `boolean`

返回该区域是否包含指定的区域

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bounds` | [`Bounds`](base.Bounds.md) | 用于测试的区域 |

#### Returns

`boolean`

是否包含测试的区域

___

### getCenter

▸ **getCenter**(): ``null`` \| [`LatLng`](base.LatLng.md)

返回该区域的中心点地理坐标

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

地理点坐标对象.

___

### intersects

▸ **intersects**(`bounds`): ``null`` \| [`Bounds`](base.Bounds.md)

返回一个新的矩形对象，表示该项矩形区域与指定矩形区域的交集，不相交返回`null`

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bounds` | [`Bounds`](base.Bounds.md) | 指定的地理矩形区域 |

#### Returns

``null`` \| [`Bounds`](base.Bounds.md)

相交的地理矩形区域，返回`null`则表示不相交

___

### containsPoint

▸ **containsPoint**(`point?`): `undefined` \| `boolean`

返回该区域是否包含指定的点(Point)

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point?` | [`LatLng`](base.LatLng.md) | 点对象 |

#### Returns

`undefined` \| `boolean`

布尔值,包含:true,不包含:false;.

___

### extend

▸ **extend**(`point?`): `void`

根据地理坐标扩展 bounds 区域，以便将该点包含在区域内

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point?` | [`LatLng`](base.LatLng.md) | 坐标对象 |

#### Returns

`void`

___

### getSouthWest

▸ **getSouthWest**(): [`LatLng`](base.LatLng.md)

获取西南角坐标

#### Returns

[`LatLng`](base.LatLng.md)

西南角坐标

___

### getNorthEast

▸ **getNorthEast**(): [`LatLng`](base.LatLng.md)

获取东北角坐标

#### Returns

[`LatLng`](base.LatLng.md)

东北角坐标

___

### setSouthWest

▸ **setSouthWest**(`sw?`): `void`

设置西南角坐标

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `sw?` | [`LatLng`](base.LatLng.md) | 西南角坐标 |

#### Returns

`void`

___

### setNorthEast

▸ **setNorthEast**(`ne?`): `void`

设置东北角坐标

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `ne?` | [`LatLng`](base.LatLng.md) | 东北角坐标 |

#### Returns

`void`

___

### clone

▸ **clone**(): [`Bounds`](base.Bounds.md)

复制一个矩形区域对象

#### Returns

[`Bounds`](base.Bounds.md)

复制的对象

___

### toString

▸ **toString**(): `string`

返回类型描述信息

#### Returns

`string`

类型信息
