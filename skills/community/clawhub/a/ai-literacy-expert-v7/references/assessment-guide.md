# AI 学习评估师指南（V5 新增）

> 本文是 V5 能力四「AI 学习评估师」的设计与实现手册。支持自适应测评、薄弱点诊断、个性化学习建议。

## 一、核心理念

- **评估即学习**：测评本身也是一次知识巩固过程
- **自适应难度**：根据答题表现动态调整题目难度
- **诊断驱动**：找出薄弱点，给出具体改进建议
- **离线可用**：评估系统完全离线运行，保护学习数据隐私

## 二、能力触发

### 2.1 触发词
- 「测评」「练习题」「学习效果」「测验」「考试」「评估」
- 「薄弱点」「哪里不会」「知识点诊断」「学习报告」
- 「生成一套题」「出个测验」「检查我学得怎么样」

### 2.2 输入参数
| 参数 | 类型 | 说明 |
|------|------|------|
| audience | enum | 中学生 / 大学生 / 教师 / 企业 |
| completed_modules | string[] | 已完成的模块列表，如 ['A1', 'A2', 'C1'] |
| target_modules | string[] | 待测评的模块（可与 completed_modules 相同） |
| difficulty | enum | 简单(1) / 中等(2) / 困难(3) / 自适应 |
| question_count | number | 生成题数（默认 20） |
| question_types | string[] | 题型偏好：单选/多选/填空/编程/实操 |

## 三、评估流程

### Phase 1 · 模块确认
```
用户：做个测评
AI：请告诉我你要测评的模块（可多选）：
     A1 AI进化历程 / A2 AI是什么 / A3 协作哲学 / ...
     或输入「全部模块」
```

### Phase 2 · 难度确认
```
AI：请选择测评难度：
     ① 简单（巩固基础）
     ② 中等（知识迁移）
     ③ 困难（综合应用）
     ④ 自适应（AI 根据表现动态调整）
```

### Phase 3 · 题量确认
```
AI：请选择题目数量：
     ① 10题（约15分钟）
     ② 20题（约30分钟）← 默认
     ③ 30题（约45分钟）
     ④ 50题（约60分钟）
```

### Phase 4 · 测评执行
- AI 生成测评题目（JSON 格式）
- 用户在单 HTML 界面作答
- 实时保存进度（IndexedDB）

### Phase 5 · 评分与报告
- AI 智能评分（支持主观题 AI 批改）
- 薄弱点诊断（知识点关联图谱）
- 个性化学习建议报告（PDF 导出）

## 四、题型设计

### 4.1 题型分类

| 题型 | 适用场景 | 计分方式 |
|------|----------|----------|
| 单选题 | 概念辨析、事实记忆 | 选对 +4 分 |
| 多选题 | 关联分析、综合判断 | 全对 +5 分，漏选 +2 分 |
| 填空题 | 关键概念、公式记忆 | 关键词匹配 +5 分 |
| 编程题 | 实践操作、代码能力 | 语法 + 逻辑 + 输出 +5 分 |
| 实操题 | 工具使用、流程掌握 | 步骤完整性 + 准确性 |

### 4.2 难度等级

| 等级 | 描述 | 示例 |
|------|------|------|
| L1 记忆 | 事实性知识 | "ChatGPT 是哪家公司发布的？" |
| L2 理解 | 概念解释 | "解释什么是 Prompt Engineering" |
| L3 应用 | 迁移使用 | "为一个数据分析任务设计 Prompt" |
| L4 分析 | 关联辨析 | "对比 RAG 与 Fine-tuning 的优劣" |
| L5 创造 | 综合创新 | "设计一个 AI 辅助教学系统" |

## 五、自适应算法

### 5.1 项目反应理论（IRT）

```
P(答对) = 1 / (1 + e^(-a*(θ - b)))
- a: 题目区分度
- b: 题目难度
- θ: 学习者能力水平
```

### 5.2 自适应策略

```
初始 θ = 0（中等水平）
每题后更新 θ：
- 答对 → θ += delta（delta 根据题目难度调整）
- 答错 → θ -= delta
根据新 θ 选择下一题：
- θ < -1 → 选择 L1/L2 题目
- -1 <= θ < 0 → 选择 L2 题目
- 0 <= θ < 1 → 选择 L3 题目
- θ >= 1 → 选择 L4/L5 题目
```

## 六、薄弱点诊断

### 6.1 知识点图谱

```javascript
const knowledgeGraph = {
  'A1': { name: 'AI进化历程', depends: [], weight: 1.0 },
  'A2': { name: 'AI是什么', depends: ['A1'], weight: 1.2 },
  'A3': { name: '协作哲学', depends: ['A2'], weight: 1.5 },
  'C1': { name: 'Prompt基础', depends: ['A2', 'A3'], weight: 2.0 },
  'C2': { name: '需求拆解', depends: ['C1'], weight: 2.0 },
  // ...
};
```

### 6.2 诊断输出

| 薄弱点 | 错误率 | 关联知识点 | 建议学习资源 |
|--------|--------|------------|--------------|
| C1 Prompt优化 | 60% | A2, A3 | → 课件「C1 Prompt进阶」 |
| C3 验证闭环 | 45% | C1, C2 | → 游戏「验证大冒险」 |

## 七、单 HTML 评估界面

### 7.1 技术栈
- HTML5 + 原生表单
- CSS：响应式 + 移动端友好
- IndexedDB：离线进度存储
- PDF-lib：报告生成

### 7.2 界面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>V5 AI 学习评估系统</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf-lib/1.17.1/pdf-lib.min.js"></script>
  <style>/* 响应式 + 测评卡片样式 */</style>
</head>
<body>
  <header>
    <h1>🎯 AI 学习评估</h1>
    <div id="progress">进度: <span id="current">0</span>/<span id="total">20</span></div>
    <div id="timer">剩余时间: <span id="time">30:00</span></div>
  </header>
  
  <main id="questions">
    <!-- 动态加载题目 -->
  </main>
  
  <div id="controls">
    <button id="prev" disabled>上一题</button>
    <button id="next">下一题</button>
    <button id="submit" disabled>提交测评</button>
  </div>
  
  <div id="report" style="display:none">
    <!-- 评估报告 -->
  </div>
  
  <script>
    // IndexedDB 存储进度
    // 自适应算法选题
    // 实时评分 + 薄弱点统计
    // PDF 报告生成
  </script>
</body>
</html>
```

### 7.3 报告模板

```html
<div id="report">
  <h2>📊 学习评估报告</h2>
  <div class="score-card">
    <div class="score">85</div>
    <div class="label">综合得分</div>
  </div>
  
  <h3>📈 薄弱点诊断</h3>
  <div class="weak-points">
    <div class="point">
      <span class="module">C1 Prompt优化</span>
      <span class="rate">正确率 40%</span>
      <span class="suggestion">→ 推荐学习「C1 Prompt进阶」课件</span>
    </div>
  </div>
  
  <h3>💡 个性化建议</h3>
  <ul>
    <li>建议优先复习 A2 模块中的「AI能力边界」章节</li>
    <li>多练习 C1 模块的「复杂任务分解」实战</li>
    <li>可尝试「协作哲学」游戏巩固协作思维</li>
  </ul>
  
  <button id="export-pdf">📕 导出 PDF 报告</button>
</div>
```

## 八、离线支持

### 8.1 IndexedDB Schema

```javascript
const db = {
  name: 'ai-literacy-assessment',
  version: 1,
  stores: {
    progress: { keyPath: 'questionId' },      // 答题进度
    results: { keyPath: 'sessionId' },          // 历史成绩
    questions: { keyPath: 'id' }                 // 缓存题目
  }
};
```

### 8.2 离线测评流程

```
1. 首次加载：AI 生成题目 → 存入 IndexedDB
2. 离线作答：读取缓存题目 → 本地作答 → 保存进度
3. 联网提交：恢复网络 → 上报成绩 → 获取报告
4. 完全离线：本地评分 → 生成离线报告
```

## 九、强制测试门控（评估专项）

| 检查项 | 标准 |
|--------|------|
| 题目生成质量 | 每个模块至少 2 道题覆盖 |
| 自适应算法 | θ 更新正确，无越界 |
| 评分准确性 | 与标准答案匹配率 100% |
| 薄弱点诊断 | 错误率 >50% 的知识点必须标记 |
| 报告生成 | PDF 可导出，内容完整 |
| 离线存储 | IndexedDB 读写成功 |
| 进度保存 | 刷新页面进度不丢失 |
| 跨浏览器 | Chrome/Edge/Safari/Firefox 均可用 |
| 移动端 | 手机答题体验流畅 |

## 十、与能力一/二/三的联动

| 联动场景 | 说明 |
|----------|------|
| 课件 → 评估 | 学完课件后自动推荐测评 |
| 游戏 → 评估 | 游戏得分映射到对应模块能力值 |
| 备课 → 评估 | 备课阶段预设评估题库 |
| 评估 → 课件 | 薄弱点直接推荐对应课件 |
| 评估 → 游戏 | 薄弱模块推荐对应游戏强化 |
