[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / DeviceInfo

# Class: DeviceInfo

[base](../modules/base.md).DeviceInfo

## Table of contents

### Accessors

- [authToken](base.DeviceInfo.md#authtoken)

### Methods

- [getInstance](base.DeviceInfo.md#getinstance)
- [init](base.DeviceInfo.md#init)
- [getParams](base.DeviceInfo.md#getparams)
- [getName](base.DeviceInfo.md#getname)
- [setCuid](base.DeviceInfo.md#setcuid)
- [getModel](base.DeviceInfo.md#getmodel)
- [getCuid](base.DeviceInfo.md#getcuid)
- [getCTM](base.DeviceInfo.md#getctm)
- [getZid](base.DeviceInfo.md#getzid)
- [getResId](base.DeviceInfo.md#getresid)
- [getChanel](base.DeviceInfo.md#getchanel)
- [getSdkVersion](base.DeviceInfo.md#getsdkversion)
- [getSdkVersionForEngine](base.DeviceInfo.md#getsdkversionforengine)
- [getOsVersion](base.DeviceInfo.md#getosversion)
- [getDpi](base.DeviceInfo.md#getdpi)
- [getPCN](base.DeviceInfo.md#getpcn)
- [getScreenSize](base.DeviceInfo.md#getscreensize)
- [getBrands](base.DeviceInfo.md#getbrands)
- [getOEM](base.DeviceInfo.md#getoem)
- [getAppId](base.DeviceInfo.md#getappid)
- [getNet](base.DeviceInfo.md#getnet)

## Accessors

### authToken

• `get` **authToken**(): `string`

#### Returns

`string`

• `set` **authToken**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

`void`

## Methods

### getInstance

▸ **getInstance**(): [`DeviceInfo`](base.DeviceInfo.md)

#### Returns

[`DeviceInfo`](base.DeviceInfo.md)

___

### init

▸ **init**(): `Promise`\<`boolean`\>

#### Returns

`Promise`\<`boolean`\>

___

### getParams

▸ **getParams**(): `DeviceParams`

#### Returns

`DeviceParams`

___

### getName

▸ **getName**(): `string`

#### Returns

`string`

___

### setCuid

▸ **setCuid**(`cuid`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `cuid` | `string` |

#### Returns

`void`

___

### getModel

▸ **getModel**(): `string`

#### Returns

`string`

___

### getCuid

▸ **getCuid**(): `string`

#### Returns

`string`

___

### getCTM

▸ **getCTM**(): `string`

#### Returns

`string`

___

### getZid

▸ **getZid**(): `string`

#### Returns

`string`

___

### getResId

▸ **getResId**(): `string`

#### Returns

`string`

___

### getChanel

▸ **getChanel**(): `string`

#### Returns

`string`

___

### getSdkVersion

▸ **getSdkVersion**(): `string`

地图SDK版本获取

#### Returns

`string`

___

### getSdkVersionForEngine

▸ **getSdkVersionForEngine**(): `string`

#### Returns

`string`

___

### getOsVersion

▸ **getOsVersion**(): `string`

获取设备系统版本，规则以『OpenHarmony』+ 系统版本号的形式返回
注：可以在用户未授权时调用

#### Returns

`string`

百度地图定义的系统版本版本

___

### getDpi

▸ **getDpi**(): `string`

#### Returns

`string`

___

### getPCN

▸ **getPCN**(): `string`

#### Returns

`string`

___

### getScreenSize

▸ **getScreenSize**(): `string`

#### Returns

`string`

___

### getBrands

▸ **getBrands**(): `string`

#### Returns

`string`

___

### getOEM

▸ **getOEM**(): `string`

#### Returns

`string`

___

### getAppId

▸ **getAppId**(): `string`

#### Returns

`string`

___

### getNet

▸ **getNet**(): `string`

#### Returns

`string`
