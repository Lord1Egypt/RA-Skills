# File Rules

## Working root
`~/.openclaw/workspace/buyma_order/`

## Directories

- `config/`
- `csv/`
- `orders/incoming/`
- `orders/current/`
- `orders/archive/`
- `templates/`
- `logs/`

## Filename rules

Always:
`tmazonORDERLISTYYMMDD_start-end.xlsx`

Example:
- `tmazonORDERLIST260307_123450-123470.xlsx`

## Base file priority

1. latest file in `orders/incoming/`
2. latest file in `orders/current/`
3. `templates/tmazonORDERLIST_template.xlsx`

## State file

`config/last_state.json`

Track:
- `last_order_number`
- `last_run_date`
- `last_file`
- `last_mail_status`
- `last_mode`
- `last_start_order`
- `last_end_order`
