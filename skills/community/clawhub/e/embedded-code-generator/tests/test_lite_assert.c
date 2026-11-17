/**
 * @file test_lite_assert.c
 * @brief Self-check tests for lite_assert.c (LOG-mode fault records).
 *
 * Run via `make test` from the skill package root. Exit code: number
 * of failed checks (0 = all pass).
 *
 * NOTE: this suite must run against LA_MODE=0 (LA_MODE_LOG, the
 * default). Halt/Reset modes stop execution, so only their hook
 * plumbing is testable via the reset-hook API here.
 */

#include <stdio.h>
#include <string.h>
#include "lite_assert.h"

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

/* --- reset hook spy ------------------------------------------------ */

static uint32_t g_hook_calls;
static void fake_reset(void)
{
    g_hook_calls++;
}

static void reset_all(void)
{
    LA_Clear();
    LA_SetResetHook(NULL);
    g_hook_calls = 0u;
}

static void test_pass_no_record(void)
{
    LA_Record_t rec;

    reset_all();
    LA_Assert(1 == 1);
    LA_Assert(2 > 1);
    CHECK("Pass: no record on true conditions", LA_GetCount() == 0u);
    CHECK("Pass: GetLast false with no records", !LA_GetLast(&rec));
}

static void test_fail_record(void)
{
    LA_Record_t rec;

    reset_all();
    LA_Assert(1 == 2);                     /* line known via __LINE__  */
    CHECK("Fail: count == 1", LA_GetCount() == 1u);
    CHECK("Fail: GetLast returns record", LA_GetLast(&rec));
    CHECK("Fail: line number recorded", rec.line != 0u);
    CHECK("Fail: expr string recorded", (rec.expr != NULL) && (strcmp(rec.expr, "1 == 2") == 0));
    CHECK("Fail: file label recorded", (rec.file != NULL) && (strstr(rec.file, "test_lite_assert") != NULL));
    CHECK("Fail: execution continues (LOG mode)", g_hook_calls == 0u);
}

static void test_explicit_fail(void)
{
    LA_Record_t rec;

    reset_all();
    LA_Fail("drv.c", 77u, "baud_rate_supported");
    CHECK("Explicit: count == 1", LA_GetCount() == 1u);
    CHECK("Explicit: GetLast copies fields", LA_GetLast(&rec) &&
          (strcmp(rec.file, "drv.c") == 0) && (rec.line == 77u) &&
          (strcmp(rec.expr, "baud_rate_supported") == 0));
}

static void test_pool_wraparound(void)
{
    uint32_t i;
    LA_Record_t rec;

    reset_all();
    for (i = 1u; i <= (uint32_t)(LA_MAX_RECORDS + 3u); i++) {
        LA_Fail("m.c", i, "overflow_test");
    }
    CHECK("Pool: total counter counts every failure",
          LA_GetCount() == (uint32_t)(LA_MAX_RECORDS + 3u));
    CHECK("Pool: GetLast sees the newest record", LA_GetLast(&rec) &&
          (rec.line == (uint32_t)(LA_MAX_RECORDS + 3u)));
}

static void test_clear_and_reset_hook(void)
{
    LA_Record_t rec;

    reset_all();
    LA_Assert(0);
    CHECK("Clear: count is 1 before clear", LA_GetCount() == 1u);
    LA_Clear();
    CHECK("Clear: count zeroed", LA_GetCount() == 0u);
    CHECK("Clear: GetLast false after clear", !LA_GetLast(&rec));

    /* Reset hook plumbing. LA_MODE_RESET is a compile-time branch:
     * with the default LOG build the hook must NOT fire (execution
     * continues); a LA_MODE_RESET build (-DLA_MODE=2) must invoke it. */
    reset_all();
    LA_SetResetHook(fake_reset);
    LA_Fail("x.c", 1u, "reset_path");
#if (LA_MODE == LA_MODE_RESET)
    CHECK("Hook: reset hook invoked on LA_Fail", g_hook_calls == 1u);
#else
    CHECK("Hook: LOG mode does not call reset hook", g_hook_calls == 0u);
#endif
    CHECK("Hook: record still written before hook", LA_GetCount() == 1u);
}

static void test_getlast_null(void)
{
    reset_all();
    CHECK("Null: GetLast rejects NULL out", !LA_GetLast(NULL));
    LA_Assert(0);
    CHECK("Null: GetLast NULL still rejected after records", !LA_GetLast(NULL));
}

int main(void)
{
    test_pass_no_record();
    test_fail_record();
    test_explicit_fail();
    test_pool_wraparound();
    test_clear_and_reset_hook();
    test_getlast_null();

    printf("Summary: %d checks, %d passed, %d failed\n",
           g_total, g_total - g_failed, g_failed);
    if (g_failed > 0) {
        printf("=== TESTS FAILED ===\n");
        return g_failed;
    }
    printf("=== ALL TESTS PASSED ===\n");
    return 0;
}
