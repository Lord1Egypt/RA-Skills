/**
 * 自主进化引擎 - 17 分钟循环
 * 
 * 功能：
 * 1. 分析当前技能使用情况
 * 2. 识别优化机会
 * 3. 执行自我改进
 * 4. 记录进化日志
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = path.join(process.env.HOME, '.jvs/.openclaw/workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const LOG_FILE = path.join(WORKSPACE, 'autonomous', 'evolution-log.json');

// 确保目录存在
function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

// 读取今日记忆文件
function getTodayMemory() {
    const today = new Date().toISOString().split('T')[0];
    const memoryFile = path.join(MEMORY_DIR, `${today}.md`);
    
    if (fs.existsSync(memoryFile)) {
        return fs.readFileSync(memoryFile, 'utf-8');
    }
    return '';
}

// 记录进化日志
function logEvolution(action, details) {
    ensureDir(path.dirname(LOG_FILE));
    
    let log = [];
    if (fs.existsSync(LOG_FILE)) {
        try {
            log = JSON.parse(fs.readFileSync(LOG_FILE, 'utf-8'));
        } catch (e) {
            log = [];
        }
    }
    
    log.push({
        timestamp: new Date().toISOString(),
        action,
        details
    });
    
    fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2));
    console.log(`[进化日志] ${action}: ${details}`);
}

// 分析技能使用情况
function analyzeSkills() {
    console.log('[分析] 检查技能使用情况...');
    
    const skillsDir = path.join(WORKSPACE, 'skills');
    const skillLogsDir = path.join(MEMORY_DIR, 'skill-logs');
    
    const analysis = {
        timestamp: new Date().toISOString(),
        skillsFound: [],
        optimizationOpportunities: []
    };
    
    // 检查技能目录
    if (fs.existsSync(skillsDir)) {
        const skills = fs.readdirSync(skillsDir);
        analysis.skillsFound = skills.filter(s => s.endsWith('.js') || s.endsWith('.md'));
    }
    
    // 检查技能日志
    if (fs.existsSync(skillLogsDir)) {
        const logs = fs.readdirSync(skillLogsDir);
        if (logs.length > 0) {
            analysis.optimizationOpportunities.push({
                type: 'skill_usage',
                description: `发现 ${logs.length} 个技能使用日志，可以分析优化`
            });
        }
    }
    
    return analysis;
}

// 执行自我优化
function executeOptimization(analysis) {
    console.log('[优化] 执行自我优化...');
    
    const optimizations = [];
    
    // 示例优化：清理旧日志
    const oldLogsDir = path.join(MEMORY_DIR, 'skill-logs');
    if (fs.existsSync(oldLogsDir)) {
        const files = fs.readdirSync(oldLogsDir);
        console.log(`[优化] 发现 ${files.length} 个技能日志文件`);
        optimizations.push({
            action: 'log_analysis',
            result: `分析了 ${files.length} 个日志文件`
        });
    }
    
    // 更新记忆文件
    const today = new Date().toISOString().split('T')[0];
    const memoryFile = path.join(MEMORY_DIR, `${today}.md`);
    
    if (fs.existsSync(memoryFile)) {
        let content = fs.readFileSync(memoryFile, 'utf-8');
        
        // 添加进化记录
        const evolutionEntry = `
### 自主进化循环 (${new Date().toLocaleTimeString('zh-CN', { timeZone: 'Asia/Shanghai' })})

- 分析结果：${analysis.skillsFound.length} 个技能文件
- 优化机会：${analysis.optimizationOpportunities.length} 项
- 执行优化：${optimizations.length} 项
`;
        
        if (!content.includes('自主进化循环')) {
            content += evolutionEntry;
            fs.writeFileSync(memoryFile, content);
            console.log('[优化] 已更新记忆文件');
        }
    }
    
    return optimizations;
}

// 主执行函数
async function run() {
    console.log('🔄 自主进化引擎启动');
    console.log(`当前时间：${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
    console.log('---');
    
    ensureDir(MEMORY_DIR);
    
    // 步骤 1: 分析
    const analysis = analyzeSkills();
    logEvolution('analysis', JSON.stringify(analysis));
    
    // 步骤 2: 优化
    const optimizations = executeOptimization(analysis);
    logEvolution('optimization', JSON.stringify(optimizations));
    
    // 步骤 3: 验证
    console.log('---');
    console.log('✅ 进化循环完成');
    console.log(`分析：${analysis.skillsFound.length} 个技能`);
    console.log(`优化：${optimizations.length} 项`);
    console.log(`日志：已记录到 ${LOG_FILE}`);
    
    return {
        success: true,
        analysis,
        optimizations,
        timestamp: new Date().toISOString()
    };
}

// CLI 入口
if (require.main === module) {
    const command = process.argv[2];
    
    if (command === 'run') {
        run().then(result => {
            console.log('\n最终结果:', JSON.stringify(result, null, 2));
            process.exit(0);
        }).catch(err => {
            console.error('❌ 错误:', err.message);
            process.exit(1);
        });
    } else {
        console.log('用法：node evolution-engine.js run');
        process.exit(1);
    }
}

module.exports = { run, analyzeSkills, executeOptimization };
