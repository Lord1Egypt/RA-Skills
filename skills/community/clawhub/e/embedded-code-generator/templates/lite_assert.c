/**
 * @file lite_assert.c
 * @brief Lightweight assert & fault-record framework implementation.
 *
 * See lite_assert.h for the full design contract.
 *
 * Reentrancy: LA_Fail() may be called from an ISR. Pool writes are
 * index-stable (a record is fully written before its slot is published),
 * so a single-context consumer via LA_GetLast() is safe. Two contexts
 * asserting at the exact same instant can interleave; production
 * images should prefer LA_MODE_HALT/RESET, where execution stops
 * right after recording anyway.
 */

#include "lite_assert.h"

/* ------------------------------------------------------------------ */
/* Internal state                                                      */
/* ------------------------------------------------------------------ */

static LA_Record_t g_pool[LA_MAX_RECORDS];
static uint32_t g_write;     /**< Next slot to write (mod pool size). */
static uint32_t g_count;     /**< Total failures, saturating at 2^32-1. */
static bool g_valid;         /**< At least one record available.      */
static void (*g_reset_hook)(void);

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

void LA_SetResetHook(void (*hook)(void))
{
    g_reset_hook = hook;
}

void LA_Fail(const char *file, uint32_t line, const char *expr)
{
    /* Record first: even in halt/reset modes the evidence must be in
     * memory before execution stops. */
    g_pool[g_write].file  = file;
    g_pool[g_write].expr  = expr;
    g_pool[g_write].line  = line;
    g_write = (g_write + 1u) % LA_MAX_RECORDS;
    g_valid = true;

    if (g_count < 0xFFFFFFFFu) {
        g_count++;
    }

#if (LA_MODE == LA_MODE_HALT)
    LA_HALT_ACTION();
#elif (LA_MODE == LA_MODE_RESET)
    if (g_reset_hook != NULL) {
        g_reset_hook();
    }
    /* No hook installed: degrade to halt so a failing system does
     * not keep running unattended. */
    LA_HALT_ACTION();
#else
    /* LA_MODE_LOG: record and continue. */
#endif
}

uint32_t LA_GetCount(void)
{
    return g_count;
}

bool LA_GetLast(LA_Record_t *out)
{
    uint32_t last;

    if ((out == NULL) || (!g_valid)) {
        return false;
    }
    /* g_write points past the newest slot; without wrap it is slot 0. */
    last = (g_write == 0u) ? (LA_MAX_RECORDS - 1u) : (g_write - 1u);
    out->file  = g_pool[last].file;
    out->expr  = g_pool[last].expr;
    out->line  = g_pool[last].line;
    return true;
}

void LA_Clear(void)
{
    uint32_t i;
    for (i = 0u; i < LA_MAX_RECORDS; i++) {
        g_pool[i].file = NULL;
        g_pool[i].expr = NULL;
        g_pool[i].line = 0u;
    }
    g_write = 0u;
    g_count = 0u;
    g_valid = false;
}
