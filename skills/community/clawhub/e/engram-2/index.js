// index.js

const CapsuleStore = require('./src/storage/capsule-store');
const Validator = require('./src/storage/validator');
const EnvChecker = require('./src/core/env-checker');
const EngramCore = require('./src/core/engram-core');

// 实例化主脑中枢 (由于性能原因使用单例模式)
let _engramInstance = null;
const getEngram = (config = {}) => {
    if(!_engramInstance) _engramInstance = new EngramCore(config);
    return _engramInstance;
}

/**
 * engram - API 对接网关
 * 供其它智能 Agent 平台或插件集成使用
 */
module.exports = {
    AEIFValidator: Validator,
    Store: CapsuleStore,
    EnvFingerprinter: EnvChecker,
    Core: EngramCore,
    
    /**
     * 集成网关：处理指令或直接进行经验咨询
     * @param {string} query - 报错或搜索词
     * @param {Object} context - 环境上下文
     */
    consultAgent: async (query, context = {}) => {
        const engram = getEngram();
        await engram.init();
        
        const advice = await engram.hook.scanAndIntercept(query, context.taskIntent || '');
        
        return {
           aeifVersion: "1.0",
           timestamp: new Date().toISOString(),
           advice: advice,
           hasMatch: !!advice
        };
    }
};
