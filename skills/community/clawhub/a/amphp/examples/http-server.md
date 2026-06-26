# AMPHP v3 — HTTP Server Patterns

---

## Minimal HTTP Server

```php
<?php declare(strict_types=1);

use Amp\Http\HttpStatus;
use Amp\Http\Server\DefaultErrorHandler;
use Amp\Http\Server\Request;
use Amp\Http\Server\RequestHandler;
use Amp\Http\Server\Response;
use Amp\Http\Server\SocketHttpServer;
use Monolog\Handler\StreamHandler;
use Monolog\Logger;
use function Amp\trapSignal;

$logger = new Logger('server');
$logger->pushHandler(new StreamHandler(STDOUT));

$server = SocketHttpServer::createForDirectAccess($logger);
$server->expose('0.0.0.0:8080');

$server->start(
    new class implements RequestHandler {
        public function handleRequest(Request $request): Response
        {
            return new Response(
                status: HttpStatus::OK,
                headers: ['Content-Type' => 'application/json'],
                body: json_encode(['status' => 'ok'], JSON_THROW_ON_ERROR),
            );
        }
    },
    new DefaultErrorHandler(),
);

if (\extension_loaded('pcntl')) {
    trapSignal([\SIGTERM, \SIGINT]);
    $server->stop();
} else {
    \Revolt\EventLoop::run(); // Windows fallback
}
```

---

## Router with Route Parameters

```php
<?php declare(strict_types=1);

use Amp\Http\HttpStatus;
use Amp\Http\Server\Request;
use Amp\Http\Server\RequestHandler;
use Amp\Http\Server\Response;
use Amp\Http\Server\Router;
use Amp\Http\Server\RequestHandler\ClosureRequestHandler; // NOT CallableRequestHandler

$router = new Router($server, $logger, $errorHandler);

// Static route
$router->addRoute('GET', '/', new HomeHandler());

// Route parameter (FastRoute syntax)
$router->addRoute('GET', '/users/{id:\d+}', new class implements RequestHandler {
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

// Inline handler via ClosureRequestHandler
$router->addRoute('POST', '/api/users', new ClosureRequestHandler(
    function (Request $request): Response {
        $data = json_decode($request->getBody()->buffer(), true, flags: JSON_THROW_ON_ERROR);
        return new Response(
            HttpStatus::CREATED,
            ['Content-Type' => 'application/json'],
            json_encode(['id' => 1, 'name' => $data['name']], JSON_THROW_ON_ERROR),
        );
    }
));

// 404 fallback
$router->setFallback(new class implements RequestHandler {
    public function handleRequest(Request $request): Response
    {
        return new Response(HttpStatus::NOT_FOUND, [], 'Not Found');
    }
});

$server->start($router, $errorHandler);
```

---

## Middleware

```php
<?php declare(strict_types=1);

use Amp\Http\Server\Middleware;
use Amp\Http\Server\Request;
use Amp\Http\Server\RequestHandler;
use Amp\Http\Server\Response;
use function Amp\Http\Server\Middleware\stackMiddleware;

class LoggingMiddleware implements Middleware
{
    public function handleRequest(Request $request, RequestHandler $next): Response
    {
        $start    = microtime(true);
        $response = $next->handleRequest($request);
        $elapsed  = (microtime(true) - $start) * 1000;
        error_log(sprintf('%s %s %.1fms', $request->getMethod(), $request->getUri(), $elapsed));
        return $response;
    }
}

class AuthMiddleware implements Middleware
{
    public function handleRequest(Request $request, RequestHandler $next): Response
    {
        if (!$this->isAuthorized($request)) {
            return new Response(\Amp\Http\HttpStatus::UNAUTHORIZED);
        }
        return $next->handleRequest($request);
    }

    private function isAuthorized(Request $request): bool
    {
        return $request->getHeader('Authorization') === 'Bearer secret';
    }
}

// stackMiddleware: applied left-to-right, first listed = outermost
$handler = stackMiddleware($router, new LoggingMiddleware(), new AuthMiddleware());
$server->start($handler, $errorHandler);
```

---

## Static Files (DocumentRoot + StaticResource)

```php
<?php declare(strict_types=1);

use Amp\Http\Server\StaticContent\DocumentRoot;
use Amp\Http\Server\StaticContent\StaticResource;

// Serve entire directory
$docRoot = new DocumentRoot($server, $errorHandler, '/var/www/public');
$router->setFallback($docRoot); // SPA-friendly fallback

// Single file (supports ETag, Range, If-None-Match automatically)
$favicon = new StaticResource($server, $errorHandler, '/var/www/favicon.ico');
$router->addRoute('GET', '/favicon.ico', $favicon);

// SPA index.html fallback inside DocumentRoot
$docRoot->setFallback(
    new StaticResource($server, $errorHandler, '/var/www/public/index.html')
);
```

---

## SocketHttpServer — direct constructor (full control)

```php
<?php declare(strict_types=1);

use Amp\Http\Server\SocketHttpServer;
use Amp\Http\Server\DefaultErrorHandler;
use Amp\Http\Server\Driver\SocketClientFactory;
use Amp\Socket\BindContext;
use Amp\Socket\Certificate;
use Amp\Socket\ResourceServerSocketFactory;
use Amp\Socket\ServerTlsContext;

// Use direct constructor when you need custom socket factory or fine-grained control
// (bypasses connection-per-IP / concurrency limits of createForDirectAccess())
$server = new SocketHttpServer(
    logger:              $logger,
    serverSocketFactory: new ResourceServerSocketFactory(),
    clientFactory:       new SocketClientFactory($logger),
);

// Expose with TLS
$tlsContext = (new ServerTlsContext())
    ->withDefaultCertificate(new Certificate('/etc/ssl/cert.pem', '/etc/ssl/key.pem'));

$server->expose('0.0.0.0:443', (new BindContext())->withTlsContext($tlsContext));

// Disable Nagle's algorithm (useful for benchmarks / small responses)
$server->expose('0.0.0.0:8080', (new BindContext())->withTcpNoDelay());

$server->start($requestHandler, new DefaultErrorHandler());
```

---

## Behind Proxy (X-Forwarded-For)

```php
<?php declare(strict_types=1);

use Amp\Http\Server\SocketHttpServer;
use Amp\Http\Server\Driver\Http1Driver;

$server = SocketHttpServer::createForBehindProxy(
    $logger,
    \Amp\Http\Server\Driver\ForwardedHeaderType::XForwardedFor,
    ['10.0.0.0/8', '172.16.0.0/12'], // trusted proxy CIDRs
);
```

---

## Sessions

```php
<?php declare(strict_types=1);

use Amp\Http\Server\Session\CookieAttributes;
use Amp\Http\Server\Session\LocalSessionStorage;
use Amp\Http\Server\Session\Session;
use Amp\Http\Server\Session\SessionMiddleware;
use function Amp\Http\Server\Middleware\stackMiddleware;

$sessionMiddleware = new SessionMiddleware(
    storage: new LocalSessionStorage(),
    cookieAttributes: CookieAttributes::default()
        ->withSecure()
        ->withHttpOnly()
        ->withSameSite(CookieAttributes::SAME_SITE_LAX)
        ->withMaxAge(3600),
);

$handler = stackMiddleware(
    new class implements \Amp\Http\Server\RequestHandler {
        public function handleRequest(\Amp\Http\Server\Request $request): \Amp\Http\Server\Response
        {
            /** @var Session $session */
            $session = $request->getAttribute(Session::class);
            $userId  = $session->get('user_id');

            $session->lock();
            try {
                $session->set('user_id', 42);
                $session->commit();
            } finally {
                $session->unlock();
            }

            return new \Amp\Http\Server\Response(\Amp\Http\HttpStatus::OK, [], "user=$userId");
        }
    },
    $sessionMiddleware,
);
```
