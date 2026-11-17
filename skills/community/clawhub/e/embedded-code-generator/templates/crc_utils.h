/**
 * @file crc_utils.h
 * @brief CRC-8, CRC-16/MODBUS, and CRC-16/CCITT checksum utilities.
 *
 * Provides both bit-by-bit and table-driven implementations.
 * Define CRC_USE_TABLE before including to use lookup tables
 * (faster, but uses 256 bytes of flash per CRC variant used).
 *
 * Supported algorithms:
 *   - CRC-8/MAXIM (normal poly 0x31 / reflected 0x8C, init 0x00, refIn/refOut=true, xorOut 0x00)
 *   - CRC-16/MODBUS (poly 0xA001, init 0xFFFF, refIn/refOut=true, xorOut 0x00)
 *   - CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF, refIn/refOut=false, xorOut 0x00)
 *
 * Verification test vectors:
 @verbatim
   CRC-8/MAXIM (Dallas/1-Wire):
     "123456789"  -> 0xA1   (standard check value)
     {0x01,0x02}  -> 0x78   (example for custom data)

   CRC-16/MODBUS:
     "123456789"  -> 0x4B37
     Modbus RTU frame example:
       Slave=0x01, Func=0x03, Addr=0x0000, Qty=0x0001
       Request:  01 03 00 00 00 01 84 0A
       CRC of [01 03 00 00 00 01] = 0x0A84 -> stored as 84 0A (little-endian)

   CRC-16/CCITT-FALSE:
     "123456789"  -> 0x29B1
 @endverbatim
 *
 * Usage example:
 * @code
 *   uint8_t data[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x01};
 *   uint16_t crc = CRC16_Modbus_Calculate(data, sizeof(data));
 *   // Append crc low-byte then high-byte for Modbus RTU:
 *   frame[6] = (uint8_t)(crc & 0xFF);
 *   frame[7] = (uint8_t)(crc >> 8);
 * @endcode
 */

#ifndef CRC_UTILS_H
#define CRC_UTILS_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration                                                       */
/* ------------------------------------------------------------------ */

/**
 * @brief Define CRC_USE_TABLE to use 256-entry lookup tables.
 *
 * Table-driven CRC is roughly 8x faster but consumes:
 *   - 256 bytes for CRC-8 table
 *   - 512 bytes for CRC-16 tables
 */
#ifdef CRC_USE_TABLE
#undef CRC_USE_TABLE
#define CRC_USE_TABLE  1
#else
#define CRC_USE_TABLE  0
#endif

/* ------------------------------------------------------------------ */
/* CRC-8                                                               */
/* ------------------------------------------------------------------ */

/**
 * @brief Calculate CRC-8/MAXIM (Dallas/1-Wire) checksum.
 *
 * Polynomial: 0x31 normal / 0x8C reflected (x^8 + x^5 + x^4 + 1)
 * Initial:    0x00
 * Reflected:  Yes (input and output)
 * XOR out:    0x00
 *
 * Standard check value: CRC8_Calculate((uint8_t*)"123456789", 9) == 0xA1.
 *
 * @param data Pointer to data buffer.
 * @param len  Length of data in bytes.
 * @return CRC-8/MAXIM value.
 */
uint8_t CRC8_Calculate(const uint8_t *data, size_t len);

/* ------------------------------------------------------------------ */
/* CRC-16/MODBUS                                                       */
/* ------------------------------------------------------------------ */

/**
 * @brief Calculate CRC-16/MODBUS.
 *
 * Polynomial: 0xA001 (reflected 0x8005)
 * Initial:    0xFFFF
 * Reflected:  Yes
 * XOR out:    0x0000
 *
 * This is the CRC used by Modbus RTU over RS485.
 *
 * @param data Pointer to data buffer.
 * @param len  Length of data in bytes.
 * @return CRC-16/MODBUS value.
 */
uint16_t CRC16_Modbus_Calculate(const uint8_t *data, size_t len);

/* ------------------------------------------------------------------ */
/* CRC-16/CCITT-FALSE                                                  */
/* ------------------------------------------------------------------ */

/**
 * @brief Calculate CRC-16/CCITT-FALSE.
 *
 * Polynomial: 0x1021
 * Initial:    0xFFFF
 * Reflected:  No
 * XOR out:    0x0000
 *
 * Used by XMODEM, Kermit (variant), and many legacy protocols.
 *
 * @param data Pointer to data buffer.
 * @param len  Length of data in bytes.
 * @return CRC-16/CCITT-FALSE value.
 */
uint16_t CRC16_CCITT_Calculate(const uint8_t *data, size_t len);

#ifdef __cplusplus
}
#endif

#endif /* CRC_UTILS_H */
