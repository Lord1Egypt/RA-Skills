"""
Preset dance for FAMIBOT action_sequence.

Only routine: showcase_custom — fixed script with open/act1/act2/close (see _showcase_custom_script).
"""

from __future__ import annotations

VOICE_FILES = {
    "cheerful": ("happy-h-2", 3000),
}

# Legacy flow-dance helper (ecovacs._routine_gap_ms); only showcase_custom is registered
TEMPO_PROFILES = {
    "cheerful": {"beat_gap_ms": 180},
    "intense": {"beat_gap_ms": 100},
    "normal": {"beat_gap_ms": 200},
}

# Used by ecovacs.compile when bookends=True (no current routine uses this)
DANCE_BOOKEND_BARK_COUNT = 3
DANCE_BOOKEND_BODY_GAP_MS = 120
DANCE_BOOKEND_BARK_INTERVAL_MS = {"cheerful": 220}
DANCE_BOOKEND_BARK_MOVE_MS_CAP = {"cheerful": 900}


def bookend_bark_config(tempo="cheerful"):
    vf, vms = VOICE_FILES["cheerful"]
    return vf, min(vms, DANCE_BOOKEND_BARK_MOVE_MS_CAP["cheerful"]), DANCE_BOOKEND_BARK_INTERVAL_MS["cheerful"]


SHOWCASE_STEP_GAP_MS = 50
SHOWCASE_TAIL_HOLD_MS = 3000
SHOWCASE_BARK_MS = 700
SHOWCASE_BARK_INTERVAL_MS = 150


def _showcase_action(action_type, delay_ms, **fields):
    return {"type": action_type, "delay": str(int(delay_ms)), **fields}


def _showcase_head_duration_ms(move_ms, count):
    ms = int(move_ms)
    c = int(count)
    return ms if c <= 1 else ms * c * 2


def _showcase_custom_script():
    """
    定制秀舞 — 脚本内自带开/收场（bookends=False）。

    开场：向下点头×3 + 连叫×3 + 尾快速摆 3s（同拍）
    第一场×3：左右摇×6 + 尾慢摆 3s + 眨眼；每轮 1 叫
    第二场×2：快扭×5+快尾×5 → 慢扭×5+慢尾×5 → 快摇×5+快尾×5 → 慢摇×5+慢尾×5 → 1 叫
    收场：向下点头×3 + 尾快速摆 3s + 连叫×3（同拍）
    """
    vf = VOICE_FILES["cheerful"][0]
    actions = []
    t = 0
    gap = SHOWCASE_STEP_GAP_MS

    def emit(delay, action_type, **fields):
        actions.append(_showcase_action(action_type, delay, **fields))

    def emit_parallel(delay, *specs):
        for spec in specs:
            kind = spec["type"]
            payload = {k: v for k, v in spec.items() if k != "type"}
            emit(delay, kind, **payload)

    def emit_barks(delay, times=1):
        for i in range(int(times)):
            emit(
                delay + i * SHOWCASE_BARK_INTERVAL_MS,
                "play_sound",
                file=vf,
                moveTimeMs=str(SHOWCASE_BARK_MS),
                count="1",
            )

    def advance(span_ms):
        nonlocal t
        t += int(span_ms) + gap

    def tail_hold(percent, move_ms=SHOWCASE_TAIL_HOLD_MS):
        return {
            "type": "wag_tail",
            "percent": str(int(percent)),
            "moveTimeMs": str(int(move_ms)),
        }

    def tail_swings(percent, move_ms):
        return {
            "type": "wag_tail",
            "percent": str(int(percent)),
            "moveTimeMs": str(int(move_ms)),
        }

    emit_parallel(
        t,
        {
            "type": "nod_head",
            "angle": "-14",
            "moveTimeMs": "420",
            "count": "3",
            "ctrlpoint": "",
        },
        tail_hold(92),
    )
    emit_barks(t, 3)
    open_span = max(
        _showcase_head_duration_ms(420, 3),
        SHOWCASE_TAIL_HOLD_MS,
        SHOWCASE_BARK_MS + 2 * SHOWCASE_BARK_INTERVAL_MS,
    )
    advance(open_span)

    for _ in range(3):
        emit_parallel(
            t,
            {
                "type": "shake_head",
                "angle": "44",
                "moveTimeMs": "260",
                "count": "6",
                "ctrlpoint": "",
            },
            tail_hold(48),
            {
                "type": "eye_control",
                "direct": "0",
                "eyetype": "3",
                "narrow": "1",
                "percent": "70",
                "moveTimeMs": "280",
                "count": "2",
                "blinkMoveTime": "120",
            },
        )
        act1_span = max(_showcase_head_duration_ms(260, 6), SHOWCASE_TAIL_HOLD_MS, 560)
        advance(act1_span)
        emit_barks(t, 1)
        advance(SHOWCASE_BARK_MS)

    act2_blocks = [
        (
            {"type": "cock_head", "angle": "18", "moveTimeMs": "240", "count": "5", "ctrlpoint": ""},
            tail_swings(90, 1900),
        ),
        (
            {"type": "cock_head", "angle": "16", "moveTimeMs": "400", "count": "5", "ctrlpoint": ""},
            tail_swings(42, 2800),
        ),
        (
            {"type": "shake_head", "angle": "42", "moveTimeMs": "240", "count": "5", "ctrlpoint": ""},
            tail_swings(88, 1900),
        ),
        (
            {"type": "shake_head", "angle": "38", "moveTimeMs": "380", "count": "5", "ctrlpoint": ""},
            tail_swings(40, 2800),
        ),
    ]
    for _ in range(2):
        for head_spec, tail_spec in act2_blocks:
            emit_parallel(t, head_spec, tail_spec)
            head_ms = int(head_spec["moveTimeMs"])
            head_count = int(head_spec["count"])
            tail_ms = int(tail_spec["moveTimeMs"])
            advance(max(_showcase_head_duration_ms(head_ms, head_count), tail_ms))
        emit_barks(t, 1)
        advance(SHOWCASE_BARK_MS)

    emit_parallel(
        t,
        {
            "type": "nod_head",
            "angle": "-14",
            "moveTimeMs": "420",
            "count": "3",
            "ctrlpoint": "",
        },
        tail_hold(92),
    )
    emit_barks(t, 3)
    return actions


DANCE_ROUTINES = {
    "showcase_custom": {
        "label": "定制秀舞",
        "tempo": "cheerful",
        "mode": "voice",
        "timing": "script",
        "bookends": False,
        "build": _showcase_custom_script,
    },
}

DEFAULT_DANCE_ROUTINE = "showcase_custom"

DANCE_ROUTINE_ALIASES = {
    "showcase_custom": "showcase_custom",
    "showcase": "showcase_custom",
    "定制舞": "showcase_custom",
    "秀舞": "showcase_custom",
    "定制秀舞": "showcase_custom",
    "dance": "showcase_custom",
    "跳舞": "showcase_custom",
    "跳": "showcase_custom",
    "跳个短舞": "showcase_custom",
    "短舞": "showcase_custom",
    # legacy → same dance
    "cheerful": "showcase_custom",
    "happy": "showcase_custom",
    "欢快": "showcase_custom",
    "欢快舞": "showcase_custom",
    "cheerful_motion": "showcase_custom",
    "cheerful_voice": "showcase_custom",
    "intense": "showcase_custom",
    "激烈": "showcase_custom",
    "intense_motion": "showcase_custom",
    "intense_voice": "showcase_custom",
    "normal": "showcase_custom",
    "正常": "showcase_custom",
    "normal_motion": "showcase_custom",
    "normal_voice": "showcase_custom",
    "nod": "showcase_custom",
    "点头舞": "showcase_custom",
    "nod_cheerful": "showcase_custom",
    "shake": "showcase_custom",
    "摇头舞": "showcase_custom",
    "shake_cheerful": "showcase_custom",
    "party": "showcase_custom",
    "派对": "showcase_custom",
}


def normalize_dance_routine(name):
    key = str(name or DEFAULT_DANCE_ROUTINE).strip().lower()
    rid = DANCE_ROUTINE_ALIASES.get(key, key)
    if rid not in DANCE_ROUTINES:
        known = ", ".join(sorted(DANCE_ROUTINES.keys()))
        raise SystemExit(f"未知跳舞 routine: {name!r}。可选: {known}")
    return rid


def list_dance_routine_ids():
    return sorted(DANCE_ROUTINES.keys())


def get_dance_routine_meta(routine_id):
    return DANCE_ROUTINES[normalize_dance_routine(routine_id)]
