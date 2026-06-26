---
name: bijie-express-tracking
description: Fast package tracking and logistics timeline lookup for 2000+ couriers with BijieServ. Use for 查快递, 快递查询, 查物流, 物流轨迹, 快递到哪了, 包裹追踪, track package, where is my package, courier tracking, 顺丰查询, 圆通查询, 中通查询, 韵达查询, 申通查询, 极兔查询, 京东物流查询, EMS查询.
---

# Bijie Express Skill

Fast express tracking, package lookup, and logistics timeline query through BijieServ.

Use this skill for package tracking, courier tracking, shipping status lookup, logistics timeline lookup, and Chinese courier queries such as 顺丰, 圆通, 中通, 韵达, 申通, 极兔, 京东物流, and EMS.

Return a concise user-facing summary with:
- current package status
- latest logistics update
- recent tracking timeline
- ETA when available
- masked sensitive data

This skill is written to be easy for both Codex-style agents and OpenClaw-style agents to follow:
- Prefer deterministic execution over free-form API reconstruction.
- Reuse the local script when possible.
- Ask the user for missing information only when needed.

## When To Use

Use this skill when the user wants to:
- check a package status
- view logistics updates or delivery timeline
- identify the courier and query a tracking number
- track common domestic or international carriers supported by BijieServ

Typical requests:
- `查一下 SF13156789012`
- `帮我查这个快递到哪了`
- `track package 123456789`
- `查询圆通/顺丰/中通/韵达/申通/极兔/京东/EMS`

## Source Of Truth

Prefer these local files in this order:
1. `scripts/express.py`: canonical query logic, headers, parameter handling, masking, and response formatting.
2. `references/company-codes.md`: courier code lookup table when carrier mapping is uncertain.
3. This file: behavioral guidance for when to run, what to ask, and how to present results.

If this file conflicts with the script, follow the script.

## Execution Policy

- Prefer running the local script instead of manually composing raw HTTP requests.
- Treat the script behavior as authoritative for endpoint, headers, payload, and error handling.
- Do not promise capabilities that are not implemented locally.
- Mask phone numbers or other sensitive details before showing results to the user.

## Inputs

Required:
- tracking number

Optional:
- courier name or courier code
- phone number if the carrier requires extra verification
- origin or destination hints when needed

## Recommended Flow

1. Extract the tracking number and optional courier name from the user request.
2. Validate the tracking number at a basic level.
   A practical baseline is 6 to 32 characters, matching the local script.
3. If the user provided a courier, map it to a company code.
4. If the user did not provide a courier:
   - first infer from common prefixes such as `SF`, `YT`, `ZT`, `YD`, `ST`, `JT`, `JD`
   - if still unclear, consult `references/company-codes.md`
   - if still unknown, ask the user which courier it is
5. Run the local query logic from `scripts/express.py`.
6. Return a concise, user-friendly summary:
   - courier name
   - tracking number
   - current status
   - latest update
   - recent timeline
   - ETA if available
7. Apply privacy masking before showing the result.

## Output Style

Keep the response compact and practical. Prefer:
- current status first
- latest logistics event second
- recent timeline after that
- ETA only when the API provides it

Good structure:
- `状态`: 已签收 / 派送中 / 运输中 / 异常件 / 退回中
- `最新轨迹`: the most recent meaningful tracking update
- `时间线`: a short list of recent nodes
- `预计送达`: only if present

## Privacy Rules

- Mask mobile numbers like `138****1234`.
- Avoid exposing full recipient address details.
- If the upstream response contains sensitive text, sanitize it before presenting it.

## Error Handling

Use these handling rules:

- Invalid tracking number:
  tell the user the number appears malformed and ask them to re-check it.
- Unknown courier:
  ask the user to confirm the courier name.
- No tracking result:
  explain that the parcel may not be shipped yet, the number may be wrong, or the carrier may not have updated tracking.
- Rate limiting or lockout:
  explain that queries are too frequent and suggest trying again later.
- Timeout or request failure:
  tell the user the query failed temporarily and suggest retrying.

## Courier Mapping Notes

Common mappings:
- `SF` -> `shunfeng`
- `YT` -> `yuantong`
- `ZT` -> `zhongtong`
- `YD` -> `yunda`
- `ST` -> `shentong`
- `JT` -> `jtexpress`
- `JD` -> `jd`
- `EMS` -> `ems`

For a broader list, use `references/company-codes.md`.

## OpenClaw Compatibility Notes

To keep this skill compatible with OpenClaw-style agents:
- keep behavior instructions explicit and step-based
- prefer local files over hidden assumptions
- avoid requiring agent-specific internal memory
- do not rely on rich UI formatting to make the result understandable
- keep the frontmatter short and searchable

If OpenClaw loads only the skill text and not repository code automatically, the agent should explicitly inspect:
- `scripts/express.py`
- `references/company-codes.md`

## Search And Discovery Notes

To improve discoverability on skill hubs such as ClawHub:
- put the core task words near the top of the file: package tracking, express tracking, logistics query, courier tracking, 查快递, 查物流
- keep the `name` and `description` closely aligned with what users actually search for
- mention both brand and task intent so users can find the skill by either `BijieServ` or `快递查询`
- include both Chinese and English task phrases because users may search in either language
- avoid vague marketing language that does not help the retrieval system understand the skill

Useful search intents covered by this skill:
- 查快递
- 快递查询
- 查物流
- 物流轨迹
- 快递到哪了
- 包裹追踪
- track package
- where is my package
- courier tracking
- shipping status

## Notes

- Send requests to `https://www.bijieserv.com/api/method/express_app.open.v1.query.exec`, not `skill.bijieserv.com`.
- Keep `Origin` and `Referer` aligned with `https://www.bijieserv.com/` when following the local script behavior.
- Do not claim per-user quota tracking, shared cache behavior, or automatic compliance enforcement unless those behaviors are actually implemented in code.
