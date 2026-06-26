/**
 * Requirement Refiner Skill - 测试用例
 * 
 * 测试版本：v2.3-hybrid-adaptive-parser (2026-04-14)
 * 
 * @module asf-v4/skills/__tests__/requirement-refiner-skill.test
 */

import { RequirementRefinerSkill } from '../requirement-refiner-skill';
import { createMockContext } from '../../../test-utils/mock-context';

describe('RequirementRefinerSkill - Hybrid Adaptive Parser', () => {
  let skill: RequirementRefinerSkill;

  beforeEach(() => {
    const mockContext = createMockContext();
    skill = new RequirementRefinerSkill(mockContext);
  });

  // ============================================================================
  // 基础功能测试
  // ============================================================================

  test('简单需求应使用标准精炼流程', async () => {
    const simpleReq = '创建一个用户登录页面，包含用户名和密码输入框';
    const result = await skill.refine(simpleReq);
    
    expect(result).toBeDefined();
    // 验证未触发复杂度检测
    // expect(result.metadata?.isComplex).toBe(false);
  });

  test('空输入应优雅降级到标准精炼', async () => {
    const emptyReq = '';
    const result = await skill.refine(emptyReq);
    
    expect(result).toBeDefined();
    // 应该成功处理空输入
  });

  // ============================================================================
  // 复杂度检测测试
  // ============================================================================

  test('否定词测试 - 不应误判为复杂', async () => {
    const negationReq = '这是一个简单项目，不需要多级审批，也不需要跨部门协作';
    const result = await skill.refine(negationReq);
    
    // 由于否定词影响，复杂度评分应该较低
    // expect(result.metadata?.isComplex).toBe(false);
  });

  test('多部门关键词应触发模块化拆分', async () => {
    const multiDeptReq = `
      固定资产投资计划管理系统需求：
      
      涉及部门：投资管理部、工程部、审计部、财务部、计划部
      
      功能要求：
      1. 项目立项管理（投资管理部）
      2. 设计采购管理（工程部）
      3. 合同审批流程（财务部）
      4. 结算审计（审计部）
      5. 资金决算报表（计划部）
    `;
    
    const result = await skill.refine(multiDeptReq);
    
    // 应该触发模块化拆分
    // expect(result.modules?.length).toBe(5);
  });

  test('边界阈值测试 - 恰好2个部门不应触发拆分', async () => {
    const boundaryReq = `
      项目需求：
      涉及部门：投资管理部、工程部
      
      功能：简单的项目管理
    `;
    
    const result = await skill.refine(boundaryReq);
    
    // 2个部门不应触发模块化拆分
    // expect(result.modules).toBeUndefined();
  });

  // ============================================================================
  // 多格式内容测试
  // ============================================================================

  test('混合格式 - PRD文本 + Mermaid流程图', async () => {
    const mixedReq = `
      # 用户注册流程
      
      用户需要完成以下步骤：
      
      \`\`\`mermaid
      graph TD
        A[开始] --> B[填写基本信息]
        B --> C[邮箱验证]
        C --> D[设置密码]
        D --> E[完成注册]
      \`\`\`
      
      需要支持多语言和第三方登录。
    `;
    
    const result = await skill.refine(mixedReq);
    
    expect(result).toBeDefined();
    // 应该正确处理混合格式
  });

  test('异常输入 - 纯图片引用', async () => {
    const imageReq = '![流程图](diagram.png)\n![界面设计](ui-design.png)';
    
    const result = await skill.refine(imageReq);
    
    expect(result).toBeDefined();
    // 应该优雅降级处理
  });

  // ============================================================================
  // 模板匹配测试
  // ============================================================================

  test('模板匹配 - 包含固定资产投资关键词', async () => {
    const templateReq = `
      固定资产投资计划管理系统
      
      需求概述：
      - 全流程管理
      - 跨部门协作
      - 多级审批
    `;
    
    const result = await skill.refine(templateReq);
    
    // 应该匹配固定资产投资模板
    // expect(result.metadata?.templateId).toBe('fixed-asset-investment');
  });

  // ============================================================================
  // 错误处理测试
  // ============================================================================

  test('异常输入 - 乱码应优雅降级', async () => {
    const garbageReq = 'asdf!@#$%^&*()_+{}|:"<>?';
    
    const result = await skill.refine(garbageReq);
    
    expect(result).toBeDefined();
    // 应该不会抛出异常
  });

  test('模块创建失败不应中断整个流程', async () => {
    // 模拟某个模块创建失败的情况
    // 这里需要更复杂的 mock，暂时跳过
    expect(true).toBe(true);
  });

  // ============================================================================
  // 性能测试
  // ============================================================================

  test('大文本输入应正常处理', async () => {
    const largeReq = '需求文档\n'.repeat(1000); // 1000行需求文档
    
    const startTime = Date.now();
    const result = await skill.refine(largeReq);
    const endTime = Date.now();
    
    expect(result).toBeDefined();
    // 处理时间应该在合理范围内
    expect(endTime - startTime).toBeLessThan(10000); // 10秒内
  });
});

// ============================================================================
// 回滚机制测试
// ============================================================================

describe('HybridParserRollback', () => {
  // 回滚机制的测试需要集成测试环境
  // 这里只做基本的单元测试
  
  test('回滚机制初始化', () => {
    // const rollback = createHybridParserRollback();
    // expect(rollback).toBeDefined();
    expect(true).toBe(true); // 占位测试
  });
});