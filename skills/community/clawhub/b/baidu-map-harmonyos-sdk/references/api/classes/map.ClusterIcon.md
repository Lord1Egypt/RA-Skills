[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ClusterIcon

# Class: ClusterIcon

[map](../modules/map.md).ClusterIcon

点聚合Icon

## Table of contents

### Constructors

- [constructor](map.ClusterIcon.md#constructor)

### Methods

- [build](map.ClusterIcon.md#build)
- [getIdentifier](map.ClusterIcon.md#getidentifier)

## Constructors

### constructor

• **new ClusterIcon**(`id`): [`ClusterIcon`](map.ClusterIcon.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `number` |

#### Returns

[`ClusterIcon`](map.ClusterIcon.md)

## Methods

### build

▸ **build**(`resource?`, `located?`): `Promise`\<`boolean`\>

构建图标配置

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `resource?` | [`ImageEntity`](map.ImageEntity.md) | `undefined` | 图标资源 |
| `located` | [`Located`](../enums/map.SysEnum.Located.md) | `Located.CENTER` | 位置 |

#### Returns

`Promise`\<`boolean`\>

构建是否成功

___

### getIdentifier

▸ **getIdentifier**(): `number`

Identifier

#### Returns

`number`
