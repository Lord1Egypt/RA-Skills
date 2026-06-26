

# Geography - 地理和几何

用于处理地理坐标、边界框和屏幕位置的类。

## LngLat

表示地理坐标(经度,纬度)。

### 构造函数

```javascript
new dmapgl.LngLat(lng, lat)
```

### 属性

- `lng` - 经度 (-180 到 180)
- `lat` - 纬度 (-90 到 90)

### 静态方法

- `convert(input)` - 转换为LngLat对象

### 实例方法

- `wrap()` - 包装经度到 -180~180 范围
- `toArray()` - 转换为数组 [lng, lat]
- `toString()` - 转换为字符串
- `distanceTo(lnglat)` - 计算到另一点的距离(米)
- `toBounds(radius)` - 转换为边界框

### 示例

```javascript
const coord = new dmapgl.LngLat(800000, 600000);
console.log(coord.lng, coord.lat);

// 转换
const coord2 = dmapgl.LngLat.convert([116.4, 39.9]);

// 距离
const distance = coord.distanceTo(coord2);
console.log(`距离: ${distance} 米`);
```

## LngLatBounds

表示地理边界框(西南角和东北角)。

### 构造函数

```javascript
new dmapgl.LngLatBounds(sw, ne)
```

### 静态方法

- `convert(input)` - 转换为LngLatBounds对象

### 实例方法

- `setNorthEast(ne)` - 设置东北角
- `setSouthWest(sw)` - 设置西南角
- `extend(obj)` - 扩展边界包含对象
- `getCenter()` - 获取中心点
- `getSouthWest()` - 获取西南角
- `getNorthEast()` - 获取东北角
- `getNorthWest()` - 获取西北角
- `getSouthEast()` - 获取东南角
- `getWest()` - 获取西边界
- `getSouth()` - 获取南边界
- `getEast()` - 获取东边界
- `getNorth()` - 获取北边界
- `toArray()` - 转换为数组 [[sw], [ne]]
- `toString()` - 转换为字符串
- `isEmpty()` - 检查是否为空
- `contains(lnglat)` - 检查是否包含坐标
- `intersects(bounds)` - 检查是否与另一边界相交

### 示例

```javascript
// 创建边界
const bounds = new dmapgl.LngLatBounds(
  [750000, 560000],  // 西南角
  [850000, 650000]   // 东北角
);

// 从地图获取
const mapBounds = map.getBounds();

// 检查是否包含
if (mapBounds.contains([116.4, 39.9])) {
  console.log('坐标在可视区域内');
}

// 扩展边界
bounds.extend([116.8, 40.2]);

// 适配视图
map.fitBounds(bounds);
```

## Point

表示二维点(x, y)。

### 构造函数

```javascript
new dmapgl.Point(x, y)
```

### 属性

- `x` - X坐标
- `y` - Y坐标

### 实例方法

- `clone()` - 克隆点
- `add(point)` - 加法
- `sub(point)` - 减法
- `mult(k)` - 乘法
- `div(k)` - 除法
- `rotate(angle)` - 旋转
- `matMult(m)` - 矩阵乘法
- `unit()` - 单位化
- `perp()` - 垂直向量
- `round()` - 四舍五入
- `mag()` - 长度
- `dist(point)` - 距离
- `angleWith(point)` - 夹角
- `angle()` - 角度

### 示例

```javascript
const p1 = new dmapgl.Point(100, 200);
const p2 = new dmapgl.Point(150, 250);

const distance = p1.dist(p2);
console.log(`距离: ${distance}`);
```

## MercatorCoordinate

墨卡托坐标,用于3D投影。

### 构造函数

```javascript
new dmapgl.MercatorCoordinate(x, y, z)
```

### 静态方法

- `fromLngLat(lngLat, altitude)` - 从经纬度创建

### 属性

- `x` - X坐标
- `y` - Y坐标
- `z` - Z坐标(高度)

### 实例方法

- `toLngLat()` - 转换为经纬度
- `toAltitude()` - 转换为海拔高度
- `meterInMercatorCoordinateUnits()` - 每米的墨卡托单位

### 示例

```javascript
// 从经纬度创建
const merc = dmapgl.MercatorCoordinate.fromLngLat(
  [800000, 600000],
  100 // 海拔高度(米)
);

// 转换回经纬度
const lngLat = merc.toLngLat();
```

## Pixel

表示屏幕像素坐标。

### 类型定义

```typescript
type Pixel = [number, number]; // [x, y]
```

## PointLike

Point或数字数组的灵活类型。

### 类型定义

```typescript
type PointLike = Point | [number, number];
```

### 示例

```javascript
const p1 = new dmapgl.Point(400, 525); // PointLike
const p2 = [400, 525]; // PointLike
```

## LngLatLike

LngLat或数组的灵活类型。

### 类型定义

```typescript
type LngLatLike = LngLat | 
                  {lng: number, lat: number} | 
                  {lon: number, lat: number} | 
                  [number, number];
```

### 示例

```javascript
const v1 = new dmapgl.LngLat(-122.42, 37.77);
const v2 = [-122.42, 37.77];
const v3 = {lon: -122.42, lat: 37.77};
```

## LngLatBoundsLike

LngLatBounds或数组的灵活类型。

### 类型定义

```typescript
type LngLatBoundsLike = LngLatBounds | 
                        [LngLatLike, LngLatLike] | 
                        [number, number, number, number];
```

### 示例

```javascript
const v1 = new dmapgl.LngLatBounds(
  new dmapgl.LngLat(-73.98, 40.76),
  new dmapgl.LngLat(-73.93, 40.80)
);
const v2 = [[-73.98, 40.76], [-73.93, 40.80]];
const v3 = [-73.98, 40.76, -73.93, 40.80];
```

## 坐标转换

### 地理坐标转像素

```javascript
const point = map.project([800000, 600000]);
console.log('像素坐标:', point.x, point.y);
```

### 像素转地理坐标

```javascript
const lngLat = map.unproject(new dmapgl.Point(100, 200));
console.log('地理坐标:', lngLat.lng, lngLat.lat);
```

## 实用示例

### 计算两点距离

```javascript
function calculateDistance(coord1, coord2) {
  const lngLat1 = dmapgl.LngLat.convert(coord1);
  const lngLat2 = dmapgl.LngLat.convert(coord2);
  
  return lngLat1.distanceTo(lngLat2);
}

const distance = calculateDistance(
  [800000, 600000],
  [116.407, 39.904]
);

console.log(`距离: ${(distance / 1000).toFixed(2)} km`);
```

### 检查点在边界内

```javascript
function isPointInBounds(point, bounds) {
  const lngLat = dmapgl.LngLat.convert(point);
  const bbox = dmapgl.LngLatBounds.convert(bounds);
  
  return bbox.contains(lngLat);
}

if (isPointInBounds([116.4, 39.9], [[750000, 560000], [850000, 650000]])) {
  console.log('点在边界内');
}
```

### 获取边界中心

```javascript
const bounds = map.getBounds();
const center = bounds.getCenter();

console.log('边界中心:', center.lng, center.lat);
```

### 扩展边界包含所有点

```javascript
const points = [
  [800000, 600000],
  [116.407, 39.904],
  [820000, 620000]
];

let bounds = new dmapgl.LngLatBounds();

points.forEach(point => {
  bounds.extend(point);
});

map.fitBounds(bounds, { padding: 50 });
```

## 注意事项

1. **坐标顺序**: DMap GL使用 [lng, lat] 顺序,而非 [lat, lng]
2. **有效范围**: 经度 -180~180,纬度 -90~90
3. **距离计算**: distanceTo 返回米为单位
4. **边界有效性**: 确保西南角的经纬度小于东北角
5. **投影限制**: 墨卡托投影在高纬度地区有变形
