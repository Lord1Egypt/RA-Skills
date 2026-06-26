# Song Writer Orchestrator - 歌曲生成编排 Skill

> Phase 2 核心编排器。管理每首歌的 5 专家串行迭代循环(3-6 轮),每轮 5 个**独立子 agent**依次操作同一首歌曲文件。

---

## 核心原则

1. **绝对文件契约**:所有输入/输出严格遵循 `FILE_CONTRACTS.md`,不得偏离
2. **子 agent 强制分离**:作词 ≠ 编曲 ≠ 韵脚 ≠ 市场 ≠ 评分,5 个独立的 `sessions_spawn` 调用
3. **主 agent 只编排**:主 agent 负责启动/等待/判断评分结果,不直接修改任何歌曲文件

---

## 触发

- Phase 1 完成后，`docs/album-overview.md` 状态为“概念确认”
- 用户指令：「开始生成歌曲」「Phase 2」「song writing round」

---

## 启动前提示（用户心理预期管理）

**⚠️ 飞书推送机制关键：消息在 turn 结束后才推送。必须先输出提示文本，然后 spawn 子 agent，最后 `sessions_yield` 结束当前 turn。**

**正确流程（严格按顺序）：**

1. 主 agent 输出提示文本：
   > 🪚 Phase 2 歌曲生成流水线已启动。
   > 每首歌将由 5 位专家串行迭代（作词 → 编曲 → 韵脚 → 市场 → 评分），最少 3 轮、最多 6 轮，N 首歌并行。
   > 预计约 **{估算时间}** 完成。
   > 期间无需等待，完成后我会主动通知你。

2. **立即 spawn 第一批子 agent**（每首歌的作词专家先启动，Round 1 开始）

3. **`sessions_yield` 结束当前 turn** → 提示推送给用户 → 子 agent 后台工作

4. 子 agent 完成后 → 主 agent 收到通知 → 自动 spawn 下一位专家（编曲 → 韵脚 → 市场 → 评分）→ 循环直到该轮完成

5. **Round 2+ 中间不停顿**：评分专家完成后如果未达标，主 agent 直接 spawn 下一轮作词专家，不询问用户

6. 全部歌曲通过后 → 主 agent 汇总结果 → 通知用户 Phase 2 完成

**禁止**：
- Round 之间停下来等用户确认（只有 Round 全部完成后才汇报）
- spawn 子 agent 后不 yield 就挂着等

**估算时间参考**：
- 3 首歌：约 45-60 分钟
- 6 首歌：约 90-120 分钟
- 9 首歌：约 2-3 小时

---

## 输入

从 `docs/album-overview.md` 读取:
- 曲目定位表(# / 曲名 / 英文名 / 叙事轴 / Hook / 悖论 / 意象 / 身体感 / 情绪弧线 / 编曲风格 / 时长)
- 调性主线
- 专辑核心概念
- **语言**(中文 / 中文+英文 / 英文 / **纯音乐**)

⚠️ **纯音乐识别**:如果曲目单中某首「语言」=「纯音乐」,该曲跳过作词专家歌词创作环节,进入「器乐描述」模式(详见下方纯音乐处理)。

---

## 执行架构

```
对曲目定位表中的每首曲目(T1-TN):
  打开 songs/TN-曲名.md(模板已由 Phase 0.5 初始化,填写基本信息表)
  并行启动 N 个 Agent 群
```

### 单首歌曲的 Agent 群内串行流程

```Round = 1
while Round <= 6:
  1. 作词专家 agent → 常规歌曲:读/写歌词区块;纯音乐:写「器乐描述」区块
  2. 编曲专家 agent → 读/写 songs/TN-曲名.md
  3. 韵脚专家 agent → 常规歌曲:韵脚分析;纯音乐:节奏/音色分析
  4. 市场专家 agent → 读/写 songs/TN-曲名.md
  5. 评分专家 agent → 读 songs/TN-曲名.md,输出评分

  读评分结果:
  if Round >= 3 and 评分 >= 80:
    ✅ 通过,标记状态为"✅ 定稿"
    更新 docs/album-overview.md 评分总览
    break
  elif Round == 6:
    ⚠️ 达最大轮次,取最高分版本
    更新 docs/album-overview.md 评分总览
    break
  else:
    标记低分维度 + 优化建议 → Round += 1
    下一轮专家读取上一轮评分结果
```

### 纯音乐处理

当曲目定位表中某首「语言」=「纯音乐」时:

- **作词专家**:跳过歌词创作,写「器乐描述」区块(主旋律情绪弧线/音色/段落意图)
- **韵脚专家**:跳过韵脚分析,写「节奏/音色分析」区块(节奏型/音色层次/动态变化)
- **编曲专家**:无变化,正常填写编曲设计
- **市场专家**:无变化,正常评估市场潜力
- **评分专家**:「韵律」维度替换为「器乐表现力」维度(0-20 分)

### 并行策略

- **N 首歌 = N 个并行 Agent 群**(N = Phase 1 曲目定位表的曲目数)
- 每群内部 5 专家串行操作同一文件
- 群与群之间互不干扰
- 全部群完成后 → 进入 Phase 3

### 子 Agent 调用格式

每个专家必须是独立的 `sessions_spawn` 调用:

```python
# 作词专家
sessions_spawn(
    runtime="subagent",
    mode="run",
    task="""
你是作词专家。正在处理歌曲:songs/T{N}-{曲名}.md

当前轮次:Round {X} / 最多 6 轮
上一轮评分:总分 {XX}(各维度分)
低分维度:[如有]
优化建议:[如有]

⚠️ 硬规则:你只能修改你负责的区块,不得修改/新增/删减其他任何区块。
详见 FILE_CONTRACTS.md 中「Phase 2 契约 → 硬规则:文件修改范围限制」。

请按照你的 SKILL.md 中的 checklist 执行。
读取 songs/T{N}-{曲名}.md 的当前内容,做你的工作,写回文件。
严格遵守 FILE_CONTRACTS.md 中 Phase 2 的文件格式契约。

最后,在你的工作区末尾输出:
✅ 作词专家 Round {X} Checklist:
- [ ] 检查项1
- [ ] 检查项2
...
"""
)

# 编曲专家 → sessions_spawn(独立调用)
# 韵脚专家 → sessions_spawn(独立调用)
# 市场专家 → sessions_spawn(独立调用)
# 评分专家 → sessions_spawn(独立调用)
```

---

## Phase 2 Checklist(全局)

完成时确认:
- [ ] 所有 `songs/T{N}-*.md` 存在且非空
- [ ] 每首评分 ≥ 80 分 + 跑满 3 轮(或达最大轮次 6 轮)
- [ ] `docs/album-overview.md` 评分总览已更新
- [ ] 每首歌曲文件格式通过 FILE_CONTRACTS.md 校验

全部 ✅ → 进入 Phase 3(歌词标准化提取)

---

## 输出文件契约

严格遵循 `FILE_CONTRACTS.md` 中 Phase 2 契约。

---

## 参考

- `examples/songs/T1-出发.md` - 98 分终稿范例
- `FILE_CONTRACTS.md` - Phase 2 文件格式契约
