# 统一要求

## 名称身份

- 正式名称对标 slug。
- 必须是短横线连接的小写英文与数字。
- 展示名称对标 display name。
- 展示名称长度不得超过 20 个字符。
- 进入 render 前必须完成 `cocoloop` 与 `clawhub` 双源去重。

## 视觉输出

- 只要任务包含任何可视化输出，就把判断写入 `output_profile.has_visual_output: true`。
- `output_profile.has_visual_output: true` 时，必须同步启用 `design_md`。
- `output_profile.has_visual_output: true` 时，最终产物必须包含 `references/design.md` 与 `references/design-md/`。

## 校验口径

- spec validator 负责校验新字段是否完整。
- render builder 负责把名称和视觉输出要求落进最终产物。
- 平台 manifest 负责继续使用规范后的 slug 与 display name。
