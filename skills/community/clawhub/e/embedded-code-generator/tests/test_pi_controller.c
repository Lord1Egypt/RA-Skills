/**
 * @file test_pi_controller.c
 * @brief Unit tests for the PI controller (float API).
 *
 * Covers: parameter validation, backward-Euler discrete response
 * (hand-computed), anti-windup clamping (saturation does not wind
 * the integral), independent integral clamping, reset semantics,
 * and runtime re-tuning.
 */

#include <stdio.h>
#include <string.h>
#include <math.h>
#include "pi_controller.h"

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
    PI_Handle_t pi;

    /* --- parameter validation --- */
    CHECK(PI_Init(&pi, 0.5f, 10.0f, 0.001f, -24.0f, 24.0f, -24.0f, 24.0f) == 0,
          "init: valid params return 0");
    CHECK(PI_Init(NULL, 0.5f, 10.0f, 0.001f, -24.0f, 24.0f, -24.0f, 24.0f) == -1,
          "init: NULL handle rejected");
    {
        PI_Handle_t p2;
        CHECK(PI_Init(&p2, 0.5f, 10.0f, 0.0f, -24.0f, 24.0f, -24.0f, 24.0f) == -1,
              "init: Ts=0 rejected");
        CHECK(PI_Init(&p2, 0.5f, 10.0f, 0.001f, 24.0f, -24.0f, -24.0f, 24.0f) == -1,
              "init: out_min >= out_max rejected");
        CHECK(PI_Init(&p2, 0.5f, 10.0f, 0.001f, -24.0f, 24.0f, 24.0f, -24.0f) == -1,
              "init: i_min >= i_max rejected");
    }

    /* --- discrete response: backward Euler, hand-computed --- */
    /* Kp=0.5 Ki=10 Ts=0.001, error=1.0:
     *   step1: i = 10*1.0*0.001 = 0.01, out = 0.5 + 0.01 = 0.51
     *   step2: i = 0.02, out = 0.52                                */
    {
        float y1 = PI_Compute(&pi, 1.0f);
        float y2 = PI_Compute(&pi, 1.0f);
        CHECK(NEAR(y1, 0.51f, 1e-5f), "compute: step1 out = Kp*e + Ki*e*Ts");
        CHECK(NEAR(y2, 0.52f, 1e-5f), "compute: step2 accumulates integral");
    }

    /* --- reset semantics --- */
    PI_Reset(&pi);
    {
        float y = PI_Compute(&pi, 1.0f);
        CHECK(NEAR(y, 0.51f, 1e-5f), "reset: integral cleared, step1 repeats");
        CHECK(NEAR(pi.integral, 0.01f, 1e-5f), "reset: integral restarted from 0");
        CHECK(NEAR(pi.prev_error, 1.0f, 1e-6f), "prev_error tracks last error");
    }

    /* --- anti-windup: saturated high does NOT integrate (error > 0) --- */
    {
        PI_Handle_t p3;
        int i;
        float y;
        (void)PI_Init(&p3, 1.0f, 100.0f, 0.01f, -1.0f, 1.0f, -1.0f, 1.0f);
        for (i = 0; i < 5; i++) {
            y = PI_Compute(&p3, 10.0f);
        }
        CHECK(NEAR(y, 1.0f, 1e-6f), "anti-windup: output clamped to out_max");
        CHECK(NEAR(p3.integral, 0.0f, 1e-4f),
              "anti-windup: saturated + error>0 does not integrate");
        /* error goes to zero: output must drop immediately (no windup) */
        y = PI_Compute(&p3, 0.0f);
        CHECK(NEAR(y, 0.0f, 1e-4f),
              "anti-windup: no residual windup when error returns to 0");
    }

    /* --- anti-windup: saturated low does NOT integrate (error < 0) --- */
    {
        PI_Handle_t p4;
        float y;
        (void)PI_Init(&p4, 1.0f, 100.0f, 0.01f, -1.0f, 1.0f, -1.0f, 1.0f);
        y = PI_Compute(&p4, -10.0f);
        CHECK(NEAR(y, -1.0f, 1e-6f), "anti-windup: output clamped to out_min");
        CHECK(NEAR(p4.integral, 0.0f, 1e-4f),
              "anti-windup: saturated + error<0 does not integrate");
    }

    /* --- independent integral clamp (state-level) --- */
    {
        PI_Handle_t p5;
        float y;
        /* Kp=0 so output = raw i_term; i limited to +-0.05.
         * Note: the template clamps the *integral state* after storing;
         * the returned output of the current step uses the pre-clamp
         * i_term (documented "belt-and-suspenders" behaviour). */
        (void)PI_Init(&p5, 0.0f, 10.0f, 0.01f, -24.0f, 24.0f, -0.05f, 0.05f);
        y = PI_Compute(&p5, 1.0f);   /* raw i_term = 0.1 */
        CHECK(NEAR(y, 0.1f, 1e-5f),
              "i-clamp: current-step output uses pre-clamp integral");
        CHECK(NEAR(p5.integral, 0.05f, 1e-5f),
              "i-clamp: integral state held at i_max");
        y = PI_Compute(&p5, 1.0f);   /* i_term = 0.05+0.1=0.15, state re-clamped */
        CHECK(NEAR(p5.integral, 0.05f, 1e-5f),
              "i-clamp: integral stays clamped across steps");
    }

    /* --- runtime re-tuning keeps integral --- */
    {
        PI_Handle_t p6;
        float y;
        (void)PI_Init(&p6, 0.5f, 10.0f, 0.001f, -24.0f, 24.0f, -24.0f, 24.0f);
        (void)PI_Compute(&p6, 1.0f);          /* integral = 0.01 */
        CHECK(PI_SetTuning(&p6, 1.0f, 20.0f) == 0, "retune: returns 0");
        CHECK(PI_SetTuning(NULL, 1.0f, 20.0f) == -1, "retune: NULL rejected");
        y = PI_Compute(&p6, 0.0f);            /* out = 0 + preserved integral */
        CHECK(NEAR(y, 0.01f, 1e-5f), "retune: integral preserved across retune");
    }

    /* --- un-inited compute fails safe --- */
    {
        PI_Handle_t p7;
        memset(&p7, 0, sizeof(p7));
        p7.inited = false;
        CHECK(NEAR(PI_Compute(&p7, 5.0f), 0.0f, 1e-6f),
              "safety: compute on un-inited handle returns 0");
        CHECK(NEAR(PI_Compute(NULL, 5.0f), 0.0f, 1e-6f),
              "safety: compute on NULL returns 0");
    }

    printf("Summary: %d checks, %d passed, %d failed\n", g_total, g_pass, g_fail);
    return (g_fail == 0) ? 0 : 1;
}
