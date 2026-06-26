import { type PanicDecodeResult } from './PanicDecoder';
export interface MonitorAnalysisResult {
    status: 'NO_PANIC' | 'PANIC_DETECTED' | 'PANIC_DECODED';
    chip: string;
    resolvedChip: string;
    markers: string[];
    excerpt: string[];
    panic?: PanicDecodeResult;
    suggestion: string;
}
export declare class MonitorAnalyzer {
    private readonly panicDecoder;
    private readonly excerptLineCount;
    analyze(args: {
        chip: string;
        log: string;
        elfPath?: string;
        addr2lineBin?: string;
    }): Promise<MonitorAnalysisResult>;
    private detectMarkers;
    private extractExcerpt;
}
