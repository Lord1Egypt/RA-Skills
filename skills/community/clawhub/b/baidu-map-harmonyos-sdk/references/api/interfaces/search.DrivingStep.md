[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / DrivingStep

# Interface: DrivingStep

[search](../modules/search.md).DrivingStep

路线中的一个路段

## Hierarchy

- [`RouteStep`](search.RouteStep.md)

  ↳ **`DrivingStep`**

## Table of contents

### Properties

- [distance](search.DrivingStep.md#distance)
- [duration](search.DrivingStep.md#duration)
- [name](search.DrivingStep.md#name)
- [wayPoints](search.DrivingStep.md#waypoints)
- [direction](search.DrivingStep.md#direction)
- [entrance](search.DrivingStep.md#entrance)
- [exit](search.DrivingStep.md#exit)
- [pathString](search.DrivingStep.md#pathstring)
- [entranceInstructions](search.DrivingStep.md#entranceinstructions)
- [exitInstructions](search.DrivingStep.md#exitinstructions)
- [instructions](search.DrivingStep.md#instructions)
- [numTurns](search.DrivingStep.md#numturns)
- [pathList](search.DrivingStep.md#pathlist)
- [trafficList](search.DrivingStep.md#trafficlist)
- [roadLevel](search.DrivingStep.md#roadlevel)
- [roadName](search.DrivingStep.md#roadname)

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

### direction

• **direction**: `number`

该路段起点方向值 单位： 度。 正北方向为0度，顺时针

___

### entrance

• `Optional` **entrance**: [`RouteNode`](search.RouteNode.md)

路段入口信息

___

### exit

• `Optional` **exit**: [`RouteNode`](search.RouteNode.md)

路段出口信息

___

### pathString

• **pathString**: `string`

缓存的点

___

### entranceInstructions

• **entranceInstructions**: `string`

路段入口的指示信息

___

### exitInstructions

• **exitInstructions**: `string`

路段出口指示信息

___

### instructions

• **instructions**: `string`

路段总体指示信息

___

### numTurns

• **numTurns**: `number`

路段转弯类型
0：无效
1：直行
2：右前方转弯
3：右转
4：右后方转弯
5：掉头
6：左后方转弯
7：左转
8：左前方转弯
9：左侧
10：右侧
11：分歧-左
12：分歧中央
13：分歧右
14：环岛
15：进渡口
16：出渡口

路段转弯类型

___

### pathList

• **pathList**: [`LatLng`](../classes/base.LatLng.md)[]

途径点信息

___

### trafficList

• **trafficList**: `number`[]

路况数据数组，个数为wayPoints个数-1,该step的路况数据，0：没路况，1：畅通，2：缓慢，3：拥堵，4：非常拥堵

___

### roadLevel

• **roadLevel**: `number`

道路类型

枚举值：返回0-9之间的值
0：高速路
1：城市高速路
2:国道
3：省道
4：县道
5：乡镇村道
6：其他道路
7：九级路
8：航线(轮渡)
9：行人道路

___

### roadName

• **roadName**: `string`

道路名称
