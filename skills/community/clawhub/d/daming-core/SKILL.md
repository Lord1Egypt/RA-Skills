# 大明朝廷-三省六部中枢（完整档案系统）

## 概述

基于完整三省六部架构的Skill市场后台预警系统，实现完整的朝廷运作记录、监控预警和反查审计能力。系统巧妙融合古代中国官僚体系与现代软件架构，提供完整的任务管理、资源调度和监控审计功能。

## 核心功能

### 🏛️ 三省六部架构
- **中书省**：接收"圣旨"（任务指令），创建任务档案
- **门下省**：审核任务草案，确保合规性，行使封驳权
- **尚书省**：协调六部工作，管理执行流程
- **六部**：户部（资源）、工部（调度）、兵部（安全）、刑部（审计）、吏部（人事）、礼部（规范）

### 📊 完整档案系统
- 任务档案持久化存储
- Token预算管理和账本记录
- 执行统计和性能监控
- 审核日志和操作记录

### 🔍 监控预警
- 锦衣卫（JinYiWei）实时监控
- 异常行为检测
- 资源使用预警
- 系统健康检查

### 📈 反查审计
- 完整操作链追溯
- 数据完整性验证
- 合规性审计报告
- 历史记录查询

## 安装与配置

### 环境要求
- Python 3.8+
- 文件系统访问权限
- 基本的目录结构

### 快速开始
1. 将技能目录复制到OpenClaw的skills目录
2. 确保依赖项已安装
3. 运行系统测试验证功能

### 依赖项
```bash
# 查看 requirements.txt
```

## 使用方法

### 基本工作流程
```python
# 1. 中书省创建任务
from skill1.zhongshu.main import create_task_archive
task_id, task_dir = create_task_archive(
    emperor_order="生成山水画",
    token_budget=500
)

# 2. 户部创建Token账本
from skill1.bu.hu.main import create_token_ledger
ledger = create_token_ledger(task_id, initial_budget=500)

# 3. 门下省审核任务
from skill1.menxia.main import audit_task_draft
audit_result = audit_task_draft(task_id, "审核通过")

# 4. 工部调度执行
from skill1.bu.gong.scheduler import GongBuScheduler
scheduler = GongBuScheduler()
dispatch_result = scheduler.dispatch_with_budget_check(
    task_id,
    {"action": "generate_image", "estimated_tokens": 100}
)

# 5. 民夫团队执行
from skill2.main import MinFuTeam
team = MinFuTeam(task_id, dispatch_result['execution_id'])
result = team.execute_comfyui({
    "action": "generate_image",
    "params": {"prompt": "山水画"},
    "estimated_tokens": 80
})
```

### 命令行界面
```bash
# 创建任务
python3 main.py create --order "任务描述" --budget 500

# 审核任务
python3 main.py audit --task-id T20260325-xxxx --notes "审核意见"

# 调度执行
python3 main.py dispatch --task-id T20260325-xxxx --action generate_image --tokens 100

# 查看任务列表
python3 main.py list

# 检查系统状态
python3 main.py status
```

## 配置选项

### skill.json 配置
```json
{
    "skill_name": "skill1_daming_court",
    "display_name": "大明朝廷-三省六部中枢（完整档案系统）",
    "description": "基于完整三省六部架构的Skill市场后台预警系统",
    "version": "2.0.0",
    "entry_function": "main.execute",
    "support_type": ["text"],
    "tags": ["daming", "court", "monitoring", "audit", "archive", "chinese-history"],
    "author": "Daming",
    "license": "MIT"
}
```

### 系统配置
- `skill1/config.py` - 系统全局配置
- `ACTIVE_TASKS_DIR` - 活动任务目录
- 各部门独立配置模块

## 数据模型

### 任务档案 (task_draft.json)
```json
{
    "task_id": "T20260325-xxxx",
    "emperor_order": "任务描述",
    "created_at": "2026-03-25T00:00:00",
    "token_budget": 500,
    "status": "draft"
}
```

### Token账本 (token_ledger.json)
```json
{
    "task_id": "T20260325-xxxx",
    "initial_budget": 500,
    "current_balance": 420,
    "transactions": [...]
}
```

### 执行统计 (execution_stats.json)
```json
{
    "task_id": "T20260325-xxxx",
    "total_executions": 3,
    "successful_executions": 3,
    "failed_executions": 0,
    "total_tokens_used": 80,
    "average_tokens_per_execution": 26.67
}
```

## 错误处理

系统包含多层错误处理机制：
1. **输入验证**：参数类型和范围检查
2. **预算检查**：Token余额验证
3. **文件系统**：目录和文件权限检查
4. **模块依赖**：导入错误处理
5. **执行异常**：任务执行失败恢复

## 扩展开发

### 添加新部门
1. 在 `skill1/` 下创建新目录
2. 实现 `main.py` 入口文件
3. 定义部门功能和接口
4. 更新系统架构文档

### 自定义执行器
1. 扩展 `MinFuTeam` 类
2. 实现新的执行方法
3. 更新工部调度逻辑
4. 添加相应的测试

## 测试与验证

### 运行测试
```bash
# 完整流程测试
python3 test_full_flow.py

# 系统健康检查
python3 system_status.py
```

### 测试覆盖率
- 正常流程测试
- 异常情况测试
- 边界条件测试
- 性能压力测试

## 性能特点

- **模块化设计**：各部门独立，松耦合
- **数据持久化**：所有操作记录到文件系统
- **预算控制**：严格的资源管理
- **监控预警**：实时异常检测
- **审计追溯**：完整操作链记录

## 安全考虑

1. **数据隔离**：每个任务独立目录
2. **权限控制**：文件系统权限管理
3. **输入验证**：所有输入参数验证
4. **错误隔离**：异常不会影响其他任务
5. **审计日志**：所有操作可追溯

## 许可证

MIT License - 详见 LICENSE 文件

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 运行测试
5. 创建 Pull Request

## 支持与反馈

- 问题报告：GitHub Issues
- 功能请求：GitHub Discussions
- 文档改进：提交 Pull Request

---

**大明永昌！** 🏛️

*系统设计灵感来源于明代官僚体系，巧妙融合传统智慧与现代技术。*