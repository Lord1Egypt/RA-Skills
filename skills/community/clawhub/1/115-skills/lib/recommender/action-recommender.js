/**
 * 主动推荐系统
 * 
 * 根据用户操作场景，主动推荐下一步操作
 */

class ActionRecommender {
  constructor() {
    // 场景推荐规则
    this.rules = {
      // 容量查询后推荐清理
      'status': [
        {
          action: 'clean',
          text: '🧹 清理空间',
          reason: '优化存储空间',
          priority: 1
        },
        {
          action: 'files',
          text: '📁 查看文件',
          reason: '浏览文件列表',
          priority: 2
        },
        {
          action: 'organize',
          text: '🤖 智能整理',
          reason: '自动分类文件',
          priority: 3
        }
      ],
      
      // 文件浏览后推荐操作
      'files': [
        {
          action: 'search',
          text: '🔍 搜索文件',
          reason: '快速查找文件',
          priority: 1
        },
        {
          action: 'download',
          text: '⬇️ 批量下载',
          reason: '下载选中文件',
          priority: 2
        },
        {
          action: 'organize',
          text: '🤖 整理文件',
          reason: '分类整理当前目录',
          priority: 3
        },
        {
          action: 'transfer',
          text: '📦 批量转存',
          reason: '转存到其他目录',
          priority: 4
        },
        {
          action: 'status',
          text: '📊 查看容量',
          reason: '了解空间使用情况',
          priority: 5
        }
      ],
      
      // 搜索后推荐批量操作
      'search': [
        {
          action: 'select_all',
          text: '✓ 全选',
          reason: '选中所有搜索结果',
          priority: 1
        },
        {
          action: 'download',
          text: '⬇️ 批量下载',
          reason: '下载搜索结果',
          priority: 2
        },
        {
          action: 'transfer',
          text: '📦 批量转存',
          reason: '转存到其他目录',
          priority: 3
        }
      ],
      
      // 下载完成后推荐整理
      'download': [
        {
          action: 'organize',
          text: '🤖 整理下载',
          reason: '分类整理下载文件',
          priority: 1
        },
        {
          action: 'files',
          text: '📁 查看文件',
          reason: '浏览下载目录',
          priority: 2
        },
        {
          action: 'share',
          text: '🔗 分享文件',
          reason: '分享给好友',
          priority: 3
        }
      ],
      
      // 整理后推荐清理
      'organize': [
        {
          action: 'clean',
          text: '🧹 清理建议',
          reason: '进一步优化空间',
          priority: 1
        },
        {
          action: 'files',
          text: '📁 查看结果',
          reason: '查看整理结果',
          priority: 2
        },
        {
          action: 'status',
          text: '📊 查看容量',
          reason: '查看空间变化',
          priority: 3
        }
      ],
      
      // 清理后推荐确认
      'clean': [
        {
          action: 'clean_confirm',
          text: '✅ 确认清理',
          reason: '执行清理操作',
          priority: 1
        },
        {
          action: 'files',
          text: '📁 查看文件',
          reason: '浏览文件列表',
          priority: 2
        },
        {
          action: 'status',
          text: '📊 查看容量',
          reason: '查看清理效果',
          priority: 3
        }
      ],
      
      // 分享后推荐管理
      'share': [
        {
          action: 'share_list',
          text: '📋 我的分享',
          reason: '查看分享列表',
          priority: 1
        },
        {
          action: 'share_update',
          text: '⏰ 修改时长',
          reason: '调整分享有效期',
          priority: 2
        },
        {
          action: 'files',
          text: '📁 返回文件',
          reason: '继续浏览文件',
          priority: 3
        }
      ],
      
      // 转存后推荐查看
      'transfer': [
        {
          action: 'files',
          text: '📁 查看文件',
          reason: '查看转存结果',
          priority: 1
        },
        {
          action: 'organize',
          text: '🤖 整理文件',
          reason: '分类整理转存文件',
          priority: 2
        },
        {
          action: 'share',
          text: '🔗 分享文件',
          reason: '分享给好友',
          priority: 3
        }
      ],
      
      // 登录后推荐操作
      'login': [
        {
          action: 'files',
          text: '📁 查看文件',
          reason: '浏览文件列表',
          priority: 1
        },
        {
          action: 'status',
          text: '📊 查看容量',
          reason: '了解空间使用情况',
          priority: 2
        },
        {
          action: 'search',
          text: '🔍 搜索文件',
          reason: '快速查找文件',
          priority: 3
        }
      ],
      
      // 删除后推荐确认
      'delete': [
        {
          action: 'files',
          text: '📁 返回',
          reason: '返回文件列表',
          priority: 1
        },
        {
          action: 'recycle',
          text: '🗑️ 回收站',
          reason: '查看回收站',
          priority: 2
        },
        {
          action: 'status',
          text: '📊 查看容量',
          reason: '查看释放空间',
          priority: 3
        }
      ]
    };

    // 快捷词到命令的映射
    this.shortcutMap = {
      '容量': 'status',
      '空间': 'status',
      '文件': 'files',
      '搜索': 'search',
      '下载': 'download',
      '整理': 'organize',
      '清理': 'clean',
      '分享': 'share',
      '转存': 'transfer',
      '登录': 'login',
      '删除': 'delete'
    };
  }

  /**
   * 根据当前动作推荐下一步
   * @param {string} action - 当前动作
   * @param {Object} context - 上下文信息（可选）
   * @returns {Array} 推荐列表
   */
  recommend(action, context = null) {
    // 标准化动作
    const normalizedAction = this._normalizeAction(action);
    
    // 获取推荐规则
    const rules = this.rules[normalizedAction];
    
    if (!rules) {
      return this._getDefaultRecommendations();
    }
    
    // 根据上下文调整推荐
    let recommendations = [...rules];
    
    if (context) {
      recommendations = this._adjustByContext(recommendations, context);
    }
    
    // 按优先级排序
    recommendations.sort((a, b) => a.priority - b.priority);
    
    // 返回前 3 个推荐
    return recommendations.slice(0, 3);
  }

  /**
   * 标准化动作
   * @param {string} action - 动作
   * @returns {string} 标准化动作
   */
  _normalizeAction(action) {
    if (!action) return 'default';
    
    // 检查是否是快捷词
    const normalized = this.shortcutMap[action];
    if (normalized) {
      return normalized;
    }
    
    return action.toLowerCase();
  }

  /**
   * 根据上下文调整推荐
   * @param {Array} recommendations - 推荐列表
   * @param {Object} context - 上下文
   * @returns {Array} 调整后的推荐
   */
  _adjustByContext(recommendations, context) {
    // 如果有选中文件，优先推荐批量操作
    if (context.selectedCount > 0) {
      const batchActions = ['download', 'transfer', 'delete', 'share'];
      
      recommendations.forEach(rec => {
        if (batchActions.includes(rec.action)) {
          rec.priority -= 1; // 提升优先级
          rec.reason = `操作选中的 ${context.selectedCount} 个文件`;
        }
      });
    }
    
    // 如果空间使用率高，优先推荐清理
    if (context.usageRate > 90) {
      const cleanRec = recommendations.find(r => r.action === 'clean');
      if (cleanRec) {
        cleanRec.priority = 0; // 最高优先级
        cleanRec.reason = '⚠️ 空间不足，建议立即清理';
      }
    }
    
    return recommendations;
  }

  /**
   * 获取默认推荐
   * @returns {Array} 默认推荐列表
   */
  _getDefaultRecommendations() {
    return [
      {
        action: 'files',
        text: '📁 查看文件',
        reason: '浏览文件列表',
        priority: 1
      },
      {
        action: 'search',
        text: '🔍 搜索文件',
        reason: '快速查找文件',
        priority: 2
      },
      {
        action: 'status',
        text: '📊 查看容量',
        reason: '了解空间使用情况',
        priority: 3
      }
    ];
  }

  /**
   * 获取场景推荐
   * @param {string} scene - 场景名称
   * @returns {Array} 推荐列表
   */
  getSceneRecommendations(scene) {
    const sceneMap = {
      'morning': [
        { action: 'files', text: '📁 查看文件', reason: '开始今天的工作' },
        { action: 'search', text: '🔍 搜索文件', reason: '查找需要的文件' }
      ],
      'night': [
        { action: 'clean', text: '🧹 清理空间', reason: '整理一天的文件' },
        { action: 'organize', text: '🤖 智能整理', reason: '自动分类文件' }
      ],
      'full_storage': [
        { action: 'clean', text: '🧹 立即清理', reason: '⚠️ 空间不足' },
        { action: 'files', text: '📁 查看大文件', reason: '找出占用空间的文件' }
      ]
    };
    
    return sceneMap[scene] || this._getDefaultRecommendations();
  }

  /**
   * 添加推荐规则
   * @param {string} action - 动作
   * @param {Object} recommendation - 推荐项
   */
  addRule(action, recommendation) {
    if (!this.rules[action]) {
      this.rules[action] = [];
    }
    
    this.rules[action].push(recommendation);
  }

  /**
   * 移除推荐规则
   * @param {string} action - 动作
   * @param {string} recAction - 推荐动作
   */
  removeRule(action, recAction) {
    if (this.rules[action]) {
      this.rules[action] = this.rules[action].filter(r => r.action !== recAction);
    }
  }

  /**
   * 获取所有推荐规则
   * @returns {Object} 推荐规则
   */
  getRules() {
    return { ...this.rules };
  }

  /**
   * 格式化推荐为显示文本
   * @param {Array} recommendations - 推荐列表
   * @returns {string} 格式化文本
   */
  formatRecommendations(recommendations) {
    if (!recommendations || recommendations.length === 0) {
      return '';
    }
    
    return recommendations.map((rec, index) => {
      return `${index + 1}. ${rec.text} - ${rec.reason}`;
    }).join('\n');
  }

  /**
   * 生成推荐卡片
   * @param {Array} recommendations - 推荐列表
   * @returns {string} 卡片文本
   */
  createCard(recommendations) {
    if (!recommendations || recommendations.length === 0) {
      return '💡 暂无推荐';
    }
    
    let card = '💡 推荐操作\n';
    card += '━━━━━━━━━━━━━━━━━━━━\n';
    
    recommendations.forEach((rec, index) => {
      card += `${index + 1}. ${rec.text}\n`;
      card += `   ${rec.reason}\n`;
    });
    
    return card;
  }
}

module.exports = ActionRecommender;
