# Genius Referrals API Endpoint Catalog

Source: https://api.geniusreferrals.com/doc fetched 2026-07-23 UTC.

Auth header: `X-Auth-Token`

## Resource Groups

- Accounts
- Advocates
- Authentications
- Bonuses
- Campaigns
- Products
- Redemption Requests
- Referrals
- Reports
- Roots
- Tags
- Vouchers
- Widgets Packages

## Endpoints Seen In Public Docs

```text
DELETE /accounts/{account_slug}/advocates
DELETE /accounts/{account_slug}/advocates/{advocate_token}
DELETE /accounts/{account_slug}/advocates/{advocate_token}/referrals/{referral_id}
DELETE /accounts/{account_slug}/bonuses/{bonus_id}
DELETE /accounts/{account_slug}/bonuses/{bonus_id}/tags/{tag_slug}
DELETE /accounts/{account_slug}/products/{product_slug}
DELETE /accounts/{account_slug}/products/{product_slug}/variants/{variant_id}
DELETE /accounts/{account_slug}/tags/{tag_slug}
DELETE /accounts/{account_slug}/vouchers/{voucher_id}
DELETE /accounts/{account_slug}/widgets-packages/{widgets_package_slug}
GET /accounts
GET /accounts/{account_slug}
GET /accounts/{account_slug}/advocates
GET /accounts/{account_slug}/advocates/{advocate_token}
GET /accounts/{account_slug}/advocates/{advocate_token}/payment-methods
GET /accounts/{account_slug}/advocates/{advocate_token}/payment-methods/{advocate_payment_method_id}
GET /accounts/{account_slug}/advocates/{advocate_token}/referrals
GET /accounts/{account_slug}/advocates/{advocate_token}/referrals/{referral_id}
GET /accounts/{account_slug}/advocates/{advocate_token}/share-links
GET /accounts/{account_slug}/bonuses
GET /accounts/{account_slug}/bonuses/checkup
GET /accounts/{account_slug}/bonuses/traces
GET /accounts/{account_slug}/bonuses/traces/{trace_id}
GET /accounts/{account_slug}/bonuses/{bonus_id}
GET /accounts/{account_slug}/campaigns
GET /accounts/{account_slug}/campaigns/{campaign_slug}
GET /accounts/{account_slug}/products
GET /accounts/{account_slug}/products/{product_slug}
GET /accounts/{account_slug}/products/{product_slug}/variants
GET /accounts/{account_slug}/products/{product_slug}/variants/{variant_id}
GET /accounts/{account_slug}/redemption-requests
GET /accounts/{account_slug}/redemption-requests/{redemption_request_id}
GET /accounts/{account_slug}/tags
GET /accounts/{account_slug}/tags/{tag_slug}
GET /accounts/{account_slug}/vouchers
GET /accounts/{account_slug}/vouchers/denominations/{currency_code}
GET /accounts/{account_slug}/vouchers/{voucher_id}
GET /accounts/{account_slug}/widgets-packages
GET /accounts/{account_slug}/widgets-packages/{widgets_package_slug}
GET /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets
GET /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets/{widget_id}
GET /reports/1099-tax-report
GET /reports/bonuses-daily-given
GET /reports/bonuses-summary-per-origin
GET /reports/click-daily-participation
GET /reports/referral-daily-participation
GET /reports/referrals-summary-per-origin
GET /reports/revenue
GET /reports/share-daily-participation
GET /reports/top-advocates
GET /test-authentication
GET /utilities/bonuses-redemption-methods
GET /utilities/bonuses-redemption-methods/{bonuses_redemption_method_slug}
GET /utilities/currencies
GET /utilities/currencies/{code}
GET /utilities/payment-methods
GET /utilities/redemption-request-actions
GET /utilities/redemption-request-actions/{redemption_request_action_slug}
GET /utilities/redemption-request-statuses
GET /utilities/redemption-request-statuses/{redemption_request_status_slug}
GET /utilities/referral-origins
GET /utilities/referral-origins/{referral_origin_slug}
PATCH /accounts/{account_slug}/advocates/{advocate_token}
PATCH /accounts/{account_slug}/bonuses/{bonus_id}
PATCH /accounts/{account_slug}/products/{product_slug}
PATCH /accounts/{account_slug}/products/{product_slug}/variants/{variant_id}
PATCH /accounts/{account_slug}/products/{product_slug}/variants/{variant_id}/prices/{currency_code}
PATCH /accounts/{account_slug}/redemption-requests/{redemption_request_id}
PATCH /accounts/{account_slug}/redemption-requests/{redemption_request_id}/redemption
PATCH /accounts/{account_slug}/tags/{tag_slug}
PATCH /accounts/{account_slug}/vouchers/{voucher_id}
PATCH /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets/{widget_id}
PATCH /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets/{widget_id}/translations/{locale}
POST /accounts/{account_slug}/advocates
POST /accounts/{account_slug}/advocates/{advocate_token}/payment-methods
POST /accounts/{account_slug}/advocates/{advocate_token}/referrals
POST /accounts/{account_slug}/bonuses
POST /accounts/{account_slug}/bonuses/force
POST /accounts/{account_slug}/bonuses/{bonus_id}/tags
POST /accounts/{account_slug}/products
POST /accounts/{account_slug}/products/{product_slug}/variants
POST /accounts/{account_slug}/redemption-requests
POST /accounts/{account_slug}/tags
POST /accounts/{account_slug}/vouchers
POST /accounts/{account_slug}/widgets-packages
POST /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets
POST /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets/{widget_id}/translations
PUT /accounts/{account_slug}/advocates/{advocate_token}
PUT /accounts/{account_slug}/advocates/{advocate_token}/payment-methods/{advocate_payment_method_id}
PUT /accounts/{account_slug}/advocates/{advocate_token}/referrals/{referral_id}
PUT /accounts/{account_slug}/products/{product_slug}
PUT /accounts/{account_slug}/products/{product_slug}/variants/{variant_id}
PUT /accounts/{account_slug}/tags/{tag_slug}
PUT /accounts/{account_slug}/widgets-packages/{widgets_package_slug}
PUT /accounts/{account_slug}/widgets-packages/{widgets_package_slug}/widgets/{widget_id}
```
