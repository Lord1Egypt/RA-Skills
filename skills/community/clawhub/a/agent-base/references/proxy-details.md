# Proxy Details and Subclass Selection

## Community Subclasses

### http-proxy-agent
- **Purpose**: HTTP(S) proxy for HTTP endpoints
- **Scenario**: Corporate intranet HTTP proxy, transparent proxy
- **Installation**: `npm install http-proxy-agent`

```ts
import { HttpProxyAgent } from 'http-proxy-agent';
const agent = new HttpProxyAgent('http://proxy.example.com:8080');
```

### https-proxy-agent
- **Purpose**: HTTP(S) proxy for HTTPS endpoints (via CONNECT tunnel)
- **Scenario**: Need to access HTTPS websites through an HTTP proxy
- **Installation**: `npm install https-proxy-agent`

```ts
import { HttpsProxyAgent } from 'https-proxy-agent';
const agent = new HttpsProxyAgent('http://proxy.example.com:8080');
```

### pac-proxy-agent
- **Purpose**: Automatic proxy configuration based on PAC files
- **Scenario**: Enterprise environments requiring automatic proxy selection based on URL rules
- **Installation**: `npm install pac-proxy-agent`

```ts
import { PacProxyAgent } from 'pac-proxy-agent';
const agent = new PacProxyAgent('pac+http://proxy.example.com/proxy.pac');
```

### socks-proxy-agent
- **Purpose**: SOCKS4/SOCKS5 proxy
- **Scenario**: SSH tunnels, Tor network
- **Installation**: `npm install socks-proxy-agent`

```ts
import { SocksProxyAgent } from 'socks-proxy-agent';
const agent = new SocksProxyAgent('socks5://127.0.0.1:1080');
```

## Selection Guide

| Requirement | Recommendation |
|-------------|----------------|
| HTTP requests through HTTP proxy | `http-proxy-agent` |
| HTTPS requests through HTTP proxy | `https-proxy-agent` |
| Automatic proxy switching based on rules | `pac-proxy-agent` |
| SOCKS proxy / SSH tunnel | `socks-proxy-agent` |
| Custom connection logic / routing | Implement yourself based on `agent-base` |

## Custom Advanced Examples

### Selecting Different Proxies Based on Target Host

```ts
import { Agent } from 'agent-base';
import { HttpsProxyAgent } from 'https-proxy-agent';
import { SocksProxyAgent } from 'socks-proxy-agent';

const proxyA = new HttpsProxyAgent('http://proxy-a:8080');
const proxyB = new SocksProxyAgent('socks5://proxy-b:1080');

class RoutedAgent extends Agent {
  async connect(req, opts) {
    if (req.host.includes('internal')) {
      return proxyA.connect(req, opts);
    }
    return proxyB.connect(req, opts);
  }
}
```

### Connection Pool + Custom Socket

```ts
import { Agent } from 'agent-base';
import * as net from 'net';
import * as tls from 'tls';

class PooledAgent extends Agent {
  connect(req, opts) {
    return new Promise((resolve, reject) => {
      const socket = opts.secureEndpoint
        ? tls.connect({ ...opts, servername: opts.host })
        : net.connect(opts);

      socket.on('connect', () => resolve(socket));
      socket.on('error', reject);
    });
  }
}

const agent = new PooledAgent({
  keepAlive: true,
  maxSockets: 10,
  keepAliveMsecs: 30000,
});
```

## Important Notes

1. **keepAlive**: When set to `true`, `connect()` is only called for new connections; reused existing connections do not trigger it
2. **secureEndpoint**: The `https` module sets this to `true`, the `http` module sets it to `false`
3. **Error Handling**: Exceptions in `connect()` are automatically caught and trigger the request's `error` event
4. **TypeScript**: `agent-base` ships with its own type definitions; no need to install additional `@types/`