/**
 * @file rs485_tc.c
 * @brief RS485 Transmit Control implementation.
 *
 * Platform-specific GPIO and USART access is abstracted through
 * weak functions that the application should override for its
 * specific MCU family.
 */

#include "rs485_tc.h"
#include <stddef.h>  /* NULL */
#include <stdint.h>  /* uintptr_t */

/* ------------------------------------------------------------------ */
/* Platform-specific weak defaults (STM32 HAL style)                   */
/*                                                                     */
/* Override these for your platform. The default implementations      */
/* assume STM32 HAL. If you are not using STM32 HAL, provide your     */
/* own versions or define RS485_PLATFORM_HAL.                          */
/* ------------------------------------------------------------------ */

#ifndef RS485_PLATFORM_HAL

/* Forward-declare STM32 HAL types so the weak defaults compile.
 * If the user provides their own platform layer, they define
 * RS485_PLATFORM_HAL and these are skipped. */

typedef struct {
    volatile uint32_t SR;   /*!< USART Status register,        offset 0x00 */
    volatile uint32_t DR;   /*!< USART Data register,          offset 0x04 */
    uint32_t Reserved[3];
    volatile uint32_t CR1;  /*!< USART Control register 1,     offset 0x0C */
} USART_RegDef_t;

/* STM32 USART SR bit positions */
#define USART_SR_TC_Pos   (6U)
#define USART_SR_TC_Msk   (1U << USART_SR_TC_Pos)

/**
 * @brief Weak GPIO write. Override for non-STM32 platforms.
 *
 * @param port  GPIO port pointer (cast from GPIO_TypeDef*).
 * @param pin   Pin number (0-based).
 * @param state 1 = high, 0 = low.
 */
__attribute__((weak))
void RS485_GPIO_WritePin(rs485_gpio_port_t *port, uint16_t pin, uint8_t state)
{
    /* STM32 BSRR-based write: pin 0..15 = set, 16..31 = reset.
     * This is a simplified generic BSRR; adapt to your HAL. */
    if (port != NULL) {
        volatile uint32_t *bsrr = (volatile uint32_t *)((uintptr_t)port + 0x18u);
        if (state) {
            *bsrr = (1u << pin);
        } else {
            *bsrr = (1u << (pin + 16u));
        }
    }
}

/**
 * @brief Weak TC-wait. Polls USART SR TC bit with a simple timeout.
 *
 * @param usart      USART peripheral pointer.
 * @param timeout_ms Timeout in milliseconds (approximate).
 * @return 0 if TC set, -1 on timeout.
 */
__attribute__((weak))
int RS485_USART_WaitTC(rs485_usart_t *usart, uint32_t timeout_ms)
{
    USART_RegDef_t *regs = (USART_RegDef_t *)usart;
    uint32_t count = 0u;
    uint32_t limit;

    if (regs == NULL) {
        return -1;
    }

    /*
     * Each iteration is ~3 instructions at typical MCU clock.
     * This is a rough approximation; for precise timeouts use
     * a hardware timer (SysTick, etc.).
     */
    limit = timeout_ms * 1000u;

    while ((regs->SR & USART_SR_TC_Msk) == 0U) {
        count++;
        if (count >= limit) {
            return -1;
        }
    }

    /* Clear TC by reading SR then writing DR (required on STM32). */
    (void)regs->SR;
    (void)regs->DR;

    return 0;
}

#else
/* User provides RS485_GPIO_WritePin and RS485_USART_WaitTC externally. */
extern void RS485_GPIO_WritePin(rs485_gpio_port_t *port, uint16_t pin, uint8_t state);
extern int  RS485_USART_WaitTC(rs485_usart_t *usart, uint32_t timeout_ms);
#endif /* RS485_PLATFORM_HAL */

/* ------------------------------------------------------------------ */
/* Internal helpers                                                    */
/* ------------------------------------------------------------------ */

static void rs485_de_set(RS485_Handle_t *h, uint8_t state)
{
    RS485_GPIO_WritePin(h->de_port, h->de_pin, state);

    /* If /RE is independently controlled, it is the inverse of DE.
     * DE=1 -> /RE=1 (receiver disabled), DE=0 -> /RE=0 (receiver enabled). */
    if (h->re_port != NULL) {
        RS485_GPIO_WritePin(h->re_port, h->re_pin, state);
    }
}

/* ================================================================== */
/* Public API                                                          */
/* ================================================================== */

int RS485_Init(RS485_Handle_t *h,
               rs485_gpio_port_t *de_port, uint16_t de_pin,
               rs485_gpio_port_t *re_port, uint16_t re_pin,
               rs485_usart_t *usart)
{

    if (h == NULL || de_port == NULL || usart == NULL) {
        return RS485_ERR_PARAM;
    }

    h->de_port = de_port;
    h->de_pin  = de_pin;
    h->re_port = re_port;
    h->re_pin  = re_pin;
    h->usart   = usart;
    h->inited  = true;
    h->transmitting = false;

    /* Start in receive mode (DE low). */
    rs485_de_set(h, 0u);

    return RS485_OK;
}

int RS485_BeginTransmit(RS485_Handle_t *h)
{

    if (h == NULL || !h->inited) {
        return RS485_ERR_PARAM;
    }

    if (h->transmitting) {
        return RS485_ERR_BUSY;
    }

    /* Assert DE high to enable the RS485 driver. */
    rs485_de_set(h, 1u);
    h->transmitting = true;

    /*
     * A small settling delay may be needed depending on transceiver
     * and bus termination. Typically < 1 µs is sufficient for
     * modern transceivers (e.g., MAX485 t_zh ~ 100 ns). Add a
     * short NOP or hardware delay here if your transceiver is slow.
     */

    return RS485_OK;
}

int RS485_EndTransmit(RS485_Handle_t *h)
{
    int rc;


    if (h == NULL || !h->inited) {
        return RS485_ERR_PARAM;
    }

    if (!h->transmitting) {
        return RS485_OK; /* Nothing to do. */
    }

    /*
     * Wait for TC (Transmission Complete).
     *
     * CRITICAL: Do NOT pull DE low immediately after the last write
     * to DR. The last byte (including its stop bit) may still be in
     * the UART shift register. Prematurely dropping DE causes the
     * final character to be truncated on the bus.
     *
     * The TC flag is set by hardware when the last frame has been
     * fully transmitted (shift register empty, no new data in DR).
     */
    rc = RS485_USART_WaitTC(h->usart, RS485_TC_TIMEOUT_DEFAULT);
    if (rc != 0) {
        /* Timeout: force DE low anyway to avoid bus lock-up. */
        rs485_de_set(h, 0u);
        h->transmitting = false;
        return RS485_ERR_TIMEOUT;
    }

    /* TC is set — safe to disable the driver. */
    rs485_de_set(h, 0u);
    h->transmitting = false;

    return RS485_OK;
}

int RS485_SendBlocking(RS485_Handle_t *h,
                       const uint8_t *data, uint16_t length,
                       uint32_t timeout_ms)
{
    USART_RegDef_t *regs;
    uint16_t i;
    int rc;


    if (h == NULL || !h->inited || data == NULL) {
        return RS485_ERR_PARAM;
    }

    if (length == 0u) {
        return RS485_OK;
    }

    regs = (USART_RegDef_t *)h->usart;

    rc = RS485_BeginTransmit(h);
    if (rc != RS485_OK) {
        return rc;
    }

    for (i = 0u; i < length; i++) {
        /* Wait until TXE (Transmit Data Register Empty) — bit 7. */
        while ((regs->SR & (1u << 7u)) == 0u) {
            /* Could add timeout here in production. */
        }
        regs->DR = data[i];
    }

    /*
     * Wait for the last byte to finish shifting out, THEN drop DE.
     * We use the caller-provided timeout here.
     */
    rc = RS485_USART_WaitTC(h->usart, timeout_ms);
    rs485_de_set(h, 0u);
    h->transmitting = false;

    return (rc == 0) ? RS485_OK : RS485_ERR_TIMEOUT;
}

bool RS485_IsTransmitting(const RS485_Handle_t *h)
{

    if (h == NULL) {
        return false;
    }

    return h->transmitting;
}
