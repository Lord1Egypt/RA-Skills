"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.MonitorAnalyzer = void 0;
const PanicDecoder_1 = require("./PanicDecoder");
class MonitorAnalyzer {
    constructor() {
        this.panicDecoder = new PanicDecoder_1.PanicDecoder();
        this.excerptLineCount = 12;
    }
    async analyze(args) {
        const resolvedChip = this.panicDecoder.resolveChip(args.chip);
        const markers = this.detectMarkers(args.log);
        const excerpt = this.extractExcerpt(args.log);
        if (markers.length === 0) {
            return {
                status: 'NO_PANIC',
                chip: args.chip,
                resolvedChip,
                markers,
                excerpt,
                suggestion: '当前 monitor 日志中未识别到 panic/backtrace 特征。'
            };
        }
        if (!args.elfPath) {
            return {
                status: 'PANIC_DETECTED',
                chip: args.chip,
                resolvedChip,
                markers,
                excerpt,
                suggestion: '已识别到 panic/backtrace 特征。请提供当前固件的 ELF 路径，以便执行 addr2line 解码。'
            };
        }
        const panic = await this.panicDecoder.decode({
            chip: args.chip,
            elfPath: args.elfPath,
            log: args.log,
            addr2lineBin: args.addr2lineBin
        });
        return {
            status: panic.status === 'OK' ? 'PANIC_DECODED' : 'PANIC_DETECTED',
            chip: args.chip,
            resolvedChip,
            markers,
            excerpt,
            panic,
            suggestion: panic.status === 'OK'
                ? panic.suggestion
                : `已识别到 panic/backtrace 特征，但暂未完成解码：${panic.suggestion}`
        };
    }
    detectMarkers(log) {
        const markers = [];
        const checks = [
            ['guru_meditation', /Guru Meditation Error:/],
            ['backtrace', /Backtrace:/],
            ['abort', /abort\(\) was called/],
            ['register_dump', /\b(?:PC|MEPC|EXCVADDR|MTVAL)\s*:\s*0x[0-9a-fA-F]+/],
            ['rebooting', /Rebooting\.\.\./],
            ['reset_reason', /rst:0x[0-9a-fA-F]+/]
        ];
        for (const [name, pattern] of checks) {
            if (pattern.test(log)) {
                markers.push(name);
            }
        }
        return markers;
    }
    extractExcerpt(log) {
        const lines = log.replace(/\r\n/g, '\n').split('\n').filter((line) => line.trim().length > 0);
        return lines.slice(-this.excerptLineCount);
    }
}
exports.MonitorAnalyzer = MonitorAnalyzer;
//# sourceMappingURL=MonitorAnalyzer.js.map