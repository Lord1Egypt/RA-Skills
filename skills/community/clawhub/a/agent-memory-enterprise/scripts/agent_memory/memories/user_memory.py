"""User Memory - long-term user preferences with Redis cache layer."""

from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy import select, update, func

from agent_memory.config import UserMemoryConfig
from agent_memory.core.base_memory import BaseMemory
from agent_memory.exceptions import MemoryNotFoundError
from agent_memory.models.user import UserPreference, UserProfile
from agent_memory.storage.postgres_client import PostgresClient
from agent_memory.storage.postgres_models import (
    UserPreferenceHistoryModel,
    UserProfileModel,
)
from agent_memory.storage.redis_client import RedisClient


class UserMemory(BaseMemory):
    """User profiles in PostgreSQL with Redis cache layer."""

    def __init__(
        self,
        pg_client: PostgresClient,
        redis_client: RedisClient,
        config: UserMemoryConfig,
    ):
        self._pg = pg_client
        self._redis = redis_client
        self._config = config

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def store(self, data: UserProfile, **kwargs) -> str:
        async with self._pg.session_factory() as session:
            prefs = {k: v.model_dump() for k, v in data.preferences.items()}
            model = UserProfileModel(
                user_id=data.user_id,
                preferences=prefs,
                history_task_ids=data.history_task_ids,
                usage_patterns=data.usage_patterns,
            )
            session.add(model)
            await session.commit()
        await self._cache_profile(data)
        return data.user_id

    async def retrieve(self, memory_id: str, **kwargs) -> Optional[UserProfile]:
        return await self.get_profile(memory_id)

    async def search(self, query: Any, **kwargs) -> list[UserProfile]:
        async with self._pg.session_factory() as session:
            stmt = select(UserProfileModel)
            if isinstance(query, dict):
                if user_id := query.get("user_id"):
                    stmt = stmt.where(UserProfileModel.user_id == user_id)
            result = await session.execute(stmt)
            models = result.scalars().all()
            return [self._model_to_profile(m) for m in models]

    async def delete(self, memory_id: str) -> bool:
        async with self._pg.session_factory() as session:
            stmt = select(UserProfileModel).where(
                UserProfileModel.user_id == memory_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model:
                await session.delete(model)
                await session.commit()
                await self._invalidate_cache(memory_id)
                return True
            return False

    async def count(self, **kwargs) -> int:
        async with self._pg.session_factory() as session:
            result = await session.execute(
                select(func.count(UserProfileModel.id))
            )
            return result.scalar_one()

    # --- Extended interface ---

    async def get_profile(self, user_id: str) -> UserProfile:
        """Get user profile (with Redis cache)."""
        # Check cache first
        cached = await self._get_cached_profile(user_id)
        if cached:
            return cached

        # Load from DB
        async with self._pg.session_factory() as session:
            stmt = select(UserProfileModel).where(
                UserProfileModel.user_id == user_id
            )
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                # Create a new empty profile
                profile = UserProfile(user_id=user_id)
                await self.store(profile)
                return profile
            profile = self._model_to_profile(model)
            await self._cache_profile(profile)
            return profile

    async def update_preference(
        self,
        user_id: str,
        key: str,
        value: Any,
        source: str = "explicit",
    ) -> UserPreference:
        """Update or create a user preference with version control."""
        profile = await self.get_profile(user_id)

        version = 1
        previous_value = None
        if key in profile.preferences:
            old_pref = profile.preferences[key]
            version = old_pref.version + 1
            previous_value = old_pref.value

        confidence = 1.0 if source == "explicit" else 0.6
        new_pref = UserPreference(
            key=key,
            value=value,
            source=source,
            confidence=confidence,
            version=version,
        )
        profile.preferences[key] = new_pref

        # Save to DB
        async with self._pg.session_factory() as session:
            prefs_data = {k: v.model_dump() for k, v in profile.preferences.items()}
            stmt = (
                update(UserProfileModel)
                .where(UserProfileModel.user_id == user_id)
                .values(preferences=prefs_data)
            )
            await session.execute(stmt)

            # Save version history
            history = UserPreferenceHistoryModel(
                user_id=user_id,
                preference_key=key,
                version=version,
                previous_value=previous_value,
                new_value=value,
                change_reason=source,
            )
            session.add(history)
            await session.commit()

        await self._invalidate_cache(user_id)
        return new_pref

    async def remove_preference(self, user_id: str, key: str) -> bool:
        """Remove a preference from user profile."""
        profile = await self.get_profile(user_id)
        if key not in profile.preferences:
            return False

        del profile.preferences[key]
        async with self._pg.session_factory() as session:
            prefs_data = {k: v.model_dump() for k, v in profile.preferences.items()}
            stmt = (
                update(UserProfileModel)
                .where(UserProfileModel.user_id == user_id)
                .values(preferences=prefs_data)
            )
            await session.execute(stmt)
            await session.commit()

        await self._invalidate_cache(user_id)
        return True

    async def add_task_history(self, user_id: str, task_id: str) -> None:
        """Add a task ID to user's task history."""
        profile = await self.get_profile(user_id)
        if task_id not in profile.history_task_ids:
            profile.history_task_ids.append(task_id)
            async with self._pg.session_factory() as session:
                stmt = (
                    update(UserProfileModel)
                    .where(UserProfileModel.user_id == user_id)
                    .values(history_task_ids=profile.history_task_ids)
                )
                await session.execute(stmt)
                await session.commit()
            await self._invalidate_cache(user_id)

    async def update_usage_pattern(
        self, user_id: str, pattern_key: str, pattern_value: Any
    ) -> None:
        """Update a usage pattern."""
        profile = await self.get_profile(user_id)
        profile.usage_patterns[pattern_key] = pattern_value
        async with self._pg.session_factory() as session:
            stmt = (
                update(UserProfileModel)
                .where(UserProfileModel.user_id == user_id)
                .values(usage_patterns=profile.usage_patterns)
            )
            await session.execute(stmt)
            await session.commit()
        await self._invalidate_cache(user_id)

    async def get_preference_history(
        self, user_id: str, key: str
    ) -> list[dict]:
        """Get version history for a preference."""
        async with self._pg.session_factory() as session:
            stmt = (
                select(UserPreferenceHistoryModel)
                .where(
                    UserPreferenceHistoryModel.user_id == user_id,
                    UserPreferenceHistoryModel.preference_key == key,
                )
                .order_by(UserPreferenceHistoryModel.version)
            )
            result = await session.execute(stmt)
            return [
                {
                    "version": h.version,
                    "previous_value": h.previous_value,
                    "new_value": h.new_value,
                    "change_reason": h.change_reason,
                    "changed_at": h.changed_at.isoformat() if h.changed_at else None,
                }
                for h in result.scalars().all()
            ]

    # --- Private helpers ---

    def _model_to_profile(self, model: UserProfileModel) -> UserProfile:
        prefs = {}
        for k, v in model.preferences.items():
            if isinstance(v, dict):
                prefs[k] = UserPreference(**v)
        return UserProfile(
            id=model.id,
            user_id=model.user_id,
            preferences=prefs,
            history_task_ids=model.history_task_ids or [],
            usage_patterns=model.usage_patterns or {},
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def _get_cached_profile(self, user_id: str) -> Optional[UserProfile]:
        r = self._redis.client
        raw = await r.get(f"user:{user_id}:profile")
        if raw:
            return UserProfile.model_validate_json(raw)
        return None

    async def _cache_profile(self, profile: UserProfile) -> None:
        r = self._redis.client
        await r.set(
            f"user:{profile.user_id}:profile",
            profile.model_dump_json(),
            ex=self._config.cache_ttl_seconds,
        )

    async def _invalidate_cache(self, user_id: str) -> None:
        r = self._redis.client
        await r.delete(f"user:{user_id}:profile")
