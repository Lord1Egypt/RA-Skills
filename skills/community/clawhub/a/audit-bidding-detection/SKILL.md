# 招投标审计工作流

围标串标检测全流程：投标人梳理→关联分析→报价分析→时间窗口→文件相似度→资质核查→风险定级→报告

## 功能概述

9步检测流程，覆盖L1-L22围标串标风险层，自动关联图谱+报价规律+时间窗口+文件相似度分析

## 使用方法

### 命令行
```bash
# 直接启动工作流
python scripts/pipeline_engine.py run --type bidding_audit --ctx project_name=XX项目

# 预览路由（不执行）
python scripts/pipeline_engine.py run "审一下招投标审计工作流" --dry-run

# 导出为可视化流程图
python scripts/pipeline_engine.py export bidding_audit --o workflow.drawio
```

### 在 OpenClaw 中使用
将此 Skill 安装后，告诉 OpenClaw：
> "启动招投标审计工作流工作流"

## 工作流步骤

详见 `workflow.yaml`

## 依赖

- pipeline_engine.py v3.0
- audit_workflow.py
- audit_router.py

## 分类

审计业务
