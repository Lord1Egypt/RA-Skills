# ClickSend access policy

An access policy limits which endpoints ClickSend connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/clicksend#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for ClickSend: its 79 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create clicksend --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v3/account/usage/{id}/{id}/subaccount"},
    {"method": "GET", "path": "v3/recharge/packages"},
    {"method": "GET", "path": "v3/recharge/transactions"},
    {"method": "GET", "path": "v3/recharge/transactions/{id}"},
    {"method": "GET", "path": "v3/lists"},
    {"method": "GET", "path": "v3/lists/{id}"},
    {"method": "GET", "path": "v3/lists/{id}/contacts"},
    {"method": "GET", "path": "v3/lists/{id}/contacts/{id}"},
    {"method": "GET", "path": "v3/countries"},
    {"method": "GET", "path": "v3/delivery-issues"},
    {"method": "POST", "path": "v3/post/letters/detect-address"},
    {"method": "GET", "path": "v3/automations/email/receipts"},
    {"method": "GET", "path": "v3/automations/email/receipts/{id}"},
    {"method": "GET", "path": "v3/email-campaigns"},
    {"method": "POST", "path": "v3/email-campaigns/price"},
    {"method": "GET", "path": "v3/email-campaigns/{id}"},
    {"method": "GET", "path": "v3/email-campaigns/{id}/history"},
    {"method": "GET", "path": "v3/email/addresses"},
    {"method": "GET", "path": "v3/email/addresses/{id}"},
    {"method": "GET", "path": "v3/sms/email-sms"},
    {"method": "GET", "path": "v3/sms/email-sms-stripped-strings"},
    {"method": "GET", "path": "v3/sms/email-sms-stripped-strings/{id}"},
    {"method": "GET", "path": "v3/fax/history"},
    {"method": "POST", "path": "v3/fax/price"},
    {"method": "GET", "path": "v3/fax/receipts"},
    {"method": "GET", "path": "v3/fax/receipts/{id}"},
    {"method": "GET", "path": "v3/automations/fax/receipts"},
    {"method": "GET", "path": "v3/automations/fax/receipts/{id}"},
    {"method": "GET", "path": "v3/country-list"},
    {"method": "GET", "path": "v3/user-countries"},
    {"method": "GET", "path": "v3/automations/fax/inbound"},
    {"method": "GET", "path": "v3/automations/fax/inbound/{id}"},
    {"method": "GET", "path": "v3/automations/sms/inbound"},
    {"method": "GET", "path": "v3/automations/sms/inbound/{id}"},
    {"method": "GET", "path": "v3/email/master-templates"},
    {"method": "GET", "path": "v3/email/master-templates-categories"},
    {"method": "GET", "path": "v3/email/master-templates-categories/{id}"},
    {"method": "GET", "path": "v3/email/master-templates-categories/{id}/master-templates"},
    {"method": "GET", "path": "v3/email/master-templates/{id}"},
    {"method": "GET", "path": "v3/mms/history"},
    {"method": "POST", "path": "v3/mms/price"},
    {"method": "GET", "path": "v3/mms/receipts"},
    {"method": "GET", "path": "v3/mms-campaigns"},
    {"method": "POST", "path": "v3/mms-campaigns/price"},
    {"method": "GET", "path": "v3/mms-campaigns/{id}"},
    {"method": "GET", "path": "v3/numbers"},
    {"method": "GET", "path": "v3/numbers/search/{id}"},
    {"method": "GET", "path": "v3/post/letters/history"},
    {"method": "POST", "path": "v3/post/letters/price"},
    {"method": "GET", "path": "v3/post/postcards/history"},
    {"method": "POST", "path": "v3/post/postcards/price"},
    {"method": "GET", "path": "v3/post/return-addresses"},
    {"method": "GET", "path": "v3/post/return-addresses/{id}"},
    {"method": "GET", "path": "v3/referral/accounts"},
    {"method": "GET", "path": "v3/search/contacts-lists"},
    {"method": "GET", "path": "v3/sms/history"},
    {"method": "GET", "path": "v3/sms/inbound"},
    {"method": "POST", "path": "v3/sms/price"},
    {"method": "GET", "path": "v3/sms/receipts"},
    {"method": "GET", "path": "v3/sms/receipts/{id}"},
    {"method": "GET", "path": "v3/sms/templates"},
    {"method": "GET", "path": "v3/sms-campaigns"},
    {"method": "POST", "path": "v3/sms-campaigns/price"},
    {"method": "GET", "path": "v3/sms-campaigns/{id}"},
    {"method": "GET", "path": "v3/automations/sms/receipts"},
    {"method": "GET", "path": "v3/automations/sms/receipts/{id}"},
    {"method": "GET", "path": "v3/statistics/sms"},
    {"method": "GET", "path": "v3/statistics/voice"},
    {"method": "GET", "path": "v3/timezones"},
    {"method": "GET", "path": "v3/email/history"},
    {"method": "POST", "path": "v3/email/price"},
    {"method": "GET", "path": "v3/email/templates"},
    {"method": "GET", "path": "v3/email/templates/{id}"},
    {"method": "GET", "path": "v3/voice/history"},
    {"method": "GET", "path": "v3/voice/lang"},
    {"method": "POST", "path": "v3/voice/price"},
    {"method": "GET", "path": "v3/voice/receipts"},
    {"method": "GET", "path": "v3/automations/voice/receipts"},
    {"method": "GET", "path": "v3/automations/voice/receipts/{id}"}
  ],
  "deny": []
}
```

## Endpoints

The ClickSend endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v3/account | write | account | Get account information. Kept out of read: response includes the account API key. |
| POST | v3/account | write | account | Create a new account. |
| PUT | v3/account-verify/send | write | account | Send account activation token. |
| PUT | v3/account-verify/verify/{id} | write | account | Verify new account. |
| GET | v3/account/usage/{id}/{id}/subaccount | read | account | Get account useage by subaccount. |
| PUT | v3/forgot-password | write | account | Forgot password. |
| PUT | v3/forgot-password/verify | write | account | Verify forgot password. |
| PUT | v3/forgot-username | write | account | Forgot username. |
| GET | v3/recharge/credit-card | write | account-recharge | Get Credit Card info. Kept out of read: response is the stored payment card information. |
| PUT | v3/recharge/credit-card | write | account-recharge | Update credit card info. |
| GET | v3/recharge/packages | read | account-recharge | Get list of all packages. |
| PUT | v3/recharge/purchase/{id} | write | account-recharge | Purchase a package. |
| GET | v3/recharge/transactions | read | account-recharge | Get all transactions. |
| GET | v3/recharge/transactions/{id} | read | account-recharge | Get specific Transaction. |
| GET | v3/lists | read | contact-lists | Get all contact lists. |
| POST | v3/lists | write | contact-lists | Create new contact list. |
| GET | v3/lists/{id} | read | contact-lists | Get specific contact list. |
| PUT | v3/lists/{id} | write | contact-lists | Update specific contact list. |
| DELETE | v3/lists/{id} | write | contact-lists | Delete a contact list. |
| POST | v3/lists/{id}/import | write | contact-lists | Import contacts to list. |
| PUT | v3/lists/{id}/remove-duplicates | write | contact-lists | Remove duplicate contacts. |
| GET | v3/lists/{id}/contacts | read | contacts | Get all contacts in a list. |
| POST | v3/lists/{id}/contacts | write | contacts | Create new contact. |
| GET | v3/lists/{id}/contacts/{id} | read | contacts | Get a specific contact. |
| PUT | v3/lists/{id}/contacts/{id} | write | contacts | Update specific contact. |
| DELETE | v3/lists/{id}/contacts/{id} | write | contacts | Delete a contact. |
| PUT | v3/lists/{id}/contacts/{id}/copy/{id} | write | contacts | Copy contact to another list. |
| PUT | v3/lists/{id}/contacts/{id}/transfer/{id} | write | contacts | Transfer contact to another list. |
| PUT | v3/lists/{id}/remove-opted-out-contacts/{id} | write | contacts | Remove all opted out contacts. |
| GET | v3/countries | read | countries | Get all country codes. |
| GET | v3/delivery-issues | read | delivery-issues | Get all delivery issues. |
| POST | v3/delivery-issues | write | delivery-issues | Create delivery Issue. |
| POST | v3/post/letters/detect-address | read | detect-address | Detects address in uploaded file. |
| GET | v3/automations/email/receipts | read | email-delivery-receipt-rules | Get all email delivery receipt automations. |
| POST | v3/automations/email/receipts | write | email-delivery-receipt-rules | Create email delivery receipt automations. |
| GET | v3/automations/email/receipts/{id} | read | email-delivery-receipt-rules | Get specific email delivery receipt automation. |
| PUT | v3/automations/email/receipts/{id} | write | email-delivery-receipt-rules | Update email delivery receipt automation. |
| DELETE | v3/automations/email/receipts/{id} | write | email-delivery-receipt-rules | Delete email delivery receipt automation. |
| GET | v3/email-campaigns | read | email-marketing | Get all email campaigns. |
| POST | v3/email-campaigns/price | read | email-marketing | Calculate email campaign price. |
| POST | v3/email-campaigns/send | write | email-marketing | Send email campaign. |
| GET | v3/email-campaigns/{id} | read | email-marketing | Get specific email campaign. |
| PUT | v3/email-campaigns/{id} | write | email-marketing | Edit email campaign. |
| PUT | v3/email-campaigns/{id}/cancel | write | email-marketing | Cancel email campaign. |
| GET | v3/email-campaigns/{id}/history | read | email-marketing | Get specific email campaign history. |
| GET | v3/email-campaigns/{id}/history/export | write | email-marketing | Export specific email campaign history. Kept out of read: generates an export file and returns a download URL. |
| PUT | v3/email/address-verify/{id}/send | write | email-marketing | Send verification token. |
| PUT | v3/email/address-verify/{id}/verify/{id} | write | email-marketing | Verify email address using verification token. |
| GET | v3/email/addresses | read | email-marketing | Get all allowed email addresses. |
| POST | v3/email/addresses | write | email-marketing | Create allowed Email Address. |
| GET | v3/email/addresses/{id} | read | email-marketing | Get specific email address. |
| DELETE | v3/email/addresses/{id} | write | email-marketing | Delete specific email address. |
| GET | v3/sms/email-sms | read | email-to-sms | Get list of email to sms allowed addresses. |
| POST | v3/sms/email-sms | write | email-to-sms | Create email to sms allowed address. |
| GET | v3/sms/email-sms-stripped-strings | read | email-to-sms | Get list of email to sms stripped string rules. |
| POST | v3/sms/email-sms-stripped-strings | write | email-to-sms | Create email to sms stripped string rule. |
| GET | v3/sms/email-sms-stripped-strings/{id} | read | email-to-sms | Get email to sms stripped string rule. |
| PUT | v3/sms/email-sms-stripped-strings/{id} | write | email-to-sms | Update email to sms stripped string rule. |
| DELETE | v3/sms/email-sms-stripped-strings/{id} | write | email-to-sms | Delete email to sms stripped string rule. |
| GET | v3/fax/history | read | fax | Get a list of Fax History. |
| POST | v3/fax/price | read | fax | Calculate Total Price for Fax Messages sent. |
| GET | v3/fax/receipts | read | fax | Get all delivery receipts. |
| POST | v3/fax/receipts | write | fax | Add a delivery receipt. |
| PUT | v3/fax/receipts-read | write | fax | Mark delivery receipts as read. |
| GET | v3/fax/receipts/{id} | read | fax | Get a single fax receipt based on message id. |
| POST | v3/fax/send | write | fax | Send a fax using supplied supported file-types. |
| GET | v3/automations/fax/receipts | read | fax-delivery-receipt-rules | Get all fax delivery receipt automations. |
| POST | v3/automations/fax/receipts | write | fax-delivery-receipt-rules | Create fax delivery receipt automations. |
| GET | v3/automations/fax/receipts/{id} | read | fax-delivery-receipt-rules | Get specific fax delivery receipt automation. |
| PUT | v3/automations/fax/receipts/{id} | write | fax-delivery-receipt-rules | Update fax delivery receipt automation. |
| DELETE | v3/automations/fax/receipts/{id} | write | fax-delivery-receipt-rules | Delete fax delivery receipt automation. |
| GET | v3/country-list | read | global-sending | List of countries. |
| GET | v3/user-countries | read | global-sending | Get Countries for Global Sending. |
| POST | v3/user-countries | write | global-sending | Select Countries for Global Sending. |
| POST | v3/user-countries/agree | write | global-sending | Agree to rules and regulation. |
| GET | v3/automations/fax/inbound | read | inbound-fax-rules | Get all inbound fax automations. |
| POST | v3/automations/fax/inbound | write | inbound-fax-rules | Create new inbound fax automation. |
| GET | v3/automations/fax/inbound/{id} | read | inbound-fax-rules | Get specific inbound fax automation. |
| PUT | v3/automations/fax/inbound/{id} | write | inbound-fax-rules | Update inbound fax automation. |
| DELETE | v3/automations/fax/inbound/{id} | write | inbound-fax-rules | Delete inbound fax automation. |
| GET | v3/automations/sms/inbound | read | inbound-sms-rules | Get all inbound sms automations. |
| POST | v3/automations/sms/inbound | write | inbound-sms-rules | Create new inbound sms automation. |
| GET | v3/automations/sms/inbound/{id} | read | inbound-sms-rules | Get specific inbound sms automation. |
| PUT | v3/automations/sms/inbound/{id} | write | inbound-sms-rules | Update inbound sms automation. |
| DELETE | v3/automations/sms/inbound/{id} | write | inbound-sms-rules | Delete inbound sms automation. |
| GET | v3/email/master-templates | read | master-email-templates | Get all master email templates. |
| GET | v3/email/master-templates-categories | read | master-email-templates | Get all master email template categories. |
| GET | v3/email/master-templates-categories/{id} | read | master-email-templates | Get specific master email template category. |
| GET | v3/email/master-templates-categories/{id}/master-templates | read | master-email-templates | Get all master email templates in a category. |
| GET | v3/email/master-templates/{id} | read | master-email-templates | Get specific master email template. |
| GET | v3/mms/history | read | mms | Get all mms history. |
| GET | v3/mms/history/export | write | mms | Export all mms history. Kept out of read: generates an export file and returns a download URL. |
| POST | v3/mms/price | read | mms | Get Price for MMS sent. |
| GET | v3/mms/receipts | read | mms | Get all delivery receipts. |
| PUT | v3/mms/receipts-read | write | mms | Mark delivery receipts as read. |
| POST | v3/mms/send | write | mms | Send MMS. |
| GET | v3/mms-campaigns | read | mms-campaigns | Get list of mms campaigns. |
| POST | v3/mms-campaigns/price | read | mms-campaigns | Calculate price for mms campaign. |
| POST | v3/mms-campaigns/send | write | mms-campaigns | Create mms campaign. |
| GET | v3/mms-campaigns/{id} | read | mms-campaigns | Get specific mms campaign. |
| PUT | v3/mms-campaigns/{id} | write | mms-campaigns | Update mms campaign. |
| PUT | v3/mms-campaigns/{id}/cancel | write | mms-campaigns | Cancel mms campaign. |
| GET | v3/numbers | read | number | Get all availible dedicated numbers. |
| POST | v3/numbers/buy/{id} | write | number | Buy dedicated number. |
| GET | v3/numbers/search/{id} | read | number | Get all dedicated numbers by country. |
| GET | v3/post/letters/history | read | post-letter | Get all post letter history. |
| GET | v3/post/letters/history/export | write | post-letter | export post letter history. Kept out of read: generates an export file and returns a download URL. |
| POST | v3/post/letters/price | read | post-letter | Calculate post letter price. |
| POST | v3/post/letters/send | write | post-letter | Send post letter. |
| GET | v3/post/postcards/history | read | post-postcard | Retrieve the history of postcards sent or scheduled. |
| GET | v3/post/postcards/history/export | write | post-postcard | Export postcard history to a CSV file. Kept out of read: generates an export file and returns a download URL. |
| POST | v3/post/postcards/price | read | post-postcard | Calculate price for sending one or more postcards. |
| POST | v3/post/postcards/send | write | post-postcard | Send one or more postcards. |
| GET | v3/post/return-addresses | read | post-return-address | Get list of post return addresses. |
| POST | v3/post/return-addresses | write | post-return-address | Create post return address. |
| GET | v3/post/return-addresses/{id} | read | post-return-address | Get specific post return address. |
| PUT | v3/post/return-addresses/{id} | write | post-return-address | Update post return address. |
| DELETE | v3/post/return-addresses/{id} | write | post-return-address | Delete specific post return address. |
| GET | v3/referral/accounts | read | referral-account | Get all referral accounts. |
| GET | v3/reseller/accounts | write | reseller-account | Get list of reseller accounts. Kept out of read: response includes client account API keys. |
| POST | v3/reseller/accounts | write | reseller-account | Create reseller account. |
| GET | v3/reseller/accounts/{id} | write | reseller-account | Get Reseller clients Account. Kept out of read: response includes the client account API key. |
| PUT | v3/reseller/accounts/{id} | write | reseller-account | Update Reseller clients Account. |
| GET | v3/search/contacts-lists | read | search | Get list of searched contact list. |
| PUT | v3/sms/cancel-all | write | sms | Update all scheduled message as cancelled. |
| GET | v3/sms/history | read | sms | Get all sms history. |
| GET | v3/sms/history/export | write | sms | Export all sms history. Kept out of read: generates an export file and returns a download URL. |
| GET | v3/sms/inbound | read | sms | Get all inbound sms. |
| POST | v3/sms/inbound | write | sms | Create inbound sms. |
| PUT | v3/sms/inbound-read | write | sms | Mark inbound SMS as read. |
| PUT | v3/sms/inbound-read/{id} | write | sms | Mark inbound SMS as read. |
| POST | v3/sms/price | read | sms | Calculate sms price. |
| GET | v3/sms/receipts | read | sms | Get all delivery receipts. |
| POST | v3/sms/receipts | write | sms | Add a delivery receipt. |
| PUT | v3/sms/receipts-read | write | sms | Mark delivery receipts as read. |
| GET | v3/sms/receipts/{id} | read | sms | Get a Specific Delivery Receipt. |
| POST | v3/sms/send | write | sms | Send sms message(s). |
| GET | v3/sms/templates | read | sms | Get lists of all sms templates. |
| POST | v3/sms/templates | write | sms | Create sms template. |
| PUT | v3/sms/templates/{id} | write | sms | Update sms template. |
| DELETE | v3/sms/templates/{id} | write | sms | Delete sms template. |
| PUT | v3/sms/{id}/cancel | write | sms | Update scheduled message as cancelled. |
| GET | v3/sms-campaigns | read | sms-campaigns | Get list of sms campaigns. |
| POST | v3/sms-campaigns/price | read | sms-campaigns | Calculate price for sms campaign. |
| POST | v3/sms-campaigns/send | write | sms-campaigns | Create sms campaign. |
| GET | v3/sms-campaigns/{id} | read | sms-campaigns | Get specific sms campaign. |
| PUT | v3/sms-campaigns/{id} | write | sms-campaigns | Update sms campaign. |
| PUT | v3/sms-campaigns/{id}/cancel | write | sms-campaigns | Cancel sms campaign. |
| GET | v3/automations/sms/receipts | read | sms-delivery-receipt-rules | Get all sms delivery receipt automations. |
| POST | v3/automations/sms/receipts | write | sms-delivery-receipt-rules | Create sms delivery receipt automations. |
| GET | v3/automations/sms/receipts/{id} | read | sms-delivery-receipt-rules | Get specific sms delivery receipt automation. |
| PUT | v3/automations/sms/receipts/{id} | write | sms-delivery-receipt-rules | Update sms delivery receipt automation. |
| DELETE | v3/automations/sms/receipts/{id} | write | sms-delivery-receipt-rules | Delete sms delivery receipt automation. |
| GET | v3/statistics/sms | read | statistics | Get sms statistics. |
| GET | v3/statistics/voice | read | statistics | Get voice statistics. |
| GET | v3/subaccounts | write | subaccounts | Get all subaccounts. Kept out of read: response includes each subaccount's API key. |
| POST | v3/subaccounts | write | subaccounts | Create new subaccount. |
| GET | v3/subaccounts/{id} | write | subaccounts | Get specific subaccount. Kept out of read: response includes the subaccount's API key. |
| PUT | v3/subaccounts/{id} | write | subaccounts | Update subaccount. |
| DELETE | v3/subaccounts/{id} | write | subaccounts | Delete a subaccount. |
| PUT | v3/subaccounts/{id}/regen-api-key | write | subaccounts | Regenerate an API Key. |
| GET | v3/timezones | read | timezones | Get supported list of timezones. |
| GET | v3/email/history | read | transactional-email | Get all transactional email history. |
| GET | v3/email/history/export | write | transactional-email | Export all Transactional Email history. Kept out of read: generates an export file and returns a download URL. |
| POST | v3/email/price | read | transactional-email | Get transactional email price. |
| POST | v3/email/send | write | transactional-email | Send transactional email. |
| PUT | v3/reseller/transfer-credit | write | transfer-credit | Transfer Credit. |
| POST | v3/uploads | write | upload | Upload File. |
| GET | v3/email/templates | read | user-email-templates | Get all user email templates. |
| POST | v3/email/templates | write | user-email-templates | Create email template. |
| GET | v3/email/templates/{id} | read | user-email-templates | Get specific user email template. |
| PUT | v3/email/templates/{id} | write | user-email-templates | Update email template. |
| DELETE | v3/email/templates/{id} | write | user-email-templates | Delete user email template. |
| PUT | v3/voice/cancel-all | write | voice | Update all voice messages as cancelled. |
| GET | v3/voice/history | read | voice | Get all voice history. |
| GET | v3/voice/history/export | write | voice | Export voice history. Kept out of read: generates an export file and returns a download URL. |
| GET | v3/voice/lang | read | voice | Get all voice languages. |
| POST | v3/voice/price | read | voice | Calculate voice price. |
| GET | v3/voice/receipts | read | voice | Get all delivery receipts. |
| POST | v3/voice/receipts | write | voice | Add a delivery receipt. |
| PUT | v3/voice/receipts-read | write | voice | Mark delivery receipts as read. |
| POST | v3/voice/send | write | voice | Send voice message(s). |
| PUT | v3/voice/{id}/cancel | write | voice | Update voice message status as cancelled. |
| GET | v3/automations/voice/receipts | read | voice-delivery-receipt-rules | Get all voice delivery receipt automations. |
| POST | v3/automations/voice/receipts | write | voice-delivery-receipt-rules | Create voice delivery receipt automations. |
| GET | v3/automations/voice/receipts/{id} | read | voice-delivery-receipt-rules | Get specific voice delivery receipt automation. |
| PUT | v3/automations/voice/receipts/{id} | write | voice-delivery-receipt-rules | Update voice delivery receipt automation. |
| DELETE | v3/automations/voice/receipts/{id} | write | voice-delivery-receipt-rules | Delete voice delivery receipt automation. |
