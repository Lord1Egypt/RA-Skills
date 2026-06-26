#!/usr/bin/env node
/**
 * 细纲创作前置数据检查工具 v1.0
 * 
 * 功能：
 * 1. 检查创作指定章节细纲所需的前置数据是否完整
 * 2. 输出缺失数据清单
 * 3. 生成创作建议
 */

const fs = require('fs');
const path = require('path');

class OutlinePreCheck {
  constructor(projectDir) {
    this.projectDir = projectDir;
    this.projectPath = path.join(projectDir, 'project.json');
    this.timelinePath = path.join(projectDir, '.timeline.json');
    this.project = null;
    this.timeline = null;
  }

  load() {
    if (fs.existsSync(this.projectPath)) {
      this.project = JSON.parse(fs.readFileSync(this.projectPath, 'utf-8'));
    }
    if (fs.existsSync(this.timelinePath)) {
      this.timeline = JSON.parse(fs.readFileSync(this.timelinePath, 'utf-8'));
    }
  }

  /**
   * 检查指定章节的前置数据
   */
  checkChapter(chapterNum) {
    const result = {
      chapter: chapterNum,
      ready: true,
      missing: [],
      available: [],
      suggestions: []
    };

    // 1. 检查 project.json
    if (!this.project) {
      result.missing.push({ type: 'critical', item: 'project.json', message: '项目文件不存在' });
      result.ready = false;
      return result;
    }
    result.available.push({ item: 'project.json', status: 'ok' });

    // 2. 检查章节情节大纲
    const chapterOutlines = this.project.plot?.chapter_outlines || [];
    const chapterOutline = chapterOutlines.find(c => c.chapter === chapterNum);
    if (!chapterOutline) {
      result.missing.push({ 
        type: 'critical', 
        item: `plot.chapter_outlines[${chapterNum}]`, 
        message: `第${chapterNum}章情节大纲不存在，需要先创建` 
      });
      result.suggestions.push(`运行: 创建第${chapterNum}章情节大纲`);
      result.ready = false;
    } else {
      result.available.push({ item: `chapter_outline[${chapterNum}]`, status: 'ok', data: chapterOutline.title });
    }

    // 3. 检查单元剧大纲
    if (chapterOutline?.unit_id) {
      const unitStories = this.project.plot?.unit_stories || [];
      const unitStory = unitStories.find(u => u.id === chapterOutline.unit_id);
      if (!unitStory) {
        result.missing.push({ 
          type: 'warning', 
          item: `plot.unit_stories[${chapterOutline.unit_id}]`, 
          message: '关联的单元剧大纲不存在' 
        });
      } else {
        result.available.push({ item: `unit_story[${chapterOutline.unit_id}]`, status: 'ok', data: unitStory.name });
      }
    }

    // 4. 检查人物设定
    const keyCharIds = chapterOutline?.key_character_ids || [];
    const characters = this.project.characters || [];
    for (const charId of keyCharIds) {
      const char = characters.find(c => c.id === charId);
      if (!char) {
        result.missing.push({ type: 'warning', item: `characters[${charId}]`, message: `人物设定不存在` });
      } else {
        result.available.push({ item: `character[${charId}]`, status: 'ok', data: char.name });
      }
    }

    // 5. 检查地点设定
    const locationIds = chapterOutline?.location_ids || [];
    const locations = this.project.location_registry || [];
    for (const locId of locationIds) {
      const loc = locations.find(l => l.id === locId);
      if (!loc) {
        result.missing.push({ type: 'info', item: `location_registry[${locId}]`, message: '地点设定不存在，细纲创作时需创建' });
      } else {
        result.available.push({ item: `location[${locId}]`, status: 'ok', data: loc.name });
      }
    }

    // 6. 检查时间线
    if (!this.timeline) {
      result.missing.push({ type: 'critical', item: '.timeline.json', message: '时间线文件不存在' });
      result.ready = false;
    } else {
      const prevChapter = this.timeline.chapters?.find(c => c.chapter === chapterNum - 1);
      if (chapterNum > 1 && !prevChapter) {
        result.missing.push({ type: 'warning', item: `timeline.chapters[${chapterNum - 1}]`, message: '前章时间线不存在' });
      } else if (prevChapter) {
        result.available.push({ item: `prev_chapter_timeline`, status: 'ok', data: prevChapter.time_end });
      }
    }

    // 7. 检查伏笔注册表
    const fr = this.project.foreshadowing_registry;
    if (!fr) {
      result.missing.push({ type: 'info', item: 'foreshadowing_registry', message: '伏笔注册表不存在' });
    } else {
      const pending = fr.pending_resolution || [];
      const toResolve = pending.filter(f => {
        const rc = f.resolve_chapter;
        if (typeof rc === 'string' && rc.includes('-')) {
          const [start, end] = rc.split('-').map(Number);
          return chapterNum >= start && chapterNum <= end;
        }
        return Number(rc) === chapterNum;
      });
      if (toResolve.length > 0) {
        result.available.push({ item: 'foreshadowing_to_resolve', status: 'ok', data: toResolve.map(f => f.id).join(', ') });
      }
    }

    return result;
  }

  /**
   * 生成创作建议
   */
  generateSuggestions(checkResult) {
    const suggestions = [];

    if (!checkResult.ready) {
      suggestions.push('【前置数据不完整，无法创作细纲】');
      for (const missing of checkResult.missing.filter(m => m.type === 'critical')) {
        suggestions.push(`- 需要先: ${missing.message}`);
      }
    } else {
      suggestions.push('【前置数据完整，可以创作细纲】');
      suggestions.push('');
      suggestions.push('创作步骤:');
      suggestions.push('1. 读取 project.json 获取章节情节大纲');
      suggestions.push('2. 读取 .timeline.json 获取前章结束时间');
      suggestions.push('3. 使用 chapter-outline-v3.json 模板创作细纲');
      suggestions.push('4. 更新 .timeline.json');
    }

    return suggestions;
  }
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  const projectDir = args[0];
  const chapterNum = parseInt(args[1]);

  if (!projectDir || !chapterNum) {
    console.log('用法: node outline-pre-check.js <项目目录> <章节号>');
    console.log('');
    console.log('示例: node outline-pre-check.js /path/to/project 1');
    process.exit(1);
  }

  const checker = new OutlinePreCheck(projectDir);
  checker.load();
  const result = checker.checkChapter(chapterNum);

  console.log(JSON.stringify(result, null, 2));
}

module.exports = OutlinePreCheck;