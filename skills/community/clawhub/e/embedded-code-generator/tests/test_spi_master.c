/**
 * @file test_spi_master.c
 * @brief Edge-accurate SPI slave simulator proving mode 0-3 correctness.
 *
 * The simulated slave lives in the GPIO hooks: it knows the configured
 * mode, captures MOSI on the correct edge (leading for CPHA=0, trailing
 * for CPHA=1), presents MISO on the opposite edge, and reloads on CS
 * assert. Master and slave exchange different patterns in both
 * directions, so a wrong sampling edge, wrong CPOL idle level or wrong
 * bit order breaks the received bytes and fails the check.
 *
 * Slave MISO rule (uniform for all modes): on a non-sampling edge the
 * slave presents bit[captured] of its pattern; on the sampling edge it
 * captures MOSI. For CPHA=0 the bit is set at the trailing edge of the
 * previous bit (or CS assert); for CPHA=1 it is set at the leading edge
 * of the same bit — exactly how real slave devices behave.
 */

#include <stdio.h>
#include <string.h>
#include "spi_master.h"

/* ------------------------------------------------------------------ */
/* Check framework                                                     */
/* ------------------------------------------------------------------ */

static int g_total = 0;
static int g_pass  = 0;
static int g_fail  = 0;

#define CHECK(cond, name)                                        \
    do {                                                         \
        g_total++;                                               \
        if (cond) { g_pass++; }                                  \
        else { g_fail++; printf("[FAIL] %s\n", name); }          \
    } while (0)

/* ------------------------------------------------------------------ */
/* Simulated slave state                                               */
/* ------------------------------------------------------------------ */

static uint8_t  sl_mode;            /* SPI mode the slave expects   */
static uint8_t  sl_msb_first;       /* bit order the slave expects  */
static uint8_t  sl_tx_byte;         /* pattern slave shifts out     */
static uint8_t  sl_rx_shift;        /* MOSI bits captured this byte */
static uint8_t  sl_last_byte;       /* last completed captured byte */
static unsigned sl_bits;            /* captured bits in this byte   */
static unsigned sl_bytes_done;      /* completed byte count         */
static int      sl_miso;            /* slave MISO output level      */
static int      sl_active;          /* CS asserted                  */

static int line_sck;
static int line_mosi;

static int sl_bit_of(uint8_t byte, unsigned idx)
{
    unsigned shift = sl_msb_first ? (7u - idx) : idx;
    return (int)((byte >> shift) & 0x01u);
}

static bool is_sampling_edge(int sck)
{
    /* Leading edge = first edge of the bit (level != CPOL idle).
     * Sampling edge = leading for CPHA=0, trailing for CPHA=1. */
    bool leading = (sck != (int)(sl_mode & 0x01u));
    bool cpha1   = ((sl_mode >> 1) & 0x01u) != 0u;

    return cpha1 ? !leading : leading;
}

static void sl_cs_assert(void)
{
    sl_active     = 1;
    sl_rx_shift   = 0u;
    sl_last_byte  = 0u;
    sl_bits       = 0u;
    sl_bytes_done = 0u;
    sl_miso       = sl_bit_of(sl_tx_byte, 0u);
}

static void sl_edge(int sck)
{
    if (!sl_active)
    {
        return;
    }

    if (is_sampling_edge(sck))
    {
        /* Capture MOSI at the sampling edge. */
        sl_rx_shift = (uint8_t)((sl_rx_shift << 1) | (unsigned)(line_mosi & 1));
        sl_bits++;
        if (sl_bits == 8u)
        {
            sl_last_byte  = sl_rx_shift;
            sl_bytes_done++;
            sl_rx_shift   = 0u;
            sl_bits       = 0u;
        }
    }
    else
    {
        /* Present the bit the master will capture next. */
        if (sl_bits < 8u)
        {
            sl_miso = sl_bit_of(sl_tx_byte, sl_bits);
        }
    }
}

/* ------------------------------------------------------------------ */
/* GPIO hooks (strong definitions override weak defaults)              */
/* ------------------------------------------------------------------ */

void SPI_SCK_Write(int level)
{
    if (level != line_sck)
    {
        sl_edge(level);
        line_sck = level;
    }
}

void SPI_MOSI_Write(int level)
{
    line_mosi = level;
}

int SPI_MISO_Read(void)
{
    return sl_miso;
}

void SPI_CS_Write(int asserted)
{
    if (asserted && !sl_active)
    {
        sl_cs_assert();
    }
    sl_active = asserted;
}

void SPI_DelayHalf(void)
{
    /* No real timing in unit test. */
}

/* ------------------------------------------------------------------ */
/* Test cases                                                          */
/* ------------------------------------------------------------------ */

int main(void)
{
    const uint8_t master_pat = 0x3Cu;   /* 0b00111100 */
    const uint8_t slave_pat  = 0xC3u;   /* 0b11000011 */
    SPI_Config_t cfg;
    uint8_t tx[4];
    uint8_t rx[4];
    int     rc;
    uint8_t m;

    /* --- parameter validation ------------------------------------- */
    CHECK(SPI_Init(NULL) == SPI_ERR_PARAM, "NULL config rejected");
    cfg.mode = 4u; cfg.msb_first = 1u; cfg.cs_active_low = 1u;
    CHECK(SPI_Init(&cfg) == SPI_ERR_PARAM, "mode 4 rejected");

    /* --- all four modes, MSB first -------------------------------- */
    for (m = SPI_MODE_0; m <= SPI_MODE_3; m++)
    {
        char name[64];

        cfg.mode = m; cfg.msb_first = 1u; cfg.cs_active_low = 1u;
        CHECK(SPI_Init(&cfg) == SPI_OK, "Init OK");

        sl_mode = m; sl_msb_first = 1u; sl_tx_byte = slave_pat;
        tx[0] = master_pat; rx[0] = 0u;

        rc = SPI_Transaction(tx, rx, 1u);
        CHECK(rc == SPI_OK, "transaction OK");

        (void)snprintf(name, sizeof(name),
                       "mode %u MSB: master got slave pattern", (unsigned)m);
        CHECK(rx[0] == slave_pat, name);
        (void)snprintf(name, sizeof(name),
                       "mode %u MSB: slave captured master pattern", (unsigned)m);
        CHECK((sl_bytes_done == 1u) && (sl_last_byte == master_pat), name);
    }

    /* --- all four modes, LSB first -------------------------------- */
    for (m = SPI_MODE_0; m <= SPI_MODE_3; m++)
    {
        char name[64];

        cfg.mode = m; cfg.msb_first = 0u; cfg.cs_active_low = 1u;
        CHECK(SPI_Init(&cfg) == SPI_OK, "Init OK (LSB)");

        sl_mode = m; sl_msb_first = 0u; sl_tx_byte = slave_pat;
        tx[0] = master_pat; rx[0] = 0u;

        rc = SPI_Transaction(tx, rx, 1u);
        CHECK((rc == SPI_OK) && (rx[0] == slave_pat), "LSB first roundtrip");
        (void)snprintf(name, sizeof(name),
                       "mode %u LSB: slave captured master pattern", (unsigned)m);
        CHECK((sl_bytes_done == 1u) && (sl_last_byte == master_pat), name);
    }

    /* --- multi-byte transaction + write-only/read-only ------------ */
    cfg.mode = SPI_MODE_0; cfg.msb_first = 1u; cfg.cs_active_low = 1u;
    CHECK(SPI_Init(&cfg) == SPI_OK, "Init OK");
    sl_mode = SPI_MODE_0; sl_msb_first = 1u; sl_tx_byte = 0x55u;

    tx[0] = 0xAAu; tx[1] = 0x0Fu; tx[2] = 0xF0u; tx[3] = 0xFFu;
    memset(rx, 0, sizeof(rx));
    rc = SPI_Transaction(tx, rx, 4u);
    CHECK(rc == SPI_OK, "4-byte transaction OK");
    CHECK(sl_bytes_done == 4u, "slave captured 4 bytes");
    CHECK((rx[0] == 0x55u) && (rx[1] == 0x55u) &&
          (rx[2] == 0x55u) && (rx[3] == 0x55u),
          "repeating slave pattern received on all bytes");

    sl_tx_byte = 0x77u;
    memset(rx, 0, sizeof(rx));
    rc = SPI_Transaction(NULL, rx, 2u);          /* read-only: 0xFF dummies */
    CHECK((rc == SPI_OK) && (rx[0] == 0x77u) && (rx[1] == 0x77u),
          "read-only transaction works (tx NULL)");

    tx[0] = 0x81u; tx[1] = 0x42u;
    rc = SPI_Transaction(tx, NULL, 2u);          /* write-only: rx NULL */
    CHECK((rc == SPI_OK) && (sl_bytes_done == 2u) &&
          (sl_last_byte == 0x42u),
          "write-only transaction works (rx NULL)");

    /* --- error paths ---------------------------------------------- */
    CHECK(SPI_Transaction(NULL, NULL, 2u) == SPI_ERR_PARAM,
          "tx and rx both NULL rejected");
    CHECK(SPI_Transaction(tx, rx, 0u) == SPI_ERR_PARAM,
          "len 0 rejected");
    CHECK(SPI_GetConfig(NULL) == SPI_ERR_PARAM, "GetConfig NULL rejected");
    CHECK((SPI_GetConfig(&cfg) == SPI_OK) && (cfg.mode == SPI_MODE_0),
          "GetConfig returns applied config");

    printf("test_spi_master: %d/%d passed\n", g_pass, g_total);
    return (g_fail == 0) ? 0 : 1;
}
