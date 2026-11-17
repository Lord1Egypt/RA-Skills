/**
 * @file test_crc.c
 * @brief Self-check tests for crc_utils.c (bit-by-bit and table builds).
 *
 * Run via `make test` from the skill package root, or manually:
 *   gcc -std=c99 -Wall -Wextra -Iscripts/templates \
 *       tests/test_crc.c scripts/templates/crc_utils.c -o test_crc && ./test_crc
 *
 * Exit code: number of failed checks (0 = all pass).
 */

#include <stdio.h>
#include "crc_utils.h"

static int g_failed = 0;
static int g_total  = 0;

#define CHECK(desc, expr)                                          \
    do {                                                           \
        g_total++;                                                 \
        if (expr) {                                                \
            printf("[PASS] %s\n", (desc));                         \
        } else {                                                   \
            g_failed++;                                            \
            printf("[FAIL] %s  (at line %d)\n", (desc), __LINE__); \
        }                                                          \
    } while (0)

int main(void)
{
    static const uint8_t modbus_frame[] = { 0x01u, 0x03u, 0x00u, 0x00u, 0x00u, 0x01u };
    static const uint8_t two_bytes[]    = { 0x01u, 0x02u };
    const uint8_t *check9 = (const uint8_t *)"123456789"; /* length 9 */

    printf("[TEST] crc_utils (CRC_USE_TABLE=%d)\n", CRC_USE_TABLE);

    /* --- CRC-8/MAXIM (poly 0x31/0x8C, init 0x00, reflected) --- */
    CHECK("CRC-8 \"123456789\" == 0xA1 (standard check value)",
          CRC8_Calculate(check9, 9u) == 0xA1u);
    CHECK("CRC-8 {0x01,0x02} == 0x78 (template example vector)",
          CRC8_Calculate(two_bytes, sizeof(two_bytes)) == 0x78u);
    CHECK("CRC-8 empty input returns init 0x00",
          CRC8_Calculate(check9, 0u) == 0x00u);

    /* --- CRC-16/MODBUS (poly 0xA001, init 0xFFFF, reflected) --- */
    CHECK("CRC-16/MODBUS \"123456789\" == 0x4B37 (standard check value)",
          CRC16_Modbus_Calculate(check9, 9u) == 0x4B37u);
    CHECK("CRC-16/MODBUS {01 03 00 00 00 01} == 0x0A84 (Modbus RTU frame)",
          CRC16_Modbus_Calculate(modbus_frame, sizeof(modbus_frame)) == 0x0A84u);
    CHECK("CRC-16/MODBUS empty input returns init 0xFFFF",
          CRC16_Modbus_Calculate(check9, 0u) == 0xFFFFu);

    /* --- CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF, non-reflected) --- */
    /* NOTE: template implements CCITT-FALSE (init 0xFFFF), whose standard
     * check value is 0x29B1. (The XMODEM variant with init 0x0000 would
     * give 0x31C3 and does not apply to this template.) */
    CHECK("CRC-16/CCITT-FALSE \"123456789\" == 0x29B1 (standard check value)",
          CRC16_CCITT_Calculate(check9, 9u) == 0x29B1u);
    CHECK("CRC-16/CCITT-FALSE empty input returns init 0xFFFF",
          CRC16_CCITT_Calculate(check9, 0u) == 0xFFFFu);

    /* --- Template-defined NULL behavior: return 0 --- */
    CHECK("CRC-8 NULL data returns 0 (template-defined)",
          CRC8_Calculate(NULL, 5u) == 0x00u);
    CHECK("CRC-16/MODBUS NULL data returns 0 (template-defined)",
          CRC16_Modbus_Calculate(NULL, 5u) == 0x0000u);
    CHECK("CRC-16/CCITT NULL data returns 0 (template-defined)",
          CRC16_CCITT_Calculate(NULL, 5u) == 0x0000u);

    printf("Summary: %d checks, %d passed, %d failed\n",
           g_total, g_total - g_failed, g_failed);

    if (g_failed == 0) {
        printf("Result: ALL PASS\n");
    } else {
        printf("Result: FAIL\n");
    }

    return g_failed;
}
