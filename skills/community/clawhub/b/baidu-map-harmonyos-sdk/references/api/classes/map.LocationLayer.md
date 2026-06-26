[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LocationLayer

# Class: LocationLayer

[map](../modules/map.md).LocationLayer

## Hierarchy

- `default`

  ↳ **`LocationLayer`**

## Table of contents

### Constructors

- [constructor](map.LocationLayer.md#constructor)

### Properties

- [instance](map.LocationLayer.md#instance)
- [locationMode](map.LocationLayer.md#locationmode)
- [enableDirection](map.LocationLayer.md#enabledirection)

### Accessors

- [visible](map.LocationLayer.md#visible)
- [location](map.LocationLayer.md#location)
- [direction](map.LocationLayer.md#direction)
- [radius](map.LocationLayer.md#radius)
- [circleFillColor](map.LocationLayer.md#circlefillcolor)

### Methods

- [setName](map.LocationLayer.md#setname)
- [getName](map.LocationLayer.md#getname)
- [getLayerId](map.LocationLayer.md#getlayerid)
- [setVisible](map.LocationLayer.md#setvisible)
- [clear](map.LocationLayer.md#clear)
- [setData](map.LocationLayer.md#setdata)
- [getData](map.LocationLayer.md#getdata)
- [setLocation](map.LocationLayer.md#setlocation)
- [setDirection](map.LocationLayer.md#setdirection)
- [setRadius](map.LocationLayer.md#setradius)
- [setCircleFillColor](map.LocationLayer.md#setcirclefillcolor)
- [update](map.LocationLayer.md#update)
- [getLocationMode](map.LocationLayer.md#getlocationmode)
- [clearCustomLocationData](map.LocationLayer.md#clearcustomlocationdata)
- [setCustomLocationData](map.LocationLayer.md#setcustomlocationdata)

## Constructors

### constructor

• **new LocationLayer**(`compass`, `basemap`): [`LocationLayer`](map.LocationLayer.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `compass` | `default` |
| `basemap` | `default` |

#### Returns

[`LocationLayer`](map.LocationLayer.md)

#### Overrides

BaseLayer.constructor

## Properties

### instance

▪ `Static` **instance**: [`LocationLayer`](map.LocationLayer.md)

___

### locationMode

• **locationMode**: [`LocationMode`](../enums/map.SysEnum.LocationMode.md) = `LocationMode.NORMAL`

___

### enableDirection

• **enableDirection**: `boolean` = `true`

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

### location

• `get` **location**(): [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

获取位置点坐标
since 1.0.0

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

• `set` **location**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> |

#### Returns

`void`

**`Deprecated`**

推荐使用mapController.setLocation
设置位置点坐标
since 1.0.0

___

### direction

• `get` **direction**(): `number`

获取位置点指向
since 1.0.0

#### Returns

`number`

• `set` **direction**(`val`): `void`

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `val` | `number` | 方向取值在 0 ~ 360(正值是顺时针) since 1.0.0 |

#### Returns

`void`

**`Deprecated`**

推荐使用mapController.setLocation
设置位置点指向

___

### radius

• `get` **radius**(): `number`

#### Returns

`number`

**`Deprecated`**

获取位置点扩散范围
since 1.0.0

• `set` **radius**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Deprecated`**

设置位置点扩散范围，单位：米
since 1.0.0

___

### circleFillColor

• `get` **circleFillColor**(): [`ColorString`](../modules/map.md#colorstring)

#### Returns

[`ColorString`](../modules/map.md#colorstring)

**`Deprecated`**

获取位置点扩散范围填充颜色
since 1.0.0

• `set` **circleFillColor**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Deprecated`**

设置位置点扩散范围填充颜色
since 1.0.0

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

___

### setLocation

▸ **setLocation**(`val`): [`LocationLayer`](map.LocationLayer.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LatLng`](base.LatLng.md) |

#### Returns

[`LocationLayer`](map.LocationLayer.md)

**`Deprecated`**

推荐使用mapController.setLocation
设置位置点坐标
since 1.2.0

___

### setDirection

▸ **setDirection**(`val`): [`LocationLayer`](map.LocationLayer.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

[`LocationLayer`](map.LocationLayer.md)

**`Deprecated`**

推荐使用mapController.setLocation
设置位置点指向
since 1.2.0

___

### setRadius

▸ **setRadius**(`val`): [`LocationLayer`](map.LocationLayer.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

[`LocationLayer`](map.LocationLayer.md)

**`Deprecated`**

设置位置点扩散范围填充颜色
since 1.2.0

___

### setCircleFillColor

▸ **setCircleFillColor**(`val`): [`LocationLayer`](map.LocationLayer.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`LocationLayer`](map.LocationLayer.md)

**`Deprecated`**

设置位置点扩散范围填充颜色
since 1.2.0

___

### update

▸ **update**(): `void`

#### Returns

`void`

#### Overrides

BaseLayer.update

___

### getLocationMode

▸ **getLocationMode**(): [`LocationMode`](../enums/map.SysEnum.LocationMode.md)

#### Returns

[`LocationMode`](../enums/map.SysEnum.LocationMode.md)

___

### clearCustomLocationData

▸ **clearCustomLocationData**(): `void`

#### Returns

`void`

___

### setCustomLocationData

▸ **setCustomLocationData**(`list`): `Promise`\<`void`\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `list` | `default`[] |

#### Returns

`Promise`\<`void`\>
