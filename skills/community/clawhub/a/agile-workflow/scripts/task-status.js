// task-status.js - 任务状态与实际文件一致性检查工具
const fs = require('fs');
const path = require('path');

function checkTaskConsistency(projectRoot) {
  const stateFile = path.join(projectRoot, '.task-state.json');
  if (!fs.existsSync(stateFile)) {
    console.error('❌ .task-state.json 不存在');
    return null;
  }

  const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  const results = {
    total: Object.keys(state).length,
    completed: 0,
    notStarted: 0,
    inconsistencies: [],
    missingFiles: []
  };

  for (const [taskId, task] of Object.entries(state)) {
    if (task.status === 'completed') {
      results.completed++;
      // 验证文件是否存在
      const filePath = path.join(projectRoot, task.output);
      if (!fs.existsSync(filePath)) {
        results.missingFiles.push({ task: taskId, file: task.output });
      }
    } else if (task.status === 'not_started') {
      results.notStarted++;
    }
  }

  return results;
}

// Example usage
const projectRoot = process.argv[2] || '.'; // 默认当前目录
const results = checkTaskConsistency(projectRoot);

if (results) {
  console.log(`📊 健康检查报告: ${projectRoot}`);
  console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  console.log(`✅ 总任务数: ${results.total}`);
  console.log(`✅ 已完成: ${results.completed}`);
  console.log(`⚠️  未开始: ${results.notStarted}`);
  console.log(`❌ 不一致: ${results.inconsistencies.length}`);
  console.log(`🗑️  文件丢失: ${results.missingFiles.length}`);
  
  if (results.missingFiles.length > 0) {
    console.log('\n⚠️  丢失文件列表:');
    results.missingFiles.forEach(f => console.log(`   - ${f.task} => ${f.file}`));
  }
}
