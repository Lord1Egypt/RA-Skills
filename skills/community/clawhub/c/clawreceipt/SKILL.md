---
name: clawreceipt
description: Use this skill to extract receipt information, record expenses, track budgets, and manage financial receipts using the ClawReceipt CLI.
---

# ClawReceipt Skill for OpenClaw

Use this skill to interface with the ClawReceipt system whenever the user wants to process a receipt, check their monthly spending budget, or export financial data.

## Trigger Conditions

Use this skill when the user wants to:

- Upload or provide a picture/text of a receipt to be recorded.
- Add a new expense, bill, or receipt to the database.
- Check their current total spend against their monthly budget.
- Update their monthly spending budget.
- List recent receipts/expenses.

## Core Workflows

### 1) Process and Add a Receipt

When the user provides a receipt image or details, extract the relevant fields (Date, Time, Store, Amount, Category) and use the CLI to save it:

1. Extract details using OCR or LLM vision capabilities.
2. Ensure you have `date` (YYYY-MM-DD), `time` (HH:MM:SS, optional), `store` (string), `amount` (float), and `category` (string, e.g., "อาหาร", "เดินทาง", "Shopping").
3. Run the CLI command in the ClawReceipt directory:

   ```bash
   python run.py add --date "YYYY-MM-DD" --time "HH:MM:SS" --store "<Store>" --amount <Amount> --category "<Category>"
   ```

4. Read the output to check if the budget was exceeded and relay that information to the user.

### 2) Check Budget Status

If the user asks "How much budget do I have left?" or "What is my total spend?":

1. Run:

   ```bash
   python run.py budget
   ```

2. Parse the output which includes "Total Spent" and "Target Budget" and accurately report to the user.
3. Alert the user if the status indicates "Exceeded Budget!".

### 3) Set New Budget

If the user wants to set a new monthly budget (e.g., "Set my budget to 5000 baht"):

1. Run:

   ```bash
   python run.py budget --set <Amount>
   ```

2. Confirm to the user that the budget has been updated successfully.

### 4) List All Receipts

If the user asks to see history or recently recorded receipts:

1. Run:

   ```bash
   python run.py list
   ```

2. Summarize the output table for the user.

### 5) Open TUI / Export (Interactive mode only)

If the user asks to see a beautiful dashboard or export to CSV/Excel, you can suggest they run:

```bash
python run.py tui
```

*(Note: As an agent, do not run the `tui` command directly as it will block the terminal. Instruct the user to run it themselves in a new terminal if they want to interact with the UI or manually export the data).*

## Required Checks Before Execution

- Verify `run.py` is present in the ClawReceipt root folder before calling.
- Ensure the active Python environment has the required dependencies (`rich`, `pandas`, `openpyxl`, `textual`, etc.) by utilizing `.\venv\Scripts\activate` if available.
- Always quote string arguments like `--store "Full Name"` to prevent shell argument splitting.

## Troubleshooting

- `UnicodeEncodeError`: Ensure the terminal is using UTF-8 encoding. The `run.py` handles this internally for Windows, but be aware if piping output.
- `unrecognized arguments`: Ensure parameters like `--category` are explicitly mapped and don't contain unescaped quotes.

## Completion Checklist

- Required fields accurately extracted and fed to the `add` command.
- Command executed successfully (exit code 0).
- Relevant confirmation (and budget alerts, if any) relayed back to the user clearly.
