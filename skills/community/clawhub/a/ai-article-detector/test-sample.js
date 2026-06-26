#!/usr/bin/env node

/**
 * 测试脚本 - 本地样本测试
 */

import AIArticleDetector from './ai-article-detector.js';

// 样本文章（模拟 AI 生成的文章）
const aiSample = `
首先，我们需要了解什么是人工智能。其次，让我们探讨人工智能的应用。最后，我们将总结人工智能的未来。

人工智能是一个快速发展的领域。值得注意的是，人工智能已经被应用于许多行业。此外，人工智能还可以用于医疗、教育和交通等领域。另外，人工智能的发展前景非常广阔。

总的来说，人工智能是未来的发展方向。综合来看，我们需要不断学习和适应人工智能的发展。需要指出的是，人工智能的发展离不开各行各业的支持。

因此，我们应该积极拥抱人工智能的发展。所以，我们需要加强人工智能的研究和应用。显而易见，人工智能将会改变我们的生活方式。不容忽视，人工智能的影响是深远的。

毫无疑问，人工智能是一个重要的技术。众所周知，人工智能已经取得了显著的成就。一方面，人工智能可以提高工作效率。另一方面，人工智能也存在一些风险和挑战。

综合以上分析，我们可以得出结论：人工智能的发展是必然的。总体而言，我们应该积极应对人工智能带来的机遇和挑战。
`;

// 样本文章（模拟人类写的文章）
const humanSample = `
嘿，我今天想和大家分享一下我用 AI 工具的真实体验 😂

说实话，刚开始用 ChatGPT 的时候，我被震撼到了。但用了一段时间后，我发现它其实有不少局限性。最大的问题？**它写出来的东西特别"假"** 🎭

为什么说假呢？你看啊：
- 那些转折词出现得超级频繁（"首先...其次...最后"）
- 句子长度特别整齐划一
- 永远不会打错字，也不会有方言
- 特别喜欢用被动语态

对比我身边朋友的文章，他们经常会：写一些"嗯...不太对啊"的感觉，用大量表情符号 😅💯，甚至会有一些小错字。这些恰恰证明了**人味儿**的存在！

所以我现在的策略是：AI 帮我快速生成框架，但我一定要加上真实案例、个人观点，甚至一些"人类才会犯的小错误" 🎯

你们有没有类似的感受？欢迎在评论区吐槽！💬
`;

const detector = new AIArticleDetector();

console.log('🧪 AI Article Detector - 测试');
console.log('='.repeat(50) + '\n');

// 测试 1: AI 样本
console.log('📝 测试 1: AI 生成的文章样本');
console.log('-'.repeat(50));
const aiResult = detector.analyzeArticle(aiSample);
console.log(`🎯 AI 概率: ${aiResult.aiProbability}/100`);
console.log(`💭 ${aiResult.interpretation}\n`);

// 显示各维度分数
console.log('📈 各维度分数:');
Object.entries(aiResult.details).forEach(([key, score]) => {
  const bars = '█'.repeat(Math.floor(score / 10));
  console.log(`  ${key.padEnd(25)} ${score.toString().padStart(3)}/100 ${bars}`);
});
console.log('\n');

// 测试 2: 人类样本
console.log('📝 测试 2: 人类写的文章样本');
console.log('-'.repeat(50));
const humanResult = detector.analyzeArticle(humanSample);
console.log(`🎯 AI 概率: ${humanResult.aiProbability}/100`);
console.log(`💭 ${humanResult.interpretation}\n`);

console.log('📈 各维度分数:');
Object.entries(humanResult.details).forEach(([key, score]) => {
  const bars = '█'.repeat(Math.floor(score / 10));
  console.log(`  ${key.padEnd(25)} ${score.toString().padStart(3)}/100 ${bars}`);
});
console.log('\n');

// 对比分析
console.log('📊 对比分析');
console.log('='.repeat(50));
console.log(`AI 样本: ${aiResult.aiProbability}/100 ✓ ${aiResult.aiProbability > 60 ? '✅ 正确' : '❌ 错误'}`);
console.log(`人类样本: ${humanResult.aiProbability}/100 ✓ ${humanResult.aiProbability < 40 ? '✅ 正确' : '❌ 错误'}`);
console.log('\n✅ 测试完成！');
