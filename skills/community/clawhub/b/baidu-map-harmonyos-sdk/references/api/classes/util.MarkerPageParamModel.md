[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / MarkerPageParamModel

# Class: MarkerPageParamModel

[util](../modules/util.md).MarkerPageParamModel

## Hierarchy

- `GeneralParamModel`

  ↳ **`MarkerPageParamModel`**

## Implements

- [`MarkerPageParam`](../interfaces/util.MarkerPageParam.md)

## Table of contents

### Constructors

- [constructor](util.MarkerPageParamModel.md#constructor)

### Properties

- [needLocation](util.MarkerPageParamModel.md#needlocation)
- [isReducedAccuracyEnough](util.MarkerPageParamModel.md#isreducedaccuracyenough)
- [popRoot](util.MarkerPageParamModel.md#poproot)
- [title](util.MarkerPageParamModel.md#title)
- [content](util.MarkerPageParamModel.md#content)
- [location](util.MarkerPageParamModel.md#location)
- [coord\_type](util.MarkerPageParamModel.md#coord_type)
- [zoom](util.MarkerPageParamModel.md#zoom)
- [src](util.MarkerPageParamModel.md#src)

### Accessors

- [getNeedLocation](util.MarkerPageParamModel.md#getneedlocation)
- [getIsReducedAccuracyEnough](util.MarkerPageParamModel.md#getisreducedaccuracyenough)
- [getPopRoot](util.MarkerPageParamModel.md#getpoproot)
- [getTitle](util.MarkerPageParamModel.md#gettitle)
- [getContent](util.MarkerPageParamModel.md#getcontent)
- [getLocation](util.MarkerPageParamModel.md#getlocation)
- [getCoord\_type](util.MarkerPageParamModel.md#getcoord_type)
- [getZoom](util.MarkerPageParamModel.md#getzoom)
- [getSrc](util.MarkerPageParamModel.md#getsrc)

### Methods

- [setTitle](util.MarkerPageParamModel.md#settitle)
- [setContent](util.MarkerPageParamModel.md#setcontent)
- [setLocation](util.MarkerPageParamModel.md#setlocation)
- [setCoord\_type](util.MarkerPageParamModel.md#setcoord_type)
- [setZoom](util.MarkerPageParamModel.md#setzoom)
- [setSrc](util.MarkerPageParamModel.md#setsrc)
- [setNeedLocation](util.MarkerPageParamModel.md#setneedlocation)
- [setIsReducedAccuracyEnough](util.MarkerPageParamModel.md#setisreducedaccuracyenough)
- [setPopRoot](util.MarkerPageParamModel.md#setpoproot)

## Constructors

### constructor

• **new MarkerPageParamModel**(`model?`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `model?` | [`MarkerPageParam`](../interfaces/util.MarkerPageParam.md) |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

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

### title

• **title**: `string`

#### Implementation of

[MarkerPageParam](../interfaces/util.MarkerPageParam.md).[title](../interfaces/util.MarkerPageParam.md#title)

___

### content

• **content**: `string`

#### Implementation of

[MarkerPageParam](../interfaces/util.MarkerPageParam.md).[content](../interfaces/util.MarkerPageParam.md#content)

___

### location

• **location**: `string`

#### Implementation of

[MarkerPageParam](../interfaces/util.MarkerPageParam.md).[location](../interfaces/util.MarkerPageParam.md#location)

___

### coord\_type

• **coord\_type**: [`CoordType`](../enums/base.CoordType.md)

#### Implementation of

[MarkerPageParam](../interfaces/util.MarkerPageParam.md).[coord_type](../interfaces/util.MarkerPageParam.md#coord_type)

#### Overrides

GeneralParamModel.coord\_type

___

### zoom

• **zoom**: `string`

#### Implementation of

[MarkerPageParam](../interfaces/util.MarkerPageParam.md).[zoom](../interfaces/util.MarkerPageParam.md#zoom)

___

### src

• **src**: `string`

#### Implementation of

[MarkerPageParam](../interfaces/util.MarkerPageParam.md).[src](../interfaces/util.MarkerPageParam.md#src)

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

### getTitle

• `get` **getTitle**(): `string`

#### Returns

`string`

___

### getContent

• `get` **getContent**(): `string`

#### Returns

`string`

___

### getLocation

• `get` **getLocation**(): `string`

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

### setTitle

▸ **setTitle**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

___

### setContent

▸ **setContent**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

___

### setLocation

▸ **setLocation**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

___

### setCoord\_type

▸ **setCoord_type**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`CoordType`](../enums/base.CoordType.md) |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Overrides

GeneralParamModel.setCoord\_type

___

### setZoom

▸ **setZoom**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

___

### setSrc

▸ **setSrc**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

___

### setNeedLocation

▸ **setNeedLocation**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Overrides

GeneralParamModel.setNeedLocation

___

### setIsReducedAccuracyEnough

▸ **setIsReducedAccuracyEnough**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Overrides

GeneralParamModel.setIsReducedAccuracyEnough

___

### setPopRoot

▸ **setPopRoot**(`value`): [`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

[`MarkerPageParamModel`](util.MarkerPageParamModel.md)

#### Overrides

GeneralParamModel.setPopRoot
