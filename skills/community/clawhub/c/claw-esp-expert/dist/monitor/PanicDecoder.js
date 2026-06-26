"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PanicDecoder = void 0;
const process_1 = require("../common/process");
const fs_1 = require("../common/fs");
class PanicDecoder {
    constructor() {
        this.xtensaToolByChip = {
            esp32: 'xtensa-esp32-elf-addr2line',
            esp32s2: 'xtensa-esp32s2-elf-addr2line',
            esp32s3: 'xtensa-esp32s3-elf-addr2line'
        };
        this.riscvTool = 'riscv32-esp-elf-addr2line';
    }
    decodeAddresses(log) {
        const registers = this.extractRegisters(log);
        const reason = this.extractReason(log);
        const addresses = this.extractAddresses(log, registers);
        return { reason, registers, addresses };
    }
    async decode(args) {
        const resolvedChip = this.resolveChip(args.chip);
        const architecture = this.resolveArchitecture(resolvedChip);
        const { reason, registers, addresses } = this.decodeAddresses(args.log);
        if (!reason && addresses.length === 0) {
            return {
                status: 'NO_PANIC',
                chip: args.chip,
                resolvedChip,
                architecture,
                suggestion: '未在日志中识别到 panic/backtrace 关键信息，请提供更完整的设备崩溃日志。'
            };
        }
        if (!await (0, fs_1.pathExists)(args.elfPath)) {
            return {
                status: 'MISSING_ELF',
                chip: args.chip,
                resolvedChip,
                architecture,
                reason,
                registers,
                backtrace: addresses,
                suggestion: '已识别到 panic 日志，但缺少 ELF 文件，无法执行 addr2line 定位。请提供 build 产物中的 ELF 路径。'
            };
        }
        const addr2lineBin = args.addr2lineBin || this.resolveAddr2lineBin(resolvedChip, architecture);
        const decodedFrames = await this.runAddr2line(addr2lineBin, args.elfPath, addresses);
        if (!decodedFrames) {
            return {
                status: 'ADDR2LINE_NOT_FOUND',
                chip: args.chip,
                resolvedChip,
                architecture,
                reason,
                registers,
                backtrace: addresses,
                addr2lineBin,
                suggestion: `已识别到 panic 日志，但未找到可执行的 ${addr2lineBin}。请先导出 ESP-IDF toolchain 环境。`
            };
        }
        return {
            status: 'OK',
            chip: args.chip,
            resolvedChip,
            architecture,
            reason,
            registers,
            backtrace: addresses,
            decodedFrames,
            addr2lineBin,
            suggestion: reason
                ? `已解码 panic：${reason}。请优先检查首个命中的源码位置。`
                : '已解码 backtrace，请优先检查首个命中的源码位置。'
        };
    }
    resolveChip(chip) {
        return chip.toLowerCase().replace(/[^a-z0-9]/g, '');
    }
    resolveArchitecture(chip) {
        if (chip === 'esp32' || chip === 'esp32s2' || chip === 'esp32s3') {
            return 'xtensa';
        }
        return 'riscv';
    }
    resolveAddr2lineBin(chip, architecture) {
        if (architecture === 'xtensa') {
            return this.xtensaToolByChip[chip] || 'xtensa-esp32-elf-addr2line';
        }
        return this.riscvTool;
    }
    extractReason(log) {
        const guruMatch = log.match(/Guru Meditation Error: Core\s+\d+ panic'ed \(([^)]+)\)/);
        if (guruMatch?.[1])
            return guruMatch[1];
        const abortMatch = log.match(/abort\(\) was called at PC [^\n]+/);
        if (abortMatch)
            return 'abort()';
        const exceptionMatch = log.match(/Unhandled debug exception: ([^\n]+)/);
        if (exceptionMatch?.[1])
            return exceptionMatch[1].trim();
        return undefined;
    }
    extractRegisters(log) {
        const registers = {};
        const pairs = log.matchAll(/\b([A-Z]{2,8})\s*:\s*(0x[0-9a-fA-F]+)/g);
        for (const match of pairs) {
            registers[match[1]] = match[2];
        }
        return registers;
    }
    extractAddresses(log, registers) {
        const addresses = [];
        const seen = new Set();
        const backtraceMatch = log.match(/Backtrace:\s*([^\n]+)/);
        if (backtraceMatch?.[1]) {
            const pairs = backtraceMatch[1].match(/0x[0-9a-fA-F]+(?::0x[0-9a-fA-F]+)?/g) || [];
            for (const pair of pairs) {
                const address = pair.split(':')[0];
                if (!seen.has(address)) {
                    seen.add(address);
                    addresses.push(address);
                }
            }
        }
        for (const key of ['PC', 'MEPC', 'RA', 'EXCVADDR', 'MTVAL']) {
            const value = registers[key];
            if (value && !seen.has(value)) {
                seen.add(value);
                addresses.push(value);
            }
        }
        return addresses;
    }
    async runAddr2line(addr2lineBin, elfPath, addresses) {
        if (addresses.length === 0) {
            return [];
        }
        try {
            const stdout = await (0, process_1.execFileText)(addr2lineBin, ['-pfiaC', '-e', elfPath, ...addresses]);
            return this.parseAddr2line(stdout, addresses);
        }
        catch {
            return null;
        }
    }
    parseAddr2line(stdout, addresses) {
        const lines = stdout.replace(/\r\n/g, '\n').split('\n').filter(Boolean);
        const frames = [];
        for (let index = 0; index < lines.length; index += 2) {
            const symbolLine = lines[index] || '';
            const locationLine = lines[index + 1] || '';
            const address = addresses[Math.floor(index / 2)] || '';
            const cleaned = symbolLine.replace(/^0x[0-9a-fA-F]+:\s*/, '');
            const functionName = cleaned.includes(' at ') ? cleaned.split(' at ')[0].trim() : cleaned.trim();
            frames.push({
                address,
                function: functionName || undefined,
                location: locationLine || undefined
            });
        }
        return frames;
    }
}
exports.PanicDecoder = PanicDecoder;
//# sourceMappingURL=PanicDecoder.js.map