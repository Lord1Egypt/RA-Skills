# Content Pipeline Skill

## 描述

这个 Skill 提供了一个完整的内容生成 pipeline：
**搜索信息 → 整理数据 → 生成脚本 → 生成数字人视频**

## 何时使用

当用户要求：
- "帮我生成一个关于 X 的视频脚本"
- "我想要一个数字人视频讲解 X"
- "帮我整理 X 的信息并生成脚本"
- "创建一个关于 X 的内容"

## 功能

### 1. 信息搜索和整理
- 从多个来源搜索信息
- 自动提取关键点
- 结构化数据组织

### 2. 脚本生成
- 支持多种风格 (分析、故事、教育)
- 自动时长分配
- 多格式输出 (Markdown, JSON)

### 3. 数字人视频生成
- 支持 HeyGen, D-ID, Synthesia
- 自动 API 调用
- 视频下载和处理

## 使用示例

### 基础用法
```bash
node pipeline.js --topic "人工智能的未来" --style "analysis"
```

### 指定提供商
```bash
node pipeline.js --topic "气候变化" --provider "d-id" --style "educational"
```

### 自定义输出
```bash
node pipeline.js --topic "区块链" --output "./my-videos" --style "story"
```

## 输出

Pipeline 会生成以下文件：

```
output/[timestamp]/
├── 01-search-results.json      # 搜索结果
├── 02-organized-data.json      # 整理后的数据
├── 03-script.md                # Markdown 脚本
├── 03-script.json              # JSON 脚本
├── 04-video-result.json        # 视频生成结果
└── REPORT.json                 # 完整报告
```

## 配置

### 环境变量

```bash
# 数字人 API Keys
export AVATAR_API_KEY="your-api-key"
export HEYGEN_API_KEY="your-heygen-key"
export DID_API_KEY="your-d-id-key"
export SYNTHESIA_API_KEY="your-synthesia-key"
```

### 脚本模板

支持的风格：
- `analysis` - 深度分析型
- `story` - 故事型
- `educational` - 教育型

## 扩展

### 添加新的脚本风格

编辑 `script-generator.js` 中的 `SCRIPT_TEMPLATES`：

```javascript
SCRIPT_TEMPLATES['my-style'] = {
  intro: '...',
  body: '...',
  conclusion: '...'
};
```

### 添加新的数字人提供商

编辑 `avatar-generator.js` 中的 `generateWithProvider` 方法。

### 集成新的搜索源

编辑 `pipeline.js` 中的 `searchInformation` 方法。

## 故障排除

### 网络搜索不可用
- 使用本地数据或用户输入
- 集成飞书知识库
- 使用 curl/wget 备选方案

### 数字人 API 失败
- 检查 API Key 是否正确
- 验证网络连接
- 查看 API 文档

### 脚本质量不佳
- 调整脚本模板
- 改进数据整理逻辑
- 添加 AI 内容增强

## 文件结构

```
content-pipeline/
├── script-generator.js         # 脚本生成引擎
├── data-organizer.js           # 数据整理工具
├── avatar-generator.js         # 数字人视频生成
├── pipeline.js                 # 主 pipeline
├── SKILL.md                    # 本文件
└── examples/
    ├── sample-data.json        # 示例数据
    └── sample-script.json      # 示例脚本
```

## 许可证

MIT

## 支持

如有问题，请查看日志文件或联系开发者。

