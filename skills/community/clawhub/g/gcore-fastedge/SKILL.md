---
name: fastedge
description: Build and deploy WebAssembly applications to Gcore FastEdge edge computing platform. Use when creating, building, or deploying FastEdge HTTP apps with Rust SDK. Triggers on phrases like "deploy to FastEdge", "build FastEdge app", "create FastEdge application", "Wasm on FastEdge", or when working with Gcore edge computing.
metadata: '{"openclaw":{"requires":{"bins":["rustup","cargo","python3"],"env":["GCORE_API_KEY"]},"primaryEnv":"GCORE_API_KEY","install":[{"id":"requests","kind":"uv","packages":["requests"],"label":"Install Python requests package (uv)"}]}}'
---

# FastEdge Skill

Build and deploy WebAssembly HTTP applications to Gcore FastEdge.

## Quick Start

### 1. Create a new FastEdge app

Initialize a Rust project with the FastEdge SDK:

```bash
mkdir myapp && cd myapp
```

Create `.cargo/config.toml`:
```toml
[build]
target = "wasm32-wasip1"
```

Create `Cargo.toml`:
```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
fastedge = "0.2"
```

Create `src/lib.rs`:
```rust
use fastedge::{
    body::Body,
    http::{Request, Response, StatusCode, Error},
};

#[fastedge::http]
fn main(_req: Request<Body>) -> Result<Response<Body>, Error> {
    Response::builder()
        .status(StatusCode::OK)
        .header("content-type", "text/plain")
        .body(Body::from("Hello from FastEdge!"))
}
```

### 2. Build the Wasm binary

Requires Rust and wasm32-wasip1 target:

```bash
rustup target add wasm32-wasip1
cargo build --release
```

Binary location: `target/wasm32-wasip1/release/myapp.wasm`

### 3. Deploy via CLI

Set your API key (get from https://accounts.gcore.com/account-settings/api-tokens):

```bash
export GCORE_API_KEY="your_api_token"
```

Upload binary:
```bash
curl -X POST \
  'https://api.gcore.com/fastedge/v1/binaries/raw' \
  -H 'accept: application/json' \
  -H "Authorization: APIKey $GCORE_API_KEY" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary '@./target/wasm32-wasip1/release/myapp.wasm'
```

Save the `id` from response (binary_id).

Create app:
```bash
curl -X POST \
  'https://api.gcore.com/fastedge/v1/apps' \
  -H 'accept: application/json' \
  -H 'client_id: 0' \
  -H "Authorization: APIKey $GCORE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "my-app-name",
    "binary": BINARY_ID,
    "status": 1
  }'
```

Your app will be at: `https://my-app-name-XXXX.fastedge.app`

## Useful Patterns

### HTML Response

```rust
Response::builder()
    .status(StatusCode::OK)
    .header("content-type", "text/html; charset=utf-8")
    .body(Body::from(html_string))
```

### Access Request Headers

```rust
let ip = req.headers()
    .get("x-real-ip")
    .and_then(|v| v.to_str().ok())
    .unwrap_or("unknown");
```

Common headers provided by FastEdge:
- `x-real-ip` - Client IP address
- `x-forwarded-for` - Proxied client IP
- `geoip-country-code` - Country code
- `geoip-city` - City name
- `host` - Request host

### Update Existing App

```bash
curl -X PUT \
  'https://api.gcore.com/fastedge/v1/apps/APP_ID' \
  -H 'accept: application/json' \
  -H "Authorization: APIKey $GCORE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "binary": NEW_BINARY_ID,
    "status": 1,
    "name": "app-name"
  }'
```

## Resources

- **Template project**: See `assets/rust-template/` for a starter template
- **Build script**: See `scripts/build_rust.py` for automated build/upload
- **API Docs**: https://gcore.com/docs/fastedge
