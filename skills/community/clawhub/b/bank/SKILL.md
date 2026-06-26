---
name: bank
description: >
  Complete personal and business banking intelligence system. Trigger whenever someone needs
  to optimize their banking setup, choose the right accounts, reduce fees, maximize interest,
  navigate banking products, resolve disputes with their bank, understand banking services,
  or build a banking structure that actually works for their financial life. Also triggers on
  phrases like "best bank account", "my bank charged me", "should I switch banks", "how do I
  set up business banking", "what is a SWIFT transfer", or any scenario involving the
  relationship between a person and the institutions that hold their money.
---

# Bank — Complete Banking Intelligence System

## What This Skill Does

Most people have the same bank account they opened as a teenager or young adult. They have
never seriously evaluated whether it is the right account for their current life. They pay
fees they do not need to pay, earn interest rates that round to zero when better rates are
available, and use products that were sold to them rather than chosen by them.

Banking is infrastructure. Bad infrastructure is invisible until it fails or costs you money.
This skill makes your banking infrastructure deliberate.

---

## Core Principle

A bank is not a relationship. It is a vendor. You are paying for services — either explicitly
in fees or implicitly in the spread between what they earn on your money and what they pay
you for it. The customer who evaluates banking decisions with this clarity consistently gets
better terms, pays less, and earns more than the customer who treats banking as a loyalty
relationship.

---

## Workflow

### Step 1: Assess the Banking Scenario
```
BANKING_SCENARIOS = {
  "account_optimization": {
    "goal":    "Ensure current accounts are the best available for actual usage patterns",
    "review":  ["Monthly fees paid", "Interest earned", "Features used vs available",
                "ATM costs", "Transfer fees"],
    "trigger": "Any time fees exceed $10/month or interest rate is below current HYSA rates"
  },
  "account_selection": {
    "goal":    "Choose the right account type for specific purpose",
    "types":   ["checking", "savings", "HYSA", "money_market", "CD", "business_checking"],
    "key":     "Match account features to actual usage — not to what sounds good"
  },
  "dispute_resolution": {
    "goal":    "Recover fees, resolve errors, escalate unresolved issues",
    "process": ["Direct request", "Formal complaint", "Regulatory escalation"],
    "success": "Most fee reversals are granted to customers who ask specifically"
  },
  "business_banking": {
    "goal":    "Separate business finances, build banking relationships, access credit",
    "needs":   ["Business checking", "merchant services", "business credit", "payroll"],
    "key":     "Business banking affects how lenders evaluate you — build it deliberately"
  },
  "international": {
    "goal":    "Minimize costs on cross-border transactions",
    "products": ["Multi-currency accounts", "international wires", "foreign ATM access"],
    "key":     "Traditional bank international fees are 3-5x what specialized providers charge"
  }
}
```

### Step 2: Account Architecture

The right banking structure separates money by purpose and ensures each dollar is held
in the account type that best serves its function.
```
ACCOUNT_ARCHITECTURE = {
  "checking": {
    "purpose":     "Daily transactions — bills, purchases, transfers",
    "what_matters": ["No monthly fee or easily waived", "ATM network or reimbursement",
                     "Mobile deposit", "Zelle or instant transfer"],
    "what_not_to_optimize_for": "Interest rate — checking balances should be minimal",
    "target_balance": "1-2 months of expenses — enough to avoid overdraft, not more"
  },

  "high_yield_savings": {
    "purpose":     "Emergency fund and short-term savings goals",
    "what_matters": ["APY as close to Fed Funds rate as possible",
                     "FDIC insured", "No minimum balance fee", "Easy transfer to checking"],
    "where_to_find": "Online banks consistently offer 4-5x the rate of traditional banks",
    "rate_reality": """
      Traditional big bank savings:  0.01% - 0.10% APY
      Online HYSA:                   4.50% - 5.25% APY
      Difference on $20,000:         $880 - $1,040 per year
      # This is free money left on the table by staying at traditional bank
    """
  },

  "money_market": {
    "purpose":     "Larger balances needing liquidity and higher rates",
    "vs_HYSA":     "Similar rates, often higher minimums, check-writing ability",
    "best_for":    "Balances over $50K where check-writing access has value"
  },

  "certificates_of_deposit": {
    "purpose":     "Fixed-rate return on money not needed for defined period",
    "CD_ladder":   """
      def build_cd_ladder(total_amount, num_rungs=5):
          rung_amount = total_amount / num_rungs
          ladder = []
          for months in [3, 6, 12, 18, 24]:
              ladder.append({
                  "amount": rung_amount,
                  "term": months,
                  "rate": get_best_cd_rate(months),
                  "maturity": today + timedelta(months=months)
              })
          # One CD matures every few months = liquidity + rate optimization
          return ladder
    """,
    "early_withdrawal": "Penalty typically 90-180 days interest — know before locking in"
  },

  "business_checking": {
    "purpose":     "Separate business and personal finances — legally and practically essential",
    "what_matters": ["Transaction volume limits", "Cash deposit ability if needed",
                     "Integration with accounting software", "ACH and wire capabilities"],
    "separate_immediately": "Commingling personal and business funds creates legal and tax problems"
  }
}
```

### Step 3: Fee Elimination
```
FEE_AUDIT = {
  "common_fees": {
    "monthly_maintenance": {
      "typical":    "$12-$25/month",
      "eliminate":  "Minimum balance requirement, direct deposit, or switch to fee-free bank",
      "ask":        "Call and request waiver — retention teams have authority to waive"
    },
    "overdraft": {
      "typical":    "$25-$35 per occurrence",
      "eliminate":  "Link savings as overdraft protection, opt out of overdraft coverage,
                     maintain buffer balance",
      "dispute":    "First-time overdraft fees are almost always reversed if you ask"
    },
    "ATM": {
      "typical":    "$2.50-$5 per transaction plus out-of-network fee",
      "eliminate":  "Choose bank with ATM reimbursement (Schwab refunds all ATM fees globally),
                     use cash back at grocery stores instead of ATM"
    },
    "wire_transfer": {
      "typical":    "$15-$35 domestic, $25-$50 international",
      "eliminate":  "ACH for domestic transfers, Wise or similar for international"
    },
    "paper_statement": {
      "typical":    "$2-$5/month",
      "eliminate":  "Enroll in paperless — takes 30 seconds"
    }
  },

  "fee_reversal_script": {
    "context":  "Works for most one-time fees from accounts in good standing",
    "script":   "Hi, I noticed a [fee type] of [amount] on my account on [date].
                 I have been a customer for [X years] and have not had this issue before.
                 I would like to request a reversal of this fee.",
    "success_rate": "Overdraft and monthly fee reversals succeed 70-80% of the time
                     for customers who ask once, politely, on a first occurrence"
  }
}
```

### Step 4: Interest Rate Optimization
```
RATE_OPTIMIZATION = {
  "savings_rate_audit": """
    def calculate_opportunity_cost(current_balance, current_apy, market_apy):
        annual_difference = current_balance * (market_apy - current_apy)
        monthly_difference = annual_difference / 12
        return {
            "annual_cost_of_staying": annual_difference,
            "monthly_cost_of_staying": monthly_difference,
            "5_year_compound_cost": current_balance * ((1 + market_apy)**5 - (1 + current_apy)**5)
        }

    # Example: $30,000 at 0.05% vs 5.00%
    # Annual difference: $1,485
    # 5-year compound difference: $8,200+
  """,

  "negotiating_rates": {
    "savings":  "Rarely negotiable at banks — switch to get better rate",
    "CD":       "Relationship pricing available at credit unions for large deposits",
    "mortgage": "Always negotiable — rate is a starting point not a final offer",
    "HELOC":    "Spread over prime is negotiable especially with strong credit",
    "credit_card": "APR reduction requests succeed 50%+ of the time for on-time payers"
  }
}
```

### Step 5: International Banking
```
INTERNATIONAL_FRAMEWORK = {
  "wire_transfers": {
    "SWIFT":      "Traditional international wire — $25-50 fee, 1-5 business days, exchange rate markup",
    "SEPA":       "European transfers — cheaper within EU, typically next day",
    "alternatives": {
      "Wise":     "Mid-market exchange rate, low fixed fee — typically 70-80% cheaper than banks",
      "Revolut":  "Multi-currency account, interbank rate up to monthly limit",
      "Payoneer": "Business-focused, good for receiving international payments"
    },
    "comparison": """
      Sending $10,000 USD to EUR:
      Traditional bank:  $35 fee + 3% exchange markup = ~$335 total cost
      Wise:              $45 fee + 0.5% = ~$95 total cost
      Savings:           $240 on a single transfer
    """
  },

  "foreign_ATM": {
    "best_option":  "Schwab Bank checking — reimburses all ATM fees worldwide, no foreign transaction fee",
    "avoid":        "Dynamic currency conversion — always choose local currency when asked"
  },

  "multi_currency_accounts": {
    "when_needed":  "Regular transactions in multiple currencies",
    "options":      ["Wise multi-currency account", "Revolut", "HSBC Premier for high-balance customers"],
    "benefit":      "Hold and convert currencies when rate is favorable rather than at point of transaction"
  }
}
```

### Step 6: Banking Disputes
```
DISPUTE_FRAMEWORK = {
  "unauthorized_transactions": {
    "timeline":     "Report within 2 business days for maximum protection under Reg E",
    "protection":   "Federal law limits liability to $50 if reported within 2 days,
                     $500 within 60 days",
    "process":      ["Call immediately to freeze card",
                     "File dispute in writing",
                     "Bank has 10 business days to investigate",
                     "Provisional credit typically issued within 5 days"]
  },

  "bank_error": {
    "documentation": "Screenshot or print the error before it is corrected",
    "process":       "Written complaint with account number, date, amount, description",
    "escalation":    "CFPB complaint if bank does not resolve within 60 days"
  },

  "regulatory_escalation": {
    "CFPB":         "Consumer Financial Protection Bureau — most powerful for US bank complaints",
    "OCC":          "For national banks (Chase, BofA, Wells Fargo)",
    "FDIC":         "For state-chartered banks",
    "effect":       "Regulatory complaints trigger formal response requirements.
                     Banks resolve CFPB complaints at much higher rates than internal complaints."
  }
}
```

---

## Banking Product Reference
```
PRODUCT_GUIDE = {
  "checking":          "Daily transactions. Optimize for: no fees, ATM access, transfer speed.",
  "savings":           "Short-term storage. Optimize for: APY, no minimums.",
  "HYSA":              "Emergency fund. Optimize for: highest APY, FDIC insurance.",
  "money_market":      "Larger liquid balances. Optimize for: APY, check writing.",
  "CD":                "Committed savings. Optimize for: APY, term matching your timeline.",
  "business_checking": "Business separation. Optimize for: transaction limits, integrations.",
  "HSA":               "Healthcare savings. Triple tax advantage — maximize if eligible.",
  "brokerage":         "Not a bank product but where idle cash above emergency fund belongs."
}
```

---

## Quality Check Before Delivering

- [ ] Current account fees identified and elimination options provided
- [ ] Interest rate opportunity cost calculated if savings at traditional bank
- [ ] Account architecture matched to user's actual financial structure
- [ ] Fee reversal script provided if relevant
- [ ] International transfer alternatives provided if cross-border scenario
- [ ] Dispute process specific to transaction type and timeline
- [ ] Regulatory escalation path provided for unresolved disputes
- [ ] Jurisdiction noted — banking regulations vary by country
