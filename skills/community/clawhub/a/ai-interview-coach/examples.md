# AI Interview Coach - Examples

This document provides concrete examples of using the AI Interview Coach skill with different difficulty levels and question counts.

---

## Difficulty Levels Explained

### Junior (初级)
- **Target**: New graduates, 0-2 years experience
- **Question Depth**: "What is it" and "How to use it"
- **Example**: "Explain what React useState does"

### Mid (中级)
- **Target**: 3-5 years experience
- **Question Depth**: "Why" and "How it works"
- **Example**: "Explain useEffect's dependency array and closure traps"

### Senior (高级)
- **Target**: 5+ years, experts, architects
- **Question Depth**: "Source code implementation" and "Design principles"
- **Example**: "Explain React Fiber's implementation and scheduling strategy"

---

## Question Count Options

| Mode | Count | Duration | Use Case |
|------|-------|----------|----------|
| Quick | 5 | 15 min | Quick self-test |
| Standard | 10 | 30 min | Regular practice |
| Deep | 15 | 45 min | Systematic review |
| Comprehensive | 20 | 60 min | Mock interview |

---

## Example 1: Resume-Based with Auto Detection (Frontend Developer, 3 years)

**User Input:**
> "请帮我准备前端工程师的面试，这是我的简历：frontend-developer-resume.pdf"

**Process:**
1. Read PDF file `frontend-developer-resume.pdf`
2. Extract content:
   - 3 years React/Vue experience → **Difficulty: Mid**
   - No question count specified → **Default: 10 questions**
   - Built e-commerce platform
   - Proficient in TypeScript, Webpack, CSS
   - Led team of 4 developers

**Generated Config:**
- **Difficulty**: 中级 (Mid)
- **Question Count**: 10题
- **Suggested Duration**: 30 minutes

**Sample Generated Questions:**

```markdown
# 面试练习题 - 前端工程师 (中级 · 10题)

### 第1题 (Technical - React)
请解释 React 的 Virtual DOM 工作原理，以及它与真实 DOM 的区别是什么？
在什么情况下 Virtual DOM 的优势最明显？

### 第5题 (Project Experience)
你在简历中提到主导开发了一个电商平台的前端架构。
请详细描述这个平台的架构设计，包括技术选型、性能优化方案，
以及你是如何解决高并发场景下的渲染性能问题的？

### 第8题 (Behavioral)
作为4人开发团队的负责人，你如何处理团队成员之间的技术分歧？
请举一个具体的例子说明。
```

---

## Example 2: Junior Level for New Graduate (Java Backend)

**User Input:**
> "你好考官，我是应届生，准备Java后端面试，来5道基础题"

**Detected Config:**
- **Difficulty**: 初级 (Junior) - "应届生" detected
- **Question Count**: 5题 - "5道" specified
- **Duration**: 15 minutes

**Sample Generated Questions:**

```markdown
# 面试练习题 - Java后端 (初级 · 5题)

### 第1题 (Technical - Java基础)
请简述 Java 中接口和抽象类有什么区别？什么情况下用接口，什么情况下用抽象类？

### 第2题 (Technical - 集合框架)
ArrayList 和 LinkedList 有什么区别？分别在什么场景下使用？

### 第3题 (Technical - 数据库)
什么是 SQL 的索引？索引有什么作用，它的优缺点分别是什么？

### 第4题 (Behavioral)
作为应届生，你认为自己最大的优势和不足是什么？

### 第5题 (Learning)
你平时通过什么方式学习新技术？请分享一个最近学习的知识点。
```

**Reference Answers (Junior Level):**

```markdown
### 第1题答案

**难度**: 初级

**考察点**: Java基础语法、面向对象设计

**参考答案**:
1. **接口**：只能包含抽象方法（Java 8+可以有default方法），多实现
2. **抽象类**：可以包含具体方法，单继承
3. **使用场景**：
   - 接口：定义行为规范，如 `Comparable`, `Runnable`
   - 抽象类：代码复用，有共同基类，如 `InputStream`

**答题建议**:
- 清晰地对比两者的语法区别
- 举出具体例子更有说服力
- 不需要深入源码，理解使用场景即可
```

---

## Example 3: Senior Level Deep Dive (System Design)

**User Input:**
> "我是资深后端架构师，来20道高级难度的系统设计题，要全面一点"

**Detected Config:**
- **Difficulty**: 高级 (Senior) - "资深架构师" detected
- **Question Count**: 20题 - "20道" specified
- **Duration**: 60 minutes

**Sample Generated Questions:**

```markdown
# 面试练习题 - 后端架构师 (高级 · 20题)

### 第1题 (System Design)
设计一个支持日活1亿用户的短视频推荐系统架构。
要求：
- 系统能够承受每秒10万次的推荐请求
- 用户画像实时更新延迟 < 5分钟
- 支持A/B测试和算法快速迭代
- 说明数据流、存储选型、缓存策略、降级方案

### 第2题 (Technical Deep Dive)
深入分析 Kafka 的零拷贝(zero-copy)实现原理。
要求：
- 解释传统IO和零拷贝的区别
- 分析 sendfile 系统调用在 Kafka 中的应用
- 讨论零拷贝对吞吐量的提升量化分析

### 第3题 (Source Code Analysis)
阅读 Redis 的 SDS (Simple Dynamic String) 源码实现，分析：
- SDS 相比 C 字符串的优势
- 内存分配策略和预分配机制
- 为什么 Redis 要自己实现字符串而不是用标准库

### 第4题 (Troubleshooting)
线上系统出现内存泄漏，导致服务每隔2小时OOM重启。
作为架构师，你如何排查和解决这个问题？
要求列出完整的排查步骤、工具使用、根因分析方法。
```

**Reference Answers (Senior Level):**

```markdown
### 第1题答案

**难度**: 高级

**题型**: 系统设计

**考察点**: 高并发架构、分布式系统、推荐系统设计、可扩展性

**参考答案**:

1. **整体架构**
   - API Gateway → 负载均衡 → 推荐服务集群
   - 分层缓存：Nginx Cache → Local Cache → Redis Cluster
   - 异步处理：消息队列解耦用户行为收集

2. **数据流设计**
   - 用户行为 → Kafka → Flink实时计算 → 用户画像存储(HBase)
   - 内容特征 → 离线计算(Spark) → 向量数据库(Milvus)
   - 推荐请求 → 召回层 → 粗排 → 精排 → 重排 → 返回

3. **存储选型**
   - 用户画像：HBase (宽表设计，支持快速读写)
   - 内容特征：MongoDB (灵活Schema)
   - 向量检索：Milvus (ANN近似最近邻)
   - 实时计数：Redis Cluster (分片存储)

4. **高可用策略**
   - 多级降级：精排服务降级 → 粗排服务降级 → 热门缓存兜底
   - 熔断限流：Sentinel实现服务保护
   - 异地多活：单元化部署，就近访问

5. **A/B测试架构**
   - 流量分配服务：基于用户ID的Hash分桶
   - 实验配置中心：实时推送配置变更
   - 指标收集：埋点上报 → 实时数仓 → 实验报告生成

**答题建议**:
- 从整体到细节，先给架构大图再深入关键模块
- 量化指标要合理（QPS、延迟、存储容量）
- 必须讨论容错和降级，这是高级工程师的必备思维
- 能提到具体的开源组件和技术选型理由
- 如果时间允许，可以画架构图辅助说明
```

---

## Example 4: Quick Practice Mode (5 Questions)

**User Input:**
> "简单练几道热热身，快速过一下"

**Detected Config:**
- **Difficulty**: 默认中级 (Mid)
- **Question Count**: 5题 - "简单练几道" detected
- **Duration**: 15 minutes

**Sample Generated Output:**

```markdown
# 面试练习题 - 技术岗位 (中级 · 5题)

> Generated on: 2026-04-18
> Difficulty: 中级
> Questions: 5题
> 建议用时: 15分钟

---

## 面试题目

### 第1题 (技术知识)
什么是浏览器的事件循环(Event Loop)？微任务和宏任务的区别是什么？

### 第2题 (技术知识)
React 的 setState 是同步的还是异步的？什么情况下是同步的？

### 第3题 (项目经验)
请描述一次你解决过的性能优化问题，使用了什么方法，效果如何？

### 第4题 (问题解决)
如果页面首次加载很慢，你会从哪些方面进行优化？

### 第5题 (行为面试)
描述一次你和产品经理意见不一致的经历，你是如何处理的？
```

---

## Example 2: Job Position-Based Interview (Product Manager)

**User Input:**
> "我想面试产品经理职位，请帮我生成一些练习题"

**Process:**
1. No resume file provided
2. Use job role "产品经理" as input
3. Generate generic PM interview questions

**Sample Generated Questions:**

```markdown
### 第2题 (Product Thinking)
假设你负责一个在线教育平台的产品，用户流失率在第三个月显著上升。
请描述你会如何分析这个问题，并提出至少3个可能的解决方案。

### 第6题 (Behavioral)
请描述一次你与研发团队在技术实现方案上产生分歧的经历。
你是如何处理的？最终结果如何？

### 第10题 (Scenario)
公司计划推出一个全新的社交功能，但市场调研显示竞品类似功能的用户接受度不高。
作为产品经理，你会如何决定是否推进这个项目？请列出你的分析框架。
```

---

## Example 3: Markdown Resume

**User Input:**
> "基于我的简历生成面试题：resume.md"

**Resume Content (resume.md):**
```markdown
# 王小明

## 工作经历
- 字节跳动 | 后端工程师 | 2021-至今
  - 负责抖音推荐系统的微服务架构设计
  - 优化Redis集群，QPS提升300%
  
## 技能
- Go, Python, Java
- Kubernetes, Docker
- Redis, MySQL, Kafka
```

**Sample Generated Questions:**

```markdown
### 第3题 (Technical - System Design)
你在抖音负责推荐系统的微服务架构。
请设计一个能够支撑每秒10万请求的推荐服务架构，
包括服务拆分策略、缓存策略和降级方案。

### 第4题 (Technical - Performance)
你提到优化Redis集群使QPS提升了300%。
请详细描述你遇到的性能瓶颈是什么，使用了哪些优化手段，
以及你是如何验证优化效果的？

### 第9题 (Technical - Database)
在高并发场景下，MySQL和Redis的数据一致性如何保证？
请列举至少3种方案并分析各自的优缺点。
```

---

## Example 4: Full Output Document Example

Below is a condensed example of the complete output format:

```markdown
# 面试练习题 - 后端工程师

> Generated on: 2026-04-14
> Source: resume.md (字节跳动后端工程师)

---

## 答题说明

1. 请在每道题下方的空白处写下你的答案
2. 完成后对照文档末尾的参考答案进行自我评估
3. 建议限时完成，模拟真实面试场景

---

## 面试题目

### 第1题
你在字节跳动负责抖音推荐系统的微服务架构设计。
请描述你是如何进行服务拆分的，以及你在设计时考虑了哪些核心因素？

---

（请在此作答）



---

### 第2题
请解释分布式系统中的CAP定理，并结合你的项目经验，
说明在推荐系统场景下你是如何权衡Consistency和Availability的？

---

（请在此作答）



---

[Questions 3-10 follow same format...]

---

## 参考答案

### 第1题答案

**考察点**: 微服务架构设计能力、系统思维、实际项目经验

**参考答案**:
一个优秀的回答应该包含以下要点：

1. **服务拆分原则**
   - 按业务领域拆分（Domain-Driven Design）
   - 单一职责原则
   - 关注服务间的依赖关系

2. **核心考虑因素**
   - 数据一致性要求
   - 服务间的通信成本
   - 团队组织结构
   - 部署和运维复杂度

3. **具体实践**
   - 用户服务、内容服务、推荐服务分离
   - 使用消息队列解耦
   - API网关统一入口

**答题建议**:
- 体现DDD思想
- 结合实际项目经验
- 说明权衡取舍的思考过程

### 第2题答案

**考察点**: 分布式系统理论理解、实际应用能力

**参考答案**:
CAP定理指出分布式系统无法同时满足一致性(Consistency)、
可用性(Availability)和分区容错性(Partition Tolerance)。

在推荐系统场景下的权衡：

1. **AP优先场景**
   - 用户个性化推荐：短暂的不一致可接受，但服务必须可用
   - 使用最终一致性方案

2. **CP优先场景**
   - 用户行为数据写入：需要强一致性
   - 使用分布式事务或补偿机制

3. **具体实践**
   - 读写分离架构
   - 缓存策略设计
   - 降级方案准备

**答题建议**:
- 先清晰解释CAP定理
- 结合具体业务场景分析
- 展示实际解决方案
```

---

## Usage Patterns

### Pattern 1: File Path Input (Auto Detection)

```
User: "帮我生成面试题，简历文件是 ./documents/my-resume.pdf"
Action: Read PDF → Infer difficulty from years of experience → Generate questions → Output markdown
```

### Pattern 2: Direct Role with Difficulty

```
User: "准备一下Java后端工程师的面试题，要高级难度的"
Action: Use "Java后端工程师" + Senior difficulty → Generate 10 senior-level questions
```

### Pattern 3: Specify Count Only

```
User: "来5道前端面试题"
Action: Use default difficulty (Mid) + 5 questions → Generate output
```

### Pattern 4: Full Customization

```
User: "我是应届生，要15道初级Java题"
Action: Junior difficulty + 15 questions → Generate comprehensive practice set
```

### Pattern 5: Follow-up Refinement

```
User: "这些题太难了，能不能简单一点？"
Action: Lower difficulty level → Regenerate with easier questions

User: "再来5道"
Action: Generate 5 additional questions at same difficulty
```

### Pattern 6: Mock Interview Simulation

```
User: "模拟面试模式，一道一道来"
Action: Switch to interactive mode → Ask question 1 → Wait for answer → Provide feedback → Continue
```

---

## Difficulty Detection Keywords

### Junior Level Keywords
| Keyword (中文) | Keyword (English) |
|----------------|-------------------|
| 应届生 | new graduate |
| 毕业生 | fresh graduate |
| 新手 | beginner |
| 入门 | entry-level |
| 初级 | junior |
| 1年经验 | 1 year experience |
| 2年经验 | 2 years experience |
| 实习生 | intern |
| 基础题 | basic questions |
| 简单点 | simpler |

### Senior Level Keywords
| Keyword (中文) | Keyword (English) |
|----------------|-------------------|
| 5年以上 | 5+ years |
| 资深 | senior |
| 专家 | expert |
| 架构师 | architect |
| 高级 | advanced |
| 深入点 | in-depth |
| 深入 | deep dive |
| 源码 | source code |
| 原理 | principles |
| 设计 | design |

## Question Count Detection Keywords

| Input Pattern | Detected Count |
|---------------|----------------|
| 5道题 / 5道 / 5题 | 5 |
| 10道题 / 10道 / 10题 | 10 |
| 15道题 / 15道 / 15题 | 15 |
| 20道题 / 20道 / 20题 | 20 |
| 几道 / 几道题 | 5 (default quick) |
| 热热身 / 简单练 / 快速 | 5 |
| 系统准备 / 深度 / 全面 | 15-20 |
| 任意数字 + 题/道 | Use that number |

## Common Interview Topics by Role

### 前端工程师 (Frontend)
**Junior**: HTML/CSS基础、JS语法、框架基础用法
**Mid**: 框架原理、性能优化、工程化实践
**Senior**: 架构设计、源码分析、性能极致优化

### 后端工程师 (Backend)
**Junior**: 语言基础、常用框架、数据库CRUD
**Mid**: 分布式理论、缓存消息队列、SQL优化
**Senior**: 系统设计、源码原理、高可用架构

### 产品经理 (PM)
**Junior**: 需求文档、原型设计、基础数据分析
**Mid**: 用户研究、数据驱动、项目管理
**Senior**: 战略规划、商业洞察、团队领导

### 算法工程师 (Algorithm)
**Junior**: 机器学习基础、常见模型、特征工程
**Mid**: 模型优化、大规模训练、A/B测试
**Senior**: 算法架构、创新研究、业务赋能

---

## Question Type Examples

### Example: Coding Question (编程题)

**User Input:**
> "我是后端开发，来几道算法题练练手"

**Detected:** Technical role + explicit "算法题" request → Increase Coding type to 50%

**Generated Output:**

```markdown
# 面试练习题 - 后端开发 (中级 · 10题)

### 第1题 (编程题)
**题目**: 实现一个LRU (Least Recently Used) 缓存机制

**要求**:
- get 和 put 操作时间复杂度为 O(1)
- 使用你熟悉的编程语言实现
- 请同时说明时间/空间复杂度

**示例**:
```
LRUCache cache = new LRUCache(2); // 容量为2

put(1, 1);
put(2, 2);
get(1);       // 返回 1
put(3, 3);    // 淘汰 key 2
get(2);       // 返回 -1 (未找到)
get(3);       // 返回 3
```

---

**请在此处编写你的代码**:

```java
class LRUCache {
    // 请在这里实现
}
```

---

**参考答案**:
```java
class LRUCache extends LinkedHashMap<Integer, Integer> {
    private int capacity;
    
    public LRUCache(int capacity) {
        super(capacity, 0.75F, true);
        this.capacity = capacity;
    }
    
    public int get(int key) {
        return super.getOrDefault(key, -1);
    }
    
    public void put(int key, int value) {
        super.put(key, value);
    }
    
    @Override
    protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
        return size() > capacity;
    }
}
```

**复杂度分析**:
- 时间: O(1) - HashMap保证get/put都是常数时间
- 空间: O(capacity) - 最多存储capacity个元素

**解题思路**:
1. 使用 HashMap + 双向链表 (或用 LinkedHashMap)
2. HashMap 存储 key 到链表节点的映射，保证 O(1) 查找
3. 双向链表维护访问顺序，头部是最久未使用，尾部是最近使用
4. get 操作时，将节点移到链表尾部
5. put 操作时，如果容量满了，移除链表头部节点
```

---

### Example: System Design Question (系统设计题)

**User Input:**
> "我是5年经验的架构师，准备面试，要系统设计题"

**Detected:** "架构师" + "系统设计" → Senior difficulty + System Design type

**Generated Output:**

```markdown
### 第3题 (系统设计)
**场景**: 设计一个短链接服务 (类似 bit.ly)

**需求**:
- 功能需求: 长链接转短链接、短链接跳转、链接过期管理
- 非功能需求:
  - 支持 1000万 日活用户
  - 读 QPS: 10万/秒
  - 写 QPS: 1000/秒
  - 短链接长度: 不超过 8 个字符
  - 可用性: 99.99%

**约束条件**:
- 短码由 [a-zA-Z0-9] 组成 (共62个字符)
- 需要支持链接分析统计

---

**请设计系统架构**:




---

**参考答案**:

**系统架构**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│  API Gateway │────▶│  Web Server  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                       ┌────────────────────────┼────────────────────────┐
                       │                        │                        │
                       ▼                        ▼                        ▼
                 ┌───────────┐           ┌───────────┐          ┌───────────┐
                 │ URL Service│           │ Analytics │          │  Cache    │
                 └─────┬─────┘           │  Service  │          │ (Redis)   │
                       │                  └───────────┘          └───────────┘
                       ▼
                 ┌───────────┐
                 │   MySQL   │
                 │(主从复制)  │
                 └───────────┘
```

**核心设计要点**:

1. **短码生成策略**
   - 方案A: 自增ID + Base62编码 (简单但可能泄露数据)
   - 方案B: 预生成随机短码池 (更好，但需要存储)
   - 方案C: MurmurHash + Base62 (分布均匀，可能有冲突)
   - **推荐**: 方案B，预生成保证唯一性，还能处理高并发

2. **存储设计**
   - MySQL: 存储短码到长链接的映射
   - Redis: 热点数据缓存 (读多写少，缓存命中率90%+)
   - 分库分表: 按短码首字符分片，或一致性Hash

3. **高可用设计**
   - 主从复制 + 读写分离
   - Redis Cluster 多副本
   - 降级方案: 缓存未命中时直接查DB

4. **扩展性考虑**
   - 预生成短码池，应对写流量突增
   - CDN 缓存跳转响应 (301永久重定向)
   - 链接过期策略: TTL + 定时清理

**关键问题处理**:
- **冲突处理**: 预生成保证唯一，Hash方案需检测冲突并重试
- **缓存穿透**: 布隆过滤器拦截不存在短码
- **数据统计**: 异步写入，避免影响主流程
```

---

### Example: Case Study (案例分析题)

**User Input:**
> "我是产品经理，准备面试，要产品分析题"

**Detected:** "产品经理" + "产品分析" → Increase Case Study type to 40%

**Generated Output:**

```markdown
### 第2题 (案例分析)
**背景**: 你负责一款在线教育APP，近3个月用户留存率(次月留存)从 45% 下降到 28%，但新增用户数保持稳定。

**问题**: 作为产品经理，你会如何分析这个问题？请提出解决方案。

**要求**:
1. 分析可能的原因（至少3个维度）
2. 设计验证方案确认根本原因
3. 提出具体改进措施
4. 如何衡量改进效果

---

**请分析此案例**:




---

**参考答案**:

**问题分析框架** (HEART + 漏斗分析):

**可能原因分析**:

| 维度 | 假设 | 验证方法 |
|------|------|----------|
| **产品体验** | 新功能上线导致学习成本增加 | 用户反馈+NPS调研 |
| **内容质量** | 课程质量下滑，用户学完不续费 | 完课率+评分数据分析 |
| **竞争环境** | 竞品推出更有吸引力的优惠 | 竞品分析+用户流失访谈 |
| **运营策略** | 过度营销导致用户预期过高 | 渠道质量分析 |

**验证方案**:
1. **定量分析**: 分群对比 (留存下降前vs后的用户)、漏斗分析、同期群分析
2. **定性分析**: 流失用户电话访谈 (样本30人)、用户行为录屏分析

**改进措施**:

| 优先级 | 措施 | 预期效果 |
|--------|------|----------|
| P0 | 优化新手引导，降低首课门槛 | 提升首周留存 |
| P1 | 建立课程质量评分体系 | 长期提升内容质量 |
| P2 | 设计召回机制 (短信/推送) | 减少流失 |

**衡量指标**:
- 北极星指标: 次月留存率 (目标: 恢复到 40%+)
- 过程指标: 完课率、NPS、人均学习时长
- 验证周期: 每2周复盘数据
```

---

### Example: Behavioral Question (行为面试)

**User Input:**
> "准备面试，要行为面试题，我是团队负责人"

**Detected:** "团队负责人" + "行为面试" → Increase Behavioral type to 50%

**Generated Output:**

```markdown
### 第5题 (行为面试)
**问题**: 描述一次你与团队成员在技术方案上产生重大分歧的经历。你们如何解决的？最终结果如何？

**建议回答框架** (STAR法则):
- **S**ituation: 描述背景
- **T**ask: 你的任务/目标
- **A**ction: 你采取的具体行动
- **R**esult: 最终结果

---

**请用STAR法则回答**:

Situation:

Task:

Action:

Result:

---

**参考答案**:

**考察点**: 冲突解决能力、技术决策能力、沟通技巧

**STAR示例**:

- **S**: 我们在开发一个支付模块时，我和另一位高级工程师对技术选型有分歧。我主张用成熟的消息队列保证最终一致性，他主张用分布式事务追求强一致性。

- **T**: 作为团队负责人，我需要在技术正确性和团队和谐之间找到平衡，确保项目按时高质量交付。

- **A**: 
  1. 我提议先不争论，各自写一份技术方案文档，列出优缺点
  2. 组织技术评审会，邀请其他资深同事参与，客观评估
  3. 用数据说话：我们做了一个小范围压测，对比两种方案的性能和一致性保证
  4. 最终证明消息队列方案在性能和可维护性上更优，但对方案做了优化，增加了对账机制弥补一致性

- **R**: 
  - 技术方案得到团队一致认可
  - 模块上线后稳定运行，TPS达到预期
  - 那位同事后来反馈说这种决策方式让他心服口服
  - 之后团队遇到分歧都用"文档+数据+评审"的方式，大大提升了决策效率

**答题要点**:
1. 展现你处理冲突的成熟方式，不是"说服"或"妥协"，而是"寻求最优解"
2. 体现数据驱动的决策思维
3. 强调团队和谐和长期信任的建立
4. 结果最好有量化指标

**常见错误**:
- 只讲自己多么正确，对方多么错误
- 避而不谈分歧，只说"我们很和谐"
- 结果是"我赢了"，而不是"我们找到了最优方案"
```

---

### Example: Mixed Types by Role

**User Input:**
> "我是全栈工程师，准备面试，10道题"

**Detected:** "全栈工程师" → 25% Coding + 25% Knowledge + 30% System Design + 20% Behavioral

**Generated Distribution:**

```markdown
# 面试练习题 - 全栈工程师 (中级 · 10题)

题目分布:
- 编程题 (3题): 算法、代码实现
- 问答型 (3题): 前后端技术原理
- 系统设计 (3题): 全栈架构设计
- 行为面试 (1题): 软技能

### 第1题 (编程题)
实现一个函数，判断两个字符串是否是异位词 (Anagram)
...

### 第4题 (问答型)
解释浏览器从输入URL到页面渲染完成的完整流程
...

### 第7题 (系统设计)
设计一个实时聊天系统，支持Web和移动端
...

### 第10题 (行为面试)
描述一次你协调前端和后端团队解决技术债务的经历
...
```

---

## Mock Interview Mode Examples (模拟面试模式)

### Example: Starting a Mock Interview

**User Input:**
> "开始模拟面试，我是前端开发，3年经验"

**System Response (Setup Phase):**

```
好的，我来为你安排一场模拟面试。

**面试配置确认**:
- 职位: 前端开发
- 经验: 3年 → 难度: 中级
- 建议题数: 10题 (预计用时30分钟)
- 题型分布: 编程30% + 问答40% + 系统设计20% + 行为10%

是否需要调整？
- 说 "开始" 直接开始
- 说 "简单一点" / "难一点" 调整难度
- 说 "5题" / "15题" 调整题数
- 说 "多来点算法题" 调整题型
```

---

### Example: Mock Interview In Progress

**System (Question 1):**

```
[面试官] 第 1/10 题 (问答型):

请解释 React 的 useEffect 钩子，它的依赖数组是如何工作的？
如何避免闭包陷阱？

⏱️ 建议思考时间: 2-3 分钟

请作答 (直接回复你的答案):
```

**User Answer:**
> "useEffect 是用来处理副作用的，依赖数组用来控制执行时机。
> 当依赖变化时才会执行。闭包陷阱可以用 useRef 解决。"

**System (Instant Feedback):**

```
[面试官反馈]

**回答评分**: ⭐⭐⭐☆☆ (3/5)

**优点**:
✓ 正确描述了 useEffect 的基本作用
✓ 提到了依赖数组和执行时机的关系

**改进空间**:
○ 缺少对闭包陷阱具体表现的解释 - 建议: 举例说明 "过期的闭包" 问题
○ 没有说明 useEffect 的执行时机 (render 后 vs layout 后)
○ useRef 解决闭包陷阱的方案不够完整 - 建议: 说明 ref 如何保持最新值

**参考答案要点**:
- useEffect 在 render 提交后异步执行，不阻塞渲染
- 依赖数组通过 Object.is 比较，空数组 [] 只在 mount 时执行
- 闭包陷阱: 回调引用了过期的 state/props
- 解决方案: useRef 存储最新值、依赖数组补全、使用函数式更新

**追问**: 如果依赖数组里有一个对象，会出现什么问题？

---
[继续] 下一题 | [追问] 深入这个问题 | [重来] 重新回答
```

---

### Example: Coding Question in Mock Interview

**System (Question 3):**

```
[面试官] 第 3/10 题 (编程题):

**题目**: 实现防抖函数 (debounce)

**要求**:
- 输入: 函数 fn 和延迟时间 delay
- 输出: 防抖后的函数
- 支持取消功能 (cancel 方法)
- 最后一次调用后 delay 时间才执行

**示例**:
```
const debounced = debounce(console.log, 1000);
debounced('a');
debounced('b');
// 1秒后输出: 'b'
```

⏱️ 建议时间: 5-8 分钟

请直接写出代码:
```

**User Code:**
```javascript
function debounce(fn, delay) {
  let timer = null;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  }
}
```

**System (Feedback):**

```
[面试官反馈]

**代码评分**: ⭐⭐⭐☆☆ (3/5)

**优点**:
✓ 核心防抖逻辑正确 (clearTimeout + setTimeout)
✓ 使用了剩余参数 ...args 传递参数

**改进空间**:
○ 未实现 cancel 功能 (题目明确要求)
○ 未考虑 this 上下文绑定问题
○ 缺少立即执行 (leading) 选项的实现

**参考答案**:
```javascript
function debounce(fn, delay, immediate = false) {
  let timer = null;
  
  const debounced = function(...args) {
    const context = this;
    const callNow = immediate && !timer;
    
    clearTimeout(timer);
    
    timer = setTimeout(() => {
      timer = null;
      if (!immediate) fn.apply(context, args);
    }, delay);
    
    if (callNow) fn.apply(context, args);
  };
  
  debounced.cancel = () => {
    clearTimeout(timer);
    timer = null;
  };
  
  return debounced;
}
```

**复杂度分析**:
- 时间: O(1) - 每次调用只涉及定时器操作
- 空间: O(1) - 只存储一个 timer 变量

---
[继续] 下一题
```

---

### Example: Final Summary Report

**System (After 10 Questions):**

```
🎉 模拟面试完成！

# 模拟面试总结报告

**面试配置**:
- 职位: 前端开发
- 难度: 中级
- 题数: 10题 (完成 10题, 跳过 0题)
- 用时: 28分钟

**总体评分**: 72/100

**各题型表现**:
| 题型 | 得分 | 评价 |
|------|------|------|
| 问答型 | 75/100 | 基础概念掌握扎实，但深入原理需加强 |
| 编程题 | 68/100 | 能实现基本功能，边界情况考虑不足 |
| 系统设计 | 70/100 | 架构思路正确，扩展性分析不够深入 |
| 行为面试 | 80/100 | STAR法则运用较好，结果量化清晰 |

**优势领域**:
1. 基础概念理解扎实
2. 沟通表达能力良好
3. 有一定的项目经验积累

**待提升领域**:
1. **边界情况处理** - 编程时多考虑异常输入
2. **源码阅读** - 建议阅读 React/Vue 核心源码
3. **性能优化** - 深入理解浏览器渲染机制和优化策略

**推荐阅读/练习**:
- 《JavaScript 高级程序设计》第 4 版
- React 官方文档 - Hooks 深入
- 前端性能优化清单 (Web.dev)
- 每日一题: LeetCode 简单/中等难度

**下次面试建议**:
- 推荐难度: 中级 → 高级 (可挑战)
- 推荐题型: 增加系统设计题比例
- 练习重点: 手写代码的边界情况处理

是否保存完整 Q&A 记录到文件？
- 说 "保存" 输出 markdown 文档
- 说 "结束" 完成本次面试
```

---

### Mock Interview Commands

在模拟面试过程中，你可以随时使用以下指令：

| 指令 | 作用 |
|------|------|
| "提示" / "hint" | 获得思考方向提示 |
| "跳过" / "skip" | 跳过当前题目 |
| "重来" / "retry" | 重新回答当前题 |
| "结束" / "stop" | 提前结束面试 |
| "暂停" / "pause" | 休息一下，稍后继续 |

---

## Interview History Examples (面试历史记录)

### Example: Viewing History Summary

**User Input:**
> "查看我的练习历史"

**System Output:**

```markdown
# 面试练习历史记录 📊

## 概览统计
- 总练习次数: **8** 次
- 累计答题: **95** 题
- 累计用时: **4.2** 小时
- 最近练习: 2026-04-18

## 难度分布
```
初级 ████████░░░░░░░░░░ 3次 (37%)
中级 █████████████░░░░░ 4次 (50%)
高级 █░░░░░░░░░░░░░░░░░ 1次 (13%)
```

## 题型覆盖统计
| 题型 | 已完成 | 平均得分 |
|------|--------|----------|
| 问答型 | 32题 | 78分 |
| 编程题 | 24题 | 65分 |
| 系统设计 | 18题 | 52分 |
| 案例分析 | 12题 | 70分 |
| 行为面试 | 9题 | 75分 |

## 最近5次练习
| 日期 | 职位 | 难度 | 得分 | 用时 | 趋势 |
|------|------|------|------|------|------|
| 04-18 | 前端开发 | 中级 | 72/100 | 28min | ↗️ +4 |
| 04-15 | 前端开发 | 中级 | 68/100 | 32min | ↗️ +8 |
| 04-12 | 前端开发 | 初级 | 85/100 | 20min | ↗️ +15 |
| 04-10 | 系统设计 | 高级 | 55/100 | 45min | - |
| 04-08 | 前端开发 | 中级 | 60/100 | 30min | - |

## 进步趋势 📈
- 总体平均分: **60分 → 72分** (+12分 ↑)
- 持续练习天数: **5天**
- 最擅长: 技术知识问答 (平均 78分)
- 需加强: 系统设计 (平均 52分)

## 成就解锁 🏆
- 🥉 坚持练习3天
- 🥈 中级难度首次突破70分
- 🎯 完成10道编程题

---
💡 提示: 说 "能力雷达图" 查看可视化能力分析
```

---

### Example: Capability Radar Chart

**User Input:**
> "显示我的能力雷达图"

**System Output:**

```markdown
# 能力雷达图分析 🎯

基于最近 **8次** 练习数据生成

## 五维能力得分

```
技术知识    ████████████████████░░░░░  78/100  [良好]
编程能力    ███████████████░░░░░░░░░░  65/100  [中等]
系统设计    ███████████░░░░░░░░░░░░░░░░  52/100  [待加强] ⚠️
案例分析    ████████████████░░░░░░░░░░░  70/100  [良好]
行为面试    ██████████████████░░░░░░░░░  72/100  [良好]
```

## 可视化雷达图

```
                技术知识
                   78
                   ████
                  ╱    ╲
                 ╱      ╲
    编程能力    ╱        ╲    系统设计
       65     █          █      52
        ╲    ╱            ╲    ╱
         ╲  ╱              ╲  ╱
          ██████████████████
        行为面试    案例分析
           72        70
```

## 能力分析

### 优势领域 💪
1. **技术知识** (78分)
   - 基础概念扎实
   - 框架原理理解到位
   - 继续保持！

2. **行为面试** (72分)
   - STAR法则运用熟练
   - 沟通表达清晰
   - 案例丰富具体

### 待加强领域 📚
1. **系统设计** (52分) ⚠️ 优先级: 高
   - 架构思路需要拓展
   - 扩展性分析不够深入
   - 建议: 多阅读经典架构案例

2. **编程能力** (65分) 优先级: 中
   - 基础算法掌握尚可
   - 边界情况处理需加强
   - 建议: 每日一题，注重代码质量

## 对比上次 (04-15)

| 维度 | 上次 | 本次 | 变化 | 状态 |
|------|------|------|------|------|
| 技术知识 | 75 | 78 | +3 ↗️ | 稳步提升 |
| 编程能力 | 62 | 65 | +3 ↗️ | 持续进步 |
| 系统设计 | 50 | 52 | +2 ↗️ | 缓慢进步 |
| 案例分析 | 68 | 70 | +2 ↗️ | 稳步提升 |
| 行为面试 | 70 | 72 | +2 ↗️ | 稳步提升 |

🎉 **全线进步！继续保持！**

## 突破建议 🚀

针对薄弱环节，推荐以下专项训练：

### 系统设计突破计划
**目标**: 从52分提升到70分

**本周任务**:
- [ ] 阅读《设计数据密集型应用》第1-3章
- [ ] 完成3道系统设计题 (缓存、消息队列、分布式ID)
- [ ] 画一个完整架构图并讲解

**推荐资源**:
- System Design Primer (GitHub)
- 系统设计面试题库
- 极客时间《从0开始学架构》

---
说 "开始练习" 立即开始推荐的专项训练
```

---

### Example: Personalized Recommendation

**User Input:**
> "推荐今天的练习"

**System Output:**

```markdown
# 个性化练习推荐 💡

基于你的历史数据分析，为你量身定制：

## 你的能力画像
```
前端开发 · 3年经验
当前水平: 中级 (平均72分)
下次目标: 高级
预计达成: 2-3周后
```

## 模式识别 🔍

### 优势领域 (保持)
- 前端技术: **82分** (React/Vue/工程化)
- 基础算法: **75分** (数组/字符串/哈希)

### 薄弱环节 (突破)
- 系统设计: **52分** ← 明显短板
- 性能优化: **60分** ← 有待提高

### 进步轨迹
```
初级难度: 85分 (已掌握) ✓
中级难度: 72分 (稳定发挥) ✓
高级难度: 55分 (挑战中) ▶
```

## 今日推荐配置 🎯

| 参数 | 推荐值 | 理由 |
|------|--------|------|
| **难度** | 高级 | 中级已连续3次≥70分，可升级 |
| **题型** | 系统设计 50% + 问答 30% + 编程 20% | 针对薄弱环节专项突破 |
| **题数** | 10题 | 适中题量，保证质量 |
| **模式** | 模拟面试 | 锻炼临场表达，适合高级题 |

### 预计用时
- 答题: 30-40分钟
- 反馈复盘: 15-20分钟
- **总计**: 约1小时

## 今日题目预览

根据推荐配置，今日练习将包括：

1. **系统设计** (5题)
   - 设计一个短链接服务
   - 设计一个实时排行榜
   - 设计一个消息推送系统
   - ...

2. **技术问答** (3题)
   - React Fiber 架构深入
   - 浏览器渲染优化策略
   - ...

3. **编程题** (2题)
   - 实现 Promise.all
   - LRU缓存实现
   - ...

## 学习目标 📝

完成今日练习后，你将：
- [ ] 掌握3种常见系统的设计思路
- [ ] 深入理解React底层原理
- [ ] 手写2个常用工具函数

预期得分: **68-75分** (挑战高级难度)

---

### 快速开始
- 说 **"开始"** 按推荐配置开始练习
- 说 **"调整"** 修改配置 (难度/题数/题型)
- 说 **"换一批"** 重新生成推荐
```

---

### Example: Progress Over Time

**User Input:**
> "看看我的进步趋势"

**System Output:**

```markdown
# 进步趋势分析 📈

统计周期: 过去30天 (12次练习)

## 总体趋势

```
得分趋势 (最近12次)

100 │                                        
 90 │              ●───●                       
 80 │      ●───●       ╲                     
 70 │  ●───╯              ●───●               
 60 │─●                      ╲───●───●───●    
 50 │                              ●          
 40 │                                         
    └──────────────────────────────────────
      1   3   5   7   9  11  13  15  17  19
      
      初级       中级过渡      中级稳定
```

## 关键里程碑 🏆

| 时间 | 事件 | 意义 |
|------|------|------|
| 第1次 | 首次练习，55分 | 起点 |
| 第3次 | 初级难度突破80分 | 掌握基础 ✓ |
| 第6次 | 首次挑战中级，62分 | 难度升级 ▶ |
| 第9次 | 中级难度稳定在70分 | 稳定发挥 ✓ |
| 第12次 | 准备挑战高级 | 下一目标 🎯 |

## 分阶段分析

### 阶段一: 基础建立 (第1-3次)
- **难度**: 初级
- **平均分**: 78分
- **特点**: 快速掌握基础概念
- **用时**: 1周

### 阶段二: 难度跃迁 (第4-6次)
- **难度**: 初级→中级
- **平均分**: 60分 → 68分
- **特点**: 适应期，波动较大
- **用时**: 1.5周

### 阶段三: 稳步提升 (第7-12次)
- **难度**: 中级稳定
- **平均分**: 68分 → 72分
- **特点**: 持续进步，波动减小
- **用时**: 2周

## 预测与建议 🔮

### 未来预测
基于当前进步速度 (每周+3分):
- **2周后**: 预计中级平均分达到 **78分**
- **3周后**: 可稳定挑战 **高级难度**
- **1个月后**: 高级难度预计达到 **65分**

### 加速建议
想要更快进步？试试：
1. **每日一题**: 保持手感，利用碎片时间
2. **专项突破**: 每周集中攻克一个薄弱环节
3. **复盘总结**: 每次练习后回顾错题
4. **模拟实战**: 每周至少1次完整模拟面试

## 同伴对比 (匿名) 👥

与其他同水平用户对比:

| 指标 | 你 | 平均 | 排名 |
|------|-----|------|------|
| 练习频次 | 每3天1次 | 每5天1次 | 前30% ✅ |
| 平均得分 | 72分 | 65分 | 前25% ✅ |
| 进步速度 | +3分/周 | +2分/周 | 前20% ✅ |

🎉 **你的努力超过了大多数同龄人！**

---
说 "查看详细" 查看每次练习的具体分析
```

---

### History Commands Summary

| 指令 | 功能 |
|------|------|
| "查看历史" / "历史记录" | 显示练习统计和列表 |
| "能力雷达图" / "雷达图" | 可视化能力分布 |
| "进步趋势" / "趋势分析" | 得分变化曲线 |
| "上次成绩" / "上次面试" | 最近一次详情 |
| "推荐练习" / "今天练什么" | 个性化推荐 |
| "继续上次" / "接着练" | 恢复未完成练习 |
| "清除历史" | 重置所有记录 (需确认) |

---

## Offer-Oriented Feature Examples (拿 Offer 导向功能)

### Example: 7-Day Sprint Plan

**User Input:**
> "我两周后要面前端，给我一个7天冲刺计划"

**System Output:**

```markdown
# 7天面试冲刺计划 - 前端工程师

> 当前水平: 中级
> 目标: 两周后参加社招面试
> 每日投入: 40分钟

## Day 1 - 基线评估
- 目标: 明确当前短板
- 任务: 6题（问答2 + 编程2 + 行为2）
- 验收: 生成薄弱项Top2

## Day 2 - JavaScript 核心
- 目标: 提升语言基础深度
- 任务: 问答3 + 编程2
- 验收: 技术知识维度 >= 70

## Day 3 - React 原理
- 任务: 问答2 + 场景题2 + 行为1

## Day 4 - 工程化与性能
- 任务: 场景题3 + 编程2

## Day 5 - 系统设计入门
- 任务: 系统设计2 + 问答2 + 行为1

## Day 6 - 模拟面试
- 任务: 10题模拟面试（限时）
- 验收: 完成度 >= 90%

## Day 7 - 复盘与补弱
- 任务: 仅做薄弱项专项题
- 验收: 薄弱维度提升 >= 8分

## 达标条件
- 综合评分 >= 75
- 能输出2分钟项目讲解版本
```

---

### Example: Job Readiness Score

**User Input:**
> "我现在能去面试前端中级岗吗？"

**System Output:**

```markdown
# 岗位就绪度评估 - 前端中级岗

**Job Readiness Score**: 71/100
**当前等级**: 可投递（建议补强后命中率更高）

## 维度评分
- 技术知识: 19/25
- 编程能力: 17/25
- 系统设计: 11/20
- 行为面试: 12/15
- 表达结构化: 12/15

## 风险项 (Top 2)
1. 系统设计稳定性与扩展性表达不足
2. 编程题边界条件覆盖不完整

## 两周提升路线
- Week 1: 每天1道系统设计 + 1道编程题复盘
- Week 2: 每2天1次模拟面试，重点练追问应对

## 投递建议
- 可以开始投递中级岗
- 优先投技术栈高度匹配的岗位
- 面试前先完成3次高压模拟面试
```

---

### Example: Answer Rewriter (高分话术改写)

**User Input:**
> "帮我把这个答案改成高分表达：我做过性能优化，主要是加缓存，页面快了很多。"

**System Output:**

```markdown
# 回答优化结果

## 你的原答案问题
1. 信息过于抽象，缺少背景与目标
2. 没有说明具体动作和技术决策
3. 缺少量化结果，面试官无法判断价值

## 高分版本（30秒）
在电商活动页项目中，我负责首屏性能优化。我们先用 Lighthouse 和 Performance 面板定位瓶颈，发现首屏资源体积过大和重复请求较多。随后我做了静态资源分包、接口缓存和图片懒加载，最终首屏渲染时间从 3.2s 降到 1.8s，转化率提升约 6%。

## 高分版本（2分钟）
我在一个高流量活动页里负责性能优化。首先我们做了基线测量：LCP 3.2s，首屏 JS 体积偏大，且关键接口存在重复请求。  
我拆成三层优化：  
1) 资源层：按路由分包，移除未使用依赖，图片改 WebP 并启用懒加载；  
2) 网络层：对热点接口做短时缓存与请求合并，减少重复请求；  
3) 渲染层：对长列表做虚拟滚动并延迟非关键模块加载。  
上线后 LCP 从 3.2s 降到 1.8s，白屏时间下降约 35%，页面转化率提升 6%。  
如果再做一版，我会补上性能监控告警，把指标波动纳入日常看板，确保优化持续有效。

## 可能追问与应对
1. Q: 你怎么确认优化不是“错觉”？  
   A: 我们在发布前后都用同一套指标（LCP/FCP/TTI）对比，并按流量分组看趋势，确保结果稳定。  
2. Q: 缓存会不会带来数据不一致？  
   A: 对实时性要求高的数据不做长缓存，只做短 TTL + 主动失效，保证性能和一致性平衡。
```
