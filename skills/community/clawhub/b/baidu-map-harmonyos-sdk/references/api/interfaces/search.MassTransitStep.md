[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / MassTransitStep

# Interface: MassTransitStep

[search](../modules/search.md).MassTransitStep

表示一个换乘路段

## Hierarchy

- [`RouteStep`](search.RouteStep.md)

  ↳ **`MassTransitStep`**

## Table of contents

### Properties

- [distance](search.MassTransitStep.md#distance)
- [duration](search.MassTransitStep.md#duration)
- [name](search.MassTransitStep.md#name)
- [wayPoints](search.MassTransitStep.md#waypoints)
- [trafficConditions](search.MassTransitStep.md#trafficconditions)
- [startLocation](search.MassTransitStep.md#startlocation)
- [endLocation](search.MassTransitStep.md#endlocation)
- [trainInfo](search.MassTransitStep.md#traininfo)
- [planeInfo](search.MassTransitStep.md#planeinfo)
- [coachInfo](search.MassTransitStep.md#coachinfo)
- [busInfo](search.MassTransitStep.md#businfo)
- [vehicleType](search.MassTransitStep.md#vehicletype)
- [instructions](search.MassTransitStep.md#instructions)
- [pathString](search.MassTransitStep.md#pathstring)

## Properties

### distance

• **distance**: `number`

路段距离

#### Inherited from

[RouteStep](search.RouteStep.md).[distance](search.RouteStep.md#distance)

___

### duration

• **duration**: `number`

路段耗时

#### Inherited from

[RouteStep](search.RouteStep.md).[duration](search.RouteStep.md#duration)

___

### name

• **name**: `string`

路段道路名称

#### Inherited from

[RouteStep](search.RouteStep.md).[name](search.RouteStep.md#name)

___

### wayPoints

• `Optional` **wayPoints**: [`LatLng`](../classes/base.LatLng.md)[]

路段所经过的地理坐标集合

#### Inherited from

[RouteStep](search.RouteStep.md).[wayPoints](search.RouteStep.md#waypoints)

___

### trafficConditions

• `Optional` **trafficConditions**: [`TrafficCondition`](search.TrafficCondition.md)[]

交通情况

___

### startLocation

• `Optional` **startLocation**: [`LatLng`](../classes/base.LatLng.md)

本路段起点

___

### endLocation

• `Optional` **endLocation**: [`LatLng`](../classes/base.LatLng.md)

本路段终点

___

### trainInfo

• `Optional` **trainInfo**: ``null`` \| [`TrainInfo`](search.TrainInfo.md)

火车具体信息

___

### planeInfo

• `Optional` **planeInfo**: ``null`` \| [`PlaneInfo`](search.PlaneInfo.md)

飞机具体信息

___

### coachInfo

• `Optional` **coachInfo**: ``null`` \| [`CoachInfo`](search.CoachInfo.md)

大巴具体信息

___

### busInfo

• `Optional` **busInfo**: ``null`` \| [`BusInfo`](search.BusInfo.md)

公交具体信息

___

### vehicleType

• `Optional` **vehicleType**: [`StepVehicleInfoType`](../enums/search.StepVehicleInfoType.md)

本路段中交通方式的类型：1火车，2飞机，3公交，4驾车，5步行，6大巴

___

### instructions

• `Optional` **instructions**: `string`

该路段换乘说明

___

### pathString

• `Optional` **pathString**: `string`

path点坐标,未解析,出于性能考虑，缓存path坐标点，当需要用到时再解析
