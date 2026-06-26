[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / MapLanguageStorageManager

# Class: MapLanguageStorageManager

[base](../modules/base.md).MapLanguageStorageManager

地图语言存储管理器单例类
提供统一的地图语言存储服务入口

## Table of contents

### Methods

- [getInstance](base.MapLanguageStorageManager.md#getinstance)
- [init](base.MapLanguageStorageManager.md#init)
- [isReady](base.MapLanguageStorageManager.md#isready)
- [setLanguage](base.MapLanguageStorageManager.md#setlanguage)
- [getLanguage](base.MapLanguageStorageManager.md#getlanguage)
- [clearLanguage](base.MapLanguageStorageManager.md#clearlanguage)
- [addLanguageChangeListener](base.MapLanguageStorageManager.md#addlanguagechangelistener)
- [removeLanguageChangeListener](base.MapLanguageStorageManager.md#removelanguagechangelistener)
- [reset](base.MapLanguageStorageManager.md#reset)

## Methods

### getInstance

▸ **getInstance**(): [`MapLanguageStorageManager`](base.MapLanguageStorageManager.md)

获取单例实例

#### Returns

[`MapLanguageStorageManager`](base.MapLanguageStorageManager.md)

MapLanguageStorageManager的单例实例

___

### init

▸ **init**(`context?`, `storageName?`): `boolean`

初始化语言存储服务

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `context` | `any` | `null` | 应用上下文，如果为null则使用getAppContext() |
| `storageName` | `string` | `STORAGE_NAME` | 存储名称，默认为"map_language_storage" |

#### Returns

`boolean`

是否初始化成功

___

### isReady

▸ **isReady**(): `boolean`

检查是否已初始化

#### Returns

`boolean`

如果已初始化返回true，否则返回false

___

### setLanguage

▸ **setLanguage**(`language`): `void`

设置地图语言

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `language` | `MapLanguage` | 目标语言 |

#### Returns

`void`

**`Throws`**

LanguageChangeException 当语言设置失败时抛出

___

### getLanguage

▸ **getLanguage**(): `MapLanguage`

获取当前地图语言

#### Returns

`MapLanguage`

当前设置的语言，默认返回中文

___

### clearLanguage

▸ **clearLanguage**(): `void`

清除语言设置，恢复默认值

#### Returns

`void`

___

### addLanguageChangeListener

▸ **addLanguageChangeListener**(`listener`): `void`

添加语言变更监听器

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `listener` | [`LanguageChangeListener`](../interfaces/base.LanguageChangeListener.md) | 监听器 |

#### Returns

`void`

___

### removeLanguageChangeListener

▸ **removeLanguageChangeListener**(`listener`): `void`

移除语言变更监听器

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `listener` | [`LanguageChangeListener`](../interfaces/base.LanguageChangeListener.md) | 监听器 |

#### Returns

`void`

___

### reset

▸ **reset**(): `void`

重置管理器（用于测试或重新初始化）

#### Returns

`void`
