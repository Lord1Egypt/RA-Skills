# 预算执行审计工作流

部门预算执行审计：预算概况→收支分析→进度分析→三公经费→项目支出→报告

## 功能概述

6步流程，覆盖预算执行率、三公经费、结转结余、项目绩效分析

## 使用方法

### 命令行
```bash
# 直接启动工作流
python scripts/pipeline_engine.py run --type budget_execution --ctx project_name=XX项目

# 预览路由（不执行）
python scripts/pipeline_engine.py run "审一下预算执行审计工作流" --dry-run

# 导出为可视化流程图
python scripts/pipeline_engine.py export budget_execution --o workflow.drawio
```

### 在 OpenClaw 中使用
将此 Skill 安装后，告诉 OpenClaw：
> "启动预算执行审计工作流工作流"

## 工作流步骤

详见 `workflow.yaml`

## 依赖

- pipeline_engine.py v3.0
- audit_workflow.py
- audit_router.py

## 分类

审计业务
