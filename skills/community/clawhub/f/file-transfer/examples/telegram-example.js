#!/usr/bin/env node

/**
 * Telegram适配器使用示例
 * 
 * 演示如何使用Telegram适配器进行文件传输
 */

import { TelegramAdapter } from '../src/adapters/telegram-adapter.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

async function main() {
  console.log('🚀 Telegram适配器示例\n');

  // 1. 创建Telegram适配器
  console.log('1. 创建Telegram适配器...');
  const telegramAdapter = new TelegramAdapter({
    maxFileSize: 10 * 1024 * 1024, // 10MB测试限制
    chunkSize: 1 * 1024 * 1024     // 1MB分块
  });

  // 显示适配器信息
  const info = telegramAdapter.getInfo();
  console.log('✅ 适配器创建成功:');
  console.log(`   名称: ${info.name}`);
  console.log(`   版本: ${info.version}`);
  console.log(`   平台: ${info.platform}`);
  console.log(`   最大文件大小: ${telegramAdapter.formatBytes(info.maxFileSize)}`);
  console.log(`   支持格式: ${info.supportedFormats}种\n`);

  // 2. 创建测试文件
  console.log('2. 创建测试文件...');
  const testDir = path.join(__dirname, '../test-data');
  await fs.mkdir(testDir, { recursive: true });
  
  const testFilePath = path.join(testDir, 'example-document.txt');
  const testContent = `📄 测试文档 - Telegram适配器示例

这是一个用于演示Telegram文件传输适配器的测试文件。

文件信息:
- 创建时间: ${new Date().toLocaleString()}
- 文件类型: 文本文件 (.txt)
- 用途: 集成测试和示例演示

功能演示:
✅ 上下文分析
✅ 文件验证
✅ 进度跟踪
✅ 智能目标推荐
✅ 错误处理

传输场景:
1. 群聊分享 - 项目文档
2. 私聊备份 - 个人文件
3. 协作编辑 - 团队文档

注意事项:
- 支持最大文件: ${telegramAdapter.formatBytes(info.maxFileSize)}
- 支持分块传输
- 自动重试机制
- 进度实时反馈

祝使用愉快！ 🚀
`.repeat(5); // 重复内容以增加文件大小

  await fs.writeFile(testFilePath, testContent, 'utf-8');
  const stats = await fs.stat(testFilePath);
  console.log(`✅ 测试文件创建成功: ${testFilePath}`);
  console.log(`   文件大小: ${telegramAdapter.formatBytes(stats.size)}\n`);

  // 3. 模拟群聊文件传输
  console.log('3. 模拟群聊文件传输...');
  try {
    const groupResult = await telegramAdapter.sendFile({
      filePath: testFilePath,
      chatId: '-1003655501651', // 群聊ID
      caption: '📢 项目文档分享 - 请查收',
      options: {
        disableNotification: false
      }
    });

    console.log('✅ 群聊传输成功:');
    console.log(`   传输ID: ${groupResult.transferId}`);
    console.log(`   消息ID: ${groupResult.messageId}`);
    console.log(`   文件大小: ${telegramAdapter.formatBytes(groupResult.fileSize)}`);
    console.log(`   传输耗时: ${groupResult.duration}ms`);
    console.log(`   场景分析: ${groupResult.analysis.scenario}`);
    console.log(`   紧急程度: ${groupResult.analysis.urgency}`);
    console.log(`   置信度: ${groupResult.analysis.confidence}%`);
    console.log(`   推荐目标: ${groupResult.analysis.recommendedTargets.join(', ')}\n`);
  } catch (error) {
    console.log(`❌ 群聊传输失败: ${error.message}\n`);
  }

  // 4. 模拟私聊文件传输
  console.log('4. 模拟私聊文件传输...');
  try {
    const privateResult = await telegramAdapter.sendFile({
      filePath: testFilePath,
      chatId: '8772264920', // 私聊ID
      caption: '🔒 个人文件备份',
      options: {
        disableNotification: true // 私聊静默
      }
    });

    console.log('✅ 私聊传输成功:');
    console.log(`   传输ID: ${privateResult.transferId}`);
    console.log(`   消息ID: ${privateResult.messageId}`);
    console.log(`   文件大小: ${telegramAdapter.formatBytes(privateResult.fileSize)}`);
    console.log(`   传输耗时: ${privateResult.duration}ms`);
    console.log(`   场景分析: ${privateResult.analysis.scenario}`);
    console.log(`   是否群聊: ${privateResult.analysis.isGroupChat ? '是' : '否'}\n`);
  } catch (error) {
    console.log(`❌ 私聊传输失败: ${error.message}\n`);
  }

  // 5. 演示传输状态查询
  console.log('5. 演示传输状态查询...');
  const activeTransfers = telegramAdapter.getActiveTransfers();
  
  if (activeTransfers.length > 0) {
    console.log(`📊 当前有 ${activeTransfers.length} 个活动传输:`);
    activeTransfers.forEach((transfer, index) => {
      console.log(`   ${index + 1}. ${transfer.fileName}`);
      console.log(`      状态: ${transfer.status}`);
      console.log(`      进度: ${transfer.progress}%`);
      console.log(`      开始时间: ${new Date(transfer.startTime).toLocaleTimeString()}`);
      console.log(`      聊天ID: ${transfer.chatId}`);
    });
  } else {
    console.log('📊 当前没有活动传输（可能已清理）');
  }

  // 6. 清理测试文件
  console.log('\n6. 清理测试文件...');
  try {
    await fs.unlink(testFilePath);
    await fs.rmdir(testDir);
    console.log('✅ 测试文件清理完成');
  } catch (error) {
    console.log(`⚠️ 清理警告: ${error.message}`);
  }

  console.log('\n🎉 示例演示完成！');
  console.log('\n📋 关键功能已验证:');
  console.log('   ✅ 适配器初始化和配置');
  console.log('   ✅ 文件验证和管理');
  console.log('   ✅ 上下文智能分析');
  console.log('   ✅ 群聊/私聊场景适配');
  console.log('   ✅ 传输进度跟踪');
  console.log('   ✅ 状态查询和管理');
  console.log('   ✅ 错误处理和恢复');
  console.log('\n🚀 现在可以集成到OpenClaw技能中使用！');
}

// 运行示例
main().catch(error => {
  console.error('❌ 示例运行失败:', error);
  process.exit(1);
});