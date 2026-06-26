# AMPHP v3 — HTTP Client Patterns

> **Import alias**: use `Request as HttpRequest` to avoid conflict with `Amp\Http\Server\Request`.

---

## Simple GET and POST

```php
<?php declare(strict_types=1);

use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request as HttpRequest;

$client = HttpClientBuilder::buildDefault();

// GET
$response = $client->request(new HttpRequest('https://api.example.com/data'));
$body     = $response->getBody()->buffer(); // MUST buffer or fully iterate!
echo $response->getStatus(); // 200

// POST with JSON body
$request = new HttpRequest('https://api.example.com/users', 'POST');
$request->setHeader('Content-Type', 'application/json');
$request->setBody(json_encode(['name' => 'Alice'], JSON_THROW_ON_ERROR));
$response = $client->request($request);
$data     = json_decode($response->getBody()->buffer(), true, flags: JSON_THROW_ON_ERROR);
```

---

## Parallel Requests with Timeout

```php
<?php declare(strict_types=1);

use Amp\Future;
use Amp\TimeoutCancellation;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request as HttpRequest;
use function Amp\async;

$client = HttpClientBuilder::buildDefault();
$urls   = ['https://a.com', 'https://b.com', 'https://c.com'];

$futures = array_map(
    fn(string $url) => async(
        fn() => $client->request(new HttpRequest($url), new TimeoutCancellation(10.0))
    ),
    $urls,
);

$responses = Future\await($futures);
```

---

## ConnectionLimitingPool — limit connections per host

```php
<?php declare(strict_types=1);

use Amp\Http\Client\Connection\ConnectionLimitingPool;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request as HttpRequest;
use Amp\Future;
use function Amp\async;

// Constructor is private — use the static factory:
$pool = ConnectionLimitingPool::byAuthority(2); // max 2 connections per host

$client = (new HttpClientBuilder())
    ->usingPool($pool)
    ->followRedirects(0)
    ->build();

$futures = array_map(
    fn(string $url) => async(fn() => $client->request(new HttpRequest($url))->getBody()->buffer()),
    ['https://example.com/1', 'https://example.com/2', 'https://example.com/3'],
);

$bodies = Future\await($futures);
```

---

## Interceptors (decompress, follow redirects, retry)

```php
<?php declare(strict_types=1);

use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Interceptor\DecompressResponse;
use Amp\Http\Client\Interceptor\FollowRedirects;
use Amp\Http\Client\Interceptor\RetryRequests;
use Amp\Http\Client\Request as HttpRequest;

$client = (new HttpClientBuilder())
    ->intercept(new DecompressResponse())
    ->intercept(new FollowRedirects(maxRedirects: 5))
    ->intercept(new RetryRequests(maxRetries: 2))
    ->build();

$response = $client->request(new HttpRequest('https://httpbin.org/get'));
$body     = $response->getBody()->buffer();
echo $response->getStatus(); // 200
```

---

## HTTP CONNECT Proxy (amphp/http-tunnel)

```php
<?php declare(strict_types=1);

use Amp\Http\Client\Connection\DefaultConnectionFactory;
use Amp\Http\Client\Connection\UnlimitedConnectionPool;
use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request as HttpRequest;
use Amp\Http\Tunnel\Http1TunnelConnector;

$tunnelConnector = new Http1TunnelConnector(
    proxyAddress: '127.0.0.1:3128',
    proxyHeaders: [
        'Proxy-Authorization' => 'Basic ' . base64_encode('user:secret'),
    ],
);

$client = (new HttpClientBuilder())
    ->usingPool(new UnlimitedConnectionPool(new DefaultConnectionFactory($tunnelConnector)))
    ->build();

$response = $client->request(new HttpRequest('https://example.com/api'));
$body     = $response->getBody()->buffer();
```

---

## Streaming Response Body

```php
<?php declare(strict_types=1);

use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request as HttpRequest;

$client   = HttpClientBuilder::buildDefault();
$response = $client->request(new HttpRequest('https://example.com/large-file'));

// Stream chunk-by-chunk instead of buffering all at once
while (null !== $chunk = $response->getBody()->read()) {
    processChunk($chunk);
}
```

---

## Key Rules

- Always call `buffer()` or fully iterate the response body — leaving it unread blocks connection reuse
- Use `Request as HttpRequest` alias to avoid conflict with `Amp\Http\Server\Request`
- `HttpClientBuilder::buildDefault()` creates a default client without any interceptors
