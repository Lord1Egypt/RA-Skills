/**
 * @file ring_buffer.c
 * @brief Lock-free SPSC ring buffer implementation.
 *
 * The buffer supports arbitrary sizes (not just powers of 2) using
 * modular arithmetic. For best performance, use a power-of-2 size
 * so the compiler can optimize modulo to bitwise AND.
 *
 * Memory barrier note:
 *   On single-core MCUs, a compiler barrier is sufficient because
 *   the ISR cannot preempt in the middle of an aligned 32-bit read
 *   on ARM Cortex-M. For multi-core or non-atomic architectures,
 *   use the RB_ENTER_CRITICAL / RB_EXIT_CRITICAL hooks.
 */

#include "ring_buffer.h"

/* ------------------------------------------------------------------ */
/* Compiler barrier (prevents instruction reordering)                  */
/* ------------------------------------------------------------------ */

#if defined(__GNUC__) || defined(__clang__)
#define RB_BARRIER()  __asm__ __volatile__("" ::: "memory")
#elif defined(__CC_ARM)
#define RB_BARRIER()  __memory_changed()
#else
#define RB_BARRIER()  ((void)0)
#endif

/* ================================================================== */
/* Public API                                                          */
/* ================================================================== */

int RB_Init(RB_Handle_t *h, rb_elem_t *buffer, rb_size_t size)
{

    if (h == NULL || buffer == NULL || size == 0u) {
        return RB_ERR_PARAM;
    }

    h->buffer = buffer;
    h->size   = size;
    h->head   = 0u;
    h->tail   = 0u;
    h->count  = 0u;
    h->inited = true;

    return RB_OK;
}

int RB_Push(RB_Handle_t *h, rb_elem_t elem)
{

    if (h == NULL || !h->inited) {
        return RB_ERR_PARAM;
    }

    RB_ENTER_CRITICAL();

    if (h->count >= h->size) {
        /* Buffer is full. */
#if RB_STRATEGY == RB_STRATEGY_OVERWRITE
        /* Overwrite oldest: advance tail (discard one element). */
        h->tail = (h->tail + 1u) % h->size;
        h->count--;
#else
        RB_EXIT_CRITICAL();
        return RB_ERR_FULL;
#endif
    }

    /* Write data at head position. */
    h->buffer[h->head] = elem;

    /*
     * Barrier: ensure the data is written BEFORE updating head.
     * This prevents the consumer from seeing a stale/garbage element
     * if interrupts fire between the data write and head update.
     */
    RB_BARRIER();

    h->head = (h->head + 1u) % h->size;
    h->count++;

    RB_EXIT_CRITICAL();

    return RB_OK;
}

int RB_Pop(RB_Handle_t *h, rb_elem_t *elem)
{

    if (h == NULL || !h->inited) {
        return RB_ERR_PARAM;
    }

    RB_ENTER_CRITICAL();

    if (h->count == 0u) {
        RB_EXIT_CRITICAL();
        return RB_ERR_EMPTY;
    }

    /* Read data at tail position. */
    if (elem != NULL) {
        *elem = h->buffer[h->tail];
    }

    RB_BARRIER();

    h->tail = (h->tail + 1u) % h->size;
    h->count--;

    RB_EXIT_CRITICAL();

    return RB_OK;
}

int RB_Peek(const RB_Handle_t *h, rb_elem_t *elem)
{

    if (h == NULL || !h->inited || elem == NULL) {
        return RB_ERR_PARAM;
    }

    RB_ENTER_CRITICAL();

    if (h->count == 0u) {
        RB_EXIT_CRITICAL();
        return RB_ERR_EMPTY;
    }

    *elem = h->buffer[h->tail];

    RB_EXIT_CRITICAL();

    return RB_OK;
}

bool RB_IsEmpty(const RB_Handle_t *h)
{
    bool empty;


    if (h == NULL || !h->inited) {
        return true;
    }

    RB_ENTER_CRITICAL();
    empty = (h->count == 0u);
    RB_EXIT_CRITICAL();

    return empty;
}

bool RB_IsFull(const RB_Handle_t *h)
{
    bool full;


    if (h == NULL || !h->inited) {
        return false;
    }

    RB_ENTER_CRITICAL();
    full = (h->count >= h->size);
    RB_EXIT_CRITICAL();

    return full;
}

rb_size_t RB_Count(const RB_Handle_t *h)
{
    rb_size_t count;


    if (h == NULL || !h->inited) {
        return 0u;
    }

    RB_ENTER_CRITICAL();
    count = h->count;
    RB_EXIT_CRITICAL();

    return count;
}

rb_size_t RB_Available(const RB_Handle_t *h)
{
    rb_size_t avail;


    if (h == NULL || !h->inited) {
        return 0u;
    }

    RB_ENTER_CRITICAL();
    avail = h->size - h->count;
    RB_EXIT_CRITICAL();

    return avail;
}

void RB_Reset(RB_Handle_t *h)
{

    if (h == NULL) {
        return;
    }

    RB_ENTER_CRITICAL();
    h->head  = 0u;
    h->tail  = 0u;
    h->count = 0u;
    RB_EXIT_CRITICAL();
}
