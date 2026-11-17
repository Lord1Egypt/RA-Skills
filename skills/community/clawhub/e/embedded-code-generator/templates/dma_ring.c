/**
 * @file dma_ring.c
 * @brief Lock-free tracking buffer for DMA circular receive mode.
 *
 * See dma_ring.h for the full design contract.
 */

#include "dma_ring.h"

int DRB_Init(DRB_Handle_t *h, uint8_t *buffer, DRB_SIZE_TYPE size)
{
    if ((h == NULL) || (buffer == NULL) || (size == 0u)) {
        return DRB_ERR_PARAM;
    }
    h->buffer = buffer;
    h->size   = size;
    h->read   = 0u;
    h->write  = 0u;
    h->flags  = 0u;
    h->inited = true;
    return DRB_OK;
}

int DRB_UpdateWriteIndex(DRB_Handle_t *h, DRB_SIZE_TYPE wpos)
{
    DRB_SIZE_TYPE produced;
    DRB_SIZE_TYPE free_before;

    if ((h == NULL) || (!h->inited) || (wpos >= h->size)) {
        return DRB_ERR_PARAM;
    }

    DRB_ENTER_CRITICAL();
    if (wpos != h->write) {
        /* Bytes newly written by DMA since the last update, with wrap.
         * 32-bit casts: DRB_SIZE_TYPE may be 16-bit and both operands
         * would promote to signed int, tripping -Wsign-compare. */
        produced = (DRB_SIZE_TYPE)((wpos >= h->write)
                       ? ((uint32_t)wpos - (uint32_t)h->write)
                       : ((uint32_t)h->size - (uint32_t)h->write + (uint32_t)wpos));

        free_before = (DRB_SIZE_TYPE)((h->write >= h->read)
                          ? ((uint32_t)h->size - (uint32_t)h->write + (uint32_t)h->read - 1u)
                          : ((uint32_t)h->read - (uint32_t)h->write - 1u));

        if (produced > free_before) {
            /* DMA lapped the read position: oldest bytes are gone.
             * Resynchronize to the oldest still-valid byte (one past
             * the new write position) so the consumer never sees
             * wrapped garbage twice. */
            h->flags |= DRB_FLAG_OVERRUN;
            h->read   = (DRB_SIZE_TYPE)((wpos + 1u) % h->size);
        }
        h->write = wpos;
    }
    DRB_EXIT_CRITICAL();
    return DRB_OK;
}

size_t DRB_Read(DRB_Handle_t *h, uint8_t *out, size_t max_len)
{
    size_t n = 0u;

    /* out == NULL with max_len > 0 is legal: drain/discard mode. */
    if ((h == NULL) || (!h->inited)) {
        return (size_t)DRB_ERR_PARAM;
    }

    DRB_ENTER_CRITICAL();
    while ((n < max_len) && (h->read != h->write)) {
        if (out != NULL) {
            out[n] = h->buffer[h->read];
        }
        h->read = (DRB_SIZE_TYPE)((h->read + 1u) % h->size);
        n++;
    }
    DRB_EXIT_CRITICAL();
    return n;
}

size_t DRB_Available(const DRB_Handle_t *h)
{
    DRB_SIZE_TYPE pending;

    if ((h == NULL) || (!h->inited)) {
        return 0u;
    }
    pending = (DRB_SIZE_TYPE)((h->write >= h->read)
                  ? ((uint32_t)h->write - (uint32_t)h->read)
                  : ((uint32_t)h->size - (uint32_t)h->read + (uint32_t)h->write));
    return (size_t)pending;
}

bool DRB_IsEmpty(const DRB_Handle_t *h)
{
    return (DRB_Available(h) == 0u);
}

bool DRB_IsOverrun(const DRB_Handle_t *h)
{
    if ((h == NULL) || (!h->inited)) {
        return false;
    }
    return (h->flags & DRB_FLAG_OVERRUN) != 0u;
}

void DRB_ClearFlags(DRB_Handle_t *h)
{
    if (h != NULL) {
        h->flags = 0u;
    }
}
