# 预算绩效管理工作流

预算绩效管理全流程：目标审核→数据收集→完成率分析→资金效率→满意度统计→综合评分→绩效报告

## 功能概述

7步标准流程，支持绩效目标审核、完成率计算、满意度统计、综合评分

## 使用方法

### 命令行
```bash
# 直接启动工作流
python scripts/pipeline_engine.py run --type budget_performance --ctx project_name=XX项目

# 预览路由（不执行）
python scripts/pipeline_engine.py run "审一下预算绩效管理工作流" --dry-run

# 导出为可视化流程图
python scripts/pipeline_engine.py export budget_performance --o workflow.drawio
```

### 在 OpenClaw 中使用
将此 Skill 安装后，告诉 OpenClaw：
> "启动预算绩效管理工作流工作流"

## 工作流步骤

详见 `workflow.yaml`

## 依赖

- pipeline_engine.py v3.0
- audit_workflow.py
- audit_router.py

## 分类

审计业务
