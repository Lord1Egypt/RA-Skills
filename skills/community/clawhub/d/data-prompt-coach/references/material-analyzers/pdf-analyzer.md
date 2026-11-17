# PDF Analyzer — PDF/Word 样表分析器

> 适用于：data-prompt-coach 引导入口 L2+ 资料感知
> 角色：用户提交 PDF/Word 样表后，分析版式/字段位置/易错点并回填 5 要素

## 触发条件

用户在引导入口提交 .pdf / .docx / .doc 文件，且场景属于：
- 场景 2（提取）— 用户提供源文件样例（简历/合同/发票/名片等）
- 场景 4（核对）— 用户提供待核对文档样例

## 分析流程

### Step 1: 文档结构识别

```yaml
file_type: "pdf"  # pdf / docx / doc
page_count: 3
text_extractable: true  # 是否可提取文本（扫描件需 OCR）
sections:
  - title: "个人信息"
    page: 1
    position: "顶部"
  - title: "教育背景"
    page: 1
    position: "中部"
  - title: "工作经历"
    page: 1-2
    position: "中部-底部"
```

### Step 2: 字段位置映射

对每份文档，识别关键字段的位置：

```yaml
fields_detected:
  - name: "姓名"
    location: "页 1 顶部"
    extraction_method: "正则：^[\u4e00-\u9fa5]{2,4}$"
    confidence: high
  - name: "电话"
    location: "页 1 顶部"
    extraction_method: "正则：1[3-9]\d{9}"
    confidence: high
    format_variations:
      - "138-0000-0001"  # 带分隔符
      - "13800000001"     # 纯数字
  - name: "邮箱"
    location: "页 1 顶部"
    extraction_method: "正则：\w+@\w+\.\w+"
    confidence: high
  - name: "学历"
    location: "教育背景段"
    extraction_method: "关键词匹配：博士/硕士/本科/大专"
    confidence: medium
    issue: "多段教育经历，需取最高"
```

### Step 3: 易错点识别

```yaml
pitfalls:
  - type: "format_inconsistent"
    field: "电话"
    issue: "带分隔符 138-0000-0001 vs 纯数字 13800000001"
    impact: "high"
  - type: "missing_field"
    field: "期望薪资"
    issue: "部分文档未填写"
    rate: 0.3
    impact: "medium"
  - type: "multi_value"
    field: "工作经历"
    issue: "多段经历，需取最近一份"
    impact: "high"
  - type: "encoding"
    field: "姓名"
    issue: "中英文混排（WANG Lei 王磊）"
    impact: "medium"
  - type: "layout_variation"
    field: "全部"
    issue: "不同文档版式差异大（字段：值 vs 表格 vs 自由文本）"
    impact: "high"
```

### Step 4: 批量处理可行性评估

```yaml
batch_assessment:
  total_files: 200  # 用户告知的数量
  format_consistency: "low"  # low / medium / high
  recommended_batch_size: 50
  estimated_complexity: "high"  # low / medium / high
  recommended_strategy:
    - "分批投喂：50 份/批，共 4 批"
    - "第一批当对齐基准，人工检查后再跑后续"
    - "每批用完全相同的提取规则和输出格式"
```

### Step 5: 回填 5 要素

```yaml
scope: "✅ 已知文件数：{N} 份"
fields:
  - "✅ 字段位置已识别：{K 个字段}"
  - "⚠️ 检测到字段易错点：{issues}，需取值规则"
processing_rules:
  - "⚠️ 检测到格式不一致：{字段名}，需处理规则"
  - "⚠️ 检测到多值字段：{字段名}，需取舍规则"
output_format: "❓ 待确认（建议 Excel 表格）"
exception_handling:
  - "⚠️ 检测到缺失字段：{字段名} {rate}%，需兜底规则"
  - "⚠️ 检测到编码问题：{issue}，需处理规则"
```

## 回填后访谈策略

| 要素 | 资料分析前 | 资料分析后 | 第 1 轮访谈重点 |
|------|----------|----------|---------------|
| 范围 | ❓ | ✅ 已知文件数 | 跳过 |
| 字段 | ❓ | ✅ 位置已识别，⚠️易错点 | 问取值规则（基于易错点） |
| 处理规则 | ❓ | ⚠️ 检测到格式问题 | 问处理规则 |
| 输出格式 | ❓ | ❓ | 问输出格式 |
| 异常处理 | ❓ | ⚠️ 检测到缺失/编码 | 问异常处理 |

**3 轮访谈维度划分**：
- 第 1 轮：取值规则（基于易错点问多值/格式取舍）
- 第 2 轮：处理规则 + 输出格式
- 第 3 轮：异常处理 + 批量策略（如文件数 >100）

## 文档类型专属坑

### 简历类

- 多段教育/工作经历，需明确"取最高学历""取最近职位"
- 联系方式格式不统一（带分隔符 vs 纯数字）
- 期望薪资写法多样（"30-40k" / "10000/月" / "面议"）
- 中英文混排姓名

### 合同类

- 关键条款在长段落中，需精确定位
- 金额大小写并存
- 日期格式多样（YYYY-MM-DD / YYYY年MM月DD日 / DD/MM/YYYY）
- 多版本对比（甲方乙方留存版可能不同）

### 发票类

- 表格结构固定但字段位置因版式而异
- 金额含税/不含税需明确
- 发票号码格式（数字 vs 含字母）

## 与 SKILL.md 的接口

**入口点**：本文件"分析流程"段落
**出口点**：本文件"回填后访谈策略"末尾
**调用方**：SKILL.md Step A2 资料感知访谈
**依赖**：用户提交的 PDF/Word 文件
