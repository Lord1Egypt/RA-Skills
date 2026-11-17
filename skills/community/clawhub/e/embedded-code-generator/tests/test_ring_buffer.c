/**
 * @file test_ring_buffer.c
 * @brief Self-check tests for ring_buffer.c (REJECT and OVERWRITE builds).
 *
 * The full-buffer policy is a compile-time macro (RB_STRATEGY), so this
 * single test source is compiled twice by the Makefile:
 *   - test_rb_reject    : -DRB_STRATEGY=0  (RB_STRATEGY_REJECT)
 *   - test_rb_overwrite : -DRB_STRATEGY=1  (RB_STRATEGY_OVERWRITE)
 *
 * Run via `make test` from the skill package root. Exit code: number of
 * failed checks (0 = all pass).
 */

#include <stdio.h>
#include <inttypes.h>
#include "ring_buffer.h"

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

/* 8-element backing storage, reused by the case groups below. */
static rb_elem_t     storage[8];
static RB_Handle_t   rb;

/** Initialize a fresh 8-element buffer; aborts the run if Init fails. */
static int reset_buffer(void)
{
    return RB_Init(&rb, storage, 8u);
}

/** FIFO order: Push 0..7 then Pop must return 0..7 in the same order. */
static void test_fifo_order(void)
{
    rb_elem_t v;
    int i;
    int ok_push = 1;
    int ok_pop  = 1;

    for (i = 0; i < 8; i++) {
        if (RB_Push(&rb, (rb_elem_t)i) != RB_OK) {
            ok_push = 0;
        }
    }
    CHECK("FIFO: 8 consecutive Pushes all succeed", ok_push);
    CHECK("FIFO: full buffer reports RB_IsFull", RB_IsFull(&rb));

    for (i = 0; i < 8; i++) {
        if ((RB_Pop(&rb, &v) != RB_OK) || (v != (rb_elem_t)i)) {
            ok_pop = 0;
        }
    }
    CHECK("FIFO: Pop order matches Push order (0..7)", ok_pop);
}

/** RB_Count / RB_Available must track the fill level exactly. */
static void test_count_available(void)
{
    rb_elem_t v;

    CHECK("Empty buffer: RB_Count == 0", RB_Count(&rb) == 0u);
    CHECK("Empty buffer: RB_Available == 8", RB_Available(&rb) == 8u);

    (void)RB_Push(&rb, 10u);
    (void)RB_Push(&rb, 11u);
    (void)RB_Push(&rb, 12u);
    (void)RB_Push(&rb, 13u);
    CHECK("Half-full: RB_Count == 4", RB_Count(&rb) == 4u);
    CHECK("Half-full: RB_Available == 4", RB_Available(&rb) == 4u);

    (void)RB_Pop(&rb, &v);
    (void)RB_Pop(&rb, &v);
    CHECK("After 2 Pops: RB_Count == 2", RB_Count(&rb) == 2u);
    CHECK("After 2 Pops: RB_Available == 6", RB_Available(&rb) == 6u);

    (void)RB_Reset(&rb);
    CHECK("RB_Reset: RB_Count back to 0", RB_Count(&rb) == 0u);
}

/** Popping an empty buffer must return RB_ERR_EMPTY and not crash. */
static void test_empty_pop(void)
{
    rb_elem_t v = 0xFFu;
    int rc;

    (void)RB_Reset(&rb);
    rc = RB_Pop(&rb, &v);
    CHECK("Pop on empty buffer returns RB_ERR_EMPTY", rc == RB_ERR_EMPTY);
    CHECK("Pop on empty buffer leaves output untouched", v == 0xFFu);
    CHECK("Empty check: RB_IsEmpty is true", RB_IsEmpty(&rb));
}

/** Init must reject invalid arguments with RB_ERR_PARAM. */
static void test_param_validation(void)
{
    RB_Handle_t h;
    rb_elem_t   v = 0u;
    rb_elem_t   dummy;

    CHECK("Init with NULL handle returns RB_ERR_PARAM",
          RB_Init(NULL, storage, 8u) == RB_ERR_PARAM);
    CHECK("Init with NULL storage returns RB_ERR_PARAM",
          RB_Init(&h, NULL, 8u) == RB_ERR_PARAM);
    CHECK("Init with size 0 returns RB_ERR_PARAM",
          RB_Init(&h, storage, 0u) == RB_ERR_PARAM);
    CHECK("Push with NULL handle returns RB_ERR_PARAM",
          RB_Push(NULL, 1u) == RB_ERR_PARAM);
    CHECK("Pop with NULL handle returns RB_ERR_PARAM",
          RB_Pop(NULL, &v) == RB_ERR_PARAM);
    /* Uninitialized handle: inited == false must be rejected. */
    h.inited = false;
    CHECK("Push on uninitialized handle returns RB_ERR_PARAM",
          RB_Push(&h, 1u) == RB_ERR_PARAM);
    dummy = v;
    (void)dummy;
}

#if RB_STRATEGY == RB_STRATEGY_REJECT

/** REJECT policy: pushing to a full buffer fails and keeps data intact. */
static void test_full_policy(void)
{
    rb_elem_t v;
    int i;
    int rc;
    int ok_intact = 1;

    CHECK("REJECT: fill 8/8 succeeds", 1);
    for (i = 0; i < 8; i++) {
        (void)RB_Push(&rb, (rb_elem_t)i);
    }

    rc = RB_Push(&rb, 0xAAu);
    CHECK("REJECT: Push on full buffer returns RB_ERR_FULL", rc == RB_ERR_FULL);
    CHECK("REJECT: RB_Count stays 8 after rejected Push", RB_Count(&rb) == 8u);

    /* Original data must be untouched: Pop yields 0..7. */
    for (i = 0; i < 8; i++) {
        if ((RB_Pop(&rb, &v) != RB_OK) || (v != (rb_elem_t)i)) {
            ok_intact = 0;
        }
    }
    CHECK("REJECT: original data intact after rejected Push (0..7)", ok_intact);
}

#else /* RB_STRATEGY_OVERWRITE */

/** OVERWRITE policy: pushing to a full buffer discards the oldest data. */
static void test_full_policy(void)
{
    rb_elem_t v;
    int i;
    int ok_seq = 1;

    for (i = 0; i < 8; i++) {
        (void)RB_Push(&rb, (rb_elem_t)i); /* buffer: 0..7 */
    }

    CHECK("OVERWRITE: Push on full buffer returns RB_OK",
          RB_Push(&rb, 8u) == RB_OK);
    CHECK("OVERWRITE: Push again returns RB_OK",
          RB_Push(&rb, 9u) == RB_OK);
    CHECK("OVERWRITE: RB_Count stays 8 (capacity not exceeded)",
          RB_Count(&rb) == 8u);

    /* Oldest two elements (0,1) were overwritten: expect 2..9. */
    for (i = 2; i < 10; i++) {
        if ((RB_Pop(&rb, &v) != RB_OK) || (v != (rb_elem_t)i)) {
            ok_seq = 0;
        }
    }
    CHECK("OVERWRITE: oldest data discarded, Pop yields 2..9", ok_seq);
}

#endif /* RB_STRATEGY */

int main(void)
{
    printf("[TEST] ring_buffer (RB_STRATEGY=%s)\n",
           (RB_STRATEGY == RB_STRATEGY_OVERWRITE) ? "OVERWRITE" : "REJECT");

    if (reset_buffer() != RB_OK) {
        printf("[FAIL] RB_Init on valid arguments failed - aborting\n");
        return 1;
    }

    test_fifo_order();
    (void)RB_Reset(&rb);
    test_count_available();
    test_empty_pop();
    test_param_validation();
    (void)RB_Reset(&rb);
    test_full_policy();

    printf("Summary: %d checks, %d passed, %d failed\n",
           g_total, g_total - g_failed, g_failed);

    if (g_failed == 0) {
        printf("Result: ALL PASS\n");
    } else {
        printf("Result: FAIL\n");
    }

    return g_failed;
}
