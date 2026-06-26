[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / OverlayLayer

# Class: OverlayLayer

[map](../modules/map.md).OverlayLayer

覆盖物图层

**`Abstract`**

由地图内部创建生成，提供覆盖物图层操作方法

**`Since`**

1.0.0

**`Author`**

dongshuifeng

**`Package`**

@bdmap/map

## Hierarchy

- `default`

  ↳ **`OverlayLayer`**

## Table of contents

### Accessors

- [visible](map.OverlayLayer.md#visible)

### Methods

- [setName](map.OverlayLayer.md#setname)
- [getName](map.OverlayLayer.md#getname)
- [getLayerId](map.OverlayLayer.md#getlayerid)
- [update](map.OverlayLayer.md#update)
- [setData](map.OverlayLayer.md#setdata)
- [getData](map.OverlayLayer.md#getdata)
- [addOverlay](map.OverlayLayer.md#addoverlay)
- [removeOverlay](map.OverlayLayer.md#removeoverlay)
- [removeOverlays](map.OverlayLayer.md#removeoverlays)
- [getOverlays](map.OverlayLayer.md#getoverlays)
- [layerCommit](map.OverlayLayer.md#layercommit)
- [getCommitStatus](map.OverlayLayer.md#getcommitstatus)
- [pauseCommit](map.OverlayLayer.md#pausecommit)
- [resumeCommit](map.OverlayLayer.md#resumecommit)
- [setVisible](map.OverlayLayer.md#setvisible)
- [clear](map.OverlayLayer.md#clear)
- [hasOverlay](map.OverlayLayer.md#hasoverlay)
- [destroy](map.OverlayLayer.md#destroy)

## Accessors

### visible

• `get` **visible**(): `boolean`

获取图层当前状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseLayer.visible

• `set` **visible**(`val`): `void`

设置图层当前状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseLayer.visible

## Methods

### setName

▸ **setName**(`name`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `name` | `string` |

#### Returns

`void`

#### Inherited from

BaseLayer.setName

___

### getName

▸ **getName**(): `string`

#### Returns

`string`

#### Inherited from

BaseLayer.getName

___

### getLayerId

▸ **getLayerId**(): `number`

#### Returns

`number`

#### Inherited from

BaseLayer.getLayerId

___

### update

▸ **update**(): `void`

主动调用绘制一次图层数据

#### Returns

`void`

#### Inherited from

BaseLayer.update

___

### setData

▸ **setData**(`strJson`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `strJson` | `string` |

#### Returns

`void`

#### Inherited from

BaseLayer.setData

___

### getData

▸ **getData**(): `string`

#### Returns

`string`

#### Inherited from

BaseLayer.getData

___

### addOverlay

▸ **addOverlay**(`o`): `Promise`\<`void`\>

添加地图覆盖物，如果有使用到自定义的图片资源，需要使用await来调用，否则会引起后续状态混乱

#### Parameters

| Name | Type |
| :------ | :------ |
| `o` | [`Overlay`](map.Overlay.md) |

#### Returns

`Promise`\<`void`\>

**`Since`**

1.0.0

___

### removeOverlay

▸ **removeOverlay**(`overlay`, `noCommit?`): `void`

移除地图覆盖物

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `overlay` | [`Overlay`](map.Overlay.md) | 覆盖物对象 |
| `noCommit?` | `boolean` | - |

#### Returns

`void`

**`Since`**

1.0.0

___

### removeOverlays

▸ **removeOverlays**(`type?`): `void`

按类型移除地图覆盖物

#### Parameters

| Name | Type |
| :------ | :------ |
| `type?` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getOverlays

▸ **getOverlays**(`type?`): [`Overlay`](map.Overlay.md)[]

获取图层覆盖物集合

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type?` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) | 指定覆盖物 |

#### Returns

[`Overlay`](map.Overlay.md)[]

**`Since`**

2.0.3

___

### layerCommit

▸ **layerCommit**(): `void`

更新图层数据渲染

#### Returns

`void`

**`Since`**

1.2.3

___

### getCommitStatus

▸ **getCommitStatus**(): `boolean`

获取可主动更新数据渲染的状态

#### Returns

`boolean`

**`Since`**

1.2.3

___

### pauseCommit

▸ **pauseCommit**(): `void`

暂停主动提交数据渲染更新的状态

#### Returns

`void`

**`Since`**

1.2.3

___

### resumeCommit

▸ **resumeCommit**(): `void`

恢复主动提交数据渲染更新的状态，并主动触发一次layerCommit

#### Returns

`void`

**`Since`**

1.2.3

___

### setVisible

▸ **setVisible**(`visible`): `void`

设置图层当前状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `visible` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Overrides

BaseLayer.setVisible

___

### clear

▸ **clear**(`model?`, `o?`, `noUpdate?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model?` | [`OverlayType`](../enums/map.SysEnum.OverlayType.md) |
| `o?` | [`Overlay`](map.Overlay.md) |
| `noUpdate?` | `boolean` |

#### Returns

`void`

#### Overrides

BaseLayer.clear

___

### hasOverlay

▸ **hasOverlay**(`o`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `o` | [`Overlay`](map.Overlay.md) |

#### Returns

`boolean`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`
