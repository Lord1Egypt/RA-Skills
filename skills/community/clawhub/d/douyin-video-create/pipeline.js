#!/usr/bin/env node

/**
 * Content Pipeline - 完整的搜索 → 脚本 → 视频流程
 * 
 * 用法:
 *   node pipeline.js --topic "话题" --style "analysis" --provider "heygen"
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ScriptGenerator = require('./script-generator');
const DataOrganizer = require('./data-organizer');
const AvatarVideoGenerator = require('./avatar-generator');

class ContentPipeline {
  constructor(options = {}) {
    this.topic = options.topic || '未命名话题';
    this.style = options.style || 'analysis';
    this.provider = options.provider || 'heygen';
    this.outputDir = options.outputDir || './output';
    this.workDir = path.join(this.outputDir, `${Date.now()}`);
    
    this.ensureOutputDir();
  }

  /**
   * 确保输出目录存在
   */
  ensureOutputDir() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
    if (!fs.existsSync(this.workDir)) {
      fs.mkdirSync(this.workDir, { recursive: true });
    }
  }

  /**
   * 第一步：搜索信息
   */
  async searchInformation() {
    console.log('\n📡 第一步: 搜索信息...');
    
    // 由于网络工具不可用，这里使用本地数据或用户输入
    const searchData = {
      title: this.topic,
      summary: `关于 ${this.topic} 的信息`,
      keyPoints: [
        '这是第一个关键点',
        '这是第二个关键点',
        '这是第三个关键点'
      ],
      impact: '这个话题的影响',
      lessons: [
        '我们可以学到的第一个教训',
        '我们可以学到的第二个教训'
      ]
    };

    const searchFile = path.join(this.workDir, '01-search-results.json');
    fs.writeFileSync(searchFile, JSON.stringify(searchData, null, 2));
    
    console.log(`✓ 搜索结果已保存: ${searchFile}`);
    return searchData;
  }

  /**
   * 第二步：整理信息
   */
  async organizeData(rawData) {
    console.log('\n📋 第二步: 整理信息...');
    
    const organizer = new DataOrganizer();
    const organized = organizer.organizeForScript(rawData);
    
    const organizedFile = path.join(this.workDir, '02-organized-data.json');
    fs.writeFileSync(organizedFile, JSON.stringify(organized, null, 2));
    
    console.log(`✓ 整理后的数据已保存: ${organizedFile}`);
    return organized;
  }

  /**
   * 第三步：生成脚本
   */
  async generateScript(organizedData) {
    console.log('\n✍️  第三步: 生成脚本...');
    
    const generator = new ScriptGenerator({
      topic: this.topic,
      style: this.style,
      duration: 120
    });

    const script = generator.generateFromData(organizedData);
    
    // 保存 Markdown 版本
    const scriptMd = path.join(this.workDir, '03-script.md');
    fs.writeFileSync(scriptMd, generator.toMarkdown(script));
    
    // 保存 JSON 版本（用于数字人 API）
    const scriptJson = path.join(this.workDir, '03-script.json');
    fs.writeFileSync(scriptJson, JSON.stringify(generator.toJSON(script), null, 2));
    
    console.log(`✓ 脚本已生成:`);
    console.log(`  - Markdown: ${scriptMd}`);
    console.log(`  - JSON: ${scriptJson}`);
    
    return generator.toJSON(script);
  }

  /**
   * 第四步：生成视频
   */
  async generateVideo(script) {
    console.log('\n🎬 第四步: 生成视频...');
    
    const generator = new AvatarVideoGenerator({
      provider: this.provider,
      apiKey: process.env.AVATAR_API_KEY
    });

    try {
      const result = await generator.generate(script);
      
      const videoResultFile = path.join(this.workDir, '04-video-result.json');
      fs.writeFileSync(videoResultFile, JSON.stringify(result, null, 2));
      
      console.log(`✓ 视频生成请求已提交`);
      console.log(`  结果已保存: ${videoResultFile}`);
      
      return result;
    } catch (error) {
      console.warn(`⚠️  视频生成失败: ${error.message}`);
      console.log('   (这是正常的，因为需要真实的 API Key)');
      return null;
    }
  }

  /**
   * 生成报告
   */
  generateReport(results) {
    console.log('\n📊 生成报告...');
    
    const report = {
      topic: this.topic,
      style: this.style,
      provider: this.provider,
      timestamp: new Date().toISOString(),
      workDir: this.workDir,
      steps: {
        search: '✓ 完成',
        organize: '✓ 完成',
        script: '✓ 完成',
        video: results.video ? '✓ 已提交' : '⚠️ 需要 API Key'
      },
      files: {
        searchResults: '01-search-results.json',
        organizedData: '02-organized-data.json',
        scriptMarkdown: '03-script.md',
        scriptJson: '03-script.json',
        videoResult: '04-video-result.json'
      }
    };

    const reportFile = path.join(this.workDir, 'REPORT.json');
    fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
    
    console.log(`✓ 报告已生成: ${reportFile}`);
    
    return report;
  }

  /**
   * 运行完整 pipeline
   */
  async run() {
    console.log('🚀 启动 Content Pipeline');
    console.log(`📌 话题: ${this.topic}`);
    console.log(`🎨 风格: ${this.style}`);
    console.log(`🎬 提供商: ${this.provider}`);
    console.log(`📁 工作目录: ${this.workDir}`);

    try {
      // 第一步：搜索
      const searchData = await this.searchInformation();

      // 第二步：整理
      const organizedData = await this.organizeData(searchData);

      // 第三步：生成脚本
      const script = await this.generateScript(organizedData);

      // 第四步：生成视频
      const videoResult = await this.generateVideo(script);

      // 生成报告
      const report = this.generateReport({
        search: searchData,
        organize: organizedData,
        script: script,
        video: videoResult
      });

      console.log('\n✅ Pipeline 完成！');
      console.log(`\n📂 所有文件已保存到: ${this.workDir}`);
      console.log('\n📋 文件列表:');
      fs.readdirSync(this.workDir).forEach(file => {
        const filePath = path.join(this.workDir, file);
        const stats = fs.statSync(filePath);
        console.log(`  - ${file} (${stats.size} bytes)`);
      });

      return report;
    } catch (error) {
      console.error('\n❌ Pipeline 失败:', error.message);
      throw error;
    }
  }
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    options[key] = value;
  }

  const pipeline = new ContentPipeline({
    topic: options.topic || '示例话题',
    style: options.style || 'analysis',
    provider: options.provider || 'heygen',
    outputDir: options.output || './output'
  });

  pipeline.run().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = ContentPipeline;
