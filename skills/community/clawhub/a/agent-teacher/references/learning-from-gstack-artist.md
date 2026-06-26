# Artist 学习指南：借鉴 Gstack

> 参考：memory/knowledge/fw-gstack-overview.md
> 原项目：https://github.com/garrytan/gstack

---

## Artist 在 Gstack 中的对应角色

> 注意：Gstack主要面向代码产品，直接对应的设计角色较少。
> 以下是从其他角色中提取的适用原则。

| Gstack角色 | 职责 | 对Artist的借鉴 |
|-----------|------|-----------------|
| **/qa** | 真浏览器验证，找到bug直接修 | 产出后验证，不只是交付 |
| **/design-review** | 前后对比，原子提交 | 记录创作演进 |
| **/retro** | 每周反思，识别成长机会 | 定期审视产出质量趋势 |
| **并行sprints** | 多个任务同时跑 | 优化并行工作流程 |

---

## Artist 可以学习的核心能力

### 1. QA验证思维

**Gstack的/qa**：
- 真浏览器点击验证，不只是静态检查
- 找到问题直接修复+生成回归测试
- 验证修复有效

**Artist应该做**：
- 生成的图不只是跑完就交
- 用工具/方法验证产出符合预期
- 如果不符合，说清楚需要调整什么

---

### 2. 前后对比和质量追踪

**Gstack的/design-review**：
- 每个版本前后截图对比
- 原子提交，每个改动独立
- 明确改进点

**Artist应该做**：
- 每次迭代保存前后对比
- 记录：这张图改了什么、为什么改
- 长期追踪自己的质量趋势

---

### 3. 并行工作流

**Gstack的并行sprints**：
- 10-15个sprint同时跑
- 不同功能、不同分支

**Artist应该做**：
- 识别可以并行的创作任务
- 不要等一个完成才开始下一个
- 用session管理不同任务的上下文

---

### 4. 定期自我反思（/retro）

**Gstack的/retro关注点**：
- 每人产出分解
- 测试健康趋势
- 成长机会

**Artist应该做**：
- 定期审视：最近产出质量稳定吗？
- 识别：哪些风格/类型效果最好
- 找到：需要提升的方向

---

### 5. 批判性审视AI辅助产出

**Gstack的AI Slop Detection**：
- 识别看起来像AI生成的平庸设计
- 保持创作的独特视角

**Artist应该做**：
- AI生成的图不要直接用，要有判断
- 问：这个图有独特视角吗？
- 确保产出有艺术家人为的审美判断

---

### 6. 设计系统思维

**Gstack的/design-consultation**：
- 从零构建设计系统
- 研究竞品、提出创意风险

**Artist应该做**：
- 为项目建立美术风格规范
- 研究同类游戏的视觉风格
- 在规范内创新，不只是随机创作

---

## 行动项

- [ ] 阅读完整Overview：memory/knowledge/fw-gstack-overview.md
- [ ] 重点看 /qa 和 /design-review 的验证方法
- [ ] 以后产出时验证是否符合预期，不只是提交
- [ ] 建立自己的质量标准和前后对比习惯

---

## 相关文件

- 总览：memory/knowledge/fw-gstack-overview.md
- Gstack原项目：https://github.com/garrytan/gstack
