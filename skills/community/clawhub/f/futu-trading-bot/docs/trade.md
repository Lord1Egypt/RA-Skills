# Trade Service 文档

所属项目：**Futu Trade Bot Skills**

## 模块位置
`src/trade_service.py`

## 概述
交易模块负责下单、改单、撤单与全部撤单，内部包含参数校验和富途 API 调用。

## 安全门闩
- 推荐默认：`trd_env="SIMULATE"`。
- `submit_order` / `modify_order` / `cancel_order`：当 `trd_env="REAL"` 时必须 `confirm=True`。
- `cancel_all_orders`：**任何环境**都必须 `confirm=True`（高 blast radius）。
- 缺少确认时函数返回 `success=False` 与说明信息，不会调用富途下单接口。

## 设计原则
- 交易环境不做内部管理，调用方必须显式传入。
- 不提供账户环境切换接口（无 `switch_account_env`）。
- 不做幂等去重校验。

## 对外接口

### `submit_order(...)`
```python
submit_order(
    code: str,
    side: str,
    qty: int,
    acc_id: int,
    trd_env: str,
    price: Optional[float] = None,
    order_type: str = "NORMAL",
    aux_price: Optional[float] = None,
    remark: Optional[str] = None,
    time_in_force: str = "DAY",
    confirm: bool = False,
) -> Dict[str, Any]
```

### `modify_order(...)` / `cancel_order(...)`
`REAL` 需要 `confirm=True`。

### `cancel_all_orders(...)`
```python
cancel_all_orders(trd_env: str, acc_id: int = 0, trdmarket: Optional[str] = None, confirm: bool = False)
```
必须 `confirm=True`。

## 使用示例
```python
from trade_service import submit_order, cancel_all_orders

result = submit_order(
    code="HK.00700",
    side="BUY",
    qty=200,
    acc_id=6017237,
    trd_env="SIMULATE",
    price=150,
    order_type="NORMAL",
)
print(result)

# cancel_all_orders(trd_env="SIMULATE", acc_id=6017237, confirm=True)
```

## 注意事项
- `REAL` 环境会尝试真实交易，请先确认交易权限状态。
- 真实交易密码解锁/锁定由 `account_manager` 处理，不在本模块内自动完成。
