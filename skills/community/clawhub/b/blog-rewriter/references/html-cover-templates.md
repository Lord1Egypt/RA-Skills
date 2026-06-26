# HTML 封面设计模板

## 基础规格

- **尺寸**: 1200x900px (4:3 比例)
- **用途**: 小红书/公众号/抖音封面
- **格式**: HTML (可用浏览器打开截图)

## 模板 1: 科技感渐变

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1200, height=900">
    <title>封面</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            width: 1200px;
            height: 900px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 80px;
        }
        .title {
            font-size: 72px;
            font-weight: 800;
            color: white;
            text-align: center;
            line-height: 1.2;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 40px;
        }
        .subtitle {
            font-size: 32px;
            color: rgba(255,255,255,0.9);
            text-align: center;
            font-weight: 400;
        }
        .accent {
            background: linear-gradient(90deg, #ffd700, #ffed4e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
    </style>
</head>
<body>
    <div class="title">主标题<br><span class="accent">关键词高亮</span></div>
    <div class="subtitle">副标题或补充说明文字</div>
</body>
</html>
```

## 模板 2: 简约白底黑字

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1200, height=900">
    <title>封面</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            width: 1200px;
            height: 900px;
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: #ffffff;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 80px;
            border: 20px solid #000;
        }
        .title {
            font-size: 80px;
            font-weight: 900;
            color: #000;
            text-align: center;
            line-height: 1.1;
            margin-bottom: 50px;
            letter-spacing: -2px;
        }
        .subtitle {
            font-size: 36px;
            color: #666;
            text-align: center;
            font-weight: 300;
        }
        .tag {
            position: absolute;
            top: 60px;
            left: 60px;
            background: #000;
            color: #fff;
            padding: 12px 24px;
            font-size: 20px;
            font-weight: 600;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="tag">干货</div>
    <div class="title">主标题</div>
    <div class="subtitle">副标题</div>
</body>
</html>
```

## 模板 3: 深色科技风

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=1200, height=900">
    <title>封面</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            width: 1200px;
            height: 900px;
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
            background: #0a0a0a;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 80px;
            position: relative;
            overflow: hidden;
        }
        .bg-grid {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0,255,255,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0,255,255,0.03) 1px, transparent 1px);
            background-size: 40px 40px;
        }
        .title {
            font-size: 68px;
            font-weight: 800;
            color: #fff;
            text-align: center;
            line-height: 1.2;
            z-index: 1;
        }
        .highlight {
            color: #00ffff;
            text-shadow: 0 0 20px rgba(0,255,255,0.5);
        }
        .subtitle {
            font-size: 28px;
            color: #888;
            text-align: center;
            margin-top: 40px;
            z-index: 1;
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="title">主标题 <span class="highlight">关键词</span></div>
    <div class="subtitle">副标题</div>
</body>
</html>
```

## 设计原则

1. **标题突出**: 主标题字号 68-80px，视觉第一焦点
2. **层次分明**: 主标题 > 副标题 > 装饰元素
3. **留白充足**: 四周 padding 至少 60-80px
4. **对比度高**: 确保文字清晰可读
5. **适配截图**: 固定 1200x900 尺寸

## 配色方案

| 风格 | 背景 | 主色 | 强调色 |
|------|------|------|--------|
| 科技渐变 | #667eea→#764ba2 | #fff | #ffd700 |
| 简约黑白 | #fff | #000 | #666 |
| 深色科技 | #0a0a0a | #fff | #00ffff |
| 温暖橙色 | #ff6b6b→#feca57 | #fff | #fff |
| 清新蓝绿 | #00b894→#0984e3 | #fff | #fff |
