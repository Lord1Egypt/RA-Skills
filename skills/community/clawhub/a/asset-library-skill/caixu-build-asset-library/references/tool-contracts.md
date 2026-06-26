# Tool Contracts

## Required objects

- `BuildAssetLibraryData`
- `asset_card`
- `merged_asset`
- `pipeline_run`

## Required output fields

- `data.library_id`
- `data.asset_cards`
- `data.merged_assets`
- `data.summary.total_assets`
- `data.summary.merged_groups`
- `data.summary.anomalies`
- `data.summary.unmerged_assets`

## Pipeline persistence

- 标准执行路径先创建 `build_asset_library` 的 `pipeline_run`
- 每个 batch / persist 阶段追加 `append_pipeline_step`
- 成功、partial、failed 都必须调用 `complete_pipeline_run`

## Document triage categories

- `personal_proof`
  适用于明确归属于 owner 的个人证书、证明、成绩单、个人荣誉
- `personal_experience`
  适用于简历、个人经历证明、任职证明、项目经历证明
- `public_notice`
  适用于公示、名单、公告等公共材料；只有能唯一映射到 owner 时才允许进入资产库
- `team_notice`
  适用于团队/多人通报、团队荣誉、喜报类材料；只有能明确 owner 参与时才允许进入资产库
- `reference_only`
  适用于只提供背景佐证、不能单独当正式个人材料的文件
- `noise`
  非材料资产、宣传海报、无关文件

## Personal library inclusion rules

- 这是单人个人资产库，不要把公共名单、团队通报默认写成个人资产
- owner 只可从高置信个人材料推断：简历、明确单人证书/成绩单/个人荣誉
- 公示/名单类只有在能保守映射到 owner 时才生成 `asset_card`
- 团队/多人材料只有在能明确判断 owner 参与时才生成 `asset_card`
- 无法保守归属到 owner 时，宁可跳过建卡

## asset_card constraints

- `library_id` 必填
- `asset_id` 应稳定，优先由 `library_id + file_id` 推导
- `material_type` 只允许：`proof | experience | rights | finance | agreement`
- `source_files` 必须保留原始 `file_id`、`file_name`、`mime_type`
- `confidence` 保守，不要伪造高值
- `holder_name`、`issuer_name`、`issue_date` 不确定时返回 `null`
- 不要输出 `"unknown"`
- 单个文件最多产出一个最终 `asset_card`，除非显式说明拆分原因

## Asset extraction defaults

- `schema_version` 固定返回 `"1.0"`
- `library_id` 直接复制输入里的 `library_id`
- `source_files` 直接复制当前文件的 `file_id`、`file_name`、`mime_type`
- `validity_status` 没有明确有效期证据时返回 `unknown`
- `sensitivity_level` 必填，默认保守填写
  - `finance` / `agreement` 优先 `high`
  - `proof` / `experience` / `rights` 优先 `medium`
- `title` 必填，用保守短标题，不要留空
- `normalized_summary` 必填，用 1 句保守摘要，不要留空

## Document category handling

- 简历类材料：
  - `material_type = experience`
  - `issuer_name = null`
  - `issue_date = null`
  - `expiry_date = null`
- 公示/名单类若仍允许进入资产库：
  - `holder_name` 必须能明确映射到 owner
  - `normalized_summary` 必须明确写出“公示/名单类佐证”，而不是正式签发证书
  - `confidence` 保持保守
- 团队/多人材料：
  - 不允许把整支团队名直接写成 `holder_name`
  - 若能识别 owner 参与，优先收敛到 owner；否则置空或跳过

## merged_asset constraints

- 不删除 raw `asset_card`
- `selected_asset_id` 必须指向真实资产
- `status` 只在有充分证据时设为 `merged`
