import { Platform, RateLimitConfig } from '../types/index.js';

interface RateLimiterState {
  requests: number[];
}

export class RateLimiter {
  private limits: Map<Platform, RateLimitConfig> = new Map();
  private states: Map<Platform, RateLimiterState> = new Map();

  constructor() {
    // Default rate limits per platform
    this.limits.set('taobao', { maxRequests: 10, windowMs: 60000 });
    this.limits.set('jd', { maxRequests: 15, windowMs: 60000 });
    this.limits.set('pdd', { maxRequests: 8, windowMs: 60000 });
    this.limits.set('douyin', { maxRequests: 10, windowMs: 60000 });
  }

  async waitForSlot(platform: Platform): Promise<void> {
    const config = this.limits.get(platform);
    if (!config) return;

    let state = this.states.get(platform);
    if (!state) {
      state = { requests: [] };
      this.states.set(platform, state);
    }

    const now = Date.now();
    const windowStart = now - config.windowMs;

    // Remove old requests outside the window
    state.requests = state.requests.filter(time => time > windowStart);

    // If at limit, wait until the oldest request expires
    if (state.requests.length >= config.maxRequests) {
      const oldestRequest = state.requests[0];
      const waitTime = oldestRequest + config.windowMs - now + 1000; // +1s buffer
      
      if (waitTime > 0) {
        console.log(`⏳ ${platform} 请求频率限制，等待 ${Math.ceil(waitTime / 1000)} 秒...`);
        await this.sleep(waitTime);
      }
      
      // Recurse to check again
      return this.waitForSlot(platform);
    }

    // Record this request
    state.requests.push(now);
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  setLimit(platform: Platform, config: RateLimitConfig): void {
    this.limits.set(platform, config);
  }
}