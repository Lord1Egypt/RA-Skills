

# 弹窗 (Popup)

在地图上显示信息弹窗,可独立使用或与标记关联。

## 基础用法

### 创建基本弹窗

```javascript
const popup = new dmapgl.Popup()
  .setLngLat([800000, 600000])
  .setHTML('<h3>北京</h3><p>中国首都</p>')
  .addTo(map);
```

### 关闭按钮

```javascript
// 带关闭按钮(默认)
const popup = new dmapgl.Popup({ closeButton: true })
  .setLngLat([800000, 600000])
  .setHTML('内容')
  .addTo(map);

// 无关闭按钮
const popup = new dmapgl.Popup({ closeButton: false })
  .setLngLat([800000, 600000])
  .setHTML('内容')
  .addTo(map);
```

## Popup 配置选项

```javascript
const popup = new dmapgl.Popup({
  // 是否显示关闭按钮
  closeButton: true,
  
  // 点击地图其他区域关闭
  closeOnClick: true,
  
  // 按ESC键关闭
  closeOnEscape: true,
  
  // 滚动时关闭
  closeOnMove: false,
  
  // 焦点管理
  focusAfterOpen: true,
  
  // 偏移量(像素或Pixel对象)
  offset: 25,
  // 或针对不同位置设置不同偏移
  offset: {
    'top': [0, 0],
    'bottom': [0, -30],
    'left': [15, 0],
    'right': [-15, 0]
  },
  
  // 最大宽度
  maxWidth: '300px',
  
  // CSS类名
  className: 'custom-popup'
});
```

## 内容设置

### HTML内容

```javascript
popup.setHTML(`
  <div class="popup-content">
    <h3>标题</h3>
    <img src="/images/photo.jpg" alt="照片" />
    <p>详细描述信息...</p>
    <button onclick="handleClick()">操作按钮</button>
  </div>
`);
```

### 文本内容

```javascript
popup.setText('纯文本内容,自动转义HTML');
```

### DOM元素

```javascript
const content = document.createElement('div');
content.className = 'popup-custom';
content.innerHTML = '<h3>自定义内容</h3>';

popup.setDOMContent(content);
```

### 动态更新内容

```javascript
// 更新HTML
popup.setHTML('<h3>新标题</h3><p>新内容</p>');

// 更新文本
popup.setText('新文本');

// 更新DOM
popup.setDOMContent(newElement);
```

## 位置控制

### 设置位置

```javascript
// 设置弹窗位置
popup.setLngLat([810000, 610000]);

// 获取当前位置
const lngLat = popup.getLngLat();
console.log('经度:', lngLat.lng);
console.log('纬度:', lngLat.lat);
```

### 锚点定位

```javascript
// 设置锚点位置
popup.setAnchor('bottom'); // top, bottom, left, right, center

// 自动调整(默认)
popup.setAnchor('auto');
```

## 显示和隐藏

### 添加到地图

```javascript
// 方法1: 链式调用
new dmapgl.Popup()
  .setLngLat([800000, 600000])
  .setHTML('内容')
  .addTo(map);

// 方法2: 单独添加
popup.addTo(map);
```

### 移除弹窗

```javascript
// 从地图移除
popup.remove();

// 检查是否在地图上
if (popup.isOpen()) {
  console.log('弹窗已打开');
}
```

### 切换显示

```javascript
// 切换显示/隐藏
if (popup.isOpen()) {
  popup.remove();
} else {
  popup.addTo(map);
}
```

## 与标记关联

```javascript
// 创建标记和弹窗
const marker = new dmapgl.Marker()
  .setLngLat([800000, 600000]);

const popup = new dmapgl.Popup({ offset: 25 })
  .setHTML('<h3>北京</h3><p>点击查看详情</p>');

// 关联弹窗到标记
marker.setPopup(popup);
marker.addTo(map);

// 点击标记自动显示弹窗
// 或者手动控制
marker.on('click', () => {
  popup.addTo(map);
});
```

## 事件处理

```javascript
const popup = new dmapgl.Popup();

// 打开事件
popup.on('open', () => {
  console.log('弹窗已打开');
});

// 关闭事件
popup.on('close', () => {
  console.log('弹窗已关闭');
});

// 监听地图点击关闭
map.on('click', () => {
  if (popup.isOpen()) {
    popup.remove();
  }
});
```

## 高级用法

### 富媒体弹窗

```javascript
const richPopup = new dmapgl.Popup({ maxWidth: '400px' })
  .setLngLat([800000, 600000])
  .setHTML(`
    <div class="rich-popup">
      <div class="popup-header">
        <h2>故宫博物院</h2>
        <span class="rating">⭐⭐⭐⭐⭐</span>
      </div>
      <div class="popup-image">
        <img src="/images/forbidden-city.jpg" alt="故宫" />
      </div>
      <div class="popup-body">
        <p>中国明清两代的皇家宫殿,世界文化遗产。</p>
        <ul>
          <li>开放时间: 8:30-17:00</li>
          <li>门票: ¥60</li>
          <li>地址: 北京市东城区景山前街4号</li>
        </ul>
      </div>
      <div class="popup-footer">
        <button class="btn-primary">导航</button>
        <button class="btn-secondary">收藏</button>
      </div>
    </div>
  `)
  .addTo(map);
```

CSS样式:

```css
.rich-popup {
  font-family: Arial, sans-serif;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.popup-image img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.popup-body {
  padding: 10px;
}

.popup-footer {
  padding: 10px;
  display: flex;
  gap: 10px;
}

.btn-primary, .btn-secondary {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-secondary {
  background: #e5e7eb;
  color: #374151;
}
```

### 异步加载内容

```javascript
const loadingPopup = new dmapgl.Popup()
  .setLngLat([800000, 600000])
  .setHTML('<div class="loading">加载中...</div>')
  .addTo(map);

// 异步获取数据
fetch(`/api/poi/${poiId}`)
  .then(res => res.json())
  .then(data => {
    loadingPopup.setHTML(`
      <div class="poi-info">
        <h3>${data.name}</h3>
        <p>${data.description}</p>
      </div>
    `);
  })
  .catch(err => {
    loadingPopup.setHTML('<p class="error">加载失败</p>');
  });
```

### 多个弹窗管理

```javascript
let activePopup = null;

function showPopup(lngLat, content) {
  // 关闭之前的弹窗
  if (activePopup) {
    activePopup.remove();
  }
  
  // 创建新弹窗
  activePopup = new dmapgl.Popup({ offset: 25 })
    .setLngLat(lngLat)
    .setHTML(content)
    .addTo(map);
}

// 使用
map.on('click', (e) => {
  showPopup(e.lngLat, `<p>坐标: ${e.lngLat.lng.toFixed(4)}, ${e.lngLat.lat.toFixed(4)}</p>`);
});
```

### 自定义动画

```javascript
// CSS动画
.custom-popup .dmapgl-popup-content {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### 响应式弹窗

```javascript
function createResponsivePopup(content) {
  const isMobile = window.innerWidth < 768;
  
  return new dmapgl.Popup({
    maxWidth: isMobile ? '90vw' : '400px',
    offset: isMobile ? [0, -10] : 25,
    className: isMobile ? 'mobile-popup' : 'desktop-popup'
  }).setHTML(content);
}
```

## 实用示例

### 点击地图显示坐标

```javascript
map.on('click', (e) => {
  new dmapgl.Popup()
    .setLngLat(e.lngLat)
    .setHTML(`
      <div>
        <strong>点击位置</strong><br/>
        经度: ${e.lngLat.lng.toFixed(6)}<br/>
        纬度: ${e.lngLat.lat.toFixed(6)}
      </div>
    `)
    .addTo(map);
});
```

### POI信息展示

```javascript
const pois = [
  { id: 1, name: '故宫', lng: 116.397, lat: 39.916, desc: '明清皇宫' },
  { id: 2, name: '天坛', lng: 116.407, lat: 39.882, desc: '祭天场所' }
];

pois.forEach(poi => {
  const marker = new dmapgl.Marker()
    .setLngLat([poi.lng, poi.lat]);
  
  const popup = new dmapgl.Popup({ offset: 25 })
    .setHTML(`
      <div class="poi-popup">
        <h4>${poi.name}</h4>
        <p>${poi.desc}</p>
        <a href="/detail/${poi.id}" target="_blank">查看详情</a>
      </div>
    `);
  
  marker.setPopup(popup).addTo(map);
});
```

### 表单验证提示

```javascript
function showValidationError(lngLat, message) {
  const popup = new dmapgl.Popup({
    closeButton: false,
    closeOnClick: false,
    className: 'error-popup'
  })
    .setLngLat(lngLat)
    .setHTML(`<div class="error">⚠️ ${message}</div>`)
    .addTo(map);
  
  // 3秒后自动关闭
  setTimeout(() => {
    popup.remove();
  }, 3000);
}
```

## 注意事项

1. **性能**: 避免同时打开过多弹窗
2. **内存**: 不再使用时调用 `remove()` 清理
3. **层级**: 弹窗默认在最上层,可通过CSS z-index调整
4. **移动端**: 考虑触摸设备的交互体验
5. **无障碍**: 确保弹窗内容可访问,支持键盘操作
6. **XSS防护**: 用户输入内容使用 `setText()` 而非 `setHTML()`
