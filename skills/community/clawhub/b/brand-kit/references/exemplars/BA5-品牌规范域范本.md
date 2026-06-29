## BA5 品牌规范域 范本

本文件包含 BA5 域（BA5-01 ~ BA5-04）的纯范本内容。

---

### BA5-01 VI手册HTML生成 · 完整结构范本

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta name="robots" content="noindex, nofollow">
  <link rel="icon" href="01_核心标志/favicon.ico" type="image/x-icon">
  <title>品牌视觉识别手册</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    html, body { width: 100%; height: 100%; }
    body { font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; }
    .vi-manual { max-width: 1200px; margin: 0 auto; padding: 40px 20px; background: #fff; }
    .vi-section { page-break-inside: avoid; margin-bottom: 60px; padding: 40px 0; border-bottom: 1px solid #eee; }
    .vi-section:last-child { border-bottom: none; }
    .vi-cover { text-align: center; padding: 100px 20px; }
    .vi-cover h1 { font-size: 48px; color: #0066FF; margin-bottom: 20px; }
    .vi-cover p { font-size: 18px; color: #666; }
    @media print {
      body { -webkit-print-color-adjust: exact; }
      .vi-section { page-break-inside: avoid; }
    }
  </style>
</head>
<body>
<div class="vi-manual">

  <!-- 封面 -->
  <section class="vi-cover vi-section">
    <h1>品牌视觉识别手册</h1>
    <p>Brand Visual Identity Manual</p>
  </section>

  <!-- 品牌概述 -->
  <section class="vi-section">
    <h2>品牌概述</h2>
    <p>描述公司品牌定位、核心理念、视觉风格。</p>
  </section>

  <!-- 标志说明 -->
  <section class="vi-section">
    <h2>标志说明</h2>
    <img src="01_核心标志/01_横版标志.png" alt="横版标志">
    <img src="01_核心标志/02_竖版标志.png" alt="竖版标志">
    <img src="01_核心标志/03_纯图标.png" alt="纯图标">
  </section>

  <!-- 色彩体系 -->
  <section class="vi-section">
    <h2>色彩体系</h2>
    <img src="06_品牌规范/01_色彩规范.png" alt="色彩规范">
  </section>

  <!-- 字体规范 -->
  <section class="vi-section">
    <h2>字体规范</h2>
    <img src="06_品牌规范/02_字体规范.png" alt="字体规范">
  </section>

  <!-- Logo使用规范 -->
  <section class="vi-section">
    <h2>Logo使用规范</h2>
    <img src="06_品牌规范/03_Logo使用规范.png" alt="Logo使用规范">
  </section>

</div>
</body>
</html>
```

**关键要点**：
- `page-break-inside: avoid` 确保打印时章节不跨页
- `-webkit-print-color-adjust: exact` 确保颜色打印准确
- 封面使用品牌主色作为标题颜色
- 每个章节按逻辑顺序组织，从概述到具体规范

---

### BA5-02 色彩规范 · SVG色板范本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 540" width="800" height="540"
     preserveAspectRatio="xMidYMid meet">
  <!-- 标题 -->
  <text x="400" y="40" font-size="28" font-weight="700" fill="#333"
        font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">
    品牌色彩体系
  </text>

  <!-- 主色色板 -->
  <text x="40" y="100" font-size="20" font-weight="600" fill="#333">主色</text>

  <!-- 科技蓝 -->
  <rect x="40" y="120" width="120" height="120" fill="#0066FF"/>
  <text x="40" y="260" font-size="14" fill="#666">科技蓝</text>
  <text x="40" y="280" font-size="14" fill="#999">#0066FF</text>

  <!-- 亮蓝 -->
  <rect x="180" y="120" width="120" height="120" fill="#00CCFF"/>
  <text x="180" y="260" font-size="14" fill="#666">亮蓝</text>
  <text x="180" y="280" font-size="14" fill="#999">#00CCFF</text>

  <!-- 强调色色板 -->
  <text x="40" y="340" font-size="20" font-weight="600" fill="#333">强调色</text>

  <!-- 活力橙 -->
  <rect x="40" y="360" width="120" height="120" fill="#FF6B35"/>
  <text x="40" y="500" font-size="14" fill="#666">活力橙</text>
  <text x="40" y="520" font-size="14" fill="#999">#FF6B35</text>

  <!-- 深色背景 -->
  <rect x="180" y="360" width="120" height="120" fill="#0A1929"/>
  <text x="180" y="500" font-size="14" fill="#666">深色背景</text>
  <text x="180" y="520" font-size="14" fill="#999">#0A1929</text>
</svg>
```

**关键要点**：
- 每个色块120×120px，确保色值可视性
- 色值标注使用14px字体，颜色#999（中性灰）
- 色名使用14px字体，颜色#666
- 色板布局保持统一间距（40px行距、40px列距）

---

### BA5-03 字体规范 · SVG范本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560"
     preserveAspectRatio="xMidYMid meet">
  <!-- 标题 -->
  <text x="400" y="40" font-size="28" font-weight="700" fill="#333"
        font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">
    品牌字体规范
  </text>

  <!-- 中文字体 -->
  <text x="40" y="100" font-size="20" font-weight="600" fill="#333">中文字体</text>
  <text x="40" y="160" font-size="36" font-weight="700" fill="#0066FF"
        font-family="Microsoft YaHei, PingFang SC, sans-serif">微软雅黑 Bold</text>
  <text x="40" y="200" font-size="24" font-weight="400" fill="#333"
        font-family="Microsoft YaHei, PingFang SC, sans-serif">微软雅黑 Regular</text>
  <text x="40" y="240" font-size="16" font-weight="400" fill="#666"
        font-family="Microsoft YaHei, PingFang SC, sans-serif">微软雅黑 Light</text>

  <!-- 英文字体 -->
  <text x="40" y="320" font-size="20" font-weight="600" fill="#333">英文字体</text>
  <text x="40" y="380" font-size="36" font-weight="700" fill="#0066FF"
        font-family="Arial, Helvetica, sans-serif">Arial Bold</text>
  <text x="40" y="420" font-size="24" font-weight="400" fill="#333"
        font-family="Arial, Helvetica, sans-serif">Arial Regular</text>

  <!-- 字号等级 -->
  <text x="40" y="500" font-size="20" font-weight="600" fill="#333">字号等级</text>
  <text x="40" y="540" font-size="14" fill="#666">大标题 48px · 副标题 32px · 正文 16px · 说明 14px</text>
</svg>
```

**关键要点**：
- 中文使用 Microsoft YaHei / PingFang SC
- 英文使用 Arial / Helvetica
- 字号覆盖大中小三档：大标题48px、副标题32px、正文16px、说明14px
- 字体颜色使用品牌主色#0066FF

---

### BA5-04 Logo使用规范 · SVG范本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 700" width="800" height="700"
     preserveAspectRatio="xMidYMid meet">
  <!-- 标题 -->
  <text x="400" y="40" font-size="28" font-weight="700" fill="#333"
        font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">
    Logo使用规范
  </text>

  <!-- 正确用法 -->
  <text x="40" y="100" font-size="22" font-weight="700" fill="#00CCFF">正确用法 ✓</text>

  <!-- 标准尺寸 -->
  <g transform="translate(40, 120)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">最小尺寸 32px</text>
  </g>

  <!-- 安全距离 -->
  <g transform="translate(220, 120)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <line x1="20" y1="80" x2="140" y2="80" stroke="#00CCFF" stroke-width="2" stroke-dasharray="4,4"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">安全距离 ≥ 0.5h</text>
  </g>

  <!-- 浅色背景 -->
  <g transform="translate(400, 120)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">浅色背景</text>
  </g>

  <!-- 深色背景 -->
  <g transform="translate(580, 120)">
    <rect x="0" y="0" width="160" height="160" fill="#0A1929"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">深色背景</text>
  </g>

  <!-- 错误用法 -->
  <text x="40" y="320" font-size="22" font-weight="700" fill="#FF6B35">错误用法 ✗</text>

  <!-- 拉伸变形 -->
  <g transform="translate(40, 340)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">拉伸变形</text>
  </g>

  <!-- 错误颜色 -->
  <g transform="translate(220, 340)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">错误颜色</text>
  </g>

  <!-- 添加特效 -->
  <g transform="translate(400, 340)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">添加特效</text>
  </g>

  <!-- 杂乱背景 -->
  <g transform="translate(580, 340)">
    <rect x="0" y="0" width="160" height="160" fill="#f5f5f5" stroke="#eee"/>
    <text x="80" y="175" font-size="12" fill="#666" text-anchor="middle">杂乱背景</text>
  </g>

  <!-- 安全距离说明 -->
  <text x="400" y="560" font-size="16" fill="#333" text-anchor="middle">
    安全距离：Logo周围至少留Logo高度50%的空白区域
  </text>
  <text x="400" y="590" font-size="14" fill="#666" text-anchor="middle">
    最小使用尺寸：Logo高度不低于32px（屏幕显示）/ 10mm（印刷）
  </text>
  <text x="400" y="620" font-size="14" fill="#666" text-anchor="middle">
    背景要求：Logo与背景需有足够对比度，避免在复杂图案上使用
  </text>
</svg>
```

**关键要点**：
- 正确用法和错误用法分两排展示，视觉对比鲜明
- 正确用法使用品牌辅色#00CCFF标注"✓"
- 错误用法使用强调色#FF6B35标注"✗"
- 安全距离标注使用虚线示意
- 底部添加详细的文字说明

---

### BA5域技术坑

**坑1：色彩值与Logo不一致**
- 问题：色彩规范中的色值与Logo SVG中的实际颜色不一致
- 修复：从Logo SVG的`<defs>`中直接提取所有`stop-color`和`fill`值
- **检查命令**：`grep -rn 'stop-color="#[^"]*"\|fill="#[^"]*"' 01_核心标志/*.svg | sort -u > /tmp/logo_colors.txt && grep -rn 'fill="#[^"]*"\|stop-color="#[^"]*"' 06_品牌规范/01_色彩规范.svg | sort -u > /tmp/standard_colors.txt && diff /tmp/logo_colors.txt /tmp/standard_colors.txt`，无输出表示一致；若有差异则需对照确认哪些色值是品牌规范中应包含的、哪些是Logo特有

**坑2：字体规范与实际使用不一致**
- 问题：字体规范中标注的字体与Logo中实际使用的字体不一致
- 修复：从Logo SVG的`font-family`属性中直接提取字体名称
- **检查命令**：`grep -rn 'font-family=' 01_核心标志/*.svg | sed 's/.*font-family="//;s/".*//' | sort -u` 提取Logo实际使用的字体，与`06_品牌规范/02_字体规范.svg`中的标注字体逐条比对

**坑3：Logo使用规范的SVG文件过大**
- 问题：正确用法和错误用法都需要嵌入完整Logo SVG，导致文件过大
- 修复：使用简化的Logo图形（纯图标小尺寸版）作为示例
- **检查命令**：`ls -lh 06_品牌规范/03_Logo使用规范.svg`，文件大小应小于30KB（标准Logo SVG约10-15KB，含8个示例不应膨胀超过2倍）