[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / WalkRunningControl

# Class: WalkRunningControl

[map](../modules/map.md).WalkRunningControl

## Table of contents

### Methods

- [getInstance](map.WalkRunningControl.md#getinstance)
- [sportRunningSetting](map.WalkRunningControl.md#sportrunningsetting)
- [walkRunning\_Create](map.WalkRunningControl.md#walkrunning_create)
- [walkRunning\_SwitchSportType](map.WalkRunningControl.md#walkrunning_switchsporttype)
- [walkRunning\_SetTrackStatus](map.WalkRunningControl.md#walkrunning_settrackstatus)
- [walkRunning\_Init](map.WalkRunningControl.md#walkrunning_init)
- [walkRunning\_StartRecord](map.WalkRunningControl.md#walkrunning_startrecord)
- [walkRunning\_StopRecord](map.WalkRunningControl.md#walkrunning_stoprecord)
- [walkRunning\_ResumeRecord](map.WalkRunningControl.md#walkrunning_resumerecord)
- [walkRunning\_PauseRecord](map.WalkRunningControl.md#walkrunning_pauserecord)
- [walkRunning\_Release](map.WalkRunningControl.md#walkrunning_release)
- [walkRunning\_UpdateRunningTime](map.WalkRunningControl.md#walkrunning_updaterunningtime)
- [walkRunning\_SwitchVoice](map.WalkRunningControl.md#walkrunning_switchvoice)
- [walkRunning\_GetWalkCountData](map.WalkRunningControl.md#walkrunning_getwalkcountdata)
- [walkRunning\_TriggerGPSDataChange](map.WalkRunningControl.md#walkrunning_triggergpsdatachange)
- [walkRunning\_GetUploadRecordParamBundle](map.WalkRunningControl.md#walkrunning_getuploadrecordparambundle)

## Methods

### getInstance

▸ **getInstance**(): [`WalkRunningControl`](map.WalkRunningControl.md)

#### Returns

[`WalkRunningControl`](map.WalkRunningControl.md)

___

### sportRunningSetting

▸ **sportRunningSetting**(`mapviewPtr`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `mapviewPtr` | `string` \| `number` |

#### Returns

`void`

___

### walkRunning\_Create

▸ **walkRunning_Create**(`mapviewPtr`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `mapviewPtr` | `string` \| `number` |

#### Returns

`boolean`

___

### walkRunning\_SwitchSportType

▸ **walkRunning_SwitchSportType**(`type`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`SportTypeEnum`](../enums/map.SportTypeEnum.md) |

#### Returns

`boolean`

___

### walkRunning\_SetTrackStatus

▸ **walkRunning_SetTrackStatus**(`status`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `status` | [`RunningTrackStatusEnum`](../enums/map.RunningTrackStatusEnum.md) |

#### Returns

`boolean`

___

### walkRunning\_Init

▸ **walkRunning_Init**(`config`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `config` | [`RunningConfig`](../interfaces/map.RunningConfig.md) |

#### Returns

`boolean`

___

### walkRunning\_StartRecord

▸ **walkRunning_StartRecord**(): `boolean`

#### Returns

`boolean`

___

### walkRunning\_StopRecord

▸ **walkRunning_StopRecord**(): `boolean`

#### Returns

`boolean`

___

### walkRunning\_ResumeRecord

▸ **walkRunning_ResumeRecord**(): `boolean`

#### Returns

`boolean`

___

### walkRunning\_PauseRecord

▸ **walkRunning_PauseRecord**(): `boolean`

#### Returns

`boolean`

___

### walkRunning\_Release

▸ **walkRunning_Release**(): `boolean`

#### Returns

`boolean`

___

### walkRunning\_UpdateRunningTime

▸ **walkRunning_UpdateRunningTime**(`nDurSecond`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `nDurSecond` | `number` |

#### Returns

`boolean`

___

### walkRunning\_SwitchVoice

▸ **walkRunning_SwitchVoice**(`nVoiceSwitch`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `nVoiceSwitch` | `number` |

#### Returns

`boolean`

___

### walkRunning\_GetWalkCountData

▸ **walkRunning_GetWalkCountData**(): [`WalkDetailData`](../interfaces/map.WalkDetailData.md)

#### Returns

[`WalkDetailData`](../interfaces/map.WalkDetailData.md)

___

### walkRunning\_TriggerGPSDataChange

▸ **walkRunning_TriggerGPSDataChange**(`gps`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `gps` | [`GPSData`](../interfaces/map.GPSData.md) |

#### Returns

`boolean`

___

### walkRunning\_GetUploadRecordParamBundle

▸ **walkRunning_GetUploadRecordParamBundle**(): `string`

#### Returns

`string`
