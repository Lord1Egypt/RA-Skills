/**
 * @file soft_i2c.h
 * @brief Bit-banged software I2C master (open-drain GPIO emulation).
 *
 * Design: Two-wire multi-drop bus emulated with open-drain semantics.
 *   - Releasing a line means driving it high (write 1); the pull-up or
 *     the slave then defines the actual level (wired-AND).
 *   - Clock stretching is respected by polling SCL before every edge
 *     (configurable via SI2C_WAIT_SCL_HIGH, can be disabled to save pins).
 *
 * Hook model (weak defaults provided in soft_i2c.c, override in app):
 *   - SI2C_SCL_Write(level)  drive SCL (0 = low, 1 = release/high)
 *   - SI2C_SCL_Read()        sample SCL (0/1), used for clock stretching
 *   - SI2C_SDA_Write(level)  drive SDA (0 = low, 1 = release/high)
 *   - SI2C_SDA_Read()        sample SDA line (0/1)
 *   - SI2C_DelayHalfBit()    half-bit delay, sets bus speed
 *
 * Protocol scope (single-byte primitives + one convenience helper):
 *   - SI2C_Start()       START condition (SDA falling while SCL high)
 *   - SI2C_Stop()        STOP condition  (SDA rising while SCL high)
 *   - SI2C_WriteByte()   clock out 8 bits, sample slave ACK (9th bit)
 *   - SI2C_ReadByte()    clock in 8 bits, drive ACK/NACK (9th bit)
 *   - SI2C_WriteThenRead() START -> addr+W -> reg -> RESTART ->
 *                        addr+R -> read N-1 with ACK, last with NACK -> STOP
 *                        (standard EEPROM / sensor register read pattern)
 *
 * Usage example:
 * @code
 *   uint8_t who_am_i = 0;
 *   if (SI2C_Init(100000u) == SI2C_OK) {
 *       // Read WHO_AM_I (reg 0x0F) from 7-bit address 0x6B (LSM6DSL)
 *       if (SI2C_WriteThenRead(0x6Bu, 0x0Fu, &who_am_i, 1u) == SI2C_OK) {
 *           // who_am_i == 0x6A
 *       }
 *   }
 * @endcode
 *
 * @note 7-bit addressing only. SI2C_WriteByte()/SI2C_ReadByte() take the
 *       full address byte including the R/W bit; only SI2C_WriteThenRead()
 *       builds it internally from a 7-bit address.
 * @note Not ISR-safe: bit-banged timing is jitter-sensitive. Call from a
 *       single task context only.
 * @note On bus lockup (slave stuck driving SDA), a recovery sequence of
 *       9 SCL pulses + STOP is recommended in the application layer.
 */

#ifndef SOFT_I2C_H
#define SOFT_I2C_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Minimum supported bus frequency (Hz). */
#define SI2C_FREQ_MIN   1000u

/** Maximum supported bus frequency (Hz): standard/fast mode limit. */
#define SI2C_FREQ_MAX   400000u

/**
 * @brief Enable SCL clock-stretching wait (default on).
 * Define to 0 before including to disable (saves one GPIO read hook).
 */
#ifndef SI2C_WAIT_SCL
#define SI2C_WAIT_SCL   1
#endif

#ifndef SI2C_NASSERT
#include <assert.h>
#define SI2C_ASSERT(x)  assert(x)
#else
#define SI2C_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define SI2C_OK           0    /**< Operation succeeded.                  */
#define SI2C_ERR_PARAM   -1    /**< Invalid argument (NULL, addr > 0x7F). */
#define SI2C_ERR_FREQ    -2    /**< Requested bus frequency out of range. */
#define SI2C_ERR_NACK    -3    /**< Slave did not acknowledge.            */

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Validate and store bus configuration.
 *
 * @param bus_freq_hz  Target bus frequency (SI2C_FREQ_MIN..SI2C_FREQ_MAX).
 *                     The actual timing is produced by the application's
 *                     SI2C_DelayHalfBit() override; this value is stored
 *                     for reference and range checking.
 * @return SI2C_OK or SI2C_ERR_FREQ.
 */
int SI2C_Init(uint32_t bus_freq_hz);

/**
 * @brief Generate a START condition.
 *
 * Sequence: release SDA -> SCL high -> SDA falls while SCL high ->
 * SCL low (bus now owned by master).
 *
 * @return SI2C_OK.
 */
int SI2C_Start(void);

/**
 * @brief Generate a STOP condition and release the bus.
 *
 * Sequence: SDA low -> SCL high -> SDA rises while SCL high.
 * Safe to call after any byte phase; also used for error abort.
 *
 * @return SI2C_OK.
 */
int SI2C_Stop(void);

/**
 * @brief Clock out one byte, then sample the slave ACK bit.
 *
 * @param byte  Data or address byte (address bytes must already contain
 *              the R/W bit, e.g. (addr7 << 1) | 0u for write).
 * @return SI2C_OK on ACK, SI2C_ERR_NACK when the slave does not pull
 *         SDA low during the 9th clock.
 */
int SI2C_WriteByte(uint8_t byte);

/**
 * @brief Clock in one byte, then drive ACK (more bytes follow) or NACK.
 *
 * @param byte     Output: received byte.
 * @param ack      true  = drive ACK  (master will read more bytes),
 *                 false = drive NACK (last byte, release bus for master).
 * @return SI2C_OK or SI2C_ERR_PARAM (byte == NULL).
 */
int SI2C_ReadByte(uint8_t *byte, bool ack);

/**
 * @brief Convenience transaction: write register address, then read data.
 *
 * START, addr+W, reg, repeated START, addr+R, (len-1) bytes with ACK,
 * last byte with NACK, STOP. Aborts with STOP on any NACK.
 *
 * @param addr7  7-bit slave address (0x00..0x7F).
 * @param reg    Register / memory address byte to write first.
 * @param data   Output buffer for read data (must not be NULL).
 * @param len    Number of bytes to read (> 0).
 * @return SI2C_OK, SI2C_ERR_PARAM, or SI2C_ERR_NACK.
 */
int SI2C_WriteThenRead(uint8_t addr7, uint8_t reg,
                       uint8_t *data, uint16_t len);

/**
 * @brief Get the bus frequency passed to SI2C_Init().
 */
uint32_t SI2C_GetFreq(void);

#ifdef __cplusplus
}
#endif

#endif /* SOFT_I2C_H */
