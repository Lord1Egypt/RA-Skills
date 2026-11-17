/**
 * @file test_soft_i2c.c
 * @brief Bit-level I2C slave simulator proving SI2C master correctness.
 *
 * The simulated slave sits inside the GPIO hooks: it tracks SCL/SDA
 * edges, detects START/STOP conditions, samples data bits on SCL rising
 * edges, drives ACK/data on SDA, and counts byte-level events. This
 * exercises the real bit-banged code path (open-drain release model,
 * 9th-clock ACK handling, repeated START) instead of mocking the API.
 */

#include <stdio.h>
#include <string.h>
#include "soft_i2c.h"

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

typedef enum {
    S_IDLE = 0,     /* waiting for START            */
    S_ADDR,         /* receiving address byte       */
    S_RX,           /* receiving data (master->slt) */
    S_TX            /* sending data (slt->master)   */
} SlavePhase;

static SlavePhase  sl_phase;
static uint8_t     sl_addr;            /* 7-bit address to match      */
static uint8_t     sl_rx_shift;        /* bit accumulator             */
static uint8_t     sl_rx_buf[8];       /* received data bytes         */
static uint8_t     sl_rx_count;
static const uint8_t *sl_tx;          /* bytes to send on read       */
static uint8_t     sl_tx_len;
static uint8_t     sl_tx_index;
static bool        sl_matched;
static bool        sl_mode_read;       /* R/W bit of address byte     */
static bool        sl_nack_data;       /* force NACK on data bytes    */
static unsigned    sl_edge_r;          /* rising edges in byte        */
static unsigned    sl_edge_f;          /* falling edges in byte       */
static int         sl_pulse_open;      /* SCL rising seen, clock open */
static unsigned    sl_bits_presented;  /* S_TX: bits shifted out      */
static bool        sl_master_acked;
static bool        sl_tx_done;

static unsigned    ev_start;           /* START conditions seen       */
static unsigned    ev_stop;            /* STOP conditions seen        */
static unsigned    ev_addr_match;      /* address matches             */
static unsigned    ev_master_ack;      /* master ACKs during read     */

/* Line state                                                         */
static int line_scl;
static int line_master_sda;           /* last level driven by master */
static int sl_sda;                    /* slave output (1 = release)  */

static int eff_sda(void)
{
    return (line_master_sda == 0) ? 0 : sl_sda;
}

static int tx_bit(uint8_t byte, unsigned idx)
{
    return (byte >> (7u - idx)) & 0x01u;
}

static void sl_reset(uint8_t addr, const uint8_t *tx, uint8_t len,
                     bool nack_data)
{
    sl_phase        = S_IDLE;
    sl_addr         = addr;
    sl_rx_shift     = 0u;
    sl_rx_count     = 0u;
    memset(sl_rx_buf, 0, sizeof(sl_rx_buf));
    sl_tx           = tx;
    sl_tx_len       = len;
    sl_tx_index     = 0u;
    sl_matched      = false;
    sl_mode_read    = false;
    sl_nack_data    = nack_data;
    sl_edge_r       = 0u;
    sl_edge_f       = 0u;
    sl_pulse_open   = 0;
    sl_bits_presented = 0u;
    sl_master_acked = false;
    sl_tx_done      = false;
    ev_start        = 0u;
    ev_stop         = 0u;
    ev_addr_match   = 0u;
    ev_master_ack   = 0u;
    line_scl        = 1;
    line_master_sda = 1;
    sl_sda          = 1;
}

/* ------------------------------------------------------------------ */
/* Edge handlers                                                       */
/* ------------------------------------------------------------------ */

static void sl_on_rising(void)
{
    int bit = eff_sda();

    if ((sl_phase == S_ADDR) || (sl_phase == S_RX))
    {
        sl_edge_r++;
        if (sl_edge_r <= 8u)
        {
            sl_rx_shift = (uint8_t)((sl_rx_shift << 1) | (unsigned)bit);
            if (sl_edge_r == 8u)
            {
                /* Full byte in: prepare the ACK output for the 9th clock. */
                if (sl_phase == S_ADDR)
                {
                    sl_matched   = ((sl_rx_shift >> 1) == sl_addr);
                    sl_mode_read = ((sl_rx_shift & 0x01u) != 0u);
                    sl_sda       = sl_matched ? 0 : 1;
                    if (sl_matched)
                    {
                        ev_addr_match++;
                    }
                }
                else
                {
                    sl_sda = sl_nack_data ? 1 : 0;
                }
            }
        }
        /* 9th rising: master is sampling our ACK; nothing to do. */
    }
    else if (sl_phase == S_TX)
    {
        sl_edge_r++;
        if (sl_edge_r == 9u)
        {
            /* 9th rising: master ACK slot. eff==0 means ACK. */
            sl_master_acked = (eff_sda() == 0);
            if (sl_master_acked && !sl_tx_done)
            {
                ev_master_ack++;
            }
            sl_bits_presented = 9u;
        }
    }
}

static void sl_on_falling(void)
{
    if ((sl_phase == S_ADDR) || (sl_phase == S_RX))
    {
        sl_edge_f++;
        if (sl_edge_f == 9u)
        {
            /* Byte complete (data + ACK clock). */
            if (sl_phase == S_ADDR)
            {
                if (sl_matched && sl_mode_read)
                {
                    sl_phase          = S_TX;
                    sl_tx_index       = 0u;
                    sl_bits_presented = 1u;
                    sl_sda            = tx_bit(sl_tx[0], 0u);
                }
                else if (sl_matched)
                {
                    sl_phase = S_RX;
                    sl_sda   = 1;   /* release ACK drive for data bits */
                }
                /* No match: stay in S_ADDR, keep NACKing. */
            }
            else
            {
                if (sl_rx_count < sizeof(sl_rx_buf))
                {
                    sl_rx_buf[sl_rx_count++] = sl_rx_shift;
                }
                sl_sda = 1;   /* release for next byte */
            }
            sl_rx_shift = 0u;
            sl_edge_r   = 0u;
            sl_edge_f   = 0u;
        }
    }
    else if (sl_phase == S_TX)
    {
        sl_edge_f++;
        if (sl_edge_f <= 7u)
        {
            /* Present the next data bit. */
            sl_bits_presented = sl_edge_f + 1u;
            sl_sda = tx_bit(sl_tx[sl_tx_index], sl_edge_f);
        }
        else if (sl_edge_f == 8u)
        {
            /* Release SDA for the master ACK slot. */
            sl_sda = 1;
        }
        else if (sl_edge_f == 9u)
        {
            if (sl_master_acked)
            {
                sl_tx_index++;
                if (sl_tx_index < sl_tx_len)
                {
                    sl_bits_presented = 1u;
                    sl_sda = tx_bit(sl_tx[sl_tx_index], 0u);
                }
                else
                {
                    sl_tx_done = true;
                    sl_sda     = 1;
                }
            }
            else
            {
                sl_tx_done = true;
                sl_sda     = 1;
            }
            sl_edge_r = 0u;
            sl_edge_f = 0u;
        }
    }
}

/* ------------------------------------------------------------------ */
/* GPIO hooks (strong definitions override weak defaults)              */
/* ------------------------------------------------------------------ */

void SI2C_SCL_Write(int level)
{
    if ((level != 0) && (line_scl == 0))
    {
        sl_pulse_open = 1;
        sl_on_rising();
    }
    else if ((level == 0) && (line_scl != 0))
    {
        /* Only a falling edge that closes an opened clock pulse counts;
         * the bus-idle SCL drop after START/STOP is not a clock. */
        if (sl_pulse_open != 0)
        {
            sl_pulse_open = 0;
            sl_on_falling();
        }
    }
    line_scl = level;
}

int SI2C_SCL_Read(void)
{
    return line_scl;
}

void SI2C_SDA_Write(int level)
{
    int prev_eff = eff_sda();

    line_master_sda = level;

    if (line_scl != 0)
    {
        int now_eff = eff_sda();

        if ((now_eff == 0) && (prev_eff != 0))
        {
            /* START: SDA falls while SCL high. */
            ev_start++;
            sl_phase          = S_ADDR;
            sl_rx_shift       = 0u;
            sl_matched        = false;
            sl_edge_r         = 0u;
            sl_edge_f         = 0u;
            sl_pulse_open     = 0;
            sl_bits_presented = 0u;
            sl_sda            = 1;
        }
        else if ((now_eff != 0) && (prev_eff == 0))
        {
            /* STOP: SDA rises while SCL high. */
            ev_stop++;
            sl_phase      = S_IDLE;
            sl_sda        = 1;
            sl_pulse_open = 0;
        }
    }
}

int SI2C_SDA_Read(void)
{
    return eff_sda();
}

void SI2C_DelayHalfBit(void)
{
    /* No real timing in unit test. */
}

/* ------------------------------------------------------------------ */
/* Test cases                                                          */
/* ------------------------------------------------------------------ */

int main(void)
{
    uint8_t  rd[4];
    int      rc;
    uint8_t  tx3[3] = { 0x5Au, 0xA5u, 0x3Cu };

    /* --- frequency validation ------------------------------------ */
    CHECK(SI2C_Init(SI2C_FREQ_MIN - 1u) == SI2C_ERR_FREQ, "freq below min rejected");
    CHECK(SI2C_Init(SI2C_FREQ_MAX + 1u) == SI2C_ERR_FREQ, "freq above max rejected");
    CHECK(SI2C_Init(100000u) == SI2C_OK, "valid freq accepted");
    CHECK(SI2C_GetFreq() == 100000u, "GetFreq returns configured value");

    /* --- happy path: write reg, repeated start, read 3 bytes ----- */
    sl_reset(0x50u, tx3, 3u, false);
    rc = SI2C_WriteThenRead(0x50u, 0x10u, rd, 3u);
    CHECK(rc == SI2C_OK, "WriteThenRead returns OK");
    CHECK(rd[0] == 0x5Au, "read byte 0 == 0x5A");
    CHECK(rd[1] == 0xA5u, "read byte 1 == 0xA5");
    CHECK(rd[2] == 0x3Cu, "read byte 2 == 0x3C");
    CHECK((sl_rx_count == 1u) && (sl_rx_buf[0] == 0x10u),
          "slave received register address 0x10");
    CHECK(ev_start == 2u, "START + repeated START seen");
    CHECK(ev_stop == 1u, "exactly one STOP seen");
    CHECK(ev_addr_match == 2u, "address matched on both phases");
    CHECK(ev_master_ack == 2u, "master ACKed first two read bytes");
    CHECK(sl_tx_done, "slave saw NACK after last read byte");

    /* --- address NACK -------------------------------------------- */
    sl_reset(0x51u, tx3, 3u, false);
    rc = SI2C_Start();
    CHECK(rc == SI2C_OK, "Start OK");
    rc = SI2C_WriteByte((uint8_t)(0x50u << 1));
    CHECK(rc == SI2C_ERR_NACK, "unmatched address gets NACK");
    (void)SI2C_Stop();
    CHECK(ev_stop == 1u, "exactly one STOP after abort");

    /* --- data NACK ----------------------------------------------- */
    sl_reset(0x50u, NULL, 0u, true);
    rc = SI2C_WriteThenRead(0x50u, 0x20u, rd, 1u);
    CHECK(rc == SI2C_ERR_NACK, "forced data NACK propagates");
    CHECK(ev_stop == 1u, "Stop issued after data NACK abort");

    /* --- WriteThenRead parameter checks -------------------------- */
    sl_reset(0x50u, tx3, 3u, false);
    CHECK(SI2C_WriteThenRead(0x50u, 0x10u, NULL, 1u) == SI2C_ERR_PARAM,
          "NULL buffer rejected");
    CHECK(SI2C_WriteThenRead(0x50u, 0x10u, rd, 0u) == SI2C_ERR_PARAM,
          "len 0 rejected");
    CHECK(SI2C_WriteThenRead(0x80u, 0x10u, rd, 1u) == SI2C_ERR_PARAM,
          "addr7 > 0x7F rejected");
    CHECK(SI2C_ReadByte(NULL, true) == SI2C_ERR_PARAM,
          "ReadByte NULL rejected");

    /* --- MSB-first bit order proof ------------------------------- */
    sl_reset(0x50u, NULL, 0u, false);
    rc = SI2C_Start();
    rc |= SI2C_WriteByte((uint8_t)(0x50u << 1));
    rc |= SI2C_WriteByte(0xA5u);
    CHECK((rc == SI2C_OK) && (sl_rx_count == 1u) && (sl_rx_buf[0] == 0xA5u),
          "0xA5 received intact (MSB first)");

    printf("test_soft_i2c: %d/%d passed\n", g_pass, g_total);
    return (g_fail == 0) ? 0 : 1;
}
