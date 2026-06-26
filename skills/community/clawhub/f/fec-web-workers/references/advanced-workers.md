# 高级 Worker 模式

## Transferable Objects

```ts
const buffer = new ArrayBuffer(10 * 1024 * 1024);
worker.postMessage(buffer, [buffer]);
// transfer 后主线程中的 buffer.byteLength 变为 0。
```

适用于图片像素、音频采样、大型二进制文件。不要在 transfer 后继续读取原引用。

## Comlink

```ts
// math.worker.ts
import { expose } from "comlink";

const mathApi = {
  batchProcess(items: number[]) {
    return items.map((item) => item * 2);
  },
};

expose(mathApi);
export type MathApi = typeof mathApi;
```

```ts
import { wrap } from "comlink";
import MathWorker from "./math.worker?worker";
import type { MathApi } from "./math.worker";

const mathApi = wrap<MathApi>(new MathWorker());
const result = await mathApi.batchProcess([1, 2, 3]);
```

## Worker Pool

- 适合大量独立任务，不适合强顺序依赖任务。
- 默认 pool size 不要超过 `navigator.hardwareConcurrency`。
- 队列中任务需要超时、取消或页面卸载清理策略。

## SharedWorker

- 适合跨 Tab 共享连接或广播状态。
- 兼容性弱于 Dedicated Worker，必须先确认目标浏览器。
- 每个连接使用 `MessagePort`，需要 `port.start()`。

## 安全与兼容

- CSP 需允许 `worker-src`。
- `SharedArrayBuffer` 需要 COOP/COEP 头。
- Worker 中可用 IndexedDB，但不可用同步 localStorage。
