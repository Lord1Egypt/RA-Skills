# Skill: Deep Research Pro (v2.2 - True Depth)

> 版本：2.2.0
> 描述：真深度研究技能，强制全文解析+结构化提取+溯源验证

## 核心原则
**没有真正的原文阅读，就没有深度研究**

---

## 🔴 强制执行流程（v2.2 新增）

### Step 1: 研究规划 (必须输出文件)
- 生成 `research/plan.md`
- 列出至少 5 个具体检索查询式
- **用户确认后才能继续**

### Step 2: 全文解析 + 结构化提取 (核心！)

**禁止跳过此步骤！**

对于每个有效来源，必须执行：

1. **获取全文**
   ```bash
   # 使用 extract-from-pdf.py 脚本
   python3 scripts/extract-from-pdf.py card-001 "https://arxiv.org/pdf/xxx.pdf"
   ```
   - 如果有DOI/URL，尝试下载PDF
   - 如果无法获取全文，标记 `full_text: false` 并**跳过该来源**

2. **结构化提取**（从PDF原文提取）
   - 样本量：具体数字
   - 主要结果：具体数值 + 单位 + 统计显著性
   - 成本影响：具体金额/百分比
   - 置信区间：95%CI
   - 原文引用：**必须从正文中复制至少50字**

3. **更新卡片**
   - 用提取的真实数据替换"待提取"
   - 标记 `full_text: true/false`

**最低要求**：
- deep 模式：至少 **10 个**带全文提取的卡片
- 质量阈值：提取后评分 ≥ 6/10

### Step 3: 溯源验证 (强制检查！)

**生成报告前必须运行：**

```bash
bash scripts/check-sourcing.sh reports/final-report.md sources/
```

- 检查每个 `[[card-xxx]]` 引用的数据是否在卡片中存在
- 如果有数据无法溯源，**拒绝生成报告**
- 修复后重新验证

### Step 4: 交叉分析
- 生成 `analysis/synthesis.md`
- 至少找出 3 组矛盾数据
- 标注每个观点的卡片来源

### Step 5: 报告生成
- 生成 `reports/final-report.md`
- **每个数据点必须标注 [[card-xxx]]**
- 报告末附溯源检查结果

---

## 🔧 工具依赖

| 工具 | 用途 | 状态 |
|------|------|------|
| **pdfplumber** | PDF全文解析 | ✅ 已安装 |
| **pdftotext** | PDF备用解析 | ✅ 已安装 |
| extract-from-pdf.py | 结构化数据提取 | ✅ 已创建 |
| check-sourcing.sh | 溯源验证 | ✅ 已创建 |

---

## 📋 执行命令

### 完整流程

```bash
# Step 1: 规划
# 编辑 research/plan.md，确认检索式

# Step 2: 检索 + 提取（循环执行）
# 对于每个来源：
python3 scripts/extract-from-pdf.py card-001 "URL"
# 检查提取结果，填入卡片

# Step 3: 溯源验证
bash scripts/check-sourcing.sh reports/final-report.md sources/

# Step 4-5: 分析与报告
# 生成最终报告
```

---

## ⚠️ 限制说明

如果无法获取全文（付费论文/报告）：
1. 标记卡片 `full_text: false`
2. 报告中对该来源的数据**仅作参考**，不作为核心结论
3. 建议人工复核关键数据

---

## 📊 版本对比

| 维度 | v2.1 | v2.2 |
|------|------|------|
| PDF解析 | ❌ | ✅ 强制 |
| 数据提取 | "待提取" | ✅ 真实提取 |
| 原文引用 | 模板话术 | ✅ 从正文复制 |
| 溯源检查 | ❌ | ✅ 强制验证 |
| 报告质量 | 有引用无验证 | 有引用+验证 |

---

## 质量门禁（v2.2 强化版）

```bash
# 1. 检查卡片数量（≥10个有全文的）
FULLTEXT_COUNT=$(grep -l "full_text: true" sources/card-*.md 2>/dev/null | wc -l)
if [ $FULLTEXT_COUNT -lt 10 ]; then
 echo "❌ 错误：全文提取卡片不足10个，当前 $FULLTEXT_COUNT 个"
 exit 1
fi

# 2. 检查溯源
bash scripts/check-sourcing.sh reports/final-report.md sources/
if [ $? -ne 0 ]; then
 echo "❌ 错误：报告中有数据无法溯源"
 exit 1
fi

# 3. 检查待提取标记
if grep -q "待提取" sources/card-*.md; then
 echo "❌ 错误：卡片中仍有'待提取'数据"
 exit 1
fi
```

---

*Skill版本：2.2.0 | 最后更新：2026-03-19*
