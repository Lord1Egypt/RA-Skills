# Invoice Use-Case Decision Table

Use this table to select the right invoice template.

| Situation | Template | Why |
|---|---|---|
| Client needs payable estimate before signature | `pro-forma-invoice` | Shows expected charges without assuming final contract state. |
| Deposit requested before kickoff | `deposit-request-invoice` | Generic deposit request when scope is approved. |
| Fixed-scope pilot deposit | `pilot-deposit-invoice` | Matches agentic workflow pilot kickoff. |
| Deposit after signed contract | `contract-deposit-invoice` | References agreement and initial payment. |
| Standalone workflow assessment | `discovery-assessment-invoice` | Bills mapping, risks, and pilot recommendation. |
| Milestone completion | `milestone-invoice` | Ties billing to milestone acceptance. |
| Prototype delivered | `prototype-delivery-invoice` | Bills delivery of the working prototype. |
| Evaluation/test work delivered | `evaluation-work-invoice` | Bills test cases, regression checks, and evaluation plan. |
| Documentation and handoff | `handoff-invoice` | Bills final docs and walkthrough. |
| Final contract balance | `final-balance-invoice` | Summarizes total, prior payments, balance. |
| Hourly consulting or development | `time-and-materials-invoice` | Bills hours and rates. |
| Monthly support | `monthly-retainer-invoice` | Bills ongoing support period. |
| Recurring operations support | `recurring-support-invoice` | Bills repeating managed monitoring/support. |
| Extra workflow or feature | `change-order-invoice` | Requires change-order reference. |
| Rush turnaround | `rush-fee-invoice` | Separates premium fee. |
| Added integration | `integration-add-on-invoice` | Bills connector/tool/data source work. |
| API/model/hosting pass-through | `usage-pass-through-invoice` | Separates third-party charges. |
| Travel or reimbursable expense | `expense-reimbursement-invoice` | Documents reimbursable costs. |
| Support hours over included amount | `support-overage-invoice` | Bills support above retainer or support window. |
| Late fee | `late-fee-invoice` | Use only when allowed and calculated from supplied terms. |
| Payment plan | `installment-invoice` | Bills one installment. |
| Partial payment received | `partial-payment-receipt-invoice` | Shows amount paid and remaining. |
| Client prepaid | `prepayment-credit-invoice` | Records prepayment/credit balance. |
| Discount or courtesy reduction | `discount-adjustment-invoice` | Shows discount transparently. |
| Error in prior invoice | `corrected-invoice` | Replaces or corrects prior invoice. |
| Project terminated midstream | `termination-invoice` | Bills earned work and authorized expenses. |
| Refund owed | `refund-memo` | Documents refund amount and reason. |
| Credit against future work | `credit-memo` | Documents credit balance. |
| Retainer renewal | `retainer-renewal-invoice` | Renews ongoing services. |
| Second workflow after success | `expansion-workflow-invoice` | Bills expansion scope. |
| Training/admin enablement | `training-invoice` | Bills training sessions and materials. |
| Advisory-only engagement | `advisory-invoice` | Bills review, planning, or oversight without build. |
| Holdback release | `holdback-release-invoice` | Bills retained amount after acceptance. |
| Tax adjustment only | `tax-only-invoice` | Adds verified tax correction. |
| Void prior invoice | `voided-invoice-notice` | Tells client not to pay prior invoice. |
| Payment complete | `paid-in-full-receipt` | Confirms no balance remains. |

Selection rule: choose by commercial trigger first, then billing model, then delivery artifact. Never use a final invoice when acceptance is still pending unless the contract bills on delivery rather than acceptance.
