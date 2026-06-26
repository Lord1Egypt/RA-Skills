# boxed-fs Usage Reference

## Prerequisites

1. **openclaw-wasm-sandbox plugin** must be installed and enabled
2. **wasm file** must be downloaded before first use

## Setup

Download the wasm file using `wasm-sandbox-download`:

```js
wasm-sandbox-download({
  url: "https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/boxed-fs/files/boxed-fs-component.wasm",
  dest: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm"
})
```

## Basic Usage

### Running wasm-sandbox-run

Always specify `workDir` to define the sandbox root. Use `mapDirs` to grant access to additional directories.

**Minimal (workDir only):**
```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["list-dir", "--path=."]
})
```

**With additional mapped directories:**
```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  mapDirs: ["/tmp::/tmp", "/data::/data"],
  args: ["list-dir", "--path=/tmp"]
})
```

## Commands

Get help with:
```js
// General help
args: ["--help"]

// Command-specific help
args: ["list-dir", "--help"]
args: ["read-file", "--help"]
args: ["write-file", "--help"]
```

### list-dir

List files and directories under a path.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["list-dir", "--path=."]
})
```

### read-file

Read file contents.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["read-file", "--path=AGENTS.md"]
})
```

### write-file

Write file contents atomically.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["write-file", "--path=output.txt", "--data=Hello, World!"]
})
```

### append-file

Append data to a file.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["append-file", "--path=log.txt", "--data=new entry"]
})
```

### open-file

Open a file for reading and emit its handle info.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["open-file", "--path=data.json"]
})
```

### open-writable-file

Open a file for writing and emit its handle info.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["open-writable-file", "--path=output.json"]
})
```

### copy-file

Copy a file within the sandbox root.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["copy-file", "--src=source.txt", "--dst=dest.txt"]
})
```

### remove-path

Remove a file or directory.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["remove-path", "--path=temp.txt"]
})
```

### mkdir-path

Create a directory path.

```js
wasm-sandbox-run({
  wasmFile: "~/.openclaw/skills/boxed-fs/files/boxed-fs-component.wasm",
  workDir: "~/.openclaw/workspace",
  args: ["mkdir-path", "--path=subdir/nested"]
})
```

## Access Control

The sandbox only allows operations on:
1. The directory specified as `workDir`
2. Additional directories explicitly mapped via `mapDirs`

Operations on non-declared paths will be denied by the sandbox.
