/**
 * 项目类型推断模块
 * 判断项目是新建（greenfield）还是迭代（brownfield/migration）
 */

class ProjectTypeInference {
  /**
   * 推断项目类型
   * @param {string} projectName - 项目名称
   * @param {string} businessGoal - 业务目标
   * @param {string} scopeBoundary - 范围边界
   * @returns {string} 'new' | 'iteration'
   */
  static inferProjectType(projectName, businessGoal, scopeBoundary) {
    const text = (projectName + ' ' + businessGoal + ' ' + scopeBoundary).toLowerCase();
    
    // 迭代项目关键词
    const iterationKeywords = [
      'migration', 'migrate', 'refactor', 'refactoring', 'upgrade', 'upgrading',
      'rewrite', 'rewriting', 'modernize', 'modernization',
      '迁移', '重构', '升级', '重写', '现代化', '替换',
      'existing', 'legacy', 'old', 'current', '现有', '遗留', '老旧'
    ];
    
    // 新建项目关键词  
    const newProjectKeywords = [
      'new', 'create', 'creating', 'build', 'building', 'develop', 'developing',
      'implement', 'implementation', 'fresh', 'greenfield',
      '新建', '创建', '开发', '实现', '全新', '从零开始'
    ];
    
    // 检查迭代关键词
    const hasIterationKeywords = iterationKeywords.some(keyword => text.includes(keyword));
    
    // 检查新建关键词
    const hasNewProjectKeywords = newProjectKeywords.some(keyword => text.includes(keyword));
    
    // 如果明确提到迭代关键词，返回iteration
    if (hasIterationKeywords) {
      return 'iteration';
    }
    
    // 如果明确提到新建关键词，返回new
    if (hasNewProjectKeywords) {
      return 'new';
    }
    
    // 默认启发式判断
    // 如果项目名包含版本号（如v1, v2）且业务目标包含"迁移"，倾向于迭代
    if ((projectName.match(/v\d+/) || projectName.match(/-\d+/)) && 
        (businessGoal.includes('迁移') || businessGoal.includes('migrate'))) {
      return 'iteration';
    }
    
    // 如果范围边界提到"现有系统"、"legacy"等，倾向于迭代
    if (scopeBoundary.includes('现有') || scopeBoundary.includes('existing') || 
        scopeBoundary.includes('legacy') || scopeBoundary.includes('老旧')) {
      return 'iteration';
    }
    
    // 默认假设为新建项目（更安全的假设）
    return 'new';
  }
  
  /**
   * 获取项目类型描述
   * @param {string} projectType - 项目类型
   * @returns {Object} 项目类型相关信息
   */
  static getProjectTypeInfo(projectType) {
    if (projectType === 'iteration') {
      return {
        displayName: '迭代项目',
        description: '基于现有系统进行迁移、重构或升级',
        focusAreas: ['兼容性保证', '数据迁移', '回滚策略', '业务连续性'],
        riskProfile: '中高风险 - 需要处理现有系统复杂性'
      };
    } else {
      return {
        displayName: '新建项目',  
        description: '从零开始构建全新系统',
        focusAreas: ['架构设计', '最佳实践', '可扩展性', '技术选型'],
        riskProfile: '中低风险 - 无历史包袱，但需求理解风险较高'
      };
    }
  }
}

module.exports = ProjectTypeInference;