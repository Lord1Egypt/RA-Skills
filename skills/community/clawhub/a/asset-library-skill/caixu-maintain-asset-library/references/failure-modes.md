# Failure Modes

## Missing library

- 找不到 `library_id` 时，先回到 `list_libraries`
- 不要假设默认库

## Weak patch evidence

- 证据不足时不要 patch
- 可保留 `needs_review`
- 必要时只记录建议，不执行修改

## Wrong asset archived

- 误归档时，优先执行 `restore_asset`
- 不做物理删除

## Empty review queue

- queue 为空不是失败
- 仍可继续查看 overview 或直接查某条资产
