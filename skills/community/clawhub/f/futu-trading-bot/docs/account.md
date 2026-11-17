# Account Manager 文档

所属项目：**Futu Trade Bot Skills**

## 模块位置
`src/account_manager.py`

## 安全提示
- `unlock_trade` / `lock_trade` 会改变真实券商账户的交易锁定状态，**必须** `confirm=True`，且仅在用户明确授权后调用。
- 不要通过 agent stdin 收集交易密码；优先使用配置中的 `trade_password_md5`。
- `get_account_info` 默认**不写盘**。仅当用户要求缓存账户列表时使用 `persist=True`（写入 `json/account_info.json`，含账户 ID / 环境 / 券商等元数据，请限制文件权限且勿提交仓库）。

## 对外接口

### `get_account_info(persist=False)`
```python
get_account_info(persist: bool = False) -> Dict[str, Any]
```

行为：
- 调用富途 `get_acc_list()`。
- 返回账户列表结构：`accounts`。
- 仅当 `persist=True` 时覆盖写 `json/account_info.json`，并在结果中设置 `persisted=True/False`。

### `unlock_trade(password=None, password_md5=None, confirm=False)`
```python
unlock_trade(
    password: Optional[str] = None,
    password_md5: Optional[str] = None,
    confirm: bool = False,
) -> Dict[str, Any]
```

- `confirm` 必须为 `True`，否则直接失败。
- 密码优先级：显式 `password_md5` → 显式 `password` → 配置 `trade_password_md5` → 配置 `trade_password`。

### `lock_trade(password=None, password_md5=None, confirm=False)`
同样需要 `confirm=True`。内部调用富途 `unlock_trade(..., is_unlock=False)`。

## 使用示例
```python
from account_manager import get_account_info, unlock_trade, lock_trade

print(get_account_info())
print(unlock_trade(confirm=True))
print(lock_trade(confirm=True))
```

## 注意事项
- 依赖 OpenD 连接可用。
- 明文密码和 MD5 都属于敏感信息。
- 对外函数返回后会关闭账户相关 context。
