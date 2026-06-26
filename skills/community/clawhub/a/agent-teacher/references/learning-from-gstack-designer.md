# Designer 学习指南：借鉴 Gstack

> 参考：memory/knowledge/fw-gstack-overview.md
> 原项目：https://github.com/garrytan/gstack

---

## Designer 在 Gstack 中的对应角色

| Gstack角色 | 职责 | 对Designer的借鉴 |
|-----------|------|-----------------|
| **/plan-design-review** | 设计评审，0-10评分 | 设计产出需要被评审 |
| **/design-consultation** | 从零构建设计系统 | 设计是系统化工作 |
| **/design-review** | 审计+修复，原子提交 | 设计需要验证和迭代 |
| **Senior Designer** | 识别AI垃圾 | 批判性审视AI产出 |

---

## Designer 可以学习的核心能力

### 1. 设计评审机制

**Gstack做法**：
- 每个设计维度0-10评分
- 明确说明10分是什么样的
- 然后修改计划达到10分

**Designer应该做**：
- 产出设计稿时自评质量（0-10）
- 明确什么是"10分设计"
- 识别当前差距

---

### 2. 设计文档标准化

**Gstack的DESIGN.md**：
- 设计决策记录在文档中
- 后续流程读取设计文档
- 文档是设计和其他环节的连接器

**Designer应该做**：
- 每个设计决策写简短说明
- 记录为什么选A不选B
- 让其他人能看懂设计逻辑

---

### 3. AI垃圾检测

**Gstack的AI Slop Detection**：
- 识别看起来像AI生成的低质量设计
- 保持设计的原创性和人性化

**Designer应该做**：
- 收到AI辅助设计时，批判性审视
- 确保设计有独特视角，不是泛泛之辈
- 问：这个设计解决的是真实问题吗？

---

### 4. 设计验证（类似/qa）

**Gstack的/qa**：
- 真浏览器测试，不只是静态检查
- 找到问题直接修复
- 生成回归测试防止问题重现

**Designer应该做**：
- 设计稿出来后，用工具模拟验证
- 美术风格图生成后，检查是否达到预期
- 如果不符合预期，说明需要调整什么

---

### 5. 前后对比思维

**Gstack的/design-review**：
- 原子提交，每个改动独立
- 前后截图对比
- 明确每个版本改进了什么

**Designer应该做**：
- 每次迭代保存前后对比
- 记录设计演进路径
- 不只是交付最终稿，也要展示过程

---

### 6. 创意风险意识

**Gstack的/design-consultation**：
- 提出安全选择 AND 创意风险
- 不只做保守设计

**Designer应该做**：
- 方案中包含"安全选项"和"创意押注"
- 说明每个选项的风险和收益
- 敢于在合适时做大胆设计

---

## 行动项

- [ ] 阅读完整Overview：memory/knowledge/fw-gstack-overview.md
- [ ] 重点看 /plan-design-review 和 /design-consultation 的设计
- [ ] 以后产出设计时，附上设计文档说明决策
- [ ] 练习对每个设计维度自评0-10

---

## 相关文件

- 总览：memory/knowledge/fw-gstack-overview.md
- Gstack原项目：https://github.com/garrytan/gstack
