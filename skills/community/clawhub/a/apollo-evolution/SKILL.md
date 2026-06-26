---
name: apollo-evolution
description: 像生命进化一样复制、变异、选择——让Skill在迭代中自我优化。
version: 1.0.0
---

# Apollo Evolution
> 像生命进化一样，让Skill在复制+变异+选择中自我优化

---

## 核心概念

生命的进化来自三个机制：
```
复制（Reproduction）→ 变异（Mutation）→ 选择（Selection）
```

Skill的优化也可以类比：
```
复制（Copy）→ 变异（Tweak）→ 测试（Test）→ 选择（Keep Best）
```

---

## 为什么重要？

- Skill不是一次性写死的，需要在实战中进化
- 同一个目标，不同写法效果差异大
- 通过"自然选择"保留最优版本

---

## 生物机制对照表

| 生命机制 | Skill机制 | 说明 |
|---------|----------|------|
| DNA复制 | Skill模板拷贝 | 保留核心逻辑 |
| 基因突变 | 参数/提示词变异 | 尝试不同方式 |
| 环境选择 | 效果测试 | 哪个解决问题更好 |
| 适者生存 | 保留最优版本 | 淘汰差的 |
| 表观遗传 | 经验传递给下一代 | 保留有用经验 |

---

## 工作流程

```
1. 复制（Copy）
   - 选定一个要优化的Skill
   - 复制一份作为"母本"

2. 变异（Tweak）
   - 改变System Prompt的某一部分
   - 调整参数（temperature, max_tokens等）
   - 修改工作流步骤

3. 测试（Test）
   - 用同一组输入测试所有版本
   - 记录效果评分

4. 选择（Select）
   - 保留效果最好的版本
   - 淘汰效果差的版本

5. 重复（Iterate）
   - 下一代继续复制+变异+选择
   - 迭代N轮后，Skill会越来越强
```

---

## 变异类型

### Prompt变异
- 改变角色设定
- 调整输出格式
- 添加/删除约束条件

### 参数变异
- temperature: 0.5 → 0.8 → 1.0
- max_tokens: 1024 → 2048 → 4096
- top_p: 0.9 → 0.95 → 1.0

### 结构变异
- 增加一个判断步骤
- 拆分复杂任务
- 添加验证环节

---

## 脚本使用方法

```bash
# 复制一个Skill作为起点
bash scripts/apollo-evolution/copy.sh apollo-workflow

# 生成变异版本
bash scripts/apollo-evolution/mutate.sh apollo-workflow-v1

# 测试并评分
bash scripts/apollo-evolution/test.sh apollo-workflow-v1 apollo-workflow-v2

# 选择最优
bash scripts/apollo-evolution/select.sh
```

---

## 状态文件

Evolution的状态存储在：
```
.memory/evolution/{skill_name}/
├── generations.json    # 代数记录
├── variants/           # 变异版本
│   ├── gen-001/
│   ├── gen-002/
│   └── ...
└── fitness.json       # 适应度评分
```

---

## 下一步

- [ ] 实现 copy.sh（Skill复制）
- [ ] 实现 mutate.sh（生成变异）
- [ ] 实现 test.sh（自动化测试）
- [ ] 实现 select.sh（选择最优）
- [ ] 集成到Apollo工作流

---

## 相关Skill

- apollo-stem（自我更新）— 与进化相关
- apollo-dream（记忆整理）— 保存进化经验
- apollo-epi（知识传承）— 传递最佳实践
