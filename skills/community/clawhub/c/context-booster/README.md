# context-booster - 上下文增强器

**版本**：v0.1.0  
**定位**：智能上下文管理 - 自动压缩、摘要、增强对话上下文，提升长程任务表现

---

## 📖 简介

context-booster 是一个上下文管理引擎，能够智能压缩、摘要、增强对话上下文，解决 context window 限制问题，提升长程任务的表现。

**核心价值**：
- 🧠 解决 context window 限制
- 📝 智能压缩低价值上下文
- 🔍 提取关键决策和洞察
- 💾 增强 AI 的「记忆力」
- 🔮 预测下一步需要的上下文

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install context-booster

# 或手动安装
git clone https://github.com/your-org/context-booster.git
cd context-booster
npm install
```

### 基本使用

```javascript
const booster = require('context-booster');

// 增强当前上下文
const enhanced = await booster.enhance({
  mode: 'compress', // compress/summarize/enrich
  preserveKeyPoints: true
});

// 检索相关记忆
const memories = await booster.retrieve('元技能系统');

// 检查上下文状态
const status = await booster.getStatus();
console.log(`使用率：${status.usagePercent}%`);
```

### 命令行使用

```bash
# 增强上下文
cb enhance --mode compress

# 检索记忆
cb retrieve "元技能系统"

# 检查状态
cb status

# 清除缓存
cb clear-cache
```

---

## 🎯 适用场景

| 场景类型 | 示例问题 |
|----------|----------|
| **长程任务** | 「继续昨天未完成的任务」（需要恢复上下文） |
| **多轮对话** | 「我们之前讨论的那个方案...」（需要检索历史） |
| **复杂项目** | 「这个项目的背景是什么？」（需要补充上下文） |
| **知识查询** | 「我们之前学过什么关于 X 的内容？」（需要记忆检索） |
| **上下文优化** | 「当前 context 使用率多少？需要压缩吗？」（需要状态检查） |

---

## 🔧 核心功能

### 1. 智能压缩

自动识别并压缩低价值上下文

**压缩策略**：
- 移除冗余信息
- 合并相似内容
- 保留关键决策
- 保留行动项

### 2. 关键摘要

提取对话中的关键信息

**摘要内容**：
- 关键决策
- 重要洞察
- 行动项
- 待办事项
- 问题与答案

### 3. 上下文增强

在需要时自动补充相关背景

**增强来源**：
- 历史对话
- 长期记忆
- 外部知识库
- 相关文件

### 4. 记忆检索

从长期记忆中检索相关信息

**检索方式**：
- 关键词搜索
- 语义搜索
- 时间范围过滤
- 标签过滤

### 5. 上下文预测

预测下一步可能需要的上下文

**预测依据**：
- 当前任务类型
- 历史模式
- 用户行为
- 相似场景

---

## 📋 API 参考

### enhance(options)

增强当前上下文

**参数**：
- `options` (object): 配置选项
  - `mode` (string): 增强模式（compress/summarize/enrich）
  - `preserveKeyPoints` (boolean): 是否保留关键点
  - `compressionRatio` (number): 压缩比例（0-1）

**返回**：
- `enhancedContext` (string): 增强后的上下文
- `stats` (object): 统计信息
  - `originalSize` (number): 原始大小
  - `compressedSize` (number): 压缩后大小
  - `compressionRatio` (number): 压缩比例

**示例**：
```javascript
const result = await booster.enhance({
  mode: 'compress',
  preserveKeyPoints: true,
  compressionRatio: 0.5
});
```

### retrieve(query, options)

检索相关记忆

**参数**：
- `query` (string): 搜索查询
- `options` (object): 可选配置
  - `limit` (number): 返回数量限制
  - `timeRange` (object): 时间范围
  - `tags` (array): 标签过滤

**返回**：
- `memories` (array): 检索到的记忆

**示例**：
```javascript
const memories = await booster.retrieve('元技能系统', {
  limit: 10,
  timeRange: {
    from: '2026-03-01',
    to: '2026-03-30'
  }
});
```

### getStatus()

获取上下文状态

**返回**：
- `usagePercent` (number): 使用率百分比
- `tokenCount` (number): 当前 token 数
- `limit` (number): token 限制
- `recommendation` (string): 建议操作

**示例**：
```javascript
const status = await booster.getStatus();
if (status.usagePercent > 80) {
  console.log('建议压缩上下文');
}
```

---

## 📝 使用示例

### 示例 1：压缩上下文

```javascript
const booster = require('context-booster');

// 当 context 使用率超过 70% 时压缩
const status = await booster.getStatus();
if (status.usagePercent > 70) {
  const result = await booster.enhance({
    mode: 'compress',
    preserveKeyPoints: true
  });
  console.log(`压缩后大小：${result.compressedSize}`);
}
```

### 示例 2：检索历史对话

```javascript
// 检索关于「技能迭代」的历史对话
const memories = await booster.retrieve('技能迭代', {
  limit: 5
});

memories.forEach(memory => {
  console.log(`[${memory.date}] ${memory.summary}`);
});
```

### 示例 3：恢复长程任务

```javascript
// 恢复昨天未完成的任务
const context = await booster.enhance({
  mode: 'enrich',
  preserveKeyPoints: true
});

// 补充项目背景
const projectInfo = await booster.retrieve('元技能系统项目');
console.log('项目背景：', projectInfo);
```

### 示例 4：预测下一步上下文

```javascript
// 预测下一步可能需要的上下文
const prediction = await booster.predictNextContext();
console.log('可能需要：', prediction.suggestedContexts);
```

---

## ⚠️ 注意事项

1. **压缩比例**：过高的压缩比例可能丢失重要信息
2. **记忆检索**：检索结果需要人工验证准确性
3. **性能影响**：频繁压缩可能影响响应速度

---

## 🐛 故障排除

### 问题 1：压缩后信息丢失

**原因**：压缩比例过高或策略不当

**解决**：
- 降低压缩比例
- 调整 preserveKeyPoints 设置
- 手动检查压缩结果

### 问题 2：检索结果不相关

**原因**：查询词不明确或记忆索引问题

**解决**：
- 优化查询词
- 添加标签过滤
- 检查记忆索引状态

---

## 📚 相关资源

- [VERSION_HISTORY.md](./VERSION_HISTORY.md) - 版本历史
- [TESTING-PROTOCOL.md](../testing/TESTING-PROTOCOL.md) - 测试协议

---

## 📄 许可证

MIT License

---

**维护者**：王的奴隶 · 严谨专业版  
**最后更新**：2026-03-30  
**问题反馈**：GitHub Issues
