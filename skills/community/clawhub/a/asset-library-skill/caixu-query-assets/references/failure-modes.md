# Failure Modes

## Empty result

- 可以是 `success`
- `asset_cards = []`
- `merged_assets = []`
- 不伪造命中

## Empty library

- 若尚无 `asset_card`，提示先执行 `build-asset-library`
- 不把“未建库”当成“查询为空”

## Storage unavailable

- SQLite 或本地库不可用时返回结构化错误
- 不要降级成空数组
