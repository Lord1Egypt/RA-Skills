/**
 * @file test_mini_shell.c
 * @brief Self-check tests for mini_shell.c (command parser).
 *
 * Run via `make test` from the skill package root. Exit code: number
 * of failed checks (0 = all pass).
 */

#include <stdio.h>
#include <string.h>
#include "mini_shell.h"

static int g_failed = 0;
static int g_total  = 0;

#define CHECK(desc, expr)                                          \
    do {                                                           \
        g_total++;                                                 \
        if (expr) {                                                \
            printf("[PASS] %s\n", (desc));                         \
        } else {                                                   \
            g_failed++;                                            \
            printf("[FAIL] %s  (at line %d)\n", (desc), __LINE__); \
        }                                                          \
    } while (0)

/* --- test handlers ------------------------------------------------- */

static int g_argc;
static char g_arg0[16];
static char g_arg1[16];
static char g_arg2[16];
static int g_rc_next;

static int cmd_capture(int argc, char *argv[], char *reply, size_t rsz)
{
    g_argc = argc;
    snprintf(g_arg0, sizeof(g_arg0), "%s", argv[0]);
    snprintf(g_arg1, sizeof(g_arg1), "%s", (argc > 1) ? argv[1] : "");
    snprintf(g_arg2, sizeof(g_arg2), "%s", (argc > 2) ? argv[2] : "");
    if ((reply != NULL) && (rsz > 0u)) {
        snprintf(reply, rsz, "ok=%s", argv[0]);
    }
    return g_rc_next;
}

static int cmd_fail42(int argc, char *argv[], char *reply, size_t rsz)
{
    (void)argc; (void)argv; (void)reply; (void)rsz;
    return -42;
}

static const Shell_Cmd_t g_cmds[] = {
    { "led",    "led on|off",  cmd_capture },
    { "fail",   "always -42",  cmd_fail42  },
    { "reboot", "reboot",      cmd_capture },
};
static Shell_Handle_t shell;

/* Shell_Execute parses destructively; wrap literals in a writable
 * buffer exactly like a UART line assembler would provide. */
static char *wr(const char *s)
{
    static char buf[96];
    snprintf(buf, sizeof(buf), "%s", s);
    return buf;
}

static void reset_all(void)
{
    (void)Shell_Init(&shell, g_cmds, 3u);
    g_argc = -1;
    g_arg0[0] = g_arg1[0] = g_arg2[0] = '\0';
    g_rc_next = 0;
}

static void test_basic(void)
{
    char reply[64];

    reset_all();
    CHECK("Init: OK on valid table", Shell_Init(&shell, g_cmds, 3u) == SHELL_OK);
    CHECK("Init: rejects NULL table", Shell_Init(&shell, NULL, 3u) == SHELL_ERR_PARAM);
    CHECK("Init: rejects zero count", Shell_Init(&shell, g_cmds, 0u) == SHELL_ERR_PARAM);

    CHECK("Run: simple command OK",
          Shell_Execute(&shell, wr("led on"), reply, sizeof(reply)) == SHELL_OK);
    CHECK("Run: argc == 2", g_argc == 2);
    CHECK("Run: argv[0] is command name", strcmp(g_arg0, "led") == 0);
    CHECK("Run: argv[1] is first arg", strcmp(g_arg1, "on") == 0);
    CHECK("Run: reply written by handler", strcmp(reply, "ok=led") == 0);
}

static void test_parsing(void)
{
    char reply[64];

    reset_all();
    (void)Shell_Execute(&shell, wr("  led \t on   3  \r\n"), reply, sizeof(reply));
    CHECK("Parse: blanks and CRLF tolerated", (g_argc == 3) &&
          (strcmp(g_arg1, "on") == 0) && (strcmp(g_arg2, "3") == 0));

    (void)Shell_Execute(&shell, wr("led\n"), reply, sizeof(reply));
    CHECK("Parse: bare LF stripped, single token", (g_argc == 1));

    CHECK("Parse: blank line ignored (SHELL_OK)",
          Shell_Execute(&shell, wr("   \t \r\n"), reply, sizeof(reply)) == SHELL_OK);
    CHECK("Parse: empty string ignored",
          Shell_Execute(&shell, wr(""), reply, sizeof(reply)) == SHELL_OK);

    CHECK("Parse: case-sensitive lookup fails on LED",
          Shell_Execute(&shell, wr("LED on"), reply, sizeof(reply)) == SHELL_ERR_NOT_FOUND);
    CHECK("Parse: prefix match does not fire (ledx)",
          Shell_Execute(&shell, wr("ledx"), reply, sizeof(reply)) == SHELL_ERR_NOT_FOUND);
}

static void test_errors(void)
{
    char reply[64];

    reset_all();
    CHECK("Err: unknown command", Shell_Execute(&shell, wr("nope x"), reply, sizeof(reply)) == SHELL_ERR_NOT_FOUND);

    g_rc_next = -42;
    CHECK("Err: handler negative propagated",
          Shell_Execute(&shell, wr("fail"), reply, sizeof(reply)) ==
          (SHELL_ERR_HANDLER + (-42) + 1));
    g_rc_next = 0;

    CHECK("Err: NULL line rejected",
          Shell_Execute(&shell, NULL, reply, sizeof(reply)) == SHELL_ERR_PARAM);
    CHECK("Err: NULL handle rejected",
          Shell_Execute(NULL, wr("led"), reply, sizeof(reply)) == SHELL_ERR_PARAM);
}

static void test_reply_safety(void)
{
    char tiny[4];
    char reply[64];

    reset_all();
    CHECK("Reply: NULL reply buffer allowed",
          Shell_Execute(&shell, wr("led on"), NULL, 0u) == SHELL_OK);
    CHECK("Reply: zero-size reply allowed",
          Shell_Execute(&shell, wr("led on"), reply, 0u) == SHELL_OK);

    (void)Shell_Execute(&shell, wr("reboot now"), tiny, sizeof(tiny));
    CHECK("Reply: tiny buffer NUL-terminated & truncated",
          (strlen(tiny) < sizeof(tiny)) && (strncmp(tiny, "ok=", 3u) == 0));
}

static void test_find(void)
{
    reset_all();
    CHECK("Find: existing command found", Shell_Find(&shell, "led") == 0);
    CHECK("Find: second entry index", Shell_Find(&shell, "reboot") == 2);
    CHECK("Find: missing returns -1", Shell_Find(&shell, "nope") == -1);
    CHECK("Find: NULL name returns -1", Shell_Find(&shell, NULL) == -1);
}

int main(void)
{
    test_basic();
    test_parsing();
    test_errors();
    test_reply_safety();
    test_find();

    printf("Summary: %d checks, %d passed, %d failed\n",
           g_total, g_total - g_failed, g_failed);
    if (g_failed > 0) {
        printf("=== TESTS FAILED ===\n");
        return g_failed;
    }
    printf("=== ALL TESTS PASSED ===\n");
    return 0;
}
