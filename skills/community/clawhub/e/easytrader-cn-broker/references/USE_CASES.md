# Known Use Cases (KUC)

Total: **4**

## `KUC-101`
**Source**: `easytrader/server.py`

Provides HTTP REST API endpoints for broker authentication and retrieving account balance information programmatically, enabling integration with external trading systems.

## `KUC-102`
**Source**: `tests/test_xqtrader.py`

Unit test that validates XueQiuTrader correctly handles account preparation with required parameters (cookies) and properly stores portfolio configuration.

## `KUC-103`
**Source**: `tests/test_easytrader.py`

Integration tests for YunHui (yh_client) broker trading operations including balance queries, today's trades/entrusts, and entrust cancellation functionality.

## `KUC-104`
**Source**: `tests/test_xq_follower.py`

Unit tests for XueQiuFollower that verify transaction projection and sell amount adjustment logic for portfolio mirroring operations.
