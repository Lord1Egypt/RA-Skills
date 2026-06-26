# Standard Agentic Commerce Engine

A standard client and server spec for agent-friendly commerce. This project gives agents a consistent way to work with compatible e-commerce backends for product discovery, cart actions, account flows, and order creation, while leaving the final payment step to the user.

clawhub: https://clawhub.com/NowLoadY/agent-commerce-engine
GitHub: https://github.com/NowLoadY/agent-commerce-engine

## Why?

Most agent-to-store integrations repeat the same work: product lookup, cart state, account handling, and order submission. This project defines one way to expose those flows so an agent can work with multiple stores through the same command set.

- **Multi-store by design**: Connect to different stores with `--store <url>`. Credentials are isolated per domain.
- **Protocol-first**: Defines a stable set of commands for search, cart, profile, orders, promotions, and brand info.
- **Practical handoff model**: Agents can help users reach an order-ready state, but payment still returns to the user.

## Where It Fits

The **Standard Agentic Commerce Engine** is useful for independent stores and headless commerce backends that want a clear, lightweight way to support agent-driven shopping flows. Instead of building a custom tool for every brand, developers can implement the documented endpoints once and let agents reuse the same interaction model across stores.

## Quick Start

1.  **Install dependency**:
    ```bash
    pip install requests
    ```

2.  **Run with Agent/CLI**:
    ```bash
    # Target any compliant store via --store
    python3 scripts/commerce.py --store https://api.yourstore.com/v1 list

    # Login to a store
    python3 scripts/commerce.py --store https://api.yourstore.com/v1 login --account user@example.com --password secret

    # View all locally registered stores
    python3 scripts/commerce.py stores
    ```

## Structure

- `SKILL.md`: Metadata and instructions for Agent discovery.
- `SERVER_SPEC.md`: Standard API response and behavior specification for backends.
- `scripts/commerce.py`: The universal CLI entry point.
- `scripts/lib/commerce_client.py`: The reusable `BaseCommerceClient` library.

## Security & Privacy

This engine handles user credentials with a narrow, explicit scope:

- **Token-only storage**: Only API tokens are persisted locally. Passwords are used for login or registration and are not written to disk.
- **Per-Domain Isolation**: Each merchant's credentials are stored in a separate subfolder: `~/.openclaw/credentials/agent-commerce-engine/<domain>/`.
- **Access Control**: Stored credential files are restricted to `0600` permissions (owner read/write only).
- **HTTPS Enforced**: The client library rejects non-HTTPS URLs for remote production endpoints. `localhost` and `127.0.0.1` are allowed for local development.
- **Stateless Identity**: Uses header-based authentication instead of browser cookies.

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `python3`  | Runtime |
| `requests` | HTTP client (installable via `pip install requests`) |

No other system dependencies are required. `COMMERCE_URL` and `COMMERCE_BRAND_ID` still exist for backward compatibility, but `--store` is the preferred interface.

## License

MIT License.

---

# 标准 Agentic 商业交互引擎

这是一个面向 Agent 购物场景的标准客户端与服务端规范。它用于把 Agent 与兼容的电商后端连接起来，覆盖商品检索、购物车操作、账户流程和订单创建，并将最终支付交还给用户。

clawhub: https://clawhub.com/NowLoadY/agent-commerce-engine
GitHub: https://github.com/NowLoadY/agent-commerce-engine

## 快速开始

```bash
pip install requests

# 通过 --store 指向任何合规商家
python3 scripts/commerce.py --store https://api.yourstore.com/v1 list

# 查看本地已登录的所有商家
python3 scripts/commerce.py stores
```

## 安全与隐私

- **仅存 Token**：密码仅用于一次性换取 Token，绝不持久化。
- **按域名隔离**：每个商家的凭据存储在独立子文件夹中。
- **权限控制**：凭据文件权限为 `0600`（仅所有者可读写）。
- **强制 HTTPS**：客户端库拒绝远程生产环境的非 HTTPS 地址；本地开发可使用 `localhost` 和 `127.0.0.1`。

## 许可协议

MIT License.
