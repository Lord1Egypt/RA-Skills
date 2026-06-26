# dingtalk-ai-table-insights - 快速开始

## 安装

技能已位于：`/home/admin/openclaw/workspace/skills/dingtalk-ai-table-insights/`

## 快速使用

### 1. 关键词筛选（推荐）

```bash
cd /home/admin/openclaw/workspace/skills/dingtalk-ai-table-insights

# 分析销售相关表格
python3 scripts/analyze_tables.py --keyword "销售"

# 分析项目相关表格
python3 scripts/analyze_tables.py --keyword "项目"
```

### 2. 全量扫描

```bash
# 分析所有有权限的表格
python3 scripts/analyze_tables.py
```

### 3. 保存到文件

```bash
python3 scripts/analyze_tables.py --keyword "销售" --output sales_insights.md
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--keyword` | 表格名称关键词筛选 | 无（全量） |
| `--output` | 输出文件路径 | 无（打印到终端） |
| `--format` | 输出格式（markdown/json） | markdown |
| `--limit` | 每个表格抽样记录数 | 50 |

## 使用场景

### 业务线分析
```bash
python3 scripts/analyze_tables.py --keyword "销售"
python3 scripts/analyze_tables.py --keyword "市场"
python3 scripts/analyze_tables.py --keyword "客服"
```

### 项目追踪
```bash
python3 scripts/analyze_tables.py --keyword "华东项目"
python3 scripts/analyze_tables.py --keyword "双 11"
```

### 职能分析
```bash
python3 scripts/analyze_tables.py --keyword "招聘"
python3 scripts/analyze_tables.py --keyword "预算"
python3 scripts/analyze_tables.py --keyword "采购"
```

### 全局扫描
```bash
python3 scripts/analyze_tables.py
```

## 输出内容

分析报告包含：
- 📋 **分析范围** - 命中的表格列表
- 🔍 **数据一致性检查** - 跨表格对比发现矛盾
- 💡 **趋势洞察** - 数据中的模式和关联
- 🚨 **风险预警** - 按优先级排序的问题
- 📋 **行动建议** - 具体可执行的建议

## 依赖

- Python 3.7+
- mcporter CLI（已配置钉钉 AI 表格 MCP）

## 示例输出

```markdown
## 📊 AI 表格洞察报告

**筛选关键词**: 销售
**分析表格数**: 5 个
**数据记录数**: 128 条

### 📋 分析范围
- 销售管理表格
- 销售日报
- 销售目标追踪表

### 🚨 风险预警
1. **高优先级**: 3 个大额订单状态"待跟进"超过 72 小时

### 📋 行动建议
- 今天内联系王五，确认 28k 订单进展
```

## 注意事项

1. **关键词匹配**: 支持模糊匹配，"销售"会匹配"销售管理"、"销售日报"等
2. **权限问题**: 部分表格可能因 token 权限无法访问，脚本会优雅跳过
3. **数据抽样**: 每个表格默认读取前 50 条记录，避免 token 超限
4. **运行时间**: 分析时间取决于表格数量，通常 1-3 分钟

## 问题排查

### 表格显示"权限不足"
- 检查表格是否已分享给组织
- 确认 MCP token 有效性

### 分析结果为空
- 确认关键词能匹配到表格
- 尝试不使用关键词进行全量扫描

### 运行缓慢
- 使用 `--keyword` 筛选表格
- 减少 `--limit` 抽样数量
