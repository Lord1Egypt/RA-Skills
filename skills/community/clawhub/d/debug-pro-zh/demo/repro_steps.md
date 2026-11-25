# 复现步骤（订单接口 500）

1. 环境：Windows 11 22H2 / Python 3.11.4 / 依赖按 requirements.txt（fastapi 0.110.0、orjson 3.10.0）
2. 命令：`python -m uvicorn app.main:app --port 8080`
3. 输入：`POST /api/v1/orders`，body 取 `fixtures/order_empty.json`（内容为空文件）
4. 期望：返回 200 与订单号；实际：返回 500，且日志出现 JSONDecodeError
5. 证据：日志见 `sample_error.txt`，栈首帧 `orders.py:88`，退出码 1
