# DeepSeek API Toolkit 🚀

> DeepSeek API 开发工具箱 — 成本优化、Prompt工程、集成模板一站式搞定

## 什么时候用这个 Skill？

当用户提到以下任何情况时激活：
- 使用 / 接入 DeepSeek API
- DeepSeek 模型（V3、V4 Pro、Reasonix、R1）
- AI API 成本优化
- 国产大模型集成
- 对比 DeepSeek vs OpenAI / Claude
- DeepSeek Prompt 优化

## 使用模式

### 模式 1：API 接入指南 🔌
用户想接入 DeepSeek API，提供完整接入方案。

**执行步骤：**
1. 读取 `deepseek-api-guide.md` 获取最新 API 端点和参数
2. 根据用户的技术栈（Python/Node.js/Java/curl）生成对应代码
3. 包含错误处理、重试逻辑、流式输出
4. 提供 API Key 配置最佳实践

**输出格式：**
```markdown
## DeepSeek API 接入方案

### 端点信息
- Base URL: https://api.deepseek.com
- 模型选择: [根据需求推荐]
- 预估成本: [token 计算]

### 代码示例
[对应语言的完整代码]

### 注意事项
[错误处理、限流、最佳实践]
```

### 模式 2：成本优化顾问 💰
用户想降低 DeepSeek API 使用成本。

**执行步骤：**
1. 读取 `cost-optimization.md` 获取成本优化策略
2. 分析用户当前使用场景
3. 从 5 个维度给出优化建议：

| 维度 | 策略 |
|------|------|
| 模型选择 | V4 Pro vs V3 vs R1，按任务类型推荐 |
| Prompt 缓存 | 利用 DeepSeek 的前缀缓存机制 |
| 批处理 | 合并请求、减少 API 调用次数 |
| Token 管理 | 精简 Prompt、控制系统输出长度 |
| 上下文优化 | 多轮对话的上下文裁剪策略 |

**输出格式：**
```markdown
## 成本优化报告

### 当前方案分析
- 月调用量: [估算]
- 月成本: [估算]
- 主要成本来源: [分析]

### 优化建议（按收益排序）
1. [最大收益的优化]
2. [次要优化]
3. [长期优化]

### 优化后预估
- 月成本: [新估算]
- 节省比例: [百分比]
```

### 模式 3：Prompt 工程专家 🎯
用户想优化给 DeepSeek 的 Prompt。

**执行步骤：**
1. 读取 `prompt-engineering.md` 获取 DeepSeek 特有的 Prompt 技巧
2. 分析用户当前 Prompt 的问题
3. 应用 DeepSeek 优化框架：

```
原 Prompt → 问题诊断 → 优化 Prompt → 效果对比
```

**DeepSeek Prompt 优化要点：**
- DeepSeek 对 system prompt 的响应比 ChatGPT 更敏感
- 中文场景用中文 system prompt 效果更好
- V4 Pro 的推理能力可通过"思考链"提示充分激活
- R1 系列自带推理，不需要额外的 CoT 提示
- 利用 JSON mode 获取结构化输出

### 模式 4：模型选型顾问 🔍
用户不确定该用 DeepSeek 哪个模型。

**执行步骤：**
1. 读取 `model-comparison.md` 获取模型对比数据
2. 了解用户的使用场景
3. 给出推荐方案

**决策树：**
```
需要推理/数学/编码？
  ├─ 是 → Reasonix（最强推理）或 R1（轻量推理）
  └─ 否 → 需要最高质量？
              ├─ 是 → V4 Pro（综合最强，降价后性价比极高）
              └─ 否 → V3（最便宜，日常对话/翻译/摘要够用）
```

## 文件结构

```
deepseek-toolkit/
├── SKILL.md                    # 本文件 — 使用指南
├── deepseek-api-guide.md       # API 端点、参数、代码模板
├── cost-optimization.md        # 成本优化策略库
├── prompt-engineering.md       # Prompt 工程技巧
├── model-comparison.md         # 模型对比与选型指南
└── README.md                   # 产品介绍
```

## 注意事项

1. **API 价格动态变化** — DeepSeek 的定价策略更新频繁（2025年5月 V4 Pro 降价 75%），每次使用时提醒用户确认最新价格
2. **兼容性** — DeepSeek API 兼容 OpenAI SDK 格式，可以复用大部分 OpenAI 生态工具
3. **限流策略** — DeepSeek 有请求频率限制，高并发场景需要做队列和重试
4. **数据合规** — DeepSeek 服务器在中国大陆，涉及敏感数据时需评估合规性
5. **缓存利用** — DeepSeek 的 Prompt 缓存命中率直接影响成本，优化 system prompt 结构可显著降低费用
