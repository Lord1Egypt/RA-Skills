/**
 * Code Archaeology 集成器
 * 从Code Archaeology分析结果中提取关键信息，用于生成上下文文档
 */

const fs = require('fs');
const path = require('path');

class CodeArchaeologyIntegrator {
  constructor(archaeologyDir) {
    this.archaeologyDir = archaeologyDir;
    this.analysisResults = {};
    this.loadAnalysisResults();
  }

  /**
   * 加载Code Archaeology分析结果
   */
  loadAnalysisResults() {
    // 支持两种目录结构：
    // 1. 统一根目录结构: /zbs_php_code_archaeology/results/
    // 2. 扁平目录结构: /zbs_php_code_archaeology/
    
    const resultsDir = path.join(this.archaeologyDir, 'results');
    const isUnifiedStructure = fs.existsSync(resultsDir) && fs.statSync(resultsDir).isDirectory();
    
    const files = [
      'zbs_php_api_analysis.md',
      'zbs_php_security_audit_results.md', 
      'zbs_php_performance_analysis.md',
      'zbs_php_technical_debt_assessment.md',
      'zbs_php_optimization_recommendations.md',
      'zbs_php_code_archaeology_final_report.md'
    ];

    files.forEach(file => {
      // 尝试统一结构路径
      let filePath = isUnifiedStructure ? path.join(resultsDir, file) : path.join(this.archaeologyDir, file);
      
      // 如果统一结构路径不存在，回退到扁平结构
      if (!fs.existsSync(filePath)) {
        filePath = path.join(this.archaeologyDir, file);
      }
      
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        const key = file.replace('.md', '').replace('zbs_php_', '');
        // 简化处理：直接存储原始内容
        this.analysisResults[key] = content;
      }
    });
  }

  /**
   * 提取业务域信息
   */
  extractBusinessDomains() {
    // 从最终报告中提取业务域
    const finalReport = this.analysisResults.code_archaeology_final_report;
    if (finalReport) {
      const domainMatch = finalReport.match(/### 完成的12个业务域([\s\S]*?)##/);
      if (domainMatch) {
        const domainText = domainMatch[1];
        const domains = [];
        const lines = domainText.split('\n');
        lines.forEach(line => {
          if (line.trim().startsWith('- ')) {
            const domain = line.replace('- ', '').split('(')[0].trim();
            if (domain) {
              domains.push(domain);
            }
          }
        });
        return domains;
      }
    }
    return ['finance']; // 默认返回财务域
  }

  /**
   * 提取财务模块API信息
   */
  extractFinancialApis() {
    const apiAnalysis = this.analysisResults.api_analysis;
    if (apiAnalysis) {
      const financialMatch = apiAnalysis.match(/#### 财务管理 \(Financial Management\)([\s\S]*?)(?:####|$)/);
      if (financialMatch) {
        const financialText = financialMatch[1];
        const apis = [];
        const lines = financialText.split('\n');
        lines.forEach(line => {
          if (line.trim().startsWith('- `')) {
            const match = line.match(/-\s*`([^`]+)`\s*-\s*(.*)/);
            if (match) {
              apis.push({
                name: match[1].trim(),
                description: match[2].trim()
              });
            }
          }
        });
        return apis;
      }
    }
    
    // 默认返回
    return [
      { name: 'api4pay.php', description: '支付处理' },
      { name: 'api4refund.php', description: '退款处理' },
      { name: 'finance.php', description: '财务基础功能' }
    ];
  }

  /**
   * 生成业务规则
   */
  generateBusinessRules(businessDomain = 'finance') {
    if (businessDomain === 'finance') {
      return {
        version: '1.0',
        domain: businessDomain,
        projectType: 'iteration',
        rules: {
          title: '财务业务规则（基于Code Archaeology分析）',
          constraints: [
            '支付金额必须大于0',
            '合同状态必须有效才能进行支付',
            '退款金额不能超过原支付金额',
            '多租户数据隔离（host_id）必须保证',
            '硬编码超级密码必须移除'
          ],
          validationRules: {
            amount: 'positive_decimal_precision_2',
            contractId: 'exists_in_ys_contract_table',
            hostId: 'valid_tenant_id',
            paymentMethod: 'enum:[bank_transfer,online_payment]'
          },
          stateTransitions: {
            'pending': ['processing', 'cancelled'],
            'processing': ['completed', 'failed'],
            'completed': [],
            'failed': ['retry', 'cancelled'],
            'cancelled': []
          }
        }
      };
    }
    
    return {
      version: '1.0',
      domain: 'general',
      projectType: 'new',
      rules: {
        title: '通用业务规则',
        constraints: ['输入必须验证', '输出必须编码', '权限必须检查'],
        validationRules: { id: 'positive_integer', name: 'non_empty_string' },
        stateTransitions: { 'active': ['inactive', 'deleted'], 'inactive': ['active', 'deleted'] }
      }
    };
  }

  /**
   * 生成技术规格
   */
  generateTechnicalSpecs(businessDomain = 'finance') {
    return {
      entities: this.extractDataModels(),
      apis: this.generateApiSpecs(businessDomain),
      integrations: this.generateIntegrationSpecs(),
      security: {
        authentication: 'JWT or OAuth 2.0 (replace Session-based)',
        authorization: 'RBAC with object-level permissions',
        dataProtection: 'Field-level encryption for sensitive data',
        inputValidation: 'Whitelist validation with parameterized queries'
      }
    };
  }

  /**
   * 提取数据模型信息
   */
  extractDataModels() {
    // 基于Code Archaeology分析结果
    return [
      {
        name: 'ys_contract',
        fields: [
          { name: 'id', type: 'int', constraints: ['primary_key', 'auto_increment'] },
          { name: 'host_id', type: 'int', constraints: ['not_null', 'tenant_isolation'] },
          { name: 'contract_no', type: 'varchar(50)', constraints: ['not_null', 'unique'] },
          { name: 'customer_id', type: 'int', constraints: ['not_null'] },
          { name: 'total_amount', type: 'decimal(10,2)', constraints: ['not_null'] },
          { name: 'status', type: 'varchar(20)', constraints: ['not_null'] },
          { name: 'created_at', type: 'datetime', constraints: ['not_null'] },
          { name: 'updated_at', type: 'datetime', constraints: ['not_null'] }
        ],
        relationships: [
          { to: 'ys_admin_user', type: 'many-to-one', foreignKey: 'customer_id' }
        ]
      },
      {
        name: 'ys_admin_user',
        fields: [
          { name: 'id', type: 'int', constraints: ['primary_key', 'auto_increment'] },
          { name: 'host_id', type: 'int', constraints: ['not_null', 'tenant_isolation'] },
          { name: 'username', type: 'varchar(50)', constraints: ['not_null', 'unique'] },
          { name: 'password_hash', type: 'varchar(255)', constraints: ['not_null'] },
          { name: 'email', type: 'varchar(100)', constraints: ['unique'] },
          { name: 'status', type: 'varchar(20)', constraints: ['not_null'] },
          { name: 'created_at', type: 'datetime', constraints: ['not_null'] },
          { name: 'updated_at', type: 'datetime', constraints: ['not_null'] }
        ],
        relationships: [
          { to: 'ys_contract', type: 'one-to-many', foreignKey: 'customer_id' }
        ]
      }
    ];
  }

  /**
   * 生成API规范
   */
  generateApiSpecs(businessDomain = 'finance') {
    if (businessDomain === 'finance') {
      return [
        {
          name: 'processPayment',
          method: 'POST',
          path: '/api/financial/payments/process',
          description: '处理合同支付（迁移自 api4pay.php）',
          request: {
            fields: [
              { name: 'contractId', type: 'integer', required: true },
              { name: 'amount', type: 'decimal', required: true },
              { name: 'paymentMethod', type: 'string', required: true }
            ]
          },
          response: {
            success: {
              fields: [
                { name: 'paymentId', type: 'integer' },
                { name: 'status', type: 'string' },
                { name: 'transactionId', type: 'string' }
              ]
            }
          },
          errorCodes: [
            'PAYMENT_AMOUNT_INVALID',
            'CONTRACT_NOT_FOUND', 
            'TENANT_ISOLATION_VIOLATION',
            'AUTHENTICATION_FAILED'
          ],
          securityFixes: [
            'Replace string concatenation with parameterized queries',
            'Add tenant isolation validation',
            'Implement proper input validation',
            'Remove hardcoded super password logic'
          ]
        },
        {
          name: 'processRefund',
          method: 'POST',
          path: '/api/financial/refunds/process',
          description: '处理退款（迁移自 api4refund.php）',
          request: {
            fields: [
              { name: 'paymentId', type: 'integer', required: true },
              { name: 'refundAmount', type: 'decimal', required: true },
              { name: 'reason', type: 'string', required: true }
            ]
          },
          response: {
            success: {
              fields: [
                { name: 'refundId', type: 'integer' },
                { name: 'status', type: 'string' },
                { name: 'refundAmount', type: 'decimal' }
              ]
            }
          },
          errorCodes: [
            'REFUND_AMOUNT_EXCEEDS_PAYMENT',
            'PAYMENT_NOT_FOUND',
            'REFUND_NOT_ALLOWED_FOR_STATUS'
          ]
        }
      ];
    }
    
    return [];
  }

  /**
   * 生成集成规范
   */
  generateIntegrationSpecs() {
    return [
      {
        name: 'database',
        type: 'mysql',
        enabled: true,
        timeout: '30s',
        retry: { maxAttempts: 3, delay: '1s' },
        config: {
          connectionPool: 10,
          timeout: '30s',
          charset: 'utf8mb4'
        }
      },
      {
        name: 'cache',
        type: 'redis',
        enabled: true,
        timeout: '5s',
        retry: { maxAttempts: 3, delay: '1s' },
        config: {
          host: 'localhost',
          port: 6379,
          timeout: '5s'
        }
      },
      {
        name: 'enterprise_wechat',
        type: 'notification',
        enabled: true,
        timeout: '10s',
        retry: { maxAttempts: 3, delay: '1s' },
        config: {
          appId: 'your-app-id',
          secret: 'your-secret'
        }
      }
    ];
  }

  /**
   * 提取安全风险信息
   */
  extractSecurityRisks() {
    return [
      {
        severity: 'critical',
        category: 'Hardcoded Credentials',
        description: '存在硬编码的超级管理员密码 SUPERDWP = \'123qwe\'，可绕过正常认证'
      },
      {
        severity: 'high',
        category: 'SQL Injection',
        description: '大量SQL查询直接拼接用户输入，存在SQL注入风险'
      },
      {
        severity: 'high',
        category: 'Weak Password Storage',
        description: '密码仅使用双重MD5哈希，没有加盐，容易受到彩虹表攻击'
      }
    ];
  }

  /**
   * 生成验证标准
   */
  generateValidationStandards(businessDomain = 'finance') {
    if (businessDomain === 'finance') {
      return `# 财务模块验证标准（基于Code Archaeology）

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
- **SQL注入防护**: 所有数据库查询必须使用参数化查询
- **认证安全**: 移除硬编码超级密码，实施现代认证机制  
- **数据隔离**: 多租户数据隔离必须100%保证
- **传输安全**: 所有敏感数据传输必须使用HTTPS

## 功能测试要求  
- **支付功能**: 支付金额精度到小数点后2位，状态转换完整
- **退款功能**: 退款金额不能超过原支付金额，支持部分退款
- **合同关联**: 支付必须关联有效合同，合同状态必须正确

## 性能测试要求
- **响应时间**: 支付处理≤2秒，并发支持≥100TPS
- **数据库**: 查询必须有适当索引，避免慢查询
- **内存**: 避免内存泄漏，特别是Excel处理场景

## 兼容性测试要求
- **API兼容**: 新API必须保持向后兼容
- **数据迁移**: 现有财务数据必须完整迁移
- **业务连续**: 迁移过程不能影响现有业务`;
    }
    
    return `# 通用验证标准

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
- 敏感数据保护必须测试

- 基础功能测试
- 安全测试
- 性能测试`;
  }
}

module.exports = CodeArchaeologyIntegrator;