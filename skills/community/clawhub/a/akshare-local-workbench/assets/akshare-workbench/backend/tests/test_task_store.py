import pandas as pd

from app.catalog.loader import get_indicator
from app.services.task_store import InMemoryTaskStore


def test_task_store_keeps_latest_task_only():
    indicator = get_indicator("stock_sh_a_spot")
    assert indicator is not None
    store = InMemoryTaskStore()

    first = store.create(indicator, pd.DataFrame([{"code": "000001"}]))
    second = store.create(indicator, pd.DataFrame([{"code": "000002"}]))

    assert store.get(first.task_id) is None
    assert store.get(second.task_id) is not None
