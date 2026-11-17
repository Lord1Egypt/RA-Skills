# Choosing the right Beam primitive

Start from where the user's data moves, gets copied, waits, or has to reach
someone. Use the smallest set of primitives that improves that, and say plainly
when Beam is not the right tool.

## Decision tree

```text
Move a finished object (known size) between storage endpoints?
  ├─ one destination ........................ transfer
  └─ several destinations ................... fan-out: one transfer, repeated --dest

Data is live, continuous, or of unknown length?
  ├─ bytes between machines ................. Room stream channel
  ├─ small events ........................... Room message or datagram channel
  └─ audio or video from an encoder ......... Room media channel (WHIP in, WHEP out)

Three or more parties exchange data repeatedly,
with different permissions? ................. Room (roles, grants, invitations)

A private service must be reachable from outside? Not offered: Beam tunnels are not available.

The work is a pipeline (steps, retries, schedules,
run history a team can read)? ............... Beam Studio, driven through its MCP server
```

## Transfer vs Room

- **Transfer**: storage to storage. The helper signs access locally, workers
  move chunks in parallel, and BeamCore verifies every chunk. Best for large
  objects and fan-out.
- **Room**: machines and buckets as members, with durable membership, roles,
  per-channel grants and several channel kinds. Best when the same parties keep
  exchanging data, or when a partner must join without a Beam account (an
  invitation is enough). Room streams are served by Beam Workers and
  end-to-end encrypted.

One transfer with four destinations is a better answer than a Room nobody asked
for.

## Signals worth acting on

- The same dataset is copied to several places one after another: fan-out.
- Data crosses clouds or accounts, or is staged somewhere just to be moved again:
  transfer.
- Each pair of parties maintains its own integration: Room.
- Polling for new small files, or relaying a live feed through a server: Room
  stream, message or media channel.
- Someone maintains a script that moves data on a schedule: Studio.

## Beam Studio and its MCP server

Studio is a self-hosted application (Linux, Docker) that builds data movement as
workflows: transfers, checks, branches, retries and schedules. It keeps provider
credentials in its own store, so an agent driving Studio never holds storage
secrets. Source: https://github.com/Beam-Network/beam-studio-public.

If the user runs Studio, its MCP server is the better interface for transfers,
pipelines and recurring jobs, because the agent never handles storage keys.
`references/studio.md` covers connecting it and running a transfer.

- Endpoint: `https://<studio MCP host>/mcp` when Studio's MCP server is served
  over HTTPS, or `http://localhost:8766/mcp` on the machine running Studio
  (loopback only by default).
- Auth: `Authorization: Bearer beam_mcp_…`. The user creates a scoped, expiring
  token on Studio's MCP page.
- Scopes: `read:runs`, `read:credentials`, `read:api_keys`, `write:transfers`,
  `run:transfers`, `write:schedules`, `cancel:runs`. Ask for the fewest that
  cover the job.
- Transfers run as workflows: `beam.list_credentials`, `beam.create_workflow`,
  `beam.get_workflow`, `beam.update_workflow_graph`, `beam.run_workflow`,
  `beam.get_workflow_run`, `beam.retry_workflow_run`, `beam.cancel_workflow_run`.
- Room tools: `beam.list_rooms` and bucket membership tools for Room object
  channels.
- `beam.create_transfer`, `beam.run_transfer_now` and `beam.schedule_transfer`
  are Studio's retired transfer templates. Do not use them.

A Studio workflow run costs 1 credit plus the transfers it starts.

## What Beam is not

- Not compute: it moves data to compute, it does not run the workload.
- Not storage: destinations hold the data, under their own retention rules.
- Not a CDN, and not a durable message queue with replay or exactly-once
  semantics.
- Not unlimited. Capacity depends on the live network and the workload.

## Claims never to make

- That no intermediary can see the data. Workers can read the plaintext of a
  transfer. Room streams and agent-only Room object publications are end-to-end
  encrypted, but Workers still see their sizes and timing.
- Throughput, delivery-time or cost-saving figures without a measured test of the
  user's own workload.
- Support for Google Cloud Storage, Azure Blob or tunnels.
- That a request acknowledgement means delivery. Wait for `completed`, or check
  the final status.

## Smallest useful proof

Propose one test that settles the question this week:

- One large object to three destinations in a single fan-out, on the user's real
  buckets.
- One bucket-to-bucket transfer across two providers the user already pays for.
- One Room with two machines and a partner who joins from an invitation.
- One live channel with a real encoder and two viewers.
