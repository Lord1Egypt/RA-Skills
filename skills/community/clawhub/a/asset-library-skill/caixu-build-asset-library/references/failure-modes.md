# Failure Modes

## binary_only

- `binary_only` 不能直接生成 `asset_card`
- 除非上游已有可信文本补充，否则跳过并发出 warning

## Low confidence extraction

- 允许保留 `null`
- 允许 lower confidence
- 不允许为了“成功率”虚构关键字段
- 不允许输出 `"unknown"`
- 明显脏值如截断 issuer、正文片段 holder、非日期格式日期，应置空或跳过

## Merge uncertainty

- 同名文件不等于同一材料
- 无法确认时保持 `merged_assets = []` 或保留 `unmerged`
- 归并失败不应抹掉已写入的 `asset_card`
- 公示/名单类和团队材料默认不归并

## Triage exclusion

- triage 判定为 `noise`、`resume_only` 或非材料文件时，应跳过
- 被排除文件必须给出原因
- 跳过不是失败，但不能继续伪造 `asset_card`
- 公示/名单类若不能唯一映射到 owner，应排除
- 团队/多人材料若无法明确 owner 参与，应排除

## Triage fallback

- 如果 `document_triage` 因 reasoning-only、timeout、rate limit 之类可恢复错误失败，pipeline 可以保守放行到 `asset_extraction`
- 这类 fallback 必须记录为 warning / audit，且 `document_role_hint` 应为 `null`
- fallback 只意味着“允许进入下一步抽取”，不代表已经确认应进入最终资产库
