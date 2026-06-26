[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / BMLocation

# Class: BMLocation

[walkridecommon](../modules/walkridecommon.md).BMLocation

## Table of contents

### Constructors

- [constructor](walkridecommon.BMLocation.md#constructor)

### Properties

- [BDLOCATION\_GCJ02\_TO\_BD09LL](walkridecommon.BMLocation.md#bdlocation_gcj02_to_bd09ll)
- [BDLOCATION\_BD09\_TO\_GCJ02](walkridecommon.BMLocation.md#bdlocation_bd09_to_gcj02)
- [BDLOCATION\_BD09LL\_TO\_GCJ02](walkridecommon.BMLocation.md#bdlocation_bd09ll_to_gcj02)
- [BDLOCATION\_WGS84\_TO\_GCJ02](walkridecommon.BMLocation.md#bdlocation_wgs84_to_gcj02)
- [TYPE\_NONE](walkridecommon.BMLocation.md#type_none)
- [TYPE\_NETWORK\_EXCEPTION](walkridecommon.BMLocation.md#type_network_exception)
- [TYPE\_SYS\_SERVICE\_EXCEPTION](walkridecommon.BMLocation.md#type_sys_service_exception)
- [TYPE\_SYS\_LOCATION\_FAIL](walkridecommon.BMLocation.md#type_sys_location_fail)
- [TYPE\_LOCATION\_SERVICE\_SWITCH\_CLOSED\_FAIL](walkridecommon.BMLocation.md#type_location_service_switch_closed_fail)
- [TYPE\_NO\_PERMISSION\_LOCATION\_FAIL](walkridecommon.BMLocation.md#type_no_permission_location_fail)
- [TYPE\_NETWORK\_LOCATION](walkridecommon.BMLocation.md#type_network_location)
- [TYPE\_SERVER\_ERROR](walkridecommon.BMLocation.md#type_server_error)
- [TYPE\_SERVER\_CHECK\_KEY\_ERROR](walkridecommon.BMLocation.md#type_server_check_key_error)

### Methods

- [setLongitude](walkridecommon.BMLocation.md#setlongitude)
- [getLongitude](walkridecommon.BMLocation.md#getlongitude)
- [setCoorType](walkridecommon.BMLocation.md#setcoortype)
- [getCoorType](walkridecommon.BMLocation.md#getcoortype)
- [setLatitude](walkridecommon.BMLocation.md#setlatitude)
- [getLatitude](walkridecommon.BMLocation.md#getlatitude)
- [setAltitude](walkridecommon.BMLocation.md#setaltitude)
- [getAltitude](walkridecommon.BMLocation.md#getaltitude)
- [setRadius](walkridecommon.BMLocation.md#setradius)
- [getRadius](walkridecommon.BMLocation.md#getradius)
- [setSpeed](walkridecommon.BMLocation.md#setspeed)
- [getSpeed](walkridecommon.BMLocation.md#getspeed)
- [setDirection](walkridecommon.BMLocation.md#setdirection)
- [getDirection](walkridecommon.BMLocation.md#getdirection)
- [setTime](walkridecommon.BMLocation.md#settime)
- [getTime](walkridecommon.BMLocation.md#gettime)
- [setLocType](walkridecommon.BMLocation.md#setloctype)
- [getLocType](walkridecommon.BMLocation.md#getloctype)
- [setAddr](walkridecommon.BMLocation.md#setaddr)
- [getAddr](walkridecommon.BMLocation.md#getaddr)
- [hasAddr](walkridecommon.BMLocation.md#hasaddr)
- [setAddrStr](walkridecommon.BMLocation.md#setaddrstr)
- [getAddrStr](walkridecommon.BMLocation.md#getaddrstr)
- [getCountry](walkridecommon.BMLocation.md#getcountry)
- [getCountryCode](walkridecommon.BMLocation.md#getcountrycode)
- [getProvince](walkridecommon.BMLocation.md#getprovince)
- [getCity](walkridecommon.BMLocation.md#getcity)
- [getCityCode](walkridecommon.BMLocation.md#getcitycode)
- [getDistrict](walkridecommon.BMLocation.md#getdistrict)
- [getStreet](walkridecommon.BMLocation.md#getstreet)
- [getStreetNumber](walkridecommon.BMLocation.md#getstreetnumber)
- [getAdCode](walkridecommon.BMLocation.md#getadcode)
- [getTown](walkridecommon.BMLocation.md#gettown)
- [setLocationDescribe](walkridecommon.BMLocation.md#setlocationdescribe)
- [getLocationDescribe](walkridecommon.BMLocation.md#getlocationdescribe)

## Constructors

### constructor

• **new BMLocation**(`x?`): [`BMLocation`](walkridecommon.BMLocation.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `x?` | `string` \| [`BMLocation`](walkridecommon.BMLocation.md) |

#### Returns

[`BMLocation`](walkridecommon.BMLocation.md)

## Properties

### BDLOCATION\_GCJ02\_TO\_BD09LL

▪ `Static` `Readonly` **BDLOCATION\_GCJ02\_TO\_BD09LL**: `string` = `"bd09ll"`

___

### BDLOCATION\_BD09\_TO\_GCJ02

▪ `Static` `Readonly` **BDLOCATION\_BD09\_TO\_GCJ02**: `string` = `"bd092gcj"`

___

### BDLOCATION\_BD09LL\_TO\_GCJ02

▪ `Static` `Readonly` **BDLOCATION\_BD09LL\_TO\_GCJ02**: `string` = `"bd09ll2gcj"`

___

### BDLOCATION\_WGS84\_TO\_GCJ02

▪ `Static` `Readonly` **BDLOCATION\_WGS84\_TO\_GCJ02**: `string` = `"gps2gcj"`

___

### TYPE\_NONE

▪ `Static` `Readonly` **TYPE\_NONE**: ``0``

___

### TYPE\_NETWORK\_EXCEPTION

▪ `Static` `Readonly` **TYPE\_NETWORK\_EXCEPTION**: `number` = `63`

___

### TYPE\_SYS\_SERVICE\_EXCEPTION

▪ `Static` `Readonly` **TYPE\_SYS\_SERVICE\_EXCEPTION**: `number` = `64`

___

### TYPE\_SYS\_LOCATION\_FAIL

▪ `Static` `Readonly` **TYPE\_SYS\_LOCATION\_FAIL**: `number` = `65`

___

### TYPE\_LOCATION\_SERVICE\_SWITCH\_CLOSED\_FAIL

▪ `Static` `Readonly` **TYPE\_LOCATION\_SERVICE\_SWITCH\_CLOSED\_FAIL**: `number` = `69`

___

### TYPE\_NO\_PERMISSION\_LOCATION\_FAIL

▪ `Static` `Readonly` **TYPE\_NO\_PERMISSION\_LOCATION\_FAIL**: `number` = `70`

___

### TYPE\_NETWORK\_LOCATION

▪ `Static` `Readonly` **TYPE\_NETWORK\_LOCATION**: `number` = `161`

___

### TYPE\_SERVER\_ERROR

▪ `Static` `Readonly` **TYPE\_SERVER\_ERROR**: `number` = `162`

___

### TYPE\_SERVER\_CHECK\_KEY\_ERROR

▪ `Static` `Readonly` **TYPE\_SERVER\_CHECK\_KEY\_ERROR**: `number` = `505`

## Methods

### setLongitude

▸ **setLongitude**(`longitude`): `void`

墨卡托坐标的X

#### Parameters

| Name | Type |
| :------ | :------ |
| `longitude` | `number` |

#### Returns

`void`

___

### getLongitude

▸ **getLongitude**(): `number`

#### Returns

`number`

___

### setCoorType

▸ **setCoorType**(`coorType`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `coorType` | `string` |

#### Returns

`void`

___

### getCoorType

▸ **getCoorType**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### setLatitude

▸ **setLatitude**(`latitude`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `latitude` | `number` |

#### Returns

`void`

___

### getLatitude

▸ **getLatitude**(): `number`

#### Returns

`number`

___

### setAltitude

▸ **setAltitude**(`altitude`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `altitude` | `number` |

#### Returns

`void`

___

### getAltitude

▸ **getAltitude**(): `number`

#### Returns

`number`

___

### setRadius

▸ **setRadius**(`radius`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius` | `number` |

#### Returns

`void`

___

### getRadius

▸ **getRadius**(): `number`

#### Returns

`number`

___

### setSpeed

▸ **setSpeed**(`speed`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `speed` | `number` |

#### Returns

`void`

___

### getSpeed

▸ **getSpeed**(): `number`

#### Returns

`number`

___

### setDirection

▸ **setDirection**(`direction`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `direction` | `number` |

#### Returns

`void`

___

### getDirection

▸ **getDirection**(): `number`

#### Returns

`number`

___

### setTime

▸ **setTime**(`time`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `time` | `string` |

#### Returns

`void`

___

### getTime

▸ **getTime**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### setLocType

▸ **setLocType**(`locType`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `locType` | `number` |

#### Returns

`void`

___

### getLocType

▸ **getLocType**(): `number`

#### Returns

`number`

___

### setAddr

▸ **setAddr**(`addr`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `addr` | ``null`` \| `Address` |

#### Returns

`void`

___

### getAddr

▸ **getAddr**(): `Address`

#### Returns

`Address`

___

### hasAddr

▸ **hasAddr**(): `boolean`

#### Returns

`boolean`

___

### setAddrStr

▸ **setAddrStr**(`addrStr`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `addrStr` | ``null`` \| `string` |

#### Returns

`void`

___

### getAddrStr

▸ **getAddrStr**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getCountry

▸ **getCountry**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getCountryCode

▸ **getCountryCode**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getProvince

▸ **getProvince**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getCity

▸ **getCity**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getCityCode

▸ **getCityCode**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getDistrict

▸ **getDistrict**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getStreet

▸ **getStreet**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getStreetNumber

▸ **getStreetNumber**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getAdCode

▸ **getAdCode**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### getTown

▸ **getTown**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### setLocationDescribe

▸ **setLocationDescribe**(`locationDescribe`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `locationDescribe` | ``null`` \| `string` |

#### Returns

`void`

___

### getLocationDescribe

▸ **getLocationDescribe**(): ``null`` \| `string`

#### Returns

``null`` \| `string`
