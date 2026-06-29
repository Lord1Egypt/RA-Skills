## BA6 扩展应用域 范本

本文件包含 BA6 域（BA6-01 ~ BA6-03）的纯范本内容。

---

### BA6-01 环境应用 · SVG范本

#### 门头招牌 (1800×600)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 600" width="1800" height="600"
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
  <!-- 背景 -->
  <rect width="1800" height="600" fill="#0A1929"/>

  <!-- Logo区域 -->
  <g transform="translate(150, 300)">
    <!-- 横版标志SVG内容嵌入 -->
    <circle r="60" fill="url(#nodeBlue)"/>
    <text x="100" y="25" font-size="48" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif">{{品牌简称}}</text>
    <text x="100" y="65" font-size="16" fill="#00CCFF"
          font-family="Arial" letter-spacing="3">{{英文简称}}</text>
  </g>

  <!-- 分隔线 -->
  <line x1="400" y1="200" x2="400" y2="400" stroke="#0066FF" stroke-width="2" opacity="0.5"/>

  <!-- 公司信息区域 -->
  <text x="450" y="220" font-size="20" fill="#FFFFFF" font-family="Microsoft YaHei, PingFang SC, sans-serif">
    {{行业类型}}
  </text>
  <text x="450" y="280" font-size="16" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif">
    {{手机号}}
  </text>
  <text x="450" y="320" font-size="14" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif">
    {{公司网址}}
  </text>

  <!-- 装饰元素 -->
  <line x1="1600" y1="100" x2="1700" y2="100" stroke="#FF6B35" stroke-width="4"/>
  <circle cx="1650" cy="500" r="20" fill="url(#nodeOrange)" opacity="0.5"/>
</svg>
```

**关键要点**：
- 深色背景配合白色/亮蓝文字
- Logo居左，公司信息居右
- 使用品牌色作为点缀

#### 展会背景板 (1920×1080)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080"
     preserveAspectRatio="xMidYMid meet">
  <!-- 背景渐变 -->
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A1929"/>
      <stop offset="100%" stop-color="#003366"/>
    </linearGradient>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#bgGrad)"/>

  <!-- 中央Logo -->
  <g transform="translate(960, 540)">
    <circle r="120" fill="url(#nodeBlue)"/>
    <text x="0" y="60" font-size="48" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">{{品牌简称}}</text>
  </g>

  <!-- 联系信息 -->
  <text x="960" y="750" font-size="24" fill="#FFFFFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{姓名}}</text>
  <text x="960" y="800" font-size="20" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{手机号}}</text>
  <text x="960" y="850" font-size="20" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{邮箱地址}}</text>
  <text x="960" y="900" font-size="20" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{公司网址}}</text>

  <!-- 两侧装饰 -->
  <circle cx="200" cy="200" r="60" fill="#FF6B35" opacity="0.2"/>
  <circle cx="1720" cy="880" r="80" fill="#00CCFF" opacity="0.2"/>
  <circle cx="200" cy="900" r="40" fill="#00CCFF" opacity="0.3"/>
  <circle cx="1720" cy="200" r="50" fill="#FF6B35" opacity="0.3"/>
</svg>
```

#### 易拉宝/海报架 (800×2400)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 2400" width="800" height="2400"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <!-- 背景 -->
  <rect width="800" height="2400" fill="#0A1929"/>

  <!-- 顶部Logo区域 -->
  <g transform="translate(400, 300)">
    <circle r="100" fill="url(#nodeBlue)"/>
    <text x="0" y="20" font-size="40" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">{{品牌简称}}</text>
  </g>

  <!-- 中间分隔线 -->
  <line x1="200" y1="600" x2="600" y2="600" stroke="#0066FF" stroke-width="2"/>

  <!-- 公司信息 -->
  <text x="400" y="700" font-size="24" fill="#FFFFFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{品牌简称}}</text>
  <text x="400" y="800" font-size="20" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{姓名}} · {{手机号}}</text>
  <text x="400" y="860" font-size="20" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{邮箱地址}}</text>
  <text x="400" y="920" font-size="20" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{公司网址}}</text>

  <!-- 底部装饰 -->
  <line x1="200" y1="2000" x2="600" y2="2000" stroke="#0066FF" stroke-width="2"/>
  <text x="400" y="2200" font-size="24" fill="#FFFFFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{英文简称}}</text>
</svg>
```

---

### BA6-02 产品周边 · SVG范本

#### 产品包装盒 (900×1350)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1350" width="900" height="1350"
     preserveAspectRatio="xMidYMid meet">
  <!-- 包装盒正面 -->
  <rect width="900" height="1350" fill="#FFFFFF"/>

  <!-- 顶部色带 -->
  <rect width="900" height="200" fill="#0066FF"/>

  <!-- Logo -->
  <g transform="translate(450, 100)">
    <circle r="60" fill="#FFFFFF"/>
    <text x="0" y="30" font-size="32" font-weight="700" fill="#0066FF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">示例</text>
  </g>

  <!-- 产品名称区域 -->
  <text x="450" y="400" font-size="48" font-weight="700" fill="#0066FF"
        font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">产品名称</text>

  <!-- 产品描述 -->
  <text x="450" y="500" font-size="24" fill="#666" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">产品描述文字</text>

  <!-- 底部信息 -->
  <text x="450" y="1200" font-size="20" fill="#999" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{品牌简称}} · 2026</text>

  <!-- 装饰元素 -->
  <circle cx="700" cy="800" r="100" fill="#FF6B35" opacity="0.1"/>
  <circle cx="200" cy="600" r="60" fill="#00CCFF" opacity="0.1"/>
</svg>
```

#### 礼品袋 (800×960)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 960" width="800" height="960"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <!-- 礼品袋主体 -->
  <rect width="800" height="960" fill="#FFFFFF"/>

  <!-- 提手 -->
  <path d="M 200 80 Q 400 20 600 80" stroke="#0066FF" stroke-width="8" fill="none"/>

  <!-- Logo -->
  <g transform="translate(400, 400)">
    <circle r="80" fill="url(#nodeBlue)"/>
    <text x="0" y="20" font-size="36" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">{{品牌简称}}</text>
  </g>

  <!-- 品牌标语 -->
  <text x="400" y="550" font-size="20" fill="#666" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{品牌标语}}</text>

  <!-- 底部装饰 -->
  <circle cx="100" cy="800" r="40" fill="#FF6B35" opacity="0.15"/>
  <circle cx="700" cy="800" r="40" fill="#00CCFF" opacity="0.15"/>
</svg>
```

#### 笔记本封面 (900×1350, A5尺寸148×210mm)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 1350" width="900" height="1350"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <!-- 笔记本封面 -->
  <rect width="900" height="1350" fill="#0A1929"/>

  <!-- Logo -->
  <g transform="translate(450, 500)">
    <circle r="100" fill="url(#nodeBlue)"/>
    <text x="0" y="30" font-size="48" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">{{品牌简称}}</text>
  </g>

  <!-- 品牌信息 -->
  <text x="450" y="700" font-size="24" fill="#FFFFFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{英文简称}}</text>
  <text x="450" y="750" font-size="18" fill="#00CCFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">network technology</text>

  <!-- 底部装饰 -->
  <line x1="200" y1="1200" x2="700" y2="1200" stroke="#0066FF" stroke-width="2"/>
  <text x="450" y="1300" font-size="16" fill="#666" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{公司网址}}</text>
</svg>
```

---

### BA6-03 多媒体模板 · SVG范本

#### 邮件签名 (1200×300)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <!-- 签名背景 -->
  <rect width="1200" height="300" fill="#FFFFFF"/>
  <rect x="0" y="0" width="8" height="300" fill="#0066FF"/>

  <!-- Logo -->
  <g transform="translate(150, 150)">
    <circle r="50" fill="url(#nodeBlue)"/>
    <text x="70" y="10" font-size="32" font-weight="700" fill="#0066FF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif">{{品牌简称}}</text>
    <text x="70" y="35" font-size="14" fill="#00CCFF" font-family="Arial" letter-spacing="2">{{英文简称}}</text>
  </g>

  <!-- 分隔线 -->
  <line x1="350" y1="80" x2="350" y2="220" stroke="#eee" stroke-width="1"/>

  <!-- 联系信息 -->
  <text x="400" y="120" font-size="18" fill="#333" font-family="Microsoft YaHei, PingFang SC, sans-serif">{{姓名}}</text>
  <text x="400" y="160" font-size="16" fill="#666" font-family="Microsoft YaHei, PingFang SC, sans-serif">{{手机号}}</text>
  <text x="400" y="200" font-size="16" fill="#666" font-family="Microsoft YaHei, PingFang SC, sans-serif">{{邮箱地址}}</text>
  <text x="400" y="240" font-size="16" fill="#0066FF" font-family="Microsoft YaHei, PingFang SC, sans-serif">{{公司网址}}</text>
</svg>
```

#### 社交媒体配图 (1200×675)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" width="1200" height="675"
     preserveAspectRatio="xMidYMid meet">
  <defs>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <!-- 背景 -->
  <rect width="1200" height="675" fill="#0A1929"/>

  <!-- 中央Logo -->
  <g transform="translate(600, 337)">
    <circle r="80" fill="url(#nodeBlue)"/>
    <text x="0" y="25" font-size="32" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">{{品牌简称}}</text>
    <text x="0" y="50" font-size="14" fill="#00CCFF" font-family="Arial" letter-spacing="2" text-anchor="middle">{{英文简称}}</text>
  </g>

  <!-- 装饰元素 -->
  <circle cx="200" cy="150" r="60" fill="#FF6B35" opacity="0.15"/>
  <circle cx="1000" cy="525" r="80" fill="#00CCFF" opacity="0.15"/>
  <circle cx="200" cy="525" r="40" fill="#00CCFF" opacity="0.2"/>
  <circle cx="1000" cy="150" r="50" fill="#FF6B35" opacity="0.2"/>

  <!-- 标语 -->
  <text x="600" y="500" font-size="24" fill="#FFFFFF" font-family="Microsoft YaHei, PingFang SC, sans-serif"
        text-anchor="middle">{{品牌标语}}</text>
</svg>
```

#### 视频封面模板 (1920×1080)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080"
     preserveAspectRatio="xMidYMid meet">
  <!-- 背景渐变 -->
  <defs>
    <linearGradient id="pptBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0A1929"/>
      <stop offset="100%" stop-color="#003366"/>
    </linearGradient>
    <radialGradient id="nodeBlue" cx="35%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#66CCFF"/>
      <stop offset="100%" stop-color="#0066FF"/>
    </radialGradient>
  </defs>
  <rect width="1920" height="1080" fill="url(#pptBg)"/>

  <!-- 左侧Logo -->
  <g transform="translate(300, 540)">
    <circle r="100" fill="url(#nodeBlue)"/>
    <text x="120" y="25" font-size="48" font-weight="700" fill="#FFFFFF"
          font-family="Microsoft YaHei, PingFang SC, sans-serif">{{品牌简称}}</text>
    <text x="120" y="65" font-size="18" fill="#00CCFF" font-family="Arial" letter-spacing="3">{{英文简称}}</text>
  </g>

  <!-- 标题占位 -->
  <text x="960" y="450" font-size="64" font-weight="700" fill="#FFFFFF"
        font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">[标题]</text>
  <text x="960" y="550" font-size="32" fill="#00CCFF"
        font-family="Microsoft YaHei, PingFang SC, sans-serif" text-anchor="middle">[副标题]</text>

  <!-- 装饰元素 -->
  <circle cx="1600" cy="200" r="100" fill="#FF6B35" opacity="0.1"/>
  <circle cx="300" cy="900" r="60" fill="#00CCFF" opacity="0.15"/>
</svg>
```

---

### BA6域技术坑

**坑1：环境应用比例与实际制作尺寸不符**
- 问题：门头招牌1800×600的1:3比例与实际店铺门脸比例不匹配
- 修复：提供常用比例的参考尺寸表，用户根据实际场景调整

**坑2：产品周边SVG文件包含非打印颜色**
- 问题：深色背景#0A1929在白色纸张上印刷效果不佳
- 修复：产品周边类资产提供白底版本和彩底版本两种选择

**坑3：多媒体模板字体在不同平台显示不一致**
- 问题：邮件签名中的字体在Gmail和Outlook中显示效果不同
- 修复：使用系统默认字体族（Microsoft YaHei, PingFang SC, sans-serif）确保最大兼容性