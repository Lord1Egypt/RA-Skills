---
name: agent-base
description: Create custom http.Agent.
---

# agent-base — Custom HTTP Agent Helper

Helps users create custom `http.Agent` subclasses based on the `agent-base` module, for scenarios such as HTTP request proxying, custom socket connections, etc.

## Trigger Scenarios

Use when the user needs to write HTTP/HTTPS/SOCKS/PAC proxies, custom HTTP connection logic, or extend `http.Agent`.

## Module Overview

`agent-base` wraps an ordinary function into an `http.Agent` instance. It is an abstract class that requires defining the `connect(req, opts)` method to create the underlying Socket.

- `connect()` can return any `Duplex` stream, or another `http.Agent` instance to delegate the request
- `connect()` can be an `async` function
- `opts.secureEndpoint` is used to distinguish between HTTP / HTTPS

## Quick Start

```ts
import * as net from 'net';
import * as tls from 'tls';
import * as http from 'http';
import { Agent } from 'agent-base';

class MyAgent extends Agent {
  connect(req, opts) {
    if (opts.secureEndpoint) {
      return tls.connect(opts);
    } else {
      return net.connect(opts);
    }
  }
}

const agent = new MyAgent({ keepAlive: true });
http.get('http://nodejs.org/api/', { agent }, (res) => {
  console.log('"response" event!', res.headers);
  res.pipe(process.stdout);
});
```

## Workflow

1. Identify user requirements: Pure HTTP/HTTPS proxy? SOCKS? PAC? Or custom routing?
2. If a mature solution exists, prioritize recommending community subclasses (see below)
3. If custom implementation is needed, write the `connect()` method based on the `Agent` abstract class
4. Provide complete, runnable TypeScript/JavaScript examples

## Proxy Details

See [references/proxy-details.md](references/proxy-details.md), which includes:
- `http-proxy-agent` — HTTP endpoint proxy
- `https-proxy-agent` — HTTPS endpoint proxy
- `pac-proxy-agent` — PAC file proxy
- `socks-proxy-agent` — SOCKS proxy
- Selection guide and comparison of each subclass