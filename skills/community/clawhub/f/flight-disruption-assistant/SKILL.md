---
name: "flight-disruption-assistant"
description: "AirnodeHub flight skill for live status, delays, cancellations, and airport boards via metered, attested AeroDataBox POST calls with approval and verification."
---

# Flight Disruption Assistant

## Execute

1. Extract the flight identifier or airport, direction, date, time window, and whether live position is needed. Resolve relative dates to an explicit `YYYY-MM-DD` in the airport’s local time; ask only when ambiguity changes the lookup. **Done when:** the request maps to a documented operation.

2. Read `https://airnode-aerodatabox.fly.dev/` once per run and use only current documented operations and parameters. Data lookups must POST JSON shaped as `{"operation":"<operation>","parameters":{...}}` to the same root; GET only reads documentation. **Done when:** the POST contract and signer address are known.

3. AeroDataBox is metered and its documentation may not state an exact per-call price. Before POSTing, state the operations and maximum call count and obtain explicit approval. Never infer approval from the information request. **Done when:** the bounded call plan is approved or declined.

4. Choose the smallest operation: `flightStatus` for the nearest operating date, `flightStatusOnDate` for a named local date, `airportSchedule` for a narrow arrival/departure board, `searchAirportsByTerm` for an unknown airport code, `airportFeedStatus` for unexpectedly absent live data, or `searchFlightNumbers` for ambiguous flight text. Extra calls require remaining approval. **Done when:** the minimum approved POST set returns data or a concrete error.

5. Report only returned facts: status, route, scheduled and estimated/actual local times, terminal/gate, location when requested, and freshness. Calculate delay only from comparable returned timestamps and label it calculated. Never invent causes, compensation, rebooking, gates, or times. **Done when:** the disruption question is answered with uncertainty and freshness.

6. Retry once only for a transient error or a narrower valid request without exceeding the call limit. If approval is denied, state that no live lookup was made. **Done when:** sourced results or the exact blocker are reported.

## Verification

Confirm all data calls used documented POST operations, stayed within the approved call count, and returned `airnode`, `requestHash`, `timestamp`, `data`, and `signature`. Cryptographically verify the documented request hash and EIP-191 signer when tooling is available; otherwise say `Attestation not cryptographically verified`. Confirm all reported facts came from `data` and all dates are explicit.
