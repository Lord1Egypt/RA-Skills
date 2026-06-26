---
name: auto-researcher
version: 1.0.0
description: 自主研究助手 - 深度调研、交叉验证、生成引用报告
runtime: prompt_only
---

# Auto Researcher - 自主研究助手

## 🎯 核心功能

自主深度研究任何主题：
- 多源交叉验证
- CRAAP 可信度评估
- 生成引用报告
- 知识图谱构建
- 持续监控更新

**灵感来源**: OpenFang Researcher Hand

---

## 📚 研究方法

### 5 阶段研究流程

```
1. 定义 (Define)
   - 澄清问题
   - 识别已知/未知
   - 设定范围

2. 搜索 (Search)
   - 多策略搜索
   - 多样化来源
   - 查询优化

3. 评估 (Evaluate)
   - CRAAP 框架
   - 提取数据
   - 记录限制

4. 综合 (Synthesize)
   - 整合发现
   - 解决矛盾
   - 识别不确定性

5. 验证 (Verify)
   - 交叉检查
   - 标注置信度
```

---

## 🔍 CRAAP 评估框架

### Currency (时效性)
- [ ] 何时发布/更新？
- [ ] 信息是否仍然当前？
- [ ] 链接是否有效？
- [ ] 技术主题>2 年可能过时

### Relevance (相关性)
- [ ] 是否直接回答问题？
- [ ] 目标受众是谁？
- [ ] 详细程度是否合适？
- [ ] 是否愿意引用？

### Authority (权威性)
- [ ] 作者资质？
- [ ] 出版机构？
- [ ] 联系信息？
- [ ] 域名类型？(.gov/.edu/组织)

### Accuracy (准确性)
- [ ] 是否有证据支持？
- [ ] 是否经过审核？
- [ ] 能否从其他来源验证？
- [ ] 是否有事实错误？

### Purpose (目的)
- [ ] 为什么存在？
- [ ] 信息/商业/说服/娱乐？
- [ ] 偏见是否明显？
- [ ] 作者是否受益？

### 评分标准
```
A (权威): 通过全部 5 项
B (可靠): 通过 4/5 项
C (有用): 通过 3/5 项，需谨慎
D (弱): 通过≤2/5 项
F (不可靠): 失败，不要引用
```

---

## 🔎 搜索优化技巧

### 查询构建

| 技巧 | 语法 | 示例 |
|------|------|------|
| 精确短语 | `"..."` | `"AI Agent 操作系统"` |
| 站内搜索 | `site:...` | `site:zhihu.com OpenClaw` |
| 排除 | `-` | `AI -artificial` |
| 文件类型 | `filetype:...` | `filetype:pdf 报告` |
| 时间范围 | `after:...` | `after:2025-01-01` |
| OR 操作符 | `OR` | `(OpenClaw OR OpenFang)` |
| 通配符 | `*` | `"如何用*赚钱"` |

### 多策略搜索模式

```
主题：OpenClaw 赚钱方法

搜索查询组合:
1. "OpenClaw 赚钱" site:zhihu.com
2. "OpenClaw 变现" after:2025-01-01
3. "OpenClaw Skill" 开发 外包
4. "ClawHub" 技能市场 收入
5. OpenClaw vs OpenFang 对比
6. "AI Agent" 副业 2025
7. site:github.com openclaw skills
8. filetype:pdf openclaw 文档
```

---

## 📊 报告生成

### 输出格式

```markdown
# 研究报告：[主题]

## 执行摘要
[200 字核心发现]

## 研究方法
- 搜索查询：[列出使用的查询]
- 来源数量：[N 个]
- 研究时间：[日期范围]

## 核心发现

### 发现 1: [标题]
**内容**: [详细描述]
**来源**: [引用，CRAAP 评分]
**置信度**: [高/中/低]

### 发现 2: [标题]
...

## 相互矛盾的信息
[列出不同来源的矛盾点，分析原因]

## 知识缺口
[识别尚未解答的问题]

## 参考文献
[APA 格式引用列表]

## 附录
- 完整搜索结果
- 原始数据
- 方法论细节
```

---

## 🧠 知识图谱构建

### 实体类型
```
- 人物 (Person)
- 组织 (Organization)
- 概念 (Concept)
- 产品 (Product)
- 事件 (Event)
- 地点 (Location)
```

### 关系类型
```
- 属于 (belongs_to)
- 创建 (created_by)
- 使用 (uses)
- 竞争 (competes_with)
- 影响 (influences)
- 引用 (cites)
```

### 存储格式
```json
{
  "entities": [
    {
      "id": "openclaw",
      "type": "Product",
      "name": "OpenClaw",
      "attributes": {
        "description": "开源 AI 助手",
        "language": "TypeScript",
        "creator": "Peter Steinberger"
      }
    }
  ],
  "relations": [
    {
      "from": "openclaw",
      "to": "peter_steinberger",
      "type": "created_by"
    }
  ]
}
```

---

## 📋 使用示例

### 激活研究
```
帮我研究一下"知乎盐选投稿指南"，要详细的
```

### 查看进度
```
研究进行得怎么样了？
```

### 获取报告
```
把研究结果整理成报告，要 APA 引用格式
```

### 持续监控
```
持续监控"OpenClaw 新功能"，有更新告诉我
```

---

## 🔧 配置选项

```toml
# 研究深度
research_depth = "deep"  # basic/standard/deep
max_sources = 20  # 最多引用来源数
min_craap_score = "B"  # 最低可信度

# 输出设置
output_format = "markdown"  # markdown/pdf/html
citation_style = "APA"  # APA/MLA/Chicago

# 监控设置
monitor_enabled = false  # 是否持续监控
monitor_frequency = "daily"  # daily/weekly
```

---

## 📊 仪表盘指标

```json
{
  "researcher_reports_generated": 0,
  "researcher_sources_evaluated": 0,
  "researcher_entities_stored": 0,
  "researcher_relations_stored": 0,
  "researcher_last_report_date": null,
  "researcher_avg_credibility_score": 0
}
```

---

## 🎯 应用场景

### 场景 1: 市场调研
```
研究"小红书 AI 工具博主"的变现方式
- 分析 Top 10 博主
- 统计变现模式
- 估算收入范围
- 给出进入建议
```

### 场景 2: 竞品分析
```
研究 OpenClaw 的竞品
- OpenFang vs ZeroClaw vs CrewAI
- 功能对比
- 性能基准
- 市场份额
```

### 场景 3: 技术调研
```
研究"AI Agent 自主赚钱"的可行性
- 现有案例
- 技术栈
- 法律风险
- 实操步骤
```

### 场景 4: 持续监控
```
监控"知乎盐选过稿率"变化
- 每周收集数据
- 追踪趋势
- 异常 alert
- 生成月报
```

---

## 📝 从 OpenFang 借鉴的功能

1. ✅ CRAAP 评估框架 (直接采用)
2. ✅ 5 阶段研究流程 (优化适配)
3. ✅ 知识图谱存储 (简化实现)
4. ✅ 多源交叉验证 (完整保留)
5. ✅ 引用报告生成 (APA/MLA 支持)

---

## 🔧 OpenClaw 适配

| OpenFang 功能 | OpenClaw 实现 |
|--------------|--------------|
| `shell_exec` | `exec` 工具 |
| `knowledge_add_entity` | `memory/store` JSON |
| `web_search` | `searxng` skill |
| `web_fetch` | `web_fetch` 工具 |
| `schedule_create` | `qqbot-cron` |
| `dashboard` | `SESSION-STATE.md` |

---

*此 Skill 受 OpenFang Researcher Hand 启发创建*
