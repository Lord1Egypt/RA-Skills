/**
 * 信息信号识别系统
 */
import { UnifiedMemorySystem } from '../core/memory';
type SignalLevel = 'noise' | 'signal' | 'core' | 'meta';
type TimeSensitivity = 'immediate' | 'continuous' | 'delayed' | 'cyclical' | 'meta';
type ImpactDepth = 'tool' | 'method' | 'strategy' | 'cognition' | 'worldview';
export interface Signal {
    title: string;
    source: string;
    level: SignalLevel;
    timeSensitivity: TimeSensitivity;
    impactDepth: ImpactDepth;
    actionability: number;
    compoundValue: number;
    reason: string;
}
export interface Pattern {
    name: string;
    level: string;
    description: string;
}
export declare class SignalRecognitionSystem {
    private memory;
    private systemName;
    constructor(memory: UnifiedMemorySystem);
    evaluateSignal(signal: Omit<Signal, 'level' | 'reason'>): {
        level: SignalLevel;
        reason: string;
    };
    addSignal(signal: Omit<Signal, 'level' | 'reason'>): void;
    generateDailyScanReport(date: string, rawSignals: Omit<Signal, 'level' | 'reason'>[]): {
        date: string;
        signals: Signal[];
        patterns: Pattern[];
        actions: string[];
    };
    private identifyPatterns;
    querySignals(query: string): Signal[];
    syncToOtherSystems(): void;
}
export {};
//# sourceMappingURL=signal.d.ts.map