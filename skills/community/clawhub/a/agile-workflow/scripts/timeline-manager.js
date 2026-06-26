#!/usr/bin/env node
/**
 * 时间线验证与更新脚本 v1.0
 * 
 * 功能：
 * 1. 验证章节细纲的时间线是否与全局时间线一致
 * 2. 更新全局时间线
 * 3. 检测时间线冲突
 */

const fs = require('fs');
const path = require('path');

class TimelineManager {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.timelinePath = path.join(projectDir, '.timeline.json');
    this.timeline = this.loadTimeline();
  }

  /**
   * 加载全局时间线
   */
  loadTimeline() {
    if (fs.existsSync(this.timelinePath)) {
      return JSON.parse(fs.readFileSync(this.timelinePath, 'utf-8'));
    }
    // 创建默认时间线
    return {
      schema: 'global-timeline-v1',
      story_meta: {
        title: '',
        start_date: new Date().toISOString(),
        current_chapter: 0,
        current_story_time: new Date().toISOString()
      },
      chapters: [],
      time_jumps: [],
      constraints: {
        max_time_jump: '1个月',
        must_specify_jump_reason: true,
        character_age_consistency: true
      }
    };
  }

  /**
   * 保存全局时间线
   */
  saveTimeline() {
    fs.writeFileSync(this.timelinePath, JSON.stringify(this.timeline, null, 2));
  }

  /**
   * 获取前一章的结束时间
   */
  getPrevChapterEndTime(chapterNum) {
    const prevChapter = this.timeline.chapters.find(c => c.chapter === chapterNum - 1);
    if (prevChapter) {
      return new Date(prevChapter.time_end);
    }
    return new Date(this.timeline.story_meta.start_date);
  }

  /**
   * 验证章节时间线
   */
  validateChapterTimeline(chapterNum, timeStart, timeEnd) {
    const errors = [];
    const prevEnd = this.getPrevChapterEndTime(chapterNum);
    const start = new Date(timeStart);
    const end = new Date(timeEnd);

    // 检查开始时间是否在前一章结束后
    if (chapterNum > 1 && start < prevEnd) {
      errors.push(`第${chapterNum}章开始时间(${timeStart})早于第${chapterNum-1}章结束时间(${prevEnd.toISOString()})`);
    }

    // 检查结束时间是否在开始时间之后
    if (end <= start) {
      errors.push(`第${chapterNum}章结束时间(${timeEnd})不在开始时间(${timeStart})之后`);
    }

    // 检查是否与已有章节冲突
    for (const chapter of this.timeline.chapters) {
      if (chapter.chapter !== chapterNum) {
        const cStart = new Date(chapter.time_start);
        const cEnd = new Date(chapter.time_end);
        if ((start >= cStart && start < cEnd) || (end > cStart && end <= cEnd)) {
          errors.push(`第${chapterNum}章时间范围与第${chapter.chapter}章冲突`);
        }
      }
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * 更新章节时间线
   */
  updateChapterTimeline(chapterNum, title, timeStart, timeEnd, keyEvents, characterStates) {
    const validation = this.validateChapterTimeline(chapterNum, timeStart, timeEnd);
    if (!validation.valid) {
      throw new Error(`时间线验证失败: ${validation.errors.join('; ')}`);
    }

    // 计算距离故事开始的天数
    const storyStart = new Date(this.timeline.story_meta.start_date);
    const chapterStart = new Date(timeStart);
    const daysSinceStart = Math.floor((chapterStart - storyStart) / (1000 * 60 * 60 * 24));

    // 更新或添加章节
    const existingIndex = this.timeline.chapters.findIndex(c => c.chapter === chapterNum);
    const chapterData = {
      chapter: chapterNum,
      title,
      time_start: timeStart,
      time_end: timeEnd,
      duration: this.calculateDuration(timeStart, timeEnd),
      days_since_start: daysSinceStart,
      key_events: keyEvents,
      character_states: characterStates
    };

    if (existingIndex >= 0) {
      this.timeline.chapters[existingIndex] = chapterData;
    } else {
      this.timeline.chapters.push(chapterData);
      this.timeline.chapters.sort((a, b) => a.chapter - b.chapter);
    }

    // 更新当前故事时间
    this.timeline.story_meta.current_chapter = chapterNum;
    this.timeline.story_meta.current_story_time = timeEnd;

    this.saveTimeline();
    return { success: true, chapter: chapterData };
  }

  /**
   * 计算持续时间
   */
  calculateDuration(timeStart, timeEnd) {
    const start = new Date(timeStart);
    const end = new Date(timeEnd);
    const diffMs = end - start;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) {
      return `${diffDays}天${diffHours % 24}小时`;
    } else if (diffHours > 0) {
      return `${diffHours}小时${diffMins % 60}分钟`;
    } else {
      return `${diffMins}分钟`;
    }
  }

  /**
   * 获取时间线摘要（供 Agent 使用）
   */
  getTimelineSummary() {
    return {
      story_start: this.timeline.story_meta.start_date,
      current_chapter: this.timeline.story_meta.current_chapter,
      current_story_time: this.timeline.story_meta.current_story_time,
      total_chapters: this.timeline.chapters.length,
      recent_chapters: this.timeline.chapters.slice(-5)
    };
  }
}

// CLI 接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const projectDir = args[0];

  if (!projectDir) {
    console.log('用法: node timeline-manager.js <项目目录> [命令] [参数]');
    console.log('');
    console.log('命令:');
    console.log('  summary           - 获取时间线摘要');
    console.log('  validate <章节号> <开始时间> <结束时间> - 验证时间线');
    console.log('  update <章节号> <标题> <开始时间> <结束时间> <关键事件JSON> - 更新时间线');
    process.exit(1);
  }

  const manager = new TimelineManager(projectDir);
  const command = args[1];

  switch (command) {
    case 'summary':
      console.log(JSON.stringify(manager.getTimelineSummary(), null, 2));
      break;
    case 'validate':
      const validateResult = manager.validateChapterTimeline(
        parseInt(args[2]),
        args[3],
        args[4]
      );
      console.log(JSON.stringify(validateResult, null, 2));
      break;
    case 'update':
      const updateResult = manager.updateChapterTimeline(
        parseInt(args[2]),
        args[3],
        args[4],
        args[5],
        JSON.parse(args[6] || '[]'),
        JSON.parse(args[7] || '{}')
      );
      console.log(JSON.stringify(updateResult, null, 2));
      break;
    default:
      console.log('当前时间线:');
      console.log(JSON.stringify(manager.timeline, null, 2));
  }
}

module.exports = TimelineManager;