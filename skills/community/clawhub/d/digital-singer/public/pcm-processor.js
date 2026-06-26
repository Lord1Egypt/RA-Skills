class PcmProcessor extends AudioWorkletProcessor {
  constructor() { super(); this.buffer = []; this.chunkSize = 1600; /* 100ms @ 16kHz */ }
  process(inputs) {
    const input = inputs[0]?.[0];
    if (!input) return true;
    for (let i = 0; i < input.length; i++) {
      this.buffer.push(Math.max(-1, Math.min(1, input[i])));
    }
    while (this.buffer.length >= this.chunkSize) {
      const chunk = this.buffer.splice(0, this.chunkSize);
      const pcm = new Int16Array(chunk.length);
      for (let i = 0; i < chunk.length; i++) pcm[i] = chunk[i] * 0x7fff;
      this.port.postMessage({ type: 'audioData', data: pcm.buffer }, [pcm.buffer]);
    }
    return true;
  }
}
registerProcessor('pcm-processor', PcmProcessor);
