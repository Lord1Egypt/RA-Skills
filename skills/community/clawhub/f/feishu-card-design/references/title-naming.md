# 飞书卡片标题命名规则

> **版本**：1.0.4 | **本文件作用**：定义"YYYYMMDD-类型-关键信息"标题格式 + 关键信息提取规则
> **设计目标**：让用户一眼看出"这是什么卡片 + 核心是什么"

---

## 1. 标题格式规范

### 1.1 标准格式

```
<8位日期>-<报告类型>-<关键信息1>-<关键信息2>-...
```

### 1.2 字段规范

| 字段 | 格式 | 示例 | 说明 |
|------|------|------|------|
| 日期 | `YYYYMMDD`（无连字符） | `20260719` | 紧凑格式，节省宽度 |
| 报告类型 | 中文标签 | `存量日报` / `行动清单` | 见下方完整类型表 |
| 关键信息 | 2-4 个，`-` 分隔 | `归档30篇-Atoms18条-主种1个` | 从内容自动提取 |
| 总长度 | ≤ 50 字符 | — | 超长截断，保证移动端可读 |

### 1.3 报告类型完整表

| 类型标签 | 适用场景 |
|---------|---------|
| 存量日报 | 矿源处理 + 价值索引 |
| 增量日报 | 发现 + 洞察 + 反思 |
| 行动清单 | 一键复制就能行动 |
| 健康报告 | Vault 健康检查 |
| 周报 | 本周回顾 + 下周建议 |
| 月报 | 月度总结 + 趋势分析 |
| 发芽日报 | 种子筛选 + 发芽候选 |
| 综合日报 | 跨轨汇总 |
| 反思报告 | 复盘 + 改进 |
| 告警通知 | Critical 告警 |
| 成功通知 | 任务完成 |
| 报告 | 兜底类型（类型不明时用） |

---

## 2. 关键信息提取规则

### 2.1 通用提取原则

- **2-4 个关键词**，用 `-` 分隔
- **从标题和内容自动提取**，未提取时 fallback 到来源
- **关键词应有信息密度**（"归档30篇"优于"日报"）
- **避免无信息词**（"报告"、"日报"、"内容"等不算关键信息）

### 2.2 各类型关键信息提取模板

#### 存量日报

**格式**：`归档X篇-AtomsY条-主种Z个`

**提取方法**：
```python
import re

def extract_stock_keywords(content: str) -> str:
    parts = []
    # 归档篇数
    m = re.search(r'\*{0,2}新增归档\*{0,2}[：:]\s*(\d+)\s*篇', content)
    if m: parts.append(f"归档{m.group(1)}篇")
    # Atoms 条数
    m = re.search(r'\*{0,2}Atoms\s*提取\*{0,2}[：:]\s*(\d+)\s*条', content)
    if m: parts.append(f"Atoms{m.group(1)}条")
    # 主种子数
    m = re.search(r'主种子\s*(\d+)\s*个', content)
    if m: parts.append(f"主种{m.group(1)}个")
    return "-".join(parts) if parts else "存量日报"
```

**示例**：
- ✅ `20260719-存量日报-归档30篇-Atoms18条-主种1个`
- ✅ `20260719-存量日报-归档15篇-Atoms10条-主种0个`
- ❌ `20260719-存量日报-日报`（无关键信息）

#### 增量日报

**格式**：`<第一个反常识金句核心>` 或 `<核心洞察>`

**提取方法**：
```python
def extract_flow_keywords(content: str) -> str:
    # 优先找反常识金句
    m = re.search(r'\*\*\d+\.\s*[「「]([^」」]+)[」」]\*\*', content)
    if m:
        quote = re.split(r'[—\-—]', m.group(1))[0].strip()
        quote = re.sub(r'[，。；：,.;:!！?？\s]+', '', quote)
        return quote[:24] if quote else "增量日报"
    # 备选：核心洞察
    m = re.search(r'\*\*核心洞察[：:]\s*(.+?)\*\*', content)
    if m:
        return re.split(r'[—\-—，。；：,.;:!！?？]', m.group(1))[0].strip()[:24]
    return "增量日报"
```

**示例**：
- ✅ `20260719-增量日报-SaaS卖软件AgentSaaS卖工作`
- ✅ `20260719-增量日报-PMF不在制作环节`
- ❌ `20260719-增量日报-增量`（无关键信息）

#### 行动清单

**格式**：`X即时-Y中期-Z长期`

**提取方法**：
```python
def extract_action_keywords(content: str) -> str:
    # 从 frontmatter distribution 块提取
    immediate = len(re.findall(r'【即时行动】', content))
    mid = len(re.findall(r'【中期行动】', content))
    long_term = len(re.findall(r'【长期行动】', content))
    parts = []
    if immediate: parts.append(f"{immediate}即时")
    if mid: parts.append(f"{mid}中期")
    if long_term: parts.append(f"{long_term}长期")
    return "-".join(parts) if parts else "行动清单"
```

**示例**：
- ✅ `20260719-行动清单-1即时-2中期-1长期`
- ✅ `20260719-行动清单-3即时-0中期-0长期`
- ❌ `20260719-行动清单-行动`（无关键信息）

#### 健康报告

**格式**：`评分XX-X级-<关键缺陷>`

**提取方法**：
```python
def extract_health_keywords(content: str) -> str:
    parts = []
    m = re.search(r'overall_score:\s*(\d+)', content)
    if m: parts.append(f"评分{m.group(1)}")
    grade_m = re.search(r'\*{0,2}评级\*{0,2}[：:]\s*([A-F])', content)
    if grade_m: parts.append(f"{grade_m.group(1)}级")
    # 关键缺陷
    m = re.search(r'🚨\s*严重[）)]', content)
    if m:
        context = content[:m.start()]
        dim_m = re.findall(r'[①②③④]\s*(.+?)（', context)
        if dim_m:
            kw_m = re.findall(r'[\u4e00-\u9fff]{2,4}', dim_m[-1])
            if kw_m: parts.append(kw_m[-1] + "缺陷")
    return "-".join(parts) if parts else "健康报告"
```

**示例**：
- ✅ `20260719-健康报告-评分54-C级-MOC缺失`
- ✅ `20260719-健康报告-评分85-B级-Atom孤儿`
- ❌ `20260719-健康报告-报告`（无关键信息）

#### 周报

**格式**：`X篇日报-Y个concept-Z主种子`

**提取方法**：
```python
def extract_weekly_keywords(content: str) -> str:
    parts = []
    m = re.search(r'(\d+)\s*篇日报', content)
    if m: parts.append(f"{m.group(1)}篇日报")
    m = re.search(r'(\d+)\s*个\s*concept', content)
    if m: parts.append(f"{m.group(1)}个concept")
    m = re.search(r'(\d+)\s*主种子', content)
    if m: parts.append(f"{m.group(1)}主种子")
    return "-".join(parts) if parts else "周报"
```

**示例**：
- ✅ `20260719-周报-7篇日报-15个concept-2主种子`
- ✅ `20260719-周报-0篇日报-0个concept-0主种子`
- ❌ `20260719-周报-周报`（无关键信息）

#### 发芽日报

**格式**：`主种X个-<主种子名>-Y个备选`

**提取方法**：
```python
def extract_sprout_keywords(content: str) -> str:
    parts = []
    m = re.search(r'主种子[（(]\s*(\d+)\s*颗', content)
    main_count = m.group(1) if m else "1"
    parts.append(f"主种{main_count}个")
    # 主种子名
    m = re.search(r'####\s*🥇\s*(.+)', content)
    if m:
        name = re.sub(r'[（(【\[].*$', '', m.group(1).strip())
        name = re.sub(r'[：:].*$', '', name).strip().replace(" ", "")[:14]
        if name: parts.append(name)
    # 备选数
    m = re.search(r'备选种子[（(]\s*(\d+)\s*颗', content)
    parts.append(f"{m.group(1) if m else '0'}个备选")
    return "-".join(parts)
```

**示例**：
- ✅ `20260719-发芽日报-主种1个-演进vs设计认识论张力-3个备选`
- ✅ `20260719-发芽日报-主种1个-Agent负向约束-2个备选`

#### 反思报告

**格式**：`<核心命题或观察>`（≤30 字）

**提取方法**：
```python
def extract_reflection_keywords(content: str) -> str:
    m = re.search(r'\*\*判断\s*\d+[：:]\s*([^*]+?)\*\*', content)
    if m: return truncate_at_word_boundary(m.group(1).strip(), 30)
    m = re.search(r'\*\*观察\s*\d+[：:]\s*([^*]+?)\*\*', content)
    if m: return truncate_at_word_boundary(m.group(1).strip(), 30)
    return "反思"

def truncate_at_word_boundary(text: str, max_len: int) -> str:
    text = re.split(r'[，。；,;：:!！?？]', text)[0].strip()
    if len(text) <= max_len: return text
    cut = text[:max_len]
    for i in range(len(cut) - 1, max(0, len(cut) - 15), -1):
        if cut[i] in " \t": return cut[:i].strip()
    return cut.strip()
```

**示例**：
- ✅ `20260719-反思报告-演进与设计的张力是obsidian-loop本质`
- ✅ `20260719-反思报告-C3三步编译法的对标步骤是关键`

---

## 3. 兜底策略

### 3.1 通用兜底（无法识别类型时）

```python
def extract_generic_keywords(content: str) -> str:
    for line in content.split("\n"):
        line = line.strip()
        if not line or line.startswith(("#", "|", ">", "-", "```")):
            continue
        short = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
        short = re.split(r'[，。；：,.;:！!?？\-\—]', short)[0].strip()
        return short[:20] if short else "报告"
    return "报告"
```

### 3.2 来源 fallback

当无法从内容提取关键信息时，使用来源作为关键信息：
- 来源 waytoagi → `20260719-报告-waytoAGI`
- 来源 wechat 公众号 → `20260719-报告-微信公众号`
- 来源 x.com → `20260719-报告-X推文`
- 来源 github → `20260719-报告-GitHub`

---

## 4. 标题长度控制

### 4.1 长度规则

| 总长度 | 处理 |
|--------|------|
| ≤ 30 字符 | ✅ 理想 |
| 30-50 字符 | ✅ 可接受 |
| 50-80 字符 | ⚠️ 关键信息截断 |
| > 80 字符 | ❌ 必须截断 |

### 4.2 截断策略

```python
def truncate_title(title: str, max_len: int = 50) -> str:
    if len(title) <= max_len:
        return title
    # 找最后一个 "-"，截到那里
    last_dash = title.rfind("-", 0, max_len)
    if last_dash > 20:
        return title[:last_dash]
    # 实在不行硬截
    return title[:max_len - 3] + "..."
```

---

## 5. 标题示例对照

### 5.1 ✅ 优秀标题

| 标题 | 评价 |
|------|------|
| `20260719-存量日报-归档30篇-Atoms18条-主种1个` | 信息密度高，一眼看出报告规模 |
| `20260719-增量日报-SaaS卖软件AgentSaaS卖工作` | 关键金句直接放标题，吸引点击 |
| `20260719-行动清单-1即时-2中期-1长期` | 行动分布清晰，用户知道该先做什么 |
| `20260719-健康报告-评分54-C级-MOC缺失` | 评分+评级+关键缺陷，紧迫感强 |
| `20260719-周报-7篇日报-15个concept-2主种子` | 一周工作量一目了然 |
| `20260719-发芽日报-主种1个-Agent负向约束-2个备选` | 主种子名 + 备选数，发芽进度清晰 |

### 5.2 ❌ 失败标题

| 标题 | 问题 |
|------|------|
| `20260719-报告-report_id` | 无关键信息 |
| `2026-07-19-日报` | 日期用了连字符，类型太笼统 |
| `20260719-增量日报` | 无关键信息 |
| `20260719-报告-自动生成的内容请查看` | 浪费标题宽度 |
| `2026年7月19日-日报-今天有很多内容要看哦` | 太长太啰嗦 |

---

## 6. 与卡片 Header 的配合

### 6.1 双层标题策略

飞书卡片 Header 有 `title` 和 `subtitle` 两个字段：

| 字段 | 用途 | 示例 |
|------|------|------|
| `title` | 完整标题（含日期+类型+关键信息） | `20260719-增量日报-SaaS卖软件AgentSaaS卖工作` |
| `subtitle` | 副标题（日期+主题描述） | `2026-07-19 · 发现 + 洞察 + 反思` |

### 6.2 配合示例

```json
{
  "header": {
    "title": {
      "tag": "plain_text",
      "content": "20260719-增量日报-SaaS卖软件AgentSaaS卖工作"
    },
    "subtitle": {
      "tag": "plain_text",
      "content": "2026-07-19 · 发现 + 洞察 + 反思"
    },
    "template": "blue"
  }
}
```

### 6.3 subtitle 模板

| 报告类型 | subtitle 模板 |
|---------|--------------|
| 存量日报 | `YYYY-MM-DD · 矿源处理 + 价值索引` |
| 增量日报 | `YYYY-MM-DD · 发现 + 洞察 + 反思` |
| 行动清单 | `YYYY-MM-DD · 一键复制就能行动` |
| 健康报告 | `YYYY-MM-DD · Vault 健康检查` |
| 周报 | `YYYY-MM-DD · 本周回顾 + 下周建议` |
| 月报 | `YYYY-MM-DD · 月度总结 + 趋势分析` |
| 发芽日报 | `YYYY-MM-DD · 种子筛选 + 发芽候选` |
| 综合日报 | `YYYY-MM-DD · 跨轨汇总` |
| 反思报告 | `YYYY-MM-DD · 复盘 + 改进` |
| 告警通知 | `YYYY-MM-DD · Critical 告警` |
| 成功通知 | `YYYY-MM-DD · 任务完成` |
