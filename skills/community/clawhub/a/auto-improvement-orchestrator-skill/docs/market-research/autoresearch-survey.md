# autoresearch 调研报告（2026-03-25）

> 作者：ainews  
> 时间：2026-03-25  
> 来源：Karpathy autoresearch / Jr. AI Scientist / AutoResearch-RL

---

## 核心发现

### Karpathy Loop（最成功实践）

**项目**: https://github.com/karpathy/autoresearch

**核心设计**:
```
Agent 修改 train.py → 训练 5 分钟 → 评估 val-bpb → 保留/回滚 → 重复
```

**三关注点分离**:
1. **一个可修改的文件**（如 `train.py`）
2. **一个客观可测试的指标**（如 validation loss）
3. **固定的时间限制**（如 5 分钟/实验）

**实际成果**:
- 700 次自主实验
- 2 天时间
- 11% 性能提升（2.02h → 1.80h）

---

### AutoResearch-RL（强化学习版本）

**论文**: https://arxiv.org/pdf/2603.07300

**核心设计**:
```python
class AutoResearchRL:
    def __init__(self):
        self.agent = PPOPolicy()  # RL Agent
        self.environment = TrainingEnv()  # 训练环境
        self.evaluator = SelfEvaluator()  # 自评估器
    
    def loop(self):
        while True:
            # 1. Agent 提出代码编辑
            code_edit = self.agent.propose_edit()
            
            # 2. 执行训练（5 分钟预算）
            checkpoint, bpb_curve = self.environment.train(code_edit, time_budget=300)
            
            # 3. 自评估器决定是否早期停止
            if self.evaluator.should_abort(bpb_curve):
                break
            
            # 4. 计算奖励并更新策略
            reward = -bpb_curve[-1]  # 最小化 val-bpb
            self.agent.update(reward)
```

**关键创新**:
- 将代码编辑视为 RL action
- val-bpb 作为 reward
- 自评估器实现早期停止

---

### Jr. AI Scientist（多 Agent 版本）

**项目**: https://github.com/Sibyl-Research-Team/AutoResearch-SibylSystem

**核心设计**:
```
多 Agent 系统:
- Planner Agent: 设计实验
- Coder Agent: 实现代码
- Trainer Agent: 执行训练
- Evaluator Agent: 评估结果
- Manager Agent: 协调流程
```

**特点**:
- 显式的多 Agent 协作
- GPU 实验执行
- 自进化外层循环

---

## 对 skill-evaluator 的借鉴

### 1. 自主改进循环（P1）

```python
# scripts/self_improve.py
def self_improve_loop(skill_path, metric="accuracy", max_iterations=100):
    """
    自主改进循环 - 借鉴 Karpathy Loop
    
    流程:
    1. 修改 Skill 代码（小改动）
    2. 运行评估
    3. 保留或回滚
    4. 重复直到收敛或达到最大迭代次数
    """
    best_score = 0
    no_improvement_count = 0
    
    for i in range(max_iterations):
        # 1. 提出代码修改（小改动，避免破坏性变更）
        change = propose_small_change(skill_path)
        
        # 2. 运行评估
        score = evaluate_skill(skill_path, metric)
        
        # 3. 保留或回滚
        if score > best_score:
            best_score = score
            commit_change(skill_path, change)
            logger.info(f"迭代{i}: 改进到 {score:.2%}")
            no_improvement_count = 0
        else:
            revert_change(skill_path, change)
            logger.info(f"迭代{i}: 无改进 ({score:.2%})")
            no_improvement_count += 1
        
        # 4. 早期停止（10 次无改进）
        if no_improvement_count >= 10:
            logger.info("10 次无改进，早期停止")
            break
    
    return best_score
```

---

### 2. 能力演进追踪（P1）

```python
# scripts/track_progress.py
def track_skill_progress(skill_path):
    """追踪 Skill 能力演进"""
    history = load_eval_history(skill_path)
    
    # 绘制能力演进曲线
    plot_metric(history, "accuracy", "准确性")
    plot_metric(history, "reliability", "可靠性")
    plot_metric(history, "efficiency", "效率")
    
    # 识别改进趋势
    trend = calculate_trend(history)
    if trend == "improving":
        print("✅ Skill 正在改进")
    elif trend == "stable":
        print("⚠️ Skill 改进停滞")
    else:
        print("❌ Skill 性能下降")
    
    # 生成改进建议
    suggestions = generate_suggestions(history, trend)
    print("\n改进建议:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
```

---

### 3. 标量奖励设计

借鉴 AutoResearch-RL 的 val-bpb 设计，我们为 skill-evaluator 设计标量奖励：

```python
# scripts/reward.py
def calculate_skill_reward(eval_result):
    """
    计算 Skill 改进的标量奖励
    
    公式:
    reward = 0.4 * accuracy + 0.25 * reliability + 0.2 * efficiency 
           + 0.1 * (1 - cost) + 0.05 * coverage
    """
    accuracy = eval_result.get("accuracy", 0)
    reliability = eval_result.get("reliability", 0)
    efficiency = eval_result.get("efficiency", 0)
    cost = eval_result.get("cost", 1)  # 归一化到 0-1
    coverage = eval_result.get("coverage", 0)
    
    reward = (
        0.40 * accuracy +
        0.25 * reliability +
        0.20 * efficiency +
        0.10 * (1 - cost) +
        0.05 * coverage
    )
    
    return reward
```

---

## 下一步行动

### P0（已完成）
- [x] 按类别调整权重配置
- [x] 红队测试脚本
- [x] Promptfoo 集成

### P1（本周开始）
- [ ] 自主改进循环（Karpathy Loop）
- [ ] 能力演进追踪
- [ ] 标量奖励设计

### P2（下月）
- [ ] 基准数据库
- [ ] 多 Agent 并行评估
- [ ] Skill 排行榜

---

*最后更新：2026-03-25*
