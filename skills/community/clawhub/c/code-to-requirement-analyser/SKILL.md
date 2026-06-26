---
name: trade-code-analyzer
version: 2.1.0
description: 智能分析交易维度前端代码，自动逆向推导业务需求，构建可复用的交易知识图谱。支持 Vue/React/Angular 多技术栈，具备智能缓存和错误恢复机制。
author: 0xSteven
tags: [code-analysis, business-reverse-engineering, trade-knowledge-graph, requirement-derivation, vue, react, angular]
---

# Trade Code Analyzer

智能分析交易维度前端代码，自动逆向推导业务需求，构建可复用的交易知识图谱。

## 核心能力

- **多技术栈代码解析**：Vue 2/3、React (JSX/TSX/Hooks)、Angular (Component/Template)
- **智能缓存机制**：基于文件指纹的增量解析，提升重复分析性能
- **鲁棒性增强**：完善的错误处理和编码检测，防止解析失败
- **交易语义识别与分类**：识别生命周期、交易类型、产品类型、渠道
- **业务规则自动提取与标准化**：验证规则、权限控制、流程控制
- **知识图谱构建与智能关联**：节点相似度计算、关系自动建立
- **需求文档自动生成**：Markdown 报告、结构化 JSON

## 适用场景

- **遗留系统分析**：从旧代码反向推导业务需求
- **代码审查**：识别业务规则遗漏、验证代码与需求一致性
- **知识管理**：沉淀交易领域业务知识
- **需求对比**：代码实现 vs 需求文档的交叉验证
- **系统重构**：理解现有业务逻辑，指导架构优化

## 快速开始

### 1. 解析单个文件

```bash
# Vue 文件（使用缓存）
python3 scripts/cli.py parse ./src/views/Order.vue

# React 文件
python3 scripts/cli.py parse ./src/views/Order.tsx

# 强制重新解析（跳过缓存）
python3 scripts/cli.py parse ./src/views/Order.vue --no-cache

# 保存结果到文件
python3 scripts/cli.py parse ./src/views/Order.vue -o result.json
```

### 2. 完整分析流程

```bash
# 分析并生成报告
python3 scripts/cli.py full ./src/views/Order.vue --generate-report report.md

# 分析并保存到知识库
python3 scripts/cli.py full ./src/views/Order.vue --save-knowledge

# 禁用缓存的完整分析
python3 scripts/cli.py full ./src/views/Order.vue --no-cache --generate-report report.md
```

### 3. 知识库操作

```bash
# 搜索知识库
python3 scripts/cli.py knowledge --search "基金"

# 查找关联知识
python3 scripts/cli.py knowledge --related KNOW-20240101-xxx

# 查看知识库概览
python3 scripts/cli.py knowledge
```

### 4. 缓存管理

```bash
# 查看缓存统计
python3 scripts/cli.py cache --stats

# 清除所有缓存
python3 scripts/cli.py cache --clear
```

## 技术栈支持

### Vue 2/3
- ✅ 单文件组件 (.vue) 完整解析
- ✅ 模板、脚本、样式分离提取
- ✅ ElementUI / Ant Design Vue / Vant 组件识别
- ✅ 数据模型、计算属性、监听器提取
- ✅ 生命周期钩子识别

### React
- ✅ JSX / TSX 文件解析
- ✅ 函数组件、类组件识别
- ✅ Hooks 使用分析 (useState, useEffect, useQuery 等)
- ✅ Ant Design / Material-UI 组件识别
- ✅ React Query / TanStack Query 识别
- ✅ Props 接口提取

### Angular
- ✅ 组件文件 (.component.ts) 解析
- ✅ 模板文件 (.component.html) 解析
- ✅ Material Design 组件识别
- ✅ 装饰器提取 (@Input, @Output, @ViewChild)
- ✅ 依赖注入分析
- ✅ 模板绑定识别

## 缓存机制

### 工作原理

```
文件内容 → SHA256 哈希 → 缓存键
                ↓
          检查缓存存在？
                ↓
        是 → 返回缓存结果（7天有效期）
        否 → 执行解析 → 保存到缓存 → 返回结果
```

### 缓存特点

- **自动失效**：文件内容变化时自动重新解析
- **过期机制**：默认 7 天过期
- **容量控制**：保留最近 100 个分析结果
- **存储位置**：`~/.openclaw/cache/trade-analyzer/`

### 使用建议

| 场景 | 建议 |
|------|------|
| 日常分析 | 使用缓存（默认） |
| CI/CD 流水线 | 使用缓存 |
| 代码变更后 | 首次分析后缓存自动更新 |
| 强制重新分析 | 使用 `--no-cache` 参数 |

## 输出格式

### 解析结果结构

```json
{
  "file_info": {
    "path": "/path/to/file.vue",
    "type": "vue",
    "size": 3584,
    "has_scoped_style": true
  },
  "structure": {
    "template_lines": 45,
    "script_lines": 120,
    "imports": [...],
    "components_used": [...]
  },
  "components": [
    {
      "name": "el-input",
      "type": "input",
      "props": {...},
      "events": ["input", "blur"],
      "business_semantic": "文本输入"
    }
  ],
  "apis": [
    {
      "method": "POST",
      "endpoint": "/api/order/submit",
      "params": {...},
      "business_purpose": "创建资源"
    }
  ],
  "business_rules": [
    {
      "rule_type": "validation",
      "expression": "required: true",
      "confidence": 0.95,
      "business_meaning": "必填校验"
    }
  ],
  "complexity": {
    "lines_of_code": 165,
    "cyclomatic_complexity": 12,
    "component_count": 8,
    "api_count": 3
  }
}
```

### 分析结果结构

```json
{
  "trade_dimension": {
    "lifecycle": ["创建", "审核"],
    "trade_type": ["申购"],
    "product_type": ["基金"],
    "channel": ["手机银行"],
    "parties": ["客户"]
  },
  "functional_requirements": [
    {
      "id": "FR-001",
      "name": "基金申购信息录入",
      "priority": "P0",
      "scenario": "客户需要申购基金时",
      "acceptance_criteria": [...]
    }
  ],
  "business_rules": [...],
  "data_dictionary": [...],
  "business_process": {...},
  "analysis_confidence": {
    "overall": 0.85,
    "dimension_confidence": 0.9,
    "component_confidence": 0.8
  },
  "suggestions": [...]
}
```

## 错误处理

### 鲁棒性特性

- **编码自动检测**：支持 UTF-8、GBK 等编码自动识别
- **正则失败保护**：所有正则匹配都有 try-except 保护
- **部分失败容忍**：单个组件/规则解析失败不影响整体结果
- **详细日志**：使用 logging 模块记录警告和错误

### 常见错误处理

| 场景 | 处理方式 |
|------|----------|
| 文件编码错误 | 尝试多种编码，使用 replace 模式 |
| 正则表达式错误 | 记录警告，返回空结果 |
| 复杂嵌套结构 | 简化处理，提取部分信息 |
| 不支持的语法 | 记录警告，跳过该项 |

## 环境配置

### 必需

```bash
# 知识库存储根目录
KNOWLEDGE_BASE_PATH="~/.openclaw/knowledge/trade/"

# 解析缓存目录
CACHE_DIR="~/.openclaw/cache/trade-analyzer/"
```

### 可选

```bash
# 用于深度语义分析的 LLM API
LLM_API_KEY="your-api-key"
```

### 安装依赖

```bash
# 基础依赖（必需）
pip install chardet

# 可选依赖（增强功能）
pip install openai  # LLM 深度分析
```

## 架构设计

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   CLI 入口   │────▶│  解析器选择  │────▶│  VueParser  │
└─────────────┘     └─────────────┘     ├─────────────┤
                                         │ ReactParser │
                                         ├─────────────┤
                                         │AngularParser│
                                         └──────┬──────┘
                                                ↓
                                         ┌─────────────┐
                                         │  CacheManager│
                                         │  (文件指纹)   │
                                         └──────┬──────┘
                                                ↓
                                         ┌─────────────┐
                                         │ TradeBusiness│
                                         │  Analyzer   │
                                         └──────┬──────┘
                                                ↓
                                         ┌─────────────┐
                                         │KnowledgeGraph│
                                         │   Builder   │
                                         └─────────────┘
```

## 版本历史

### v2.1.0 (当前版本)

- ✅ **React 解析器完整实现**：支持 JSX/TSX、Hooks、React Query
- ✅ **智能缓存机制**：基于文件指纹的增量解析
- ✅ **错误处理增强**：完善的异常保护和日志记录
- ✅ **编码自动检测**：支持多编码格式
- ✅ **CLI 缓存管理**：新增 `cache` 命令

### v2.0.0

- 多技术栈支持（Vue、React、Angular 占位）
- 知识图谱构建
- 业务规则提取
- 需求文档生成

## 扩展开发

### 添加新解析器

```python
from parser.base import BaseCodeParser, ParsedComponent, ParsedAPI, ParsedRule

class NewFrameworkParser(BaseCodeParser):
    def parse(self) -> Dict[str, Any]:
        # 实现解析逻辑
        pass
    
    def extract_components(self) -> List[ParsedComponent]:
        # 提取组件
        pass
    
    def extract_apis(self) -> List[ParsedAPI]:
        # 提取 API
        pass
    
    def extract_business_rules(self) -> List[ParsedRule]:
        # 提取业务规则
        pass
```

### 自定义交易分类

```yaml
# config/taxonomy.yaml
lifecycle:
  创建:
    indicators: ["录入", "选择", "确认"]
  审核:
    indicators: ["初审", "复审", "终审"]

trade_types:
  买入:
    variants: ["认购", "申购", "定投"]
```

## 故障排查

### 诊断命令

```bash
# 检查解析器状态
python3 -c "
import sys
sys.path.insert(0, 'scripts')
from parser.vue_parser import VueParser
from parser.react_parser import ReactParser
print('✓ VueParser 可用')
print('✓ ReactParser 可用')
"

# 检查缓存状态
python3 scripts/cli.py cache --stats
```

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| 解析失败 | 检查文件编码，使用 `--no-cache` 重试 |
| 缓存不更新 | 使用 `--no-cache` 强制重新解析 |
| React 解析为空 | 确保文件后缀为 .jsx 或 .tsx |
| 知识库写入失败 | 检查 KNOWLEDGE_BASE_PATH 权限 |

## 许可证

MIT License

## 作者

0xSteven

---

*持续优化中，欢迎反馈和贡献。*
