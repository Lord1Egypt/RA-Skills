# 坐标转换与坐标系

## 坐标系类型

- **WGS84**：GPS 常用大地坐标系。
- **GCJ02**：国测局坐标系，由 WGS84 加密。
- **BD09**：百度坐标系，在 GCJ02 上再次加密。BD09LL 为百度经纬度，BD09MC 为百度墨卡托米制。
- 国内（含港澳台）：地图 SDK 默认输入输出 BD09LL；可全局声明为 GCJ02，则全应用输入/输出为 GCJ02。海外统一 WGS84。
- 定位 SDK 默认输出 GCJ02；与地图混用时需统一，通常地图设为 BD09LL 且定位设置 `setCoorType("bd09ll")`，或地图设为 GCJ02。

## 全局坐标类型（自 4.3.0）

- `SDKInitializer.setCoordType(CoordType.BD09LL);` 或 `CoordType.GCJ02;` 声明全局类型。
- `SDKInitializer.getCoordType();` 获取当前类型。
- 自动转换仅适用于国内 GCJ02 输入；海外用 WGS84 无需转换。

## 通用坐标转换（CoordinateConverter）

- 将 WGS84/GCJ02 等转为 BD09LL（或当前声明的类型），需使用 SDK 提供的 CoordinateConverter，勿用非官方算法。
- 示例（其它坐标系 → 百度经纬度）：
  - 高德/腾讯等（COMMON）：`CoordinateConverter().from(CoordType.COMMON).coord(sourceLatLng).convert();`
  - GPS 设备原始坐标：`CoordinateConverter().from(CoordinateConverter.CoordType.GPS).coord(sourceLatLng).convert();`
- BD09MC → BD09LL：`from(CoordType.BD09MC).coord(sourceLatLng).convert();`
- 返回 `LatLng desLatLng = converter.convert();`

## 注意事项

- 国内非 BD09LL 坐标需先转为 BD09LL 再叠加到百度地图，否则会偏移。
- 海外 POI 使用 WGS84，地图海外也为 WGS84，无需转换。同时使用国内外数据时，自动坐标转换方式不适用，需手动按场景转换。
