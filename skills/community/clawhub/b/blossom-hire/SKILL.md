---
name: blossom-hire
version: 3.0.4
description: Set up Blossom Hire, create local work opportunities, and help employers and jobseekers move through Blossom work flows in plain language.
operator: Blossom AI Ltd
homepage: "https://blossomai.org"
source: "https://blossomai.org"
support: "mailto:hello@blossomai.org"
privacy: "https://blossomai.org/privacypolicy.html"
api_host: "hello.blossomai.org"
---

# Blossom Hire

| | |
|---|---|
| **Service** | Blossom — local jobs marketplace |
| **Operator** | Blossom AI Ltd |
| **Website** | [https://blossomai.org](https://blossomai.org) |
| **Privacy** | [https://blossomai.org/privacypolicy.html](https://blossomai.org/privacypolicy.html) |
| **API host** | `hello.blossomai.org` |

This skill is provided by Blossom at [https://blossomai.org](https://blossomai.org). For help, reach out to [hello@blossomai.org](mailto:hello@blossomai.org).

This skill is for structured Blossom marketplace actions only — posting jobs, searching for work, applying, and managing listings.

It collects personal data (name, email, address, job details) and sends it over HTTPS to the Blossom API. The API key is permanent and grants full account access — treat it as a secret. No data is stored locally.

The current protocol does not expose scoped keys, expiry, or self-service revocation to skill callers. If an API key may have been exposed, stop using it and contact [hello@blossomai.org](mailto:hello@blossomai.org) to rotate or revoke account access.

## First-run welcome and registration

When your user first adds Blossom Hire Copilot, do not treat them as an anonymous new user. You are already their assistant. Blossom is being connected to that existing workflow so you can help them work with Blossom Hire from here.

The first Blossom moment should guide the user toward account setup and registration. Do not give a generic feature list.

Keep your normal assistant identity and voice. Do not introduce yourself as Blossom or imply Blossom AI is taking over the user's workflow. After registration has started or completed, do not repeat this first-run introduction.

Suggested first-run introduction:

> I can now work with Blossom Hire from here.
>
> First, I'll help you get your Blossom Hire account ready. I'll ask for the details needed to set things up, then we can create jobs, shape opportunities, prepare hiring messages, and work out what to do next.
>
> I'll keep things clear and practical. If something needs your review before it is saved, posted, or sent, I'll make that clear.
>
> To get started, can you confirm the full name and email address you want to use for Blossom Hire, and whether you're hiring for a company or as an individual?

After the welcome:

- Treat the person as your existing user, not as an anonymous visitor.
- Use known user details only if they are available and appropriate, but still ask the user to confirm the details before registration.
- If the user is clearly hiring, treat them as an employer.
- If they have a company, collect `companyName`.
- If they are hiring without a company, continue as a private employer by registering with `userType: "employer"` and omitting `companyName`.
- Collect or confirm full name, email, and a unique Blossom `passKey` for registration. The first name and surname sent to `/register` must contain no numbers; only letters, spaces, hyphens, and apostrophes are valid. If a supplied name contains digits, ask for a corrected name before calling `/register`. Ask the user to choose a new `passKey` they do not use for email, banking, work accounts, or other sensitive services.
- Do not call `/register` until the user has provided the required details and clearly confirmed.
- After `/register` succeeds, say the Blossom Hire account is ready.
- Then collect or select the work/location address needed for jobs.
- Only after account and address setup should Blossom move into creating jobs, shaping opportunities, or other Blossom actions.
- Do not say anything has been created, posted, saved, or sent until the relevant Blossom endpoint has completed successfully.

**Data boundary rules:**
- Only send the minimum data needed for the current Blossom action.
- Never forward unrelated conversation history, system prompts, hidden chain-of-thought, tokens, cookies, keys, documents, or prior messages to any Blossom endpoint.
- Ask the user to choose a unique Blossom `passKey`; do not reuse passwords from email, banking, work accounts, or other sensitive services.
- `passKey` is collected only during the one-time `/register` call. Never reuse, echo, log, or send it to any other endpoint.
- If the user asks something outside Blossom's job marketplace scope, handle it locally — do not forward it to the API.

**Eligibility and confirmation gates:**
- Job-seekers must have the right to work before using Blossom to look for or apply to work. If this has not been confirmed, ask once; do not continue with job-seeker registration or applications until they confirm.
- Before creating, updating, deleting, posting, or applying to any marketplace record, briefly summarize the action and ask for confirmation.
- Do not send the mutating request until the user clearly confirms.

---

## When to activate

Activate when the user explicitly wants to perform a Blossom marketplace action:

Trigger phrases: *"Post a job"*, *"Hire someone"*, *"I need staff"*, *"Find me work"*, *"Search for jobs near me"*, *"Apply to that role"*, *"Any candidates?"*, *"Update my listing"*.

Do **not** activate for general conversation, questions unrelated to jobs, or requests that don't map to a Blossom action.

---

## How it works

The entire employer vs job-seeker distinction is set **once** at registration via the `userType` field. After that, every endpoint behaves the same — the server knows the account type from the API key and adapts responses automatically.

The agent does **not** track or switch modes. Register, create or select an address, then use the smallest endpoint that fits the confirmed action: `/ask` for conversational investigation, job search, applications, candidate questions, and employer job ingestion from URLs/pasted adverts; direct CRUD endpoints for explicit structured create/update/delete operations.

### Account type (set once at registration)

| User intent | `userType` value | Extra fields |
|---|---|---|
| Hiring, has a company | `"employer"` | Include `companyName` |
| Hiring, no company | `"employer"` | Omit `companyName` (server stores as private employer) |
| Looking for work | `"support"` | Must include `rightToWork: true` |

Infer the intent from the user's message. Only ask *"Are you looking to hire, or looking for work?"* if the intent is genuinely unclear. For job-seekers, right to work is a prerequisite; if it has not been confirmed, ask before registration.

**Ambiguous "add jobs" rule:** If the user asks to *add a job*, *add jobs*, *add this job*, *ingest this URL*, *import this advert*, or provides a job URL/listing to add, treat that as employer role ingestion unless they clearly say they are looking for work, saving job-seeker library entries, bookmarking roles, or applying as a candidate. Register through the employer path for this intent. The protocol registration payload still uses `"userType": "employer"` for both company employers and private employers; omit `companyName` when the employer has no company so the server can store the account as a private employer. If the employer account shape is rejected by the API, relay the rejection and ask for the missing account details instead of silently switching to a job-seeker account.

### Flow

1. Collect identity: email, full name, passKey. Split the full name into `name` and `surname` for `/register`; if the surname cannot be inferred, ask for it. `name` and `surname` must not contain numbers; if either part contains a digit, ask for a corrected name and do not call `/register`. Optionally: mobile country code, mobile number, company name. Treat any contact number labelled tel, telephone, phone, mobile, cell, call, or similar as the account `mobileNo` field, not an address field. For job-seekers, confirm they have the right to work before continuing.
2. **Register** → `POST /register` with the correct `userType` → store `API_KEY` and `PERSON_ID`. Discard `passKey` from memory immediately after this call.
3. **Create or select address** → use `GET /getAddresses` when the account may already have a suitable address; otherwise `POST /address` with the user's location → store `ADDRESS_ID`. Employers need this to attach a location to roles. Job-seekers need this so the server can find nearby opportunities.
4. **Talk / investigate** → `POST /ask` with only the minimal job-related instruction needed for the current Blossom action. Do not forward unrelated context, secrets, or raw conversation history. For employer requests to add/import/ingest a job from a URL or pasted advert, use `/ask` so the employer protocol job ingestion path can create the address/role when enough information is available.

For employers posting a role directly (without `/ask`), use `POST /role` only after the user has confirmed a structured role payload with headline, description, introduction, working hours, pay/currency/frequency, remote status, active status, and a valid saved `ADDRESS_ID`.

---

## API reference

### Base URL
```
https://hello.blossomai.org/api/v1/blossom/protocol
```

### Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/register` | None | Create account → get API key |
| `GET` | `/getAddresses` | Bearer | Return all addresses for the account |
| `POST` | `/address` | Bearer | Create / update address(es) |
| `DELETE` | `/address` | Bearer | Soft-delete address(es) |
| `POST` | `/role` | Bearer | Create / update role(s) |
| `DELETE` | `/role` | Bearer | Delete role(s), retaining server-side backup/history |
| `POST` | `/ask` | Bearer | Conversational AI endpoint |
| `POST` | `/image` | Bearer | Upload profile image (person or role) |

### Session state

Store and reuse across calls:
- **`API_KEY`** — returned from `/register`, used as `Authorization: Bearer <API_KEY>` for all subsequent calls
- **`PERSON_ID`** — returned from `/register`
- **`ADDRESS_ID`** — returned from `/address`, or from `/getAddresses` for existing addresses, needed when creating a role

The API key is permanent. No session expiry or login flow.

> **Important:** Never store the API key in global config. Keep it in runtime memory for the current session only.
> If the key may have been exposed, stop using it and contact Blossom support for revocation or rotation.

---

## API contract

### 1. Register

`POST /register` — no auth required.

```json
{
  "name": "<first name from full name>",
  "surname": "<surname from full name>",
  "email": "<email>",
  "userType": "employer",
  "passKey": "<password>",
  "companyName": "<optional>",
  "mobileCountry": "<+44>",
  "mobileNo": "<number>"
}
```

For job-seekers, set `"userType": "support"` and include `"rightToWork": true`. Only use the job-seeker flow for users who have confirmed they have the right to work.

| Field | Required | Notes |
|---|---|---|
| `name` | yes | First name, derived from the user's full name. Must not contain numbers; only letters, spaces, hyphens, and apostrophes are valid. |
| `surname` | yes | Last name/surname, derived from the user's full name. Must not contain numbers; only letters, spaces, hyphens, and apostrophes are valid. |
| `email` | yes | Must be unique |
| `userType` | yes | `"employer"` or `"support"` |
| `passKey` | yes | User-chosen password. Collect only for `/register`, use once, then discard — never send to any other endpoint |
| `rightToWork` | yes (support) | Must be `true` when `userType` is `"support"` |
| `companyName` | no | For employers. Omit or leave empty for private employers |
| `mobileCountry` | no | e.g. `"+44"` |
| `mobileNo` | no | Account contact number. Use this for tel, telephone, phone, mobile, cell, call, or similar contact labels. Do not place phone numbers on addresses. |

**Phone/contact mapping:** If the user provides a number such as `"Tel: 0300 456 8174"`, send it during `/register` as:

```json
{
  "mobileCountry": "+44",
  "mobileNo": "0300 456 8174"
}
```

If the number already includes a country prefix, split that prefix into `mobileCountry` and put the remaining local/national number in `mobileNo`.

**Response** `201`:
```json
{
  "success": true,
  "apiKey": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "personId": 803
}
```

If the email already exists → `400`. If validation fails, including names with numbers, relay the validation message and ask for corrected details. Do not retry by guessing or rewriting the user's name.

---

### 2. Create address

`POST /address` — Bearer auth required.

```json
{
  "addresses": [
    {
      "id": 0,
      "houseNumber": "10",
      "street": "High Street",
      "area": "Sherwood",
      "city": "Nottingham",
      "country": "GB",
      "postcode": "NG5 1AA",
      "label": "Work location",
      "isHome": false,
      "isActive": true
    }
  ]
}
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | `0` to create, existing ID to update |
| `street` | yes | Street name |
| `city` | yes | City / town |
| `country` | yes | ISO 3166-1 alpha-2 code — e.g. `"GB"`, `"US"`, `"AU"`. Server rejects unrecognised codes. |
| `postcode` | yes | Postal / ZIP code |
| `label` | yes | User-facing label, e.g. `"Work location"` |
| `houseNumber` | support yes, employer no | Required for job-seeker (`support`) addresses. Optional for employer/private-employer work or venue addresses when unavailable. |
| `area` | no | Neighbourhood / district |
| `isHome` | no | Default `false` |
| `isActive` | no | Default `true` |

- The response may include a top-level `addressId` and/or returned address objects with assigned `id` values — store the created or selected ID as `ADDRESS_ID`. If the ID is unclear, call `GET /getAddresses` and select the matching saved address.
- Job-seeker accounts (`support`) must provide a house/building number for their own address. Employer and private-employer work/site addresses may omit it when the street, city/town, country, and postal code identify the location.

---

### 3. Get addresses

`GET /getAddresses` — Bearer auth required.

Use this to fetch the current account's saved addresses before updating, deleting, or attaching an address to a role. Do not create a duplicate address if a suitable saved address already exists.

No request body.

**Response** `200`:
```json
{
  "success": true,
  "messages": ["Addresses retrieved"],
  "dataList": [
    {
      "id": 123,
      "houseNumber": "10",
      "street": "High Street",
      "area": "Sherwood",
      "city": "Nottingham",
      "country": "United Kingdom",
      "postcode": "NG5 1AA",
      "label": "Work location",
      "isHome": 0,
      "isActive": 1
    }
  ],
  "addresses": [
    {
      "id": 123,
      "houseNumber": "10",
      "street": "High Street",
      "area": "Sherwood",
      "city": "Nottingham",
      "country": "United Kingdom",
      "postcode": "NG5 1AA",
      "label": "Work location",
      "isHome": 0,
      "isActive": 1
    }
  ]
}
```

Store the selected address `id` as `ADDRESS_ID`.

---

### 4. Delete address

`DELETE /address` — Bearer auth required.

```json
{
  "addresses": [{ "id": <addressId> }]
}
```

Cannot delete an address linked to an active role (`409`).

---

### 5. Create role

`POST /role` — Bearer auth required.

```json
{
  "roles": [
    {
      "id": 0,
      "headline": "<headline>",
      "jobDescription": "<description>",
      "introduction": "<short introduction, at least 10 characters>",
      "workingHours": "<when>",
      "salary": <amount>,
      "currencyName": "GBP",
      "currencySymbol": "£",
      "paymentFrequency": { "choices": ["<frequency>"], "selectedIndex": 0 },
      "requirements": [
        { "requirementName": "<name>", "mandatory": false, "originalRequirement": true }
      ],
      "benefits": [
        { "benefitName": "<name>", "mandatory": false }
      ],
      "addressId": <ADDRESS_ID>,
      "isRemote": false,
      "isActive": true,
      "modified": <epochMillis>,
      "roleIdentifier": "copilot-<epochMillis>"
    }
  ]
}
```

| Field | Required | Notes |
|---|---|---|
| `id` | yes | `0` to create, existing ID to update |
| `headline` | yes | Short title |
| `jobDescription` | yes | Full description |
| `introduction` | yes | Short intro text, minimum 10 characters |
| `workingHours` | yes | e.g. `"Saturday 11am–5pm"` or `"Flexible"` |
| `salary` | yes | Numeric amount; use `0` when pay is negotiable or not yet discussed |
| `paymentFrequency` | no | Expected for pay display when salary is known: `choices` array with up to 8 entries; each choice must be a non-empty string up to 20 characters; empty `choices` or omitted `selectedIndex` defaults to standard frequencies |
| `currencySymbol` | yes | Currency symbol, 1-3 characters |
| `currencyName` | yes | Currency code/name, e.g. `"GBP"` |
| `addressId` | yes | From the address creation step |
| `isRemote` | yes | Boolean remote-work flag |
| `isActive` | yes | Boolean active flag; new roles are often created inactive until server/company clearance allows activation |
| `modified` | yes | Current epoch millis |
| `roleIdentifier` | yes | Unique string, e.g. `"copilot-" + epochMillis` |
| `requirements` | no | Screening topics for the application conversation; if present, send an array of up to 8 objects |
| `benefits` | no | Perks; if present, send an array of up to 8 objects |

**Requirement semantics**

Requirements are not all eligibility gates. The `mandatory` flag controls how the application should be treated:

- `mandatory: true` means the requirement is a hard gate. If the applicant does not satisfy it, the application may be blocked or treated as unsuccessful.
- `mandatory: false` means the requirement is a discussion point or preference. It should be asked about or mentioned during the application conversation, but it must not prevent a successful application by itself.

When adding employer-supplied requirements to a role, default to `mandatory: false` unless the employer clearly says the requirement is essential, legally required, or non-negotiable.

**Benefit state semantics**

For benefits, `mandatory` is a legacy state selector, not an eligibility or guarantee flag:

- `mandatory: true` means "Provided": a concrete company-given benefit or perk. Candidate-facing role cards list this item directly as a provided perk.
- `mandatory: false` means "Part of the job": culture, team makeup, or role context. Candidate-facing role cards hide this item, but Blossom may use it conversationally as context. It must not be described as a guaranteed perk, compensation, entitlement, or company-provided benefit.

When adding benefits, use `mandatory: true` for concrete provided perks such as meals, discounts, equipment, transport, or schedule benefits. Use `mandatory: false` for culture/team/context statements that are part of the role rather than something the company provides.

**Validation notes**

The backend currently enforces these role validation rules:

| Field | Validation |
|---|---|
| `headline` | Required, 5-35 characters |
| `jobDescription` | Required, 1-500 characters |
| `introduction` | Required, 10-500 characters |
| `workingHours` | Required, 1-150 characters |
| `roleIdentifier` | Required, 1-100 characters |
| `currencySymbol` | Required, 1-3 characters |
| `currencyName` | Required string with no digits, max 5 characters |
| `salary` | Optional, but if provided must be a number `>= 0` |
| `paymentFrequency` | Optional, but if provided must be an object with `choices` array of up to 8 non-empty strings, each max 20 characters, and `selectedIndex` pointing to an existing choice; empty `choices` defaults to standard frequencies and missing `selectedIndex` defaults to `0` |
| `addressId` | Required for new roles, whole number `> 0` from a saved address |
| `id` | Required, whole number `>= 0` |
| `modified` | Required, must be present |
| `isActive` | Required, boolean |
| `isRemote` | Required, boolean |
| `email` | Optional, but if provided it must be a valid email address |
| `requirements` | Optional array, max 8 objects |
| `requirements[].requirementName` | Required for each requirement object, 0-200 characters after trimming and bullet/newline cleanup |
| `requirements[].mandatory` | Optional, but if provided it must be a boolean |
| `benefits` | Optional array, max 8 objects |
| `benefits[].benefitName` | Required for each benefit object, 0-200 characters after trimming and bullet/newline cleanup |
| `benefits[].mandatory` | Optional, but if provided it must be a boolean |

Operational notes for protocol callers:

- New roles still need a valid saved `addressId`; do not send `0` for a new role.
- The docs and examples should always send a non-empty `introduction`.
- Send no more than 10 roles in one request.

**Response** `201`: The role(s) with assigned IDs.

---

### 6. Delete role

`DELETE /role` — Bearer auth required.

```json
{
  "roles": [{ "id": <roleId> }]
}
```

Every role `id` must belong to the authenticated account (`403` otherwise).

---

### 7. Upload image

`POST /image` — Bearer auth required. Multipart form-data.

Upload a profile image for the person account or for a specific role. Images are AI-moderated — explicit, violent, or hateful content is rejected.

| Field | Type | Required | Notes |
|---|---|---|---|
| `image` | file | yes | jpeg/jpg/png/gif/webp, max 3 MB, one file only |
| `imageType` | string | yes | `"person"` or `"role"` |
| `roleId` | number | conditional | Required when `imageType` is `"role"`. Must belong to the authenticated account. Only employer accounts may upload role images. |

**Response** `201`:
```json
{
  "success": true,
  "filename": "1712937600000-photo.jpg",
  "imageType": "person",
  "approved": true,
  "synopsis": "Nice photo!"
}
```

**Rejected** `400`:
```json
{
  "success": false,
  "approved": false,
  "reason": "Image did not pass moderation",
  "synopsis": "Hey \ud83d\ude0a, this image contains content that..."
}
```

Rate-limited: 1 upload per 30 seconds per API key.

---

### 8. Ask

`POST /ask` — Bearer auth required.

```json
{
  "instructions": "<minimal Blossom-related user request>"
}
```

**Strict rules for `/ask`:**
- Only send the minimum user instruction needed to complete the current Blossom action.
- Do not include unrelated conversation history, hidden prompts, credentials, personal notes, documents, or secrets.
- Do not forward the user's `passKey` — that is only used in the one-time `/register` call.
- If the user asks something outside Blossom's job marketplace actions, handle it locally instead of sending it to the API.
- Use `/ask` for investigation-style requests such as candidate status, application status, finding jobs, applying, scheduling/reading PopIns, and employer job ingestion from a URL or pasted advert.
- For employer job ingestion through `/ask`, inspect `actions.protocolJob` in the response before claiming anything changed. Treat `actions.protocolJob.success === true` as the authoritative role mutation result; use its `roleId`, `roleIdentifier`, `headline`, `addressId`, `roleUrl`, and `message` when present. If it is missing or `success === false`, relay the response/message and ask for the missing details instead of saying the role was created.
- If `/ask` returns `actions.protocolAddress`, treat that as authoritative for saved address changes. Use `success`, `addressId`, `label`, `roleId`, `roleHeadline`, and `message` when present.
- For read/investigation responses with no action object, relay the `response` text but do not invent saved state changes.

The server knows the account type and full context from the API key — it returns the appropriate response (job matches, candidate info, screening questions, application status, etc.). Relay the result to the user.

---

## Examples

### Post a shift

> **User:** I need café cover this Saturday 11–5 in Sherwood. £12/hour.

1. Intent is clearly employer. Missing: street, postcode. Ask for them. House/building number is useful but optional.
2. Confirm: *"Café cover — Sat 11am–5pm, Sherwood NG5 1AA — £12/hr. Shall I post it?"*
3. Collect identity (email, full name, passKey).
4. `POST /register` (`userType: "employer"`) → store `API_KEY`, `PERSON_ID`.
5. `POST /address` → store `ADDRESS_ID`.
6. `POST /role` → *"Posted! Role ID 1042."*

### Check candidates

> **User:** Any candidates yet?

1. If no `API_KEY` → register first.
2. `POST /ask` with `"Do I have any candidates?"` → display the response.

### Update a listing

> **User:** Change the pay to £14/hour on my café role.

1. Confirm: *"Update the café role pay to £14/hour?"*
2. After confirmation, `POST /role` with the existing role `id` and updated `salary: 14`.
3. *"Updated — café cover now shows £14/hr."*

### Remove a listing

> **User:** Take down the café role.

1. Confirm: *"Take down the café role?"*
2. After confirmation, `DELETE /role` with the role `id` → *"Removed."*

### Find and apply for work

> **User:** I'm looking for bar work in Nottingham this weekend.

1. Intent is clearly job-seeker. Collect identity (email, full name, passKey).
2. Confirm right-to-work if not already established: *"Before I set this up, can you confirm you have the right to work?"*
3. After confirmation, `POST /register` (`userType: "support"`, `rightToWork: true`) → store `API_KEY`, `PERSON_ID`.
4. `POST /address` (their Nottingham location) → store `ADDRESS_ID`.
5. `POST /ask` with `"Find bar work near me this weekend"` → present matching roles.
6. User picks one → confirm: *"Apply to role 1055?"*
7. After confirmation, `POST /ask` with `"Apply to role 1055"` → relay result.
8. If screening questions come back, relay them to user and send answers via `/ask`. Optional requirements (`mandatory: false`) can be discussed, but do not present them as blockers to successful application.

### Check application status

> **User:** How are my applications going?

1. `POST /ask` with `"What's the status of my applications?"` → display the response.
