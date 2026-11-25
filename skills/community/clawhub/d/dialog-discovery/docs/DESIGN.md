# Dialog Discovery Skill 设计文档

> 版本：v2.1
> 更新时间：2026-04-21
> 场景：金条（loan）/ 催收（collection）/ 会展（exhibition）

---

## 一、定位

Dialog Discovery 是一个**独立的数据挖掘 skill**，负责从原始对话数据中做弱监督发现，产出候选 goodcase/badcase、问题模式、候选规则和话术。

**核心区别**：

| Skill | 输入 | 输出 | 职责边界 |
|-------|------|------|----------|
| **dialog-discovery** | 原始对话（未标注，50-2000条） | good_seed/bad_seed/候选规则/候选话术 | 只做挖掘，不做 PE 改写 |
| **pe-self-improving** | 挖掘结果/对练结果/金牌对话 | 候选PE/验证报告 | 负责 PE 进化、对练、门禁 |

典型链路：`dialog-discovery（挖掘）` → `pe-self-improving（进化）`

---

## 二、系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    原始对话数据                           │
│          (Excel / JSON / CSV, ASR转写文本)                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Step 1: 标准化 + ASR 清洗                    │
│  normalize_dialogs.py                                   │
│  · 角色分离（机器人/用户/ASR交替启发式）                    │
│  · ASR 噪声评估                                         │
│  · 对话元信息（轮次/结束类型/长度）                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           Step 2: 弱监督特征提取 + 分桶                    │
│  template_match_dialogs.py                              │
│  · 7 大特征维度（见第三节）                                │
│  · 信号生成（positive/negative/risk/quality）              │
│  · 评分 + seed 分桶                                      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           Step 3: 分桶聚类分析                            │
│  cluster_dialogs.py                                     │
│  · 按 seed_label 分桶统计                                │
│  · 高频信号分布                                          │
│  · 模式共性分析                                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│     Step 4: LLM 深度提取候选规则/约束/假设（v2.1）        │
│  extract_rules_from_cluster.py                          │
│  · --mode llm（默认）：LLM 从抽样对话归纳实质规则/话术    │
│  · --mode stats：信号频率统计（辅助参考）                  │
│  · good_seed → 候选规则 + 候选话术                        │
│  · bad_seed → 约束规则 + 问题模式                         │
│  · gray → 待验证假设                                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│      Step 5: 深度分析（v2.1 新增，推荐）                   │
│  · 抽样读 good_seed / bad_seed 原文                      │
│  · 归纳策略类型（利益对比/流程引导/情感共鸣）               │
│  · 识别关键转折点（从拒绝到接受）                          │
│  · 追加或修正 LLM 自动提取结果                             │
│  · 写入 warm 层 6 个规范文件                              │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           Step 6: 人工 review 抽样包                      │
│  sample_for_review.py                                   │
│  · 各桶抽样 30 条                                        │
│  · 校准规则误伤                                          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│       Step 7: 自动进化特征规则（v2.0）                     │
│  auto_evolve_features.py                                │
│  · 信号覆盖缺口检测                                      │
│  · 提取未覆盖的高频短语                                    │
│  · 自动补入 feature_rules                                │
│  · 记录进化历史                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 三、特征提取体系（7 大维度）

### 3.1 用户信号

| 特征 | 配置键 | 说明 |
|------|--------|------|
| 拒绝信号 | `user_refusal` | "不用""不需要""算了"等 |
| 忙碌信号 | `user_busy` | "忙""开会""开车"等 |
| 询问信号 | `user_question` | "干嘛""什么事"等 |
| 兴趣信号 | `user_interest` | "多少钱""怎么借""额度"等 |
| 接受信号 | `user_acceptance` | "可以""行""好的"等 |
| 负面情绪 | `user_negative_emotion` | "烦""骚扰""骗人"等 |
| 终止信号 | `user_terminal` | "挂了""就这样"等 |

### 3.2 用户主动提问分类（v2.0 新增）

| 提问类型 | 配置键 | 关键词示例 |
|----------|--------|------------|
| 还款相关 | `user_question_types.repayment` | "怎么还款""违约金""灵活还" |
| 利率费用 | `user_question_types.interest_rate` | "利息多少""年化""手续费" |
| 安全征信 | `user_question_types.safety` | "安全吗""征信""隐私""数据" |
| 额度多少 | `user_question_types.amount` | "能借多少""最高多少" |
| 用途方式 | `user_question_types.usage` | "能用来干嘛""提现到银行卡" |
| 时效相关 | `user_question_types.timing` | "多久到账""有效期""截止" |

### 3.3 流程阶段识别（v2.0 新增）

| 阶段 | 配置键 | 识别依据 |
|------|--------|----------|
| 阶段A（引导期） | `stage_keywords.stage_a` | "客户经理""搜索备用金""白条" |
| 阶段B（额度确认） | `stage_keywords.stage_b` | "查看额度""人脸识别""审核中" |
| 阶段C（借款意向） | `stage_keywords.stage_c` | "我要借款""灵活还""确认借款" |
| 阶段D（完成借款） | `stage_keywords.stage_d` | "到账""借款成功" |

**产出信号**：
- `stage_a_drop`：对话在阶段A就断了（开场拒绝）
- `mid_flow_drop`：对话在阶段B/C断了（中途放弃，高价值优化对象）

### 3.4 Agent 信号

| 特征 | 配置键 | 说明 |
|------|--------|------|
| 禁止表达 | `agent_forbidden` | "保证""一定""绝对"等 |
| 福利导向 | `agent_benefit` | "免息券""免费""备用金"等 |
| 二次确认 | `agent_confirm` | "您是愿意""我确认一下"等 |
| 状态锚定 | `agent_anchor` | "找到了吗""看到了吗"等 |
| 推进动作 | `agent_push` | "看一下""点进去""先打开"等 |

### 3.5 合规风险扩展（v2.0 新增）

| 风险类型 | 配置键 | 关键词示例 |
|----------|--------|------------|
| 虚假宣传 | `compliance_keywords.false_promotion` | "最高30万""全额提到银行卡" |
| 违规承诺 | `compliance_keywords.illegal_promise` | "大概率涨""快速提额""两周内提额" |
| 信息泄露 | `compliance_keywords.info_leak` | "您的额度是""你额度" |

### 3.6 流程打断与拉回（v2.0 新增）

| 检测项 | 配置键 | 说明 |
|--------|--------|------|
| 用户打断信号 | `interruption_signals.user_interruption_keywords` | "等一下""什么意思""不对吧" |
| 用户偏题信号 | `interruption_signals.user_topic_shift_keywords` | "征信""安全""手续费"等 |
| 机器人拉回信号 | `reconnection_signals.agent_reconnect_keywords` | "那咱们继续""那您现在""回到" |

**产出信号**：
- `failed_reconnect`：用户打断后机器人没拉回
- `no_reconnect_on_interruption`：多次打断均未拉回
- `successful_reconnect`：成功拉回（正向信号）

### 3.7 特殊场景

| 场景 | 配置键 | 关键词 |
|------|--------|--------|
| 领导/老板在场 | `special_scene_keywords.leader` | "领导""老板""在开会" |
| 开车 | `special_scene_keywords.driving` | "开车""在开车" |
| 学生 | `special_scene_keywords.student` | "学生""还在上学" |
| 老人 | `special_scene_keywords.elderly` | "老人""退休""年纪大" |

---

## 四、弱监督分桶机制

### 4.1 分桶定义

| 分桶 | 含义 | 判定条件 |
|------|------|----------|
| **good_seed** | 高置信正向样本 | good_score ≥ 8, bad_score ≤ 3, confidence ≥ 0.75 |
| **bad_seed** | 高置信失败样本 | bad_score ≥ 8, confidence ≥ 0.75 |
| **gray_high_risk** | 高风险边界 | bad_score ≥ 6 |
| **gray_potential_good** | 正向潜力 | good_score ≥ 5 |
| **gray** | 普通灰区 | 其余 |

### 4.2 评分计算

```python
good_score = Σ(positive_signal_weights)
bad_score = Σ(negative_signal_weights) + Σ(risk_signal_weights)
confidence = 1.0 - noise_penalties
```

权重配置在 `scenes/{scene}.yaml` 的 `weak_supervision.signal_weights`。

### 4.3 ASR 场景特殊处理

- **"中途挂断"只是过程信号**，不能直接等于 badcase
- **"利率高/额度低"是产品异议**，不等于对话失败
- **"别打了/骚扰"才是对话拒绝**，二者必须分离

---

## 五、自动进化机制（v2.0 新增）

### 5.1 设计思路

每次挖掘完成后，自动检测特征覆盖缺口并补齐，不需要人工提醒。

### 5.2 工作流程

```
挖掘完成（loan-match.json）
  ↓
auto_evolve_features.py 自动运行
  ↓
1. 找特征未覆盖的对话
   · 信号稀疏的对话（positive+negative+risk ≤ 1）
   · 灰区对话（confidence < 0.7）
   · 用户有实质内容但没触发任何用户侧特征的对话
  ↓
2. 从 turns 级别提取用户/机器人短句
   · 按标点断句，提取 2-12 字短句
   · 过滤 ASR 碎片、语气词、业务无关词
  ↓
3. 归类
   · 能归入现有类别的 → 自动补入 feature_rules
   · 无法归入的 → 建议新 feature_rules 类别
  ↓
4. 写回 scenes/{scene}.yaml
  ↓
5. 记录进化历史
   ~/pe-self-improving/memory/{scene}/warm/evidence/evolution-log-*.json
```

### 5.3 关键过滤

| 过滤层 | 说明 |
|--------|------|
| ASR 碎片过滤 | "用户未说话""户未"等非语义片段 |
| 语气词过滤 | "嗯嗯""嗯我"等纯语气词 |
| 业务词过滤 | "京东""金条""白条"等非区分性词 |
| 停用词过滤 | "的话""就是""然后"等常见连接词 |
| 子串去重 | 长短语已存在时，移除短子串 |

### 5.4 当前局限

1. **中文分词**：目前用整句匹配而非 jieba 分词，对长句覆盖有限
2. **新类别质量控制**：低频短语可能产生噪声类别，需加 min_freq 阈值
3. **Layer 2（LLM 模式发现）**：尚未实现，可用 LLM 对灰区做深度模式发现

---

## 六、共享资源机制

### 6.1 软链接共享

dialog-discovery 通过软链接复用 pe-self-improving 的场景配置：

```
dialog-discovery/scenes/ → ../pe-self-improving/scenes/
dialog-discovery/prompts/collection → ../pe-self-improving/prompts/collection
dialog-discovery/prompts/exhibition → ../pe-self-improving/prompts/exhibition
dialog-discovery/prompts/loan → ../pe-self-improving/prompts/loan
```

### 6.2 配置唯一来源原则

- 评分标准 → 只在 `scenes/{scene}.yaml` 的 `scoring` 字段
- 特征规则 → 只在 `scenes/{scene}.yaml` 的 `feature_rules` 字段
- 弱监督权重 → 只在 `scenes/{scene}.yaml` 的 `weak_supervision` 字段
- **禁止在脚本里维护第二份业务规则真相**

### 6.3 学习库不拆分

挖掘结果继续写入统一学习库（v2.1 对齐 warm 层规范结构）：

```
~/pe-self-improving/memory/{target_scene}/warm/
├── candidates/
│   ├── rules.md           # 候选正向规则 + 约束规则
│   └── utterances.md      # 候选话术
├── evidence/
│   ├── rules.md           # 规则证据（对话原文支撑）
│   └── utterances.md      # 话术证据
├── learnings/
│   ├── insights.md        # 成功/失败洞察
│   └── issues.md          # 问题模式
└── (以下为 pe-self-improving 产出)
    evolution-chain-*.md    # 进化思维链
    evolution-log-*.json    # 自动进化日志
    badcase-coverage-*.md   # 修复覆盖报告
```

---

## 七、标准执行链路

```bash
# 1. 标准化 + ASR 清洗（含交替启发式角色分离）
python3 scripts/normalize_dialogs.py \
  --input "对话数据.xlsx" \
  --scene "loan" \
  --output "loan-normalized.json"

# 2. 弱监督特征提取与 seed 分桶
python3 scripts/template_match_dialogs.py \
  --input "loan-normalized.json" \
  --scene "loan" \
  --output "loan-match.json"

# 3. 按 seed_label 分桶聚类
python3 scripts/cluster_dialogs.py \
  --scores "loan-match.json" \
  --scene "loan" \
  --output "loan-cluster.json"

# 4. LLM 深度提取（默认模式，自动写入 warm 层 6 个文件）
python3 scripts/extract_rules_from_cluster.py \
  --clusters "loan-cluster-clusters.json" \
  --scene "loan"

# 如只需信号频率统计（不写 warm 层）：
# python3 scripts/extract_rules_from_cluster.py \
#   --clusters "loan-cluster-clusters.json" \
#   --scene "loan" \
#   --mode stats \
#   --output "loan-rules-stats.md"

# 5. 深度分析（v2.1 新增，推荐手动执行）
# - 读 good_seed / bad_seed 原文，归纳实质规则和话术
# - 追加或修正 LLM 提取结果
# - 写入 warm 层 6 个规范文件

# 6. 生成人工 review 包
python3 scripts/sample_for_review.py \
  --input "loan-match.json" \
  --output-json "loan-review.json" \
  --output-md "loan-review.md" \
  --sample-size 30

# 7. 自动进化特征规则（必须执行）
python3 scripts/auto_evolve_features.py \
  --input "loan-match.json" \
  --scene "loan"
```

可选：统一评分输出

```bash
python3 scripts/batch_score_dialogs.py \
  --input "loan-match.json" \
  --scene "loan" \
  --output "loan-weak-label.json" \
  --mode weak_label
```

---

## 八、脚本清单

| 脚本 | 用途 | 长任务 |
|------|------|--------|
| `normalize_dialogs.py` | 标准化 + ASR 清洗 | 否 |
| `template_match_dialogs.py` | 弱监督特征提取 + 分桶 | 否 |
| `batch_score_dialogs.py` | 统一评分（rules/llm/hybrid/weak_label） | 是 |
| `llm_score_background.py` | 后台 LLM 评分 | 是 |
| `cluster_dialogs.py` | 分桶聚类分析 | 否 |
| `extract_rules_from_cluster.py` | LLM 深度提取候选规则/约束/假设（v2.1 重写） | 是（LLM调用） |
| `sample_for_review.py` | 生成人工 review 包 | 否 |
| `auto_evolve_features.py` | **自动进化特征规则（v2.0）** | 否 |
| `discover_dialogs.py` | 一键挖掘入口 | 是 |
| `identify_scene.py` | 场景识别 | 否 |
| `common.py` | 公共工具 | - |
| `llm_client.py` | LLM 客户端 | - |

---

## 九、v2.0 金条场景挖掘实例数据

### 分桶分布

| 分桶 | v1 | v2 | v3（合规否决） | 说明 |
|------|-----|-----|----------------|------|
| good_seed | 85 | 85 | **34** | 合规否决降级 51 条 |
| bad_seed | 710 | 710 | 710 | 不变 |
| gray_high_risk | 345 | 345 | **412** | 合规风险对话归入此桶 |
| gray | 117 | 117 | 141 | |
| gray_potential_good | 50 | 50 | 10 | |

### LLM 评分校准结果

弱监督分桶 vs LLM 评分一致性：

| 弱监督标签 | 数量 | LLM 确认率 | LLM 降级 | LLM 反转 |
|-----------|------|-----------|---------|----------|
| bad_seed | 50 | 74.0% ✅ | 24.0% | 2.0% |
| good_seed (v2) | 70 | 7.1% ❌ | 35.7% | 57.1% |
| good_seed (v3) | 32 | 9.4% | 28.1% | 62.5% |

**核心发现**：good_seed 假阳性严重，主因是弱监督没检测 agent 合规风险。v3 加入合规一票否决后，good_seed 从 85 降到 34，但 LLM 确认率仍低（弱监督合规关键词覆盖不足）。

### 新特征洞察（v2.0）

| 维度 | 发现 |
|------|------|
| 流程阶段 | 38.1% bad_seed 走到阶段 C 才放弃，优化阶段 C ROI 最高 |
| 打断拉回 | 拉回成功率仅 9.3%（159/1708），几乎所有打断都没正确拉回 |
| 用户提问 | TOP3：安全/征信(73) > 利率(69) > 还款方式(48) |
| 合规风险 | 虚假宣传 55.8% + 信息泄露 30.8% 是两大风险 |
| 自动进化 | 首次运行发现 8 个可补入关键词 + 44 个新类别建议 |

---

## 十、硬约束

1. **"中途挂断"不是单点结论**：只能作为过程信号，必须和其他信号组合判断
2. **产品异议 ≠ 对话失败**：利率高/额度低 ≠ 别打了/骚扰
3. **配置唯一来源**：所有规则只从 `scenes/{scene}.yaml` 读取
4. **合规一票否决**：agent 有合规风险（forbidden_hits / compliance_risk）→ 不得进入 good_seed，降级为 gray_high_risk
5. **自动进化必须执行**：每次挖掘后必须运行 `auto_evolve_features.py`
6. **学习库不拆分**：挖掘结果写入 `~/pe-self-improving/memory/{scene}/warm/`
7. **warm 层路径规范**（v2.1 新增）：只写 `candidates/`、`evidence/`、`learnings/` 三个子目录共 6 个文件，禁止在 warm 根目录创建文件

---

*Dialog Discovery Skill v2.1*
*创建时间：2026-04-08*
*更新时间：2026-04-21（v2.1 重写 extract_rules 引入 LLM 深度提取、对齐 warm 层路径规范、增强 ASR 交替启发式角色分离、新增深度分析步骤）*
