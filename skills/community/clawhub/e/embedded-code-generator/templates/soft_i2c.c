/**
 * @file soft_i2c.c
 * @brief Bit-banged software I2C master (open-drain GPIO emulation).
 *
 * All bus edges follow open-drain semantics: writing 0 drives the line
 * low, writing 1 releases it (pull-up wins). The weak platform hooks
 * below must be overridden by the application; the defaults are no-ops
 * so the module links without hardware.
 *
 * Timing: every half-bit is separated by SI2C_DelayHalfBit(). If
 * SI2C_WAIT_SCL is 1 (default), each SCL-high phase additionally polls
 * SI2C_SCL_Read() so clock stretching by a slow slave is respected.
 */

#include "soft_i2c.h"

/* ------------------------------------------------------------------ */
/* Platform hooks — weak defaults, override in application             */
/* ------------------------------------------------------------------ */

#if !defined(SI2C_SCL_WRITE)
__attribute__((weak))
void SI2C_SCL_Write(int level) { (void)level; }
#define SI2C_SCL_WRITE(level) SI2C_SCL_Write(level)
#endif

#if !defined(SI2C_SCL_READ)
__attribute__((weak))
int SI2C_SCL_Read(void) { return 1; }
#define SI2C_SCL_READ() SI2C_SCL_Read()
#endif

#if !defined(SI2C_SDA_WRITE)
__attribute__((weak))
void SI2C_SDA_Write(int level) { (void)level; }
#define SI2C_SDA_WRITE(level) SI2C_SDA_Write(level)
#endif

#if !defined(SI2C_SDA_READ)
__attribute__((weak))
int SI2C_SDA_Read(void) { return 1; }
#define SI2C_SDA_READ() SI2C_SDA_Read()
#endif

#if !defined(SI2C_DELAY_HALF_BIT)
__attribute__((weak))
void SI2C_DelayHalfBit(void) { }
#define SI2C_DELAY_HALF_BIT() SI2C_DelayHalfBit()
#endif

/* ------------------------------------------------------------------ */
/* Module state                                                        */
/* ------------------------------------------------------------------ */

static uint32_t m_bus_freq = 100000u;   /**< Configured bus frequency. */
static bool     m_inited   = false;     /**< SI2C_Init() was called.   */

/* ------------------------------------------------------------------ */
/* Internal helpers                                                    */
/* ------------------------------------------------------------------ */

/** Release SDA, then wait until SCL is actually high (clock stretching). */
static void i2c_scl_high_wait(void)
{
    SI2C_SCL_WRITE(1);
#if SI2C_WAIT_SCL
    {
        uint32_t guard = 0u;
        while ((SI2C_SCL_READ() == 0) && (guard < 100000u))
        {
            guard++;
        }
    }
#endif
    SI2C_DELAY_HALF_BIT();
}

/* ------------------------------------------------------------------ */
/* Public API                                                          */
/* ------------------------------------------------------------------ */

int SI2C_Init(uint32_t bus_freq_hz)
{
    if ((bus_freq_hz < SI2C_FREQ_MIN) || (bus_freq_hz > SI2C_FREQ_MAX))
    {
        return SI2C_ERR_FREQ;
    }

    m_bus_freq = bus_freq_hz;
    m_inited   = true;

    /* Release both lines: bus idle state. */
    SI2C_SCL_WRITE(1);
    SI2C_SDA_WRITE(1);

    return SI2C_OK;
}

int SI2C_Start(void)
{
    SI2C_ASSERT(m_inited);

    /* Both lines released, SCL high. */
    SI2C_SDA_WRITE(1);
    i2c_scl_high_wait();

    /* START: SDA falls while SCL is high. */
    SI2C_SDA_WRITE(0);
    SI2C_DELAY_HALF_BIT();

    /* Prepare for the first data bit. */
    SI2C_SCL_WRITE(0);
    SI2C_DELAY_HALF_BIT();

    return SI2C_OK;
}

int SI2C_Stop(void)
{
    SI2C_ASSERT(m_inited);

    /* SDA low, then SCL high. */
    SI2C_SCL_WRITE(0);
    SI2C_DELAY_HALF_BIT();
    SI2C_SDA_WRITE(0);
    SI2C_DELAY_HALF_BIT();

    /* STOP: SDA rises while SCL is high. */
    i2c_scl_high_wait();
    SI2C_SDA_WRITE(1);
    SI2C_DELAY_HALF_BIT();

    return SI2C_OK;
}

int SI2C_WriteByte(uint8_t byte)
{
    int      i;
    bool     ack;

    SI2C_ASSERT(m_inited);

    /* 8 data bits, MSB first, changed while SCL is low. */
    for (i = 7; i >= 0; i--)
    {
        SI2C_SDA_WRITE((byte >> i) & 0x01u);
        SI2C_DELAY_HALF_BIT();
        i2c_scl_high_wait();
        SI2C_SCL_WRITE(0);
        SI2C_DELAY_HALF_BIT();
    }

    /* 9th clock: release SDA and sample the slave ACK. */
    SI2C_SDA_WRITE(1);
    SI2C_DELAY_HALF_BIT();
    i2c_scl_high_wait();
    ack = (SI2C_SDA_READ() == 0);
    SI2C_SCL_WRITE(0);
    SI2C_DELAY_HALF_BIT();

    return ack ? SI2C_OK : SI2C_ERR_NACK;
}

int SI2C_ReadByte(uint8_t *byte, bool ack)
{
    int    i;
    uint8_t value = 0u;

    if (byte == NULL)
    {
        return SI2C_ERR_PARAM;
    }

    SI2C_ASSERT(m_inited);

    /* Release SDA: the slave drives the data bits. */
    SI2C_SDA_WRITE(1);

    for (i = 7; i >= 0; i--)
    {
        i2c_scl_high_wait();
        value = (uint8_t)(value << 1);
        if (SI2C_SDA_READ() != 0)
        {
            value |= 0x01u;
        }
        SI2C_SCL_WRITE(0);
        SI2C_DELAY_HALF_BIT();
    }

    /* 9th clock: master drives ACK (more bytes) or NACK (last byte). */
    SI2C_SDA_WRITE(ack ? 0 : 1);
    SI2C_DELAY_HALF_BIT();
    i2c_scl_high_wait();
    SI2C_SCL_WRITE(0);
    SI2C_DELAY_HALF_BIT();

    /* Release SDA so the slave (or STOP) can drive the line again. */
    SI2C_SDA_WRITE(1);

    *byte = value;
    return SI2C_OK;
}

int SI2C_WriteThenRead(uint8_t addr7, uint8_t reg,
                       uint8_t *data, uint16_t len)
{
    uint16_t i;
    int      rc;

    if ((data == NULL) || (len == 0u) || (addr7 > 0x7Fu))
    {
        return SI2C_ERR_PARAM;
    }

    /* Write phase: register address. */
    rc = SI2C_Start();
    if (rc != SI2C_OK)
    {
        (void)SI2C_Stop();
        return rc;
    }

    rc = SI2C_WriteByte((uint8_t)((addr7 << 1) | 0x00u));  /* addr + W */
    if (rc == SI2C_OK)
    {
        rc = SI2C_WriteByte(reg);
    }
    if (rc != SI2C_OK)
    {
        (void)SI2C_Stop();
        return rc;
    }

    /* Read phase: repeated START with R/W = 1. */
    rc = SI2C_Start();
    if (rc != SI2C_OK)
    {
        (void)SI2C_Stop();
        return rc;
    }

    rc = SI2C_WriteByte((uint8_t)((addr7 << 1) | 0x01u));  /* addr + R */
    if (rc != SI2C_OK)
    {
        (void)SI2C_Stop();
        return rc;
    }

    for (i = 0u; i < len; i++)
    {
        /* ACK every byte except the last one. */
        rc = SI2C_ReadByte(&data[i], i < (uint16_t)(len - 1u));
        if (rc != SI2C_OK)
        {
            (void)SI2C_Stop();
            return rc;
        }
    }

    return SI2C_Stop();
}

uint32_t SI2C_GetFreq(void)
{
    return m_bus_freq;
}
