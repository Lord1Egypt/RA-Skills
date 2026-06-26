"""Lightweight local store for extracted entities and relations."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from datapulse.core.entities import Entity, EntityType, Relation, normalize_entity_name


class EntityStore:
    """JSON-backed entity storage with in-memory index."""

    def __init__(self, path: str | None = None):
        self.path = Path(path or os.getenv("DATAPULSE_ENTITY_STORE", "entity_store.json") or "entity_store.json")
        self.entities: dict[str, Entity] = {}
        self.relations: list[Relation] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            self.entities = {}
            self.relations = []
            return

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.entities = {}
            self.relations = []
            return

        self.entities = {}
        entities = raw.get("entities", {})
        if isinstance(entities, dict):
            for key, payload in entities.items():
                if not isinstance(payload, dict):
                    continue
                entity = Entity.from_dict(payload)
                self.entities[key] = entity

        relations_payload = raw.get("relations", [])
        self.relations = []
        if isinstance(relations_payload, list):
            for raw_relation in relations_payload:
                if not isinstance(raw_relation, dict):
                    continue
                relation = Relation(
                    source_entity=normalize_entity_name(str(raw_relation.get("source_entity", ""))),
                    target_entity=normalize_entity_name(str(raw_relation.get("target_entity", ""))),
                    relation_type=str(raw_relation.get("relation_type", "RELATED_TO")),
                    keywords=[str(item) for item in raw_relation.get("keywords", []) if str(item)],
                    weight=float(raw_relation.get("weight", 1.0) or 1.0),
                    source_item_ids=[str(item) for item in raw_relation.get("source_item_ids", []) if str(item)],
                )
                self.relations.append(relation)

    def _save(self) -> None:
        payload: dict[str, Any] = {
            "entities": {key: value.to_dict() for key, value in self.entities.items()},
            "relations": [relation.to_dict() for relation in self.relations],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def add_entity(self, entity: Entity) -> bool:
        """Add or merge entity. Returns True when added or merged."""
        if not isinstance(entity, Entity):
            return False
        existing = self.entities.get(entity.id)
        if existing is None:
            self.entities[entity.id] = entity
            self._save()
            return True

        merged_source_ids = sorted(set(existing.source_item_ids + entity.source_item_ids))
        merged = Entity(
            name=existing.name,
            entity_type=existing.entity_type,
            display_name=existing.display_name or entity.display_name,
            source_item_ids=merged_source_ids,
            mention_count=existing.mention_count + max(1, entity.mention_count),
            extra={**existing.extra, **entity.extra},
        )
        if merged == existing:
            return False
        self.entities[entity.id] = merged
        self._save()
        return True

    def add_entities(self, entities: list[Entity]) -> int:
        if not entities:
            return 0
        added = 0
        for entity in entities:
            if self.add_entity(entity):
                added += 1
        return added

    def add_relation(self, relation: Relation) -> bool:
        if not isinstance(relation, Relation):
            return False
        norm_source = relation.source_entity
        norm_target = relation.target_entity
        for idx, existing in enumerate(self.relations):
            if (
                existing.source_entity == norm_source
                and existing.target_entity == norm_target
                and existing.relation_type == relation.relation_type
            ):
                merged = Relation(
                    source_entity=existing.source_entity,
                    target_entity=existing.target_entity,
                    relation_type=existing.relation_type,
                    keywords=sorted(set(existing.keywords + relation.keywords)),
                    weight=max(existing.weight, relation.weight),
                    source_item_ids=sorted(set(existing.source_item_ids + relation.source_item_ids)),
                )
                if merged != existing:
                    self.relations[idx] = merged
                    self._save()
                return merged != existing
        self.relations.append(relation)
        self._save()
        return True

    def add_relations(self, relations: list[Relation]) -> int:
        if not relations:
            return 0
        added = 0
        for relation in relations:
            if self.add_relation(relation):
                added += 1
        return added

    def get_entity(self, name: str) -> Entity | None:
        normalized = normalize_entity_name(name) if name else ""
        for entity in self.entities.values():
            if entity.name == normalized:
                return entity
        return None

    def query_by_type(self, entity_type: str | EntityType) -> list[Entity]:
        if isinstance(entity_type, str):
            et = entity_type.strip().upper()
        else:
            et = entity_type.value
        return [e for e in self.entities.values() if e.entity_type.value == et]

    def query_related(self, entity_name: str) -> list[dict[str, Any]]:
        if not entity_name:
            return []
        normalized = normalize_entity_name(entity_name)
        related: list[dict[str, Any]] = []
        for relation in self.relations:
            if relation.source_entity == normalized or relation.target_entity == normalized:
                related.append({
                    "source_entity": relation.source_entity,
                    "target_entity": relation.target_entity,
                    "relation_type": relation.relation_type,
                    "keywords": relation.keywords,
                    "weight": relation.weight,
                    "source_item_ids": relation.source_item_ids,
                })
        return related

    def query_by_source_item(self, item_id: str) -> list[Entity]:
        if not item_id:
            return []
        normalized_item = str(item_id).strip()
        return [
            entity
            for entity in self.entities.values()
            if normalized_item in entity.source_item_ids
        ]

    def cross_source_entities(self, min_sources: int = 2) -> list[Entity]:
        threshold = max(1, min_sources)
        return [e for e in self.entities.values() if len(e.source_item_ids) >= threshold]

    def entity_source_count(self, name: str) -> int:
        entity = self.get_entity(name)
        return len(entity.source_item_ids) if entity else 0

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        for entity in self.entities.values():
            key = entity.entity_type.value
            by_type[key] = by_type.get(key, 0) + 1

        cross_source = sum(1 for entity in self.entities.values() if len(entity.source_item_ids) >= 2)
        return {
            "total_entities": len(self.entities),
            "total_relations": len(self.relations),
            "cross_source_entities": cross_source,
            "by_type": by_type,
        }
