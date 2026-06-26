---
name: enhanced-search
description: "增强的智能搜索能力，优化搜索结果并提供摘要。类似Tavily Web Search的功能，但基于现有web_search工具构建。"
metadata:
  author: 袭人 (Xi Ren)
  version: 1.0.0
  created: 2026-03-12
---

# 🔍 Enhanced Search Skill

基于OpenClaw现有web_search工具的增强搜索能力，提供优化结果和智能摘要。

## 功能特点

### 🎯 核心功能
1. **智能搜索优化**：自动优化搜索查询，提高结果相关性
2. **结果摘要生成**：对搜索结果进行摘要，节省阅读时间
3. **多源整合**：整合多个搜索结果，提供全面信息
4. **上下文感知**：根据对话上下文调整搜索策略

### 📊 与web_search的区别
| 功能 | web_search | enhanced-search |
|------|-----------|----------------|
| 基础搜索 | ✅ | ✅ |
| 结果优化 | ❌ | ✅ |
| 自动摘要 | ❌ | ✅ |
| 多源整合 | ❌ | ✅ |
| 上下文感知 | ❌ | ✅ |

## 使用方法

### 基本搜索
```
搜索 [查询内容]
```

### 带上下文的搜索
```
帮我了解 [主题]，我需要 [具体信息]
```

### 深度搜索
```
深度搜索 [复杂查询]，需要详细信息和来源
```

## 实现原理

### 架构设计
```
用户查询 → 查询优化 → 并行搜索 → 结果整合 → 摘要生成 → 格式化输出
```

### 技术栈
- **基础工具**：OpenClaw web_search
- **优化算法**：查询扩展、关键词提取
- **摘要模型**：基于规则的摘要生成
- **整合逻辑**：多结果去重和排序

## 配置选项

### 环境变量（可选）
```bash
# 搜索优化级别
export ENHANCED_SEARCH_OPTIMIZATION=high  # low|medium|high

# 摘要长度
export ENHANCED_SEARCH_SUMMARY_LENGTH=medium  # short|medium|long

# 结果数量
export ENHANCED_SEARCH_RESULT_COUNT=5  # 1-10
```

### 配置文件
创建 `~/.openclaw/workspace/config/enhanced-search.json`：
```json
{
  "optimization": "high",
  "summary": true,
  "max_results": 5,
  "sources": ["web", "docs", "memory"],
  "cache_ttl": 3600
}
```

## 示例

### 示例1：基础搜索
**用户输入**：搜索"鸿蒙智行最新动态"

**处理流程**：
1. 优化查询："鸿蒙智行 最新消息 2026 动态"
2. 执行搜索：调用web_search
3. 生成摘要：提取关键信息
4. 格式化输出：结构化展示结果

### 示例2：上下文搜索
**对话上下文**：用户之前问了关于问界M7的问题

**用户输入**：搜索"智能驾驶技术"

**处理流程**：
1. 结合上下文：优化为"问界M7 智能驾驶技术 最新进展"
2. 执行搜索
3. 生成针对性摘要
4. 突出与问界M7相关的信息

## 性能优化

### 缓存机制
- 搜索结果缓存：1小时
- 查询优化缓存：24小时
- 摘要模板缓存：永久

### 并行处理
- 多个搜索查询并行执行
- 摘要生成与结果获取并行

## 错误处理

### 常见错误及解决方案
1. **网络超时**：自动重试，降低优化级别
2. **无结果**：扩展查询，尝试相关关键词
3. **API限制**：使用缓存结果，提示用户稍后重试

### 降级策略
- 主功能失败时降级到基础web_search
- 摘要失败时返回原始结果
- 优化失败时使用原始查询

## 扩展能力

### 插件系统（规划中）
1. **源插件**：添加新的搜索源
2. **优化插件**：自定义查询优化算法
3. **摘要插件**：不同的摘要风格
4. **输出插件**：自定义结果格式

### 集成能力
1. **与self-improving-agent集成**：记录搜索模式和优化效果
2. **与知识库集成**：优先搜索本地知识
3. **与工作流集成**：作为自动化流水线的一部分

## 开发指南

### 项目结构
```
enhanced-search/
├── SKILL.md              # 技能文档（本文件）
├── search_optimizer.py   # 查询优化器
├── result_summarizer.py  # 结果摘要器
├── cache_manager.py      # 缓存管理器
├── config_loader.py      # 配置加载器
└── main.py              # 主入口
```

### 核心模块说明

#### 1. 查询优化器 (`search_optimizer.py`)
```python
class SearchOptimizer:
    def optimize(self, query, context=None):
        """优化搜索查询"""
        # 1. 关键词提取
        # 2. 查询扩展
        # 3. 上下文融合
        # 4. 返回优化后的查询列表
```

#### 2. 结果摘要器 (`result_summarizer.py`)
```python
class ResultSummarizer:
    def summarize(self, results, query):
        """生成结果摘要"""
        # 1. 提取关键信息
        # 2. 去重和排序
        # 3. 生成结构化摘要
        # 4. 返回格式化结果
```

## 测试用例

### 单元测试
```python
def test_search_optimization():
    optimizer = SearchOptimizer()
    optimized = optimizer.optimize("华为汽车")
    assert "鸿蒙智行" in optimized  # 查询扩展测试
```

### 集成测试
```python
def test_full_search_flow():
    # 完整搜索流程测试
    query = "智能驾驶技术"
    results = enhanced_search(query)
    assert len(results) > 0
    assert "摘要" in results[0]
```

## 部署说明

### 快速部署
```bash
# 1. 复制技能目录
cp -r enhanced-search ~/.openclaw/workspace/skills/

# 2. 测试技能
cd ~/.openclaw/workspace/skills/enhanced-search
python main.py --test

# 3. 集成到OpenClaw
# 技能会自动被OpenClaw加载
```

### 验证部署
```bash
# 验证技能加载
openclaw skills list | grep enhanced-search

# 测试功能
openclaw skills test enhanced-search
```

## 维护指南

### 日常维护
1. **监控搜索质量**：定期检查优化效果
2. **更新关键词库**：根据趋势更新查询扩展词库
3. **优化缓存策略**：根据使用模式调整缓存时间

### 性能监控
- 搜索响应时间
- 缓存命中率
- 用户满意度（通过self-improving-agent收集）

### 版本更新
1. **小版本更新**：优化算法和bug修复
2. **大版本更新**：添加新功能或重构架构

## 贡献指南

### 代码贡献
1. Fork项目
2. 创建功能分支
3. 提交Pull Request
4. 通过测试用例

### 文档贡献
1. 更新示例和文档
2. 添加使用案例
3. 翻译或本地化

## 许可证

MIT License

## 联系方式

- **作者**：袭人 (Xi Ren)
- **项目**：OpenClaw Enhanced Search Skill
- **创建时间**：2026-03-12
- **最后更新**：2026-03-12

---

**备注**：此技能为Tavily Web Search的替代方案，专为无法直接安装clawhub技能的环境设计。