#!/usr/bin/env node
/**
 * 工作流优化迭代分析器 v1.0
 * 
 * 功能：
 * 1. 扫描所有文件，识别核心模块和冗余版本
 * 2. 分析依赖关系和使用情况
 * 3. 生成清理建议报告
 * 4. 提供安全删除方案
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const WORKFLOW_DIR = '/home/ubutu/.openclaw/workspace/skills/agile-workflow';
const CORE_DIR = path.join(WORKFLOW_DIR, 'core');

// ============ 文件分类规则 ============

const KEEP_PATTERNS = [
  // 核心引擎（主版本）
  'agile-workflow-engine.js',
  'task-scheduler.js',
  'dependency-manager.js',
  'task-state-tracker.js',
  
  // Agent 管理
  'agent-process-pool.js',
  'agent-manager.js',
  'agent-supervisor.js',
  
  // 并发控制
  'concurrent-executor.js',
  'load-balancer.js',
  
  // 监控和健康检查
  'health-check.js',
  'self-healing-monitor.js',
  'log-monitor.js',
  'task-report-monitor.js',
  'health-monitor.js',
  
  // 配置和管理
  'config-manager.js',
  'version-manager.js',
  'project-manager.js',
  'global-process-manager.js',
  
  // Token 和质量控制
  'token-counter.js',
  'auto-chunker.js',
  'quality-validator.js',
  'quality-validator-rules.js',
  
  // 缓存和性能
  'cache-manager.js',
  'cache-backend.js',
  'memory-manager.js',
  'performance-tuner.js',
  
  // 依赖和任务管理
  'dependency-graph-manager.js',
  'merge-strategy-manager.js',
  
  // 集成和适配
  'integration-adapter.js',
  'write-domain-isolator.js',
  'context-router.js',
  'prompt-cache.js',
  'message-bus.js',
  'llm-gateway.js',
  
  // 验证和告警
  'execution-verifier.js',
  'data-verifier.js',
  'report-validator.js',
  'violation-alarm.js',
  'monitoring-alert-system.js',
  
  // 创意和评分
  'creativity-scorer.js',
  
  // 工作流配置
  'workflow-config.js',
  
  // 新任务依赖模型
  'task-dependency-generator.js',
  'repair-task-states.js'
];

const DELETE_PATTERNS = [
  // 老版本引擎
  'agile-workflow-engine-v5.js',
  'agile-workflow-engine-v7.js',
  
  // 老版本执行器
  'concurrent-executor-v2.js',
  
  // 老版本健康检查
  'health-check-v2.js',
  
  // 测试框架（已有独立 test 目录）
  'test-framework.js',
  
  // 压力测试（非生产必需）
  'stress-test.js'
];

// ============ 分析函数 ============

/**
 * 扫描目录中的所有 JS 文件
 */
function scanJSFiles(dir) {
  const files = [];
  
  function walk(currentDir) {
    const entries = fs.readdirSync(currentDir);
    
    for (const entry of entries) {
      if (entry === 'node_modules') continue;
      
      const fullPath = path.join(currentDir, entry);
      const stat = fs.statSync(fullPath);
      
      if (stat.isDirectory()) {
        walk(fullPath);
      } else if (entry.endsWith('.js')) {
        const relPath = path.relative(WORKFLOW_DIR, fullPath);
        const size = stat.size;
        
        files.push({
          path: relPath,
          fullPath: fullPath,
          size: size,
          sizeStr: formatSize(size)
        });
      }
    }
  }
  
  walk(dir);
  return files;
}

/**
 * 格式化文件大小
 */
function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

/**
 * 检查文件是否被引用
 */
function checkFileReferences(filePath) {
  try {
    const fileName = path.basename(filePath);
    const result = execSync(`cd "${WORKFLOW_DIR}" && grep -r "${fileName}" core/ scripts/ 2>/dev/null | grep -v node_modules | wc -l`, { encoding: 'utf8' });
    return parseInt(result.trim(), 10);
  } catch (e) {
    return 0;
  }
}

/**
 * 分析文件使用情况
 */
function analyzeFiles(files) {
  const analysis = {
    keep: [],
    delete: [],
    unknown: []
  };
  
  for (const file of files) {
    const fileName = path.basename(file.path);
    const relPath = file.path;
    
    // 检查是否在保留列表
    if (KEEP_PATTERNS.some(p => fileName.includes(p) || relPath.includes(p))) {
      analysis.keep.push(file);
      continue;
    }
    
    // 检查是否在删除列表
    if (DELETE_PATTERNS.some(p => fileName.includes(p) || relPath.includes(p))) {
      const refs = checkFileReferences(file.fullPath);
      file.references = refs;
      analysis.delete.push(file);
      continue;
    }
    
    // 其他文件需要人工审查
    const refs = checkFileReferences(file.fullPath);
    file.references = refs;
    analysis.unknown.push(file);
  }
  
  return analysis;
}

/**
 * 生成清理报告
 */
function generateReport(analysis) {
  console.log('='.repeat(80));
  console.log('📊 工作流优化迭代分析报告');
  console.log('='.repeat(80));
  
  console.log('\n✅ 保留文件（核心模块）:');
  console.log(`   数量：${analysis.keep.length}`);
  console.log('   文件列表:');
  for (const file of analysis.keep.slice(0, 20)) {
    console.log(`     - ${file.path} (${file.sizeStr})`);
  }
  if (analysis.keep.length > 20) {
    console.log(`     ... 还有 ${analysis.keep.length - 20} 个文件`);
  }
  
  console.log('\n❌ 建议删除（老版本/冗余）:');
  console.log(`   数量：${analysis.delete.length}`);
  console.log('   文件列表:');
  for (const file of analysis.delete) {
    const refInfo = file.references > 0 ? `⚠️ 被引用 ${file.references} 次` : '✅ 无引用';
    console.log(`     - ${file.path} (${file.sizeStr}) ${refInfo}`);
  }
  
  console.log('\n⚠️ 需要人工审查:');
  console.log(`   数量：${analysis.unknown.length}`);
  console.log('   文件列表:');
  for (const file of analysis.unknown) {
    const refInfo = file.references > 0 ? `📌 被引用 ${file.references} 次` : 'ℹ️ 无引用';
    console.log(`     - ${file.path} (${file.sizeStr}) ${refInfo}`);
  }
  
  // 统计可释放空间
  const deleteSize = analysis.delete.reduce((sum, f) => sum + f.size, 0);
  const unknownSize = analysis.unknown.reduce((sum, f) => sum + f.size, 0);
  
  console.log('\n📈 空间统计:');
  console.log(`   保留文件总大小：${formatSize(analysis.keep.reduce((sum, f) => sum + f.size, 0))}`);
  console.log(`   可删除文件大小：${formatSize(deleteSize)}`);
  console.log(`   待审查文件大小：${formatSize(unknownSize)}`);
  
  console.log('\n' + '='.repeat(80));
  console.log('💡 建议操作:');
  console.log('   1. 确认删除列表中的文件无引用');
  console.log('   2. 运行清理脚本删除老版本');
  console.log('   3. 审查未知文件，决定保留或删除');
  console.log('='.repeat(80));
}

/**
 * 生成清理脚本
 */
function generateCleanupScript(filesToDelete) {
  const scriptPath = path.join(WORKFLOW_DIR, 'scripts', 'cleanup-old-versions.sh');
  
  let script = `#!/bin/bash
# 工作流老版本清理脚本
# 生成时间：${new Date().toISOString()}

set -e

WORKFLOW_DIR="/home/ubutu/.openclaw/workspace/skills/agile-workflow"
BACKUP_DIR="$WORKFLOW_DIR/backups/$(date +%Y%m%d_%H%M%S)"

echo "🔍 开始清理老版本文件..."
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"
echo "✅ 备份目录：$BACKUP_DIR"
echo ""

# 文件列表
FILES_TO_DELETE=(
`;
  
  for (const file of filesToDelete) {
    script += `  "${file.path}"\n`;
  }
  
  script += `)

# 删除文件
for file in "\${FILES_TO_DELETE[@]}"; do
  src="$WORKFLOW_DIR/$file"
  if [ -f "$src" ]; then
    # 备份
    cp "$src" "$BACKUP_DIR/"
    echo "📦 已备份：$file"
    
    # 删除
    rm "$src"
    echo "❌ 已删除：$file"
  else
    echo "⚠️ 文件不存在：$file"
  fi
done

echo ""
echo "✅ 清理完成！"
echo "📦 备份位置：$BACKUP_DIR"
echo ""
echo "如需恢复，从备份目录复制文件回原位置即可。"
`;
  
  fs.writeFileSync(scriptPath, script.replace(/\\n/g, '\n'));
  fs.chmodSync(scriptPath, 0o755);
  
  console.log(`\n✅ 已生成清理脚本：${scriptPath}`);
  console.log(`   运行：bash ${scriptPath}`);
}

// ============ 主函数 ============

function main() {
  console.log('🔍 扫描工作流目录...\n');
  
  // 扫描所有 JS 文件
  const files = scanJSFiles(CORE_DIR);
  console.log(`📊 发现 ${files.length} 个 JS 文件\n`);
  
  // 分析文件使用情况
  const analysis = analyzeFiles(files);
  
  // 生成报告
  generateReport(analysis);
  
  // 生成清理脚本
  if (analysis.delete.length > 0) {
    generateCleanupScript(analysis.delete);
  }
}

main();
