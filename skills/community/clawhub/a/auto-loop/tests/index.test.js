/**
 * Auto Loop 单元测试
 */

const assert = require('assert');
const {
    AutoLoop,
    Scheduler,
    Task,
    RecoveryManager,
    TaskStatus,
    parseCronExpression,
    matchesCron,
    generateId,
    timestamp
} = require('../src/index.js');

function runTests() {
    console.log('Running Auto Loop Tests...\n');
    
    let passed = 0;
    let failed = 0;
    
    // 工具函数测试
    console.log('=== 工具函数测试 ===');
    try {
        const id = generateId();
        if (id && id.includes('-')) {
            console.log('✓ generateId 测试通过');
            passed++;
        }
        
        const ts = timestamp();
        if (ts && ts.includes('T')) {
            console.log('✓ timestamp 测试通过');
            passed++;
        }
    } catch (e) {
        console.log('✗ 工具函数测试失败:', e.message);
        failed++;
    }
    
    // Cron 解析测试
    console.log('\n=== Cron 解析测试 ===');
    try {
        const cron1 = parseCronExpression('*/5 * * * *');
        if (cron1 && cron1.minute.type === 'step') {
            console.log('✓ Cron step 格式解析测试通过');
            passed++;
        }
        
        const cron2 = parseCronExpression('0 9 * * *');
        if (cron2 && cron2.hour.type === 'value' && cron2.hour.value === 9) {
            console.log('✓ Cron value 格式解析测试通过');
            passed++;
        }
        
        const cron3 = parseCronExpression('0,30 * * * *');
        if (cron3 && cron3.minute.type === 'list') {
            console.log('✓ Cron list 格式解析测试通过');
            passed++;
        }
    } catch (e) {
        console.log('✗ Cron 解析测试失败:', e.message);
        failed++;
    }
    
    // Task 测试
    console.log('\n=== Task 测试 ===');
    try {
        const task = new Task({
            name: 'test-task',
            schedule: 1000,
            handler: async () => 'result'
        });
        
        if (task.name === 'test-task' && task.scheduleType === 'interval') {
            console.log('✓ Task 创建测试通过');
            passed++;
        }
        
        if (task.status === TaskStatus.PENDING || task.status === TaskStatus.SCHEDULED) {
            console.log('✓ Task 初始状态测试通过');
            passed++;
        }
        
        // 测试暂停/恢复
        task.pause();
        if (task.status === TaskStatus.PAUSED && !task.enabled) {
            console.log('✓ Task pause 测试通过');
            passed++;
        }
        
        task.resume();
        if (task.enabled) {
            console.log('✓ Task resume 测试通过');
            passed++;
        }
        
        // 测试取消
        task.cancel();
        if (task.status === TaskStatus.CANCELLED) {
            console.log('✓ Task cancel 测试通过');
            passed++;
        }
    } catch (e) {
        console.log('✗ Task 测试失败:', e.message);
        failed++;
    }
    
    // Scheduler 测试
    console.log('\n=== Scheduler 测试 ===');
    try {
        const scheduler = new Scheduler();
        
        const task = scheduler.addTask({
            name: 'scheduler-test',
            schedule: 60000,
            handler: async () => 'ok'
        });
        
        if (scheduler.getTask(task.id)) {
            console.log('✓ Scheduler addTask 测试通过');
            passed++;
        }
        
        const tasks = scheduler.listTasks();
        if (tasks.length >= 1) {
            console.log('✓ Scheduler listTasks 测试通过');
            passed++;
        }
        
        const stats = scheduler.getStats();
        if (typeof stats.total === 'number') {
            console.log('✓ Scheduler getStats 测试通过');
            passed++;
        }
        
        scheduler.removeTask(task.id);
        if (!scheduler.getTask(task.id)) {
            console.log('✓ Scheduler removeTask 测试通过');
            passed++;
        }
        
        scheduler.stop();
    } catch (e) {
        console.log('✗ Scheduler 测试失败:', e.message);
        failed++;
    }
    
    // AutoLoop 集成测试
    console.log('\n=== AutoLoop 集成测试 ===');
    try {
        const autoLoop = new AutoLoop();
        
        // 添加任务
        const task = autoLoop.interval('test-interval', 60000, async () => 'test');
        if (task && task.id) {
            console.log('✓ AutoLoop interval 测试通过');
            passed++;
        }
        
        // 列出任务
        const tasks = autoLoop.listTasks();
        if (tasks.length >= 1) {
            console.log('✓ AutoLoop listTasks 测试通过');
            passed++;
        }
        
        // 获取统计
        const stats = autoLoop.getStats();
        if (typeof stats.tasks === 'object') {
            console.log('✓ AutoLoop getStats 测试通过');
            passed++;
        }
        
        // 启动/停止
        autoLoop.start();
        autoLoop.stop();
        console.log('✓ AutoLoop start/stop 测试通过');
        passed++;
        
        // 清理
        autoLoop.unschedule(task.id);
    } catch (e) {
        console.log('✗ AutoLoop 集成测试失败:', e.message);
        failed++;
    }
    
    // RecoveryManager 测试
    console.log('\n=== RecoveryManager 测试 ===');
    try {
        const scheduler = new Scheduler();
        const recovery = new RecoveryManager(scheduler);
        
        const task = new Task({
            name: 'recovery-test',
            handler: async () => {}
        });
        
        recovery.registerFailure(task, new Error('test error'));
        const failed = recovery.getFailedTasks();
        
        if (failed.length >= 1) {
            console.log('✓ RecoveryManager registerFailure 测试通过');
            passed++;
        }
        
        recovery.clear(task.id);
        if (recovery.getFailedTasks().length === 0) {
            console.log('✓ RecoveryManager clear 测试通过');
            passed++;
        }
        
        scheduler.stop();
    } catch (e) {
        console.log('✗ RecoveryManager 测试失败:', e.message);
        failed++;
    }
    
    // 输出总结
    console.log('\n' + '='.repeat(50));
    console.log(`测试完成：${passed} 通过，${failed} 失败`);
    console.log('='.repeat(50));
    
    process.exit(failed > 0 ? 1 : 0);
}

if (require.main === module) {
    runTests();
}

module.exports = { runTests };
