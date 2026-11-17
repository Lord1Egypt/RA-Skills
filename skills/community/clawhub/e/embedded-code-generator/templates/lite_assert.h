/**
 * @file lite_assert.h
 * @brief Lightweight assert & fault-record framework for production
 *        firmware.
 *
 * Standard <assert.h> disappears in NDEBUG builds and hard-halts in
 * debug builds — neither behaviour fits shipped products. This module
 * provides a compile-time configurable policy:
 *
 *   - LA_MODE_LOG   (default): record the failure and keep running.
 *   - LA_MODE_HALT:  record, then call the halt action (default:
 *                    infinite loop; override LA_HALT_ACTION() with
 *                    e.g. __disable_irq(); while(1);).
 *   - LA_MODE_RESET: record, then invoke the user-installed reset
 *                    hook (LA_SetResetHook); without a hook it falls
 *                    back to the halt action.
 *
 * The record pool keeps the most recent LA_MAX_RECORDS failures
 * (oldest overwritten, saturating total counter), queryable from a
 * shell command, console, or debugger memory window — no printf
 * required on the hot path.
 *
 * Usage example:
 * @code
 *   void parse_frame(uint8_t len) {
 *       LA_Assert(len <= FRAME_MAX);   // record & continue in LOG mode
 *       ...
 *   }
 *
 *   void fault_dump(void) {             // called from your console
 *       LA_Record_t rec;
 *       uint32_t n = LA_GetCount();
 *       if (LA_GetLast(&rec)) {
 *           printf("last fault: %s:%u (%s), total=%u\n",
 *                  rec.file, (unsigned)rec.line, rec.expr,
 *                  (unsigned)n);
 *       }
 *   }
 * @endcode
 */

#ifndef LITE_ASSERT_H
#define LITE_ASSERT_H

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
 * @brief Failure policy:
 *   0 = LA_MODE_LOG   record and continue (default)
 *   1 = LA_MODE_HALT  record and halt (LA_HALT_ACTION)
 *   2 = LA_MODE_RESET record and call the reset hook
 */
#ifndef LA_MODE
#define LA_MODE  0
#endif

#define LA_MODE_LOG    0
#define LA_MODE_HALT   1
#define LA_MODE_RESET  2

/** Record pool depth (oldest record is overwritten when full). */
#ifndef LA_MAX_RECORDS
#define LA_MAX_RECORDS  8u
#endif

/**
 * @brief Halt action for LA_MODE_HALT (and RESET without hook).
 * Override before including, e.g.:
 *   #define LA_HALT_ACTION()  do { __disable_irq(); while (1) { } } while (0)
 */
#ifndef LA_HALT_ACTION
#define LA_HALT_ACTION()  do { } while (1)
#endif

/**
 * @brief Source-file label stored in records. Override with a short
 * module name if __FILE__ paths are too long for your record budget.
 */
#ifndef LA_FILE
#define LA_FILE  __FILE__
#endif

#ifndef LA_NASSERT
#include <assert.h>
#define LA_ASSERT_INTERNAL(x)  assert(x)
#else
#define LA_ASSERT_INTERNAL(x)  ((void)0)
#endif

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/** One fault record (values, not pointers — safe after file returns). */
typedef struct {
    const char *file;   /**< Source file label (static storage).      */
    const char *expr;   /**< Stringified condition.                   */
    uint32_t line;      /**< Line number of the failed LA_Assert.     */
} LA_Record_t;

/* ------------------------------------------------------------------ */
/* Core API                                                            */
/* ------------------------------------------------------------------ */

/**
 * @brief Check a condition; on failure run the configured policy.
 *
 * Never disappears in release builds (unlike <assert.h>). With
 * LA_MODE_LOG it returns to the caller after recording.
 */
#define LA_Assert(cond)                                                      \
    ((cond) ? (void)0                                                        \
            : LA_Fail(LA_FILE, (uint32_t)(__LINE__), #cond))

/**
 * @brief Explicitly record a fault (e.g., from a switch default:).
 * Same policy path as LA_Assert.
 */
void LA_Fail(const char *file, uint32_t line, const char *expr);

/** @brief Total number of failures since boot / LA_Clear (saturating). */
uint32_t LA_GetCount(void);

/**
 * @brief Copy the most recent failure record.
 * @return true if any failure has been recorded.
 */
bool LA_GetLast(LA_Record_t *out);

/**
 * @brief Drop all records and reset the counter.
 * @note Not ISR-safe; call from init/console context only.
 */
void LA_Clear(void);

/**
 * @brief Install the reset hook used by LA_MODE_RESET.
 * @param hook  Handler executed after recording (NULL = fall back to
 *              the halt action).
 */
void LA_SetResetHook(void (*hook)(void));

#ifdef __cplusplus
}
#endif

#endif /* LITE_ASSERT_H */
