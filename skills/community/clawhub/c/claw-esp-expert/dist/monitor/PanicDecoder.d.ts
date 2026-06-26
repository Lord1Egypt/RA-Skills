export interface PanicFrame {
    address: string;
    function?: string;
    location?: string;
}
export interface PanicDecodeResult {
    status: 'OK' | 'NO_PANIC' | 'MISSING_ELF' | 'ADDR2LINE_NOT_FOUND';
    chip?: string;
    resolvedChip?: string;
    architecture?: 'xtensa' | 'riscv';
    reason?: string;
    registers?: Record<string, string>;
    backtrace?: string[];
    decodedFrames?: PanicFrame[];
    addr2lineBin?: string;
    suggestion: string;
}
export declare class PanicDecoder {
    private readonly xtensaToolByChip;
    private readonly riscvTool;
    decodeAddresses(log: string): {
        reason?: string;
        registers: Record<string, string>;
        addresses: string[];
    };
    decode(args: {
        chip: string;
        elfPath: string;
        log: string;
        addr2lineBin?: string;
    }): Promise<PanicDecodeResult>;
    resolveChip(chip: string): string;
    private resolveArchitecture;
    private resolveAddr2lineBin;
    private extractReason;
    private extractRegisters;
    private extractAddresses;
    private runAddr2line;
    private parseAddr2line;
}
