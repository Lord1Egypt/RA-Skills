"use strict";
/**
 * 信息信号识别系统
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.SignalRecognitionSystem = void 0;
class SignalRecognitionSystem {
    constructor(memory) {
        this.systemName = 'signal';
        this.memory = memory;
    }
    evaluateSignal(signal) {
        const timeValue = signal.timeSensitivity === 'meta' ? 10 :
            signal.timeSensitivity === 'delayed' ? 8 :
                signal.timeSensitivity === 'continuous' ? 6 :
                    signal.timeSensitivity === 'cyclical' ? 4 : 2;
        const depthValue = signal.impactDepth === 'worldview' ? 10 :
            signal.impactDepth === 'cognition' ? 8 :
                signal.impactDepth === 'strategy' ? 6 :
                    signal.impactDepth === 'method' ? 4 : 2;
        const totalValue = (timeValue + depthValue + signal.actionability + signal.compoundValue) / 4;
        if (totalValue >= 8)
            return { level: 'meta', reason: `综合价值${totalValue.toFixed(1)}，属于元信号` };
        if (totalValue >= 6)
            return { level: 'core', reason: `综合价值${totalValue.toFixed(1)}，属于核心信号` };
        if (totalValue >= 3)
            return { level: 'signal', reason: `综合价值${totalValue.toFixed(1)}，属于普通信号` };
        return { level: 'noise', reason: `综合价值${totalValue.toFixed(1)}，属于噪音` };
    }
    addSignal(signal) {
        const evaluation = this.evaluateSignal(signal);
        const fullSignal = { ...signal, ...evaluation };
        if (evaluation.level === 'meta' || evaluation.level === 'core') {
            this.memory.addToL2(signal.title, fullSignal, 'insight', evaluation.level === 'meta' ? 5 : 4, [signal.impactDepth, signal.timeSensitivity], this.systemName);
            if (evaluation.level === 'meta') {
                this.memory.addToL3({
                    id: '', level: 'L3', category: 'worldview', key: signal.title, value: fullSignal,
                    tags: [signal.impactDepth], importance: 5, system: this.systemName,
                    createdAt: new Date().toISOString(), accessedAt: new Date().toISOString(), accessCount: 0
                });
            }
        }
        else if (evaluation.level === 'signal') {
            this.memory.addToL1(signal.title, `${signal.source}: ${evaluation.reason}`, 'task', 2);
        }
    }
    generateDailyScanReport(date, rawSignals) {
        const signals = rawSignals.map(s => {
            const evaluation = this.evaluateSignal(s);
            return { ...s, ...evaluation };
        });
        const valuableSignals = signals.filter(s => s.level !== 'noise');
        for (const signal of valuableSignals) {
            this.addSignal(signal);
        }
        const patterns = this.identifyPatterns(valuableSignals);
        const actions = valuableSignals.filter(s => s.level === 'core' || s.level === 'meta').map(s => `关注：${s.title} - ${s.reason}`);
        return { date, signals: valuableSignals, patterns, actions };
    }
    identifyPatterns(signals) {
        const patterns = [];
        const depthGroups = {};
        for (const s of signals) {
            if (!depthGroups[s.impactDepth])
                depthGroups[s.impactDepth] = [];
            depthGroups[s.impactDepth].push(s);
        }
        for (const [depth, group] of Object.entries(depthGroups)) {
            if (group.length >= 3) {
                patterns.push({
                    name: `${depth}层信号聚集`,
                    level: 'domain',
                    description: `在${depth}层面发现${group.length}个相关信号`
                });
            }
        }
        return patterns;
    }
    querySignals(query) {
        const results = this.memory.queryL2(query, undefined, 3);
        return results.filter(e => e.system === this.systemName).map(e => e.value);
    }
    syncToOtherSystems() {
        const worldviews = this.memory.queryL3('worldview');
        this.memory.syncToSystem('workflow', worldviews);
        this.memory.syncToSystem('goal', worldviews);
    }
}
exports.SignalRecognitionSystem = SignalRecognitionSystem;
//# sourceMappingURL=signal.js.map