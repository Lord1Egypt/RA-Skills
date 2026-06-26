# Workflow: Full HTTP Server (Router + Middleware + Static + WebSocket + Graceful Shutdown)

This workflow assembles a production-ready HTTP server with all common features wired together.

---

## Complete server.php

```php
<?php declare(strict_types=1);

use Amp\Http\HttpStatus;
use Amp\Http\Server\DefaultErrorHandler;
use Amp\Http\Server\Middleware;
use Amp\Http\Server\Request;
use Amp\Http\Server\RequestHandler;
use Amp\Http\Server\Response;
use Amp\Http\Server\Router;
use Amp\Http\Server\RequestHandler\ClosureRequestHandler;
use Amp\Http\Server\SocketHttpServer;
use Amp\Http\Server\StaticContent\DocumentRoot;
use Amp\Http\Server\StaticContent\StaticResource;
use Amp\Websocket\Server\AllowOriginAcceptor;
use Amp\Websocket\Server\Websocket;
use Amp\Websocket\Server\WebsocketClientHandler;
use Amp\Websocket\WebsocketClient;
use Monolog\Handler\StreamHandler;
use Monolog\Logger;
use function Amp\Http\Server\Middleware\stackMiddleware;
use function Amp\trapSignal;
use function Amp\async;
use function Amp\delay;

require __DIR__ . '/vendor/autoload.php';

// 1. Logger
$logger = new Logger('server');
$logger->pushHandler(new StreamHandler(STDOUT));

// 2. HTTP server
$server       = SocketHttpServer::createForDirectAccess($logger);
$errorHandler = new DefaultErrorHandler();
$server->expose('0.0.0.0:8080');

// 3. Router
$router = new Router($server, $logger, $errorHandler);

// Static route
$router->addRoute('GET', '/api/status', new class implements RequestHandler {
    public function handleRequest(Request $request): Response
    {
        return new Response(
            status: HttpStatus::OK,
            headers: ['Content-Type' => 'application/json'],
            body: json_encode(['status' => 'ok', 'version' => PHP_VERSION], JSON_THROW_ON_ERROR),
        );
    }
});

// Route with parameter (FastRoute syntax)
$router->addRoute('GET', '/api/users/{id:\d+}', new class implements RequestHandler {
    public function handleRequest(Request $request): Response
    {
        $args = $request->getAttribute(Router::class); // ['id' => '42']
        $id   = (int) $args['id'];
        return new Response(
            HttpStatus::OK,
            ['Content-Type' => 'application/json'],
            json_encode(['id' => $id], JSON_THROW_ON_ERROR),
        );
    }
});

// Inline handler
$router->addRoute('POST', '/api/echo', new ClosureRequestHandler(
    function (Request $request): Response {
        $body = $request->getBody()->buffer();
        return new Response(HttpStatus::OK, ['Content-Type' => 'text/plain'], $body);
    }
));

// 4. WebSocket endpoint
$websocket = new Websocket(
    httpServer:    $server,
    logger:        $logger,
    acceptor:      new AllowOriginAcceptor(['http://localhost:8080']),
    clientHandler: new class implements WebsocketClientHandler {
        public function handleClient(
            WebsocketClient $client,
            Request $request,
            Response $response,
        ): void {
            // Push-only pattern: send time every second, drain incoming messages
            $sender = async(function () use ($client): void {
                while (!$client->isClosed()) {
                    $client->sendText(json_encode(
                        ['time' => date('Y-m-d H:i:s'), 'ts' => time()],
                        JSON_THROW_ON_ERROR,
                    ));
                    delay(1.0);
                }
            });

            while ($client->receive() !== null) {
                // drain to prevent receive buffer deadlock
            }

            $sender->ignore();
        }
    },
);
$router->addRoute('GET', '/ws', $websocket);

// 5. Static files
$docRoot = new DocumentRoot($server, $errorHandler, __DIR__ . '/public');
$docRoot->setFallback(
    new StaticResource($server, $errorHandler, __DIR__ . '/public/index.html'),
);
$router->setFallback($docRoot);

// 6. Middleware stack (applied outermost-first: Logging wraps Auth wraps Router)
$handler = stackMiddleware(
    $router,
    new class implements Middleware {
        public function handleRequest(Request $request, RequestHandler $next): Response
        {
            $start    = hrtime(true);
            $response = $next->handleRequest($request);
            $ms       = round((hrtime(true) - $start) / 1e6, 1);
            error_log(sprintf('%s %s %dms', $request->getMethod(), $request->getUri(), $ms));
            return $response;
        }
    },
);

// 7. Start
$server->start($handler, $errorHandler);

// 8. Graceful shutdown
// On Windows: pcntl is not available — trapSignal() would throw. Fall back to EventLoop::run().
if (extension_loaded('pcntl')) {
    trapSignal([\SIGTERM, \SIGINT]);
    $server->stop();
} else {
    \Revolt\EventLoop::run();
}
```

---

## Key points

- **Router** comes from `amphp/http-server-router`; import `Amp\Http\Server\Router`
- `stackMiddleware($handler, $m1, $m2, ...)` — first listed = outermost (runs first on request, last on response)
- `DocumentRoot` + `setFallback(StaticResource)` = SPA-friendly fallback to `index.html`
- Always add WebSocket route **before** `setFallback` — otherwise static files catch the WS upgrade path
- `$server->stop()` is called after `trapSignal()` returns, ensuring in-flight requests finish
- On Windows: wrap `trapSignal` in `extension_loaded('pcntl')` guard and fall back to `EventLoop::run()`
- `ClosureRequestHandler` is in `Amp\Http\Server\RequestHandler\ClosureRequestHandler` (not `CallableRequestHandler`)

---

## Packages needed

```bash
composer require revolt/event-loop amphp/amp
composer require amphp/http-server
composer require amphp/http-server-router
composer require amphp/http-server-static-content
composer require amphp/websocket-server
composer require monolog/monolog
```
