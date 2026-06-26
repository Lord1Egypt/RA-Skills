[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / AddressComponent

# Interface: AddressComponent

[search](../modules/search.md).AddressComponent

此类表示地址解析结果的层次化地址信息。

## Table of contents

### Properties

- [streetNumber](search.AddressComponent.md#streetnumber)
- [street](search.AddressComponent.md#street)
- [town](search.AddressComponent.md#town)
- [district](search.AddressComponent.md#district)
- [city](search.AddressComponent.md#city)
- [province](search.AddressComponent.md#province)
- [countryName](search.AddressComponent.md#countryname)
- [countryCode](search.AddressComponent.md#countrycode)
- [adcode](search.AddressComponent.md#adcode)
- [direction](search.AddressComponent.md#direction)
- [distance](search.AddressComponent.md#distance)
- [countryCodeIso](search.AddressComponent.md#countrycodeiso)
- [countryCodeIso2](search.AddressComponent.md#countrycodeiso2)
- [townCode](search.AddressComponent.md#towncode)
- [cityLevel](search.AddressComponent.md#citylevel)

## Properties

### streetNumber

• `Optional` **streetNumber**: `string`

门牌号码

___

### street

• `Optional` **street**: `string`

街道名称（行政区划中的街道层级）

___

### town

• `Optional` **town**: `string`

乡镇名称

___

### district

• `Optional` **district**: `string`

区县名称

___

### city

• `Optional` **city**: `string`

城市名称

___

### province

• `Optional` **province**: `string`

省份名称

___

### countryName

• `Optional` **countryName**: `string`

国家名称

___

### countryCode

• `Optional` **countryCode**: `number`

国家号码

___

### adcode

• `Optional` **adcode**: `number`

行政区域编码
http://mapopen-pub-webserviceapi.bj.bcebos.com/geocoding/%E5%8C%BA%E5%8E%BF%E7%BA%A7%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92%E6%B8%85%E5%8D%95V35.xlsx

___

### direction

• `Optional` **direction**: `string`

相对当前坐标点的方向，当有门牌号的时候返回数据

___

### distance

• `Optional` **distance**: `number`

相对当前坐标点的距离，当有门牌号的时候返回数据

___

### countryCodeIso

• `Optional` **countryCodeIso**: `string`

国家英文缩写（三位）

___

### countryCodeIso2

• `Optional` **countryCodeIso2**: `string`

国家英文缩写（两位）

___

### townCode

• `Optional` **townCode**: `string`

乡镇id

___

### cityLevel

• `Optional` **cityLevel**: `number`

城市所在级别（仅国外有参考意义。国外行政区划与中国有差异，
城市对应的层级不一定为『city』。country、province、city、district、town分别对应0-4级，
若city_level=3，则district层级为该国家的city层级）
