[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / [SysEnum](../modules/map.SysEnum.md) / CollisionBehavior

# Enumeration: CollisionBehavior

[map](../modules/map.md).[SysEnum](../modules/map.SysEnum.md).CollisionBehavior

## Table of contents

### Enumeration Members

- [NOT\_COLLIDE](map.SysEnum.CollisionBehavior.md#not_collide)
- [ALWAYS\_SHOW](map.SysEnum.CollisionBehavior.md#always_show)
- [HIDE\_BY\_PRIORITY](map.SysEnum.CollisionBehavior.md#hide_by_priority)
- [COLLIDE\_WITH\_INNER](map.SysEnum.CollisionBehavior.md#collide_with_inner)
- [COLLIDE\_WITH\_BASEPOI](map.SysEnum.CollisionBehavior.md#collide_with_basepoi)
- [COLLIDE\_INNER\_AND\_BASEPOI](map.SysEnum.CollisionBehavior.md#collide_inner_and_basepoi)
- [INNER\_AND\_BASEPOI](map.SysEnum.CollisionBehavior.md#inner_and_basepoi)
- [DODGE\_WITH\_INNER](map.SysEnum.CollisionBehavior.md#dodge_with_inner)
- [COLLIDE\_WITH\_ALL\_LAYERS](map.SysEnum.CollisionBehavior.md#collide_with_all_layers)

## Enumeration Members

### NOT\_COLLIDE

• **NOT\_COLLIDE** = ``0``

**`Default`**

```ts
不参与碰撞
```

**`Since`**

1.1.0

___

### ALWAYS\_SHOW

• **ALWAYS\_SHOW** = ``1``

参与碰撞，但强制显示

**`Since`**

1.1.0

___

### HIDE\_BY\_PRIORITY

• **HIDE\_BY\_PRIORITY** = ``2``

参与碰撞，根据碰撞优先级决定是否显示

**`Since`**

1.1.0

___

### COLLIDE\_WITH\_INNER

• **COLLIDE\_WITH\_INNER** = ``4``

图层内部的点碰撞

**`Since`**

1.1.0

___

### COLLIDE\_WITH\_BASEPOI

• **COLLIDE\_WITH\_BASEPOI** = ``8``

图层与底图的POI进行碰撞，碰掉底图的POI

**`Since`**

1.1.0

___

### COLLIDE\_INNER\_AND\_BASEPOI

• **COLLIDE\_INNER\_AND\_BASEPOI** = ``12``

图层内部点先碰撞，再与底图的POI进行碰撞，碰掉底图的POI

**`Since`**

1.1.0

___

### INNER\_AND\_BASEPOI

• **INNER\_AND\_BASEPOI** = ``12``

___

### DODGE\_WITH\_INNER

• **DODGE\_WITH\_INNER** = ``16``

图层内部点避让

**`Since`**

1.1.0

___

### COLLIDE\_WITH\_ALL\_LAYERS

• **COLLIDE\_WITH\_ALL\_LAYERS** = ``512``

所有图层都碰撞，按优先级碰

**`Since`**

1.1.0
