/**
 * @file key_scan.h
 * @brief Debounced polling key scanner with short / long / repeat events.
 *
 * Scans raw GPIO levels fed in by the caller (one call per key per
 * scan period, typically 1 ms) and emits clean edge events:
 * DOWN (press confirmed), UP (release confirmed), LONG (held past the
 * long-press threshold, once per press) and REPEAT (auto-repeat while
 * still held). The raw level is a plain function argument, so the
 * module is trivially testable and independent of the GPIO API:
 * whatever MCU/framework you use, just pass HAL_GPIO_ReadPin() /
 * gpio_get_level() / digitalRead() results in.
 *
 * Features:
 *   - Time-based debounce for both press and release edges (contact
 *     bounce can also fake a short release while holding a key).
 *   - Wrap-around safe: tick math uses unsigned subtraction, correct
 *     across the 32-bit rollover at ~49.7 days.
 *   - Fully configurable via compile-time macros (debounce time,
 *     long-press time, repeat interval, active level, key count).
 *   - No dynamic memory, no ISR usage: call KS_Update() from the main
 *     loop or a 1 ms tick task.
 *
 * Usage example:
 * @code
 *   #include "key_scan.h"
 *
 *   // Call every 1 ms from SysTick handler main loop / scheduler.
 *   void key_task_1ms(uint32_t tick_now) {
 *       // Key 0: active-low button on PA0.
 *       switch (KS_Update(0u, (uint8_t)HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_0),
 *                         tick_now)) {
 *       case KS_EVT_DOWN:  led_on();  break;               // short press start
 *       case KS_EVT_UP:    beep();    break;               // released (short press)
 *       case KS_EVT_LONG:  enter_setting(); break;         // held >= 1 s
 *       case KS_EVT_REPEAT: value_inc(); break;            // auto-repeat
 *       default: break;                                    // KS_EVT_NONE
 *       }
 *   }
 * @endcode
 *
 * @note Keep KS_DEBOUNCE_TICKS around 20 for a 1 ms scan period
 *       (20 ms, typical mechanical switch spec). Do not call from an
 *       ISR if KS_EVT handlers do more than set flags.
 */

#ifndef KEY_SCAN_H
#define KEY_SCAN_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Maximum number of scanned keys (ids 0 .. KS_MAX_KEYS-1). */
#ifndef KS_MAX_KEYS
#define KS_MAX_KEYS  8u
#endif

/** Debounce time in scan periods for BOTH press and release edges. */
#ifndef KS_DEBOUNCE_TICKS
#define KS_DEBOUNCE_TICKS  20u
#endif

/** Hold time (scan periods) after which a LONG event fires, once. */
#ifndef KS_LONG_PRESS_TICKS
#define KS_LONG_PRESS_TICKS  1000u
#endif

/** Interval (scan periods) between REPEAT events after the LONG one. */
#ifndef KS_REPEAT_TICKS
#define KS_REPEAT_TICKS  200u
#endif

/** Electrical level that means "pressed": 0 = active-low (default,
 *  pull-up + button to GND), 1 = active-high. */
#ifndef KS_ACTIVE_LEVEL
#define KS_ACTIVE_LEVEL  0u
#endif

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/** Scan result for one key on one KS_Update() call. */
typedef enum {
    KS_EVT_NONE = 0,   /**< No state change worth reporting.           */
    KS_EVT_DOWN,       /**< Press confirmed after debounce.            */
    KS_EVT_UP,         /**< Release confirmed after debounce.          */
    KS_EVT_LONG,       /**< Held past KS_LONG_PRESS_TICKS (once/press).*/
    KS_EVT_REPEAT      /**< Auto-repeat while held past LONG.          */
} KS_Event_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Reset all key states (nothing pressed, no pending debounce).
 * @note Call once at startup; not reentrant.
 */
void KS_Init(void);

/**
 * @brief Feed one raw key level and get the resulting event.
 *
 * Call once per scan period (typ. 1 ms) for each key. The level is
 * the RAW electrical level; interpretation as "pressed" depends on
 * KS_ACTIVE_LEVEL. Tick wrap-around is handled internally.
 *
 * @param id        Key index, 0 .. KS_MAX_KEYS-1. Invalid ids return
 *                  KS_EVT_NONE (defensive, no side effects).
 * @param raw_level Raw electrical level of the pin: 0 or 1.
 * @param now       Current tick in scan periods (e.g. ms counter).
 * @return Event for this key on this call (exactly one, may be NONE).
 */
KS_Event_t KS_Update(uint8_t id, uint8_t raw_level, uint32_t now);

/**
 * @brief Query the debounced (stable) pressed state of a key.
 * @param id  Key index; invalid ids return false.
 * @return true while the key is stably pressed (between DOWN and UP).
 */
bool KS_IsPressed(uint8_t id);

#ifdef __cplusplus
}
#endif

#endif /* KEY_SCAN_H */
