# Pipecat (Python)

```bash
pip install linepref
```

Run the check before starting the call, handle key presses from your telephony transport, and report when the
pipeline ends.

```python
import asyncio
from linepref import Client, OPT_OUT_DISCLOSURE

lp = Client()

async def place_call(number: str, website: str | None = None):
    # 1. Check before dialling.
    result = await asyncio.to_thread(lp.check, number, website)
    if not result.should_call:
        return result  # use result.booking_url, or do not contact

    # 2. Add OPT_OUT_DISCLOSURE to the first thing the bot says.
    # ... build and run the pipeline ...

    # 5. After the pipeline finishes:
    await asyncio.to_thread(lp.report_outcome, number, "connected_human")
    return result

# 3. Wherever your transport delivers a DTMF key press (for example an input DTMF frame's digit):
async def on_dtmf(number: str, digit: str):
    scope = await asyncio.to_thread(lp.handle_key_press, number, str(digit))
    if scope:
        ...  # confirm briefly and end the call
```

`handle_key_press` records an opt-out for key 9 (this caller) or 8 (all participating AI callers) and returns
the scope, or `None` for any other key.
