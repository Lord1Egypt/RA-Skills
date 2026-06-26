# 显示定位

## 坐标系说明

- 定位 SDK 支持国内输出：国测局坐标、百度墨卡托、百度经纬度；海外仅 WGS84。定位 SDK 默认输出 GCJ02，地图 SDK 默认 BD09LL；混用时需统一，见 [coordinate.md](coordinate.md)。

## 前置条件

- 开发包需包含定位能力（下载 SDK 时勾选基本定位）。
- AndroidManifest：声明定位相关权限；在 `<application>` 内声明定位 Service 组件。

## 开启定位图层与传数据

1. 开启：`mBaiduMap.setMyLocationEnabled(true)`。
2. 继承 `BDAbstractLocationListener`，在 `onReceiveLocation(BDLocation location)` 中构造 `MyLocationData` 并传给地图：
   - `MyLocationData.Builder().accuracy(radius).direction(direction).latitude(lat).longitude(lng).build()`
   - `mBaiduMap.setMyLocationData(locData)`。
3. 使用 `LocationClient`：`LocationClient option = new LocationClient(context)`，`LocationClientOption` 设置 `setOpenGps`、`setCoorType("bd09ll")`、`setScanSpan` 等，`setLocOption(option)`，`registerLocationListener(myLocationListener)`，`start()`。
4. 生命周期：在 `onDestroy` 中 `mLocationClient.stop()`、`mBaiduMap.setMyLocationEnabled(false)`，再执行 MapView 的 `onDestroy()`。

## MyLocationConfiguration（自定义样式）

构造：`MyLocationConfiguration(LocationMode mode, boolean enableDirection, BitmapDescriptor customMarker, int accuracyCircleFillColor, int accuracyCircleStrokeColor)`。

- **定位模式**：`LocationMode.NORMAL`（普通）、`LocationMode.FOLLOWING`（跟随）、`LocationMode.COMPASS`（罗盘）。
- **自定义定位图标**：`BitmapDescriptorFactory.fromResource(R.drawable.xxx)` 传入。
- **精度圈**：填充色、边框色用 ARGB；精度圈大小由定位精度自动决定，不可手动设。
- 设置：`mBaiduMap.setMyLocationConfiguration(config)`。

## 自定义定位图标（v7.5.7+）

- Builder 构造：`MyLocationConfiguration.Builder(LocationMode locationMode, boolean enableArrow)`，enableArrow 为 true 表示箭头模式，false 为整体模式。
- 方法：`setCustomMarker(BitmapDescriptor)`、`setMarkerSize(float)`（0.2~3 倍）、`setArrow(BitmapDescriptor)`、`setArrowSize(float)`、`setAnimation(boolean)`（中心图呼吸动画，非箭头模式 false）、`setGifMarker(String gifPath)`（中心 gif）。设置后通过 `setMyLocationConfiguration` 生效。

## 注意

- 定位频次在 LocationClientOption 中设置；详见定位 SDK 文档。
- 定位指针方向依赖陀螺仪，需自行处理，不在地图 SDK 范畴。
