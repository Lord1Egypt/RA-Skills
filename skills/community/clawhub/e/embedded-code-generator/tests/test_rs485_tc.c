/**
 * @file test_rs485_tc.c
 * @brief Unit tests for the RS485 direction-control driver.
 *
 * The template's platform hooks (RS485_GPIO_WritePin /
 * RS485_USART_WaitTC) are __attribute__((weak)); this test provides
 * strong mock overrides that record call sequences. The USART is a
 * fake register block in RAM (SR/DR layout per the template).
 *
 * Covers: init validation + receive-mode default, DE assertion order,
 * BUSY guard, TC-wait pass/fail paths, force-DE-low on timeout,
 * byte-accurate blocking send, and state queries.
 */

#include <stdio.h>
#include <string.h>
#include "rs485_tc.h"

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
/* Mock platform layer (strong symbols override weak defaults)         */
/* ------------------------------------------------------------------ */

/* GPIO call log: [0]=(port,pin,state) triplets */
static void  *log_port[64];
static uint16_t log_pin[64];
static uint8_t  log_state[64];
static int      log_n;

/* WaitTC behavior: 0 = TC set (success), 1 = timeout */
static int waittc_mode;
static int waittc_calls;
static uint32_t last_timeout_ms;

/* Fake USART register block: SR @0x00, DR @0x04 (DR holds last byte) */
static uint32_t fake_usart[8];

static void mock_reset(void)
{
    log_n = 0;
    waittc_calls = 0;
    waittc_mode = 0;
    last_timeout_ms = 0;
    /* TXE (bit7) | TC (bit6) set so TX loops never stall */
    fake_usart[0] = (1u << 7) | (1u << 6);
    memset(fake_usart + 1, 0, sizeof(fake_usart) - sizeof(uint32_t));
}

void RS485_GPIO_WritePin(rs485_gpio_port_t *port, uint16_t pin, uint8_t state)
{
    if (log_n < 64) {
        log_port[log_n]  = port;
        log_pin[log_n]   = pin;
        log_state[log_n] = state;
        log_n++;
    }
}

int RS485_USART_WaitTC(rs485_usart_t *usart, uint32_t timeout_ms)
{
    (void)usart;
    waittc_calls++;
    last_timeout_ms = timeout_ms;
    return (waittc_mode != 0) ? -1 : 0;
}

/* ------------------------------------------------------------------ */
/* Test helpers                                                        */
/* ------------------------------------------------------------------ */

static uint8_t dummy_port;   /* stand-in GPIO port address */

/** DE state after the n-th GPIO call (searches log backwards). */
static uint8_t de_state_after(int n)
{
    int i;
    for (i = (n < log_n ? n : log_n) - 1; i >= 0; i--) {
        if (log_pin[i] == 5u && log_port[i] == (void *)&dummy_port) {
            return log_state[i];
        }
    }
    return 0xFFu;
}

int main(void)
{
    RS485_Handle_t h;

    /* --- Init validation --- */
    mock_reset();
    CHECK(RS485_Init(&h, &dummy_port, 5u, NULL, 0u,
                     (rs485_usart_t *)fake_usart) == RS485_OK,
          "init: valid handle returns OK");
    CHECK(log_n == 1 && log_state[0] == 0u,
          "init: DE driven low (receive mode) on init");
    CHECK(h.inited && !h.transmitting, "init: state flags set");

    mock_reset();
    CHECK(RS485_Init(NULL, &dummy_port, 5u, NULL, 0u,
                     (rs485_usart_t *)fake_usart) == RS485_ERR_PARAM,
          "init: NULL handle rejected");
    CHECK(RS485_Init(&h, NULL, 5u, NULL, 0u,
                     (rs485_usart_t *)fake_usart) == RS485_ERR_PARAM,
          "init: NULL de_port rejected");
    CHECK(RS485_Init(&h, &dummy_port, 5u, NULL, 0u, NULL) == RS485_ERR_PARAM,
          "init: NULL usart rejected");

    /* --- Begin/End transmit cycle --- */
    mock_reset();
    (void)RS485_Init(&h, &dummy_port, 5u, NULL, 0u, (rs485_usart_t *)fake_usart);
    log_n = 0;
    CHECK(RS485_BeginTransmit(&h) == RS485_OK, "begin: returns OK");
    CHECK(de_state_after(log_n) == 1u, "begin: DE asserted high");
    CHECK(RS485_IsTransmitting(&h), "begin: transmitting flag set");
    CHECK(RS485_BeginTransmit(&h) == RS485_ERR_BUSY,
          "begin: second begin while transmitting -> BUSY");

    CHECK(RS485_EndTransmit(&h) == RS485_OK, "end: TC ok returns OK");
    CHECK(waittc_calls == 1, "end: waits for TC exactly once");
    CHECK(de_state_after(log_n) == 0u, "end: DE dropped after TC");
    CHECK(!RS485_IsTransmitting(&h), "end: transmitting flag cleared");

    /* --- End without Begin: nothing to do --- */
    log_n = 0;
    CHECK(RS485_EndTransmit(&h) == RS485_OK, "end: idle end is a no-op OK");
    CHECK(waittc_calls == 1, "end: idle end does not poll TC");

    /* --- Timeout path: DE force-dropped --- */
    mock_reset();
    (void)RS485_Init(&h, &dummy_port, 5u, NULL, 0u, (rs485_usart_t *)fake_usart);
    log_n = 0;
    (void)RS485_BeginTransmit(&h);
    waittc_mode = 1;
    CHECK(RS485_EndTransmit(&h) == RS485_ERR_TIMEOUT,
          "timeout: TC wait failure reported");
    CHECK(de_state_after(log_n) == 0u,
          "timeout: DE force-dropped to avoid bus lock-up");
    CHECK(!RS485_IsTransmitting(&h), "timeout: state cleaned up");

    /* --- Blocking send: DE sequence + DR write (single register,
     *     only the LAST byte is observable in the fake block) --- */
    {
        uint8_t tx[4] = {0xA1u, 0xB2u, 0xC3u, 0xD4u};
        mock_reset();
        (void)RS485_Init(&h, &dummy_port, 5u, NULL, 0u,
                         (rs485_usart_t *)fake_usart);
        log_n = 0;
        CHECK(RS485_SendBlocking(&h, tx, 4u, 100u) == RS485_OK,
              "send: 4-byte send returns OK");
        CHECK(waittc_calls == 1 && last_timeout_ms == 100u,
              "send: caller timeout passed to WaitTC");
        CHECK((fake_usart[1] & 0xFFu) == tx[3],
              "send: DR holds the last transmitted byte");
        CHECK(de_state_after(log_n) == 0u, "send: DE low after completion");
        CHECK(!RS485_IsTransmitting(&h), "send: not transmitting after send");
    }

    /* --- Send validation --- */
    {
        uint8_t tx[2] = {1u, 2u};
        mock_reset();
        (void)RS485_Init(&h, &dummy_port, 5u, NULL, 0u,
                         (rs485_usart_t *)fake_usart);
        CHECK(RS485_SendBlocking(NULL, tx, 2u, 10u) == RS485_ERR_PARAM,
              "send: NULL handle rejected");
        CHECK(RS485_SendBlocking(&h, NULL, 2u, 10u) == RS485_ERR_PARAM,
              "send: NULL data rejected");
        CHECK(RS485_SendBlocking(&h, tx, 0u, 10u) == RS485_OK,
              "send: zero-length is a no-op OK");
        CHECK((fake_usart[1] == 0u) && waittc_calls == 0,
              "send: zero-length writes nothing");
    }

    /* --- Send timeout propagates --- */
    {
        uint8_t tx[1] = {0x55u};
        mock_reset();
        (void)RS485_Init(&h, &dummy_port, 5u, NULL, 0u,
                         (rs485_usart_t *)fake_usart);
        waittc_mode = 1;
        CHECK(RS485_SendBlocking(&h, tx, 1u, 10u) == RS485_ERR_TIMEOUT,
              "send: TC timeout returns ERR_TIMEOUT");
    }

    /* --- IsTransmitting NULL-safe --- */
    CHECK(!RS485_IsTransmitting(NULL), "state: NULL handle reports false");

    printf("Summary: %d checks, %d passed, %d failed\n", g_total, g_pass, g_fail);
    return (g_fail == 0) ? 0 : 1;
}
