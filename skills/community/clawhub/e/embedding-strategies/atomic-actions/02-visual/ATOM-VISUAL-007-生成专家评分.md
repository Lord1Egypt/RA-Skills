# ATOM-VISUAL-007 - 生成专家评分

> 版本：V1.0  
> 状态：🟡 待规范  
> 最后更新：2026-03-07

---

## 📋 动作定义

**名称：** 生成专家评分  
**分类：** 呈现层（Visual Layer）  
**编号：** ATOM-VISUAL-007

**一句话描述：** 从 3 个维度评估内容质量（完整性/正确性/缺失项）

---

## 🎯 输入输出

### 输入
- **类型：** 文本
- **内容：** 待评估的内容

### 输出
- **类型：** Markdown 表格
- **内容：** 评分结果（百分比 + 说明）

---

## ⚙️ 偏好设置

### 评分维度
| 维度 | 说明 | 评分标准 |
|------|------|----------|
| **完整性** | 内容覆盖全面程度 | 85%=核心内容全，缺少细节 |
| **正确性** | 关键信息准确程度 | 90%=关键信息准，XX 处需核实 |
| **缺失项** | 缺少的部分 | 15%=缺少 XX、XX、XX 三部分 |

### 评分标准
- **百分比：** 0-100%
- **说明：** 每项必须有具体说明
- **体现 Critical Thinking：** 不是简单吹捧

### 表述风格
- **直接：** 不拐弯抹角
- **建设性：** 指出问题同时给建议
- **专业：** 体现领域知识

---

## 📝 操作步骤

```powershell
# 1. 分析内容
$content = "待评估的内容"

# 2. 评估完整性
$completeness = AssessCompleteness($content)
# 返回：@{Score=85; Comment="核心内容覆盖全面，缺少 XX 细节"}

# 3. 评估正确性
$accuracy = AssessAccuracy($content)
# 返回：@{Score=90; Comment="关键信息准确，XX 处需核实"}

# 4. 识别缺失项
$missing = IdentifyMissing($content)
# 返回：@{Score=15; Comment="缺少 XX、XX、XX 三部分"}

# 5. 生成评分表格
$ratingTable = @"
| 维度 | 评分 | 说明 |
|------|------|------|
| **完整性** | $($completeness.Score)% | $($completeness.Comment) |
| **正确性** | $($accuracy.Score)% | $($accuracy.Comment) |
| **缺失项** | $($missing.Score)% | $($missing.Comment) |
"@

return $ratingTable
```

---

## 🔄 使用场景

### 场景 1：专家点评 HTML 生成
```
触发：生成专家点评
  ↓
调用：ATOM-VISUAL-007
  ↓
输出：评分表格
  ↓
嵌入：HTML 的"专家评分"章节
```

### 场景 2：项目方案评审
```
触发：项目方案提交
  ↓
调用：ATOM-VISUAL-007
  ↓
输出：方案评分
```

---

## 🔗 关联动作

### 前置动作
- ATOM-ANALYSIS-017：专家视角分析

### 后置动作
- ATOM-VISUAL-005：生成 HTML 文件

### 常组合使用
- ATOM-ANALYSIS-017 + ATOM-VISUAL-007 + ATOM-VISUAL-005
  （分析 → 评分 → HTML）

---

## ✅ 检查清单

执行前确认：
- [ ] 3 个维度都评分
- [ ] 百分比 + 说明都有
- [ ] 体现 Critical Thinking

---

_模块化定义 | 可独立调用 | 2026-03-07_
