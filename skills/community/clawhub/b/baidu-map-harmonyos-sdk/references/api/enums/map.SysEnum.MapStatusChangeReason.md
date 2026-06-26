[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / [SysEnum](../modules/map.SysEnum.md) / MapStatusChangeReason

# Enumeration: MapStatusChangeReason

[map](../modules/map.md).[SysEnum](../modules/map.SysEnum.md).MapStatusChangeReason

地图状态改变的原因

**`Since`**

1.2.1

## Table of contents

### Enumeration Members

- [UN\_KNOW](map.SysEnum.MapStatusChangeReason.md#un_know)
- [REASON\_GESTURE](map.SysEnum.MapStatusChangeReason.md#reason_gesture)
- [REASON\_TOUCH](map.SysEnum.MapStatusChangeReason.md#reason_touch)
- [REASON\_DEVELOPER](map.SysEnum.MapStatusChangeReason.md#reason_developer)

## Enumeration Members

### UN\_KNOW

• **UN\_KNOW** = ``0``

___

### REASON\_GESTURE

• **REASON\_GESTURE** = ``1``

用户手势触发导致的地图状态改变,比如双击、拖拽、滑动底图

___

### REASON\_TOUCH

• **REASON\_TOUCH** = ``2``

用户触发点击导致的地图状态改变, 比如点击定位控件、缩放控件、指南针图标

___

### REASON\_DEVELOPER

• **REASON\_DEVELOPER** = ``3``

开发者调用API方法,导致的地图状态改变
