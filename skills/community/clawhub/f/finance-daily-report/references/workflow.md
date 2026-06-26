# 财经日报生成流程（新架构）

## 架构设计

**核心原则：** kimi-k2.5 采集原始数据 → Claude 审核数据质量 → Claude 按 9 模块标准自己写日报。

| 阶段 | 执行者 | Token 消耗 |
|------|--------|-----------|
| Phase 1: 数据采集 | Python 脚本 + kimi-k2.5 | ~18,000 tokens (kimi) |
| Phase 2: 质量审核 | Claude subagent | ~3,000-5,000 tokens |
| Phase 3: 撰写日报 | Claude subagent | ~8,000-12,000 tokens |

**总计 Claude token 消耗：~11,000-17,000**（Claude 负责质检 + 撰写，不当传话筒）

---

## Phase 1：数据采集（Python 脚本，0 Claude token）

### 执行命令

```bash
cd ~/.openclaw/skills/finance-daily-report
python3 scripts/collect_and_structure.py --date YYYY-MM-DD \
  2>/tmp/collector.log > /tmp/report_data.json
```

### 输出格式

脚本输出 `/tmp/report_data.json`，包含 9 个模块的原始数据：

```json
{
  "date": "2026-03-13",
  "generated_at": "2026-03-14T13:12:00",
  "total_tokens": 17975,
  "collector_model": "kimi-k2.5",
  "modules": {
    "market_theme": {...},
    "global_macro": {...},
    "fx_usd": {...},
    "rates_bonds": {...},
    "equities": {...},
    "commodities": {...},
    "china_market": {...},
    "sector_news": {...},
    "tomorrow_preview": {...}
  }
}
```

### 模块重采（可选）

如果某个模块数据缺失，可单独重采：

```bash
python3 scripts/collect_and_structure.py --date YYYY-MM-DD --module fx_usd
```

---

## Phase 2：质量审核（Claude subagent 执行）

### 审核步骤

1. **读取数据**：加载 `/tmp/report_data.json`

2. **检查每个模块**：
   - N/A 数量统计
   - 异常值检测（价格/涨跌幅是否合理）
   - 缺失模块识别

3. **汇率全 N/A 处理**：
   - 调用单模块重采：`collect_and_structure.py --module fx_usd`
   - 或用 `web_fetch` 直接抓取 Trading Economics 补充数据

4. **核心数据交叉核验**：
   - 至少用 `web_fetch` 抓一个备用源对比关键数字
   - 核验对象：股指点位、汇率、美债收益率、原油/黄金价格

5. **质检结果**：
   - 通过的模块：标记 `verified=true`
   - 不通过的模块：尝试修复（重采或 web_fetch 补数据）
   - 修复失败：标记"数据暂缺"，记录原因

### 输出

审核后的数据结构（内存中传递，不写文件）：

```json
{
  "modules": {
    "fx_usd": {
      "data": {...},
      "quality_status": "verified|needs_repair|missing",
      "issues": ["N/A 过多", "数值异常"],
      "cross_check_url": "https://..."
    }
  }
}
```

---

## Phase 3：撰写日报（Claude subagent 执行）

### 输入

审核通过的数据（Phase 2 输出）

### 撰写规范

1. **9 模块结构**（按顺序）：
   - 市场主线
   - 全球宏观速览
   - 汇率与美元
   - 全球利率与美债
   - 核心股市表现
   - 商品与核心资产
   - 中国市场与流动性
   - 行业热点
   - 明日重点前瞻

2. **时区**：Asia/Shanghai，只写过去 24 小时内新信息

3. **关键事实取证规范**：
   - 数字/价格/点位/收益率/日期/政策/事件 **必须绑定具体 URL**
   - 来源引用格式：`[来源名](URL)` 或表格内嵌链接
   - 核心市场数据至少交叉核验一次

4. **行业热点**：必须有具体公告或权威报道链接

5. **明日前瞻**：
   - 只允许写可核验的官方日历/已公布事件
   - **禁止推测**未公布的数据或事件

6. **参考文档**：
   - 文档结构：`references/template.md`
   - 核验规范：`references/verification.md`

### 输出

1. **日报 markdown 原文**：直接返回给主会话发送
2. **文件保存**：`/root/.openclaw/workspace/finance-reports/YYYY-MM-DD.md`
3. **证据映射**（可选）：`/root/.openclaw/workspace/finance-reports/YYYY-MM-DD-evidence.json`

---

## 关键设计原则

| 组件 | 职责 | 备注 |
|------|------|------|
| `collect_and_structure.py` | 数据采集 + 结构化 | kimi-k2.5 干脏活省 token |
| `render_report.py` | **不再使用** | Claude 自己写 markdown，不需要模板渲染 |
| Claude subagent | 质量审核 + 日报撰写 | 不当传话筒，直接生成最终内容 |
| 文件保存 | `/root/.openclaw/workspace/finance-reports/` | 按日期命名 |

---

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| kimi-k2.5 采集失败 | 自动切换 doubao-seed-mini |
| 单个模块采集失败 | 标记"数据暂缺"，继续其他模块 |
| 交叉核验冲突 | 按来源优先级取值，注明口径差异 |
| 审核不通过且无法修复 | 模块标记"数据暂缺"，在日报中说明 |

---

## 快速命令

```bash
# 完整流程（今日数据）
cd ~/.openclaw/skills/finance-daily-report

# Phase 1: 采集
python3 scripts/collect_and_structure.py --date $(date +%Y-%m-%d) \
  2>/tmp/collector.log > /tmp/report_data.json

# Phase 2 & 3: 由 Claude subagent 自动执行（通过 SKILL.md 入口）
```
