#!/usr/bin/env node

/**
 * 新闻简报发布脚本
 * 生成简报并发布到飞书
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function main() {
  console.log('=== 开始新闻简报发布流程 ===');
  
  const scriptDir = __dirname;
  const briefScript = path.join(scriptDir, 'news-brief.js');
  const latestBriefFile = path.join(scriptDir, 'latest-brief.md');
  const historyDir = path.join(scriptDir, 'history');
  
  try {
    // 1. 生成新闻简报
    console.log('1. 生成新闻简报...');
    const { stdout, stderr } = await execPromise(`node "${briefScript}" --run-now`);
    console.log(stdout);
    if (stderr) console.error(stderr);
    
    // 2. 等待文件更新（新闻简报脚本可能需要时间）
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 3. 读取最新简报
    console.log('2. 读取简报内容...');
    let briefContent;
    
    // 直接读取今天的历史文件（新闻简报脚本保存到这里）
    const today = new Date();
    const dateStr = today.toISOString().split('T')[0].replace(/-/g, '-');
    const todayFile = path.join(historyDir, `${dateStr}.md`);
    
    if (fs.existsSync(todayFile)) {
      briefContent = fs.readFileSync(todayFile, 'utf-8');
      console.log(`从今天的历史文件 ${dateStr}.md 读取简报`);
      
      // 同时更新latest-brief.md以便其他用途
      fs.writeFileSync(latestBriefFile, briefContent);
      console.log('已更新latest-brief.md文件');
    } else {
      // 如果今天的历史文件不存在，查找最新的历史文件
      const files = fs.readdirSync(historyDir)
        .filter(f => f.endsWith('.md'))
        .sort()
        .reverse();
      
      if (files.length > 0) {
        const latestFile = path.join(historyDir, files[0]);
        briefContent = fs.readFileSync(latestFile, 'utf-8');
        console.log(`从最新历史文件 ${files[0]} 读取简报`);
        
        // 更新latest-brief.md
        fs.writeFileSync(latestBriefFile, briefContent);
        console.log('已更新latest-brief.md文件');
      } else {
        throw new Error('找不到简报文件');
      }
    }
    
    // 4. 显示简报内容（在实际部署中，这里会调用OpenClaw的message工具）
    console.log('3. 简报内容预览（前500字符）:');
    console.log(briefContent.substring(0, 500) + '...');
    
    // 5. 这里应该是调用OpenClaw message工具发布到飞书的代码
    // 由于我们是在OpenClaw环境中运行，可以通过cron任务的delivery配置自动发布
    console.log('4. 简报已准备好发布到飞书');
    console.log('注意：实际发布由OpenClaw cron任务的delivery配置处理');
    
    // 返回简报内容，供OpenClaw使用
    return briefContent;
    
  } catch (error) {
    console.error('新闻简报发布失败:', error.message);
    throw error;
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  main().catch(error => {
    console.error('脚本执行失败:', error);
    process.exit(1);
  });
}

module.exports = main;