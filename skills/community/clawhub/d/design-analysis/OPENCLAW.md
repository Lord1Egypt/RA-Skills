# Design Analysis Skill - OpenClaw集成指南

## 技能概览

本技能将「设计素材分析 + HTML演示生成」的工作流程固化为OpenClaw技能。

**核心功能**:
1. 扫描指定文件夹中的设计素材（图片文件）
2. 自动分析设计特点并生成结构化内容
3. 生成交互式HTML演示文档（支持翻页、导航）

## 使用方法

### 方法一: 自然语言指令

在OpenClaw对话中直接说:

> 请分析 ~/Desktop/01.DesignAnalysis 文件夹中的设计素材，生成一个HTML演示文档。

或更具体:

> 帮我分析 ~/Desktop/mydesign 文件夹，生成1920×1080尺寸的HTML演示，标题为"产品设计方案"。

### 方法二: 显式调用（开发测试）

```javascript
// 在OpenClaw开发环境中
const result = await require('~/.openclaw/workspace/skills/design-analysis/run.js').run({
  input_folder: "~/Desktop/01.DesignAnalysis",
  output_file: "~/Desktop/output.html",
  title: "设计分析报告",
  dimensions: { width: 1920, height: 1280 },
  layout: { textWidth: 30, imageWidth: 70 }
});
```

## 参数详解

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `input_folder` | string | ✅ | - | 设计素材文件夹路径（必须包含图片） |
| `output_file` | string | ✅ | - | 输出HTML文件路径 |
| `title` | string | ❌ | "设计分析演示" | 文档标题 |
| `dimensions.width` | number | ❌ | 1920 | 页面宽度(px) |
| `dimensions.height` | number | ❌ | 1280 | 页面高度(px) |
| `layout.textWidth` | number | ❌ | 30 | 文字区域宽度百分比 |
| `layout.imageWidth` | number | ❌ | 70 | 图片区域宽度百分比 |
| `sections` | array | ❌ | auto | 自定义章节数组（不传则自动生成） |

## 自动生成的章节结构

如果不传 `sections` 参数，技能会根据图片数量自动生成以下章节:

1. **设计分析总览** - 项目概述、素材清单、分析维度
2. **视觉层次分析** - 排版系统、标题层级、强调元素
3. **色彩与布局系统** - 主题色、色彩规范、布局结构、间距圆角
4. **交互与动效** - 翻页机制、动效设计、响应式适配、可用性考虑

每章会自动关联一张图片（按文件时间顺序）。

## 自定义章节

通过 `sections` 参数可以完全自定义章节内容和图片映射:

```javascript
const mySections = [
  {
    title: "第一章：设计概览",
    tags: ["UI", "UX"],
    content: "<h2>项目背景</h2><p>详细描述...</p>",
    image: "screenshot1.png"  // 文件名，相对于 input_folder
  },
  {
    title: "第二章：色彩分析",
    tags: ["配色"],
    content: "<h2>色彩系统</h2><p>...</p>",
    image: "screenshot2.png"
  }
];

await run({
  input_folder: "~/Desktop/mydesign",
  output_file: "~/Desktop/custom.html",
  sections: mySections
});
```

每章的 `content` 字段是HTML字符串，支持所有HTML标签和内联样式。

## 输出文件

生成的HTML文件是完全独立的，包含:
- 所有CSS样式（内联在 `<style>` 中）
- 交互JavaScript（底部 `<script>`）
- 图片使用相对路径引用

**打开方式**:
- 直接双击HTML文件在浏览器中打开
- 或拖拽到浏览器窗口
- 支持Chrome、Firefox、Safari、Edge等现代浏览器

## 使用场景

- **设计评审** - 将设计稿整理成演示文档，便于团队评审
- **方案展示** - 向客户或利益相关者展示设计方案
- **设计归档** - 将设计决策和分析记录下来
- **设计系统** - 分析并展示设计系统的各个组成部分
- **个人笔记** - 整理学习的设计案例

## 注意事项

1. **图片路径**: HTML中的图片路径是相对路径，确保 `output_file` 和 `input_folder` 的相对关系正确。建议将HTML输出到父目录:

   ```
   正确:
   input_folder: ~/Desktop/01.DesignAnalysis
   output_file:  ~/Desktop/DESIGN_ANALYSIS.html
   
   这样HTML中图片路径为: 01.DesignAnalysis/xxx.png
   ```

2. **文件数量**: 自动生成模式下，至少需要1张图片；自定义模式下，每章的image字段必须对应实际存在的文件。

3. **浏览器兼容**: 使用了CSS Grid、Flexbox、ES6等现代特性，需要现代浏览器支持。

4. **性能**: 大量高分辨率图片可能导致页面加载缓慢，建议单页图片不超过3000px尺寸。

## 示例会话

```
用户: 请分析我的设计素材，生成演示文档
AI: 好的，请提供设计素材文件夹路径

用户: ~/Desktop/01.DesignAnalysis
AI: 正在分析... ✓ 发现2个图片文件
   生成章节: 设计总览 → 视觉层次 → 色彩系统
   输出文件: ~/Desktop/DESIGN_ANALYSIS.html
   完成！
```

## 故障排除

### HTML中图片不显示
- 检查文件路径是否正确
- 在浏览器中右键"检查"，查看Network标签
- 确认图片文件确实存在于指定位置

### 生成失败
- 检查输入文件夹是否存在
- 确认文件夹内至少有一个支持的图片格式
- 检查输出路径是否有写入权限

### 页面样式异常
- 清除浏览器缓存后重试
- 确认浏览器版本较新（支持ES6）

## 进阶使用

### 与其他技能配合

可以和以下技能组合使用:
- `feishu-create-doc` - 生成后自动上传到飞书文档
- `feishu-im-user-message` - 发送给团队成员
- `cron` - 定时自动生成设计日报

### 批量处理

如果需要批量处理多个设计文件夹:

```javascript
const folders = [
  "~/Desktop/design1",
  "~/Desktop/design2",
  "~/Desktop/design3"
];

for (const folder of folders) {
  const name = path.basename(folder);
  await run({
    input_folder: folder,
    output_file: `~/Desktop/${name}_analysis.html`,
    title: `${name} - 设计分析`
  });
}
```

## 版本历史

- **v1.0.0** (2026-03-11)
  - 初始版本发布
  - 支持自动图片扫描和章节生成
  - 支持自定义尺寸和布局
  - 支持完全自定义章节
  - 完整的交互式HTML输出