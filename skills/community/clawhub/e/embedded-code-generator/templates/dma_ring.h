/**
 * @file dma_ring.h
 * @brief Lock-free tracking buffer for DMA circular receive mode.
 *
 * Typical use: UART/SPI/ADC DMA in circular mode writes into a RAM
 * buffer continuously; the CPU must fetch the new data without ever
 * stopping the DMA stream. This module tracks the hardware write
 * index (derived from the DMA counter by the caller) and exposes a
 * safe read side with wrap-around handling.
 *
 * Design:
 *   - The DMA engine is the single producer: it owns the buffer and
 *     advances its own write position. This module never writes into
 *     the buffer.
 *   - The CPU is the single consumer: it calls DRB_UpdateWriteIndex()
 *     with the current hardware write position (e.g.,
 *     @c size - __HAL_DMA_GET_COUNTER(&hdma) on STM32), then reads
 *     the newly arrived bytes with DRB_Read().
 *   - Single-producer/single-consumer by contract: UpdateWriteIndex()
 *     and Read() must run in the same context (e.g., the UART idle
 *     ISR or one dedicated task). If they run in different contexts
 *     on an MCU where 32-bit loads are not atomic, wrap the calls in
 *     the critical-section hooks DRB_ENTER_CRITICAL()/DRB_EXIT_CRITICAL().
 *
 * Overflow semantics:
 *   If the DMA laps the read position (a full buffer + extra data
 *   arrived between two updates), the oldest data is lost by the
 *   hardware. DRB_UpdateWriteIndex() detects this and sets the
 *   DRB_FLAG_OVERRUN flag; DRB_Read() then resynchronizes by skipping
 *   the unread region instead of returning garbage.
 *
 * Usage example:
 * @code
 *   static uint8_t rx_dma_buf[256];
 *   static DRB_Handle_t rx;
 *
 *   void uart_init(void) { DRB_Init(&rx, rx_dma_buf, sizeof(rx_dma_buf)); }
 *
 *   void uart_idle_isr(void) {
 *       uint16_t wpos = sizeof(rx_dma_buf)
 *                     - __HAL_DMA_GET_COUNTER(&huart1.hdmarx);
 *       DRB_UpdateWriteIndex(&rx, wpos);
 *       uint8_t chunk[32];
 *       size_t n;
 *       while ((n = DRB_Read(&rx, chunk, sizeof(chunk))) > 0u) {
 *           protocol_feed(chunk, n);
 *       }
 *   }
 * @endcode
 */

#ifndef DMA_RING_H
#define DMA_RING_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/**
 * @brief Size type for indices. uint16_t is enough for buffers up to
 *        65535 bytes and saves RAM; uint32_t on huge buffers.
 */
#ifndef DRB_SIZE_TYPE
#define DRB_SIZE_TYPE  uint16_t
#endif

/**
 * @brief Optional critical-section hooks for non-atomic architectures.
 */
#ifndef DRB_ENTER_CRITICAL
#define DRB_ENTER_CRITICAL()  ((void)0)
#define DRB_EXIT_CRITICAL()   ((void)0)
#endif

#ifndef DRB_NASSERT
#include <assert.h>
#define DRB_ASSERT(x)  assert(x)
#else
#define DRB_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Return codes and flags                                              */
/* ------------------------------------------------------------------ */

#define DRB_OK            0    /**< Operation succeeded.                  */
#define DRB_ERR_PARAM    -1    /**< Invalid argument (NULL, size 0).      */
#define DRB_ERR_EMPTY    -2    /**< No new data since last read.          */

#define DRB_FLAG_OVERRUN 0x1u  /**< DMA lapped the read position; oldest
                                    data was overwritten by hardware.    */

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/**
 * @brief DMA ring tracking handle. All fields are private.
 */
typedef struct {
    uint8_t *buffer;               /**< Backing storage (DMA target).   */
    DRB_SIZE_TYPE size;            /**< Buffer capacity in bytes.       */
    volatile DRB_SIZE_TYPE read;   /**< Next byte to be read (CPU-owned). */
    volatile DRB_SIZE_TYPE write;  /**< Last known DMA write position.  */
    volatile uint32_t flags;       /**< DRB_FLAG_xxx (sticky, user clears). */
    bool inited;
} DRB_Handle_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Bind a tracking handle to a DMA target buffer.
 *
 * The buffer must be the exact array configured into the DMA stream
 * (circular mode). Content is not touched.
 *
 * @return DRB_OK or DRB_ERR_PARAM.
 */
int DRB_Init(DRB_Handle_t *h, uint8_t *buffer, DRB_SIZE_TYPE size);

/**
 * @brief Publish the current hardware write position.
 *
 * Call this whenever you want to harvest new data (typically in the
 * UART idle interrupt or a polling tick). @p wpos is the DMA write
 * index in [0, size); on STM32 it is
 * @c size - __HAL_DMA_GET_COUNTER(&hdma).
 *
 * If the DMA lapped the read position, DRB_FLAG_OVERRUN is set and
 * the read index resynchronizes to the oldest still-valid byte.
 *
 * @return DRB_OK or DRB_ERR_PARAM.
 */
int DRB_UpdateWriteIndex(DRB_Handle_t *h, DRB_SIZE_TYPE wpos);

/**
 * @brief Read up to @p max_len newly arrived bytes (contiguous run).
 *
 * Stops at the buffer tail: if more data is pending beyond the wrap,
 * call again. @p out may be NULL to just drain (discard) data.
 *
 * @return Number of bytes actually read (0 if empty), or DRB_ERR_PARAM.
 */
size_t DRB_Read(DRB_Handle_t *h, uint8_t *out, size_t max_len);

/**
 * @brief Bytes pending since the last read (never exceeds capacity).
 */
size_t DRB_Available(const DRB_Handle_t *h);

/**
 * @brief True if no new data since the last read.
 */
bool DRB_IsEmpty(const DRB_Handle_t *h);

/**
 * @brief Sticky overrun flag, set by DRB_UpdateWriteIndex().
 * @return true if the DMA lapped the read position since DRB_Init()
 *         or the last DRB_ClearFlags().
 */
bool DRB_IsOverrun(const DRB_Handle_t *h);

/**
 * @brief Clear sticky flags (call after logging an overrun event).
 */
void DRB_ClearFlags(DRB_Handle_t *h);

#ifdef __cplusplus
}
#endif

#endif /* DMA_RING_H */
