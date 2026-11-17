/**
 * @file spi_master.h
 * @brief Bit-banged SPI master with full-duplex transfer, CS control and
 *        configurable mode 0-3 (CPOL/CPHA).
 *
 * Design: Classic 4-wire SPI (SCK / MOSI / MISO / CS). All four CPOL/CPHA
 * combinations are supported via a config struct; MSB-first or LSB-first
 * shift order is selectable. CS polarity is configurable (active low by
 * default) and is wrapped around every transaction.
 *
 * Timing (per bit, leading = first SCK edge of the bit, trailing = second):
 *   - CPHA = 0: MOSI is set while SCK is idle, data is sampled at the
 *     leading edge, MOSI changes again after the trailing edge.
 *   - CPHA = 1: MOSI changes at the leading edge, data is sampled at the
 *     trailing edge.
 *
 * Hook model (weak defaults provided in spi_master.c, override in app):
 *   - SPI_SCK_Write(level)   drive SCK (0/1)
 *   - SPI_MOSI_Write(level)  drive MOSI (0/1)
 *   - SPI_MISO_Read()        sample MISO (0/1)
 *   - SPI_CS_Write(asserted) drive CS: 1 = selected, 0 = deselected
 *                            (polarity handled inside the hook)
 *   - SPI_DelayHalf()        half SCK period delay, sets clock speed
 *
 * Usage example:
 * @code
 *   SPI_Config_t cfg = {
 *       .mode         = 0,     // CPOL=0 CPHA=0 (most common)
 *       .msb_first    = 1,
 *       .cs_active_low = 1,
 *   };
 *   uint8_t tx[3] = { 0x9Fu, 0x00u, 0x00u };   // JEDEC ID command
 *   uint8_t rx[3] = { 0 };
 *
 *   if (SPI_Init(&cfg) == SPI_OK) {
 *       SPI_Transaction(tx, rx, 3u);           // CS low, 3 bytes, CS high
 *       // rx now holds manufacturer / memory type / capacity
 *   }
 * @endcode
 *
 * @note Not ISR-safe: bit-banged timing is jitter-sensitive. Call from a
 *       single task context only.
 * @note Full-duplex: SPI_Transaction() clocks one byte per element. Pass
 *       rx = NULL for write-only, tx = NULL for read-only (0xFF dummy).
 */

#ifndef SPI_MASTER_H
#define SPI_MASTER_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

#define SPI_MODE_0   0   /**< CPOL=0, CPHA=0 (leading rising edge).  */
#define SPI_MODE_1   1   /**< CPOL=0, CPHA=1 (trailing rising edge). */
#define SPI_MODE_2   2   /**< CPOL=1, CPHA=0 (leading falling edge). */
#define SPI_MODE_3   3   /**< CPOL=1, CPHA=1 (trailing falling edge). */

#ifndef SPI_NASSERT
#include <assert.h>
#define SPI_ASSERT(x)  assert(x)
#else
#define SPI_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define SPI_OK           0    /**< Operation succeeded.               */
#define SPI_ERR_PARAM   -1    /**< Invalid argument (NULL, mode > 3). */

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/**
 * @brief SPI master configuration.
 */
typedef struct {
    uint8_t mode;           /**< SPI mode 0..3 (SPI_MODE_x).            */
    uint8_t msb_first;      /**< 1 = MSB first (default), 0 = LSB first.*/
    uint8_t cs_active_low;  /**< 1 = CS asserted low (default).         */
} SPI_Config_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Validate and apply the configuration; SCK returns to its idle
 *        level and CS is deasserted.
 *
 * @param cfg  Pointer to configuration (must not be NULL, mode <= 3).
 * @return SPI_OK or SPI_ERR_PARAM.
 */
int SPI_Init(const SPI_Config_t *cfg);

/**
 * @brief Full-duplex transfer of one byte (no CS control).
 *
 * Clocks 8 bits out on MOSI while simultaneously clocking 8 bits in
 * from MISO. Assert/deassert CS around it for a framed transaction,
 * or use SPI_Transaction().
 *
 * @param tx   Byte to transmit.
 * @param rx   Output: received byte (may be NULL to ignore).
 * @return SPI_OK.
 */
int SPI_Transfer(uint8_t tx, uint8_t *rx);

/**
 * @brief Framed transaction: assert CS, transfer len bytes, deassert CS.
 *
 * @param tx   Transmit buffer (NULL = transmit 0xFF dummies for reads).
 * @param rx   Receive buffer (NULL = discard received bytes for writes).
 * @param len  Number of bytes (> 0; tx and rx must not both be NULL).
 * @return SPI_OK or SPI_ERR_PARAM.
 */
int SPI_Transaction(const uint8_t *tx, uint8_t *rx, uint16_t len);

/**
 * @brief Read back the current configuration.
 *
 * @param cfg  Output: current configuration (must not be NULL).
 * @return SPI_OK or SPI_ERR_PARAM.
 */
int SPI_GetConfig(SPI_Config_t *cfg);

#ifdef __cplusplus
}
#endif

#endif /* SPI_MASTER_H */
