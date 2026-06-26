---
name: boxed-fs
description: WebAssembly sandboxed file system operations for secure file read/write within explicitly declared directories. Use when needing to read, write, append, copy, remove, or list files in a controlled sandbox environment.
---

# boxed-fs

WebAssembly sandboxed file system operations. All file operations run inside a WASM sandbox with access control.

## Quick Start

```js
// Download wasm first (one-time)
wasm-sandbox-download({
  url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fs/files/boxed-fs-component.wasm",
  dest: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm"
})

// List files
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["list-dir", "--path", "."]
})

// Read file
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["read-file", "--path", "example.txt"]
})
```

## Supported Operations

- **read-file** - Read file contents
- **write-file** - Write file contents atomically
- **append-file** - Append data to a file
- **open-file** - Open a file for reading
- **open-writable-file** - Open a file for writing
- **copy-file** - Copy a file within root
- **remove-path** - Remove a file or directory
- **mkdir-path** - Create a directory path
- **list-dir** - List files and directories under a path

## Trigger When

boxed-fs triggers when the user asks to read, write, append, copy, remove, list, or otherwise manipulate files in a sandboxed environment, or when explicitly requested to use boxed-fs.

boxed-fs 在用户要求在沙箱环境中读取、写入、追加、复制、删除、列出或以其他方式操作文件时触发，或在明确请求使用 boxed-fs 时触发。

## Usage Reference

See [USAGE.md](references/USAGE.md) for detailed command usage and examples.
