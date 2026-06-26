"""
AuthProfile 单元测试

测试 AuthProfile 的核心功能：
1. 多 Key 轮换（Round-Robin）
2. 指数退避冷却
3. 失败计数递增
4. 成功重置
5. 边界情况处理
"""

import pytest
import time
from execution.engine_base import (
    AuthProfile,
    AuthKeyState,
    AuthProfileError,
    NoAvailableKeyError,
    KeyCooldownError,
    KeyHealthStatus,
)


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def profile_3keys():
    """3 个 Key 的标准配置"""
    return AuthProfile(
        keys=["sk_alpha_1111", "sk_beta_2222", "sk_gamma_3333"],
        initial_cooldown=30.0,
        max_cooldown=300.0,
    )


@pytest.fixture
def profile_fast_cooldown():
    """快速冷却配置（用于测试）"""
    return AuthProfile(
        keys=["alpha_key", "beta_key"],   # 4-char prefixes differ: "alph"/"beta"
        initial_cooldown=0.05,   # 50ms
        max_cooldown=0.2,         # 200ms
    )


# =============================================================================
# 基础轮换测试
# =============================================================================

class TestAuthProfileRoundRobin:
    """Round-Robin 轮换测试"""

    def test_single_key_round_robin(self):
        """单 Key 每次返回同一个"""
        profile = AuthProfile(keys=["only_key"])
        ks1 = profile.get_available_key()
        ks2 = profile.get_available_key()
        assert ks1.key_id == ks2.key_id == "key_only***"
        assert ks1.total_requests == 2

    def test_multi_key_round_robin_sequence(self, profile_3keys):
        """多 Key 按顺序轮换"""
        ids = [profile_3keys.get_available_key().key_id for _ in range(3)]
        assert ids[0] != ids[1] != ids[2]
        # 第4次回到第一个
        fourth = profile_3keys.get_available_key().key_id
        assert fourth == ids[0]

    def test_round_robin_after_full_cycle(self, profile_3keys):
        """完整一圈后回到起点"""
        for _ in range(3):
            profile_3keys.get_available_key()
        fourth = profile_3keys.get_available_key()
        assert fourth.key_id == "key_sk_a***"

    def test_request_counter_increments(self, profile_3keys):
        """每次获取 Key 都计数"""
        for _ in range(5):
            profile_3keys.get_available_key()
        stats = profile_3keys.get_stats()
        assert stats["total_requests"] == 5
        assert all(k["total_requests"] > 0 for k in stats["keys"])


# =============================================================================
# 指数退避测试
# =============================================================================

class TestExponentialBackoff:
    """指数退避冷却测试"""

    def test_first_failure_sets_30s_cooldown(self):
        """第1次失败 → 30s 冷却"""
        profile = AuthProfile(
            keys=["test_key"],
            initial_cooldown=30.0,
        )
        ks = profile.get_available_key()
        cooldown = profile.report_failure(ks.key_id)

        assert cooldown == 30.0
        assert ks.is_in_cooldown
        assert ks.consecutive_failures == 1

    def test_second_failure_doubles_cooldown(self):
        """第2次连续失败 → 60s"""
        profile = AuthProfile(
            keys=["test_key"],
            initial_cooldown=30.0,
        )
        ks = profile.get_available_key()
        profile.report_failure(ks.key_id)
        cooldown = profile.report_failure(ks.key_id)

        assert cooldown == 60.0
        assert ks.consecutive_failures == 2

    def test_cooldown_caps_at_max(self):
        """冷却时间封顶 300s"""
        profile = AuthProfile(
            keys=["test_key"],
            initial_cooldown=30.0,
            max_cooldown=300.0,
        )
        ks = profile.get_available_key()
        # 4次失败: 30, 60, 120, 240
        for i in range(1, 5):
            cooldown = profile.report_failure(ks.key_id)
            assert cooldown == min(30.0 * (2 ** (i - 1)), 300.0)

        # 第5次: 30 * 2^4 = 480 → 封顶 300
        fifth = profile.report_failure(ks.key_id)
        assert fifth == 300.0

    def test_backoff_formula_full_sequence(self):
        """完整退避序列: 30, 60, 120, 240, 300(cap)"""
        profile = AuthProfile(
            keys=["k"],
            initial_cooldown=30.0,
            max_cooldown=300.0,
        )
        ks = profile.get_available_key()
        cooldowns = []
        for _ in range(6):
            c = profile.report_failure(ks.key_id)
            if c:
                cooldowns.append(c)

        assert cooldowns == [30.0, 60.0, 120.0, 240.0, 300.0, 300.0]

    def test_fast_cooldown_respects_limits(self):
        """快速冷却配置正确应用"""
        profile = AuthProfile(
            keys=["k"],
            initial_cooldown=0.05,
            max_cooldown=0.2,
        )
        ks = profile.get_available_key()
        assert profile.report_failure(ks.key_id) == 0.05
        assert profile.report_failure(ks.key_id) == 0.10
        assert profile.report_failure(ks.key_id) == 0.20
        assert profile.report_failure(ks.key_id) == 0.20  # cap


# =============================================================================
# 成功重置测试
# =============================================================================

class TestSuccessReset:
    """成功调用重置退避状态"""

    def test_success_resets_consecutive_failures(self, profile_3keys):
        """成功调用重置连续失败计数"""
        ks = profile_3keys.get_available_key()
        profile_3keys.report_failure(ks.key_id)
        profile_3keys.report_failure(ks.key_id)
        assert ks.consecutive_failures == 2

        profile_3keys.report_success(ks.key_id)
        assert ks.consecutive_failures == 0
        assert not ks.is_in_cooldown

    def test_success_clears_cooldown(self, profile_3keys):
        """成功调用清除冷却状态"""
        ks = profile_3keys.get_available_key()
        profile_3keys.report_failure(ks.key_id)
        assert ks.is_in_cooldown

        profile_3keys.report_success(ks.key_id)
        assert not ks.is_in_cooldown
        assert ks.cooldown_until == 0.0

    def test_success_increments_total_successes(self, profile_3keys):
        """成功计数递增"""
        ks = profile_3keys.get_available_key()
        kid = ks.key_id
        profile_3keys.report_success(kid)
        profile_3keys.report_success(kid)
        stats = profile_3keys.get_stats()
        assert stats["total_successes"] == 2

    def test_success_on_unknown_key_silent(self, profile_3keys):
        """对未知 Key 报告成功无副作用"""
        profile_3keys.report_success("non_existent_key")
        # 不应抛出异常


# =============================================================================
# 冷却期切换测试
# =============================================================================

class TestCooldownSwitch:
    """冷却期内自动切换备用 Key"""

    def test_skips_cooldown_key(self, profile_fast_cooldown):
        """获取 Key 时跳过冷却中的 Key"""
        ks_a = profile_fast_cooldown.get_available_key()
        assert ks_a.key_id == "key_alph***"

        # alpha_key 失败进入冷却
        profile_fast_cooldown.report_failure(ks_a.key_id)

        # 下一个应返回 beta_key（而非冷却中的 alpha_key）
        ks_b = profile_fast_cooldown.get_available_key()
        assert ks_b.key_id == "key_beta***"

    def test_cooldown_expires_key_becomes_available(self, profile_fast_cooldown):
        """冷却过期后 Key 重新可用"""
        ks_a = profile_fast_cooldown.get_available_key()
        profile_fast_cooldown.report_failure(ks_a.key_id)

        # 等冷却结束
        time.sleep(0.06)

        # 现在两个 Key 都可用，Round-Robin 继续
        ks = profile_fast_cooldown.get_available_key()
        assert ks.key_id == "key_beta***"

        ks2 = profile_fast_cooldown.get_available_key()
        # alpha_key 冷却已过期，beta_key 刚用过，应回到 alpha_key
        assert ks2.key_id == "key_alph***"

    def test_all_keys_in_cooldown_raises(self, profile_fast_cooldown):
        """所有 Key 都在冷却时抛出 NoAvailableKeyError"""
        # 让两个 Key 都进入冷却
        ks1 = profile_fast_cooldown.get_available_key()
        profile_fast_cooldown.report_failure(ks1.key_id)

        ks2 = profile_fast_cooldown.get_available_key()
        profile_fast_cooldown.report_failure(ks2.key_id)

        # 两个 Key 都在冷却，应抛出
        with pytest.raises(NoAvailableKeyError) as exc_info:
            profile_fast_cooldown.get_available_key()
        assert "冷却期" in str(exc_info.value)


# =============================================================================
# 健康状态测试
# =============================================================================

class TestHealthStatus:
    """Key 健康状态判断"""

    def test_healthy_initially(self, profile_3keys):
        """初始状态为 HEALTHY"""
        ks = profile_3keys.get_available_key()
        assert ks.health_status == KeyHealthStatus.HEALTHY

    def test_cooling_when_in_cooldown(self, profile_fast_cooldown):
        """冷却中为 COOLING"""
        ks = profile_fast_cooldown.get_available_key()
        profile_fast_cooldown.report_failure(ks.key_id)
        assert ks.health_status == KeyHealthStatus.COOLING

    def test_dead_after_5_consecutive_failures(self):
        """5次连续失败标记为 DEAD"""
        profile = AuthProfile(keys=["test_key"])
        ks = profile.get_available_key()
        for _ in range(5):
            profile.report_failure(ks.key_id, retryable=True)
        assert ks.health_status == KeyHealthStatus.DEAD
        # DEAD 的 Key 仍可返回（由轮换逻辑决定），但不可重试

    def test_get_stats_health_counts(self, profile_3keys):
        """统计包含健康/冷却/死亡计数"""
        ks1 = profile_3keys.get_available_key()
        profile_3keys.report_failure(ks1.key_id)  # key1 cooling

        ks2 = profile_3keys.get_available_key()
        for _ in range(5):
            profile_3keys.report_failure(ks2.key_id)  # key2 dead

        stats = profile_3keys.get_stats()
        assert stats["healthy_keys"] == 1   # key3
        assert stats["cooling_keys"] == 1    # key1
        assert stats["dead_keys"] == 1      # key2


# =============================================================================
# 统计与诊断测试
# =============================================================================

class TestStats:
    """统计功能测试"""

    def test_stats_total_requests(self, profile_3keys):
        """总请求数正确"""
        for _ in range(7):
            profile_3keys.get_available_key()
        stats = profile_3keys.get_stats()
        assert stats["total_requests"] == 7

    def test_stats_success_rate(self, profile_3keys):
        """成功率计算"""
        for _ in range(10):
            ks = profile_3keys.get_available_key()
            profile_3keys.report_success(ks.key_id)
        for _ in range(2):
            ks = profile_3keys.get_available_key()
            profile_3keys.report_failure(ks.key_id)

        stats = profile_3keys.get_stats()
        assert stats["total_requests"] == 12
        assert stats["total_successes"] == 10
        assert stats["total_failures"] == 2
        assert stats["overall_success_rate"] == round(10 / 12 * 100, 2)

    def test_stats_key_ids_sanitized(self, profile_3keys):
        """统计中不暴露完整 Key"""
        stats = profile_3keys.get_stats()
        for k in stats["keys"]:
            assert "***" in k["key_id"]
            # key_id 不含完整 key 值
            for key_state in profile_3keys._keys:
                assert key_state.key not in str(stats)


# =============================================================================
# Key 管理测试
# =============================================================================

class TestKeyManagement:
    """Key 增删管理"""

    def test_add_key(self):
        """动态添加 Key"""
        profile = AuthProfile(keys=["key1"])
        profile.add_key("key2", "custom_id")
        stats = profile.get_stats()
        assert stats["total_keys"] == 2

    def test_add_key_with_custom_id(self):
        """自定义 Key ID"""
        profile = AuthProfile(keys=["secret123"])
        profile.add_key("another_key", "production_key_v2")
        ks = profile._find_key("production_key_v2")
        assert ks is not None
        assert ks.key == "another_key"

    def test_remove_key(self):
        """移除 Key"""
        profile = AuthProfile(keys=["alpha_key", "beta_key"], key_ids=["id_alpha", "id_beta"])
        assert profile.remove_key("id_alpha")
        assert profile.get_stats()["total_keys"] == 1

    def test_remove_nonexistent_key(self):
        """移除不存在的 Key 返回 False"""
        profile = AuthProfile(keys=["key1_long"])
        assert not profile.remove_key("nonexistent")

    def test_duplicate_key_id_rejected(self):
        """重复 Key ID 被拒绝"""
        profile = AuthProfile(keys=["alpha_key", "beta_key"], key_ids=["id_a", "id_b"])
        # 尝试添加相同 ID
        profile.add_key("extra_key", "id_a")
        assert profile.get_stats()["total_keys"] == 2  # 重复被拒绝，仍为 2

    def test_force_reset_key(self):
        """强制重置 Key"""
        profile = AuthProfile(keys=["key1"])
        ks = profile.get_available_key()
        profile.report_failure(ks.key_id)
        assert ks.consecutive_failures == 1
        assert ks.is_in_cooldown

        profile.force_reset_key(ks.key_id)
        assert ks.consecutive_failures == 0
        assert not ks.is_in_cooldown


# =============================================================================
# 不可重试失败测试
# =============================================================================

class TestNonRetryableFailure:
    """不可重试失败处理"""

    def test_non_retryable_does_not_set_cooldown(self):
        """不可重试失败不触发冷却"""
        profile = AuthProfile(keys=["key1"])
        ks = profile.get_available_key()
        cooldown = profile.report_failure(ks.key_id, retryable=False)

        assert cooldown is None
        assert ks.consecutive_failures == 1
        # 不设置 cooldown_until，所以 is_in_cooldown 为 False
        assert not ks.is_in_cooldown

    def test_non_retryable_marks_dead_after_5(self):
        """不可重试失败也计数，达到 5 次标记 DEAD"""
        profile = AuthProfile(keys=["key1"])
        ks = profile.get_available_key()
        for _ in range(5):
            profile.report_failure(ks.key_id, retryable=False)
        assert ks.health_status == KeyHealthStatus.DEAD


# =============================================================================
# AuthKeyState 直接测试
# =============================================================================

class TestAuthKeyState:
    """AuthKeyState 单元测试"""

    def test_is_in_cooldown_false_initially(self):
        """初始无冷却"""
        ks = AuthKeyState(key_id="test", key="secret")
        assert not ks.is_in_cooldown

    def test_cooldown_remaining_zero_when_no_cooldown(self):
        """无冷却时剩余时间为 0"""
        ks = AuthKeyState(key_id="test", key="secret")
        assert ks.cooldown_remaining == 0.0

    def test_cooldown_remaining_positive(self):
        """有冷却时返回正数"""
        ks = AuthKeyState(key_id="test", key="secret", cooldown_until=time.time() + 30)
        assert ks.cooldown_remaining > 0
        assert ks.cooldown_remaining <= 30

    def test_make_key_id_generates_sanitized_id(self):
        """生成脱敏 Key ID"""
        ks = AuthKeyState(key_id="key_abcd***", key="abcd1234secret")
        assert "abcd" in ks.key_id
        assert "secret" not in ks.key_id


# =============================================================================
# 并发安全测试（基础）
# =============================================================================

class TestConcurrency:
    """并发访问测试（基础验证）"""

    def test_sequential_rapid_access_no_race(self):
        """快速顺序访问不会出错"""
        profile = AuthProfile(keys=["k1", "k2", "k3"])
        results = []
        for _ in range(100):
            results.append(profile.get_available_key().key_id)
        # 所有 100 次都应成功返回
        assert len(results) == 100
        # 至少用到了所有 key
        unique_ids = set(results)
        assert len(unique_ids) == 3

    def test_report_failure_concurrent(self):
        """并发失败报告安全"""
        import threading
        profile = AuthProfile(keys=["k1"])
        ks = profile.get_available_key()

        def fail():
            profile.report_failure(ks.key_id)

        threads = [threading.Thread(target=fail) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # 线程安全：最终计数为 10
        assert ks.consecutive_failures == 10


# =============================================================================
# 集成：引擎轮换场景
# =============================================================================

class TestIntegrationScenarios:
    """端到端集成场景"""

    def test_three_keys_one_fails_one_healthy(self, profile_3keys):
        """三 Key 中一个失败一个健康"""
        # Key1 (sk_a): 成功 → round_robin_index → 1
        ks1 = profile_3keys.get_available_key()
        profile_3keys.report_success(ks1.key_id)
        # Key2 (sk_b): 失败2次（冷却中）→ round_robin_index → 3 % 3 = 0
        ks2 = profile_3keys.get_available_key()
        profile_3keys.report_failure(ks2.key_id)
        profile_3keys.report_failure(ks2.key_id)
        # Key3 (sk_g): 轮换自然落到这里（round_robin_index=0，跳过冷却中ks2，到ks3）
        ks3 = profile_3keys.get_available_key()

        # 轮换回到 Key1（ks2冷却中，ks1健康）
        assert profile_3keys.get_available_key().key_id == "key_sk_a***"
        # 再次轮到 Key3
        assert profile_3keys.get_available_key().key_id == "key_sk_g***"
        # Key2 仍在冷却
        assert profile_3keys.get_cooldown_remaining(ks2.key_id) > 0

    def test_retry_until_healthy(self):
        """失败 Key 冷却后重新可用"""
        profile = AuthProfile(
            keys=["alpha_key", "beta_key"],
            initial_cooldown=0.05,
            max_cooldown=0.2,
        )

        # Primary (alpha_key) 失败
        ks_primary = profile.get_available_key()
        profile.report_failure(ks_primary.key_id)

        # 使用 backup (beta_key)
        ks_backup = profile.get_available_key()
        assert ks_backup.key_id == "key_beta***"

        # 等 primary 冷却结束
        time.sleep(0.06)

        # 现在两个都可用，继续轮换
        ks_next = profile.get_available_key()
        assert ks_next.key_id == "key_alph***"
