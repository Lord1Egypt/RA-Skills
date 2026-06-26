[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / AlgorithmUtil

# Class: AlgorithmUtil

[base](../modules/base.md).AlgorithmUtil

算法工具类

## Table of contents

### Methods

- [aesDecryptAsync](base.AlgorithmUtil.md#aesdecryptasync)
- [aesDecryptCRT](base.AlgorithmUtil.md#aesdecryptcrt)
- [hexStringConvertBytes](base.AlgorithmUtil.md#hexstringconvertbytes)
- [uint8ArrayToString](base.AlgorithmUtil.md#uint8arraytostring)

## Methods

### aesDecryptAsync

▸ **aesDecryptAsync**(`geom`, `aesSaltKey`, `aesVitKey`): `Promise`\<`string`\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `geom` | `string` |
| `aesSaltKey` | `string` |
| `aesVitKey` | `string` |

#### Returns

`Promise`\<`string`\>

___

### aesDecryptCRT

▸ **aesDecryptCRT**(`geom`, `aesSaltKey`, `aesVitKey`, `callback`): `Promise`\<`void`\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `geom` | `string` |
| `aesSaltKey` | `string` |
| `aesVitKey` | `string` |
| `callback` | (`result`: `string`) => `void` |

#### Returns

`Promise`\<`void`\>

___

### hexStringConvertBytes

▸ **hexStringConvertBytes**(`data`): `Uint8Array`

转16进制

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `data` | `string` | 密文 |

#### Returns

`Uint8Array`

___

### uint8ArrayToString

▸ **uint8ArrayToString**(`array`): `string`

#### Parameters

| Name | Type |
| :------ | :------ |
| `array` | `Uint8Array` |

#### Returns

`string`
