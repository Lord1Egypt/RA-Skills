---
name: archiver
description: Use the Archiver library for streaming archive packaging in Node.js. Supports creating ZIP/TAR archives, appending content from streams, strings, buffers, file paths, directories, and glob patterns, as well as registering custom formats.
---

# Archiver — Streaming Archive Packaging

A Node.js streaming archive library that supports ZIP and TAR, capable of appending content from multiple data sources.

## Use Cases

Use when users need to compress and package, create zip/tar archives, package directories, or programmatically generate compressed files.

## Trigger Words

Compress, package, archive, zip, tar, archive, archiver.

## Installation

```bash
npm install archiver
```

## Quick Start: ZIP Packaging

```js
const fs = require('fs');
const archiver = require('archiver');

const output = fs.createWriteStream('output.zip');
const archive = archiver('zip', { zlib: { level: 9 } });

output.on('close', () => {
  console.log(`${archive.pointer()} bytes written`);
});

archive.on('error', (err) => { throw err; });

archive.pipe(output);

// Append — multiple data sources
archive.append(fs.createReadStream('file.txt'), { name: 'file.txt' });  // Stream
archive.append('string content', { name: 'readme.txt' });               // String
archive.append(Buffer.from('data'), { name: 'data.bin' });              // Buffer
archive.file('local-file.txt', { name: 'renamed.txt' });                // Local file
archive.directory('src/', 'src');                                        // Directory → subdirectory in archive
archive.directory('dist/', false);                                       // Directory contents → archive root
archive.glob('*.js', { cwd: __dirname });                                // Glob match

// ⚠️ `archive.directory()` does NOT support ignore/filter patterns.
//    To exclude node_modules, use glob() instead (see Excluding node_modules below).

archive.finalize();
```

## Data Source Overview

| Method | Data Source | name Parameter |
|--------|-------------|----------------|
| `archive.append(stream, { name })` | ReadStream | Required |
| `archive.append(string, { name })` | String | Required |
| `archive.append(buffer, { name })` | Buffer | Required |
| `archive.file(path, { name })` | File path | Optional, can rename |
| `archive.directory(path, dest)` | Directory | `false` = contents to root; string = subdirectory name |
| `archive.glob(pattern, { cwd })` | Glob match | Auto-uses matched filenames |

## TAR Packaging

```js
const archive = archiver('tar', {
  gzip: true,
  gzipOptions: { level: 6 }
});
```

TAR-specific options:

| Option | Description | Default |
|--------|-------------|---------|
| `gzip` | Enable gzip compression | `false` |
| `gzipOptions.level` | Compression level 0-9 | 6 |

## Events

```js
archive.on('warning', (err) => {
  if (err.code === 'ENOENT') console.warn('File not found:', err);
  else throw err;
});

archive.on('error', (err) => { throw err; });

// Events on the piped destination stream (from Node.js Stream API)
output.on('close', () => { /* File descriptor closed */ });
output.on('end', () => { /* Data drained */ });
output.on('finish', () => { /* All data written */ });
```

- **`warning`** — Non-fatal errors (e.g., file not found, stat failure, etc.); `ENOENT` can be ignored, others should be thrown
- **`error`** — Fatal errors; must be handled
- **`close`** (output) — Emitted after the file descriptor is closed; `archive.pointer()` can be used to get the total byte count at this point
- **`end`** (output) — Data drained; emitted regardless of the data source
- **`progress`** — Progress tracking, see below

## Progress Tracking

```js
archive.on('progress', (progress) => {
  console.log(`${progress.entries.processed} / ${progress.entries.total} entries`);
  console.log(`${progress.fs.processedBytes} / ${progress.fs.totalBytes} bytes`);
});
```

`progress` object structure:

```
{
  entries: { total: number, processed: number },
  fs: { totalBytes: number, processedBytes: number }
}
```

## Common Patterns

### Pattern 1: Responsive Archiving — HTTP Streaming Output

```js
app.get('/download', (req, res) => {
  res.attachment('archive.zip');
  const archive = archiver('zip', { zlib: { level: 1 } }); // Low compression = faster

  archive.on('error', (err) => { res.status(500).end(); });

  archive.pipe(res);
  archive.directory('user-files/', false);
  archive.finalize();
});
```

### Pattern 2: Conditional Append — On-Demand Packaging

```js
const archive = archiver('zip');

// Dynamically append based on conditions
if (includeSource) {
  archive.directory('src/', 'source');
}
if (includeDocs) {
  archive.glob('docs/**/*.md', { cwd: __dirname });
}

archive.finalize();
```

### Pattern 3: In-Memory Archiving — No File Output

```js
const { Writable } = require('stream');

const chunks = [];
const memoryStream = new Writable({
  write(chunk, enc, cb) { chunks.push(chunk); cb(); }
});

const archive = archiver('zip');
archive.pipe(memoryStream);

archive.append('hello', { name: 'hello.txt' });
archive.finalize();

memoryStream.on('finish', () => {
  const buffer = Buffer.concat(chunks);
  console.log(`Archive in memory: ${buffer.length} bytes`);
  // Can be used for uploading, sending, etc.
});
```

### Pattern 4: Excluding node_modules When Packaging a Project

> `archive.directory()` has **no built-in ignore** — it adds everything recursively.
> To skip `node_modules`, use one of these approaches:

**Option A — glob() with ignore (recommended):**

```js
const archive = archiver('zip', { zlib: { level: 9 } });
archive.pipe(fs.createWriteStream('project.zip'));

// glob picks up files but lets you set ignore patterns
archive.glob('**/*', {
  cwd: '/path/to/project',
  ignore: ['node_modules/**', '.git/**', 'dist/**'],
  dot: true,             // include dotfiles
});

archive.finalize();
```

**Option B — Manual directory walk (custom filtering):**

```js
const klaw = require('klaw');       // or fs.walk / @nodelib/fs.walk

archive.glob('**/*', {
  cwd: rootDir,
  ignore: ['node_modules/**'],
  dot: true,
});
archive.finalize();
```

> **Why not `archive.directory()`?** `directory()` is a one-shot bulk append with no filter callback. For any kind of exclusion, always switch to `glob()` — it's the same code walking underneath, just with pattern support.

**Option C — Pre-build a file list:**

```js
const klaw = require('klaw');  // npm install klaw

async function zipWithFilter(srcDir, outPath) {
  const archive = archiver('zip', { zlib: { level: 9 } });
  archive.pipe(fs.createWriteStream(outPath));

  for await (const file of klaw(srcDir)) {
    if (file.stats.isFile() && !file.path.includes('node_modules')) {
      archive.file(file.path, { name: path.relative(srcDir, file.path) });
    }
  }

  await archive.finalize();
}
```

### Pattern 5: Batch Packaging — Multiple Archives in Series

```js
async function createBatchedArchives(fileGroups, outputDir) {
  for (const [i, files] of fileGroups.entries()) {
    await new Promise((resolve, reject) => {
      const output = fs.createWriteStream(`${outputDir}/batch-${i}.zip`);
      const archive = archiver('zip');

      archive.on('error', reject);
      output.on('close', resolve);

      archive.pipe(output);
      files.forEach(f => archive.file(f, { name: path.basename(f) }));
      archive.finalize();
    });
    console.log(`Batch ${i} complete`);
  }
}
```

## Custom Format Registration

```js
archiver.registerFormat('myformat', module);
const archive = archiver('myformat');
```

Check if a format is registered:
```js
if (archiver.isRegisteredFormat('zip')) {
  // ZIP is available
}
```

## Symlink Handling

```js
archive.symlink('target', { name: 'link-name' });
```

## Common Options Reference — `archiver(format, options)`

```js
const archive = archiver('zip', {
  zlib: { level: 9 },          // Compression level 0-9
  comment: 'my comment',       // ZIP comment
  forceLocalTime: true,        // Use local time instead of UTC
  forceZip64: false,           // Whether to force Zip64
  namePrependSlash: false,     // Prepend / to filenames
  statConcurrency: 4           // Stat concurrency
});
```

For the full API reference, see [references/api-reference.md](references/api-reference.md).