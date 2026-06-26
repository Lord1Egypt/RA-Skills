# Tool Contracts

## Required objects

- `LibraryOverview`
- `ReviewQueueData`
- `PatchAssetCardData`

## Overview expectations

- `get_library_overview` 必须返回：
  - `library_id`
  - `counts.assets_total`
  - `counts.needs_review_assets`
  - `last_ingest_at`
  - `last_build_at`

## Review queue expectations

- `list_review_queue` 只返回 `active + needs_review` 资产
- review queue 是维护入口，不代表只能维护 queue 内资产

## Patch expectations

- `patch_asset_card` 只修改显式给出的字段
- patch 后资产默认进入 `reviewed`
- `change_event` 必须保留 action 和 changed_fields

## Archive / restore expectations

- `archive_asset` 把资产改成 `asset_state = archived`
- `restore_asset` 把资产改成 `asset_state = active`
- 这两个动作都必须返回更新后的 `asset_card` 和 `change_event`

## Query expectations

- 默认查询只消费 `active` 资产
- 维护完成后应用 `query_assets` 验证变更是否立即生效
