/**
 * Observable Pattern
 * 
 * A lightweight reactive programming pattern for event streams.
 * Similar to RxJS but minimal and focused on AlephNet's needs.
 */

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Observer interface
 */
export interface Observer<T> {
  next: (value: T) => void;
  error?: (err: Error) => void;
  complete?: () => void;
}

/**
 * Subscription interface for cleanup
 */
export interface Subscription {
  unsubscribe(): void;
  readonly closed: boolean;
}

/**
 * Observable producer function
 */
export type Producer<T> = (observer: Observer<T>) => (() => void) | void;

// ═══════════════════════════════════════════════════════════════════════════
// OBSERVABLE CLASS
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Observable implementation
 */
export class Observable<T> {
  constructor(private producer: Producer<T>) {}
  
  /**
   * Subscribe to the observable
   */
  subscribe(observer: Observer<T> | ((value: T) => void)): Subscription {
    const normalizedObserver: Observer<T> = 
      typeof observer === 'function' 
        ? { next: observer }
        : observer;
    
    let closed = false;
    const cleanup = this.producer({
      next: (value) => {
        if (!closed) normalizedObserver.next(value);
      },
      error: (err) => {
        if (!closed) {
          closed = true;
          normalizedObserver.error?.(err);
        }
      },
      complete: () => {
        if (!closed) {
          closed = true;
          normalizedObserver.complete?.();
        }
      }
    });
    
    return {
      unsubscribe: () => {
        if (!closed) {
          closed = true;
          cleanup?.();
        }
      },
      get closed() { return closed; }
    };
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // OPERATORS
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Transform values
   */
  map<U>(fn: (value: T) => U): Observable<U> {
    return new Observable<U>((observer) => {
      const sub = this.subscribe({
        next: (value) => observer.next(fn(value)),
        error: observer.error,
        complete: observer.complete
      });
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Filter values
   */
  filter(predicate: (value: T) => boolean): Observable<T> {
    return new Observable<T>((observer) => {
      const sub = this.subscribe({
        next: (value) => {
          if (predicate(value)) observer.next(value);
        },
        error: observer.error,
        complete: observer.complete
      });
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Take first n values
   */
  take(count: number): Observable<T> {
    return new Observable<T>((observer) => {
      let remaining = count;
      const sub = this.subscribe({
        next: (value) => {
          if (remaining > 0) {
            remaining--;
            observer.next(value);
            if (remaining === 0) {
              sub.unsubscribe();
              observer.complete?.();
            }
          }
        },
        error: observer.error,
        complete: observer.complete
      });
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Skip first n values
   */
  skip(count: number): Observable<T> {
    return new Observable<T>((observer) => {
      let skipped = 0;
      const sub = this.subscribe({
        next: (value) => {
          if (skipped >= count) {
            observer.next(value);
          } else {
            skipped++;
          }
        },
        error: observer.error,
        complete: observer.complete
      });
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Debounce values
   */
  debounce(ms: number): Observable<T> {
    return new Observable<T>((observer) => {
      let timeout: NodeJS.Timeout | null = null;
      
      const sub = this.subscribe({
        next: (value) => {
          if (timeout) clearTimeout(timeout);
          timeout = setTimeout(() => observer.next(value), ms);
        },
        error: (err) => {
          if (timeout) clearTimeout(timeout);
          observer.error?.(err);
        },
        complete: () => {
          if (timeout) clearTimeout(timeout);
          observer.complete?.();
        }
      });
      
      return () => {
        if (timeout) clearTimeout(timeout);
        sub.unsubscribe();
      };
    });
  }
  
  /**
   * Throttle values
   */
  throttle(ms: number): Observable<T> {
    return new Observable<T>((observer) => {
      let lastTime = 0;
      
      const sub = this.subscribe({
        next: (value) => {
          const now = Date.now();
          if (now - lastTime >= ms) {
            lastTime = now;
            observer.next(value);
          }
        },
        error: observer.error,
        complete: observer.complete
      });
      
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Merge with another observable
   */
  merge(other: Observable<T>): Observable<T> {
    return new Observable<T>((observer) => {
      let completed1 = false;
      let completed2 = false;
      
      const checkComplete = () => {
        if (completed1 && completed2) {
          observer.complete?.();
        }
      };
      
      const sub1 = this.subscribe({
        next: observer.next,
        error: observer.error,
        complete: () => { completed1 = true; checkComplete(); }
      });
      
      const sub2 = other.subscribe({
        next: observer.next,
        error: observer.error,
        complete: () => { completed2 = true; checkComplete(); }
      });
      
      return () => {
        sub1.unsubscribe();
        sub2.unsubscribe();
      };
    });
  }
  
  /**
   * Scan (reduce over time)
   */
  scan<U>(fn: (acc: U, value: T) => U, initial: U): Observable<U> {
    return new Observable<U>((observer) => {
      let acc = initial;
      
      const sub = this.subscribe({
        next: (value) => {
          acc = fn(acc, value);
          observer.next(acc);
        },
        error: observer.error,
        complete: observer.complete
      });
      
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Distinct until changed
   */
  distinctUntilChanged(compare?: (a: T, b: T) => boolean): Observable<T> {
    return new Observable<T>((observer) => {
      let lastValue: T | undefined;
      let hasValue = false;
      const eq = compare || ((a, b) => a === b);
      
      const sub = this.subscribe({
        next: (value) => {
          if (!hasValue || !eq(lastValue!, value)) {
            hasValue = true;
            lastValue = value;
            observer.next(value);
          }
        },
        error: observer.error,
        complete: observer.complete
      });
      
      return () => sub.unsubscribe();
    });
  }
  
  /**
   * Convert to promise (first value)
   */
  toPromise(): Promise<T> {
    return new Promise((resolve, reject) => {
      const sub = this.take(1).subscribe({
        next: (value) => {
          resolve(value);
        },
        error: reject,
        complete: () => reject(new Error('Observable completed without emitting'))
      });
    });
  }
  
  // ═══════════════════════════════════════════════════════════════════════
  // STATIC FACTORIES
  // ═══════════════════════════════════════════════════════════════════════
  
  /**
   * Create from a single value
   */
  static of<T>(...values: T[]): Observable<T> {
    return new Observable<T>((observer) => {
      for (const value of values) {
        observer.next(value);
      }
      observer.complete?.();
    });
  }
  
  /**
   * Create from an array
   */
  static from<T>(iterable: Iterable<T>): Observable<T> {
    return new Observable<T>((observer) => {
      for (const value of iterable) {
        observer.next(value);
      }
      observer.complete?.();
    });
  }
  
  /**
   * Create from a promise
   */
  static fromPromise<T>(promise: Promise<T>): Observable<T> {
    return new Observable<T>((observer) => {
      promise
        .then((value) => {
          observer.next(value);
          observer.complete?.();
        })
        .catch((err) => observer.error?.(err));
    });
  }
  
  /**
   * Create an interval observable
   */
  static interval(ms: number): Observable<number> {
    return new Observable<number>((observer) => {
      let count = 0;
      const id = setInterval(() => {
        observer.next(count++);
      }, ms);
      return () => clearInterval(id);
    });
  }
  
  /**
   * Create a timer observable
   */
  static timer(ms: number): Observable<void> {
    return new Observable<void>((observer) => {
      const id = setTimeout(() => {
        observer.next();
        observer.complete?.();
      }, ms);
      return () => clearTimeout(id);
    });
  }
  
  /**
   * Create empty observable that completes immediately
   */
  static empty<T>(): Observable<T> {
    return new Observable<T>((observer) => {
      observer.complete?.();
    });
  }
  
  /**
   * Merge multiple observables
   */
  static merge<T>(...observables: Observable<T>[]): Observable<T> {
    return new Observable<T>((observer) => {
      let completedCount = 0;
      const subscriptions: Subscription[] = [];
      
      for (const obs of observables) {
        const sub = obs.subscribe({
          next: observer.next,
          error: observer.error,
          complete: () => {
            completedCount++;
            if (completedCount === observables.length) {
              observer.complete?.();
            }
          }
        });
        subscriptions.push(sub);
      }
      
      return () => subscriptions.forEach(s => s.unsubscribe());
    });
  }
  
  /**
   * Combine latest values from multiple observables
   */
  static combineLatest<T extends unknown[]>(
    ...observables: { [K in keyof T]: Observable<T[K]> }
  ): Observable<T> {
    return new Observable<T>((observer) => {
      const values: unknown[] = new Array(observables.length);
      const hasValue: boolean[] = new Array(observables.length).fill(false);
      let completedCount = 0;
      const subscriptions: Subscription[] = [];
      
      observables.forEach((obs, index) => {
        const sub = obs.subscribe({
          next: (value) => {
            values[index] = value;
            hasValue[index] = true;
            if (hasValue.every(Boolean)) {
              observer.next([...values] as T);
            }
          },
          error: observer.error,
          complete: () => {
            completedCount++;
            if (completedCount === observables.length) {
              observer.complete?.();
            }
          }
        });
        subscriptions.push(sub);
      });
      
      return () => subscriptions.forEach(s => s.unsubscribe());
    });
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// SUBJECT (Observable + Observer)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Subject - an Observable that can be manually controlled
 */
export class Subject<T> extends Observable<T> {
  private observers: Set<Observer<T>> = new Set();
  private _closed = false;
  
  constructor() {
    super((observer) => {
      this.observers.add(observer);
      return () => this.observers.delete(observer);
    });
  }
  
  next(value: T): void {
    if (this._closed) return;
    for (const observer of this.observers) {
      observer.next(value);
    }
  }
  
  error(err: Error): void {
    if (this._closed) return;
    this._closed = true;
    for (const observer of this.observers) {
      observer.error?.(err);
    }
    this.observers.clear();
  }
  
  complete(): void {
    if (this._closed) return;
    this._closed = true;
    for (const observer of this.observers) {
      observer.complete?.();
    }
    this.observers.clear();
  }
  
  get closed(): boolean {
    return this._closed;
  }
  
  asObservable(): Observable<T> {
    return new Observable((observer) => {
      return this.subscribe(observer).unsubscribe;
    });
  }
}

/**
 * BehaviorSubject - Subject with current value
 */
export class BehaviorSubject<T> extends Subject<T> {
  constructor(private currentValue: T) {
    super();
  }
  
  get value(): T {
    return this.currentValue;
  }
  
  next(value: T): void {
    this.currentValue = value;
    super.next(value);
  }
  
  subscribe(observer: Observer<T> | ((value: T) => void)): Subscription {
    const sub = super.subscribe(observer);
    // Emit current value immediately
    if (typeof observer === 'function') {
      observer(this.currentValue);
    } else {
      observer.next(this.currentValue);
    }
    return sub;
  }
}

/**
 * ReplaySubject - Subject that replays last N values to new subscribers
 */
export class ReplaySubject<T> extends Subject<T> {
  private buffer: T[] = [];
  
  constructor(private bufferSize: number = Infinity) {
    super();
  }
  
  next(value: T): void {
    this.buffer.push(value);
    if (this.buffer.length > this.bufferSize) {
      this.buffer.shift();
    }
    super.next(value);
  }
  
  subscribe(observer: Observer<T> | ((value: T) => void)): Subscription {
    // Replay buffered values
    const normalizedObserver: Observer<T> = 
      typeof observer === 'function' 
        ? { next: observer }
        : observer;
    
    for (const value of this.buffer) {
      normalizedObserver.next(value);
    }
    
    return super.subscribe(observer);
  }
}
