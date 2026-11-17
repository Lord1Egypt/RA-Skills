---
name: "gaoshu-questionbank-workflow"
description: "高数题库批量出题工作流：选章→撞车排查→生成→分布校验→双维度去重→入库→复核→归档"
---

# 高等数学智能题库 · 批量出题工作流技能

> 版本：1.1（2026-09-01 升级：merge 去重升级为「q[:80] + 数学签名归一化」双维度，实战验证抓出 30+ 措辞微变同题）
> 适用：省级大学数学 OpenClaw 培训 / 高数题库扩展生产
> 目标：每批 40 题（14+13+13 三章），质量红线全部达标后入库

---

## 一、技能概述

本技能定义「高等数学智能题库」从选题到入库的完整生产流水线。已在主库 3746 题上稳定运行 24+ 批次（B54–B77 等），每批 40 题零质量事故。

**何时使用**：用户要求"继续 BXX / 生成下一批题目 / 补某章题目"时，按本工作流执行。

**核心质量红线**（每批必须全部满足）：
1. 40 题 = 三章（14+13+13），solution 分数全部为整数且 sum=10
2. reviewed 100% = True（导入时 `--approved`）
3. 与主库 0 重复（**双维度**：q[:80] 精确比对 + 数学签名归一化比对，导入前 merge 校验）
4. type/bloom/diff 三章全部精确命中目标分布
5. 答案逐题验算（生成前手算、merge 后抽查）

---

## 二、项目结构与工具

```
kaoyan1/
├── data/
│   ├── 高数智能题库_主库.json      # 主库（每题 20 字段）
│   ├── pending/                    # 生成脚本/raw 文件/进度快照
│   ├── approved/                   # 入库后归档
│   └── backlog/ rejected/
├── pipeline/
│   └── import_batch.py             # 入库脚本：python import_batch.py <file> --approved
└── 题库建设工作流_v2.md            # 工作流参考
```

- 主库 JSON：数组，每题含 q/type/options/answer/solution/hints/common_errors/bloom_level/thinking_type/tags/difficulty/estimated_time/prerequisites/chapter/section/application/id/author/created/reviewed
- 章目标量：Ch1=450, Ch2=550, Ch3=550, Ch4=200, Ch5=400, Ch6=550, Ch7=400, Ch8=400（总 3500）
- 运行环境：Windows + Python 3.12（标准库即可，无需第三方依赖）

---

## 三、八步工作流

### ① 选章
1. 读主库统计各章完成率（或读 MEMORY.md 进度表）
2. 原则：优先补完成率最低的章；每批 3 章 = 1 个 14 题章 + 2 个 13 题章
3. 完成率接近时按"目标缺口"选（缺口 = 目标 - 现有）
4. 每批结束后在记忆文档更新「下批建议」，下一批按建议执行

### ② 撞车排查（最关键，决定质量）
1. 提取目标章全部题目的 q 文本到快照文件（按行，每题一行）：
   ```python
   lines = [q['q'].replace('\n',' ') for q in master if q['chapter'] in ('3','6','8')]
   open('data/pending/bXX_existing_XXX.txt','w',encoding='utf-8').write('\n'.join(lines))
   ```
2. **通读**目标章全部现有题（快照文件直接 read）
3. 小章（如 Ch4）生成逐题列表（type|bloom|difficulty|q 一行一题）
4. 候选题目设计完成后，对关键表达式 grep 快照确认不撞
5. 已知雷区：
   - 常见积分/极限模板（`∫xe^x`、`∫x/(1+x²)²`、`(e^x-1-x)/x²`、`tan x - x` 等）主库已有 N 遍
   - 双中值题：主库已有 `1/f'(ξ₁)+1/f'(ξ₂)=2`、`f'(ξ₁)f'(ξ₂)=1`，同型必撞
   - 选择题固定开头（如 `下列反常积分中收敛的是（ ）`）前 80 字符即触发去重 → 用变体措辞（如加逗号）
   - 特征方程/欧拉方程系数组合、傅里叶展开函数（`f(x)=x`、`x²` 在 [-π,π] 已多版本）
   - **措辞/格式微变不算新题**：`求 vs 计算`、`$ vs $$`、`∑ vs Σ`、`\frac1x vs \frac{1}{x}`、开头动词差异——同一数学题改措辞仍会撞数学签名归一化（2026-09-01 教训，见⑦）

### ③ 写生成脚本（每章一个 gen_bXX_chY.py）
- 每题一个 `P.append({...})`，字段见第四节 schema
- 脚本末尾内嵌自校验：打印 type/bloom/diff 三个 Counter 与目标对比 + score sum=10 检查
- 中文文本内部禁止 ASCII 引号（会破坏 Python 字符串 → 用全角引号）；LaTeX 反斜杠用 `\\` 转义
- solution 每步有梯度（6+4 或 4+4+2），总计恰为 10

### ④ 跑脚本自校验
- 每个 gen 脚本运行后检查输出：
  - type/bloom/diff 与目标**完全一致**
  - `Score sum=10: True`
- 分布有偏差 → 调整某题 bloom_level/difficulty 字段（不换题）或删/补 calc 题
- ⚠️ 13 题章只写 13 题；14 题章写 14 题（写多会破坏 calc=4/5）

### ⑤ merge 合并 + 双维度去重（merge_bXX.py）——★2026-09-01 升级
1. 读三个 `bXX_chY_raw.txt` → 逐章校验（题数/score/chapter/diff）→ 合并 40 题
2. **第一维 q[:80] 精确比对**：与主库 q[:80] 去重比对 → 写 `bXX_raw.txt`
   ```python
   existing = {q['q'][:80] for q in master}
   dups = [q for q in batch if q['q'][:80] in existing]
   ```
3. **第二维 数学签名归一化比对（必做，q[:80] 会漏掉措辞/格式微变的同题）**：
   - 归一化规则（顺序执行）：去全部空白 → 去中文标点（，。；：、？！（）()[]{}""''）→ 去 `$` → `\limits`/`\displaystyle` 删除、`\dfrac`→`\frac` → `∑`/`Σ`→`\sum` → 去 `\,`/`\!`/`~` → `\frac1x` 简写展开为 `\frac{1}{x}`（正则循环 3 次）→ 去开头动词（求极限/证明/计算/判断/讨论/利用/求/设函数/设/解，取第一个命中）→ 去结尾句号
   - 判定：归一化后**完全一致** → 候选重复 → **逐对核对答案**：
     - 答案一致 → 真重复，删
     - 答案不同 → 保留，且**分别验算**——同题干不同答案可能是不同题（选项不同）或**错题**（答案笔误）
   - 参考实现（可直接嵌入 merge 脚本）：
     ```python
     import re
     def norm(s):
         s = re.sub(r"\s+", "", s)
         s = re.sub(r"[，。；：、？！（）()\[\]{}\"']", "", s)
         s = s.replace("$", "").replace("\\limits", "").replace("\\dfrac", "\\frac").replace("\\displaystyle", "")
         s = s.replace("∑", "\\sum").replace("Σ", "\\sum")
         s = s.replace("\\,", "").replace("\\!", "").replace("~", "")
         for _ in range(3):
             s = re.sub(r"\\frac(\d+|[a-zA-Z])(\d+|[a-zA-Z])", r"\\frac{\1}{\2}", s)
         for v in ["求极限", "证明", "计算", "判断", "讨论", "利用", "求", "设函数", "设", "解"]:
             if s.startswith(v):
                 s = s[len(v):]
                 break
         return s.rstrip("。")
     # 比对：norm(new_q) in {norm(q['q']) for q in master} → 撞车
     ```
4. 有 DUP → 查看撞题 → 替换该题（换题或改措辞）→ 重跑该章 gen + merge
5. **删除后须重跑双维度扫描**，确认残留均为刻意保留（不同题/不同题型/换壳变体），避免误删

### ⑥ 导入主库
```bash
python pipeline/import_batch.py data/pending/bXX_raw.txt --approved
# 期望输出: 入库: 40 题 | 去重: 0 题 | 状态: 已审核
```

### ⑦ verify 复核（verify_bXX.py）
- 主库总题数 = 上批 + 40
- 尾部 40 题：reviewed 全 True、score 全 10、id 唯一、chapter/type 分布正确
- 全库统计：reviewed!=True 数量 = 0；q[:80] 重复组数 = 0；**数学签名归一化重复组数 = 0**
- 更新各章完成率

### ⑧ 记录归档
1. MEMORY.md 追加本批记录：时间、章节组合、主库增量、分布确认、撞车避让明细、亮点题 2-3 道、更新进度表与下批建议
2. 定期更新进度存档文档（`出题进度_B01-BXX_日期.md`）
3. 生成脚本/merge/verify/raw 全部保留在 data/pending/（不清理）

---

## 四、题目 Schema 规范

```json
{
  "q": "题干（LaTeX，$…$）",
  "type": "calc|choice|fill|judgment|proof",
  "options": ["A. …", "B. …"],          // 仅 choice
  "answer": "答案",
  "solution": [{"text": "步骤1", "score": 6}, {"text": "步骤2", "score": 4}],  // 分数和=10
  "hints": [{"level": 1, "text": "提示1"}, {"level": 2, "text": "提示2"}],     // 2-3 层，递进
  "common_errors": [
    {"error": "典型错误", "reason": "原因", "type": "conceptual|computational|procedural|strategy"}
  ],
  "bloom_level": "L1-L6",
  "thinking_type": "程序性|分析性|批判性|创造性",
  "tags": ["…"],
  "difficulty": "basic|advanced|mastery|challenge",
  "estimated_time": 2-10,
  "prerequisites": ["…"],
  "chapter": "1-8",
  "section": "与主库现有分类一致",
  "application": "应用领域（纯数学/物理/金融/AI/医学/无人机等）"
}
```

**Bloom 层级参考**：L1 记忆/程序、L2 理解、L3 应用、L4 分析、L5 综合/评价、L6 创造/证明

---

## 五、分布模板（每批必须精确命中）

| 章规模 | type | bloom | difficulty |
|:---:|:---|:---|:---|
| **14 题章** | calc5 / choice2 / fill2 / judgment2 / proof3 | L1=1, L2=2, L3=3, L4=3, L5=3, L6=2 | basic1 / adv5 / mastery5 / chal3 |
| **13 题章** | calc4 / choice2 / fill2 / judgment2 / proof3 | L1=1, L2=1, L3=3, L4=3, L5=3, L6=2 | basic1 / adv4 / mastery5 / chal3 |

（各章批量历史：B54–B77 全部精确命中，此为成熟标准）

---

## 六、质量标准与验收清单

**入库前（merge 通过才算）**：
- [ ] 三章题数 = 14/13/13
- [ ] 每章 chapter 字段与文件名一致
- [ ] score 全部整数且 sum=10
- [ ] type/bloom/diff 三章精确命中模板
- [ ] 与主库 0 重复（**q[:80] + 数学签名归一化双维度**）

**入库后（verify 通过才算）**：
- [ ] 主库 +40
- [ ] 尾部 40 题 reviewed 全 True、score 全 10、id 唯一
- [ ] 全库 reviewed!=True = 0
- [ ] 全库 q[:80] 重复组数 = 0
- [ ] 全库数学签名归一化重复组数 = 0

**内容质量**：
- 答案逐题验算（隐函数二阶导、旋转曲面、反常积分值等易错点手算）
- hints 分层递进（先概念后操作）
- common_errors 覆盖概念/计算/过程/策略四类错误
- 题面数值先验证再写入

---

## 七、常见错误与历史教训

| 现象 | 原因 | 对策 |
|:-----|:-----|:-----|
| 生成脚本 SyntaxError | 中文文本内嵌 ASCII 引号 | 用全角引号「」或转义 |
| 撞车漏检 | grep 时 `\tan` 的 `\t` 被正则当制表符 | grep 用 `\\tan` 或纯文本 `tan` |
| 双中值题重复 | 结论变体（和/积/倒数）仍撞前 80 字符 | 直接换题，不做同型变体 |
| 选择题去重误报 | 固定开头（`下列…中收敛的是`） | 措辞加变体（加逗号等） |
| 13 题章写出 14 题 | 模板混淆 | 写前确认章规模与分布模板 |
| **措辞/格式微变漏检（2026-09-01）** | 同题但 `求 vs 计算`、`$ vs $$`、`∑ vs Σ`、`\frac1x vs \frac{1}{x}`、开头动词差异 → q[:80] 不同 | merge 必做数学签名归一化二次扫描；设计阶段避免"改措辞当新题" |
| **同题干不同答案（2026-09-01）** | 可能是不同题（选项内容不同）或**错题**（答案笔误） | 逐对核对答案：答案一致→删；不同→分别验算，错题删除（例：HC0884-020 特解 +xe^x 应为 -xe^x，靠比对暴露） |
| **早批次重复密度高（2026-09-01）** | 7/24-8/01 批次措辞不规范（HC03不定积分-001~025 与 -096~-102、HC01极限计算家族） | 新批次设计阶段查重 + merge 双维度扫描兜底 |

---

## 八、交付物与归档

每批交付：
- `data/pending/gen_bXX_chY.py`（3 个生成脚本，含自校验）
- `data/pending/merge_bXX.py`（含双维度去重）、`verify_bXX.py`
- `data/pending/bXX_chY_raw.txt`、`bXX_raw.txt`
- 主库增量 +40（reviewed=True）
- MEMORY.md 批次记录 + 进度表更新
- 定期：`出题进度_B01-BXX_日期.md`（含亮点题、下批建议）

---

## 九、培训要点（省级培训使用）

1. **演示路径**：从主库统计 → 撞车排查 → 生成 3-5 题示范 → merge（含双维度去重演示）→ import → verify 全流程走一遍
2. **强调质量红线**：分布模板精确命中 + score=10 + 双维度 0 重复是硬指标，任何一条不满足不放行入库
3. **撞车排查是质量核心**：宁可多花时间通读现有题，不要靠运气；**数学签名归一化是第二道保险**，q[:80] 挡不住措辞微变
4. **练习任务**：给定一个 13 题章，学员独立完成 13 题生成并通过 merge 双维度校验
5. **常见坑演示**：ASCII 引号、`\t` grep、选择题措辞重复、`求 vs 计算` 措辞微变
