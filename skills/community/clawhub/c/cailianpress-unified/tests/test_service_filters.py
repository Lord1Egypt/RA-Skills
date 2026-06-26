from scripts.cls_service import ClsService
from scripts.models.schemas import ClsItem


class DummyService(ClsService):
    def _load_telegraph_items(self):
        items = [
            ClsItem(1, "a", "", "", "B", True, 20000, 1774577000, "2026-03-27 10:00:00", "", [], [], [], "nodeapi"),
            ClsItem(2, "b", "", "", "C", False, 5000, 1774577100, "2026-03-27 10:05:00", "", [], [], [], "nodeapi"),
            ClsItem(3, "c", "", "", "A", True, 30000, 1774577200, "2026-03-27 10:10:00", "", [], [], [], "nodeapi"),
        ]
        return items, "nodeapi", False


def test_get_red_filters_red_items():
    service = DummyService()
    result = service.get_red()
    assert result.count == 2
    assert all(item.is_red for item in result.items)


def test_get_hot_filters_by_reading():
    service = DummyService()
    result = service.get_hot(min_reading=10000)
    assert result.count == 2
    assert all(item.reading_num >= 10000 for item in result.items)
