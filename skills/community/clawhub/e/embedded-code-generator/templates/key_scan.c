/**
 * @file key_scan.c
 * @brief Debounced polling key scanner - implementation.
 *
 * Four-state per-key machine:
 *
 *   IDLE --(active)--> GOING_DOWN --(stable for DEBOUNCE)--> DOWN
 *   DOWN --(inactive)--> GOING_UP --(stable for DEBOUNCE)--> IDLE (UP event)
 *
 * In DOWN state, holding past KS_LONG_PRESS_TICKS fires LONG once and
 * then REPEAT every KS_REPEAT_TICKS. A bounce during GOING_DOWN/UP
 * just returns to the previous stable state (bounce rejection).
 *
 * All durations are measured with unsigned subtraction of the caller's
 * tick, so a 32-bit rollover of @p now is handled correctly.
 */

#include "key_scan.h"

/* Internal stable/debounce states. */
typedef enum {
    KS_S_IDLE = 0,     /**< Stable released.                            */
    KS_S_GOING_DOWN,   /**< Raw level active, not yet debounced.        */
    KS_S_DOWN,         /**< Stable pressed (confirmed).                 */
    KS_S_GOING_UP      /**< Raw level inactive, not yet debounced.      */
} KS_State_t;

typedef struct {
    KS_State_t state;      /**< Current debounce state.                  */
    uint8_t    long_fired; /**< LONG already fired for current press.    */
    uint32_t   t_state;    /**< Tick when current state was entered.     */
    uint32_t   t_press;    /**< Tick when press was confirmed (DOWN).    */
    uint32_t   t_repeat;   /**< Tick when LONG/last REPEAT fired.        */
} KS_KeyState_t;

static KS_KeyState_t ks_keys[KS_MAX_KEYS];

/* Raw level -> "pressed" semantics according to configured polarity. */
static bool ks_is_active(uint8_t raw_level)
{
    return (raw_level != 0u) ? (KS_ACTIVE_LEVEL == 1u) : (KS_ACTIVE_LEVEL == 0u);
}

void KS_Init(void)
{
    uint8_t i;
    for (i = 0u; i < (uint8_t)KS_MAX_KEYS; i++) {
        ks_keys[i].state      = KS_S_IDLE;
        ks_keys[i].long_fired = 0u;
        ks_keys[i].t_state    = 0u;
        ks_keys[i].t_press    = 0u;
        ks_keys[i].t_repeat   = 0u;
    }
}

KS_Event_t KS_Update(uint8_t id, uint8_t raw_level, uint32_t now)
{
    KS_KeyState_t *k;

    if ((uint32_t)id >= (uint32_t)KS_MAX_KEYS) {
        return KS_EVT_NONE; /* defensive: invalid id has no side effects */
    }

    k = &ks_keys[id];

    switch (k->state) {
    case KS_S_IDLE:
        if (ks_is_active(raw_level)) {
            k->state   = KS_S_GOING_DOWN;
            k->t_state = now;
        }
        break;

    case KS_S_GOING_DOWN:
        if (!ks_is_active(raw_level)) {
            k->state = KS_S_IDLE; /* bounce: reject, stay released */
            break;
        }
        if ((uint32_t)(now - k->t_state) >= (uint32_t)KS_DEBOUNCE_TICKS) {
            k->state      = KS_S_DOWN;
            k->t_press    = now;
            k->t_repeat   = now;
            k->long_fired = 0u;
            return KS_EVT_DOWN;
        }
        break;

    case KS_S_DOWN:
        if (!ks_is_active(raw_level)) {
            k->state   = KS_S_GOING_UP;
            k->t_state = now;
            break;
        }
        if ((k->long_fired == 0u) &&
            ((uint32_t)(now - k->t_press) >= (uint32_t)KS_LONG_PRESS_TICKS)) {
            k->long_fired = 1u;
            k->t_repeat   = now;
            return KS_EVT_LONG;
        }
        if ((k->long_fired != 0u) &&
            ((uint32_t)(now - k->t_repeat) >= (uint32_t)KS_REPEAT_TICKS)) {
            k->t_repeat = now;
            return KS_EVT_REPEAT;
        }
        break;

    case KS_S_GOING_UP:
        if (ks_is_active(raw_level)) {
            k->state = KS_S_DOWN; /* bounce while releasing: still held */
            break;
        }
        if ((uint32_t)(now - k->t_state) >= (uint32_t)KS_DEBOUNCE_TICKS) {
            k->state = KS_S_IDLE;
            return KS_EVT_UP;
        }
        break;

    default:
        /* Corrupted state: recover to idle. Should never happen. */
        k->state = KS_S_IDLE;
        break;
    }

    return KS_EVT_NONE;
}

bool KS_IsPressed(uint8_t id)
{
    if ((uint32_t)id >= (uint32_t)KS_MAX_KEYS) {
        return false;
    }
    return (ks_keys[id].state == KS_S_DOWN) || (ks_keys[id].state == KS_S_GOING_UP);
}
