import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]


def load_main(monkeypatch):
    monkeypatch.syspath_prepend(str(SKILL_DIR))
    spec = importlib.util.spec_from_file_location("fs_wc_main_test", SKILL_DIR / "main.py")
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sample_market(**overrides):
    market = {
        "market_id": 30,
        "title": "Folarin Balogun (R32)",
        "lower_bound": -2.5,
        "upper_bound": 25.5,
        "num_buckets": 28,
        "state_vector": [0.0] * 28,
        "metadata": {
            "scope": "World Cup",
            "categories": ["WC"],
            "position": "FWD",
            "round": "R32",
            "player": "Folarin Balogun",
            "team": "USA",
            "expectedPts": 6.11,
        },
    }
    market.update(overrides)
    return market


def test_strategy_default_uses_multimodal_density_recipe(monkeypatch):
    module = load_main(monkeypatch)
    recipe, pos, expected, desc = module.strategy_for_market(sample_market())

    assert pos == "FWD"
    assert expected == pytest.approx(6.11)
    assert recipe["position_type"] == "density"
    density = recipe["position_params"]["density"]
    assert len(density) == 28
    assert sum(density) == pytest.approx(1.0)

    # Multimodal: the low appearance cluster and higher return cluster should
    # produce at least two local maxima rather than one symmetric Gaussian peak.
    peaks = [
        i for i in range(1, len(density) - 1)
        if density[i] > density[i - 1] and density[i] > density[i + 1]
    ]
    assert len(peaks) >= 2
    assert "multimodal" in desc


def test_recipe_mean_norm_supports_density(monkeypatch):
    module = load_main(monkeypatch)
    market = sample_market(num_buckets=4, lower_bound=0, upper_bound=4)
    recipe = {"position_type": "density", "position_params": {"density": [0, 1, 0, 0]}}
    # Bucket centers are 0.5, 1.5, 2.5, 3.5 -> normalized mean 1.5/4.
    assert module.recipe_mean_norm(recipe, market) == pytest.approx(0.375)


class RetryClient:
    err_cls: Any

    def __init__(self):
        self.buy_calls = 0
        self.relogin_calls = 0

    def buy(self, *args, **kwargs):
        self.buy_calls += 1
        if self.buy_calls == 1:
            raise self.err_cls(401, "expired")
        return {"position_id": 4, "trade_size": 123.0}

    def relogin(self, username, password):
        self.relogin_calls += 1
        assert username == "alice"
        assert password == "secret"
        return {"username": username}


def test_execute_trade_relogin_retries_once_on_401(monkeypatch, capsys):
    module = load_main(monkeypatch)
    client = RetryClient()
    client.err_cls = module.FSHTTPError
    market = sample_market(state_vector=[1.0] * 28)
    recipe, pos, expected, desc = module.strategy_for_market(market)

    traded = module._execute_trade(
        client, market, recipe, expected, desc,
        dry_run=False, username="alice", password="secret",
    )

    out = capsys.readouterr().out
    assert traded is True
    assert client.buy_calls == 2
    assert client.relogin_calls == 1
    assert "401" in out
    assert "retry succeeded" in out
    assert "market_id=30 position_id=4" in out


def test_execute_trade_does_not_relogin_in_dry_run(monkeypatch, capsys):
    module = load_main(monkeypatch)
    client = RetryClient()
    client.err_cls = module.FSHTTPError
    market = sample_market(state_vector=[1.0] * 28)
    recipe, pos, expected, desc = module.strategy_for_market(market)

    traded = module._execute_trade(
        client, market, recipe, expected, desc,
        dry_run=True, username="alice", password="secret",
    )

    assert traded is False
    assert client.buy_calls == 0
    assert client.relogin_calls == 0
    assert "WOULD BUY" in capsys.readouterr().out
