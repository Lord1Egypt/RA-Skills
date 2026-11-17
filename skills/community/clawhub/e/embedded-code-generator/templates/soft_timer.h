/**
 * @file soft_timer.h
 * @brief Polling software timers for a bare-metal main loop.
 *
 * Non-preemptive timers driven by a millisecond tick you supply.
 * No ISR usage, no dynamic memory, no dependency on any RTOS:
 * call ST_Process() from the main loop (or a low-priority task) and
 * feed it the current tick (SysTick counter, HAL_GetTick(), ...).
 *
 * Features:
 *   - One-shot and periodic modes; one-shot timers deactivate
 *     themselves after firing.
 *   - Wrap-around safe: tick math uses signed difference, correct
 *     across the 32-bit rollover at ~49.7 days.
 *   - A callback may safely call ST_Stop() on its own timer id
 *     (already processed for the current round) and may start/stop
 *     other timers.
 *   - Callbacks run in ST_Process() context — keep them short; do
 *     not call blocking APIs inside a callback.
 *
 * Usage example:
 * @code
 *   static void led_blink(uint32_t id, void *user);
 *
 *   void app_init(void) {
 *       ST_Init();
 *       ST_Add(500u, ST_MODE_PERIODIC, led_blink, NULL);
 *   }
 *
 *   void main_loop(void) {
 *       ST_Process(HAL_GetTick());
 *       // ... other work ...
 *   }
 * @endcode
 */

#ifndef SOFT_TIMER_H
#define SOFT_TIMER_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Maximum number of concurrently registered timers. */
#ifndef ST_MAX_TIMERS
#define ST_MAX_TIMERS  8u
#endif

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/** Timer mode: fire once, or reload every period. */
typedef enum {
    ST_MODE_ONCE = 0,     /**< Fire a single time, then deactivate.   */
    ST_MODE_PERIODIC = 1  /**< Reload after every firing.             */
} ST_Mode_t;

/** Timer callback: @p id is the timer handle, @p user the user pointer. */
typedef void (*ST_Callback_t)(uint32_t id, void *user);

/** Invalid id returned by ST_Add() when the pool is full. */
#define ST_INVALID_ID  0xFFFFFFFFu

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Reset the timer pool (all timers stopped and freed).
 * @note Call once before adding timers; not reentrant.
 */
void ST_Init(void);

/**
 * @brief Register a timer and start it immediately.
 *
 * @param now     Current system tick in ms (deadline = now + period).
 * @param period  Reload period in ticks (must be > 0).
 * @param mode    ST_MODE_ONCE or ST_MODE_PERIODIC.
 * @param cb      Callback executed when the timer expires.
 * @param user    Opaque pointer passed back to the callback.
 * @return Timer id (usable with ST_Stop/ST_Start), or ST_INVALID_ID
 *         if the pool is full or arguments are invalid.
 */
uint32_t ST_Add(uint32_t now, uint32_t period, ST_Mode_t mode,
                ST_Callback_t cb, void *user);

/**
 * @brief Stop a timer (it stays registered; restart with ST_Start()).
 * @return true if the timer existed and was active.
 */
bool ST_Stop(uint32_t id);

/**
 * @brief Restart a stopped timer with its original period/mode.
 *        Deadline is stamped as now + period immediately.
 * @param now  Current system tick in ms (same time base as ST_Process).
 * @return true on success.
 */
bool ST_Start(uint32_t id, uint32_t now);

/**
 * @brief True if the timer id is valid and currently running.
 */
bool ST_IsActive(uint32_t id);

/**
 * @brief Ticks until expiry (0 if already due or inactive).
 */
uint32_t ST_GetRemaining(uint32_t id, uint32_t now);

/**
 * @brief Drive all timers. Call periodically from the main loop.
 *
 * @param now  Current system tick in ms (any uint32_t value; wrap-safe).
 * @return Number of callbacks executed during this call.
 */
uint32_t ST_Process(uint32_t now);

#ifdef __cplusplus
}
#endif

#endif /* SOFT_TIMER_H */
