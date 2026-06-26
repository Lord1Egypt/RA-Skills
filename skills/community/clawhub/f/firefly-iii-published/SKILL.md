# Firefly III Client Skill

## Purpose
A production-ready client for Firefly III personal finance management, allowing for programmatic access to transactions, accounts, recurring rules, and automation.

## Security Considerations
See `SECURITY.md` for information on token safety, environment variables, and network security when using this skill.

## Setup
1. Ensure Firefly III is running and you have an OAuth Personal Access Token.
2. Set the following environment variables:
   ```bash
   FIREFLY_URL=http://your-instance-url
   FIREFLY_TOKEN=your_personal_access_token
   ```
3. Install dependencies:
   ```bash
   pip install requests
   ```

## CLI Reference
The `api.py` script serves as a generic wrapper for the Firefly III REST API.

- `python3 api.py request <METHOD> <ENDPOINT> [-d <JSON_DATA>]`

### Examples
- **List Accounts:** 
  `python3 api.py request GET api/v1/accounts`
  
- **Create Transaction:** 
  `python3 api.py request POST api/v1/transactions -d '{"amount": "10.00", "description": "Coffee", "source_id": 1, "destination_id": 2, "date": "2026-04-06", "type": "withdrawal"}'`
  
- **Create Recurring Transaction:** 
  `python3 api.py request POST api/v1/recurrences -d '{"type": "withdrawal", "title": "Example", "first_date": "2026-04-30", "repeat_freq": "monthly", "nr_of_repetitions": 12, "repetitions": [{"type": "monthly", "moment": "30"}], "transactions": [{"description": "Item", "amount": "100.00", "source_id": 1, "destination_id": 2}]}'`
  
- **Create Rule:** 
  `python3 api.py request POST api/v1/rules -d '{"title": "Example Rule", "trigger": "destination_account_is", "value": "Netflix", "action": "link_to_bill", "action_value": "Netflix Bill"}'`
