/**
 * 过程文件管理器
 * 管理AI Plan Generator工作流中的所有过程文件位置
 */

const fs = require('fs');
const path = require('path');

class ProcessFileManager {
  constructor(baseDir = '/Users/admin/.openclaw/workspace') {
    this.baseDir = baseDir;
    this.processFiles = {
      input: null,
      campaign: null,
      tasks: null,
      context: null,
      analysis: null,
      archaeology: null
    };
  }

  /**
   * 设置过程文件位置
   */
  setProcessFileLocations(inputFile, projectName) {
    const projectDir = path.join(this.baseDir, projectName);
    
    // 创建项目目录
    fs.mkdirSync(projectDir, { recursive: true });
    
    // 输入文件位置
    this.processFiles.input = path.resolve(inputFile);
    
    // 战役文档位置
    this.processFiles.campaign = path.join(projectDir, `${projectName}-campaign.md`);
    
    // 任务分解位置
    const tasksDir = path.join(projectDir, 'task-decomposition');
    fs.mkdirSync(tasksDir, { recursive: true });
    this.processFiles.tasks = {
      json: path.join(tasksDir, 'tasks.json'),
      markdown: path.join(tasksDir, 'tasks.md'),
      clawteam: path.join(tasksDir, 'clawteam-tasks.json')
    };
    
    // 上下文文档位置
    const contextDir = path.join(projectDir, 'context-documents');
    fs.mkdirSync(contextDir, { recursive: true });
    this.processFiles.context = {
      businessRules: path.join(contextDir, 'business-rules.json'),
      technicalSpecs: path.join(contextDir, 'technical-specs.yaml'),
      validationStandards: path.join(contextDir, 'validation-standards.md'),
      integrationConfig: path.join(contextDir, 'integration-config.json')
    };
    
    // 分析报告位置
    this.processFiles.analysis = path.join(contextDir, 'analysis-report.json');
    
    return this.processFiles;
  }

  /**
   * 设置Code Archaeology位置
   */
  setArchaeologyLocation(archaeologyDir) {
    // 验证Code Archaeology目录结构
    const resolvedPath = path.resolve(archaeologyDir);
    
    // 检查是否为统一根目录结构
    if (fs.existsSync(path.join(resolvedPath, 'results'))) {
      this.processFiles.archaeology = {
        root: resolvedPath,
        results: path.join(resolvedPath, 'results'),
        process: path.join(resolvedPath, 'process'), 
        source: path.join(resolvedPath, 'source'),
        status: path.join(resolvedPath, 'zbs_php_archaeology_status.json')
      };
    } else {
      // 扁平结构（向后兼容）
      this.processFiles.archaeology = resolvedPath;
    }
    
    return this.processFiles;
  }

  /**
   * 生成过程文件位置报告
   */
  generateProcessFileReport() {
    return {
      timestamp: new Date().toISOString(),
      baseDirectory: this.baseDir,
      files: {
        input: this.processFiles.input,
        campaign: this.processFiles.campaign,
        tasks: this.processFiles.tasks,
        context: this.processFiles.context,
        analysis: this.processFiles.analysis,
        archaeology: this.processFiles.archaeology
      }
    };
  }

  /**
   * 保存过程文件位置报告
   */
  saveProcessFileReport(projectName) {
    const report = this.generateProcessFileReport();
    const reportPath = path.join(this.baseDir, projectName, 'process-files-report.json');
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    return reportPath;
  }

  /**
   * 获取标准目录结构
   */
  getStandardDirectoryStructure(projectName) {
    return {
      projectRoot: `${projectName}/`,
      input: `${projectName}/input.json (源输入文件)`,
      campaign: `${projectName}/${projectName}-campaign.md`,
      tasks: `${projectName}/task-decomposition/`,
      context: `${projectName}/context-documents/`,
      archaeology: `zbs_php_code_archaeology/ (源分析成果)`
    };
  }
}

module.exports = ProcessFileManager;