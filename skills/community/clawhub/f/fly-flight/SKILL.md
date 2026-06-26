---
name: fly-flight
description: "Query China domestic transport options through one skill. Use when a user wants domestic flight or high-speed rail results, departure and arrival times, stations or airports, airline or train details, or public reference fares from open web sources. Route the request by transport mode and return a shared outer response shape. 一个同时支持中国国内航班和高铁查询的统一 transport skill，可根据 mode 路由到航班或高铁 provider。"
metadata: { "openclaw": { "requires": { "bins": ["python3", "node"] } } }
---

# Fly Flight

Use the unified transport entrypoint in this skill to handle China domestic trip lookup for both flights and high-speed rail.

这是一个统一的中国境内出行查询 skill，同时支持航班和高铁。
它通过同一个 transport 入口按 mode 路由到底层 provider。

## Requirements

Require the following runtime environment before using this skill:

- `python3`
- `node`
- Network access to Tongcheng public flight pages and official 12306 public endpoints

使用这个 skill 前，运行环境必须具备：

- `python3`
- `node`
- 能访问同程公开航班页面和 12306 官方公开接口的网络环境

These dependencies are required whether the skill is installed from GitHub or from ClawHub.  
无论这个 skill 是从 GitHub 安装还是从 ClawHub 安装，这些依赖都必须满足。

Current implementation status:

- `flight` mode is implemented through Tongcheng public flight pages.
- `train` mode is implemented through official 12306 public high-speed rail query and public price endpoints.

## Quick Start

Flight query:

```bash
python3 {baseDir}/scripts/transport_service.py search \
  --mode flight --from 北京 --to 上海 --date 2026-03-20 --sort-by price --pretty
```

High-speed rail query:

```bash
python3 {baseDir}/scripts/transport_service.py search \
  --mode train --from 北京 --to 上海 --date 2026-03-20 \
  --seat-type second_class --sort-by price --pretty
```

The legacy flight-only entrypoint remains available for backward compatibility:

```bash
python3 {baseDir}/scripts/domestic_flight_public_service.py search \
  --from 北京 --to 上海 --date 2026-03-20 --sort-by price --pretty
```

Optional local HTTP mode:

```bash
python3 {baseDir}/scripts/transport_service.py serve --port 8766
```

## Workflow

1. Determine transport mode.
   Use `flight` for flights, airports, airlines, or plane tickets.
   Use `train` for high-speed rail, rail tickets, stations, or train numbers.
   If the user is ambiguous, infer conservatively from their wording or ask.

2. Route to the correct provider.
   Use [scripts/transport_service.py](./scripts/transport_service.py) as the shared entrypoint.
   Flight mode delegates to [scripts/providers/flight_public_service.py](./scripts/providers/flight_public_service.py).
   Train mode delegates to [scripts/providers/train_public_service.py](./scripts/providers/train_public_service.py).

3. Preserve a shared outer response shape.
   Return `mode`, `provider`, `trip_type`, `outbound`, and optional `return`.
   Keep mode-specific fields inside each leg's `options`.

4. Apply only mode-specific filters that make sense.
   Flight filters: airline, direct-only, preferred airports.
   Train filters: train type, seat type, preferred stations.

5. Summarize results with the mode label.
   Clearly say whether the result is a flight result or a train result.
   Treat public-source prices as reference prices that can differ from final checkout prices.

## Output Rules

- Prefer up to 5 options unless the user asked for more.
- State the exact travel date in `YYYY-MM-DD`.
- Keep the outer response consistent across modes.
- Do not force a single shared field schema for airports and stations; keep mode-specific details inside `options`.
- For round trips, clearly separate `outbound` and `return`.
- For train mode, explain that prices come from official public fare data and seat availability comes from public query results.

## Resources

- Use [scripts/transport_service.py](./scripts/transport_service.py) as the unified CLI and HTTP entrypoint.
- Use [scripts/providers/flight_public_service.py](./scripts/providers/flight_public_service.py) for flight lookups.
- Use [scripts/providers/train_public_service.py](./scripts/providers/train_public_service.py) for high-speed rail lookups.
- Use [scripts/domestic_flight_public_service.py](./scripts/domestic_flight_public_service.py) only for backward compatibility.
- Use [scripts/extract_tongcheng_state.js](./scripts/extract_tongcheng_state.js) to decode the Tongcheng public page payload.
- Use [references/provider-public-web.md](./references/provider-public-web.md) for public-source notes and limitations.
