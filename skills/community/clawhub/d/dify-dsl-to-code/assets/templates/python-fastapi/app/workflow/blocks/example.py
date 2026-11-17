"""EXAMPLE block handler — replace with real blocks generated per DSL."""
from __future__ import annotations


def template_transform(node_id, config, pool, engine):
    pool.set(node_id, "output", pool.resolve(config.get("template", "")))


HANDLERS = {
    "tpl-1": template_transform,
}
