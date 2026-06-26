

# Root - 根属性

样式文件的根级别属性，定义地图的基本配置。

## 必需属性

### version

样式规范版本（必须为8）。

```javascript
{
  "version": 8
}
```

## 可选属性

### name

样式的名称。

```javascript
{
  "version": 8,
  "name": "My Custom Style"
}
```

### metadata

元数据，用于存储自定义信息。

```javascript
{
  "version": 8,
  "metadata": {
    "mapcenter": [801292.5499279505, 606918.7969073517],
    "mapbounds": [716638.2414098255, 548483.5939021005, 894455.0756895209, 728066.4667000007],
    "indexbounds": [-4823200.0, -528738.6842773687, 1888538.6842773688, 6183000.0],
    "mapscale": 0.002828908127455374,
    "topscale": 2.018358341600529e-8,
    "epsgcode": 0
  }
}
```

### center

地图初始中心点。

```javascript
{
  "version": 8,
  "center": [800000, 600000]  // [x, y] 地方平面坐标
}
```

### zoom

初始缩放级别。

```javascript
{
  "version": 8,
  "zoom": 11
}
```

### bearing

初始旋转角度（逆时针，单位：度）。

```javascript
{
  "version": 8,
  "bearing": 0
}
```

### pitch

初始俯仰角（0-85度）。

```javascript
{
  "version": 8,
  "pitch": 0
}
```

### sources

数据源定义对象。

```javascript
{
  "version": 8,
  "sources": {
    "矢量切片": {
      "tiles": ["zyzx://vector_2025/standard/tiles/{z}/{x}/{y}.mvt"],
      "type": "vector"
    },
    "satellite": {
      "type": "raster",
      "tiles": ["zyzx://img?year=&type=Sate&z={z}&x={x}&y={y}'],
      'tileSize': 512
    }
  }
}
```

详见 [Sources](sources.md)

### layers

图层定义数组。

```javascript
{
  "version": 8,
  "sources": { /* ... */ },
  "layers": [
    {
      "id": "background",
      "type": "background",
      "paint": {
        "background-color": "#f0f0f0"
      }
    },
    {
      "id": "roads",
      "type": "line",
      "source": "satellite",
      "source-layer": "road",
      "paint": {
        "line-color": "#3b82f6",
        "line-width": 2
      }
    }
  ]
}
```

详见 [Layers](layers.md)

### sprite

图标集URL。

```javascript
{
  "version": 8,
  "sprite": "zyzx://vector_2025/standard/sprites/sprite"
}
```

详见 [Sprite](sprite.md)

### glyphs

字体URL模板。

```javascript
{
  "version": 8,
  "glyphs": "zyzx://vector_2025/standard/fonts/{fontstack}/{range}.pbf"
}
```

详见 [Glyphs](glyphs.md)

### transition

全局过渡动画配置。

```javascript
{
  "version": 8,
  "transition": {
    "duration": 300,
    "delay": 0
  }
}
```

详见 [Transition](transition.md)

### light

全局光照配置。

```javascript
{
  "version": 8,
  "light": {
    "anchor": "viewport",
    "position": [1, 90, 80],
    "intensity": 0.5
  }
}
```

详见 [Light](light.md)

### terrain

地形配置。

```javascript
{
  "version": 8,
  "terrain": {
    "source": "dmap-dem",
    "exaggeration": 1.5
  }
}
```

详见 [Terrain](terrain.md)

### fog

雾效配置。

```javascript
{
  "version": 8,
  "fog": {
    "range": [0.5, 10],
    "color": "#ffffff",
    "horizon-blend": 0.1
  }
}
```

详见 [Fog](fog.md)


## 完整示例

```javascript
{
  "version": 8,
  "name": "DMap Custom Style",
  "metadata": {
  },
  "center": [800000, 600000],
  "zoom": 11,
  "bearing": 0,
  "pitch": 0,
  "sources": {
    "矢量切片": {
      "type": "vector",
      "tiles": ["zyzx://vector_2025/standard/tiles/{z}/{x}/{y}.mvt"]
    }
  },
  "sprite": "zyzx://vector_2025/standard/sprites/sprite",
  "glyphs": "zyzx://vector_2025/standard/fonts/{fontstack}/{range}.pbf",
  "layers": [
    {
      "id": "background",
      "type": "background",
      "paint": {
        "background-color": "#f0f0f0"
      }
    }
  ],
  "transition": {
    "duration": 300
  },
  "light": {
    "anchor": "viewport",
    "position": [1, 90, 80],
    "intensity": 0.5
  }
}
```

## 注意事项

1. **version**: 必须为8
2. **sources和layers**: 通常一起使用
3. **顺序**: layers数组的顺序决定渲染顺序
4. **引用**: layer的source必须在sources中定义
5. **性能**: 过多的layers影响性能
6. **验证**: 使用样式验证工具检查格式
