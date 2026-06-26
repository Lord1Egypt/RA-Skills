[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PlanNode

# Class: PlanNode

[search](../modules/search.md).PlanNode

路径规划中的出行节点信息,出行节点包括：起点，终点，途经点
<p>
出行节点信息可以通过两种方式确定：
</p>
<p>
1： 给定出行节点经纬度坐标, 添加poiID绑路更准确
</p>
<p>
2： 给定出行节点地名和城市名, 添加poiID绑路更准确
</p>

## Table of contents

### Constructors

- [constructor](search.PlanNode.md#constructor)

### Accessors

- [location](search.PlanNode.md#location)
- [city](search.PlanNode.md#city)
- [cityCode](search.PlanNode.md#citycode)
- [cityName](search.PlanNode.md#cityname)
- [name](search.PlanNode.md#name)
- [poiId](search.PlanNode.md#poiid)

### Methods

- [withLocation](search.PlanNode.md#withlocation)
- [withLocationAndPoiId](search.PlanNode.md#withlocationandpoiid)
- [withCityNameAndPlaceName](search.PlanNode.md#withcitynameandplacename)
- [withCityNameAndPlaceNameAndPoiId](search.PlanNode.md#withcitynameandplacenameandpoiid)
- [withCityCodeAndPlaceName](search.PlanNode.md#withcitycodeandplacename)
- [withCityCodeAndPlaceNameAndPoiId](search.PlanNode.md#withcitycodeandplacenameandpoiid)

## Constructors

### constructor

• **new PlanNode**(`params`): [`PlanNode`](search.PlanNode.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `params` | [`PlanNodeParams`](../interfaces/search.PlanNodeParams.md) |

#### Returns

[`PlanNode`](search.PlanNode.md)

## Accessors

### location

• `get` **location**(): ``null`` \| [`LatLng`](base.LatLng.md)

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

___

### city

• `get` **city**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### cityCode

• `get` **cityCode**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### cityName

• `get` **cityName**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### name

• `get` **name**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

___

### poiId

• `get` **poiId**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

## Methods

### withLocation

▸ **withLocation**(`location`): [`PlanNode`](search.PlanNode.md)

通过指定经纬度确定出行节点信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `location` | [`LatLng`](base.LatLng.md) | 经纬度 |

#### Returns

[`PlanNode`](search.PlanNode.md)

出行节点对象

___

### withLocationAndPoiId

▸ **withLocationAndPoiId**(`location`, `poiId`): [`PlanNode`](search.PlanNode.md)

通过指定经纬度坐标和poiId确定出行节点信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `location` | [`LatLng`](base.LatLng.md) | 经纬度 |
| `poiId` | `string` | poiId |

#### Returns

[`PlanNode`](search.PlanNode.md)

出行节点信息

___

### withCityNameAndPlaceName

▸ **withCityNameAndPlaceName**(`city`, `placeName`): [`PlanNode`](search.PlanNode.md)

通过地名和城市名确定出行节点信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `city` | `string` | 城市名 |
| `placeName` | `string` | 地点名 |

#### Returns

[`PlanNode`](search.PlanNode.md)

出行节点对象

___

### withCityNameAndPlaceNameAndPoiId

▸ **withCityNameAndPlaceNameAndPoiId**(`city`, `placeName`, `poiId`): [`PlanNode`](search.PlanNode.md)

通过地名和城市名和poiId确定出行节点信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `city` | `string` | 城市名 |
| `placeName` | `string` | 地点名 |
| `poiId` | `string` |  |

#### Returns

[`PlanNode`](search.PlanNode.md)

出行节点对象

___

### withCityCodeAndPlaceName

▸ **withCityCodeAndPlaceName**(`cityCode`, `placeName`): [`PlanNode`](search.PlanNode.md)

通过地名和城市编码确定出行节点信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityCode` | `number` | 城市ID |
| `placeName` | `string` | 地点名 |

#### Returns

[`PlanNode`](search.PlanNode.md)

出行节点对象

___

### withCityCodeAndPlaceNameAndPoiId

▸ **withCityCodeAndPlaceNameAndPoiId**(`cityCode`, `placeName`, `poiId`): [`PlanNode`](search.PlanNode.md)

通过地名和城市编码和PoiId确定出行节点信息

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityCode` | `number` | 城市ID |
| `placeName` | `string` | 地点名 |
| `poiId` | `string` |  |

#### Returns

[`PlanNode`](search.PlanNode.md)

出行节点对象
