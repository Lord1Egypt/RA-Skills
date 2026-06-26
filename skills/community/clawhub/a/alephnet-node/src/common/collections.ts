/**
 * Collection Utilities
 * 
 * Specialized data structures and collection utilities for AlephNet.
 */

// ═══════════════════════════════════════════════════════════════════════════
// LRU CACHE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * LRU (Least Recently Used) Cache
 */
export class LRUCache<K, V> {
  private cache = new Map<K, V>();
  private readonly maxSize: number;
  
  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }
  
  get(key: K): V | undefined {
    if (!this.cache.has(key)) return undefined;
    
    // Move to end (most recently used)
    const value = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, value);
    
    return value;
  }
  
  set(key: K, value: V): void {
    // If key exists, delete it first to update position
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }
    
    // Evict oldest if at capacity
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      if (firstKey !== undefined) {
        this.cache.delete(firstKey);
      }
    }
    
    this.cache.set(key, value);
  }
  
  has(key: K): boolean {
    return this.cache.has(key);
  }
  
  delete(key: K): boolean {
    return this.cache.delete(key);
  }
  
  clear(): void {
    this.cache.clear();
  }
  
  size(): number {
    return this.cache.size;
  }
  
  keys(): IterableIterator<K> {
    return this.cache.keys();
  }
  
  values(): IterableIterator<V> {
    return this.cache.values();
  }
  
  entries(): IterableIterator<[K, V]> {
    return this.cache.entries();
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// TTL CACHE
// ═══════════════════════════════════════════════════════════════════════════

interface CacheEntry<V> {
  value: V;
  expiresAt: number;
}

/**
 * Cache with Time-To-Live expiration
 */
export class TTLCache<K, V> {
  private cache = new Map<K, CacheEntry<V>>();
  private readonly defaultTTLMs: number;
  private cleanupInterval: NodeJS.Timeout | null = null;
  
  constructor(defaultTTLMs: number, cleanupIntervalMs?: number) {
    this.defaultTTLMs = defaultTTLMs;
    
    if (cleanupIntervalMs) {
      this.startCleanup(cleanupIntervalMs);
    }
  }
  
  get(key: K): V | undefined {
    const entry = this.cache.get(key);
    if (!entry) return undefined;
    
    if (Date.now() > entry.expiresAt) {
      this.cache.delete(key);
      return undefined;
    }
    
    return entry.value;
  }
  
  set(key: K, value: V, ttlMs?: number): void {
    const expiresAt = Date.now() + (ttlMs ?? this.defaultTTLMs);
    this.cache.set(key, { value, expiresAt });
  }
  
  has(key: K): boolean {
    const value = this.get(key);
    return value !== undefined;
  }
  
  delete(key: K): boolean {
    return this.cache.delete(key);
  }
  
  clear(): void {
    this.cache.clear();
  }
  
  size(): number {
    return this.cache.size;
  }
  
  private startCleanup(intervalMs: number): void {
    this.cleanupInterval = setInterval(() => {
      const now = Date.now();
      for (const [key, entry] of this.cache) {
        if (now > entry.expiresAt) {
          this.cache.delete(key);
        }
      }
    }, intervalMs);
  }
  
  dispose(): void {
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
    this.cache.clear();
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// PRIORITY QUEUE
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Min-heap based priority queue
 */
export class PriorityQueue<T> {
  private heap: Array<{ priority: number; value: T }> = [];
  
  enqueue(value: T, priority: number): void {
    this.heap.push({ priority, value });
    this.bubbleUp(this.heap.length - 1);
  }
  
  dequeue(): T | undefined {
    if (this.heap.length === 0) return undefined;
    if (this.heap.length === 1) return this.heap.pop()!.value;
    
    const result = this.heap[0].value;
    this.heap[0] = this.heap.pop()!;
    this.bubbleDown(0);
    
    return result;
  }
  
  peek(): T | undefined {
    return this.heap[0]?.value;
  }
  
  size(): number {
    return this.heap.length;
  }
  
  isEmpty(): boolean {
    return this.heap.length === 0;
  }
  
  clear(): void {
    this.heap = [];
  }
  
  private bubbleUp(index: number): void {
    while (index > 0) {
      const parentIndex = Math.floor((index - 1) / 2);
      if (this.heap[parentIndex].priority <= this.heap[index].priority) break;
      
      [this.heap[parentIndex], this.heap[index]] = [this.heap[index], this.heap[parentIndex]];
      index = parentIndex;
    }
  }
  
  private bubbleDown(index: number): void {
    while (true) {
      const leftChild = 2 * index + 1;
      const rightChild = 2 * index + 2;
      let smallest = index;
      
      if (leftChild < this.heap.length && 
          this.heap[leftChild].priority < this.heap[smallest].priority) {
        smallest = leftChild;
      }
      
      if (rightChild < this.heap.length && 
          this.heap[rightChild].priority < this.heap[smallest].priority) {
        smallest = rightChild;
      }
      
      if (smallest === index) break;
      
      [this.heap[smallest], this.heap[index]] = [this.heap[index], this.heap[smallest]];
      index = smallest;
    }
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// RING BUFFER
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Fixed-size circular buffer
 */
export class RingBuffer<T> {
  private buffer: (T | undefined)[];
  private head = 0;
  private tail = 0;
  private count = 0;
  private readonly capacity: number;
  
  constructor(capacity: number) {
    this.capacity = capacity;
    this.buffer = new Array(capacity);
  }
  
  push(item: T): T | undefined {
    let evicted: T | undefined;
    
    if (this.count === this.capacity) {
      evicted = this.buffer[this.head];
      this.head = (this.head + 1) % this.capacity;
    } else {
      this.count++;
    }
    
    this.buffer[this.tail] = item;
    this.tail = (this.tail + 1) % this.capacity;
    
    return evicted;
  }
  
  shift(): T | undefined {
    if (this.count === 0) return undefined;
    
    const item = this.buffer[this.head];
    this.buffer[this.head] = undefined;
    this.head = (this.head + 1) % this.capacity;
    this.count--;
    
    return item;
  }
  
  peek(): T | undefined {
    if (this.count === 0) return undefined;
    return this.buffer[this.head];
  }
  
  peekLast(): T | undefined {
    if (this.count === 0) return undefined;
    const index = (this.tail - 1 + this.capacity) % this.capacity;
    return this.buffer[index];
  }
  
  size(): number {
    return this.count;
  }
  
  isEmpty(): boolean {
    return this.count === 0;
  }
  
  isFull(): boolean {
    return this.count === this.capacity;
  }
  
  clear(): void {
    this.buffer = new Array(this.capacity);
    this.head = 0;
    this.tail = 0;
    this.count = 0;
  }
  
  toArray(): T[] {
    const result: T[] = [];
    for (let i = 0; i < this.count; i++) {
      const index = (this.head + i) % this.capacity;
      result.push(this.buffer[index]!);
    }
    return result;
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// MULTI MAP
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Map that allows multiple values per key
 */
export class MultiMap<K, V> {
  private map = new Map<K, V[]>();
  
  add(key: K, value: V): void {
    const existing = this.map.get(key);
    if (existing) {
      existing.push(value);
    } else {
      this.map.set(key, [value]);
    }
  }
  
  get(key: K): V[] {
    return this.map.get(key) || [];
  }
  
  getFirst(key: K): V | undefined {
    const values = this.map.get(key);
    return values?.[0];
  }
  
  has(key: K): boolean {
    return this.map.has(key);
  }
  
  hasValue(key: K, value: V): boolean {
    const values = this.map.get(key);
    return values?.includes(value) ?? false;
  }
  
  delete(key: K): boolean {
    return this.map.delete(key);
  }
  
  deleteValue(key: K, value: V): boolean {
    const values = this.map.get(key);
    if (!values) return false;
    
    const index = values.indexOf(value);
    if (index === -1) return false;
    
    values.splice(index, 1);
    if (values.length === 0) {
      this.map.delete(key);
    }
    
    return true;
  }
  
  clear(): void {
    this.map.clear();
  }
  
  size(): number {
    return this.map.size;
  }
  
  valueCount(): number {
    let count = 0;
    for (const values of this.map.values()) {
      count += values.length;
    }
    return count;
  }
  
  keys(): IterableIterator<K> {
    return this.map.keys();
  }
  
  entries(): IterableIterator<[K, V[]]> {
    return this.map.entries();
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// SORTED MAP
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Map that maintains sorted order by key
 */
export class SortedMap<K, V> {
  private entries: Array<{ key: K; value: V }> = [];
  private comparator: (a: K, b: K) => number;
  
  constructor(comparator?: (a: K, b: K) => number) {
    this.comparator = comparator || ((a, b) => {
      if (a < b) return -1;
      if (a > b) return 1;
      return 0;
    });
  }
  
  set(key: K, value: V): void {
    const index = this.findIndex(key);
    
    if (index >= 0 && this.comparator(this.entries[index].key, key) === 0) {
      this.entries[index].value = value;
    } else {
      const insertIndex = index >= 0 ? index : ~index;
      this.entries.splice(insertIndex, 0, { key, value });
    }
  }
  
  get(key: K): V | undefined {
    const index = this.findIndex(key);
    if (index >= 0 && this.comparator(this.entries[index].key, key) === 0) {
      return this.entries[index].value;
    }
    return undefined;
  }
  
  has(key: K): boolean {
    const index = this.findIndex(key);
    return index >= 0 && this.comparator(this.entries[index].key, key) === 0;
  }
  
  delete(key: K): boolean {
    const index = this.findIndex(key);
    if (index >= 0 && this.comparator(this.entries[index].key, key) === 0) {
      this.entries.splice(index, 1);
      return true;
    }
    return false;
  }
  
  clear(): void {
    this.entries = [];
  }
  
  size(): number {
    return this.entries.length;
  }
  
  first(): { key: K; value: V } | undefined {
    return this.entries[0];
  }
  
  last(): { key: K; value: V } | undefined {
    return this.entries[this.entries.length - 1];
  }
  
  keys(): K[] {
    return this.entries.map(e => e.key);
  }
  
  values(): V[] {
    return this.entries.map(e => e.value);
  }
  
  range(from: K, to: K): Array<{ key: K; value: V }> {
    const result: Array<{ key: K; value: V }> = [];
    for (const entry of this.entries) {
      if (this.comparator(entry.key, from) >= 0 && this.comparator(entry.key, to) <= 0) {
        result.push(entry);
      }
    }
    return result;
  }
  
  private findIndex(key: K): number {
    let low = 0;
    let high = this.entries.length - 1;
    
    while (low <= high) {
      const mid = Math.floor((low + high) / 2);
      const cmp = this.comparator(this.entries[mid].key, key);
      
      if (cmp < 0) {
        low = mid + 1;
      } else if (cmp > 0) {
        high = mid - 1;
      } else {
        return mid;
      }
    }
    
    return ~low; // Bitwise NOT gives insertion point
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// ARRAY UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Chunk an array into smaller arrays
 */
export function chunk<T>(array: T[], size: number): T[][] {
  const result: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    result.push(array.slice(i, i + size));
  }
  return result;
}

/**
 * Flatten nested arrays
 */
export function flatten<T>(arrays: T[][]): T[] {
  return arrays.reduce((acc, arr) => acc.concat(arr), []);
}

/**
 * Remove duplicates from array
 */
export function unique<T>(array: T[]): T[] {
  return [...new Set(array)];
}

/**
 * Group array items by key
 */
export function groupBy<T, K extends string | number>(
  array: T[],
  keyFn: (item: T) => K
): Record<K, T[]> {
  return array.reduce((groups, item) => {
    const key = keyFn(item);
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(item);
    return groups;
  }, {} as Record<K, T[]>);
}

/**
 * Find item by predicate or return undefined
 */
export function findOrUndefined<T>(
  array: T[],
  predicate: (item: T, index: number) => boolean
): T | undefined {
  for (let i = 0; i < array.length; i++) {
    if (predicate(array[i], i)) return array[i];
  }
  return undefined;
}

/**
 * Shuffle array in place (Fisher-Yates)
 */
export function shuffle<T>(array: T[]): T[] {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

/**
 * Create an array of numbers from start to end
 */
export function range(start: number, end: number, step: number = 1): number[] {
  const result: number[] = [];
  for (let i = start; i < end; i += step) {
    result.push(i);
  }
  return result;
}
