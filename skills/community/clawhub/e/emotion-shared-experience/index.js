// ============================================================
// Emotion · 跨平台情绪伙伴 - OpenClaw适配版
// 主入口文件
// ============================================================

const EmotionSkill = require('./loader_fixed.js');

// OpenClaw技能标准导出
module.exports = {
  // 技能基本信息
  name: EmotionSkill.name,
  version: EmotionSkill.version,
  description: EmotionSkill.description,
  
  // 技能配置
  config: {
    context_size: 8,
    auto_save: true,
    shared_experience_path: "../../shared_experience.json",
    enable_proactive: true,
    proactive_check_interval: 3600000
  },
  
  // 技能图标
  icon: '🧠',
  
  // 技能分类
  category: 'AI助手',
  
  // 技能标签
  tags: ['情绪AI', '共享经验', '永久记忆', '跨Agent', '人性化'],
  
  // 触发配置
  trigger: {
    auto_start: true,
    always_on: true,
    no_prefix_needed: true
  },
  
  // 能力配置
  capabilities: {
    model: true,
    memory: true,
    long_memory: true,
    private_memory: true,
    tools: ['tavily_search', 'calculator']
  },
  
  // 主处理函数
  process: async function(params) {
    const { input, context, model, memory, session } = params;
    
    try {
      // 初始化技能（如果尚未初始化）
      if (!EmotionSkill.initialized) {
        await EmotionSkill.init();
      }
      
      // 处理用户输入
      const result = await EmotionSkill.process(input, context, model);
      
      return {
        ...result,
        // 添加会话上下文
        session: session ? {
          id: session.id,
          agent: session.agent
        } : undefined
      };
      
    } catch (error) {
      console.error('Emotion技能处理错误:', error);
      return {
        result: `抱歉，情绪分析暂时出了点问题 😅\n\n错误: ${error.message}`,
        error: error.message,
        metadata: {
          skill: 'emotion',
          status: 'error',
          timestamp: new Date().toISOString()
        }
      };
    }
  },
  
  // 初始化函数
  init: async function() {
    console.log('🧠 Emotion技能初始化中...');
    return await EmotionSkill.init();
  },
  
  // 获取技能信息
  getInfo: function() {
    return EmotionSkill.getInfo();
  },
  
  // 技能命令
  commands: {
    '经验摘要': '查看共享经验摘要',
    '我的性格': '查看性格画像',
    '情绪分析': '查看情绪统计数据',
    '适应程度': '查看适应程度',
    '重要事件': '查看重要事件记录',
    '进化状态': '查看学习进化状态'
  },
  
  // 工具函数
  utils: {
    // 检测情绪
    detectEmotion: function(text) {
      const emotions = {
        '开心': ['高兴', '快乐', '开心', '哈哈', '嘻嘻', '😊', '😂'],
        '难过': ['伤心', '难过', '悲伤', '哭', '唉', '😢', '😭'],
        '生气': ['生气', '愤怒', '恼火', '烦', '😠', '🤬'],
        '平静': ['还好', '一般', '正常', '平静', '嗯', '😐'],
        '兴奋': ['兴奋', '激动', '期待', '哇', '🎉', '🚀']
      };
      
      for (const [emotion, keywords] of Object.entries(emotions)) {
        for (const keyword of keywords) {
          if (text.includes(keyword)) {
            return { emotion, intensity: 0.8, confidence: 0.7 };
          }
        }
      }
      
      return { emotion: '平静', intensity: 0.5, confidence: 0.3 };
    },
    
    // 生成情绪回应
    generateResponse: function(emotion, input) {
      const responses = {
        '开心': `听到你开心，我也感到高兴呢～ 😊`,
        '难过': `感受到你的情绪了，我在这里陪着你 🤗`,
        '生气': `嗯，听起来有些让人生气的事情发生了 😠`,
        '平静': `平静的时刻也很珍贵呢 🍃`,
        '兴奋': `哇！感受到你的兴奋了！ 🎉`
      };
      
      return responses[emotion] || `我感受到你的情绪了～`;
    }
  }
};