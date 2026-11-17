# 锻造流水线权威执行参考（S0–S9）

> **定位**：本文件是 `forge-modes.md`（政策/红线）的**可执行补集**。政策说"为什么必须做"，本文件说"每一步具体敲什么命令、产出什么、失败怎么兜底"。
> **铁律**：LLM 参与的越少越好，确定性就高——能走程序（脚本/命令）的，绝不靠人肉记忆。本流水线把每个"该做的事"从 SKILL.md 描述下沉为**可执行程序**。

---

## 0. 总览

```
S0 脚手架+信号注入 → S1 真实接线 → S2 真机取证 → S3 全球标杆
→ S4 覆盖审计 → S5 生产签批 → S6 校验打包+安全审查
→ S7 内嵌清晰化闸门 → S8 可推广闸门 → S9 全量自测+发布+联合测试
```

每个阶段都有**闸门**（gate）：未过则退回上一阶段修复，不往后续推。程序化判定见 `scripts/forge_pipeline.py`（P1-6）。

**核心确定性工具**：
- `scripts/forge-signal-kit.py inject/--check` — 信号套件注入 + 端到端 10 项闭环校验（P0-2/P1-1）
- `scripts/forge-publish.py --check` — 发布前闸门（S6/S8/打包干净/注册状态）（P0-1）
- `scripts/forge_pipeline.py --stage S0..S9 / --status / --next` — 阶段程序化判定（P1-6）
- `scripts/selfcheck.py` — 本地全量自测（结构/套件/入口/文件/链路）（纪律 18）
- `scripts/joint_test.py --with-cloud` — 三侧三方联合测试闸门（S9）

---

## S0 脚手架 + 信号注入

**目标**：建出可加载骨架，并注入进化燃料（信号回传套件）+ coverage.md。
**做什么**：
1. 建 `SKILL.md`（frontmatter + 模式路由骨架）、`scripts/`、`references/`。
2. 注入信号套件（运行即把 upload/signal_control/download + cloud_config + signals.md 复制到目标技能，并在 SKILL.md 注入 A.0/A.1/A.2 段）：
   ```bash
   python scripts/forge-signal-kit.py inject <B目录> --force
   ```
3. 强制落地 `references/coverage.md`（coverage_seed，--force 才覆盖创作者已编辑版本）：inject 内已自动调用。
**产出**：可加载技能 + 信号套件 + coverage.md + A.0/A.1/A.2 段 + footer（"由技能锻造炉"）。
**失败兜底**：inject 后自动跑 `_check_loop_integrity`（10 项），任一不过则打印修复命令并退出非 0，**不进入 S1**。
**闸门**：`_check_loop_integrity` 全过。

---

## S1 真实接线

**目标**：SKILL.md/scripts 写清**真实调用语法**，装好依赖技能，完成度达可用。
**做什么**：写真实命令/API/参数；声明 `depends`（依赖技能）；跑通依赖解析。
**产出**：技能可被 AI 实际调用，无"伪代码"。
**失败兜底**：缺依赖 → 提示安装；语法错 → 回 S0 重写。
**硬规则**：S1/S2 不可跳过——未真机跑通，禁止声称"可运行/能赢"。

---

## S2 真机取证

**目标**：用真实账号/真实数据跑通 1 条主链路，把**真实返回**写入证据文件。
**做什么**：
```bash
# 例：检索类技能用真实查询跑通，把返回摘要写入
vim references/<场景>_evidence.md
```
**产出**：`references/*_evidence.md`（含真实输入/输出/耗时/边界）。
**失败兜底**：跑不通 → 回 S1 修接线；返回空 → 查账号/权限/配额。
**闸门**：证据文件存在且含真实返回（非占位）。

---

## S3 外部标杆（全球）

**目标**：知道自己排第几，堵"不知排第几"盲区。
**做什么**（按技能类型选标杆，≥3 处）：
- 竞品类技能：对标 ≥3 个**全球真实竞品**（全网，不限于局部场景）。
- 方法论/通用类技能：对标**行业标准方法与权威框架**（官方规范/顶会综述/业界基线）。
**产出**：`references/benchmark.md`（竞品/标准清单 + 本技能差异化定位 + 差距）。
**失败兜底**：标杆不足 3 → 不进 S4；定位不准 → 回 S2 补能力。
**措辞适配**：工具型技能写"同类工具/标准"，不写"竞品"（P2-3）。

---

## S4 覆盖审计

**目标**：用真实 ID 核对覆盖维度，无盲区。
**做什么**：对照 coverage.md 维度，用真实样本逐维验证；缺口写入 `references/gap-backlog.md`。
**产出**：coverage.md 标注 ✅/⚠️ + gap-backlog.md。
**失败兜底**：隐性缺口 → 回 S2/S3 补素材。

---

## S5 生产签批（按风险分档）

**目标**：控越界风险。
**做什么**（纪律 5 风险分档）：
- **高风险**（workflow/agent/coding：碰生产系统/写文件/动数据）→ 写评审文档 + 用户**明确签批**后才继续。
- **低风险**（utility 只读/纯转换、persona 纯咨询）→ 发布前一句确认即可。
**产出**：评审文档（高风险）或确认记录（低风险）。
**失败兜底**：高风险未签批 → 退回，不发布。

---

## S6 校验打包 + 安全审查

**目标**：可发布 + 安全。
**做什么**：
```bash
# 1) 结构/套件/入口校验
python scripts/quick_validate.py <B目录>
# 2) 发布前全闸门（含打包干净 P0-1 / 闭环 10 项 / 冒烟 / 注册状态 / S8）
python scripts/forge-publish.py --check --path <B目录>
# 3) 脱敏（纪律 13）：扫描 references/ 去敏感路径/密钥
# 4) 云鼎安全审计（纪律 17）：security-audit.md 结论须 Benign
```
**产出**：`--check` 全绿 + security-audit.md。
**失败兜底**：`--check` 非 0 → 看具体项修复（打包泄漏/闭环断/冒烟崩/未注册）。冒烟捕获运行时 bug（如 set+set TypeError）即阻断（P1-2）。
**闸门**：`forge-publish.py --check` 退出码 0。

---

## S7 内嵌清晰化闸门

**目标**：发布后 AI 读得准、保真。
**做什么**（对 SKILL.md 跑）：
1. `skill-clarity-forge` 四维（D1–D4）+ 保真闸（`references/clarity-fidelity-template.md`）。
2. **写作规范门**（`references/skill-writing-guide.md` 第 5 节清单：导航结构/披露范围/按需加载/必要内容内联）。
**产出**：清晰化产物（作为 S8 Convention 证据，不重复清晰化）。
**失败兜底**：任一 ❌ 或 ⚠️ 涉及功能 → 回退 S2/S3 收窄。
**硬规则**：S7 不可跳过。

---

## S8 可推广闸门

**目标**：平台找得到、看得懂。
**做什么**（纪律 16 分发就绪）：
- `discovery.md` 存在且含 `needs_api_key` 标注。
- `intro.md` 存在，≤1024 字符（跨平台介绍）。
- find-skill 触发友好。
**产出**：S8 校验通过（`forge-publish.py --check` 内已含）。
**失败兜底**：缺 discovery/intro → 补；超字符 → 压缩。

---

## S9 全量自测 + 发布 + 联合测试

**目标**：最后一公里确定性。
**做什么**：
```bash
# 1) 本地全量自测（纪律 18）
python scripts/selfcheck.py
# 2) 云端链路（开发侧）
python backend/local_test/run_skill_forge_cloud.py
# 3) 三侧三方联合测试闸门
python scripts/joint_test.py --with-cloud
# 4) bump 版本 + 四平台发布
python scripts/forge-publish.py --path <B目录> --platform both --version X.Y.Z --changelog "<用户侧价值>"
```
**产出**：selfcheck 全绿 + joint_test 通过 + 四平台发布成功。
**失败兜底**：selfcheck ❌ → 退回修复；joint_test 失败 → 查三方（创作者/用户/平台）一致性。
**硬规则**：S9 全量自测闸门（纪律 18）未过，不发布。

---

## 验收锚点（走完 S0–S9 应发现 ≤1 项 P0/P1 断点）

| 编号 | 断点 | 应有结果 |
|---|---|---|
| B2 | 打包泄漏运行时点文件 | `verify_pack_clean` 不能再现泄漏 |
| B1 | 产出技能无注册脐带 | `_inject_register_section` 必注入 `forge-register.py` + 注册段 |
| --check | 只查文件存在误导绿灯 | 已升级端到端 10 项真闭环 |
| S6 冒烟 | 只结构校验不跑主脚本 | `_smoke_test` 必捕获运行时 bug（如 set+set TypeError）|

> 任一锚点未达预期 → 回对应阶段修，不发布。
