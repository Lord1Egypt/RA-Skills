# AI Article Detector 🤖

一个强大的 AI 文章检测 Skill，可以分析任何网页文章，判断其是否由 AI 生成。

**输入**: 文章链接  
**输出**: 0-100 的 AI 写作概率分数

```bash
$ node ai-article-detector.js "https://www.xiaohongshu.com/explore/xxx"

====================================
📊 AI 文章检测结果
====================================

🎯 AI 写作概率: 75/100
💭 较高概率是 AI 生成（70-90% 确定）

📈 各维度分数:
  • 词汇多样性: 85
  • 句子变化: 45
  • 段落规律性: 78
  • AI 模板词: 88
  • 文本熵: 35
  • 情感强度: 62
  • 被动语态: 68
  • 个性化标记: 82
```

## 快速开始

### 安装
```bash
cd ~/.openclaw/skills/ai-article-detector
npm install
```

### 使用
```bash
node ai-article-detector.js "https://example.com/article"
```

## 工作原理

采用 **8 维度评分系统**，综合分析：

1. **词汇多样性** - 词汇重复度
2. **句子变化** - 句子长度多样性
3. **段落规律性** - 段落长度统一度
4. **AI 模板词** - 常见转折词频率 ⭐
5. **文本熵** - 文本随机性
6. **情感强度** - 极端词汇使用
7. **被动语态** - 被动表达比例
8. **个性化标记** - 表情、特殊符号使用

## 分数解释

- **80-100**: 极高概率是 AI（95%+ 确定）
- **60-79**: 较高概率是 AI（70-90% 确定）
- **40-59**: 中等概率是 AI（50-70% 确定）
- **20-39**: 较低概率是 AI（20-50% 确定）
- **0-19**: 极低概率是 AI（人类写作风格）

## 特点

✅ **多维度分析** - 8 个独立特征维度  
✅ **加权评分** - 基于可靠性的权重分配  
✅ **隐私保护** - 本地分析，无数据上传  
✅ **快速检测** - 秒级响应  
✅ **易于集成** - Node.js + JSON 输出  

## 限制

⚠️ 这是基于统计特征的估计，不是 100% 准确  
⚠️ 高级 AI 模型（Claude、GPT-4）的文章可能绕过检测  
⚠️ 当前优化语言：中文  
⚠️ 建议配合人工审阅使用  

## 与 OpenClaw 集成

```javascript
import AIArticleDetector from './ai-article-detector.js';

const detector = new AIArticleDetector();
const result = await detector.detect('https://example.com/article');

console.log(`AI 概率: ${result.aiProbability}/100`);
```

## 靓仔的适用场景

✅ 审核用户投稿  
✅ 竞争对手内容分析  
✅ 原创度评估  
✅ 内容质量检查  

❌ 法律诉讼证据（法律权重不足）  
❌ 实时作弊检测  

---

**版本**: 1.0.0  
**更新**: 2026-03-10
