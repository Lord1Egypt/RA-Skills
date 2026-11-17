/**
 * @file rs485_tc.h
 * @brief RS485 half-duplex direction (Transmit Control) driver.
 *
 * Manages the DE (Driver Enable) and /RE (Receiver Enable) pins for
 * RS485 transceivers.  DE is asserted before transmission and
 * de-asserted only after the UART's TC (Transmission Complete) flag
 * is set, ensuring the last stop bit has been shifted out.
 *
 * @warning A common bug is de-asserting DE immediately after writing
 *          the last byte to DR. The byte may still be in the shift
 *          register; dropping DE truncates the last character. Always
 *          wait for USART_SR.TC == 1 before pulling DE low.
 *
 * Two usage modes are provided:
 *   1. Blocking:  RS485_SendBlocking() handles DE/TC internally.
 *   2. Callback:  RS485_BeginTransmit() / RS485_EndTransmit() for use
 *                 with DMA or interrupt-driven UART.
 *
 * Usage example (blocking):
 * @code
 *   static RS485_Handle_t rs485;
 *
 *   void App_Init(void) {
 *       RS485_Init(&rs485, GPIOA, 1, GPIOA, 0, USART1);
 *   }
 *
 *   void App_Send(const uint8_t *data, uint16_t len) {
 *       RS485_SendBlocking(&rs485, data, len, 100);
 *   }
 * @endcode
 *
 * Usage example (DMA / interrupt):
 * @code
 *   void StartDMATransfer(const uint8_t *data, uint16_t len) {
 *       RS485_BeginTransmit(&rs485);
 *       HAL_UART_Transmit_DMA(&huart1, data, len);
 *   }
 *
 *   void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart) {
 *       if (huart->Instance == USART1) {
 *           RS485_EndTransmit(&rs485);  // Waits for TC, then DE low
 *       }
 *   }
 * @endcode
 */

#ifndef RS485_TC_H
#define RS485_TC_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Platform abstraction                                                */
/* ------------------------------------------------------------------ */

/**
 * @brief Define RS485_PLATFORM_HAL before including to provide your own
 *        GPIO / UART register access macros. Otherwise a minimal
 *        STM32 HAL-compatible shim is expected.
 *
 * You must provide:
 *   - RS485_GPIO_WritePin(port, pin, state)
 *   - RS485_USART_WaitTC(usart, timeout_ms)  -> 0 on success, -1 on timeout
 */

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Maximum number of poll iterations while waiting for TC. */
#ifndef RS485_TC_TIMEOUT_DEFAULT
#define RS485_TC_TIMEOUT_DEFAULT  100u
#endif

/** Enable parameter null-checks. */
#ifndef RS485_NASSERT
#include <assert.h>
#define RS485_ASSERT(x)  assert(x)
#else
#define RS485_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/** Opaque GPIO port type — redefine for your platform. */
typedef void rs485_gpio_port_t;

/** Opaque USART peripheral type — redefine for your platform. */
typedef void rs485_usart_t;

/**
 * @brief RS485 direction-control handle.
 *
 * Holds the DE/RE pin assignments and the associated USART peripheral.
 * When RE is tied to DE on the transceiver board, set re_port = NULL
 * and re_pin = 0; the driver will only toggle DE (which also controls
 * /RE through the hardware tie).
 */
typedef struct {
    rs485_gpio_port_t *de_port;   /**< GPIO port for DE pin.            */
    uint16_t           de_pin;    /**< GPIO pin number for DE.          */
    rs485_gpio_port_t *re_port;   /**< GPIO port for /RE pin (NULL if tied to DE). */
    uint16_t           re_pin;    /**< GPIO pin number for /RE.         */
    rs485_usart_t     *usart;     /**< USART peripheral for TC polling. */
    bool               inited;    /**< Initialization flag.             */
    volatile bool      transmitting; /**< True while DE is asserted.    */
} RS485_Handle_t;

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define RS485_OK            0    /**< Success.                          */
#define RS485_ERR_PARAM    -1    /**< Invalid parameter.                */
#define RS485_ERR_TIMEOUT  -2    /**< TC flag did not set in time.      */
#define RS485_ERR_BUSY     -3    /**< Transmission already in progress. */

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Initialize the RS485 direction-control handle.
 *
 * Configures the handle and sets DE low (receive mode).
 * The GPIO pins must already be configured as outputs by the caller.
 *
 * @param h       Pointer to handle.
 * @param de_port GPIO port for DE pin.
 * @param de_pin  Pin number for DE.
 * @param re_port GPIO port for /RE, or NULL if tied to DE.
 * @param re_pin  Pin number for /RE, or 0 if tied to DE.
 * @param usart   USART peripheral instance (for TC flag access).
 * @return RS485_OK on success, RS485_ERR_PARAM on invalid arguments.
 */
int RS485_Init(RS485_Handle_t *h,
               rs485_gpio_port_t *de_port, uint16_t de_pin,
               rs485_gpio_port_t *re_port, uint16_t re_pin,
               rs485_usart_t *usart);

/**
 * @brief Assert DE (and de-assert /RE) to enter transmit mode.
 *
 * Call this BEFORE writing data to the UART (or starting DMA).
 *
 * @param h Pointer to handle.
 * @return RS485_OK or RS485_ERR_BUSY if already transmitting.
 */
int RS485_BeginTransmit(RS485_Handle_t *h);

/**
 * @brief Wait for TC flag, then de-assert DE (return to receive mode).
 *
 * @note This function MUST be called after the last byte has been
 *       written to the UART. It polls the USART TC flag and only
 *       pulls DE low after TC is set, guaranteeing the last byte
 *       (including stop bits) has been fully shifted out.
 *
 * @param h Pointer to handle.
 * @return RS485_OK on success, RS485_ERR_TIMEOUT if TC never sets.
 */
int RS485_EndTransmit(RS485_Handle_t *h);

/**
 * @brief Send a buffer in blocking mode with automatic DE/TC handling.
 *
 * @param h          Pointer to handle.
 * @param data       Pointer to data buffer.
 * @param length     Number of bytes to send.
 * @param timeout_ms Timeout in milliseconds for TC wait.
 * @return RS485_OK on success, or a negative error code.
 */
int RS485_SendBlocking(RS485_Handle_t *h,
                       const uint8_t *data, uint16_t length,
                       uint32_t timeout_ms);

/**
 * @brief Check if the RS485 bus is currently in transmit mode.
 *
 * @param h Pointer to handle.
 * @return true if DE is asserted, false otherwise.
 */
bool RS485_IsTransmitting(const RS485_Handle_t *h);

#ifdef __cplusplus
}
#endif

#endif /* RS485_TC_H */
