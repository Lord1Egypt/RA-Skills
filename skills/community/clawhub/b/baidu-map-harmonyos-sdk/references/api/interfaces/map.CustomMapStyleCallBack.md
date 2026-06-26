[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / CustomMapStyleCallBack

# Interface: CustomMapStyleCallBack

[map](../modules/map.md).CustomMapStyleCallBack

设置在线个性化地图回调，返回值为true代表用户处理

**`Since`**

2.0.0

## Table of contents

### Methods

- [onPreLoadLastCustomMapStyle](map.CustomMapStyleCallBack.md#onpreloadlastcustommapstyle)
- [onCustomMapStyleLoadSuccess](map.CustomMapStyleCallBack.md#oncustommapstyleloadsuccess)
- [onCustomMapStyleLoadFailed](map.CustomMapStyleCallBack.md#oncustommapstyleloadfailed)

## Methods

### onPreLoadLastCustomMapStyle

▸ **onPreLoadLastCustomMapStyle**(`customStylePath`): `boolean`

预加载最新一次请求到的在线个性化样式。注：当开发者收到该回调时，本地缓存的最新一次请求到的在线个性化样式还没有更新到地图上。

1、开发者可以使用默认返回值false，由SDK内部实现样式本地缓存的个性化样式预加载逻辑，开发者无需做任何处理。
2、开发者也可以在该回调中根据返回的个性化样式文件路径，结合MapView#setMapCustomStylePath(String)、
1、开发者返回false，由SDK内部实现样式加载失败的逻辑，开发者无需做任何处理。
2、开发者也可以在该回调中根据返回的个性化样式文件路径及请求状态，
结合{Mapcontroller.setCustomStylePath(String)}、
{Mapcontroller.setCustomStyleEnable(boolean)}两个接口自行实现样式加载失败的逻辑，并将返回值置为true。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `customStylePath` | ``null`` \| `string` | 本地缓存的最新一次请求到的在线个性化样式文件路径 |

#### Returns

`boolean`

返回true:表示这部分逻辑由开发者处理，SDK不做任何处理，即本地缓存的个性化样式预加载逻辑需要开发者自行实现；
返回false:默认走SDK内部处理逻辑

___

### onCustomMapStyleLoadSuccess

▸ **onCustomMapStyleLoadSuccess**(`hasUpdate`, `customStylePath`): `boolean`

在线个性化样式加载成功回调。注：当开发者收到该回调时，新的在线个性化样式还没有更新到地图上。

1、开发者返回false，由SDK内部实现样式加载失败的逻辑，开发者无需做任何处理。
2、开发者也可以在该回调中根据返回的个性化样式文件路径及请求状态，
结合{Mapcontroller.setCustomStylePath(String)}、
{Mapcontroller.setCustomStyleEnable(boolean)}两个接口自行实现样式加载失败的逻辑，并将返回值置为true。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `hasUpdate` | `boolean` | 当前请求的在线个性化样式相比本地缓存的最新在线个性化样式是否有更新，true:有更新；false:没有更新 |
| `customStylePath` | ``null`` \| `string` | 当前请求到的在线个性化样式文件路径 |

#### Returns

`boolean`

返回true:表示这部分逻辑由开发者处理,SDK不做任何处理,即新的样式更新需要开发者自行实现；
        返回false:默认走SDK内部处理逻辑

___

### onCustomMapStyleLoadFailed

▸ **onCustomMapStyleLoadFailed**(`status`, `message`, `customStylePath`): `boolean`

在线个性化样式加载失败回调。注：当开发者收到该回调时，SDK还没有尝试将本地缓存的个性化样式文件更新到地图上。

1、开发者返回false，由SDK内部实现样式加载失败的逻辑，开发者无需做任何处理。
2、开发者也可以在该回调中根据返回的个性化样式文件路径及请求状态，
结合{Mapcontroller.setCustomStylePath(String)}、
{Mapcontroller.setCustomStyleEnable(boolean)}两个接口自行实现样式加载失败的逻辑，并将返回值置为true。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `status` | `number` | 加载失败状态码 |
| `message` | `string` | 加载失败信息描述 |
| `customStylePath` | ``null`` \| `string` | 本地缓存的最新一次请求到的在线个性化样式文件路径 |

#### Returns

`boolean`

返回true:表示这部分逻辑由开发者处理，SDK不做任何处理，即样式加载失败的逻辑需要开发者自行实现；
        返回false:默认走SDK内部处理逻辑
