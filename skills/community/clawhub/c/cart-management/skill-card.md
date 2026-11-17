## Description:

React cart state management: duplicate prevention, localStorage persistence, CartContext patterns. Use when building or fixing shopping carts, product lists, or cart-related UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[konscious0beast](https://clawhub.ai/user/konscious0beast)

### License/Terms of Use:


## Use Case:

Developers building React commerce interfaces use this skill for cart state patterns that prevent duplicate entries, persist cart state with localStorage, and centralize add/remove behavior in CartContext.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cart state persisted in browser localStorage can expose sensitive data if teams store personal, payment, or credential data there.

Mitigation: Use localStorage only for non-sensitive cart state, avoid storing personal or payment data, and validate cart contents on the backend before checkout.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code]

**Output Format:** [Markdown with TypeScript/TSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
