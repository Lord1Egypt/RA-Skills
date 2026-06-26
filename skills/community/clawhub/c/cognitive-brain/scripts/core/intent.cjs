#!/usr/bin/env node
/**
 * Cognitive Brain - 意图识别模块
 * 识别用户输入的意图
 */

// 意图分类
const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('intent');
const INTENTS = {
  // 信息类
  QUESTION: {
    name: 'question',
    patterns: [
      /^(什么|怎么|为什么|如何|哪|谁|多少|几)/,
      /\?|？$/,
      /(是什么|怎么做|为什么|如何)/
    ],
    description: '询问信息'
  },

  REQUEST: {
    name: 'request',
    patterns: [
      /^(帮我|请|麻烦|能|可以|能否)/,
      /(做|完成|执行|处理)/
    ],
    description: '请求帮助'
  },

  // 动作类
  COMMAND: {
    name: 'command',
    patterns: [
      /^(打开|关闭|启动|停止|删除|创建|设置)/,
      /^\/\w+/
    ],
    description: '执行命令'
  },

  SEARCH: {
    name: 'search',
    patterns: [
      /(搜索|查找|找一下|查一下|搜索一下)/,
      /(有没有|是否存在)/
    ],
    description: '搜索查询'
  },

  // 交互类
  GREETING: {
    name: 'greeting',
    patterns: [
      /^(你好|hi|hello|hey|早上好|晚上好)/i,
      /(在吗|在不在)/
    ],
    description: '问候'
  },

  FEEDBACK: {
    name: 'feedback',
    patterns: [
      /(谢谢|感谢|太好了|很好|不错|棒)/,
      /(不对|错了|不是|糟糕|差)/
    ],
    description: '反馈评价'
  },

  CORRECTION: {
    name: 'correction',
    patterns: [
      /(不对|错了|不是|其实|实际)/,
      /(应该是|其实是|我意思是)/
    ],
    description: '纠正信息'
  },

  // 记忆类
  REMEMBER: {
    name: 'remember',
    patterns: [
      /(记住|记得|别忘|记下来)/,
      /(这个很重要|保存这个)/
    ],
    description: '要求记忆'
  },

  RECALL: {
    name: 'recall',
    patterns: [
      /(还记得|记得吗|之前说过|上次)/,
      /(回忆|想起来)/
    ],
    description: '回忆往事'
  },

  // 社交类
  CHITCHAT: {
    name: 'chitchat',
    patterns: [
      /^(哈哈|呵呵|嗯|哦|啊)/,
      /(怎么样|如何|聊聊天)/
    ],
    description: '闲聊'
  },

  UNKNOWN: {
    name: 'unknown',
    patterns: [],
    description: '未知意图'
  }
};

// 槽位提取规则
const SLOT_PATTERNS = {
  entity: [
    /叫(.+?)的/,
    /(这个|那个)\s*(\S+)/,
    /(项目|文件|文件夹|配置)\s*[:：]?\s*(\S+)/
  ],
  time: [
    /(今天|明天|昨天|后天|前天)/,
    /(\d{1,2})[点时](\d{1,2})?分?/,
    /(早上|中午|下午|晚上|凌晨)/
  ],
  location: [
    /在(.+?)(里|上|中)/,
    /(这里|那里|本地|远程)/
  ],
  action: [
    /(做|完成|执行|处理|删除|创建|修改|查看|搜索)(.+?)/
  ]
};

/**
 * 识别意图
 */
function recognizeIntent(text) {
  const results = [];

  for (const [key, intent] of Object.entries(INTENTS)) {
    if (key === 'UNKNOWN') continue;

    let score = 0;
    let matchedPatterns = [];

    for (const pattern of intent.patterns) {
      if (pattern.test(text)) {
        score += 0.3;
        matchedPatterns.push(pattern.toString());
      }
    }

    if (score > 0) {
      results.push({
        intent: intent.name,
        confidence: Math.min(score, 1),
        description: intent.description,
        matchedPatterns
      });
    }
  }

  // 排序并返回最佳匹配
  results.sort((a, b) => b.confidence - a.confidence);

  if (results.length === 0) {
    return {
      intent: 'unknown',
      confidence: 0,
      description: '未知意图',
      slots: extractSlots(text)
    };
  }

  return {
    ...results[0],
    slots: extractSlots(text),
    alternatives: results.slice(1, 3)
  };
}

/**
 * 提取槽位
 */
function extractSlots(text) {
  const slots = {};

  for (const [slotName, patterns] of Object.entries(SLOT_PATTERNS)) {
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        slots[slotName] = match[1] || match[0];
        break;
      }
    }
  }

  return slots;
}

/**
 * 批量识别
 */
function recognizeBatch(texts) {
  return texts.map(text => ({
    text,
    ...recognizeIntent(text)
  }));
}

/**
 * 获取意图统计
 */
function getIntentStats(history) {
  const stats = {};

  for (const item of history) {
    const intent = item.intent || 'unknown';
    stats[intent] = (stats[intent] || 0) + 1;
  }

  return Object.entries(stats)
    .sort((a, b) => b[1] - a[1])
    .map(([intent, count]) => ({ intent, count }));
}

/**
 * 从文本推断优先级
 */
function inferPriority(text) {
  const urgentPatterns = [
    /(紧急|着急|马上|立刻|快点|急)/,
    /(重要|关键|必须|一定要)/
  ];

  const lowPatterns = [
    /(有空|方便|不急|慢慢)/,
    /(顺便|闲暇)/
  ];

  for (const pattern of urgentPatterns) {
    if (pattern.test(text)) return 'high';
  }

  for (const pattern of lowPatterns) {
    if (pattern.test(text)) return 'low';
  }

  return 'normal';
}

/**
 * 从文本推断情感
 */
function inferSentiment(text) {
  const positivePatterns = [
    /(谢谢|感谢|太好了|很好|不错|棒|喜欢|开心)/,
    /(完美|优秀|太棒了|赞)/
  ];

  const negativePatterns = [
    /(不对|错了|糟糕|差|讨厌|烦|生气)/,
    /(失望|不满|抱怨)/
  ];

  const neutralPatterns = [
    /^(好的|嗯|哦|行|可以)/
  ];

  for (const pattern of positivePatterns) {
    if (pattern.test(text)) return 'positive';
  }

  for (const pattern of negativePatterns) {
    if (pattern.test(text)) return 'negative';
  }

  for (const pattern of neutralPatterns) {
    if (pattern.test(text)) return 'neutral';
  }

  return 'neutral';
}

// ===== 主函数 =====
async function main() {
  const text = process.argv.slice(2).join(' ');

  if (!text) {
    console.log(`
意图识别模块

用法:
  node intent.cjs "用户输入文本"

示例:
  node intent.cjs "帮我搜索一下天气"
  node intent.cjs "你还记得我上次说的项目吗"
  node intent.cjs "今天要做什么"
    `);
    return;
  }

  const result = recognizeIntent(text);

  console.log('📝 输入:', text);
  console.log('\n🎯 识别结果:');
  console.log(`   意图: ${result.intent}`);
  console.log(`   置信度: ${(result.confidence * 100).toFixed(1)}%`);
  console.log(`   描述: ${result.description}`);

  if (Object.keys(result.slots).length > 0) {
    console.log('\n📦 槽位:');
    for (const [key, value] of Object.entries(result.slots)) {
      console.log(`   ${key}: ${value}`);
    }
  }

  console.log('\n📊 其他推断:');
  console.log(`   优先级: ${inferPriority(text)}`);
  console.log(`   情感: ${inferSentiment(text)}`);

  if (result.alternatives && result.alternatives.length > 0) {
    console.log('\n🔄 备选意图:');
    result.alternatives.forEach(alt => {
      console.log(`   ${alt.intent} (${(alt.confidence * 100).toFixed(1)}%)`);
    });
  }
}

main();

// 导出模块
module.exports = {
  recognizeIntent,
  recognizeBatch,
  inferPriority,
  inferSentiment,
  INTENTS
};
