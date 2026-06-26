"use strict";
/**
 * 双端环形缓冲区（Head-Tail Ring Buffer）
 * 实现内存保护机制，防止大输出导致 OOM
 *
 * - Head: 固定 4KB，保留初始输出（根因证据）
 * - Tail: 4KB 环形队列，保留最新输出（最新状态）
 * - 中间数据：自动丢弃
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.RingBuffer = void 0;
exports.createRingBuffer = createRingBuffer;
const constants_1 = require("./constants");
class RingBuffer {
    headBuffer;
    headLength = 0;
    headFull = false;
    tailBuffer;
    tailStart = 0;
    tailEnd = 0;
    tailFull = false;
    totalWritten = 0;
    headSize;
    tailSize;
    constructor(headSize = constants_1.TRUNCATE_HEAD_BYTES, tailSize = constants_1.TRUNCATE_TAIL_BYTES) {
        this.headSize = headSize;
        this.tailSize = tailSize;
        this.headBuffer = Buffer.alloc(headSize);
        this.tailBuffer = Buffer.alloc(tailSize);
    }
    /**
     * 写入数据到缓冲区
     * 优先写入 Head，Head 满后写入 Tail 环形队列
     */
    write(data) {
        const buffer = typeof data === 'string' ? Buffer.from(data) : data;
        const n = buffer.length;
        this.totalWritten += n;
        for (let i = 0; i < n; i++) {
            const byte = buffer[i];
            // 优先写入 Head
            if (this.headLength < this.headSize) {
                this.headBuffer[this.headLength] = byte;
                this.headLength++;
                if (this.headLength === this.headSize) {
                    this.headFull = true;
                }
            }
            else {
                // Head 已满，写入 Tail 环形队列
                this.tailBuffer[this.tailEnd] = byte;
                this.tailEnd = (this.tailEnd + 1) % this.tailSize;
                // 如果追上了起始位置，移动起始位置（丢弃最旧的数据）
                if (this.tailFull || this.tailEnd === this.tailStart) {
                    this.tailStart = (this.tailStart + 1) % this.tailSize;
                    this.tailFull = true;
                }
            }
        }
        return n;
    }
    /**
     * 获取拼接后的完整数据
     * Head + [截断提示] + Tail
     */
    getBytes() {
        // 计算 Tail 中的有效数据
        let tailData;
        if (this.tailFull) {
            // Tail 已满，从 tailStart 到 tailEnd 是有效数据
            if (this.tailEnd > this.tailStart) {
                tailData = this.tailBuffer.subarray(this.tailStart, this.tailEnd);
            }
            else if (this.tailEnd < this.tailStart) {
                // 环形跨越边界
                const part1 = this.tailBuffer.subarray(this.tailStart);
                const part2 = this.tailBuffer.subarray(0, this.tailEnd);
                tailData = Buffer.concat([part1, part2]);
            }
            else {
                // tailStart == tailEnd 且 full，说明整个 buffer 都是有效数据
                tailData = this.tailBuffer;
            }
        }
        else {
            // Tail 未满，从 0 到 tailEnd 是有效数据
            tailData = this.tailBuffer.subarray(0, this.tailEnd);
        }
        // 如果 Head 未满且 Tail 为空，直接返回 Head
        if (this.headLength < this.headSize && tailData.length === 0) {
            return this.headBuffer.subarray(0, this.headLength);
        }
        // 需要拼接 Head 和 Tail
        // 计算被丢弃的字节数
        const headData = this.headBuffer.subarray(0, this.headLength);
        const omittedBytes = Math.max(0, this.totalWritten - headData.length - tailData.length);
        // 构建结果
        if (omittedBytes > 0) {
            const placeholder = constants_1.TRUNCATE_PLACEHOLDER.replace('%d', omittedBytes.toString());
            return Buffer.concat([headData, Buffer.from(placeholder), tailData]);
        }
        return Buffer.concat([headData, tailData]);
    }
    /**
     * 获取字符串形式
     */
    toString() {
        return this.getBytes().toString('utf8');
    }
    /**
     * 获取总共写入的字节数
     */
    getTotalWritten() {
        return this.totalWritten;
    }
    /**
     * 获取头部缓冲区长度
     */
    getHeadLength() {
        return this.headLength;
    }
    /**
     * 获取尾部缓冲区有效数据长度
     */
    getTailLength() {
        if (this.tailFull) {
            if (this.tailEnd > this.tailStart) {
                return this.tailEnd - this.tailStart;
            }
            else if (this.tailEnd < this.tailStart) {
                return this.tailSize - this.tailStart + this.tailEnd;
            }
            else {
                return this.tailSize;
            }
        }
        return this.tailEnd;
    }
    /**
     * 重置缓冲区
     */
    reset() {
        this.headLength = 0;
        this.headFull = false;
        this.tailStart = 0;
        this.tailEnd = 0;
        this.tailFull = false;
        this.totalWritten = 0;
    }
    /**
     * 克隆当前缓冲区内容
     */
    clone() {
        const clone = new RingBuffer(this.headSize, this.tailSize);
        clone.headBuffer = Buffer.from(this.headBuffer);
        clone.headLength = this.headLength;
        clone.headFull = this.headFull;
        clone.tailBuffer = Buffer.from(this.tailBuffer);
        clone.tailStart = this.tailStart;
        clone.tailEnd = this.tailEnd;
        clone.tailFull = this.tailFull;
        clone.totalWritten = this.totalWritten;
        return clone;
    }
    /**
     * 是否被截断
     */
    isTruncated() {
        return this.totalWritten > constants_1.MAX_OUTPUT_BYTES;
    }
    /**
     * 获取被丢弃的字节数
     */
    getOmittedBytes() {
        const currentLength = this.headLength + this.getTailLength();
        return Math.max(0, this.totalWritten - currentLength);
    }
}
exports.RingBuffer = RingBuffer;
/**
 * 创建默认大小的 RingBuffer
 */
function createRingBuffer() {
    return new RingBuffer(constants_1.TRUNCATE_HEAD_BYTES, constants_1.TRUNCATE_TAIL_BYTES);
}
//# sourceMappingURL=ringbuf.js.map