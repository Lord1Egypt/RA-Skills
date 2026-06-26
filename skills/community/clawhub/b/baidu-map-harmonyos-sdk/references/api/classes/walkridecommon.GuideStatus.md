[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / GuideStatus

# Class: GuideStatus

[walkridecommon](../modules/walkridecommon.md).GuideStatus

导航状态，MSG_NAVI_STATUS_CHANGE消息中会用到
对应navi_engine_guidance_def.h中的NE_Guide_SubStatus_Enum

## Table of contents

### Constructors

- [constructor](walkridecommon.GuideStatus.md#constructor)

### Properties

- [GUIDE\_START](walkridecommon.GuideStatus.md#guide_start)
- [FARAWAY](walkridecommon.GuideStatus.md#faraway)
- [YAWING](walkridecommon.GuideStatus.md#yawing)
- [REPLAN\_OK](walkridecommon.GuideStatus.md#replan_ok)
- [ARRIVE\_DEST](walkridecommon.GuideStatus.md#arrive_dest)
- [INDOOR\_END](walkridecommon.GuideStatus.md#indoor_end)
- [FINAL\_END](walkridecommon.GuideStatus.md#final_end)
- [ARRIVE\_DEST\_NEAR](walkridecommon.GuideStatus.md#arrive_dest_near)
- [REPLAN\_FAIL](walkridecommon.GuideStatus.md#replan_fail)

## Constructors

### constructor

• **new GuideStatus**(): [`GuideStatus`](walkridecommon.GuideStatus.md)

#### Returns

[`GuideStatus`](walkridecommon.GuideStatus.md)

## Properties

### GUIDE\_START

▪ `Static` `Readonly` **GUIDE\_START**: ``1``

开始导航

___

### FARAWAY

▪ `Static` `Readonly` **FARAWAY**: ``2``

偏离路线

___

### YAWING

▪ `Static` `Readonly` **YAWING**: ``3``

偏航中

___

### REPLAN\_OK

▪ `Static` `Readonly` **REPLAN\_OK**: ``4``

路线计算完成

___

### ARRIVE\_DEST

▪ `Static` `Readonly` **ARRIVE\_DEST**: ``5``

到达目的地

___

### INDOOR\_END

▪ `Static` `Readonly` **INDOOR\_END**: ``6``

室内目的地到达

___

### FINAL\_END

▪ `Static` `Readonly` **FINAL\_END**: ``7``

到达最终目的地

___

### ARRIVE\_DEST\_NEAR

▪ `Static` `Readonly` **ARRIVE\_DEST\_NEAR**: ``8``

到达目的地附近

___

### REPLAN\_FAIL

▪ `Static` `Readonly` **REPLAN\_FAIL**: ``10``

偏航规划失败 引擎没有该字段
