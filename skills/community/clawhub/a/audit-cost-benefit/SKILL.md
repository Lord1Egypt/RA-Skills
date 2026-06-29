# 成本效益审计工作流

成本效益分析：成本归集→效益测算→对比分析→敏感性模拟→报告

## 功能概述

5步分析流程，覆盖全口径成本、效益测算、对标分析、敏感性模拟

## 使用方法

### 命令行
```bash
# 直接启动工作流
python scripts/pipeline_engine.py run --type cost_benefit --ctx project_name=XX项目

# 预览路由（不执行）
python scripts/pipeline_engine.py run "审一下成本效益审计工作流" --dry-run

# 导出为可视化流程图
python scripts/pipeline_engine.py export cost_benefit --o workflow.drawio
```

### 在 OpenClaw 中使用
将此 Skill 安装后，告诉 OpenClaw：
> "启动成本效益审计工作流工作流"

## 工作流步骤

详见 `workflow.yaml`

## 依赖

- pipeline_engine.py v3.0
- audit_workflow.py
- audit_router.py

## 分类

审计业务
