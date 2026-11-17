/**
 * @file test_adc_avg_filter.c
 * @brief Deterministic unit tests for the ADC averaging filter.
 *
 * Covers: plain mean with rounding, trimmed mean outlier rejection,
 * 32-bit accumulator overflow safety (255 x full scale), stateless
 * (idempotent) repeated runs, and parameter validation.
 */

#include <stdio.h>
#include <string.h>
#include "adc_avg_filter.h"

/* ------------------------------------------------------------------ */
/* Check framework                                                     */
/* ------------------------------------------------------------------ */

static int g_total = 0;
static int g_pass  = 0;
static int g_fail  = 0;

#define CHECK(cond, name)                                        \
    do {                                                         \
        g_total++;                                               \
        if (cond) { g_pass++; }                                  \
        else { g_fail++; printf("[FAIL] %s\n", name); }          \
    } while (0)

/* ------------------------------------------------------------------ */
/* Deterministic sample sources                                        */
/* ------------------------------------------------------------------ */

/** Replays a fixed table, restarting from index 0 on each reset. */
static const uint16_t *seq_tab;
static unsigned        seq_len;
static unsigned        seq_idx;

static void seq_reset(const uint16_t *tab, unsigned len)
{
    seq_tab = tab;
    seq_len = len;
    seq_idx = 0u;
}

static uint16_t seq_read(void)
{
    uint16_t v = seq_tab[seq_idx];

    seq_idx = (seq_idx + 1u) % seq_len;
    return v;
}

/** Always returns a fixed value (for overflow test). */
static unsigned fixed_val;
static unsigned fixed_calls;

static uint16_t fixed_read(void)
{
    fixed_calls++;
    return (uint16_t)fixed_val;
}

/** Callback that counts invocations (for call-count check). */
static uint16_t counting_read(void)
{
    return fixed_read();
}

/* ------------------------------------------------------------------ */
/* Test cases                                                          */
/* ------------------------------------------------------------------ */

int main(void)
{
    static uint16_t buf[ADCF_MAX_SAMPLES];
    uint16_t out = 0u;
    unsigned i;
    int      rc;

    /* --- plain mean with round-to-nearest ------------------------- */
    {
        const uint16_t tab[] = { 100u, 200u, 201u, 300u };
        seq_reset(tab, 4u);
        rc = ADCF_Collect(seq_read, buf, 4u);
        CHECK(rc == ADCF_OK, "collect OK");
        rc = ADCF_Mean(buf, 4u, &out);
        /* sum=801 -> 801/4 = 200.25 -> rounds to 200 */
        CHECK((rc == ADCF_OK) && (out == 200u), "mean 801/4 rounds to 200");

        seq_reset(tab, 4u);
        (void)ADCF_Collect(seq_read, buf, 4u);
        rc = ADCF_Mean(buf, 4u, &out);
        CHECK((rc == ADCF_OK) && (out == 200u), "mean is idempotent (same table)");
    }

    {
        /* sum=802 -> 802/4 = 200.5 -> rounds to 201 (half up) */
        const uint16_t tab[] = { 100u, 200u, 202u, 300u };
        seq_reset(tab, 4u);
        (void)ADCF_Collect(seq_read, buf, 4u);
        rc = ADCF_Mean(buf, 4u, &out);
        CHECK((rc == ADCF_OK) && (out == 201u), "mean 802/4 rounds to 201");
    }

    /* --- trimmed mean rejects single-sample glitches -------------- */
    {
        /* 1 and 1000 are outliers; remaining 100/200/300 -> 200 */
        const uint16_t tab[] = { 100u, 200u, 300u, 1000u, 1u };
        seq_reset(tab, 5u);
        rc = ADCF_Collect(seq_read, buf, 5u);
        rc |= ADCF_TrimmedMean(buf, 5u, &out);
        CHECK((rc == ADCF_OK) && (out == 200u),
              "trimmed mean drops min and max");

        /* All-equal samples stay stable after trimming. */
        const uint16_t tab2[] = { 1234u, 1234u, 1234u, 1234u };
        seq_reset(tab2, 4u);
        (void)ADCF_Collect(seq_read, buf, 4u);
        rc = ADCF_TrimmedMean(buf, 4u, &out);
        CHECK((rc == ADCF_OK) && (out == 1234u),
              "trimmed mean stable on constant input");

        /* Glitch on an otherwise constant signal is removed. */
        const uint16_t tab3[] = { 500u, 500u, 500u, 500u, 4000u, 500u, 500u };
        seq_reset(tab3, 7u);
        rc = ADCF_Filter(seq_read, buf, 7u, &out);
        CHECK((rc == ADCF_OK) && (out == 500u),
              "one-shot filter removes spike from constant signal");
    }

    /* --- overflow safety: 255 x full scale ------------------------ */
    fixed_val = 65535u; fixed_calls = 0u;
    rc = ADCF_Filter(fixed_read, buf, 255u, &out);
    CHECK((rc == ADCF_OK) && (out == 65535u),
          "255 x 0xFFFF mean stays at full scale (uint32 accumulator)");
    CHECK(fixed_calls == 255u, "read callback called exactly 255 times");

    /* Plain mean hits the same ceiling. */
    fixed_val = 65535u;
    (void)ADCF_Collect(fixed_read, buf, 255u);
    rc = ADCF_Mean(buf, 255u, &out);
    CHECK((rc == ADCF_OK) && (out == 65535u),
          "plain mean of 255 x 0xFFFF does not wrap");

    /* Half scale keeps exact value. */
    fixed_val = 32768u;
    (void)ADCF_Collect(fixed_read, buf, 255u);
    rc = ADCF_TrimmedMean(buf, 255u, &out);
    CHECK((rc == ADCF_OK) && (out == 32768u),
          "trimmed mean of 255 x 0x8000 is exact");

    /* --- one-shot filter == collect + trimmed --------------------- */
    {
        const uint16_t tab[] = { 10u, 20u, 30u, 40u, 100u };
        uint16_t manual;

        seq_reset(tab, 5u);
        (void)ADCF_Collect(seq_read, buf, 5u);
        rc = ADCF_TrimmedMean(buf, 5u, &manual);

        seq_reset(tab, 5u);
        rc |= ADCF_Filter(seq_read, buf, 5u, &out);
        CHECK((rc == ADCF_OK) && (out == manual) && (out == 30u),
              "Filter matches Collect+TrimmedMean");
    }

    /* --- parameter validation ------------------------------------- */
    fixed_val = 1u;
    CHECK(ADCF_Collect(NULL, buf, 4u) == ADCF_ERR_PARAM, "Collect NULL fn rejected");
    CHECK(ADCF_Collect(fixed_read, NULL, 4u) == ADCF_ERR_PARAM, "Collect NULL buf rejected");
    CHECK(ADCF_Collect(fixed_read, buf, 0u) == ADCF_ERR_PARAM, "Collect n=0 rejected");
    CHECK(ADCF_Collect(fixed_read, buf, ADCF_MAX_SAMPLES) == ADCF_OK,
          "Collect n=255 (uint8_t max) accepted");
    CHECK(ADCF_Mean(NULL, 4u, &out) == ADCF_ERR_PARAM, "Mean NULL buf rejected");
    CHECK(ADCF_Mean(buf, 2u, NULL) == ADCF_ERR_PARAM, "Mean NULL out rejected");
    CHECK(ADCF_TrimmedMean(buf, 2u, &out) == ADCF_ERR_PARAM,
          "TrimmedMean n<3 rejected");
    CHECK(ADCF_Filter(NULL, buf, 8u, &out) == ADCF_ERR_PARAM, "Filter NULL fn rejected");
    CHECK(ADCF_Filter(fixed_read, buf, 2u, &out) == ADCF_ERR_PARAM,
          "Filter n<3 rejected");

    /* --- read callback invocation count --------------------------- */
    fixed_calls = 0u;
    (void)ADCF_Collect(counting_read, buf, 16u);
    CHECK(fixed_calls == 16u, "Collect calls read_fn exactly n times");

    /* --- statelessness: buffer content fully determines output ---- */
    for (i = 0u; i < 8u; i++)
    {
        buf[i] = (uint16_t)(100u + i * 10u);
    }
    rc = ADCF_TrimmedMean(buf, 8u, &out);
    /* drop 100 and 170 -> (110+120+130+140+150+160) = 810 / 6 = 135 */
    CHECK((rc == ADCF_OK) && (out == 135u),
          "trimmed mean from pre-filled buffer");
    rc = ADCF_TrimmedMean(buf, 8u, &out);
    CHECK((rc == ADCF_OK) && (out == 135u),
          "repeated call gives identical result (no hidden state)");

    printf("test_adc_avg_filter: %d/%d passed\n", g_pass, g_total);
    return (g_fail == 0) ? 0 : 1;
}
