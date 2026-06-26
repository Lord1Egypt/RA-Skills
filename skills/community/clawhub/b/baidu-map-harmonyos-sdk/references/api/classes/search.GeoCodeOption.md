[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / GeoCodeOption

# Class: GeoCodeOption

[search](../modules/search.md).GeoCodeOption

地理编码请求参数
正向地理编码服务提供将结构化地址数据（如：北京市海淀区上地十街十号）转换为对应坐标点（经纬度）功能；
地址结构越完整，地址内容越准确，解析的坐标精度越高。
地理编码服务当前未推出国际化服务，解析地址仅限国内

## Table of contents

### Constructors

- [constructor](search.GeoCodeOption.md#constructor)

### Accessors

- [city](search.GeoCodeOption.md#city)
- [address](search.GeoCodeOption.md#address)

## Constructors

### constructor

• **new GeoCodeOption**(`city`, `address`): [`GeoCodeOption`](search.GeoCodeOption.md)

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `city` | `string` | 地址所在的城市名 必须参数 用于指定上述地址所在的城市，当多个城市都有上述地址时，该参数起到过滤作用，但不限制坐标召回城市 |
| `address` | `string` | 待解析的地址。最多支持84个字节。 必须参数 可以输入2种样式的值，分别是： 1、标准的结构化地址信息，如北京市海淀区上地十街十号，推荐，地址结构越完整，解析精度越高） 2、支持“*路与*路交叉口”描述方式，如北一环路和阜阳路的交叉路口 第二种方式并不总是有返回结果，只有当地址库中存在该地址描述时才有返回。 |

#### Returns

[`GeoCodeOption`](search.GeoCodeOption.md)

## Accessors

### city

• `get` **city**(): `string`

#### Returns

`string`

• `set` **city**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

`void`

___

### address

• `get` **address**(): `string`

#### Returns

`string`

• `set` **address**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

`void`
