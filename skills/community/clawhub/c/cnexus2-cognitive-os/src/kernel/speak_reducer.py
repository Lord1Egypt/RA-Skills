"""speak_reducer — L1 Step 4.

Signature:
    speak_fn(decision, context, state, *, degradation_level="L0") -> Response

§03 Rules:
    1. IDLE strategy -> empty text, inference_type="idle"
    2. SPEAK strategy -> passes context to inference, returns response with text
    3. No state mutation
    4. degradation_level alters inference_type:
       L0/L1 -> "llm"
       L2     -> "template"
       L3     -> "fixed" (REFUGE mode)
"""

_DEGRADATION_INFERENCE_MAP = {
    "L0": "llm",
    "L1": "llm",
    "L2": "template",
    "L3": "fixed",
}

def speak_fn(decision, context, state, **kwargs):
    degradation_level = kwargs.get("degradation_level", "L0")

    strategy = decision.get("strategy", "SPEAK")

    if strategy == "IDLE":
        return dict(text="", inference_type="idle", confidence=1.0,
                    latency_ms=0, metadata={})

    # SPEAK or other strategies
    inference_type = _DEGRADATION_INFERENCE_MAP.get(degradation_level, "llm")

    return dict(
        text=context.get("context_bundle", ""),
        inference_type=inference_type,
        confidence=decision.get("confidence", 0.5),
        latency_ms=0,
        metadata={"degradation_level": degradation_level},
    )
