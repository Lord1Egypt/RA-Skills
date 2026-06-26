---
name: KYC & Identity
description: Know-Your-Customer verification via MasterPay Global. Submit personal data, upload identity documents, and track approval status.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - AIOT_API_BASE_URL
    primaryEnv: AIOT_API_BASE_URL
---

# KYC & Identity

Use this skill when the user needs to complete identity verification, upload KYC documents, or check verification status.

## Configuration

The default API base URL is `https://payment-api-dev.aiotnetwork.io`. All endpoints are relative to this URL.

To override (e.g. for local development):

```bash
export AIOT_API_BASE_URL="http://localhost:8080"
```

If `AIOT_API_BASE_URL` is not set, use `https://payment-api-dev.aiotnetwork.io` as the base for all requests.

## Available Tools

- `create_masterpay_user` — Create a MasterPay user account (prerequisite for all MasterPay operations) | `POST /api/v1/masterpay/users` | Requires auth
- `get_kyc_status` — Check current KYC verification status and document upload progress | `GET /api/v1/masterpay/kyc/status` | Requires auth
- `get_kyc_metadata` — Get valid document types, occupations, nationalities, and countries for KYC forms | `GET /api/v1/masterpay/kyc/metadata` | Requires auth
- `submit_kyc` — Submit KYC personal data for review (uses profile data) | `POST /api/v1/masterpay/kyc/submit` | Requires auth
- `upload_kyc_document` — Upload a KYC document (passport, ID, proof of address) via multipart or base64 JSON | `POST /api/v1/masterpay/kyc/documents` | Requires auth
- `submit_wallet_kyc` — Submit wallet-level KYC for a card wallet (requires profile phone number and identity document ID number) | `POST /api/v1/masterpay/wallets/kyc` | Requires auth
- `get_profile` — Get user profile data used for KYC submission | `GET /api/v1/profile` | Requires auth
- `update_profile` — Update user profile data (english_first_name, english_last_name, dob, gender, nationality, occupation, source_of_fund, phone_number, phone_country_code, country, address1, address2, address3, city, state, zip, billing_same_as_home) | `PUT /api/v1/profile` | Requires auth
- `get_document` — Get stored identity document info | `GET /api/v1/profile/document` | Requires auth
- `update_document` — Update identity document (fields: identity_type (passport|identity_card), id_number — id_number is required for wallet KYC) | `PUT /api/v1/profile/document` | Requires auth

## Recommended Flows

### Complete KYC Verification

Full flow from profile setup to KYC approval

0. Create MasterPay user: POST /api/v1/masterpay/users — required once before any MasterPay operation
1. Get metadata: GET /api/v1/masterpay/kyc/metadata — learn valid nationalities, occupations, document types
2. Update profile: PUT /api/v1/profile with {english_first_name, english_last_name, dob (YYYY-MM-DD), gender, phone_number, phone_country_code (with '+' prefix, e.g. '+65'), nationality, occupation (use value from metadata endpoint), source_of_fund, country (e.g. 'SG', 'ARGENTINA'), address1, city, state, zip, billing_same_as_home: true}
3. Upload documents: POST /api/v1/masterpay/kyc/documents — JSON body: {document_type, file_data (base64), file_name, mime_type (image/jpeg|image/png|application/pdf)}. Valid document types: PassportFront, PassportBack, NationalIdFront, NationalIdBack, DrivingLicenseFront, DrivingLicenseBack, Selfie, ProofOfAddress. Also supports multipart/form-data with 'file' field.
4. Submit KYC: POST /api/v1/masterpay/kyc/submit — uses profile data, resolves country codes to names, and sends to MasterPay
5. Poll status: GET /api/v1/masterpay/kyc/status — wait for 'approved' (can take minutes to days)


## Rules

- MasterPay user must be created (POST /masterpay/users) before any KYC, wallet, or card operation — this is a one-time setup step
- Profile must include personal info AND address fields (country, address1, city, state) before submitting KYC
- Use country names or ISO alpha-2 codes in the profile country field (e.g. 'SG', 'ARGENTINA') — the backend resolves them to full country names for MasterPay
- Phone country code in profile must include the '+' prefix (e.g. '+65') — MasterPay requires it
- Documents should be uploaded before submission — MasterPay requires passport/ID and proof of address, but our backend does not block submission without them
- KYC review can take minutes to several days — poll status periodically
- Once approved, KYC does not need to be repeated
- Document uploads support both JSON (document_type, file_data as base64, file_name, mime_type) and multipart/form-data (file field + document_type form field) — max 15MB per file

## Agent Guidance

Follow these instructions when executing this skill:

- Always follow the documented flow order. Do not skip steps.
- If a tool requires authentication, verify the session has a valid bearer token before calling it.
- If a tool requires a transaction PIN, ask the user for it fresh each time. Never cache or log PINs.
- Never expose, log, or persist secrets (passwords, tokens, full card numbers, CVVs).
- If the user requests an operation outside this skill's scope, decline and suggest the appropriate skill.
- If a step fails, check the error and follow the recovery guidance below before retrying.

- Before any KYC operation, ensure a MasterPay user exists by calling `create_masterpay_user`. This is a one-time setup. Other MasterPay handlers also auto-create the user, but calling it explicitly is good practice.
- Profile fields use these exact JSON keys: `english_first_name`, `english_last_name`, `dob` (format: YYYY-MM-DD), `gender`, `nationality`, `occupation`, `source_of_fund`, `phone_number`, `phone_country_code`.
- Occupation MUST be a value from the metadata endpoint (`get_kyc_metadata`). Valid values include: GovernmentOfficers, GovernmentWorkers, SoeAndStateOrganExecutives, SoeAndStateOrganEmployees, PrivateBusinessOwnersAndExecutives, PrivateBusinessEmployees, NonGovernmentOrganizationExecutives, NonGovernmentOrganizationEmployees, SoleTraders, Retirees, Students, Unemployed, Freelancer. Always call metadata first to get the current list.
- Complete profile (`update_profile`) with all required fields INCLUDING address fields (country, address1, city, state, zip, billing_same_as_home) before calling `submit_kyc`. The backend validates profile fields are present and returns 400 if any are missing.
- Document upload via JSON requires: `document_type` (e.g. PassportFront, NationalIdFront, Selfie, ProofOfAddress), `file_data` (base64-encoded), `file_name`, `mime_type` (image/jpeg, image/png, or application/pdf). Alternatively, use multipart/form-data with a `file` field and `document_type` form field.
- The `update_document` endpoint (PUT /profile/document) accepts: `identity_type` ("passport" or "identity_card") and `id_number` (passport number, NRIC, etc.). The `id_number` is sent as MasterPay's orgCode during wallet KYC. Always set `id_number` before calling `submit_wallet_kyc`.
- `submit_wallet_kyc` requires: (1) profile with phone_number + phone_country_code, (2) identity document with `id_number` set. It will fail with INCOMPLETE_PROFILE if `id_number` is missing.
- KYC review takes minutes to days. Poll `get_kyc_status` periodically — there are no push notifications.
- Use ISO alpha-2 country codes (e.g., "SG", "MY") for the profile country field. Include the "+" prefix for phone country codes (e.g., "+65").
