[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / OpenClientUtil

# Class: OpenClientUtil

[util](../modules/util.md).OpenClientUtil

调起百度客户端工具类

**`Author`**

v_wangfujun

## Table of contents

### Constructors

- [constructor](util.OpenClientUtil.md#constructor)

### Methods

- [getBaiduMapVersion](util.OpenClientUtil.md#getbaidumapversion)
- [checkBaiduMapInstalled](util.OpenClientUtil.md#checkbaidumapinstalled)
- [openAppMarket](util.OpenClientUtil.md#openappmarket)

## Constructors

### constructor

• **new OpenClientUtil**(): [`OpenClientUtil`](util.OpenClientUtil.md)

#### Returns

[`OpenClientUtil`](util.OpenClientUtil.md)

## Methods

### getBaiduMapVersion

▸ **getBaiduMapVersion**(`context`): `number`

获取百度地图客户端版本号

#### Parameters

| Name | Type |
| :------ | :------ |
| `context` | `UIAbilityContext` |

#### Returns

`number`

返回0代表没有安装百度地图客户端

___

### checkBaiduMapInstalled

▸ **checkBaiduMapInstalled**(): `boolean`

判断是否安装百度地图客户端

#### Returns

`boolean`

返回false代表没有安装百度地图客户端

___

### openAppMarket

▸ **openAppMarket**(`context`): `Promise`\<`void`\>

调转到应用市场中安装百度地图app

#### Parameters

| Name | Type |
| :------ | :------ |
| `context` | `UIAbilityContext` |

#### Returns

`Promise`\<`void`\>
