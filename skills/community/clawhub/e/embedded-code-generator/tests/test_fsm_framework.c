/**
 * @file test_fsm_framework.c
 * @brief Key-decoder scenario tests for the table-driven FSM.
 *
 * State model (classic key handling):
 *   IDLE --PRESS--> DEBOUNCE --RELEASE--> IDLE
 *   DEBOUNCE --TICK--> PRESSED
 *   PRESSED --RELEASE--> IDLE        (action: short press)
 *   PRESSED --TICK--> PRESSED        (guard: long press; action: beep)
 *   PRESSED --TICK--> PRESSED        (no guard; action: count tick)
 *
 * Covers: transition firing, callback order (exit -> action -> entry),
 * guard chaining (first passing guard wins), all-guards-fail ->
 * FSM_ERR_GUARD with state preserved, unmatched event -> FSM_ERR_NO_TRANS
 * with state preserved, user_data plumbing, Reset and parameter checks.
 */

#include <stdio.h>
#include <string.h>
#include "fsm_framework.h"

/* ------------------------------------------------------------------ */
/* Check framework                                                     */
/* ------------------------------------------------------------------ */

static int g_total = 0;
static int g_pass  = 0;
static int g_fail  = 0;

#define CHECK(cond, name)                                        \
    do {                                                         \
        g_total++;                                               \
        if (cond) { g_pass++; }                                  \
        else { g_fail++; printf("[FAIL] %s\n", name); }          \
    } while (0)

/* ------------------------------------------------------------------ */
/* Key decoder fixture                                                 */
/* ------------------------------------------------------------------ */

enum { ST_IDLE = 0, ST_DEBOUNCE, ST_PRESSED };
enum { EV_PRESS = 0, EV_RELEASE, EV_TICK };

typedef struct {
    unsigned tick_count;        /* ticks while PRESSED            */
    unsigned long_press_after;  /* long-press threshold (ticks)   */
    unsigned entry_count;
    unsigned exit_count;
    int      last_exit_state;
    int      last_entry_state;
    int      action_old_state[8];  /* machine state seen by action */
    unsigned exit_seen_by_action[8];  /* exit_count at action time    */
    unsigned action_count;
} KeyCtx;

static bool Guard_LongPress(FSM_Machine_t *m, FSM_Event_t ev)
{
    KeyCtx *c = (KeyCtx *)m->cfg->user_data;

    (void)ev;
    return (c->tick_count >= c->long_press_after) ? true : false;
}

static bool Guard_Never(FSM_Machine_t *m, FSM_Event_t ev)
{
    (void)m; (void)ev;
    return false;
}

static void Act_RecordAndCount(FSM_Machine_t *m, FSM_Event_t ev)
{
    KeyCtx *c = (KeyCtx *)m->cfg->user_data;

    (void)ev;
    if (c->action_count < 8u)
    {
        c->action_old_state[c->action_count] = (int)m->state;
        c->exit_seen_by_action[c->action_count] = c->exit_count;
        c->action_count++;
    }
}

static void Act_CountTick(FSM_Machine_t *m, FSM_Event_t ev)
{
    KeyCtx *c = (KeyCtx *)m->cfg->user_data;

    (void)ev;
    c->tick_count++;
}

/* Reset the press timer on the DEBOUNCE->PRESSED edge. Must live in the
 * transition action, NOT in on_entry: self-loops (PRESSED->PRESSED on
 * tick) re-fire on_entry and would wipe the counter every tick. */
static void Act_ResetPressTimer(FSM_Machine_t *m, FSM_Event_t ev)
{
    KeyCtx *c = (KeyCtx *)m->cfg->user_data;

    (void)ev;
    c->tick_count = 0u;
}

static void On_Entry(FSM_Machine_t *m, FSM_Event_t ev)
{
    KeyCtx *c = (KeyCtx *)m->cfg->user_data;

    (void)ev;
    c->entry_count++;
    c->last_entry_state = (int)m->state;
}

static void On_Exit(FSM_Machine_t *m, FSM_Event_t ev)
{
    KeyCtx *c = (KeyCtx *)m->cfg->user_data;

    (void)ev;
    c->exit_count++;
    c->last_exit_state = (int)m->state;
}

static const FSM_Transition_t kKeyTable[] = {
    { ST_IDLE,     EV_PRESS,   ST_DEBOUNCE, NULL,             NULL },
    { ST_DEBOUNCE, EV_RELEASE, ST_IDLE,     NULL,             NULL },
    { ST_DEBOUNCE, EV_TICK,    ST_PRESSED,  NULL,             Act_ResetPressTimer },
    { ST_PRESSED,  EV_RELEASE, ST_IDLE,     NULL,             Act_RecordAndCount },
    /* Guard chain: first passing guard wins. */
    { ST_PRESSED,  EV_TICK,    ST_PRESSED,  Guard_LongPress,  Act_RecordAndCount },
    { ST_PRESSED,  EV_TICK,    ST_PRESSED,  NULL,             Act_CountTick },
};

static const FSM_Config_t kKeyCfg = {
    .table     = kKeyTable,
    .count     = sizeof(kKeyTable) / sizeof(kKeyTable[0]),
    .initial   = ST_IDLE,
    .on_entry  = On_Entry,
    .on_exit   = On_Exit,
    .user_data = NULL,          /* bound per-machine in tests */
};

/* ------------------------------------------------------------------ */
/* Test cases                                                          */
/* ------------------------------------------------------------------ */

int main(void)
{
    FSM_Machine_t fsm;
    FSM_Config_t  cfg;
    KeyCtx        ctx;
    int           rc;

    /* --- parameter checks ----------------------------------------- */
    memset(&fsm, 0, sizeof(fsm));   /* deterministic pre-init state */
    CHECK(FSM_Init(NULL, &kKeyCfg) == FSM_ERR_PARAM, "Init NULL machine rejected");
    CHECK(FSM_Init(&fsm, NULL) == FSM_ERR_PARAM, "Init NULL config rejected");
    CHECK(FSM_Dispatch(&fsm, EV_TICK) == FSM_ERR_PARAM,
          "Dispatch before Init rejected");
    /* Init without user_data but also without callbacks is safe. */
    {
        FSM_Config_t bare = kKeyCfg;

        bare.on_entry  = NULL;
        bare.on_exit   = NULL;
        bare.user_data = NULL;
        CHECK(FSM_Init(&fsm, &bare) == FSM_OK, "Init without callbacks OK");
        CHECK(FSM_Dispatch(&fsm, EV_PRESS) == FSM_OK,
              "unguarded rule works without user_data");
    }
    /* Re-init properly with user_data bound. */
    cfg = kKeyCfg;
    cfg.user_data = &ctx;
    memset(&ctx, 0, sizeof(ctx));
    ctx.long_press_after = 2u;   /* threshold must exist before ticks */
    CHECK(FSM_Init(&fsm, &cfg) == FSM_OK, "re-Init OK");
    CHECK(FSM_GetState(&fsm) == ST_IDLE, "initial state is IDLE");
    CHECK(ctx.entry_count == 1u, "on_entry fired for initial state");
    CHECK(FSM_GetState(NULL) == FSM_STATE_NONE, "GetState(NULL) -> NONE");

    /* --- basic transition + callback order ------------------------ */
    rc = FSM_Dispatch(&fsm, EV_PRESS);
    CHECK(rc == FSM_OK, "IDLE+PRESS transitions");
    CHECK(FSM_GetState(&fsm) == ST_DEBOUNCE, "now in DEBOUNCE");
    CHECK((ctx.exit_count == 1u) && (ctx.last_exit_state == (int)ST_IDLE),
          "on_exit fired for IDLE");
    CHECK((ctx.entry_count == 2u) && (ctx.last_entry_state == (int)ST_DEBOUNCE),
          "on_entry fired for DEBOUNCE");

    /* Unmatched event in DEBOUNCE: RELEASE exists, TICK exists; try
     * PRESS (not wired from DEBOUNCE). */
    rc = FSM_Dispatch(&fsm, EV_PRESS);
    CHECK(rc == FSM_ERR_NO_TRANS, "DEBOUNCE+PRESS unmatched");
    CHECK(FSM_GetState(&fsm) == ST_DEBOUNCE, "state preserved after NO_TRANS");

    /* --- debounce -> pressed -------------------------------------- */
    rc = FSM_Dispatch(&fsm, EV_TICK);
    CHECK((rc == FSM_OK) && (FSM_GetState(&fsm) == ST_PRESSED),
          "DEBOUNCE+TICK -> PRESSED");
    CHECK(ctx.tick_count == 0u, "press timer reset on entry");

    /* --- guard chain: short ticks take the unguarded rule ---------
     * Act_CountTick only counts ticks; Act_RecordAndCount is the only
     * action that increments action_count. */
    rc = FSM_Dispatch(&fsm, EV_TICK);       /* tick 1 */
    CHECK(rc == FSM_OK, "short tick 1 taken by unguarded rule");
    CHECK((ctx.tick_count == 1u) && (ctx.action_count == 0u),
          "CountTick ran (tick=1), LongPress guard skipped");

    rc = FSM_Dispatch(&fsm, EV_TICK);       /* tick 2 */
    CHECK((rc == FSM_OK) && (ctx.tick_count == 2u) && (ctx.action_count == 0u),
          "short tick 2 still unguarded rule");

    /* Third tick: tick_count == 2 >= threshold -> long press. */
    rc = FSM_Dispatch(&fsm, EV_TICK);
    CHECK(rc == FSM_OK, "long-press tick accepted");
    CHECK((ctx.action_count == 1u) && (ctx.tick_count == 2u),
          "LongPress action ran, CountTick did NOT run");
    CHECK((ctx.action_old_state[0] == (int)ST_PRESSED) &&
          (ctx.exit_seen_by_action[0] == ctx.exit_count),
          "action saw pre-transition state, on_exit ran first");

    /* --- short press release path --------------------------------- */
    rc = FSM_Dispatch(&fsm, EV_RELEASE);
    CHECK((rc == FSM_OK) && (FSM_GetState(&fsm) == ST_IDLE),
          "PRESSED+RELEASE -> IDLE");
    CHECK((ctx.action_count == 2u) &&
          (ctx.action_old_state[1] == (int)ST_PRESSED),
          "short-press action saw PRESSED (pre-transition)");

    /* --- all guards fail -> ERR_GUARD, state preserved ------------ */
    {
        static const FSM_Transition_t t[] = {
            { ST_IDLE, EV_TICK, ST_DEBOUNCE, Guard_Never, NULL },
            { ST_IDLE, EV_TICK, ST_PRESSED,  Guard_Never, NULL },
        };
        FSM_Config_t g = { t, 2u, ST_IDLE, NULL, NULL, NULL };

        CHECK(FSM_Init(&fsm, &g) == FSM_OK, "guard-fail fixture init");
        rc = FSM_Dispatch(&fsm, EV_TICK);
        CHECK(rc == FSM_ERR_GUARD, "both guards failing -> ERR_GUARD");
        CHECK(FSM_GetState(&fsm) == ST_IDLE, "state preserved after ERR_GUARD");
    }

    /* --- unmatched event with non-empty table --------------------- */
    CHECK(FSM_Dispatch(&fsm, EV_PRESS) == FSM_ERR_NO_TRANS,
          "unmatched event -> ERR_NO_TRANS");

    /* --- empty / NULL table --------------------------------------- */
    {
        FSM_Config_t e = { NULL, 0u, ST_IDLE, NULL, NULL, NULL };

        CHECK(FSM_Init(&fsm, &e) == FSM_OK, "empty table init");
        CHECK(FSM_Dispatch(&fsm, EV_TICK) == FSM_ERR_NO_TRANS,
              "empty table -> ERR_NO_TRANS");
    }

    /* --- reset ----------------------------------------------------- */
    cfg = kKeyCfg;
    cfg.user_data = &ctx;
    memset(&ctx, 0, sizeof(ctx));
    (void)FSM_Init(&fsm, &cfg);
    (void)FSM_Dispatch(&fsm, EV_PRESS);
    (void)FSM_Dispatch(&fsm, EV_TICK);      /* now PRESSED */
    {
        uint32_t before = fsm.transitions;

        rc = FSM_Reset(&fsm);
        CHECK((rc == FSM_OK) && (FSM_GetState(&fsm) == ST_IDLE),
              "Reset returns to initial state");
        CHECK(fsm.transitions == before, "Reset does not count as transition");
        CHECK(ctx.last_exit_state == (int)ST_PRESSED,
              "Reset fired on_exit for PRESSED");
        CHECK(ctx.last_entry_state == (int)ST_IDLE,
              "Reset fired on_entry for IDLE");
    }
    /* Table integrity: const table survived the dispatch storms. */
    CHECK((kKeyCfg.count == 6u) && (kKeyTable[0].source == ST_IDLE) &&
          (kKeyTable[5].action == Act_CountTick),
          "const table intact");

    printf("test_fsm_framework: %d/%d passed\n", g_pass, g_total);
    return (g_fail == 0) ? 0 : 1;
}
