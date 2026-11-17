/**
 * @file test_lowpass_filter.c
 * @brief Unit tests for the first-order IIR low-pass filter (float API).
 *
 * Covers: alpha computation from fc/Ts (bilinear), parameter validation,
 * hand-computed step response, geometric convergence to steady state,
 * reset semantics, fail-safe pass-through, and relative filtering
 * strength between alphas.
 */

#include <stdio.h>
#include <string.h>
#include <math.h>
#include "lowpass_filter.h"

static int g_total = 0;
static int g_pass  = 0;
static int g_fail  = 0;

#define CHECK(cond, name)                                        \
    do {                                                         \
        g_total++;                                               \
        if (cond) { g_pass++; }                                  \
        else { g_fail++; printf("[FAIL] %s\n", name); }          \
    } while (0)

#define NEAR(a, b, eps)  (fabsf((a) - (b)) < (eps))

int main(void)
{
    LPF_Handle_t lpf;

    /* --- InitFreq: alpha = w*Ts / (1 + w*Ts), w = 2*pi*fc --- */
    /* fc=200, Ts=0.001 -> w*Ts = 1.256637 -> alpha = 0.55681 */
    CHECK(LPF_InitFreq(&lpf, 200.0f, 0.001f) == 0, "initFreq: valid params return 0");
    CHECK(NEAR(lpf.alpha, 0.55681f, 1e-4f), "initFreq: alpha matches bilinear formula");
    CHECK(NEAR(lpf.one_minus, 1.0f - lpf.alpha, 1e-6f), "initFreq: one_minus precomputed");
    CHECK(LPF_InitFreq(NULL, 200.0f, 0.001f) == -1, "initFreq: NULL rejected");
    CHECK(LPF_InitFreq(&lpf, 0.0f, 0.001f) == -1, "initFreq: fc=0 rejected");
    CHECK(LPF_InitFreq(&lpf, 200.0f, 0.0f) == -1, "initFreq: Ts=0 rejected");

    /* --- InitAlpha validation --- */
    CHECK(LPF_InitAlpha(&lpf, 0.5f) == 0, "initAlpha: valid alpha returns 0");
    CHECK(LPF_InitAlpha(NULL, 0.5f) == -1, "initAlpha: NULL rejected");
    CHECK(LPF_InitAlpha(&lpf, 0.0f) == -1, "initAlpha: alpha=0 rejected");
    CHECK(LPF_InitAlpha(&lpf, 1.0f) == -1, "initAlpha: alpha=1 rejected");
    CHECK(LPF_InitAlpha(&lpf, -0.2f) == -1, "initAlpha: negative alpha rejected");

    /* --- step response, alpha=0.5, input 10:
     *     y1 = 0.5*10 = 5.0
     *     y2 = 0.5*10 + 0.5*5  = 7.5
     *     y3 = 0.5*10 + 0.5*7.5 = 8.75                            */
    (void)LPF_InitAlpha(&lpf, 0.5f);
    {
        float y1 = LPF_Update(&lpf, 10.0f);
        float y2 = LPF_Update(&lpf, 10.0f);
        float y3 = LPF_Update(&lpf, 10.0f);
        CHECK(NEAR(y1, 5.0f, 1e-5f), "step: y1 = alpha*x");
        CHECK(NEAR(y2, 7.5f, 1e-5f), "step: y2 = a*x + (1-a)*y1");
        CHECK(NEAR(y3, 8.75f, 1e-5f), "step: y3 geometric");
    }

    /* --- steady-state convergence --- */
    {
        int i;
        float y = 0.0f;
        for (i = 0; i < 300; i++) {
            y = LPF_Update(&lpf, 10.0f);
        }
        CHECK(fabsf(y - 10.0f) < 0.001f, "steady: converges to DC input");
    }

    /* --- heavier filtering = slower rise --- */
    {
        LPF_Handle_t fast, slow;
        int i;
        float yf = 0.0f, ys = 0.0f;
        (void)LPF_InitAlpha(&fast, 0.9f);
        (void)LPF_InitAlpha(&slow, 0.1f);
        for (i = 0; i < 5; i++) {
            yf = LPF_Update(&fast, 10.0f);
            ys = LPF_Update(&slow, 10.0f);
        }
        CHECK(yf > ys, "compare: alpha=0.9 rises faster than alpha=0.1");
    }

    /* --- reset semantics --- */
    LPF_Reset(&lpf);
    CHECK(NEAR(lpf.y_prev, 0.0f, 1e-9f), "reset: state cleared");
    CHECK(NEAR(LPF_Update(&lpf, 10.0f), 5.0f, 1e-5f),
          "reset: first sample after reset = alpha*x");

    /* --- fail-safe pass-through on un-inited handle --- */
    {
        LPF_Handle_t bad;
        memset(&bad, 0, sizeof(bad));
        bad.inited = false;
        CHECK(NEAR(LPF_Update(&bad, 3.25f), 3.25f, 1e-6f),
              "safety: un-inited update passes input through");
        CHECK(NEAR(LPF_Update(NULL, 1.5f), 1.5f, 1e-6f),
              "safety: NULL update passes input through");
    }

    printf("Summary: %d checks, %d passed, %d failed\n", g_total, g_pass, g_fail);
    return (g_fail == 0) ? 0 : 1;
}
