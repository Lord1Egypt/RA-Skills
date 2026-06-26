---
name: figma-design-analyzer
description: 分析Figma设计文件，提取设计系统数据（颜色、字体、间距、组件），导出截图，并与实际实现进行比对验证。使用JavaScript/Node.js实现，当用户需要处理Figma设计文件、提取设计规范、导出设计资源或验证设计实现时使用此技能。
compatibility: 需要Node.js 20+，通过FIGMA_ACCESS_TOKEN环境变量提供Figma个人访问令牌。
---

# Figma设计分析技能 (JavaScript版)

使用Node.js分析Figma设计文件，提取设计系统，导出资源，验证实现一致性。

## 快速开始

1. **设置令牌**：
   ```bash
   export FIGMA_ACCESS_TOKEN=your_figma_token
   ```

2. **安装Node.js依赖**：
   ```bash
   npm install  # 或 yarn install
   ```
   

3. **使用技能**：
   - 在Claude中：直接描述您的Figma分析需求
   - 命令行：`node scripts/figma-cli.js --help`

## 核心功能

### 1. 文件信息获取
获取Figma文件的完整结构和元数据：
```bash
node scripts/figma-cli.js info "文件ID或URL"
```

### 2. 设计属性提取
提取颜色、字体、间距、组件等设计系统数据：
```bash
node scripts/figma-cli.js extract "文件ID" --output design-system.json
```

### 3. 截图导出
导出设计节点的PNG/JPG截图：
```bash
node scripts/figma-cli.js export "文件ID" --node-id "节点ID" --format png
```

### 4. 比对验证
将实际实现（CSS/代码）与设计进行比对：
```bash
node scripts/figma-cli.js compare "文件ID" implementation.css --output report.json
```

## 输出格式

- **JSON**：机器可读的结构化数据（默认）
- **HTML**：可视化比对报告
- **PNG/JPG**：设计截图

## 错误处理

- 验证FIGMA_ACCESS_TOKEN环境变量
- 检查文件访问权限
- 处理API限制和网络错误
- 提供明确的错误信息和解决建议

## 示例用例

1. **设计系统文档生成**：提取所有设计规范
2. **开发资源准备**：批量导出图标和组件截图  
3. **实现质量检查**：比对CSS与设计一致性
4. **设计评审**：分析设计规范遵循情况

## 下一步

1. 设置您的FIGMA_ACCESS_TOKEN
2. 提供Figma文件URL或ID
3. 描述您的具体需求

技能会自动处理分析并生成结果。