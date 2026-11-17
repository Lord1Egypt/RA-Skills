/**
 * @file test_svpwm.c
 * @brief Unit tests for the SVPWM modulator.
 *
 * Covers: init validation, zero-vector symmetry (all duties 0.5),
 * sector mapping across all six hexagon sectors (angle sweep with
 * hand-checked N-variable mapping), duty bounds, overmodulation
 * clamping, bus-voltage scaling, and sector query.
 */

#include <stdio.h>
#include <string.h>
#include <math.h>
#include "svpwm.h"

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

/** Reference amplitude in volts for the angle sweep. */
#define VREF  5.0f
#define VDC   24.0f

static float deg2rad(float d)
{
    return d * 3.14159265358979f / 180.0f;
}

int main(void)
{
    SVPWM_Handle_t sv;

    /* --- Init validation --- */
    CHECK(SVPWM_Init(&sv, VDC, 0.0001f) == SVPWM_OK, "init: valid params return OK");
    CHECK(NEAR(sv.half_dc, VDC / 1.7320508f, 1e-3f),
          "init: half_dc = Vdc / sqrt(3)");
    CHECK(SVPWM_Init(NULL, VDC, 0.0001f) == SVPWM_ERR_PARAM, "init: NULL rejected");
    CHECK(SVPWM_Init(&sv, 0.0f, 0.0001f) == SVPWM_ERR_PARAM, "init: Vdc=0 rejected");
    CHECK(SVPWM_Init(&sv, -12.0f, 0.0001f) == SVPWM_ERR_PARAM,
          "init: negative Vdc rejected");

    /* --- zero vector: all three duties 0.5 (symmetry) --- */
    {
        float ta, tb, tc;
        CHECK(SVPWM_Compute(&sv, 0.0f, 0.0f, &ta, &tb, &tc) == SVPWM_OK,
              "zero: compute OK");
        CHECK(NEAR(ta, 0.5f, 1e-5f) && NEAR(tb, 0.5f, 1e-5f) && NEAR(tc, 0.5f, 1e-5f),
              "zero: all duties 0.5 at zero vector");
    }

    /* --- sector sweep: 30/90/150/210/270/330 deg -> sectors 1..6 --- */
    {
        const float angles[6] = {30.0f, 90.0f, 150.0f, 210.0f, 270.0f, 330.0f};
        int k;
        for (k = 0; k < 6; k++) {
            float va = VREF * cosf(deg2rad(angles[k]));
            float vb = VREF * sinf(deg2rad(angles[k]));
            float ta, tb, tc;
            (void)SVPWM_Compute(&sv, va, vb, &ta, &tb, &tc);
            CHECK(SVPWM_GetSector(&sv) == (uint8_t)(k + 1),
                  "sector: angle sweep maps to consecutive sectors 1..6");
            CHECK(ta >= 0.0f && ta <= 1.0f && tb >= 0.0f && tb <= 1.0f &&
                  tc >= 0.0f && tc <= 1.0f,
                  "sector: duties within [0,1]");
        }
    }

    /* --- hand-checked duty in sector 1 centre (theta = 30 deg) --- */
    {
        /* va = 5*cos30 = 4.3301, vb = 2.5, Vdc = 24
         * X = sqrt(3)*vb/Vdc = 0.18042
         * Y = (sqrt(3)/2*vb + 1.5*va)/Vdc = (2.1651 + 6.4952)/24 = 0.36084
         * Z = (sqrt(3)/2*vb - 1.5*va)/Vdc = (2.1651 - 6.4952)/24 = -0.18042
         * sector 1: t1 = -Z = 0.18042, t2 = X = 0.18042, t0 = 0.63916
         * ta = t1+t2+t0/2 = 0.68000
         * tb = t2+t0/2    = 0.50000
         * tc = t0/2       = 0.31958                                */
        float va = VREF * cosf(deg2rad(30.0f));
        float vb = VREF * sinf(deg2rad(30.0f));
        float ta, tb, tc;
        (void)SVPWM_Compute(&sv, va, vb, &ta, &tb, &tc);
        CHECK(NEAR(ta, 0.68000f, 1e-3f), "duty: sector1 ta hand-checked");
        CHECK(NEAR(tb, 0.50000f, 1e-3f), "duty: sector1 tb hand-checked");
        CHECK(NEAR(tc, 0.31958f, 1e-3f), "duty: sector1 tc hand-checked");
        /* min/max injection keeps the max duty referenced to 1.0-ish:
         * ta is max, tc is min, tb is the middle -> ta-tb == tb-tc */
        CHECK(NEAR(ta - tb, tb - tc, 1e-3f),
              "duty: symmetric around midpoint (linear region)");
    }

    /* --- overmodulation: duties stay bounded, vector projected --- */
    {
        float ta, tb, tc;
        /* amplitude 100 V >> half_dc 13.86: heavy saturation */
        (void)SVPWM_Compute(&sv, 100.0f, 0.0f, &ta, &tb, &tc);
        CHECK(ta >= 0.0f && ta <= 1.0f && tb >= 0.0f && tb <= 1.0f &&
              tc >= 0.0f && tc <= 1.0f,
              "overmod: duties clamped to [0,1]");
    }

    /* --- bus voltage update scales duties inversely --- */
    {
        float ta1, tb1, tc1, ta2, tb2, tc2;
        /* (va,vb)=(3,2) sits inside sector 1 (not on a boundary),
         * so the active-vector duty responds to Vdc scaling */
        (void)SVPWM_Compute(&sv, 3.0f, 2.0f, &ta1, &tb1, &tc1);
        (void)SVPWM_SetBusVoltage(&sv, 2.0f * VDC);
        (void)SVPWM_Compute(&sv, 3.0f, 2.0f, &ta2, &tb2, &tc2);
        /* same vector at double bus voltage -> smaller modulation index */
        CHECK(ta2 < ta1, "vdc: doubling bus voltage shrinks duty demand");
        CHECK(SVPWM_SetBusVoltage(&sv, 0.0f) == SVPWM_ERR_PARAM,
              "vdc: zero bus voltage rejected");
        CHECK(SVPWM_SetBusVoltage(NULL, 12.0f) == SVPWM_ERR_PARAM,
              "vdc: NULL handle rejected");
    }

    /* --- compute validation --- */
    {
        float ta, tb, tc;
        CHECK(SVPWM_Compute(NULL, 0.0f, 0.0f, &ta, &tb, &tc) == SVPWM_ERR_PARAM,
              "compute: NULL handle rejected");
        CHECK(SVPWM_Compute(&sv, 0.0f, 0.0f, NULL, &tb, &tc) == SVPWM_ERR_PARAM,
              "compute: NULL output rejected");
    }

    /* --- sector query on un-inited handle --- */
    {
        SVPWM_Handle_t bad;
        memset(&bad, 0, sizeof(bad));
        bad.inited = false;
        CHECK(SVPWM_GetSector(&bad) == 0u, "state: un-inited sector reads 0");
    }

    printf("Summary: %d checks, %d passed, %d failed\n", g_total, g_pass, g_fail);
    return (g_fail == 0) ? 0 : 1;
}
