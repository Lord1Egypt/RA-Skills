---
name: better-skill-audit
description: >
  [DEPRECATED — renamed to skill-deep-audit. Install that one instead:
  `clawhub install skill-deep-audit`.] Generic skill-quality auditor for any
  agent skill. 7-dimension static analysis, 115-point scoring, L1/L2 depths,
  --fix workflow. Functionality preserved for backward compatibility only;
  no new features will be added to this slug.
---
> ⚠️ **DEPRECATED — this skill was renamed to [`skill-deep-audit`](https://clawhub.com/skills/skill-deep-audit).**
>
> The slug `better-skill-audit` is kept for backward compatibility only — no new features will land here. Please install the new slug instead:
>
> ```bash
> clawhub install skill-deep-audit
> ```
>
> Source code now lives at [Songhonglei/build-better-skills/skills/skill-deep-audit](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-deep-audit).

---

# better-skill-audit — 通用 Skill 审计

> 本工具脱胎于财务域审计工具，已剥离全部财务专用规则（finws 门面、受控域、主数据校验、
> 业务文件合规等），保留并泛化为**任意 Skill 通用**的质量审计框架。

## 设计指导原则

```
能不能跑起来？  → D3 可移植性 + D4 可用性规范
跑起来对不对？  → D1 流程闭环 + D6 代码文档质量
跑完安不安全？  → D5 安全风险
符不符合规范？  → D2 工具/命令规范
整体健不健康？  → D7 依赖体量
```

## 严格禁止（NEVER DO）

- 不执行被审计 Skill 的任何写操作（只做查询、可达性验证和静态分析）
- 不修改被审计的 Skill 文件（只读、只报告；`--fix` 除外，须用户显式授权）
- 不伪造检查结果，无法判断时标注「无法确认，需人工验证」

## 必须遵守（MUST DO）

- 每次审计开始前必须询问并等待用户选择检查深度（L1 / L2 dryRun）
- 有任何 ERR 则最终结果为 FAIL，无论总分多高
- 审计结束后必须写入记分卡 MD 文件
- L2 dryRun 校验失败（外部依赖不可用）时降级为 WARN 并注明原因，不中止审计

---

## 本 skill 依赖（全部软依赖，缺失自动降级）

| 依赖 | 用途 | 缺失时行为 |
|-----------|------|----------|
| Hub 查询工具（如 clawhub / hub-skill-query） | Hub 发布状态查询（D7-W1）、依赖存在性验证（D7-W2 第三步） | 跳过 Hub 校验，相关项降级为 WARN，不中止审计 |

> 本 skill 核心是纯静态/只读分析，**无任何外部硬依赖**，不安装任何工具也能完成 L1 静态审计。

---

## Step 0：询问检查深度

审计开始时展示以下选项，**等待用户明确选择后再继续**：

```
请选择检查深度：

L1 静态分析（约 2 分钟）
   读取文件、结构检查、关键词扫描、语法检测
   满分 112（跳过需碰外部系统的项），通过线 ≥90
   适合：初稿快速检查

L2 dryRun（约 5 分钟，推荐）⭐
   L1 + Hub 存在性校验 + 依赖存在性验证 + 分支可达性模拟
   （文件存在性 / env 配置 / 未命中分支只读验证）
   满分 115，通过线 ≥90
   适合：上线前 / 发布前完整验收

默认推荐 L2 dryRun，回复 1 / L1 选静态，2 / L2 选 dryRun（直接回车默认 L2）。

⚠️ 说明：L2 dryRun 仅做只读查询与可达性验证，不执行任何写入/更新操作，
   也不会实际运行被审计 skill 的业务流程。
```

---

## Step 1：定位 Skill 目录

用户可以提供：
- Skill 名称（如 `my-skill`）→ 在 `~/.openclaw/workspace/skills/` 下查找同名目录（部分用户路径为 `skills/` 子目录，按实际情况调整）
- 相对/绝对路径（如 `skills/my-skill/`）→ 直接使用

```bash
ls {skill-path}/
cat {skill-path}/SKILL.md | head -20
```

若找不到目录 → 告知用户并停止，不猜测路径。

---

## Step 2：静态分析（全部深度均执行）

按照 [references/check-rules.md](./references/check-rules.md) 逐条执行静态检查。

> ⚖️ **判定一致性约束**：每条规则的命中与否，**以该规则在 check-rules.md 中给定的 grep 模式、关键词清单、数值阈值为准**，不依赖 Agent 主观发挥。规则未明确的边界场景按「防误报通则」处理（标「待人工确认」，不硬判）。这保证不同 Agent / 多次执行对同一被审 skill 的判定结果稳定一致。

### 2.1 收集文件清单

```bash
# 脚本扩展名须覆盖混合语言 skill：.js/.cjs/.mjs/.ts 不能漏
find {skill-path} -type f \( \
  -name "*.py" -o -name "*.sh" -o -name "*.md" -o -name "*.json" -o -name "*.yaml" \
  -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) \
  | grep -v __pycache__ | grep -v node_modules | grep -v .git
```

> ⚠️ **扩展名覆盖盲点**：`find -name "*.js"` **不匹配** `.cjs` / `.mjs` / `.ts`。Python 脚本经常 `subprocess` 调本目录下的 `xxx.cjs`，若文件清单漏了 `.cjs`，会误判「被调脚本不存在」（D6-E4/E6 假阳性）。后续所有按扩展名扫描的命令同样要带全这组扩展名。

### 2.2 逐维度静态扫描

按顺序执行：**D1 → D2 → D3 → D4 → D5 → D6**

> ℹ️ **D7 不在本步**：D7（依赖与体量）需要先统计代码量（见 2.4）和做 Hub/存在性验证，统一放到 **Step 4** 处理，本步只扫 D1–D6。

**执行层级说明**：
- 规则标题含 `L1` → 所有深度均执行
- 规则标题含 `L2 dryRun` → 仅 L2 dryRun 执行；L1 时标注 `➖ 跳过（L2 dryRun 项）`
- **D4-E5 扫描时须排除** `{skill-path}/AUDIT-*.md`，审计报告由本工具生成，不属于被审计 Skill 的打包内容

每条规则：
1. 确认执行层级是否匹配当前检查深度，不匹配则记录 ➖ 跳过
2. 执行对应扫描命令（grep/正则/文件解析/Agent 阅读判断）
3. 记录：通过 ✅ / 失败 ❌ / 跳过 ➖
4. 累计扣分

### 2.3 D6-E1 脚本语法检测

```bash
# Python
for f in $(find {skill-path}/scripts -name "*.py" 2>/dev/null); do
  python3 -m py_compile "$f" 2>&1 && echo "OK: $f" || echo "SYNTAX ERR: $f"
done

# Shell
for f in $(find {skill-path}/scripts -name "*.sh" 2>/dev/null); do
  bash -n "$f" 2>&1 && echo "OK: $f" || echo "SYNTAX ERR: $f"
done
```

### 2.4 统计代码量（D7 前置）

```bash
# 脚本文件数（含混合 skill 的 .js/.cjs/.mjs/.ts）
find {skill-path}/scripts -type f \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) 2>/dev/null | grep -v node_modules | wc -l

# 代码总行数（-r 保证无匹配时不hang）
find {skill-path} \( -name "*.py" -o -name "*.sh" -o -name "*.js" -o -name "*.cjs" -o -name "*.mjs" -o -name "*.ts" \) | grep -v node_modules | xargs -r wc -l 2>/dev/null | tail -1

# 依赖其他 Skill：精确提取依赖清单（见 D7-W2「三步联立」算法）

# ① 列出所有可疑 import 候选（先拿模块名，归属后面反查）
grep -rnE "^\s*(from [a-zA-Z_][a-zA-Z0-9_]* import|import [a-zA-Z_][a-zA-Z0-9_]*)" {skill-path}/scripts/ 2>/dev/null
# ①补：找 sys.path 注入 / skill_root 拼接（这才是 import 归属哪个 skill 的物理证据）
grep -rnE "sys\.path\.insert.*skills/|_skill_root|skills/[a-z-]+/scripts" {skill-path}/scripts/ 2>/dev/null

# ② subprocess 调其他 skill 脚本路径
grep -rnE "skills/[a-z-]+/scripts|_skill_root.*scripts" {skill-path} 2>/dev/null | grep -v __pycache__
# ③ SKILL.md 显式声明
grep -nE "metadata.*requires|依赖.*skill|需先安装|使用 .* skill" {skill-path}/SKILL.md 2>/dev/null
# → Agent 据此汇总去重、按三步联立确定归属、标注用途、做存在性验证（见 D7-W2），输出到报告「六、Skill 依赖」章节
# → 标准库/已知 PyPI 包（os/sys/json/re/requests/openpyxl 等）直接排除，不进归属判定
```

---

## Step 3：Hub 存在性校验（L2 dryRun 执行）

> **前置依赖检查**：本步骤依赖 Hub 查询工具（如 clawhub / hub-skill-query）。若不可用 → 跳过 Hub 校验，D7-W1 标注「无法校验（Hub 工具未安装）」，降级为 WARN，不中止审计。

1. 从 frontmatter 提取 `name` 字段
2. 通过可用的 Hub 查询工具校验是否已发布
3. 结果记入 D7-W1（未发布 → WARN，不计 ERR）

---

## Step 4：依赖与体量分析（D7）

- **D7-W1** Hub 发布状态（Step 3 结果汇总）
- **D7-W2** 精确提取依赖 skill 清单 + 标注用途 + 存在性验证（本地✅/Hub有未装⚠️/找不到❌）→ 无论几个都在报告「六、Skill 依赖」章节输出完整清单；≥5 个 WARN；依赖「找不到」的 → ERR；依赖「Hub 有未装」的 → WARN
- **D7-W3** 代码 ≥ 5000 行或脚本 ≥ 10 个 → 识别高内聚模块，给出拆分方向建议

---

## Step 5：汇总评分

**满分 115 分**

| 维度 | 满分 |
|------|------|
| D1 流程闭环与幂等性 | 13 |
| D2 工具与命令规范 | 10 |
| D3 可移植性与防御 | 15 |
| D4 Skill 可用性规范 | 21 |
| D5 安全与操作风险 | 21 |
| D6 代码与文档质量 | 31 |
| D7 依赖与体量健康度 | 4 |
| **合计** | **115** |

> 📊 **分值规则**：ERR 全统一 3 分（命中即 FAIL，分值无意义）；WARN 按真实优先级分 3 档（高3/中2/低1）。

**双重判定（两个条件同时满足才算通过）**：

通过线统一 90 分（L1/L2 dryRun 两档一致，跳过项不计入实际满分但不影响通过线）：

| 检查深度 | 实际满分 | 通过线 |
|---------|---------|-------|
| L1 静态 | 112 分 | **≥ 90 分** |
| L2 dryRun | 115 分 | **≥ 90 分** |

| 条件 | 结果 |
|------|------|
| 总分 ≥ 对应通过线 **且** 零 ERR | ✅ **PASS** |
| 有任何 ERR，**或** 总分 < 通过线 | ❌ **FAIL** |

---

## Step 6：生成记分卡 MD 文件

按照 [references/output-template.md](./references/output-template.md) 生成完整报告。

写入路径：`{skill-path}/AUDIT-{YYYY-MM-DD}.md`

> `AUDIT-*.md` 不应被打包进 Skill（D4-E5 会检测这一点）。

---

## Step 7：输出摘要

```
📋 审计完成：{skill-name}
─────────────────────────────────────
综合评分：{score}/{满分}   {PASS ✅ / FAIL ❌}（L1 满分112 / L2 dryRun 满分115）
通过线：≥90 分（L1/L2 dryRun 统一）且 零ERR（双重判定）
检查深度：{L1 静态 / L2 dryRun}

🔴 ERR {n} 项 | 🟡 WARN {n} 项
最高优先级修复：{ERR 中最高扣分项的 ID 和名称}

修复所有 ERR 后预计得分：{estimated}/{满分}

📁 记分卡：{skill-path}/AUDIT-{date}.md

🔧 修复：{N} 项可一键修复 / {M} 项需人工确认
   回复「修复」可启动一键修复（修复前会自动备份）
```

---

## Step 8：一键修复（`--fix`）行为规范

> ⚠️ **本步骤是 better-skill-audit 唯一允许修改被审计 skill 文件的动作**，且只能在用户**显式授权**后执行。日常审计（Step 0-7）严格遵守「只审计、不修复」红线。

### 触发条件

- 用户在审计报告后明确回复「修复」「应用修复」「`--fix`」「修复 5.1」等指令
- **未经用户明确授权，绝不自动修复**（报告里只「建议」，不「执行」）

### 修复范围分级（对应报告「五、修复建议」两小节）

| 小节 | 类型 | 可否一键修复 |
|------|------|------------|
| **5.1 可一键修复** | 纯文本/配置/文档（补 version、补前置条件、改文案、补依赖声明、规范引用前缀等，无业务逻辑） | ✅ 用户说「修复」即可批量改 |
| **5.2 需人工确认** | 业务逻辑/脚本代码（改控制流、字段匹配、HTTP 调用、列名映射、移除越权步骤等） | ⚠️ 必须逐条向用户确认，用户点头一条改一条 |

### 执行流程（必须严格按顺序）

1. **修复前备份（强制）**：
   - 把整个被审 skill 目录复制到备份路径：`{skill-path}.bak-{YYYYMMDD-HHMMSS}`
   - **立即告知用户完整备份路径**
   - 备份失败 → 中止修复，不动任何文件
   ```bash
   BACKUP="{skill-path}.bak-$(date +%Y%m%d-%H%M%S)"
   cp -r "{skill-path}" "$BACKUP" && echo "✅ 已备份到 $BACKUP"
   ```

2. **逐项修复**：
   - 5.1 项：按报告「③ 解法」直接 edit，每改一项简短报告「✅ 已修 [ID]」
   - 5.2 项：仅在用户对该条明确确认后才改；用户没点头的不动

3. **修复后不自动重审**：
   - 修复完成后**提醒用户**：`🔧 已修复 {n} 项。是否现在重新审计确认修复效果？（回复"重新审计"启动）`
   - **必须等用户确认「重新审计」后**，才重新跑 Step 0-7

4. **修复记录**：在报告或回复中列出「改了哪些文件 + 哪些项 + 备份路径」，便于用户回滚

### 红线（修复时同样适用）

- 不执行任何写操作
- 不删除任何文件（即使看似冗余），如需删除必须单独问用户
- 5.2 业务逻辑项**绝不擅自改**，哪怕「看起来很安全」
- 修复后若用户要回滚：指引用户用备份目录覆盖恢复

---

## 规则参考

- 完整规则判定逻辑 → [references/check-rules.md](./references/check-rules.md)
- 防误报/边界场景通则 → [references/check-rules.md「防误报通则」段](./references/check-rules.md)
- 受控域名配置（D2-E1，默认空）→ [references/controlled-domains.md](./references/controlled-domains.md)
- 报告 MD 模板 → [references/output-template.md](./references/output-template.md)