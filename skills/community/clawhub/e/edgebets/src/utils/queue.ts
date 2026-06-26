import { sleep } from './polling';

/**
 * Simple queue to rate-limit API requests
 */
export class RequestQueue {
  private queue: Array<() => Promise<void>> = [];
  private running = 0;
  private maxConcurrent: number;
  private delayBetween: number;
  private lastRequestTime = 0;

  constructor(maxConcurrent = 1, delayBetween = 2000) {
    this.maxConcurrent = maxConcurrent;
    this.delayBetween = delayBetween;
  }

  /**
   * Add a task to the queue and wait for its result
   */
  async add<T>(task: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      const wrappedTask = async () => {
        try {
          // Ensure minimum delay between requests
          const now = Date.now();
          const timeSinceLastRequest = now - this.lastRequestTime;
          if (timeSinceLastRequest < this.delayBetween) {
            await sleep(this.delayBetween - timeSinceLastRequest);
          }

          this.lastRequestTime = Date.now();
          const result = await task();
          resolve(result);
        } catch (error) {
          reject(error);
        }
      };

      this.queue.push(wrappedTask);
      this.processQueue();
    });
  }

  /**
   * Process queued tasks respecting concurrency limits
   */
  private async processQueue(): Promise<void> {
    if (this.running >= this.maxConcurrent || this.queue.length === 0) {
      return;
    }

    const task = this.queue.shift();
    if (!task) return;

    this.running++;
    try {
      await task();
    } finally {
      this.running--;
      this.processQueue();
    }
  }

  /**
   * Get current queue status
   */
  getStatus(): { queued: number; running: number } {
    return {
      queued: this.queue.length,
      running: this.running,
    };
  }
}
