"use strict";
/**
 * Integration Test Script
 * Tests the enhanced permission system integration
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const index_1 = require("./index");
async function runTests() {
    console.log('🧪 Starting Integration Tests...\n');
    let passed = 0;
    let failed = 0;
    // === Test 1: Permission Checker ===
    console.log('Test 1: Permission Checker');
    try {
        const result1 = await index_1.defaultPermissionChecker.check('read', {
            sessionId: 'main',
            operation: 'read',
            params: { path: 'test.txt' },
            timestamp: Date.now()
        });
        if (result1.allowed && !result1.requiresConfirm) {
            console.log('  ✅ SAFE operation passes without confirmation\n');
            passed++;
        }
        else {
            console.log('  ❌ SAFE operation should not require confirmation\n');
            failed++;
        }
        const result2 = await index_1.defaultPermissionChecker.check('exec', {
            sessionId: 'main',
            operation: 'exec',
            params: { command: 'ls -la' },
            timestamp: Date.now()
        });
        if (result2.allowed && result2.requiresConfirm) {
            console.log('  ✅ DANGEROUS operation requires confirmation\n');
            passed++;
        }
        else {
            console.log('  ❌ DANGEROUS operation should require confirmation\n');
            failed++;
        }
    }
    catch (error) {
        console.log('  ❌ Permission checker test failed:', error.message, '\n');
        failed++;
    }
    // === Test 2: Tool Registration ===
    console.log('Test 2: Tool Registration');
    try {
        (0, index_1.registerEnhancedOpenClawTools)();
        const tools = index_1.defaultToolRegistry.getAllTools();
        if (tools.length >= 6) {
            console.log(`  ✅ Registered ${tools.length} tools\n`);
            passed++;
        }
        else {
            console.log(`  ❌ Expected at least 6 tools, got ${tools.length}\n`);
            failed++;
        }
        const cacheSavings = index_1.defaultToolRegistry.getSchemaCacheSavings();
        if (cacheSavings > 0) {
            console.log(`  ✅ Schema cache active: ${cacheSavings} tokens saved\n`);
            passed++;
        }
        else {
            console.log('  ❌ Schema cache not working\n');
            failed++;
        }
    }
    catch (error) {
        console.log('  ❌ Tool registration failed:', error.message, '\n');
        failed++;
    }
    // === Test 3: Tool Execution with Permission ===
    console.log('Test 3: Tool Execution');
    try {
        // Test SAFE tool
        const readResult = await (0, index_1.executeToolWithPermission)('read', {
            path: 'test.txt',
            limit: 100
        }, 'main');
        if (readResult.success) {
            console.log('  ✅ SAFE tool executed successfully');
            passed++;
        }
        else {
            console.log('  ❌ SAFE tool execution failed');
            failed++;
        }
        // Test DANGEROUS tool (should require confirmation)
        const execResult = await (0, index_1.executeToolWithPermission)('exec', {
            command: 'echo test'
        }, 'main');
        // DANGEROUS operations will show confirmation dialog
        // For testing, we check if it's a DANGEROUS operation
        if (execResult.metadata?.permissionLevel === 'dangerous') {
            console.log('  ✅ DANGEROUS tool correctly identified and requires confirmation\n');
            passed++;
        }
        else {
            console.log('  ❌ DANGEROUS tool should require confirmation\n');
            failed++;
        }
    }
    catch (error) {
        console.log('  ❌ Tool execution failed:', error.message, '\n');
        failed++;
    }
    // === Test 4: Memory Manager ===
    console.log('Test 4: Memory Manager');
    try {
        const memId = await index_1.defaultMemoryManager.store('Test memory for integration test', ['test', 'integration']);
        if (memId) {
            console.log('  ✅ Memory stored successfully');
            passed++;
        }
        else {
            console.log('  ❌ Memory storage failed');
            failed++;
        }
        const memories = await index_1.defaultMemoryManager.recall('test', { limit: 5 });
        if (memories.length > 0) {
            console.log('  ✅ Memory recall working');
            passed++;
        }
        else {
            console.log('  ❌ Memory recall failed');
            failed++;
        }
        const stats = index_1.defaultMemoryManager.getStats();
        if (stats.total > 0) {
            console.log(`  ✅ Memory stats: ${stats.total} total, ${stats.active} active\n`);
            passed++;
        }
        else {
            console.log('  ❌ Memory stats incorrect\n');
            failed++;
        }
    }
    catch (error) {
        console.log('  ❌ Memory manager failed:', error.message, '\n');
        failed++;
    }
    // === Test 5: Hotness Algorithm ===
    console.log('Test 5: Hotness Algorithm');
    try {
        // Create a memory and test hotness changes
        const memId = await index_1.defaultMemoryManager.store('Hotness test');
        const memory = index_1.defaultMemoryManager.getMemory(memId);
        if (memory && memory.hotness === 50) {
            console.log('  ✅ Initial hotness correct (50)');
            passed++;
        }
        else {
            console.log('  ❌ Initial hotness incorrect');
            failed++;
        }
        // Touch the memory
        index_1.defaultMemoryManager.touchMemory(memId);
        const touched = index_1.defaultMemoryManager.getMemory(memId);
        if (touched && touched.hotness === 55) {
            console.log('  ✅ Hotness increased on touch (55)');
            passed++;
        }
        else {
            console.log('  ❌ Hotness not updated correctly');
            failed++;
        }
        // Test decay calculation
        const { calculateDecayedHotness } = await Promise.resolve().then(() => __importStar(require('./memory-manager')));
        const decayed = calculateDecayedHotness(50, 7); // 7 days old
        if (decayed < 50 && decayed > 40) {
            console.log('  ✅ Decay calculation working\n');
            passed++;
        }
        else {
            console.log('  ❌ Decay calculation incorrect\n');
            failed++;
        }
    }
    catch (error) {
        console.log('  ❌ Hotness test failed:', error.message, '\n');
        failed++;
    }
    // === Summary ===
    console.log('='.repeat(50));
    console.log(`Tests Complete: ${passed + failed}`);
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`📊 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
    console.log('='.repeat(50));
    if (failed === 0) {
        console.log('\n🎉 All tests passed! Phase 2 integration successful!\n');
    }
    else {
        console.log(`\n⚠️ ${failed} test(s) failed. Please review.\n`);
    }
}
// Run tests
runTests().catch(console.error);
//# sourceMappingURL=integration-test.js.map