"""observe_reducer — L1 Step 1."""
def observe_fn(raw_input, state):
    return dict(
        type="text_input" if raw_input.strip() else "empty_observation",
        raw=raw_input,
        normalized=raw_input.strip().lower(),
        is_empty=not bool(raw_input.strip()),
        timestamp=0.0,
    )
