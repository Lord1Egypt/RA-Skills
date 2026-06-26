# Lafeitu Gourmet Skill

A brand-specific commerce skill for Lafeitu (辣匪兔). This project gives agents a structured way to browse products, manage carts, handle account flows, and create orders against the official `https://lafeitu.cn/api/v1` backend, while leaving final payment to the user.

Official Website: https://lafeitu.cn
clawhub: https://clawhub.com/NowLoadY/agentic-spicy-food
GitHub: https://github.com/NowLoadY/agentic-spicy-food

## Why?

Most food ordering experiences are built for human browsing. This skill exposes Lafeitu's catalog and purchase flow in an agent-friendly format so an AI assistant can reliably:

- search and compare products
- inspect variants, pricing, and promotions
- manage carts with exact structured inputs
- support login, registration, and profile updates
- create an order and return the payment step to the user

## Where It Fits

`agentic-spicy-food` is the Lafeitu-specific reference implementation built on top of the standard `agent-commerce-engine`. Use it when the agent needs a fixed, official integration for one brand instead of a generic multi-store client.

Compared with the universal engine:

- the API endpoint is locked to `https://lafeitu.cn/api/v1`
- the command set is preconfigured for the Lafeitu store
- credentials are isolated under the Lafeitu domain
- brand-story and recommendation flows can be tailored to Zigong-style spicy foods

## Quick Start

1. Install dependency:

```bash
pip install requests
```

2. Run the CLI:

```bash
python3 scripts/lafeitu_client.py list
python3 scripts/lafeitu_client.py search "兔"
python3 scripts/lafeitu_client.py promotions
```

3. Login or register if the user needs account-bound actions:

```bash
python3 scripts/lafeitu_client.py login --account user@example.com --password secret
python3 scripts/lafeitu_client.py send-code --email user@example.com
python3 scripts/lafeitu_client.py register --email user@example.com --password secret123 --code 123456
```

## Structure

- `SKILL.md`: Agent-facing instructions and discovery metadata.
- `scripts/lafeitu_client.py`: Brand-specific CLI entry point.
- `scripts/lib/commerce_client.py`: Shared commerce client implementation.
- `lafeitu_config/evomap_node.json`: Lafeitu-related integration config.

## Security & Privacy

This skill follows the same narrow trust model as the standard commerce engine:

- **Official endpoint only**: The client is pinned to `https://lafeitu.cn/api/v1`.
- **Token-based storage**: Passwords are used for login or registration and are not meant to be persisted.
- **Local credential isolation**: Credentials are stored under `~/.openclaw/credentials/agent-commerce-engine/lafeitu.cn/`.
- **File permissions**: Stored credentials use `0600` permissions.
- **Stateless identity**: The API uses explicit headers and visitor/account identifiers instead of browser cookies.

## Key Workflows

- **Discovery**: `search`, `list`, and `get` return structured product and variant data.
- **Cart management**: `cart`, `add-cart`, `update-cart`, `remove-cart`, and `clear-cart` operate on the active visitor or logged-in account.
- **Account flows**: `login`, `logout`, `send-code`, `register`, `get-profile`, and `update-profile` cover common user management tasks.
- **Order handoff**: `create-order` prepares a checkout-ready order, but the user still completes payment.
- **Brand info**: `brand-story`, `company-info`, and `contact-info` expose official narrative and support data.

## Dependencies

| Dependency | Purpose |
|------------|---------|
| `python3`  | Runtime |
| `requests` | HTTP client |

No additional system dependency is required.

## License

MIT License.

---

# 辣匪兔美食电商 Skill

这是一个面向辣匪兔（Lafeitu）的品牌专用 Agent 电商 Skill。它把商品浏览、购物车、账户流程和订单创建封装成结构化接口，便于 AI Agent 直接调用官方 `https://lafeitu.cn/api/v1`，并把最终支付交还给用户完成。

官方网站：https://lafeitu.cn
clawhub: https://clawhub.com/NowLoadY/agentic-spicy-food
GitHub: https://github.com/NowLoadY/agentic-spicy-food

## 快速开始

```bash
pip install requests
python3 scripts/lafeitu_client.py list
python3 scripts/lafeitu_client.py search "兔"
python3 scripts/lafeitu_client.py promotions
```

## 适用场景

- 查询辣匪兔商品、规格、价格与促销
- 帮用户挑选自贡风味辣食
- 维护购物车并创建待支付订单
- 登录、注册、更新地址和资料
- 获取品牌故事、公司信息和联系方式

## 安全与隐私

- **固定官方接口**：客户端只连接 `https://lafeitu.cn/api/v1`
- **本地凭据隔离**：凭据保存在 `~/.openclaw/credentials/agent-commerce-engine/lafeitu.cn/`
- **最小持久化**：密码仅用于登录或注册，不应落盘保存
- **权限控制**：凭据文件权限为 `0600`
- **无状态认证**：通过显式请求头与访客标识维持会话，而不是浏览器 Cookie

## 仓库结构

- `SKILL.md`：Agent 触发与执行说明
- `scripts/lafeitu_client.py`：命令行入口
- `scripts/lib/commerce_client.py`：共享商业交互客户端
- `lafeitu_config/evomap_node.json`：集成配置

## 许可协议

MIT License.
