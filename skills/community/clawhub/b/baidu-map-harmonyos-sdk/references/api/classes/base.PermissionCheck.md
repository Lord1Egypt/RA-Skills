[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / PermissionCheck

# Class: PermissionCheck

[base](../modules/base.md).PermissionCheck

权限检查类 - 百度地图SDK权限验证组件
使用前需先调用init方法，使用后需调用destroy方法清理资源

## Table of contents

### Properties

- [AUTH\_STATE\_APP\_NOT\_EXIST](base.PermissionCheck.md#auth_state_app_not_exist)
- [AUTH\_STATE\_APP\_DENY](base.PermissionCheck.md#auth_state_app_deny)
- [AUTH\_STATE\_USER\_DENY](base.PermissionCheck.md#auth_state_user_deny)

### Methods

- [init](base.PermissionCheck.md#init)
- [setApiKey](base.PermissionCheck.md#setapikey)
- [getApiKey](base.PermissionCheck.md#getapikey)
- [isPrivacyMode](base.PermissionCheck.md#isprivacymode)
- [permissionCheck](base.PermissionCheck.md#permissioncheck)
- [setPermissionCheckResultListener](base.PermissionCheck.md#setpermissioncheckresultlistener)
- [getPermissionResult](base.PermissionCheck.md#getpermissionresult)
- [isInit](base.PermissionCheck.md#isinit)
- [getDeviceParams](base.PermissionCheck.md#getdeviceparams)
- [destroy](base.PermissionCheck.md#destroy)

## Properties

### AUTH\_STATE\_APP\_NOT\_EXIST

▪ `Static` `Readonly` **AUTH\_STATE\_APP\_NOT\_EXIST**: ``200``

___

### AUTH\_STATE\_APP\_DENY

▪ `Static` `Readonly` **AUTH\_STATE\_APP\_DENY**: ``202``

___

### AUTH\_STATE\_USER\_DENY

▪ `Static` `Readonly` **AUTH\_STATE\_USER\_DENY**: ``252``

## Methods

### init

▸ **init**(`context`): `Promise`\<`boolean`\>

初始化权限检查模块

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `context` | `UIAbilityContext` | 应用上下文 |

#### Returns

`Promise`\<`boolean`\>

初始化是否成功

___

### setApiKey

▸ **setApiKey**(`ak`): `void`

设置API密钥

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `ak` | `string` | API密钥 |

#### Returns

`void`

___

### getApiKey

▸ **getApiKey**(): `string`

获取当前API密钥

#### Returns

`string`

当前API密钥

___

### isPrivacyMode

▸ **isPrivacyMode**(): `boolean`

获取隐私模式状态

#### Returns

`boolean`

是否开启隐私模式

___

### permissionCheck

▸ **permissionCheck**(): `Promise`\<`number`\>

执行权限检查
返回鉴权码说明：
-1: 内部错误（网络原因未发起验证/服务端内部错误）
0: 通过校验
2: 参数错误
-10/-11: 网络错误
101: ak不存在
102: mcode签名值不正确
202-205、210、233: 无请求权限
231: 用户uid，ak不存在
232: 用户ak被封禁
301-355: 配额不存在
601: 未认证
602: 认证中

#### Returns

`Promise`\<`number`\>

权限检查结果码的Promise

___

### setPermissionCheckResultListener

▸ **setPermissionCheckResultListener**(`listener`): `void`

设置权限检查结果监听器

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `listener` | ``null`` \| [`PermissionCheckResultListener`](../interfaces/base.PermissionCheckResultListener.md) | 结果监听器 |

#### Returns

`void`

___

### getPermissionResult

▸ **getPermissionResult**(): `number`

获取当前权限检查结果

#### Returns

`number`

权限检查结果码

___

### isInit

▸ **isInit**(): `boolean`

检查是否已初始化

#### Returns

`boolean`

是否已初始化

___

### getDeviceParams

▸ **getDeviceParams**(): `Map`\<`string`, `string`\>

获取设备参数映射（用于调试）

#### Returns

`Map`\<`string`, `string`\>

设备参数映射的副本

___

### destroy

▸ **destroy**(): `void`

清理资源，释放内存
应用销毁时调用此方法

#### Returns

`void`
