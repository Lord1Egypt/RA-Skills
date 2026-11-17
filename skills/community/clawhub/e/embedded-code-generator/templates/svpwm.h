/**
 * @file svpwm.h
 * @brief Space Vector PWM (SVPWM) for three-phase motor control.
 *
 * Implements the standard seven-segment SVPWM algorithm used in
 * Field-Oriented Control (FOC) of PMSM and BLDC motors.
 *
 * Inputs:  Valpha, Vbeta (Clarke-transform output voltage), Vdc (bus)
 * Outputs: Ta, Tb, Tc (three-phase duty cycles, range 0.0 ~ 1.0)
 *
 * The algorithm:
 *   1. Determine the sector (1..6) from Valpha and Vbeta.
 *   2. Calculate the active-vector dwell times T1, T2 and
 *      zero-vector time T0 = Tpwm - T1 - T2.
 *   3. Apply center-aligned (symmetric) PWM by distributing T0
 *      equally between V0 and V7 (seven-segment sequence).
 *   4. Add neutral-point (min/max) injection to center the duty
 *      cycles in [0, 1].
 *
 * Overmodulation: When T1 + T2 > Tpwm, the vectors are scaled back
 * proportionally to fit within the hexagon boundary. This provides
 * a smooth transition from linear to six-step operation.
 *
 * @note This module uses float. For MCUs without an FPU, consider
 *       the Q15/Q17 fixed-point version or the ARM CMSIS-DSP
 *       arm_svm_pwm_f32() function.
 *
 * Sector determination:
 * @code
 *   Sector 1: Vref in 0°  ~ 60°   (Vbeta > 0, Vbeta < sqrt(3)*Valpha)
 *   Sector 2: Vref in 60° ~ 120°  (Vbeta > 0, Vbeta > sqrt(3)*Valpha)
 *   Sector 3: Vref in 120°~ 180°  (Valpha < 0, Vbeta > -sqrt(3)*Valpha)
 *   Sector 4: Vref in 180°~ 240°  (Vbeta < 0, Vbeta > sqrt(3)*Valpha)
 *   Sector 5: Vref in 240°~ 300°  (Vbeta < 0, Vbeta < sqrt(3)*Valpha)
 *   Sector 6: Vref in 300°~ 360°  (Valpha > 0, Vbeta < -sqrt(3)*Valpha)
 * @endcode
 *
 * Usage example:
 * @code
 *   static SVPWM_Handle_t svpwm;
 *
 *   void FOC_Init(void) {
 *       SVPWM_Init(&svpwm, 24.0f, 1.0f);  // 24V bus, PWM period = 1.0 (normalized)
 *   }
 *
 *   void FOC_Loop(void) {
 *       float ta, tb, tc;
 *       SVPWM_Compute(&svpwm, valpha, vbeta, &ta, &tb, &tc);
 *       PWM_SetDuty(TIM1, 1, ta);
 *       PWM_SetDuty(TIM1, 2, tb);
 *       PWM_SetDuty(TIM1, 3, tc);
 *   }
 * @endcode
 */

#ifndef SVPWM_H
#define SVPWM_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration                                                       */
/* ------------------------------------------------------------------ */

#ifndef SVPWM_NASSERT
#include <assert.h>
#define SVPWM_ASSERT(x)  assert(x)
#else
#define SVPWM_ASSERT(x)  ((void)0)
#endif

/** sqrt(3) constant. */
#define SVPWM_SQRT3  1.7320508075688772f

/** 1/sqrt(3). */
#define SVPWM_INV_SQRT3  0.5773502691896258f

/** sqrt(3)/2. */
#define SVPWM_SQRT3_2  0.8660254037844386f

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define SVPWM_OK            0
#define SVPWM_ERR_PARAM    -1

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/**
 * @brief SVPWM state handle.
 */
typedef struct {
    float vdc;          /**< DC bus voltage in volts (must be > 0).      */
    float t_pwm;        /**< PWM period in seconds (for timing calc).    */
    float half_dc;      /**< Maximum phase voltage = Vdc / sqrt(3).      */
    uint8_t sector;     /**< Last computed sector (1..6, for debugging). */
    bool  inited;       /**< Initialization flag.                        */
} SVPWM_Handle_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Initialize the SVPWM module.
 *
 * @param h     Pointer to handle.
 * @param vdc   DC bus voltage in volts (must be > 0).
 * @param pwm_period PWM period in seconds (e.g., 0.0001 for 10 kHz).
 *                   This is used only for internal timing; duty cycles
 *                   are always output normalized to [0, 1].
 * @return SVPWM_OK or SVPWM_ERR_PARAM.
 */
int SVPWM_Init(SVPWM_Handle_t *h, float vdc, float pwm_period);

/**
 * @brief Compute SVPWM duty cycles.
 *
 * @param h      Pointer to handle.
 * @param valpha Alpha-axis voltage (from Clarke transform / PI output).
 * @param vbeta  Beta-axis voltage.
 * @param ta     Output: phase A duty cycle (0.0 ~ 1.0).
 * @param tb     Output: phase B duty cycle (0.0 ~ 1.0).
 * @param tc     Output: phase C duty cycle (0.0 ~ 1.0).
 * @return SVPWM_OK or SVPWM_ERR_PARAM.
 */
int SVPWM_Compute(SVPWM_Handle_t *h,
                  float valpha, float vbeta,
                  float *ta, float *tb, float *tc);

/**
 * @brief Update the bus voltage at runtime (e.g., from ADC measurement).
 *
 * @param h   Pointer to handle.
 * @param vdc New DC bus voltage in volts.
 * @return SVPWM_OK or SVPWM_ERR_PARAM.
 */
int SVPWM_SetBusVoltage(SVPWM_Handle_t *h, float vdc);

/**
 * @brief Get the last computed sector (for debugging / visualization).
 *
 * @param h Pointer to handle.
 * @return Sector number 1..6, or 0 if not initialized.
 */
uint8_t SVPWM_GetSector(const SVPWM_Handle_t *h);

#ifdef __cplusplus
}
#endif

#endif /* SVPWM_H */
