/**
 * @file pi_controller.h
 * @brief Position-form PI controller with anti-windup clamping.
 *
 * Provides a float implementation and an optional Q16 fixed-point implementation
 * (enable by defining PI_USE_Q16 before including this header).
 *
 * Discretization: Backward Euler (implicit) method.
 *   integral[n] = integral[n-1] + Ki * error * Ts
 *   output[n]   = Kp * error[n] + integral[n]
 *
 * @note The controller must be called at a fixed period Ts. Jitter in Ts
 *       degrades performance; use a hardware timer ISR for best results.
 *
 * Usage example:
 * @code
 *   static PI_Handle_t pi_speed;
 *
 *   void Motor_Init(void) {
 *       PI_Init(&pi_speed, 0.5f, 10.0f, 0.001f, -24.0f, 24.0f, -24.0f, 24.0f);
 *   }
 *
 *   // Called every 1 ms from timer ISR
 *   void Timer_ISR(void) {
 *       float error = target_rpm - actual_rpm;
 *       float output = PI_Compute(&pi_speed, error);
 *       Motor_SetVoltage(output);
 *   }
 * @endcode
 */

#ifndef PI_CONTROLLER_H
#define PI_CONTROLLER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/**
 * @brief Define this before including to use the Q16 fixed-point API
 *        instead of the float API.
 */
#ifdef PI_USE_Q16
#undef PI_USE_Q16
#define PI_USE_Q16  1
#else
#define PI_USE_Q16  0
#endif

/**
 * @brief Enable runtime assertion for null-pointer checks.
 *        Override by defining PI_NASSERT before including.
 */
#ifndef PI_NASSERT
#include <assert.h>
#define PI_ASSERT(x)  assert(x)
#else
#define PI_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Q16 fixed-point type                                                */
/* ------------------------------------------------------------------ */

#if PI_USE_Q16

/** Q16.16 signed fixed-point type (16 integer bits, 16 fractional bits). */
typedef int32_t q16_t;

#define Q16_SHIFT       16
#define Q16_ONE         (1 << Q16_SHIFT)

/** Convert float to Q16.16. */
static inline q16_t q16_from_float(float f) {
    return (q16_t)(f * 65536.0f);
}

/** Convert Q16.16 to float. */
static inline float q16_to_float(q16_t q) {
    return (float)q / 65536.0f;
}

#endif /* PI_USE_Q16 */

/* ------------------------------------------------------------------ */
/* Float API                                                           */
/* ------------------------------------------------------------------ */

#if !PI_USE_Q16

/**
 * @brief PI controller state structure (float version).
 *
 * All fields are private; access through the API functions only.
 */
typedef struct {
    float Kp;           /**< Proportional gain.                        */
    float Ki;           /**< Integral gain (per-second, NOT per-Ts).    */
    float Ts;           /**< Sample time in seconds.                    */
    float integral;     /**< Accumulated integral term.                 */
    float out_min;      /**< Output lower clamp.                        */
    float out_max;      /**< Output upper clamp.                        */
    float i_min;        /**< Integral lower clamp (anti-windup).        */
    float i_max;        /**< Integral upper clamp (anti-windup).        */
    float prev_error;   /**< Previous error (for diagnostics/tuning).   */
    bool  inited;       /**< Initialization flag.                       */
} PI_Handle_t;

/**
 * @brief Initialize a PI controller.
 *
 * @param h       Pointer to controller handle.
 * @param kp      Proportional gain.
 * @param ki      Integral gain (in units of 1/second).
 * @param ts      Sample / execution period in seconds (must be > 0).
 * @param out_min Minimum output value.
 * @param out_max Maximum output value.
 * @param i_min   Minimum integral value (set to out_min for clamping).
 * @param i_max   Maximum integral value (set to out_max for clamping).
 * @return 0 on success, -1 on invalid parameter.
 */
int PI_Init(PI_Handle_t *h, float kp, float ki, float ts,
            float out_min, float out_max, float i_min, float i_max);

/**
 * @brief Compute one PI iteration.
 *
 * Uses backward Euler discretization with conditional integration
 * anti-windup (clamping).
 *
 * @param h     Pointer to controller handle.
 * @param error Current error (setpoint - measurement).
 * @return Clamped controller output.
 */
float PI_Compute(PI_Handle_t *h, float error);

/**
 * @brief Reset the integral accumulator and previous error to zero.
 *
 * Call this when the controller is disabled or when the setpoint
 * changes abruptly to avoid integral windup during the transition.
 *
 * @param h Pointer to controller handle.
 */
void PI_Reset(PI_Handle_t *h);

/**
 * @brief Update Kp and Ki at runtime.
 *
 * The integral term is preserved; only gains change.
 *
 * @param h  Pointer to controller handle.
 * @param kp New proportional gain.
 * @param ki New integral gain.
 * @return 0 on success, -1 on invalid parameter.
 */
int PI_SetTuning(PI_Handle_t *h, float kp, float ki);

#else /* Q16 fixed-point version */

/* ------------------------------------------------------------------ */
/* Q16 Fixed-point API                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief PI controller state structure (Q16.16 fixed-point version).
 *
 * All gains and values are stored in Q16.16 format.
 * Use q16_from_float() / q16_to_float() for conversion.
 */
typedef struct {
    q16_t Kp;           /**< Proportional gain in Q16.16.              */
    q16_t Ki;           /**< Integral gain in Q16.16 (per-second).     */
    q16_t Ts;           /**< Sample time in Q16.16 (seconds).          */
    q16_t integral;     /**< Accumulated integral in Q16.16.           */
    q16_t out_min;      /**< Output lower clamp in Q16.16.             */
    q16_t out_max;      /**< Output upper clamp in Q16.16.             */
    q16_t i_min;        /**< Integral lower clamp in Q16.16.           */
    q16_t i_max;        /**< Integral upper clamp in Q16.16.           */
    q16_t prev_error;   /**< Previous error in Q16.16.                 */
    bool  inited;       /**< Initialization flag.                       */
} PI_Handle_t;

int   PI_Init(PI_Handle_t *h, q16_t kp, q16_t ki, q16_t ts,
              q16_t out_min, q16_t out_max, q16_t i_min, q16_t i_max);
q16_t PI_Compute(PI_Handle_t *h, q16_t error);
void  PI_Reset(PI_Handle_t *h);
int   PI_SetTuning(PI_Handle_t *h, q16_t kp, q16_t ki);

#endif /* PI_USE_Q16 */

#ifdef __cplusplus
}
#endif

#endif /* PI_CONTROLLER_H */
