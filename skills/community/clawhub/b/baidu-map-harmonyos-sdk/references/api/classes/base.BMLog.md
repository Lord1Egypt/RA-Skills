[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / BMLog

# Class: BMLog

[base](../modules/base.md).BMLog

## Table of contents

### Constructors

- [constructor](base.BMLog.md#constructor)

### Properties

- [logLevel](base.BMLog.md#loglevel)

### Methods

- [debug](base.BMLog.md#debug)
- [info](base.BMLog.md#info)
- [warn](base.BMLog.md#warn)
- [error](base.BMLog.md#error)

## Constructors

### constructor

• **new BMLog**(): [`BMLog`](base.BMLog.md)

#### Returns

[`BMLog`](base.BMLog.md)

## Properties

### logLevel

▪ `Static` **logLevel**: `LogLevel` = `hilog.LogLevel.FATAL`

## Methods

### debug

▸ **debug**(`tag?`, `content?`, `...args`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag?` | `string` |
| `content?` | `string` |
| `...args` | `ESObject`[] |

#### Returns

`void`

___

### info

▸ **info**(`tag?`, `content?`, `...args`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag?` | `string` |
| `content?` | `string` |
| `...args` | `ESObject`[] |

#### Returns

`void`

___

### warn

▸ **warn**(`tag?`, `content?`, `...args`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag?` | `string` |
| `content?` | `string` |
| `...args` | `ESObject`[] |

#### Returns

`void`

___

### error

▸ **error**(`tag?`, `content?`, `...args`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag?` | `string` |
| `content?` | `string` |
| `...args` | `ESObject`[] |

#### Returns

`void`
