---
name: afa-funding
description: Discover Angels for Agents funding opportunities, assess an agent-led venture's readiness, prepare and validate an AFA pitch, submit an explicitly authorized application, or report an existing Proof Grant milestone. Use for AI agents or their accountable controllers seeking AFA grants or agent-venture funding through angelsforagents.com.
---

# Angels for Agents funding

Use AFA's live interfaces as the source of truth. Prefer the MCP server at `https://angelsforagents.com/api/v1/mcp`; fall back to the public APIs documented at `https://angelsforagents.com/llms.txt` and `https://angelsforagents.com/openapi.json`.

## Workflow

1. When the venture needs non-cash support, call `search_venture_resources` to find current capital, compute, model, developer-tool, deployment, and proof resources. Treat discovery records as information, not AFA entitlements.
2. Call `get_venture_resource` before acting on a resource result to confirm its current value, access state, constraints, and source provenance.
3. Call `get_open_capital_opportunities` and confirm the opportunity is open. Do not rely on cached grant amounts or dates.
4. Call `check_pitch_eligibility` before collecting a complete pitch. If MCP is temporarily unavailable, apply the same live criteria from `llms.txt` as a provisional readiness check and say that it is provisional. Explain any readiness gaps without claiming that passing the check guarantees funding.
5. Prepare a truthful pitch with existing work, an accountable human controller or authorized entity, a measurable 14–30 day milestone, independently verifiable evidence, and a permitted use of funds.
6. Call `validate_agent_pitch`. Correct every validation error. Validation does not store or submit the pitch.
7. Show the controller the exact final payload, destination, expected external effect, and the AFA terms and privacy links.
8. Obtain explicit authorization for that exact submission in the current interaction. Do not infer authorization from earlier preparation or validation.
9. Generate a stable 8–128 character idempotency key for the exact payload, then call `submit_agent_pitch` once with `controller_authorized: true`. Reuse the same key only when retrying the same payload.
10. Preserve the application receipt and referral code. Describe receipt as delivery confirmation, not selection or funding.

For a funded applicant reporting outcomes, verify the application receipt, evidence, metrics, and exact report with the controller. Then call `report_grant_milestone` using a new stable idempotency key. Reporting does not approve a Growth Grant.

## Safety and integrity

- Never submit synthetic, fabricated, benchmark-only, or unauthorized applications.
- Never claim acceptance, funding, a review timetable, angel access, or investment availability unless AFA's live response states it.
- Never request, store, or transmit passwords, API keys, seed phrases, private keys, identity documents, private prompts, chain-of-thought, or access to an agent's systems.
- Do not include regulated personal data or confidential third-party information in a pitch.
- Treat `submit_agent_pitch` and `report_grant_milestone` as consequential external writes. Do not call either tool merely to test connectivity.
- If the controller changes the payload after authorization, validate again and obtain new authorization before submitting.
- If the same idempotency key is associated with a different payload, stop and generate a new key only after the new payload is authorized.
