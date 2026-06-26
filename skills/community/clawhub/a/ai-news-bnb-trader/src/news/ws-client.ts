import { EventEmitter } from 'events';
import { NewsItem } from '../types.js';

export class NewsWsClient extends EventEmitter {
  private ws?: WebSocket;
  private retry = 1000;
  constructor(private url: string) { super(); }

  start() {
    this.ws = new WebSocket(this.url);
    this.ws.onopen = () => { this.retry = 1000; };
    this.ws.onmessage = (m) => {
      try {
        const p = JSON.parse(String(m.data));
        this.emit('news', p as NewsItem);
      } catch {
        this.emit('error', new Error('bad ws payload'));
      }
    };
    this.ws.onclose = () => {
      setTimeout(() => this.start(), this.retry);
      this.retry = Math.min(this.retry * 2, 30000);
    };
    this.ws.onerror = () => this.ws?.close();
  }
}
