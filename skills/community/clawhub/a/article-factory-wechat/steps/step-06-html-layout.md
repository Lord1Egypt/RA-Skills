# Step 6: HTML排版优化

**目标：** 将文章转为精美HTML格式，适配微信公众号阅读体验

！！注意：下述样式仅供参考，需根据实际内容、文章主题、用户意向风格进行优化。

## 微信公众号CSS兼容性说明

微信公众号对部分CSS特性支持有限，必须遵守以下规则：

❌ **不支持的CSS特性（必须移除）**：

- `transition` - 过渡动画
- `:hover` `:active` 等伪类交互样式
- `@keyframes` 和 `animation` 动画
- `position: fixed` - 固定定位（会被微信强制重置）
- `float` 浮动布局可能存在兼容性问题，优先使用 flexbox
- 外部字体文件引入，只能使用系统默认字体

✅ **安全兼容的CSS特性**：

- 所有基础选择器和盒模型
- `flexbox` 弹性布局
- 线性渐变 `linear-gradient`
- `border-radius` 圆角
- `box-shadow` 阴影
- 内联CSS样式（全部内联，不使用`<link>`外部样式表）

## 设计系统

### 颜色系统

| 用途   | 色值        | 说明        |
| ---- | --------- | --------- |
| 主色调  | `#2c3e50` | 深蓝灰色，专业稳重 |
| 辅助色  | `#3498db` | 蓝色链接/强调   |
| 强调色  | `#e74c3c` | 红色重点标记    |
| 正文文字 | `#333333` | 高对比度，易读   |
| 次要文字 | `#666666` | 注释、引用     |
| 边框分割 | `#eaecef` | 浅色分割线     |
| 背景色  | `#ffffff` | 纯白色背景     |

### 排版系统

| 元素      | 字体大小 | 行高  | 说明           |
| ------- | ---- | --- | ------------ |
| h1 文章标题 | 26px | 1.4 | 居中，加粗        |
| h2 章节标题 | 22px | 1.5 | 带左侧边栏强调      |
| h3 小节标题 | 18px | 1.5 | 半加粗          |
| 正文      | 16px | 1.8 | 舒适行高，首行缩进2em |
| 引用      | 15px | 1.7 | 斜体，浅色背景      |
| 代码块     | 14px | 1.6 | 深色背景，等宽字体    |
| 脚注/来源   | 14px | 1.5 | 灰色文字         |

### 间距系统（8px网格）

- 段落上下间距：16px
- 章节上下间距：32px
- 内边距：按照 8/16/24/32 阶梯
- 外边距：保持呼吸感，避免内容拥挤

## 核心组件样式

可参考以下内联CSS样式的组件代码，根据实际需要优化并应用：

### 章节标题（带左侧色条）

```html
<h2 style="font-size: 22px; font-weight: 600; color: #2c3e50; margin: 32px 0 16px 0; padding-left: 12px; border-left: 4px solid #3498db; line-height: 1.5;">章节标题</h2>
```

### 正文段落

```html
<p style="font-size: 16px; line-height: 1.8; color: #333333; margin: 16px 0; text-align: justify; text-indent: 2em;">正文内容</p>
```

### 信息提示框

```html
<div style="background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f0 100%); border-radius: 8px; padding: 16px 20px; margin: 20px 0; border-left: 4px solid #3498db;">
  <div style="font-weight: 600; color: #2c3e50; margin-bottom: 8px; font-size: 16px;">提示</div>
  <div style="font-size: 15px; color: #555; line-height: 1.7;">这是一条提示信息</div>
</div>
```

### 警告提示框

```html
<div style="background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%); border-radius: 8px; padding: 16px 20px; margin: 20px 0; border-left: 4px solid #e74c3c;">
  <div style="font-weight: 600; color: #e74c3c; margin-bottom: 8px; font-size: 16px;">注意</div>
  <div style="font-size: 15px; color: #555; line-height: 1.7;">这是一条警告信息</div>
</div>
```

### 代码块

```html
<pre style="background: #2d3436; color: #f8f8f2; border-radius: 6px; padding: 16px; margin: 20px 0; overflow-x: auto;"><code style="font-family: 'SF Mono', Menlo, Monaco, Consolas, monospace; font-size: 14px; line-height: 1.6;">代码内容</code></pre>
```

### 行内代码

```html
<p style="font-size: 16px; line-height: 1.8; color: #333333; margin: 16px 0; text-align: justify; text-indent: 2em;">这是一段文字包含<code style="font-family: 'SF Mono', Menlo, Monaco, Consolas, monospace; font-size: 14px; line-height: 1.6; background: #f1f3f4; padding: 2px 6px; border-radius: 4px; color: #e74c3c; font-size: 0.9em;">行内代码</code>内容</p>
```

### 数据卡片布局

```html
<div style="display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 140px; background: #f8f9fa; border-radius: 8px; padding: 16px; text-align: center;">
    <div style="font-size: 14px; color: #666; margin-bottom: 8px;">指标1</div>
    <div style="font-size: 24px; font-weight: 700; color: #3498db;">100</div>
  </div>
  <div style="flex: 1; min-width: 140px; background: #f8f9fa; border-radius: 8px; padding: 16px; text-align: center;">
    <div style="font-size: 14px; color: #666; margin-bottom: 8px;">指标2</div>
    <div style="font-size: 24px; font-weight: 700; color: #3498db;">200</div>
  </div>
</div>
```

### 重点强调

```html
<p style="font-size: 16px; line-height: 1.8; color: #333333; margin: 16px 0; text-align: justify; text-indent: 2em;">这是一段<strong style="color: #e74c3c; font-weight: 600;">强调文字</strong>内容</p>
```

### 引用

```html
<blockquote style="background: linear-gradient(135deg, #f5f7fa 0%, #e4e9f0 100%); border-radius: 8px; padding: 16px 20px; margin: 20px 0; border-left: 4px solid #3498db;">
  <p style="text-indent: 0; margin: 0; font-size: 15px; color: #555; font-style: italic;">引用内容</p>
</blockquote>
```

### 列表（微信兼容版）

**⚠️ 注意：微信公众号对** **`<ul>`** **和** **`<li>`** **标签支持有限，建议使用以下替代方案**

#### 无序列表替代方案

```html
<div style="font-size: 16px; line-height: 1.8; color: #333333; margin: 16px 0 16px 2em; padding: 0;">
  <div style="margin: 8px 0;">• 请求头、查询参数</div>
  <div style="margin: 8px 0;">• 表单数据、JSON Body</div>
  <div style="margin: 8px 0;">• Cookies、IP地址</div>
  <div style="margin: 8px 0;">• 甚至能测试各种HTTP状态码、重定向、延迟响应</div>
</div>
```

#### 有序列表替代方案

```html
<div style="font-size: 16px; line-height: 1.8; color: #333333; margin: 16px 0 16px 2em; padding: 0;">
  <div style="margin: 8px 0;">1. 想找各种新奇API → public-apis</div>
  <div style="margin: 8px 0;">2. 写前端Demo要占位接口 → JSONPlaceholder</div>
  <div style="margin: 8px 0;">3. 调试HTTP请求抓包 → Httpbin</div>
</div>
```

### 图片

```html
<img style="max-width: 100% !important; height: auto !important; border-radius: 8px; margin: 20px auto; display: block; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);" src="images/cover.png" alt="图片描述">
```

## 优化原则

1. **可读性优先**：足够的行高和字号，舒适的对比度
2. **留白呼吸**：适当间距，避免内容拥挤
3. **层次清晰**：通过字号、颜色、边距建立清晰的视觉层级
4. **兼容性优先**：只使用微信支持的CSS特性，移除不兼容的动效
5. **内联CSS**：所有样式使用内联方式，确保微信公众号正确渲染
6. **图片路径**：使用相对路径引用图片。确保图片文件存在于文章所在目录或 `images` 子目录中
7. **列表处理**：避免使用 `<ul>` 和 `<li>` 标签，使用 `<div>` 模拟列表结构以确保微信正确渲染

