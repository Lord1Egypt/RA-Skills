# Fallback Chain Validation Log

## v3.3.5+2 — 3 层 fallback 链验证矩阵

### 链结构（cron prompt 已注入 3 templates）

```
L1: batch_web_search (主源：财联社/新华/证券时报)
   ↓ 失败（success=false / formatted_content=[] / {"error": "..."}）
L2: extract_content_from_websites 抓 https://www.cls.cn/telegraph
   ↓ 失败（JS 动态加载，curl 占位）
L3: extract_content_from_websites 多源池（按任务类型动态选最权威 2 个）：
   - 东方财富快讯 https://finance.eastmoney.com/news/cywjh.html（SSG 渲染 + 结构化列表）
   - 新浪财经首页 https://finance.sina.com.cn/（含"国际焦点"分类）
   - 21 经济网 https://www.21jingji.com/
   - 中金 https://www.cnfin.com/
```

### 验证矩阵

| 任务 | L1 状态 | L2 状态 | L3 使用源 | 备注 |
|------|---------|---------|-----------|------|
| 6/15 晨报 | ❌ MCP `{"error":"..."}` | ❌ JS 占位 | 东方财富快讯 + 新浪首页 | 7 条要闻全事件型 |
| 6/15 周末 | ❌ MCP `{"error":"..."}` | ❌ JS 占位 | 东方财富 + 21jingji | 表格化输出 |
| **6/15 晚报** | ✅ 成功（7 条要闻） | n/a | n/a | **L1 一次过，未触发 fallback** |

### 6/15 晚报实跑数据（验证非 fallback 路径主流通畅）

- L1 成功：`batch_web_search` 返回 20 条 organic results（10/查询 × 2 查询）
- 主源用：`操盘必读 6/15`（mp.cnfol.com） + `证券时报 gs.html` + `新浪财经 6/15 要闻`（3 源）
- L1 来源的多样性证明 L1 主流通畅，**fallback 仅作兜底**

## ⚠️ 维护教训 — 选 fallback URL 优先用"主题聚合页"而非"单篇文章"

### 6/15 晚报实跑发现（2026-06-15 20:00 cron）

- 尝试抓 `https://finance.sina.com.cn/headline/2026-06-15/doc-inicmxay6762199.shtml`
- 返回内容**完全不是 A 股要闻**——是关于美伊协议 / 原油 / 黄金的**地缘 + 大宗商品**文
- 该 URL 是新浪"headline"频道下的**单篇头条文章**，主题不可预测（每天头条可能是美股/地缘/科技/财经/体育）
- 当时 L1 已成功（20 条 organic），未强制依赖 L3 这条 URL，但若 L1+L2 失败时正好撞上"非 A 股主题"的头条 → fallback 也白搭

### 修复指引（v3.3.5+5 起生效）

- ✅ 优先用**主题聚合页**（每天 N 条要闻，主题限定财经）：
  - 东方财富快讯 `cywjh.html` — SSG 渲染 + 结构化列表（**最稳**）
  - 新浪财经**首页** `finance.sina.com.cn/` — 含"国际焦点"分类
  - 21 经济网首页 / 中金首页
- ❌ 避免用**单篇头条文章**（URL 含 `/doc-...shtml` 或 `/20XX-XX-XX/doc-...`）— 主题不可控
- 当前 templates 3 个 fallback 提示段已用 `finance.sina.com.cn/`（首页）— **正确**
- 该问题不影响当前协议（L1+L2 成功率已够高），仅作未来扩展 fallback 池时的选 URL 规范

## 历史教训（v3.3.5+1 → v3.3.5+4 演进）

- **L1 失败率 20%**（agent.log 35 次调用 7 次失败）→ v3.3.5+4 加 retry-once
- **L2 失败率 100%**（cls.cn/telegraph 是 JS 动态加载）→ v3.3.5+2 改用 SSG 页
- **L3 选 URL 原则**：聚合 > 单篇（v3.3.5+5）

## 维护建议

- 每次 cron 失败时检查本表更新
- 季度审计 fallback URL 是否仍可达（curl 200/200 含内容）
- 主题聚合页优先级：东方财富快讯 > 新浪首页 ≥ 21jingji ≥ 中金
