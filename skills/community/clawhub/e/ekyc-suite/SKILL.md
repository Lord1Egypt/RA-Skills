---
name: ekyc-suite
version: 1.0.0
description: |
  KYC and eKYC identity verification suite for AI agents — 8 financial-grade biometric and document verification capabilities in one skill.
  Face comparison and face matching (similarity score 0-100), face liveness detection for selfie verification (anti-deepfake, anti-fraud screening),
  video liveness detection (deepfake detection with auto-retry), document OCR for ID card, bank card, driver license, and vehicle license,
  plus media labeling with 15+ image analysis attributes for fraud prevention and compliance.
  Use for: know-your-customer (KYC) onboarding, identity verification, face recognition and face verification,
  AML compliance checks, fintech customer onboarding, biometric selfie verification, document verification,
  deepfake and AI-generated content detection, anti-fraud risk screening, and AI security audits.
  Trigger when user says "compare two faces", "is this photo AI-generated", "is this video real",
  "read ID card", "read bank card number", "read driver's license", "read vehicle license",
  "check for mask", "detect coercion", "check if in car", "do KYC", "ekyc", "verify identity".
  Do NOT use for: conceptual KYC questions (no actual image processing),
  requests to transmit names/ID numbers as text.
env:
  - KYC_APPID
  - KYC_SECRET
  - LABEL_APPID
  - LABEL_SECRET
tags:
  - kyc
  - ekyc
  - face-comparison
  - face-verification
  - face-recognition
  - face-matching
  - liveness-detection
  - deepfake-detection
  - ocr
  - id-card
  - bank-card
  - driver-license
  - vehicle-license
  - media-labeling
  - image-analysis
  - anti-fraud
  - fraud-prevention
  - identity-verification
  - biometric
  - ai-security
  - compliance
  - fintech
  - aml
  - know-your-customer
  - document-verification
  - face-liveness
  - selfie-verification
  - deepfake
  - onboarding
homepage: https://github.com/wefi-ai/eKYC-suite
metadata:
  clawdbot:
    emoji: "🔐"
    requires:
      env: ["KYC_APPID", "KYC_SECRET", "LABEL_APPID", "LABEL_SECRET"]
    primaryEnv: "KYC_APPID"
    files: ["scripts/*"]
---

# eKYC Suite

Financial-grade electronic identity verification toolkit with 8 capabilities covering face comparison, liveness detection, document OCR, and media labeling. All inputs are image or video files only.

---

## Quick Reference

| Capability | Command |
|-----------|---------|
| Face compare | `python scripts/ekyc_api.py face_compare --photo1 <a> --photo2 <b>` |
| Photo liveness | `python scripts/ekyc_api.py photo_liveness_detect --file <photo>` |
| Video liveness | `python scripts/ekyc_api.py video_liveness_detect --file <video>` |
| ID card OCR | `python scripts/ekyc_api.py id_card_ocr --image <img> --side <0\|1>` |
| Bank card OCR | `python scripts/ekyc_api.py bank_card_ocr --image <img>` |
| Driver license | `python scripts/ekyc_api.py driver_license_ocr --image <img>` |
| Vehicle license | `python scripts/ekyc_api.py vehicle_license_ocr --image <img> --side <1\|2>` |
| Media labeling | `python scripts/ekyc_api.py media_labeling --file <f> --labels "A14,B03" --type image` |

---

## External Endpoints

| Endpoint | Capabilities | Data Sent |
|----------|-------------|-----------|
| `https://kyc1.qcloud.com` | 2, 3, 4, 5 (liveness, ID/bank card OCR) | Base64-encoded images/videos + signed request |
| `https://miniprogram-kyc.tencentcloudapi.com` | 1, 6, 7 (face compare, driver/vehicle license OCR) | Base64-encoded images + signed request |
| `https://kyc2.qcloud.com` | 8 (media labeling) | Base64-encoded images/videos + signed request |

No personal text data (names, ID numbers) is transmitted. Only image/video binary data is sent.

---

## Security & Privacy

This software does not store, cache, or retain any submitted data.

API verification results are for reference only and do not constitute legal identity confirmation. This software must not be used as the sole basis for automated decisions that produce legal effects or significant consequences for individuals. Users should implement appropriate business logic and human review processes for high-stakes identity decisions.

---

## Trust Statement

By installing and using this skill, image and video data you provide will be transmitted to Tencent Cloud's identity verification API for processing. Only install this skill if you trust the upstream service provider's data handling practices. This skill does not independently store, process, or retain any biometric data.

---

## Goal

Receive user-uploaded images or videos, call the corresponding identity verification API, return structured results and explain them to the user in plain language.

---

## When to Use

Use this Skill when the user's request involves any of these scenarios:

- "Compare these two photos — same person?" / "face similarity score"
- "Is this photo AI-generated?" / "Is this video real?" / "deepfake detection"
- "Read this ID card" / "Read bank card number" / "Read driver's license" / "Read vehicle license"
- "Check for mask" / "Detect coercion" / "Wearing hat?" / "On the phone?"
- "Unconscious or asleep?" / "Wearing sunglasses?" / "Inside a car?"
- "In a hotel room?" / "Has tattoo?" / "Multiple people?" / "Wearing headphones?"
- "Facial sheet mask?" / "Critical patient?" / "At a car dealership?"
- Any request containing "face comparison", "liveness detection", "OCR", "media labeling", "ekyc"

## Do NOT Use

Do not use this Skill in these situations:

- User is only asking "what is KYC" or "how does eKYC work" → answer from knowledge directly
- User provides names, ID numbers, phone numbers as text → refuse and redirect (see Privacy Rule below)
- User wants face liveness + identity verification combo (requires transmitting name + ID number) → explain privacy limitation

---

## Critical Rules

### Rule 1: Privacy — NEVER Accept Personal Text

**NEVER accept or transmit names, ID numbers, phone numbers, or any personal text data.**

If the user provides such information, respond:

> "To protect your privacy, this service does not accept names, ID numbers, or other personal text. Transmitting sensitive information through AI conversations carries leakage risks. Please upload image or video files directly — I will complete verification through image recognition."

### Rule 2: NEVER Rewrite Signing Code

Always use the Python scripts in `scripts/`. The signing algorithm uses **SHA1** (produces 40-character uppercase hex).

Previous AI models have replaced SHA1 with SHA256 (64 characters), causing 100% authentication failure. Scripts include assertion: `assert len(signature) == 40`. If you see a 64-character signature, you are using SHA256 by mistake — stop and use the provided scripts.

### Rule 3: Dual-Path Response Parsing

API responses may return data at the top level OR nested inside a `result` object. Always check both:

```python
value = data.get("field") or (data.get("result", {}) or {}).get("field")
```

Skipping dual-path parsing causes `None` / `undefined` errors.

---

## Environment Variables

```bash
# Capabilities 1-7 (face comparison, liveness detection, document OCR)
KYC_APPID=your_kyc_appid
KYC_SECRET=your_kyc_secret

# Capability 8 (media labeling, separate credential set)
LABEL_APPID=your_label_appid
LABEL_SECRET=your_label_secret
```

**Obtain credentials:**
- Key A (KYC) and Key B (LABEL): Contact Huiyan tech support (WeChat: blue-201809)
- Or register at [Tencent Cloud Face Verification Console](https://console.cloud.tencent.com/faceid/access) to obtain Key A

**⚠️ IMPORTANT: Use TEST credentials (free 100 calls). Do NOT use production credentials — production IDs incur charges billed by the upstream provider.**

**Partial configuration supported:** Key A alone enables capabilities 1-7. Key B alone enables capability 8. When a user requests an unconfigured capability, clearly indicate which credentials are missing and how to obtain them.

---

## 8 Capabilities

### Capability 1: Face Comparison

- **Trigger**: "compare these two photos", "same person?", "face similarity"
- **User provides**: Two photos containing faces
- **If user uploads only one**: Ask "Please upload a second photo for comparison"
- **Execute**: `python scripts/ekyc_api.py face_compare --photo1 <photo1> --photo2 <photo2>`
- **Returns**: similarity (score 0-100)
- **Result interpretation**:
  - **≥80**: High confidence match — can be determined as the same person (false acceptance rate ~1/10,000)
  - **70-79**: Can be determined as the same person (false acceptance rate ~1/1,000); threshold may be adjusted per business scenario
  - **<70**: Not recommended to determine as the same person; suggest clearer photos for re-comparison
- **Reply example**: "The similarity between the two photos is 95.7 (out of 100), a high-confidence match — they can be determined as the same person."

### Capability 2: Photo Liveness Detection

- **Trigger**: "is this photo real?", "AI-generated?", "photoshopped?"
- **User provides**: One photo containing a face
- **Execute**: `python scripts/ekyc_api.py photo_liveness_detect --file <photo>`
- **Returns**: riskLevel (risk level), riskTag (risk tag number)
- **Result interpretation**:
  - **Level 1**: No attack risk — genuine face photo, no forgery detected
  - **Level 2**: Medium suspicion — suspicious features present, suggest re-detection with different photo
  - **Level 3**: High suspicion — photo is likely forged/AI-generated, recommend rejection
- **Risk tag meanings** (include in reply):
  - 01=Eyes closed / 02=Action not completed / 03=Suspected replay attack / 04=Suspected synthetic attack
  - 05=Suspected fraud template / 06=Suspected watermark / 07=Reflection check failed / 08=Multiple faces
  - 09=Poor face quality / 10=Distance check failed / 11=Suspected adversarial attack / 12=Suspected attack traces on face
- **Reply example**: "Detection result: Risk level 3 (high suspicion), risk tag 04 (suspected synthetic attack). This photo is likely AI-synthesized — not recommended for identity verification."

### Capability 3: Video Liveness Detection

- **Trigger**: "is this video real?", "deepfake?", "video liveness"
- **User provides**: A video containing a face (≤20MB; videos exceeding 20 seconds will return an error)
- **If video too large**: Prompt "Video must be ≤20MB. Please compress and re-upload"
- **Execute**: `python scripts/ekyc_api.py video_liveness_detect --file <video>`
- **Network retry**: Video uploads may encounter 999999 network errors. Script auto-retries up to 3 times with exponential backoff. If all 3 fail, tell user "Network temporarily busy, please try again in a few minutes"
- **Returns & interpretation**: Same as Capability 2
- **Reply example**: "Video detection result: Risk level 1 (no attack risk). This video is genuine — no deepfake or synthetic traces detected."

### Capability 4: ID Card OCR

- **Trigger**: "read ID card", "extract ID card info"
- **User provides**: ID card photo + side indicator
  - `0` = Portrait side (front, with photo)
  - `1` = National emblem side (back, with issuing authority and validity)
- **If user doesn't specify side**: Ask "Is this the portrait side (front with photo) or the emblem side (back with national emblem)?"
- **Execute**: `python scripts/ekyc_api.py id_card_ocr --image <photo> --side <0|1>`
- **Returns**:
  - Portrait side (side=0): name, sex, nation (ethnicity), birth, idcard (ID number), address
  - Emblem side (side=1): authority (issuing authority), validDate (validity period)
- **Result interpretation**: Organize returned fields into a clear list for the user
- **Reply example** (portrait side): "ID card recognition result: Name: Li Ming, Sex: Male, Ethnicity: Han, Birth: 1992-06-20, ID No.: 440305199206******, Address: 88 Keji Road, Nanshan District, Shenzhen, Guangdong."
- **Reply example** (emblem side): "ID card recognition result: Issuing authority: Shenzhen Public Security Bureau, Validity: 2015.03.20–2035.03.20."

### Capability 5: Bank Card OCR

- **Trigger**: "read bank card", "card number", "bank card OCR"
- **User provides**: Bank card front photo
- **Execute**: `python scripts/ekyc_api.py bank_card_ocr --image <photo>`
- **Returns**: bankcardNo (card number), bankcardValidDate (expiry date)
- **Result interpretation**: Display card number and expiry. If expiry is empty, the card face does not print an expiry date
- **Reply example**: "Bank card recognition result: Card No. 6222 0200 **** **** 000, Expiry: 08/28."

### Capability 6: Driver's License OCR

- **Trigger**: "read driver's license", "driver license info"
- **User provides**: Driver's license photo
- **⚠️ Main page only**: If user submits the supplementary page (back), the API returns error -9005. Reply: "Driver's license OCR only supports the main page (front). Please re-upload the front page."
- **Execute**: `python scripts/ekyc_api.py driver_license_ocr --image <photo>`
- **Returns**: licenseNo, name, sex, nationality, address, birth, fetchDate, driveClass, validDateFrom, validDateTo
- **Result interpretation**: Organize as clear list; highlight vehicle class and validity period
- **Reply example**: "Driver's license recognition result: License No.: 440305199206200013, Name: Li Ming, Vehicle class: C1, Valid: 2020-05-28 to 2026-05-28."

### Capability 7: Vehicle License OCR

- **Trigger**: "read vehicle license", "vehicle info"
- **User provides**: Vehicle license photo + side indicator
  - `1` = Main page (basic vehicle information)
  - `2` = Supplementary page (passenger capacity, inspection records, etc.)
- **If user doesn't specify**: Ask "Is this the main page or the supplementary page?"
- **Execute**: `python scripts/ekyc_api.py vehicle_license_ocr --image <photo> --side <1|2>`
- **Returns**:
  - Main page (side=1): plateNo, vehicleType, owner, model, vin, engineNo, registeDate, issueDate
  - Supplementary (side=2): additionally returns authorizedCarryCapacity, authorizedLoadQuality, fileNumber, total, inspectionRecord, externalDimensions, curbWeright
- **Result interpretation**: Organize as clear list. Main page: highlight plate number and VIN. Supplementary: highlight passenger capacity and inspection records
- **Reply example**: "Vehicle license recognition result: Plate: 粤B88888, Type: Small sedan, Owner: Li Ming, VIN: LGWEE6K58RH000001, Engine: DKZ000001, Registered: 2022-03-15."

### Capability 8: Media Labeling

- **Trigger**: "check for mask", "detect coercion", "wearing hat?", "on the phone?", "inside a car?", "multiple people?", "tattoo?", "hotel room?", "media labeling"
- **User provides**: Image or video + attribute description (you auto-map to label codes based on user description)
- **Label reference table** (auto-select based on user description):

**Portrait labels: Detect user status and risk**

| Code | Label | Description | Use case |
|------|-------|-------------|----------|
| A10 | Unconscious/asleep | Eyes closed or eyelids forced open | Safety monitoring, risk alert |
| A09 | Under coercion | Coerced posture detected | Anti-fraud, security alert |
| A15 | Critical patient | Critical condition patient | Loan fraud prevention, compliance |
| A11 | On the phone | User is on a phone call | Call scenario, third-party guidance |
| A04 | Wearing headphones | Headphones detected on ears | Call scenario, third-party guidance |
| A05 | Nudity | Sensitive body exposure | Compliance review |
| A13 | Tattoo | Tattoo detected | Feature marking, risk analysis |
| A02 | Mask covering face | Medical mask obstructing face | Identity detection, compliance |
| A14 | Wearing hat | Hat detected | Obstruction detection, disguise |
| A01 | Facial sheet mask | Sheet mask applied | Skincare or obstruction detection |
| A06 | Wearing sunglasses | Sunglasses detected | Obstruction detection, compliance |

**Environment labels: Detect business scenario**

| Code | Label | Description | Use case |
|------|-------|-------------|----------|
| B02 | Multiple people | Multiple people in frame | Group scenario, third-party guidance |
| B03 | Inside passenger vehicle | Inside a passenger car (sedan, SUV, etc.) | Auto loans, travel, compliance |
| B06 | In hotel | Inside a hotel room | Scenario review, risk control |
| B07 | At car dealership | Inside a car dealership | Consumer finance, compliance |

- **Max 5 label codes per request**
- **Execute**: `python scripts/ekyc_api.py media_labeling --file <file> --labels "A02,A14" --type image`
  - type: `image` for photos, `video` for videos
- **Async process**: This API is a 2-step async operation (submit → wait → query). The script handles this automatically. Typically returns results in 5-10 seconds
- **Returns**: fileLabel (label result array), liveStatus (liveness status), compareStatus (face comparison status)
- **Result interpretation**:
  - fileLabel value per label: `1`=detected, `0`=not detected, empty=recognition error (suggest retry)
  - liveStatus: `1`=live, `0`=not live
  - compareStatus: `1`=faces match, `0`=faces don't match
- **Reply example**:
  ```
  Media labeling results:
  - A14 (Wearing hat): ✅ Detected
  - A02 (Mask covering face): ❌ Not detected
  Liveness status: Live
  ```

---

## Full Example

### Positive: User requests face comparison

**User**: "Are these two photos the same person?" + [upload Photo A] + [upload Photo B]

**Your actions**:
1. Confirm two photos received
2. Execute `python scripts/ekyc_api.py face_compare --photo1 PhotoA --photo2 PhotoB`
3. Receive: `{"success": true, "similarity": "95.7", "orderNo": "ekyc..."}`
4. Reply: "The similarity between the two photos is 95.7 (out of 100), a high-confidence match — they can be determined as the same person."

### Negative: User provides personal text

**User**: "Verify Li Ming, ID number 440305199206200013, against this photo" + [upload photo]

**Your actions**:
1. Detect name and ID number provided → **trigger Privacy Rule**
2. **Do NOT execute any API call**
3. Reply: "To protect your privacy, this service does not accept names or ID numbers as text. Please upload two face photos directly — I will determine if they are the same person through image comparison."

---

## Definition of Done

After each API call, verify all conditions are met:

- [ ] API returned code=0 (success)
- [ ] Raw data has been converted to user-friendly natural language
- [ ] Result interpretation included (not just numbers — explain what they mean)
- [ ] If error occurred (code≠0), user has been informed with reason and suggested action
- [ ] No API keys, orderNo, or other technical details exposed in conversation (unless user asks)

---

## Error Handling

When errors occur, explain in user-friendly language with suggested actions:

### Common Error Codes (All Capabilities)

| Error Code | User-facing message |
|-----------|-------------------|
| 1101 / 1102 | "Authentication failed — API credentials may be misconfigured. Please check the keys in your .env file." |
| 1103 | "Current IP is not whitelisted. Please contact your administrator." |
| 1106 | "Invalid request. Please check your request format." |
| 1107 | "Invalid request parameters. Please verify all required fields." |
| 1502 | "Invalid version parameter. Please use version 1.0.0." |
| 1503 | "File checksum error. Please retry the upload." |
| 1505 | "No permission to access this resource. Please check your appid authorization." |
| 1506 / 1507 | "Too many requests. Please wait 10 seconds and try again." |
| 1601 | "Request body too large. Please reduce the file size." |
| 1602 | "Request body parameter error. Please check your request format." |
| 999999 / 999998 / 999997 | "Network temporarily busy, auto-retrying... (if 3 retries fail, ask user to try again later)" |

### Face & Liveness Error Codes (Capabilities 1-3)

| Error Code | User-facing message |
|-----------|-------------------|
| 66660016 | "Image or video file is abnormal. Please re-capture or use a different file." |
| 66660023 / 66660048 | "No proper face detected. Please face the camera directly with a clear, frontal view." |
| 66660037 | "Multiple faces detected in photo. Please use a photo with only one face." |
| 66660041 | "Face is occluded or eyes are closed. Please retry with a clear photo." |
| 66660078 | "No face detected. Please ensure the photo has a clear, frontal face with good lighting." |
| 1603 | "Invalid video file. Please check the video format and try again." |
| 1606 | "Response decryption failed. Please retry." |
| 1607 | "Query result not found. The verification order may have expired." |
| FailedOperation.CoveredFace | "Face is occluded. Please submit an unobstructed face photo." |
| FailedOperation.IncompleteFace | "Incomplete face detected. Please submit a full face photo." |
| FailedOperation.PoorImageQuality | "Image quality too poor. Please check the photo quality." |
| FailedOperation.ImageDecodeFailed | "Image decode failed. The file may be corrupted." |
| FailedOperation.VideoDecodeFailed | "Video decode failed. Please check the video format." |
| FailedOperation.VideoDurationExceeded | "Video too long — max 20 seconds supported. Please trim and re-upload." |
| FailedOperation.DetectEngineSystemError | "Detection engine error. Please retry." |
| FailedOperation.UnKnown | "Internal error. Please retry or contact support." |

### OCR Error Codes (Capabilities 4-7)

| Error Code | User-facing message |
|-----------|-------------------|
| -1102 | "Image decode failed — file may be corrupted. Please re-capture or use a different photo." |
| -1300 | "Image is empty. Please upload a valid image file." |
| -1301 | "Required parameter is missing. Please check your request." |
| -1304 | "Parameter value too long. Please check input length limits." |
| -9001 | "Invalid request type. Please check the side/type parameter." |
| -9002 | "OCR recognition failed — photo may not be clear enough. Please re-capture in good lighting." |
| -9005 | "Invalid image or unsupported image type. For driver's license, only the main page (front) is supported." |
| -9006 | "Image preprocessing failed. Please try a different photo." |
| 66661001 | "Not an ID card or image is not clear enough. Please verify the document type and ensure the photo is sharp and complete." |
| 66661013 / 66661005 | "Please adjust the angle and ensure the document is clear and complete." |

### Media Labeling Error Codes (Capability 8)

| Error Code | User-facing message |
|-----------|-------------------|
| 66660000 | "Invalid order number. Please check the orderNo parameter." |
| 66660001 | "Invalid appId. Please verify your credentials." |
| 66660002 | "Request has expired. Please regenerate the signature and retry." |
| 66660003 | "Trial quota exceeded. Please upgrade your plan or contact support." |
| 66660004 | "Concurrent request limit reached. Please wait a moment and retry." |
| 66660013 | "Invalid request parameters. Please check your request format." |
| 66660016 | "Image or video file is abnormal. Please re-capture or use a different file." |
| 66661014 | "Media labeling result not found. The order may have expired — please resubmit." |
| 66661015 | "Media labeling still processing, please wait... (script auto-retries)" |
| 66661016 | "Too many labels per request (max 5). Please reduce label count and retry." |
| 66661018 | "Some label codes do not exist or are not yet available." |
| 66661019 | "No labels provided. Please specify at least one label code." |
| 66661020 | "Label code format is invalid. Use format like A01, B03." |
| 66661021 | "Your appId is not authorized for this service. Please contact support." |
| 66661022 | "Media labeling processing failed. Please resubmit the request." |
| 66661023 | "Image pre-check failed. Please ensure the image meets quality requirements." |
| 1104 | "Authentication signature expired or invalid. Please retry — the system will auto-refresh." |
| 400101 | "Missing required parameter. Please check the request format." |
| 400103 | "Invalid parameter value. Please verify label codes and input format." |
| 400105 | "Appid does not match the credential set. Please check your Key A / Key B configuration." |
| 400106 | "Signature verification failed. Please ensure the correct credential set is used." |
| 400501 | "File upload failed. Please check the file and retry." |
| 400502 | "File format not supported. Please use JPG, PNG, or MP4." |
| 400505 | "File processing timeout. Please retry with a smaller file." |
| 400506 | "File content is empty or corrupted. Please re-upload." |
| 400601 | "Service temporarily unavailable. Please retry later." |
| 400602 | "Service quota exceeded. Please contact support to increase your quota." |

For unlisted error codes: "Unexpected error (code: XXX, message: XXX). Please contact technical support."

---

## Authentication Architecture

### Capabilities 1-7 (KYC Auth) — 3 Steps

```
Step 1: GET access_token ← app_id + secret
Step 2: GET SIGN ticket  ← app_id + access_token
Step 3: Signature = sort([appId, orderNo, nonce, "1.0.0", ticket]) → concat → SHA1 → 40-char uppercase
```

Implementation: `scripts/kyc_auth.py` — **DO NOT rewrite, call directly**

### Capability 8 (Label Auth) — 2 Steps

```
Step 1: GET ticket directly ← appId + secret (no access_token step)
Step 2: Signature = sort([appId, orderNo, nonce, "1.0.0", ticket, unixTimeStamp]) → concat → SHA1 → 40-char uppercase
```

Key difference: 6 parameters (adds unixTimeStamp), and ticket is obtained directly without access_token.

Implementation: `scripts/label_auth.py` — **DO NOT rewrite, call directly**

---

## Legal Notice

This software does not store, cache, or retain any submitted data.

API verification results are for reference only and do not constitute legal identity confirmation. This software must not be used as the sole basis for automated decisions that produce legal effects or significant consequences for individuals. Users should implement appropriate business logic and human review processes for high-stakes identity decisions.

---

## Rate Limits

- Capabilities 1-7 (KYC): 100 calls per appid (test quota)
- Capability 8 (Media Labeling): Concurrency-limited, default 1 concurrent request; contact tech support for expansion
