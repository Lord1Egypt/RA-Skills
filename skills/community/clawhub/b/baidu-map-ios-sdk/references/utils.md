# 工具组件

**边界**：坐标转换、几何、视野、调起地图等；与其它文档组合使用。优先用本文 API，勿手写（见 [SKILL.md](../SKILL.md)）。

## 坐标转换 (BMKGeometry)

头文件：`BaiduMapAPI_Utils/BMKGeometry.h`

| 函数 | 说明 |
|------|------|
| `BMKMapPointForCoordinate:` | 经纬度 → 直角地理坐标 |
| `BMKCoordinateForMapPoint:` | 直角地理坐标 → 经纬度 |
| `BMKCoordTrans:fromType:toType:` | 经纬度坐标系转换（WGS84/GCJ02/BD09） |
| `BMKConvertToBaiduMercatorFromBD09LL:` | BD09 经纬度 → 百度墨卡托 |
| `BMKConvertToBD09LLFromBaiduMercator:` | 百度墨卡托 → BD09 经纬度 |

**坐标系类型**（BMKTypes.h）：`BMK_COORDTYPE_GPS`(WGS84)、`BMK_COORDTYPE_COMMON`(GCJ02)、`BMK_COORDTYPE_BD09LL`(百度)。**注意**：地图 SDK 全局为 BD09；定位 SDK 的 **coordinateType 默认为 BMKLocationCoordinateTypeGCJ02**，用于地图时需设为 BMKLocationCoordinateTypeBMK09LL 或先用 BMKCoordTrans 转换，见 [location.md](location.md)「坐标系」。

## 几何计算

| 函数 | 说明 |
|------|------|
| `BMKMetersPerMapPointAtLatitude:` | 指定纬度下 1 MapPoint 对应的米数 |
| `BMKMapPointsPerMeterAtLatitude:` | 指定纬度下 1 米对应的 MapPoint 数 |
| `BMKMetersBetweenMapPoints` | 两点间距离（米） |
| `BMKMetersBetweenCoordinates` | 两点间距离（米） |
| `BMKGetDirectionFromCoords` | 从起点到终点的方位角（0°=北，CLLocationDirection） |
| `BMKMapRectInset` | 矩形内缩 |
| `BMKMapRectUnion` | 矩形并集 |
| `BMKMapRectContainsPoint` | 点是否在矩形内 |

**大地线 slerp**（球面线性插值，SDK 未提供）：`f∈[0,1]` 时 `coord = slerp(from, to, f)` 沿大地线插值。将经纬度转单位球坐标 (x,y,z)，`dot = from·to`，`omega = acos(dot)`，`a = sin((1-f)*omega)/sin(omega)`，`b = sin(f*omega)/sin(omega)`，`p = a*from + b*to`，再转回经纬度。

## 动画插值器 (BMKInterpolator)

头文件：`BaiduMapAPI_Map/BMKInterpolator.h`

用于 BMKMapTrackAnimation 等动画的插值曲线：

| 类型 | 说明 |
|------|------|
| BMKLinearInterpolator | 线性（默认） |
| BMKAccelerateDecelerateInterpolator | 先加速后减速 |
| BMKAccelerateInterpolator | 加速 |
| BMKDecelerateInterpolator | 减速 |
| BMKAnticipateInterpolator | 回弹后前进 |
| BMKOvershootInterpolator | 超出后回弹 |
| BMKBounceInterpolator | 弹跳 |
| BMKCycleInterpolator | 正弦循环 |

## 调起百度地图

头文件：`BaiduMapAPI_Utils/BMKNavigation.h`、`BMKOpenPoi.h`、`BMKOpenRoute.h`

| 类 | 说明 |
|----|------|
| BMKNavigation | 调起百度地图导航 |
| BMKOpenPoi | 打开 POI 详情 |
| BMKOpenRoute | 打开路线规划 |
| BMKOpenPanorama | 打开街景 |

## 常用枚举 (BMKCommonDef)

头文件：`BaiduMapAPI_Map/BMKCommonDef.h`

| 枚举 | 说明 |
|------|------|
| BMKRotateAnmination | Marker 使用动画旋转 |
| BMKRotateItem | 使用外部设置的 rotate |
| BMKRotateGeoNorth | 旋转基准为地理北（与 BMKGetDirectionFromCoords 一致） |
| BMKRotateScreenUpper | 旋转基准为屏幕正上方 |
| BMKAnimationTrackXY | 轨迹动画跟随 X、Y |
| BMKFollowMapRotateAxisPitch | 跟随地图俯仰角 |
| BMKFollowMapRotateAxisYaw | 跟随地图偏航角 |

## 地图视野适配

根据 polyline 或 annotations 设置地图可见区域：

```objc
// 单条 polyline
- (void)mapViewFitPolyline:(BMKPolyline *)polyline withMapView:(BMKMapView *)mapView {
    if (polyline.pointCount < 1) return;
    BMKMapPoint pt = polyline.points[0];
    double leftTop_x = pt.x, leftTop_y = pt.y, rightBottom_x = pt.x, rightBottom_y = pt.y;
    for (int i = 1; i < polyline.pointCount; i++) {
        BMKMapPoint p = polyline.points[i];
        leftTop_x = MIN(leftTop_x, p.x);
        rightBottom_x = MAX(rightBottom_x, p.x);
        leftTop_y = MIN(leftTop_y, p.y);
        rightBottom_y = MAX(rightBottom_y, p.y);
    }
    BMKMapRect rect = BMKMapRectMake(leftTop_x, leftTop_y, rightBottom_x - leftTop_x, rightBottom_y - leftTop_y);
    [mapView fitVisibleMapRect:rect edgePadding:UIEdgeInsetsMake(20, 10, 20, 10) withAnimated:YES];
}

// 或使用 showAnnotations:padding:animated:
[mapView showAnnotations:mapView.annotations padding:UIEdgeInsetsMake(0, 50, 0, 40) animated:YES];

// 视野适配标准见 ui-standards.md
```

### 全点视野适配（标注 + 路线途经点）

当标注与路线途经点分布较广时，`showAnnotations` 仅适配标注，可能遗漏路线点。应在 **mapViewDidFinishLoading** 中收集所有坐标，用 `BMKMapPointForCoordinate` + `BMKMapRectUnion` 构建 BMKMapRect，再调用 `fitVisibleMapRect`：

```objc
- (void)fitMapToAllPoints {
    NSMutableArray<NSValue *> *allCoords = [NSMutableArray array];
    for (id<BMKAnnotation> ann in self.mapView.annotations) {
        CLLocationCoordinate2D c = ann.coordinate;
        [allCoords addObject:[NSValue valueWithBytes:&c objCType:@encode(CLLocationCoordinate2D)]];
    }
    for (MarchRouteModel *route in routes) {
        for (NSValue *v in route.waypoints) { [allCoords addObject:v]; }
    }
    if (allCoords.count == 0) return;
    CLLocationCoordinate2D first; [allCoords.firstObject getValue:&first];
    BMKMapRect rect = BMKMapRectMake(BMKMapPointForCoordinate(first).x, BMKMapPointForCoordinate(first).y, 0, 0);
    for (NSValue *v in allCoords) {
        CLLocationCoordinate2D c; [v getValue:&c];
        rect = BMKMapRectUnion(rect, BMKMapRectMake(BMKMapPointForCoordinate(c).x, BMKMapPointForCoordinate(c).y, 0, 0));
    }
    [self.mapView fitVisibleMapRect:rect edgePadding:UIEdgeInsetsMake(100, 44, bottomPad + 44, 44) withAnimated:YES];
}
```

---

## 按需方案

| 需求 | 能力 | 说明 |
|------|------|------|
| 路线全屏可见 | fitVisibleMapRect / showAnnotations | 本文 |
| 坐标转换 | BMKCoordTrans、BMKMapPointForCoordinate | 本文 |
| 国内外/境内判断 | 百度 **iOS 定位 SDK** | **最佳**：`[BMKLocationManager BMKLocationDataAvailableForCoordinate:withCoorType:]`，坐标类型 BMKLocationCoordinateTypeBMK09LL，返回 YES=国内。未集成定位 SDK 时可用多矩形或逆地理（BMKReverseGeoCodeSearch）辅助。 |
| 调起百度地图导航 | BMKNavigation | 本文 |
