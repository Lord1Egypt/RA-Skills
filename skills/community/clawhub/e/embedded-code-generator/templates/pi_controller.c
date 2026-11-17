/**
 * @file pi_controller.c
 * @brief Position-form PI controller implementation with anti-windup.
 *
 * Anti-windup strategy: conditional integration (clamping).
 * When the output saturates AND the error would drive the integral
 * further into saturation, integration is paused. This prevents
 * integral windup without requiring a back-calculation factor.
 *
 * @note For the Q16 version, multiplication of two Q16.16 values
 *       produces a Q32.32 result which is shifted right by 16
 *       to obtain Q16.16. A 64-bit intermediate is used to avoid
 *       overflow when both operands are large.
 */

#include "pi_controller.h"
#include <stddef.h>  /* NULL */

/* ================================================================== */
/* Float implementation                                                */
/* ================================================================== */

#if !PI_USE_Q16

int PI_Init(PI_Handle_t *h, float kp, float ki, float ts,
            float out_min, float out_max, float i_min, float i_max)
{

    if (h == NULL) {
        return -1;
    }

    /* Parameter validation */
    if (ts <= 0.0f) {
        return -1;
    }
    if (out_min >= out_max) {
        return -1;
    }
    if (i_min >= i_max) {
        return -1;
    }

    h->Kp         = kp;
    h->Ki         = ki;
    h->Ts         = ts;
    h->out_min    = out_min;
    h->out_max    = out_max;
    h->i_min      = i_min;
    h->i_max      = i_max;
    h->integral   = 0.0f;
    h->prev_error = 0.0f;
    h->inited     = true;

    return 0;
}

float PI_Compute(PI_Handle_t *h, float error)
{
    float output;
    float p_term;
    float i_term;


    if (h == NULL || !h->inited) {
        return 0.0f;
    }

    /* Proportional term */
    p_term = h->Kp * error;

    /*
     * Anti-windup: conditional integration (clamping).
     *
     * Only integrate when:
     *   - Output is not saturated, OR
     *   - The error would move the output AWAY from the saturation limit.
     *
     * This is the standard clamping anti-windup method described by
     * Åström & Hägglund.
     */
    i_term = h->integral + h->Ki * error * h->Ts;

    /* Tentative unclamped output */
    output = p_term + i_term;

    if (output > h->out_max) {
        /* Output saturated high: only integrate if error is negative
         * (i.e., trying to bring output back down). */
        if (error < 0.0f) {
            h->integral = i_term;
        }
        output = h->out_max;
    } else if (output < h->out_min) {
        /* Output saturated low: only integrate if error is positive. */
        if (error > 0.0f) {
            h->integral = i_term;
        }
        output = h->out_min;
    } else {
        /* Not saturated — freely integrate. */
        h->integral = i_term;
    }

    /* Clamp integral to independent limits (belt-and-suspenders). */
    if (h->integral > h->i_max) {
        h->integral = h->i_max;
    } else if (h->integral < h->i_min) {
        h->integral = h->i_min;
    }

    h->prev_error = error;

    return output;
}

void PI_Reset(PI_Handle_t *h)
{

    if (h == NULL) {
        return;
    }

    h->integral   = 0.0f;
    h->prev_error = 0.0f;
}

int PI_SetTuning(PI_Handle_t *h, float kp, float ki)
{

    if (h == NULL) {
        return -1;
    }

    h->Kp = kp;
    h->Ki = ki;

    return 0;
}

#else /* PI_USE_Q16 */

/* ================================================================== */
/* Q16.16 Fixed-point implementation                                   */
/* ================================================================== */

/**
 * @brief Saturating Q16 multiply: (a * b) >> 16 with 64-bit intermediate.
 *
 * @param a First operand in Q16.16.
 * @param b Second operand in Q16.16.
 * @return Product in Q16.16, saturated to int32 range.
 */
static q16_t q16_mul(q16_t a, q16_t b)
{
    int64_t product = (int64_t)a * (int64_t)b;
    product >>= Q16_SHIFT;

    /* Saturate to int32 range */
    if (product > INT32_MAX) {
        product = INT32_MAX;
    } else if (product < INT32_MIN) {
        product = INT32_MIN;
    }

    return (q16_t)product;
}

/**
 * @brief Clamp a Q16 value to [lo, hi].
 */
static q16_t q16_clamp(q16_t val, q16_t lo, q16_t hi)
{
    if (val > hi) return hi;
    if (val < lo) return lo;
    return val;
}

int PI_Init(PI_Handle_t *h, q16_t kp, q16_t ki, q16_t ts,
            q16_t out_min, q16_t out_max, q16_t i_min, q16_t i_max)
{

    if (h == NULL) {
        return -1;
    }

    if (ts <= 0) {
        return -1;
    }
    if (out_min >= out_max) {
        return -1;
    }
    if (i_min >= i_max) {
        return -1;
    }

    h->Kp         = kp;
    h->Ki         = ki;
    h->Ts         = ts;
    h->out_min    = out_min;
    h->out_max    = out_max;
    h->i_min      = i_min;
    h->i_max      = i_max;
    h->integral   = 0;
    h->prev_error = 0;
    h->inited     = true;

    return 0;
}

q16_t PI_Compute(PI_Handle_t *h, q16_t error)
{
    q16_t p_term;
    q16_t i_term;
    q16_t output;


    if (h == NULL || !h->inited) {
        return 0;
    }

    p_term = q16_mul(h->Kp, error);

    /* integral += Ki * error * Ts */
    {
        q16_t ki_err   = q16_mul(h->Ki, error);
        q16_t ki_err_ts = q16_mul(ki_err, h->Ts);

        /* Check for overflow before addition */
        if ((ki_err_ts > 0) && (h->integral > INT32_MAX - ki_err_ts)) {
            i_term = INT32_MAX;
        } else if ((ki_err_ts < 0) && (h->integral < INT32_MIN - ki_err_ts)) {
            i_term = INT32_MIN;
        } else {
            i_term = h->integral + ki_err_ts;
        }
    }

    output = p_term + i_term;
    /* Overflow guard for p_term + i_term */
    if ((p_term > 0 && i_term > 0 && output < 0) ||
        (p_term < 0 && i_term < 0 && output > 0)) {
        output = (output < 0) ? INT32_MAX : INT32_MIN;
    }

    /* Anti-windup clamping */
    if (output > h->out_max) {
        if (error < 0) {
            h->integral = i_term;
        }
        output = h->out_max;
    } else if (output < h->out_min) {
        if (error > 0) {
            h->integral = i_term;
        }
        output = h->out_min;
    } else {
        h->integral = i_term;
    }

    h->integral = q16_clamp(h->integral, h->i_min, h->i_max);
    h->prev_error = error;

    return output;
}

void PI_Reset(PI_Handle_t *h)
{

    if (h == NULL) {
        return;
    }

    h->integral   = 0;
    h->prev_error = 0;
}

int PI_SetTuning(PI_Handle_t *h, q16_t kp, q16_t ki)
{

    if (h == NULL) {
        return -1;
    }

    h->Kp = kp;
    h->Ki = ki;

    return 0;
}

#endif /* PI_USE_Q16 */
