#!/usr/bin/env node

/**
 * Design Analysis Skill - OpenClaw Wrapper
 * 提供给OpenClaw调用的封装接口
 */

const { designAnalysis } = require('./index');

/**
 * 执行设计分析任务
 * OpenClaw会调用此函数，传入参数如下：
 *
 * @param {Object} params
 * @param {string} params.input_folder - 设计素材文件夹路径
 * @param {string} params.output_file - HTML输出路径
 * @param {string} [params.title] - 演示文档标题
 * @param {Object} [params.dimensions] - 页面尺寸 {width, height}
 * @param {Object} [params.layout] - 布局比例 {textWidth, imageWidth}
 * @param {Array} [params.sections] - 自定义章节配置
 * @param {Object} params.context - OpenClaw上下文信息
 */
async function run(params) {
  console.log('🎨 Design Analysis Skill 启动');
  console.log('📥 接收参数:', JSON.stringify(params, null, 2));

  try {
    // 参数验证和默认值处理
    const inputFolder = params.input_folder || params.inputFolder;
    const outputFile = params.output_file || params.outputFile;

    if (!inputFolder) {
      throw new Error('input_folder/inputFolder 是必填参数');
    }
    if (!outputFile) {
      throw new Error('output_file/outputFile 是必填参数');
    }

    const result = await designAnalysis({
      inputFolder: inputFolder,
      outputFile: outputFile,
      title: params.title || '设计分析演示',
      dimensions: params.dimensions || { width: 1920, height: 1280 },
      layout: params.layout || { textWidth: 30, imageWidth: 70 },
      sections: params.sections
    });

    if (result.success) {
      console.log('✅ 分析完成');
      return {
        status: 'success',
        result: result,
        message: `设计分析完成，生成 ${result.totalPages} 页HTML文档`
      };
    } else {
      console.error('❌ 分析失败:', result.error);
      return {
        status: 'error',
        error: result.error,
        message: '设计分析失败'
      };
    }
  } catch (error) {
    console.error('❌ Skill执行异常:', error);
    return {
      status: 'error',
      error: error.message,
      message: 'Skill执行异常'
    };
  }
}

// 命令行测试模式
if (require.main === module && process.argv.length >= 4) {
  const [inputFolder, outputFile, title] = process.argv.slice(2);

  run({
    input_folder: inputFolder,
    output_file: outputFile,
    title: title
  }).then(result => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.status === 'success' ? 0 : 1);
  }).catch(error => {
    console.error('执行失败:', error);
    process.exit(1);
  });
} else if (require.main === module) {
  console.log(`
设计分析技能 - 用法测试:
  node run.js <输入文件夹> <输出HTML文件> [标题]

示例:
  node run.js ~/Desktop/01.DesignAnalysis ~/Desktop/output.html "设计分析报告"
  `);
}

module.exports = { run };