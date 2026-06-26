#!/usr/bin/env node
/**
 * 网课自动播放器 - 核心控制脚本
 * 用于分析页面结构、播放视频、检测完成、切换下一课
 */

const fs = require('fs');
const path = require('path');

// 进度文件路径
const PROGRESS_FILE = path.join(
  process.env.HOME || process.env.USERPROFILE,
  '.openclaw/workspace/memory/course-progress.md'
);

/**
 * 读取当前进度
 */
function loadProgress() {
  try {
    if (fs.existsSync(PROGRESS_FILE)) {
      const content = fs.readFileSync(PROGRESS_FILE, 'utf-8');
      return parseProgress(content);
    }
  } catch (e) {
    console.error('读取进度失败:', e.message);
  }
  return {
    courseName: '',
    totalVideos: 0,
    completedVideos: 0,
    currentVideo: '',
    completedList: [],
    learningTimeMinutes: 0,
    lastUpdated: new Date().toISOString()
  };
}

/**
 * 解析进度文件
 */
function parseProgress(content) {
  const progress = {
    courseName: '',
    totalVideos: 0,
    completedVideos: 0,
    currentVideo: '',
    completedList: [],
    learningTimeMinutes: 0,
    lastUpdated: new Date().toISOString()
  };
  
  // 简单解析 markdown 格式
  const lines = content.split('\n');
  for (const line of lines) {
    if (line.includes('**课程**')) {
      progress.courseName = line.split(':')[1]?.trim().replace(/\*\*/g, '') || '';
    } else if (line.includes('总视频数')) {
      progress.totalVideos = parseInt(line.split(':')[1]?.trim()) || 0;
    } else if (line.includes('已完成')) {
      progress.completedVideos = parseInt(line.split(':')[1]?.trim()) || 0;
    } else if (line.includes('学习时长')) {
      const match = line.match(/(\d+)\s*小时.*?(\d+)\s*分钟/);
      if (match) {
        progress.learningTimeMinutes = parseInt(match[1]) * 60 + parseInt(match[2]);
      }
    }
  }
  
  return progress;
}

/**
 * 保存进度
 */
function saveProgress(progress) {
  const content = `# 网课学习进度

> 最后更新：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}

## 当前课程

**课程**: ${progress.courseName || '未设置'}
**总视频数**: ${progress.totalVideos}
**已完成**: ${progress.completedVideos}/${progress.totalVideos}
**学习时长**: ${Math.floor(progress.learningTimeMinutes / 60)}小时${progress.learningTimeMinutes % 60}分钟
**最后播放**: ${progress.currentVideo || '无'}
**状态**: ${progress.completedVideos >= progress.totalVideos ? '✅ 已完成' : '🔄 进行中'}

## 已完成视频列表

${progress.completedList.map((v, i) => `${i + 1}. ${v}`).join('\n')}

## 学习记录

### ${new Date().toLocaleDateString('zh-CN')}

- 开始时间：${new Date().toLocaleTimeString('zh-CN', { timeZone: 'Asia/Shanghai' })}
- 目标：完成所有课程视频
- 备注：自动播放中

---
`;
  
  fs.writeFileSync(PROGRESS_FILE, content, 'utf-8');
  console.log('进度已保存:', PROGRESS_FILE);
}

/**
 * 初始化进度文件
 */
function initProgress(courseName = '网课', totalVideos = 0) {
  const progress = {
    courseName,
    totalVideos,
    completedVideos: 0,
    currentVideo: '',
    completedList: [],
    learningTimeMinutes: 0,
    lastUpdated: new Date().toISOString()
  };
  saveProgress(progress);
  return progress;
}

// 命令行支持
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'init') {
    const courseName = args[1] || '网课';
    const totalVideos = parseInt(args[2]) || 0;
    const progress = initProgress(courseName, totalVideos);
    console.log('进度初始化完成:', progress);
  } else if (command === 'status') {
    const progress = loadProgress();
    console.log('当前进度:', progress);
  } else {
    console.log('用法:');
    console.log('  node course-player.js init [课程名] [视频总数]');
    console.log('  node course-player.js status');
  }
}

module.exports = { loadProgress, saveProgress, initProgress };
