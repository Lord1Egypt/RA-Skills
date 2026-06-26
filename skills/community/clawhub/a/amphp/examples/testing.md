# AMPHP v3 — Testing Patterns

> All async tests must extend `Amp\PHPUnit\AsyncTestCase`. It runs each test method inside the Revolt event loop so `await()`, `delay()`, and `async()` work directly.

---

## Basic async test

```php
<?php declare(strict_types=1);

use Amp\PHPUnit\AsyncTestCase;
use function Amp\delay;
use function Amp\async;

class MyServiceTest extends AsyncTestCase
{
    public function testAsyncOperation(): void
    {
        // await(), delay(), async() all work directly inside test methods
        $result = someAsyncFunction()->await();
        $this->assertSame('expected', $result);
    }

    public function testWithDelay(): void
    {
        $start = microtime(true);
        delay(0.1);
        $elapsed = microtime(true) - $start;

        $this->assertGreaterThanOrEqual(0.09, $elapsed);
    }

    public function testParallelFutures(): void
    {
        $futures = [
            async(fn() => 'a'),
            async(fn() => 'b'),
            async(fn() => 'c'),
        ];

        $results = \Amp\Future\await($futures);
        $this->assertSame(['a', 'b', 'c'], $results);
    }
}
```

---

## Running tests

```bash
# Run all tests (phpunit.xml sets zend.assertions=1 automatically)
php vendor/bin/phpunit

# Single test file
php vendor/bin/phpunit test/MyServiceTest.php

# Single test method
php vendor/bin/phpunit --filter testAsyncOperation

# If phpunit.xml doesn't set assertions, add flags manually:
php -dzend.assertions=1 -dassert.exception=1 vendor/bin/phpunit
```

---

## Testing an HTTP RequestHandler

```php
<?php declare(strict_types=1);

use Amp\ByteStream;
use Amp\Http\HttpStatus;
use Amp\Http\Server\Driver\Client;
use Amp\Http\Server\Request;
use Amp\Http\Server\Response;
use Amp\PHPUnit\AsyncTestCase;
use League\Uri\Http;

class ApiHandlerTest extends AsyncTestCase
{
    private ApiHandler $handler;
    private Client $client;

    protected function setUp(): void
    {
        parent::setUp();
        $this->handler = new ApiHandler();
        // Mock the Client interface — only needed for Request constructor
        $this->client = $this->createMock(Client::class);
    }

    private function makeRequest(string $method, string $path): Request
    {
        return new Request(
            $this->client,
            $method,
            Http::new('http://localhost:8080' . $path), // League\Uri\Http::new() for URI
        );
    }

    private function decodeBody(Response $response): array
    {
        $body = ByteStream\buffer($response->getBody());
        return json_decode($body, true, flags: JSON_THROW_ON_ERROR);
    }

    public function testReturns200(): void
    {
        $response = $this->handler->handleRequest($this->makeRequest('GET', '/api/status'));
        $this->assertSame(HttpStatus::OK, $response->getStatus());
    }

    public function testJsonContentType(): void
    {
        $response = $this->handler->handleRequest($this->makeRequest('GET', '/api/status'));
        $this->assertSame('application/json', $response->getHeader('content-type'));
    }

    public function testResponseBody(): void
    {
        $response = $this->handler->handleRequest($this->makeRequest('GET', '/api/status'));
        $data = $this->decodeBody($response);

        $this->assertArrayHasKey('status', $data);
        $this->assertSame('ok', $data['status']);
    }

    public function testNotFound(): void
    {
        $response = $this->handler->handleRequest($this->makeRequest('GET', '/api/unknown'));
        $this->assertSame(HttpStatus::NOT_FOUND, $response->getStatus());
    }
}
```

> **Key**: `Amp\Http\Server\Request` constructor takes `(Client $client, string $method, UriInterface $uri)`. Use `League\Uri\Http::new($url)` to create the URI.

---

## Testing async services with mocks

```php
<?php declare(strict_types=1);

use Amp\PHPUnit\AsyncTestCase;
use Amp\Future;
use function Amp\async;

interface UserRepository
{
    public function find(int $id): ?array;
}

class UserServiceTest extends AsyncTestCase
{
    public function testFetchUser(): void
    {
        $mockRepo = $this->createMock(UserRepository::class);
        $mockRepo->method('find')
            ->with(42)
            ->willReturn(['id' => 42, 'name' => 'Alice']);

        $service = new UserService($mockRepo);
        $user    = $service->getUser(42);

        $this->assertSame('Alice', $user['name']);
    }

    public function testConcurrentRequests(): void
    {
        $service = new UserService(new InMemoryUserRepository());

        $futures = array_map(
            fn(int $id) => async(fn() => $service->getUser($id)),
            [1, 2, 3],
        );

        $users = \Amp\Future\await($futures);
        $this->assertCount(3, $users);
    }
}
```

---

## setUp() and tearDown() in async tests

```php
<?php declare(strict_types=1);

use Amp\PHPUnit\AsyncTestCase;
use Amp\File;

class FileServiceTest extends AsyncTestCase
{
    private string $tempDir;

    protected function setUp(): void
    {
        parent::setUp(); // ALWAYS call parent::setUp() first

        $this->tempDir = sys_get_temp_dir() . '/test-' . uniqid();
        File\createDirectoryRecursively($this->tempDir, 0755);
    }

    protected function tearDown(): void
    {
        // Clean up test artifacts
        foreach (File\listFiles($this->tempDir) as $name) {
            File\deleteFile($this->tempDir . '/' . $name);
        }
        File\deleteDirectory($this->tempDir);

        parent::tearDown(); // ALWAYS call parent::tearDown() last
    }

    public function testWriteAndRead(): void
    {
        $path = $this->tempDir . '/data.txt';
        File\write($path, 'hello');
        $this->assertSame('hello', File\read($path));
    }
}
```

---

## Key Rules

- Always extend `Amp\PHPUnit\AsyncTestCase` — never extend `TestCase` directly for async tests
- Always call `parent::setUp()` first and `parent::tearDown()` last in overrides
- `Request` constructor for testing: `new Request($client, $method, Http::new($url))` — use `League\Uri\Http::new()`
- Use `ByteStream\buffer($response->getBody())` to read a response body in tests
- `phpunit.xml` should set `zend.assertions=1` and `assert.exception=1`; otherwise add `-dzend.assertions=1` flags
- `createMock(Client::class)` is sufficient for the HTTP client dependency in `Request` — it's never called
