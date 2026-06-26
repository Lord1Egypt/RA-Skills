# AutoThink Skill

智能 thinking 级别自动切换器。

## 功能

- **自动评估** 消息复杂度，推荐合适的 thinking 级别 (low/medium/high)
- **手动覆盖** 通过前缀快速指定：
  - `-h` 或 `--high` → 强制 high
  - `-l` 或 `--low` → 强制 low  
  - `-m` 或 `--medium` → 强制 medium
- **透明集成** 与 OpenClaw Agent 配合工作

## 快速开始

### 安装

```bash
cd C:\Users\Ponker\.openclaw\workspace\skills\autothink-1.0.0
npm install
```

### 注册到 OpenClaw

```bash
# 方式1: 使用 clawhub (推荐)
clawhub register autothink

# 方式2: 手动复制到 npm 全局目录
# (略)
```

## 使用方式

### 手动模式（方案四）

在你的消息前加前缀：

```
-h 帮我设计一个分布式电商系统
-l 今天星期几
-m 详细解释一下这个错误
```

前缀会被自动移除，只发送实际内容给 agent。

### 自动模式（方案一）

与 `openclaw agent` 配合使用：

```bash
# 自动分析并设置 thinking 级别后处理消息
autothink-process "你的消息内容"
```

或者在脚本中使用：

```javascript
const { AutoThinkEngine } = require('autothink');

const engine = new AutoThinkEngine();
const result = engine.processMessage("帮我分析一下这个复杂的系统架构");
console.log(result.thinkingLevel); // 输出: high
```

## 复杂度评估算法

AutoThink 通过多个维度综合评分：

| 因素 | 权重 |
|------|------|
| 消息长度 (>500字符 +3, >200 +2) | 长度反映信息密度 |
| 复杂关键词 (分析、设计、架构等) | +2 |
| 技术关键词 (代码、系统、API等) | +1 |
| 问号数量 (多个问题) | +1 |
| 代码块 (```) | +2 |
| 多行文本 (>5行) | +1 |

总分 ≥4 → **high**  
总分 2-3 → **medium**  
总分 ≤1 → **low**

## 作为 OpenClaw Hook 集成

要实现完全透明的自动切换，需要在 OpenClaw 中注册 `message_preprocessor` hook：

```javascript
// ~/.openclaw/plugins/autothink-hook.js
const { AutoThinkEngine } = require('autothink');
const engine = new AutoThinkEngine();

module.exports = {
  name: 'autothink-hook',
  hook: 'message_preprocessor',
  async process(message, context) {
    const analysis = engine.analyzeComplexity(message);
    context.thinking = analysis.level;
    return message; // 可修改消息内容
  }
};
```

然后在 OpenClaw 配置中启用：

```json
{
  "plugins": {
    "autothink-hook": {
      "enabled": true
    }
  }
}
```

**注意**: Hook 系统需要 OpenClaw v2026.3.13+ 支持。

## 开发

```bash
# 运行测试
node src/index.js

# 构建（如果有需要）
npm run build
```

## License

MIT
