# LiveKit Agents (Python)

```bash
pip install linepref
```

```python
from linepref import Client, OPT_OUT_DISCLOSURE
from linepref.livekit import precheck, attach_opt_out, report

lp = Client()  # optional: Client(api_key="lp_...") or set LINEPREF_KEY

async def entrypoint(ctx):
    dial_info = json.loads(ctx.job.metadata)
    number = dial_info["phone_number"]

    # 1. Check before dialling.
    result = await precheck(lp, number, website=dial_info.get("website"))
    if not result.should_call:
        # result.advice is "use_link" (see result.booking_url) or "do_not_call"
        return

    await ctx.connect()

    # 3. Key presses: 9 stops this caller, 8 stops all participating AI callers.
    def on_opt_out(scope: str) -> None:
        # say a short confirmation, then end the call
        ...
    attach_opt_out(ctx.room, lp, number, on_opt_out=on_opt_out)

    # ... create the SIP participant and start the session as usual.
    # 2. Put OPT_OUT_DISCLOSURE in the agent's first turn.

    # 5. After the call ends:
    await report(lp, number, "connected_human", hold_seconds=35, local_hour=14)
```

`attach_opt_out` listens for the room's `sip_dtmf_received` event and reads `dtmf.digit`.
The client fails open: if the service cannot be reached, `precheck` returns advice `unknown` and the call
proceeds.
