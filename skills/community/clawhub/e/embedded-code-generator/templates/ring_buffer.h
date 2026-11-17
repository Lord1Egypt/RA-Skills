/**
 * @file ring_buffer.h
 * @brief ISR-safe FIFO ring buffer for embedded systems.
 *
 * Design: Single-Producer / Single-Consumer (SPSC) lock-free queue.
 * The producer (writer) only modifies @p head, and the consumer
 * (reader) only modifies @p tail.  Each index is declared volatile
 * and accessed with a compiler barrier to prevent reordering.
 *
 * ISR safety:
 *   - RB_Push()    may be called from an ISR (producer).
 *   - RB_Pop()     may be called from the main loop (consumer).
 *   - RB_Peek()    read-only, safe in consumer context.
 *   - RB_IsEmpty() / RB_IsFull() / RB_Count() / RB_Available()
 *     are safe from either context on 32-bit platforms where
 *     aligned 32-bit reads are atomic.
 *   - RB_Init()    is NOT ISR-safe; call once during initialization.
 *   - RB_Reset()   is NOT ISR-safe; ensure no concurrent access.
 *
 * @note On architectures where 32-bit reads are not atomic
 *       (e.g., 8-bit AVR), disable interrupts around multi-byte
 *       access to head/tail. A RB_EnterCritical() / RB_ExitCritical()
 *       hook is provided for this purpose.
 *
 * Full-buffer policy is configurable:
 *   - RB_STRATEGY_REJECT (default): Push returns RB_ERR_FULL.
 *   - RB_STRATEGY_OVERWRITE:       Push overwrites the oldest data.
 *
 * Usage example:
 * @code
 *   static uint8_t uart_rx_buf[128];
 *   static RB_Handle_t uart_rx_rb;
 *
 *   void UART_Init(void) {
 *       RB_Init(&uart_rx_rb, uart_rx_buf, sizeof(uart_rx_buf));
 *   }
 *
 *   void USART1_IRQHandler(void) {
 *       uint8_t byte = USART1->DR;
 *       RB_Push(&uart_rx_rb, byte);  // ISR producer
 *   }
 *
 *   void MainLoop(void) {
 *       uint8_t byte;
 *       while (RB_Pop(&uart_rx_rb, &byte) == RB_OK) {
 *           ProcessByte(byte);
 *       }
 *   }
 * @endcode
 */

#ifndef RING_BUFFER_H
#define RING_BUFFER_H

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
 * @brief Element type. Defaults to uint8_t; define RB_ELEM_TYPE before
 *        including to use a different type (e.g., uint16_t, a struct).
 */
#ifndef RB_ELEM_TYPE
#define RB_ELEM_TYPE  uint8_t
#endif

/**
 * @brief Size type for buffer indices. Use uint16_t on 8-bit MCUs to
 *        save RAM; uint32_t on 32-bit MCUs for atomic access.
 */
#ifndef RB_SIZE_TYPE
#define RB_SIZE_TYPE  uint32_t
#endif

/**
 * @brief Full-buffer strategy:
 *   0 = reject new data (default)
 *   1 = overwrite oldest data
 */
#ifndef RB_STRATEGY
#define RB_STRATEGY  0
#endif

#define RB_STRATEGY_REJECT     0
#define RB_STRATEGY_OVERWRITE  1

/**
 * @brief Optional critical-section hooks for non-atomic architectures.
 *
 * If your MCU cannot atomically access RB_SIZE_TYPE variables,
 * define RB_ENTER_CRITICAL() and RB_EXIT_CRITICAL() before including.
 * Example for AVR:
 *   #define RB_ENTER_CRITICAL()  uint8_t sreg = SREG; cli()
 *   #define RB_EXIT_CRITICAL()   SREG = sreg
 */
#ifndef RB_ENTER_CRITICAL
#define RB_ENTER_CRITICAL()  ((void)0)
#define RB_EXIT_CRITICAL()   ((void)0)
#endif

#ifndef RB_NASSERT
#include <assert.h>
#define RB_ASSERT(x)  assert(x)
#else
#define RB_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define RB_OK          0    /**< Operation succeeded.               */
#define RB_ERR_PARAM  -1    /**< Invalid argument (NULL, size 0).   */
#define RB_ERR_FULL   -2    /**< Buffer is full (reject strategy).  */
#define RB_ERR_EMPTY  -3    /**< Buffer is empty.                   */

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/** Element type alias. */
typedef RB_ELEM_TYPE rb_elem_t;

/** Index / size type alias. */
typedef RB_SIZE_TYPE rb_size_t;

/**
 * @brief Ring buffer handle.
 *
 * All fields are private; use the API functions only.
 * head — next write position (producer-owned)
 * tail — next read position  (consumer-owned)
 * count — total elements currently in buffer
 */
typedef struct {
    rb_elem_t *buffer;          /**< Pointer to backing storage.      */
    volatile rb_size_t size;    /**< Buffer capacity (power of 2 recommended). */
    volatile rb_size_t head;    /**< Next write index.                */
    volatile rb_size_t tail;    /**< Next read index.                 */
    volatile rb_size_t count;   /**< Number of elements in buffer.    */
    bool inited;                /**< Initialization flag.             */
} RB_Handle_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Initialize a ring buffer.
 *
 * @param h      Pointer to handle.
 * @param buffer Pointer to pre-allocated storage array.
 * @param size   Capacity in elements (must be > 0; power-of-2 recommended
 *               for fastest index wrap, but not required).
 * @return RB_OK or RB_ERR_PARAM.
 */
int RB_Init(RB_Handle_t *h, rb_elem_t *buffer, rb_size_t size);

/**
 * @brief Push one element into the buffer (producer).
 *
 * Safe to call from an ISR when paired with RB_Pop() in the main loop.
 *
 * @param h    Pointer to handle.
 * @param elem Element to add.
 * @return RB_OK, RB_ERR_FULL (reject strategy), or RB_ERR_PARAM.
 */
int RB_Push(RB_Handle_t *h, rb_elem_t elem);

/**
 * @brief Pop one element from the buffer (consumer).
 *
 * @param h    Pointer to handle.
 * @param elem Output: popped element (may be NULL to just discard).
 * @return RB_OK, RB_ERR_EMPTY, or RB_ERR_PARAM.
 */
int RB_Pop(RB_Handle_t *h, rb_elem_t *elem);

/**
 * @brief Peek at the oldest element without removing it.
 *
 * @param h    Pointer to handle.
 * @param elem Output: element at the front.
 * @return RB_OK, RB_ERR_EMPTY, or RB_ERR_PARAM.
 */
int RB_Peek(const RB_Handle_t *h, rb_elem_t *elem);

/**
 * @brief Check if buffer is empty.
 * @return true if empty, false otherwise.
 */
bool RB_IsEmpty(const RB_Handle_t *h);

/**
 * @brief Check if buffer is full.
 * @return true if full, false otherwise.
 */
bool RB_IsFull(const RB_Handle_t *h);

/**
 * @brief Get number of elements currently in the buffer.
 *
 * Safe from either context when rb_size_t access is atomic.
 */
rb_size_t RB_Count(const RB_Handle_t *h);

/**
 * @brief Get number of free slots.
 */
rb_size_t RB_Available(const RB_Handle_t *h);

/**
 * @brief Reset buffer to empty state.
 *
 * @warning NOT ISR-safe. Call only when no concurrent access is
 *          possible (e.g., during initialization or with interrupts
 *          disabled).
 */
void RB_Reset(RB_Handle_t *h);

#ifdef __cplusplus
}
#endif

#endif /* RING_BUFFER_H */
