## BA2 设计生成域 范本

本文件包含 BA2 域（BA2-01 ~ BA2-05）的纯范本内容。

---

### BA2-01 Logo SVG生成 · 完整SVG结构范本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="-15 -15 270 270"
     width="270" height="270"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="brandBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0066FF"/>
      <stop offset="50%" stop-color="#0099FF"/>
      <stop offset="100%" stop-color="#00CCFF"/>
    </linearGradient>
    <linearGradient id="brandOrange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF6B35"/>
      <stop offset="100%" stop-color="#FFA052"/>
    </linearGradient>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
    <radialGradient id="nodeOrange" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFB380"/>
      <stop offset="100%" stop-color="#FF6B35"/>
    </radialGradient>
  </defs>

  <rect x="-15" y="-15" width="270" height="270" fill="#FFFFFF"/>

  <g transform="translate(120, 120)">
    <g transform="translate(-40,0)">
      <line x1="-42" y1="-52" x2="42" y2="52" stroke="url(#brandBlue)" stroke-width="14" stroke-linecap="round"/>
      <line x1="-42" y1="52" x2="42" y2="-52" stroke="url(#brandBlue)" stroke-width="14" stroke-linecap="round"/>
    </g>
    <g transform="translate(40,0)">
      <line x1="-42" y1="-52" x2="42" y2="52" stroke="url(#brandBlue)" stroke-width="14" stroke-linecap="round"/>
      <line x1="-42" y1="52" x2="42" y2="-52" stroke="url(#brandOrange)" stroke-width="14" stroke-linecap="round"/>
    </g>
    <circle r="22" fill="url(#nodeBlue)"/>
    <circle r="22" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.5"/>
    <circle r="8" fill="#FFFFFF" opacity="0.9"/>
    <circle cx="-88" cy="-95" r="9" fill="url(#nodeBlue)"/>
    <circle cx="88" cy="-95" r="9" fill="url(#nodeOrange)"/>
    <circle cx="-88" cy="95" r="9" fill="url(#nodeBlue)"/>
    <circle cx="88" cy="95" r="9" fill="url(#nodeBlue)"/>
    <line x1="-88" y1="-95" x2="0" y2="0" stroke="url(#brandBlue)" stroke-width="2" opacity="0.6"/>
    <line x1="88" y1="-95" x2="0" y2="0" stroke="url(#brandOrange)" stroke-width="2" opacity="0.6"/>
    <line x1="-88" y1="95" x2="0" y2="0" stroke="url(#brandBlue)" stroke-width="2" opacity="0.6"/>
    <line x1="88" y1="95" x2="0" y2="0" stroke="url(#brandBlue)" stroke-width="2" opacity="0.6"/>
  </g>
</svg>
```

**关键要点**：
- viewBox有边缘节点时需扩大留padding：`viewBox="-{padding} -{padding} {size+2*padding} {size+2*padding}"`
- 背景rect必须覆盖整个viewBox（不能只覆盖原始尺寸，否则透明区域导致PNG内容偏移）
- preserveAspectRatio必须设为`"xMidYMid meet"`确保按比例缩放居中
- 渐变放在`<defs>`中，通过`url(#id)`引用
- 主体定位用`<g transform="translate(centerX, centerY)">`

---

### BA2-02 标志形态派生 · 三种形态对照

| 形态 | 布局 | viewBox参考 | 文字处理 | 纵横比 |
|------|------|-------------|---------|--------|
| 横版 | 图形左 + 文字右 | `0 0 600 240` | "{{品牌简称}}"水平排列，字号48-60 | 2.5:1 |
| 竖版 | 图形上 + 文字下 | `0 0 400 480` | "{{品牌简称}}"居中，英文下方，字号40-50 | 5:6 |
| 纯图标 | 仅图形 | `-15 -15 270 270` | 无文字 | 1:1 |

横版文字SVG示例片段：
```xml
<!-- 横版：viewBox 600×240，图形居中左侧，文字右侧 -->
<g transform="translate(120, 120)">
  <!-- 图形部分（纯图标内容，缩小至约100×100） -->
  <!-- 将纯图标viewBox的-15 -15 270 270映射到此处约0,-50到0,50区域 -->
</g>
<text x="280" y="140" font-size="52" font-weight="700" fill="#0066FF"
      font-family="Microsoft YaHei, PingFang SC, sans-serif">{{品牌简称}}</text>
<text x="280" y="180" font-size="14" fill="#00CCFF" font-family="Arial"
      letter-spacing="3">{{英文简称}}</text>
```

竖版文字SVG示例片段：
```xml
<!-- 竖版：viewBox 400×480，图形居中上方，文字下方居中 -->
<g transform="translate(200, 180)">
  <!-- 图形部分（纯图标内容，缩小至约160×160） -->
  <!-- 将纯图标viewBox的-15 -15 270 270映射到此处 -->
</g>
<text x="200" y="350" font-size="48" font-weight="700" fill="#0066FF"
      font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">{{品牌简称}}</text>
<text x="200" y="395" font-size="13" fill="#00CCFF" font-family="Arial"
      letter-spacing="5" text-anchor="middle">{{英文简称}}</text>
```

**关键设计要点**：
- 横版图形区域约100×100，文字区域约300×60
- 竖版图形区域约160×160，文字区域约280×80
- 中英文字间距：中文下方留10-15px后接英文
- 英文使用letter-spacing="3-5"增加视觉延伸感

---

### BA2-03 SVG资产批量生成 · 各类别SVG要点

**商标注册稿件**（945×945，8cm@300dpi）：
- 黑白稿：纯黑色 `#000000` + 白色背景
- 彩色稿：使用品牌色（蓝#0066FF + 橙#FF6B35）
- 图形商标：仅Logo图形，无文字
- 文字商标：仅"{{品牌简称}}"文字，无图形
- 组合商标：图形+文字，推荐注册

**数字化应用**：
- App图标：圆角矩形容器，`rx="18%"`，Logo居中
- 社交头像：圆形容器，`clip-path: circle()`，Logo居中
- 文档水印：半透明，`opacity="0.1"`
- 黑白版：单色黑 `#000000`
- 反白版：白色主体 `#FFFFFF`，用于深色背景

**办公文具**：
- 名片：90×54mm，正面深色背景+Logo+信息，背面白色+大Logo
- C5信封：229×162mm，左上角寄信人+右下角收信人区
- A4信纸：210×297mm，顶部Logo+底部联系信息

**宣传物料**：
- PPT封面：16:9 (1920×1080)，Logo+标题+副标题
- 网站Banner：1920×600，Logo+标语
- 员工工牌：竖版，照片区+姓名+Logo+挂绳孔

**品牌规范**（06_品牌规范）：
- 色彩规范：品牌标准色色板，含HEX/RGB标注
- 字体规范：中文字体+英文字体标准，字号等级体系
- Logo使用规范：正确用法+错误用法对照，安全距离标注

**环境应用**（07_环境应用）：
- 门头招牌：3:1 (1800×600)，深色背景+Logo+电话+网址
- 展会背景板：16:9 (1920×1080)，渐变背景+Logo+联系信息
- 易拉宝/海报架：1:3 (800×2400)，垂直布局+Logo+联系信息

**产品周边**（08_产品周边）：
- 产品包装盒：1:1.5 (900×1350)，白底+色带+Logo+产品名
- 礼品袋：1:1.2 (800×960)，白底+提手+Logo+Slogan
- 笔记本封面：2:3 (900×1350)，深色背景+Logo+英文+网址

**多媒体模板**（09_多媒体模板）：
- 邮件签名：4:1 (1200×300)，Logo+联系信息
- 社交媒体配图：16:9 (1200×675)，深色背景+Logo+标语
- 视频封面模板：16:9 (1920×1080)，渐变背景+Logo+标题占位

---

### BA2-04 信息注入 · 替换映射表范本

| 占位符 | 替换为 | 涉及文件 | 字号调整 |
|--------|--------|---------|---------|
| {{姓名}} | {{姓名}} | 名片正面、工牌 | — |
| {{手机}} | {{手机号}} | 名片正面、名片背面、信纸 | — |
| {{邮箱}} | {{邮箱地址}} | 名片正面、名片背面、信纸、PPT | — |
| {{网址}} | {{公司网址}} | 名片背面、信纸、PPT、Banner | — |
| {{地址}} | {{办公地址}} | 名片正面、名片背面、信封、信纸 | 14→11px（分两行） |

地址分行策略：
```
第一行：{{地址第一行}}
第二行：{{地址第二行}}
```

---

### BA2-05 小尺寸优化版 · 完整SVG范本

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- 简化版SVG：用于16-128px小尺寸渲染 -->
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="-15 -15 270 270" width="270" height="270"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0066FF"/>
      <stop offset="100%" stop-color="#00CCFF"/>
    </linearGradient>
    <linearGradient id="g2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF6B35"/>
      <stop offset="100%" stop-color="#FFA052"/>
    </linearGradient>
    <radialGradient id="ng1" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
    <radialGradient id="ng2" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFB380"/>
      <stop offset="100%" stop-color="#FF6B35"/>
    </radialGradient>
  </defs>

  <rect x="-15" y="-15" width="270" height="270" fill="#FFFFFF"/>
  <g transform="translate(120, 120)">
    <g transform="translate(-40,0)">
      <line x1="-42" y1="-52" x2="42" y2="52" stroke="url(#g1)" stroke-width="14" stroke-linecap="round"/>
      <line x1="-42" y1="52" x2="42" y2="-52" stroke="url(#g1)" stroke-width="14" stroke-linecap="round"/>
    </g>
    <g transform="translate(40,0)">
      <line x1="-42" y1="-52" x2="42" y2="52" stroke="url(#g1)" stroke-width="14" stroke-linecap="round"/>
      <line x1="-42" y1="52" x2="42" y2="-52" stroke="url(#g2)" stroke-width="14" stroke-linecap="round"/>
    </g>
    <circle r="22" fill="url(#ng1)"/>
    <circle r="8" fill="#FFFFFF" opacity="0.9"/>
    <!-- 卫星节点：r=9→12（+33%） -->
    <circle cx="-88" cy="-95" r="12" fill="url(#ng1)"/>
    <circle cx="88" cy="-95" r="12" fill="url(#ng2)"/>
    <circle cx="-88" cy="95" r="12" fill="url(#ng1)"/>
    <circle cx="88" cy="95" r="12" fill="url(#ng1)"/>
    <!-- 连接线：stroke-width=2→3（+50%） -->
    <line x1="-88" y1="-95" x2="0" y2="0" stroke="url(#g1)" stroke-width="3" opacity="0.6"/>
    <line x1="88" y1="-95" x2="0" y2="0" stroke="url(#g2)" stroke-width="3" opacity="0.6"/>
    <line x1="-88" y1="95" x2="0" y2="0" stroke="url(#g1)" stroke-width="3" opacity="0.6"/>
    <line x1="88" y1="95" x2="0" y2="0" stroke="url(#g1)" stroke-width="3" opacity="0.6"/>
    <!-- 已移除：虚线圆环、细线圆环、外围轴点、虚线连接线 -->
  </g>
</svg>
```

**移除/增强规则速查**：

| 元素类型 | 移除条件 | 原因 | 增强策略 | 幅度 |
|---------|---------|------|---------|------|
| 虚线圆环 | stroke-dasharray + stroke-width<2 | 虚线在64px下变实心 | — | — |
| 细线圆环 | stroke-width<1 | 1024→64缩小16倍后0.05px消失 | — | — |
| 小点 | r<6 | 缩小后亚像素不可见 | — | — |
| 虚线连接线 | stroke-width<1.5 | 同细线 | — | — |
| 卫星节点 | — | — | 放大半径 | +33% |
| 连接线 | — | — | 加粗stroke | +50% |
| 中心节点 | — | 已足够大 | 保持不变 | — |
| X形核心 | — | stroke-width=14已足够 | 保持不变 | — |

---

### BA2域技术坑

**坑1：SVG XML特殊字符未转义**
- 问题：HTML页面中SVG显示为破碎图标❌
- 根因：SVG是XML格式，文本中的`&`必须转义为`&amp;`。某SVG中含`Specifications & Features`未转义，导致浏览器解析失败。仅含英文`&`的SVG触发，纯中文SVG不受影响
- 触发场景：公司名称中的"&"、英文文本中的"&"（如"John & Jane"、"Specifications & Features"）
- 修复：所有SVG文本中的`&`→`&amp;`、`<`→`&lt;`、`>`→`&gt;`
- **检查命令**：`grep -rn '&[^a-zA-Z#;]' *.svg` 扫描所有SVG文件中的未转义`&`（排除`&amp;`、`&lt;`等合法实体）
- **预防**：生成SVG时，对所有`<text>`标签内的内容做XML转义检查

**坑2：SVG `<defs>` 缺失**
- 问题：SVG在HTML中正常显示但PNG渲染失败（纯色块无内容）
- 根因：SVG中引用了`url(#g1)`/`url(#g2)`等渐变，但`<defs>`未定义。某项目中5个SVG最初缺失`<defs>`
- 修复：每个使用渐变引用的SVG必须在`<svg>`内包含完整的`<defs>`定义
- **检查命令**：`for f in *.svg; do if grep -q 'url(#g' "$f" && ! grep -q '<defs>' "$f"; then echo "MISSING: $f"; fi; done`
