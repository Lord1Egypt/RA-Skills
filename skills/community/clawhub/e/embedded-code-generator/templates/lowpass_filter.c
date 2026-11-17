/**
 * @file lowpass_filter.c
 * @brief First-order IIR low-pass filter implementation.
 */

#include "lowpass_filter.h"
#include <stddef.h>  /* NULL */

#ifndef M_PI
#define M_PI  3.14159265358979323846f
#endif

/* ================================================================== */
/* Float implementation                                                */
/* ================================================================== */

#if !LPF_USE_Q16

int LPF_InitFreq(LPF_Handle_t *h, float fc, float ts)
{
    float omega_dt;


    if (h == NULL) {
        return -1;
    }
    if (fc <= 0.0f || ts <= 0.0f) {
        return -1;
    }

    /*
     * Nyquist check: fc must be less than fs/2.
     * Above Nyquist, the bilinear transform warps the frequency
     * response severely and the filter is unusable. Warn via
     * return code -2 (still initializes but caller should check).
     */
    if (fc >= 0.5f / ts) {
        return -1;  /* Above Nyquist — reject outright */
    }

    /*
     * Bilinear transform (pre-warped) for first-order LPF:
     *   alpha = omega*Ts / (1 + omega*Ts)
     * where omega = 2*pi*fc.
     *
     * For fc << fs, this is approximately alpha = 2*pi*fc*Ts.
     */
    omega_dt = 2.0f * M_PI * fc * ts;

    if (omega_dt <= 0.0f) {
        return -1;
    }

    h->alpha     = omega_dt / (1.0f + omega_dt);
    h->one_minus = 1.0f - h->alpha;
    h->y_prev    = 0.0f;
    h->fc        = fc;
    h->Ts        = ts;
    h->inited    = true;

    return 0;
}

int LPF_InitAlpha(LPF_Handle_t *h, float alpha)
{

    if (h == NULL) {
        return -1;
    }
    if (alpha <= 0.0f || alpha >= 1.0f) {
        return -1;
    }

    h->alpha     = alpha;
    h->one_minus = 1.0f - alpha;
    h->y_prev    = 0.0f;
    h->fc        = 0.0f;
    h->Ts        = 0.0f;
    h->inited    = true;

    return 0;
}

float LPF_Update(LPF_Handle_t *h, float x)
{

    if (h == NULL || !h->inited) {
        return x;  /* Fail-safe: pass input through. */
    }

    /* y[n] = alpha * x[n] + (1 - alpha) * y[n-1] */
    h->y_prev = h->alpha * x + h->one_minus * h->y_prev;

    return h->y_prev;
}

void LPF_Reset(LPF_Handle_t *h)
{

    if (h == NULL) {
        return;
    }

    h->y_prev = 0.0f;
}

#else /* LPF_USE_Q16 */

/* ================================================================== */
/* Q16.16 Fixed-point implementation                                   */
/* ================================================================== */

static q16_t lpf_q16_mul(q16_t a, q16_t b)
{
    int64_t product = (int64_t)a * (int64_t)b;
    product >>= LPF_Q16_SHIFT;

    if (product > INT32_MAX) return (q16_t)INT32_MAX;
    if (product < INT32_MIN) return (q16_t)INT32_MIN;
    return (q16_t)product;
}

int LPF_InitFreq(LPF_Handle_t *h, q16_t fc, q16_t ts)
{
    /*
     * Q16 computation of alpha:
     *   omega_dt = 2*pi*fc*ts  (all in Q16.16)
     *   alpha = omega_dt / (Q16_ONE + omega_dt)
     *
     * To avoid overflow in the multiply, use 64-bit intermediates.
     */
    int64_t omega_dt;
    q16_t two_pi;

    if (h == NULL || fc <= 0 || ts <= 0) {
        return -1;
    }

    /* 2*pi in Q16.16 */
    two_pi = (q16_t)(2.0f * 3.14159265358979f * 65536.0f);

    /* omega_dt = (2*pi * fc * ts) >> 16, using 64-bit to avoid overflow */
    omega_dt = ((int64_t)two_pi * (int64_t)fc) >> LPF_Q16_SHIFT;
    omega_dt = (omega_dt * (int64_t)ts) >> LPF_Q16_SHIFT;

    if (omega_dt <= 0) {
        return -1;
    }

    /* alpha = omega_dt / (Q16_ONE + omega_dt) — all in Q16 domain */
    h->alpha = (q16_t)((omega_dt << LPF_Q16_SHIFT) / ((int64_t)(1 << LPF_Q16_SHIFT) + omega_dt));

    /* Clamp alpha to valid range (0, 1) in Q16 */
    if (h->alpha >= (1 << LPF_Q16_SHIFT)) {
        h->alpha = (1 << LPF_Q16_SHIFT) - 1;
    }
    if (h->alpha <= 0) {
        h->alpha = 1;
    }

    h->one_minus = (1 << LPF_Q16_SHIFT) - h->alpha;
    h->y_prev    = 0;
    h->fc        = fc;
    h->Ts        = ts;
    h->inited    = true;

    return 0;
}

int LPF_InitAlpha(LPF_Handle_t *h, q16_t alpha)
{
    if (h == NULL) {
        return -1;
    }
    if (alpha <= 0 || alpha >= (1 << LPF_Q16_SHIFT)) {
        return -1;
    }

    h->alpha     = alpha;
    h->one_minus = (1 << LPF_Q16_SHIFT) - alpha;
    h->y_prev    = 0;
    h->fc        = 0;
    h->Ts        = 0;
    h->inited    = true;

    return 0;
}

q16_t LPF_Update(LPF_Handle_t *h, q16_t x)
{
    q16_t term1, term2;

    if (h == NULL || !h->inited) {
        return x;
    }

    /* y = alpha*x + (1-alpha)*y_prev */
    term1 = lpf_q16_mul(h->alpha, x);
    term2 = lpf_q16_mul(h->one_minus, h->y_prev);

    h->y_prev = term1 + term2;

    return h->y_prev;
}

void LPF_Reset(LPF_Handle_t *h)
{
    if (h == NULL) {
        return;
    }
    h->y_prev = 0;
}

#endif /* LPF_USE_Q16 */
