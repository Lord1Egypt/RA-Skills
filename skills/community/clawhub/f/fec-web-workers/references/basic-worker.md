# 基础 Worker 与生命周期

## Worker 文件

```ts
// workers/heavy-compute.worker.ts
self.onmessage = (event: MessageEvent<{ numbers: number[] }>) => {
  const result = [...event.data.numbers].sort((a, b) => a - b);
  self.postMessage(result);
};
```

## Vite 导入

```ts
import HeavyComputeWorker from "./workers/heavy-compute.worker?worker";

const worker = new HeavyComputeWorker();
worker.postMessage({ numbers: [3, 1, 4, 1, 5] });
worker.onmessage = (event: MessageEvent<number[]>) => {
  console.log(event.data);
};
worker.onerror = (error) => {
  console.error(error.message);
};
```

## React 生命周期封装

```tsx
import { useCallback, useEffect, useRef, useState } from "react";

export function useWorker<TRequest, TResult>(factory: () => Worker) {
  const workerRef = useRef<Worker | null>(null);
  const [result, setResult] = useState<TResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    const worker = factory();
    workerRef.current = worker;
    worker.onmessage = (event: MessageEvent<TResult>) => {
      setResult(event.data);
      setIsRunning(false);
    };
    worker.onerror = (event) => {
      setError(event.message);
      setIsRunning(false);
    };
    return () => worker.terminate();
  }, [factory]);

  const run = useCallback((data: TRequest) => {
    setIsRunning(true);
    setError(null);
    workerRef.current?.postMessage(data);
  }, []);

  return { run, result, error, isRunning };
}
```

## 验证

- Performance 面板中长任务减少。
- 用户输入延迟下降。
- 组件卸载后没有继续收到 worker message。
