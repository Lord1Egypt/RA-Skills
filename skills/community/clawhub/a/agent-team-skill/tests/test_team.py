#!/usr/bin/env python3
"""Tests for team.py"""

import json
import os
import sys
from io import StringIO
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import team


@pytest.fixture
def temp_data_file(tmp_path: Path):
    """Create a temporary data file for testing.

    Uses environment variable for test isolation to ensure tests don't
    accidentally read/write production data.
    """
    data_file = tmp_path / "team.json"
    # Set both env var and global for robust test isolation
    os.environ["AGENT_TEAM_DATA_FILE"] = str(data_file)
    team.set_data_file(str(data_file))
    yield data_file
    # Cleanup
    team.set_data_file(None)
    os.environ.pop("AGENT_TEAM_DATA_FILE", None)


@pytest.fixture
def sample_member_data():
    """Sample member data for testing."""
    return {
        "agent_id": "agent-001",
        "name": "Alice",
        "role": "Developer",
        "is_leader": True,
        "enabled": True,
        "tags": ["backend", "api"],
        "expertise": ["python", "go"],
        "not_good_at": ["frontend"],
        "load_workflow": True,
        "group": "backend-team",
    }


class TestListCommand:
    """Tests for the list command."""

    def test_list_empty_data(self, temp_data_file, capsys):
        """Test listing when no data exists."""
        team.list_members()
        captured = capsys.readouterr()
        assert "No team members found" in captured.out

    def test_list_with_members(self, temp_data_file, sample_member_data, capsys):
        """Test listing with existing members."""
        # Save sample data
        team.save_data({"team": {"agent-001": sample_member_data}})

        team.list_members()
        captured = capsys.readouterr()

        assert "Alice" in captured.out
        assert "Developer" in captured.out
        assert "backend" in captured.out
        assert "Total: 1 member(s)" in captured.out


class TestUpdateCommand:
    """Tests for the update command."""

    def test_add_new_member(self, temp_data_file, capsys):
        """Test adding a new member."""
        team.update_member(
            agent_id="agent-001",
            name="Alice",
            role="Developer",
            is_leader=True,
            enabled=True,
            tags="backend, api",
            expertise="python, go",
            not_good_at="frontend",
        )
        captured = capsys.readouterr()
        assert "Added member: Alice (agent-001) (Leader)" in captured.out

        # Verify data was saved
        data = team.load_data()
        assert "agent-001" in data["team"]
        assert data["team"]["agent-001"]["name"] == "Alice"
        assert data["team"]["agent-001"]["is_leader"] is True

    def test_update_existing_member(self, temp_data_file, sample_member_data, capsys):
        """Test updating an existing member."""
        # Save initial data
        team.save_data({"team": {"agent-001": sample_member_data}})

        # Update the member
        team.update_member(
            agent_id="agent-001",
            name="Alice Updated",
            role="Senior Developer",
            is_leader=False,
            enabled=False,
            tags="backend, api, database",
            expertise="python, go, postgresql",
            not_good_at="frontend, design",
        )
        captured = capsys.readouterr()
        assert "Updated member: Alice Updated (agent-001)" in captured.out

        # Verify data was updated
        data = team.load_data()
        assert data["team"]["agent-001"]["name"] == "Alice Updated"
        assert data["team"]["agent-001"]["role"] == "Senior Developer"
        assert data["team"]["agent-001"]["enabled"] is False
        assert data["team"]["agent-001"]["is_leader"] is False

    def test_tags_parsing(self, temp_data_file):
        """Test that tags are correctly parsed from comma-separated string."""
        team.update_member(
            agent_id="agent-001",
            name="Test",
            role="Test",
            is_leader=False,
            enabled=True,
            tags=" tag1 , tag2 , tag3 ",
            expertise="skill1",
            not_good_at="weakness1",
        )

        data = team.load_data()
        assert data["team"]["agent-001"]["tags"] == ["tag1", "tag2", "tag3"]

    def test_only_one_leader_allowed(self, temp_data_file, capsys):
        """Test that only one leader is allowed per team."""
        # Add first member as leader
        team.update_member(
            agent_id="agent-001",
            name="Alice",
            role="Team Lead",
            is_leader=True,
            enabled=True,
            tags="backend",
            expertise="python",
            not_good_at="frontend",
        )

        # Add second member as leader
        team.update_member(
            agent_id="agent-002",
            name="Bob",
            role="Developer",
            is_leader=True,
            enabled=True,
            tags="frontend",
            expertise="react",
            not_good_at="backend",
        )
        captured = capsys.readouterr()

        # Should show that Alice's leader status was removed
        assert "Removed leader status from Alice" in captured.out
        assert "Added member: Bob (agent-002) (Leader)" in captured.out

        # Verify only Bob is leader
        data = team.load_data()
        assert data["team"]["agent-001"]["is_leader"] is False
        assert data["team"]["agent-002"]["is_leader"] is True


class TestResetCommand:
    """Tests for the reset command."""

    def test_reset_clears_data(self, temp_data_file, sample_member_data, capsys):
        """Test that reset clears all data."""
        # Save some data first
        team.save_data({"team": {"agent-001": sample_member_data}})

        # Reset
        team.reset_data()
        captured = capsys.readouterr()
        assert "reset to empty" in captured.out

        # Verify data is empty
        data = team.load_data()
        assert data["team"] == {}


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_load_data_file_not_exists(self, tmp_path):
        """Test loading when file doesn't exist."""
        non_existent = tmp_path / "nonexistent.json"
        team.set_data_file(str(non_existent))
        data = team.load_data()
        assert data == {"team": {}}
        team.set_data_file(None)

    def test_load_data_invalid_json(self, tmp_path):
        """Test loading when JSON is invalid."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("not valid json {")
        team.set_data_file(str(invalid_file))
        data = team.load_data()
        assert data == {"team": {}}
        team.set_data_file(None)

    def test_load_data_missing_team_key(self, tmp_path):
        """Test loading when JSON is missing 'team' key."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text('{"other": "data"}')
        team.set_data_file(str(bad_file))
        data = team.load_data()
        assert data == {"team": {}}
        team.set_data_file(None)

    def test_custom_data_file_path(self, tmp_path):
        """Test using a custom data file path."""
        custom_file = tmp_path / "custom_team.json"
        team.set_data_file(str(custom_file))

        team.update_member(
            agent_id="test-001",
            name="Test User",
            role="Tester",
            is_leader=False,
            enabled=True,
            tags="test",
            expertise="testing",
            not_good_at="coding",
        )

        assert custom_file.exists()
        team.set_data_file(None)


class TestCLI:
    """Tests for command-line interface."""

    def test_list_cli(self, temp_data_file, monkeypatch, capsys):
        """Test list command via CLI."""
        monkeypatch.setattr(sys, "argv", ["team.py", "--data-file", str(temp_data_file), "list"])
        team.main()
        captured = capsys.readouterr()
        assert "No team members found" in captured.out

    def test_update_cli(self, temp_data_file, monkeypatch, capsys):
        """Test update command via CLI."""
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "team.py",
                "--data-file",
                str(temp_data_file),
                "update",
                "--agent-id",
                "cli-001",
                "--name",
                "CLI User",
                "--role",
                "CLI Role",
                "--is-leader",
                "false",
                "--enabled",
                "true",
                "--tags",
                "cli",
                "--expertise",
                "testing",
                "--not-good-at",
                "nothing",
            ],
        )
        team.main()
        captured = capsys.readouterr()
        assert "Added member: CLI User (cli-001)" in captured.out

    def test_reset_cli(self, temp_data_file, sample_member_data, monkeypatch, capsys):
        """Test reset command via CLI."""
        team.save_data({"team": {"agent-001": sample_member_data}})

        monkeypatch.setattr(
            sys, "argv", ["team.py", "--data-file", str(temp_data_file), "reset"]
        )
        team.main()
        captured = capsys.readouterr()
        assert "reset to empty" in captured.out

    def test_no_command_shows_help(self, monkeypatch, capsys):
        """Test that running without command shows help."""
        monkeypatch.setattr(sys, "argv", ["team.py"])

        with pytest.raises(SystemExit) as exc_info:
            team.main()

        assert exc_info.value.code == 1


class TestNewFields:
    """Tests for new fields: load_workflow and group."""

    def test_update_with_load_workflow_true(self, temp_data_file):
        """Test adding member with load_workflow set to true."""
        team.update_member(
            agent_id="agent-001",
            name="Alice",
            role="Developer",
            is_leader=True,
            enabled=True,
            tags="backend",
            expertise="python",
            not_good_at="frontend",
            load_workflow="true",
        )

        data = team.load_data()
        assert data["team"]["agent-001"]["load_workflow"] is True

    def test_update_with_load_workflow_false(self, temp_data_file):
        """Test adding member with load_workflow set to false."""
        team.update_member(
            agent_id="agent-001",
            name="Bob",
            role="Developer",
            is_leader=False,
            enabled=True,
            tags="frontend",
            expertise="react",
            not_good_at="backend",
            load_workflow="false",
        )

        data = team.load_data()
        assert data["team"]["agent-001"]["load_workflow"] is False

    def test_update_with_group(self, temp_data_file):
        """Test adding member with group field."""
        team.update_member(
            agent_id="agent-001",
            name="Alice",
            role="Developer",
            is_leader=False,
            enabled=True,
            tags="backend",
            expertise="python",
            not_good_at="frontend",
            group="backend-team",
        )

        data = team.load_data()
        assert data["team"]["agent-001"]["group"] == "backend-team"

    def test_list_shows_group(self, temp_data_file, capsys):
        """Test that list command displays group field."""
        team.save_data({
            "team": {
                "agent-001": {
                    "agent_id": "agent-001",
                    "name": "Alice",
                    "role": "Developer",
                    "is_leader": False,
                    "enabled": True,
                    "tags": ["backend"],
                    "expertise": ["python"],
                    "not_good_at": ["frontend"],
                    "group": "backend-team",
                }
            }
        })

        team.list_members()
        captured = capsys.readouterr()
        assert "Group: backend-team" in captured.out
        assert "Alice" in captured.out

    def test_list_shows_load_workflow(self, temp_data_file, capsys):
        """Test that list command displays load_workflow field."""
        team.save_data({
            "team": {
                "agent-001": {
                    "agent_id": "agent-001",
                    "name": "Alice",
                    "role": "Developer",
                    "is_leader": False,
                    "enabled": True,
                    "tags": ["backend"],
                    "expertise": ["python"],
                    "not_good_at": ["frontend"],
                    "load_workflow": True,
                }
            }
        })

        team.list_members()
        captured = capsys.readouterr()
        assert "load_workflow: True" in captured.out

    def test_backward_compatibility_no_new_fields(self, temp_data_file):
        """Test that old data without new fields still works."""
        # Save data without new fields (old format)
        team.save_data({
            "team": {
                "agent-001": {
                    "agent_id": "agent-001",
                    "name": "Alice",
                    "role": "Developer",
                    "is_leader": True,
                    "enabled": True,
                    "tags": ["backend"],
                    "expertise": ["python"],
                    "not_good_at": ["frontend"],
                }
            }
        })

        # Should load without error
        data = team.load_data()
        assert data["team"]["agent-001"]["name"] == "Alice"
        # New fields should be missing (not error)
        assert "load_workflow" not in data["team"]["agent-001"]
        assert "group" not in data["team"]["agent-001"]

    def test_update_preserves_existing_fields(self, temp_data_file):
        """Test that updating existing member preserves new fields (merge behavior)."""
        # Save initial data with new fields
        team.save_data({
            "team": {
                "agent-001": {
                    "agent_id": "agent-001",
                    "name": "Alice",
                    "role": "Developer",
                    "is_leader": True,
                    "enabled": True,
                    "tags": ["backend"],
                    "expertise": ["python"],
                    "not_good_at": ["frontend"],
                    "load_workflow": True,
                    "group": "backend-team",
                }
            }
        })

        # Update without specifying new fields
        team.update_member(
            agent_id="agent-001",
            name="Alice Updated",
            role="Senior Developer",
            is_leader=True,
            enabled=True,
            tags="backend,api",
            expertise="python,go",
            not_good_at="frontend,design",
        )

        data = team.load_data()
        # New fields should be preserved
        assert data["team"]["agent-001"]["load_workflow"] is True
        assert data["team"]["agent-001"]["group"] == "backend-team"
        # But name and role should be updated
        assert data["team"]["agent-001"]["name"] == "Alice Updated"
        assert data["team"]["agent-001"]["role"] == "Senior Developer"

    def test_cli_with_new_fields(self, temp_data_file, monkeypatch, capsys):
        """Test update command via CLI with new fields."""
        monkeypatch.setattr(
            sys,
            "argv",
            [
                "team.py",
                "--data-file",
                str(temp_data_file),
                "update",
                "--agent-id",
                "cli-001",
                "--name",
                "CLI User",
                "--role",
                "CLI Role",
                "--is-leader",
                "false",
                "--enabled",
                "true",
                "--tags",
                "cli",
                "--expertise",
                "testing",
                "--not-good-at",
                "nothing",
                "--load-workflow",
                "true",
                "--group",
                "test-group",
            ],
        )
        team.main()
        captured = capsys.readouterr()
        assert "Added member: CLI User (cli-001)" in captured.out

        data = team.load_data()
        assert data["team"]["cli-001"]["load_workflow"] is True
        assert data["team"]["cli-001"]["group"] == "test-group"

    def test_env_var_isolation(self, temp_data_file):
        """Test that environment variable provides test isolation."""
        # temp_data_file fixture already sets AGENT_TEAM_DATA_FILE
        # and team.set_data_file(), so we just verify it works

        team.update_member(
            agent_id="env-test-001",
            name="Env Test",
            role="Tester",
            is_leader=False,
            enabled=True,
            tags="test",
            expertise="testing",
            not_good_at="nothing",
        )

        # Verify file was created at temp path
        assert temp_data_file.exists()
        data = team.load_data()
        assert data["team"]["env-test-001"]["name"] == "Env Test"

    def test_grouped_members_in_list(self, temp_data_file, capsys):
        """Test that grouped members are displayed correctly in list."""
        team.save_data({
            "team": {
                "agent-001": {
                    "agent_id": "agent-001",
                    "name": "Alice",
                    "role": "Developer",
                    "is_leader": True,
                    "enabled": True,
                    "tags": ["backend"],
                    "expertise": ["python"],
                    "not_good_at": ["frontend"],
                    "group": "backend-team",
                },
                "agent-002": {
                    "agent_id": "agent-002",
                    "name": "Bob",
                    "role": "Developer",
                    "is_leader": False,
                    "enabled": True,
                    "tags": ["frontend"],
                    "expertise": ["react"],
                    "not_good_at": ["backend"],
                    "group": "frontend-team",
                },
                "agent-003": {
                    "agent_id": "agent-003",
                    "name": "Carol",
                    "role": "Developer",
                    "is_leader": False,
                    "enabled": True,
                    "tags": ["devops"],
                    "expertise": ["kubernetes"],
                    "not_good_at": ["design"],
                    # No group - ungrouped
                },
            }
        })

        team.list_members()
        captured = capsys.readouterr()
        assert "Group: backend-team" in captured.out
        assert "Group: frontend-team" in captured.out
        assert "Alice" in captured.out
        assert "Bob" in captured.out
        assert "Carol" in captured.out