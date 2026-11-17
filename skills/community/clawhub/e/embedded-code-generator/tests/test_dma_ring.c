/**
 * @file test_dma_ring.c
 * @brief Self-check tests for dma_ring.c (DMA circular-mode tracking).
 *
 * Run via `make test` from the skill package root. Exit code: number
 * of failed checks (0 = all pass).
 */

#include <stdio.h>
#include <string.h>
#include "dma_ring.h"

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

static uint8_t     buf[8];
static DRB_Handle_t rb;

static void reset_all(void)
{
    memset(buf, 0, sizeof(buf));
    (void)DRB_Init(&rb, buf, (DRB_SIZE_TYPE)sizeof(buf));
}

/* Basic: init validation. */
static void test_init(void)
{
    DRB_Handle_t bad;
    CHECK("DRB Init: OK on valid args",
          DRB_Init(&rb, buf, (DRB_SIZE_TYPE)sizeof(buf)) == DRB_OK);
    CHECK("DRB Init: rejects NULL buffer",
          DRB_Init(&bad, NULL, 8u) == DRB_ERR_PARAM);
    CHECK("DRB Init: rejects size 0",
          DRB_Init(&bad, buf, 0u) == DRB_ERR_PARAM);
}

/* Sequential: DMA writes 0,1,2 then CPU reads them back. */
static void test_sequential(void)
{
    uint8_t out[8];
    size_t n;

    reset_all();
    CHECK("Seq: empty right after init", DRB_IsEmpty(&rb));
    /* Simulate the DMA engine writing 0,1,2 into the buffer. */
    buf[0] = 0u; buf[1] = 1u; buf[2] = 2u;
    CHECK("Seq: update wpos=3 accepted",
          DRB_UpdateWriteIndex(&rb, 3u) == DRB_OK);
    CHECK("Seq: available == 3", DRB_Available(&rb) == 3u);

    n = DRB_Read(&rb, out, sizeof(out));
    CHECK("Seq: read returns 3 bytes", n == 3u);
    CHECK("Seq: bytes preserved", (out[0] == 0u) && (out[1] == 1u) && (out[2] == 2u));
    CHECK("Seq: empty after drain", DRB_IsEmpty(&rb));
}

/* Wrap: DMA crosses the buffer tail and continues from index 0. */
static void test_wrap(void)
{
    uint8_t out[8];
    size_t n;

    reset_all();
    (void)DRB_UpdateWriteIndex(&rb, 6u);          /* wrote 6 bytes  */
    n = DRB_Read(&rb, out, sizeof(out));          /* drain 6        */
    CHECK("Wrap: drained 6 after first update", n == 6u);

    (void)DRB_UpdateWriteIndex(&rb, 2u);          /* wrapped: 6->7,0,1,2 */
    CHECK("Wrap: available == 4 after wrap", DRB_Available(&rb) == 4u);
    n = DRB_Read(&rb, out, sizeof(out));
    CHECK("Wrap: read 4 bytes across the tail", n == 4u);
    CHECK("Wrap: empty after drain", DRB_IsEmpty(&rb));
}

/* Chunked read: Read stops at the tail; the caller loops. */
static void test_chunked_read(void)
{
    uint8_t out[8];   /* large enough for the whole run */
    size_t n1;
    size_t n2;

    reset_all();
    (void)DRB_UpdateWriteIndex(&rb, 5u);          /* indices 0..4   */
    n1 = DRB_Read(&rb, out, 3u);                  /* cap at 3       */
    n2 = DRB_Read(&rb, out + n1, sizeof(out) - n1);
    CHECK("Chunk: first chunk capped at 3", n1 == 3u);
    CHECK("Chunk: second chunk takes the rest", n2 == 2u);
    CHECK("Chunk: third read is empty", DRB_Read(&rb, out, sizeof(out)) == 0u);
}

/* Overrun: DMA laps the read position; oldest data reported lost.
 * Sequence: write 5 (read still at 0, only 2 free slots left with the
 * one-slot gap), then write 3 more -> produced 6 > free 2 -> overrun. */
static void test_overrun(void)
{
    uint8_t out[8];
    size_t n;

    reset_all();
    CHECK("Ovr: no overrun initially", !DRB_IsOverrun(&rb));
    (void)DRB_UpdateWriteIndex(&rb, 5u);          /* 5 new, read at 0 */
    CHECK("Ovr: no overrun when data fits", !DRB_IsOverrun(&rb));
    (void)DRB_UpdateWriteIndex(&rb, 3u);          /* laps: 6 > 2 free  */
    CHECK("Ovr: overrun flag set", DRB_IsOverrun(&rb));
    n = DRB_Read(&rb, out, sizeof(out));
    CHECK("Ovr: read resyncs, no garbage (<= capacity)", n <= 8u);
    CHECK("Ovr: empty after resync read", DRB_IsEmpty(&rb));
    DRB_ClearFlags(&rb);
    CHECK("Ovr: flag cleared by DRB_ClearFlags", !DRB_IsOverrun(&rb));
}

/* Drain mode: NULL out buffer discards data. */
static void test_drain(void)
{
    reset_all();
    (void)DRB_UpdateWriteIndex(&rb, 4u);
    CHECK("Drain: NULL out discards 4 bytes",
          DRB_Read(&rb, NULL, 100u) == 4u);
    CHECK("Drain: empty after discard", DRB_IsEmpty(&rb));
    CHECK("Drain: NULL out with 0 len is valid", DRB_Read(&rb, NULL, 0u) == 0u);
}

/* Parameter validation. */
static void test_params(void)
{
    DRB_Handle_t uninit;
    uint8_t out[2];

    reset_all();
    memset(&uninit, 0, sizeof(uninit));
    CHECK("Param: update rejects wpos >= size",
          DRB_UpdateWriteIndex(&rb, (DRB_SIZE_TYPE)sizeof(buf)) == DRB_ERR_PARAM);
    CHECK("Param: update rejects NULL handle", DRB_UpdateWriteIndex(NULL, 1u) == DRB_ERR_PARAM);
    CHECK("Param: read rejects NULL handle", DRB_Read(NULL, out, sizeof(out)) == (size_t)DRB_ERR_PARAM);
    CHECK("Param: NULL out with len>0 is legal drain mode",
          (reset_all(), DRB_UpdateWriteIndex(&rb, 4u) == DRB_OK) &&
          (DRB_Read(&rb, NULL, 100u) == 4u));
    CHECK("Param: available on uninit is 0", DRB_Available(&uninit) == 0u);
    CHECK("Param: overrun on uninit is false", !DRB_IsOverrun(&uninit));
}

int main(void)
{
    test_init();
    test_sequential();
    test_wrap();
    test_chunked_read();
    test_overrun();
    test_drain();
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
