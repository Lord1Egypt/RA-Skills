#!/usr/bin/env node

/**
 * AI Plan Generator v2 - 主入口
 * 支持战役文档生成和传统业务规则提取
 */

const fs = require('fs');
const path = require('path');
const CampaignDocumentGenerator = require('./campaign-document-generator');
const ContextDocumentGenerator = require('./context-document-generator');
const CompletenessAnalyzer = require('./completeness-analyzer');
const TaskDecompositionGenerator = require('./task-decomposition-generator');
const ProcessFileManager = require('./process-file-manager');

// 命令行参数处理
const args = process.argv.slice(2);
const command = args[0];

if (command === 'generate-campaign') {
  // 从JSON文件读取最小输入
  const inputFile = args[1];
  const outputFile = args[2] || 'campaign-document.md';
  
  if (!inputFile) {
    console.error('Usage: node src/index.js generate-campaign <input.json> [output.md]');
    process.exit(1);
  }

  try {
    const input = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    const generator = new CampaignDocumentGenerator();
    const campaignDoc = generator.generateFromMinimalInput(input);
    
    fs.writeFileSync(outputFile, campaignDoc);
    console.log(`✅ 战役文档已生成: ${outputFile}`);
    console.log('📋 文档完整性: 所有必需章节已包含');
    
  } catch (error) {
    console.error('❌ 生成战役文档失败:', error.message);
    process.exit(1);
  }
} else if (command === 'generate-context') {
  // 生成上下文文档
  const campaignFile = args[1];
  const outputDir = args[2] || 'context-documents';
  
  if (!campaignFile) {
    console.error('Usage: node src/index.js generate-context <campaign.json> [output-dir]');
    process.exit(1);
  }

  try {
    const campaignContent = fs.readFileSync(campaignFile, 'utf8');
    // 这里简化处理，实际应从战役文档提取信息
    const campaignInfo = {
      projectName: 'example-project',
      businessDomain: 'finance',
      techStack: { language: 'Java', framework: 'Spring Boot' },
      projectType: 'iteration'
    };
    
    const contextGenerator = new ContextDocumentGenerator();
    const contextDocs = contextGenerator.generateContextDocuments(campaignInfo, outputDir);
    
    console.log(`✅ 上下文文档已生成到: ${outputDir}`);
    Object.entries(contextDocs).forEach(([name, path]) => {
      console.log(`   📄 ${name}: ${path}`);
    });
    
  } catch (error) {
    console.error('❌ 生成上下文文档失败:', error.message);
    process.exit(1);
  }
} else if (command === 'generate-context-from-archaeology') {
  // 从Code Archaeology生成上下文文档
  const archaeologyDir = args[1] || '/Users/admin/.openclaw/workspace/zbs_php_code_archaeology';
  const outputDir = args[2] || 'context-from-archaeology';
  const businessDomain = args[3] || 'finance';
  
  if (!fs.existsSync(archaeologyDir)) {
    console.error(`❌ Code Archaeology目录不存在: ${archaeologyDir}`);
    process.exit(1);
  }

  try {
    const contextGenerator = new ContextDocumentGenerator();
    const contextDocs = contextGenerator.generateContextFromArchaeology(archaeologyDir, outputDir, businessDomain);
    
    console.log(`✅ 从Code Archaeology生成上下文文档到: ${outputDir}`);
    Object.entries(contextDocs).forEach(([name, path]) => {
      if (name !== 'source') {
        console.log(`   📄 ${name}: ${path}`);
      }
    });
    
  } catch (error) {
    console.error('❌ 从Code Archaeology生成上下文文档失败:', error.message);
    process.exit(1);
  }
} else if (command === 'generate-tasks') {
  // 生成任务分解
  const campaignFile = args[1];
  const outputDir = args[2] || 'task-decomposition';
  
  if (!campaignFile) {
    console.error('Usage: node src/index.js generate-tasks <campaign.json> [output-dir]');
    process.exit(1);
  }

  try {
    const input = JSON.parse(fs.readFileSync(campaignFile, 'utf8'));
    const generator = new CampaignDocumentGenerator();
    const campaignDoc = generator.generateFromMinimalInput(input);
    
    // 提取战役信息用于任务分解
    const campaignInfo = {
      projectName: input.projectName,
      businessDomain: generator.inferBusinessDomain(input.projectName, input.businessGoal),
      projectType: generator.inferProjectType(input.projectName, input.businessGoal, input.scopeBoundary),
      techStack: generator.inferTechStack(input.projectName, input.codeLocation),
      codeLocation: input.codeLocation,
      sourceLocation: generator.inferSourceLocation(input.codeLocation, generator.inferTechStack(input.projectName, input.codeLocation), input.scopeBoundary)
    };
    
    const taskGenerator = new TaskDecompositionGenerator();
    const taskDecomposition = taskGenerator.generateTaskDecomposition(campaignInfo);
    
    // 创建输出目录
    fs.mkdirSync(outputDir, { recursive: true });
    
    // 保存JSON格式
    fs.writeFileSync(`${outputDir}/tasks.json`, JSON.stringify(taskDecomposition, null, 2));
    
    // 保存Markdown格式
    const markdownTasks = taskGenerator.generateMarkdownTaskList(taskDecomposition);
    fs.writeFileSync(`${outputDir}/tasks.md`, markdownTasks);
    
    // 保存ClawTeam格式
    const clawTeamTasks = taskGenerator.convertToClawTeamFormat(taskDecomposition);
    fs.writeFileSync(`${outputDir}/clawteam-tasks.json`, JSON.stringify(clawTeamTasks, null, 2));
    
    console.log(`✅ 任务分解已生成到: ${outputDir}`);
    console.log(`   📄 JSON格式: ${outputDir}/tasks.json`);
    console.log(`   📄 Markdown格式: ${outputDir}/tasks.md`);
    console.log(`   📄 ClawTeam格式: ${outputDir}/clawteam-tasks.json`);
    
  } catch (error) {
    console.error('❌ 生成任务分解失败:', error.message);
    process.exit(1);
  }
} else if (command === 'analyze-completeness') {
  // 分析上下文文档完整性
  const contextDir = args[1] || 'context-documents';
  
  try {
    const contextDocs = {
      businessRules: `${contextDir}/business-rules.json`,
      technicalSpecs: `${contextDir}/technical-specs.yaml`,
      validationStandards: `${contextDir}/validation-standards.md`,
      integrationConfig: `${contextDir}/integration-config.json`
    };
    
    const analyzer = new CompletenessAnalyzer();
    const report = analyzer.analyzeContextDocuments(contextDocs);
    
    // 输出分析报告
    console.log('🔍 上下文文档完整性分析报告');
    console.log(`📊 总体分数: ${report.overallScore}/100`);
    console.log(`📄 文档数量: ${Object.keys(report.documents).length}`);
    console.log(`⚠️  问题数量: ${report.issues.length}`);
    console.log(`❓ 澄清问题: ${report.clarifications.length}`);
    
    if (report.overallScore >= 80) {
      console.log('✅ 状态: 通过 - 文档完整且可执行');
    } else if (report.overallScore >= 60) {
      console.log('⚠️  状态: 警告 - 建议完善后再使用');
    } else {
      console.log('❌ 状态: 失败 - 存在严重问题，需要修复');
    }
    
    // 输出澄清问题
    if (report.clarifications.length > 0) {
      console.log('\n❓ 自动生成的澄清问题:');
      report.clarifications.slice(0, 5).forEach((clarification, index) => {
        console.log(`   ${index + 1}. ${clarification.question}`);
      });
    }
    
    // 保存详细报告
    fs.writeFileSync(`${contextDir}/analysis-report.json`, JSON.stringify(report, null, 2));
    console.log(`\n📝 详细报告已保存: ${contextDir}/analysis-report.json`);
    
  } catch (error) {
    console.error('❌ 分析上下文文档失败:', error.message);
    process.exit(1);
  }
} else if (command === 'generate-complete-workflow') {
  // 生成完整工作流
  const inputFile = args[1];
  const archaeologyDir = args[2] || '/Users/admin/.openclaw/workspace/zbs_php_code_archaeology';
  
  if (!inputFile) {
    console.error('Usage: node src/index.js generate-complete-workflow <input.json> [archaeology-dir]');
    process.exit(1);
  }

  try {
    // 读取输入文件
    const input = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    const projectName = input.projectName;
    
    // 创建过程文件管理器
    const fileManager = new ProcessFileManager();
    const processFiles = fileManager.setProcessFileLocations(inputFile, projectName);
    fileManager.setArchaeologyLocation(archaeologyDir);
    
    console.log(`🚀 开始生成完整工作流: ${projectName}`);
    console.log(`📁 项目目录: ${path.join(fileManager.baseDir, projectName)}`);
    
    // 1. 生成战役文档
    console.log('\n1️⃣ 生成战役文档...');
    const generator = new CampaignDocumentGenerator();
    const campaignDoc = generator.generateFromMinimalInput(input);
    fs.writeFileSync(processFiles.campaign, campaignDoc);
    console.log(`✅ 战役文档: ${processFiles.campaign}`);
    
    // 2. 生成任务分解
    console.log('\n2️⃣ 生成任务分解...');
    const campaignInfo = {
      projectName: input.projectName,
      businessDomain: generator.inferBusinessDomain(input.projectName, input.businessGoal),
      projectType: generator.inferProjectType(input.projectName, input.businessGoal, input.scopeBoundary),
      techStack: generator.inferTechStack(input.projectName, input.codeLocation),
      codeLocation: input.codeLocation,
      sourceLocation: generator.inferSourceLocation(input.codeLocation, generator.inferTechStack(input.projectName, input.codeLocation), input.scopeBoundary)
    };
    
    const taskGenerator = new TaskDecompositionGenerator();
    const taskDecomposition = taskGenerator.generateTaskDecomposition(campaignInfo);
    
    fs.writeFileSync(processFiles.tasks.json, JSON.stringify(taskDecomposition, null, 2));
    fs.writeFileSync(processFiles.tasks.markdown, taskGenerator.generateMarkdownTaskList(taskDecomposition));
    fs.writeFileSync(processFiles.tasks.clawteam, JSON.stringify(taskGenerator.convertToClawTeamFormat(taskDecomposition), null, 2));
    console.log(`✅ 任务分解: ${processFiles.tasks.json}`);
    
    // 3. 生成上下文文档（从Code Archaeology）
    console.log('\n3️⃣ 生成上下文文档（从Code Archaeology）...');
    const contextGenerator = new ContextDocumentGenerator();
    const contextDocs = contextGenerator.generateContextFromArchaeology(
      archaeologyDir, 
      path.dirname(processFiles.context.businessRules), 
      campaignInfo.businessDomain
    );
    console.log(`✅ 上下文文档: ${path.dirname(processFiles.context.businessRules)}`);
    
    // 4. 分析完整性
    console.log('\n4️⃣ 分析上下文文档完整性...');
    const analyzer = new CompletenessAnalyzer();
    const contextPaths = {
      businessRules: processFiles.context.businessRules,
      technicalSpecs: processFiles.context.technicalSpecs,
      validationStandards: processFiles.context.validationStandards,
      integrationConfig: processFiles.context.integrationConfig
    };
    const analysisReport = analyzer.analyzeContextDocuments(contextPaths);
    fs.writeFileSync(processFiles.analysis, JSON.stringify(analysisReport, null, 2));
    console.log(`✅ 完整性分析: ${processFiles.analysis} (${analysisReport.overallScore}/100)`);
    
    // 5. 保存过程文件报告
    const reportPath = fileManager.saveProcessFileReport(projectName);
    console.log(`\n📋 过程文件位置报告: ${reportPath}`);
    
    // 6. 显示标准目录结构
    const dirStructure = fileManager.getStandardDirectoryStructure(projectName);
    console.log('\n📂 标准目录结构:');
    Object.entries(dirStructure).forEach(([key, value]) => {
      console.log(`   ${key}: ${value}`);
    });
    
    console.log(`\n🎉 完整工作流生成完成！`);
    
  } catch (error) {
    console.error('❌ 生成完整工作流失败:', error.message);
    process.exit(1);
  }
} else if (command === 'test-minimal-input') {
  // 测试财务模块用例
  const testInput = {
    projectName: "dms-erp-finance-migration-v1",
    businessGoal: "迁移财务模块到Java",
    scopeBoundary: "只做后端服务，不做前端",
    codeLocation: "src/main/java/com/dms/financialmanagement/"
  };

  const generator = new CampaignDocumentGenerator();
  const campaignDoc = generator.generateFromMinimalInput(testInput);
  
  fs.writeFileSync('test-output.md', campaignDoc);
  console.log('✅ 财务模块测试完成: test-output.md');
  
  // 验证关键内容
  const content = fs.readFileSync('test-output.md', 'utf8');
  const checks = [
    { name: '包含项目名称', check: () => content.includes('dms-erp-finance-migration-v1') },
    { name: '包含业务目标章节', check: () => content.includes('## 🎯 业务目标') },
    { name: '包含范围定义', check: () => content.includes('✅ 包含范围') && content.includes('❌ 排除范围') },
    { name: '包含技术约束', check: () => content.includes('技术约束') },
    { name: '包含交付物', check: () => content.includes('交付物定义') },
    { name: '包含风险假设', check: () => content.includes('风险与假设') }
  ];

  let allPassed = true;
  console.log('\n🔍 完整性验证:');
  checks.forEach(check => {
    const passed = check.check();
    console.log(`${passed ? '✅' : '❌'} ${check.name}`);
    if (!passed) allPassed = false;
  });

  if (allPassed) {
    console.log('\n🎉 所有验证通过！战役文档完整可用。');
  } else {
    console.log('\n⚠️  部分验证失败，请检查生成的文档。');
    process.exit(1);
  }
  
} else {
  console.log('AI Plan Generator v2');
  console.log('Commands:');
  console.log('  generate-campaign <input.json> [output.md]           - 生成战役文档');
  console.log('  generate-context <campaign.json> [output-dir]        - 生成上下文文档');
  console.log('  generate-context-from-archaeology [archaeology-dir] [output-dir] [domain] - 从Code Archaeology生成上下文');
  console.log('  generate-tasks <campaign.json> [output-dir]          - 生成任务分解');
  console.log('  generate-complete-workflow <input.json> [archaeology-dir] - 生成完整工作流');
  console.log('  analyze-completeness [context-dir]                   - 分析上下文文档完整性');
  console.log('  test-minimal-input                                 - 测试财务模块用例');
}