[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / BMThreadUtils

# Class: BMThreadUtils

[base](../modules/base.md).BMThreadUtils

线程工具类

## Table of contents

### Constructors

- [constructor](base.BMThreadUtils.md#constructor)

### Properties

- [mainThreadId](base.BMThreadUtils.md#mainthreadid)

### Methods

- [initMainThreadId](base.BMThreadUtils.md#initmainthreadid)
- [isOnUiThread](base.BMThreadUtils.md#isonuithread)
- [assertOnUiThread](base.BMThreadUtils.md#assertonuithread)
- [runOnUiThread](base.BMThreadUtils.md#runonuithread)
- [runOnTaskPool](base.BMThreadUtils.md#runontaskpool)
- [generateTask](base.BMThreadUtils.md#generatetask)

## Constructors

### constructor

• **new BMThreadUtils**(): [`BMThreadUtils`](base.BMThreadUtils.md)

#### Returns

[`BMThreadUtils`](base.BMThreadUtils.md)

## Properties

### mainThreadId

▪ `Static` **mainThreadId**: `number` = `0`

主线程ID

## Methods

### initMainThreadId

▸ **initMainThreadId**(): `void`

设置主线程ID

process.tid可以获取到调用时的所在线程的ID，但没有直接获取到主线程的ID的api；
Ability初始化时，通过process获取主线程ID，保存在BMThreadUtils.mainThreadId。

#### Returns

`void`

___

### isOnUiThread

▸ **isOnUiThread**(): `boolean`

判断是否在主线程

#### Returns

`boolean`

如果当前所在为主线程，返回true；否则返回false

___

### assertOnUiThread

▸ **assertOnUiThread**(): `void`

判断是否在主线程，如果不是则抛出异常

#### Returns

`void`

___

### runOnUiThread

▸ **runOnUiThread**(`func?`, `...args`): `Promise`\<`void`\>

切换至主线程执行

如果当前在主线程，则直接执行func；否则通过taskpool.Task发送到主线程执行。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `func?` | `Function` | 待执行方法 |
| `...args` | `Object`[] | 参数 |

#### Returns

`Promise`\<`void`\>

___

### runOnTaskPool

▸ **runOnTaskPool**(`func`, `...args`): `Promise`\<`Object`\>

切换至工作线程执行

api使用限制：
1.在工作线程执行的函数，必须有@Concurrent注解；由于@Concurrent的限制，可将方法放置于ConcurrentFuctions.ets中。
2.在工作线程执行的函数，参数必须为可序列化的（如果需要其他不可序列化的参数，请通过全局、单例等方法在函数执行时获取）。

如果待执行函数中需要向host线程回调，请直接使用原生api来实现：
     1）设置回调函数，通过task.onReceiveData(callback)设置。
     2）在task的func中，通过task.sendData(...args: Object[])向host线程发送数据，args为calback所需要的参数。

#### Parameters

| Name | Type |
| :------ | :------ |
| `func` | `Function` |
| `...args` | `Object`[] |

#### Returns

`Promise`\<`Object`\>

___

### generateTask

▸ **generateTask**(`func`, `...args`): `any`

生成待执行任务

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `func` | `Function` | 待执行方法 |
| `...args` | `Object`[] | 参数 |

#### Returns

`any`

taskpool.Task
