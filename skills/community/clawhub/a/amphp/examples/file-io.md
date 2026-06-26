# AMPHP v3 — Filesystem Patterns (amphp/file)

> All functions are in the `Amp\File` namespace. They are async-safe — they do not block the event loop.

---

## One-shot read and write

```php
<?php declare(strict_types=1);

use Amp\File;

// Write entire content at once
File\write('/tmp/hello.txt', 'Hello, World!');

// Read entire file at once
$content = File\read('/tmp/hello.txt'); // 'Hello, World!'
```

---

## exists, getSize, deleteFile

```php
<?php declare(strict_types=1);

use Amp\File;

$path = '/tmp/data.txt';

File\exists($path);           // false — not created yet
File\write($path, 'content');
File\exists($path);           // true

$size = File\getSize($path);  // 7 (bytes)

File\deleteFile($path);
File\exists($path);           // false again
```

---

## createDirectoryRecursively and listFiles

```php
<?php declare(strict_types=1);

use Amp\File;

// mkdir -p equivalent
File\createDirectoryRecursively('/tmp/app/logs/2024', 0755);

File\write('/tmp/app/logs/2024/a.log', 'log1');
File\write('/tmp/app/logs/2024/b.log', 'log2');

$entries = File\listFiles('/tmp/app/logs/2024');
// IMPORTANT: listFiles() returns filenames only — NOT full paths!
// $entries === ['a.log', 'b.log']  (order not guaranteed)

sort($entries); // sort for determinism

// Build full paths manually:
$paths = array_map(fn(string $name) => '/tmp/app/logs/2024/' . $name, $entries);
```

> **Gotcha**: `File\listFiles()` returns **filenames only** (e.g. `['a.log', 'b.log']`), not full paths. Prepend the directory path yourself when you need full paths.

---

## deleteDirectory

```php
<?php declare(strict_types=1);

use Amp\File;

// Remove a directory (must be empty, or use recursive approach)
File\deleteDirectory('/tmp/app/logs/2024');

// For a non-empty directory, delete contents first:
$entries = File\listFiles('/tmp/app/logs');
foreach ($entries as $name) {
    File\deleteFile('/tmp/app/logs/' . $name);
}
File\deleteDirectory('/tmp/app/logs');
```

---

## openFile() — streaming write

```php
<?php declare(strict_types=1);

use Amp\File;

// Open for writing ('w' truncates, 'a' appends, 'r' read-only)
$file = File\openFile('/tmp/output.txt', 'w');

foreach (['chunk1', 'chunk2', 'chunk3'] as $chunk) {
    $file->write($chunk);
}

$file->end(); // flush and close the write end
```

---

## openFile() — streaming read

```php
<?php declare(strict_types=1);

use Amp\File;

$file = File\openFile('/tmp/output.txt', 'r');

$content = '';
while (null !== $chunk = $file->read()) {
    $content .= $chunk; // null signals end of file
}
// $content === 'chunk1chunk2chunk3'
```

---

## Append to existing file

```php
<?php declare(strict_types=1);

use Amp\File;

File\write('/tmp/log.txt', 'line1');

$file = File\openFile('/tmp/log.txt', 'a'); // append mode
$file->write("\nline2");
$file->end();

$content = File\read('/tmp/log.txt');
// $content === "line1\nline2"
```

---

## Full cycle — write, verify, read, cleanup

```php
<?php declare(strict_types=1);

use Amp\File;

$dir  = '/tmp/demo';
$path = $dir . '/data.bin';

File\createDirectoryRecursively($dir, 0755);
File\write($path, pack('N', 42)); // 4-byte big-endian integer

$size    = File\getSize($path);   // 4
$content = File\read($path);
$value   = unpack('N', $content)[1]; // 42

File\deleteFile($path);
File\deleteDirectory($dir);
```

---

## Key Rules

- All `File\*` functions are fiber-suspending — they yield to the event loop while waiting for disk I/O
- `File\listFiles()` returns **filenames only**, not full paths — prepend the directory yourself
- `openFile()` modes: `'r'` read, `'w'` write (truncate), `'a'` append, `'r+'` read+write
- After streaming writes, call `$file->end()` to flush; after reads, the file closes when the resource is destroyed
- `File\write()` / `File\read()` are convenience wrappers — equivalent to open + write/read all + close
- `File\deleteDirectory()` requires the directory to be empty; delete contents first for non-empty dirs
