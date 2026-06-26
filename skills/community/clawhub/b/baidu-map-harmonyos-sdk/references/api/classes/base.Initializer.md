[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / Initializer

# Class: Initializer

[base](../modules/base.md).Initializer

用于初始化权限并管理令牌的单例类。

## Implements

- [`PermissionCheckResultListener`](../interfaces/base.PermissionCheckResultListener.md)

## Table of contents

### Accessors

- [watchSearchTime](base.Initializer.md#watchsearchtime)
- [watchSearchMaxNum](base.Initializer.md#watchsearchmaxnum)
- [coordType](base.Initializer.md#coordtype)

### Methods

- [getInstance](base.Initializer.md#getinstance)
- [initialize](base.Initializer.md#initialize)

## Accessors

### watchSearchTime

• `get` **watchSearchTime**(): `number`

#### Returns

`number`

• `set` **watchSearchTime**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

`void`

___

### watchSearchMaxNum

• `get` **watchSearchMaxNum**(): `number`

#### Returns

`number`

• `set` **watchSearchMaxNum**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

`void`

___

### coordType

• `get` **coordType**(): [`CoordType`](../enums/base.CoordType.md)

获取使用的坐标类型，支持GCJ02和 BD09LL两种坐标[CoordType](../enums/base.CoordType.md)的输入输出，默认是BD09LL坐标

#### Returns

[`CoordType`](../enums/base.CoordType.md)

使用的坐标类型

• `set` **coordType**(`value`): `void`

设置使用的坐标类型，支持GCJ02和BD09LL两种坐标[CoordType](../enums/base.CoordType.md)的输入输出，默认是BD09LL坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`CoordType`](../enums/base.CoordType.md) |

#### Returns

`void`

## Methods

### getInstance

▸ **getInstance**(): [`Initializer`](base.Initializer.md)

获取 Initializer 的单例实例。

#### Returns

[`Initializer`](base.Initializer.md)

Initializer 的单例实例。

___

### initialize

▸ **initialize**(`ak`, `context`): `Promise`\<`boolean`\>

使用提供的 API 密钥初始化权限。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `ak` | `string` | 用于初始化的 API 密钥。 |
| `context` | `UIAbilityContext` | UIAbility上下文，建议每个Hap包中只包含一个UIAbility。(https://developer.huawei.com/consumer/cn/doc/harmonyos-faqs/faqs-ability-66) |

#### Returns

`Promise`\<`boolean`\>
