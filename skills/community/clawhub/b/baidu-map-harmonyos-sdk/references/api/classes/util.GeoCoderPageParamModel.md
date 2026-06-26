[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / GeoCoderPageParamModel

# Class: GeoCoderPageParamModel

[util](../modules/util.md).GeoCoderPageParamModel

## Hierarchy

- `GeneralParamModel`

  ↳ **`GeoCoderPageParamModel`**

## Implements

- [`GeoCoderPageParam`](../interfaces/util.GeoCoderPageParam.md)

## Table of contents

### Constructors

- [constructor](util.GeoCoderPageParamModel.md#constructor)

### Properties

- [needLocation](util.GeoCoderPageParamModel.md#needlocation)
- [isReducedAccuracyEnough](util.GeoCoderPageParamModel.md#isreducedaccuracyenough)
- [popRoot](util.GeoCoderPageParamModel.md#poproot)
- [address](util.GeoCoderPageParamModel.md#address)
- [location](util.GeoCoderPageParamModel.md#location)
- [name](util.GeoCoderPageParamModel.md#name)
- [coord\_type](util.GeoCoderPageParamModel.md#coord_type)
- [zoom](util.GeoCoderPageParamModel.md#zoom)
- [src](util.GeoCoderPageParamModel.md#src)

### Accessors

- [getNeedLocation](util.GeoCoderPageParamModel.md#getneedlocation)
- [getIsReducedAccuracyEnough](util.GeoCoderPageParamModel.md#getisreducedaccuracyenough)
- [getPopRoot](util.GeoCoderPageParamModel.md#getpoproot)
- [getAddress](util.GeoCoderPageParamModel.md#getaddress)
- [getLocation](util.GeoCoderPageParamModel.md#getlocation)
- [getName](util.GeoCoderPageParamModel.md#getname)
- [getCoord\_type](util.GeoCoderPageParamModel.md#getcoord_type)
- [getZoom](util.GeoCoderPageParamModel.md#getzoom)
- [getSrc](util.GeoCoderPageParamModel.md#getsrc)

### Methods

- [setAddress](util.GeoCoderPageParamModel.md#setaddress)
- [setLocation](util.GeoCoderPageParamModel.md#setlocation)
- [setName](util.GeoCoderPageParamModel.md#setname)
- [setCoord\_type](util.GeoCoderPageParamModel.md#setcoord_type)
- [setZoom](util.GeoCoderPageParamModel.md#setzoom)
- [setSrc](util.GeoCoderPageParamModel.md#setsrc)
- [setNeedLocation](util.GeoCoderPageParamModel.md#setneedlocation)
- [setIsReducedAccuracyEnough](util.GeoCoderPageParamModel.md#setisreducedaccuracyenough)
- [setPopRoot](util.GeoCoderPageParamModel.md#setpoproot)

## Constructors

### constructor

• **new GeoCoderPageParamModel**(`model?`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `model?` | [`GeoCoderPageParam`](../interfaces/util.GeoCoderPageParam.md) |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Overrides

GeneralParamModel.constructor

## Properties

### needLocation

• **needLocation**: `string`

#### Inherited from

GeneralParamModel.needLocation

___

### isReducedAccuracyEnough

• **isReducedAccuracyEnough**: `string`

#### Inherited from

GeneralParamModel.isReducedAccuracyEnough

___

### popRoot

• **popRoot**: `string`

#### Inherited from

GeneralParamModel.popRoot

___

### address

• **address**: `string`

#### Implementation of

[GeoCoderPageParam](../interfaces/util.GeoCoderPageParam.md).[address](../interfaces/util.GeoCoderPageParam.md#address)

___

### location

• **location**: `string`

#### Implementation of

[GeoCoderPageParam](../interfaces/util.GeoCoderPageParam.md).[location](../interfaces/util.GeoCoderPageParam.md#location)

___

### name

• **name**: `string`

#### Implementation of

[GeoCoderPageParam](../interfaces/util.GeoCoderPageParam.md).[name](../interfaces/util.GeoCoderPageParam.md#name)

___

### coord\_type

• **coord\_type**: [`CoordType`](../enums/base.CoordType.md)

#### Implementation of

[GeoCoderPageParam](../interfaces/util.GeoCoderPageParam.md).[coord_type](../interfaces/util.GeoCoderPageParam.md#coord_type)

#### Overrides

GeneralParamModel.coord\_type

___

### zoom

• **zoom**: `string`

#### Implementation of

[GeoCoderPageParam](../interfaces/util.GeoCoderPageParam.md).[zoom](../interfaces/util.GeoCoderPageParam.md#zoom)

___

### src

• **src**: `string`

#### Implementation of

[GeoCoderPageParam](../interfaces/util.GeoCoderPageParam.md).[src](../interfaces/util.GeoCoderPageParam.md#src)

## Accessors

### getNeedLocation

• `get` **getNeedLocation**(): `string`

#### Returns

`string`

#### Inherited from

GeneralParamModel.getNeedLocation

___

### getIsReducedAccuracyEnough

• `get` **getIsReducedAccuracyEnough**(): `string`

#### Returns

`string`

#### Inherited from

GeneralParamModel.getIsReducedAccuracyEnough

___

### getPopRoot

• `get` **getPopRoot**(): `string`

#### Returns

`string`

#### Inherited from

GeneralParamModel.getPopRoot

___

### getAddress

• `get` **getAddress**(): `string`

#### Returns

`string`

___

### getLocation

• `get` **getLocation**(): `string`

#### Returns

`string`

___

### getName

• `get` **getName**(): `string`

#### Returns

`string`

___

### getCoord\_type

• `get` **getCoord_type**(): [`CoordType`](../enums/base.CoordType.md)

#### Returns

[`CoordType`](../enums/base.CoordType.md)

#### Overrides

GeneralParamModel.getCoord\_type

___

### getZoom

• `get` **getZoom**(): `string`

#### Returns

`string`

___

### getSrc

• `get` **getSrc**(): `string`

#### Returns

`string`

## Methods

### setAddress

▸ **setAddress**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

___

### setLocation

▸ **setLocation**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

___

### setName

▸ **setName**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

___

### setCoord\_type

▸ **setCoord_type**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`CoordType`](../enums/base.CoordType.md) |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Overrides

GeneralParamModel.setCoord\_type

___

### setZoom

▸ **setZoom**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

___

### setSrc

▸ **setSrc**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

___

### setNeedLocation

▸ **setNeedLocation**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Overrides

GeneralParamModel.setNeedLocation

___

### setIsReducedAccuracyEnough

▸ **setIsReducedAccuracyEnough**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Overrides

GeneralParamModel.setIsReducedAccuracyEnough

___

### setPopRoot

▸ **setPopRoot**(`value`): [`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`GeoCoderPageParamModel`](util.GeoCoderPageParamModel.md)

#### Overrides

GeneralParamModel.setPopRoot
