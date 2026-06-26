# Design-to-HTML Skill

将视觉设计稿转换为像素级精准的 HTML/CSS 代码。

## 安装依赖

```bash
cd ~/.openclaw/skills/design-to-html
npm install
```

如果遇到 puppeteer 安装问题：

```bash
# 安装 puppeteer 时跳过 chromium（使用系统已安装的）
npm install puppeteer --puppeteer_skip_download=true

# 或使用更轻量的替代方案
npm install playwright sharp pixelmatch pngjs
```

## 使用方法

### 基础用法

```
用户：帮我把这个设计图转成 HTML 代码
（上传图片）

Agent：分析图片 -> 生成 HTML -> 渲染对比 -> 优化迭代
```

### 命令行测试

```bash
# 分析设计图
node scripts/analyze.js design.png analysis.json

# 渲染 HTML
node scripts/render.html iteration_1.html rendered_1.png --width 1920 --height 1080

# 对比差异
node scripts/compare.js design.png rendered_1.png diff_1.png

# 运行完整流程
node scripts/pipeline.js design.png --threshold 95 --iterations 5 --output-dir ./output
```

## 工作流程

1. **分析设计图** - 提取尺寸、颜色、布局信息
2. **生成初始 HTML** - 基于分析结果创建基础代码
3. **渲染对比** - 截图并与原图像素级对比
4. **优化迭代** - 根据差异报告改进 HTML（至少5次）
5. **输出结果** - 最终 HTML + 对比报告

## 示例案例

见 `references/examples/` 目录：

- button-example.md - 简单按钮组件
- card-example.md - 卡片布局
- layout-example.md - 完整页面

## 输出文件

- `analysis.json` - 设计分析报告
- `iteration_*.html` - 各轮迭代的 HTML
- `rendered_*.png` - 渲染截图
- `diff_*.png` - 差异可视化
- `comparison_report.md` - 最终对比报告
- `final.html` - 最优版本