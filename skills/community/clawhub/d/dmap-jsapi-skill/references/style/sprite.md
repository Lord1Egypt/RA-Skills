

# Sprite - 图标集

Sprite 提供用于渲染地图符号的小图标集合。

## 配置

### 基本配置

```javascript
{
  "sprite": "zyzx://vector_2025/standard/sprites/sprite"
}
```

### 自定义 Sprite

```javascript
{
  "sprite": "https://example.com/sprites/mysprite"
}
```

这会加载:
- `https://example.com/sprites/mysprite.json` - 元数据
- `https://example.com/sprites/mysprite.png` - 图片
- `https://example.com/sprites/mysprite@2x.png` - 高分辨率图片

## 使用 Sprite 图标

### 在图层中使用

```javascript
map.addLayer({
  id: 'icons',
  type: 'symbol',
  source: 'places',
  layout: {
    'icon-image': 'restaurant-15',  // sprite中的图标ID
    'icon-size': 1
  }
});
```

### 添加自定义图标

```javascript
// 从图片添加
const image = new Image(32, 32);
image.src = 'custom-icon.png';
image.onload = () => {
  map.addImage('custom-icon', image);
};

// 使用
map.addLayer({
  id: 'custom-icons',
  type: 'symbol',
  source: 'points',
  layout: {
    'icon-image': 'custom-icon'
  }
});
```

### 动态生成图标

```javascript
// 创建Canvas图标
const canvas = document.createElement('canvas');
canvas.width = 64;
canvas.height = 64;
const ctx = canvas.getContext('2d');

// 绘制圆形
ctx.beginPath();
ctx.arc(32, 32, 28, 0, 2 * Math.PI);
ctx.fillStyle = '#3b82f6';
ctx.fill();
ctx.strokeStyle = '#fff';
ctx.lineWidth = 4;
ctx.stroke();

// 添加到地图
map.addImage('circle-icon', canvas);
```

## Sprite 元数据格式

```json
{
  "restaurant-15": {
    "width": 32,
    "height": 32,
    "x": 0,
    "y": 0,
    "pixelRatio": 1,
    "visible": true
  },
  "cafe-15": {
    "width": 32,
    "height": 32,
    "x": 32,
    "y": 0,
    "pixelRatio": 1,
    "visible": true
  }
}
```

## 注意事项

1. **性能**: 合并多个小图标到一个sprite减少请求
2. **分辨率**: 提供@2x版本支持高分辨率屏幕
3. **大小**: 单个sprite不宜过大，建议拆分为多个
4. **缓存**: sprite会被浏览器缓存
5. **更新**: 修改sprite后需要清除缓存
