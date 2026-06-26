[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IMapClickListener

# Interface: IMapClickListener

[map](../modules/map.md).IMapClickListener

## Table of contents

### Methods

- [onClickedMapObj](map.IMapClickListener.md#onclickedmapobj)
- [onClickedBackground](map.IMapClickListener.md#onclickedbackground)

## Methods

### onClickedMapObj

▸ **onClickedMapObj**(`arrClickObjs`): `void`

一般情况下的点击回调（一般的 poi 点、指南针、反 geo 等）

#### Parameters

| Name | Type |
| :------ | :------ |
| `arrClickObjs` | [`MapClickObj`](../classes/map.MapClickObj.md)[] |

#### Returns

`void`

___

### onClickedBackground

▸ **onClickedBackground**(`x`, `y`): `void`

点击到底图空白区域，没有点到任何可点对象

#### Parameters

| Name | Type |
| :------ | :------ |
| `x` | `number` |
| `y` | `number` |

#### Returns

`void`
