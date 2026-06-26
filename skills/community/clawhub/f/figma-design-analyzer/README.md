# Figma Design Analyzer Skill

一个Claude Code技能，用于分析Figma设计文件、提取设计系统、导出截图和验证设计实现一致性。

## 功能特性

### 🎨 设计系统提取
- **颜色提取**: 自动提取设计中的所有颜色值（HEX、RGB、RGBA）
- **字体分析**: 提取字体家族、大小、字重、行高等属性
- **间距尺度**: 分析间距、尺寸和布局网格系统
- **组件识别**: 识别和分类设计组件

### 📸 截图导出
- **节点截图**: 导出任意设计节点的PNG/JPG截图
- **批量导出**: 支持批量导出多个组件或页面
- **多倍缩放**: 支持0.5x, 1x, 2x, 3x, 4x缩放
- **格式转换**: 自动处理图片格式转换

### 🔍 比对验证
- **设计一致性检查**: 比对CSS/代码实现与Figma设计
- **差异报告**: 生成详细的比对报告和改进建议
- **通过率统计**: 计算设计实现的一致性通过率
- **可视化报告**: 生成HTML格式的可视化比对报告

### 📊 文件信息
- **元数据获取**: 获取文件基本信息、版本历史
- **结构分析**: 分析页面、画板、组件结构
- **协作信息**: 查看评论和协作状态

## 安装使用

### 前提条件
1. **Node.js 20+**: 确保已安装Node.js 20或更高版本
2. **Figma访问令牌**: 从Figma账户设置中获取个人访问令牌

项目包含 `.env.example` 文件，复制为 `.env` 并填写您的令牌即可：
```bash
cp .env.example .env
# 编辑 .env 文件，将 FIGMA_ACCESS_TOKEN 替换为您的实际令牌
```

### 安装步骤

#### 方法一：通过skills仓库安装（推荐）
```bash
# 使用npx从skills仓库安装
npx skills add yourusername/agent-skills/figma-design-analyzer
```

#### 方法二：手动安装
```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/agent-skills.git
cd agent-skills/skills/figma-design-analyzer

# 2. 安装依赖
npm install

# 3. 设置环境变量
# 方法A：使用环境变量文件（推荐）
cp .env.example .env
# 编辑 .env 文件，填写您的 FIGMA_ACCESS_TOKEN

# 方法B：直接设置环境变量
export FIGMA_ACCESS_TOKEN=your_figma_personal_access_token

# 4. 测试安装
npm test
```

#### 方法三：在Claude Code中直接使用
1. 确保技能目录位于 `~/.claude/skills/figma-design-analyzer/`
2. Claude会自动检测并加载技能

## 快速开始

### 1. 设置环境变量
```bash
# 推荐：使用环境变量文件
cp .env.example .env
# 编辑 .env 文件，填写您的 FIGMA_ACCESS_TOKEN

# 或使用传统方式：
# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export FIGMA_ACCESS_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc

# 临时设置
export FIGMA_ACCESS_TOKEN=your_token_here
```

### 2. 使用命令行工具
```bash
# 查看帮助
node scripts/figma-cli.js --help

# 获取文件信息
node scripts/figma-cli.js info "https://figma.com/file/abc123"

# 提取设计系统
node scripts/figma-cli.js extract "文件ID" --output design-system.json

# 导出截图
node scripts/figma-cli.js export "文件ID" --node-id "节点ID" --format png --scale 2

# 比对验证
node scripts/figma-cli.js compare "文件ID" styles.css --output report.json
```

### 3. 在Claude中使用
在Claude对话中直接描述您的需求：
- "分析这个Figma文件：https://figma.com/file/abc123"
- "提取这个设计的所有颜色和字体"
- "导出按钮组件的截图"
- "检查我的CSS是否与设计一致"

## API参考

### 命令行参数

#### `info` - 获取文件信息
```bash
node scripts/figma-cli.js info <file_url_or_id> [--output <path>]
```

#### `extract` - 提取设计系统
```bash
node scripts/figma-cli.js extract <file_url_or_id> [--output <path>]
```

#### `export` - 导出截图
```bash
node scripts/figma-cli.js export <file_url_or_id> --node-id <id> [--format png|jpg] [--scale <number>] [--output <path>]
```

#### `compare` - 比对验证
```bash
node scripts/figma-cli.js compare <file_url_or_id> <implementation_path> [--output <path>]
```

### 输出格式

技能支持多种输出格式：

#### JSON输出（默认）
```json
{
  "file_id": "abc123",
  "summary": {
    "total_colors": 24,
    "total_fonts": 8,
    "pass_rate": 85
  },
  "details": {
    "colors": [...],
    "fonts": [...]
  }
}
```

#### HTML报告
生成可视化的比对报告，包含：
- 通过率图表
- 详细差异列表
- 改进建议
- 颜色对比可视化

#### 图片文件
- PNG格式截图
- JPG格式截图
- 多倍缩放支持

## 开发指南

### 项目结构
```
figma-design-analyzer/
├── SKILL.md                    # 技能定义文件
├── README.md                   # 项目说明
├── package.json               # 依赖配置
├── scripts/
│   ├── figma-cli.js           # 命令行入口
│   ├── test-runner.js         # 测试运行器
│   ├── modules/
│   │   ├── file-info.js       # 文件信息模块
│   │   ├── design-extractor.js # 设计提取模块
│   │   ├── screenshot-exporter.js # 截图导出模块
│   │   └── design-comparator.js # 比对验证模块
│   └── test-data/             # 测试数据
├── evals/
│   └── evals.json             # 评估测试用例
├── references/                # 参考文档
└── assets/                    # 静态资源
```

### 运行测试
```bash
# 运行所有测试
npm test

# 或直接运行测试脚本
node scripts/test-runner.js

# 运行特定测试
node scripts/test-runner.js --test file-info
```

### 扩展开发

#### 添加新功能模块
1. 在 `scripts/modules/` 目录创建新模块
2. 实现功能逻辑
3. 在 `figma-cli.js` 中添加对应的命令
4. 更新 `SKILL.md` 文档

#### 修改设计提取逻辑
编辑 `scripts/modules/design-extractor.js`：
- 修改 `traverseNode` 函数添加新的属性提取
- 更新 `extractDesignSystem` 函数修改输出结构

#### 自定义比对规则
编辑 `scripts/modules/design-comparator.js`：
- 修改 `compareDesignSystems` 函数添加新的比对维度
- 更新 `generateRecommendations` 函数自定义建议逻辑

## 配置选项

### 环境变量
| 变量名 | 必填 | 描述 | 示例 |
|--------|------|------|------|
| `FIGMA_ACCESS_TOKEN` | 是 | Figma个人访问令牌 | `figd_xxxxxxxxxxxx` |
| `FIGMA_EXPORT_DIR` | 否 | 截图导出目录 | `./exports` |
| `FIGMA_API_TIMEOUT` | 否 | API请求超时(ms) | `30000` |

### 性能优化
对于大型设计文件：
```bash
# 增加内存限制
export NODE_OPTIONS="--max-old-space-size=4096"

# 设置API超时
export FIGMA_API_TIMEOUT=60000
```

## 常见问题

### Q: 获取 "认证失败" 错误
A: 确保 `FIGMA_ACCESS_TOKEN` 环境变量已正确设置，且令牌未过期。

### Q: 截图导出失败
A: 检查节点ID是否正确，以及是否有访问权限。某些节点可能不支持截图导出。

### Q: 比对结果不准确
A: CSS解析基于简单规则，对于复杂CSS可能需要手动调整。可考虑使用专门的CSS解析库改进。

### Q: API限制错误
A: Figma API有调用频率限制。建议：
1. 添加延迟处理
2. 缓存结果
3. 分批处理大型文件

### Q: 技能未触发
A: 确保技能目录位于正确位置，且 `SKILL.md` 中的描述包含相关关键词。

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 开发规范
- 使用ES6+语法
- 添加JSDoc注释
- 编写单元测试
- 更新相关文档

## 许可证

MIT License

## 支持

- 提交Issue: [GitHub Issues](https://github.com/yourusername/agent-skills/issues)
- 文档: [技能文档](./references/)
- 示例: [测试用例](./evals/evals.json)

---

**提示**: 对于生产环境使用，建议：
1. 设置API调用限制和重试逻辑
2. 添加结果缓存机制
3. 实现增量同步功能
4. 集成到CI/CD流水线中