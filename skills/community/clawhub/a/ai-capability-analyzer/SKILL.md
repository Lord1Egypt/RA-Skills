---
name: ai-capability-analyzer
description: 智能分析用户需求并推荐最适合的ClawHub技能，提供实时技能搜索、安全评估和使用建议。
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
        - CLAWHUB_API_KEY
      bins:
        - curl
        - jq
        - node
    primaryEnv: OPENAI_API_KEY
    emoji: "🔍"
    homepage: "https://github.com/your-username/ai-capability-analyzer"
---

## 功能概述

AI Agent Capability Analyzer 是一个智能技能推荐和分析工具，专门针对ClawHub平台的完整技能生态系统。它能够：

- 分析用户的具体需求场景
- **实时搜索** 3,286+个ClawHub技能中的最匹配选项
- 提供技能安全性评估（基于100/3规则）
- 生成详细的技能比较报告
- 提供安装和使用指导
- 支持富文本处理、Web开发、数据分析等细分领域

## 使用场景

当用户说以下类型的话时触发：
- "我需要一个能处理YouTube视频的技能"
- "推荐一些好的AI摘要工具"
- "哪个技能最适合自动化我的开发工作流？"
- "分析一下Capability Evolver和Self-Improving Agent的区别"
- "帮我找一个安全的AI技能来处理敏感数据"

## 技术架构

### 核心组件
1. **需求理解模块**: 使用LLM解析用户需求
2. **技能数据库**: 集成ClawHub API获取最新技能数据
3. **安全评估引擎**: 基于下载量、评分、作者信誉进行风险评估
4. **推荐算法**: 多维度匹配用户需求与技能特性
5. **报告生成器**: 生成结构化的分析和建议报告

### 依赖项
- **环境变量**:
  - `OPENAI_API_KEY`: 用于需求理解和内容生成
  - `CLAWHUB_API_KEY`: 用于访问ClawHub技能数据库（可选）
- **系统工具**:
  - `curl`: API调用
  - `jq`: JSON数据处理

## 使用方法

### 基本查询
```bash
# 分析特定需求
node analyze.cjs --query "我需要处理大量文档摘要"

# 比较多个技能
node analyze.cjs --compare "capability-evolver,self-improving-agent"

# 安全评估
node analyze.cjs --security-check "youtube-downloader-skill"
```

### 高级功能
```bash
# 生成完整报告
node analyze.cjs --query "自动化我的GitHub工作流" --format detailed

# 仅显示高安全性技能
node analyze.cjs --query "AI内容生成" --safety-only true

# 获取安装命令
node analyze.cjs --query "最好的文本摘要工具" --install-cmd true
```

## 安全特性

### 内置安全检查
- **100/3规则验证**: 自动检查技能是否满足安全标准
- **权限分析**: 评估技能请求的系统权限是否合理
- **作者信誉**: 检查开发者历史和社区评价
- **恶意软件扫描**: 集成VirusTotal API（如果可用）

### 隐私保护
- 所有用户查询在本地处理（除非明确启用云API）
- 不存储用户的具体需求数据
- API密钥仅用于必要的外部服务调用

## 输出格式

### 简洁模式（默认）
```
🎯 推荐技能: Summarize (10,956+ 下载, ⭐⭐⭐⭐⭐)
✅ 安全评级: 高 (满足100/3规则)
📋 功能: 智能文本摘要，支持长文档处理
🚀 安装: clawhub install summarize
```

### 详细模式
```
📊 技能分析报告
================

🔍 需求分析: [用户需求解析结果]

🏆 Top 3 推荐:
1. Summarize (10,956+ 下载, 132星)
   - 功能: 智能文本摘要
   - 安全性: ⭐⭐⭐⭐⭐ (高)
   - 适用场景: 文档处理、内容创作
   - 安装命令: clawhub install summarize

2. Humanize AI Text (8,771+ 下载, 45星)  
   - 功能: AI文本人性化处理
   - 安全性: ⭐⭐⭐⭐ (中高)
   - 适用场景: 内容优化、文案润色
   - 安装命令: clawhub install humanize-ai-text

3. Free Ride (7,927+ 下载, 28星)
   - 功能: 多功能内容生成
   - 安全性: ⭐⭐⭐ (中)
   - 适用场景: 创意写作、内容生成
   - 安装命令: clawhub install free-ride

🛡️ 安全建议:
- 优先选择前两个技能，它们都满足100/3安全规则
- 在生产环境使用前，建议先在测试环境中验证
- 注意检查API密钥权限设置

📈 趋势洞察:
- 文本摘要类技能在2026年需求增长了45%
- 用户更倾向于选择高评分(>50星)的技能
```

## 开发者信息

- **作者**: 基于ClawHub生态系统调研分析
- **版本**: 1.0.0
- **许可证**: MIT
- **源码**: 可通过ClawHub CLI查看和修改
- **更新策略**: 定期同步ClawHub最新技能数据

## 故障排除

### 常见问题
1. **API密钥错误**: 确保OPENAI_API_KEY环境变量已正确设置
2. **网络连接问题**: 检查curl是否能正常访问外部API
3. **技能数据过期**: 运行 `./update-skills-db.sh` 更新本地缓存

### 调试模式
```bash
# 启用详细日志
DEBUG=1 ./analyze.sh --query "测试查询"
```

## 示例对话

**用户**: "我需要一个能自动总结长篇文章的AI技能"

**AI Agent Capability Analyzer**:
```
🎯 推荐技能: Summarize (10,956+ 下载, ⭐⭐⭐⭐⭐)
✅ 安全评级: 高 (满足100/3规则)
📋 功能: 智能文本摘要，支持长文档处理，可处理PDF、网页、纯文本
🚀 安装: clawhub install summarize
💡 使用提示: 直接说"总结这篇文章"或提供URL即可
```

**用户**: "比较一下Capability Evolver和Self-Improving Agent"

**AI Agent Capability Analyzer**:
```
📊 技能对比分析
================

🤖 Capability Evolver (35,581+ 下载, 33星)
- 核心功能: AI自进化引擎，让代理自主改进能力
- 优势: 下载量最高，社区广泛采用
- 适用: 希望AI持续自我优化的高级用户
- 安全性: ⭐⭐⭐⭐⭐

🧠 Self-Improving Agent (15,962+ 下载, 132星)  
- 核心功能: 自主学习框架，基于交互优化响应
- 优势: 评分最高(132星)，社区最认可
- 适用: 注重稳定性和质量的用户
- 安全性: ⭐⭐⭐⭐⭐

💡 建议: 
- 如果追求最新功能和活跃社区 → 选择 Capability Evolver
- 如果重视稳定性和社区评价 → 选择 Self-Improving Agent
- 两者都安全可靠，可根据具体需求选择
```