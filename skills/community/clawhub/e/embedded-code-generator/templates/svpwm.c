/**
 * @file svpwm.c
 * @brief Seven-segment SVPWM implementation.
 *
 * Reference:
 *   - "Modern Power Electronics and AC Drives", Bimal K. Bose
 *   - AN1078 "Sensorless Field Oriented Control" (Microchip)
 *
 * The seven-segment sequence for one PWM period (center-aligned):
 *   V0 -> V_k -> V_(k+1) -> V7 -> V_(k+1) -> V_k -> V0
 *   T0/2   T1/2     T2/2    T0    T2/2      T1/2   T0/2
 *
 * This minimizes switching transitions (each phase switches once
 * per half-period) and produces the lowest harmonic distortion.
 */

#include "svpwm.h"
#include <stddef.h>  /* NULL */

/* ================================================================== */
/* Public API                                                          */
/* ================================================================== */

int SVPWM_Init(SVPWM_Handle_t *h, float vdc, float pwm_period)
{

    if (h == NULL) {
        return SVPWM_ERR_PARAM;
    }

    if (vdc <= 0.0f || pwm_period <= 0.0f) {
        return SVPWM_ERR_PARAM;
    }

    h->vdc     = vdc;
    h->t_pwm   = pwm_period;
    /*
     * Maximum phase voltage for sinusoidal SVPWM is Vdc/sqrt(3).
     * This is the radius of the inscribed circle in the hexagon.
     */
    h->half_dc = vdc * SVPWM_INV_SQRT3;
    h->sector  = 0u;
    h->inited  = true;

    return SVPWM_OK;
}

int SVPWM_SetBusVoltage(SVPWM_Handle_t *h, float vdc)
{

    if (h == NULL) {
        return SVPWM_ERR_PARAM;
    }
    if (vdc <= 0.0f) {
        return SVPWM_ERR_PARAM;
    }

    h->vdc     = vdc;
    h->half_dc = vdc * SVPWM_INV_SQRT3;

    return SVPWM_OK;
}

uint8_t SVPWM_GetSector(const SVPWM_Handle_t *h)
{

    if (h == NULL) {
        return 0u;
    }
    return h->sector;
}

int SVPWM_Compute(SVPWM_Handle_t *h,
                  float valpha, float vbeta,
                  float *ta, float *tb, float *tc)
{
    float t1, t2, t0;
    float ta_tmp, tb_tmp, tc_tmp;
    float x, y, z;
    uint8_t sector;


    if (h == NULL || !h->inited || ta == NULL || tb == NULL || tc == NULL) {
        return SVPWM_ERR_PARAM;
    }

    /*
     * Sector determination using the standard three-comparator method.
     *
     * Compute:
     *   Vref1 = Vbeta
     *   Vref2 = (sqrt(3)*Valpha - Vbeta) / 2
     *   Vref3 = (-sqrt(3)*Valpha - Vbeta) / 2
     *
     * Then:
     *   N = sign(Vref1) + 2*sign(Vref2) + 4*sign(Vref3)
     *   N maps to sector via lookup table.
     */
    x = vbeta;
    y = (SVPWM_SQRT3 * valpha - vbeta) * 0.5f;
    z = (-SVPWM_SQRT3 * valpha - vbeta) * 0.5f;

    {
        uint8_t a = (x > 0.0f) ? 1u : 0u;
        uint8_t b = (y > 0.0f) ? 1u : 0u;
        uint8_t c = (z > 0.0f) ? 1u : 0u;
        uint8_t n = (uint8_t)(a + 2u * b + 4u * c);

        /* N-to-sector mapping (1-indexed) */
        switch (n) {
            case 1:  sector = 2u; break;
            case 2:  sector = 6u; break;
            case 3:  sector = 1u; break;
            case 4:  sector = 4u; break;
            case 5:  sector = 3u; break;
            case 6:  sector = 5u; break;
            default: sector = 1u; break;
        }
    }
    h->sector = sector;

    /*
     * Compute dwell times using the standard X/Y/Z intermediate
     * variables (normalized to PWM period Ts):
     *
     *   X = sqrt(3) * Vbeta / Vdc
     *   Y = (sqrt(3)/2 * Vbeta + 3/2 * Valpha) / Vdc
     *   Z = (sqrt(3)/2 * Vbeta - 3/2 * Valpha) / Vdc
     *
     * Sector → (T1, T2) mapping:
     *   1: (-Z,  X)   2: ( Y, -Z)   3: ( X,  Y)
     *   4: ( Z, -X)   5: (-Y,  Z)   6: (-X, -Y)
     *
     * Reference: Microchip AN1078, TI InstaSPIN User Guide.
     */
    {
        float X = SVPWM_SQRT3 * vbeta / h->vdc;
        float Y = (SVPWM_SQRT3 * 0.5f * vbeta + 1.5f * valpha) / h->vdc;
        float Z = (SVPWM_SQRT3 * 0.5f * vbeta - 1.5f * valpha) / h->vdc;

        switch (sector) {
            case 1u:
                t1 = -Z;
                t2 =  X;
                break;
            case 2u:
                t1 =  Y;
                t2 = -Z;
                break;
            case 3u:
                t1 =  X;
                t2 =  Y;
                break;
            case 4u:
                t1 =  Z;
                t2 = -X;
                break;
            case 5u:
                t1 = -Y;
                t2 =  Z;
                break;
            case 6u:
            default:
                t1 = -X;
                t2 = -Y;
                break;
        }
    }

    /*
     * Overmodulation handling.
     *
     * If T1 + T2 > 1 (normalized PWM period), the reference vector
     * exceeds the hexagon boundary. Scale both times proportionally
     * so they fit, effectively projecting the reference onto the
     * hexagon. This is the simplest overmodulation strategy (Mode I).
     *
     * For a smooth transition to six-step, a more sophisticated
     * overmodulation algorithm (Mode II) can be implemented, but
     * this linear projection is sufficient for most FOC applications
     * and avoids discontinuities in the output voltage.
     */
    if ((t1 + t2) > 1.0f) {
        float scale = 1.0f / (t1 + t2);
        t1 *= scale;
        t2 *= scale;
    }

    /* Clamp negative times (numerical safety). */
    if (t1 < 0.0f) t1 = 0.0f;
    if (t2 < 0.0f) t2 = 0.0f;

    t0 = 1.0f - t1 - t2;
    if (t0 < 0.0f) t0 = 0.0f;

    /*
     * Seven-segment duty cycle computation.
     *
     * For each sector, determine the compare values for the three
     * phases. The center-aligned PWM counter counts 0 -> PR -> 0.
     * The duty cycles (Ta, Tb, Tc) represent the fraction of the
     * period during which each phase is HIGH.
     *
     * The table below maps sector -> (CMPA, CMPB, CMPC) where:
     *   CMPA corresponds to phase A on-time fraction
     *   CMPB corresponds to phase B on-time fraction
     *   CMPC corresponds to phase C on-time fraction
     */
    switch (sector) {
        case 1u:
            ta_tmp = t1 + t2 + t0 * 0.5f;
            tb_tmp = t2 + t0 * 0.5f;
            tc_tmp = t0 * 0.5f;
            break;
        case 2u:
            ta_tmp = t1 + t0 * 0.5f;
            tb_tmp = t1 + t2 + t0 * 0.5f;
            tc_tmp = t0 * 0.5f;
            break;
        case 3u:
            ta_tmp = t0 * 0.5f;
            tb_tmp = t1 + t2 + t0 * 0.5f;
            tc_tmp = t2 + t0 * 0.5f;
            break;
        case 4u:
            ta_tmp = t0 * 0.5f;
            tb_tmp = t1 + t0 * 0.5f;
            tc_tmp = t1 + t2 + t0 * 0.5f;
            break;
        case 5u:
            ta_tmp = t2 + t0 * 0.5f;
            tb_tmp = t0 * 0.5f;
            tc_tmp = t1 + t2 + t0 * 0.5f;
            break;
        case 6u:
        default:
            ta_tmp = t1 + t2 + t0 * 0.5f;
            tb_tmp = t0 * 0.5f;
            tc_tmp = t1 + t0 * 0.5f;
            break;
    }

    /*
     * Neutral-point injection (min/max injection).
     *
     * The seven-segment duties are in [0, 1] but may not be centered.
     * Add a common-mode shift so that max→1 and min→0 (or both centered
     * around 0.5 when there is headroom). The shift is:
     *   v_shift = (1 - d_max - d_min) / 2
     * This increases the linear modulation range by ~15% compared to
     * sinusoidal PWM (the "bus utilization" benefit of SVPWM).
     */
    {
        float dmax, dmin, v_shift;

        dmax = ta_tmp;
        dmin = ta_tmp;

        if (tb_tmp > dmax) dmax = tb_tmp;
        if (tc_tmp > dmax) dmax = tc_tmp;
        if (tb_tmp < dmin) dmin = tb_tmp;
        if (tc_tmp < dmin) dmin = tc_tmp;

        v_shift = (1.0f - dmax - dmin) * 0.5f;

        ta_tmp += v_shift;
        tb_tmp += v_shift;
        tc_tmp += v_shift;
    }

    /*
     * Clamp to [0, 1]. After neutral-point injection, the values
     * should already be in range, but clamp for safety against
     * numerical errors, especially near the overmodulation boundary.
     */
    if (ta_tmp < 0.0f) ta_tmp = 0.0f;
    if (ta_tmp > 1.0f) ta_tmp = 1.0f;
    if (tb_tmp < 0.0f) tb_tmp = 0.0f;
    if (tb_tmp > 1.0f) tb_tmp = 1.0f;
    if (tc_tmp < 0.0f) tc_tmp = 0.0f;
    if (tc_tmp > 1.0f) tc_tmp = 1.0f;

    *ta = ta_tmp;
    *tb = tb_tmp;
    *tc = tc_tmp;

    return SVPWM_OK;
}
