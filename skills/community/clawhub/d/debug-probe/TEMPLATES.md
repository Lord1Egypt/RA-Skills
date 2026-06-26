# Diagnostic Buffer Templates

Pick the template matching your project language. Copy to a temporary file (remove in Phase 6).

## TypeScript / JavaScript (Browser)

```typescript
// diag-buffer.ts — temporary file, remove in Phase 6
const buffer: string[] = [];
const MAX = 500;

export function diagLog(h: string, ...args: string[]): void {
  const line = `[DIAG][${h}] ${args.join(' ')}`;
  buffer.push(line);
  if (buffer.length > MAX) buffer.shift();
  console.info(line);
}

(globalThis as any).__diagDump = () => {
  console.info(`=== DIAG DUMP (${buffer.length} lines) ===\n${buffer.join('\n')}\n=== END ===`);
};
(globalThis as any).__diagClear = () => { buffer.length = 0; };
```

User exports logs by typing `__diagDump()` in the browser console.

## TypeScript / JavaScript (Node.js)

```typescript
// diag-buffer.ts — temporary file, remove in Phase 6
const buffer: string[] = [];
const MAX = 500;

export function diagLog(h: string, ...args: string[]): void {
  const line = `[DIAG][${h}] ${args.join(' ')}`;
  buffer.push(line);
  if (buffer.length > MAX) buffer.shift();
  console.info(line);
}

export function diagDump(): void {
  console.info(`=== DIAG DUMP (${buffer.length} lines) ===\n${buffer.join('\n')}\n=== END ===`);
}

export function diagClear(): void {
  buffer.length = 0;
}
```

For CLI tools, register `diagDump`/`diagClear` via REPL or expose a signal handler.

## Python

```python
# diag_buffer.py — temporary file, remove in Phase 6
_buffer: list[str] = []
MAX = 500

def diag_log(h: str, *args: str) -> None:
    line = f"[DIAG][{h}] {' '.join(args)}"
    _buffer.append(line)
    if len(_buffer) > MAX:
        _buffer.pop(0)
    print(line, flush=True)

def diag_dump() -> None:
    print(f"=== DIAG DUMP ({len(_buffer)} lines) ===\n" + "\n".join(_buffer) + "\n=== END ===")

def diag_clear() -> None:
    _buffer.clear()
```

Import and call `diag_dump()` / `diag_clear()` as needed, or wire to a signal/keyboard shortcut.

## Go

```go
// diag_buffer.go — temporary file, remove in Phase 6
package diag

import (
	"fmt"
	"strings"
	"sync"
)

var (
	buffer []string
	mu     sync.Mutex
)

const maxLines = 500

func Log(h string, args ...string) {
	mu.Lock()
	defer mu.Unlock()
	line := fmt.Sprintf("[DIAG][%s] %s", h, strings.Join(args, " "))
	buffer = append(buffer, line)
	if len(buffer) > maxLines {
		buffer = buffer[1:]
	}
	fmt.Println(line)
}

func Dump() {
	mu.Lock()
	defer mu.Unlock()
	fmt.Printf("=== DIAG DUMP (%d lines) ===\n%s\n=== END ===\n", len(buffer), strings.Join(buffer, "\n"))
}

func Clear() {
	mu.Lock()
	defer mu.Unlock()
	buffer = nil
}
```

Expose `Dump()` / `Clear()` via HTTP endpoint, signal handler, or debug command.

## Usage Pattern (all languages)

```typescript
// In the code paths being investigated:
import { diagLog } from '../utils/diag-buffer'; // DIAG: remove after debug

diagLog('H1', 'userId=' + uid, 'tokenExp=' + exp); // DIAG: remove after debug
diagLog('H2', 'cacheHit=' + hit, 'cacheAge=' + age); // DIAG: remove after debug
```

Key points:
- All instrumentation tagged with `DIAG: remove after debug` comment for easy cleanup
- Each log call starts with hypothesis ID (H1, H2, ...)
- Values formatted as `key=value` pairs — no full object dumps
