/**
 * Quick Test - 快速验证测试
 * 
 * 验证核心模块可以正常加载和实例化
 */

import { HarnessOrchestrator } from '../harness/orchestrator.js';
import { CodeReviewWorkflow } from '../workflows/code-review.js';
import { WALProtocol } from '../memory/wal.js';
import { WorkingBuffer } from '../memory/working-buffer.js';

console.log('🧪 Harness Engineering 快速验证测试\n');

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`✅ ${name}`);
    passed++;
  } catch (error) {
    console.error(`❌ ${name}: ${error.message}`);
    failed++;
  }
}

// 测试模块加载和实例化
test('HarnessOrchestrator 加载', () => {
  if (!HarnessOrchestrator) throw new Error('Module not loaded');
});

test('HarnessOrchestrator 实例化', () => {
  const o = new HarnessOrchestrator({ enableLogging: false });
  if (!o) throw new Error('Failed to instantiate');
});

test('CodeReviewWorkflow 加载', () => {
  if (!CodeReviewWorkflow) throw new Error('Module not loaded');
});

test('CodeReviewWorkflow 实例化', () => {
  const w = new CodeReviewWorkflow({ enableLogging: false });
  if (!w) throw new Error('Failed to instantiate');
});

test('WALProtocol 加载', () => {
  if (!WALProtocol) throw new Error('Module not loaded');
});

test('WALProtocol 实例化', () => {
  const w = new WALProtocol({ walDir: './tests/fixtures/wal-quick', enableCompaction: false });
  if (!w) throw new Error('Failed to instantiate');
});

test('WorkingBuffer 加载', () => {
  if (!WorkingBuffer) throw new Error('Module not loaded');
});

test('WorkingBuffer 实例化', () => {
  const b = new WorkingBuffer({ bufferDir: './tests/fixtures/buffer-quick', autoSave: false });
  if (!b) throw new Error('Failed to instantiate');
});

// 统计
console.log(`\n${'='.repeat(50)}`);
console.log(`测试结果：${passed} 通过，${failed} 失败`);
console.log(`${'='.repeat(50)}\n`);

if (failed > 0) {
  process.exit(1);
} else {
  console.log('✅ 所有核心模块验证通过！\n');
}
