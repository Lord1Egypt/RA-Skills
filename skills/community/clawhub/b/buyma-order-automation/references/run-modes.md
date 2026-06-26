# Run Modes

## Regular daily run

Purpose:
- Process newly available orders
- Guarantee mail sending by 08:30
- Include all orders up to 07:00 without fail
- Include as many orders from 07:00 to 08:00 as feasible while still guaranteeing mail before 08:30

Behavior:
- Start at any practical time before deadline
- Use the last known delivered workbook state
- Continue from the latest valid base workbook
- Always perform memo check/input for target orders
- Do not use an artificially early cutoff such as 01:00
- Use a dynamic practical cutoff close enough to the deadline to still finish save and mail send
- Stop immediately on BUYMA access failure, CSV failure, or mail failure
- Notify via Telegram with file attachment if output exists

## Ad hoc range run

Trigger:
- Operator asks for a specific order-number range
- Example: 123450~123470

Behavior:
- Use the specified range only
- Always perform memo check/input for that range
- Build workbook immediately
- Notify completion by Telegram
- Send mail immediately
- Filename must include date and range
