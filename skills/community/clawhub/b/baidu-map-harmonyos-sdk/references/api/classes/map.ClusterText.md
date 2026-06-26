[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ClusterText

# Class: ClusterText

[map](../modules/map.md).ClusterText

点聚合Icon

## Table of contents

### Constructors

- [constructor](map.ClusterText.md#constructor)

### Methods

- [build](map.ClusterText.md#build)
- [getIdentifier](map.ClusterText.md#getidentifier)

## Constructors

### constructor

• **new ClusterText**(`id`): [`ClusterText`](map.ClusterText.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `number` |

#### Returns

[`ClusterText`](map.ClusterText.md)

## Methods

### build

▸ **build**(`text`, `textStyle`, `located?`): `boolean`

构建文本配置

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `text` | `string` | `undefined` | 文本内容 |
| `textStyle` | [`TextStyle`](map.TextStyle.md) | `undefined` | 文本样式 |
| `located` | [`Located`](../enums/map.SysEnum.Located.md) | `Located.CENTER` | 位置 |

#### Returns

`boolean`

构建是否成功

___

### getIdentifier

▸ **getIdentifier**(): `number`

Identifier

#### Returns

`number`
