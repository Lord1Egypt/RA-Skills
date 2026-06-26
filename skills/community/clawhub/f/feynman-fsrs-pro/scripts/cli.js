#!/usr/bin/env node
/**
 * feynman-fsrs-pro CLI 工具
 * 提供命令行接口让 AI 调用数据库函数
 * 
 * 用法:
 *   node cli.js get-due-tasks
 *   node cli.js get-note-content <conceptName>
 *   node cli.js update-study-progress <conceptName> <rating> <feedback> <summary>
 *   node cli.js get-new-notes
 *   node cli.js get-stats
 */

import { get_due_tasks, get_note_content, update_study_progress, get_new_notes, get_study_stats } from './database.js';
import { import_new_note } from './database.js';

const command = process.argv[2];

async function main() {
  try {
    switch (command) {
      case 'get-due-tasks': {
        const tasks = await get_due_tasks();
        console.log(JSON.stringify({ success: true, data: tasks }));
        break;
      }
      case 'get-note-content': {
        const conceptName = process.argv[3];
        if (!conceptName) throw new Error('缺少 conceptName 参数');
        const content = await get_note_content(conceptName);
        console.log(JSON.stringify({ success: true, data: content }));
        break;
      }
      case 'update-study-progress': {
        const conceptName = process.argv[3];
        const rating = parseInt(process.argv[4]);
        const feedback = process.argv[5] || '';
        const summary = process.argv[6] || '';
        if (!conceptName || isNaN(rating)) throw new Error('参数错误');
        const result = await update_study_progress({ concept_name: conceptName, rating, feedback, summary });
        console.log(JSON.stringify({ success: true, data: result }));
        break;
      }
      case 'get-new-notes': {
        const notes = await get_new_notes();
        console.log(JSON.stringify({ success: true, data: notes }));
        break;
      }
      case 'import-note': {
        const conceptName = process.argv[3];
        const filePath = process.argv[4];
        if (!conceptName || !filePath) throw new Error('缺少参数');
        await import_new_note(conceptName, filePath);
        console.log(JSON.stringify({ success: true }));
        break;
      }
      case 'get-stats': {
        const stats = await get_study_stats();
        console.log(JSON.stringify({ success: true, data: stats }));
        break;
      }
      default:
        console.log(JSON.stringify({ success: false, error: `未知命令: ${command}` }));
    }
  } catch (err) {
    console.error(JSON.stringify({ success: false, error: err.message }));
  }
}

main();
