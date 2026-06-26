# Workflow Patterns Reference

## Example: Hospital Form Summary Tool (完整的workflow案例)

This is a real-world example of how the workflow refinement process works, from initial request to final skill.

### Phase 1: Initial Request

**User said:** "刚刚你给我做的软件不错，但是需要新增几个功能..."

**Discovery process (问了6轮问题):**

1. Q: "需要新增什么功能？" → A: 6个具体需求
2. Q: "项目库Excel在哪里？" → A: /mnt/d/all_project.xlsx
3. Q: "项目库有几个sheet？" → A: 检查后发现7个，4个有效
4. Q: "如何匹配项目？" → A: 按项目代码（非名称）
5. Q: "售后代码怎么处理？" → A: #N/A或中文则忽略，用项目编码
6. Q: "平均值怎么算？" → A: 每个表单类型单独平均，排除0

### Phase 2: Confirmation (需求确认)

**Presented summary:**

```
## 工作流需求确认

### 目标
更新医院表单汇总工具，支持项目库导入、导出Excel、新增表单类型等

### 输入
- 表单数据Excel (表单表)
- 项目库Excel (all_project.xlsx，多sheet)

### 输出
- 带筛选功能的汇总表格
- 可导出为Excel

### 步骤
1. 导入项目库 (多sheet解析，合并单元格处理)
2. 加载表单数据
3. 匹配项目代码，获取项目信息
4. 计算各表单平均值
5. 展示表格 (支持筛选)
6. 导出Excel

### 确认问题
1. 以上是否正确？
2. 售后代码规则对吗？(#N/A/中文→忽略)
3. 平均值计算方式对吗？(每表单单独平均)
```

**User确认:** "对，就是这样"

### Phase 3: Build (构建)

**Skill structure built:**
- SKILL.md: 完整工作流说明
- scripts/hospital_forms_app.py: 主程序 (591行)
- references/: 无 (简单项目)
- assets/: 无

**Key decisions made:**
- 使用 openpyxl 处理合并单元格
- 使用 xlrd 处理 .xls 文件
- 平均值排除0，每个表单类型独立计算
- 导出时无标红 (用户要求)

### Phase 4: Present and Validate

**Presented:**
- 更新了 `/mnt/d/医院表单工具/hospital_forms_app.py` (v2.5)
- 新增功能列表
- 测试结果

**User反馈:**
- "导入表单表时提示没有sheet_names" → 修复为 `wb.sheetnames`
- "标红有bug，取消标红" → 移除所有红色标记
- "第一行是表头" → 简化表头检测

### Phase 5: Finalize

- 清理缓存
- 更新 README.txt
- 更新 build_exe.txt
- 更新 memory log

## Workflow Decision Tree

```
用户提出需求
  ↓
[Step 1: Discovery — 主动提问，逐一确认]
  ├─ 1.1 目标澄清
  │   ├─ 最终交付什么？
  │   ├─ "完成"的定义？
  │   └─ 核心问题是什么？
  ├─ 1.2 输入规格 (7个维度)
  │   ├─ 数据来源（文件/API/手动）
  │   ├─ 文件格式（.xlsx/.csv/.json）
  │   ├─ 文件位置（本地/网盘/飞书）
  │   ├─ 数据结构（表头/字段/类型）
  │   ├─ 数据量（行数/文件数）
  │   ├─ 数据质量（缺失值/异常处理）
  │   └─ 输入参数（筛选/阈值/范围）
  ├─ 1.3 输出规格 (6个维度)
  │   ├─ 产出形式（文件/报表/图表/动作）
  │   ├─ 输出格式（.xlsx/.pdf/控制台）
  │   ├─ 输出位置（本地/飞书/邮件）
  │   ├─ 输出内容（字段/信息）
  │   ├─ 排序/筛选/统计规则
  │   └─ 格式要求（模板/颜色/公式）
  ├─ 1.4 流程步骤
  │   └─ 每步的输入→输出关系
  └─ 1.5 约束条件
      └─ 时间/技术/业务/性能限制
  ↓
[Step 2: Confirmation — 结构化总结]
  ├─ 输入规格表（7项）
  ├─ 输出规格表（6项）
  ├─ 流程步骤列表
  ├─ 约束条件列表
  ├─ 确认问题（4个）
  └─ 循环直到用户确认
  ↓
[Step 3: Build]
  ├─ 创建skill目录
  ├─ 写SKILL.md
  ├─ 添加scripts/references/assets
  └─ 测试
  ↓
[Step 4: Present and Validate]
  ├─ 展示结果
  ├─ 用户反馈
  └─ 迭代修改
  ↓
[Step 5: Finalize]
  ├─ 打包skill
  ├─ 更新MEMORY.md
  └─ 通知用户
```

## Fuzzy Matching Examples

### 项目名匹配
- 用户说: "孝感中心"
- 匹配: "孝感中心医院东城院区", "孝感中心医院"
- 处理: 问"您是指孝感中心医院还是孝感中心医院东城院区？"

### 表单名匹配
- 用户说: "受理单据"
- 匹配: "受理单"
- 处理: 直接匹配（前缀匹配）

### 文件路径
- 用户说: "D盘的那个表"
- 匹配: /mnt/d/all_project.xlsx
- 处理: 问"您是指 /mnt/d/all_project.xlsx 吗？"

## Iteration Pattern

**每次用户反馈后:**

1. 记录反馈内容到 memory/2026-03-15.md
2. 修改代码/文档
3. 重新呈现结果
4. 等待确认

**循环直到用户说 "可以了" 或 "完成了"**
