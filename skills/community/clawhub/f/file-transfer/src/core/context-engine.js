/**
 * Context Engine - 智能上下文分析引擎
 * 
 * 负责分析文件传输的上下文信息，包括：
 * 1. 聊天环境分析（群聊/私聊/频道）
 * 2. 用户意图识别（分享/备份/协作）
 * 3. 文件类型智能匹配
 * 4. 传输目标智能推荐
 * 
 * @module core/context-engine
 */

/**
 * 上下文分析结果
 * @typedef {Object} ContextAnalysis
 * @property {string} scenario - 场景类型：'share'|'backup'|'collaborate'|'archive'
 * @property {string} urgency - 紧急程度：'low'|'medium'|'high'|'critical'
 * @property {string[]} recommendedTargets - 推荐传输目标
 * @property {Object} metadata - 附加元数据
 * @property {boolean} isGroupChat - 是否群聊
 * @property {string} chatType - 聊天类型：'private'|'group'|'channel'
 * @property {string} fileCategory - 文件分类：'document'|'image'|'video'|'archive'|'code'
 */

/**
 * 文件传输上下文
 * @typedef {Object} TransferContext
 * @property {string} filePath - 文件路径
 * @property {string} fileName - 文件名
 * @property {number} fileSize - 文件大小（字节）
 * @property {string} fileType - 文件MIME类型
 * @property {string} caption - 文件描述
 * @property {Object} chatInfo - 聊天信息
 * @property {Object} userInfo - 用户信息
 * @property {Object} channelInfo - 通道信息
 * @property {string[]} history - 历史消息上下文
 */

/**
 * 智能上下文分析引擎
 */
export class ContextEngine {
  /**
   * 创建上下文引擎实例
   * @param {Object} config - 引擎配置
   */
  constructor(config = {}) {
    this.config = {
      enableAI: config.enableAI ?? false,
      maxHistoryLength: config.maxHistoryLength ?? 10,
      scenarioWeights: config.scenarioWeights ?? {
        share: 1.0,
        backup: 0.8,
        collaborate: 1.2,
        archive: 0.6
      },
      ...config
    };

    // 文件类型到场景的映射
    this.fileTypeToScenario = {
      // 文档类
      'application/pdf': 'share',
      'application/msword': 'collaborate',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'collaborate',
      'text/plain': 'share',
      'text/markdown': 'collaborate',
      
      // 图片类
      'image/jpeg': 'share',
      'image/png': 'share',
      'image/gif': 'share',
      'image/svg+xml': 'collaborate',
      
      // 视频类
      'video/mp4': 'share',
      'video/quicktime': 'share',
      
      // 压缩包
      'application/zip': 'archive',
      'application/x-rar-compressed': 'archive',
      'application/x-tar': 'archive',
      
      // 代码
      'text/javascript': 'collaborate',
      'application/json': 'collaborate',
      'text/x-python': 'collaborate'
    };

    // 场景优先级规则
    this.scenarioRules = {
      share: {
        urgency: 'medium',
        recommendedTargets: ['current_chat', 'related_chats'],
        notificationLevel: 'normal'
      },
      backup: {
        urgency: 'low',
        recommendedTargets: ['backup_folder', 'cloud_storage'],
        notificationLevel: 'silent'
      },
      collaborate: {
        urgency: 'high',
        recommendedTargets: ['collaborators', 'team_chat'],
        notificationLevel: 'important'
      },
      archive: {
        urgency: 'low',
        recommendedTargets: ['archive_folder', 'long_term_storage'],
        notificationLevel: 'silent'
      }
    };

    // 文件分类映射
    this.fileCategories = {
      document: ['application/pdf', 'application/msword', 'text/plain', 'text/markdown'],
      image: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
      video: ['video/mp4', 'video/quicktime'],
      archive: ['application/zip', 'application/x-rar-compressed', 'application/x-tar'],
      code: ['text/javascript', 'application/json', 'text/x-python']
    };
  }

  /**
   * 确定传输场景
   * @private
   */
  determineScenario(context) {
    // 1. 基于文件类型
    const fileBasedScenario = this.fileTypeToScenario[context.fileType];
    if (fileBasedScenario) {
      return fileBasedScenario;
    }
    
    // 2. 基于聊天类型
    if (context.chatInfo?.isGroupChat) {
      return 'collaborate';
    }
    
    // 3. 基于文件大小
    if (context.fileSize > 50 * 1024 * 1024) { // 大于50MB
      return 'archive';
    }
    
    // 4. 默认场景
    return 'share';
  }

  /**
   * 确定紧急程度
   * @private
   */
  determineUrgency(context, scenario) {
    const rule = this.scenarioRules[scenario];
    if (rule) {
      return rule.urgency;
    }
    
    // 基于文件大小和聊天类型
    if (context.fileSize > 100 * 1024 * 1024) { // 大于100MB
      return 'high';
    }
    
    if (context.chatInfo?.isGroupChat) {
      return 'medium';
    }
    
    return 'low';
  }

  /**
   * 确定推荐目标
   * @private
   */
  determineTargets(context, scenario) {
    const rule = this.scenarioRules[scenario];
    if (rule) {
      return rule.recommendedTargets;
    }
    
    // 默认目标
    if (context.chatInfo?.isGroupChat) {
      return ['current_chat', 'group_members'];
    }
    
    return ['current_chat'];
  }

  /**
   * 分类文件类型
   * @private
   */
  categorizeFile(fileType) {
    for (const [category, types] of Object.entries(this.fileCategories)) {
      if (types.includes(fileType)) {
        return category;
      }
    }
    
    return 'document'; // 默认分类
  }

  /**
   * 计算置信度
   * @private
   */
  calculateConfidence(context, scenario) {
    let confidence = 0.5; // 基础置信度
    
    // 有明确的文件类型映射
    if (this.fileTypeToScenario[context.fileType] === scenario) {
      confidence += 0.2;
    }
    
    // 有聊天信息
    if (context.chatInfo) {
      confidence += 0.1;
    }
    
    // 有文件描述
    if (context.caption && context.caption.trim().length > 0) {
      confidence += 0.1;
    }
    
    // 有历史上下文
    if (context.history && context.history.length > 0) {
      confidence += 0.1;
    }
    
    return Math.min(confidence, 1.0);
  }

  /**
   * 提取用户意图
   * @private
   */
  extractUserIntent(context) {
    const caption = context.caption || '';
    const history = context.history || [];
    
    // 简单的关键词匹配
    const keywords = {
      share: ['分享', '发送', '给', '转发', 'share', 'send'],
      backup: ['备份', '保存', '存储', 'backup', 'save'],
      collaborate: ['协作', '合作', '编辑', '修改', 'collaborate', 'edit'],
      archive: ['归档', '存档', '整理', 'archive', 'organize']
    };
    
    const allText = [caption, ...history].join(' ').toLowerCase();
    
    for (const [intent, words] of Object.entries(keywords)) {
      for (const word of words) {
        if (allText.includes(word.toLowerCase())) {
          return intent;
        }
      }
    }
    
    return 'unknown';
  }

  /**
   * 获取降级分析结果
   * @private
   */
  getFallbackAnalysis(context) {
    return {
      scenario: 'share',
      urgency: 'medium',
      recommendedTargets: ['current_chat'],
      metadata: {
        fileType: context.fileType,
        fileSize: context.fileSize,
        fileName: context.fileName,
        isFallback: true
      },
      isGroupChat: false,
      chatType: 'private',
      fileCategory: this.categorizeFile(context.fileType),
      timestamp: new Date().toISOString(),
      confidence: 0.5
    };
  }

  /**
   * 分析传输上下文
   * @param {TransferContext} context - 传输上下文
   * @returns {Promise<ContextAnalysis>} 上下文分析结果
   */
  async analyzeContext(context) {
    try {
      // 1. 确定场景
      const scenario = this.determineScenario(context);
      
      // 2. 确定紧急程度
      const urgency = this.determineUrgency(context, scenario);
      
      // 3. 确定推荐目标
      const recommendedTargets = this.determineTargets(context, scenario);
      
      // 4. 确定文件分类
      const fileCategory = this.categorizeFile(context.fileType);
      
      // 5. 计算置信度
      const confidence = this.calculateConfidence(context, scenario);
      
      // 6. 构建分析结果
      const analysis = {
        scenario,
        urgency,
        recommendedTargets,
        metadata: {
          fileType: context.fileType,
          fileSize: context.fileSize,
          fileName: context.fileName,
          chatType: context.chatInfo?.chatType || 'private',
          userIntent: this.extractUserIntent(context)
        },
        isGroupChat: context.chatInfo?.isGroupChat || false,
        chatType: context.chatInfo?.chatType || 'private',
        fileCategory,
        timestamp: new Date().toISOString(),
        confidence
      };
      
      return analysis;
    } catch (error) {
      console.warn(`Context analysis failed: ${error.message}, using fallback`);
      return this.getFallbackAnalysis(context);
    }
  }

  /**
   * 获取引擎状态
   * @returns {Object} 引擎状态信息
   */
  getStatus() {
    return {
      version: '0.2.0-beta',
      config: this.config,
      scenarios: Object.keys(this.scenarioRules),
      fileTypes: Object.keys(this.fileTypeToScenario),
      isOperational: true,
      lastAnalysis: new Date().toISOString()
    };
  }
}

export default ContextEngine;