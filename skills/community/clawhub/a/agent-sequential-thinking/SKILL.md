# 序列思考 Skill (Sequential Thinking)

基于 MCP Sequential Thinking Server 设计的复杂任务分解工具。

## 功能

1. **任务分解** - 将复杂问题分解为可管理的步骤
2. **动态调整** - 随理解深入修订和调整思考步骤数
3. **分支探索** - 探索替代推理路径
4. **假设验证** - 生成和验证解决方案假设

## 思考流程

```
问题定义 → 信息收集 → 问题分解 → 多维分析 → 
建立连接 → 生成方案 → 评估选择 → 实施反馈
```

## 使用方法

### 输入参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `thought` | 当前思考内容 | "首先分析问题边界..." |
| `thoughtNumber` | 当前步骤编号 | 1 |
| `totalThoughts` | 预估总步骤数 | 8 |
| `nextThoughtNeeded` | 是否需要下一步 | true |
| `isRevision` | 是否修订之前思考 | false |
| `revisesThought` | 修订的步骤编号 | 3 |
| `branchFromThought` | 分支起点 | 5 |
| `branchId` | 分支标识 | "方案A" |
| `needsMoreThoughts` | 需要更多步骤 | false |

### 示例输出

```json
{
  "thoughtNumber": 1,
  "totalThoughts": 8,
  "thought": "首先分析问题边界：用户需要一个金融数据看板",
  "nextThoughtNeeded": true,
  "branches": []
}
```

## 适用场景

- ✅ 分解复杂问题
- ✅ 需要修订的规划和设计
- ✅ 初始不清楚全貌的问题
- ✅ 需要多步骤保持上下文的任务
- ✅ 需要过滤无关信息的情况

## System Prompt 集成

在 Agent 的 System Prompt 中添加：

```
## 思考模式

遇到复杂任务时，使用序列思考：

1. 问题定义
   - 明确任务目标和边界
   - 识别关键约束

2. 信息收集
   - 检索相关记忆
   - 搜索必要信息

3. 问题分解
   - 拆分为子任务
   - 确定优先级

4. 多维分析
   - 技术角度：可行性、复杂度
   - 用户角度：体验、偏好
   - 时间角度：紧急度、工作量

5. 建立连接
   - 关联已有知识
   - 识别依赖关系

6. 生成方案
   - 提出多个候选方案
   - 考虑分支可能性

7. 评估选择
   - 对比方案优劣
   - 选择最优路径

8. 实施反馈
   - 执行并监控结果
   - 根据反馈调整
```

## 分支示例

当发现当前路径可能不是最优时，创建分支：

```
thoughtNumber: 5
thought: "方案A（Streamlit）可行，但方案B（React）可能更适合长期维护"
branchFromThought: 5
branchId: "方案B"
totalThoughts: 10  // 增加步骤数以探索分支
```

## 修订示例

当发现之前的思考有误时，修订：

```
thoughtNumber: 6
thought: "修正：方案A的部署问题可以通过更新依赖解决"
isRevision: true
revisesThought: 4
```

## 与 OpenClaw 集成

### 自动触发条件

- 任务涉及多个步骤
- 问题复杂度超过阈值
- 用户明确要求"思考一下"
- 需要对比多个方案

### 思考输出格式

思考过程可以输出为 Markdown，记录在 `memory/thinking-YYYY-MM-DD.md`：

```markdown
# 思考记录：金融数据看板部署

## 步骤 1：问题定义
任务：部署金融数据看板到公网

## 步骤 2：信息收集
- 已有：本地运行正常
- 需要：公网 URL、免费方案

## 步骤 3：问题分解
1. 选择部署平台
2. 修复依赖问题
3. 上传代码
4. 测试访问

## 步骤 4：多维分析
...

## 步骤 7：评估选择
方案 A（Streamlit Cloud）：推荐
理由：免费、自动部署、适合展示

## 步骤 8：实施反馈
结果：部署成功
URL: https://finance-dashboard-xxx.streamlit.app
```

---

*基于 MCP Sequential Thinking Server 设计*