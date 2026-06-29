# 经济责任审计工作流

领导干部经责审计全流程：了解情况→制定方案→财务分析→重大决策核查→内控测试→疑点汇总→取证定性→编制底稿→形成报告→报告复核

## 功能概述

10步全流程，4个checkpoint确认点，覆盖任中/离任/自然资源资产审计

## 使用方法

### 命令行
```bash
# 直接启动工作流
python scripts/pipeline_engine.py run --type economic_responsibility --ctx project_name=XX项目

# 预览路由（不执行）
python scripts/pipeline_engine.py run "审一下经济责任审计工作流" --dry-run

# 导出为可视化流程图
python scripts/pipeline_engine.py export economic_responsibility --o workflow.drawio
```

### 在 OpenClaw 中使用
将此 Skill 安装后，告诉 OpenClaw：
> "启动经济责任审计工作流工作流"

## 工作流步骤

详见 `workflow.yaml`

## 依赖

- pipeline_engine.py v3.0
- audit_workflow.py
- audit_router.py

## 分类

审计业务
