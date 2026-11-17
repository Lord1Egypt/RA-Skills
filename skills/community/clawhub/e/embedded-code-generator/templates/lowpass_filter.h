/**
 * @file lowpass_filter.h
 * @brief First-order IIR low-pass filter.
 *
 * Difference equation:
 *   y[n] = alpha * x[n] + (1 - alpha) * y[n-1]
 *
 * Two initialization methods:
 *   1. LPF_InitFreq()  — specify cutoff frequency fc and sample time Ts;
 *                        alpha is computed automatically.
 *   2. LPF_InitAlpha() — specify alpha directly.
 *
 * Alpha computation from fc and Ts (pre-warped bilinear transform):
 *   alpha = 1 / (1 + 1 / (2*pi*fc*Ts))
 *
 * Alternatively, the simple RC approximation:
 *   alpha = Ts / (RC + Ts), where RC = 1/(2*pi*fc)
 *
 * Both forms produce nearly identical results when fc << fs.
 *
 * @note The cutoff frequency fc should be at least 10x lower than the
 *       sampling frequency fs (fc < fs/10). If fc approaches fs/2
 *       (Nyquist), the bilinear transform introduces significant
 *       frequency warping and the filter response becomes inaccurate.
 *
 * A Q16.16 fixed-point version is available by defining LPF_USE_Q16.
 *
 * Usage example:
 * @code
 *   static LPF_Handle_t lpf_current;
 *
 *   void ADC_Init(void) {
 *       // 200 Hz cutoff, 1 kHz sample rate
 *       LPF_InitFreq(&lpf_current, 200.0f, 0.001f);
 *   }
 *
 *   // Called every 1 ms
 *   float FilterCurrent(float raw_adc) {
 *       return LPF_Update(&lpf_current, raw_adc);
 *   }
 * @endcode
 */

#ifndef LOWPASS_FILTER_H
#define LOWPASS_FILTER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

#ifdef LPF_USE_Q16
#undef LPF_USE_Q16
#define LPF_USE_Q16  1
#else
#define LPF_USE_Q16  0
#endif

#ifndef LPF_NASSERT
#include <assert.h>
#define LPF_ASSERT(x)  assert(x)
#else
#define LPF_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Float API                                                           */
/* ------------------------------------------------------------------ */

#if !LPF_USE_Q16

/**
 * @brief First-order low-pass filter state (float version).
 */
typedef struct {
    float alpha;       /**< Filter coefficient (0 < alpha < 1).       */
    float one_minus;   /**< 1 - alpha, precomputed for efficiency.    */
    float y_prev;      /**< Previous output y[n-1].                   */
    float fc;          /**< Cutoff frequency in Hz (for reference).   */
    float Ts;          /**< Sample time in seconds (for reference).   */
    bool  inited;      /**< Initialization flag.                      */
} LPF_Handle_t;

/**
 * @brief Initialize filter from cutoff frequency and sample time.
 *
 * Computes alpha using the bilinear transform approximation:
 *   alpha = 2*pi*fc*Ts / (1 + 2*pi*fc*Ts)
 *
 * @param h  Pointer to filter handle.
 * @param fc Cutoff frequency in Hz (must be > 0).
 * @param ts Sample time in seconds (must be > 0).
 * @return 0 on success, -1 on invalid parameter.
 */
int LPF_InitFreq(LPF_Handle_t *h, float fc, float ts);

/**
 * @brief Initialize filter with an explicit alpha value.
 *
 * @param h     Pointer to filter handle.
 * @param alpha Filter coefficient (must be > 0 and < 1).
 *              Smaller alpha = heavier filtering (lower cutoff).
 * @return 0 on success, -1 on invalid parameter.
 */
int LPF_InitAlpha(LPF_Handle_t *h, float alpha);

/**
 * @brief Process one input sample and return the filtered output.
 *
 * @param h Pointer to filter handle.
 * @param x New input sample x[n].
 * @return Filtered output y[n].
 */
float LPF_Update(LPF_Handle_t *h, float x);

/**
 * @brief Reset the filter state (y[n-1] = 0).
 *
 * @param h Pointer to filter handle.
 */
void LPF_Reset(LPF_Handle_t *h);

#else

/* ------------------------------------------------------------------ */
/* Q16.16 Fixed-point API                                              */
/* ------------------------------------------------------------------ */

typedef int32_t q16_t;

#define LPF_Q16_SHIFT  16

typedef struct {
    q16_t alpha;       /**< Alpha in Q16.16.                         */
    q16_t one_minus;   /**< (1 - alpha) in Q16.16.                   */
    q16_t y_prev;      /**< Previous output in Q16.16.               */
    q16_t fc;          /**< Cutoff freq in Q16.16 (reference).       */
    q16_t Ts;          /**< Sample time in Q16.16 (reference).       */
    bool  inited;
} LPF_Handle_t;

int   LPF_InitFreq(LPF_Handle_t *h, q16_t fc, q16_t ts);
int   LPF_InitAlpha(LPF_Handle_t *h, q16_t alpha);
q16_t LPF_Update(LPF_Handle_t *h, q16_t x);
void  LPF_Reset(LPF_Handle_t *h);

#endif /* LPF_USE_Q16 */

#ifdef __cplusplus
}
#endif

#endif /* LOWPASS_FILTER_H */
