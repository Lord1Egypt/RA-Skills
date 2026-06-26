/**
 * Version Control System - Test Script
 * Tests all version control features
 *
 * Run with: node dist/test-version-control.js
 */
const { VersionControlManager, defaultVersionControl } = require('./index');
console.log('='.repeat(70));
console.log('🕐 Version Control System - Test Suite');
console.log('='.repeat(70));
console.log('');
let passed = 0;
let failed = 0;
// === Test 1: Create Versioned Memory ===
console.log('Test 1: Create Versioned Memory');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager();
    const memory = vcm.createVersionedMemory('Initial content', ['test', 'initial'], 'user123');
    if (memory.version === 1 && memory.history.length === 1) {
        console.log('  ✅ Versioned memory created successfully');
        console.log(`     ID: ${memory.id}`);
        console.log(`     Version: ${memory.version}`);
        console.log(`     History entries: ${memory.history.length}`);
        passed++;
    }
    else {
        console.log('  ❌ Versioned memory creation failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 2: Update Memory (Auto Versioning) ===
console.log('Test 2: Update Memory with Auto Versioning');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager();
    const memory = vcm.createVersionedMemory('Content v1', ['test']);
    const updated = vcm.updateMemory(memory.id, 'Content v2', 'user123', 'Updated content');
    if (updated && updated.version === 2 && updated.history.length === 2) {
        console.log('  ✅ Memory updated with new version');
        console.log(`     New version: ${updated.version}`);
        console.log(`     History entries: ${updated.history.length}`);
        console.log(`     Latest entry reason: ${updated.history[1].changeReason}`);
        passed++;
    }
    else {
        console.log('  ❌ Memory update failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 3: Get Version History ===
console.log('Test 3: Get Version History');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager();
    const memory = vcm.createVersionedMemory('Content v1', ['test']);
    vcm.updateMemory(memory.id, 'Content v2', 'user123', 'Update 1');
    vcm.updateMemory(memory.id, 'Content v3', 'user123', 'Update 2');
    const history = vcm.getHistory(memory.id);
    if (history.length === 3) {
        console.log('  ✅ Version history retrieved successfully');
        console.log(`     Total versions: ${history.length}`);
        history.forEach(v => {
            console.log(`     v${v.version}: ${v.content.substring(0, 20)}...`);
        });
        passed++;
    }
    else {
        console.log('  ❌ Version history retrieval failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 4: Rollback to Previous Version ===
console.log('Test 4: Rollback to Previous Version');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager();
    const memory = vcm.createVersionedMemory('Original content', ['test']);
    vcm.updateMemory(memory.id, 'Modified content', 'user123', 'Modification');
    vcm.updateMemory(memory.id, 'Another change', 'user123', 'Another update');
    const rolledBack = vcm.rollback(memory.id, 1, 'user123');
    if (rolledBack && rolledBack.version === 3 && rolledBack.content === 'Original content') {
        console.log('  ✅ Rollback successful');
        console.log(`     Current version: ${rolledBack.version}`);
        console.log(`     Content: ${rolledBack.content}`);
        console.log(`     Rollback reason: ${rolledBack.history[2].changeReason}`);
        passed++;
    }
    else {
        console.log('  ❌ Rollback failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 5: Get Version Diff ===
console.log('Test 5: Get Version Diff');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager();
    const memory = vcm.createVersionedMemory('Content v1', ['tag1']);
    vcm.updateMemory(memory.id, 'Content v2', 'user123', 'Changed content');
    vcm.updateMemory(memory.id, 'Content v2', 'user123', 'Changed tags', ['tag2']);
    const diff = vcm.getDiff(memory.id, 1, 3);
    if (diff.hasChanges && diff.changes) {
        console.log('  ✅ Version diff calculated successfully');
        console.log(`     Content changed: ${diff.changes.contentChanged}`);
        console.log(`     Hotness changed: ${diff.changes.hotnessChanged}`);
        console.log(`     Tags changed: ${diff.changes.tagsChanged}`);
        passed++;
    }
    else {
        console.log('  ❌ Version diff calculation failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 6: Version Statistics ===
console.log('Test 6: Version Statistics');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager();
    const memory = vcm.createVersionedMemory('Initial', ['test']);
    // Create multiple versions
    for (let i = 2; i <= 5; i++) {
        vcm.updateMemory(memory.id, `Content v${i}`, 'user123', `Update ${i}`);
    }
    const stats = vcm.getVersionStats(memory.id);
    if (stats && stats.totalVersions === 5) {
        console.log('  ✅ Version statistics retrieved successfully');
        console.log(`     Total versions: ${stats.totalVersions}`);
        console.log(`     Current version: ${stats.currentVersion}`);
        console.log(`     Average lifespan: ${(stats.averageVersionLifespan / 1000).toFixed(2)}s`);
        passed++;
    }
    else {
        console.log('  ❌ Version statistics retrieval failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 7: Cleanup Old Versions ===
console.log('Test 7: Cleanup Old Versions');
console.log('-'.repeat(70));
try {
    const vcm = new VersionControlManager({ maxVersions: 100 });
    const memory = vcm.createVersionedMemory('Initial', ['test']);
    // Create 20 versions
    for (let i = 2; i <= 20; i++) {
        vcm.updateMemory(memory.id, `Content v${i}`, 'user123', `Update ${i}`);
    }
    const removed = vcm.cleanupOldVersions(memory.id, 10);
    const finalMemory = vcm.getVersionedMemory(memory.id);
    if (removed === 10 && finalMemory && finalMemory.history.length === 10) {
        console.log('  ✅ Old versions cleaned up successfully');
        console.log(`     Removed: ${removed} versions`);
        console.log(`     Remaining: ${finalMemory.history.length} versions`);
        passed++;
    }
    else {
        console.log('  ❌ Cleanup failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Test 8: Export/Import JSON ===
console.log('Test 8: Export/Import JSON');
console.log('-'.repeat(70));
try {
    const vcm1 = new VersionControlManager();
    const memory = vcm1.createVersionedMemory('Test content', ['test']);
    vcm1.updateMemory(memory.id, 'Updated content', 'user123', 'Update');
    const exported = vcm1.exportToJSON(memory.id);
    if (exported) {
        const vcm2 = new VersionControlManager();
        const imported = vcm2.importFromJSON(exported);
        if (imported && imported.id === memory.id && imported.version === 2) {
            console.log('  ✅ Export/Import successful');
            console.log(`     Exported ID: ${imported.id}`);
            console.log(`     Imported version: ${imported.version}`);
            console.log(`     History entries: ${imported.history.length}`);
            passed++;
        }
        else {
            console.log('  ❌ Import failed');
            failed++;
        }
    }
    else {
        console.log('  ❌ Export failed');
        failed++;
    }
}
catch (error) {
    console.log('  ❌ Error:', error.message);
    failed++;
}
console.log('');
// === Summary ===
console.log('='.repeat(70));
console.log('📊 TEST SUMMARY');
console.log('='.repeat(70));
console.log(`Total Tests: ${passed + failed}`);
console.log(`✅ Passed: ${passed}`);
console.log(`❌ Failed: ${failed}`);
console.log(`📊 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
console.log('='.repeat(70));
if (failed === 0) {
    console.log('\n🎉 ALL TESTS PASSED!');
    console.log('✨ Version Control System is ready for use!');
    console.log('='.repeat(70) + '\n');
    process.exit(0);
}
else {
    console.log(`\n⚠️  ${failed} test(s) failed. Please review.`);
    console.log('='.repeat(70) + '\n');
    process.exit(1);
}
//# sourceMappingURL=test-version-control.js.map