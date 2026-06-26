# Failure Rules

## Immediate stop conditions

- BUYMA access failure
- CSV download failure without fallback CSV
- Mail send failure

## Required response

Stop the run immediately and notify via Telegram.

Failure text format:
`BUYMA 자동화 실패 / 단계: {stage} / 파일 첨부`

## Telegram fallback

- Send failure summary
- Attach output file if it exists
- Include run mode and target range if known

## CSV download failure

- If operator later provides a BUYMA CSV file, resume using that file
- Mark run as `resumed-from-manual-csv` in logs/state

## Mail send failure

- Notify via Telegram immediately
- Attach output workbook in Telegram
- Preserve workbook in `orders/current/`
