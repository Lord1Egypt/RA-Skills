# Publish Notes / 发布说明

## Required publish discipline

1. Do not trust `发布成功` text alone
2. After publish, always check creator manage page
3. Confirm the new work appears with:
   - expected timestamp
   - expected duration
   - expected title snippet

## AI declaration

Validated operator guidance from real usage:

- Right panel: `发文助手`
- Enter: `自主声明`
- Click: `添加声明`
- Choose: `内容由AI生成`

If automation fails to find these elements:
- report honestly that publish may still succeed but AI declaration is not verified
- treat declaration support as incomplete until logs explicitly confirm clicks

## Current known behavior

- Multi-shot pipeline is validated
- Douyin publish + backend verification is validated
- AI declaration path was identified by human feedback and added to script logic
- If logs do not explicitly show successful declaration clicks, do not claim it succeeded

## Recommended result format

When finishing a run, report:
- local output folder
- final mp4 path
- publish title
- backend verification result
- whether AI declaration was explicitly verified
