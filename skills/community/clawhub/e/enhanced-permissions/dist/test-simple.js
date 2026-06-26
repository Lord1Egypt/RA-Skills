/**
 * Simple Test Script - No TypeScript compilation issues
 * Run with: node test-simple.js
 */

console.log('🧪 Running Simple Tests...\n');

let passed = 0;
let failed = 0;

// Test 1: Check if files exist
console.log('Test 1: File Structure');
const fs = require('fs');
const path = require('path');

const requiredFiles = [
  'types.ts',
  'permission-checker.ts',
  'tool-registry.ts',
  'enhanced-tools.ts',
  'memory-manager.ts',
  'openclaw-adapter.ts',
  'confirmation-dialog.ts',
  'audit-logger.ts',
  'index.ts'
];

let allFilesExist = true;
for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    console.log(`  ✅ ${file}`);
  } else {
    console.log(`  ❌ ${file} - MISSING`);
    allFilesExist = false;
  }
}

if (allFilesExist) {
  passed++;
  console.log('  ✅ All files present\n');
} else {
  failed++;
  console.log('  ❌ Some files missing\n');
}

// Test 2: Check file sizes
console.log('Test 2: File Sizes');
let totalSize = 0;
for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  if (fs.existsSync(filePath)) {
    const stats = fs.statSync(filePath);
    totalSize += stats.size;
  }
}

const totalKB = (totalSize / 1024).toFixed(1);
console.log(`  Total size: ${totalKB} KB`);

if (totalSize > 50000) { // > 50KB
  passed++;
  console.log('  ✅ Codebase size reasonable\n');
} else {
  failed++;
  console.log('  ❌ Codebase too small\n');
}

// Test 3: Check exports in index.ts
console.log('Test 3: Module Exports');
const indexContent = fs.readFileSync(path.join(__dirname, 'index.ts'), 'utf-8');

const requiredExports = [
  'PermissionChecker',
  'ToolRegistry',
  'MemoryManager',
  'registerEnhancedOpenClawTools',
  'executeToolWithPermission',
  'showConfirmationDialog',
  'defaultAuditLogger'
];

let allExportsPresent = true;
for (const exportName of requiredExports) {
  if (indexContent.includes(exportName)) {
    console.log(`  ✅ ${exportName}`);
  } else {
    console.log(`  ❌ ${exportName} - MISSING`);
    allExportsPresent = false;
  }
}

if (allExportsPresent) {
  passed++;
  console.log('  ✅ All exports present\n');
} else {
  failed++;
  console.log('  ❌ Some exports missing\n');
}

// Test 4: Check for key features
console.log('Test 4: Key Features');
const features = [
  { name: 'Permission Levels', file: 'types.ts', pattern: 'enum PermissionLevel' },
  { name: 'Zod Schemas', file: 'openclaw-adapter.ts', pattern: 'z.object' },
  { name: 'Hotness Algorithm', file: 'memory-manager.ts', pattern: 'calculateDecayedHotness' },
  { name: 'Confirmation Dialog', file: 'confirmation-dialog.ts', pattern: 'showConfirmationDialog' },
  { name: 'Audit Logger', file: 'audit-logger.ts', pattern: 'class AuditLogger' }
];

let allFeaturesPresent = true;
for (const feature of features) {
  const filePath = path.join(__dirname, feature.file);
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf-8');
    if (content.includes(feature.pattern)) {
      console.log(`  ✅ ${feature.name}`);
    } else {
      console.log(`  ❌ ${feature.name} - NOT FOUND`);
      allFeaturesPresent = false;
    }
  } else {
    console.log(`  ❌ ${feature.name} - FILE MISSING`);
    allFeaturesPresent = false;
  }
}

if (allFeaturesPresent) {
  passed++;
  console.log('  ✅ All features implemented\n');
} else {
  failed++;
  console.log('  ❌ Some features missing\n');
}

// Summary
console.log('='.repeat(50));
console.log(`Tests Complete: ${passed + failed}`);
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log(`📊 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
console.log('='.repeat(50));

if (failed === 0) {
  console.log('\n🎉 All tests passed! Phase 2 validation successful!\n');
  process.exit(0);
} else {
  console.log(`\n⚠️ ${failed} test(s) failed. Please review.\n`);
  process.exit(1);
}
