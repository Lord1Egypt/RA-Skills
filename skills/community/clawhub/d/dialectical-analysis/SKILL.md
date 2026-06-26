# 辩证商业分析 Skill / Dialectical Business Analysis Skill

多代理辩证商业分析，通过正向和反向Agent的对抗性讨论，生成高质量、经得起考验的商业分析报告。

Multi-agent dialectical business analysis through constructive and critical debate, generating high-quality, rigorously-tested business analysis reports.

## 版本历史 / Version History

- **V1.0**: 基础双代理固定5轮辩论 / Basic dual-agent fixed 5-round debate
- **V2.0**: 动态轮次、仲裁者Agent、知识增强、实时干预 / Dynamic rounds, arbitrator agent, knowledge enhancement, real-time intervention
- **V3.0**: 多维度分析框架 / Multi-dimensional analysis framework

## 触发关键词 / Trigger Keywords

- 辩证分析 / Dialectical Analysis
- 商业辩论 / Business Debate
- 方案论证 / Solution Argumentation
- 正反分析 / Pro-Con Analysis
- 可行性评估 / Feasibility Assessment

## 参数 / Parameters

| 参数 Parameter | 类型 Type | 说明 Description |
|-----------|------|-------------|
| topic | string | 分析主题 / Analysis topic |
| background | string | 背景上下文 / Background context |
| focus_questions | array | 需要关注的问题 / Key questions to address |
| constraints | array | 约束条件 / Constraints (预算、时间等) |
| version | string | 版本 v1/v2/v3 (默认: v2) |
| dimensions | array | V3维度 / Dimensions for V3 |
| max_rounds | number | 最大辩论轮次 / Max debate rounds |
| enable_search | boolean | 启用知识增强 / Enable knowledge enhancement |
| add_intervention | string | 实时注入问题 / User injection during debate |

## 语言支持 / Language Support

**核心指令**: 英文 / English

**输入/输出**: 与用户输入语言一致
- 用户用中文 → 中文输出
- 用户用英文 → 英文输出
- 分析过程使用用户语言
- 报告生成使用用户语言

**Core instructions**: English

**Input/Output**: Matches user's input language
- User writes in Chinese → output in Chinese
- User writes in English → output in English
- Analysis conducted in user's language
- Report generated in user's language

## 功能 / Features

### V2.0 功能

1. **动态轮次**: 根据议题复杂度自动调整轮次(3-8轮) / Dynamic rounds: automatically adjusts (3-8) based on topic complexity
2. **仲裁者Agent**: 提供第三方客观总结 / Arbitrator agent: third-party objective summary
3. **知识增强**: 自动搜索行业数据( tavily/brave/ddg ) / Knowledge enhancement: auto-search industry data
4. **实时干预**: 用户可中途注入问题 / Real-time intervention: inject questions mid-debate

### V3.0 功能

1. **多维度分析**: 技术-市场-财务-法律框架 / Multi-dimensional: Tech-Market-Finance-Legal framework
2. **维度评分**: 每维度1-10分 / Dimension scoring: 1-10 per dimension
3. **加权评分**: 自定义各维度权重 / Weighted scoring: custom weights per dimension

## 使用示例 / Usage Examples

### 中文示例
```
使用 Skill: dialectical-business-analysis
参数: topic=是否进入智能家居摄像头市场, background=公司专注软件研发..., focus_questions=["市场时机","竞争壁垒"], constraints=["预算2000万"]
```

### English Example
```
Use Skill: dialectical-business-analysis
Params: topic=Should we enter the smart home camera market?, background=Company focuses on software R&D..., version=v2
```

### 命令行 / CLI
```bash
python3 dialectic_runner.py --topic "分析主题" --version v2
python3 dialectic_runner.py --topic "Should we enter X market?" --version v3 --dimensions "tech,market,finance,legal"
```

## 配置 / Configuration

### 环境变量 / Environment Variables

| 变量 Variable | 说明 Description |
|----------|-------------|
| TAVILY_API_KEY | Tavily搜索API密钥 (推荐) / Tavily search API key (recommended) |
| BRAVE_API_KEY | Brave Search API密钥 (备选) / Brave Search API key (fallback) |

如未配置任一，skill将尝试ddg CLI备选。/ If neither is configured, skill will attempt ddg CLI fallback.

## 架构 / Architecture

```
┌─────────────────────────────────────┐
│         主协调器 Main Orchestrator  │
│  - 辩论协调 / Debate coordination    │
│  - 收敛检测 / Convergence detection │
│  - 报告生成 / Report generation     │
└─────────────────────────────────────┘
         ↑                    ↑
    ┌────┴────┐          ┌────┴────┐
    │   正向   │◄────────►│   反向   │
    │  Pro    │  辩论    │   Con   │
    └─────────┘          └─────────┘
    
    可选 / Optional:
    ┌─────────────┐
    │  仲裁者     │ (V2+)
    │  Arbitrator │
    └─────────────┘
    
    知识增强 / Knowledge:
    ┌─────────────┐
    │   Tavily   │ (V2+)
    │   Search   │
    └─────────────┘
```

## 需求 / Requirements

- Python 3.8+
- OpenClaw框架 / OpenClaw framework
- 可选: Tavily API密钥用于知识增强 / Optional: Tavily API key for knowledge enhancement

## 备注 / Notes

- 知识增强需要配置API密钥 / Knowledge enhancement requires API key configuration
- 默认轮次: 5轮(V1), 3-8动态(V2+) / Default rounds: 5 (V1), 3-8 dynamic (V2+)
- 满足收敛条件时辩论自动结束 / Debate automatically ends when convergence conditions met
- 最终报告包含共识、分歧和建议 / Final report includes consensus, disagreements, and recommendations

---

## 运行时依赖 / Runtime Dependencies

### 必需 / Required
- Python 3.8+

### 可选搜索功能 / Optional (Search Feature)
如需启用知识增强功能，需要以下任一配置：

| 依赖 | 说明 | 获取方式 |
|------|------|----------|
| TAVILY_API_KEY | Tavily搜索API（推荐） | https://tavily.com |
| BRAVE_API_KEY | Brave Search API | https://brave.com/search/api |
| ddg CLI | DuckDuckGo命令行工具 | `brew install ddg` |

**注意**：如未配置任何API，搜索功能将尝试使用免费的DuckDuckGo HTML接口（无需配置）。

### 安全说明
- 所有搜索逻辑已内置，不依赖外部Skill
- 搜索仅在用户明确启用时运行
- 不执行任何外部脚本
