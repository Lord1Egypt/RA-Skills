[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / WalkInNaviModel

# Class: WalkInNaviModel

[walkridecommon](../modules/walkridecommon.md).WalkInNaviModel

步行行中页model

## Table of contents

### Constructors

- [constructor](walkridecommon.WalkInNaviModel.md#constructor)

### Properties

- [curSpeed](walkridecommon.WalkInNaviModel.md#curspeed)
- [addDist](walkridecommon.WalkInNaviModel.md#adddist)
- [distRatio](walkridecommon.WalkInNaviModel.md#distratio)
- [hasFaraway](walkridecommon.WalkInNaviModel.md#hasfaraway)
- [isPaused](walkridecommon.WalkInNaviModel.md#ispaused)
- [remainInfo](walkridecommon.WalkInNaviModel.md#remaininfo)
- [arriveTime](walkridecommon.WalkInNaviModel.md#arrivetime)
- [guidePanelIcon](walkridecommon.WalkInNaviModel.md#guidepanelicon)
- [guidePanelFirstLine](walkridecommon.WalkInNaviModel.md#guidepanelfirstline)
- [guidePanelSecondLine](walkridecommon.WalkInNaviModel.md#guidepanelsecondline)
- [modelUid](walkridecommon.WalkInNaviModel.md#modeluid)

### Methods

- [updateGuideStatus](walkridecommon.WalkInNaviModel.md#updateguidestatus)
- [updateGuideStatusWithModel](walkridecommon.WalkInNaviModel.md#updateguidestatuswithmodel)
- [updateRemainInfo](walkridecommon.WalkInNaviModel.md#updateremaininfo)
- [getSingleLineText](walkridecommon.WalkInNaviModel.md#getsinglelinetext)
- [getNormalText](walkridecommon.WalkInNaviModel.md#getnormaltext)
- [guideTextStyleScale](walkridecommon.WalkInNaviModel.md#guidetextstylescale)

## Constructors

### constructor

• **new WalkInNaviModel**(): [`WalkInNaviModel`](walkridecommon.WalkInNaviModel.md)

#### Returns

[`WalkInNaviModel`](walkridecommon.WalkInNaviModel.md)

## Properties

### curSpeed

• **curSpeed**: `number` = `0`

___

### addDist

• **addDist**: `number` = `0`

___

### distRatio

• **distRatio**: `number` = `0`

___

### hasFaraway

• **hasFaraway**: `boolean` = `false`

___

### isPaused

• **isPaused**: `boolean` = `true`

___

### remainInfo

• **remainInfo**: `string` = `""`

___

### arriveTime

• **arriveTime**: `string` = `""`

___

### guidePanelIcon

• **guidePanelIcon**: `any`

___

### guidePanelFirstLine

• **guidePanelFirstLine**: `any` = `""`

___

### guidePanelSecondLine

• **guidePanelSecondLine**: `any` = `""`

___

### modelUid

• **modelUid**: `number` = `-1`

## Methods

### updateGuideStatus

▸ **updateGuideStatus**(`guidePanelIcon`, `guidePanelContent`, `guidePanelSecondLine?`): `void`

更新诱导面板UI

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `guidePanelIcon` | `Resource` | `undefined` | 诱导面板图标 |
| `guidePanelContent` | `string` | `undefined` | 诱导面板内容 |
| `guidePanelSecondLine` | `string` | `''` | - |

#### Returns

`void`

___

### updateGuideStatusWithModel

▸ **updateGuideStatusWithModel**(`model`): `void`

更新诱导面板UI

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `model` | `RouteMessageModel` | 路段的model |

#### Returns

`void`

___

### updateRemainInfo

▸ **updateRemainInfo**(`remainInfo`, `arriveTime`): `void`

更新剩余信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `remainInfo` | `string` | 剩余信息 |
| `arriveTime` | `string` |  |

#### Returns

`void`

___

### getSingleLineText

▸ **getSingleLineText**(`singleLineText`, `scaleValue`): `MutableStyledString`

单行文案
加粗 + 变大

#### Parameters

| Name | Type |
| :------ | :------ |
| `singleLineText` | `string` |
| `scaleValue` | `number` |

#### Returns

`MutableStyledString`

___

### getNormalText

▸ **getNormalText**(`normal`, `scaleValue`): `MutableStyledString`

普通双行文案

#### Parameters

| Name | Type |
| :------ | :------ |
| `normal` | `string` |
| `scaleValue` | `number` |

#### Returns

`MutableStyledString`

___

### guideTextStyleScale

▸ **guideTextStyleScale**(`guideLineText`, `singleLine`, `scaleValue`): `MutableStyledString`

文案样式修改

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `guideLineText` | [`GuideLineText`](walkridecommon.GuideLineText.md) | 原始文案 |
| `singleLine` | `boolean` | 是否单行 |
| `scaleValue` | `number` | 缩放值 |

#### Returns

`MutableStyledString`

增加了样式的文案
