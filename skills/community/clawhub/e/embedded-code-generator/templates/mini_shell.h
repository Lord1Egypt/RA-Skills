/**
 * @file mini_shell.h
 * @brief Table-driven command shell parser for UART/console lines.
 *
 * Parses one command line ("led on 3") into argc/argv and dispatches
 * to a registered handler via a const command table. Pure parsing
 * layer: it neither reads the UART nor prints anything — wire it to
 * your own line assembler (e.g., ring buffer + line terminator) and
 * reply channel (printf, rt_kprintf, CDC, ...).
 *
 * Parsing rules:
 *   - Tokens are separated by one or more spaces/tabs; leading and
 *     trailing blanks are ignored.
 *   - A trailing "\r\n" or "\n" is stripped. An empty (blank-only)
 *     line is silently ignored (SHELL_OK, nothing executed).
 *   - Command matching is case-sensitive (embed-friendly, no strlwr).
 *   - Quoted arguments are NOT supported (documented limitation).
 *   - argv points into the caller's line buffer, which is modified
 *     in place; keep it valid until the handler returns.
 *
 * Usage example:
 * @code
 *   static int cmd_led(int argc, char *argv[], char *reply, size_t rsz);
 *
 *   static const Shell_Cmd_t g_cmds[] = {
 *       { "led",   "led on|off",        cmd_led   },
 *       { "reboot","reboot the board",  cmd_reboot},
 *   };
 *
 *   void line_received(char *line) {   // "led on\r\n"
 *       char reply[64];
 *       if (Shell_Execute(&shell, line, reply, sizeof(reply)) == SHELL_OK
 *           && reply[0] != '\0') {
 *           printf("%s\n", reply);
 *       }
 *   }
 * @endcode
 */

#ifndef MINI_SHELL_H
#define MINI_SHELL_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ------------------------------------------------------------------ */
/* Configuration macros                                                */
/* ------------------------------------------------------------------ */

/** Maximum number of tokens (argc) on one line. */
#ifndef SHELL_MAX_ARGS
#define SHELL_MAX_ARGS  8
#endif

/** Maximum command name length (excluding NUL). */
#ifndef SHELL_MAX_NAME
#define SHELL_MAX_NAME  15u
#endif

/* ------------------------------------------------------------------ */
/* Return codes                                                        */
/* ------------------------------------------------------------------ */

#define SHELL_OK            0    /**< Executed (or blank line ignored). */
#define SHELL_ERR_PARAM    -1    /**< Invalid argument (NULL handle).   */
#define SHELL_ERR_NOT_FOUND -2   /**< Command not in table.             */
#define SHELL_ERR_TOO_MANY  -3   /**< More tokens than SHELL_MAX_ARGS.  */
#define SHELL_ERR_HANDLER   -4   /**< Handler returned negative.        */

/* ------------------------------------------------------------------ */
/* Types                                                               */
/* ------------------------------------------------------------------ */

/**
 * @brief Command handler.
 *
 * @param argc  Token count (>= 1; argv[0] is the command name).
 * @param argv  Token pointers into the caller's line buffer.
 * @param reply Output buffer for a human-readable reply (may be NULL;
 *              write "" if nothing to say — do not assume it is empty).
 * @param rsz   Size of the reply buffer (0 if reply is NULL).
 * @return 0 or positive on success, negative on failure (the negative
 *         value is propagated as SHELL_ERR_HANDLER + (code + 1)).
 */
typedef int (*Shell_Handler_t)(int argc, char *argv[], char *reply, size_t rsz);

/** One command table entry (build the table as const/flash-resident). */
typedef struct {
    const char *name;   /**< Command word, case-sensitive, NUL-terminated. */
    const char *help;   /**< Short help text.                              */
    Shell_Handler_t handler;
} Shell_Cmd_t;

/** Shell instance (binds a command table; stateless otherwise). */
typedef struct {
    const Shell_Cmd_t *cmds;
    size_t count;
} Shell_Handle_t;

/* ------------------------------------------------------------------ */
/* API                                                                 */
/* ------------------------------------------------------------------ */

/**
 * @brief Bind a shell instance to a command table.
 * @return SHELL_OK or SHELL_ERR_PARAM.
 */
int Shell_Init(Shell_Handle_t *h, const Shell_Cmd_t *cmds, size_t count);

/**
 * @brief Parse and execute one command line (destructive parse).
 *
 * The line buffer is tokenized in place (NULs written between tokens);
 * trailing CR/LF is ignored. On success, @p reply receives whatever
 * the handler wrote (always NUL-terminated; "" if handler stays quiet
 * or reply is NULL).
 *
 * @return SHELL_OK, SHELL_ERR_PARAM, SHELL_ERR_NOT_FOUND,
 *         SHELL_ERR_TOO_MANY, or SHELL_ERR_HANDLER (+ handler code).
 */
int Shell_Execute(Shell_Handle_t *h, char *line, char *reply, size_t rsz);

/**
 * @brief Look up a command without executing it.
 * @return Index into the table, or -1 if not found.
 */
int Shell_Find(const Shell_Handle_t *h, const char *name);

#ifdef __cplusplus
}
#endif

#endif /* MINI_SHELL_H */
