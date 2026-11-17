# 模式 C · 重铸/整合本地技能（方法论）

> **加载时机**：进入「模式 C 重铸/整合」时由锻造炉读取本文件（按需加载，不常驻）。
> 配套 `SKILL.md` §模式 C。本文件是 Method C 的完整操作手册：数据源、聚类算法、三维打分、报告 schema、合并 SOP、安全护栏、密钥外部化。
> 状态：已签批实施（skill-forge v2.7.0）。

---

## 0. 一句话定位

用户的 agent 会装越来越多技能，同类技能（多个文献检索 / 多个设计 / 多个电商文案）会**本机并存、互相重叠**。Mode C 把"整理它们"变成一套**可解释、可回滚、默认只读**的流程：库审计 → 聚类 → 三维打分 → 重铸计划 → 用户选基座 + 逐技能确认 → 合并 → 继承基座 slug 接入迭代环。

**边界（硬约束）**：默认只出报告，不写、不删、不覆盖任何技能；合并是可选的、逐技能确认的高权限操作；所有判定可解释、可回滚。

---

## 1. 数据源（真实、可算，非猜测）

| 维度 | 来源 | 计算 |
|------|------|------|
| **使用率** | `~/.workbuddy/usage-log.json`（每技能 `recentDates` / `lastUsedDate` / `firstSeenDate`） | 使用天数 + 时效加权（近 30 天权重高）；无记录 = 0 |
| **完整度** | 技能目录结构 | `SKILL.md` 存在 + `references/` + `scripts/` + `tests/` 各 +1 分；行数在 100–600 合理区间 +1；满分 5 |
| **牛逼度** | 结构代理（粗排） | 用 frontmatter 质量（description 触发句 / recommends 完整性 / version 存在 / footer 存在）做 0–5 粗分；最终选基座时可对候选跑**真·10 维评分尺**（D1–D10，详见 `skill-review-rubric.md`）做精排 |

`usage-log.json` 的 key 为技能 slug（或 name），值为含 `recentDates`（按天的字符串数组）、`lastUsedDate`、`firstSeenDate` 的对象。`recast_scan.py` 按 slug 匹配。

---

## 2. 同类判定（先轻量后可选语义）

### 2.1 轻量（默认）
- name / description 关键词重叠（含中英文同义映射，见脚本内 `SYNONYM` 表）；
- `recommends:` 引用图互为邻居；
- 目录名 / slug 词干相似度（Levenshtein ≤ 阈值）。
- 三者任意命中即聚为一类，**可解释、零依赖、零网络**。

### 2.2 可选语义精校（用户显式启用 + 本地有 key）
- 对轻量无法判定的"疑似重叠"聚类，调用向量模型对 SKILL.md + references 摘要做 embedding 相似度；
- **无 key 或调用失败 → 静默回退轻量模式**，不阻塞主流程；
- 向量 key 读取顺序（**均不进包**）：
  1. env `SILICONFLOW_API_KEY`（若用其他模型，再读 `SILICONFLOW_API_BASE`；硅基流动默认 `https://api.siliconflow.cn/v1/embeddings`）；
  2. `~/.workbuddy/secrets/cjg-evo/siliconflow.json`（结构：`{"api_key": "...", "base_url": "..."}` 或仅 `{"api_key": "..."}`）。

> **关于向量 key 的说明**：硅基流动只是"推荐的一个免费向量模型"，**不是唯一选项**。用户可：
> - 用自己的硅基流动免费 key（注册后填进上面的 secrets 文件或设为 env）；
> - 或换任何其他 OpenAI 兼容 embedding 端点（改 `base_url` 即可）。
> Mode C 绝不把任何 key 打进技能包（同方案 C 密钥外部化铁律）。没有 key 时，轻量聚类完全可用。

---

## 3. 三维推荐基座排序

对每个聚类，按加权综合分排序，推荐 top-1 为基座：

```
base_score = 0.4 × norm(使用率) + 0.25 × norm(完整度) + 0.35 × norm(牛逼度)
```

推荐理由必须**给出可解释依据**（如"使用率最高（近 30 天 12 天）+ 完整度满（含 references/scripts）+ 牛逼度 D1 触发句达标"）。

- 使用率权重最高（0.4）——最常用 = 最可能该保留为入口；
- 牛逼度次之（0.35）——质量差的技能不该当基座；
- 完整度（0.25）——结构完整的更易承接合并。

---

## 4. 报告 schema（每聚类）

```yaml
cluster:
  id: recast-001
  theme: "文献检索类"
  members:
    - slug: smartlib-literature-search
      path: ~/.workbuddy/skills/smartlib-literature-search
      type: utility
      usage_score: 0.82        # 来自 usage-log
      completeness_score: 5/5
      brilliance_proxy: 4/5
      is_base_candidate: true
    - slug: global-biblio-base
      ...
  recommended_base:
    slug: smartlib-literature-search
    reason: "使用率最高 + 完整度满 + 触发句达标；其余并入其能力"
  predicted_impact:
    positive:
      - "合并后单一技能覆盖 X/Y/Z 全部检索场景，减少选择成本"
      - "继承基座使用动量，迭代环立即有信号"
    negative:
      - "被并技能若含独特引用/参数，需人工核对是否并入"
      - "合并技能首次发布需重新走质检（quick_validate + 真机测试）"
  workflow_impact:            # 仅供参考，基于静态引用图推断
    depends_on_members:
      - skill: sweeping-monk
        via: "recommends: smartlib-literature-search"
        note: "若 deprecated 该技能，扫地僧的文献检索建议需更新为合并后 slug"
    confidence: "best-effort（仅扫描 frontmatter recommends + agents/*.md，不保证完整）"
  proposed_merged_shape:
    slug: <base slug 继承>
    outline: "SKILL.md = 基座正文 + 被并者独有能力节；references 合并去重；scripts 保留各自"
```

`recast_scan.py` 直接渲染此 schema 为 Markdown 报告，写到用户指定路径（默认打印到终端）。

---

## 5. 合并执行 SOP（仅用户逐技能确认后）

1. **备份**：每个成员技能整目录复制到 `.backup/YYYY-MM-DDTHH-MMSS_<slug>/`。
2. **建合并技能**：默认复用**基座目录**（slug 不变）；把被并者的独有能力合并进 `SKILL.md` + 去重合并 `references/` + 保留各自 `scripts/`。
3. **标记 deprecated**：被并技能目录保留，frontmatter 加 `deprecated: true` + SKILL.md 顶部加注 `> 本技能已被 <base> 合并，建议改用 <base> slug`。**绝不物理删除。**
4. **继承动量**：合并技能用基座 slug + 基座在 `usage-log.json` 的历史（不新建 slug，避免使用率归零）。
5. **注入治理**：按纪律 11 注入 §零 进化燃料 + footer（Tier 1/2）。
6. **质检 + 版本**：`quick_validate.py` + `package_skill.py`；frontmatter `version` 取基座版本 `minor+1`。
7. **接迭代环**：合并技能自带燃料，用户开始用后即自然进入 `signal → distill → proposal → 应用 → 重发` 闭环（被并者的历史信号也随 slug 继承）。

---

## 6. 安全护栏（硬约束，不可省略）

| 护栏 | 规则 |
|------|------|
| 只读默认 | 分析报告阶段**零写入**；扫描器仅读 `~/.workbuddy/skills/` + `usage-log.json` |
| 不删只 deprecated | 被并技能保留，仅标 `deprecated: true`，可被 agent 正常加载但不主动触发 |
| 先备份 | 任何写入前整目录备份到 `.backup/`，可一键恢复 |
| 逐技能确认 | 合并每个技能都需用户明确 yes；不允许批量默认合并 |
| 范围锁死 | 扫描/合并仅在 `~/.workbuddy/skills/`；不接任意外部路径（防误扫桌面/文档） |
| 密钥外部化 | 向量 key 仅本地 secrets/env；包内零密钥；无 key 回退轻量 |
| 不自动跑脚本 | 合并出的技能其 `scripts/` 不被自动执行，仅静态合并 |
| 隐私 | 不扫描对话历史；工作流影响仅基于静态引用图，标注"仅供参考" |

---

## 7. 验收标准（A1–A9）

- A1 分析报告零副作用：跑 `recast_scan.py` 后随机抽查 5 个技能目录，确认内容/时间戳无改动。
- A2 聚类可解释：每聚类给成员 + 命中理由（关键词/recommends/目录相似），非黑盒。
- A3 三维分有依据：使用率来自 `usage-log.json`、完整度来自结构、牛逼度来自评分尺；三项均可在报告溯源。
- A4 语义可选：有本地 key 时语义精校可用；删除 key 后重跑自动回退轻量且不报错。
- A5 合并需确认：直接调用合并流程在无用户确认时**拒绝**执行（dry-run 仅打印计划）。
- A6 deprecated 不删：合并后原技能仍在目录、仍可加载，仅 `deprecated: true`。
- A7 继承动量：合并技能用基座 slug，其在 `usage-log.json` 的历史完好。
- A8 注入合规：合并技能通过 `quick_validate.py`，含 §零 燃料 + footer（纪律 11）。
- A9 零密钥进包：`forge-publish.py --check` 确认包内无向量 key（同方案 C）。

---

## 8. 风险与缓解

| 风险 | 等级 | 缓解 |
|------|------|------|
| 误判"同类"合并掉互补技能 | 中 | 轻量聚类可解释 + 报告先审 + 逐技能确认 + deprecated 保留可恢复 |
| 工作流影响漏判（误伤依赖） | 中 | 静态引用图 + 显式"仅供参考"标注 + deprecated 不删（依赖方可继续用旧 slug） |
| 合并技能质量倒退 | 中 | 合并后强制 `quick_validate` + 真机测试（纪律 6）后才建议发布 |
| 向量 key 泄漏（若误进包） | 高 | 密钥外部化硬约束 + A9 回归校验（同方案 C） |
| 扫描误触个人目录 | 低 | 范围锁死 `~/.workbuddy/skills/`，拒绝外部路径 |
