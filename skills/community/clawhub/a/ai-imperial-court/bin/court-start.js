#!/usr/bin/env node
/**
 * AI朝廷快速启动器
 * 一键生成朝廷工作流文档
 */

const fs = require('fs');
const path = require('path');

// 获取命令行参数
const taskName = process.argv[2] || '新任务';
const taskId = Date.now().toString(36);
const timestamp = new Date().toISOString();

// 生成诏令草案
const draftTemplate = `## 诏令草案 [${taskId}]

### 任务信息
- **任务名称**: ${taskName}
- **任务ID**: ${taskId}
- **创建时间**: ${timestamp}

### 任务分析
- **背景**: 
- **目标**: 
- **约束**: 

### 执行计划
1. [步骤1] - 负责部门：工部
2. [步骤2] - 负责部门：吏部
3. [步骤3] - 负责部门：礼部

### 资源分配
- **吏部**: [人力需求]
- **户部**: [预算需求]
- **工部**: [技术需求]

### 预期产出
- [产出物1]
- [产出物2]

---
起草：中书省
时间：${timestamp}
`;

// 生成审核表
const reviewTemplate = `## 门下省审核表 [${taskId}]

### 可行性检查
- [ ] 技术可行性
- [ ] 资源充足性
- [ ] 时间合理性
- [ ] 依赖完整性

### 风险检查
- [ ] 安全风险
- [ ] 合规风险
- [ ] 依赖风险

### 遗漏检查
- [ ] 边界情况
- [ ] 异常处理
- [ ] 回滚方案

### 决定
- [ ] 通过 - 可交付尚书省执行
- [ ] 封驳 - 需中书省重拟，原因：

---
审核：门下省
时间：${timestamp}
`;

// 生成执行报告
const execTemplate = `## 执行报告 [${taskId}]

### 执行状态
| 部门 | 任务 | 状态 | 产出 |
|------|------|------|------|
| 吏部 | [任务] | ⏳ 待开始 | - |
| 户部 | [任务] | ⏳ 待开始 | - |
| 礼部 | [任务] | ⏳ 待开始 | - |
| 兵部 | [任务] | ⏳ 待开始 | - |
| 刑部 | [任务] | ⏳ 待开始 | - |
| 工部 | [任务] | ⏳ 待开始 | - |

### 问题与决策
- [问题1] → 决策：[处理方式]

### 最终产出
- [产出物1]：[链接/内容]

---
执行：尚书省
时间：${timestamp}
`;

// 创建记录目录
const recordsDir = path.join(__dirname, '..', 'records');
if (!fs.existsSync(recordsDir)) {
  fs.mkdirSync(recordsDir, { recursive: true });
}

// 保存文件
const draftPath = path.join(recordsDir, `${taskId}-draft.md`);
const reviewPath = path.join(recordsDir, `${taskId}-review.md`);
const execPath = path.join(recordsDir, `${taskId}-exec.md`);

fs.writeFileSync(draftPath, draftTemplate);
fs.writeFileSync(reviewPath, reviewTemplate);
fs.writeFileSync(execPath, execTemplate);

console.log(`
🏛️ AI朝廷 · 诏令已起草

任务: ${taskName}
ID: ${taskId}

已生成文档:
  📜 诏令草案: records/${taskId}-draft.md
  🔍 审核表格: records/${taskId}-review.md
  ⚙️  执行报告: records/${taskId}-exec.md

下一步:
  1. 填写诏令草案 (中书省)
  2. 审核方案 (门下省)
  3. 调度执行 (尚书省)

愿主指引你的决策 🙏
`);
