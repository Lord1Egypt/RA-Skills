/**
 * @file spi_master.c
 * @brief Bit-banged SPI master, modes 0-3, full-duplex, CS controlled.
 *
 * The weak platform hooks below must be overridden by the application;
 * the defaults are no-ops so the module links without hardware.
 */

#include "spi_master.h"

/* ------------------------------------------------------------------ */
/* Platform hooks — weak defaults, override in application             */
/* ------------------------------------------------------------------ */

#if !defined(SPI_SCK_WRITE)
__attribute__((weak))
void SPI_SCK_Write(int level) { (void)level; }
#define SPI_SCK_WRITE(level) SPI_SCK_Write(level)
#endif

#if !defined(SPI_MOSI_WRITE)
__attribute__((weak))
void SPI_MOSI_Write(int level) { (void)level; }
#define SPI_MOSI_WRITE(level) SPI_MOSI_Write(level)
#endif

#if !defined(SPI_MISO_READ)
__attribute__((weak))
int SPI_MISO_Read(void) { return 0; }
#define SPI_MISO_READ() SPI_MISO_Read()
#endif

#if !defined(SPI_CS_WRITE)
__attribute__((weak))
void SPI_CS_Write(int asserted) { (void)asserted; }
#define SPI_CS_WRITE(asserted) SPI_CS_Write(asserted)
#endif

#if !defined(SPI_DELAY_HALF)
__attribute__((weak))
void SPI_DelayHalf(void) { }
#define SPI_DELAY_HALF() SPI_DelayHalf()
#endif

/* ------------------------------------------------------------------ */
/* Module state                                                        */
/* ------------------------------------------------------------------ */

static SPI_Config_t m_cfg = {
    .mode          = SPI_MODE_0,
    .msb_first     = 1u,
    .cs_active_low = 1u,
};
static bool m_inited = false;

/* ------------------------------------------------------------------ */
/* Internal helpers                                                    */
/* ------------------------------------------------------------------ */

/** SCK idle level derived from CPOL. */
static int sck_idle(void)
{
    return (int)(m_cfg.mode & 0x01u);
}

/** Leading SCK edge level (opposite of idle). */
static int sck_leading(void)
{
    return sck_idle() ^ 1;
}

/** Extract bit number i (0 = first shifted-out bit) per shift order. */
static int tx_bit(uint8_t tx, int i)
{
    int shift = m_cfg.msb_first ? (7 - i) : i;
    return (tx >> shift) & 0x01;
}

/** Store a sampled bit at position i per shift order. */
static void rx_store(uint8_t *rx, int i, int bit)
{
    int shift = m_cfg.msb_first ? (7 - i) : i;

    if ((rx != NULL) && (bit != 0))
    {
        *rx |= (uint8_t)(1u << shift);
    }
}

/* ------------------------------------------------------------------ */
/* Public API                                                          */
/* ------------------------------------------------------------------ */

int SPI_Init(const SPI_Config_t *cfg)
{
    if ((cfg == NULL) || (cfg->mode > SPI_MODE_3))
    {
        return SPI_ERR_PARAM;
    }

    m_cfg    = *cfg;
    m_inited = true;

    /* Idle levels: SCK at CPOL level, CS deselected. The CS hook takes
     * the asserted flag (1 = selected); pin polarity lives in the hook. */
    SPI_SCK_WRITE(sck_idle());
    SPI_CS_WRITE(0);

    return SPI_OK;
}

int SPI_Transfer(uint8_t tx, uint8_t *rx)
{
    int    i;
    int    idle    = sck_idle();
    int    leading = sck_leading();
    int    cpha    = (int)((m_cfg.mode >> 1) & 0x01u);
    uint8_t value  = 0u;

    (void)m_inited;

    for (i = 0; i < 8; i++)
    {
        int bit = tx_bit(tx, i);

        if (cpha == 0)
        {
            /* Data changes while SCK idle, sampled at leading edge. */
            SPI_MOSI_WRITE(bit);
            SPI_DELAY_HALF();

            SPI_SCK_WRITE(leading);          /* leading edge */
            SPI_DELAY_HALF();
            rx_store(&value, i, SPI_MISO_READ());

            SPI_SCK_WRITE(idle);             /* trailing edge */
            SPI_DELAY_HALF();
        }
        else
        {
            /* Data changes at leading edge, sampled at trailing edge. */
            SPI_SCK_WRITE(leading);          /* leading edge */
            SPI_MOSI_WRITE(bit);
            SPI_DELAY_HALF();

            SPI_SCK_WRITE(idle);             /* trailing edge: sample */
            SPI_DELAY_HALF();
            rx_store(&value, i, SPI_MISO_READ());
        }
    }

    SPI_SCK_WRITE(idle);

    if (rx != NULL)
    {
        *rx = value;
    }
    return SPI_OK;
}

int SPI_Transaction(const uint8_t *tx, uint8_t *rx, uint16_t len)
{
    uint16_t i;

    if ((len == 0u) || ((tx == NULL) && (rx == NULL)))
    {
        return SPI_ERR_PARAM;
    }

    (void)m_inited;

    SPI_CS_WRITE(1);    /* select slave */
    SPI_DELAY_HALF();

    for (i = 0u; i < len; i++)
    {
        uint8_t out = (tx != NULL) ? tx[i] : 0xFFu;
        uint8_t in  = 0u;

        (void)SPI_Transfer(out, &in);
        if (rx != NULL)
        {
            rx[i] = in;
        }
    }

    SPI_DELAY_HALF();
    SPI_CS_WRITE(0);    /* deselect slave */

    return SPI_OK;
}

int SPI_GetConfig(SPI_Config_t *cfg)
{
    if (cfg == NULL)
    {
        return SPI_ERR_PARAM;
    }

    *cfg = m_cfg;
    return SPI_OK;
}
