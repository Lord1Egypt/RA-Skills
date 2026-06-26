# 图片资源

**边界**：技能内 `assets/images/` 图片及用途；集成与构建见 [cocoapods.md](cocoapods.md)、[project-config.md](project-config.md)。

**路线小车**：路线上的小车图标**必须优先使用**本技能提供的纹理图（下表 icon_car / car_triangle / track_car）；仅当无可用纹理时，才使用纯色或自绘图片。实现时先 `[UIImage imageNamed:@"icon_car"]`（或对应名称），为 nil 再回退。

| 图片 | 用途 |
|------|------|
| icon_car | 小车 marker（**路线小车优先**） |
| car_triangle | 带方向小车（车头朝上） |
| track_car | 带方向小车（车头朝右），**轨迹动画推荐** |
| icon_start | 起点标注 |
| icon_end | 终点标注 |
| icon_via | 途经点 |
| **路况纹理**（BMKMultiPolyline + BMKMultiTexturePolylineView，drawIndexs 来自 BMKDrivingStep.traffics） | |
| traffic_texture_unknown | 无数据（traffics=0，drawIndex 0） |
| traffic_texture_smooth | 畅通（traffics=1，drawIndex 1） |
| traffic_texture_slow | 缓行（traffics=2，drawIndex 2） |
| traffic_texture_congestion | 拥堵（traffics=3，drawIndex 3） |
| traffic_texture_severe_congestion | 严重拥堵（traffics=4，drawIndex 4） |
