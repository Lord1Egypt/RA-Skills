/**
 * 任务分解生成器
 * 基于战役文档生成详细的任务分解，支持ClawTeam任务分配
 */

class TaskDecompositionGenerator {
  constructor() {
    this.taskTemplates = {};
  }

  /**
   * 生成任务分解文档
   * @param {Object} campaignInfo - 战役文档信息
   * @returns {Object} 任务分解结果
   */
  generateTaskDecomposition(campaignInfo) {
    const { businessDomain, projectType, techStack } = campaignInfo;
    
    const tasks = {
      metadata: {
        projectName: campaignInfo.projectName,
        businessDomain: businessDomain,
        projectType: projectType,
        techStack: techStack,
        sourceLocation: campaignInfo.sourceLocation || 'src/',
        codeLocation: campaignInfo.codeLocation || 'src/',
        generatedAt: new Date().toISOString()
      },
      taskGroups: []
    };

    // 生成核心功能任务组
    tasks.taskGroups.push(this.generateCoreFunctionalityTasks(businessDomain, projectType));
    
    // 生成技术架构任务组
    tasks.taskGroups.push(this.generateTechnicalArchitectureTasks(techStack, projectType));
    
    // 生成集成任务组
    tasks.taskGroups.push(this.generateIntegrationTasks(businessDomain, techStack));
    
    // 生成测试验证任务组
    tasks.taskGroups.push(this.generateTestingTasks(businessDomain, projectType));
    
    // 生成部署运维任务组
    tasks.taskGroups.push(this.generateDeploymentTasks(projectType));

    return tasks;
  }

  /**
   * 生成核心功能任务
   */
  generateCoreFunctionalityTasks(businessDomain, projectType) {
    const isIteration = projectType === 'iteration';
    
    const tasks = {
      name: '核心功能开发',
      priority: 'critical',
      description: '实现业务核心功能模块',
      tasks: []
    };

    switch (businessDomain) {
      case 'finance':
        tasks.tasks = [
          {
            id: 'financial_management_process_payment',
            title: '合同支付处理功能',
            description: '实现合同支付处理的核心逻辑，包括金额验证、状态管理、外部系统调用',
            priority: 'critical',
            estimatedEffort: '8h',
            dependencies: [],
            acceptanceCriteria: [
              '支付金额精度到小数点后2位',
              '支持多种支付方式（银行转账、在线支付、信用卡）',
              '支付状态转换完整（待支付→处理中→完成/失败/取消）',
              '超时自动取消机制'
            ],
            tags: ['payment', 'finance', 'core']
          },
          {
            id: 'financial_management_generate_invoice',
            title: '发票生成功能', 
            description: '实现发票生成逻辑，包括税率计算、发票类型处理、合规性验证',
            priority: 'critical',
            estimatedEffort: '6h',
            dependencies: [],
            acceptanceCriteria: [
              '发票金额与合同金额一致',
              '税率计算准确（支持不同税率场景）',
              '支持正常发票和红字发票',
              '发票号码唯一性保证'
            ],
            tags: ['invoice', 'finance', 'core']
          },
          {
            id: 'financial_management_reconcile_accounts',
            title: '账户对账功能',
            description: '实现账户对账逻辑，处理部分退款、多次对账等复杂场景',
            priority: 'high',
            estimatedEffort: '10h',
            dependencies: ['financial_management_process_payment'],
            acceptanceCriteria: [
              '支持部分退款场景',
              '支持多次对账操作',
              '对账差异自动识别和处理',
              '对账结果可追溯'
            ],
            tags: ['reconciliation', 'finance', 'core']
          }
        ];
        
        if (isIteration) {
          tasks.tasks.push({
            id: 'financial_data_migration',
            title: '财务数据迁移',
            description: '将现有财务数据迁移到新系统，确保数据一致性',
            priority: 'critical',
            estimatedEffort: '12h',
            dependencies: [],
            acceptanceCriteria: [
              '数据迁移零丢失',
              '业务逻辑一致性100%保证',
              '迁移过程可回滚',
              '迁移后数据验证通过'
            ],
            tags: ['migration', 'data', 'finance']
          });
        }
        break;
        
      case 'user':
        tasks.tasks = [
          {
            id: 'user_authentication_register',
            title: '用户注册功能',
            description: '实现用户注册逻辑，包括用户名验证、密码强度检查、邮箱验证',
            priority: 'critical',
            estimatedEffort: '6h',
            dependencies: [],
            acceptanceCriteria: [
              '用户名唯一性验证',
              '密码符合复杂度要求（8位以上，包含大小写字母、数字、特殊字符）',
              '邮箱格式验证和唯一性检查',
              '注册邮件发送成功'
            ],
            tags: ['auth', 'user', 'core']
          },
          {
            id: 'user_authentication_login',
            title: '用户登录功能',
            description: '实现用户登录逻辑，包括密码验证、会话管理、安全防护',
            priority: 'critical', 
            estimatedEffort: '8h',
            dependencies: ['user_authentication_register'],
            acceptanceCriteria: [
              '密码加密验证正确',
              '登录失败次数限制（5次后锁定）',
              '会话超时自动失效',
              'CSRF防护启用'
            ],
            tags: ['auth', 'user', 'core']
          },
          {
            id: 'user_permission_management',
            title: '权限管理功能',
            description: '实现基于角色的权限管理，支持细粒度权限控制',
            priority: 'high',
            estimatedEffort: '10h',
            dependencies: ['user_authentication_login'],
            acceptanceCriteria: [
              '角色创建、修改、删除功能',
              '权限分配到角色和用户',
              '权限继承和覆盖机制',
              '权限变更审计日志'
            ],
            tags: ['permission', 'user', 'core']
          }
        ];
        
        if (isIteration) {
          tasks.tasks.push({
            id: 'user_data_migration',
            title: '用户数据迁移',
            description: '将现有用户数据迁移到新认证系统',
            priority: 'critical',
            estimatedEffort: '8h',
            dependencies: [],
            acceptanceCriteria: [
              '用户凭证兼容性保证',
              '密码哈希算法迁移',
              '权限配置完整迁移',
              '迁移后用户可正常登录'
            ],
            tags: ['migration', 'data', 'user']
          });
        }
        break;
        
      default:
        tasks.tasks = [
          {
            id: 'core_entity_management',
            title: '核心实体管理',
            description: '实现通用实体的增删改查功能',
            priority: 'high',
            estimatedEffort: '6h',
            dependencies: [],
            acceptanceCriteria: [
              'CRUD操作完整实现',
              '输入验证和错误处理',
              '分页和排序支持',
              '审计日志记录'
            ],
            tags: ['core', 'general']
          }
        ];
    }

    return tasks;
  }

  /**
   * 生成技术架构任务
   */
  generateTechnicalArchitectureTasks(techStack, projectType) {
    const tasks = {
      name: '技术架构实现',
      priority: 'high',
      description: '搭建项目技术架构和基础设施',
      tasks: []
    };

    // 基础架构任务
    tasks.tasks.push({
      id: 'project_structure_setup',
      title: `${techStack.language}项目结构搭建`,
      description: `按照${techStack.framework}最佳实践搭建项目目录结构`,
      priority: 'high',
      estimatedEffort: '4h',
      dependencies: [],
      acceptanceCriteria: [
        `项目结构符合${techStack.framework}标准`,
        '包/模块划分合理',
        '配置文件组织清晰',
        '构建脚本配置完成'
      ],
      tags: ['architecture', 'setup']
    });

    // 数据库任务
    tasks.tasks.push({
      id: 'database_schema_design',
      title: '数据库Schema设计',
      description: '设计并实现数据库表结构，包括索引、约束、关系',
      priority: 'high',
      estimatedEffort: '6h',
      dependencies: ['project_structure_setup'],
      acceptanceCriteria: [
        '表结构设计符合业务需求',
        '主键、外键、索引合理设置',
        '数据类型选择合适',
        '约束条件完整定义'
      ],
      tags: ['database', 'schema']
    });

    // API任务
    tasks.tasks.push({
      id: 'api_design_implementation',
      title: 'API设计与实现',
      description: '设计RESTful API接口并实现基础框架',
      priority: 'high',
      estimatedEffort: '8h',
      dependencies: ['project_structure_setup'],
      acceptanceCriteria: [
        'API接口设计符合REST规范',
        '请求/响应格式统一',
        '错误码定义完整',
        'API文档自动生成'
      ],
      tags: ['api', 'rest']
    });

    // 安全任务
    tasks.tasks.push({
      id: 'security_implementation',
      title: '安全机制实现',
      description: '实现认证、授权、输入验证等安全机制',
      priority: 'critical',
      estimatedEffort: '8h',
      dependencies: ['api_design_implementation'],
      acceptanceCriteria: [
        '认证机制实现（JWT/OAuth等）',
        '授权控制实现（RBAC/ABAC）',
        '输入验证和XSS防护',
        '敏感数据加密存储'
      ],
      tags: ['security', 'auth']
    });

    if (projectType === 'iteration') {
      tasks.tasks.push({
        id: 'compatibility_layer',
        title: '兼容性层实现',
        description: '实现与现有系统的兼容性层，确保平滑迁移',
        priority: 'high',
        estimatedEffort: '10h',
        dependencies: ['api_design_implementation'],
        acceptanceCriteria: [
          '现有API接口兼容',
          '数据格式向后兼容',
          '版本控制机制实现',
          '迁移开关配置'
        ],
        tags: ['compatibility', 'migration']
      });
    }

    return tasks;
  }

  /**
   * 生成集成任务
   */
  generateIntegrationTasks(businessDomain, techStack) {
    const tasks = {
      name: '系统集成',
      priority: 'medium',
      description: '实现与外部系统的集成',
      tasks: []
    };

    switch (businessDomain) {
      case 'finance':
        tasks.tasks = [
          {
            id: 'alibaba_oss_integration',
            title: '阿里云OSS集成',
            description: '集成阿里云OSS服务，用于财务文档存储',
            priority: 'medium',
            estimatedEffort: '4h',
            dependencies: ['project_structure_setup'],
            acceptanceCriteria: [
              'OSS客户端配置完成',
              '文件上传/下载功能实现',
              '错误处理和重试机制',
              '性能监控集成'
            ],
            tags: ['integration', 'oss', 'storage']
          },
          {
            id: 'longfor_system_integration',
            title: '龙湖系统集成',
            description: '集成龙湖财务系统API',
            priority: 'high',
            estimatedEffort: '8h',
            dependencies: ['api_design_implementation'],
            acceptanceCriteria: [
              '龙湖API客户端实现',
              '认证和授权配置',
              '错误处理和熔断机制',
              '数据同步验证'
            ],
            tags: ['integration', 'longfor', 'finance']
          },
          {
            id: 'enterprise_wechat_integration',
            title: '企业微信集成',
            description: '集成企业微信通知服务',
            priority: 'low',
            estimatedEffort: '3h',
            dependencies: ['project_structure_setup'],
            acceptanceCriteria: [
              '企业微信API配置',
              '通知模板定义',
              '发送队列实现',
              '失败重试机制'
            ],
            tags: ['integration', 'wechat', 'notification']
          }
        ];
        break;
        
      case 'user':
        tasks.tasks = [
          {
            id: 'oauth_provider_integration',
            title: 'OAuth提供商集成',
            description: '集成第三方OAuth认证（Google/GitHub等）',
            priority: 'medium',
            estimatedEffort: '6h',
            dependencies: ['security_implementation'],
            acceptanceCriteria: [
              'OAuth客户端配置',
              '回调处理实现',
              '用户信息映射',
              '错误处理完善'
            ],
            tags: ['integration', 'oauth', 'auth']
          },
          {
            id: 'email_service_integration',
            title: '邮件服务集成',
            description: '集成邮件服务用于用户通知',
            priority: 'medium',
            estimatedEffort: '4h',
            dependencies: ['project_structure_setup'],
            acceptanceCriteria: [
              'SMTP配置完成',
              '邮件模板管理',
              '发送队列实现',
              '退信处理机制'
            ],
            tags: ['integration', 'email', 'notification']
          }
        ];
        break;
        
      default:
        tasks.tasks = [
          {
            id: 'database_integration',
            title: '数据库集成',
            description: '集成数据库连接池和ORM框架',
            priority: 'high',
            estimatedEffort: '4h',
            dependencies: ['project_structure_setup'],
            acceptanceCriteria: [
              '数据库连接池配置',
              'ORM框架集成',
              '事务管理实现',
              '性能监控配置'
            ],
            tags: ['integration', 'database']
          }
        ];
    }

    return tasks;
  }

  /**
   * 生成测试任务
   */
  generateTestingTasks(businessDomain, projectType) {
    const tasks = {
      name: '测试与验证',
      priority: 'high',
      description: '实现全面的测试覆盖和验证',
      tasks: []
    };

    // 单元测试任务
    tasks.tasks.push({
      id: 'unit_test_implementation',
      title: '单元测试实现',
      description: '为所有核心功能实现单元测试',
      priority: 'high',
      estimatedEffort: '12h',
      dependencies: ['core_entity_management'], // 依赖核心功能
      acceptanceCriteria: [
        '核心业务逻辑100%覆盖',
        '边界条件测试完整',
        '异常场景测试覆盖',
        '测试覆盖率≥75%'
      ],
      tags: ['testing', 'unit']
    });

    // 集成测试任务
    tasks.tasks.push({
      id: 'integration_test_implementation',
      title: '集成测试实现',
      description: '实现系统集成测试，验证外部系统交互',
      priority: 'medium',
      estimatedEffort: '8h',
      dependencies: ['unit_test_implementation'],
      acceptanceCriteria: [
        '所有外部集成点测试覆盖',
        '错误场景测试完整',
        '性能基准测试通过',
        '数据一致性验证'
      ],
      tags: ['testing', 'integration']
    });

    // 安全测试任务
    tasks.tasks.push({
      id: 'security_test_implementation',
      title: '安全测试实现',
      description: '实现安全测试用例，验证安全机制',
      priority: 'high',
      estimatedEffort: '6h',
      dependencies: ['security_implementation'],
      acceptanceCriteria: [
        'SQL注入防护测试',
        'XSS攻击防护测试',
        'CSRF防护测试',
        '权限越权测试'
      ],
      tags: ['testing', 'security']
    });

    if (projectType === 'iteration') {
      tasks.tasks.push({
        id: 'compatibility_test_implementation',
        title: '兼容性测试实现',
        description: '实现兼容性测试，验证与现有系统的一致性',
        priority: 'critical',
        estimatedEffort: '10h',
        dependencies: ['integration_test_implementation'],
        acceptanceCriteria: [
          'API接口兼容性验证',
          '数据格式一致性验证',
          '业务逻辑一致性验证',
          '回滚测试验证'
        ],
        tags: ['testing', 'compatibility', 'migration']
      });
    }

    return tasks;
  }

  /**
   * 生成部署任务
   */
  generateDeploymentTasks(projectType) {
    const tasks = {
      name: '部署与运维',
      priority: 'medium',
      description: '实现部署配置和运维支持',
      tasks: [
        {
          id: 'ci_cd_pipeline_setup',
          title: 'CI/CD流水线配置',
          description: '配置持续集成和持续部署流水线',
          priority: 'medium',
          estimatedEffort: '6h',
          dependencies: ['unit_test_implementation'],
          acceptanceCriteria: [
            '代码提交自动构建',
            '自动化测试执行',
            '代码质量检查',
            '部署到测试环境'
          ],
          tags: ['devops', 'ci-cd']
        },
        {
          id: 'monitoring_alerting_setup',
          title: '监控告警配置',
          description: '配置应用监控和告警机制',
          priority: 'medium',
          estimatedEffort: '4h',
          dependencies: ['ci_cd_pipeline_setup'],
          acceptanceCriteria: [
            '应用性能监控',
            '错误率告警配置',
            '资源使用监控',
            '日志集中管理'
          ],
          tags: ['devops', 'monitoring']
        }
      ]
    };

    if (projectType === 'iteration') {
      tasks.tasks.push({
        id: 'rollback_strategy_implementation',
        title: '回滚策略实现',
        description: '实现安全的回滚策略和机制',
        priority: 'high',
        estimatedEffort: '4h',
        dependencies: ['ci_cd_pipeline_setup'],
        acceptanceCriteria: [
          '一键回滚功能',
          '数据回滚脚本',
          '回滚验证测试',
          '回滚文档完善'
        ],
        tags: ['devops', 'rollback', 'migration']
      });
    }

    return tasks;
  }

  /**
   * 转换为ClawTeam任务格式
   */
  convertToClawTeamFormat(taskDecomposition) {
    const clawTeamTasks = [];
    
    taskDecomposition.taskGroups.forEach(group => {
      group.tasks.forEach(task => {
        clawTeamTasks.push({
          id: task.id,
          title: task.title,
          description: task.description,
          priority: task.priority,
          estimatedHours: parseInt(task.estimatedEffort),
          dependencies: task.dependencies,
          acceptanceCriteria: task.acceptanceCriteria,
          tags: task.tags,
          status: 'pending'
        });
      });
    });
    
    return clawTeamTasks;
  }

  /**
   * 生成Markdown格式任务列表
   */
  generateMarkdownTaskList(taskDecomposition) {
    let markdown = `# ${taskDecomposition.metadata.projectName} - 任务分解\n\n`;
    markdown += `> 生成时间: ${taskDecomposition.metadata.generatedAt}\n`;
    markdown += `> 业务领域: ${taskDecomposition.metadata.businessDomain}\n`;
    markdown += `> 项目类型: ${taskDecomposition.metadata.projectType}\n`;
    markdown += `> 技术栈: ${taskDecomposition.metadata.techStack.language} / ${taskDecomposition.metadata.techStack.framework}\n\n`;
    
    taskDecomposition.taskGroups.forEach(group => {
      markdown += `## ${group.name}\n\n`;
      markdown += `**优先级**: ${group.priority} | **描述**: ${group.description}\n\n`;
      
      markdown += '| 任务ID | 标题 | 优先级 | 预估工时 | 依赖 |\n';
      markdown += '|--------|------|--------|----------|------|\n';
      
      group.tasks.forEach(task => {
        const dependencies = task.dependencies.length > 0 ? task.dependencies.join(', ') : '-';
        markdown += `| \`${task.id}\` | ${task.title} | ${task.priority} | ${task.estimatedEffort} | ${dependencies} |\n`;
      });
      
      markdown += '\n';
    });
    
    return markdown;
  }
}

module.exports = TaskDecompositionGenerator;