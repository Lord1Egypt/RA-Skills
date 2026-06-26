---
name: code-hug
description: AI驱动的软件开发工作流编排器，基于六层控制系统提供端到端项目管理能力，包含全面的代码分析、商业智能提取和智能工作流自动化。
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🤗","os":["darwin","linux","win32"],"requires":{"bins":["python","node","java","git","bash","php"]}}}
---

# Code Hug

Code Hug 是一个先进的 AI 驱动的软件开发工作流编排器，提供全面的端到端项目管理能力。基于六层控制系统构建，它无缝集成了代码考古学、商业智能提取和智能工作流自动化。

## 核心能力

### 智能工作流编排
- **端到端流水线**: 需求分析 → 功能分解 → 代码实现 → 集成验证 → 部署准备
- **质量门禁**: 可配置的 YAML 准入/准出标准验证
- **会话管理**: 完整的审计轨迹和决策日志
- **成果物管理**: 各阶段产出物的自动归档和版本跟踪

### 高级代码分析与商业智能
- **业务规则提取**: 自动发现和记录嵌入的业务逻辑
- **PRD生成**: 从代码实现反向工程生成产品需求  
- **工作流映射**: 提取和可视化端到端业务流程
- **数据模型分析**: 发现实体关系和数据流
- **多语言支持**: 全面支持 Java、JavaScript/TypeScript、Python、PHP 和 Vue.js 项目

### 智能诊断与自动修复
- **失败分析**: 支持 Java 和 JavaScript/TypeScript 项目失败诊断
- **自动修复**: 构建配置、依赖冲突、编译错误
- **智能建议**: 上下文感知的代码改进建议
- **安全控制**: 内置安全检查和回滚机制

## 系统要求

### 运行时依赖
- **Python 3.10+**: 核心编排引擎
- **Node.js 18+**: JavaScript/TypeScript 分析能力  
- **Java**: Java 项目分析和编译支持
- **Git**: 版本控制集成
- **Bash**: 系统命令执行

### 安装验证
```bash
# Python 依赖
pip install PyYAML requests python-dotenv

# 验证安装
python3 -c "import yaml; print('OK')"
node --version
java -version
```

## 可用工具

| 工具 | 描述 | 参数 |
|------|------|------|
| `codehug:start_session` | 启动新的工作流会话 | `project_name`, `project_root`, `tech_stack` |
| `codehug:run_stage` | 执行指定阶段 | `session_id`, `stage`, `context` |
| `codehug:diagnose` | 诊断构建/测试失败 | `session_id`, `build_log`, `test_log` |
| `codehug:auto_fix` | 尝试自动修复问题 | `session_id`, `problem_type`, `project_root` |
| `codehug:validate` | 运行集成验证 | `session_id`, `project_root`, `test_cases` |
| `codehug:get_status` | 获取当前会话状态 | `session_id` |
| `codehug:extract_business_rules` | 从代码库提取业务规则 | `project_root`, `output_format` |
| `codehug:generate_prd` | 生成PRD文档 | `project_root`, `business_context` |
| `codehug:map_workflows` | 映射业务工作流 | `project_root`, `workflow_types` |

## 配置

在 `~/.openclaw/config.json` 中添加:

```json
{
  "skills": {
    "code-hug": {
      "project_root": "/path/to/your/project",
      "auto_fix_enabled": true,
      "max_fix_attempts": 3,
      "enable_safety_checks": true,
      "enable_rollback": true,
      "notification_channels": ["webchat", "email"],
      "business_intelligence_enabled": true
    }
  }
}
```

## 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `project_root` | string | 必填 | 项目根目录 |
| `auto_fix_enabled` | boolean | true | 启用自动修复 |
| `max_fix_attempts` | integer | 3 | 最大自动修复尝试次数 |
| `enable_safety_checks` | boolean | true | 启用安全验证 |
| `enable_rollback` | boolean | true | 启用回滚机制 |
| `notification_channels` | array | ["webchat"] | 通知渠道 |
| `business_intelligence_enabled` | boolean | true | 启用商业智能提取 |

## 使用示例

### 1. 启动新会话
```
/codehug:start_session {
  "project_name": "membership-service",
  "project_root": "/Users/dev/projects/membership-service", 
  "tech_stack": ["Java 17", "Spring Boot 3", "MySQL 8"]
}
```

### 2. 执行需求分析（包含商业智能）
```
/codehug:run_stage {
  "session_id": "membership-service-001",
  "stage": "requirements_analysis",
  "context": {
    "business_context_provided": true,
    "success_metrics_defined": true,
    "stakeholder_identified": true,
    "extract_business_rules": true,
    "generate_prd": true
  }
}
```

### 3. 提取业务规则
```
/codehug:extract_business_rules {
  "project_root": "/Users/dev/projects/membership-service",
  "output_format": "markdown"
}
```

### 4. 诊断构建失败
```
/codehug:diagnose {
  "session_id": "membership-service-001",
  "build_log": "[ERROR] COMPILATION ERROR: cannot find symbol...",
  "test_log": ""
}
```

### 5. 自动修复
```
/codehug:auto_fix {
  "session_id": "membership-service-001",
  "problem_type": "compilation_error",
  "project_root": "/Users/dev/projects/membership-service"
}
```

## 阶段定义

| 阶段 | 准入标准 | 准出标准 | 产出物 |
|------|---------|---------|--------|
| `requirements_analysis` | 业务背景、成功指标、干系人 | PRD完整性≥0.8、干系人批准、技术可行性确认 | prd.md, business_rules.json |
| `functional_decomposition` | PRD批准、架构约束、技术栈 | 技术规格完整性≥0.9、API契约验证、数据库Schema评审 | tech_spec.md, api_contracts.json |
| `code_implementation` | 技术规格批准、编码规范、开发环境 | 单元测试覆盖率≥80%、静态分析通过、代码评审≥0.85 | source_code/, test_coverage.json |
| `integration_validation` | 代码批准、构建脚本、测试环境 | 构建成功、集成测试通过、冒烟测试通过 | test_results.json, integration_report.md |
| `deployment_preparation` | 集成验证批准、部署脚本、回滚计划 | 部署包验证、生产就绪确认、监控配置 | deployment_plan.md, production_checklist.md |

## 支持的项目类型

- ✅ **Java**: Maven/Gradle 项目、Spring Boot、Java EE
- ✅ **JavaScript/TypeScript**: npm/yarn/pnpm、Node.js、React、Vue.js
- ✅ **Python**: Django、Flask、数据科学项目  
- ✅ **PHP**: 遗留企业应用、现代框架
- ✅ **混合项目**: 多语言微服务架构

## 问题类型与自动修复支持

| 问题类型 | 描述 | 自动修复支持 |
|----------|------|-------------|
| `build_configuration` | 构建配置错误（Java版本、Maven/Gradle配置） | ✅ 完全支持 |
| `dependency_conflict` | 依赖冲突、版本不兼容 | ✅ 完全支持 |
| `compilation_error` | 编译错误、语法错误、符号未找到 | ✅ 完全支持 |
| `test_failure` | 单元/集成测试失败 | ⚠️ 部分支持 |
| `runtime_error` | 运行时错误（空指针、内存溢出） | ⚠️ 建议性修复 |
| `environment_issue` | 环境问题（权限、磁盘空间、网络） | ⚠️ 建议性修复 |
| `business_rule_violation` | 违反提取的业务规则 | ✅ 完全支持 |

## 错误处理

### 常见错误码
| 错误码 | 描述 | 解决方案 |
|--------|------|---------|
| `SESSION_NOT_FOUND` | 会话不存在 | 验证 session_id |
| `STAGE_INVALID` | 阶段名称无效 | 检查阶段是否在定义列表中 |
| `ENTRY_CRITERIA_NOT_MET` | 不满足准入标准 | 验证上下文先决条件 |
| `EXIT_CRITERIA_NOT_MET` | 不满足准出标准 | 完成所需产出物 |
| `AUTO_FIX_FAILED` | 自动修复失败 | 查看日志，考虑手动干预 |
| `VALIDATION_FAILED` | 集成验证失败 | 检查构建日志和测试报告 |

## 审计日志

所有操作都会记录到审计轨迹中:

```json
{
  "timestamp": "2026-03-24T12:50:00Z",
  "action": "stage_completed",
  "actor": "code-hug",
  "details": {
    "session_id": "membership-service-001",
    "stage": "requirements_analysis",
    "artifact": "/path/to/prd.md",
    "business_rules_extracted": true
  }
}
```

## 与代码考古学集成

Code Hug 与代码考古学技能无缝集成，提供:
- **增强的商业智能**: 更深入的业务规则提取和PRD生成
- **全面分析**: 结合技术和业务视角
- **智能工作流**: 业务感知的工作流编排
- **统一报告**: 集成的技术和业务评估报告

## 最佳实践

- **渐进式采用**: 从单个阶段开始，再启用完整流水线
- **安全第一**: 始终启用安全检查和回滚机制
- **业务上下文**: 提供丰富的业务上下文以获得更好的智能提取
- **定期验证**: 与领域专家验证假设和提取的规则
- **持续改进**: 使用审计日志优化工作流配置

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-24 | 初始发布，从 workflow-orchestrator 演化而来，增强了商业智能能力 |