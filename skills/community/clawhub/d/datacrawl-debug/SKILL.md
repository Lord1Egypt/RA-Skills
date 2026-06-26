---
name: datacrawl-debug
description: >-
  Use when user needs to process web data, debug data collection code, clean processed data, or iterate on data processing strategies.
  Use when generating data processing code from URL and field descriptions.
  Use when diagnosing data processing errors like 403, timeout, selector failures, encoding issues.
  Use when cleaning, deduplicating, normalizing, and formatting processed data.
  Use when optimizing data processing strategies based on run history analysis.
  Use when user mentions "数据处理", "数据整理", "数据清洗", "数据代码", "数据调试", "data processing", "data extraction", "debug data".
author:
  name: 秒技工作室
  link: https://xiaping.coze.site
homepage: https://xiaping.coze.site
license: MIT-0
version: 1.2.0
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "技能基础配置、5大核心模块、适用场景"
    - name: instructions
      tokens: 4000
      loaded: trigger
      description: "数据处理全流程：配置生成→代码生成→调试修复→数据清洗→迭代优化"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "错误模式库、代码模板、清洗规则、评分算法"
  resource_paths:
    - references/process_best_practices.md
    - references/data_handling_guide.md
    - references/data_quality_checklist.md
metadata:
  datacrawl:
    core_modules:
      - ProcessEngine: "数据处理配置生成+HTML解析器"
      - CodeGenerator: "3模式代码自动生成(requests_bs4/playwright/api_client)"
      - DebugRunner: "8类错误模式库+诊断+修复建议"
      - DataCleaner: "文本清洗+类型标准化+多格式输出"
      - IterateOptimizer: "运行历史分析+配置自动改进"
    enemy: "数据混乱和访问异常"
    memory_hook: "处理得了·修得好·洗得净·跑得稳"
---

# DataProcess Debug — 数据处理全流程工具

> 处理得了·修得好·洗得净·跑得稳

## 核心定位

数据处理的"急诊室+健身房"——出了问题来急诊（DebugRunner），日常训练来健身（IterateOptimizer），全程配营养师（DataCleaner）。

## 5大核心模块

### 1. ProcessEngine — 数据处理配置生成 + 结果解析
```
scripts/process-engine.py config --url URL --fields 字段1 字段2 --mode static|dynamic|api
scripts/process-engine.py extract --html "HTML内容" --fields 字段1 字段2
```
- 站点类型自动识别（电商/B2B/社媒/内容/政府/开发者）
- 3种模式工具推荐 + CSS/XPath选择器建议
- HTML结构化提取（文本/链接/图片/表格/列表）

### 2. CodeGenerator — 数据处理代码自动生成
```
scripts/code-generator.py --name 项目名 --url URL --fields 字段1 字段2 --mode requests_bs4|playwright|api_client
```
- 3种模板自动选择：静态页面/动态渲染/API接口
- 生成完整可运行代码 + 依赖安装 + 使用步骤

### 3. DebugRunner — 代码调试与修复
```
scripts/debug-runner.py --error "错误信息"
```
- 8类错误模式库：connection/http_error/timeout/selector_error/encoding/json_parse/selenium_playwright/rate_limit
- HTTP子类型精准诊断（403限流/429限流/503服务不可用等各有方案）
- 代码片段扫描（缺异常处理/超时/延迟/UA自动检测）

### 4. DataCleaner — 数据清洗格式化
```
scripts/data-cleaner.py clean --input 数据 --remove-html --remove-duplicates
scripts/data-cleaner.py normalize --input 数据 --schema 类型定义
scripts/data-cleaner.py format --input 数据 --format json|csv|jsonl --fields 字段列表
```

### 5. IterateOptimizer — 自我迭代优化
```
scripts/iterate-optimizer.py analyze --input 运行历史.json
scripts/iterate-optimizer.py improve --config 当前配置 --analysis 分析结果
```
- 成功率趋势 / 错误聚类 / 字段覆盖率 / 优化建议
- 自动调整延迟/超时/重试/模式切换

## 合规声明

### 核心原则
- **遵守 robots.txt**：先检查目标站点的 robots.txt 协议
- **控制请求频率**：合理设置请求间隔，避免对服务器造成压力
- **使用官方 API**：优先使用官方提供的 API 接口获取数据
- **合法授权**：仅处理有合法授权的数据

### 常见问题处理建议
| 问题 | 建议方案 |
|------|----------|
| 连接失败 | 检查URL有效性，添加重试机制 |
| 超时错误 | 增加超时时间，等待后重试 |
| 选择器失效 | 检查页面结构，更新选择器 |
| 编码问题 | 指定正确编码，使用容错解析 |

### 动态页面处理
当目标站点使用 JavaScript 渲染内容时：
1. 使用 Playwright 等工具进行页面渲染
2. 等待页面完全加载后再提取数据
3. 添加适当的页面等待时间

### 注意事项
- 本技能旨在帮助开发者**调试和处理**已获取的公开数据
- 不鼓励也不支持任何形式的未授权数据访问
- 使用前请确保您的数据获取行为符合目标站点的服务条款

## 使用流程

1. **配置**: `process-engine.py config` → 了解目标站点+推荐方案
2. **生成代码**: `code-generator.py` → 获得起始代码模板
3. **调试**: 遇错 → `debug-runner.py` → 秒级诊断
4. **清洗**: `data-cleaner.py` → 去重+标准化+格式化
5. **迭代**: `iterate-optimizer.py` → 基于运行数据持续改进
