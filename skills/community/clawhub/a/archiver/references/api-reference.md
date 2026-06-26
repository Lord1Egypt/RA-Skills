# Archiver API Reference

## Constructor

```js
const archive = archiver(format, options)
```

- `format` — `'zip'` | `'tar'`
- `options` — Format-specific options (see below)

---

## Methods

### archive.append(data, options)

Append content to the archive.

- `data` — `ReadableStream` | `Buffer` | `string`
- `options.name` — Filename within the archive (required)
- `options.prefix` — Path prefix
- `options.date` — File date (Date | string), defaults to current time
- `options.mode` — File permissions (e.g., 0o644)
- `options.store` — `true` to store without compression (ZIP only), `false` to compress

**Additional options (when data is a ReadStream):**
- `options.stats` — fs.Stats object (avoids an extra stat call)
- `options.sourceMetadata` — Custom metadata

### archive.file(filepath, options)

Append a file from the file system.

- `filepath` — File path
- `options.name` — Filename within the archive; defaults to `path.basename(filepath)` if not provided
- `options.prefix`, `options.date`, `options.mode`, `options.store` — Same as append

### archive.directory(dirpath, destpath, options)

Append an entire directory.

- `dirpath` — Local directory path
- `destpath` — Path within the archive. `false` places contents at the archive root; a string becomes the subdirectory name
- `options` — Same as file()

### archive.glob(pattern, options)

Match and append files via a glob pattern.

- `pattern` — Glob pattern
- `options.cwd` — Base directory for searching (required)
- `options.root` — Root path prefix (used for relative paths)
- `options.dot` — Include files starting with `.`
- `options.nodir` — Exclude directories
- `options.ignore` — Glob pattern(s) to exclude
- `options.expand` — `true` to enable brace expansion (e.g., `{a,b}`)
- `options.nonull` — Do not throw when no matches are found

```js
// Ignore node_modules and .git
archive.glob('**/*', {
  cwd: 'project/',
  ignore: ['node_modules/**', '.git/**']
});
```

### archive.symlink(target, options)

Add a symbolic link (only supported by certain formats).

- `target` — Link target
- `options.name` — Filename within the archive
- `options.mode` — Link permissions

### archive.finalize()

Finalize the archive build. No further content can be appended after this call. Events (close/end/finish) must be registered before this call.

### archive.pointer()

Returns the current number of bytes written (ZIP: before compression, TAR: file content only).

```js
archive.on('progress', () => {
  console.log(archive.pointer());
});
```

### archive.pipe(destination)

Pipe archive data to a destination writable stream.

---

## Events

### archive.on('progress', callback)

```js
archive.on('progress', (progress) => {
  // progress = {
  //   entries: { total: number, processed: number },
  //   fs: { totalBytes: number, processedBytes: number }
  // }
});
```

### archive.on('warning', callback)

- `err.code === 'ENOENT'` — File/directory does not exist; can be ignored
- Other — Should be treated as an error

### archive.on('error', callback)

Fatal errors; must be handled.

### archive.on('entry', callback)

Emitted when each entry is added to the archive (useful for logging/tracking).

```js
archive.on('entry', (entry) => {
  console.log(`Added: ${entry.name} (${entry.size} bytes)`);
});
```

---

## ZIP Options

```js
archiver('zip', {
  zlib: { level: 9 },       // Compression level 0-9 (0=store, 1=fastest, 9=smallest)
  comment: 'comment',       // Archive comment
  forceLocalTime: true,     // Use local time
  forceZip64: false,        // Force Zip64 format
  namePrependSlash: false,  // Prepend filenames with /
  store: false,             // Disable compression globally
  statConcurrency: 4        // Number of parallel stat calls
})
```

## TAR Options

```js
archiver('tar', {
  gzip: true,
  gzipOptions: { level: 6 },  // gzip compression level
  statConcurrency: 4
})
```

---

## Static Methods

### archiver.registerFormat(format, module)

Register a custom archive format.

```js
archiver.registerFormat('zip-encrypted', require('archiver-zip-encrypted'));
```

### archiver.isRegisteredFormat(format)

```js
archiver.isRegisteredFormat('zip') // → true
archiver.isRegisteredFormat('rar') // → false
```

---

## Common Errors

| Error Code | Meaning | Handling |
|------------|---------|----------|
| `ENOENT` | File/directory does not exist | Can be ignored (warning event) |
| `EACCES` | Insufficient permissions | Should abort |
| `ENOTDIR` | Path is not a directory | Check the dirpath |
| `QUEUEDONE` | Content appended after `finalize()` | Ensure finalize is the last step |