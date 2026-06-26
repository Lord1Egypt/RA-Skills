# AMPHP v3 — ByteStream Patterns

---

## ReadableBuffer and WritableBuffer

```php
<?php declare(strict_types=1);

use Amp\ByteStream\ReadableBuffer;
use Amp\ByteStream\WritableBuffer;
use function Amp\ByteStream\buffer;

// Wrap a string as a ReadableStream
$stream  = new ReadableBuffer("Hello, World!");
$content = buffer($stream); // "Hello, World!"

// Collect written chunks
$buf = new WritableBuffer();
$buf->write("chunk1");
$buf->write("chunk2");
$buf->end();
$result = $buf->buffer(); // "chunk1chunk2"
```

---

## pipe() — transfer data between streams

```php
<?php declare(strict_types=1);

use Amp\ByteStream\ReadableBuffer;
use Amp\ByteStream\WritableBuffer;
use function Amp\ByteStream\pipe;

$source = new ReadableBuffer("transfer me");
$sink   = new WritableBuffer();

pipe($source, $sink);
$sink->end(); // IMPORTANT: pipe() does NOT close the sink — caller must do it

echo $sink->buffer(); // "transfer me"
```

---

## ReadableIterableStream — wrap array/iterator

```php
<?php declare(strict_types=1);

use Amp\ByteStream\ReadableIterableStream;
use function Amp\ByteStream\buffer;

// Wraps an array of strings as a ReadableStream.
// Unlike ReadableBuffer, it stays open until the iterator is exhausted.
// Required as source for Base64DecodingReadableStream (see below).
$chunks  = ['Hello ', 'World', '!'];
$stream  = new ReadableIterableStream($chunks);
$content = buffer($stream); // "Hello World!"

// Also works with a Generator:
$stream = new ReadableIterableStream((function () {
    yield 'line1';
    yield 'line2';
})());
```

---

## Payload — bufferable + streamable access

```php
<?php declare(strict_types=1);

use Amp\ByteStream\Payload;
use Amp\ByteStream\ReadableBuffer;

$payload = new Payload(new ReadableBuffer("binary data"));

// Option 1: buffer all at once
$bytes = $payload->buffer(); // "binary data"

// Option 2: stream chunk-by-chunk
$stream = new Payload(new ReadableBuffer("binary data"));
while (null !== $chunk = $stream->read()) {
    processChunk($chunk); // null signals end of stream
}
```

---

## GZIP Compression / Decompression

```php
<?php declare(strict_types=1);

use Amp\ByteStream\Compression\CompressingWritableStream;
use Amp\ByteStream\Compression\DecompressingReadableStream;
use Amp\ByteStream\ReadableBuffer;
use Amp\ByteStream\WritableBuffer;
use function Amp\ByteStream\buffer;

// Compress
$sink       = new WritableBuffer();
$compressor = new CompressingWritableStream($sink, \ZLIB_ENCODING_GZIP);
$compressor->write("some data");
$compressor->end();
$compressed = $sink->buffer();

// Decompress
$source       = new ReadableBuffer($compressed);
$decompressor = new DecompressingReadableStream($source, \ZLIB_ENCODING_GZIP);
$original     = buffer($decompressor); // "some data"
```

---

## Base64 Encode / Decode

```php
<?php declare(strict_types=1);

use Amp\ByteStream\Base64\Base64DecodingReadableStream;
use Amp\ByteStream\Base64\Base64EncodingReadableStream;
use Amp\ByteStream\ReadableBuffer;
use Amp\ByteStream\ReadableIterableStream;
use function Amp\ByteStream\buffer;

// Encode to Base64
$encoded = buffer(new Base64EncodingReadableStream(new ReadableBuffer("hello world")));

// IMPORTANT: Use ReadableIterableStream (NOT ReadableBuffer) as the decoder source.
// ReadableBuffer closes itself after returning EOF, which causes Base64DecodingReadableStream
// to throw StreamException on the follow-up isClosed() check.
// ReadableIterableStream only closes after the iterator is exhausted — safe to use here.
$decoded = buffer(new Base64DecodingReadableStream(new ReadableIterableStream([$encoded])));
// $decoded === "hello world"
```

---

## splitLines() — iterate a stream line by line

```php
<?php declare(strict_types=1);

use Amp\Socket;
use function Amp\async;
use function Amp\ByteStream\splitLines;

$server = Socket\listen('tcp://127.0.0.1:9000');

while ($socket = $server->accept()) {
    async(function () use ($socket): void {
        foreach (splitLines($socket) as $line) {
            $socket->write(strtoupper($line) . "\n");
        }
        $socket->end();
    });
}
```

---

## ReadableResourceStream / WritableResourceStream

```php
<?php declare(strict_types=1);

use Amp\ByteStream\ReadableResourceStream;
use Amp\ByteStream\WritableResourceStream;
use function Amp\ByteStream\buffer;

$resource = fopen('/path/to/file.txt', 'r');
stream_set_blocking($resource, false);
$readable = new ReadableResourceStream($resource);
$content  = buffer($readable);

$out = new WritableResourceStream(fopen('/tmp/out.txt', 'w'));
$out->write("line\n");
$out->end();
```
