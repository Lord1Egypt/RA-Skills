[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / LicenseRequestModel

# Class: LicenseRequestModel

[walkridecommon](../modules/walkridecommon.md).LicenseRequestModel

## Table of contents

### Constructors

- [constructor](walkridecommon.LicenseRequestModel.md#constructor)

### Properties

- [LICENSE\_BASE\_URL](walkridecommon.LicenseRequestModel.md#license_base_url)
- [LICENSE\_PATH](walkridecommon.LicenseRequestModel.md#license_path)
- [METHOD](walkridecommon.LicenseRequestModel.md#method)
- [bundle](walkridecommon.LicenseRequestModel.md#bundle)

### Methods

- [fetch](walkridecommon.LicenseRequestModel.md#fetch)

## Constructors

### constructor

• **new LicenseRequestModel**(): [`LicenseRequestModel`](walkridecommon.LicenseRequestModel.md)

#### Returns

[`LicenseRequestModel`](walkridecommon.LicenseRequestModel.md)

## Properties

### LICENSE\_BASE\_URL

▪ `Static` **LICENSE\_BASE\_URL**: `string` = `'https://api.map.baidu.com'`

___

### LICENSE\_PATH

▪ `Static` **LICENSE\_PATH**: `string` = `'/license/device/file'`

___

### METHOD

▪ `Static` **METHOD**: `string` = `'POST'`

___

### bundle

• **bundle**: `Map`\<`string`, `string` \| `number`\>

## Methods

### fetch

▸ **fetch**(`bundle`): `Promise`\<`IHttpResponse`\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `bundle` | `Map`\<`string`, `string` \| `number`\> |

#### Returns

`Promise`\<`IHttpResponse`\>
