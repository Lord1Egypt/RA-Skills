---
name: "clawtip"
description: >
  Executes a clawtip payment transaction for third-party skills.
  Trigger this tool strictly when a third-party service initiates a valid clawtip payment request, when the user explicitly requests creation of a clawtip payment user token, or when the user asks to view their clawtip wallet (DO NOT TRIGGER WITHOUT A VALID CONDITION).
  When the user requests to view their clawtip wallet (e.g., "查看我的clawtip钱包", "查看钱包", "打开clawtip钱包"), provide the wallet link:https://clawtip.jd.com/qrcode?bizUrl=https://jpay.jd.com/ecnya2a/claw/index
  Runtime dependency: Node.js (`node`) must be installed on the host system prior to deployment — it is required by the bundled JS encryption tooling.
  Security notice: the `u` is persisted as plaintext JSON in `configs/config.json`; restrict OS-level file permissions in security-sensitive environments.
metadata:
    author: "payment-infra-rd"
    category: "payment_utilities"
    capabilities:
        - "payment.process"
    permissions:
        - "network.outbound"
        - "credential.read"
        - "credential.write"
    required_binaries:
        - "node"
    required_env: []
    credential_storage:
        type: "local_file"
        path: "configs/config.json"
        format: "plaintext_json"
        fields: ["u"]
    invocation_policy:
        disable_model_invocation: false
        allowed_triggers:
            - "third_party_skill_payment_request"
            - "user_explicit_token_creation"
            - "user_explicit_wallet_view"
            - "user_explicit_register_status_query"
        prohibited_triggers:
            - "speculative_or_predictive_invocation"
            - "ambient_context_without_explicit_request"
---


# Process the Payment Request

## 1. Required Parameters

Provide the following parameters strictly according to their defined formats:

* **`order_no`** (string, **required**): The order number from the calling skill's Phase 1 (order creation).
* **`indicator`** (string, **required**): The indicator value from the calling skill's Phase 1, typically an MD5 hash of the skill name.

> [!NOTE]
> The script will automatically locate the order JSON file from the fixed directory based on `order_no` and `indicator`:
> - Linux/macOS: `/root/openclaw/skills/orders/{indicator}/{order_no}.json`
> - Windows: `C:\openclaw\skills\orders\{indicator}\{order_no}.json`
>
> This JSON file is written by the calling skill's order creation phase and contains all payment-related fields (`payTo`, `encrypted_data`, `amount`, `order_no`, `question`, `description`, `skill_name`, `resource_url`, etc.).
>
> **You (the LLM) MUST NOT open, read, parse, or extract any values from this file.** The script handles all file reading internally. Your only responsibility is to pass `order_no` and `indicator` as command-line arguments.

## 2. Hyperparameters

* **`skill-version`** (string): The version of the skill. Currently set to `1.0.8`.

## 3. Execution Command

Execute the script using the following bash command. Replace the placeholders `<...>` with the validated parameter values. Wrap parameters that may contain spaces in quotes.

```bash
python3 scripts/payment_process.py <order_no> <indicator> <skill-version>
```

## 4. Result Processing Rules

Analyze the standard output of the execution command and strictly follow these response protocols **in the given order**. **Stop at the first matching step; do not continue to subsequent steps.**

### ⚡ Global Priority Rule

> If the output contains `已获取到支付凭证`, **go to Step 2 (Obtain Credential) first** to return the order number to the calling skill. The credential has already been saved to the order file by the script, and the calling skill will read it from there for decryption.
>
> **However**, if the output **also** contains `授权链接: <AUTH_URL>` or `鉴权链接: <AUTH_URL>`, you **MUST preserve** the full original output (including the authorization/authentication URL) in memory. This is because the credential may decrypt to a **failed** status, in which case you will need to **fall back to Step 3** using the preserved authorization/authentication URL.
>
> **In summary:**
> 1. If `已获取到支付凭证` is present → go to **Step 2** first.
> 2. After the calling skill decrypts the credential and reports the status:
>    - If the decrypted status is **成功** → go to **Step 4 Case A**. Done.
>    - If the decrypted status is **处理中** → go to **Step 4 Case B**. Done.
>    - If the decrypted status is **失败 (FAIL)** → go to **Step 2.1 (Credential Decryption Fallback)** to check whether a preserved `授权链接:` or `鉴权链接:` exists, and if so, fall back to **Step 3**.
> 3. If `已获取到支付凭证` is **NOT** present → evaluate **Step 1**, then **Step 3** in order.

---

### **Step 1 — Network/System Failure (check first)**

* **Trigger:** The output contains `网络或系统异常:`.
* **Action:** Report the specific error returned by the script. Additionally, if the output contains `返回消息: <MESSAGE>`, display the `<MESSAGE>` to the user as supplementary error context. Advise the user on the next steps. **Stop here; do not proceed to Step 2.**

---

### **Step 2 — Obtain Credential**

* **Trigger:** The output contains `已获取到支付凭证` and `订单号: <ORDER_NO>`.
* **Meaning:** The HTTP request reached the server successfully. The credential (an encrypted blob containing the actual payment status) has been saved to the order file by the script. The calling skill will read it from there for decryption.
* **Action:**
  1. **Preserve the full original script output** in memory (including any `授权链接:` or `鉴权链接:` if present, and any `返回消息:` if present). You may need it later in Step 2.1.
  2. Return the order number to the calling skill for further processing:
     > **订单号：** `<ORDER_NO>`
     
     将此订单号返回给调用方 skill，由调用方根据订单号从订单文件中读取支付凭证并解密，再根据其中的支付状态进行后续处理。

* **After returning the order number:** Wait for the calling skill to report the decrypted `PAY_STATUS`. Then proceed to **Step 4** to route by decrypted status. If the status is **失败 (FAIL)**, Step 4 Case C will direct you to **Step 2.1**.

---

### **Step 2.1 — Credential Decryption Fallback (回退处理)**

> This step is triggered **only** when the calling skill decrypts the credential and the resulting status is **失败 (FAIL)**.

* **Trigger:** The calling skill reports `PAY_STATUS: FAIL` (or equivalent 失败 status) after decrypting the credential from Step 2.
* **Action:** Check the **preserved original script output** from Step 2 for the presence of authorization/authentication URLs:

  #### **Case A: Preserved output contains `授权链接: <AUTH_URL>`**
  
  * **Meaning:** The user has not yet been authorized. The credential contained a failure status because the payment could not proceed without authorization. The `授权链接` was present in the original output but was deferred in favor of credential processing.
  * **Action:** Fall back to **Step 3 Case A** — treat this as an authorization-required scenario. Execute all actions defined in Step 3 Case A using the preserved `<AUTH_URL>`.

  #### **Case B: Preserved output contains `鉴权链接: <AUTH_URL>`**
  
  * **Meaning:** The payment failed because authentication was not completed. The `鉴权链接` was present in the original output but was deferred.
  * **Action:** Fall back to **Step 3 Case B** — treat this as an authentication-required scenario. Execute all actions defined in Step 3 Case B using the preserved `<AUTH_URL>`.

  #### **Case C: Preserved output contains NEITHER `授权链接:` NOR `鉴权链接:`**
  
  * **Meaning:** The payment genuinely failed due to business logic, and there is no authorization/authentication recovery path.
  * **Action:** Report the failure to the user. Emphasize that the transaction was declined due to business logic. Report any error code and reason provided by the calling skill. Additionally, if the **preserved original script output** contains `返回消息: <MESSAGE>`, display the `<MESSAGE>` to the user as supplementary failure context. If no specific error details were provided, inform the user that the payment failed and suggest they contact support or retry later.

---

### **Step 3 — Authorization / Authentication Required**

> ⚠️ **PREREQUISITE CHECK:** This step is evaluated in two scenarios:
> 1. The original script output does **NOT** contain `已获取到支付凭证` at all.
> 2. You were directed here from **Step 2.1** after a credential decryption failure with a preserved authorization/authentication URL.

> ⚠️ **LINK VERIFICATION (MANDATORY):** Before presenting any `授权链接` or `鉴权链接` to the user, you **MUST** verify the extracted URL for accuracy:
> 1. Confirm the URL is a **complete, well-formed URL** (starts with `http://` or `https://`, no truncation, no extra whitespace or line breaks).
> 2. Ensure the URL is **exactly as output by the script** — do NOT modify, truncate, or re-encode any part of it.
> 3. If the URL contains query parameters (e.g., `clawtipId`), verify they are intact and not corrupted.
> 4. **Do NOT hallucinate or fabricate a URL.** Only use the URL that appears after `授权链接:` or `鉴权链接:` in the script output.
> 5. If the URL appears malformed or incomplete, report the issue to the user instead of presenting a broken link.

#### **Case A: 失败 + 授权链接 → 待授权 (Authorization Required)**

* **Trigger (direct):** The output contains **ALL** of the following:
  1. `支付状态: 失败` ← **REQUIRED** (exact match)
  2. `授权链接: <AUTH_URL>` ← **REQUIRED**
  3. Does **NOT** contain `已获取到支付凭证` ← **REQUIRED**

* **Trigger (fallback from Step 2.1 Case A):** The calling skill reported `PAY_STATUS: FAIL` after credential decryption, and the preserved original output contains `授权链接: <AUTH_URL>`.

* **Meaning:** The user has not yet been authorized. The payment cannot proceed until the user completes authorization via the provided link.
* **Action:**
  1. Provide the extracted `<AUTH_URL>` to the user as the official **authorization** link. Additionally, if the output (or preserved output) contains `返回消息: <MESSAGE>`, display the `<MESSAGE>` to the user as supplementary context.
  2. Extract `{clawtip_id}` from the authorization URL (the `clawtipId` query parameter, e.g., `...?clawtipId={clawtip_id}`).
  3. Create a `scheduled task` to query the user's registration status:
      * **Query Phrase:** Use a phrase like `查询token注册状态 {clawtip_id}` or `query token register status {clawtip_id}`.
      * **Frequency & Duration:** Execute once per minute for the next 5 executions (after complete, you should notice user in the main session).
      * **Crucial Note:** **Check the registration status, NOT the payment result.**
      * **Execution Limit:** If it exceeds 5 times, cancel the scheduled task (`clawtip-payment user token register status {clawtip_id}`).
      * **Conflict Handling:** Cancel any currently running scheduled tasks related to `查询token注册状态` before starting the new one.
      * **Task Name:** `clawtip-payment user token register status {clawtip_id}`。当用户需要授权，并创建了授权任务后，需要显示提示用户可以说当用户扫码完成授权后，可以说`我已授权`或`我已完成授权`以继续之前的流程

#### **Case B: 处理中 + 鉴权链接 → 待鉴权 (Authentication Required)**

* **Trigger (direct):** The output contains **ALL** of the following:
  1. `支付状态: 处理中` ← **REQUIRED** (exact match)
  2. `鉴权链接: <AUTH_URL>` ← **REQUIRED**
  3. Does **NOT** contain `已获取到支付凭证` ← **REQUIRED**

* **Trigger (fallback from Step 2.1 Case B):** The calling skill reported `PAY_STATUS: FAIL` after credential decryption, and the preserved original output contains `鉴权链接: <AUTH_URL>`.

* **Meaning:** The payment is pending authentication. The user must complete authentication before the transaction can proceed.
* **Action:** Provide the extracted `<AUTH_URL>` to the user as the official **authentication** link. Additionally, if the output (or preserved output) contains `返回消息: <MESSAGE>`, display the `<MESSAGE>` to the user as supplementary context.

> **Stop here if Step 3 matched; do not proceed to Step 4.**

---

### **Step 4 — Route by Decrypted Status**

After the calling skill decrypts the credential and reports the status, follow the corresponding case:

#### **Case A: 成功 (Transaction Success)**

* **Trigger:** The decrypted status is **成功**.
* **Action:**
  1. Confirm to the user that the payment has been processed successfully.
  2. Display the full decrypted payment info clearly:
     **Payment Success Info:** `<DECRYPTED_PAY_INFO>`

---

#### **Case B: 处理中 (Processing)**

* **Trigger:** The decrypted status is **处理中**.
* **Action:** Inform the user that the payment is still being processed. Suggest they wait a moment and then check the payment status again.

---

#### **Case C: 失败 (Failed)**

* **Trigger:** The decrypted status is **失败** (or `FAIL`).
* **Action:** **Go to Step 2.1 (Credential Decryption Fallback)** to determine whether a recovery path (authorization/authentication) is available from the preserved original output. Do **NOT** simply report the failure here — always check Step 2.1 first.

---

# Create User Payment Token

When the user explicitly requests to create a token with a phrase like `创建token xxx` or `create token xxx`, execute the following command.

## 1. Required Parameters

Provide the following parameters strictly according to their defined formats:

* **`user_token`** (string): the user's token provided by `xxx` of `创建token xxx`.

## 2. Execution Command

```bash
python3 scripts/create_token.py <user_token>
```

## 3. Other Actions

You should check and cancel the running scheduled task about `查询token注册状态` if it is running (named `clawtip-payment user token register status ${device_id}`). The `device_id` is a flexible value.

---

# Query the User Register Status

When the user explicitly requests to query the user register status with a phrase like `查询token注册状态 xxx` or `query token register status xxx`, or `我已注册`, execute the following command.

## 1. Required Parameters

Provide the following parameter:

* **`device_id`** (string): The user's device ID.

## 2. Execution Command

```bash
python3 scripts/check_register_status.py <device_id>
```

## 3. Result Processing Rules

Analyze the standard output of the execution command and strictly follow these response protocols:

### **Case A: Processing**

* **Trigger:** The output matches the pattern `Status: processing`.
* **Action:** Inform the user that the registration is still processing, and optionally tell them the current count.

### **Case B: Successful**

* **Trigger:** The output matches the pattern `Status: successful`.
* **Action:** Confirm to the user that the registration is successful, and they have obtained the user token. You should check and cancel the running scheduled task about `查询token注册状态` if it is running (named `clawtip-payment user token register status ${device_id}`). The `device_id` is a flexible value.

### **Case C: Execution Failure**

* **Trigger:** Any error message, timeout, or failure to match the patterns above.
* **Action:** Report the specific error returned by the script.

---

# View Clawtip Wallet

When the user requests to view their clawtip wallet with phrases like `查看我的clawtip钱包`, `查看钱包`, `打开clawtip钱包`, `查看clawtip钱包`, `clawtip钱包管理` or `view my clawtip wallet`, respond with the following:

> 您可以通过以下链接，扫描二维码查看您的 clawtip 钱包：
>
> 👉 [查看 Clawtip 钱包](https://clawtip.jd.com/qrcode?bizUrl=https://jpay.jd.com/ecnya2a/claw/index)
>
> 请在浏览器中打开此链接然后扫描二维码以查看您的钱包详情。