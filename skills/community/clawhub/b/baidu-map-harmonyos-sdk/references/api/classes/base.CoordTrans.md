[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / CoordTrans

# Class: CoordTrans

[base](../modules/base.md).CoordTrans

经纬度坐标系转换工具类

## Table of contents

### Constructors

- [constructor](base.CoordTrans.md#constructor)

### Methods

- [baiduToGcj](base.CoordTrans.md#baidutogcj)
- [wgsToGcj](base.CoordTrans.md#wgstogcj)
- [gcjToBaidu](base.CoordTrans.md#gcjtobaidu)
- [wgsToBaidu](base.CoordTrans.md#wgstobaidu)

## Constructors

### constructor

• **new CoordTrans**(): [`CoordTrans`](base.CoordTrans.md)

#### Returns

[`CoordTrans`](base.CoordTrans.md)

## Methods

### baiduToGcj

▸ **baiduToGcj**(`latLng`): ``null`` \| [`LatLng`](base.LatLng.md)

百度转国测局

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | 百度经纬度 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

若转换成功，返回国测局经纬度；否则，返回null。

___

### wgsToGcj

▸ **wgsToGcj**(`latLng`): ``null`` \| [`LatLng`](base.LatLng.md)

wgs84转国测局

#### Parameters

| Name | Type |
| :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

___

### gcjToBaidu

▸ **gcjToBaidu**(`latLng`): ``null`` \| [`LatLng`](base.LatLng.md)

国测局转百度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `latLng` | ``null`` \| [`LatLng`](base.LatLng.md) | 国测局经纬度 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

若转换成功，返回百度经纬度；否则，返回null。

___

### wgsToBaidu

▸ **wgsToBaidu**(`latLng`): ``null`` \| [`LatLng`](base.LatLng.md)

wgs84转百度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | WGS84经纬度 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

若转换成功，返回百度经纬度；否则，返回null。
