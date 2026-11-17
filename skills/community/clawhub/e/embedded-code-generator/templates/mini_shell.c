/**
 * @file mini_shell.c
 * @brief Table-driven command shell parser for UART/console lines.
 *
 * See mini_shell.h for the full design contract.
 */

#include <string.h>
#include "mini_shell.h"

int Shell_Init(Shell_Handle_t *h, const Shell_Cmd_t *cmds, size_t count)
{
    size_t i;

    if ((h == NULL) || (cmds == NULL) || (count == 0u)) {
        return SHELL_ERR_PARAM;
    }
    /* Fail fast on malformed tables: every entry needs name+handler. */
    for (i = 0u; i < count; i++) {
        if ((cmds[i].name == NULL) || (cmds[i].name[0] == '\0') ||
            (cmds[i].handler == NULL)) {
            return SHELL_ERR_PARAM;
        }
    }
    h->cmds  = cmds;
    h->count = count;
    return SHELL_OK;
}

int Shell_Find(const Shell_Handle_t *h, const char *name)
{
    size_t i;

    if ((h == NULL) || (name == NULL)) {
        return -1;
    }
    for (i = 0u; i < h->count; i++) {
        if (strcmp(h->cmds[i].name, name) == 0) {
            return (int)i;
        }
    }
    return -1;
}

/* Is this char a token separator? */
static bool is_blank(char c)
{
    return (c == ' ') || (c == '\t');
}

int Shell_Execute(Shell_Handle_t *h, char *line, char *reply, size_t rsz)
{
    char *argv[SHELL_MAX_ARGS];
    int argc = 0;
    int idx;
    int rc;

    if ((h == NULL) || (line == NULL)) {
        return SHELL_ERR_PARAM;
    }
    if (reply != NULL && rsz > 0u) {
        reply[0] = '\0';
    }

    /* Strip trailing CR/LF (tolerates "cmd\r\n", "cmd\n", "cmd"). */
    {
        size_t len = strlen(line);
        while ((len > 0u) &&
               ((line[len - 1u] == '\n') || (line[len - 1u] == '\r'))) {
            line[--len] = '\0';
        }
    }

    /* Tokenize in place. */
    {
        char *p = line;
        while (*p != '\0') {
            while (is_blank(*p)) {
                p++;
            }
            if (*p == '\0') {
                break;
            }
            if (argc >= SHELL_MAX_ARGS) {
                return SHELL_ERR_TOO_MANY;
            }
            argv[argc++] = p;
            while ((*p != '\0') && !is_blank(*p)) {
                p++;
            }
            if (*p != '\0') {
                *p++ = '\0';
            }
        }
    }

    if (argc == 0) {
        return SHELL_OK;   /* blank line: ignore silently */
    }

    idx = Shell_Find(h, argv[0]);
    if (idx < 0) {
        return SHELL_ERR_NOT_FOUND;
    }

    rc = h->cmds[idx].handler(argc, argv, reply, rsz);
    if (rc < 0) {
        /* Propagate the handler code below the SHELL_ERR_* range:
         * rc=-N maps to -(N+3), e.g. rc=-42 -> -45.  rc in [-1000, -1]
         * keeps the subtraction overflow-free; pathological magnitudes
         * clamp to SHELL_ERR_HANDLER. */
        if (rc > -1001) {
            return rc - 3;
        }
        return SHELL_ERR_HANDLER;
    }
    return SHELL_OK;
}
