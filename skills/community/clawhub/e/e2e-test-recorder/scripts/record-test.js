/**
 * 端到端测试录制模块
 * 支持录制完整的测试流程
 */

const { ScreenRecorder } = require('./record-browser');
const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const ora = require('ora');

/**
 * 录制端到端测试
 * @param {Object} config 测试配置
 */
async function recordE2ETest(config) {
  const {
    url,
    testName = 'E2E Test',
    testSteps = [],
    output = './recordings/e2e-test.mp4',
    headless = false,
    annotations = true,
    timeout = 60000,
    viewport = { width: 1920, height: 1080 }
  } = config;

  const spinner = ora(`准备录制测试: ${testName}`).start();
  
  try {
    // 创建录制器
    const recorder = new ScreenRecorder({
      outputPath: output,
      headless,
      viewport,
      fps: 24,
      quality: 85
    });

    spinner.text = `启动浏览器并访问: ${url}`;
    
    // 开始录制
    await recorder.startRecording(url);
    
    spinner.succeed(chalk.green('✅ 录制已开始'));
    console.log(chalk.cyan(`📋 测试名称: ${testName}`));
    console.log(chalk.cyan(`🔗 测试URL: ${url}`));
    console.log(chalk.cyan(`📝 测试步骤数: ${testSteps.length}`));
    
    // 执行测试步骤
    if (testSteps.length > 0) {
      console.log(chalk.blue('\n🔄 开始执行测试步骤:'));
      
      for (let i = 0; i < testSteps.length; i++) {
        const step = testSteps[i];
        const stepNumber = i + 1;
        
        console.log(chalk.cyan(`  步骤 ${stepNumber}/${testSteps.length}: ${step.description || step.action}`));
        
        // 添加标注（如果启用）
        if (annotations && step.description) {
          await recorder.addAnnotation(`步骤 ${stepNumber}: ${step.description}`, { x: 50, y: 50 + (i * 40) });
          await recorder.page.waitForTimeout(500); // 等待标注显示
        }
        
        // 执行步骤
        await recorder.executeAction(step);
        
        // 步骤间延迟
        const delay = step.delay || 1000;
        if (delay > 0) {
          await recorder.page.waitForTimeout(delay);
        }
        
        // 验证步骤结果（如果有验证器）
        if (step.validator) {
          const isValid = await validateStep(recorder.page, step.validator);
          if (!isValid) {
            console.log(chalk.yellow(`⚠️  步骤 ${stepNumber} 验证失败，继续执行`));
          }
        }
      }
      
      console.log(chalk.green('\n✅ 所有测试步骤执行完成'));
    } else {
      // 如果没有步骤，等待一段时间
      console.log(chalk.yellow('⏳ 无测试步骤，等待中...'));
      await recorder.page.waitForTimeout(timeout);
    }
    
    // 停止录制
    const result = await recorder.stopRecording();
    
    console.log(chalk.green('\n🎬 测试录制完成'));
    console.log(chalk.cyan('📊 录制结果:'));
    console.log(chalk.cyan(`   文件: ${result.filePath}`));
    console.log(chalk.cyan(`   时长: ${result.duration.toFixed(2)} 秒`));
    console.log(chalk.cyan(`   大小: ${(result.fileSize / (1024 * 1024)).toFixed(2)} MB`));
    
    // 生成测试报告
    const report = generateTestReport(config, result);
    await saveTestReport(report, output);
    
    return {
      ...result,
      report,
      testName,
      stepCount: testSteps.length,
      success: true
    };
    
  } catch (error) {
    spinner.fail(chalk.red(`❌ 测试录制失败: ${error.message}`));
    console.error(chalk.red('错误详情:'), error);
    throw error;
  }
}

/**
 * 验证测试步骤
 */
async function validateStep(page, validator) {
  try {
    if (typeof validator === 'function') {
      return await validator(page);
    }
    
    if (validator.selector) {
      const element = await page.$(validator.selector);
      if (!element) return false;
      
      if (validator.text) {
        const text = await page.evaluate(el => el.textContent, element);
        return text.includes(validator.text);
      }
      
      return true;
    }
    
    return true;
  } catch (error) {
    console.error(chalk.red('验证失败:'), error);
    return false;
  }
}

/**
 * 生成测试报告
 */
function generateTestReport(config, result) {
  const timestamp = new Date().toISOString();
  
  return {
    metadata: {
      testName: config.testName,
      url: config.url,
      timestamp,
      duration: result.duration,
      fileSize: result.fileSize,
      filePath: result.filePath
    },
    config: {
      headless: config.headless,
      annotations: config.annotations,
      viewport: config.viewport,
      stepCount: config.testSteps.length
    },
    steps: config.testSteps.map((step, index) => ({
      stepNumber: index + 1,
      description: step.description,
      action: step.action,
      selector: step.selector,
      delay: step.delay
    })),
    result: {
      success: true,
      duration: result.duration,
      frameCount: result.frameCount,
      outputFile: result.filePath
    },
    systemInfo: {
      nodeVersion: process.version,
      platform: process.platform,
      timestamp
    }
  };
}

/**
 * 保存测试报告
 */
async function saveTestReport(report, videoPath) {
  const reportDir = path.dirname(videoPath);
  const reportName = path.basename(videoPath, path.extname(videoPath));
  const reportPath = path.join(reportDir, `${reportName}.json`);
  
  await fs.writeJson(reportPath, report, { spaces: 2 });
  console.log(chalk.green(`📄 测试报告已保存: ${reportPath}`));
  
  return reportPath;
}

/**
 * 录制API测试
 */
async function recordAPITest(config) {
  const {
    apiUrl,
    tests = [],
    output = './recordings/api-test.gif',
    viewport = { width: 1280, height: 720 }
  } = config;

  console.log(chalk.cyan('🚀 开始录制API测试'));
  console.log(chalk.cyan(`🔗 API地址: ${apiUrl}`));
  console.log(chalk.cyan(`📋 测试数量: ${tests.length}`));
  
  // 创建简单的HTML页面用于显示API测试结果
  const htmlContent = generateAPITestPage(apiUrl, tests);
  const htmlPath = path.join(path.dirname(output), 'api-test-page.html');
  await fs.writeFile(htmlPath, htmlContent);
  
  const fileUrl = `file://${htmlPath}`;
  
  // 定义测试步骤
  const testSteps = tests.map((test, index) => ({
    description: `测试 ${index + 1}: ${test.name}`,
    action: 'evaluate',
    text: `
      (function() {
        const testIndex = ${index};
        const test = ${JSON.stringify(test)};
        runAPITest(testIndex, test);
      })();
    `,
    delay: 3000
  }));
  
  // 录制测试
  return await recordE2ETest({
    url: fileUrl,
    testName: 'API测试录制',
    testSteps,
    output,
    headless: true,
    annotations: false,
    viewport
  });
}

/**
 * 生成API测试页面HTML
 */
function generateAPITestPage(apiUrl, tests) {
  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API测试录制</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            padding: 40px;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 40px;
            font-size: 2.5em;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }
        .api-url {
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            font-family: monospace;
            font-size: 1.2em;
            text-align: center;
        }
        .test-list {
            display: grid;
            gap: 20px;
        }
        .test-item {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s ease;
            opacity: 0.5;
            transform: translateY(20px);
        }
        .test-item.active {
            opacity: 1;
            transform: translateY(0);
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .test-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .test-name {
            font-size: 1.3em;
            font-weight: bold;
        }
        .test-status {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        .status-pending {
            background: rgba(255, 193, 7, 0.3);
            color: #ffc107;
        }
        .status-running {
            background: rgba(0, 123, 255, 0.3);
            color: #007bff;
            animation: pulse 1.5s infinite;
        }
        .status-success {
            background: rgba(40, 167, 69, 0.3);
            color: #28a745;
        }
        .status-error {
            background: rgba(220, 53, 69, 0.3);
            color: #dc3545;
        }
        .test-details {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .detail-row {
            display: flex;
            margin-bottom: 8px;
        }
        .detail-label {
            width: 120px;
            font-weight: bold;
            opacity: 0.8;
        }
        .detail-value {
            flex: 1;
            font-family: monospace;
            word-break: break-all;
        }
        .response {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
            max-height: 200px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 0.9em;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }
        .progress-bar {
            height: 4px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 2px;
            margin-top: 20px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00b09b, #96c93d);
            width: 0%;
            transition: width 1s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔌 API测试录制</h1>
        
        <div class="api-url">
            📍 ${apiUrl}
        </div>
        
        <div class="test-list" id="testList">
            ${tests.map((test, index) => `
            <div class="test-item" id="test-${index}">
                <div class="test-header">
                    <div class="test-name">${test.name}</div>
                    <div class="test-status status-pending">等待中</div>
                </div>
                <div class="test-details" style="display: none;">
                    <div class="detail-row">
                        <div class="detail-label">端点:</div>
                        <div class="detail-value">${test.endpoint}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">方法:</div>
                        <div class="detail-value">${test.method}</div>
                    </div>
                    <div class="detail-row">
                        <div class="detail-label">预期状态:</div>
                        <div class="detail-value">${test.expectedStatus}</div>
                    </div>
                    <div class="response" id="response-${index}"></div>
                </div>
            </div>
            `).join('')}
        </div>
        
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill"></div>
        </div>
    </div>

    <script>
        const tests = ${JSON.stringify(tests)};
        const apiUrl = '${apiUrl}';
        let currentTestIndex = 0;
        
        function runAPITest(index, test) {
            const testElement = document.getElementById(\`test-\${index}\`);
            const statusElement = testElement.querySelector('.test-status');
            const detailsElement = testElement.querySelector('.test-details');
            const responseElement = document.getElementById(\`response-\${index}\`);
            
            // 激活当前测试项
            testElement.classList.add('active');
            detailsElement.style.display = 'block';
            statusElement.textContent = '运行中';
            statusElement.className = 'test-status status-running';
            
            // 更新进度条
            const progress = ((index + 1) / tests.length) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
            
            // 执行API请求
            const url = apiUrl + test.endpoint;
            const options = {
                method: test.method,
                headers: {
                    'Content-Type': 'application/json'
                }
            };
            
            if (test.data) {
                options.body = JSON.stringify(test.data);
            }
            
            fetch(url, options)
                .then(async response => {
                    const responseData = await response.json().catch(() => ({}));
                    
                    // 显示响应
                    responseElement.textContent = JSON.stringify(responseData, null, 2);
                    
                    // 检查状态码
                    if (response.status === test.expectedStatus) {
                        statusElement.textContent = '成功';
                        statusElement.className = 'test-status status-success';
                    } else {
                        statusElement.textContent = \`失败: \${response.status}\`;
                        statusElement.className = 'test-status status-error';
                    }
                })
                .catch(error => {
                    responseElement.textContent = \`错误: \${error.message}\`;
                    statusElement.textContent = '错误';
                    statusElement.className = 'test-status status-error';
                });
        }
        
        // 初始隐藏所有详情
        document.querySelectorAll('.test-details').forEach(el => {
            el.style.display = 'none';
        });
    </script>
</body>
</html>
  `;
}

/**
 * 批量录制测试套件
 */
async function recordTestSuite(suiteConfig) {
  const results = [];
  
  console.log(chalk.cyan(`🚀 开始录制测试套件: ${suiteConfig.name}`));
  console.log(chalk.cyan(`📋 包含 ${suiteConfig.tests.length} 个测试`));
  
  for (let i = 0; i < suiteConfig.tests.length; i++) {
    const testConfig = suiteConfig.tests[i];
    const testNumber = i + 1;
    
    console.log(chalk.blue(`\n📝 测试 ${testNumber}/${suiteConfig.tests.length}: ${testConfig.testName}`));
    
    try {
      const result = await recordE2ETest(testConfig);
      results.push({
        ...result,
        testNumber,
        suiteName: suiteConfig.name
      });
      
      console.log(chalk.green(`✅ 测试 ${testNumber} 录制完成`));
    } catch (error) {
      console.error(chalk.red(`❌ 测试 ${testNumber} 录制失败: ${error.message}`));
      results.push({
        testNumber,
        suiteName: suiteConfig.name,
        success: false,
        error: error.message
      });
    }
    
    // 测试间延迟
    if (suiteConfig.delayBetweenTests) {
      await new Promise(resolve => setTimeout(resolve, suiteConfig.delayBetweenTests));
    }
  }
  
  // 生成套件报告
  const suiteReport = {
    suiteName: suiteConfig.name,
    totalTests: suiteConfig.tests.length,
    successfulTests: results.filter(r => r.success).length,
    failedTests: results.filter(r => !r.success).length,
    results: results.map(r => ({
      testNumber: r.testNumber,
      testName: r.testName,
      success: r.success,
      duration: r.duration,
      filePath: r.filePath
    }))
  };
  
  const reportPath = path.join(suiteConfig.outputDir || './recordings', `${suiteConfig.name}-report.json`);
  await fs.writeJson(reportPath, suiteReport, { spaces: 2 });
  
  console.log(chalk.green(`\n🎉 测试套件录制完成`));
  console.log(chalk.cyan(`📊 结果: ${suiteReport.successfulTests}/${suiteReport.totalTests} 成功`));
  console.log(chalk.cyan(`📄 报告: ${reportPath}`));
  
  return suiteReport;
}

module.exports = {
  recordE2ETest,
  recordAPITest,
  recordTestSuite,
  generateTestReport,
  saveTestReport
};