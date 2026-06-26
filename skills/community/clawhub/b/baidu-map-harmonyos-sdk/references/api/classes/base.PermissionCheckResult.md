[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / PermissionCheckResult

# Class: PermissionCheckResult

[base](../modules/base.md).PermissionCheckResult

权限检查结果类，包含完整的认证信息

## Table of contents

### Constructors

- [constructor](base.PermissionCheckResult.md#constructor)

### Properties

- [mErrorCode](base.PermissionCheckResult.md#merrorcode)
- [msg](base.PermissionCheckResult.md#msg)
- [mToken](base.PermissionCheckResult.md#mtoken)
- [uid](base.PermissionCheckResult.md#uid)
- [appid](base.PermissionCheckResult.md#appid)
- [mAdvancePermission](base.PermissionCheckResult.md#madvancepermission)
- [mUserAdvancePermission](base.PermissionCheckResult.md#museradvancepermission)
- [mNewAdvancePermission](base.PermissionCheckResult.md#mnewadvancepermission)
- [mNewUserAdvancePermission](base.PermissionCheckResult.md#mnewuseradvancepermission)

### Methods

- [toString](base.PermissionCheckResult.md#tostring)

## Constructors

### constructor

• **new PermissionCheckResult**(): [`PermissionCheckResult`](base.PermissionCheckResult.md)

#### Returns

[`PermissionCheckResult`](base.PermissionCheckResult.md)

## Properties

### mErrorCode

• **mErrorCode**: `number` = `0`

错误码

___

### msg

• **msg**: `string` = `''`

认证结果消息

___

### mToken

• **mToken**: `string` = `''`

认证token

___

### uid

• **uid**: `string` = `'-1'`

用户ID

___

### appid

• **appid**: `string` = `'-1'`

应用ID

___

### mAdvancePermission

• **mAdvancePermission**: `number` = `0`

AK权限

___

### mUserAdvancePermission

• **mUserAdvancePermission**: `number` = `0`

用户权限

___

### mNewAdvancePermission

• **mNewAdvancePermission**: `number` = `0`

新版AK权限

___

### mNewUserAdvancePermission

• **mNewUserAdvancePermission**: `number` = `0`

新版用户权限

## Methods

### toString

▸ **toString**(): `string`

格式化输出认证结果信息

#### Returns

`string`
