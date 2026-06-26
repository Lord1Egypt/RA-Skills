[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / map

# Module: map

## Table of contents

### References

- [OverlayEvent](map.md#overlayevent)
- [MapEvent](map.md#mapevent)
- [TouchType](map.md#touchtype)
- [Event](map.md#event)
- [CommonEvent](map.md#commonevent)
- [WinRound](map.md#winround)
- [LatLngBound](map.md#latlngbound)
- [EOverLayTypeName](map.md#eoverlaytypename)
- [BMScaleBarView](map.md#bmscalebarview)
- [MapNodeView](map.md#mapnodeview)

### Namespaces

- [SysEnum](map.SysEnum.md)

### Enumerations

- [FloorAnimateType](../enums/map.FloorAnimateType.md)
- [RunningTrackStatusEnum](../enums/map.RunningTrackStatusEnum.md)
- [CoordsTypEnum](../enums/map.CoordsTypEnum.md)
- [SportTypeEnum](../enums/map.SportTypeEnum.md)
- [LocationKindEnum](../enums/map.LocationKindEnum.md)
- [AnimationType](../enums/map.AnimationType.md)
- [HexagonType](../enums/map.HexagonType.md)
- [LayerTag](../enums/map.LayerTag.md)
- [PauseType](../enums/map.PauseType.md)
- [ResumeType](../enums/map.ResumeType.md)
- [CityTriggerType](../enums/map.CityTriggerType.md)
- [AllCityAction](../enums/map.AllCityAction.md)
- [MapLanguage](../enums/map.MapLanguage.md)

### Classes

- [ItsClickObj](../classes/map.ItsClickObj.md)
- [MapClickObj](../classes/map.MapClickObj.md)
- [AlphaAnimation](../classes/map.AlphaAnimation.md)
- [Animation](../classes/map.Animation.md)
- [AnimationSet](../classes/map.AnimationSet.md)
- [RotateAnimation](../classes/map.RotateAnimation.md)
- [ScaleAnimation](../classes/map.ScaleAnimation.md)
- [SingleScaleAnimation](../classes/map.SingleScaleAnimation.md)
- [TrackAnimation](../classes/map.TrackAnimation.md)
- [Transformation](../classes/map.Transformation.md)
- [MapComInit](../classes/map.MapComInit.md)
- [MapControllerManager](../classes/map.MapControllerManager.md)
- [MapUIStyleModel](../classes/map.MapUIStyleModel.md)
- [MapUIStyleLogoModel](../classes/map.MapUIStyleLogoModel.md)
- [WalkRunningControl](../classes/map.WalkRunningControl.md)
- [FavoriteManager](../classes/map.FavoriteManager.md)
- [HeatMap](../classes/map.HeatMap.md)
- [HeatMapAnimation](../classes/map.HeatMapAnimation.md)
- [HeatMapBuilder](../classes/map.HeatMapBuilder.md)
- [HexagonMap](../classes/map.HexagonMap.md)
- [HexagonMapBuilder](../classes/map.HexagonMapBuilder.md)
- [FileTileProvider](../classes/map.FileTileProvider.md)
- [ImageTileLayer](../classes/map.ImageTileLayer.md)
- [UrlTileProvider](../classes/map.UrlTileProvider.md)
- [CompassLayer](../classes/map.CompassLayer.md)
- [LocationLayer](../classes/map.LocationLayer.md)
- [OverlayLayer](../classes/map.OverlayLayer.md)
- [LocalMapManager](../classes/map.LocalMapManager.md)
- [LocalMapConstants](../classes/map.LocalMapConstants.md)
- [LocalMapResource](../classes/map.LocalMapResource.md)
- [LocalMapResourceUtils](../classes/map.LocalMapResourceUtils.md)
- [Bd\_3DModel](../classes/map.Bd_3DModel.md)
- [MultiPointItem](../classes/map.MultiPointItem.md)
- [Track](../classes/map.Track.md)
- [Arc](../classes/map.Arc.md)
- [Building](../classes/map.Building.md)
- [Circle](../classes/map.Circle.md)
- [ClusterGroup](../classes/map.ClusterGroup.md)
- [ClusterIcon](../classes/map.ClusterIcon.md)
- [ClusterTemplate](../classes/map.ClusterTemplate.md)
- [ClusterText](../classes/map.ClusterText.md)
- [Ground](../classes/map.Ground.md)
- [Label](../classes/map.Label.md)
- [Marker](../classes/map.Marker.md)
- [MultiPoint](../classes/map.MultiPoint.md)
- [Overlay](../classes/map.Overlay.md)
- [Polygon](../classes/map.Polygon.md)
- [Polyline](../classes/map.Polyline.md)
- [Prism](../classes/map.Prism.md)
- [TextPathMarker](../classes/map.TextPathMarker.md)
- [LineStyle](../classes/map.LineStyle.md)
- [BaseGroupUI](../classes/map.BaseGroupUI.md)
- [BaseUI](../classes/map.BaseUI.md)
- [FrameLayout](../classes/map.FrameLayout.md)
- [HorizontalLayout](../classes/map.HorizontalLayout.md)
- [ImageUI](../classes/map.ImageUI.md)
- [LabelUI](../classes/map.LabelUI.md)
- [PopView](../classes/map.PopView.md)
- [TextStyle](../classes/map.TextStyle.md)
- [VerticalLayout](../classes/map.VerticalLayout.md)
- [MapController](../classes/map.MapController.md)
- [MapOptions](../classes/map.MapOptions.md)
- [MapStatus](../classes/map.MapStatus.md)
- [GestureListener](../classes/map.GestureListener.md)
- [MapParams](../classes/map.MapParams.md)
- [BmObject](../classes/map.BmObject.md)
- [Gradient](../classes/map.Gradient.md)
- [MapUIOperateModel](../classes/map.MapUIOperateModel.md)
- [GeoBound](../classes/map.GeoBound.md)
- [ImageEntity](../classes/map.ImageEntity.md)
- [ParticleOptions](../classes/map.ParticleOptions.md)
- [Stroke](../classes/map.Stroke.md)
- [WinBound](../classes/map.WinBound.md)
- [BaseMap](../classes/map.BaseMap.md)

### Interfaces

- [AnimationListener](../interfaces/map.AnimationListener.md)
- [TraceAnimationListener](../interfaces/map.TraceAnimationListener.md)
- [TrackUpdateListener](../interfaces/map.TrackUpdateListener.md)
- [IndoorFloorBundles](../interfaces/map.IndoorFloorBundles.md)
- [RunningConfig](../interfaces/map.RunningConfig.md)
- [WalkDetailData](../interfaces/map.WalkDetailData.md)
- [GPSData](../interfaces/map.GPSData.md)
- [IMapClickListener](../interfaces/map.IMapClickListener.md)
- [FavoritePoiInfo](../interfaces/map.FavoritePoiInfo.md)
- [OverlayDragEvent](../interfaces/map.OverlayDragEvent.md)
- [OverlayDragListener](../interfaces/map.OverlayDragListener.md)
- [LocalMapListener](../interfaces/map.LocalMapListener.md)
- [cityMapItemStatusModelInterface](../interfaces/map.cityMapItemStatusModelInterface.md)
- [MapStatusWinBound](../interfaces/map.MapStatusWinBound.md)
- [MapStatusMapBound](../interfaces/map.MapStatusMapBound.md)
- [MapStatusBundle](../interfaces/map.MapStatusBundle.md)
- [MapOptionBundle](../interfaces/map.MapOptionBundle.md)
- [DefaultMsg](../interfaces/map.DefaultMsg.md)
- [ImageOpt](../interfaces/map.ImageOpt.md)
- [IGeoPoint](../interfaces/map.IGeoPoint.md)
- [IAnchor](../interfaces/map.IAnchor.md)
- [IDimension](../interfaces/map.IDimension.md)
- [LayerInfo](../interfaces/map.LayerInfo.md)
- [ColorInfo](../interfaces/map.ColorInfo.md)
- [IMapStatusOption](../interfaces/map.IMapStatusOption.md)
- [IGestureOption](../interfaces/map.IGestureOption.md)
- [IShowOption](../interfaces/map.IShowOption.md)
- [IMapOption](../interfaces/map.IMapOption.md)
- [BundleOptions](../interfaces/map.BundleOptions.md)
- [IStrokeOption](../interfaces/map.IStrokeOption.md)
- [IOverlayOption](../interfaces/map.IOverlayOption.md)
- [ICircleOption](../interfaces/map.ICircleOption.md)
- [IDotOption](../interfaces/map.IDotOption.md)
- [IGroundOption](../interfaces/map.IGroundOption.md)
- [ILabelOption](../interfaces/map.ILabelOption.md)
- [IPolygonOption](../interfaces/map.IPolygonOption.md)
- [IPolylineOption](../interfaces/map.IPolylineOption.md)
- [IArcOption](../interfaces/map.IArcOption.md)
- [ITextPathMarkerOption](../interfaces/map.ITextPathMarkerOption.md)
- [IMultiPointOption](../interfaces/map.IMultiPointOption.md)
- [ITrackOption](../interfaces/map.ITrackOption.md)
- [I3DModelOption](../interfaces/map.I3DModelOption.md)
- [IBaseMarkerOption](../interfaces/map.IBaseMarkerOption.md)
- [IMarkerOption](../interfaces/map.IMarkerOption.md)
- [IInfoWindow](../interfaces/map.IInfoWindow.md)
- [ILocation](../interfaces/map.ILocation.md)
- [ILocationConfig](../interfaces/map.ILocationConfig.md)
- [IGetPoint](../interfaces/map.IGetPoint.md)
- [IViewportOption](../interfaces/map.IViewportOption.md)
- [IViewportFit](../interfaces/map.IViewportFit.md)
- [INinePatch](../interfaces/map.INinePatch.md)
- [EventBundle](../interfaces/map.EventBundle.md)
- [MapRenderValidFrameBundle](../interfaces/map.MapRenderValidFrameBundle.md)
- [EventUIBundle](../interfaces/map.EventUIBundle.md)
- [EventOverlayBundle](../interfaces/map.EventOverlayBundle.md)
- [OnTouchListener](../interfaces/map.OnTouchListener.md)
- [IMotionEvent](../interfaces/map.IMotionEvent.md)
- [CustomMapStyleCallBack](../interfaces/map.CustomMapStyleCallBack.md)
- [MapUIOperate](../interfaces/map.MapUIOperate.md)

### Type Aliases

- [ColorString](map.md#colorstring)
- [NetURLString](map.md#neturlstring)
- [RawfileURLString](map.md#rawfileurlstring)
- [ImageURLString](map.md#imageurlstring)
- [ImageSourceType](map.md#imagesourcetype)
- [ISetCenter](map.md#isetcenter)
- [TMapViewEvent](map.md#tmapviewevent)
- [TLayer](map.md#tlayer)
- [Callback](map.md#callback)
- [Nullable](map.md#nullable)
- [ToObject](map.md#toobject)
- [Maybe](map.md#maybe)

### Variables

- [MapComponent](map.md#mapcomponent)
- [LOCAL\_MAP\_LIMIT\_DESK\_SIZE](map.md#local_map_limit_desk_size)

## References

### OverlayEvent

Re-exports [OverlayEvent](../enums/map.SysEnum.OverlayEvent.md)

___

### MapEvent

Re-exports [MapEvent](../enums/map.SysEnum.MapEvent.md)

___

### TouchType

Re-exports [TouchType](../enums/map.SysEnum.TouchType.md)

___

### Event

Re-exports [Event](../enums/map.SysEnum.Event.md)

___

### CommonEvent

Re-exports [CommonEvent](../enums/map.SysEnum.CommonEvent.md)

___

### WinRound

Renames and re-exports [WinBound](../classes/map.WinBound.md)

___

### LatLngBound

Renames and re-exports [GeoBound](../classes/map.GeoBound.md)

___

### EOverLayTypeName

Renames and re-exports [OverlayType](../enums/map.SysEnum.OverlayType.md)

___

### BMScaleBarView

Renames and re-exports [MapComponent](map.md#mapcomponent)

___

### MapNodeView

Renames and re-exports [MapComponent](map.md#mapcomponent)

## Type Aliases

### ColorString

Ƭ **ColorString**: `string` \| `number`

设置描边颜色，可设置：rgb或rgba或者#十六进制

___

### NetURLString

Ƭ **NetURLString**: `string`

前缀 http:// 或者 https:// 标记的图像地址

___

### RawfileURLString

Ƭ **RawfileURLString**: `string`

rawfile:// 标记的图像地址

___

### ImageURLString

Ƭ **ImageURLString**: [`NetURLString`](map.md#neturlstring) \| [`RawfileURLString`](map.md#rawfileurlstring)

图像资源类型定义

**`Param`**

网络图像资源地址

**`Param`**

本地Rawfile图像资源地址

**`Since`**

1.0.0

___

### ImageSourceType

Ƭ **ImageSourceType**: [`ImageURLString`](map.md#imageurlstring) \| `PixelMap`

图像资源类型定义

**`Param`**

图像资源地址

**`Param`**

[image.PixelMap图像像素类](https://developer.huawei.com/consumer/cn/doc/harmonyos-references/js-apis-image-0000001821001457#ZH-CN_TOPIC_0000001821001457__pixelmap7)

**`Since`**

1.0.0

___

### ISetCenter

Ƭ **ISetCenter**: [`LatLng`](../classes/base.LatLng.md) \| [`IGeoPoint`](../interfaces/map.IGeoPoint.md)

复合型坐标点

**`Since`**

1.0.0

___

### TMapViewEvent

Ƭ **TMapViewEvent**: [`EventBundle`](../interfaces/map.EventBundle.md) \| [`MapStatusBundle`](../interfaces/map.MapStatusBundle.md) \| [`DefaultMsg`](../interfaces/map.DefaultMsg.md) \| `boolean` \| [`MapRenderValidFrameBundle`](../interfaces/map.MapRenderValidFrameBundle.md)

地图事件回调类别

**`Since`**

1.0.2

___

### TLayer

Ƭ **TLayer**: `BaseLayer` \| `CompassLayer` \| `LocationLayer` \| [`OverlayLayer`](../classes/map.OverlayLayer.md)

图层类型

**`Since`**

1.0.1

___

### Callback

Ƭ **Callback**\<`T`\>: (`data`: `T`, `reason?`: [`MapStatusChangeReason`](../enums/map.SysEnum.MapStatusChangeReason.md)) => `void`

事件回调结构

**`Since`**

1.0.0

#### Type parameters

| Name |
| :------ |
| `T` |

#### Type declaration

▸ (`data`, `reason?`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `data` | `T` |
| `reason?` | [`MapStatusChangeReason`](../enums/map.SysEnum.MapStatusChangeReason.md) |

##### Returns

`void`

___

### Nullable

Ƭ **Nullable**\<`T`\>: `T` \| ``null`` \| `undefined`

可为空类型

**`Since`**

1.0.1

#### Type parameters

| Name |
| :------ |
| `T` |

___

### ToObject

Ƭ **ToObject**\<`T`\>: `Record`\<`string`, `T`\>

#### Type parameters

| Name |
| :------ |
| `T` |

___

### Maybe

Ƭ **Maybe**\<`T`\>: `T` \| `undefined`

#### Type parameters

| Name |
| :------ |
| `T` |

## Variables

### MapComponent

• **MapComponent**: `any`

___

### LOCAL\_MAP\_LIMIT\_DESK\_SIZE

• `Const` **LOCAL\_MAP\_LIMIT\_DESK\_SIZE**: ``"local_map_limit_size"``
