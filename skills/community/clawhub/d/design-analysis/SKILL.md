# Design Analysis Skill

自动化设计分析工具，用于分析设计素材（截图、设计稿）并生成结构化的HTML演示文档。

## When to Use

- 需要对设计素材（截图、设计稿）进行结构化分析时
- 需要生成图文并茂的HTML演示文档时
- 需要按照章节分页展示设计分析内容时
- 希望固化「设计分析 + HTML生成」的工作流程时

## How to Use

### 基本用法

```javascript
// 分析文件夹中的设计素材并生成HTML
const result = await designAnalysis({
  inputFolder: "~/Desktop/01.DesignAnalysis",
  outputFile: "~/Desktop/design_analysis.html",
  title: "设计分析报告",
  dimensions: { width: 1920, height: 1280 },
  layout: { textWidth: 30, imageWidth: 70 }
});
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `inputFolder` | string | ✅ | 包含设计素材的文件夹路径 |
| `outputFile` | string | ✅ | 输出的HTML文件路径 |
| `title` | string | ❌ | 演示文档标题（默认：设计分析演示） |
| `dimensions` | object | ❌ | 页面尺寸 {width, height}（默认：1920×1280） |
| `layout` | object | ❌ | 布局比例 {textWidth, imageWidth}（默认：30/70） |
| `sections` | array | ❌ | 自定义章节配置（不传则自动生成） |

### 自定义章节

```javascript
const result = await designAnalysis({
  inputFolder: "~/Desktop/design",
  outputFile: "~/Desktop/analysis.html",
  sections: [
    {
      title: "设计概览",
      tags: ["UI/UX", "设计系统"],
      content: "<h2>项目背景</h2><p>...</p>",
      image: "screenshot1.png"
    },
    // ... 更多章节
  ]
});
```

### 返回值

```typescript
{
  success: boolean,
  outputPath: string,
  totalPages: number,
  analysis: {
    fileCount: number,
    imageFiles: string[],
    sections: string[]
  }
}
```

## Examples

### 示例1：基础使用

```javascript
const result = await designAnalysis({
  inputFolder: "~/Desktop/01.DesignAnalysis",
  outputFile: "~/Desktop/DESIGN_ANALYSIS_DEMO.html"
});
```

### 示例2：自定义尺寸和布局

```javascript
const result = await designAnalysis({
  inputFolder: "~/Desktop/design_materials",
  outputFile: "~/Desktop/presentation.html",
  title: "产品设计方案",
  dimensions: { width: 1920, height: 1080 },
  layout: { textWidth: 25, imageWidth: 75 }
});
```

## Features

- ✅ 自动扫描文件夹中的图片文件（支持 PNG、JPG、JPEG、GIF）
- ✅ 智能分析图片内容（基于文件名和时间戳）
- ✅ 生成多章节HTML演示文档
- ✅ 30/70 分栏布局（文字/图片）
- ✅ 侧边导航点和底部控制栏
- ✅ 键盘方向键支持
- ✅ 平滑翻页动画
- ✅ 响应式设计（移动端适配）
- ✅ 可自定义页面尺寸和布局比例
- ✅ 支持自定义章节内容

## Output Structure

生成的HTML包含：

```
├── Navigation Dock（右侧导航点）
├── Page Controls（底部翻页控制）
├── Pages Container（页面容器）
│   ├── Page 1（章节1）
│   │   ├── Text Section (30% - 左侧)
│   │   └── Image Section (70% - 右侧)
│   ├── Page 2（章节2）
│   └── ...
└── JavaScript（交互逻辑）
```

## Customization

可以通过参数自定义：
- **尺寸**：支持任意分辨率的固定尺寸
- **布局**：文字区和图片区的宽度比例
- **主题色**：修改CSS中的渐变色值
- **字体**：调整字体家族和大小
- **动画**：修改动画时长和效果

## Limitations

- 仅支持本地图片文件（不支持URL）
- 图片路径使用绝对路径，跨机器分享需调整
- 单页最大高度1280px（可根据需要调整）
- 图片自动缩放，保持原始比例

## Troubleshooting

### 图片不显示
- 检查图片路径是否正确
- 确认图片文件是否存在
- 查看浏览器控制台错误信息

### 页面空白
- 检查HTML文件是否完整写入
- 确认浏览器支持ES6语法
- 尝试在不同浏览器中打开

## See Also

- [HTML5 Presentation Patterns](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Using_HTML5)
- [CSS Flexbox Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)