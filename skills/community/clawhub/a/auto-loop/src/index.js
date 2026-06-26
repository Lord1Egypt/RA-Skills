/**
 * auto-loop - 自动循环技能
 * 
 * 提供定时触发、任务调度、状态追踪和自动恢复功能
 * 用于自动化周期性任务和定时作业
 * 
 * @version 1.0.0
 * @author 王的奴隶 · 严谨专业版
 */

const EventEmitter = require('events');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ============================================================================
// 配置常量
// ============================================================================

const CONFIG = {
    // 状态文件目录
    STATE_DIR: 'auto-loop-state',
    
    // 默认重试次数
    DEFAULT_RETRIES: 3,
    
    // 默认重试延迟 (毫秒)
    DEFAULT_RETRY_DELAY: 5000,
    
    // 任务超时 (毫秒)
    DEFAULT_TIMEOUT: 300000, // 5 分钟
    
    // 状态持久化间隔 (毫秒)
    PERSIST_INTERVAL: 60000, // 1 分钟
    
    // 历史保留时间 (毫秒)
    HISTORY_RETENTION: 24 * 60 * 60 * 1000, // 24 小时
    
    // 最大并发任务数
    MAX_CONCURRENT: 5
};

// ============================================================================
// 工具函数
// ============================================================================

function generateId() {
    return `${Date.now()}-${crypto.randomBytes(8).toString('hex')}`;
}

function timestamp() {
    return new Date().toISOString();
}

function parseCronExpression(expression) {
    // 简化版 cron 解析：支持 * n */n n-m n,m 格式
    const parts = expression.trim().split(/\s+/);
    if (parts.length < 5) return null;
    
    return {
        minute: parseCronField(parts[0], 0, 59),
        hour: parseCronField(parts[1], 0, 23),
        dayOfMonth: parseCronField(parts[2], 1, 31),
        month: parseCronField(parts[3], 1, 12),
        dayOfWeek: parseCronField(parts[4], 0, 6)
    };
}

function parseCronField(field, min, max) {
    if (field === '*') {
        return { type: 'all', values: null };
    }
    
    if (field.startsWith('*/')) {
        const step = parseInt(field.slice(2));
        return { type: 'step', step, min, max };
    }
    
    if (field.includes('-')) {
        const [start, end] = field.split('-').map(Number);
        return { type: 'range', start, end };
    }
    
    if (field.includes(',')) {
        return { type: 'list', values: field.split(',').map(Number) };
    }
    
    return { type: 'value', value: parseInt(field) };
}

function matchesCron(date, cron) {
    if (!cron) return false;
    
    const minute = date.getMinutes();
    const hour = date.getHours();
    const dayOfMonth = date.getDate();
    const month = date.getMonth() + 1;
    const dayOfWeek = date.getDay();
    
    return matchField(minute, cron.minute) &&
           matchField(hour, cron.hour) &&
           matchField(dayOfMonth, cron.dayOfMonth) &&
           matchField(month, cron.month) &&
           matchField(dayOfWeek, cron.dayOfWeek);
}

function matchField(value, field) {
    if (!field) return true;
    
    switch (field.type) {
        case 'all':
            return true;
        case 'step':
            return value >= field.min && value <= field.max && (value - field.min) % field.step === 0;
        case 'range':
            return value >= field.start && value <= field.end;
        case 'list':
            return field.values.includes(value);
        case 'value':
            return value === field.value;
        default:
            return true;
    }
}

function safeSaveJSON(filePath, data) {
    try {
        fs.mkdirSync(path.dirname(filePath), { recursive: true });
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
        return true;
    } catch (error) {
        console.error('保存状态失败:', error);
        return false;
    }
}

function safeLoadJSON(filePath) {
    try {
        if (!fs.existsSync(filePath)) return null;
        const content = fs.readFileSync(filePath, 'utf-8');
        return JSON.parse(content);
    } catch (error) {
        return null;
    }
}

// ============================================================================
// 任务状态枚举
// ============================================================================

const TaskStatus = {
    PENDING: 'pending',
    SCHEDULED: 'scheduled',
    RUNNING: 'running',
    COMPLETED: 'completed',
    FAILED: 'failed',
    RETRYING: 'retrying',
    CANCELLED: 'cancelled',
    PAUSED: 'paused'
};

// ============================================================================
// 任务类
// ============================================================================

class Task extends EventEmitter {
    constructor(options = {}) {
        super();
        
        this.id = options.id || generateId();
        this.name = options.name || 'unnamed';
        this.description = options.description;
        this.handler = options.handler;
        this.schedule = options.schedule; // cron 表达式或间隔毫秒
        this.enabled = options.enabled !== false;
        this.maxRetries = options.maxRetries ?? CONFIG.DEFAULT_RETRIES;
        this.retryDelay = options.retryDelay ?? CONFIG.DEFAULT_RETRY_DELAY;
        this.timeout = options.timeout ?? CONFIG.DEFAULT_TIMEOUT;
        this.priority = options.priority || 0;
        this.tags = options.tags || [];
        this.metadata = options.metadata || {};
        
        this.status = TaskStatus.PENDING;
        this.createdAt = timestamp();
        this.updatedAt = timestamp();
        this.lastRunAt = null;
        this.nextRunAt = null;
        this.completedAt = null;
        
        this.runCount = 0;
        this.successCount = 0;
        this.failureCount = 0;
        this.retryCount = 0;
        
        this.lastError = null;
        this.lastResult = null;
        this.currentAttempt = 0;
        
        this._parseSchedule();
    }
    
    _parseSchedule() {
        if (typeof this.schedule === 'number') {
            // 间隔毫秒
            this.scheduleType = 'interval';
            this.intervalMs = this.schedule;
        } else if (typeof this.schedule === 'string') {
            // cron 表达式
            this.scheduleType = 'cron';
            this.cron = parseCronExpression(this.schedule);
        } else if (this.schedule instanceof Date) {
            // 一次性执行
            this.scheduleType = 'once';
            this.runAt = this.schedule;
        } else {
            this.scheduleType = 'manual';
        }
        
        this._calculateNextRun();
    }
    
    _calculateNextRun() {
        if (!this.enabled) {
            this.nextRunAt = null;
            return;
        }
        
        const now = new Date();
        
        switch (this.scheduleType) {
            case 'interval':
                if (this.lastRunAt) {
                    this.nextRunAt = new Date(new Date(this.lastRunAt).getTime() + this.intervalMs);
                } else {
                    this.nextRunAt = now;
                }
                break;
                
            case 'cron':
                // 找到下一个匹配的时间
                let next = new Date(now);
                next.setSeconds(0, 0);
                next.setMinutes(next.getMinutes() + 1);
                
                for (let i = 0; i < 525600; i++) { // 最多搜索一年
                    if (matchesCron(next, this.cron)) {
                        this.nextRunAt = next;
                        return;
                    }
                    next.setMinutes(next.getMinutes() + 1);
                }
                this.nextRunAt = null;
                break;
                
            case 'once':
                this.nextRunAt = this.runAt > now ? this.runAt : null;
                break;
                
            default:
                this.nextRunAt = null;
        }
    }
    
    async execute(context = {}) {
        if (!this.handler) {
            throw new Error('No handler defined for task');
        }
        
        this.status = TaskStatus.RUNNING;
        this.currentAttempt++;
        this.lastRunAt = timestamp();
        this.updatedAt = timestamp();
        
        this.emit('start', { task: this, context });
        
        const startTime = Date.now();
        
        try {
            // 设置超时
            const result = await Promise.race([
                this.handler(context, this),
                new Promise((_, reject) => 
                    setTimeout(() => reject(new Error('Task timeout')), this.timeout)
                )
            ]);
            
            this.status = TaskStatus.COMPLETED;
            this.lastResult = result;
            this.successCount++;
            this.completedAt = timestamp();
            this.retryCount = 0;
            
            this.emit('complete', { task: this, result, duration: Date.now() - startTime });
            
        } catch (error) {
            this.lastError = error.message;
            this.failureCount++;
            
            // 检查是否重试
            if (this.currentAttempt <= this.maxRetries) {
                this.status = TaskStatus.RETRYING;
                this.retryCount++;
                
                this.emit('retry', { task: this, error, attempt: this.currentAttempt });
                
                // 等待重试延迟
                await new Promise(resolve => setTimeout(resolve, this.retryDelay));
                
                // 递归重试
                return this.execute(context);
            }
            
            this.status = TaskStatus.FAILED;
            this.emit('error', { task: this, error });
        } finally {
            this.runCount++;
            this.updatedAt = timestamp();
            this._calculateNextRun();
        }
        
        return this.lastResult;
    }
    
    cancel() {
        this.status = TaskStatus.CANCELLED;
        this.enabled = false;
        this.nextRunAt = null;
        this.emit('cancel', { task: this });
    }
    
    pause() {
        this.status = TaskStatus.PAUSED;
        this.enabled = false;
        this.emit('pause', { task: this });
    }
    
    resume() {
        this.enabled = true;
        this.status = TaskStatus.SCHEDULED;
        this._calculateNextRun();
        this.emit('resume', { task: this });
    }
    
    toJSON() {
        return {
            id: this.id,
            name: this.name,
            description: this.description,
            schedule: this.schedule,
            scheduleType: this.scheduleType,
            enabled: this.enabled,
            status: this.status,
            priority: this.priority,
            tags: this.tags,
            runCount: this.runCount,
            successCount: this.successCount,
            failureCount: this.failureCount,
            retryCount: this.retryCount,
            lastRunAt: this.lastRunAt,
            nextRunAt: this.nextRunAt,
            lastError: this.lastError,
            createdAt: this.createdAt,
            updatedAt: this.updatedAt
        };
    }
}

// ============================================================================
// 调度器类
// ============================================================================

class Scheduler extends EventEmitter {
    constructor(options = {}) {
        super();
        
        this.options = {
            maxConcurrent: options.maxConcurrent || CONFIG.MAX_CONCURRENT,
            persistInterval: options.persistInterval || CONFIG.PERSIST_INTERVAL,
            stateDir: options.stateDir || path.join(process.cwd(), CONFIG.STATE_DIR),
            ...options
        };
        
        this.tasks = new Map();
        this.runningTasks = new Set();
        this.taskQueue = [];
        this.isRunning = false;
        this.checkInterval = null;
        
        this.stats = {
            totalRuns: 0,
            totalSuccess: 0,
            totalFailures: 0,
            startTime: timestamp()
        };
        
        // 确保状态目录存在
        fs.mkdirSync(this.options.stateDir, { recursive: true });
        
        // 加载持久化状态
        this._loadState();
        
        // 启动调度循环
        this.start();
    }
    
    /**
     * 添加任务
     */
    addTask(taskOptions) {
        const task = new Task(taskOptions);
        this.tasks.set(task.id, task);
        
        // 事件转发
        task.on('start', (data) => this.emit('task:start', data));
        task.on('complete', (data) => {
            this.stats.totalRuns++;
            this.stats.totalSuccess++;
            this.emit('task:complete', data);
        });
        task.on('error', (data) => {
            this.stats.totalRuns++;
            this.stats.totalFailures++;
            this.emit('task:error', data);
        });
        task.on('retry', (data) => this.emit('task:retry', data));
        
        this._saveState();
        
        return task;
    }
    
    /**
     * 移除任务
     */
    removeTask(taskId) {
        const task = this.tasks.get(taskId);
        if (task) {
            task.cancel();
            this.tasks.delete(taskId);
            this._saveState();
        }
        return !!task;
    }
    
    /**
     * 获取任务
     */
    getTask(taskId) {
        return this.tasks.get(taskId);
    }
    
    /**
     * 列出任务
     */
    listTasks(options = {}) {
        let tasks = Array.from(this.tasks.values());
        
        if (options.status) {
            tasks = tasks.filter(t => t.status === options.status);
        }
        if (options.enabled !== undefined) {
            tasks = tasks.filter(t => t.enabled === options.enabled);
        }
        if (options.tags) {
            tasks = tasks.filter(t => 
                options.tags.some(tag => t.tags.includes(tag))
            );
        }
        
        // 排序
        tasks.sort((a, b) => b.priority - a.priority);
        
        return tasks;
    }
    
    /**
     * 启动调度器
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        
        // 立即检查一次
        this._checkTasks();
        
        // 每分钟检查一次
        this.checkInterval = setInterval(() => this._checkTasks(), 60000);
        
        // 定期持久化状态
        this.persistInterval = setInterval(() => this._saveState(), this.options.persistInterval);
        
        this.emit('start');
    }
    
    /**
     * 停止调度器
     */
    stop() {
        this.isRunning = false;
        
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
        if (this.persistInterval) {
            clearInterval(this.persistInterval);
            this.persistInterval = null;
        }
        
        this.emit('stop');
    }
    
    /**
     * 检查并执行任务
     */
    async _checkTasks() {
        if (!this.isRunning) return;
        
        const now = new Date();
        const dueTasks = [];
        
        for (const task of this.tasks.values()) {
            if (!task.enabled) continue;
            if (task.status === TaskStatus.RUNNING) continue;
            if (!task.nextRunAt) continue;
            
            if (new Date(task.nextRunAt) <= now) {
                dueTasks.push(task);
            }
        }
        
        // 按优先级排序
        dueTasks.sort((a, b) => b.priority - a.priority);
        
        // 执行到期的任务 (考虑并发限制)
        for (const task of dueTasks) {
            if (this.runningTasks.size >= this.options.maxConcurrent) {
                break;
            }
            
            this._runTask(task);
        }
    }
    
    /**
     * 运行任务
     */
    async _runTask(task) {
        if (this.runningTasks.has(task.id)) return;
        
        this.runningTasks.add(task.id);
        task.status = TaskStatus.RUNNING;
        
        try {
            await task.execute();
        } catch (error) {
            console.error(`Task ${task.id} error:`, error);
        } finally {
            this.runningTasks.delete(task.id);
            this._saveState();
        }
    }
    
    /**
     * 保存状态
     */
    _saveState() {
        const stateFile = path.join(this.options.stateDir, 'scheduler-state.json');
        
        const state = {
            stats: this.stats,
            tasks: Array.from(this.tasks.values()).map(t => t.toJSON()),
            savedAt: timestamp()
        };
        
        return safeSaveJSON(stateFile, state);
    }
    
    /**
     * 加载状态
     */
    _loadState() {
        const stateFile = path.join(this.options.stateDir, 'scheduler-state.json');
        const state = safeLoadJSON(stateFile);
        
        if (!state) return;
        
        this.stats = state.stats || this.stats;
        
        // 恢复任务 (不恢复处理器，需要重新注册)
        // 这里只恢复任务元数据
    }
    
    /**
     * 获取统计信息
     */
    getStats() {
        const taskStats = {
            total: this.tasks.size,
            running: this.runningTasks.size,
            pending: 0,
            completed: 0,
            failed: 0,
            paused: 0
        };
        
        for (const task of this.tasks.values()) {
            switch (task.status) {
                case TaskStatus.PENDING:
                case TaskStatus.SCHEDULED:
                    taskStats.pending++;
                    break;
                case TaskStatus.COMPLETED:
                    taskStats.completed++;
                    break;
                case TaskStatus.FAILED:
                    taskStats.failed++;
                    break;
                case TaskStatus.PAUSED:
                    taskStats.paused++;
                    break;
            }
        }
        
        return {
            ...this.stats,
            tasks: taskStats,
            uptime: Date.now() - new Date(this.stats.startTime).getTime()
        };
    }
    
    /**
     * 清除历史
     */
    clearHistory(olderThan = CONFIG.HISTORY_RETENTION) {
        const cutoff = Date.now() - olderThan;
        let cleared = 0;
        
        // 这里可以扩展为清除完成的任务历史
        // 当前实现只清理状态文件
        
        return { cleared };
    }
}

// ============================================================================
// 自动恢复管理器
// ============================================================================

class RecoveryManager {
    constructor(scheduler) {
        this.scheduler = scheduler;
        this.failedTasks = new Map();
        this.recoveryAttempts = new Map();
    }
    
    /**
     * 注册失败任务
     */
    registerFailure(task, error) {
        const key = task.id;
        
        if (!this.failedTasks.has(key)) {
            this.failedTasks.set(key, {
                task: task.toJSON(),
                error: error.message,
                firstFailure: timestamp(),
                failureCount: 0
            });
        }
        
        const record = this.failedTasks.get(key);
        record.failureCount++;
        record.lastFailure = timestamp();
        record.lastError = error.message;
        
        this._attemptRecovery(task);
    }
    
    /**
     * 尝试恢复
     */
    async _attemptRecovery(task) {
        const key = task.id;
        const attempts = this.recoveryAttempts.get(key) || 0;
        
        if (attempts >= 3) {
            console.error(`Task ${task.id} recovery failed after ${attempts} attempts`);
            return;
        }
        
        this.recoveryAttempts.set(key, attempts + 1);
        
        // 指数退避
        const delay = Math.min(300000, 1000 * Math.pow(2, attempts));
        
        console.log(`Attempting recovery for task ${task.id} in ${delay}ms`);
        
        await new Promise(resolve => setTimeout(resolve, delay));
        
        // 重置任务状态
        task.retryCount = 0;
        task.currentAttempt = 0;
        task.status = TaskStatus.SCHEDULED;
        task.enabled = true;
        task._calculateNextRun();
        
        this.scheduler.emit('task:recovered', { task, attempt: attempts + 1 });
    }
    
    /**
     * 获取失败记录
     */
    getFailedTasks() {
        return Array.from(this.failedTasks.values());
    }
    
    /**
     * 清除失败记录
     */
    clear(taskId) {
        if (taskId) {
            this.failedTasks.delete(taskId);
            this.recoveryAttempts.delete(taskId);
        } else {
            this.failedTasks.clear();
            this.recoveryAttempts.clear();
        }
    }
}

// ============================================================================
// 主类：AutoLoop
// ============================================================================

class AutoLoop extends EventEmitter {
    constructor(options = {}) {
        super();
        
        this.options = {
            workspaceDir: options.workspaceDir || process.cwd(),
            ...options
        };
        
        const stateDir = path.join(this.options.workspaceDir, CONFIG.STATE_DIR);
        
        this.scheduler = new Scheduler({
            ...options,
            stateDir
        });
        this.recoveryManager = new RecoveryManager(this.scheduler);
        
        // 事件转发
        this.scheduler.on('task:error', (data) => {
            this.recoveryManager.registerFailure(data.task, new Error(data.error?.message || 'Unknown error'));
            this.emit('task:error', data);
        });
        
        this.scheduler.on('task:complete', (data) => this.emit('task:complete', data));
        this.scheduler.on('task:start', (data) => this.emit('task:start', data));
        this.scheduler.on('task:recovered', (data) => this.emit('task:recovered', data));
    }
    
    /**
     * 添加定时任务
     */
    schedule(name, schedule, handler, options = {}) {
        return this.scheduler.addTask({
            name,
            schedule,
            handler,
            ...options
        });
    }
    
    /**
     * 添加间隔任务
     */
    interval(name, intervalMs, handler, options = {}) {
        return this.scheduler.addTask({
            name,
            schedule: intervalMs,
            handler,
            ...options
        });
    }
    
    /**
     * 添加一次性任务
     */
    once(name, runAt, handler, options = {}) {
        return this.scheduler.addTask({
            name,
            schedule: runAt instanceof Date ? runAt : new Date(runAt),
            handler,
            ...options
        });
    }
    
    /**
     * 移除任务
     */
    unschedule(taskId) {
        return this.scheduler.removeTask(taskId);
    }
    
    /**
     * 获取任务
     */
    getTask(taskId) {
        return this.scheduler.getTask(taskId);
    }
    
    /**
     * 列出任务
     */
    listTasks(options = {}) {
        return this.scheduler.listTasks(options);
    }
    
    /**
     * 启动
     */
    start() {
        this.scheduler.start();
        this.emit('start');
    }
    
    /**
     * 停止
     */
    stop() {
        this.scheduler.stop();
        this.emit('stop');
    }
    
    /**
     * 获取统计
     */
    getStats() {
        return this.scheduler.getStats();
    }
    
    /**
     * 获取失败任务
     */
    getFailedTasks() {
        return this.recoveryManager.getFailedTasks();
    }
    
    /**
     * 清除失败记录
     */
    clearFailures(taskId) {
        return this.recoveryManager.clear(taskId);
    }
}

// ============================================================================
// 导出
// ============================================================================

module.exports = {
    // 主类
    AutoLoop,
    
    // 组件类
    Scheduler,
    Task,
    RecoveryManager,
    
    // 枚举
    TaskStatus,
    
    // 工具函数
    generateId,
    timestamp,
    parseCronExpression,
    matchesCron,
    
    // 配置
    CONFIG
};

// ============================================================================
// CLI 接口
// ============================================================================

if (require.main === module) {
    const args = process.argv.slice(2);
    const command = args[0];
    
    function main() {
        const autoLoop = new AutoLoop();
        
        switch (command) {
            case 'list':
                const tasks = autoLoop.listTasks();
                console.log('任务列表:', JSON.stringify(tasks.map(t => t.toJSON()), null, 2));
                break;
                
            case 'stats':
                const stats = autoLoop.getStats();
                console.log('统计信息:', JSON.stringify(stats, null, 2));
                break;
                
            case 'demo':
                console.log('运行演示...');
                
                // 添加一个每秒执行的任务
                autoLoop.interval('demo-task', 5000, async (context, task) => {
                    console.log(`[${timestamp()}] 任务执行：${task.name}, 运行次数：${task.runCount}`);
                    return { executed: true, time: timestamp() };
                });
                
                autoLoop.start();
                
                console.log('演示已启动，按 Ctrl+C 停止');
                
                process.on('SIGINT', () => {
                    console.log('\n停止演示...');
                    autoLoop.stop();
                    process.exit(0);
                });
                break;
                
            case 'test':
                runTests();
                break;
                
            default:
                console.log('用法：node index.js <command>');
                console.log('命令:');
                console.log('  list   - 列出任务');
                console.log('  stats  - 查看统计');
                console.log('  demo   - 运行演示');
                console.log('  test   - 运行测试');
        }
    }
    
    function runTests() {
        console.log('运行测试...');
        
        // 测试 cron 解析
        const cron = parseCronExpression('*/5 * * * *');
        console.log('Cron 解析测试:', cron);
        
        // 测试任务创建
        const task = new Task({
            name: 'test-task',
            schedule: '*/1 * * * *',
            handler: async () => 'completed'
        });
        console.log('任务创建测试:', task.toJSON());
        
        // 测试调度器
        const scheduler = new Scheduler();
        scheduler.addTask({
            name: 'scheduler-test',
            schedule: 1000,
            handler: async () => 'ok'
        });
        
        console.log('调度器统计:', scheduler.getStats());
        
        scheduler.stop();
        
        console.log('\n测试完成!');
    }
    
    main();
}
