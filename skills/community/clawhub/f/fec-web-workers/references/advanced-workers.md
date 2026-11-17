#Advanced Worker mode

## Transferable Objects

```ts
const buffer = new ArrayBuffer(10 * 1024 * 1024);
worker.postMessage(buffer, [buffer]);
// After transfer, buffer.byteLength in the main thread becomes 0.
```

Suitable for image pixels, audio samples, and large binary files. Do not continue to read the original reference after transfer.

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

- Suitable for a large number of independent tasks, not suitable for tasks with strong sequence dependencies.
- Default pool size should not exceed `navigator.hardwareConcurrency`.
- Tasks in the queue require timeout, cancellation or page unloading cleaning strategies.

## SharedWorker

- Suitable for sharing connections or broadcasting status across tabs.
- Compatibility is weaker than Dedicated Worker, the target browser must be confirmed first.
- Uses `MessagePort` per connection, requires `port.start()`.

## Security and Compatibility

- CSP needs to allow `worker-src`.
- `SharedArrayBuffer` requires COOP/COEP headers.
- IndexedDB is available in Worker, but synchronized localStorage is not.
