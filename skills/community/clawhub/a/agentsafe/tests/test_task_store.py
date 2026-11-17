"""Task store acceptance: restart recovery, cleanup, concurrency."""

import threading

import pytest

from agentsafe.schemas import StageState, StageStatus, TaskState
from agentsafe.task_store import (
    MemoryTaskStore,
    SqliteTaskStore,
    new_task_id,
    open_task_store,
)

ADDR = "0x" + "ab" * 20


class TestTaskId:
    def test_unguessable_and_wellformed(self):
        ids = {new_task_id() for _ in range(50)}
        assert len(ids) == 50
        for t in ids:
            assert 20 <= len(t) <= 32

    def test_no_secret_embedding(self):
        assert "ghp" not in new_task_id() and "sk-" not in new_task_id()


class TestSqliteStore:
    def test_create_get_roundtrip(self, tmp_path):
        store = SqliteTaskStore(tmp_path / "tasks.db")
        task = store.create_task(ADDR)
        assert task.state is TaskState.QUEUED
        fetched = store.get(task.task_id)
        assert fetched is not None and fetched.address == ADDR

    def test_unknown_task_returns_none(self, tmp_path):
        store = SqliteTaskStore(tmp_path / "tasks.db")
        assert store.get("nope") is None

    def test_restart_recovery_via_persistent_file(self, tmp_path):
        """Service restart = new store instance on the same db file."""
        db = tmp_path / "tasks.db"
        s1 = SqliteTaskStore(db)
        task = s1.create_task(ADDR)
        s1.link_run(task.task_id, 12345)
        s1.set_state(task.task_id, TaskState.RUNNING)
        s1.upsert_stage(task.task_id, StageStatus(name="fetch_source", state=StageState.COMPLETED))

        s2 = SqliteTaskStore(db)  # "restarted" service
        recovered = s2.get(task.task_id)
        assert recovered is not None
        assert recovered.run_id == 12345
        assert recovered.state is TaskState.RUNNING
        assert recovered.stages[0].name == "fetch_source"

    def test_concurrent_updates_are_serialized(self, tmp_path):
        store = SqliteTaskStore(tmp_path / "tasks.db")
        task = store.create_task(ADDR)

        def hammer(i):
            store.link_run(task.task_id, i)
            store.set_state(task.task_id, TaskState.RUNNING)
            store.upsert_stage(
                task.task_id, StageStatus(name=f"stage{i}", state=StageState.RUNNING)
            )

        threads = [threading.Thread(target=hammer, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        got = store.get(task.task_id)
        assert got.run_id is not None
        assert len(got.stages) == 8

    def test_link_run_unknown_task_raises(self, tmp_path):
        store = SqliteTaskStore(tmp_path / "tasks.db")
        with pytest.raises(KeyError):
            store.link_run("missing", 1)

    def test_cleanup_expired(self, tmp_path):
        import time

        store = SqliteTaskStore(tmp_path / "tasks.db")
        task = store.create_task(ADDR)
        time.sleep(0.02)  # guarantee created_at < cutoff (Windows clock ticks)
        assert store.cleanup_expired(retention_days=0) == 1
        assert store.get(task.task_id) is None


class TestMemoryStore:
    def test_basic_flow(self):
        store = MemoryTaskStore()
        task = store.create_task(ADDR)
        store.link_run(task.task_id, 7)
        store.set_state(task.task_id, TaskState.COMPLETED)
        got = store.get(task.task_id)
        assert got.run_id == 7 and got.state is TaskState.COMPLETED
        assert store.get("zzz") is None

    def test_cleanup(self):
        import time

        store = MemoryTaskStore()
        store.create_task(ADDR)
        time.sleep(0.02)
        assert store.cleanup_expired(retention_days=0) == 1


class TestFactory:
    def test_open_store_modes(self, tmp_path):
        assert isinstance(open_task_store("sqlite", tmp_path / "t.db"), SqliteTaskStore)
        assert isinstance(open_task_store("memory", tmp_path / "t.db"), MemoryTaskStore)
        with pytest.raises(ValueError):
            open_task_store("redis", tmp_path / "t.db")


class _FakePipeline:
    def __init__(self, store: "_FakeRedis"):
        self._store = store
        self._ops: list[tuple[str, tuple]] = []

    def set(self, key, value, ex=None):
        self._ops.append(("set", (key, value, ex)))
        return self

    def execute(self):
        for op, args in self._ops:
            self._store.data[args[0]] = args[1]
        return [True] * len(self._ops)


class _FakeRedis:
    """Minimal redis-py surface used by RedisTaskStore (no network I/O)."""

    def __init__(self):
        self.data: dict[str, str] = {}

    def pipeline(self):
        return _FakePipeline(self)

    def set(self, key, value, ex=None):
        self.data[key] = value
        return True

    def get(self, key):
        return self.data.get(key)

    def mget(self, keys):
        return [self.data.get(k) for k in keys]

    def scan_iter(self, match=None, count=None):
        import fnmatch

        for key in list(self.data):
            if fnmatch.fnmatchcase(key, match or "*"):
                yield key

    def ping(self):
        return True


class TestRedisStore:
    """RedisTaskStore behavior with a fake client (offline, hermetic)."""

    @pytest.fixture()
    def store(self, monkeypatch):
        import agentsafe.task_store as ts

        fake = _FakeRedis()
        captured: dict = {}

        def fake_from_url(url, **kwargs):
            captured["url"] = url
            captured["kwargs"] = kwargs
            return fake

        monkeypatch.setattr(ts.redis_client, "from_url", fake_from_url)
        # rediss:// TLS URL must be accepted unchanged.
        store = ts.RedisTaskStore("rediss://default:secret@upstash.example:6379")
        assert captured["url"].startswith("rediss://")
        assert captured["kwargs"]["socket_connect_timeout"] > 0
        return store

    def test_create_get_roundtrip(self, store):
        task = store.create_task(ADDR)
        loaded = store.get(task.task_id)
        assert loaded is not None
        assert loaded.task_id == task.task_id
        assert loaded.address == ADDR
        assert loaded.state == TaskState.QUEUED

    def test_get_unknown_returns_none(self, store):
        assert store.get(new_task_id()) is None

    def test_link_run_and_state_persist(self, store):
        task = store.create_task(ADDR)
        store.link_run(task.task_id, 12345)
        store.set_state(task.task_id, TaskState.RUNNING)
        loaded = store.get(task.task_id)
        assert loaded.run_id == 12345
        assert loaded.state == TaskState.RUNNING

    def test_mark_paid_and_payment_refs(self, store):
        task = store.create_task(ADDR)
        store.mark_paid(task.task_id, "ref-abc-123")
        loaded = store.get(task.task_id)
        assert loaded.paid is True
        assert loaded.payment_ref == "ref-abc-123"
        assert store.payment_refs() == {"ref-abc-123"}

    def test_unknown_task_mutations_raise(self, store):
        with pytest.raises(KeyError):
            store.link_run(new_task_id(), 1)
        with pytest.raises(KeyError):
            store.set_state(new_task_id(), TaskState.RUNNING)
        with pytest.raises(KeyError):
            store.mark_paid(new_task_id(), "ref")
