/**
 * 上下文文档生成器
 * 生成业务规则、技术规格、验证标准等AI可执行的上下文文档
 */

const fs = require('fs');
const path = require('path');
const CodeArchaeologyIntegrator = require('./code-archaeology-integrator');

class ContextDocumentGenerator {
  constructor(archaeologyDir = null) {
    this.domainRules = {};
    this.techStackTemplates = {};
    this.archaeologyIntegrator = archaeologyDir ? new CodeArchaeologyIntegrator(archaeologyDir) : null;
  }

  /**
   * 生成完整的上下文文档包
   * @param {Object} campaignDoc - 战役文档信息
   * @param {string} outputDir - 输出目录
   * @param {string} archaeologyDir - Code Archaeology目录（可选）
   */
  generateContextDocuments(campaignDoc, outputDir, archaeologyDir = null) {
    const { projectName, businessDomain, techStack, projectType } = campaignDoc;
    
    // 如果提供了archaeologyDir，创建新的integrator
    if (archaeologyDir) {
      this.archaeologyIntegrator = new CodeArchaeologyIntegrator(archaeologyDir);
    }
    
    // 创建输出目录
    fs.mkdirSync(outputDir, { recursive: true });
    
    // 1. 生成业务规则文档
    const businessRules = this.generateBusinessRules(businessDomain, projectType);
    this.writeDocument(`${outputDir}/business-rules.json`, JSON.stringify(businessRules, null, 2));
    this.writeDocument(`${outputDir}/business-rules.md`, this.convertToMarkdown(businessRules));
    
    // 2. 生成技术规格文档
    const technicalSpecs = this.generateTechnicalSpecs(businessDomain, techStack, projectType);
    this.writeDocument(`${outputDir}/technical-specs.yaml`, this.convertToYaml(technicalSpecs));
    
    // 3. 生成验证标准文档
    const validationStandards = this.generateValidationStandards(businessDomain, techStack);
    this.writeDocument(`${outputDir}/validation-standards.md`, validationStandards);
    
    // 4. 生成集成点配置
    const integrationConfig = this.generateIntegrationConfig(businessDomain, techStack);
    this.writeDocument(`${outputDir}/integration-config.json`, JSON.stringify(integrationConfig, null, 2));
    
    return {
      businessRules: `${outputDir}/business-rules.json`,
      technicalSpecs: `${outputDir}/technical-specs.yaml`, 
      validationStandards: `${outputDir}/validation-standards.md`,
      integrationConfig: `${outputDir}/integration-config.json`
    };
  }

  /**
   * 从Code Archaeology生成上下文文档
   * @param {string} archaeologyDir - Code Archaeology目录
   * @param {string} outputDir - 输出目录
   * @param {string} businessDomain - 业务域
   */
  generateContextFromArchaeology(archaeologyDir, outputDir, businessDomain = 'finance') {
    if (!this.archaeologyIntegrator) {
      this.archaeologyIntegrator = new CodeArchaeologyIntegrator(archaeologyDir);
    }
    
    // 创建输出目录
    fs.mkdirSync(outputDir, { recursive: true });
    
    // 1. 生成业务规则文档（基于Code Archaeology）
    const businessRules = this.archaeologyIntegrator.generateBusinessRules(businessDomain);
    this.writeDocument(`${outputDir}/business-rules.json`, JSON.stringify(businessRules, null, 2));
    this.writeDocument(`${outputDir}/business-rules.md`, this.convertToMarkdown(businessRules));
    
    // 2. 生成技术规格文档（基于Code Archaeology）
    const technicalSpecs = this.archaeologyIntegrator.generateTechnicalSpecs(businessDomain);
    this.writeDocument(`${outputDir}/technical-specs.yaml`, this.convertToYaml(technicalSpecs));
    
    // 3. 生成验证标准文档（基于Code Archaeology）
    const validationStandards = this.archaeologyIntegrator.generateValidationStandards(businessDomain);
    this.writeDocument(`${outputDir}/validation-standards.md`, validationStandards);
    
    // 4. 生成集成配置（基于Code Archaeology）
    const integrationConfig = {
      version: '1.0',
      domain: businessDomain,
      integrations: this.archaeologyIntegrator.generateIntegrationSpecs(),
      securityRisks: this.archaeologyIntegrator.extractSecurityRisks()
    };
    this.writeDocument(`${outputDir}/integration-config.json`, JSON.stringify(integrationConfig, null, 2));
    
    return {
      businessRules: `${outputDir}/business-rules.json`,
      technicalSpecs: `${outputDir}/technical-specs.yaml`, 
      validationStandards: `${outputDir}/validation-standards.md`,
      integrationConfig: `${outputDir}/integration-config.json`,
      source: 'code-archaeology'
    };
  }

  /**
   * 生成业务规则文档
   */
  generateBusinessRules(businessDomain, projectType) {
    const isIteration = projectType === 'iteration';
    
    const rules = {
      general: {
        title: '通用业务规则',
        constraints: [
          '所有输入必须经过验证',
          '关键操作必须记录日志',
          '错误处理必须友好且安全'
        ],
        validationRules: {
          id: 'positive_integer',
          name: 'non_empty_string',
          email: 'valid_email_format'
        },
        stateTransitions: {
          'draft': ['active', 'deleted'],
          'active': ['inactive', 'archived'],
          'inactive': ['active', 'deleted'],
          'archived': [],
          'deleted': []
        }
      },
      finance: {
        title: '财务业务规则',
        constraints: [
          '支付金额必须大于0',
          '支付状态必须为待支付或部分支付',
          '必须验证合同有效性',
          '发票金额必须与合同金额一致',
          '对账必须处理部分退款场景'
        ],
        validationRules: {
          amount: 'positive_decimal_with_precision_2',
          contractId: 'exists_in_database',
          paymentMethod: 'enum:[bank_transfer,online_payment,credit_card]',
          invoiceType: 'enum:[normal,credit_note]',
          refundAmount: 'less_than_or_equal_to_original_amount'
        },
        stateTransitions: {
          'pending': ['processing', 'cancelled'],
          'processing': ['completed', 'failed', 'timeout_cancelled'],
          'completed': [],
          'failed': ['retry', 'cancelled'],
          'cancelled': [],
          'timeout_cancelled': []
        }
      },
      user: {
        title: '用户管理业务规则',
        constraints: [
          '用户名必须唯一',
          '密码必须符合复杂度要求',
          '邮箱必须经过验证',
          '权限变更必须经过审批',
          '登录失败次数限制'
        ],
        validationRules: {
          username: 'unique_alphanumeric_3_20_chars',
          password: 'complex_password_min_8_chars',
          email: 'valid_email_format_unique',
          roleId: 'exists_in_role_table',
          loginAttempts: 'integer_0_5'
        },
        stateTransitions: {
          'unverified': ['active', 'deleted'],
          'active': ['suspended', 'inactive', 'deleted'],
          'suspended': ['active', 'deleted'],
          'inactive': ['active', 'deleted'],
          'deleted': []
        }
      }
    };

    const domainRules = rules[businessDomain] || rules.general;
    
    // 为迭代项目添加额外约束
    if (isIteration) {
      domainRules.constraints.push('必须保持与现有系统业务逻辑一致');
      domainRules.constraints.push('数据迁移过程不能丢失业务规则');
    }
    
    return {
      version: '1.0',
      domain: businessDomain,
      projectType: projectType,
      rules: domainRules
    };
  }

  /**
   * 生成技术规格文档
   */
  generateTechnicalSpecs(businessDomain, techStack, projectType) {
    const specs = {
      entities: this.generateDataModels(businessDomain, techStack),
      apis: this.generateApiSpecs(businessDomain, techStack),
      integrations: this.generateIntegrationSpecs(businessDomain, techStack)
    };
    
    // 为迭代项目添加兼容性要求
    if (projectType === 'iteration') {
      specs.compatibility = {
        existingSystem: 'must_maintain_backward_compatibility',
        dataFormat: 'must_support_legacy_data_formats',
        apiVersioning: 'versioned_apis_required'
      };
    }
    
    return specs;
  }

  /**
   * 生成数据模型定义
   */
  generateDataModels(businessDomain, techStack) {
    const models = {
      general: [
        {
          name: 'BaseEntity',
          fields: this.generateBaseFields(techStack),
          relationships: []
        }
      ],
      finance: [
        {
          name: 'ContractPayment',
          fields: [
            ...this.generateBaseFields(techStack),
            { name: 'contractId', type: this.mapType('Long', techStack), constraints: ['foreignKey:Contract.id', 'notNull'] },
            { name: 'amount', type: this.mapType('BigDecimal', techStack), constraints: ['notNull', 'positive', 'precision:2'] },
            { name: 'paymentMethod', type: this.mapType('String', techStack), constraints: ['notNull', 'enum:bank_transfer,online_payment,credit_card'] },
            { name: 'status', type: this.mapType('String', techStack), constraints: ['notNull', 'enum:pending,processing,completed,failed,cancelled,timeout_cancelled'] },
            { name: 'transactionId', type: this.mapType('String', techStack), constraints: ['unique'] }
          ],
          relationships: [
            { to: 'Contract', type: 'many-to-one' },
            { to: 'PaymentRecord', type: 'one-to-many' }
          ]
        },
        {
          name: 'Invoice',
          fields: [
            ...this.generateBaseFields(techStack),
            { name: 'contractId', type: this.mapType('Long', techStack), constraints: ['foreignKey:Contract.id', 'notNull'] },
            { name: 'invoiceNumber', type: this.mapType('String', techStack), constraints: ['notNull', 'unique'] },
            { name: 'amount', type: this.mapType('BigDecimal', techStack), constraints: ['notNull', 'positive', 'precision:2'] },
            { name: 'invoiceType', type: this.mapType('String', techStack), constraints: ['notNull', 'enum:normal,credit_note'] },
            { name: 'taxRate', type: this.mapType('BigDecimal', techStack), constraints: ['notNull', 'range:0-1'] }
          ],
          relationships: [
            { to: 'Contract', type: 'many-to-one' }
          ]
        }
      ],
      user: [
        {
          name: 'User',
          fields: [
            ...this.generateBaseFields(techStack),
            { name: 'username', type: this.mapType('String', techStack), constraints: ['notNull', 'unique', 'length:3-20'] },
            { name: 'email', type: this.mapType('String', techStack), constraints: ['notNull', 'unique', 'email_format'] },
            { name: 'passwordHash', type: this.mapType('String', techStack), constraints: ['notNull'] },
            { name: 'status', type: this.mapType('String', techStack), constraints: ['notNull', 'enum:unverified,active,suspended,inactive,deleted'] },
            { name: 'loginAttempts', type: this.mapType('Integer', techStack), constraints: ['default:0', 'range:0-5'] }
          ],
          relationships: [
            { to: 'Role', type: 'many-to-many' },
            { to: 'LoginLog', type: 'one-to-many' }
          ]
        }
      ]
    };

    return models[businessDomain] || models.general;
  }

  /**
   * 生成基础字段（ID, createdAt, updatedAt等）
   */
  generateBaseFields(techStack) {
    return [
      { name: 'id', type: this.mapType('Long', techStack), constraints: ['primaryKey', 'autoIncrement'] },
      { name: 'createdAt', type: this.mapType('DateTime', techStack), constraints: ['notNull', 'default:current_timestamp'] },
      { name: 'updatedAt', type: this.mapType('DateTime', techStack), constraints: ['notNull', 'default:current_timestamp', 'onUpdate:current_timestamp'] }
    ];
  }

  /**
   * 类型映射（根据技术栈转换类型）
   */
  mapType(type, techStack) {
    const mappings = {
      'Java': {
        'Long': 'Long',
        'Integer': 'Integer', 
        'String': 'String',
        'BigDecimal': 'BigDecimal',
        'DateTime': 'LocalDateTime',
        'Boolean': 'Boolean'
      },
      'Python': {
        'Long': 'int',
        'Integer': 'int',
        'String': 'str',
        'BigDecimal': 'Decimal',
        'DateTime': 'datetime',
        'Boolean': 'bool'
      },
      'Go': {
        'Long': 'int64',
        'Integer': 'int32',
        'String': 'string',
        'BigDecimal': 'decimal.Decimal',
        'DateTime': 'time.Time',
        'Boolean': 'bool'
      },
      'C#': {
        'Long': 'long',
        'Integer': 'int',
        'String': 'string',
        'BigDecimal': 'decimal',
        'DateTime': 'DateTime',
        'Boolean': 'bool'
      },
      'Rust': {
        'Long': 'i64',
        'Integer': 'i32',
        'String': 'String',
        'BigDecimal': 'rust_decimal::Decimal',
        'DateTime': 'chrono::DateTime<chrono::Utc>',
        'Boolean': 'bool'
      },
      'JavaScript': {
        'Long': 'number',
        'Integer': 'number',
        'String': 'string',
        'BigDecimal': 'string', // JavaScript doesn't have native decimal
        'DateTime': 'Date',
        'Boolean': 'boolean'
      }
    };

    const language = techStack.language;
    return mappings[language]?.[type] || type;
  }

  /**
   * 生成API规范
   */
  generateApiSpecs(businessDomain, techStack) {
    const apis = {
      general: [
        {
          name: 'createEntity',
          method: 'POST',
          path: '/api/{entity}/create',
          request: { fields: [{ name: 'name', type: 'String', required: true }] },
          response: { success: { fields: [{ name: 'id', type: 'Long' }] } },
          errorCodes: ['ENTITY_CREATION_FAILED', 'VALIDATION_ERROR']
        }
      ],
      finance: [
        {
          name: 'processPayment',
          method: 'POST',
          path: '/api/financial/payments/process',
          request: {
            fields: [
              { name: 'contractId', type: 'Long', required: true },
              { name: 'amount', type: 'BigDecimal', required: true },
              { name: 'paymentMethod', type: 'String', required: true }
            ]
          },
          response: {
            success: {
              fields: [
                { name: 'paymentId', type: 'Long' },
                { name: 'status', type: 'String' },
                { name: 'transactionId', type: 'String' }
              ]
            }
          },
          errorCodes: [
            'PAYMENT_AMOUNT_INVALID',
            'CONTRACT_NOT_FOUND',
            'PAYMENT_PROCESSING_TIMEOUT',
            'EXTERNAL_SYSTEM_UNAVAILABLE'
          ]
        },
        {
          name: 'generateInvoice',
          method: 'POST', 
          path: '/api/financial/invoices/generate',
          request: {
            fields: [
              { name: 'contractId', type: 'Long', required: true },
              { name: 'invoiceType', type: 'String', required: false }
            ]
          },
          response: {
            success: {
              fields: [
                { name: 'invoiceId', type: 'Long' },
                { name: 'invoiceNumber', type: 'String' },
                { name: 'amount', type: 'BigDecimal' }
              ]
            }
          },
          errorCodes: [
            'CONTRACT_NOT_FOUND',
            'INVOICE_GENERATION_FAILED',
            'TAX_CALCULATION_ERROR'
          ]
        }
      ],
      user: [
        {
          name: 'registerUser',
          method: 'POST',
          path: '/api/users/register',
          request: {
            fields: [
              { name: 'username', type: 'String', required: true },
              { name: 'email', type: 'String', required: true },
              { name: 'password', type: 'String', required: true }
            ]
          },
          response: {
            success: {
              fields: [
                { name: 'userId', type: 'Long' },
                { name: 'verificationToken', type: 'String' }
              ]
            }
          },
          errorCodes: [
            'USERNAME_ALREADY_EXISTS',
            'EMAIL_ALREADY_EXISTS',
            'PASSWORD_TOO_WEAK',
            'REGISTRATION_FAILED'
          ]
        }
      ]
    };

    return apis[businessDomain] || apis.general;
  }

  /**
   * 生成集成规范
   */
  generateIntegrationSpecs(businessDomain, techStack) {
    const integrations = {
      general: [
        {
          name: 'database',
          type: 'database',
          config: { connectionPool: '10', timeout: '30s' }
        }
      ],
      finance: [
        {
          name: 'alibabaOSS',
          type: 'file_storage',
          config: { bucket: 'financial-documents', region: 'cn-hangzhou' }
        },
        {
          name: 'longForSystem',
          type: 'external_api',
          config: { baseUrl: 'https://api.longfor.com', timeout: '10s' }
        },
        {
          name: 'enterpriseWechat',
          type: 'notification',
          config: { appId: 'wx123456', secret: 'secret123' }
        }
      ],
      user: [
        {
          name: 'oauthProvider',
          type: 'authentication',
          config: { provider: 'google', clientId: 'client123', clientSecret: 'secret123' }
        },
        {
          name: 'emailService',
          type: 'notification',
          config: { smtpHost: 'smtp.gmail.com', port: 587 }
        }
      ]
    };

    return integrations[businessDomain] || integrations.general;
  }

  /**
   * 生成验证标准
   */
  generateValidationStandards(businessDomain, techStack) {
    const standards = {
      general: `# 验证标准

## 单元测试要求
- 所有业务逻辑必须有单元测试覆盖
- 测试覆盖率 ≥ 70%
- 边界条件必须测试

## 集成测试要求  
- 所有外部集成点必须有集成测试
- 错误场景必须测试
- 性能基准必须验证

## 安全测试要求
- 输入验证必须测试
- 权限控制必须测试
- 敏感数据保护必须测试`,
      
      finance: `# 财务模块验证标准

## 单元测试要求
- 支付金额计算精度必须精确到小数点后2位
- 支付状态转换必须覆盖所有路径
- 发票税率计算必须准确
- 对账逻辑必须处理部分退款场景
- 测试覆盖率 ≥ 75%

## 集成测试要求
- Alibaba OSS文件上传/下载必须正常
- LongFor系统API调用必须成功
- Enterprise WeChat通知必须发送
- 外部支付网关集成必须正常

## 安全测试要求
- 支付金额篡改必须被拒绝
- 未授权访问必须被阻止
- 敏感财务数据必须加密存储
- 审计日志必须完整记录

## 性能测试要求
- 支付处理响应时间 ≤ 3秒
- 并发支持 ≥ 80TPS
- 内存使用必须稳定`,
      
      user: `# 用户模块验证标准

## 单元测试要求
- 密码复杂度验证必须准确
- 用户名唯一性检查必须正常
- 邮箱格式验证必须严格
- 权限变更逻辑必须正确
- 测试覆盖率 ≥ 75%

## 集成测试要求
- OAuth认证流程必须正常
- 邮件发送必须成功
- 第三方认证集成必须正常
- 会话管理必须安全

## 安全测试要求
- 密码必须加密存储（bcrypt/scrypt）
- SQL注入必须被阻止
- XSS攻击必须被防御
- CSRF保护必须启用
- 登录失败次数限制必须生效

## 性能测试要求
- 认证响应时间 ≤ 1秒
- 并发支持 ≥ 200TPS
- 密码哈希计算时间合理`
    };

    return standards[businessDomain] || standards.general;
  }

  /**
   * 生成集成配置
   */
  generateIntegrationConfig(businessDomain, techStack) {
    return {
      version: '1.0',
      domain: businessDomain,
      techStack: techStack,
      integrations: this.generateIntegrationSpecs(businessDomain, techStack).map(integration => ({
        name: integration.name,
        type: integration.type,
        enabled: true,
        timeout: integration.config?.timeout || '30s',
        retry: { maxAttempts: 3, delay: '1s' }
      }))
    };
  }

  /**
   * 转换为Markdown格式
   */
  convertToMarkdown(businessRules) {
    // 处理两种格式：扁平格式（来自Code Archaeology）和嵌套格式（来自上下文生成器）
    const rules = businessRules.rules ? businessRules.rules : businessRules;
    let md = `# ${rules.title}\n\n`;
    
    md += '## 约束条件\n';
    if (Array.isArray(rules.constraints)) {
      rules.constraints.forEach(constraint => {
        md += `- ${constraint}\n`;
      });
    }
    
    md += '\n## 验证规则\n';
    if (rules.validationRules && typeof rules.validationRules === 'object') {
      md += '| 字段 | 规则 |\n|------|------|\n';
      Object.entries(rules.validationRules).forEach(([field, rule]) => {
        md += `| ${field} | ${rule} |\n`;
      });
    }
    
    md += '\n## 状态转换\n';
    if (rules.stateTransitions && typeof rules.stateTransitions === 'object') {
      Object.entries(rules.stateTransitions).forEach(([state, transitions]) => {
        if (Array.isArray(transitions) && transitions.length > 0) {
          md += `- ${state} → ${transitions.join(', ')}\n`;
        } else {
          md += `- ${state} → (终态)\n`;
        }
      });
    }
    
    return md;
  }

  /**
   * 转换为YAML格式
   */
  convertToYaml(obj) {
    // 简单的YAML转换（实际项目中应使用专业库）
    return JSON.stringify(obj, null, 2)
      .replace(/"/g, '')
      .replace(/\{/g, '')
      .replace(/\}/g, '')
      .replace(/:/g, ': ')
      .replace(/,/g, '');
  }

  /**
   * 写入文档文件
   */
  writeDocument(filePath, content) {
    fs.writeFileSync(filePath, content);
  }
}

module.exports = ContextDocumentGenerator;