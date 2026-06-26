---
name: architecture-evolution-coordinator
version: 1.0.0
layer: tooling
function_type: evolution_coordination
health: healthy
dependencies: [evolution-watcher, unified-query-gateway, memory-integration]
issue: 星型记忆架构自主进化计划的协调器，包含完整五阶段演进提示词与理念级进化试点能力
---

# 🦞 星型记忆架构自主进化计划 – 架构演进协调器

## ⚠️ 开发测试版本

**此技能为架构演进协调器的参考实现，包含完整的五阶段演进提示词和理念级进化试点框架。**

**主要用途**：
1. 为DeepSeek R1等AI助手提供星型记忆架构自主进化的执行指南
2. 协调现有27个单功能插件的协同工作
3. 支持理念级进化试点：分析外部项目（如NeverOnce）并生成融合方案

**当前阶段**：第5阶段（ClawHub发布与功能完善）进行中
**系统健康度**：100%（集成测试22/22通过）
**核心指标**：检索延迟<10ms，零循环依赖，25/27插件健康

---

## 📋 完整执行提示词

以下是为AI助手（DeepSeek R1）准备的完整执行提示词，定义了星型记忆架构从当前状态到理念级自主进化的五阶段演进路径：

```markdown
# 🦞 星型记忆架构自主进化计划 – 给 DeepSeek R1 的执行提示词（2026‑03‑20 实际情况更新版）

## 📊 版本状态: 2026‑03‑20
## 🎯 当前阶段: 第 5 阶段（ClawHub 发布与功能完善）进行中
## 🚀 下一阶段: 第五阶段核心理念级进化试点准备

---（完整内容见下方）---
```

**注**：由于篇幅限制，完整提示词超过7000字，包含：
- 角色定义与约束条件
- 五阶段详细实施计划（Phase 1-4.5已完成，Phase 5进行中）
- 系统健康状态与性能指标
- 技术债务跟踪与管理
- 理念级进化试点框架

完整提示词可通过本技能的`prompts/full_evolution_guide.md`文件获取。

---

## 🛠️ 核心功能

### 1. 架构演进协调
- **状态机约束**：严格执行五阶段顺序，仅执行当前阶段允许的操作
- **退化检测与修复**：自动识别前阶段功能退化并进行修复
- **健康监控**：集成`evolution-watcher`的插件健康检查与报告生成

### 2. 理念级进化试点框架
- **外部项目分析**：从GitHub、arXiv等源提取核心理念
- **功能对比匹配**：将外部功能点与现有插件`function_type`元数据匹配
- **融合方案生成**：新插件草案或现有插件改造建议
- **沙盒验证**：复用`evolution-watcher`沙盒测试框架

### 3. 电子邮件报告集成
- **自动报告**：`evolution-watcher`报告自动发送至`johnson007.ye@gmail.com`
- **定制收件人**：支持配置多个收件人邮箱
- **报告格式**：Markdown + HTML，支持丰富格式

---

## 🚀 快速开始

### 作为AI助手使用
```bash
# 加载本技能作为执行指南
# AI助手应严格遵循提示词中的阶段约束

# 检查当前阶段状态
python3 scripts/check_phase_status.py

# 运行理念级分析试点（以NeverOnce项目为例）
python3 scripts/analyze_external_project.py https://github.com/WeberG619/neveronce
```

### 作为独立协调器使用
```bash
# 安装依赖
pip install -r requirements.txt

# 运行架构健康检查
python3 scripts/architecture_health_check.py

# 生成演进报告
python3 scripts/generate_evolution_report.py --phase 5
```

---

## 📁 文件结构

```
architecture-evolution-coordinator/
├── SKILL.md                          # 本文件
├── prompts/
│   ├── full_evolution_guide.md       # 完整7000字执行提示词
│   ├── phase5_implementation.md      # 第五阶段详细实施方案
│   └── neveronce_analysis_template.md # NeverOnce项目分析模板
├── scripts/
│   ├── check_phase_status.py         # 阶段状态检查
│   ├── analyze_external_project.py   # 外部项目分析
│   ├── architecture_health_check.py  # 架构健康检查
│   └── generate_evolution_report.py   # 演进报告生成
├── templates/
│   ├── new_plugin_draft.md           # 新插件草案模板
│   └── fusion_proposal.md            # 融合方案模板
└── examples/
    └── neveronce_analysis_example.md # NeverOnce分析示例
```

---

## 🎯 理念级进化试点：NeverOnce项目分析

### 项目信息
- **名称**: NeverOnce
- **描述**: Persistent, correctable memory for AI. The memory layer that learns from mistakes.
- **GitHub**: https://github.com/WeberG619/neveronce
- **关键特性**: 持久化记忆、可纠正性、从错误中学习、零依赖、跨平台

### 分析框架（预定义）
1. **核心理念提取**：
   - 持久化记忆机制
   - 错误学习与纠正算法
   - 记忆衰减与强化策略

2. **与现有架构对比**：
   - 对比`memory-integration`的持久化方案
   - 对比`forgetting-curve`的记忆衰减算法
   - 对比`learning-coordinator`的学习机制

3. **融合机会识别**：
   - 可纠正记忆层作为新插件
   - 错误学习算法增强现有学习协调器
   - 跨平台支持集成到现有工具层

### 预期产出
1. **分析报告**：NeverOnce核心理念与现有架构对比
2. **融合方案**：具体代码变更建议或新插件草案
3. **实施路线图**：分阶段集成计划

---

## 🔧 技术要求

### 已实现保障
- ✅ **沙盒测试**：所有自动生成代码必须先通过沙盒测试
- ✅ **用户确认**：所有代码修改需展示diff和测试报告
- ✅ **性能优化**：缓存检索延迟<10ms
- ✅ **元数据支持**：完整插件`function_type`元数据

### 待实现功能（Phase 5）
- 🔄 **去重与版本追踪**：外部项目数据库
- 🔄 **算法提取**：从文档/代码提取算法信息
- 🔄 **理念引擎原型**：完整"发现→解析→对比→生成→验证"流程

---

## 📊 系统集成

### 依赖插件
| 插件 | 版本 | 用途 |
|------|------|------|
| `evolution-watcher` | v0.6.2+ | 监控、沙盒验证、报告生成 |
| `unified-query-gateway` | v0.1.0+ | 统一检索与缓存管理 |
| `memory-integration` | v0.1.0+ | 记忆同步与增强搜索 |
| `learning-coordinator` | v0.1.0+ | 学习机制协调 |

### 数据流
```
外部项目 → 理念提取 → 功能对比 → 融合方案 → 沙盒验证 → 用户确认 → 实施
          ↑                                          ↓
      元数据匹配                              报告生成 → 电子邮件
```

---

## 📝 配置说明

### 环境变量
```bash
# 电子邮件报告
export EVOLUTION_COORDINATOR_SENDER_EMAIL="your-email@gmail.com"
export EVOLUTION_COORDINATOR_SENDER_PASSWORD="your-app-password"
export EVOLUTION_COORDINATOR_RECIPIENT_EMAIL="johnson007.ye@gmail.com"

# GitHub API（可选）
export GITHUB_TOKEN="your_github_token"

# 架构路径
export OPENCLAW_WORKSPACE="/root/.openclaw/workspace"
```

### 配置文件
```yaml
# config/coordinator_config.yaml
monitoring_sources:
  - type: github
    url: https://github.com/WeberG619/neveronce
    keywords: [memory, ai, learning, correction]
  
  - type: arxiv
    categories: [cs.AI, cs.LG]
    keywords: [memory, reinforcement learning]

analysis_depth: medium  # quick/medium/deep
output_format: markdown  # markdown/html/json
```

---

## 🧪 测试与验证

### 单元测试
```bash
# 运行所有测试
pytest tests/ -v

# 测试特定模块
pytest tests/test_idea_extraction.py
pytest tests/test_fusion_generation.py
```

### 集成测试
```bash
# 验证与evolution-watcher集成
python3 tests/integration/test_evolution_watcher_integration.py

# 验证报告生成与发送
python3 tests/integration/test_email_reporting.py
```

### 沙盒测试
```bash
# 运行理念分析沙盒测试
python3 scripts/sandbox_test_idea_analysis.py --project https://github.com/WeberG619/neveronce
```

---

## 📈 性能指标

| 指标 | 目标值 | 当前值 | 状态 |
|------|--------|--------|------|
| **理念分析时间** | <30秒 | 待测量 | ⏳ |
| **融合方案生成** | <60秒 | 待测量 | ⏳ |
| **报告生成延迟** | <5秒 | 待测量 | ⏳ |
| **电子邮件发送** | <10秒 | 待测量 | ⏳ |
| **内存使用** | <100MB | 待测量 | ⏳ |

---

## 🚨 故障排除

### 常见问题
1. **电子邮件发送失败**
   - 检查环境变量配置
   - 验证SMTP服务器可达性
   - 检查发件人邮箱应用密码

2. **GitHub API限制**
   - 配置GITHUB_TOKEN环境变量
   - 降低请求频率
   - 使用本地缓存

3. **插件依赖缺失**
   - 运行`python3 scripts/check_dependencies.py`
   - 安装缺失插件：`clawhub install <plugin-name>`
   - 更新插件版本

### 日志查看
```bash
# 查看协调器日志
tail -f logs/coordinator.log

# 查看理念分析日志
tail -f logs/idea_analysis.log

# 查看电子邮件日志
tail -f logs/email_sender.log
```

---

## 📄 许可证与贡献

### 许可证
MIT License - 详见LICENSE文件

### 贡献指南
1. Fork本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建Pull Request

### 代码规范
- 遵循PEP 8 Python代码规范
- 所有函数必须有类型提示
- 关键功能必须有单元测试
- 公共API必须有文档字符串

---

## 📞 支持与反馈

### 问题报告
- GitHub Issues: [创建新Issue](https://github.com/your-org/architecture-evolution-coordinator/issues)
- 电子邮件: 架构演进相关问题可发送至协调团队邮箱

### 功能请求
1. 描述需求场景
2. 提供具体用例
3. 说明预期行为
4. 提交功能请求Issue

### 紧急支持
对于生产环境关键问题，请联系维护团队。

---

## 🔄 更新历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| v1.0.0 | 2026-03-20 | 初始发布，包含完整五阶段演进提示词 |
| v1.0.1 | 计划中 | 添加NeverOnce分析示例 |
| v1.1.0 | 计划中 | 理念级进化引擎原型 |

**最后更新**: 2026-03-20 12:50 GMT+8