# Design Analysis Skill

自动化设计分析工具，用于分析设计素材（截图、设计稿）并生成结构化的HTML演示文档。

## 快速开始

### 1. 技能结构

技能位于: `~/.openclaw/workspace/skills/design-analysis/`

包含文件:
- `index.js` - 核心逻辑（设计分析与HTML生成）
- `run.js` - OpenClaw调用接口
- `SKILL.md` - 详细技能文档
- `package.json` - 技能配置
- `README.md` - 本文件

### 2. 测试技能

```bash
# 直接运行测试
node run.js ~/Desktop/01.DesignAnalysis ~/Desktop/DESIGN_ANALYSIS.html "设计分析报告"
```

### 3. 在OpenClaw中使用

OpenClaw会自动加载 `~/.openclaw/workspace/skills/` 目录下的所有技能。

在对话中可以直接使用:

```
请分析 ~/Desktop/01.DesignAnalysis 文件夹中的设计素材，并生成HTML演示文档。
```

OpenClaw会调用此技能完成任务。

### 3. 参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input_folder` | string | ✅ | 包含设计素材的文件夹路径 |
| `output_file` | string | ✅ | 输出的HTML文件路径 |
| `title` | string | ❌ | 演示文档标题（默认：设计分析演示） |
| `dimensions` | object | ❌ | 页面尺寸 {width, height}（默认：1920×1280） |
| `layout` | object | ❌ | 布局比例 {textWidth, imageWidth}（默认：30/70） |
| `sections` | array | ❌ | 自定义章节配置数组 |
| `context` | object | ❌ | OpenClaw上下文信息 |

### 4. 自定义章节

不传 `sections` 参数时，工具会自动分析图片文件并生成默认章节（概览 → 视觉层次 → 色彩系统 → 交互设计）。

传入 `sections` 可完全自定义章节内容：

```javascript
const customSections = [
  {
    title: "第一章",
    tags: ["标签1", "标签2"],
    content: "<h2>标题</h2><p>内容...</p>",
    image: "图片文件名.png"
  },
  // ...
];
```

### 5. 输出结构

生成的HTML文件包含：

- ✅ 固定尺寸画布（默认1920×1280）
- ✅ 30/70分栏布局（左侧文字 + 右侧图片）
- ✅ 侧边导航点（右侧圆形导航）
- ✅ 底部翻页控制（上一页/下一页 + 页码）
- ✅ 键盘方向键支持
- ✅ 平滑翻页动画
- ✅ 响应式设计（移动端适配）
- ✅ 图片自动缩放和容错

## 技术细节

### 核心功能

1. **扫描素材文件夹**
   - 自动识别图片文件（.png, .jpg, .jpeg, .gif, .webp）
   - 按修改时间排序（最新的在前）

2. **章节生成**
   - 根据图片数量自动生成分析章节
   - 每章对应一张图片（按顺序）
   - 提供设计分析的标准内容模板

3. **HTML构建**
   - 使用模板字符串生成完整HTML
   - 嵌入所有样式和JavaScript
   - 支持绝对图片路径

4. **文件输出**
   - 确保输出目录存在
   - 写入UTF-8编码的HTML文件

### 图片路径处理

HTML中使用相对路径指向图片文件，假设HTML文件与图片在同一目录结构下。例如:

```
Desktop/
├── DESIGN_ANALYSIS.html
└── 01.DesignAnalysis/
    ├── 截屏1.png
    └── 截屏2.png
```

HTML中图片路径为: `01.DesignAnalysis/截屏1.png`

**注意**: 如果需要跨机器分享，需要调整图片路径或使用本地服务器。

## 示例

### 示例1: 基础使用

```bash
node run.js ~/Desktop/design_materials ~/Desktop/presentation.html
```

### 示例2: 自定义标题和尺寸

```bash
node run.js ~/Desktop/design_materials ~/Desktop/presentation.html "产品设计方案" --dimensions=1920,1080
```

（需要扩展 `run.js` 支持命令行参数解析）

## 与其他技能的集成

此技能可以作为设计工作流的一部分：

1. **设计整理** - 先整理设计素材到文件夹
2. **素材分析** - 使用本技能生成分析文档
3. **方案分享** - 将HTML发送给团队或客户

## 故障排除

### 图片不显示

- 检查图片路径是否正确
- 确认HTML文件与图片的相对路径关系
- 在浏览器中打开开发者工具查看网络请求

### 页面空白

- 确认输出文件已完整写入
- 检查浏览器控制台是否有错误
- 确认图片文件存在且格式正确

## License

MIT