# PE Self-Improving Architecture v3（证据驱动版）

本文档在 v2 基础上，进一步解决以下问题：

1. 学习库沉淀方式偏日志化，缺少资产视角
2. 规则 / 话术的晋升标准不够硬
3. 缺少证据累计机制，无法稳定支持 HOT 晋升
4. 缺少降级 / 废弃机制，HOT 容易持续膨胀
5. 缺少运行时读取规范，学习库容易越读越脏

v3 的核心思想只有一句话：

> **把学习库从“日志库”升级为“证据驱动的知识资产库”。**

---

## 一、v3 的核心对象

### 1. Run
表示一轮完整的优化事件。

负责回答：
- 这一轮做了什么
- 当前状态是什么
- 有哪些文件产物
- 最终是否采纳 / 回滚

载体：`specs/run-manifest.md`

### 2. Issue
表示问题模式。

负责回答：
- 本轮到底出现了什么问题
- 是否是已知问题
- 对哪个维度造成影响

建议未来逐步归一化，而不是只保留自然语言描述。

### 3. Asset
表示知识资产，分为两类：
- Rule
- Utterance

负责回答：
- 哪条规则/话术值得长期保留
- 当前处于 candidate / warm / hot / cold / deprecated 哪个状态

### 4. Evidence
表示资产的累计证据。

负责回答：
- 某条规则验证过几次
- 有没有副作用
- 是否达到 HOT 晋升门槛

---

## 二、v3 的标准流水线

```text
输入识别
→ 场景装载
→ 问题提取与归一化
→ 候选资产生成（rule / utterance）
→ preflight 静态门禁
→ 提交候选PE
→ 验证 run
→ PE采纳决策
→ evidence 更新
→ promotion review
→ 写入学习库
→ 运行时装配
```

---

## 三、两套决策系统必须分离

### 3.1 PE采纳决策
回答：
- 这个候选 PE 版本要不要上

依据：
- `specs/acceptance-gates.md`

### 3.2 知识晋升决策
回答：
- 这条规则/话术要不要进 HOT

依据：
- `specs/promotion-gates.md`
- `specs/evidence-model.md`

### 为什么必须分离

因为：
- 有些 PE 不值得采纳，但其中某条洞察值得保留为 WARM
- 有些 PE 被采纳，但其中部分话术并不值得晋升 HOT

所以：
- **版本决策 ≠ 资产决策**

---

## 四、学习库目录建议（v3）

```text
~/pe-self-improving/memory/
├── collection/
│   ├── hot/
│   │   ├── rules.md
│   │   ├── utterances.md
│   │   └── index.md
│   ├── warm/
│   │   ├── candidates/
│   │   │   ├── rules.md
│   │   │   └── utterances.md
│   │   ├── evidence/
│   │   │   ├── rules.md
│   │   │   └── utterances.md
│   │   └── learnings/
│   │       ├── insights.md
│   │       └── issues.md
│   └── cold/
│
├── exhibition/
│   ├── hot/
│   ├── warm/
│   └── cold/
│
└── shared/
```

### 说明

- `hot/`：运行时优先装配资产
- `warm/candidates/`：待验证候选资产
- `warm/evidence/`：资产累计证据
- `warm/learnings/`：成功/失败/洞察日志
- `cold/`：归档，不参与运行时装配
- `shared/`：仅 API / 工程经验，不放业务策略

---

## 五、运行时读取规范

v3 不推荐再用“把整个学习库读一遍”的方式拼 PE。

### 运行时推荐装配顺序

1. 场景精确匹配的 `hot/rules.md`
2. 子场景精确匹配的 `hot/utterances.md`
3. 与当前 issue 高匹配的 `warm/candidates/`
4. 本轮新增 insight
5. `shared/` 中与工程相关的通用经验

### 明确禁止

以下内容默认不参与运行时 prompt 装配：
- `cold/`
- `deprecated`
- 不相关场景的 hot/warm
- 全量历史 failure 长文
- 未归一化的原始 issue 长文

---

## 六、资产生命周期

### 状态流转

```text
candidate -> warm -> hot
warm -> cold
hot -> warm
hot/warm -> deprecated
```

### 各状态意义

- `candidate`：本轮新增，等待证据
- `warm`：初步有效，但证据不足
- `hot`：稳定有效，优先装配
- `cold`：历史保留，不用于装配
- `deprecated`：明确废弃

---

## 七、脚本职责建议（v3）

### 已有脚本继续保留
- `start_sparring.py`
- `get_sparring_result.py`
- `submit_pe.py`
- `verify_run.py`
- `write_learning.py`

### 新增脚本建议

#### 1. `update_evidence.py`
职责：
- 读取 run manifest + verify result
- 为本轮涉及的 rule / utterance 更新累计 evidence

#### 2. `review_promotions.py`
职责：
- 读取 warm candidates + evidence
- 判断是否满足 HOT 晋升门禁
- 输出晋升/保留/降级建议

#### 3. `review_demotions.py`
职责：
- 读取 hot assets 的近期证据
- 判断是否需要降级 / 废弃

---

## 八、v3 的最小落地路线

为了避免一次性重构过重，建议按以下顺序实施：

### Phase A：先补规范
1. `specs/promotion-gates.md`
2. `specs/evidence-model.md`
3. `docs/ARCHITECTURE_V3.md`

### Phase B：再补最小脚本骨架
1. `scripts/update_evidence.py`
2. `scripts/review_promotions.py`

### Phase C：再补学习库细分目录
1. `warm/candidates/rules.md`
2. `warm/candidates/utterances.md`
3. `warm/evidence/rules.md`
4. `warm/evidence/utterances.md`

### Phase D：最后再做自动晋升/降级
1. verify 后自动更新 evidence
2. 再自动跑 promotion review
3. 输出晋升建议，不强制自动写 HOT

---

## 九、v3 的成败标准

如果 v3 落地成功，这套系统应能稳定回答以下问题：

1. 这条规则为什么在 HOT？
2. 它被验证过几次？
3. 它修复了什么问题？
4. 它有没有副作用？
5. 如果它最近失效了，谁负责把它降级？
6. 运行时到底应该读哪部分学习库？

如果这些问题答不清，说明学习库仍然偏“经验日志”，还不是“高可用资产库”。
