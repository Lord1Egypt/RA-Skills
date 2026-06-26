from pathlib import Path


def test_skill_metadata_mentions_canvas_agent_env() -> None:
    skill = Path(__file__).resolve().parents[1] / "SKILL.md"
    text = skill.read_text()
    assert "AI_VIDEO_AGENT_TOKEN" in text
    assert "generate_image.py" in text
    assert "generate_video.py" in text
