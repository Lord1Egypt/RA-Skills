[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / ITTSPlugin

# Interface: ITTSPlugin

[walkridecommon](../modules/walkridecommon.md).ITTSPlugin

导航语音TTS播放器接口

## Table of contents

### Methods

- [init](walkridecommon.ITTSPlugin.md#init)
- [unInit](walkridecommon.ITTSPlugin.md#uninit)
- [playTTSText](walkridecommon.ITTSPlugin.md#playttstext)

## Methods

### init

▸ **init**(): `void`

#### Returns

`void`

___

### unInit

▸ **unInit**(): `void`

#### Returns

`void`

___

### playTTSText

▸ **playTTSText**(`speech`, `bPreempt`): `number`

获取导航过程中语音,进行播报

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `speech` | `string` | 播报语音文本 |
| `bPreempt` | `boolean` | 是否抢占播报 |

#### Returns

`number`

播报状态码
