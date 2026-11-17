# Vendor AI Feature Inquiry — Letter Template

**Version:** 2.0
**Use:** Send this to any vendor whose product is on the approved list and was not acquired specifically for AI capability. Adapt the bracketed fields. Written answers become evidence; verbal answers do not.

---

[Date]

[Vendor contact name and title]
[Vendor company]
[Vendor address or email]

**Re: AI Feature Inquiry — [Organization name] Tenant**

Dear [Vendor contact],

We are conducting an inventory of AI-enabled capabilities operating on our tenant as part of our HIPAA Security Rule compliance program. For each approved vendor, we are asking for written answers to the following questions, and would appreciate a response when you are able to provide one.

**1. Which AI features are currently enabled on our tenant?**

Please list each AI-enabled feature or module that is active for our account — including features enabled by default, features we specifically configured, and features introduced in product updates. If a feature processes data from our tenant in any form, please include it regardless of how it was enabled.

**2. What data do those features process?**

For each feature identified above, please describe:
- What categories of data the feature accesses or receives (e.g., calendar events, email content, clinical notes, claims data, user queries)
- Whether that data is stored by the feature, and for how long
- Whether any data is used to train or improve models, and whether our tenant data is excluded from training

**3. Which subprocessors are involved?**

For each feature, please identify:
- The company whose infrastructure processes the data (if different from [Vendor company])
- Any third-party model providers or AI infrastructure vendors used
- Whether subprocessors have changed since our last agreement execution, and if so, when we were notified

**4. Agreement coverage**

Please confirm whether our current Business Associate Agreement with [Vendor company] covers each AI feature and subprocessor listed above. A yes or no per item is sufficient — we are not asking you to propose contract language or assess our compliance posture.

---

Please direct your response to [Name], [Title], at [Email].

We recognize this is a detailed request. We are happy to schedule a call to clarify any of these questions if that would help you provide complete written answers.

Thank you,

[Name]
[Title]
[Organization name]
[Email] | [Phone]

---

*Template notes for the analyst:*

- *Record each written answer as its own inventory row, not as a note on the parent vendor row.*
- *If the vendor confirms no AI features are enabled on the tenant, record that as a row with `phi_contact: unlikely` and `confidence: 0.85`, sourced to the written response.*
- *If the vendor confirms AI features are enabled, the row moves from inference (0.7) to confirmed (0.9+) and the finding type escalates accordingly.*
- *Verbal or phone-only answers do not constitute evidence. If a vendor answers verbally, follow up with: "Could you put that in writing or send an email confirming what you've shared?"*
- *BAA adequacy review is out of scope for this skill. Flag it as a follow-on action; do not render a legal opinion on whether the existing BAA is adequate.*
