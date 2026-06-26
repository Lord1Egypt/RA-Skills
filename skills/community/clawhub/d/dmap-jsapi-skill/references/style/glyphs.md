

# Glyphs - 字体

Glyphs 提供文本标签渲染所需的字体系列。

## 配置

### 基本配置

```javascript
{
  "glyphs": "zyzx://vector_2025/standard/fonts/{fontstack}/{range}.pbf"
}
```

### URL模板

URL模板包含两个占位符:
- `{fontstack}` - 字体名称，如 "Open Sans Regular"
- `{range}` - Unicode范围，如 "0-255"

### 自定义字体服务

```javascript
{
  "glyphs": "https://example.com/fonts/{fontstack}/{range}.pbf"
}
```

## 使用字体

### 在图层中指定字体

```javascript
map.addLayer({
  id: 'labels',
  type: 'symbol',
  source: 'places',
  layout: {
    'text-field': ['get', 'name'],
    'text-font': ['Open Sans Regular', 'Arial Unicode MS Regular'],
    'text-size': 14
  }
});
```

### 字体回退

```javascript
'text-font': [
  'Noto Sans SC Regular',  // 首选
  'Noto Sans Regular',     // 备选1
  'Arial Unicode MS Regular'  // 备选2
]
```

## 常用字体

### 英文字体

- Open Sans Regular
- Open Sans Bold
- Open Sans Italic
- Arial Unicode MS Regular

### 中文字体

- Noto Sans SC Regular (简体中文)
- Noto Sans SC Bold
- Noto Sans TC Regular (繁体中文)
- PingFang SC Regular

### 多语言支持

```javascript
'text-font': [
  'Noto Sans SC Regular',  // 中文
  'Noto Sans JP Regular',  // 日文
  'Noto Sans KR Regular',  // 韩文
  'Open Sans Regular'      // 拉丁文
]
```

## 本地字体

### 使用系统字体

```javascript
var map = new dmapgl.Map({
  container: 'map',
  style: style,
  localIdeographFontFamily: 'sans-serif'  // CJK字符使用本地字体
});
```

### 禁用本地字体

```javascript
var map = new dmapgl.Map({
  container: 'map',
  style: style,
  localIdeographFontFamily: false  // 使用服务器字体
});
```

## 字体格式

Glyphs 使用 Signed Distance Field (SDF) 格式的 PBF 文件:

- **PBF**: Protocol Buffers 格式
- **SDF**: 支持任意缩放不失真
- **分块**: 按Unicode范围分块加载

## Unicode范围

常见的Unicode范围块:

- `0-255`: 基本拉丁字符
- `256-511`: 拉丁扩展
- `19968-40959`: CJK统一表意文字
- `12352-12447`: 平假名
- `12448-12543`: 片假名
- `44032-55215`: 韩文音节

## 注意事项

1. **性能**: 只加载需要的Unicode范围
2. **带宽**: 中文字体文件较大，考虑本地字体
3. **回退**: 始终提供多个字体备选
4. **许可**: 确保字体使用许可合规
5. **CDN**: 使用CDN加速字体加载
