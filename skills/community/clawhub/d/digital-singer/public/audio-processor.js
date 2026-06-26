/**
 * 麦克风 → 16kHz 单声道 Int16 PCM
 * 参考 NuwaAI demo: audio-processor.js
 * 浏览器 AudioContext sampleRate 通常是 48000/44100，需要重采样到 16kHz
 */
class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.inRate = sampleRate; // 浏览器实际采样率
    this.outRate = 16000;
    this.chunkSize = 3200; // 16kHz × 200ms = 3200 样点
    this.floatBuf = new Float32Array(this.chunkSize * 4);
    this.floatLen = 0;
    this.resampleAcc = 0;
    this.port.onmessage = (e) => {
      if (e.data?.type === 'reset') {
        this.floatLen = 0;
        this.resampleAcc = 0;
      }
    };
  }

  process(inputs) {
    const input = inputs[0];
    if (!input || input.length === 0) return true;
    const ch = input[0];
    const inRate = this.inRate;
    const outRate = this.outRate;

    for (let i = 0; i < ch.length; i++) {
      this.resampleAcc += outRate;
      while (this.resampleAcc >= inRate) {
        this.resampleAcc -= inRate;
        if (this.floatLen < this.floatBuf.length) {
          this.floatBuf[this.floatLen++] = ch[i];
        }
      }
    }

    if (this.floatLen >= this.chunkSize) {
      const pcm = new Int16Array(this.chunkSize);
      for (let i = 0; i < this.chunkSize; i++) {
        const x = this.floatBuf[i];
        pcm[i] = Math.max(-32768, Math.min(32767, Math.round(x * 32768)));
      }
      this.port.postMessage({ type: 'audioData', data: pcm.buffer }, [pcm.buffer]);
      const rest = this.floatLen - this.chunkSize;
      if (rest > 0) this.floatBuf.copyWithin(0, this.chunkSize, this.floatLen);
      this.floatLen = rest;
    }
    return true;
  }
}
registerProcessor('audio-processor', AudioProcessor);
