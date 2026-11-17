---
name: get-net-pic
description: "当用户说「登录xxx官网」「获取xxx网页图片」「下载官网图片」时触发。用来获取指定网站首页的图片资源并整理成文档。"
---

# get-net-pic 使用说明

## 适用场景

- 用户说「登录 XXX 官网」「打开 XXX 网站」
- 用户说「获取网页图片」「下载官网轮播图」「保存网站图片」
- 用户说「把网站图片整理成文档」

## 标准流程

### Step 1: 获取网页 HTML 内容

使用 `web_fetch` 工具抓取目标网站首页的原始 HTML：

```text
web_fetch(url="https://目标网站.com")
```

部分网站是 SPA（单页应用），直接抓取只能拿到骨架 HTML。这种情况下：
- 先尝试通过 `extractMode=text` 或 `extractMode=markdown` 获取可读内容
- 再尝试获取原始 HTML 提取图片 URL（使用 `raw-html` 模式）

### Step 2: 提取图片 URL

从返回的 HTML 中提取所有图片资源链接。目标图片包括：

| 类型 | 说明 | 常见关键词 |
|------|------|-----------|
| 轮播图/英雄图 | 首页大图 Banner | `hero`, `banner`, `slide`, `carousel`, `splash`, `main` |
| 功能展示图 | 产品/服务特性展示 | `feature`, `showcase`, `promo`, `intro` |
| 图标/Logo | 品牌标识 | `logo`, `icon`（酌情排除） |
| 背景图 | CSS 背景图片 | 通过 `background-image: url(...)` 提取 |
| 分享封面 | OG 分享图 | `share-image`, `og-image`, `thumbnail` |

**提取方法：**

1. 从 HTML 中匹配 `src="..."`、`data-src="..."` 属性
2. 从 CSS 中匹配 `background-image: url(...)`、`background: url(...)`
3. 从 HTML 中匹配 `meta[property="og:image"]` 的 `content` 属性

### Step 3: 下载图片

使用 PowerShell 下载图片到桌面临时文件夹：

```powershell
# 创建桌面目录
$desktop = [Environment]::GetFolderPath('Desktop')
$dir = Join-Path $desktop '<网站名>_images'
New-Item -ItemType Directory -Path $dir -Force | Out-Null

# 逐一下载（使用 WebClient 或 Invoke-WebRequest）
$urls = @('图片URL1', '图片URL2', ...)
$i = 1
foreach ($url in $urls) {
    $ext = [System.IO.Path]::GetExtension($url).Split('?')[0]
    $fname = '{0:D2}{1}' -f $i, $ext
    $file = Join-Path $dir $fname
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFile($url, $file)
    $i++
}
```

**注意：**
- 图片 URL 可能有相对路径，需要补全为绝对 URL（拼接 `https://域名`）
- 部分 CDN 图片 URL 带签名参数，保留原样不要截断
- 下载失败时跳过（`-ErrorAction SilentlyContinue`），不要中断整个流程

### Step 4: 生成本地图片预览

下载完成后，读取图片文件展示给用户确认：

```powershell
Get-ChildItem $dir | Select-Object Name, Length
```

### Step 5: 生成 DOCX 文档

使用 `docx` 技能创建 Word 文档，将图片嵌入文档中：

```javascript
const { Document, Packer, Paragraph, TextRun, ImageRun, 
        Header, Footer, AlignmentType, HeadingLevel,
        PageNumber } = require('docx');
const fs = require('fs');
const path = require('path');

// 图片目录
const imgDir = 'C:\\Users\\dugao\\Desktop\\<网站名>_images';
const files = fs.readdirSync(imgDir).filter(f => /\.(jpg|jpeg|png|webp|svg)$/i.test(f));

const doc = new Document({
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 } } },
    children: [
      // 标题
      new Paragraph({
        heading: HeadingLevel.TITLE,
        children: [new TextRun({ text: '<网站名> - 官网图片', size: 48, bold: true, font: 'Arial' })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: '生成时间：' + new Date().toLocaleString('zh-CN'), size: 20, color: '666666' })]
      }),
      // 逐张图片
      ...files.map((f, i) => [
        new Paragraph({
          heading: HeadingLevel.HEADING_2,
          children: [new TextRun({ text: '图片 ' + (i+1) + '：' + f })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 100, after: 200 },
          children: [new ImageRun({
            type: f.endsWith('.svg') ? 'png' : f.split('.').pop(),
            data: fs.readFileSync(path.join(imgDir, f)),
            transformation: { width: 500, height: 300 }
          })]
        })
      ]).flat()
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('C:\\Users\\dugao\\Desktop\\<网站名>官网图片.docx', buf);
  console.log('文档已生成');
});
```

## 注意事项

### 图片处理规则

| 场景 | 处理方式 |
|------|---------|
| 图片 URL 是相对路径 | 拼接 `https://域名` 补全 |
| 图片格式不支持（.gif 动画） | 仅下载静态帧 |
| 图片过大（> 10MB） | 下载后提示用户，照常嵌入文档 |
| 图片下载失败 | 跳过，继续下载下一张，最后汇总报告 |
| SVG 格式 | 下载但嵌入 DOCX 时需转为 PNG（参考 docx-js.md） |

### 文档排版建议

- 每张图片单独一页，配文件名和序号
- 图片宽高比保持原样，宽度不超过 500px
- 首页加标题和生成时间
- 页脚加页码

### 限制说明

- 本 Skill 只能获取**公开可访问**的网页资源，无法处理需要登录认证的网站
- 部分网站使用 JavaScript 动态渲染图片，可能无法抓取到全部资源
- 遵守目标网站的 `robots.txt` 和使用条款

## 易错点

1. **相对路径未补全**：图片 URL 可能是 `/assets/xxx.jpg` 而非 `https://domain/assets/xxx.jpg`，必须先补全
2. **文件名冲突**：不同图片可能同名，下载时用序号前缀避免覆盖
3. **编码问题**：PowerShell 脚本中包含中文路径时可能报错，建议使用纯英文路径
4. **DOCX 图片嵌入**：`ImageRun` 必须指定 `type` 参数，`transformation` 中 width/height 单位是像素