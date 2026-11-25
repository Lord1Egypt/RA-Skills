# Dialog Discovery Skill

从原始对话数据中做**弱监督发现**：先筛高置信正向种子、失败种子和边界风险样本，再提取候选规则、候选话术与问题模式。

> **定位**：这是一个独立的数据挖掘 skill，负责原始对话分析，不负责 PE 对练、PE 改写、PE 提交与验证。
> **当前重点场景**：已针对 **金条人工外呼 ASR 转写文本** 做了专项增强。
> **共享资源**：本 skill 通过软链接复用 `../pe-self-improving/` 下的 `scenes/` 与部分 `prompts/`，避免重复维护。

---

## 一、适用场景

当用户表达以下意图时触发：

- “挖掘对话数据”
- “挖掘 goodcase / badcase”
- “聚类分析对话”
- “批量分析对话”
- “批量评分”
- “从原始对话中学习”
- “自动筛选优质案例”
- 提供 Excel / JSON / CSV 大文件（通常 >50 条）并希望从中发现规律
- 提供 **ASR 转写文本 / 录音转文字**，希望从中筛选候选好案例、坏案例或模式

**负向排除**：
- 用户明确说“优化 PE / 进化 PE / 对练 / 对练结果” → 转到 `pe-self-improving`
- 用户明确说“金牌客服 / 金牌对话 / 学习金牌案例” → 优先转到 `pe-self-improving`

---

## 二、当前工作模型

本 skill 不假设：
- 文本是干净的
- 数据有人工标注
- 一轮规则就能直接给最终 good / bad 标签

默认采用的工作模型是：

```text
原始对话
  → 标准化 / ASR 清洗
  → 特征提取 / 弱监督信号生成
  → 分桶：good_seed / bad_seed / gray_* 
  → 聚类分析
  → 提取候选规则 / 约束规则 / 待验证假设
  → 生成人工 review 包
```

**重要**：
当前输出更接近：
- 高置信正向样本
- 高置信失败样本
- 高风险边界样本

而不是最终版 goodcase / badcase 标注器。

---

## 三、核心入口

命中本 skill 后，优先阅读：

- `playbooks/discover-from-raw-dialogs.md`

这是主执行说明，包含：
- 输入要求
- 数据类型判断
- 标准执行链路
- ASR 场景下的弱监督分桶逻辑
- 脚本调用顺序
- 输出规范
- 学习库写入规则

---

## 四、资源结构

### 4.1 本 skill 自有内容

- `playbooks/discover-from-raw-dialogs.md`
- `scripts/normalize_dialogs.py` - ASR 友好标准化
- `scripts/template_match_dialogs.py` - 弱监督特征提取与分桶
- `scripts/batch_score_dialogs.py` - rules / llm / hybrid / weak_label
- `scripts/llm_score_background.py` - 后台 LLM 评分
- `scripts/cluster_dialogs.py` - 基于 seed_label 的分桶聚类
- `scripts/extract_rules_from_cluster.py` - 从分桶结果提取候选规则 / 假设
- `scripts/sample_for_review.py` - 生成人工 review 包
- `scripts/auto_evolve_features.py` - 自动进化特征规则（挖掘后必须执行）
- `scripts/identify_scene.py`
- `scripts/discover_dialogs.py`
- `scripts/common.py`
- `scripts/llm_client.py`

### 4.2 软链接共享内容

- `scenes/` → `../pe-self-improving/scenes/`
- `prompts/collection` → `../pe-self-improving/prompts/collection`
- `prompts/exhibition` → `../pe-self-improving/prompts/exhibition`
- `prompts/loan` → `../pe-self-improving/prompts/loan`
- `prompts/output-format.md` → `../pe-self-improving/prompts/output-format.md`

**原则**：
- 修改评分标准、特征规则、弱监督权重 → 只改 `scenes/{scene}.yaml`
- 不在两个 skill 内重复维护场景配置

---

## 五、硬约束

### 5.1 学习库不拆分

挖掘结果继续写入统一学习库：

```text
~/pe-self-improving/memory/{target_scene}/warm/
```

不要为本 skill 单独再造一套 memory 目录。

### 5.2 长任务优先后台执行

以下脚本属于长任务，优先后台执行：

- `scripts/batch_score_dialogs.py`
- `scripts/llm_score_background.py`
- `scripts/discover_dialogs.py`

外层 timeout 要大于脚本内部超时，建议 600s+。

### 5.3 配置唯一来源

统一从 `scenes/{scene}.yaml` 读取：
- `scoring`
- `feature_rules`
- `asr_robustness`
- `weak_supervision`

禁止在脚本里维护第二份业务规则真相。

### 5.4 “中途挂断”不是单点结论

在 ASR / 外呼场景中：
- `early_hangup` 只能作为过程信号
- 不能直接等价为 badcase
- 必须和拒绝、负面情绪、长单边输出、重复推进等信号组合判断

### 5.5 产品异议 ≠ 对话失败

对于人工外呼文本：
- “利率高 / 额度低 / 借不出来” 更可能是 **product objection**
- “别打了 / 不想听 / 挂了 / 不方便继续” 才更接近 **conversation rejection**

这两类信号必须分开处理。

---

## 六、默认输出物

在一次完整挖掘中，常见输出包括：

- 标准化结果 JSON
- 弱监督分桶结果 JSON
- `good_seed / bad_seed / gray_*` 分桶聚类结果
- 候选规则文档
- 人工 review 抽样包（JSON / Markdown）

如果是金条 ASR 场景，优先关注：
- `good_seed`
- `bad_seed`
- `gray_high_risk`

---

## 七、维护原则

- 新增挖掘流程 → 放 `playbooks/`
- 新增挖掘脚本 → 放 `scripts/`
- 新增场景规则 / 评分标准 / 弱监督权重 → 修改软链接目标 `../pe-self-improving/scenes/*.yaml`
- 不要把 PE 对练、PE 优化、PE 提交逻辑重新混回来
- 如果文档描述和代码能力冲突，以“当前脚本实际行为”为准，及时同步 playbook

---

*创建时间：2026-04-11*
*最近更新：2026-04-11（对齐 ASR 弱监督分桶重构）*
*用途：从原始对话数据中独立挖掘候选好案例、失败案例与边界模式*