# 高层模式抽象与路由策略

## 六种核心模式

| 模式 | 触发信号 | 核心目标 | 典型场景 |
|------|---------|---------|---------|
| **Comfort（犒劳模式）** | 独食、加班后、情绪低落、"就想吃好的" | 高多巴胺回报、熟悉感、满足感 | 独食犒劳、压力进食 |
| **Efficiency（效率模式）** | 时间紧、快手、外卖、"随便吃点"、单人 | 极速、低决策成本、可执行性强 | 工作日午餐、加班晚餐 |
| **Social（社交模式）** | 聚餐、请客、聚会、家庭、商务、同学 | 分食性、共识度、体面感 | 商务宴请、家庭聚会 |
| **Performance（炫技模式）** | 露一手、展示厨艺、品质优先、"好好做一顿" | 视觉冲击、复杂度、成就感 | 厨艺展示、周末大餐 |
| **Health（健康模式）** | 减脂、增肌、轻食、痛风/高血压/糖尿病 | 目标达成率、营养素精确度 | 健身餐、病号餐 |
| **Adventure（探索模式）** | 想吃某菜系、露营、火锅、全素、"换换口味" | 新颖性、主题一致性 | 地域探索、特殊饮食 |

---

## 模式判定规则

1. 从用户输入中提取关键字，匹配模式触发信号。
2. 若匹配多个模式，按以下优先序裁决：**Health > Comfort > Performance > Social > Efficiency > Adventure**。
3. 若无法判定，默认 Efficiency（快速通道）或 Social（慢速通道）。
4. 模式一旦确定，所有下层规则（肉源选择、工艺分配、菜品池、专家评审角度）围绕该模式的目标展开。
5. **模式不是锁死的**：若用户在交互中补充信息导致模式切换（如从 Efficiency 变为 Comfort），重新编译。

---

## 模式判定与约束裁决序的关系

> **区分两个层次：模式选配置，裁决序解冲突。**

- **模式判定**解决的是"用哪套默认配置"（即：哪些约束默认激活、哪些文件加载、方案倾向什么风格）。
- **约束裁决序**（见 SKILL.md §决策优先级裁决序）解决的是"当激活的约束之间冲突时谁赢"。
- 两者**串行而非平行**：先判定模式 → 激活对应的默认约束集 → 再用裁决序仲裁约束间的冲突。

具体关系：
- Health 模式优先于 Social 模式 → Health 模式下优先激活健康约束、加载 expert-cabinet
- 但 Priority 2（用户显式指令）仍可覆盖 Health 模式的某些默认（如用户明确说"今天就想放纵一次，不减脂了"）
- Priority 1（忌口、临床红线）不可被任何模式或用户指令覆盖
- Comfort 模式下心理咨询角度优先，但 Priority 1 的临床警告仍然悬挂

---

## 模式感知条件加载

> **核心原则**：不加载与当前模式无关的文件或章节。context window 是公共资源，每一段不相关的规则都在稀释模型对真正重要约束的注意力。

| 模式 | 必加载 | 按需加载（仅当用户信号触发时） | 不加载 |
|------|--------|-------------------------------|--------|
| **Comfort** | algorithm-engine（§1-3, §5-7）+ output-schema + heuristics | cuisine-profiles（若用户有菜系偏好） | expert-cabinet（犒劳不需要专家说教） |
| **Efficiency** | algorithm-engine（§1-4, §6-7）+ output-schema + heuristics | — | cuisine-profiles, expert-cabinet |
| **Social** | **全部参考文件** | — | — |
| **Performance** | algorithm-engine（全部）+ output-schema + cuisine-profiles + heuristics | expert-cabinet（按需）、memory-system | — |
| **Health** | algorithm-engine（§1-3, §5-6）+ expert-cabinet + output-schema + heuristics | cuisine-profiles（按需） | algorithm-engine §7 特殊场景模板（除减脂外） |
| **Adventure** | algorithm-engine（§7 特殊场景按子类型）+ output-schema + cuisine-profiles | heuristics（按需）、memory-system | expert-cabinet（探索不需要专家审判） |

**按需加载的触发信号**：
- cuisine-profiles：用户提"我是X人" / "想吃X菜" / "X菜好吃" / 档案中地域权重绝对值 >= 2
- expert-cabinet：慢速通道 + 用户未催"快点" + 用户未表示"太长了"
- memory-system 全文：冷启动阶段 / 用户主动打标时。日常无需加载
- dishes-reference：选菜不确定时 / Health 模式 / Adventure（全素）模式 / 大席面 N > 6 时 / 菜名记忆模糊时
- algorithm-engine §2 厨房资源模型：仅交付形式为"下厨"时
- algorithm-engine §4 外卖耐受度：仅交付形式为"外卖"时
- algorithm-engine §7 露营/火锅/全素模板：仅命中对应特殊意图时
