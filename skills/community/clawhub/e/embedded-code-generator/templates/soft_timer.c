/**
 * @file soft_timer.c
 * @brief Polling software timers for a bare-metal main loop.
 *
 * See soft_timer.h for the full design contract.
 */

#include "soft_timer.h"

/* ------------------------------------------------------------------ */
/* Internal types                                                      */
/* ------------------------------------------------------------------ */

typedef struct {
    ST_Callback_t cb;          /**< User callback (NULL = free slot).   */
    void *user;                /**< Opaque user pointer.                */
    uint32_t period;           /**< Reload period in ticks.             */
    uint32_t deadline;         /**< Next expiry tick.                   */
    ST_Mode_t mode;            /**< Once or periodic.                   */
    bool active;               /**< Running state.                      */
    bool in_round;             /**< Already handled in current pass.    */
} ST_Slot_t;

static ST_Slot_t g_slots[ST_MAX_TIMERS];

/** Signed difference, wrap-around safe: >0 means deadline in future. */
static int32_t ticks_left(uint32_t now, uint32_t deadline)
{
    return (int32_t)(deadline - now);
}

void ST_Init(void)
{
    uint32_t i;
    for (i = 0u; i < ST_MAX_TIMERS; i++) {
        g_slots[i].cb      = NULL;
        g_slots[i].user    = NULL;
        g_slots[i].period  = 0u;
        g_slots[i].deadline = 0u;
        g_slots[i].mode    = ST_MODE_ONCE;
        g_slots[i].active  = false;
        g_slots[i].in_round = false;
    }
}

uint32_t ST_Add(uint32_t now, uint32_t period, ST_Mode_t mode,
                ST_Callback_t cb, void *user)
{
    uint32_t i;

    if ((cb == NULL) || (period == 0u) ||
        ((mode != ST_MODE_ONCE) && (mode != ST_MODE_PERIODIC))) {
        return ST_INVALID_ID;
    }
    for (i = 0u; i < ST_MAX_TIMERS; i++) {
        if (g_slots[i].cb == NULL) {
            g_slots[i].cb      = cb;
            g_slots[i].user    = user;
            g_slots[i].period  = period;
            g_slots[i].mode    = mode;
            g_slots[i].deadline = now + period;   /* armed immediately */
            g_slots[i].active  = true;
            g_slots[i].in_round = false;
            return i;
        }
    }
    return ST_INVALID_ID;
}

bool ST_Stop(uint32_t id)
{
    if ((id >= ST_MAX_TIMERS) || (g_slots[id].cb == NULL)) {
        return false;
    }
    if (g_slots[id].active) {
        g_slots[id].active = false;
        return true;
    }
    return false;
}

bool ST_Start(uint32_t id, uint32_t now)
{
    if ((id >= ST_MAX_TIMERS) || (g_slots[id].cb == NULL)) {
        return false;
    }
    g_slots[id].deadline = now + g_slots[id].period;
    g_slots[id].in_round = false;
    g_slots[id].active   = true;
    return true;
}

bool ST_IsActive(uint32_t id)
{
    if ((id >= ST_MAX_TIMERS) || (g_slots[id].cb == NULL)) {
        return false;
    }
    return g_slots[id].active;
}

uint32_t ST_GetRemaining(uint32_t id, uint32_t now)
{
    int32_t left;

    if ((id >= ST_MAX_TIMERS) || (g_slots[id].cb == NULL) ||
        (!g_slots[id].active)) {
        return 0u;
    }
    left = ticks_left(now, g_slots[id].deadline);
    return (left > 0) ? (uint32_t)left : 0u;
}

uint32_t ST_Process(uint32_t now)
{
    uint32_t fired = 0u;
    uint32_t i;

    /* Pass 1: mark due timers, reload or deactivate them. Callbacks
     * are executed in pass 2 so a callback that stops/restarts timers
     * (including its own) cannot corrupt the scan. */
    for (i = 0u; i < ST_MAX_TIMERS; i++) {
        g_slots[i].in_round = false;
        if (g_slots[i].cb == NULL || !g_slots[i].active) {
            continue;
        }
        if (ticks_left(now, g_slots[i].deadline) > 0) {
            continue;   /* not due yet */
        }
        if (g_slots[i].mode == ST_MODE_PERIODIC) {
            g_slots[i].deadline = now + g_slots[i].period;
        } else {
            g_slots[i].active = false;  /* one-shot: auto-deactivate */
        }
        g_slots[i].in_round = true;
    }

    /* Pass 2: execute callbacks. */
    for (i = 0u; i < ST_MAX_TIMERS; i++) {
        if (g_slots[i].in_round) {
            g_slots[i].in_round = false;
            g_slots[i].cb(i, g_slots[i].user);
            fired++;
        }
    }
    return fired;
}
