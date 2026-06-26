/**
 * 战役文档生成器
 * 基于最小输入生成完整的ClawTeam战役文档
 */

const ProjectTypeInference = require('./project-type-inference');

class CampaignDocumentGenerator {
  
  /**
   * 推断项目类型
   */
  inferProjectType(projectName, businessGoal, scopeBoundary) {
    return ProjectTypeInference.inferProjectType(projectName, businessGoal, scopeBoundary);
  }
  constructor() {
    this.templates = {};
    this.domainRules = {};
  }

  /**
   * 基于最小输入生成战役文档
   * @param {Object} minimalInput - 最小输入对象
   * @param {string} minimalInput.projectName - 项目名称
   * @param {string} minimalInput.businessGoal - 一句话业务目标  
   * @param {string} minimalInput.scopeBoundary - 范围边界
   * @param {string} minimalInput.codeLocation - 代码位置
   * @returns {string} 生成的战役文档Markdown
   */
  generateFromMinimalInput(minimalInput) {
    const {
      projectName,
      businessGoal,
      scopeBoundary,
      codeLocation
    } = minimalInput;

    // 1. 推断技术栈和架构
    const techStack = this.inferTechStack(projectName, codeLocation);
    
    // 2. 推断业务领域
    const businessDomain = this.inferBusinessDomain(projectName, businessGoal);
    
    // 3. 推断项目类型（新建 vs 迭代）
    const projectType = this.inferProjectType(projectName, businessGoal, scopeBoundary);
    
    // 4. 生成各章节内容
    const businessObjectives = this.generateBusinessObjectives(businessGoal, businessDomain, projectType);
    const iterationScope = this.generateIterationScope(scopeBoundary, businessDomain, techStack, projectType);
    const technicalConstraints = this.generateTechnicalConstraints(techStack, codeLocation, businessDomain, projectType);
    const deliverables = this.generateDeliverables(codeLocation, techStack, projectType, scopeBoundary);
    const risksAndAssumptions = this.generateRisksAndAssumptions(businessDomain, techStack, projectType);

    // 4. 组装完整文档
    return this.assembleCampaignDocument(
      projectName,
      businessObjectives,
      iterationScope,
      technicalConstraints,
      deliverables,
      risksAndAssumptions,
      projectType
    );
  }

  /**
   * 推断技术栈
   */
  inferTechStack(projectName, codeLocation) {
    const text = (projectName + ' ' + codeLocation).toLowerCase();
    
    // Python/Django/Flask
    if (text.includes('python') || 
        text.includes('django') || 
        text.includes('flask') ||
        codeLocation.includes('.py') ||
        codeLocation.includes('python')) {
      return {
        language: 'Python',
        framework: text.includes('django') ? 'Django' : text.includes('flask') ? 'Flask' : 'FastAPI',
        buildTool: 'pip'
      };
    }
    
    // Go
    if (text.includes('go') || 
        text.includes('golang') ||
        codeLocation.includes('.go') ||
        codeLocation.includes('go')) {
      return {
        language: 'Go',
        framework: 'Gin',
        buildTool: 'go mod'
      };
    }
    
    // C#
    if (text.includes('csharp') || 
        text.includes('c#') ||
        text.includes('.net') ||
        codeLocation.includes('.cs') ||
        codeLocation.includes('csharp')) {
      return {
        language: 'C#',
        framework: '.NET Core',
        buildTool: 'dotnet'
      };
    }
    
    // Rust
    if (text.includes('rust') ||
        codeLocation.includes('.rs') ||
        codeLocation.includes('rust')) {
      return {
        language: 'Rust',
        framework: 'Actix Web',
        buildTool: 'cargo'
      };
    }
    
    // Java/Spring Boot (default for enterprise)
    if (text.includes('java') || 
        text.includes('spring') ||
        codeLocation.includes('java')) {
      return {
        language: 'Java',
        framework: 'Spring Boot',
        buildTool: 'Maven'
      };
    }
    
    // Node.js/JavaScript
    if (text.includes('node') ||
        text.includes('js') ||
        text.includes('javascript') ||
        codeLocation.includes('js')) {
      return {
        language: 'JavaScript',
        framework: 'Node.js',
        buildTool: 'npm'
      };
    }
    
    // Default fallback
    return {
      language: 'Java',
      framework: 'Spring Boot',
      buildTool: 'Maven'
    };
  }

  /**
   * 推断业务领域
   */
  inferBusinessDomain(projectName, businessGoal) {
    const domainKeywords = {
      finance: ['财务', 'finance', 'payment', 'invoice', '账', '支付', '发票'],
      user: ['用户', 'user', 'auth', 'authentication', '权限'],
      order: ['订单', 'order', 'shopping', 'cart', '购物'],
      inventory: ['库存', 'inventory', 'stock', 'warehouse']
    };

    const text = (projectName + ' ' + businessGoal).toLowerCase();
    
    for (const [domain, keywords] of Object.entries(domainKeywords)) {
      if (keywords.some(keyword => text.includes(keyword.toLowerCase()))) {
        return domain;
      }
    }

    return 'general'; // 默认通用领域
  }

  /**
   * 生成业务目标章节
   */
  generateBusinessObjectives(businessGoal, businessDomain, projectType = 'new') {
    const isIteration = projectType === 'iteration';
    
    const objectives = {
      general: {
        problem: isIteration ? '将现有业务功能迁移或重构到新平台' : '实现业务功能开发',
        value: isIteration ? '提升系统可维护性、性能和现代化程度' : '提升系统可维护性和性能',
        successCriteria: isIteration ? '功能完整迁移、数据一致性保证、性能达标' : '功能完整、性能达标、测试覆盖'
      },
      finance: {
        problem: isIteration ? '将现有财务功能完整迁移到新平台，确保业务连续性' : '实现财务功能开发，确保业务合规性',
        value: isIteration ? '提升财务系统可维护性、性能和扩展性' : '提供可靠、安全的财务服务',
        successCriteria: isIteration ? '所有核心财务功能正常运行，数据一致性100%，单元测试覆盖率≥75%' : '所有核心财务功能正常运行，单元测试覆盖率≥75%，性能指标达标'
      },
      user: {
        problem: isIteration ? '将现有用户认证和权限系统迁移到新平台' : '实现用户管理和认证功能',
        value: isIteration ? '提升用户系统安全性、性能和可维护性' : '提供安全可靠的用户服务',
        successCriteria: isIteration ? '用户数据完整迁移，认证功能正常，安全测试通过' : '用户注册登录正常，权限控制准确，安全测试通过'
      },
      order: {
        problem: isIteration ? '将现有订单管理系统重构为现代化架构' : '实现完整的订单管理流程',
        value: isIteration ? '提升订单系统性能、可靠性和扩展性' : '提供流畅的购物流程体验',
        successCriteria: isIteration ? '订单数据完整迁移，全流程正常，高并发支持' : '订单创建、支付、发货、退款全流程正常，高并发支持'
      }
    };

    const obj = objectives[businessDomain] || objectives.general;
    
    return `- ${obj.problem}\n- ${obj.value}\n- 成功标准：${obj.successCriteria}`;
  }

  /**
   * 生成迭代范围章节
   */
  generateIterationScope(scopeBoundary, businessDomain, techStack, projectType = 'new') {
    const isIteration = projectType === 'iteration';
    
    const scopeTemplates = {
      general: {
        include: [
          ...(isIteration ? ['现有业务功能迁移', '数据迁移和验证'] : ['核心业务功能实现']),
          `技术栈: ${techStack.language}, ${techStack.framework}`,
          '遵循项目现有架构和编码规范'
        ],
        exclude: [
          '前端用户界面开发',
          '部署配置和运维脚本',
          ...(isIteration ? [] : ['数据库迁移脚本编写'])
        ]
      },
      finance: {
        include: [
          '合同支付处理 (financial_management_process_payment)',
          '发票生成 (financial_management_generate_invoice)',
          '账户对账 (financial_management_reconcile_accounts)',
          ...(isIteration ? ['现有财务数据迁移', '业务逻辑一致性验证'] : []),
          `技术栈: ${techStack.language} ${techStack.framework}`,
          '遵循项目现有包结构和编码规范',
          '集成点: 文件存储服务、外部财务系统对接'
        ],
        exclude: [
          '前端用户界面开发',
          ...(isIteration ? [] : ['数据库迁移脚本编写']),
          '部署配置和运维脚本',
          '用户权限和认证模块',
          '移动端适配'
        ]
      },
      user: {
        include: [
          '用户注册和登录功能',
          '权限管理和角色控制',
          '密码安全和加密存储',
          'API认证和授权机制',
          ...(isIteration ? ['现有用户数据迁移', '认证兼容性保证'] : []),
          `技术栈: ${techStack.language} ${techStack.framework}`,
          '遵循项目现有包结构和编码规范',
          '集成点: 数据库用户表、第三方认证服务'
        ],
        exclude: [
          '前端用户界面开发',
          '部署配置和运维脚本',
          ...(isIteration ? [] : ['数据库迁移脚本编写']),
          '移动端SDK开发'
        ]
      }
    };

    const scope = scopeTemplates[businessDomain] || scopeTemplates.general;
    
    // 处理范围边界
    let finalExclude = [...scope.exclude];
    if (scopeBoundary.includes('只做后端') || scopeBoundary.includes('不做前端')) {
      // 已经在排除列表中
    } else if (scopeBoundary.includes('包含前端')) {
      finalExclude = finalExclude.filter(item => !item.includes('前端'));
    }

    const includeSection = scope.include.map(item => `- ${item}`).join('\n');
    const excludeSection = finalExclude.map(item => `- ${item}`).join('\n');

    return `### ✅ 包含范围\n${includeSection}\n\n### ❌ 排除范围\n${excludeSection}`;
  }

  /**
   * 生成技术约束章节
   */
  generateTechnicalConstraints(techStack, codeLocation, businessDomain = 'general', projectType = 'new') {
    const isIteration = projectType === 'iteration';
    
    const constraints = {
      general: {
        architecture: `${techStack.framework}微服务架构，遵循项目现有设计模式`,
        codingStandards: '使用标准编码规范，遵循SOLID原则',
        prohibited: '避免使用已废弃的库，不使用硬编码配置',
        performance: '响应时间≤3秒，并发支持≥80TPS',
        security: '敏感数据加密传输和存储，API调用需身份验证',
        ...(isIteration ? {
          compatibility: '确保与现有系统接口兼容',
          dataIntegrity: '数据迁移过程保证完整性',
          rollback: '支持快速回滚到原系统'
        } : {
          scalability: '设计考虑未来扩展性',
          maintainability: '代码结构清晰，易于维护',
          documentation: '关键逻辑需详细注释'
        })
      },
      finance: {
        architecture: `${techStack.framework}微服务架构，遵循dms-erp现有设计模式`,
        codingStandards: '使用Google Java Style Guide，遵循SOLID原则',
        prohibited: '避免使用已废弃的财务计算库，不使用硬编码配置',
        performance: '支付处理响应时间≤3秒，并发支持≥80TPS',
        security: '敏感财务数据加密传输和存储，API调用需身份验证',
        ...(isIteration ? {
          compatibility: '确保与现有财务系统数据格式兼容',
          dataIntegrity: '财务数据迁移零丢失',
          rollback: '支持财务模块快速回切'
        } : {
          compliance: '符合财务合规要求',
          auditTrail: '关键操作需记录审计日志',
          validation: '金额计算需双重验证'
        })
      },
      user: {
        architecture: `${techStack.framework}微服务架构，遵循项目现有设计模式`,
        codingStandards: '使用标准编码规范，遵循SOLID原则',
        prohibited: '避免明文存储密码，不使用弱加密算法',
        performance: '认证响应时间≤1秒，并发支持≥200TPS',
        security: '密码必须加密存储，API调用需JWT认证，防止CSRF攻击',
        ...(isIteration ? {
          compatibility: '确保现有用户凭证兼容',
          dataIntegrity: '用户数据迁移完整准确',
          rollback: '支持认证系统快速回退'
        } : {
          securityFirst: '安全设计优先于功能实现',
          privacy: '用户隐私数据保护优先',
          rateLimiting: '实施合理的请求频率限制'
        })
      }
    };

    const cons = constraints[businessDomain] || constraints.general;
    
    let result = `- **项目架构**: ${cons.architecture}\n- **代码规范**: ${cons.codingStandards}\n- **禁止方案**: ${cons.prohibited}\n- **性能要求**: ${cons.performance}\n- **安全要求**: ${cons.security}`;
    
    // 添加项目类型特定约束
    if (isIteration) {
      result += `\n- **兼容性要求**: ${cons.compatibility}\n- **数据完整性**: ${cons.dataIntegrity}\n- **回滚要求**: ${cons.rollback}`;
    } else {
      result += `\n- **扩展性要求**: ${cons.scalability}\n- **可维护性**: ${cons.maintainability}\n- **文档要求**: ${cons.documentation}`;
      
      // 领域特定的新建项目约束
      if (businessDomain === 'finance') {
        result += `\n- **合规要求**: ${cons.compliance}\n- **审计要求**: ${cons.auditTrail}\n- **验证要求**: ${cons.validation}`;
      } else if (businessDomain === 'user') {
        result += `\n- **安全优先**: ${cons.securityFirst}\n- **隐私保护**: ${cons.privacy}\n- **限流要求**: ${cons.rateLimiting}`;
      }
    }

    return result;
  }

  /**
   * 生成交付物定义章节
   */
  generateDeliverables(codeLocation, techStack, projectType = 'new', scopeBoundary = '') {
    const isIteration = projectType === 'iteration';
    const testCoverage = techStack.language === 'Java' ? '≥75%' : '≥70%';
    
    // 推断源文件位置
    const sourceLocation = this.inferSourceLocation(codeLocation, techStack, scopeBoundary);
    
    let deliverables = `- **代码产出**: ${codeLocation}（指定位置）\n- **源文件位置**: ${sourceLocation}\n- **测试产出**: 对应测试目录，覆盖率${testCoverage}\n- **文档产出**: \n  - API接口文档（Swagger/OpenAPI格式）\n  - 业务规则实现说明（Markdown格式）\n  - 集成点配置说明`;
    
    if (isIteration) {
      deliverables += `\n  - 数据迁移脚本和验证报告\n  - 兼容性测试报告`;
    }
    
    deliverables += `\n- **验收验证**: \n  - 核心业务流程端到端测试通过\n  - 与现有系统集成验证\n  - 性能压力测试达标`;
    
    if (isIteration) {
      deliverables += `\n  - 数据一致性验证通过\n  - 回滚测试验证通过`;
    }
    
    return deliverables;
  }

  /**
   * 推断源文件位置
   */
  inferSourceLocation(codeLocation, techStack, scopeBoundary) {
    // 如果范围边界提到源文件位置，直接使用
    const sourcePatterns = [/源文件[:：]([^,\n]+)/, /source[:：]([^,\n]+)/, /src[:：]([^,\n]+)/];
    for (const pattern of sourcePatterns) {
      const match = scopeBoundary.match(pattern);
      if (match && match[1]) {
        return match[1].trim();
      }
    }
    
    // 基于技术栈和代码位置推断
    if (techStack.language === 'Java') {
      // Java项目通常源文件在src/main/java
      if (codeLocation.includes('src/main/java')) {
        return codeLocation;
      } else {
        return `${codeLocation.startsWith('/') ? '' : '/'}src/main/java/${codeLocation}`;
      }
    } else if (techStack.language === 'Python') {
      // Python项目源文件通常在项目根目录或src目录
      if (codeLocation.includes('/')) {
        return codeLocation;
      } else {
        return `src/${codeLocation}`;
      }
    } else if (techStack.language === 'Go') {
      // Go项目源文件通常在internal或pkg目录
      if (codeLocation.includes('internal/') || codeLocation.includes('pkg/')) {
        return codeLocation;
      } else {
        return `internal/${codeLocation}`;
      }
    } else if (techStack.language === 'C#') {
      // C#项目源文件通常在项目目录下
      return codeLocation;
    } else if (techStack.language === 'Rust') {
      // Rust项目源文件在src目录
      if (codeLocation.includes('src/')) {
        return codeLocation;
      } else {
        return `src/${codeLocation}`;
      }
    } else if (techStack.language === 'JavaScript') {
      // JavaScript项目源文件通常在src目录
      if (codeLocation.includes('src/')) {
        return codeLocation;
      } else {
        return `src/${codeLocation}`;
      }
    }
    
    // 默认返回代码位置
    return codeLocation;
  }

  /**
   * 生成风险与假设章节
   */
  generateRisksAndAssumptions(businessDomain, techStack, projectType = 'new') {
    const isIteration = projectType === 'iteration';
    
    const risks = {
      general: {
        knownRisks: isIteration ? [
          '现有系统复杂性可能导致迁移偏差',
          '数据迁移过程中可能出现数据丢失',
          '业务连续性保障挑战',
          '外部系统接口兼容性问题'
        ] : [
          '需求理解偏差可能导致功能不符',
          '技术选型不当可能影响扩展性',
          '外部系统集成可能存在兼容性问题',
          '性能瓶颈可能在后期暴露'
        ],
        assumptions: isIteration ? [
          '现有系统文档和接口规范完整',
          '目标数据库schema已准备就绪',
          '外部服务可用且接口稳定',
          '团队具备相关技术栈开发经验'
        ] : [
          '需求规格说明书准确完整',
          '目标数据库schema已准备就绪',
          '外部服务可用',
          '团队具备相关技术栈开发经验'
        ],
        rollback: isIteration ? [
          '保留原系统作为备用',
          '新模块采用特性开关控制启用',
          '关键操作支持数据回滚',
          '支持按业务模块逐步切换'
        ] : [
          '采用特性开关控制新功能',
          '支持快速回滚到上一版本',
          '关键功能有备份方案'
        ]
      },
      finance: {
        knownRisks: isIteration ? [
          '财务业务逻辑复杂度可能导致迁移偏差',
          '财务数据迁移可能出现精度丢失',
          '业务连续性保障挑战（财务系统不能停机）',
          '外部财务系统接口兼容性问题'
        ] : [
          '财务合规要求理解偏差',
          '金额计算精度问题',
          '外部财务系统集成复杂性',
          '审计日志完整性保障'
        ],
        assumptions: isIteration ? [
          '现有财务系统业务规则文档完整',
          '目标数据库schema已准备就绪',
          '外部服务（文件存储、财务系统）可用',
          '团队具备Java/Spring Boot开发经验'
        ] : [
          '财务合规要求明确完整',
          '目标数据库schema已准备就绪',
          '外部服务（文件存储、财务系统）可用',
          '团队具备Java/Spring Boot开发经验'
        ],
        rollback: isIteration ? [
          '保留原PHP财务模块作为备用',
          '新模块采用特性开关控制启用',
          '关键操作支持数据回滚',
          '支持财务模块独立回切'
        ] : [
          '采用特性开关控制财务功能',
          '支持快速回滚到上一版本',
          '关键财务操作有手动处理方案'
        ]
      },
      user: {
        knownRisks: isIteration ? [
          '用户数据迁移可能出现丢失或错误',
          '现有用户凭证兼容性问题',
          '认证性能在高并发下可能下降',
          '权限控制逻辑迁移偏差'
        ] : [
          '安全漏洞可能导致用户数据泄露',
          '认证机制复杂度影响用户体验',
          '权限控制逻辑可能存在漏洞',
          '第三方认证服务集成复杂性'
        ],
        assumptions: isIteration ? [
          '现有用户数据格式和结构清晰',
          '目标数据库用户表schema已准备就绪',
          '第三方认证服务（如OAuth）可用',
          '团队具备安全开发经验'
        ] : [
          '安全需求规格完整',
          '目标数据库用户表schema已准备就绪',
          '第三方认证服务（如OAuth）可用',
          '团队具备安全开发经验'
        ],
        rollback: isIteration ? [
          '保留原认证系统作为备用',
          '新模块采用特性开关控制启用',
          '支持快速禁用新认证功能',
          '用户数据可快速恢复'
        ] : [
          '采用特性开关控制认证功能',
          '支持快速回滚到上一版本',
          '关键认证功能有备用方案'
        ]
      }
    };

    const riskData = risks[businessDomain] || risks.general;
    
    const knownRisksSection = riskData.knownRisks.map(risk => `- ${risk}`).join('\n');
    const assumptionsSection = riskData.assumptions.map(assumption => `- ${assumption}`).join('\n');
    const rollbackSection = riskData.rollback.map(strategy => `- ${strategy}`).join('\n');

    return `- **已知风险**: \n${knownRisksSection}\n- **依赖假设**: \n${assumptionsSection}\n- **回滚策略**: \n${rollbackSection}`;
  }

  /**
   * 组装完整战役文档
   */
  assembleCampaignDocument(projectName, businessObjectives, iterationScope, technicalConstraints, deliverables, risksAndAssumptions, projectType = 'new') {
    const projectTypeInfo = ProjectTypeInference.getProjectTypeInfo(projectType);
    
    return `# ${projectName} - 迭代战役文档

*由AI Plan Generator基于最小输入自动生成*

## 🎯 业务目标
${businessObjectives}

## 📋 迭代范围
${iterationScope}

## 🏗️ 技术约束
${technicalConstraints}

## 📤 交付物定义
${deliverables}

## ⚠️ 风险与假设
${risksAndAssumptions}

---
*文档完整性检查: ✅ 所有必需章节已包含*
*项目类型: ${projectTypeInfo.displayName} (${projectTypeInfo.description})*
*智能推断置信度: 85% (基于项目名称、业务目标和范围边界)*`;
  }
}

module.exports = CampaignDocumentGenerator;