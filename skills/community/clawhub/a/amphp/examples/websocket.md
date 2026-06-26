# AMPHP v3 — WebSocket Patterns

> **Import note**: `WebsocketClient` is in `amphp/websocket` (`Amp\Websocket`), NOT in `amphp/websocket-server`.

---

## Echo Server (receive → reply)

```php
<?php declare(strict_types=1);

use Amp\Http\Server\Request;
use Amp\Http\Server\Response;
use Amp\Websocket\WebsocketClient;
use Amp\Websocket\Server\AllowOriginAcceptor;
use Amp\Websocket\Server\Websocket;
use Amp\Websocket\Server\WebsocketClientHandler;

$websocket = new Websocket(
    httpServer:    $server,
    logger:        $logger,
    acceptor:      new AllowOriginAcceptor(['https://example.com']),
    clientHandler: new class implements WebsocketClientHandler {
        public function handleClient(
            WebsocketClient $client,
            Request $request,
            Response $response,
        ): void {
            while ($message = $client->receive()) {   // null = client disconnected
                $client->sendText($message->buffer()); // sendText() or sendBinary()
            }
        }
    },
);

$router->addRoute('GET', '/ws', $websocket);
```

---

## Push-Only Pattern (server pushes, drains receive buffer)

Not draining incoming messages causes receive buffer overflow and deadlock.

```php
<?php declare(strict_types=1);

use Amp\Http\Server\Request;
use Amp\Http\Server\Response;
use Amp\Websocket\WebsocketClient;
use Amp\Websocket\Server\WebsocketClientHandler;
use function Amp\async;
use function Amp\delay;

new class implements WebsocketClientHandler {
    public function __construct(private readonly float $interval = 1.0) {}

    public function handleClient(
        WebsocketClient $client,
        Request $request,
        Response $response,
    ): void {
        // Sender fiber: push data to client on a schedule
        $sender = async(function () use ($client): void {
            while (!$client->isClosed()) {
                $client->sendText(json_encode(
                    ['time' => date('Y-m-d H:i:s'), 'timestamp' => time()],
                    JSON_THROW_ON_ERROR,
                ));
                delay($this->interval);
            }
        });

        // REQUIRED: drain incoming messages to prevent buffer deadlock
        while ($client->receive() !== null) {
            // ignore client messages
        }

        // Client disconnected — suppress unhandled errors from the sender fiber
        $sender->ignore();
    }
};
```

---

## Broadcast Gateway (push to all connected clients)

```php
<?php declare(strict_types=1);

use Amp\Http\Server\Request;
use Amp\Http\Server\Response;
use Amp\Websocket\WebsocketClient;
use Amp\Websocket\Server\WebsocketClientGateway;
use Amp\Websocket\Server\WebsocketClientHandler;

$gateway = new WebsocketClientGateway();

$clientHandler = new class($gateway) implements WebsocketClientHandler {
    public function __construct(private readonly WebsocketClientGateway $gateway) {}

    public function handleClient(
        WebsocketClient $client,
        Request $request,
        Response $response,
    ): void {
        // addClient() auto-removes on disconnect — no removeClient() needed
        $this->gateway->addClient($client);

        while ($message = $client->receive()) {
            // Broadcast incoming message to ALL connected clients
            $this->gateway->broadcastText($message->buffer());
        }
    }
};

// Push server-side event from anywhere:
$gateway->broadcastText(json_encode(['type' => 'update', 'data' => $payload], JSON_THROW_ON_ERROR));
```

---

## WebSocket Client (amphp/websocket-client)

```php
<?php declare(strict_types=1);

use Amp\TimeoutCancellation;
use Amp\Websocket\Client\Rfc6455Connector;
use Amp\Websocket\Client\WebsocketHandshake;

$connector  = new Rfc6455Connector();
$handshake  = (new WebsocketHandshake('wss://echo.websocket.org'))
    ->withHeader('Authorization', 'Bearer ' . $token);

$connection = $connector->connect($handshake, new TimeoutCancellation(10.0));

$connection->sendText('Hello, Server!');

while ($message = $connection->receive()) {
    echo $message->buffer() . "\n";
    if ($message->buffer() === 'bye') {
        break;
    }
}

$connection->close();
```

---

## Streaming Large Binary WebSocket Messages

```php
<?php declare(strict_types=1);

use Amp\Websocket\Client\Rfc6455Connector;
use Amp\Websocket\Client\WebsocketHandshake;

$connector  = new Rfc6455Connector();
$connection = $connector->connect(new WebsocketHandshake('wss://stream.example.com'));

while ($message = $connection->receive()) {
    if ($message->isBinary()) {
        // Stream large binary payload without buffering all at once
        while (null !== $chunk = $message->read()) {
            processBinaryChunk($chunk);
        }
    } else {
        handleText($message->buffer());
    }
}
```

---

## Key Rules

- `WebsocketClient` → `Amp\Websocket\WebsocketClient` (from `amphp/websocket`)
- `WebsocketClientHandler`, `Websocket`, `AllowOriginAcceptor` → `Amp\Websocket\Server\*`
- Push-only handlers **must** drain incoming messages to prevent deadlock
- After the receive loop exits, call `$sender->ignore()` to suppress abandoned-fiber errors
- `addClient()` in `WebsocketClientGateway` automatically removes clients on disconnect
