/**
 * @file adc_avg_filter.c
 * @brief Stateless ADC averaging filter (plain and min/max-trimmed mean).
 *
 * The accumulator is deliberately uint32_t: 255 samples of a full-scale
 * 16-bit ADC sum to 16,711,425, which fits comfortably in 32 bits. With a
 * uint16_t accumulator the same sum would wrap after ~4 samples.
 */

#include "adc_avg_filter.h"

/* ------------------------------------------------------------------ */
/* Public API                                                          */
/* ------------------------------------------------------------------ */

int ADCF_Collect(ADCF_ReadFn read_fn, uint16_t *buf, uint8_t n)
{
    uint8_t i;

    if ((read_fn == NULL) || (buf == NULL) ||
        (n == 0u))   /* uint8_t n can never exceed ADCF_MAX_SAMPLES */
    {
        return ADCF_ERR_PARAM;
    }

    for (i = 0u; i < n; i++)
    {
        buf[i] = read_fn();
    }

    return ADCF_OK;
}

int ADCF_Mean(const uint16_t *buf, uint8_t n, uint16_t *out)
{
    uint32_t sum = 0u;
    uint8_t  i;

    if ((buf == NULL) || (out == NULL) ||
        (n == 0u))   /* uint8_t n can never exceed ADCF_MAX_SAMPLES */
    {
        return ADCF_ERR_PARAM;
    }

    for (i = 0u; i < n; i++)
    {
        sum += buf[i];
    }

    /* Round-to-nearest: add half the divisor before dividing. */
    *out = (uint16_t)((sum + (uint32_t)(n / 2u)) / (uint32_t)n);
    return ADCF_OK;
}

int ADCF_TrimmedMean(const uint16_t *buf, uint8_t n, uint16_t *out)
{
    uint32_t sum = 0u;
    uint16_t min_val;
    uint16_t max_val;
    uint8_t  i;
    uint8_t  trim;      /* number of samples left after dropping 2 */
    bool     min_skipped = false;
    bool     max_skipped = false;

    if ((buf == NULL) || (out == NULL) ||
        (n < 3u))    /* uint8_t n can never exceed ADCF_MAX_SAMPLES */
    {
        return ADCF_ERR_PARAM;
    }

    /* Locate the single lowest and single highest sample. */
    min_val = buf[0];
    max_val = buf[0];
    for (i = 1u; i < n; i++)
    {
        if (buf[i] < min_val)
        {
            min_val = buf[i];
        }
        if (buf[i] > max_val)
        {
            max_val = buf[i];
        }
    }

    /* Sum everything except one occurrence of min and one of max. */
    for (i = 0u; i < n; i++)
    {
        if ((buf[i] == min_val) && !min_skipped)
        {
            min_skipped = true;      /* drop the lowest sample */
            continue;
        }
        if ((buf[i] == max_val) && !max_skipped)
        {
            max_skipped = true;      /* drop the highest sample */
            continue;
        }
        sum += buf[i];
    }

    trim = (uint8_t)(n - 2u);
    *out = (uint16_t)((sum + (uint32_t)(trim / 2u)) / (uint32_t)trim);
    return ADCF_OK;
}

int ADCF_Filter(ADCF_ReadFn read_fn, uint16_t *buf, uint8_t n, uint16_t *out)
{
    int rc;

    if ((read_fn == NULL) || (buf == NULL) || (out == NULL) ||
        (n < 3u))    /* uint8_t n can never exceed ADCF_MAX_SAMPLES */
    {
        return ADCF_ERR_PARAM;
    }

    rc = ADCF_Collect(read_fn, buf, n);
    if (rc != ADCF_OK)
    {
        return rc;
    }

    return ADCF_TrimmedMean(buf, n, out);
}
