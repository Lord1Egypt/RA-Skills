[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / RoutePageParamModel

# Class: RoutePageParamModel

[util](../modules/util.md).RoutePageParamModel

## Hierarchy

- `GeneralParamModel`

  ↳ **`RoutePageParamModel`**

## Implements

- [`RoutePageParam`](../interfaces/util.RoutePageParam.md)

## Table of contents

### Constructors

- [constructor](util.RoutePageParamModel.md#constructor)

### Properties

- [coord\_type](util.RoutePageParamModel.md#coord_type)
- [needLocation](util.RoutePageParamModel.md#needlocation)
- [isReducedAccuracyEnough](util.RoutePageParamModel.md#isreducedaccuracyenough)
- [popRoot](util.RoutePageParamModel.md#poproot)
- [type](util.RoutePageParamModel.md#type)
- [param](util.RoutePageParamModel.md#param)
- [src](util.RoutePageParamModel.md#src)

### Accessors

- [getCoord\_type](util.RoutePageParamModel.md#getcoord_type)
- [getNeedLocation](util.RoutePageParamModel.md#getneedlocation)
- [getIsReducedAccuracyEnough](util.RoutePageParamModel.md#getisreducedaccuracyenough)
- [getPopRoot](util.RoutePageParamModel.md#getpoproot)
- [getType](util.RoutePageParamModel.md#gettype)
- [getParam](util.RoutePageParamModel.md#getparam)
- [getSrc](util.RoutePageParamModel.md#getsrc)

### Methods

- [setType](util.RoutePageParamModel.md#settype)
- [setParam](util.RoutePageParamModel.md#setparam)
- [setSrc](util.RoutePageParamModel.md#setsrc)
- [setCoord\_type](util.RoutePageParamModel.md#setcoord_type)
- [setNeedLocation](util.RoutePageParamModel.md#setneedlocation)
- [setIsReducedAccuracyEnough](util.RoutePageParamModel.md#setisreducedaccuracyenough)
- [setPopRoot](util.RoutePageParamModel.md#setpoproot)

## Constructors

### constructor

• **new RoutePageParamModel**(`routeModel?`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `routeModel?` | [`RoutePageParam`](../interfaces/util.RoutePageParam.md) |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

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

### type

• **type**: `string`

#### Implementation of

[RoutePageParam](../interfaces/util.RoutePageParam.md).[type](../interfaces/util.RoutePageParam.md#type)

___

### param

• **param**: `string`

#### Implementation of

[RoutePageParam](../interfaces/util.RoutePageParam.md).[param](../interfaces/util.RoutePageParam.md#param)

___

### src

• **src**: `string`

#### Implementation of

[RoutePageParam](../interfaces/util.RoutePageParam.md).[src](../interfaces/util.RoutePageParam.md#src)

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

### getType

• `get` **getType**(): `string`

#### Returns

`string`

___

### getParam

• `get` **getParam**(): `string`

#### Returns

`string`

___

### getSrc

• `get` **getSrc**(): `string`

#### Returns

`string`

## Methods

### setType

▸ **setType**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

___

### setParam

▸ **setParam**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

___

### setSrc

▸ **setSrc**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

___

### setCoord\_type

▸ **setCoord_type**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`CoordType`](../enums/base.CoordType.md) |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Overrides

GeneralParamModel.setCoord\_type

___

### setNeedLocation

▸ **setNeedLocation**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Overrides

GeneralParamModel.setNeedLocation

___

### setIsReducedAccuracyEnough

▸ **setIsReducedAccuracyEnough**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Overrides

GeneralParamModel.setIsReducedAccuracyEnough

___

### setPopRoot

▸ **setPopRoot**(`value`): [`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`RoutePageParamModel`](util.RoutePageParamModel.md)

#### Overrides

GeneralParamModel.setPopRoot
