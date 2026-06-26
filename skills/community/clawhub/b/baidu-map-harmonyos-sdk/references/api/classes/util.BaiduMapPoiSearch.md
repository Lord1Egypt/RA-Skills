[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / BaiduMapPoiSearch

# Class: BaiduMapPoiSearch

[util](../modules/util.md).BaiduMapPoiSearch

SDK调起百度地图APP  POi相关功能

**`Author`**

v_wangfujun

## Table of contents

### Constructors

- [constructor](util.BaiduMapPoiSearch.md#constructor)

### Methods

- [getInstance](util.BaiduMapPoiSearch.md#getinstance)
- [openBaiduMapPoiDetialsPage](util.BaiduMapPoiSearch.md#openbaidumappoidetialspage)
- [openBaiduMapPoiNearbySearch](util.BaiduMapPoiSearch.md#openbaidumappoinearbysearch)

## Constructors

### constructor

• **new BaiduMapPoiSearch**(): [`BaiduMapPoiSearch`](util.BaiduMapPoiSearch.md)

#### Returns

[`BaiduMapPoiSearch`](util.BaiduMapPoiSearch.md)

## Methods

### getInstance

▸ **getInstance**(): [`BaiduMapPoiSearch`](util.BaiduMapPoiSearch.md)

#### Returns

[`BaiduMapPoiSearch`](util.BaiduMapPoiSearch.md)

___

### openBaiduMapPoiDetialsPage

▸ **openBaiduMapPoiDetialsPage**(`para`, `context`): `boolean`

SDK调起百度地图APP Poi详情页功能

#### Parameters

| Name | Type |
| :------ | :------ |
| `para` | [`PoiDetailPageParamModel`](util.PoiDetailPageParamModel.md) |
| `context` | `UIAbilityContext` |

#### Returns

`boolean`

**`Author`**

v_wangfujun

___

### openBaiduMapPoiNearbySearch

▸ **openBaiduMapPoiNearbySearch**(`para`, `context`): `boolean`

SDK调起百度地图APP Poi列表页功能

#### Parameters

| Name | Type |
| :------ | :------ |
| `para` | [`PoiSearchPageParamModel`](util.PoiSearchPageParamModel.md) |
| `context` | `UIAbilityContext` |

#### Returns

`boolean`

**`Author`**

v_wangfujun
