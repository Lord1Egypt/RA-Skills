"""L2 degradation policy."""
def apply_degradation(level):
    policies = {
        "L0": dict(cognize=dict(update_emotion=True), decide=dict(strategies=["SPEAK","RECALL_FIRST","REPAIR","IDLE"]), speak=dict(inference_type="llm")),
        "L1": dict(cognize=dict(update_emotion=True, delta_halved=True), decide=dict(strategies=["SPEAK","RECALL"]), speak=dict(inference_type="llm")),
        "L2": dict(cognize=dict(update_emotion=False), decide=dict(strategies=["SPEAK"]), speak=dict(inference_type="template")),
        "L3": dict(cognize=dict(update_emotion=False), decide=dict(strategies=["REPAIR"]), speak=dict(inference_type="fixed")),
    }
    return policies.get(level, policies["L3"])
