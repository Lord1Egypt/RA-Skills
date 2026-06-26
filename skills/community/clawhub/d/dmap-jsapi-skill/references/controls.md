

# 地图控件 (Controls)

DMap GL提供多种内置控件,增强地图交互功能。

## NavigationControl - 导航控件

缩放和旋转按钮。

### 基础用法

```javascript
const nav = new dmapgl.NavigationControl();
map.addControl(nav);
```

### 配置选项

```javascript
const nav = new dmapgl.NavigationControl({
  // 显示哪些按钮
  showZoom: true,      // 缩放按钮
  showCompass: true,   // 指南针/重置旋转
  visualizePitch: true // 显示俯仰指示器
});

map.addControl(nav);
```

### 位置控制

```javascript
// 添加到右上角(默认)
map.addControl(nav, 'top-right');

// 其他位置
map.addControl(nav, 'top-left');
map.addControl(nav, 'bottom-right');
map.addControl(nav, 'bottom-left');
```

## ScaleControl - 比例尺

显示当前地图比例。

### 基础用法

```javascript
const scale = new dmapgl.ScaleControl();
map.addControl(scale, 'bottom-left');
```

### 配置选项

```javascript
const scale = new dmapgl.ScaleControl({
  maxWidth: 100,        // 最大宽度(像素)
  unit: 'metric'        // 单位: 'imperial'(英里), 'metric'(米), 'nautical'(海里)
});

map.addControl(scale, 'bottom-left');
```

### 动态更新

```javascript
// 更新单位
scale.setUnit('imperial');
```

## FullscreenControl - 全屏控件

切换地图全屏显示。

### 基础用法

```javascript
const fullscreen = new dmapgl.FullscreenControl();
map.addControl(fullscreen, 'top-right');
```

### 配置容器

```javascript
// 指定全屏容器(默认为地图容器)
const fullscreen = new dmapgl.FullscreenControl({
  container: document.getElementById('fullscreen-container')
});

map.addControl(fullscreen);
```

### 事件监听

```javascript
fullscreen.on('fullscreenchange', () => {
  if (document.fullscreenElement) {
    console.log('进入全屏');
  } else {
    console.log('退出全屏');
  }
});
```

## AttributionControl - 版权信息

显示数据来源版权信息。

### 基础用法

```javascript
const attribution = new dmapgl.AttributionControl({
  compact: false,  // 紧凑模式
  customAttribution: '© 自定义版权信息'
});

map.addControl(attribution);
```

### 配置选项

```javascript
const attribution = new dmapgl.AttributionControl({
  // 紧凑模式(小屏幕自动启用)
  compact: true,
  
  // 自定义版权文本
  customAttribution: [
    '© DMap',
    '© OpenStreetMap contributors'
  ]
});
```

## 自定义控件

### 创建简单控件

```javascript
class CustomControl {
  constructor() {
    this._map = null;
    this._container = null;
  }
  
  onAdd(map) {
    this._map = map;
    
    // 创建容器
    this._container = document.createElement('div');
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';
    
    // 创建按钮
    const button = document.createElement('button');
    button.type = 'button';
    button.innerHTML = '🎯';
    button.title = '回到中心点';
    
    button.addEventListener('click', () => {
      map.flyTo({
        center: [800000, 600000],
        zoom: 11
      });
    });
    
    this._container.appendChild(button);
    
    return this._container;
  }
  
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}

// 使用
const customCtrl = new CustomControl();
map.addControl(customCtrl, 'top-right');
```

### 复杂控件示例

```javascript
class LayerSwitcher {
  constructor(layers) {
    this.layers = layers;
    this._map = null;
    this._container = null;
  }
  
  onAdd(map) {
    this._map = map;
    
    this._container = document.createElement('div');
    this._container.className = 'layer-switcher mapboxgl-ctrl';
    
    // 标题
    const title = document.createElement('h4');
    title.textContent = '图层切换';
    this._container.appendChild(title);
    
    // 图层列表
    this.layers.forEach(layer => {
      const item = document.createElement('div');
      item.className = 'layer-item';
      
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.id = layer.id;
      checkbox.checked = true;
      
      const label = document.createElement('label');
      label.htmlFor = layer.id;
      label.textContent = layer.name;
      
      checkbox.addEventListener('change', (e) => {
        const visibility = e.target.checked ? 'visible' : 'none';
        map.setLayoutProperty(layer.mapLayerId, 'visibility', visibility);
      });
      
      item.appendChild(checkbox);
      item.appendChild(label);
      this._container.appendChild(item);
    });
    
    return this._container;
  }
  
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}

// 使用
const layerSwitcher = new LayerSwitcher([
  { id: 'roads', name: '道路', mapLayerId: 'road-layer' },
  { id: 'buildings', name: '建筑物', mapLayerId: 'building-layer' },
  { id: 'labels', name: '标签', mapLayerId: 'label-layer' }
]);

map.addControl(layerSwitcher, 'top-right');
```

CSS样式:

```css
.layer-switcher {
  background: white;
  padding: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  min-width: 150px;
}

.layer-switcher h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
}

.layer-item {
  display: flex;
  align-items: center;
  margin: 5px 0;
}

.layer-item input {
  margin-right: 8px;
}

.layer-item label {
  cursor: pointer;
  font-size: 13px;
}
```

## 控件管理

### 移除控件

```javascript
// 移除特定控件
map.removeControl(nav);

// 或者通过引用
const controls = [];
const nav = new dmapgl.NavigationControl();
controls.push(nav);
map.addControl(nav);

// 清理所有控件
controls.forEach(ctrl => map.removeControl(ctrl));
controls.length = 0;
```

### 检查控件是否存在

```javascript
// 没有直接的方法,需要自己跟踪
const hasControl = controls.includes(someControl);
```

## 实用示例

### 组合控件

```javascript
// 创建控件组
function addStandardControls(map) {
  // 导航
  map.addControl(new dmapgl.NavigationControl(), 'top-right');
  
  // 比例尺
  map.addControl(new dmapgl.ScaleControl({ maxWidth: 80 }), 'bottom-left');
  
  // 全屏
  map.addControl(new dmapgl.FullscreenControl(), 'top-right');
  
  // 定位
  map.addControl(new dmapgl.GeolocateControl({
    positionOptions: { enableHighAccuracy: true },
    trackUserLocation: true
  }), 'top-right');
  
  // 版权
  map.addControl(new dmapgl.AttributionControl({
    compact: true
  }));
}

addStandardControls(map);
```

### 响应式控件

```javascript
function setupResponsiveControls(map) {
  const nav = new dmapgl.NavigationControl();
  const scale = new dmapgl.ScaleControl();
  
  function updateControls() {
    const isMobile = window.innerWidth < 768;
    
    // 移动端隐藏部分控件
    if (isMobile) {
      map.removeControl(nav);
      map.removeControl(scale);
    } else {
      map.addControl(nav, 'top-right');
      map.addControl(scale, 'bottom-left');
    }
  }
  
  window.addEventListener('resize', updateControls);
  updateControls();
}
```

### 主题切换

```javascript
class ThemeControl {
  constructor() {
    this._map = null;
    this._container = null;
    this._isDark = false;
  }
  
  onAdd(map) {
    this._map = map;
    
    this._container = document.createElement('div');
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group theme-control';
    
    const button = document.createElement('button');
    button.type = 'button';
    button.innerHTML = '🌙';
    button.title = '切换主题';
    
    button.addEventListener('click', () => {
      this.toggleTheme();
    });
    
    this._container.appendChild(button);
    return this._container;
  }
  
  toggleTheme() {
    this._isDark = !this._isDark;
    
    const style = this._isDark 
      ? 'zyzx://vector/black/styles/style.json'
      : 'zyzx://vector/shallow/styles/style.json';
    
    this._map.setStyle(style);
    
    // 更新图标
    const button = this._container.querySelector('button');
    button.innerHTML = this._isDark ? '☀️' : '🌙';
  }
  
  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}

map.addControl(new ThemeControl(), 'top-right');
```

## 注意事项

1. **位置选择**: 避免控件重叠,合理规划位置
2. **性能**: 控件数量影响性能,保持简洁
3. **移动端**: 考虑触摸设备的可用性
4. **无障碍**: 确保控件可键盘访问
5. **样式定制**: 通过CSS类名自定义控件外观
6. **内存管理**: 移除控件时调用 `onRemove()`
