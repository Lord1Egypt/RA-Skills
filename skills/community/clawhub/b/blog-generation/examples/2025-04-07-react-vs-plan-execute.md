# ReAct vs Plan-and-Execute：我试了两种Agent架构后，发现选择比努力更重要

说实话，我刚做 Agent 的时候，根本不知道还有这么多架构流派。拿着 LangChain 的 ReAct 模板就往上怼，结果在生产环境栽了个大跟头——一个复杂的任务，Agent 在那儿反复思考、调用工具、再思考、再调用，循环了 20 多次还没搞定。用户直接放弃了。

后来我才明白：**Agent 架构选错了，后面的优化都是徒劳。**

这篇文章聊聊我踩过的坑，以及 ReAct 和 Plan-and-Execute 到底该怎么选。

---

## 什么是 ReAct？

ReAct（Reasoning + Acting）大概是现在最流行的 Agent 架构了。它的核心思想很简单：

**思考 → 行动 → 观察 → 再思考 → 再行动...**

就像一个边想边做的人，每做一步都要停下来看看结果，然后决定下一步怎么做。

**典型的工作流程：**

```
用户：查询北京今天的天气，然后发邮件给张三

Agent:
1. 思考：用户要我查天气，我需要调用天气查询工具
2. 行动：调用 get_weather(city="北京")
3. 观察：天气 API 返回"晴，25度"
4. 思考：现在知道天气了，接下来要发邮件。我需要张三的邮箱地址
5. 行动：调用 get_contact(name="张三")
6. 观察：返回邮箱 zhangsan@example.com
7. 思考：现在可以发邮件了
8. 行动：调用 send_email(to="zhangsan@example.com", content="北京今天晴，25度")
9. 观察：邮件发送成功
10. 思考：任务完成
```

**代码示例（简化版）：**

```python
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
    
    def run(self, query, max_iterations=10):
        context = f"用户请求：{query}\n\n"
        
        for i in range(max_iterations):
            # 1. 思考
            thought = self.llm.predict(
                f"{context}\n基于以上信息，你需要：\n1. 分析当前状态\n2. 决定下一步行动\n\n思考："
            )
            context += f"思考：{thought}\n"
            
            # 2. 决定行动
            action_json = self.llm.predict(
                f"{context}\n根据你的思考，选择一个工具行动（JSON格式）："
            )
            action = parse_json(action_json)
            
            if action["tool"] == "finish":
                return action["answer"]
            
            # 3. 执行行动
            tool_result = self.tools[action["tool"]].run(**action["params"])
            context += f"行动：使用 {action['tool']}\n观察：{tool_result}\n\n"
        
        return "达到最大迭代次数，任务未完成"
```

**ReAct 的优点：**
- 灵活性强，适合处理不确定性高的任务
- 每一步都可以根据最新观察调整策略
- 思路清晰，容易调试

**但缺点也很明显：**
- **Token 消耗大**：每步都要 LLM 参与
- **延迟高**：串行执行，工具调用次数多
- **容易陷入循环**：遇到边界情况会一直反复尝试
- **不适合复杂任务**：步骤一多，上下文就爆炸

---

## 什么是 Plan-and-Execute？

Plan-and-Execute（计划与执行）走的是另一条路：**先想好了再做**。

它把任务分成两个阶段：
1. **Planning（计划阶段）**：LLM 一次性生成完整的执行计划
2. **Execution（执行阶段）**：按照计划逐步执行，必要时可以重新规划

**典型的工作流程：**

```
用户：查询北京今天的天气，然后发邮件给张三

阶段1 - 制定计划：
Agent 思考后生成计划：
[
  {"step": 1, "action": "查询北京天气", "tool": "get_weather", "params": {"city": "北京"}},
  {"step": 2, "action": "获取张三邮箱", "tool": "get_contact", "params": {"name": "张三"}},
  {"step": 3, "action": "发送邮件", "tool": "send_email", "depends_on": [1, 2]}
]

阶段2 - 执行计划：
- 并行执行 step 1 和 step 2（因为无依赖）
- 获取结果后执行 step 3
- 完成
```

**代码示例（简化版）：**

```python
class PlanAndExecuteAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
    
    def create_plan(self, query):
        """第一步：制定计划"""
        prompt = f"""
        用户请求：{query}
        
        可用工具：{list(self.tools.keys())}
        
        请制定一个详细的执行计划，以 JSON 数组格式返回：
        [
          {{"step": 1, "action": "描述", "tool": "工具名", "params": {{}}, "depends_on": []}},
          ...
        ]
        """
        plan_json = self.llm.predict(prompt)
        return parse_json(plan_json)
    
    def execute_plan(self, plan):
        """第二步：执行计划"""
        results = {}
        
        for step in sorted(plan, key=lambda x: x["step"]):
            # 等待依赖完成
            for dep in step.get("depends_on", []):
                if dep not in results:
                    raise Exception(f"步骤 {step['step']} 依赖的步骤 {dep} 尚未完成")
            
            # 执行当前步骤
            tool = self.tools[step["tool"]]
            
            # 替换参数中的变量引用
            params = resolve_params(step["params"], results)
            
            result = tool.run(**params)
            results[step["step"]] = result
            
            # 如果执行失败，可以重新规划
            if is_failure(result):
                return self.replan(plan, step, result)
        
        return results
    
    def run(self, query):
        plan = self.create_plan(query)
        print(f"生成的计划：{json.dumps(plan, ensure_ascii=False, indent=2)}")
        return self.execute_plan(plan)
```

**Plan-and-Execute 的优点：**
- **效率高**：可以并行执行独立步骤
- **Token 消耗低**：计划阶段只用一次 LLM
- **结构清晰**：任务分解明确，便于监控
- **适合复杂任务**：多步骤任务也能很好处理

**缺点：**
- **不够灵活**：计划一旦制定，中途调整成本高
- **需要重规划机制**：遇到意外情况要能重新生成计划
- **对 LLM 规划能力要求高**：计划不合理会导致执行失败

---

## 两种架构的详细对比

| 维度 | ReAct | Plan-and-Execute |
|------|-------|------------------|
| **执行方式** | 串行，一步一思考 | 先计划，后执行（可并行） |
| **灵活性** | 高，随时调整策略 | 中，需要重规划机制 |
| **Token 消耗** | 高（每步都调用 LLM） | 低（计划阶段只用一次） |
| **延迟** | 高（串行+多次 LLM 调用） | 低（可并行执行） |
| **适用任务** | 简单、不确定性高 | 复杂、步骤明确 |
| **调试难度** | 低（步骤清晰） | 中（需要追踪计划执行） |
| **容错性** | 高（随时可调整） | 中（需要重规划） |

---

## 我是怎么选择的？

经过几个项目的折腾，我总结了一个简单的决策树：

```
任务分析：
│
├─► 步骤是否明确可预测？
│   ├─ 是 → Plan-and-Execute
│   └─ 否 → ReAct
│
├─► 是否需要频繁根据反馈调整？
│   ├─ 是 → ReAct
│   └─ 否 → Plan-and-Execute
│
├─► 步骤数量？
│   ├─ ≤ 3步 → ReAct（简单直接）
│   └─ > 3步 → Plan-and-Execute（避免上下文爆炸）
│
└─► 是否需要并行执行？
    ├─ 是 → Plan-and-Execute
    └─ 否 → 都可以
```

**我的实战经验：**

| 场景 | 推荐架构 | 原因 |
|------|----------|------|
| 客服问答 | ReAct | 用户问题不确定，需要灵活应对 |
| 数据分析报告生成 | Plan-and-Execute | 步骤明确：获取数据→清洗→分析→可视化→生成报告 |
| 代码审查 | ReAct | 需要逐行分析，不确定哪里有问题 |
| 自动化工作流 | Plan-and-Execute | 步骤固定，追求效率 |
| 研究助手 | 混合 | 先 Plan 粗粒度步骤，每个步骤内部用 ReAct |

---

## 混合架构：取长补短

其实现在越来越多的框架采用**混合策略**：

```python
class HybridAgent:
    """混合架构：顶层 Plan-and-Execute，底层 ReAct"""
    
    def run(self, query):
        # 1. 先做高层规划
        high_level_plan = self.create_high_level_plan(query)
        
        results = []
        for step in high_level_plan:
            # 2. 每个复杂步骤内部用 ReAct 执行
            if step["complexity"] == "high":
                result = self.react_agent.run(step["task"])
            else:
                # 简单步骤直接执行
                result = self.execute_simple(step)
            
            results.append(result)
            
            # 3. 检查是否需要重规划
            if should_replan(results):
                high_level_plan = self.replan(query, results)
        
        return self.synthesize_results(results)
```

这样既保证了整体效率，又保留了应对不确定性的能力。

---

## 踩坑记录

**坑 1：ReAct 的无限循环**

有一次做网页爬虫 Agent，遇到反爬机制返回了验证码页面。Agent 一直在"观察页面→尝试点击→失败→再观察"的循环里出不来。

**解决方案：**
- 设置最大迭代次数
- 加入异常检测机制
- 连续失败 3 次就触发人工介入或重规划

**坑 2：Plan-and-Execute 的计划过于乐观**

LLM 制定的计划经常假设一切顺利，但现实中工具调用会失败、API 会超时、数据会缺失。

**解决方案：**
- 每个步骤都要有错误处理
- 计划里预留备选方案
- 执行失败时触发局部重试或全局重规划

**坑 3：两种架构的上下文管理**

ReAct 的上下文会线性增长，Plan-and-Execute 在执行阶段如果不注意，也会累积大量中间结果。

**解决方案：**
- ReAct：定期总结历史，保留关键信息
- Plan-and-Execute：每个步骤只传递必要的结果，不要传递整个执行历史

---

## 写在最后

选架构不是选边站，而是**根据任务特点做权衡**。

我的建议是：

1. **从 ReAct 开始**：实现简单，容易调试，适合快速验证想法
2. **遇到性能瓶颈时**：如果 Token 消耗太大或响应太慢，考虑 Plan-and-Execute
3. **复杂任务用混合**：别纠结非此即彼，取长补短才是王道
4. **监控和优化**：不管选哪种，都要加日志、加监控，数据说话

最后说句掏心窝的话：架构只是工具，**理解你的任务和用户才是核心**。别为了追求"先进"的架构，把简单问题复杂化了。

你目前在用哪种架构？遇到了什么问题？欢迎在评论区聊聊。

---

*这篇文章整理自我在实际项目中的架构选型经验。技术变化快，但选择的原则相对恒定。希望能帮你少走点弯路。*
