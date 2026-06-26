# Workflow: TCP Echo Server with Socket + ByteStream

This workflow builds a TCP server that accepts connections, reads lines from each client, echoes them back in uppercase, and handles multiple clients concurrently.

---

## Complete TCP server

```php
<?php declare(strict_types=1);

use Amp\Socket;
use function Amp\async;
use function Amp\ByteStream\splitLines;
use function Amp\trapSignal;

require __DIR__ . '/vendor/autoload.php';

// 1. Bind and listen on TCP port
$server = Socket\listen('tcp://0.0.0.0:9000');

echo "Listening on tcp://0.0.0.0:9000\n";

// 2. Accept clients in a loop
// Each client is handled in its own async fiber — fully concurrent
while ($socket = $server->accept()) {
    async(function () use ($socket): void {
        handleClient($socket);
    });
}

function handleClient(Socket\Socket $socket): void
{
    $peer = $socket->getRemoteAddress()->toString();
    echo "Connected: $peer\n";

    try {
        // splitLines() yields one line at a time, suspending between reads
        foreach (splitLines($socket) as $line) {
            $response = strtoupper($line) . "\n";
            $socket->write($response);
        }
    } finally {
        // end() sends EOF; close() terminates immediately
        $socket->end();
        echo "Disconnected: $peer\n";
    }
}
```

---

## TCP server with binary protocol (chunked reads)

```php
<?php declare(strict_types=1);

use Amp\Socket;
use function Amp\async;

$server = Socket\listen('tcp://0.0.0.0:9001');

while ($socket = $server->accept()) {
    async(function () use ($socket): void {
        try {
            // Read chunks as they arrive; null = client disconnected
            while (null !== $chunk = $socket->read()) {
                // Echo the raw bytes back
                $socket->write($chunk);
            }
        } finally {
            $socket->end();
        }
    });
}
```

---

## TCP client

```php
<?php declare(strict_types=1);

use Amp\Socket;
use Amp\TimeoutCancellation;

// Connect with a timeout
$socket = Socket\connect('tcp://127.0.0.1:9000', cancellation: new TimeoutCancellation(5.0));

$socket->write("hello world\n");
$socket->write("foo bar\n");

// Read the responses
foreach (\Amp\ByteStream\splitLines($socket) as $line) {
    echo "Server replied: $line\n";
    // Break after receiving expected lines:
    if ($line === 'FOO BAR') {
        break;
    }
}

$socket->end();
```

---

## TLS server

```php
<?php declare(strict_types=1);

use Amp\Socket;
use Amp\Socket\BindContext;
use Amp\Socket\Certificate;
use Amp\Socket\ServerTlsContext;

$tlsContext = (new ServerTlsContext())
    ->withDefaultCertificate(new Certificate('/etc/ssl/cert.pem', '/etc/ssl/key.pem'));

$bindContext = (new BindContext())->withTlsContext($tlsContext);

$server = Socket\listen('tcp://0.0.0.0:9443', $bindContext);

while ($socket = $server->accept()) {
    async(function () use ($socket): void {
        // Upgrade to TLS — suspends until handshake completes
        $socket->setupTls();
        handleClient($socket);
    });
}
```

---

## Connect via Unix domain socket

```php
<?php declare(strict_types=1);

use Amp\Socket;

// Server
$server = Socket\listen('unix:///tmp/app.sock');

while ($socket = $server->accept()) {
    async(fn() => handleClient($socket));
}

// Client
$client = Socket\connect('unix:///tmp/app.sock');
$client->write("ping\n");
```

---

## Graceful shutdown

```php
<?php declare(strict_types=1);

use Amp\Socket;
use function Amp\async;
use function Amp\trapSignal;

$server = Socket\listen('tcp://0.0.0.0:9000');

// Track active client fibers
$futures = [];

async(function () use ($server, &$futures): void {
    while ($socket = $server->accept()) {
        $future = async(fn() => handleClient($socket));
        $futures[] = $future;
        $future->ignore(); // don't crash on unhandled exceptions from clients
    }
});

// Wait for SIGTERM or SIGINT, then stop accepting and close
if (extension_loaded('pcntl')) {
    trapSignal([\SIGTERM, \SIGINT]);
} else {
    \Revolt\EventLoop::run();
}

$server->close();
\Amp\Future\await($futures); // wait for in-flight clients to finish
echo "Server stopped.\n";
```

---

## Key points

- `Socket\listen($uri)` returns a `SocketServer`; each `$server->accept()` call suspends until a client arrives
- Each client must be handled in `async()` — otherwise the accept loop blocks while the client is served
- `splitLines($socket)` yields one text line at a time, suspending between reads — perfect for line-based protocols
- `$socket->read()` returns `null` on disconnect; `splitLines()` stops iterating silently on disconnect
- `$socket->end()` sends EOF (graceful close); `$socket->close()` terminates immediately
- For TLS: call `$socket->setupTls()` after accepting — it suspends until the TLS handshake completes
- `Socket\connect()` accepts an optional `Cancellation` for connection timeout

---

## Packages needed

```bash
composer require revolt/event-loop amphp/amp
composer require amphp/socket
composer require amphp/byte-stream  # for splitLines()
```
