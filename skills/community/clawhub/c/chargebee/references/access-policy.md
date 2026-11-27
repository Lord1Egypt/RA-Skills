# Chargebee access policy

An access policy limits which endpoints Chargebee connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/chargebee#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Chargebee: its 184 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create chargebee --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "api/v2/addons"},
    {"method": "GET", "path": "api/v2/addons/{id}"},
    {"method": "GET", "path": "api/v2/addresses"},
    {"method": "GET", "path": "api/v2/alerts"},
    {"method": "GET", "path": "api/v2/alerts/{id}"},
    {"method": "GET", "path": "api/v2/alerts/{id}/alert_statuses"},
    {"method": "GET", "path": "api/v2/attached_items/{id}"},
    {"method": "GET", "path": "api/v2/business_entities"},
    {"method": "GET", "path": "api/v2/business_entities/transfers"},
    {"method": "GET", "path": "api/v2/business_entities/{id}"},
    {"method": "GET", "path": "api/v2/business_rules"},
    {"method": "GET", "path": "api/v2/business_rules/{id}"},
    {"method": "GET", "path": "api/v2/business_rules/{id}/draft"},
    {"method": "GET", "path": "api/v2/business_rulesets"},
    {"method": "GET", "path": "api/v2/business_rulesets/{id}"},
    {"method": "GET", "path": "api/v2/business_rulesets/{id}/rules"},
    {"method": "GET", "path": "api/v2/cards/{id}"},
    {"method": "GET", "path": "api/v2/collections_payment_promises"},
    {"method": "GET", "path": "api/v2/collections_payment_promises/{id}"},
    {"method": "GET", "path": "api/v2/comments"},
    {"method": "GET", "path": "api/v2/comments/{id}"},
    {"method": "GET", "path": "api/v2/configurations"},
    {"method": "GET", "path": "api/v2/coupon_codes"},
    {"method": "GET", "path": "api/v2/coupon_codes/{id}"},
    {"method": "GET", "path": "api/v2/coupon_sets"},
    {"method": "GET", "path": "api/v2/coupon_sets/{id}"},
    {"method": "GET", "path": "api/v2/coupons"},
    {"method": "GET", "path": "api/v2/coupons/{id}"},
    {"method": "GET", "path": "api/v2/credit_notes"},
    {"method": "GET", "path": "api/v2/credit_notes/{id}"},
    {"method": "GET", "path": "api/v2/credit_notes/{id}/download_einvoice"},
    {"method": "GET", "path": "api/v2/credit_units"},
    {"method": "GET", "path": "api/v2/currencies/list"},
    {"method": "GET", "path": "api/v2/currencies/{id}"},
    {"method": "GET", "path": "api/v2/custom_field_configs"},
    {"method": "GET", "path": "api/v2/custom_field_configs/retrieve"},
    {"method": "GET", "path": "api/v2/customers"},
    {"method": "GET", "path": "api/v2/customers/{id}"},
    {"method": "GET", "path": "api/v2/customers/{id}/contacts"},
    {"method": "GET", "path": "api/v2/customers/{id}/create_subscription_estimate"},
    {"method": "POST", "path": "api/v2/customers/{id}/create_subscription_for_items_estimate"},
    {"method": "GET", "path": "api/v2/customers/{id}/customer_entitlements"},
    {"method": "GET", "path": "api/v2/customers/{id}/email_logs"},
    {"method": "GET", "path": "api/v2/customers/{id}/hierarchy"},
    {"method": "GET", "path": "api/v2/customers/{id}/hierarchy_detail"},
    {"method": "GET", "path": "api/v2/customers/{id}/payment_vouchers"},
    {"method": "GET", "path": "api/v2/customers/{id}/upcoming_invoices_estimate"},
    {"method": "GET", "path": "api/v2/differential_prices"},
    {"method": "GET", "path": "api/v2/differential_prices/{id}"},
    {"method": "GET", "path": "api/v2/disputes"},
    {"method": "GET", "path": "api/v2/disputes/{id}"},
    {"method": "GET", "path": "api/v2/einvoices"},
    {"method": "GET", "path": "api/v2/einvoices/{id}"},
    {"method": "GET", "path": "api/v2/entitlements"},
    {"method": "POST", "path": "api/v2/estimates/create_invoice"},
    {"method": "POST", "path": "api/v2/estimates/create_invoice_for_items"},
    {"method": "POST", "path": "api/v2/estimates/create_subscription"},
    {"method": "POST", "path": "api/v2/estimates/create_subscription_for_items"},
    {"method": "POST", "path": "api/v2/estimates/gift_subscription"},
    {"method": "POST", "path": "api/v2/estimates/gift_subscription_for_items"},
    {"method": "POST", "path": "api/v2/estimates/payment_schedules"},
    {"method": "POST", "path": "api/v2/estimates/update_subscription"},
    {"method": "POST", "path": "api/v2/estimates/update_subscription_for_items"},
    {"method": "GET", "path": "api/v2/events"},
    {"method": "GET", "path": "api/v2/events/{id}"},
    {"method": "GET", "path": "api/v2/features"},
    {"method": "GET", "path": "api/v2/features/{id}"},
    {"method": "GET", "path": "api/v2/features/{id}/item_entitlements"},
    {"method": "GET", "path": "api/v2/full_exports/status"},
    {"method": "GET", "path": "api/v2/gateway_request_logs"},
    {"method": "GET", "path": "api/v2/gateway_request_logs/{id}"},
    {"method": "GET", "path": "api/v2/gateway_webhook_logs"},
    {"method": "GET", "path": "api/v2/gateway_webhook_logs/{id}"},
    {"method": "GET", "path": "api/v2/gifts"},
    {"method": "GET", "path": "api/v2/gifts/{id}"},
    {"method": "GET", "path": "api/v2/grant_blocks"},
    {"method": "GET", "path": "api/v2/hosted_pages"},
    {"method": "GET", "path": "api/v2/hosted_pages/{id}"},
    {"method": "GET", "path": "api/v2/invoices"},
    {"method": "GET", "path": "api/v2/invoices/payment_reference_numbers"},
    {"method": "GET", "path": "api/v2/invoices/{id}"},
    {"method": "GET", "path": "api/v2/invoices/{id}/download_einvoice"},
    {"method": "GET", "path": "api/v2/invoices/{id}/payment_schedules"},
    {"method": "GET", "path": "api/v2/invoices/{id}/payment_vouchers"},
    {"method": "GET", "path": "api/v2/invoices/{id}/payments"},
    {"method": "GET", "path": "api/v2/item_families"},
    {"method": "GET", "path": "api/v2/item_families/{id}"},
    {"method": "GET", "path": "api/v2/item_prices"},
    {"method": "GET", "path": "api/v2/item_prices/{id}"},
    {"method": "GET", "path": "api/v2/item_prices/{id}/applicable_item_prices"},
    {"method": "GET", "path": "api/v2/item_prices/{id}/applicable_items"},
    {"method": "GET", "path": "api/v2/items"},
    {"method": "GET", "path": "api/v2/items/{id}"},
    {"method": "GET", "path": "api/v2/items/{id}/attached_items"},
    {"method": "GET", "path": "api/v2/items/{id}/item_entitlements"},
    {"method": "GET", "path": "api/v2/ledger_account_balances"},
    {"method": "GET", "path": "api/v2/ledger_operations"},
    {"method": "GET", "path": "api/v2/ledger_operations/{id}"},
    {"method": "GET", "path": "api/v2/meters"},
    {"method": "GET", "path": "api/v2/offer_fulfillments/{id}"},
    {"method": "GET", "path": "api/v2/omnichannel_one_time_orders"},
    {"method": "GET", "path": "api/v2/omnichannel_one_time_orders/{id}"},
    {"method": "GET", "path": "api/v2/omnichannel_subscription_items/{id}/scheduled_changes"},
    {"method": "GET", "path": "api/v2/omnichannel_subscriptions"},
    {"method": "GET", "path": "api/v2/omnichannel_subscriptions/{id}"},
    {"method": "GET", "path": "api/v2/omnichannel_subscriptions/{id}/omnichannel_transactions"},
    {"method": "GET", "path": "api/v2/orders"},
    {"method": "GET", "path": "api/v2/orders/{id}"},
    {"method": "GET", "path": "api/v2/organization_details"},
    {"method": "GET", "path": "api/v2/organization_details/{id}"},
    {"method": "GET", "path": "api/v2/payment_intents/{id}"},
    {"method": "GET", "path": "api/v2/payment_schedule_schemes"},
    {"method": "GET", "path": "api/v2/payment_schedule_schemes/{id}"},
    {"method": "GET", "path": "api/v2/payment_schedules"},
    {"method": "GET", "path": "api/v2/payment_sources"},
    {"method": "GET", "path": "api/v2/payment_sources/{id}"},
    {"method": "GET", "path": "api/v2/payment_vouchers/{id}"},
    {"method": "GET", "path": "api/v2/pc2_migration_item_families"},
    {"method": "GET", "path": "api/v2/pc2_migration_item_families/{id}"},
    {"method": "GET", "path": "api/v2/pc2_migration_item_prices"},
    {"method": "GET", "path": "api/v2/pc2_migration_item_prices/{id}"},
    {"method": "GET", "path": "api/v2/pc2_migration_items"},
    {"method": "GET", "path": "api/v2/pc2_migration_items/applicable_items"},
    {"method": "GET", "path": "api/v2/pc2_migration_items/{id}"},
    {"method": "GET", "path": "api/v2/pc2_migrations/{id}"},
    {"method": "GET", "path": "api/v2/plans"},
    {"method": "GET", "path": "api/v2/plans/{id}"},
    {"method": "GET", "path": "api/v2/price_ramps"},
    {"method": "GET", "path": "api/v2/price_ramps/{id}"},
    {"method": "GET", "path": "api/v2/price_variants"},
    {"method": "GET", "path": "api/v2/price_variants/{id}"},
    {"method": "GET", "path": "api/v2/products"},
    {"method": "GET", "path": "api/v2/products/{id}"},
    {"method": "GET", "path": "api/v2/products/{id}/variants"},
    {"method": "GET", "path": "api/v2/promotional_credits"},
    {"method": "GET", "path": "api/v2/promotional_credits/{id}"},
    {"method": "POST", "path": "api/v2/purchases/estimate"},
    {"method": "GET", "path": "api/v2/quotes"},
    {"method": "GET", "path": "api/v2/quotes/{id}"},
    {"method": "GET", "path": "api/v2/quotes/{id}/quote_entitlements"},
    {"method": "GET", "path": "api/v2/quotes/{id}/quote_line_groups"},
    {"method": "GET", "path": "api/v2/ramps"},
    {"method": "GET", "path": "api/v2/ramps/{id}"},
    {"method": "GET", "path": "api/v2/recorded_purchases/{id}"},
    {"method": "GET", "path": "api/v2/resource_migrations/retrieve_latest"},
    {"method": "GET", "path": "api/v2/retry_segments/{id}"},
    {"method": "GET", "path": "api/v2/rules/{id}"},
    {"method": "GET", "path": "api/v2/site_migration_details"},
    {"method": "GET", "path": "api/v2/site_pc_meta_records"},
    {"method": "GET", "path": "api/v2/subscriptions"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/advance_invoice_estimate"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/alert_statuses"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/applicable_alerts"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/cancel_subscription_estimate"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/cancel_subscription_for_items_estimate"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/change_term_end_estimate"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/contract_terms"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/discounts"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/entitlement_overrides"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/pause_subscription_estimate"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/regenerate_invoice_estimate"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/renewal_estimate"},
    {"method": "POST", "path": "api/v2/subscriptions/{id}/resume_subscription_estimate"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/retrieve_advance_invoice_schedule"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/retrieve_with_scheduled_changes"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/scheduled_changes"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/subscription_entitlements"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/usage_charges"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/usage_summary"},
    {"method": "GET", "path": "api/v2/subscriptions/{id}/usages"},
    {"method": "GET", "path": "api/v2/time_machines/{id}"},
    {"method": "GET", "path": "api/v2/transactions"},
    {"method": "GET", "path": "api/v2/transactions/{id}"},
    {"method": "GET", "path": "api/v2/unbilled_charges"},
    {"method": "POST", "path": "api/v2/unbilled_charges/invoice_now_estimate"},
    {"method": "GET", "path": "api/v2/usage_files/{id}/processing_status"},
    {"method": "GET", "path": "api/v2/usages"},
    {"method": "GET", "path": "api/v2/variants/{id}"},
    {"method": "GET", "path": "api/v2/vaulted_payment_methods/{id}"},
    {"method": "GET", "path": "api/v2/virtual_bank_accounts"},
    {"method": "GET", "path": "api/v2/virtual_bank_accounts/{id}"},
    {"method": "GET", "path": "api/v2/webhook_endpoints"},
    {"method": "GET", "path": "api/v2/webhook_endpoints/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The Chargebee endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | api/v2/addons | read | addons | List addons. |
| POST | api/v2/addons | write | addons | Create an addon. |
| POST | api/v2/addons/copy | write | addons | Copy an addon. |
| GET | api/v2/addons/{id} | read | addons | Retrieve an addon. |
| POST | api/v2/addons/{id} | write | addons | Update an addon. |
| POST | api/v2/addons/{id}/delete | write | addons | Delete an addon. |
| POST | api/v2/addons/{id}/unarchive | write | addons | Unarchive an addon. |
| GET | api/v2/addresses | read | addresses | Retrieve an address. |
| POST | api/v2/addresses | write | addresses | Update an address. |
| GET | api/v2/alerts | read | alerts | List alerts. |
| POST | api/v2/alerts | write | alerts | Create an alert. |
| GET | api/v2/alerts/{id} | read | alerts | Retrieve an alert. |
| POST | api/v2/alerts/{id} | write | alerts | Update an alert. |
| GET | api/v2/alerts/{id}/alert_statuses | read | alerts | List alert statuses for an alert. |
| POST | api/v2/alerts/{id}/delete | write | alerts | Delete an alert. |
| GET | api/v2/attached_items/{id} | read | attached_items | Retrieve an attached item. |
| POST | api/v2/attached_items/{id} | write | attached_items | Update an attached item. |
| POST | api/v2/attached_items/{id}/delete | write | attached_items | Delete an attached item. |
| POST | api/v2/batch/usage_events | write | batch | Ingest usage events in batch. |
| GET | api/v2/business_entities | read | business_entities | List business entities. |
| POST | api/v2/business_entities | write | business_entities | Create a business entity. |
| GET | api/v2/business_entities/transfers | read | business_entities | List business entity transfers. |
| POST | api/v2/business_entities/transfers | write | business_entities | Transfer a customer to another business entity. |
| GET | api/v2/business_entities/{id} | read | business_entities | Retrieve a business entity. |
| POST | api/v2/business_entities/{id} | write | business_entities | Update business entity. |
| GET | api/v2/business_rules | read | business_rules | List business rules. |
| POST | api/v2/business_rules | write | business_rules | Create a business rule. |
| POST | api/v2/business_rules/apply_rules | write | business_rules | Apply business rules. |
| GET | api/v2/business_rules/{id} | read | business_rules | Retrieve a business rule. |
| POST | api/v2/business_rules/{id}/activate | write | business_rules | Activate a business rule. |
| POST | api/v2/business_rules/{id}/deactivate | write | business_rules | Deactivate a business rule. |
| POST | api/v2/business_rules/{id}/delete | write | business_rules | Delete a business rule. |
| POST | api/v2/business_rules/{id}/delete_draft | write | business_rules | Delete a business rule draft. |
| GET | api/v2/business_rules/{id}/draft | read | business_rules | Retrieve a business rule draft. |
| POST | api/v2/business_rules/{id}/draft | write | business_rules | Update a business rule draft. |
| POST | api/v2/business_rules/{id}/release | write | business_rules | Release a business rule. |
| GET | api/v2/business_rulesets | read | business_rulesets | List business rulesets. |
| POST | api/v2/business_rulesets | write | business_rulesets | Create a business ruleset. |
| GET | api/v2/business_rulesets/{id} | read | business_rulesets | Retrieve a business ruleset. |
| POST | api/v2/business_rulesets/{id} | write | business_rulesets | Update a business ruleset. |
| POST | api/v2/business_rulesets/{id}/activate | write | business_rulesets | Activate a business ruleset. |
| POST | api/v2/business_rulesets/{id}/add_rules | write | business_rulesets | Add business rules to a ruleset. |
| POST | api/v2/business_rulesets/{id}/deactivate | write | business_rulesets | Deactivate a business ruleset. |
| POST | api/v2/business_rulesets/{id}/delete | write | business_rulesets | Delete a business ruleset. |
| POST | api/v2/business_rulesets/{id}/remove_rules | write | business_rulesets | Remove business rules from a ruleset. |
| GET | api/v2/business_rulesets/{id}/rules | read | business_rulesets | List rules in a business ruleset. |
| GET | api/v2/cards/{id} | read | cards | Retrieve card for a customer. |
| GET | api/v2/collections_payment_promises | read | collections_payment_promises | List collections payment promises. |
| POST | api/v2/collections_payment_promises | write | collections_payment_promises | Create a collections payment promise. |
| GET | api/v2/collections_payment_promises/{id} | read | collections_payment_promises | Retrieve a payment promise. |
| POST | api/v2/collections_payment_promises/{id} | write | collections_payment_promises | Update a collections payment promise. |
| POST | api/v2/collections_payment_promises/{id}/cancel | write | collections_payment_promises | Cancel a collections payment promise. |
| GET | api/v2/comments | read | comments | List comments. |
| POST | api/v2/comments | write | comments | Create a comment. |
| GET | api/v2/comments/{id} | read | comments | Retrieve a comment. |
| POST | api/v2/comments/{id}/delete | write | comments | Delete a comment. |
| GET | api/v2/configurations | read | configurations | List site configurations. |
| GET | api/v2/coupon_codes | read | coupon_codes | List coupon codes. |
| GET | api/v2/coupon_codes/{id} | read | coupon_codes | Retrieve a coupon code. |
| POST | api/v2/coupon_codes/{id}/archive | write | coupon_codes | Archive a coupon code. |
| GET | api/v2/coupon_sets | read | coupon_sets | List coupon sets. |
| POST | api/v2/coupon_sets | write | coupon_sets | Create a coupon set. |
| GET | api/v2/coupon_sets/{id} | read | coupon_sets | Retrieve a coupon set. |
| POST | api/v2/coupon_sets/{id}/add_coupon_codes | write | coupon_sets | Add coupon codes to coupon set. |
| POST | api/v2/coupon_sets/{id}/delete | write | coupon_sets | Delete a coupon set. |
| POST | api/v2/coupon_sets/{id}/delete_unused_coupon_codes | write | coupon_sets | Delete unused coupon codes. |
| POST | api/v2/coupon_sets/{id}/update | write | coupon_sets | Update a coupon set. |
| GET | api/v2/coupons | read | coupons | List coupons. |
| POST | api/v2/coupons | write | coupons | Create a coupon. |
| POST | api/v2/coupons/copy | write | coupons | Copy a coupon. |
| POST | api/v2/coupons/create_for_items | write | coupons | Create a coupon for items. |
| GET | api/v2/coupons/{id} | read | coupons | Retrieve a coupon. |
| POST | api/v2/coupons/{id} | write | coupons | Update a coupon. |
| POST | api/v2/coupons/{id}/delete | write | coupons | Delete a coupon. |
| POST | api/v2/coupons/{id}/unarchive | write | coupons | Unarchive a coupon. |
| POST | api/v2/coupons/{id}/update_for_items | write | coupons | Update a coupon for items. |
| GET | api/v2/credit_notes | read | credit_notes | List credit notes. |
| POST | api/v2/credit_notes | write | credit_notes | Create credit note. |
| POST | api/v2/credit_notes/import_credit_note | write | credit_notes | Import credit note. |
| GET | api/v2/credit_notes/{id} | read | credit_notes | Retrieve a credit note. |
| POST | api/v2/credit_notes/{id}/delete | write | credit_notes | Delete a credit note. |
| GET | api/v2/credit_notes/{id}/download_einvoice | read | credit_notes | Download e-invoice for credit note. |
| POST | api/v2/credit_notes/{id}/pdf | write | credit_notes | Retrieve credit note as PDF. |
| POST | api/v2/credit_notes/{id}/record_refund | write | credit_notes | Record refund for a credit note. |
| POST | api/v2/credit_notes/{id}/refund | write | credit_notes | Refund a credit note. |
| POST | api/v2/credit_notes/{id}/remove_tax_withheld_refund | write | credit_notes | Remove tax withheld refunds from a credit note. |
| POST | api/v2/credit_notes/{id}/resend_einvoice | write | credit_notes | Resend failed einvoice in credit notes. |
| POST | api/v2/credit_notes/{id}/send_einvoice | write | credit_notes | Send an einvoice for credit notes. |
| POST | api/v2/credit_notes/{id}/send_email | write | credit_notes | Send Credit Note Email. |
| POST | api/v2/credit_notes/{id}/update | write | credit_notes | Update Credit Note Details. |
| POST | api/v2/credit_notes/{id}/void | write | credit_notes | Void a credit note. |
| GET | api/v2/credit_units | read | credit_units | List credit units. |
| POST | api/v2/credit_units | write | credit_units | Create a credit unit. |
| POST | api/v2/credit_units/{id} | write | credit_units | Update a credit unit. |
| POST | api/v2/credit_units/{id}/archive_command | write | credit_units | Archive a credit unit. |
| POST | api/v2/credit_units/{id}/reactivate_command | write | credit_units | Reactivate a credit unit. |
| POST | api/v2/csv_tax_rules | write | csv_tax_rules | Taxes Csv import. |
| POST | api/v2/currencies | write | currencies | Add a new currency. |
| GET | api/v2/currencies/list | read | currencies | List currencies. |
| GET | api/v2/currencies/{id} | read | currencies | Retrieve a currency. |
| POST | api/v2/currencies/{id} | write | currencies | Update a currency. |
| POST | api/v2/currencies/{id}/add_schedule | write | currencies | Add schedule. |
| POST | api/v2/currencies/{id}/remove_schedule | write | currencies | Remove schedule. |
| GET | api/v2/custom_field_configs | read | custom_field_configs | List custom field configurations. |
| GET | api/v2/custom_field_configs/retrieve | read | custom_field_configs | Retrieve a custom field configuration. |
| GET | api/v2/customers | read | customers | List customers. |
| POST | api/v2/customers | write | customers | Create a customer. |
| POST | api/v2/customers/merge | write | customers | Merge customers. |
| POST | api/v2/customers/move | write | customers | Move a customer. |
| GET | api/v2/customers/{id} | read | customers | Retrieve a customer. |
| POST | api/v2/customers/{id} | write | customers | Update a customer. |
| POST | api/v2/customers/{id}/add_contact | write | customers | Add contacts to a customer. |
| POST | api/v2/customers/{id}/assign_payment_role | write | customers | Assign payment role. |
| POST | api/v2/customers/{id}/change_billing_date | write | customers | Change billing date. |
| POST | api/v2/customers/{id}/clear_personal_data | write | customers | Clear personal data of a customer. |
| POST | api/v2/customers/{id}/collect_payment | write | customers | Collect payment for customer. |
| GET | api/v2/customers/{id}/contacts | read | customers | List of contacts for a customer. |
| POST | api/v2/customers/{id}/copy_card | write | customers | Copy card. |
| GET | api/v2/customers/{id}/create_subscription_estimate | read | customers | Create subscription for a customer estimate. |
| POST | api/v2/customers/{id}/create_subscription_for_items_estimate | read | customers | Estimate for creating a subscription. |
| POST | api/v2/customers/{id}/create_subscription_quote | write | customers | Create quote for a new subscription. |
| POST | api/v2/customers/{id}/create_subscription_quote_for_items | write | customers | Create a quote for subscription creation. |
| POST | api/v2/customers/{id}/credit_card | write | customers | Update card for a customer. |
| GET | api/v2/customers/{id}/customer_entitlements | read | customers | List customer entitlements. |
| POST | api/v2/customers/{id}/delete | write | customers | Delete a customer. |
| POST | api/v2/customers/{id}/delete_card | write | customers | Delete card for a customer. |
| POST | api/v2/customers/{id}/delete_contact | write | customers | Delete contacts for a customer. |
| POST | api/v2/customers/{id}/delete_relationship | write | customers | Unlink a customer from its parent account. |
| GET | api/v2/customers/{id}/email_logs | read | customers | List email logs for a customer. |
| GET | api/v2/customers/{id}/hierarchy | read | customers | Get account hierarchy for a customer. |
| GET | api/v2/customers/{id}/hierarchy_detail | read | customers | Get paginated account hierarchy for a customer. |
| POST | api/v2/customers/{id}/import_for_items | write | customers | Import a subscription. |
| POST | api/v2/customers/{id}/import_subscription | write | customers | Import subscription for customer. |
| GET | api/v2/customers/{id}/payment_vouchers | read | customers | List vouchers for a customer. |
| POST | api/v2/customers/{id}/record_excess_payment | write | customers | Record an excess payment for a customer. |
| POST | api/v2/customers/{id}/relationships | write | customers | Link a customer to an account hierarchy. |
| POST | api/v2/customers/{id}/send_payment_request | write | customers | Send Payment Request Email. |
| POST | api/v2/customers/{id}/subscription_for_items | write | customers | Create a subscription. |
| POST | api/v2/customers/{id}/subscriptions | write | customers | Create subscription for customer. |
| POST | api/v2/customers/{id}/switch_gateway | write | customers | Switch gateway. |
| GET | api/v2/customers/{id}/upcoming_invoices_estimate | read | customers | Upcoming invoices estimate. |
| POST | api/v2/customers/{id}/update_billing_info | write | customers | Update billing info for a customer. |
| POST | api/v2/customers/{id}/update_contact | write | customers | Update contacts for a customer. |
| POST | api/v2/customers/{id}/update_hierarchy_settings | write | customers | Update account hierarchy access settings for a customer. |
| POST | api/v2/customers/{id}/update_payment_method | write | customers | Update payment method for a customer. |
| GET | api/v2/differential_prices | read | differential_prices | List differential prices. |
| GET | api/v2/differential_prices/{id} | read | differential_prices | Retrieve a differential price. |
| POST | api/v2/differential_prices/{id} | write | differential_prices | Update a differential price. |
| POST | api/v2/differential_prices/{id}/delete | write | differential_prices | Delete a differential price. |
| GET | api/v2/disputes | read | disputes | List Disputes. |
| GET | api/v2/disputes/{id} | read | disputes | Retrieve A Dispute. |
| GET | api/v2/einvoices | read | einvoices | List e-invoices. |
| GET | api/v2/einvoices/{id} | read | einvoices | Retrieve an e-invoice. |
| GET | api/v2/entitlements | read | entitlements | List entitlements. |
| POST | api/v2/entitlements | write | entitlements | Manage entitlements for a feature. |
| POST | api/v2/estimates/create_invoice | read | estimates | Create invoice estimate. |
| POST | api/v2/estimates/create_invoice_for_items | read | estimates | Create invoice for items estimate. |
| POST | api/v2/estimates/create_subscription | read | estimates | Create subscription estimate. |
| POST | api/v2/estimates/create_subscription_for_items | read | estimates | Estimate for creating a customer and subscription. |
| POST | api/v2/estimates/gift_subscription | read | estimates | Gift subscription estimate. |
| POST | api/v2/estimates/gift_subscription_for_items | read | estimates | Gift subscription estimate for items. |
| POST | api/v2/estimates/payment_schedules | read | estimates | Create a payment schedule estimate. |
| POST | api/v2/estimates/update_subscription | read | estimates | Update subscription estimate. |
| POST | api/v2/estimates/update_subscription_for_items | read | estimates | Estimate for updating a subscription. |
| GET | api/v2/events | read | events | List events. |
| GET | api/v2/events/{id} | read | events | Retrieve an event. |
| POST | api/v2/exports/addons | write | exports | Export addons. |
| POST | api/v2/exports/attached_items | write | exports | Export attached items. |
| POST | api/v2/exports/coupons | write | exports | Export coupons. |
| POST | api/v2/exports/credit_notes | write | exports | Export credit notes. |
| POST | api/v2/exports/customers | write | exports | Export customers. |
| POST | api/v2/exports/deferred_revenue | write | exports | Export deferred revenue reports. |
| POST | api/v2/exports/differential_prices | write | exports | Export differential price. |
| POST | api/v2/exports/invoices | write | exports | Export invoices. |
| POST | api/v2/exports/item_families | write | exports | Export item families. |
| POST | api/v2/exports/item_prices | write | exports | Export item prices. |
| POST | api/v2/exports/items | write | exports | Export items. |
| POST | api/v2/exports/orders | write | exports | Export orders. |
| POST | api/v2/exports/plans | write | exports | Export plans. |
| POST | api/v2/exports/price_variants | write | exports | Export price variants. |
| POST | api/v2/exports/ramps | write | exports | Export Subscription Ramps. |
| POST | api/v2/exports/revenue_recognition | write | exports | Export revenue recognition reports. |
| POST | api/v2/exports/subscriptions | write | exports | Export subscriptions. |
| POST | api/v2/exports/transactions | write | exports | Export transactions. |
| GET | api/v2/exports/{id} | write | exports | Retrieve an export. Kept out of read: returns a pre-signed download URL. |
| GET | api/v2/features | read | features | List features. |
| POST | api/v2/features | write | features | Create a feature. |
| GET | api/v2/features/{id} | read | features | Retrieve a feature. |
| POST | api/v2/features/{id} | write | features | Update a feature. |
| POST | api/v2/features/{id}/activate_command | write | features | Activate a feature. |
| POST | api/v2/features/{id}/archive_command | write | features | Archive a feature. |
| POST | api/v2/features/{id}/delete | write | features | Delete a feature. |
| GET | api/v2/features/{id}/item_entitlements | read | features | List item entitlements for a feature. |
| POST | api/v2/features/{id}/item_entitlements | write | features | Upsert or remove item entitlements for a feature. |
| POST | api/v2/features/{id}/reactivate_command | write | features | Reactivate a feature. |
| GET | api/v2/full_exports/status | read | full_exports | Retrieve full export status. |
| GET | api/v2/gateway_request_logs | read | gateway_request_logs | List gateway request logs. |
| GET | api/v2/gateway_request_logs/{id} | read | gateway_request_logs | Retrieve a gateway request log. |
| GET | api/v2/gateway_webhook_logs | read | gateway_webhook_logs | List gateway webhook logs. |
| GET | api/v2/gateway_webhook_logs/{id} | read | gateway_webhook_logs | Retrieve a gateway webhook log. |
| GET | api/v2/gifts | read | gifts | List gifts. |
| POST | api/v2/gifts | write | gifts | Create a gift. |
| POST | api/v2/gifts/create_for_items | write | gifts | Create a gift subscription for items. |
| GET | api/v2/gifts/{id} | read | gifts | Retrieve a gift. |
| POST | api/v2/gifts/{id}/cancel | write | gifts | Cancel a gift. |
| POST | api/v2/gifts/{id}/claim | write | gifts | Claim a gift. |
| POST | api/v2/gifts/{id}/update_gift | write | gifts | Update a gift. |
| GET | api/v2/grant_blocks | read | grant_blocks | List grant blocks. |
| GET | api/v2/hosted_pages | read | hosted_pages | List hosted pages. |
| POST | api/v2/hosted_pages/accept_quote | write | hosted_pages | Accept a quote. |
| POST | api/v2/hosted_pages/checkout_existing | write | hosted_pages | Checkout existing subscription. |
| POST | api/v2/hosted_pages/checkout_existing_for_items | write | hosted_pages | Create checkout to update a subscription. |
| POST | api/v2/hosted_pages/checkout_gift | write | hosted_pages | Checkout gift subscription. |
| POST | api/v2/hosted_pages/checkout_gift_for_items | write | hosted_pages | Checkout gift subscription for items. |
| POST | api/v2/hosted_pages/checkout_new | write | hosted_pages | Checkout new subscription. |
| POST | api/v2/hosted_pages/checkout_new_for_items | write | hosted_pages | Create checkout for a new subscription. |
| POST | api/v2/hosted_pages/checkout_one_time | write | hosted_pages | Checkout one-time payments. |
| POST | api/v2/hosted_pages/checkout_one_time_for_items | write | hosted_pages | Checkout charge-items and one-time charges. |
| POST | api/v2/hosted_pages/claim_gift | write | hosted_pages | Claim a gift subscription. |
| POST | api/v2/hosted_pages/collect_now | write | hosted_pages | Collect now. |
| POST | api/v2/hosted_pages/events | write | hosted_pages | Notify an event. |
| POST | api/v2/hosted_pages/extend_subscription | write | hosted_pages | Extend subscription. |
| POST | api/v2/hosted_pages/manage_payment_sources | write | hosted_pages | Manage payment sources. |
| POST | api/v2/hosted_pages/pre_cancel | write | hosted_pages | Create a pre-cancel hosted page. |
| POST | api/v2/hosted_pages/retrieve_agreement_pdf | write | hosted_pages | Retrieve direct debit agreement PDF. |
| POST | api/v2/hosted_pages/view_voucher | write | hosted_pages | Create a hosted page to view Boleto vouchers. |
| GET | api/v2/hosted_pages/{id} | read | hosted_pages | Retrieve a hosted page. |
| POST | api/v2/hosted_pages/{id}/acknowledge | write | hosted_pages | Acknowledge a hosted page. |
| POST | api/v2/in_app_subscriptions/{id}/import_receipt | write | in_app_subscriptions | Import receipt. |
| POST | api/v2/in_app_subscriptions/{id}/import_subscription | write | in_app_subscriptions | Import subscription without receipt. |
| POST | api/v2/in_app_subscriptions/{id}/process_purchase_command | write | in_app_subscriptions | Process purchase command. |
| POST | api/v2/in_app_subscriptions/{id}/retrieve | write | in_app_subscriptions | Retrieve store subscription. |
| GET | api/v2/invoices | read | invoices | List invoices. |
| POST | api/v2/invoices | write | invoices | Create an invoice. |
| POST | api/v2/invoices/charge | write | invoices | Create invoice for a one-time charge. |
| POST | api/v2/invoices/charge_addon | write | invoices | Create invoice for a non-recurring addon. |
| POST | api/v2/invoices/create_for_charge_items_and_charges | write | invoices | Create invoice for items and one-time charges. |
| POST | api/v2/invoices/import_invoice | write | invoices | Import invoice. |
| GET | api/v2/invoices/payment_reference_numbers | read | invoices | List payment reference numbers. |
| GET | api/v2/invoices/{id} | read | invoices | Retrieve an invoice. |
| POST | api/v2/invoices/{id}/add_addon_charge | write | invoices | Add non-recurring addon to a pending invoice. |
| POST | api/v2/invoices/{id}/add_charge | write | invoices | Add one-time charge to a pending invoice. |
| POST | api/v2/invoices/{id}/add_charge_item | write | invoices | Add a charge-item to a pending invoice. |
| POST | api/v2/invoices/{id}/apply_credits | write | invoices | Apply credits for an invoice. |
| POST | api/v2/invoices/{id}/apply_payment_schedule_scheme | write | invoices | Apply payment schedule scheme to an invoice. |
| POST | api/v2/invoices/{id}/apply_payments | write | invoices | Apply payments for an invoice. |
| POST | api/v2/invoices/{id}/close | write | invoices | Close a pending invoice. |
| POST | api/v2/invoices/{id}/collect_payment | write | invoices | Collect payment for an invoice. |
| POST | api/v2/invoices/{id}/delete | write | invoices | Delete an invoice. |
| POST | api/v2/invoices/{id}/delete_line_items | write | invoices | Delete line items. |
| GET | api/v2/invoices/{id}/download_einvoice | read | invoices | Download e-invoice. |
| POST | api/v2/invoices/{id}/pause_dunning | write | invoices | Pause dunning for invoice. |
| GET | api/v2/invoices/{id}/payment_schedules | read | invoices | Retrieve payment schedules for an invoice. |
| GET | api/v2/invoices/{id}/payment_vouchers | read | invoices | List vouchers for an invoice. |
| GET | api/v2/invoices/{id}/payments | read | invoices | List payments for an invoice. |
| POST | api/v2/invoices/{id}/pdf | write | invoices | Retrieve invoice as PDF. |
| POST | api/v2/invoices/{id}/record_payment | write | invoices | Record an invoice payment. |
| POST | api/v2/invoices/{id}/record_refund | write | invoices | Record refund for an invoice. |
| POST | api/v2/invoices/{id}/record_tax_withheld | write | invoices | Record tax withheld for an invoice. |
| POST | api/v2/invoices/{id}/refund | write | invoices | Refund an invoice. |
| POST | api/v2/invoices/{id}/remove_credit_note | write | invoices | Remove credit note from an invoice. |
| POST | api/v2/invoices/{id}/remove_payment | write | invoices | Remove payment from an invoice. |
| POST | api/v2/invoices/{id}/remove_payment_schedule_scheme | write | invoices | Remove payment schedule scheme from an invoice. |
| POST | api/v2/invoices/{id}/remove_tax_withheld | write | invoices | Remove tax withheld for an invoice. |
| POST | api/v2/invoices/{id}/resend_einvoice | write | invoices | Resend failed einvoice in invoices. |
| POST | api/v2/invoices/{id}/resume_dunning | write | invoices | Resume dunning for invoice. |
| POST | api/v2/invoices/{id}/send_einvoice | write | invoices | Send an einvoice for invoices. |
| POST | api/v2/invoices/{id}/send_email | write | invoices | Send Invoice Email. |
| POST | api/v2/invoices/{id}/stop_dunning | write | invoices | Stop dunning for invoice. |
| POST | api/v2/invoices/{id}/sync_usages | write | invoices | Sync usages. |
| POST | api/v2/invoices/{id}/update_details | write | invoices | Update invoice details. |
| POST | api/v2/invoices/{id}/void | write | invoices | Void an invoice. |
| POST | api/v2/invoices/{id}/void_before_capture | write | invoices | Void authorizations before capture. |
| POST | api/v2/invoices/{id}/write_off | write | invoices | Write off an invoice. |
| GET | api/v2/item_families | read | item_families | List item families. |
| POST | api/v2/item_families | write | item_families | Create an item family. |
| GET | api/v2/item_families/{id} | read | item_families | Retrieve an item family. |
| POST | api/v2/item_families/{id} | write | item_families | Update an item family. |
| POST | api/v2/item_families/{id}/delete | write | item_families | Delete an item family. |
| GET | api/v2/item_prices | read | item_prices | List item prices. |
| POST | api/v2/item_prices | write | item_prices | Create an item price. |
| GET | api/v2/item_prices/{id} | read | item_prices | Retrieve an item price. |
| POST | api/v2/item_prices/{id} | write | item_prices | Update an item price. |
| GET | api/v2/item_prices/{id}/applicable_item_prices | read | item_prices | List applicable item prices for a plan-item price. |
| GET | api/v2/item_prices/{id}/applicable_items | read | item_prices | List applicable items for a plan-item price. |
| POST | api/v2/item_prices/{id}/delete | write | item_prices | Delete an item price. |
| POST | api/v2/item_prices/{id}/differential_prices | write | item_prices | Create a differential price. |
| GET | api/v2/items | read | items | List items. |
| POST | api/v2/items | write | items | Create an item. |
| GET | api/v2/items/{id} | read | items | Retrieve an item. |
| POST | api/v2/items/{id} | write | items | Update an item. |
| GET | api/v2/items/{id}/attached_items | read | items | List attached items. |
| POST | api/v2/items/{id}/attached_items | write | items | Create an attached item. |
| POST | api/v2/items/{id}/delete | write | items | Delete an item. |
| GET | api/v2/items/{id}/item_entitlements | read | items | List item entitlements for an item. |
| POST | api/v2/items/{id}/item_entitlements | write | items | Upsert or remove item entitlements for an item. |
| GET | api/v2/ledger_account_balances | read | ledger_account_balances | List ledger account balances. |
| POST | api/v2/ledger_account_balances/update_overdraft_limit | write | ledger_account_balances | Update the overdraft limit. |
| GET | api/v2/ledger_operations | read | ledger_operations | List ledger operations. |
| POST | api/v2/ledger_operations/allocate | write | ledger_operations | Allocate. |
| POST | api/v2/ledger_operations/authorize | write | ledger_operations | Authorize. |
| POST | api/v2/ledger_operations/capture | write | ledger_operations | Capture. |
| POST | api/v2/ledger_operations/capture_authorization | write | ledger_operations | Capture authorization. |
| POST | api/v2/ledger_operations/release_authorization | write | ledger_operations | Release authorization. |
| GET | api/v2/ledger_operations/{id} | read | ledger_operations | Retrieve ledger operation. |
| POST | api/v2/metered_features | write | metered_features | Create a metered feature. |
| POST | api/v2/metered_features/{id}/archive_command | write | metered_features | Archive a metered feature. |
| POST | api/v2/metered_features/{id}/delete | write | metered_features | Delete a metered feature. |
| POST | api/v2/metered_features/{id}/reactivate_command | write | metered_features | Reactivate a metered feature. |
| GET | api/v2/meters | read | meters | List all available meters. |
| POST | api/v2/non_subscriptions/{id}/one_time_purchase | write | non_subscriptions | One time purchase. |
| POST | api/v2/offer_events | write | offer_events | Create an offer event. |
| POST | api/v2/offer_fulfillments | write | offer_fulfillments | Create an offer fulfillment. |
| GET | api/v2/offer_fulfillments/{id} | read | offer_fulfillments | Retrieve an offer fulfillment. |
| POST | api/v2/offer_fulfillments/{id} | write | offer_fulfillments | Update an offer fulfillment. |
| GET | api/v2/omnichannel_one_time_orders | read | omnichannel_one_time_orders | List omnichannel one time orders. |
| GET | api/v2/omnichannel_one_time_orders/{id} | read | omnichannel_one_time_orders | Retrieve a one time order. |
| GET | api/v2/omnichannel_subscription_items/{id}/scheduled_changes | read | omnichannel_subscription_items | List scheduled changes for omnichannel subscription item. |
| GET | api/v2/omnichannel_subscriptions | read | omnichannel_subscriptions | List omnichannel subscriptions. |
| GET | api/v2/omnichannel_subscriptions/{id} | read | omnichannel_subscriptions | Retrieve an omnichannel subscription. |
| POST | api/v2/omnichannel_subscriptions/{id}/move | write | omnichannel_subscriptions | Move an omnichannel subscription. |
| GET | api/v2/omnichannel_subscriptions/{id}/omnichannel_transactions | read | omnichannel_subscriptions | List omnichannel transactions of an omnichannel subscription. |
| GET | api/v2/orders | read | orders | List orders. |
| POST | api/v2/orders | write | orders | Create an order. |
| POST | api/v2/orders/import_order | write | orders | Import an order. |
| GET | api/v2/orders/{id} | read | orders | Retrieve an order. |
| POST | api/v2/orders/{id} | write | orders | Update an order. |
| POST | api/v2/orders/{id}/assign_order_number | write | orders | Assign order number. |
| POST | api/v2/orders/{id}/cancel | write | orders | Cancel an order. |
| POST | api/v2/orders/{id}/create_refundable_credit_note | write | orders | Create a refundable credit note. |
| POST | api/v2/orders/{id}/delete | write | orders | Delete an imported order. |
| POST | api/v2/orders/{id}/reopen | write | orders | Reopen a cancelled order. |
| POST | api/v2/orders/{id}/resend | write | orders | Resend an order. |
| GET | api/v2/organization_details | read | organization_details | List organization details. |
| POST | api/v2/organization_details | write | organization_details | Update organization details. |
| GET | api/v2/organization_details/{id} | read | organization_details | Retrieve organization details. |
| POST | api/v2/payment_intents | write | payment_intents | Create a payment intent. |
| GET | api/v2/payment_intents/{id} | read | payment_intents | Retrieve a payment intent. |
| POST | api/v2/payment_intents/{id} | write | payment_intents | Update a payment intent. |
| GET | api/v2/payment_schedule_schemes | read | payment_schedule_schemes | List payment schedule schemes. |
| POST | api/v2/payment_schedule_schemes | write | payment_schedule_schemes | Create a payment schedule scheme. |
| GET | api/v2/payment_schedule_schemes/{id} | read | payment_schedule_schemes | Retrieve a payment schedule scheme. |
| POST | api/v2/payment_schedule_schemes/{id}/delete | write | payment_schedule_schemes | Delete a payment schedule scheme. |
| GET | api/v2/payment_schedules | read | payment_schedules | List payment schedules. |
| GET | api/v2/payment_sources | read | payment_sources | List payment sources. |
| POST | api/v2/payment_sources/create_bank_account | write | payment_sources | Create a bank account payment source. |
| POST | api/v2/payment_sources/create_card | write | payment_sources | Create a card payment source. |
| POST | api/v2/payment_sources/create_using_payment_intent | write | payment_sources | Create using payment intent. |
| POST | api/v2/payment_sources/create_using_permanent_token | write | payment_sources | Create using permanent token. |
| POST | api/v2/payment_sources/create_using_temp_token | write | payment_sources | Create using gateway temporary token. |
| POST | api/v2/payment_sources/create_using_token | write | payment_sources | Create using Chargebee token. |
| POST | api/v2/payment_sources/create_voucher_payment_source | write | payment_sources | Create a voucher payment method. |
| GET | api/v2/payment_sources/{id} | read | payment_sources | Retrieve a payment source. |
| POST | api/v2/payment_sources/{id}/delete | write | payment_sources | Delete a payment source. |
| POST | api/v2/payment_sources/{id}/delete_local | write | payment_sources | Local delete a payment source. |
| POST | api/v2/payment_sources/{id}/export_payment_source | write | payment_sources | Export payment source. |
| GET | api/v2/payment_sources/{id}/gateway_payment_method_tokens | write | payment_sources | List Gateway Payment Method Tokens For A Payment Source. Kept out of read: returns gateway payment method tokens. |
| POST | api/v2/payment_sources/{id}/switch_gateway_account | write | payment_sources | Switch gateway account. |
| POST | api/v2/payment_sources/{id}/update_bank_account | write | payment_sources | Update a bank account payment source. |
| POST | api/v2/payment_sources/{id}/update_card | write | payment_sources | Update a card payment source. |
| POST | api/v2/payment_sources/{id}/verify_bank_account | write | payment_sources | Verify bank account payment source. |
| POST | api/v2/payment_vouchers | write | payment_vouchers | Create a voucher for the customer to initiate payment. |
| GET | api/v2/payment_vouchers/{id} | read | payment_vouchers | Retrieve voucher data. |
| GET | api/v2/pc2_migration_item_families | read | pc2_migration_item_families | List pc2 migration item families. |
| POST | api/v2/pc2_migration_item_families | write | pc2_migration_item_families | Create a pc2_migration_item_family. |
| GET | api/v2/pc2_migration_item_families/{id} | read | pc2_migration_item_families | Retrieve a pc2 migration item family. |
| POST | api/v2/pc2_migration_item_families/{id} | write | pc2_migration_item_families | Update a pc2_migration_item_family. |
| POST | api/v2/pc2_migration_item_families/{id}/delete | write | pc2_migration_item_families | Delete draft family. |
| GET | api/v2/pc2_migration_item_prices | read | pc2_migration_item_prices | List pc2 migration item prices. |
| GET | api/v2/pc2_migration_item_prices/{id} | read | pc2_migration_item_prices | Retrieve a pc2 migration item price. |
| POST | api/v2/pc2_migration_item_prices/{id} | write | pc2_migration_item_prices | Update a pc2_migration_item_price. |
| POST | api/v2/pc2_migration_item_prices/{id}/delete | write | pc2_migration_item_prices | Delete draft item price. |
| GET | api/v2/pc2_migration_items | read | pc2_migration_items | List pc2 migration items. |
| POST | api/v2/pc2_migration_items | write | pc2_migration_items | Create a pc2_migration_item. |
| GET | api/v2/pc2_migration_items/applicable_items | read | pc2_migration_items | Applicable_items a pc2_migration_item. |
| GET | api/v2/pc2_migration_items/{id} | read | pc2_migration_items | Retrieve a pc2 migration item. |
| POST | api/v2/pc2_migration_items/{id} | write | pc2_migration_items | Update a pc2_migration_item. |
| POST | api/v2/pc2_migration_items/{id}/delete | write | pc2_migration_items | Delete draft item. |
| POST | api/v2/pc2_migrations | write | pc2_migrations | Create a pc2_migration. |
| GET | api/v2/pc2_migrations/{id} | read | pc2_migrations | Retrieve a pc2 migration. |
| POST | api/v2/pc2_migrations/{id}/contact_support | write | pc2_migrations | Contact_support a pc2_migration. |
| POST | api/v2/pc2_migrations/{id}/initiate | write | pc2_migrations | Initiate a pc2_migration. |
| POST | api/v2/personalized_offers | write | personalized_offers | List personalized offers. |
| GET | api/v2/plans | read | plans | List plans. |
| POST | api/v2/plans | write | plans | Create a plan. |
| POST | api/v2/plans/copy | write | plans | Copy a plan. |
| GET | api/v2/plans/{id} | read | plans | Retrieve a plan. |
| POST | api/v2/plans/{id} | write | plans | Update a plan. |
| POST | api/v2/plans/{id}/delete | write | plans | Delete a plan. |
| POST | api/v2/plans/{id}/unarchive | write | plans | Unarchive a plan. |
| POST | api/v2/portal_sessions | write | portal_sessions | Create a portal session. |
| GET | api/v2/portal_sessions/{id} | write | portal_sessions | Retrieve a portal session. Kept out of read: returns a portal access token and URL. |
| POST | api/v2/portal_sessions/{id}/activate | write | portal_sessions | Activate a portal session. |
| POST | api/v2/portal_sessions/{id}/logout | write | portal_sessions | Logout a portal session. |
| GET | api/v2/price_ramps | read | price_ramps | List price ramps. |
| POST | api/v2/price_ramps | write | price_ramps | Create a price ramp. |
| GET | api/v2/price_ramps/{id} | read | price_ramps | Retrieve a price ramp. |
| POST | api/v2/price_ramps/{id} | write | price_ramps | Update a price ramp. |
| POST | api/v2/price_ramps/{id}/delete | write | price_ramps | Delete a price ramp. |
| GET | api/v2/price_variants | read | price_variants | List price variants. |
| POST | api/v2/price_variants | write | price_variants | Create a price variant. |
| GET | api/v2/price_variants/{id} | read | price_variants | Retrieve a price variant. |
| POST | api/v2/price_variants/{id} | write | price_variants | Update a price variant. |
| POST | api/v2/price_variants/{id}/delete | write | price_variants | Delete a price variant. |
| POST | api/v2/pricing_page_sessions/create_for_existing_subscription | write | pricing_page_sessions | Create pricing page for existing subscription. |
| POST | api/v2/pricing_page_sessions/create_for_new_subscription | write | pricing_page_sessions | Create pricing page for new subscription. |
| GET | api/v2/products | read | products | List products. |
| POST | api/v2/products | write | products | Create a product. |
| GET | api/v2/products/{id} | read | products | Retrieve a product. |
| POST | api/v2/products/{id} | write | products | Update a product. |
| POST | api/v2/products/{id}/delete | write | products | Delete a product. |
| POST | api/v2/products/{id}/update_options | write | products | Add remove or update options for the product. |
| GET | api/v2/products/{id}/variants | read | products | List product variants. |
| POST | api/v2/products/{id}/variants | write | products | Create a product variant. |
| GET | api/v2/promotional_credits | read | promotional_credits | List promotional credits. |
| POST | api/v2/promotional_credits/add | write | promotional_credits | Add promotional credits. |
| POST | api/v2/promotional_credits/deduct | write | promotional_credits | Deduct promotional credits. |
| POST | api/v2/promotional_credits/set | write | promotional_credits | Set promotional credits. |
| GET | api/v2/promotional_credits/{id} | read | promotional_credits | Retrieve a promotional credit. |
| POST | api/v2/promotional_grants | write | promotional_grants | Create Promotional Grant. |
| POST | api/v2/purchases | write | purchases | Create a purchase. |
| POST | api/v2/purchases/estimate | read | purchases | Estimates for purchase. |
| GET | api/v2/quotes | read | quotes | List quotes. |
| POST | api/v2/quotes/create_for_charge_items_and_charges | write | quotes | Create a quote for charges and charge items. |
| POST | api/v2/quotes/create_for_onetime_charges | write | quotes | Create quote for one-time charges. |
| POST | api/v2/quotes/update_subscription_quote | write | quotes | Create quote for updating a subscription. |
| POST | api/v2/quotes/update_subscription_quote_for_items | write | quotes | Create a quote for subscription update. |
| GET | api/v2/quotes/{id} | read | quotes | Retrieve a quote. |
| POST | api/v2/quotes/{id}/convert | write | quotes | Convert a quote. |
| POST | api/v2/quotes/{id}/delete | write | quotes | Delete a quote. |
| POST | api/v2/quotes/{id}/edit_create_subscription_quote | write | quotes | Edit quote for a new subscription. |
| POST | api/v2/quotes/{id}/edit_create_subscription_quote_for_items | write | quotes | Edit a quote for subscription creation. |
| POST | api/v2/quotes/{id}/edit_for_charge_items_and_charges | write | quotes | Edit a quote for charges and charge items. |
| POST | api/v2/quotes/{id}/edit_one_time_quote | write | quotes | Edit quote for one-time charges. |
| POST | api/v2/quotes/{id}/edit_update_subscription_quote | write | quotes | Edit quote for updating a subscription. |
| POST | api/v2/quotes/{id}/edit_update_subscription_quote_for_items | write | quotes | Edit a quote for subscription update. |
| POST | api/v2/quotes/{id}/extend_expiry_date | write | quotes | Extend expiry date. |
| POST | api/v2/quotes/{id}/pdf | write | quotes | Retrieve a quote as PDF. |
| GET | api/v2/quotes/{id}/quote_entitlements | read | quotes | List Quote Entitlements. |
| GET | api/v2/quotes/{id}/quote_line_groups | read | quotes | List quote line groups. |
| POST | api/v2/quotes/{id}/update_status | write | quotes | Update quote status. |
| GET | api/v2/ramps | read | ramps | List subscription ramps. |
| GET | api/v2/ramps/{id} | read | ramps | Retrieve a subscription ramp. |
| POST | api/v2/ramps/{id}/delete | write | ramps | Delete a subscription ramp. |
| POST | api/v2/ramps/{id}/update | write | ramps | Update a subscription ramp. |
| POST | api/v2/recorded_purchases | write | recorded_purchases | Record a purchase. |
| GET | api/v2/recorded_purchases/{id} | read | recorded_purchases | Retrieve a recorded purchase. |
| GET | api/v2/resource_migrations/retrieve_latest | read | resource_migrations | Retrieve latest migration details. |
| GET | api/v2/retry_segments/{id} | read | retry_segments | Retrieve a retry segment. |
| GET | api/v2/rules/{id} | read | rules | Retrieve rule data. |
| GET | api/v2/site_migration_details | read | site_migration_details | List site migration details. |
| GET | api/v2/site_pc_meta_records | read | site_pc_meta_records | List site pc meta records. |
| GET | api/v2/subscriptions | read | subscriptions | List subscriptions. |
| POST | api/v2/subscriptions | write | subscriptions | Create a subscription. |
| POST | api/v2/subscriptions/import_subscription | write | subscriptions | Import a subscription. |
| GET | api/v2/subscriptions/{id} | read | subscriptions | Retrieve a subscription. |
| POST | api/v2/subscriptions/{id} | write | subscriptions | Update a subscription. |
| POST | api/v2/subscriptions/{id}/add_charge_at_term_end | write | subscriptions | Add charge at term end. |
| POST | api/v2/subscriptions/{id}/advance_invoice_estimate | read | subscriptions | Advance invoice estimate. |
| GET | api/v2/subscriptions/{id}/alert_statuses | read | subscriptions | List alert statuses for a subscription. |
| GET | api/v2/subscriptions/{id}/applicable_alerts | read | subscriptions | List applicable alerts for a subscription. |
| POST | api/v2/subscriptions/{id}/cancel | write | subscriptions | Cancel a subscription. |
| POST | api/v2/subscriptions/{id}/cancel_for_items | write | subscriptions | Cancel a subscription. |
| POST | api/v2/subscriptions/{id}/cancel_subscription_estimate | read | subscriptions | Cancel subscription estimate. |
| POST | api/v2/subscriptions/{id}/cancel_subscription_for_items_estimate | read | subscriptions | Cancel subscription for items estimate. |
| POST | api/v2/subscriptions/{id}/change_term_end | write | subscriptions | Change term end. |
| POST | api/v2/subscriptions/{id}/change_term_end_estimate | read | subscriptions | Subscription change term end estimate. |
| POST | api/v2/subscriptions/{id}/charge_addon_at_term_end | write | subscriptions | Charge addon at term end. |
| POST | api/v2/subscriptions/{id}/charge_future_renewals | write | subscriptions | Charge future renewals. |
| GET | api/v2/subscriptions/{id}/contract_terms | read | subscriptions | List contract terms for a subscription. |
| POST | api/v2/subscriptions/{id}/create_ramp | write | subscriptions | Create a subscription ramp. |
| POST | api/v2/subscriptions/{id}/delete | write | subscriptions | Delete a subscription. |
| POST | api/v2/subscriptions/{id}/delete_usage | write | subscriptions | **Advanced Usage-Based Billing** For high-scale usage ingestion, use [Advanced Usage-Based Billing](https://www.chargebee.com/docs/billing/2.0/usage-based-billing/understanding-usages) with the... |
| GET | api/v2/subscriptions/{id}/discounts | read | subscriptions | List discounts for a subscription. |
| POST | api/v2/subscriptions/{id}/edit_advance_invoice_schedule | write | subscriptions | Edit advance invoice schedule. |
| GET | api/v2/subscriptions/{id}/entitlement_overrides | read | subscriptions | List entitlement overrides for a subscription. |
| POST | api/v2/subscriptions/{id}/entitlement_overrides | write | subscriptions | Upsert or remove entitlement overrides for a subscription. |
| POST | api/v2/subscriptions/{id}/import_contract_term | write | subscriptions | Import contract term. |
| POST | api/v2/subscriptions/{id}/import_unbilled_charges | write | subscriptions | Import unbilled charges. |
| POST | api/v2/subscriptions/{id}/move | write | subscriptions | Move a subscription. |
| POST | api/v2/subscriptions/{id}/override_billing_profile | write | subscriptions | Override billing profile. |
| POST | api/v2/subscriptions/{id}/pause | write | subscriptions | Pause a subscription. |
| POST | api/v2/subscriptions/{id}/pause_subscription_estimate | read | subscriptions | Pause subscription estimate. |
| POST | api/v2/subscriptions/{id}/reactivate | write | subscriptions | Reactivate a subscription. |
| POST | api/v2/subscriptions/{id}/regenerate_invoice | write | subscriptions | Regenerate an invoice. |
| POST | api/v2/subscriptions/{id}/regenerate_invoice_estimate | read | subscriptions | Regenerate invoice estimate. |
| POST | api/v2/subscriptions/{id}/remove_advance_invoice_schedule | write | subscriptions | Remove an advance invoice schedule. |
| POST | api/v2/subscriptions/{id}/remove_coupons | write | subscriptions | Remove coupons. |
| POST | api/v2/subscriptions/{id}/remove_scheduled_cancellation | write | subscriptions | Remove scheduled cancellation. |
| POST | api/v2/subscriptions/{id}/remove_scheduled_changes | write | subscriptions | Remove scheduled changes from a subscription. |
| POST | api/v2/subscriptions/{id}/remove_scheduled_pause | write | subscriptions | Remove scheduled pause. |
| POST | api/v2/subscriptions/{id}/remove_scheduled_resumption | write | subscriptions | Remove scheduled resumption. |
| GET | api/v2/subscriptions/{id}/renewal_estimate | read | subscriptions | Subscription renewal estimate. |
| POST | api/v2/subscriptions/{id}/resume | write | subscriptions | Resume a subscription. |
| POST | api/v2/subscriptions/{id}/resume_subscription_estimate | read | subscriptions | Resume subscription estimate. |
| GET | api/v2/subscriptions/{id}/retrieve_advance_invoice_schedule | read | subscriptions | Retrieve advance invoice. |
| GET | api/v2/subscriptions/{id}/retrieve_with_scheduled_changes | read | subscriptions | Retrieve a subscription with scheduled changes. |
| GET | api/v2/subscriptions/{id}/scheduled_changes | read | subscriptions | Scheduled_changes a subscription_scheduled_change. |
| GET | api/v2/subscriptions/{id}/subscription_entitlements | read | subscriptions | List subscription entitlements. |
| POST | api/v2/subscriptions/{id}/subscription_entitlements/set_availability | write | subscriptions | Enable or disable subscription entitlements. |
| POST | api/v2/subscriptions/{id}/update_for_items | write | subscriptions | Update a subscription. |
| POST | api/v2/subscriptions/{id}/update_scheduled_changes | write | subscriptions | Update_scheduled_changes a subscription_scheduled_change. |
| GET | api/v2/subscriptions/{id}/usage_charges | read | subscriptions | Retrieve usage charges for a subscription. |
| GET | api/v2/subscriptions/{id}/usage_summary | read | subscriptions | Retrieve usage summary for a subscription. |
| GET | api/v2/subscriptions/{id}/usages | read | subscriptions | **Advanced Usage-Based Billing** For high-scale usage ingestion, use [Advanced Usage-Based Billing](https://www.chargebee.com/docs/billing/2.0/usage-based-billing/understanding-usages) with the... |
| POST | api/v2/subscriptions/{id}/usages | write | subscriptions | **Advanced Usage-Based Billing** For high-scale usage ingestion, use [Advanced Usage-Based Billing](https://www.chargebee.com/docs/billing/2.0/usage-based-billing/understanding-usages) with the... |
| GET | api/v2/time_machines/{id} | read | time_machines | Retrieve a time machine. |
| POST | api/v2/time_machines/{id}/start_afresh | write | time_machines | Start afresh. |
| POST | api/v2/time_machines/{id}/travel_forward | write | time_machines | Travel forward. |
| POST | api/v2/tokens/create_for_card | write | tokens | Create a card payment method token. |
| POST | api/v2/tokens/create_using_temp_token | write | tokens | Create using vault temp token. |
| GET | api/v2/tokens/{id} | write | tokens | Retrieve a token. Kept out of read: returns payment token data. |
| GET | api/v2/transactions | read | transactions | List transactions. |
| POST | api/v2/transactions/create_authorization | write | transactions | Create an authorization payment. |
| GET | api/v2/transactions/{id} | read | transactions | Retrieve a transaction. |
| POST | api/v2/transactions/{id}/delete_offline_transaction | write | transactions | Delete an offline transaction. |
| POST | api/v2/transactions/{id}/reconcile | write | transactions | Reconcile transaction. |
| POST | api/v2/transactions/{id}/record_refund | write | transactions | Record an offline refund. |
| POST | api/v2/transactions/{id}/refund | write | transactions | Refund a payment. |
| POST | api/v2/transactions/{id}/void | write | transactions | Void an authorization transaction. |
| GET | api/v2/unbilled_charges | read | unbilled_charges | List unbilled charges. |
| POST | api/v2/unbilled_charges | write | unbilled_charges | Create unbilled charges for item subscription. |
| POST | api/v2/unbilled_charges/create | write | unbilled_charges | Create unbilled charges for a subscription. |
| POST | api/v2/unbilled_charges/invoice_now_estimate | read | unbilled_charges | Create an estimate for unbilled charges. |
| POST | api/v2/unbilled_charges/invoice_unbilled_charges | write | unbilled_charges | Create an invoice for unbilled charges. |
| POST | api/v2/unbilled_charges/{id}/delete | write | unbilled_charges | Delete an unbilled charge. |
| POST | api/v2/usage_events | write | usage_events | Ingest a usage event. |
| POST | api/v2/usage_files/upload_url | write | usage_files | Retrieve usage file upload URL. |
| GET | api/v2/usage_files/{id}/processing_status | read | usage_files | Retrieve file processing status. |
| GET | api/v2/usages | read | usages | **Advanced Usage-Based Billing** For high-scale usage ingestion, use [Advanced Usage-Based Billing](https://www.chargebee.com/docs/billing/2.0/usage-based-billing/understanding-usages) with the... |
| POST | api/v2/usages/pdf | write | usages | Retrieve usages for an invoice as PDF. |
| GET | api/v2/variants/{id} | read | variants | Retrieve a product variant. |
| POST | api/v2/variants/{id} | write | variants | Update a product variant. |
| POST | api/v2/variants/{id}/delete | write | variants | Delete a product variant. |
| GET | api/v2/vaulted_payment_methods/{id} | read | vaulted_payment_methods | Retrieve vaulted payment method. |
| GET | api/v2/virtual_bank_accounts | read | virtual_bank_accounts | List virtual bank accounts. |
| POST | api/v2/virtual_bank_accounts | write | virtual_bank_accounts | Create a virtual bank account. |
| POST | api/v2/virtual_bank_accounts/create_using_permanent_token | write | virtual_bank_accounts | Create a virtual bank account using permanent token. |
| GET | api/v2/virtual_bank_accounts/{id} | read | virtual_bank_accounts | Retrieve a virtual bank account. |
| POST | api/v2/virtual_bank_accounts/{id}/delete | write | virtual_bank_accounts | Delete a virtual bank account. |
| POST | api/v2/virtual_bank_accounts/{id}/delete_local | write | virtual_bank_accounts | Local delete a virtual bank account. |
| GET | api/v2/webhook_endpoints | read | webhook_endpoints | List webhook endpoints. |
| POST | api/v2/webhook_endpoints | write | webhook_endpoints | Create a webhook endpoint. |
| GET | api/v2/webhook_endpoints/{id} | read | webhook_endpoints | Retrieve a webhook endpoint. |
| POST | api/v2/webhook_endpoints/{id} | write | webhook_endpoints | Update webhook endpoint. |
| POST | api/v2/webhook_endpoints/{id}/delete | write | webhook_endpoints | Delete a webhook endpoint. |
