---
name: construction-assistant
description: 施工项目管理助手。支持施工进度跟踪、材料清单管理、安全检查记录、施工日志生成、工程量计算。使用场景：(1) 创建/更新施工进度计划，(2) 管理材料和设备清单，(3) 记录安全检查和整改，(4) 生成施工日志和报告，(5) 计算工程量和成本估算。
---

# Construction Assistant - 施工助手

## 核心能力

本技能提供施工项目管理的核心功能，帮助 AI 助理高效处理施工现场相关任务。

### 1. 施工进度管理 ✅
- 创建施工进度计划（18 道标准工序）
- 更新工序实际进度和状态
- 计算进度偏差并预警延期
- 生成进度分析报告

### 2. 材料管理 ✅
- 根据进度计划估算材料需求
- 统计周期内（周/月）材料用量
- 对比库存生成采购建议
- 缺料预警和采购计划

### 3. 施工日志 ✅
- 自动生成标准日报格式
- 天气、人员、材料记录
- 周报/月报汇总生成

### 4. 安全质量 📋
- 安全检查清单（日常/专项/节假日）
- 质量问题整改跟踪
- 验收记录管理

### 5. 工程量计算 📋
- 常见工程量计算公式
- 快速估算指标
- 材料损耗率参考

## 工作流程

### 进度管理流程

```
1. 收集项目基本信息（工期、工序、依赖关系）
2. 创建进度计划表 → 使用 scripts/create_schedule.py
3. 每日/每周更新实际进度
4. 对比计划与实际，识别偏差
5. 生成进度报告 → 使用 references/report_templates.md
```

### 安全检查流程

```
1. 选择检查类型（日常/专项/节前）
2. 加载检查清单 → references/safety_checklist.md
3. 记录检查结果和隐患
4. 生成整改通知单
5. 跟踪整改闭环
```

## 快速开始

### 1. 创建施工进度计划

```bash
python3 scripts/create_schedule.py \
  --project-name "XX 项目" \
  --start-date "2026-03-21" \
  --output schedule.json
```

### 2. 更新工序进度

```bash
# 更新工序 ID 为 5 的进度到 80%
python3 scripts/update_progress.py \
  --schedule schedule.json \
  --task-id 5 \
  --progress 80 \
  --status "in_progress"

# 标记工序完成
python3 scripts/update_progress.py \
  --schedule schedule.json \
  --task-id 5 \
  --actual-end "2026-04-15"

# 检查进度偏差
python3 scripts/update_progress.py \
  --schedule schedule.json \
  --check \
  --output progress_report.md
```

### 3. 生成施工日志

```bash
python3 scripts/generate_daily_log.py \
  --date "2026-03-21" \
  --weather "晴" \
  --temperature 18 \
  --workers 45 \
  --tasks "基础钢筋绑扎完成 5 吨" \
  --output daily_log.md
```

### 4. 材料需求统计

```bash
# 统计下周材料需求
python3 scripts/material_summary.py \
  --schedule schedule.json \
  --period "next_week" \
  --output material_report.md

# 统计本月材料需求
python3 scripts/material_summary.py \
  --schedule schedule.json \
  --period "next_month" \
  --inventory inventory.json \
  --output material_report.md
```

### 5. 生成周报

```bash
python3 scripts/generate_weekly_report.py \
  --project "XX 项目" \
  --year 2026 \
  --week 12 \
  --schedule schedule.json \
  --output weekly_report_w12.md
```

## 资源文件

### scripts/
- `create_schedule.py` - 创建施工进度计划 ✅
- `update_progress.py` - 更新工序进度和偏差分析 ✅
- `generate_daily_log.py` - 生成施工日志 ✅
- `generate_weekly_report.py` - 生成周报/月报 ✅
- `material_summary.py` - 材料需求统计与采购计划 ✅
- `calculate_quantity.py` - 工程量计算
- `safety_check.py` - 安全检查记录

### references/
- `report_templates.md` - 各类报告模板
- `safety_checklist.md` - 安全检查清单
- `quantity_formulas.md` - 工程量计算公式
- `material_codes.md` - 材料编码规范

### assets/
- `templates/` - Word/Excel 模板文件
- `icons/` - 进度图标、状态图标

## 使用示例

**用户**: "帮我创建 XX 项目的施工进度计划，工期 180 天，从 3 月 21 日开始"

**助理**: 调用 `create_schedule.py` 创建进度计划，包含 18 道标准工序。

**用户**: "今天完成了基础钢筋绑扎，5 吨钢筋，用工 12 人"

**助理**: 调用 `update_progress.py` 更新进度，调用 `generate_daily_log.py` 生成日报。

**用户**: "统计下周的材料需求，看看要不要采购"

**助理**: 调用 `material_summary.py` 分析进度计划，生成材料报告和采购建议。

**用户**: "生成第 12 周的周报"

**助理**: 调用 `generate_weekly_report.py` 汇总本周进度、质量、安全情况。

---

## 下一步

1. 根据实际项目需求完善脚本功能
2. 添加项目特定的模板和检查清单
3. 集成到 ClawHub 进行版本管理
