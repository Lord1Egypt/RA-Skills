const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const { execSync } = require('child_process');

/**
 * 业务测试验证报告生成和上传工具
 * 基于funcpulse技能的业务测试验证结果生成报告并上传到平台
 */

// API配置
const API_CONFIG = {
  baseUrl: 'http://ai-testcase.jd.com',
  endpoint: '/aiCase/api/funcpulse/saveValidationReports',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
};

/**
 * 获取git配置的用户名
 * @returns {string} git用户名或兜底值
 */
function getGitUserName() {
  try {
    const gitUserName = execSync('git config user.name', { encoding: 'utf8', timeout: 5000 }).trim();
    return gitUserName || '未知测试人员';
  } catch (error) {
    console.warn('无法获取git用户名，使用兜底值:', error.message);
    return '未知测试人员';
  }
}

/**
 * 获取代码库地址 - 优先通过git获取远程仓库地址，获取不到则使用工程绝对路径
 * @returns {string} 代码库URL或工程绝对路径
 */
function getCodebaseUrl() {
  try {
    // 尝试获取git远程仓库地址
    const gitRemoteUrl = execSync('git config --get remote.origin.url', { encoding: 'utf8', timeout: 5000 }).trim();
    if (gitRemoteUrl) {
      return gitRemoteUrl;
    }
  } catch (error) {
    console.warn('无法通过git获取远程仓库地址:', error.message);
  }

  // 如果无法获取git远程地址，则返回当前工作目录的绝对路径
  try {
    const absolutePath = process.cwd();
    return absolutePath;
  } catch (error) {
    console.warn('无法获取当前工作目录:', error.message);
    return '未知工程路径';
  }
}

/**
 * 从Markdown报告中提取信息
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {Object} 提取的报告信息
 */
function extractReportInfo(reportContent) {
  const info = {
    testerName: '',
    versionInfo: '',
    reportDate: new Date().toISOString().split('T')[0], // 默认当前日期
    functionName: '',
    codebaseUrl: '',
    involvedRepos: [],
    testCaseCount: 0,
    coveredCases: 0,
    uncoveredCases: 0,
    coverageRate: 0
  };


  // 提取测试人员姓名 - 优先使用git配置的用户名，其次从报告中提取，最后使用兜底值
  info.testerName = getGitUserName();


  // 提取版本信息
  const versionMatch = reportContent.match(/\*\*版本\*\*[:：]?\s*([^\n]+)/);
  if (versionMatch) {
    info.versionInfo = versionMatch[1].trim();
  }

  // 提取报告日期
  const dateMatch = reportContent.match(/\*\*日期\*\*[:：]?\s*(\d{4}-\d{2}-\d{2})/);
  if (dateMatch) {
    info.reportDate = dateMatch[1];
  }

  // 提取功能名称
  const titleMatch = reportContent.match(/#\s+业务测试验证报告[:：]?\s*(.+)/);
  if (titleMatch) {
    info.functionName = titleMatch[1].trim();
  }

  // 提取代码库URL - 优先通过git获取，否则使用报告中的地址
  info.codebaseUrl = getCodebaseUrl();

  // 如果git获取失败且报告中有代码库地址，则使用报告中的地址
  if (!info.codebaseUrl || info.codebaseUrl === '未知工程路径') {
    const repoMatch = reportContent.match(/\*\*代码库地址\*\*[:：]?\s*([^\n]+)/);
    if (repoMatch) {
      info.codebaseUrl = repoMatch[1].trim();
    }
  }
  // 提取涉及的仓库
  const reposMatch = reportContent.match(/\*\*涉及的仓库\*\*[:：]?\s*([^\n]+)/);
  if (reposMatch) {
    info.involvedRepos = reposMatch[1].trim().split(',').map(repo => repo.trim());
  }

  // 提取测试用例统计
  const caseCountMatch = reportContent.match(/\*\*测试用例总数\*\*[:：]?\s*(\d+)/);
  if (caseCountMatch) {
    info.testCaseCount = parseInt(caseCountMatch[1]);
  }

  const coveredMatch = reportContent.match(/\*\*已覆盖用例\*\*[:：]?\s*(\d+)/);
  if (coveredMatch) {
    info.coveredCases = parseInt(coveredMatch[1]);
  }

  const uncoveredMatch = reportContent.match(/\*\*未覆盖用例\*\*[:：]?\s*(\d+)/);
  if (uncoveredMatch) {
    info.uncoveredCases = parseInt(uncoveredMatch[1]);
  }

  // 计算覆盖率
  if (info.testCaseCount > 0) {
    info.coverageRate = ((info.coveredCases / info.testCaseCount) * 100).toFixed(2);
  }

  return info;
}

/**
 * 解析Markdown报告中的缺陷
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {Array} 缺陷列表
 */
function parseDefectsFromReport(reportContent) {
  const defects = [];

  // 按严重程度分割报告内容
  const sections = reportContent.split(/#{2,3}\s+/);

  sections.forEach(section => {
    if (section.includes('缺陷列表')) {
      const criticalDefects = parseCriticalDefects(section);
      defects.push(...criticalDefects);

      const highDefects = parseHighDefects(section);
      defects.push(...highDefects);

      const mediumDefects = parseMediumDefects(section);
      defects.push(...mediumDefects);

      const lowDefects = parseLowDefects(section);
      defects.push(...lowDefects);
    }
  });

  return defects;
}

/**
 * 解析关键缺陷
 */
function parseCriticalDefects(section) {
  const defects = [];
  const defectBlocks = section.split(/\n(?=#{4}\s+)/);

  defectBlocks.forEach(block => {
    if (block.trim() && block.includes('[关键]')) {
      const defect = {
        severity: 'CRITICAL',
        title: extractField(block, '缺陷'),
        requirementId: extractField(block, '关联需求'),
        testCaseId: extractField(block, '关联用例'),
        location: extractField(block, '位置'),
        steps: extractField(block, '重现步骤'),
        expected: extractField(block, '期望结果'),
        actual: extractField(block, '实际结果'),
        impact: extractField(block, '影响'),
        fix: extractField(block, '修复建议')
      };

      if (defect.title) {
        defects.push(defect);
      }
    }
  });

  return defects;
}

/**
 * 解析高优先级缺陷
 */
function parseHighDefects(section) {
  const defects = [];
  const defectBlocks = section.split(/\n(?=#{4}\s+)/);

  defectBlocks.forEach(block => {
    if (block.trim() && block.includes('[高]')) {
      const defect = {
        severity: 'HIGH',
        title: extractField(block, '缺陷'),
        requirementId: extractField(block, '关联需求'),
        testCaseId: extractField(block, '关联用例'),
        location: extractField(block, '位置'),
        description: extractField(block, '描述'),
        impact: extractField(block, '影响'),
        fix: extractField(block, '修复建议')
      };

      if (defect.title) {
        defects.push(defect);
      }
    }
  });

  return defects;
}

/**
 * 解析中优先级缺陷
 */
function parseMediumDefects(section) {
  const defects = [];
  const defectBlocks = section.split(/\n(?=#{4}\s+)/);

  defectBlocks.forEach(block => {
    if (block.trim() && block.includes('[中]')) {
      const defect = {
        severity: 'MEDIUM',
        title: extractField(block, '缺陷'),
        requirementId: extractField(block, '关联需求'),
        testCaseId: extractField(block, '关联用例'),
        details: extractField(block, '详情') || extractField(block, '描述')
      };

      if (defect.title) {
        defects.push(defect);
      }
    }
  });

  return defects;
}

/**
 * 解析低优先级缺陷
 */
function parseLowDefects(section) {
  const defects = [];
  const defectBlocks = section.split(/\n(?=#{4}\s+)/);

  defectBlocks.forEach(block => {
    if (block.trim() && block.includes('[低]')) {
      const defect = {
        severity: 'LOW',
        title: extractField(block, '缺陷'),
        requirementId: extractField(block, '关联需求'),
        testCaseId: extractField(block, '关联用例'),
        details: extractField(block, '详情') || extractField(block, '描述')
      };

      if (defect.title) {
        defects.push(defect);
      }
    }
  });

  return defects;
}

/**
 * 从文本块中提取字段值
 */
function extractField(text, fieldName) {
  const patterns = [
    new RegExp(`${fieldName}[:：]\\s*(.+?)(?=\\n#{4}|\\n##|\\n###|$)`, 's'),
    new RegExp(`${fieldName}[:：]\\s*(.+?)(?=\\n\\n|\\n#{2,3}|$)`, 's'),
    new RegExp(`${fieldName}[:：]\\s*(.+)`, 'i')
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1].trim();
    }
  }

  return '';
}

/**
 * 提取追踪矩阵
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {string} 追踪矩阵内容
 */
function extractTraceabilityMatrix(reportContent) {
  const matrixMatch = reportContent.match(/#{2,3}\\s+需求-用例-代码追踪矩阵[\\s\\S]*?(?=\\n#{2,3}|$)/);
  if (matrixMatch) {
    return matrixMatch[0].replace(/#{2,3}\\s+需求-用例-代码追踪矩阵/, '').trim();
  }
  return '';
}

/**
 * 提取建议
 * @param {string} reportContent - Markdown格式的报告内容
 * @returns {string} 建议列表
 */
function extractRecommendations(reportContent) {
  const recommendations = [];

  // 查找建议部分
  const recommendationsMatch = reportContent.match(/#{2,3}\\s+建议[\\s\\S]*?(?=\\n#{2,3}|$)/);
  if (recommendationsMatch) {
    const recommendationsSection = recommendationsMatch[0];

    // 提取列表项
    const items = recommendationsSection.match(/\\d+\\.\\s*(.+)/g);
    if (items) {
      items.forEach(item => {
        recommendations.push(item.replace(/^\\d+\\.\\s*/, '').trim());
      });
    }
  }

  return recommendations.join('\\n');
}

/**
 * 构建上传请求数据
 * @param {string} reportContent - 完整的Markdown报告内容
 * @param {Object} reportInfo - 提取的报告信息
 * @returns {Object} 上传请求数据
 */
function buildUploadRequestData(reportContent, reportInfo) {
  const defects = parseDefectsFromReport(reportContent);
  const traceabilityMatrix = extractTraceabilityMatrix(reportContent);
  const prioritizedRecommendations = extractRecommendations(reportContent);

  return {
    reportMessage: reportContent,
    testerName: reportInfo.testerName || '未知测试人员',
    versionInfo: reportInfo.versionInfo || '未知版本',
    reportDate: reportInfo.reportDate,
    functionName: reportInfo.functionName || '未知功能',
    codebaseUrl: reportInfo.codebaseUrl || '',
    involvedRepos: reportInfo.involvedRepos.join(', ') || '未知仓库',
    testCaseCount: reportInfo.testCaseCount || 0,
    coveredCases: reportInfo.coveredCases || 0,
    uncoveredCases: reportInfo.uncoveredCases || 0,
    coverageRate: reportInfo.coverageRate || 0,
    defects: defects,
    traceabilityMatrix: traceabilityMatrix,
    prioritizedRecommendations: prioritizedRecommendations
  };
}

/**
 * 发送HTTP请求
 * @param {Object} options - HTTP请求选项
 * @param {string} data - 请求数据
 * @returns {Promise} 响应Promise
 */
function sendHttpRequest(options, data) {
  return new Promise((resolve, reject) => {
    const protocol = options.protocol === 'https:' ? https : http;
    const req = protocol.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const parsedData = JSON.parse(responseData);
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            data: parsedData
          });
        } catch (error) {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            data: responseData
          });
        }
      });
    });
    
    req.on('error', (error) => {
      reject(error);
    });
    
    if (data) {
      req.write(data);
    }
    
    req.end();
  });
}

/**
 * 上传报告到API
 * @param {string} reportContent - 完整的Markdown报告内容
 * @param {Object} reportInfo - 提取的报告信息（可选）
 * @returns {Promise<Object>} 上传结果
 */
async function uploadReportToAPI(reportContent, reportInfo = null) {
  try {
    // 如果未提供reportInfo，则自动提取
    if (!reportInfo) {
      reportInfo = extractReportInfo(reportContent);
    }
    
    // 验证报告内容
    if (!validateReportContent(reportContent)) {
      throw new Error('报告内容验证失败：报告内容不完整或无效');
    }
    
    // 构建请求数据
    const requestData = buildUploadRequestData(reportContent, reportInfo);
    
    // 打印请求参数
    console.log('=== 请求参数 ===');
    console.log('URL:', API_CONFIG.baseUrl + API_CONFIG.endpoint);
    console.log('Method:', API_CONFIG.method);
    console.log('Headers:', API_CONFIG.headers);
    console.log('Request Data:', JSON.stringify(requestData, null, 2));
    
    // 准备HTTP请求
    const url = new URL(API_CONFIG.baseUrl + API_CONFIG.endpoint);
    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: API_CONFIG.method,
      headers: {
        ...API_CONFIG.headers,
        'Content-Length': Buffer.byteLength(JSON.stringify(requestData))
      }
    };
    
    console.log('正在上传报告到:', API_CONFIG.baseUrl + API_CONFIG.endpoint);
    
    // 发送请求
    const response = await sendHttpRequest(options, JSON.stringify(requestData));
    
    // 打印响应参数
    console.log('=== 响应参数 ===');
    console.log('Status Code:', response.statusCode);
    console.log('Headers:', response.headers);
    console.log('Response Data:', JSON.stringify(response.data, null, 2));
    
    // 处理响应
    if (response.statusCode >= 200 && response.statusCode < 300) {
      console.log('报告上传成功');
      return response.data;
    } else {
      console.error('报告上传失败，状态码:', response.statusCode);
      throw new Error(`API请求失败: ${response.statusCode} - ${JSON.stringify(response.data)}`);
    }
  } catch (error) {
    console.error('上传报告时发生错误:', error.message);
    throw error;
  }
}

/**
 * 验证报告内容
 * @param {string} reportContent - 报告内容
 * @returns {boolean} 是否有效
 */
function validateReportContent(reportContent) {
  if (!reportContent || reportContent.trim().length === 0) {
    return false;
  }
  
  // 检查是否包含基本结构 - 标题和缺陷列表部分
  if (!reportContent.includes('#') || (!reportContent.includes('缺陷') && !reportContent.includes('发现'))) {
    return false;
  }
  
  return true;
}

/**
 * 将远程报告URL添加到原始报告文件
 * @param {string} filePath - 报告文件路径
 * @param {string} remoteUrl - 远程报告URL
 */
function addRemoteReportUrl(filePath, remoteUrl) {
  try {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // 如果已经存在远程URL，则不重复添加
    if (content.includes('远程报告地址')) {
      return;
    }
    
    // 在文件末尾添加远程报告地址
    const remoteUrlSection = `\\n\\n---\\n\\n## 远程报告地址\\n\\n[查看在线报告](${remoteUrl})\\n`;
    content += remoteUrlSection;
    
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('已添加远程报告地址到文件:', filePath);
  } catch (error) {
    console.error('添加远程报告地址失败:', error.message);
  }
}

/**
 * 获取Git仓库信息
 * @param {string} repoPath - 仓库路径
 * @returns {Object} 仓库信息
 */
function getGitRepoInfo(repoPath) {
  try {
    const remoteUrl = execSync('git config --get remote.origin.url', { 
      cwd: repoPath,
      encoding: 'utf8' 
    }).trim();
    
    const branch = execSync('git rev-parse --abbrev-ref HEAD', { 
      cwd: repoPath,
      encoding: 'utf8' 
    }).trim();
    
    const latestCommit = execSync('git rev-parse HEAD', { 
      cwd: repoPath,
      encoding: 'utf8' 
    }).trim();
    
    return {
      remoteUrl,
      branch,
      latestCommit,
      path: repoPath
    };
  } catch (error) {
    console.error('获取Git仓库信息失败:', error.message);
    return {
      remoteUrl: '',
      branch: '',
      latestCommit: '',
      path: repoPath
    };
  }
}

/**
 * 分析多仓库变更
 * @param {Array} repoPaths - 仓库路径列表
 * @returns {Array} 仓库变更信息
 */
function analyzeMultiRepoChanges(repoPaths) {
  const repoInfos = [];
  
  repoPaths.forEach(repoPath => {
    if (fs.existsSync(path.join(repoPath, '.git'))) {
      const repoInfo = getGitRepoInfo(repoPath);
      
      // 获取最近的提交信息
      try {
        const recentCommits = execSync('git log --oneline -10', { 
          cwd: repoPath,
          encoding: 'utf8' 
        }).trim().split('\\n');
        
        repoInfo.recentCommits = recentCommits;
      } catch (error) {
        repoInfo.recentCommits = [];
      }
      
      repoInfos.push(repoInfo);
    }
  });
  
  return repoInfos;
}

// 导出函数供外部使用
module.exports = {
  extractReportInfo,
  parseDefectsFromReport,
  buildUploadRequestData,
  uploadReportToAPI,
  addRemoteReportUrl,
  validateReportContent,
  getGitRepoInfo,
  analyzeMultiRepoChanges
};

// 如果直接运行此脚本，则执行单个报告上传
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('用法:');
    console.log('  node generate-validation-report.js <报告文件路径>');
    console.log('  node generate-validation-report.js <报告文件路径> --repos <仓库路径1,仓库路径2,...>');
    process.exit(1);
  }
  
  const filePath = args[0];
  let repoPaths = [];
  
  // 解析仓库路径参数
  const reposIndex = args.indexOf('--repos');
  if (reposIndex !== -1 && reposIndex + 1 < args.length) {
    repoPaths = args[reposIndex + 1].split(',').map(p => p.trim());
  }
  
  console.log('正在上传报告:', filePath);
  if (repoPaths.length > 0) {
    console.log('分析的仓库:', repoPaths);
  }
  
  uploadValidationReportFromFile(filePath, repoPaths)
    .then(result => {
      console.log('报告上传成功');
      console.log('远程报告地址:', result.message);
    })
    .catch(error => {
      console.error('报告上传失败:', error.message);
      process.exit(1);
    });
}

/**
 * 从文件上传报告的便捷函数
 * @param {string} filePath - 报告文件路径
 * @param {Array} repoPaths - 仓库路径列表
 * @returns {Promise<Object>} 上传结果
 */
async function uploadValidationReportFromFile(filePath, repoPaths = []) {
  const reportContent = fs.readFileSync(filePath, 'utf8');
  
  // 如果有仓库路径，分析多仓库变更
  if (repoPaths.length > 0) {
    const repoInfos = analyzeMultiRepoChanges(repoPaths);
    console.log('多仓库分析结果:', repoInfos);
  }
  
  const result = await uploadReportToAPI(reportContent);
  
  // 添加远程报告地址到原始文件
  if (result.message) {
    addRemoteReportUrl(filePath, result.message);
  }
  
  return result;
}
