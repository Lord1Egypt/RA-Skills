[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / HomePageParamModel

# Class: HomePageParamModel

[util](../modules/util.md).HomePageParamModel

## Hierarchy

- `GeneralParamModel`

  ↳ **`HomePageParamModel`**

## Implements

- [`HomePageParam`](../interfaces/util.HomePageParam.md)

## Table of contents

### Constructors

- [constructor](util.HomePageParamModel.md#constructor)

### Properties

- [coord\_type](util.HomePageParamModel.md#coord_type)
- [needLocation](util.HomePageParamModel.md#needlocation)
- [isReducedAccuracyEnough](util.HomePageParamModel.md#isreducedaccuracyenough)
- [popRoot](util.HomePageParamModel.md#poproot)
- [bounds](util.HomePageParamModel.md#bounds)
- [zoom](util.HomePageParamModel.md#zoom)
- [center](util.HomePageParamModel.md#center)
- [userlocation](util.HomePageParamModel.md#userlocation)
- [src](util.HomePageParamModel.md#src)

### Accessors

- [getCoord\_type](util.HomePageParamModel.md#getcoord_type)
- [getNeedLocation](util.HomePageParamModel.md#getneedlocation)
- [getIsReducedAccuracyEnough](util.HomePageParamModel.md#getisreducedaccuracyenough)
- [getPopRoot](util.HomePageParamModel.md#getpoproot)
- [getBounds](util.HomePageParamModel.md#getbounds)
- [getZoom](util.HomePageParamModel.md#getzoom)
- [getCenter](util.HomePageParamModel.md#getcenter)
- [getUserlocation](util.HomePageParamModel.md#getuserlocation)
- [getSrc](util.HomePageParamModel.md#getsrc)

### Methods

- [setBounds](util.HomePageParamModel.md#setbounds)
- [setZoom](util.HomePageParamModel.md#setzoom)
- [setCenter](util.HomePageParamModel.md#setcenter)
- [setUserlocation](util.HomePageParamModel.md#setuserlocation)
- [setSrc](util.HomePageParamModel.md#setsrc)
- [setCoord\_type](util.HomePageParamModel.md#setcoord_type)
- [setNeedLocation](util.HomePageParamModel.md#setneedlocation)
- [setIsReducedAccuracyEnough](util.HomePageParamModel.md#setisreducedaccuracyenough)
- [setPopRoot](util.HomePageParamModel.md#setpoproot)

## Constructors

### constructor

• **new HomePageParamModel**(`homeModel?`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `homeModel?` | [`HomePageParam`](../interfaces/util.HomePageParam.md) |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

#### Overrides

GeneralParamModel.constructor

## Properties

### coord\_type

• **coord\_type**: [`CoordType`](../enums/base.CoordType.md)

#### Inherited from

GeneralParamModel.coord\_type

___

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

### bounds

• **bounds**: `string`

#### Implementation of

[HomePageParam](../interfaces/util.HomePageParam.md).[bounds](../interfaces/util.HomePageParam.md#bounds)

___

### zoom

• **zoom**: `string`

#### Implementation of

[HomePageParam](../interfaces/util.HomePageParam.md).[zoom](../interfaces/util.HomePageParam.md#zoom)

___

### center

• **center**: `string`

#### Implementation of

[HomePageParam](../interfaces/util.HomePageParam.md).[center](../interfaces/util.HomePageParam.md#center)

___

### userlocation

• **userlocation**: `string`

#### Implementation of

[HomePageParam](../interfaces/util.HomePageParam.md).[userlocation](../interfaces/util.HomePageParam.md#userlocation)

___

### src

• **src**: `string`

#### Implementation of

[HomePageParam](../interfaces/util.HomePageParam.md).[src](../interfaces/util.HomePageParam.md#src)

## Accessors

### getCoord\_type

• `get` **getCoord_type**(): [`CoordType`](../enums/base.CoordType.md)

#### Returns

[`CoordType`](../enums/base.CoordType.md)

#### Inherited from

GeneralParamModel.getCoord\_type

___

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

### getBounds

• `get` **getBounds**(): `string`

#### Returns

`string`

___

### getZoom

• `get` **getZoom**(): `string`

#### Returns

`string`

___

### getCenter

• `get` **getCenter**(): `string`

#### Returns

`string`

___

### getUserlocation

• `get` **getUserlocation**(): `string`

#### Returns

`string`

___

### getSrc

• `get` **getSrc**(): `string`

#### Returns

`string`

## Methods

### setBounds

▸ **setBounds**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

___

### setZoom

▸ **setZoom**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

___

### setCenter

▸ **setCenter**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

___

### setUserlocation

▸ **setUserlocation**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

___

### setSrc

▸ **setSrc**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

___

### setCoord\_type

▸ **setCoord_type**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`CoordType`](../enums/base.CoordType.md) |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

#### Overrides

GeneralParamModel.setCoord\_type

___

### setNeedLocation

▸ **setNeedLocation**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

#### Overrides

GeneralParamModel.setNeedLocation

___

### setIsReducedAccuracyEnough

▸ **setIsReducedAccuracyEnough**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

#### Overrides

GeneralParamModel.setIsReducedAccuracyEnough

___

### setPopRoot

▸ **setPopRoot**(`value`): [`HomePageParamModel`](util.HomePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`HomePageParamModel`](util.HomePageParamModel.md)

#### Overrides

GeneralParamModel.setPopRoot
