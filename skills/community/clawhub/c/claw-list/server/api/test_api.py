import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

os.environ.update({"POSTGRES_USER":"x","POSTGRES_PASSWORD":"x","POSTGRES_DB":"x"})

from sqlalchemy.pool import StaticPool
from main import app, Base, get_db

import main as _main
_sqlite_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_main.engine = _sqlite_engine
TestSession = sessionmaker(bind=_sqlite_engine)
Base.metadata.create_all(bind=_sqlite_engine)

def override_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_db
client = TestClient(app)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def clean_db():
    # Wipe all tables between tests
    db = TestSession()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()

def make_agent(agent_id, display_name="Test", scope="own"):
    return client.post("/admin/agents", json={
        "agent_id": agent_id, "display_name": display_name, "scope": scope
    })

def make_list(agent_id, name="My List"):
    return client.post("/lists", json={"name": name}, headers={"x-agent-id": agent_id})

def make_item(agent_id, list_id, title="Do something", **kwargs):
    return client.post(f"/lists/{list_id}/items",
        json={"title": title, **kwargs}, headers={"x-agent-id": agent_id})


# ── Admin: agents ─────────────────────────────────────────────────────────────

def test_create_agent():
    r = make_agent("agent1", "Agent One", "own")
    assert r.status_code == 201
    assert r.json()["scope"] == "own"

def test_create_agent_duplicate():
    make_agent("agent1")
    r = make_agent("agent1")
    assert r.status_code == 409

def test_list_agents():
    make_agent("a1")
    make_agent("a2")
    r = client.get("/admin/agents")
    assert r.status_code == 200
    assert len(r.json()) == 2

def test_update_agent_scope():
    make_agent("agent1", scope="own")
    r = client.put("/admin/agents/agent1", json={"scope": "all"})
    assert r.status_code == 200
    assert r.json()["scope"] == "all"

def test_delete_agent():
    make_agent("agent1")
    r = client.delete("/admin/agents/agent1")
    assert r.status_code == 204
    r = client.get("/admin/agents")
    assert r.json() == []


# ── Unknown agent is rejected ─────────────────────────────────────────────────

def test_unknown_agent_rejected():
    r = client.get("/lists", headers={"x-agent-id": "ghost"})
    assert r.status_code == 403


# ── Lists ─────────────────────────────────────────────────────────────────────

def test_create_list():
    make_agent("agent1")
    r = make_list("agent1", "Shopping")
    assert r.status_code == 201
    assert r.json()["name"] == "Shopping"
    assert r.json()["agent_id"] == "agent1"

def test_own_scope_sees_only_own_lists():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="own")
    make_list("agent1", "List A")
    make_list("agent2", "List B")

    r = client.get("/lists", headers={"x-agent-id": "agent1"})
    names = [l["name"] for l in r.json()]
    assert "List A" in names
    assert "List B" not in names

def test_all_scope_sees_all_lists():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="all")
    make_list("agent1", "List A")
    make_list("agent2", "List B")

    r = client.get("/lists", headers={"x-agent-id": "agent2"})
    names = [l["name"] for l in r.json()]
    assert "List A" in names
    assert "List B" in names

def test_cannot_delete_other_agents_list():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="own")
    list_id = make_list("agent1").json()["id"]

    r = client.delete(f"/lists/{list_id}", headers={"x-agent-id": "agent2"})
    assert r.status_code == 403

def test_all_scope_cannot_delete_other_agents_list():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="all")
    list_id = make_list("agent1").json()["id"]

    r = client.delete(f"/lists/{list_id}", headers={"x-agent-id": "agent2"})
    assert r.status_code == 403


# ── Items ─────────────────────────────────────────────────────────────────────

def test_create_item_with_notes():
    make_agent("agent1")
    list_id = make_list("agent1").json()["id"]
    r = make_item("agent1", list_id, "Fix the thing", notes="Context from conversation", priority=2)
    assert r.status_code == 201
    assert r.json()["notes"] == "Context from conversation"
    assert r.json()["priority"] == 2

def test_own_scope_cannot_read_other_agents_list_items():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="own")
    list_id = make_list("agent1").json()["id"]

    r = client.get(f"/lists/{list_id}/items", headers={"x-agent-id": "agent2"})
    assert r.status_code == 403

def test_all_scope_can_read_other_agents_list_items():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="all")
    list_id = make_list("agent1").json()["id"]
    make_item("agent1", list_id, "Secret task")

    r = client.get(f"/lists/{list_id}/items", headers={"x-agent-id": "agent2"})
    assert r.status_code == 200
    assert r.json()[0]["title"] == "Secret task"

def test_own_scope_cannot_add_item_to_other_agents_list():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="own")
    list_id = make_list("agent1").json()["id"]

    r = make_item("agent2", list_id, "Sneaky task")
    assert r.status_code == 403

def test_all_scope_cannot_add_item_to_other_agents_list():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="all")
    list_id = make_list("agent1").json()["id"]

    r = make_item("agent2", list_id, "Sneaky task")
    assert r.status_code == 403

def test_update_item():
    make_agent("agent1")
    list_id = make_list("agent1").json()["id"]
    item_id = make_item("agent1", list_id, "Old title").json()["id"]

    r = client.put(f"/items/{item_id}",
        json={"title": "New title", "done": True},
        headers={"x-agent-id": "agent1"})
    assert r.status_code == 200
    assert r.json()["title"] == "New title"
    assert r.json()["done"] is True

def test_cannot_update_other_agents_item():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="all")
    list_id = make_list("agent1").json()["id"]
    item_id = make_item("agent1", list_id, "Agent1 task").json()["id"]

    r = client.put(f"/items/{item_id}",
        json={"title": "Hijacked"},
        headers={"x-agent-id": "agent2"})
    assert r.status_code == 403

def test_delete_item():
    make_agent("agent1")
    list_id = make_list("agent1").json()["id"]
    item_id = make_item("agent1", list_id).json()["id"]

    r = client.delete(f"/items/{item_id}", headers={"x-agent-id": "agent1"})
    assert r.status_code == 204

def test_cannot_delete_other_agents_item():
    make_agent("agent1", scope="own")
    make_agent("agent2", scope="own")
    list_id = make_list("agent1").json()["id"]
    item_id = make_item("agent1", list_id).json()["id"]

    r = client.delete(f"/items/{item_id}", headers={"x-agent-id": "agent2"})
    assert r.status_code == 403
