/**
 * @file test_key_scan.c
 * @brief Self-check tests for key_scan.c (debounced key scanner).
 *
 * Run via `make test` from the skill package root. Exit code: number
 * of failed checks (0 = all pass).
 *
 * The suite is compiled TWICE (like the ring buffer tests): once with
 * the default active-low polarity and once with -DKS_ACTIVE_LEVEL=1u
 * (active-high). Press/release raw levels below go through the
 * RAW_PRESSED / RAW_RELEASED macros so both builds exercise the full
 * state machine under their own polarity.
 */

#include <stdio.h>
#include <stdbool.h>
#include "key_scan.h"

#if KS_ACTIVE_LEVEL == 1u
#define RAW_PRESSED   1u
#define RAW_RELEASED  0u
#define POLARITY_TAG  "active-high"
#else
#define RAW_PRESSED   0u
#define RAW_RELEASED  1u
#define POLARITY_TAG  "active-low"
#endif

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

/* --- press + release, full debounce cycle --------------------------- */
static void test_down_and_up(void)
{
    KS_Init();
    CHECK("Cycle: idle key sees no event",
          KS_Update(0u, RAW_RELEASED, 0u) == KS_EVT_NONE);
    CHECK("Cycle: press starts debounce (no event yet)",
          KS_Update(0u, RAW_PRESSED, 100u) == KS_EVT_NONE);
    CHECK("Cycle: no DOWN at 19 ticks", KS_Update(0u, RAW_PRESSED, 119u) == KS_EVT_NONE);
    CHECK("Cycle: DOWN exactly at 20 ticks", KS_Update(0u, RAW_PRESSED, 120u) == KS_EVT_DOWN);
    CHECK("Cycle: DOWN is an edge (no repeat next tick)",
          KS_Update(0u, RAW_PRESSED, 121u) == KS_EVT_NONE);
    CHECK("Cycle: IsPressed true while held", KS_IsPressed(0u));
    CHECK("Cycle: release starts debounce (no event yet)",
          KS_Update(0u, RAW_RELEASED, 200u) == KS_EVT_NONE);
    CHECK("Cycle: no UP at 19 ticks", KS_Update(0u, RAW_RELEASED, 219u) == KS_EVT_NONE);
    CHECK("Cycle: UP exactly at 20 ticks", KS_Update(0u, RAW_RELEASED, 220u) == KS_EVT_UP);
    CHECK("Cycle: IsPressed false after UP", !KS_IsPressed(0u));
}

/* --- bounce rejection on both edges --------------------------------- */
static void test_bounce(void)
{
    KS_Init();
    /* Press bounce: active 5 ticks, then glitch back before debounce. */
    CHECK("Bounce: press pending", KS_Update(0u, RAW_PRESSED, 100u) == KS_EVT_NONE);
    CHECK("Bounce: glitch cancels pending press",
          KS_Update(0u, RAW_RELEASED, 105u) == KS_EVT_NONE);
    CHECK("Bounce: re-press restarts debounce",
          KS_Update(0u, RAW_PRESSED, 106u) == KS_EVT_NONE);
    CHECK("Bounce: no DOWN at 19 ticks of the restarted debounce",
          KS_Update(0u, RAW_PRESSED, 125u) == KS_EVT_NONE);
    CHECK("Bounce: DOWN after full 20 stable ticks",
          KS_Update(0u, RAW_PRESSED, 126u) == KS_EVT_DOWN);
    CHECK("Bounce: pressed after bounce-then-confirm", KS_IsPressed(0u));

    /* Release bounce: inactive 5 ticks, then back to pressed. */
    CHECK("Bounce: release pending", KS_Update(0u, RAW_RELEASED, 300u) == KS_EVT_NONE);
    CHECK("Bounce: glitch while releasing keeps key held",
          KS_Update(0u, RAW_PRESSED, 305u) == KS_EVT_NONE);
    CHECK("Bounce: release restarts debounce",
          KS_Update(0u, RAW_RELEASED, 306u) == KS_EVT_NONE);
    CHECK("Bounce: no UP at 19 ticks", KS_Update(0u, RAW_RELEASED, 325u) == KS_EVT_NONE);
    CHECK("Bounce: UP after full 20 stable ticks",
          KS_Update(0u, RAW_RELEASED, 326u) == KS_EVT_UP);
}

/* --- long press once + auto-repeat cadence -------------------------- */
static void test_long_and_repeat(void)
{
    KS_Init();
    CHECK("Long: press pending", KS_Update(0u, RAW_PRESSED, 0u) == KS_EVT_NONE);
    CHECK("Long: DOWN at 20 ticks", KS_Update(0u, RAW_PRESSED, 20u) == KS_EVT_DOWN);
    CHECK("Long: no LONG at 999 ticks", KS_Update(0u, RAW_PRESSED, 1019u) == KS_EVT_NONE);
    CHECK("Long: LONG exactly at 1000 ticks held",
          KS_Update(0u, RAW_PRESSED, 1020u) == KS_EVT_LONG);
    CHECK("Long: LONG fires only once per press",
          KS_Update(0u, RAW_PRESSED, 1021u) == KS_EVT_NONE);
    CHECK("Repeat: no REPEAT one tick early",
          KS_Update(0u, RAW_PRESSED, 1219u) == KS_EVT_NONE);
    CHECK("Repeat: first REPEAT 200 ticks after LONG",
          KS_Update(0u, RAW_PRESSED, 1220u) == KS_EVT_REPEAT);
    CHECK("Repeat: cadence holds (next REPEAT +200)",
          KS_Update(0u, RAW_PRESSED, 1420u) == KS_EVT_REPEAT);
    CHECK("Long: release pending", KS_Update(0u, RAW_RELEASED, 1500u) == KS_EVT_NONE);
    CHECK("Long: UP after release debounce",
          KS_Update(0u, RAW_RELEASED, 1520u) == KS_EVT_UP);
    /* New press must be able to produce LONG again. */
    CHECK("Long: re-press pending", KS_Update(0u, RAW_PRESSED, 2000u) == KS_EVT_NONE);
    CHECK("Long: second press DOWN", KS_Update(0u, RAW_PRESSED, 2020u) == KS_EVT_DOWN);
    CHECK("Long: LONG fires again on the new press",
          KS_Update(0u, RAW_PRESSED, 3020u) == KS_EVT_LONG);
}

/* --- 32-bit tick wrap-around ---------------------------------------- */
static void test_wraparound(void)
{
    uint32_t t;
    bool clean = true;

    KS_Init();
    (void)KS_Update(0u, RAW_RELEASED, 0xFFFFFFF0u);
    /* Press 8 ticks before the rollover: DOWN is due at t=12 (wrapped). */
    CHECK("Wrap: press pending", KS_Update(0u, RAW_PRESSED, 0xFFFFFFF8u) == KS_EVT_NONE);
    for (t = 0xFFFFFFF9u; t != 12u; t++) {
        if (KS_Update(0u, RAW_PRESSED, t) != KS_EVT_NONE) {
            clean = false;
            break;
        }
    }
    CHECK("Wrap: no premature fire across 0xFFFFFFFF->0", clean);
    CHECK("Wrap: DOWN exactly 20 ticks after press across the rollover",
          clean && (KS_Update(0u, RAW_PRESSED, 12u) == KS_EVT_DOWN));
}

/* --- keys are independent ------------------------------------------- */
static void test_two_keys(void)
{
    KS_Init();
    CHECK("Multi: key0 press pending", KS_Update(0u, RAW_PRESSED, 0u) == KS_EVT_NONE);
    CHECK("Multi: key1 press pending", KS_Update(1u, RAW_PRESSED, 5u) == KS_EVT_NONE);
    CHECK("Multi: key0 DOWN at its own 20 ticks",
          KS_Update(0u, RAW_PRESSED, 20u) == KS_EVT_DOWN);
    CHECK("Multi: key1 not confirmed early (only 15 ticks)",
          KS_Update(1u, RAW_PRESSED, 20u) == KS_EVT_NONE);
    CHECK("Multi: key1 DOWN at its own 20 ticks",
          KS_Update(1u, RAW_PRESSED, 25u) == KS_EVT_DOWN);
    CHECK("Multi: both keys read pressed", KS_IsPressed(0u) && KS_IsPressed(1u));
    CHECK("Multi: key0 release pending", KS_Update(0u, RAW_RELEASED, 100u) == KS_EVT_NONE);
    CHECK("Multi: key0 UP after debounce",
          KS_Update(0u, RAW_RELEASED, 120u) == KS_EVT_UP);
    CHECK("Multi: key1 still pressed after key0 released", KS_IsPressed(1u));
    CHECK("Multi: key1 unaffected by key0 release",
          KS_Update(1u, RAW_PRESSED, 120u) == KS_EVT_NONE);
}

/* --- defensive behavior on invalid ids ------------------------------ */
static void test_defensive(void)
{
    KS_Init();
    CHECK("Defensive: id 255 rejected", KS_Update(255u, RAW_PRESSED, 999u) == KS_EVT_NONE);
    CHECK("Defensive: id == KS_MAX_KEYS rejected",
          KS_Update((uint8_t)KS_MAX_KEYS, RAW_PRESSED, 999u) == KS_EVT_NONE);
    CHECK("Defensive: IsPressed(255) is false", !KS_IsPressed(255u));
    CHECK("Defensive: IsPressed(KS_MAX_KEYS) is false",
          !KS_IsPressed((uint8_t)KS_MAX_KEYS));
    /* Invalid calls must not disturb the real key 0. */
    CHECK("Defensive: key0 still works after invalid ids (pending)",
          KS_Update(0u, RAW_PRESSED, 1000u) == KS_EVT_NONE);
    CHECK("Defensive: key0 still works after invalid ids (DOWN)",
          KS_Update(0u, RAW_PRESSED, 1020u) == KS_EVT_DOWN);
}

/* --- polarity mapping of the compiled configuration ----------------- */
static void test_polarity(void)
{
    uint32_t t;
    bool fired = false;

    KS_Init();
    /* Holding the RELEASED level must never produce DOWN or a pressed
     * read, whichever polarity this binary was compiled with. */
    for (t = 0u; t <= 40u; t++) {
        if (KS_Update(0u, RAW_RELEASED, t) != KS_EVT_NONE) {
            fired = true;
        }
    }
    CHECK("Polarity(" POLARITY_TAG "): released level never fires DOWN", !fired);
    CHECK("Polarity(" POLARITY_TAG "): released level never reads pressed",
          !KS_IsPressed(0u));
    CHECK("Polarity: suite compiled for " POLARITY_TAG, true);
}

int main(void)
{
    test_down_and_up();
    test_bounce();
    test_long_and_repeat();
    test_wraparound();
    test_two_keys();
    test_defensive();
    test_polarity();

    printf("Summary: %d checks, %d passed, %d failed\n",
           g_total, g_total - g_failed, g_failed);
    if (g_failed > 0) {
        printf("=== TESTS FAILED ===\n");
        return g_failed;
    }
    printf("=== ALL TESTS PASSED ===\n");
    return 0;
}
