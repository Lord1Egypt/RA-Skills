"""Tests for the notification module (roundtable.notify)."""

from __future__ import annotations

from roundtable.notify import Notifier, validate_notification_config

# ---------------------------------------------------------------------------
# Notifier basics
# ---------------------------------------------------------------------------


def test_notifier_disabled_by_default():
    """Notifier with no config should be disabled."""
    n = Notifier(None)
    assert n.enabled is False
    assert n.should_notify("speech") is False


def test_notifier_enabled_with_config():
    """Notifier with enabled=True and channels should be enabled."""
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_123"}]},
        send_fn=lambda p, c, m: sent.append((p, c, m)),
    )
    assert n.enabled is True
    assert n.should_notify("speech") is True


def test_notifier_enabled_when_channels_are_configured():
    """Providing channels should enable notifications unless explicitly disabled."""
    sent = []
    n = Notifier(
        {"channels": [{"platform": "feishu", "chat_id": "oc_123"}]},
        send_fn=lambda p, c, m: sent.append((p, c, m)),
    )
    assert n.enabled is True
    n.notify("concluded", discussion_id="rt_x", topic="T", conclusion="done")
    assert len(sent) == 1


def test_notifier_respects_explicit_disabled_with_channels():
    n = Notifier(
        {"enabled": False, "channels": [{"platform": "feishu", "chat_id": "oc_123"}]},
        send_fn=lambda p, c, m: None,
    )
    assert n.enabled is False


def test_notifier_no_send_fn():
    """Notifier without send_fn should be disabled even with config."""
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_123"}]},
    )
    assert n.enabled is False


def test_notifier_no_channels():
    """Notifier with empty channels should be disabled."""
    n = Notifier(
        {"enabled": True, "channels": []},
        send_fn=lambda p, c, m: None,
    )
    assert n.enabled is False


def test_notifier_events_filter():
    """Only subscribed events should pass the filter."""
    sent = []
    n = Notifier(
        {
            "enabled": True,
            "channels": [{"platform": "feishu", "chat_id": "oc_123"}],
            "events": ["speech"],
        },
        send_fn=lambda p, c, m: sent.append(m),
    )
    assert n.should_notify("speech") is True
    assert n.should_notify("round_start") is False
    assert n.should_notify("round_end") is False
    assert n.should_notify("concluded") is False


# ---------------------------------------------------------------------------
# Message formatting
# ---------------------------------------------------------------------------


def test_format_speech_message():
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}]},
        send_fn=lambda p, c, m: sent.append(m),
    )
    n.notify(
        "speech",
        discussion_id="rt_abcd1234",
        topic="Test Topic",
        participant="alice",
        display_name="Alice",
        role="Engineer",
        round_num=1,
        content="Hello world",
    )
    assert len(sent) == 1
    msg = sent[0]
    assert "rt_abcd1234" in msg
    assert "Alice" in msg
    assert "(Engineer)" in msg
    assert "第1轮" in msg
    assert "Hello world" in msg


def test_format_round_start_message():
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}]},
        send_fn=lambda p, c, m: sent.append(m),
    )
    n.notify(
        "round_start",
        discussion_id="rt_test",
        topic="My Topic",
        round_num=2,
    )
    assert len(sent) == 1
    assert "第2轮讨论开始" in sent[0]


def test_format_round_end_message():
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}]},
        send_fn=lambda p, c, m: sent.append(m),
    )
    n.notify(
        "round_end",
        discussion_id="rt_test",
        topic="T",
        round_num=3,
        convergence=0.75,
        key_points=["Point A", "Point B"],
    )
    assert len(sent) == 1
    msg = sent[0]
    assert "第3轮讨论结束" in msg
    assert "0.75" in msg
    assert "Point A" in msg


def test_format_concluded_message():
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}]},
        send_fn=lambda p, c, m: sent.append(m),
    )
    n.notify(
        "concluded",
        discussion_id="rt_test",
        topic="T",
        conclusion="We agreed on X",
        convergence=0.9,
        consensus_points=["Agreed on A"],
        disagreement_points=["Disagree on B"],
    )
    assert len(sent) == 1
    msg = sent[0]
    assert "讨论结束" in msg
    assert "We agreed on X" in msg
    assert "0.90" in msg


def test_concluded_message_keeps_full_conclusion():
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}]},
        send_fn=lambda p, c, m: sent.append(m),
    )
    conclusion = "x" * 500
    n.notify(
        "concluded",
        discussion_id="rt_test",
        topic="T",
        conclusion=conclusion,
    )
    assert conclusion in sent[0]


def test_content_truncation():
    """Content over 200 chars should be truncated."""
    sent = []
    n = Notifier(
        {"enabled": True, "channels": [{"platform": "feishu", "chat_id": "oc_x"}]},
        send_fn=lambda p, c, m: sent.append(m),
    )
    long_content = "x" * 300
    n.notify(
        "speech",
        discussion_id="rt_test",
        topic="T",
        participant="alice",
        display_name="Alice",
        round_num=1,
        content=long_content,
    )
    msg = sent[0]
    assert "..." in msg
    assert len(msg) < 400  # Reasonable length


# ---------------------------------------------------------------------------
# Multi-channel dispatch
# ---------------------------------------------------------------------------


def test_multi_channel_dispatch():
    """Messages should be sent to all configured channels."""
    sent = []
    n = Notifier(
        {
            "enabled": True,
            "channels": [
                {"platform": "feishu", "chat_id": "oc_1"},
                {"platform": "feishu", "chat_id": "oc_2"},
            ],
        },
        send_fn=lambda p, c, m: sent.append((c, m)),
    )
    n.notify("speech", discussion_id="rt_x", topic="T", participant="a", display_name="A", round_num=1, content="hi")
    assert len(sent) == 2
    assert sent[0][0] == "oc_1"
    assert sent[1][0] == "oc_2"


def test_channel_send_failure_isolated():
    """Failure on one channel should not affect others."""
    call_count = [0]

    def flaky_send(p, c, m):
        call_count[0] += 1
        if c == "oc_fail":
            raise RuntimeError("boom")

    sent = []
    n = Notifier(
        {
            "enabled": True,
            "channels": [
                {"platform": "feishu", "chat_id": "oc_fail"},
                {"platform": "feishu", "chat_id": "oc_ok"},
            ],
        },
        send_fn=flaky_send,
    )
    # Use a wrapper to also track ok sends
    original_send = n._send_fn

    def tracking_send(p, c, m):
        if original_send:
            original_send(p, c, m)
        if c == "oc_ok":
            sent.append(m)

    n._send_fn = tracking_send

    n.notify("speech", discussion_id="rt_x", topic="T", participant="a", display_name="A", round_num=1, content="hi")
    assert len(sent) == 1  # oc_ok received the message


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_validate_valid_config():
    errors = validate_notification_config(
        {
            "enabled": True,
            "channels": [{"platform": "feishu", "chat_id": "oc_123"}],
            "events": ["speech", "round_end"],
        }
    )
    assert errors == []


def test_validate_invalid_channels():
    errors = validate_notification_config({"channels": "not_a_list"})
    assert any("channels" in e for e in errors)


def test_validate_missing_chat_id():
    errors = validate_notification_config(
        {
            "channels": [{"platform": "feishu"}],
        }
    )
    assert any("chat_id" in e for e in errors)


def test_validate_unknown_events():
    errors = validate_notification_config(
        {
            "events": ["speech", "bogus_event"],
        }
    )
    assert any("bogus_event" in e for e in errors)


def test_validate_not_dict():
    errors = validate_notification_config("not a dict")
    assert len(errors) == 1
