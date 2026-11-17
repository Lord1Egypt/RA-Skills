/**
 * @file adc_avg_filter.h
 * @brief Stateless ADC averaging filter: collect N samples and compute
 *        either a plain mean or a min/max-trimmed mean.
 *
 * Design: Pure functions over a caller-provided sample buffer — no static
 * state, so every call with the same input sequence yields the same result
 * (idempotent), and the module is trivially re-entrant across ADC channels.
 *
 * Overflow safety: the accumulator is uint32_t. Worst case for a 16-bit
 * ADC is 255 samples x 65535 = 16,711,425 < 2^32, so the sum can never
 * wrap. (A uint16_t accumulator would wrap at 4 samples of full scale.)
 *
 * Trimmed mean: drops exactly one highest and one lowest sample before
 * averaging (requires n >= 3). This rejects single-sample glitches
 * (Switching noise spikes, ESD hits) that a plain mean would smear into
 * the result.
 *
 * Usage example:
 * @code
 *   uint16_t raw[16];
 *   uint16_t filtered;
 *
 *   // One call: collect 16 samples, drop min/max, average the rest
 *   if (ADCF_Filter(App_AdcRead, raw, 16u, &filtered) == ADCF_OK) {
 *       UseMeasurement(filtered);
 *   }
 * @endcode
 *
 * @note ADCF_Filter() blocks for n conversion times. For slow ADCs call
 *       it from a task, not an ISR; the read callback is free to read a
 *       hardware register or trigger-and-wait.
 * @note Drop window is fixed at one sample per side. For heavier noise
 *       rejection increase n, or chain ADCF_TrimmedMean over a sorted copy.
 */

#ifndef ADC_AVG_FILTER_H
#define ADC_AVG_FILTER_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Maximum supported sample count (uint8_t range with room for checks). */
#define ADCF_MAX_SAMPLES   255u

#ifndef ADCF_NASSERT
#include <assert.h>
#define ADCF_ASSERT(x)  assert(x)
#else
#define ADCF_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define ADCF_OK           0    /**< Operation succeeded.                  */
#define ADCF_ERR_PARAM   -1    /**< Invalid argument (NULL, n == 0/n > max, trimmed with n < 3). */

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/**
 * @brief Raw sample source callback.
 *
 * Must perform (or trigger and await) one ADC conversion and return the
 * raw result. Called exactly n times per ADCF_Collect() / ADCF_Filter().
 */
typedef uint16_t (*ADCF_ReadFn)(void);

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Collect n raw samples into buf via the read callback.
 *
 * @param read_fn  Sample source (must not be NULL).
 * @param buf      Output buffer (must not be NULL), at least n elements.
 * @param n        Sample count (1..ADCF_MAX_SAMPLES).
 * @return ADCF_OK or ADCF_ERR_PARAM.
 */
int ADCF_Collect(ADCF_ReadFn read_fn, uint16_t *buf, uint8_t n);

/**
 * @brief Plain arithmetic mean with rounding: (sum + n/2) / n.
 *
 * @param buf  Sample buffer (must not be NULL).
 * @param n    Sample count (>= 1).
 * @param out  Output: mean value.
 * @return ADCF_OK or ADCF_ERR_PARAM.
 */
int ADCF_Mean(const uint16_t *buf, uint8_t n, uint16_t *out);

/**
 * @brief Min/max-trimmed mean: drops one highest and one lowest sample,
 *        then averages the remaining (n-2) with rounding.
 *
 * @param buf  Sample buffer (must not be NULL).
 * @param n    Sample count (>= 3).
 * @param out  Output: trimmed mean value.
 * @return ADCF_OK or ADCF_ERR_PARAM.
 */
int ADCF_TrimmedMean(const uint16_t *buf, uint8_t n, uint16_t *out);

/**
 * @brief One-shot filter: collect n samples, then trimmed mean.
 *
 * Convenience equivalent of ADCF_Collect() + ADCF_TrimmedMean().
 *
 * @param read_fn  Sample source (must not be NULL).
 * @param buf      Scratch buffer (must not be NULL), at least n elements.
 * @param n        Sample count (3..ADCF_MAX_SAMPLES).
 * @param out      Output: filtered value.
 * @return ADCF_OK or ADCF_ERR_PARAM.
 */
int ADCF_Filter(ADCF_ReadFn read_fn, uint16_t *buf, uint8_t n, uint16_t *out);

#ifdef __cplusplus
}
#endif

#endif /* ADC_AVG_FILTER_H */
