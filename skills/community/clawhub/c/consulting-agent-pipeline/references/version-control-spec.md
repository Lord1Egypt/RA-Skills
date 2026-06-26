# Version Control Spec — 版本快照与验证规则

> 首钢吉泰安项目留下了 v1/v2/v3/v4/v5/适配版_v2 共6个版本目录。每次迭代都必须有版本快照，回退有据可查。

## 版本命名规范

```
{产物类型}_{项目ID}_v{N}[_{日期}][_{说明}]

示例：
  PPT_框架_SG_v3_20260409_深改版.pptx
  PPT_正式提交_SG_v2_20260412_适配版.pptx
  调研报告_SG_G1_污泥_v1_20260410.docx
  审核意见_SG_v4_第3轮_20260410.md
```

## 版本快照时机

每个 Phase 结束时必须做快照：
- `Phase 1`（调研）→ 每个专题一份 `产出文档_v{N}.md`
- `Phase 3`（执行）→ 每个版本一份完整目录快照
- `Phase 4`（审核）→ 每轮审核意见一份 `audit_v{N}_r{N}.md`

## 目录快照规则

```bash
# 快照脚本（每次交付后执行）
snapshot_dir.sh
  输入：源目录路径 + 版本标签
  输出：快照目录 `__snapshots/v{N}_${日期}/`
  包含：全套文件副本 + 快照元数据.json
  不包含：node_modules/.git/大型PDF原始文件
```

## 首钢吉泰安版本目录结构

```
03_PPT框架协作包/
├── 05_PPT框架初稿/          # v1（2026-04-09）
├── 06_修订版/               # v2（2026-04-09）
├── 06_深改版/               # v3（2026-04-09）
├── 07_v5深化版/             # v4→v5（2026-04-10）
├── 08_v4审核收口版/         # v4 收口版（保留不动）
└── 08_正式提交app/
    └── 适配版_20260412/     # v2（2026-04-12/04-13）
```

**关键原则**：每个版本目录保留原版不动，新修改写入新版目录。禁止覆盖历史版本。

## 验证规则

### PPTX 交付物验证（每轮必须执行）

```yaml
schema: deliverable-schema
checks:
  - name: page-count
    description: 页数必须等于约定页数
    severity: P0

  - name: chart-files
    description: 所有图表文件必须存在且被 PPTX 引用
    severity: P0

  - name: fonts-embedded
    description: 关键字体必须嵌入
    severity: P1

  - name: hyperlinks
    description: 超链接必须有效（来源角标）
    severity: P1

  - name: forbidden-terms
    description: 禁用词扫描通过
    severity: P0
```

### 目录结构验证

```bash
validate-handoff.sh
  检查：交接文档 YAML frontmatter 格式正确
  检查：sender/receiver 已在 AGENT_REGISTRY 注册
  检查：status 为有效状态值
  检查：depends_on 引用的任务ID存在
  检查：produces 引用的任务ID已被规划
```

## 回退流程

当新版本发现问题需要回退时：
1. 编排者（Orion）在 PROJECT_STATE 中记录：`current_version` 回退到 `v{N}`
2. 通知相关 Agent 从哪个版本继续
3. 在 DECISION_LOG 中记录回退原因
4. **不删除**新版本目录（保留快照）

## 首钢吉泰安回退实例

v4→v5 迭代中，v5 新增内容质量不稳定：
- **决策**：保留 v4 作为稳定回退版本，新增 v5 为探索版
- **执行**：v5 写入 `07_v5深化版/`，v4 保留在 `08_v4审核收口版/`
- **结果**：双版本并存，汇报时灵活选择
