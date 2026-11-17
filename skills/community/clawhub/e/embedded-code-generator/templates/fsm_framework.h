/**
 * @file fsm_framework.h
 * @brief Table-driven finite state machine framework with guard
 *        conditions, suited for key decoding, protocol parsers, mode
 *        managers and any (state, event) driven logic.
 *
 * Design: Transitions live in a const table (flash-friendly, no dynamic
 * memory). Each entry maps (source, event) -> target, with optional
 * guard and action callbacks. Dispatch rules:
 *
 *   1. The first table entry matching (current state, event) whose guard
 *      passes (or has no guard) is taken.
 *   2. If entries match but every guard fails -> FSM_ERR_GUARD, state
 *      unchanged. This enables guard chaining: list the same
 *      (state, event) pair several times with different guards, e.g.
 *      "long press" guarded by time > threshold, then "short press".
 *   3. If no entry matches at all -> FSM_ERR_NO_TRANS, state unchanged.
 *   4. On a taken transition the callbacks run in this order:
 *      on_exit(old) -> action -> on_entry(new).
 *
 * Usage example (key decoder: IDLE -> DEBOUNCE -> PRESSED -> REPEAT):
 * @code
 *   static bool Guard_LongPress(FSM_Machine_t *m, FSM_Event_t ev);
 *   static void Act_StartBeep(FSM_Machine_t *m, FSM_Event_t ev);
 *
 *   static const FSM_Transition_t kTable[] = {
 *       { ST_IDLE,     EV_PRESS,  ST_DEBOUNCE, NULL,             NULL },
 *       { ST_DEBOUNCE, EV_RELEASE, ST_IDLE,    NULL,             NULL },
 *       { ST_DEBOUNCE, EV_TICK,   ST_PRESSED,  NULL,             NULL },
 *       { ST_PRESSED,  EV_RELEASE, ST_IDLE,    NULL,             Act_ShortPress },
 *       { ST_PRESSED,  EV_TICK,   ST_PRESSED,  Guard_LongPress,  Act_LongPress },
 *   };
 *
 *   static const FSM_Config_t kCfg = {
 *       .table = kTable, .count = 5u, .initial = ST_IDLE,
 *       .on_entry = NULL, .on_exit = NULL, .user_data = &g_key_ctx,
 *   };
 *
 *   FSM_Machine_t key_fsm;
 *   FSM_Init(&key_fsm, &kCfg);
 *   ...
 *   (void)FSM_Dispatch(&key_fsm, EV_PRESS);   // feed events from main loop
 * @endcode
 *
 * @note Not ISR-safe by design: call FSM_Dispatch() from a single context.
 *       Event queueing between ISR and task is the application's job.
 * @note Event IDs are per-machine; the same FSM_Event_t value can mean
 *       different things in different tables.
 */

#ifndef FSM_FRAMEWORK_H
#define FSM_FRAMEWORK_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Reserved id for "no state" (returned before FSM_Init succeeds). */
#define FSM_STATE_NONE   ((FSM_State_t)-1)

#ifndef FSM_NASSERT
#include <assert.h>
#define FSM_ASSERT(x)  assert(x)
#else
#define FSM_ASSERT(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define FSM_OK            0    /**< Transition taken.                     */
#define FSM_ERR_PARAM    -1    /**< Invalid argument (NULL machine etc.). */
#define FSM_ERR_NO_TRANS -2    /**< No (state, event) rule matched.       */
#define FSM_ERR_GUARD    -3    /**< Rule(s) matched but every guard failed. */

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

typedef int16_t FSM_State_t;    /**< State id, user-defined enumeration.  */
typedef uint8_t FSM_Event_t;    /**< Event id, user-defined enumeration.  */

struct FSM_Machine_s;

/**
 * @brief Guard: return true to allow the transition to be taken.
 * May inspect machine state / user_data (timers, counters, inputs).
 */
typedef bool (*FSM_GuardFn)(struct FSM_Machine_s *m, FSM_Event_t ev);

/**
 * @brief Action: runs after the guard passes, before on_entry(new).
 */
typedef void (*FSM_ActionFn)(struct FSM_Machine_s *m, FSM_Event_t ev);

/**
 * @brief One transition rule: (source, event) -> target.
 */
typedef struct {
    FSM_State_t  source;   /**< Source state.                        */
    FSM_Event_t  event;    /**< Triggering event.                    */
    FSM_State_t  target;   /**< Destination state.                   */
    FSM_GuardFn  guard;    /**< Optional guard, NULL = unconditional. */
    FSM_ActionFn action;   /**< Optional action, NULL = none.        */
} FSM_Transition_t;

/**
 * @brief Static machine configuration (recommend const, in flash).
 */
typedef struct {
    const FSM_Transition_t *table;     /**< Rule array, may be NULL (count 0). */
    uint16_t                count;     /**< Number of rules.                   */
    FSM_State_t             initial;   /**< State after FSM_Init/FSM_Reset.    */
    FSM_ActionFn            on_entry;  /**< Optional, called on new state.     */
    FSM_ActionFn            on_exit;   /**< Optional, called on old state.     */
    void                   *user_data; /**< Opaque context for guards/actions. */
} FSM_Config_t;

/**
 * @brief Machine instance (RAM): one per concurrent FSM.
 */
typedef struct FSM_Machine_s {
    const FSM_Config_t *cfg;          /**< Bound configuration.       */
    FSM_State_t         state;        /**< Current state.             */
    uint32_t            transitions;  /**< Successful transition count. */
    uint8_t             inited;       /**< FSM_Init() done.           */
} FSM_Machine_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Bind configuration and enter the initial state.
 *
 * on_entry(initial) is invoked (if configured) but does not count as a
 * transition.
 *
 * @param m    Machine instance (must not be NULL).
 * @param cfg  Configuration (must not be NULL).
 * @return FSM_OK or FSM_ERR_PARAM.
 */
int FSM_Init(FSM_Machine_t *m, const FSM_Config_t *cfg);

/**
 * @brief Feed one event to the machine (see dispatch rules in header).
 *
 * @param m   Machine instance (must not be NULL, must be initialised).
 * @param ev  Event id.
 * @return FSM_OK, FSM_ERR_NO_TRANS, FSM_ERR_GUARD or FSM_ERR_PARAM.
 */
int FSM_Dispatch(FSM_Machine_t *m, FSM_Event_t ev);

/**
 * @brief Current state (FSM_STATE_NONE before successful init).
 */
FSM_State_t FSM_GetState(const FSM_Machine_t *m);

/**
 * @brief Force back to the initial state. Runs on_exit(current) and
 *        on_entry(initial) if configured; does not count as a transition.
 *
 * @return FSM_OK or FSM_ERR_PARAM.
 */
int FSM_Reset(FSM_Machine_t *m);

#ifdef __cplusplus
}
#endif

#endif /* FSM_FRAMEWORK_H */
