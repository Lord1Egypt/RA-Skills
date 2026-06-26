# 数据分析 Skill 工作流详解

## 标准流程（EDA → 清洗 → 分析 → 可视化 → 洞察 → 输出）

### Step 1: EDA（探索性数据分析）

**目标**: 快速了解数据全貌，识别数据质量问题。

**执行**:
```bash
python3 scripts/analyze.py <数据文件> --output-dir ./output
```

**输出**: `summary.json` 包含：
- 数据形状（行数、列数）
- 列类型分布（数值列、分类列、时间列）
- 缺失值统计
- 重复行统计
- 数值列描述性统计（count/mean/std/min/25%/50%/75%/max）
- 分类列 Top5 频次

**判断逻辑**:
- 缺失率 > 30% 的列 → 提示用户是否删除
- 重复行 > 5% → 提示用户确认清洗策略
- 数值列唯一值 < 5 → 可能是分类变量，建议转换

### Step 2: 数据清洗

**自动清洗规则**:
1. 删除全空行/列
2. 删除重复行（记录日志）
3. 数值列缺失值 → 用中位数填充
4. 分类列缺失值 → 用 "未知" 填充

**清洗日志**: 记录每一步操作，写入 `summary.json` 的 `clean_log` 字段。

### Step 3: 统计分析

**数值列**:
- 描述性统计（均值、标准差、四分位数）
- 相关性矩阵（如有多列）
- 分布偏度/峰度（可选）

**分类列**:
- 唯一值数量
- Top N 频次分布
- 占比计算

### Step 4: 可视化

**自动图表生成规则**:

| 图表类型 | 适用列 | 生成条件 | 数量限制 |
|---------|--------|---------|---------|
| 柱状图 | 数值列/分类列 | 自动 | 数值列最多 3，分类列最多 2 |
| 饼状图 | 分类列 | 唯一值 ≥ 2 | 最多 2 列 |
| 折线图 | 数值列 | 数据点 ≥ 2 | 最多 3 列 |
| 条形图 | 分类列 | 唯一值 ≥ 2 | 最多 2 列 |

**图表保存**: `output/charts/` 目录，PNG 格式，150 DPI。

**中文字体**: 自动检测系统字体（PingFang SC / SimHei / Microsoft YaHei 等），确保中文正常显示。

### Step 5: AI 洞察生成

**调用时机**: 图表生成完成后。

**调用方式**: 参考 `references/insight_generation.md`，调用 Kimi 或 DeepSeek API。

**Prompt 构建**:
- 注入 `summary.json` 关键信息
- 注入图表描述（类型、列名、特征）
- 要求输出 5 个章节：数据质量评估、核心发现、分布特征、异常点识别、业务建议

**输出**: Markdown 格式洞察文本。

### Step 6: 导出 Word 报告

**执行**:
```bash
python3 scripts/export_report.py ./output/summary.json "<洞察文本>" --output ./数据分析报告.docx
```

**报告结构**:
1. 封面（标题、生成时间、数据文件名）
2. 数据概览（基本信息表、列信息表）
3. 数据清洗记录（操作日志）
4. 统计分析（数值列统计表、分类列统计表）
5. 可视化图表（嵌入 PNG 图片）
6. AI 数据洞察（Markdown 渲染）
7. 结论与建议

**Word 样式**:
- 标题：Heading 1-4
- 表格：Table Grid 样式，表头蓝色背景
- 图表：宽度 5.5 英寸，居中

## 完整示例

```bash
# 1. 分析数据
python3 scripts/analyze.py sales_2024.xlsx --output-dir ./output

# 2. 生成洞察（Agent 调用 Kimi/DeepSeek）
insight=$(python3 -c "
import os, json, requests
# ... 调用 API 生成洞察 ...
print(insight_text)
")

# 3. 导出报告
python3 scripts/export_report.py ./output/summary.json "$insight" --output ./销售数据分析报告.docx
```

## 常见问题

### Q: 图表中文乱码？
A: 脚本自动检测中文字体，如仍乱码，检查系统是否安装 PingFang SC / SimHei / Microsoft YaHei。

### Q: 数值列被识别为字符串？
A: 检查数据源格式，CSV 可能因编码问题导致类型识别错误。脚本会尝试 utf-8 / utf-8-sig / gbk 三种编码。

### Q: 洞察生成失败？
A: 检查 API Key 配置（KIMI_API_KEY / DEEPSEEK_API_KEY 环境变量），确认网络可访问 API 端点。

### Q: Word 报告格式错乱？
A: 确保 python-docx 版本 >= 0.8.11，旧版本样式支持不完整。
