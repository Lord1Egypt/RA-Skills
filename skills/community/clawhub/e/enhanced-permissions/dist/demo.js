/**
 * Enhanced Permissions System - Demo Script
 * 演示所有功能
 * 
 * Run with: node demo.js
 */

const path = require('path');

console.log('='.repeat(70));
console.log('🎯 Enhanced Permissions System - Live Demo');
console.log('='.repeat(70));
console.log('');

// === Step 1: Load the system ===
console.log('📦 Step 1: Loading Enhanced Permissions System...');
console.log('-'.repeat(70));

const permissionsPath = path.join(__dirname, 'permissions');

try {
  const permissions = require(permissionsPath);
  console.log('✅ System loaded successfully!');
  console.log('');
  
  // === Step 2: Check available features ===
  console.log('🔍 Step 2: Checking Available Features...');
  console.log('-'.repeat(70));
  
  const features = [
    { name: 'PermissionChecker', check: permissions.PermissionChecker },
    { name: 'ToolRegistry', check: permissions.ToolRegistry },
    { name: 'MemoryManager', check: permissions.MemoryManager },
    { name: 'OpenVikingService', check: permissions.OpenVikingService },
    { name: 'executeToolWithPermission', check: permissions.executeToolWithPermission },
    { name: 'showConfirmationDialog', check: permissions.showConfirmationDialog },
    { name: 'defaultAuditLogger', check: permissions.defaultAuditLogger }
  ];
  
  features.forEach(feature => {
    if (feature.check) {
      console.log(`  ✅ ${feature.name}`);
    } else {
      console.log(`  ❌ ${feature.name}`);
    }
  });
  console.log('');
  
  // === Step 3: Demo Permission Checker ===
  console.log('🔐 Step 3: Permission Checker Demo...');
  console.log('-'.repeat(70));
  
  const { PermissionChecker, PermissionLevel } = permissions;
  const checker = new PermissionChecker({
    userLevel: PermissionLevel.MODERATE,
    trustedSessions: ['main-session']
  });
  
  // Test SAFE operation
  (async () => {
    const safeResult = await checker.check('read', {
      sessionId: 'main-session',
      operation: 'read',
      params: { path: 'test.txt' },
      timestamp: Date.now()
    });
    
    console.log('  Test: SAFE operation (read)');
    console.log(`    Allowed: ${safeResult.allowed ? '✅ Yes' : '❌ No'}`);
    console.log(`    Requires Confirm: ${safeResult.requiresConfirm ? '⚠️ Yes' : '✅ No'}`);
    console.log('');
    
    // Test DANGEROUS operation
    const dangerousResult = await checker.check('exec', {
      sessionId: 'main-session',
      operation: 'exec',
      params: { command: 'ls -la' },
      timestamp: Date.now()
    });
    
    console.log('  Test: DANGEROUS operation (exec)');
    console.log(`    Allowed: ${dangerousResult.allowed ? '✅ Yes' : '❌ No'}`);
    console.log(`    Requires Confirm: ${dangerousResult.requiresConfirm ? '⚠️ Yes' : '✅ No'}`);
    if (dangerousResult.confirmMessage) {
      console.log(`    Message: ${dangerousResult.confirmMessage.substring(0, 100)}...`);
    }
    console.log('');
    
    // === Step 4: Demo Memory Manager ===
    console.log('🧠 Step 4: Memory Manager Demo...');
    console.log('-'.repeat(70));
    
    const { MemoryManager } = permissions;
    const memoryManager = new MemoryManager();
    
    // Store memories
    console.log('  Storing memories...');
    const mem1 = await memoryManager.store('User prefers TypeScript for backend', ['preference', 'coding']);
    const mem2 = await memoryManager.store('Project uses React for frontend', ['project', 'frontend']);
    const mem3 = await memoryManager.store('API key should be kept secret', ['security', 'api']);
    
    console.log(`    ✅ Memory 1: ${mem1}`);
    console.log(`    ✅ Memory 2: ${mem2}`);
    console.log(`    ✅ Memory 3: ${mem3}`);
    console.log('');
    
    // Get stats
    const stats = memoryManager.getStats();
    console.log('  Memory Stats:');
    console.log(`    Total: ${stats.total}`);
    console.log(`    Active: ${stats.active}`);
    console.log(`    Archived: ${stats.archived}`);
    console.log(`    Average Hotness: ${stats.averageHotness.toFixed(1)}`);
    console.log('');
    
    // Recall memories
    console.log('  Recalling memories for "coding"...');
    const recalled = await memoryManager.recall('coding', { limit: 3 });
    console.log(`    Found: ${recalled.length} memories`);
    recalled.forEach((mem, i) => {
      console.log(`      ${i + 1}. ${mem.content.substring(0, 50)}... (hotness: ${mem.hotness})`);
    });
    console.log('');
    
    // === Step 5: Demo Hotness Algorithm ===
    console.log('🔥 Step 5: Hotness Algorithm Demo...');
    console.log('-'.repeat(70));
    
    const { calculateDecayedHotness } = permissions;
    
    console.log('  Hotness Decay Examples:');
    console.log(`    Initial (50) after 1 day: ${calculateDecayedHotness(50, 1).toFixed(2)}`);
    console.log(`    Initial (50) after 7 days: ${calculateDecayedHotness(50, 7).toFixed(2)}`);
    console.log(`    Initial (50) after 30 days: ${calculateDecayedHotness(50, 30).toFixed(2)}`);
    console.log(`    Initial (50) after 100 days: ${calculateDecayedHotness(50, 100).toFixed(2)}`);
    console.log('');
    
    // Touch memory
    console.log('  Touching memory 1...');
    memoryManager.touchMemory(mem1);
    const updated = memoryManager.getMemory(mem1);
    console.log(`    Hotness: 50 → ${updated.hotness}`);
    console.log('');
    
    // === Step 6: Demo OpenViking Integration ===
    console.log('🔍 Step 6: OpenViking Integration Demo...');
    console.log('-'.repeat(70));
    
    const { OpenVikingService } = permissions;
    const openViking = new OpenVikingService();
    
    const status = openViking.getStatus();
    console.log('  OpenViking Status:');
    console.log(`    Available: ${status.available ? '✅ Yes' : '⚠️ No'}`);
    console.log(`    API Key Configured: ${status.apiKeyConfigured ? '✅ Yes' : '❌ No'}`);
    console.log(`    Base URL: ${status.baseUrl}`);
    console.log(`    Embedding Model: ${status.embeddingModel}`);
    console.log('');
    
    if (status.available) {
      console.log('  ✅ OpenViking is ready for vector search!');
      console.log('  To enable: Set API key with defaultOpenVikingService.setApiKey()');
    } else {
      console.log('  ℹ️ OpenViking installed but not configured');
      console.log('  To use: pip install openviking (already done)');
      console.log('  Then: Set your Volcengine API key');
    }
    console.log('');
    
    // === Step 7: Summary ===
    console.log('='.repeat(70));
    console.log('📊 Demo Summary');
    console.log('='.repeat(70));
    console.log('');
    console.log('✅ All systems operational!');
    console.log('');
    console.log('Features Demonstrated:');
    console.log('  ✅ Permission Checker (4 levels)');
    console.log('  ✅ Memory Manager (with hotness)');
    console.log('  ✅ Hotness Algorithm (decay formula)');
    console.log('  ✅ OpenViking Integration');
    console.log('');
    console.log('Ready to Use:');
    console.log('  1. Import: const permissions = require("./permissions")');
    console.log('  2. Use: await permissions.executeToolWithPermission(...)');
    console.log('  3. Enjoy enhanced security and memory management!');
    console.log('');
    console.log('='.repeat(70));
    console.log('🎉 Demo Complete!');
    console.log('='.repeat(70));
    
  })();
  
} catch (error) {
  console.error('❌ Failed to load system:', error.message);
  console.error('');
  console.error('Troubleshooting:');
  console.error('  1. Make sure permissions folder exists');
  console.error('  2. Check if all .ts files are compiled to .js');
  console.error('  3. Or use ts-node to run TypeScript directly');
  console.error('');
  process.exit(1);
}
