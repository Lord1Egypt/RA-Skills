import pytest

from data_hub import DataHub


@pytest.fixture
def hub():
    return DataHub()


@pytest.fixture
def hub_with_snapshot(tmp_path):
    path = str(tmp_path / "risk_snapshot.json")
    return DataHub(snapshot_path=path), path
