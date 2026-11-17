/**
 * @file test_soft_timer.c
 * @brief Self-check tests for soft_timer.c (polling timers).
 *
 * Run via `make test` from the skill package root. Exit code: number
 * of failed checks (0 = all pass).
 */

#include <stdio.h>
#include <inttypes.h>
#include "soft_timer.h"

static int g_failed = 0;
static int g_total  = 0;

#define CHECK(desc, expr)                                          \
    do {                                                           \
        g_total++;                                                 \
        if (expr) {                                                \
            printf("[PASS] %s\n", (desc));                         \
        } else {                                                   \
            g_failed++;                                            \
            printf("[FAIL] %s  (at line %d)\n", (desc), __LINE__); \
        }                                                          \
    } while (0)

/* --- callback spies ------------------------------------------------ */
static uint32_t g_calls_a;
static uint32_t g_calls_b;
static uint32_t g_last_id;
static void   *g_last_user;

static void cb_a(uint32_t id, void *user)
{
    g_calls_a++;
    g_last_id = id;
    g_last_user = user;
}
static void cb_b(uint32_t id, void *user)
{
    g_calls_b++;
    (void)id;
    (void)user;
}

/* Stop-own-id-from-callback pattern: must not corrupt the scan. */
static uint32_t g_self_id;
static void cb_stop_self(uint32_t id, void *user)
{
    (void)user;
    ST_Stop(id);
    g_calls_b++;
}

static void reset_all(void)
{
    ST_Init();
    g_calls_a = 0u;
    g_calls_b = 0u;
    g_last_id = ST_INVALID_ID;
    g_last_user = NULL;
}

static void test_add_and_once(void)
{
    reset_all();
    CHECK("Once: Add returns valid id",
          ST_Add(0u, 100u, ST_MODE_ONCE, cb_a, NULL) != ST_INVALID_ID);
    CHECK("Once: active after add", ST_IsActive(0u));
    CHECK("Once: remaining is full period", ST_GetRemaining(0u, 0u) == 100u);
    CHECK("Once: not fired before deadline", ST_Process(99u) == 0u);
    CHECK("Once: fires exactly at deadline", ST_Process(100u) == 1u);
    CHECK("Once: callback saw its own id", g_last_id == 0u);
    CHECK("Once: deactivated after firing", !ST_IsActive(0u));
    CHECK("Once: does not fire again", ST_Process(1000u) == 0u);
    CHECK("Once: still one call", g_calls_a == 1u);
}

static void test_periodic(void)
{
    uint32_t i;
    uint32_t fired;

    reset_all();
    (void)ST_Add(0u, 50u, ST_MODE_PERIODIC, cb_a, NULL);
    fired = 0u;
    for (i = 0u; i < 200u; i++) {
        fired += ST_Process(i);
    }
    /* Fires at t=50,100,150 (t=200 excluded by the loop bound). */
    CHECK("Periodic: fires every 50 ticks over 200 (3 times)", fired == 3u);
    CHECK("Periodic: callback count matches", g_calls_a == 3u);
    CHECK("Periodic: still active", ST_IsActive(0u));
}

static void test_stop_start(void)
{
    reset_all();
    (void)ST_Add(0u, 10u, ST_MODE_PERIODIC, cb_a, NULL);
    CHECK("Stop: stop reports active", ST_Stop(0u));
    CHECK("Stop: not active after stop", !ST_IsActive(0u));
    CHECK("Stop: no fire while stopped", ST_Process(10000u) == 0u);

    CHECK("Start: restart OK", ST_Start(0u, 20000u));
    CHECK("Start: not due right after restart", ST_Process(20000u + 5u) == 0u);
    CHECK("Start: due one period later", ST_Process(20000u + 10u) == 1u);
    CHECK("Start: invalid id rejected", !ST_Start(99u, 0u));
}

static void test_stop_own_callback(void)
{
    reset_all();
    g_self_id = ST_Add(0u, 20u, ST_MODE_PERIODIC, cb_stop_self, NULL);
    CHECK("SelfStop: timer registered", g_self_id != ST_INVALID_ID);
    CHECK("SelfStop: fires at 20 and stops itself", ST_Process(20u) == 1u);
    CHECK("SelfStop: deactivated by its own callback", !ST_IsActive(g_self_id));
    CHECK("SelfStop: never fires again", ST_Process(1000u) == 0u);
}

static void test_wraparound(void)
{
    uint32_t id;

    reset_all();
    id = ST_Add(0u, 100u, ST_MODE_ONCE, cb_a, NULL);
    /* Re-arm near the 32-bit rollover: 0xFFFFFF9C + 100 wraps to 0.
     * Ticks 0xFFFFFF9D..0xFFFFFFFF must NOT fire (99 remaining, then 1);
     * the timer is due exactly at t=0. */
    CHECK("Wrap: timer added", id != ST_INVALID_ID);
    {
        uint32_t now = 0xFFFFFF9Cu;
        uint32_t t;

        (void)ST_Start(id, now);                 /* due at 0 (wrapped) */
        for (t = now + 1u; t != 0u; t++) {       /* 99 ticks pre-wrap  */
            if (ST_Process(t) != 0u) {
                break;                           /* premature fire     */
            }
        }
        CHECK("Wrap: no premature fire across 0xFFFFFFFF->0", t == 0u);
        CHECK("Wrap: fires exactly one period after wrap", ST_Process(0u) == 1u);
    }
}

static void test_multiple_and_args(void)
{
    int cookie = 7;

    reset_all();
    CHECK("Multi: two timers registered",
          (ST_Add(0u, 10u, ST_MODE_PERIODIC, cb_a, &cookie) != ST_INVALID_ID) &&
          (ST_Add(0u, 20u, ST_MODE_PERIODIC, cb_b, NULL) != ST_INVALID_ID));
    CHECK("Multi: only timer A due at t=10", ST_Process(10u) == 1u);
    CHECK("Multi: user pointer passed through", (g_last_user == &cookie));
    CHECK("Multi: both due at t=20", ST_Process(20u) == 2u);
    CHECK("Multi: counts independent", (g_calls_a == 2u) && (g_calls_b == 1u));
}

static void test_params(void)
{
    reset_all();
    CHECK("Param: Add rejects zero period",
          ST_Add(0u, 0u, ST_MODE_ONCE, cb_a, NULL) == ST_INVALID_ID);
    CHECK("Param: Add rejects NULL callback",
          ST_Add(0u, 10u, ST_MODE_ONCE, NULL, NULL) == ST_INVALID_ID);
    CHECK("Param: Add rejects invalid mode",
          ST_Add(0u, 10u, (ST_Mode_t)9, cb_a, NULL) == ST_INVALID_ID);
    CHECK("Param: Stop rejects invalid id", !ST_Stop(99u));
    /* Pool of 8: nine Adds must yield 8 ids then ST_INVALID_ID. */
    CHECK("Param: pool exhaustion returns INVALID",
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) != ST_INVALID_ID &&
          ST_Add(0u, 1u, ST_MODE_ONCE, cb_b, NULL) == ST_INVALID_ID);
}

int main(void)
{
    test_add_and_once();
    test_periodic();
    test_stop_start();
    test_stop_own_callback();
    test_wraparound();
    test_multiple_and_args();
    test_params();

    printf("Summary: %d checks, %d passed, %d failed\n",
           g_total, g_total - g_failed, g_failed);
    if (g_failed > 0) {
        printf("=== TESTS FAILED ===\n");
        return g_failed;
    }
    printf("=== ALL TESTS PASSED ===\n");
    return 0;
}
