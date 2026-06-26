/**
 * 双端环形缓冲区（Head-Tail Ring Buffer）
 * 实现内存保护机制，防止大输出导致 OOM
 *
 * - Head: 固定 4KB，保留初始输出（根因证据）
 * - Tail: 4KB 环形队列，保留最新输出（最新状态）
 * - 中间数据：自动丢弃
 */
export declare class RingBuffer {
    private headBuffer;
    private headLength;
    private headFull;
    private tailBuffer;
    private tailStart;
    private tailEnd;
    private tailFull;
    private totalWritten;
    private readonly headSize;
    private readonly tailSize;
    constructor(headSize?: number, tailSize?: number);
    /**
     * 写入数据到缓冲区
     * 优先写入 Head，Head 满后写入 Tail 环形队列
     */
    write(data: Buffer | string): number;
    /**
     * 获取拼接后的完整数据
     * Head + [截断提示] + Tail
     */
    getBytes(): Buffer;
    /**
     * 获取字符串形式
     */
    toString(): string;
    /**
     * 获取总共写入的字节数
     */
    getTotalWritten(): number;
    /**
     * 获取头部缓冲区长度
     */
    getHeadLength(): number;
    /**
     * 获取尾部缓冲区有效数据长度
     */
    getTailLength(): number;
    /**
     * 重置缓冲区
     */
    reset(): void;
    /**
     * 克隆当前缓冲区内容
     */
    clone(): RingBuffer;
    /**
     * 是否被截断
     */
    isTruncated(): boolean;
    /**
     * 获取被丢弃的字节数
     */
    getOmittedBytes(): number;
}
/**
 * 创建默认大小的 RingBuffer
 */
export declare function createRingBuffer(): RingBuffer;
//# sourceMappingURL=ringbuf.d.ts.map