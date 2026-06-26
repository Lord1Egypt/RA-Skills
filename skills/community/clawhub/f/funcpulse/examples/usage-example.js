/**
 * FuncPulse 使用示例
 * 演示如何使用funcpulse技能进行业务测试验证分析
 */

const { uploadReportToAPI, extractReportInfo, analyzeMultiRepoChanges } = require('../scripts/generate-validation-report');

// 示例1: 基本的报告上传
async function basicReportUpload() {
  const reportContent = `
# 业务测试验证报告: 用户管理功能

**日期**: 2026-04-14
**测试人员**: 张三
**版本**: v1.2.0
**代码库地址**: https://github.com/example/user-management
**涉及的仓库**: user-service, auth-service, notification-service

## 执行摘要

- **测试用例总数**: 25
- **已覆盖用例**: 22
- **未覆盖用例**: 3
- **测试覆盖率**: 88.00%
- **关键发现**: 用户注册流程中存在验证码发送失败的问题

## 需求-代码映射分析

需求REQ-001(用户注册)已完全实现，相关代码位于UserController和UserService中。
需求REQ-002(用户登录)部分实现，缺少第三方登录集成。
需求REQ-003(用户信息修改)已完全实现。

## 测试用例验证结果

- TC-001(用户手机号注册): 通过
- TC-002(用户邮箱注册): 通过
- TC-003(验证码发送): 失败
- TC-004(用户登录): 通过
- TC-005(第三方登录): 未覆盖

## 未覆盖需求分析

需求REQ-005(微信登录集成)未在代码中找到对应实现。
需求REQ-006(用户头像上传)缺少对应的测试用例。

## 缺陷列表

#### [关键] 验证码发送失败
- **关联需求**: REQ-001
- **关联用例**: TC-003
- **位置**: SmsService.java:45
- **重现步骤**:
  1. 进入用户注册页面
  2. 输入有效手机号
  3. 点击发送验证码按钮
- **期望结果**: 成功发送验证码短信
- **实际结果**: 返回"短信发送失败"错误
- **影响**: 用户无法完成注册流程
- **修复建议**: 检查短信服务商API配置和调用参数

#### [高] 第三方登录未实现
- **关联需求**: REQ-002
- **关联用例**: TC-005
- **位置**: AuthController.java
- **描述**: 微信、QQ等第三方登录功能未实现
- **影响**: 用户无法使用第三方账号登录
- **修复建议**: 集成第三方登录SDK，实现OAuth流程

#### [中] 缺少头像上传功能
- **关联需求**: REQ-006
- **关联用例**: 无
- **详情**: 用户信息修改页面缺少头像上传功能

## 需求-用例-代码追踪矩阵

| 需求ID | 需求描述 | 相关代码 | 测试用例 | 验证状态 |
|--------|----------|----------|----------|----------|
| REQ-001 | 用户注册 | UserController.java, UserService.java | TC-001, TC-002, TC-003 | 部分通过 |
| REQ-002 | 用户登录 | AuthController.java, AuthService.java | TC-004, TC-005 | 部分通过 |
| REQ-003 | 用户信息修改 | UserProfileController.java | TC-006, TC-007 | 通过 |
| REQ-004 | 密码重置 | PasswordController.java | TC-008 | 通过 |
| REQ-005 | 微信登录 | 未实现 | TC-005 | 未覆盖 |

## 建议

1. **立即**: 修复验证码发送功能，确保用户注册流程正常
2. **高优先级**: 实现第三方登录功能，提升用户体验
3. **中优先级**: 添加用户头像上传功能
4. **低优先级**: 优化用户注册表单的UI体验
`;

  try {
    console.log('上传业务测试验证报告...');
    const result = await uploadReportToAPI(reportContent);
    console.log('报告上传成功:', result.message);
    return result;
  } catch (error) {
    console.error('报告上传失败:', error.message);
    throw error;
  }
}

// 示例2: 提取报告信息
function extractReportInfoExample() {
  const reportContent = `
# 业务测试验证报告: 订单管理功能

**日期**: 2026-04-14
**测试人员**: 李四
**版本**: v2.1.0
**代码库地址**: https://github.com/example/order-management
**涉及的仓库**: order-service, payment-service, inventory-service

## 执行摘要

- **测试用例总数**: 30
- **已覆盖用例**: 28
- **未覆盖用例**: 2
- **测试覆盖率**: 93.33%
`;

  const info = extractReportInfo(reportContent);
  console.log('提取的报告信息:', JSON.stringify(info, null, 2));
  return info;
}

// 示例3: 多仓库分析
function multiRepoAnalysisExample() {
  const repoPaths = [
    '/path/to/user-service',
    '/path/to/auth-service',
    '/path/to/notification-service'
  ];
  
  console.log('分析多仓库变更...');
  // 注意：实际使用时需要提供真实存在的仓库路径
  // const repoInfos = analyzeMultiRepoChanges(repoPaths);
  // console.log('仓库分析结果:', JSON.stringify(repoInfos, null, 2));
  
  console.log('多仓库分析示例完成');
}

// 运行示例
async function runExamples() {
  console.log('=== FuncPulse 使用示例 ===\\n');
  
  console.log('1. 提取报告信息示例:');
  extractReportInfoExample();
  
  console.log('\\n2. 多仓库分析示例:');
  multiRepoAnalysisExample();
  
  console.log('\\n3. 报告上传示例:');
  // 注意：实际使用时需要取消注释
  // await basicReportUpload();
  
  console.log('\\n=== 示例运行完成 ===');
}

// 如果直接运行此示例
if (require.main === module) {
  runExamples().catch(console.error);
}

module.exports = {
  basicReportUpload,
  extractReportInfoExample,
  multiRepoAnalysisExample,
  runExamples
};
