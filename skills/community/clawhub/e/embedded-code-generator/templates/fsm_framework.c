/**
 * @file fsm_framework.c
 * @brief Table-driven FSM engine: guard chaining, entry/exit callbacks.
 *
 * Complexity is O(count) per dispatch — fine for typical tables of a few
 * dozen rules. Keep hot machines' tables short or order rules by
 * frequency if dispatch time matters.
 */

#include "fsm_framework.h"

/* ------------------------------------------------------------------ */
/* Internal helpers                                                    */
/* ------------------------------------------------------------------ */

/** Find the first rule for (state, ev) at or after start_index. */
static int fsm_find_rule(const FSM_Machine_t *m,
                         FSM_State_t state, FSM_Event_t ev,
                         uint16_t start_index)
{
    uint16_t i;

    if ((m->cfg == NULL) || (m->cfg->table == NULL))
    {
        return -1;
    }

    for (i = start_index; i < m->cfg->count; i++)
    {
        const FSM_Transition_t *t = &m->cfg->table[i];

        if ((t->source == state) && (t->event == ev))
        {
            return (int)i;
        }
    }
    return -1;
}

/* ------------------------------------------------------------------ */
/* Public API                                                          */
/* ------------------------------------------------------------------ */

int FSM_Init(FSM_Machine_t *m, const FSM_Config_t *cfg)
{
    if ((m == NULL) || (cfg == NULL))
    {
        return FSM_ERR_PARAM;
    }

    m->cfg         = cfg;
    m->state       = cfg->initial;
    m->transitions = 0u;
    m->inited      = 1u;

    if (cfg->on_entry != NULL)
    {
        cfg->on_entry(m, 0u);   /* no event context on initial entry */
    }

    return FSM_OK;
}

int FSM_Dispatch(FSM_Machine_t *m, FSM_Event_t ev)
{
    uint16_t          search_from = 0u;
    bool              rule_found  = false;
    FSM_State_t       old_state;
    const FSM_Config_t *cfg;

    if ((m == NULL) || (m->inited == 0u))
    {
        return FSM_ERR_PARAM;
    }

    cfg = m->cfg;
    old_state = m->state;

    /* Scan matching rules; guards may chain several entries for the
     * same (state, event) pair — first passing guard wins. */
    for (;;)
    {
        int idx = fsm_find_rule(m, old_state, ev, search_from);

        if (idx < 0)
        {
            break;      /* no more candidate rules */
        }

        rule_found = true;

        {
            const FSM_Transition_t *t = &cfg->table[idx];

            if ((t->guard == NULL) || t->guard(m, ev))
            {
                /* Taken: exit old -> action -> enter new. */
                if (cfg->on_exit != NULL)
                {
                    cfg->on_exit(m, ev);
                }
                if (t->action != NULL)
                {
                    t->action(m, ev);
                }

                m->state = t->target;
                m->transitions++;

                if (cfg->on_entry != NULL)
                {
                    cfg->on_entry(m, ev);
                }
                return FSM_OK;
            }
        }

        search_from = (uint16_t)(idx + 1u);
    }

    return rule_found ? FSM_ERR_GUARD : FSM_ERR_NO_TRANS;
}

FSM_State_t FSM_GetState(const FSM_Machine_t *m)
{
    if (m == NULL)
    {
        return FSM_STATE_NONE;
    }
    return m->state;
}

int FSM_Reset(FSM_Machine_t *m)
{
    if ((m == NULL) || (m->inited == 0u))
    {
        return FSM_ERR_PARAM;
    }

    if ((m->cfg->on_exit != NULL) && (m->state != m->cfg->initial))
    {
        m->cfg->on_exit(m, 0u);
    }

    m->state = m->cfg->initial;

    if (m->cfg->on_entry != NULL)
    {
        m->cfg->on_entry(m, 0u);
    }

    return FSM_OK;
}
